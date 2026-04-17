#!/usr/bin/env python3
"""
DOKODU BRAIN — TikTok Pipeline
Automatyczny post-production dla TikToków:
  1. Whisper transkrypcja z word-level timestamps
  2. Generowanie stylowanych napisów ASS (polskie znaki, word-by-word highlight)
  3. Auto-cięcie pauz (>0.8s ciszy)
  4. Renderowanie intro/outro (Remotion)
  5. FFmpeg: napisy burned-in + intro/outro concat
  6. Generowanie opisu + hashtagów

Użycie:
  # Pojedynczy klip:
  python3 tiktok_pipeline.py process video.mp4

  # Cały batch (folder z nagraniami):
  python3 tiktok_pipeline.py batch /path/to/raw_clips/

  # Tylko napisy (bez montażu):
  python3 tiktok_pipeline.py subtitles video.mp4

  # Generowanie scenariuszy (batch 10 do telepromptera):
  python3 tiktok_pipeline.py scenarios --count 10

Wymagania:
  pip3 install faster-whisper
  sudo apt-get install ffmpeg
  (opcjonalnie) npm install w remotion/
"""

import sys
import re
import json
import argparse
import subprocess
import shutil
from pathlib import Path
from datetime import timedelta
from typing import Optional

BRAIN_DIR = Path(__file__).parent.parent
REMOTION_DIR = BRAIN_DIR / "remotion"
TIKTOK_DIR = BRAIN_DIR / "20_AREAS" / "AREA_YouTube" / "tiktok_publish"
IDEAS_BANK = BRAIN_DIR / "20_AREAS" / "AREA_YouTube" / "TikTok_Ideas_Bank.md"
DROPBOX_DIR = Path.home() / "Dropbox" / "Apps" / "Parrot Teleprompter"

# Subtitle style config
ASS_STYLE = {
    "fontname": "Inter",
    "fontsize": 68,
    "primary_color": "&H00FFFFFF",      # White
    "highlight_color": "&H0000D2FF",    # Yellow (FFE135 → BGR)
    "outline_color": "&H00000000",      # Black outline
    "back_color": "&H80000000",         # Semi-transparent shadow
    "bold": -1,
    "outline": 4,
    "shadow": 2,
    "alignment": 5,                     # Center middle
    "margin_v": 520,                    # Push below face area
    "max_words_per_line": 4,
}


# ══════════════════════════════════════════════
# ASS SUBTITLE GENERATION
# ══════════════════════════════════════════════

def format_ass_time(seconds: float) -> str:
    """Format seconds to ASS time: H:MM:SS.CC"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int((seconds - int(seconds)) * 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def generate_ass_header() -> str:
    """Generate ASS file header with TikTok-optimized styling."""
    s = ASS_STYLE
    return f"""[Script Info]
Title: TikTok Subtitles — Dokodu
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{s['fontname']},{s['fontsize']},{s['primary_color']},{s['highlight_color']},{s['outline_color']},{s['back_color']},{s['bold']},0,0,0,100,100,0,0,1,{s['outline']},{s['shadow']},{s['alignment']},40,40,{s['margin_v']},1
Style: Highlight,{s['fontname']},{s['fontsize']},{s['highlight_color']},{s['primary_color']},{s['outline_color']},{s['back_color']},{s['bold']},0,0,0,100,100,0,0,1,{s['outline']},{s['shadow']},{s['alignment']},40,40,{s['margin_v']},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def words_to_ass_events(words: list, max_per_line: int = 4) -> str:
    """
    Convert word-level timestamps to ASS dialogue events.
    Groups words into chunks of max_per_line, highlights current word.
    """
    lines = []
    chunks = []

    # Group words into display chunks
    current_chunk = []
    for w in words:
        current_chunk.append(w)
        if len(current_chunk) >= max_per_line:
            chunks.append(current_chunk)
            current_chunk = []
    if current_chunk:
        chunks.append(current_chunk)

    for chunk in chunks:
        start = chunk[0]["start"]
        end = chunk[-1]["end"]

        # Build karaoke-style text with word-by-word highlight
        # Each word gets highlighted when it's spoken
        parts = []
        for i, word in enumerate(chunk):
            word_start = word["start"] - start
            duration_cs = int((word["end"] - word["start"]) * 100)
            # Gap before this word (if any)
            if i > 0:
                gap = word["start"] - chunk[i - 1]["end"]
                if gap > 0:
                    gap_cs = int(gap * 100)
                    parts.append(f"{{\\k{gap_cs}}}")
            elif word_start > 0:
                parts.append(f"{{\\k{int(word_start * 100)}}}")

            # The word itself with karaoke highlight
            parts.append(f"{{\\kf{duration_cs}}}{word['word']}")

        text = "".join(parts)
        start_t = format_ass_time(start)
        end_t = format_ass_time(end + 0.1)  # Small buffer
        lines.append(f"Dialogue: 0,{start_t},{end_t},Default,,0,0,0,,{text}")

    return "\n".join(lines)


def generate_ass_subtitles(words: list, output_path: Path) -> None:
    """Generate complete ASS subtitle file from word timestamps."""
    header = generate_ass_header()
    events = words_to_ass_events(words, ASS_STYLE["max_words_per_line"])
    content = header + events + "\n"
    output_path.write_text(content, encoding="utf-8")


# ══════════════════════════════════════════════
# WHISPER TRANSCRIPTION
# ══════════════════════════════════════════════

def transcribe_with_words(audio_path: Path, model_size: str = "medium") -> dict:
    """Transcribe audio and return word-level timestamps."""
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("ERROR: Brak faster-whisper. Instalacja:")
        print("  pip3 install faster-whisper")
        sys.exit(1)

    print(f"  Ładuję model {model_size}...")
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    print(f"  Transkrybuję z word timestamps...")
    segments, info = model.transcribe(
        str(audio_path),
        language="pl",
        word_timestamps=True,
        vad_filter=True,
    )

    all_words = []
    full_text = []
    for segment in segments:
        full_text.append(segment.text.strip())
        if segment.words:
            for word in segment.words:
                all_words.append({
                    "word": word.word.strip(),
                    "start": word.start,
                    "end": word.end,
                })

    result = {
        "text": " ".join(full_text),
        "words": all_words,
        "language": info.language,
        "duration": info.duration,
    }
    print(f"  ✓ {len(all_words)} słów, {info.duration:.1f}s")
    return result


# ══════════════════════════════════════════════
# SILENCE DETECTION & AUTO-CUT
# ══════════════════════════════════════════════

def detect_silences(words: list, threshold: float = 0.8) -> list:
    """Find silence gaps > threshold between words. Returns list of (start, end) to cut."""
    cuts = []
    for i in range(1, len(words)):
        gap = words[i]["start"] - words[i - 1]["end"]
        if gap > threshold:
            # Keep a small buffer (0.15s) on each side
            cut_start = words[i - 1]["end"] + 0.15
            cut_end = words[i]["start"] - 0.15
            if cut_end > cut_start:
                cuts.append((cut_start, cut_end))
    return cuts


def build_ffmpeg_trim_filter(duration: float, silences: list) -> str:
    """Build FFmpeg filter_complex for removing silence segments."""
    if not silences:
        return ""

    # Build segments to KEEP
    keep = []
    pos = 0.0
    for start, end in silences:
        if start > pos:
            keep.append((pos, start))
        pos = end
    if pos < duration:
        keep.append((pos, duration))

    # Build filter
    parts = []
    for i, (start, end) in enumerate(keep):
        parts.append(
            f"[0:v]trim=start={start:.3f}:end={end:.3f},setpts=PTS-STARTPTS[v{i}];"
            f"[0:a]atrim=start={start:.3f}:end={end:.3f},asetpts=PTS-STARTPTS[a{i}]"
        )

    v_concat = "".join(f"[v{i}]" for i in range(len(keep)))
    a_concat = "".join(f"[a{i}]" for i in range(len(keep)))
    n = len(keep)
    parts.append(f"{v_concat}{a_concat}concat=n={n}:v=1:a=1[outv][outa]")

    return ";".join(parts)


# ══════════════════════════════════════════════
# FFMPEG OPERATIONS
# ══════════════════════════════════════════════

def extract_audio(video_path: Path, audio_path: Path) -> bool:
    """Extract audio from video for Whisper."""
    result = subprocess.run(
        ["ffmpeg", "-y", "-i", str(video_path), "-vn", "-acodec", "pcm_s16le",
         "-ar", "16000", "-ac", "1", str(audio_path)],
        capture_output=True, text=True,
    )
    return result.returncode == 0


def burn_subtitles(video_path: Path, ass_path: Path, output_path: Path) -> bool:
    """Burn ASS subtitles into video using FFmpeg."""
    # Escape path for FFmpeg filter (backslashes and colons)
    ass_escaped = str(ass_path).replace("\\", "/").replace(":", "\\:")

    result = subprocess.run(
        ["ffmpeg", "-y", "-i", str(video_path),
         "-vf", f"ass={ass_escaped}",
         "-c:v", "libx264", "-preset", "fast", "-crf", "23",
         "-c:a", "aac", "-b:a", "128k",
         str(output_path)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"  FFmpeg error: {result.stderr[-500:]}")
    return result.returncode == 0


def remove_silences(video_path: Path, output_path: Path, silences: list,
                    duration: float) -> bool:
    """Remove silence segments from video."""
    if not silences:
        shutil.copy2(video_path, output_path)
        return True

    filter_complex = build_ffmpeg_trim_filter(duration, silences)
    result = subprocess.run(
        ["ffmpeg", "-y", "-i", str(video_path),
         "-filter_complex", filter_complex,
         "-map", "[outv]", "-map", "[outa]",
         "-c:v", "libx264", "-preset", "fast", "-crf", "23",
         "-c:a", "aac", "-b:a", "128k",
         str(output_path)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"  FFmpeg error: {result.stderr[-500:]}")
    return result.returncode == 0


def concat_videos(parts: list, output_path: Path) -> bool:
    """Concatenate video files (intro + main + outro)."""
    # Create concat file
    concat_file = output_path.parent / "concat_list.txt"
    with open(concat_file, "w") as f:
        for part in parts:
            f.write(f"file '{part}'\n")

    result = subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0",
         "-i", str(concat_file),
         "-c:v", "libx264", "-preset", "fast", "-crf", "23",
         "-c:a", "aac", "-b:a", "128k",
         str(output_path)],
        capture_output=True, text=True,
    )
    concat_file.unlink(missing_ok=True)
    return result.returncode == 0


def render_remotion_clip(composition_id: str, output_path: Path) -> bool:
    """Render a Remotion composition to MP4."""
    result = subprocess.run(
        ["npx", "remotion", "render", composition_id, str(output_path)],
        cwd=str(REMOTION_DIR),
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"  Remotion render error: {result.stderr[-300:]}")
    return result.returncode == 0


# ══════════════════════════════════════════════
# DAVINCI RESOLVE EXPORT (FCPXML)
# ══════════════════════════════════════════════

def get_video_info(video_path: Path) -> dict:
    """Get video metadata via FFprobe."""
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json",
         "-show_format", "-show_streams", str(video_path)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return {"fps": 30, "width": 1080, "height": 1920, "duration": 60.0}

    data = json.loads(result.stdout)
    video_stream = next(
        (s for s in data.get("streams", []) if s["codec_type"] == "video"), {}
    )
    # Parse frame rate (e.g. "30/1" or "30000/1001")
    fps_str = video_stream.get("r_frame_rate", "30/1")
    num, den = map(int, fps_str.split("/"))
    fps = round(num / den)

    return {
        "fps": fps,
        "width": int(video_stream.get("width", 1080)),
        "height": int(video_stream.get("height", 1920)),
        "duration": float(data.get("format", {}).get("duration", 60.0)),
    }


def frames_str(seconds: float, fps: int) -> str:
    """Convert seconds to FCPXML frame duration string: '12345/30000s'."""
    # FCPXML uses rational time: frames * timebase
    total_frames = round(seconds * fps)
    return f"{total_frames * 1000}/{fps * 1000}s"


def generate_fcpxml(video_path: Path, words: list, silences: list,
                    duration: float, output_path: Path,
                    include_subtitles: bool = True) -> None:
    """
    Generate FCPXML 1.11 timeline for DaVinci Resolve.
    Creates a timeline with:
    - Original video with silence gaps marked
    - Subtitle markers at word positions
    - Cut points at silence boundaries
    """
    info = get_video_info(video_path)
    fps = info["fps"]
    abs_path = str(video_path.resolve())
    file_url = f"file://{abs_path}"

    # Build segments to keep (between silences)
    keep_segments = []
    pos = 0.0
    for s_start, s_end in silences:
        if s_start > pos:
            keep_segments.append({"start": pos, "end": s_start})
        pos = s_end
    if pos < duration:
        keep_segments.append({"start": pos, "end": duration})

    if not keep_segments:
        keep_segments = [{"start": 0.0, "end": duration}]

    # Build FCPXML
    clips_xml = []
    offset = 0.0
    for i, seg in enumerate(keep_segments):
        seg_dur = seg["end"] - seg["start"]
        clip_xml = f"""            <clip name="Segment {i+1}" offset="{frames_str(offset, fps)}" duration="{frames_str(seg_dur, fps)}" start="{frames_str(seg["start"], fps)}">
              <video ref="r2" offset="{frames_str(seg["start"], fps)}" duration="{frames_str(seg_dur, fps)}" start="{frames_str(seg["start"], fps)}"/>
            </clip>"""
        clips_xml.append(clip_xml)
        offset += seg_dur

    total_duration = sum(s["end"] - s["start"] for s in keep_segments)

    # Add subtitle markers if requested
    markers_xml = ""
    if include_subtitles and words:
        marker_lines = []
        for w in words[::5]:  # Every 5th word as marker (not too dense)
            marker_lines.append(
                f'            <marker start="{frames_str(w["start"], fps)}" '
                f'duration="{frames_str(0.1, fps)}" value="{w["word"]}"/>'
            )
        markers_xml = "\n".join(marker_lines)

    fcpxml = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE fcpxml>
<fcpxml version="1.11">
  <resources>
    <format id="r1" name="FFVideoFormat1080x1920p{fps}" frameDuration="{frames_str(1.0/fps, fps)}" width="{info['width']}" height="{info['height']}"/>
    <asset id="r2" name="{video_path.stem}" src="{file_url}" start="0s" duration="{frames_str(duration, fps)}" hasVideo="1" hasAudio="1" format="r1"/>
  </resources>
  <library>
    <event name="TikTok Edit">
      <project name="{video_path.stem}_edit">
        <sequence format="r1" duration="{frames_str(total_duration, fps)}">
          <spine>
{chr(10).join(clips_xml)}
          </spine>
        </sequence>
      </project>
    </event>
  </library>
</fcpxml>
"""
    output_path.write_text(fcpxml, encoding="utf-8")


# ══════════════════════════════════════════════
# METADATA GENERATION
# ══════════════════════════════════════════════

def generate_tiktok_metadata(transcript: str, clip_name: str) -> dict:
    """Generate TikTok description and hashtags from transcript."""
    # Extract first sentence as hook
    sentences = re.split(r'[.!?]', transcript)
    hook = sentences[0].strip() if sentences else clip_name

    # Core hashtags for Dokodu content
    base_hashtags = [
        "#AI", "#SztucznaInteligencja", "#Automatyzacja",
        "#AIwBiznesie", "#TechTips", "#PolskiTech",
    ]

    # Content-specific hashtags based on keywords
    keyword_hashtags = {
        "prompt": "#Promptowanie",
        "chatgpt": "#ChatGPT",
        "claude": "#Claude",
        "copilot": "#Copilot",
        "excel": "#Excel",
        "n8n": "#n8n",
        "agent": "#AIAgent",
        "automatyzacja": "#AutomatyzacjaProcesów",
        "firma": "#Biznes",
        "dane": "#BigData",
    }

    extra = []
    text_lower = transcript.lower()
    for keyword, hashtag in keyword_hashtags.items():
        if keyword in text_lower:
            extra.append(hashtag)

    hashtags = base_hashtags + extra[:4]  # Max ~10 hashtags total

    description = f"{hook}\n\n{'  '.join(hashtags)}"

    return {
        "description": description,
        "hashtags": hashtags,
        "hook": hook,
        "transcript": transcript,
    }


# ══════════════════════════════════════════════
# SCENARIO GENERATOR
# ══════════════════════════════════════════════

def load_ideas_bank() -> list:
    """Parse TikTok_Ideas_Bank.md and return list of ideas."""
    if not IDEAS_BANK.exists():
        print(f"ERROR: Brak pliku {IDEAS_BANK}")
        return []

    text = IDEAS_BANK.read_text(encoding="utf-8")
    ideas = []

    # Parse table rows: | T-XXX | hook | treść | format | status |
    for match in re.finditer(
        r'\|\s*(T-\d+)\s*\|\s*"?([^"|]+)"?\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*(\w+)\s*\|',
        text
    ):
        idea_id, hook, content, fmt, status = match.groups()
        if status.strip() == "POMYSŁ":
            ideas.append({
                "id": idea_id.strip(),
                "hook": hook.strip().strip('"'),
                "content": content.strip(),
                "format": fmt.strip(),
                "status": status.strip(),
            })

    return ideas


def generate_scenarios(count: int = 10) -> list:
    """
    Generate teleprompter-ready scenarios from Ideas Bank.
    Follows TikTok_Playbook.md structure:
      [0-0.5s] HOOK → [0.5-3s] PROBLEM → [3-8s] KONTEKST →
      [8-45s] WARTOŚĆ → [45-55s] PUNCHLINE → [55-60s] CTA
    """
    ideas = load_ideas_bank()
    if not ideas:
        print("Brak pomysłów w statusie POMYSŁ")
        return []

    selected = ideas[:count]
    scenarios = []

    for idea in selected:
        # Build full spoken script from idea skeleton
        hook = idea["hook"]
        content = idea["content"]

        script = f"""{idea['id']} — SCENARIUSZ TIKTOK
Format: {idea['format']}
Czas: 45 sekund
Struktura: Hook → Problem → Wartość → Punchline → CTA




{hook}

{content}

Obserwuj — więcej takich w każdym tygodniu.
"""
        scenarios.append({
            "id": idea["id"],
            "script": script,
            "hook": hook,
        })

    return scenarios


def export_scenarios_to_dropbox(scenarios: list) -> int:
    """Export scenarios to Dropbox for Parrot Teleprompter."""
    exported = 0

    if not DROPBOX_DIR.exists():
        DROPBOX_DIR.mkdir(parents=True, exist_ok=True)

    for sc in scenarios:
        filename = f"TikTok_{sc['id']}_scenariusz.txt"
        filepath = DROPBOX_DIR / filename
        filepath.write_text(sc["script"], encoding="utf-8")
        exported += 1
        print(f"  ✓ {filename}")

    return exported


# ══════════════════════════════════════════════
# MAIN PIPELINE
# ══════════════════════════════════════════════

def process_clip(video_path: Path, output_dir: Path,
                 model_size: str = "medium",
                 with_intro: bool = True,
                 with_cta: bool = True,
                 cut_silences: bool = True) -> bool:
    """Full post-production pipeline for a single TikTok clip."""

    clip_name = video_path.stem
    work_dir = output_dir / clip_name
    work_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*50}")
    print(f"TikTok Pipeline — {clip_name}")
    print(f"{'='*50}\n")

    # Step 1: Extract audio
    audio_path = work_dir / "audio.wav"
    print("  [1/6] Ekstrakcja audio...")
    if not extract_audio(video_path, audio_path):
        print("  ERROR: Nie udało się wyciągnąć audio")
        return False
    print("  ✓ Audio extracted")

    # Step 2: Whisper transcription with word timestamps
    print("  [2/6] Transkrypcja Whisper...")
    result = transcribe_with_words(audio_path, model_size)
    words = result["words"]
    duration = result["duration"]

    # Save transcript
    (work_dir / "transkrypcja.txt").write_text(result["text"], encoding="utf-8")

    # Step 3: Generate ASS subtitles
    print("  [3/6] Generowanie napisów ASS...")
    ass_path = work_dir / "napisy.ass"
    generate_ass_subtitles(words, ass_path)
    print(f"  ✓ napisy.ass ({len(words)} słów)")

    # Step 4: Cut silences
    current_video = video_path
    if cut_silences:
        print("  [4/6] Wykrywanie i cięcie pauz...")
        silences = detect_silences(words, threshold=0.8)
        if silences:
            trimmed_path = work_dir / "trimmed.mp4"
            total_cut = sum(e - s for s, e in silences)
            print(f"  Znaleziono {len(silences)} pauz ({total_cut:.1f}s do wycięcia)")
            if remove_silences(current_video, trimmed_path, silences, duration):
                current_video = trimmed_path
                print(f"  ✓ Wycięto {total_cut:.1f}s ciszy")
            else:
                print("  ⚠ Nie udało się wyciąć pauz, kontynuuję z oryginałem")
        else:
            print("  ✓ Brak długich pauz do wycięcia")
    else:
        print("  [4/6] Pomijam cięcie pauz")

    # Step 5: Burn subtitles
    print("  [5/6] Wypalanie napisów...")
    subtitled_path = work_dir / "subtitled.mp4"
    if not burn_subtitles(current_video, ass_path, subtitled_path):
        print("  ERROR: Nie udało się wypalić napisów")
        return False
    print("  ✓ Napisy wypalone")
    current_video = subtitled_path

    # Step 6: Concat intro + main + CTA
    parts_to_concat = []
    if with_intro:
        print("  [6/6] Renderowanie intro/CTA (Remotion)...")
        intro_path = work_dir / "intro.mp4"
        if render_remotion_clip("TikTok-Intro", intro_path):
            parts_to_concat.append(intro_path)
            print("  ✓ Intro")
        else:
            print("  ⚠ Nie udało się zrenderować intro, pomijam")

    parts_to_concat.append(current_video)

    if with_cta:
        cta_path = work_dir / "cta.mp4"
        if render_remotion_clip("TikTok-CTA", cta_path):
            parts_to_concat.append(cta_path)
            print("  ✓ CTA")
        else:
            print("  ⚠ Nie udało się zrenderować CTA, pomijam")

    # Final concat
    final_path = work_dir / f"{clip_name}_final.mp4"
    if len(parts_to_concat) > 1:
        if not concat_videos(parts_to_concat, final_path):
            # Fallback: just use subtitled version
            shutil.copy2(current_video, final_path)
    else:
        shutil.copy2(current_video, final_path)

    # Generate metadata
    metadata = generate_tiktok_metadata(result["text"], clip_name)
    (work_dir / "opis.txt").write_text(metadata["description"], encoding="utf-8")
    (work_dir / "hashtagi.txt").write_text("\n".join(metadata["hashtags"]), encoding="utf-8")

    # Generate FCPXML for DaVinci Resolve
    fcpxml_path = work_dir / f"{clip_name}.fcpxml"
    silences_for_xml = detect_silences(words, threshold=0.8) if cut_silences else []
    generate_fcpxml(video_path, words, silences_for_xml, duration, fcpxml_path)
    print(f"  ✓ {clip_name}.fcpxml     (DaVinci Resolve timeline)")

    # Summary
    final_size = final_path.stat().st_size / (1024 * 1024)
    print(f"\n{'─'*50}")
    print(f"  ✓ GOTOWE: {final_path.name} ({final_size:.1f} MB)")
    print(f"  Pliki w: {work_dir}")
    print(f"  - {clip_name}_final.mp4  (gotowy do uploadu)")
    print(f"  - {clip_name}.fcpxml     (timeline DaVinci — File > Import > Timeline)")
    print(f"  - napisy.ass             (napisy ASS)")
    print(f"  - transkrypcja.txt       (surowy tekst)")
    print(f"  - opis.txt               (opis TikTok)")
    print(f"  - hashtagi.txt           (hashtagi)")

    # Cleanup temp files
    audio_path.unlink(missing_ok=True)
    trimmed = work_dir / "trimmed.mp4"
    trimmed.unlink(missing_ok=True)

    return True


def process_batch(input_dir: Path, output_dir: Path, **kwargs) -> None:
    """Process all video files in a directory."""
    video_files = sorted(
        p for p in input_dir.iterdir()
        if p.suffix.lower() in (".mp4", ".mov", ".mkv", ".webm")
    )

    if not video_files:
        print(f"Brak plików wideo w {input_dir}")
        return

    print(f"\nZnaleziono {len(video_files)} klipów do przetworzenia\n")
    success = 0
    for i, vf in enumerate(video_files, 1):
        print(f"\n[{i}/{len(video_files)}] {vf.name}")
        if process_clip(vf, output_dir, **kwargs):
            success += 1

    print(f"\n{'='*50}")
    print(f"BATCH COMPLETE: {success}/{len(video_files)} klipów przetworzonych")
    print(f"Wyniki w: {output_dir}")


# ══════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="TikTok Pipeline — Dokodu",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="Komenda")

    # process — single clip
    p_proc = subparsers.add_parser("process", help="Przetwórz pojedynczy klip")
    p_proc.add_argument("video", type=Path, help="Ścieżka do pliku wideo")
    p_proc.add_argument("--output", "-o", type=Path, default=TIKTOK_DIR,
                        help=f"Katalog wyjściowy (domyślnie: {TIKTOK_DIR})")
    p_proc.add_argument("--model", default="medium",
                        choices=["tiny", "base", "small", "medium", "large"])
    p_proc.add_argument("--no-intro", action="store_true", help="Bez intro")
    p_proc.add_argument("--no-cta", action="store_true", help="Bez CTA")
    p_proc.add_argument("--no-cut", action="store_true", help="Bez cięcia pauz")

    # batch — folder of clips
    p_batch = subparsers.add_parser("batch", help="Przetwórz folder klipów")
    p_batch.add_argument("input_dir", type=Path, help="Katalog z nagraniami")
    p_batch.add_argument("--output", "-o", type=Path, default=TIKTOK_DIR)
    p_batch.add_argument("--model", default="medium",
                         choices=["tiny", "base", "small", "medium", "large"])
    p_batch.add_argument("--no-intro", action="store_true")
    p_batch.add_argument("--no-cta", action="store_true")
    p_batch.add_argument("--no-cut", action="store_true")

    # subtitles — only generate subtitles
    p_sub = subparsers.add_parser("subtitles", help="Tylko napisy (bez montażu)")
    p_sub.add_argument("video", type=Path)
    p_sub.add_argument("--output", "-o", type=Path, default=None)
    p_sub.add_argument("--model", default="medium",
                       choices=["tiny", "base", "small", "medium", "large"])

    # davinci — generate DaVinci Resolve timeline only
    p_dv = subparsers.add_parser("davinci", help="Eksport timeline do DaVinci Resolve (FCPXML)")
    p_dv.add_argument("video", type=Path, help="Ścieżka do pliku wideo")
    p_dv.add_argument("--output", "-o", type=Path, default=None,
                      help="Plik wyjściowy .fcpxml")
    p_dv.add_argument("--model", default="medium",
                      choices=["tiny", "base", "small", "medium", "large"])
    p_dv.add_argument("--silence-threshold", type=float, default=0.8,
                      help="Próg ciszy do cięcia w sekundach (domyślnie: 0.8)")

    # scenarios — generate teleprompter scripts
    p_sc = subparsers.add_parser("scenarios", help="Generuj scenariusze z Ideas Bank")
    p_sc.add_argument("--count", "-n", type=int, default=10,
                      help="Ile scenariuszy wygenerować")
    p_sc.add_argument("--dropbox", action="store_true",
                      help="Eksportuj do Dropbox (Parrot Teleprompter)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "process":
        if not args.video.exists():
            print(f"ERROR: Plik nie istnieje: {args.video}")
            sys.exit(1)
        process_clip(
            args.video, args.output,
            model_size=args.model,
            with_intro=not args.no_intro,
            with_cta=not args.no_cta,
            cut_silences=not args.no_cut,
        )

    elif args.command == "batch":
        if not args.input_dir.is_dir():
            print(f"ERROR: Katalog nie istnieje: {args.input_dir}")
            sys.exit(1)
        process_batch(
            args.input_dir, args.output,
            model_size=args.model,
            with_intro=not args.no_intro,
            with_cta=not args.no_cta,
            cut_silences=not args.no_cut,
        )

    elif args.command == "subtitles":
        if not args.video.exists():
            print(f"ERROR: Plik nie istnieje: {args.video}")
            sys.exit(1)

        # Extract audio
        audio_path = Path("/tmp/tiktok_audio.wav")
        print("Ekstrakcja audio...")
        extract_audio(args.video, audio_path)

        # Transcribe
        result = transcribe_with_words(audio_path, args.model)

        # Generate ASS
        out = args.output or args.video.with_suffix(".ass")
        generate_ass_subtitles(result["words"], out)
        print(f"\n✓ Napisy zapisane: {out}")

        audio_path.unlink(missing_ok=True)

    elif args.command == "davinci":
        if not args.video.exists():
            print(f"ERROR: Plik nie istnieje: {args.video}")
            sys.exit(1)

        print(f"\nDaVinci Resolve Export — {args.video.name}")
        print(f"{'='*50}\n")

        # Extract audio
        audio_path = Path("/tmp/tiktok_audio.wav")
        print("  Ekstrakcja audio...")
        extract_audio(args.video, audio_path)

        # Transcribe
        result = transcribe_with_words(audio_path, args.model)
        words = result["words"]

        # Detect silences
        silences = detect_silences(words, threshold=args.silence_threshold)
        if silences:
            total_cut = sum(e - s for s, e in silences)
            print(f"  Znaleziono {len(silences)} pauz ({total_cut:.1f}s)")
        else:
            print(f"  Brak pauz > {args.silence_threshold}s")

        # Generate FCPXML
        out = args.output or args.video.with_suffix(".fcpxml")
        generate_fcpxml(args.video, words, silences, result["duration"], out)

        # Also save transcript and ASS subtitles
        txt_path = args.video.with_suffix(".txt")
        txt_path.write_text(result["text"], encoding="utf-8")
        ass_path = args.video.with_suffix(".ass")
        generate_ass_subtitles(words, ass_path)

        print(f"\n✓ Pliki gotowe:")
        print(f"  {out.name}  — File > Import > Timeline w DaVinci")
        print(f"  {ass_path.name}  — napisy ASS (importuj jako subtitle track)")
        print(f"  {txt_path.name}  — surowa transkrypcja")

        audio_path.unlink(missing_ok=True)

    elif args.command == "scenarios":
        scenarios = generate_scenarios(args.count)
        if not scenarios:
            sys.exit(1)

        print(f"\nWygenerowano {len(scenarios)} scenariuszy:\n")
        for sc in scenarios:
            print(f"  {sc['id']}: {sc['hook']}")

        if args.dropbox:
            print(f"\nEksport do Dropbox ({DROPBOX_DIR})...")
            exported = export_scenarios_to_dropbox(scenarios)
            print(f"\n✓ Wyeksportowano {exported} scenariuszy do Parrot Teleprompter")
        else:
            # Save to tiktok_publish
            TIKTOK_DIR.mkdir(parents=True, exist_ok=True)
            for sc in scenarios:
                filepath = TIKTOK_DIR / f"{sc['id']}_scenariusz.txt"
                filepath.write_text(sc["script"], encoding="utf-8")
            print(f"\n✓ Scenariusze w: {TIKTOK_DIR}")
            print("  Dodaj --dropbox żeby wyeksportować do Parrot Teleprompter")


if __name__ == "__main__":
    main()
