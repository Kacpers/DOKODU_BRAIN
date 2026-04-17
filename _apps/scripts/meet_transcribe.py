#!/usr/bin/env python3
"""
Meet Transcribe — DOKODU BRAIN
Pobiera nagrania z Google Meet (Drive), paruje z Calendar, transkrybuje Whisper.

Pipeline:
  1. Google Drive API → pobierz nowe MP4 z "Meet Recordings"
  2. Google Calendar API → sparuj po timestamp (±30 min)
  3. ffmpeg → wyciągnij audio (WAV)
  4. Whisper → transkrypcja PL
  5. Zapisz MD do meetings_transcripts/
  6. Usuń: lokalne pliki + plik na Drive

Użycie:
  python3 meet_transcribe.py                  # wszystkie nowe nagrania
  python3 meet_transcribe.py --latest         # tylko najnowsze
  python3 meet_transcribe.py --model small    # szybszy model
  python3 meet_transcribe.py --keep-drive     # nie usuwaj z Drive
  python3 meet_transcribe.py --dry-run        # pokaż co zrobi, bez akcji

Auth (jednorazowo):
  python3 meet_auth.py
"""

import argparse
import os
import pickle
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

BRAIN_DIR = Path(__file__).parent.parent
TRANSCRIPTS_DIR = BRAIN_DIR / "meetings_transcripts"
TOKEN_PATH = Path.home() / ".config" / "dokodu" / "meet_token.pickle"
PROCESSED_FILE = TRANSCRIPTS_DIR / ".processed_ids"


def get_credentials():
    if not TOKEN_PATH.exists():
        print("ERROR: Brak tokenu. Uruchom najpierw: python3 meet_auth.py")
        sys.exit(1)

    with open(TOKEN_PATH, "rb") as f:
        creds = pickle.load(f)

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_PATH, "wb") as f:
            pickle.dump(creds, f)

    return creds


def get_processed_ids():
    if not PROCESSED_FILE.exists():
        return set()
    return set(PROCESSED_FILE.read_text().strip().splitlines())


def save_processed_id(file_id):
    with open(PROCESSED_FILE, "a") as f:
        f.write(file_id + "\n")


def find_meet_recordings(drive_service, only_latest=False):
    """Znajdź nagrania Meet na Google Drive."""
    query = "mimeType='video/mp4' and trashed=false"

    # Szukaj w folderze Meet Recordings lub po nazwie
    # Google Meet zapisuje pliki z nazwą zawierającą datę
    results = drive_service.files().list(
        q=query,
        spaces="drive",
        fields="files(id, name, createdTime, modifiedTime, parents, size)",
        orderBy="createdTime desc",
        pageSize=50,
    ).execute()

    files = results.get("files", [])

    # Filtruj — Meet recordings mają charakterystyczną nazwę
    # np. "GMT20260414-070000 - Recording" lub nazwa spotkania
    meet_files = []
    for f in files:
        name = f["name"].lower()
        if any(kw in name for kw in ["recording", "nagranie", "meet", "gmt"]):
            meet_files.append(f)

    # Filtruj już przetworzone
    processed = get_processed_ids()
    meet_files = [f for f in meet_files if f["id"] not in processed]

    if only_latest and meet_files:
        meet_files = [meet_files[0]]

    return meet_files


def match_calendar_event(cal_service, file_created_time):
    """Znajdź event w kalendarzu pasujący do czasu nagrania (±30 min)."""
    created_dt = datetime.fromisoformat(file_created_time.replace("Z", "+00:00"))

    # Szukaj eventów w oknie ±2h od czasu utworzenia pliku
    time_min = (created_dt - timedelta(hours=2)).isoformat()
    time_max = (created_dt + timedelta(hours=2)).isoformat()

    events_result = cal_service.events().list(
        calendarId="primary",
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy="startTime",
        timeZone="Europe/Warsaw",
    ).execute()

    events = events_result.get("items", [])
    if not events:
        return None

    # Znajdź najbliższy event (po czasie rozpoczęcia)
    best_match = None
    best_diff = timedelta(hours=99)

    for event in events:
        start = event.get("start", {})
        start_str = start.get("dateTime", start.get("date", ""))
        if not start_str or "T" not in start_str:
            continue

        event_dt = datetime.fromisoformat(start_str)
        # Normalizuj do UTC-aware jeśli trzeba
        if event_dt.tzinfo and created_dt.tzinfo:
            diff = abs(event_dt - created_dt)
        else:
            # Porównaj naiwnie
            diff = abs(event_dt.replace(tzinfo=None) - created_dt.replace(tzinfo=None))

        if diff < best_diff:
            best_diff = diff
            best_match = event

    # Akceptuj match tylko jeśli ±60 min
    if best_match and best_diff <= timedelta(minutes=60):
        return best_match

    return None


def download_file(drive_service, file_id, dest_path):
    """Pobierz plik z Google Drive."""
    request = drive_service.files().get_media(fileId=file_id)

    with open(dest_path, "wb") as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            if status:
                pct = int(status.progress() * 100)
                print(f"    Pobieranie: {pct}%", end="\r")
    print(f"    Pobieranie: 100%")


def extract_audio(video_path, audio_path):
    """Wyciągnij audio z MP4 przez ffmpeg."""
    cmd = [
        "ffmpeg", "-i", str(video_path),
        "-vn", "-acodec", "pcm_s16le",
        "-ar", "16000", "-ac", "1",
        str(audio_path),
        "-y", "-loglevel", "error",
    ]
    subprocess.run(cmd, check=True)


def transcribe_audio(audio_path, model_name="medium"):
    """Transkrybuj audio przez Whisper."""
    import whisper

    print(f"    Ładuję model Whisper ({model_name})...")
    model = whisper.load_model(model_name)

    print(f"    Transkrybuję... (może potrwać kilka minut)")
    result = model.transcribe(str(audio_path), language="pl", verbose=False)

    segments = result["segments"]
    text = " ".join(seg["text"].strip() for seg in segments)
    return text, segments


def format_transcript_md(file_info, event, transcript, segments):
    """Sformatuj transkrypcję jako Markdown."""
    created = datetime.fromisoformat(file_info["createdTime"].replace("Z", "+00:00"))
    date_str = created.strftime("%Y-%m-%d")

    if event:
        title = event.get("summary", "Spotkanie")
        start = event.get("start", {})
        end = event.get("end", {})
        start_time = ""
        end_time = ""

        if "dateTime" in start:
            start_dt = datetime.fromisoformat(start["dateTime"])
            start_time = start_dt.strftime("%H:%M")
        if "dateTime" in end:
            end_dt = datetime.fromisoformat(end["dateTime"])
            end_time = end_dt.strftime("%H:%M")

        time_range = f"{start_time}–{end_time}" if start_time and end_time else ""

        attendees = event.get("attendees", [])
        attendee_emails = [a.get("email", "") for a in attendees if a.get("email")]
    else:
        title = file_info["name"].replace(".mp4", "").replace("_", " ")
        # Wyczyść nazwy typu "GMT20260414-070000 - Recording"
        title = re.sub(r"GMT\d{8}-\d{6}\s*-?\s*", "", title).strip()
        if not title:
            title = "Spotkanie bez nazwy"
        time_range = created.strftime("%H:%M")
        attendee_emails = []

    # Bezpieczna nazwa pliku
    safe_title = re.sub(r"[^\w\s-]", "", title).strip().replace(" ", "-")[:60]
    filename = f"{date_str}_{safe_title}.md"

    # Czas trwania na podstawie segmentów
    duration_min = ""
    if segments:
        last_seg = segments[-1]
        duration_min = f" (~{int(last_seg['end'] / 60)} min)"

    # YAML frontmatter
    attendees_yaml = "\n".join(f'  - "{e}"' for e in attendee_emails)
    if not attendees_yaml:
        attendees_yaml = "  []"

    md = f"""---
date: {date_str}
time: "{time_range}"
event: "{title}"
attendees:
{attendees_yaml}
source: meet_recording
---

# {title}
**Data:** {date_str} {time_range}{duration_min}
"""

    if attendee_emails:
        md += f"**Uczestnicy:** {', '.join(attendee_emails)}\n"

    md += f"""
---

## Transkrypcja

{transcript}
"""

    return filename, md


def delete_from_drive(drive_service, file_id):
    """Usuń plik z Google Drive."""
    drive_service.files().delete(fileId=file_id).execute()


def main():
    parser = argparse.ArgumentParser(description="Meet Transcribe — DOKODU BRAIN")
    parser.add_argument("--latest", action="store_true", help="Tylko najnowsze nagranie")
    parser.add_argument("--model", default="medium", choices=["tiny", "base", "small", "medium", "large"],
                        help="Model Whisper (domyślnie: medium)")
    parser.add_argument("--keep-drive", action="store_true", help="Nie usuwaj nagrania z Drive")
    parser.add_argument("--dry-run", action="store_true", help="Pokaż co zrobi, bez akcji")
    args = parser.parse_args()

    print(f"\n{'=' * 50}")
    print(f"Meet Transcribe — DOKODU BRAIN")
    print(f"{'=' * 50}\n")

    # Auth
    creds = get_credentials()
    drive_service = build("drive", "v3", credentials=creds)
    cal_service = build("calendar", "v3", credentials=creds)

    # Znajdź nagrania
    print("  Szukam nagrań Meet na Drive...")
    recordings = find_meet_recordings(drive_service, only_latest=args.latest)

    if not recordings:
        print("  Brak nowych nagrań do przetworzenia.")
        return

    print(f"  Znaleziono {len(recordings)} nowych nagrań.\n")

    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

    for i, rec in enumerate(recordings, 1):
        print(f"  [{i}/{len(recordings)}] {rec['name']}")
        size_mb = int(rec.get("size", 0)) / (1024 * 1024)
        print(f"    Rozmiar: {size_mb:.1f} MB")

        # Paruj z kalendarzem
        event = match_calendar_event(cal_service, rec["createdTime"])
        if event:
            print(f"    📅 Sparowano: {event.get('summary', '?')}")
            attendees = event.get("attendees", [])
            if attendees:
                emails = [a.get("email", "") for a in attendees[:3]]
                print(f"    👥 Uczestnicy: {', '.join(emails)}")
        else:
            print(f"    ⚠️  Brak pasującego eventu w kalendarzu")

        if args.dry_run:
            print(f"    [DRY RUN] Pomijam pobieranie i transkrypcję.\n")
            continue

        # Pobierz do tymczasowego katalogu
        with tempfile.TemporaryDirectory() as tmpdir:
            video_path = Path(tmpdir) / "recording.mp4"
            audio_path = Path(tmpdir) / "recording.wav"

            # Pobierz MP4
            print(f"    ⬇️  Pobieram z Drive...")
            download_file(drive_service, rec["id"], video_path)

            # Wyciągnij audio
            print(f"    🔊 Wyciągam audio (ffmpeg)...")
            extract_audio(video_path, audio_path)

            # Usuń video od razu (oszczędność miejsca)
            video_path.unlink()

            # Transkrybuj
            print(f"    🎙️  Whisper ({args.model})...")
            transcript, segments = transcribe_audio(audio_path, args.model)

            # Sformatuj i zapisz
            filename, md_content = format_transcript_md(rec, event, transcript, segments)
            output_path = TRANSCRIPTS_DIR / filename

            # Unikaj nadpisywania
            if output_path.exists():
                stem = output_path.stem
                for n in range(2, 100):
                    candidate = TRANSCRIPTS_DIR / f"{stem}_{n}.md"
                    if not candidate.exists():
                        output_path = candidate
                        break

            output_path.write_text(md_content, encoding="utf-8")
            print(f"    ✅ Zapisano: {output_path.name}")

            # Oznacz jako przetworzony
            save_processed_id(rec["id"])

        # Usuń z Drive
        if not args.keep_drive:
            print(f"    🗑️  Usuwam z Drive...")
            try:
                delete_from_drive(drive_service, rec["id"])
                print(f"    ✅ Usunięto z Drive")
            except Exception as e:
                print(f"    ⚠️  Nie udało się usunąć z Drive: {e}")

        print()

    print(f"{'=' * 50}")
    print(f"Gotowe! Transkrypcje w: {TRANSCRIPTS_DIR}")
    print()
    print("Następne kroki:")
    print("  • Przejrzyj transkrypcję i promptuj co potrzebujesz")
    print("  • /brain-meeting-notes — przetwórz do profilu klienta")
    print("  • 'Wyciągnij wymagania z tego spotkania' — specyfikacja")
    print()


if __name__ == "__main__":
    main()
