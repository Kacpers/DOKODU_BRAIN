#!/usr/bin/env python3
"""
DOKODU BRAIN — Whisper Transcribe
Transkrybuje nagranie wideo/audio i generuje:
  - transkrypcja.txt     (surowy tekst, baza do blog posta)
  - napisy.srt           (napisy do DaVinci Resolve / YouTube)
  - chapters_template.md (template chapters z placeholderami na czas)
  - linkedin_post.txt    (gotowy post do wklejenia na LinkedIn)

Wyniki trafiają do: BRAIN/movies/YT-XXX/publish/

Użycie:
  python3 whisper_transcribe.py YT-002 --file /ścieżka/do/nagrania.mp4
  python3 whisper_transcribe.py YT-002 --file nagranie.mp4 --model medium
  python3 whisper_transcribe.py YT-002 --file nagranie.mp4 --no-linkedin

Modele (jakość vs szybkość):
  tiny    — najszybszy, mniej dokładny
  base    — dobry balans dla testów
  small   — zalecany dla PL
  medium  — najlepsza jakość PL (domyślny)
  large   — najwolniejszy, najdokładniejszy
"""

import sys
import re
import json
import argparse
from pathlib import Path
from datetime import timedelta

BRAIN_DIR  = Path(__file__).parent.parent
MOVIES_DIR = BRAIN_DIR / "30_RESOURCES" / "RES_YouTube" / "movies"


# ══════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════

def format_srt_time(seconds: float) -> str:
    td = timedelta(seconds=seconds)
    total_s = int(td.total_seconds())
    ms = int((td.total_seconds() - total_s) * 1000)
    h = total_s // 3600
    m = (total_s % 3600) // 60
    s = total_s % 60
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def segments_to_srt(segments) -> str:
    lines = []
    for i, seg in enumerate(segments, 1):
        start = format_srt_time(seg.start)
        end   = format_srt_time(seg.end)
        text  = seg.text.strip()
        lines.append(f"{i}\n{start} --> {end}\n{text}\n")
    return "\n".join(lines)


def segments_to_txt(segments) -> str:
    return " ".join(seg.text.strip() for seg in segments)


def parse_metadata(video_id: str) -> dict:
    meta_file = MOVIES_DIR / video_id / "metadata.md"
    if not meta_file.exists():
        return {"title": video_id, "id": video_id}
    text = meta_file.read_text(encoding="utf-8")
    m = re.search(r"^#\s+(?:YT-\d+\s+—\s+)?(.+)$", text, re.MULTILINE)
    title = m.group(1).strip() if m else video_id
    return {"title": title, "id": video_id}


def build_chapters_template(video_id: str, segments) -> str:
    """Generuje template chapters na podstawie scenariusza.md (sekcje ## )."""
    script_file = MOVIES_DIR / video_id / "scenariusz.md"
    lines = [
        f"# Chapters template — {video_id}",
        "# Uzupełnij czasy po obejrzeniu nagrania\n",
        "## Do wklejenia w opisie YouTube:",
        "",
    ]

    if script_file.exists():
        text = script_file.read_text(encoding="utf-8")
        sections = re.findall(r"^##\s+(.+)$", text, re.MULTILINE)
        for section in sections:
            # Usuń znaczniki czasu jeśli są (np. "(0:00–0:40)")
            clean = re.sub(r"\s*\(\d+:\d+[–-]\d+:\d+\)", "", section).strip()
            lines.append(f"0:00 {clean}")
    else:
        lines.append("0:00 Intro")
        lines.append("# Brak scenariusza.md — uzupełnij sekcje ręcznie")

    lines += [
        "",
        "---",
        "# Szacowane czasy na podstawie transkrypcji (co ~10 min):",
    ]
    checkpoints = [s for s in segments if s.start % 600 < 5]
    for seg in checkpoints[:10]:
        m_val = int(seg.start // 60)
        s_val = int(seg.start % 60)
        preview = seg.text.strip()[:60]
        lines.append(f"{m_val}:{s_val:02d} — \"{preview}...\"")

    return "\n".join(lines)


def build_linkedin_post(data: dict, transcript: str) -> str:
    """Generuje gotowy post LinkedIn na podstawie tytułu i transkrypcji."""
    title = data["title"]
    video_id = data["id"]

    # Pierwsze 500 znaków transkrypcji jako kontekst
    intro = transcript[:500].rsplit(" ", 1)[0] + "..."

    return f"""# POST LINKEDIN — {video_id}
# Wygenerowano automatycznie — przejrzyj i dostosuj przed publikacją
# ─────────────────────────────────────────

Właśnie opublikowałem nowy film: {title}

{intro}

Co znajdziesz w filmie:
→ [UZUPEŁNIJ — 3 główne punkty wartości]
→ [UZUPEŁNIJ]
→ [UZUPEŁNIJ]

Link w komentarzu (algorytm LinkedIn nie lubi linków w poście).

#AI #Automatyzacja #Python #AIwFirmie #GeminiCLI

─────────────────────────────────────────
💡 Wskazówka: dodaj link do YT w pierwszym komentarzu po publikacji
"""


# ══════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Whisper transkrypcja dla DOKODU BRAIN")
    parser.add_argument("video_id", help="ID filmu, np. YT-002")
    parser.add_argument("--file", required=True, help="Ścieżka do pliku audio/video")
    parser.add_argument("--model", default="medium", choices=["tiny", "base", "small", "medium", "large"],
                        help="Model Whisper (domyślnie: medium)")
    parser.add_argument("--no-linkedin", action="store_true", help="Pomiń generowanie posta LinkedIn")
    args = parser.parse_args()

    video_id = args.video_id.upper() if args.video_id.upper().startswith("YT-") else f"YT-{args.video_id}"
    audio_file = Path(args.file)

    if not audio_file.exists():
        print(f"ERROR: Plik nie istnieje: {audio_file}")
        sys.exit(1)

    print(f"\n{'='*50}")
    print(f"Whisper Transcribe — {video_id}")
    print(f"{'='*50}\n")

    # Import whisper
    try:
        import whisper
    except ImportError:
        print("ERROR: Brak biblioteki whisper.")
        print("Zainstaluj: pip3 install openai-whisper")
        print("Wymagany też: sudo apt-get install ffmpeg")
        sys.exit(1)

    # Output dir
    publish_dir = MOVIES_DIR / video_id / "publish"
    publish_dir.mkdir(parents=True, exist_ok=True)

    data = parse_metadata(video_id)
    print(f"  Film: {data['title']}")
    print(f"  Plik: {audio_file.name}")
    print(f"  Model: {args.model}\n")

    # Transkrypcja
    print(f"  Ładuję model {args.model}...")
    model = whisper.load_model(args.model)

    print(f"  Transkrybuję... (może potrwać kilka minut)")
    result = model.transcribe(str(audio_file), language="pl", verbose=False)
    segments = result["segments"]
    print(f"  ✓ Transkrypcja gotowa — {len(segments)} segmentów\n")

    # 1. Surowy tekst
    txt_content = segments_to_txt(segments)
    (publish_dir / "transkrypcja.txt").write_text(txt_content, encoding="utf-8")
    print(f"  ✓ transkrypcja.txt ({len(txt_content)} znaków)")

    # 2. SRT napisy
    srt_content = segments_to_srt(segments)
    (publish_dir / "napisy.srt").write_text(srt_content, encoding="utf-8")
    print(f"  ✓ napisy.srt ({len(segments)} segmentów)")

    # 3. Chapters template
    chapters = build_chapters_template(video_id, segments)
    (publish_dir / "chapters_template.md").write_text(chapters, encoding="utf-8")
    print(f"  ✓ chapters_template.md")

    # 4. LinkedIn post
    if not args.no_linkedin:
        linkedin = build_linkedin_post(data, txt_content)
        (publish_dir / "linkedin_post.txt").write_text(linkedin, encoding="utf-8")
        print(f"  ✓ linkedin_post.txt")

    print(f"\n{'='*50}")
    print(f"Gotowe! Pliki w:")
    print(f"  {publish_dir}")
    print()
    print("Następne kroki:")
    print("  1. Sprawdź transkrypcja.txt — czy jest poprawna")
    print("  2. Wgraj napisy.srt do DaVinci Resolve lub YouTube Studio")
    print("  3. Uzupełnij czasy w chapters_template.md")
    if not args.no_linkedin:
        print("  4. Przejrzyj linkedin_post.txt i wklej na LinkedIn")
    print()


if __name__ == "__main__":
    main()
