#!/usr/bin/env python3
"""
DOKODU BRAIN — YT Publish Kit
Generuje komplet materiałów do publikacji odcinka YouTube:
  - thumbnail_base.png  (Remotion still render)
  - opis_youtube.txt    (gotowy do wklejenia w YT Studio)
  - tagi.txt            (tagi gotowe do wklejenia)
  - prompter.txt        (scenariusz dla Parrot Promptera)
  - checklist.md        (co zrobić przed publikacją)

Wyniki trafiają do:
  - BRAIN: movies/YT-XXX/publish/
  - Dropbox: Scenariusze/YT-XXX_publish/

Użycie:
  python3 yt_publish_kit.py YT-002
  python3 yt_publish_kit.py YT-002 --no-thumbnail   # pomiń render (szybszy)
"""

import sys
import re
import os
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

BRAIN_DIR       = Path(__file__).parent.parent
MOVIES_DIR      = BRAIN_DIR / "30_RESOURCES" / "RES_YouTube" / "movies"
REMOTION_DIR    = Path("/home/kacper/DOKODU/remotion")
DROPBOX_DIR     = Path("/mnt/c/Users/Kacper/Dropbox/Scenariusze")
PARROT_DIR      = Path("/mnt/c/Users/Kacper/Dropbox/Apps/Parrot Teleprompter")
EXPORT_SCRIPT   = Path(__file__).parent / "export_prompter.py"


# ══════════════════════════════════════════════
# PARSOWANIE metadata.md
# ══════════════════════════════════════════════

def extract_section(text: str, header: str) -> str:
    """Wyciąga zawartość sekcji markdown między nagłówkami."""
    pattern = rf"##\s+{re.escape(header)}\n(.*?)(?=\n##\s|\Z)"
    m = re.search(pattern, text, re.DOTALL)
    return m.group(1).strip() if m else ""


def extract_frontmatter_field(text: str, field: str) -> str:
    m = re.search(rf"^{field}:\s*(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else ""


def parse_metadata(video_id: str) -> dict:
    meta_file = MOVIES_DIR / video_id / "metadata.md"
    if not meta_file.exists():
        print(f"ERROR: Brak metadata.md dla {video_id}")
        sys.exit(1)

    text = meta_file.read_text(encoding="utf-8")

    # Opis YouTube — wyciągamy akapity i linki
    opis_raw = extract_section(text, "Opis YouTube")

    # Tagi — linia z backtick-oddzielonymi tagami
    tagi_section = extract_section(text, r"Tagi \(\d+\)")
    tagi_raw = re.findall(r"`([^`]+)`", tagi_section)

    # Hashtagi
    hashtagi = ""
    m = re.search(r"\*\*Hashtagi:\*\*\s*(.+)", text)
    if m:
        hashtagi = m.group(1).strip()

    # Chapters
    chapters = ""
    m = re.search(r"\*\*Chapters:\*\*\s*\n(.+?)(?=\n\n|\n##|\Z)", text, re.DOTALL)
    if m:
        chapters = m.group(1).strip()

    # Tytuł z nagłówka H1
    m = re.search(r"^#\s+(?:YT-\d+\s+—\s+)?(.+)$", text, re.MULTILINE)
    title = m.group(1).strip() if m else video_id

    return {
        "id": video_id,
        "title": title,
        "opis_raw": opis_raw,
        "tagi": tagi_raw,
        "hashtagi": hashtagi,
        "chapters": chapters,
        "deadline": extract_frontmatter_field(text, "deadline"),
        "lokowanie": extract_frontmatter_field(text, "lokowanie"),
    }


# ══════════════════════════════════════════════
# GENERATORY PLIKÓW
# ══════════════════════════════════════════════

def build_opis(data: dict) -> str:
    """Opis YouTube gotowy do wklejenia w YT Studio."""
    lines = []
    lines.append(f"# OPIS YOUTUBE — {data['id']}: {data['title']}")
    lines.append(f"# Wygenerowano: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")
    lines.append("=" * 60)
    lines.append("OPIS (wklej do YT Studio → Opis):")
    lines.append("=" * 60)
    lines.append("")

    # Wyczyść markdown z opisu
    opis = data["opis_raw"]
    # Usuń nagłówki **Akapit X:**
    opis = re.sub(r"\*\*Akapit \d+[^:]*:\*\*\s*", "", opis)
    # Usuń nagłówki **Linki:**
    opis = re.sub(r"\*\*Linki:\*\*\s*", "\n", opis)
    # Usuń **Hashtagi:** linia (dodamy osobno)
    opis = re.sub(r"\*\*Hashtagi:\*\*.*", "", opis)
    # Usuń **Chapters:** linia
    opis = re.sub(r"\*\*Chapters:\*\*.*", "", opis, flags=re.DOTALL)
    # Wyczyść pogrubienia
    opis = re.sub(r"\*\*([^*]+)\*\*", r"\1", opis)
    # Wielokrotne puste linie
    opis = re.sub(r"\n{3,}", "\n\n", opis)
    lines.append(opis.strip())
    lines.append("")
    if data["hashtagi"]:
        lines.append(data["hashtagi"])
    lines.append("")

    if data["chapters"]:
        lines.append("─" * 40)
        lines.append("CHAPTERS:")
        lines.append(data["chapters"])

    return "\n".join(lines)


def build_tagi(data: dict) -> str:
    """Tagi gotowe do wklejenia w YT Studio (przecinkiem)."""
    lines = []
    lines.append(f"# TAGI — {data['id']}: {data['title']}")
    lines.append(f"# Wklej w YT Studio → Tagi (każdy tag osobno lub przecinkiem)")
    lines.append("")
    lines.append(", ".join(data["tagi"]))
    lines.append("")
    lines.append("─" * 40)
    lines.append("Każdy tag osobno:")
    for tag in data["tagi"]:
        lines.append(f"  {tag}")
    return "\n".join(lines)


def build_checklist(data: dict) -> str:
    """Checklist przed i po publikacji."""
    lines = [
        f"# Checklist publikacji — {data['id']}: {data['title']}",
        f"Wygenerowano: {datetime.now().strftime('%Y-%m-%d')}",
        "",
        "## Przed nagraniem",
        "- [ ] Podepnij kartę w AI Studio (Tier 1) — unikniesz błędu 429",
        "- [ ] Sprawdź Node.js: `node --version` (wymagane 18+)",
        "- [ ] Przejrzyj scenariusz w Parrot Prompterze",
        "- [ ] Nagraj screencasts (lista w metadata.md)",
        "",
        "## Przed montażem",
        "- [ ] Wgraj surowe nagranie",
        "- [ ] Wyrenderuj animacje Remotion (9 szt. + thumbnail)",
        "- [ ] Wklej face photo na thumbnail_base.png w Canvie",
        "",
        "## Przed publikacją w YT Studio",
        "- [ ] Wklej opis z `opis_youtube.txt`",
        "- [ ] Wklej tagi z `tagi.txt`",
        "- [ ] Wgraj thumbnail (po dodaniu twarzy w Canvie)",
        "- [ ] Dodaj chapters (po nagraniu — uzupełnij czasy)",
        "- [ ] Ustaw kartę końcową (link do YT-001)",
        "- [ ] Sprawdź placement lokowania:",
    ]

    if data["lokowanie"] and data["lokowanie"] != "null":
        lines.append(f"      → {data['lokowanie']}")
    else:
        lines.append("      → brak lokowania w tym odcinku")

    lines += [
        "",
        "## Po publikacji",
        "- [ ] Zaktualizuj `opublikowany: true` w metadata.md",
        "- [ ] Dodaj link do metadata.md (`link: https://youtu.be/...`)",
        "- [ ] Zaktualizuj tracker YT_Videos.md (✅ Opublikowany)",
        "- [ ] Wrzuć post na LinkedIn z linkiem",
        "- [ ] Wyślij newsletter (jeśli planowany)",
        "",
        "---",
        f"*{data['id']} — {data['title']}*",
    ]
    return "\n".join(lines)


# ══════════════════════════════════════════════
# REMOTION THUMBNAIL RENDER
# ══════════════════════════════════════════════

def render_thumbnail(video_id: str, out_path: Path) -> bool:
    comp_id = f"{video_id}-Thumbnail"
    print(f"  Renderuję thumbnail: {comp_id}...")
    result = subprocess.run(
        ["npx", "remotion", "still", comp_id, str(out_path), "--frame=0"],
        cwd=REMOTION_DIR,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print(f"  ✓ Thumbnail zapisany: {out_path.name}")
        return True
    else:
        print(f"  ✗ Remotion błąd: {result.stderr[-300:]}")
        print(f"    (Sprawdź czy kompozycja '{comp_id}' istnieje w Root.tsx)")
        return False


# ══════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════

def main():
    args = sys.argv[1:]
    no_thumbnail = "--no-thumbnail" in args
    ids = [a for a in args if not a.startswith("--")]

    if not ids:
        print("Użycie: python3 yt_publish_kit.py YT-002 [--no-thumbnail]")
        sys.exit(1)

    video_id = ids[0].upper() if ids[0].upper().startswith("YT-") else f"YT-{ids[0]}"

    print(f"\n{'='*50}")
    print(f"YT Publish Kit — {video_id}")
    print(f"{'='*50}\n")

    # Parsuj metadata
    data = parse_metadata(video_id)
    print(f"  Film: {data['title']}")

    # Katalogi wyjściowe
    publish_dir  = MOVIES_DIR / video_id / "publish"
    dropbox_dir  = DROPBOX_DIR / f"{video_id}_publish"
    publish_dir.mkdir(parents=True, exist_ok=True)
    dropbox_dir.mkdir(parents=True, exist_ok=True)

    print(f"  Output BRAIN:   {publish_dir}")
    print(f"  Output Dropbox: {dropbox_dir}")
    print()

    # 1. Opis YouTube
    opis_content = build_opis(data)
    (publish_dir / "opis_youtube.txt").write_text(opis_content, encoding="utf-8")
    (dropbox_dir / "opis_youtube.txt").write_text(opis_content, encoding="utf-8")
    print("  ✓ opis_youtube.txt")

    # 2. Tagi
    tagi_content = build_tagi(data)
    (publish_dir / "tagi.txt").write_text(tagi_content, encoding="utf-8")
    (dropbox_dir / "tagi.txt").write_text(tagi_content, encoding="utf-8")
    print("  ✓ tagi.txt")

    # 3. Checklist
    checklist_content = build_checklist(data)
    (publish_dir / "checklist.md").write_text(checklist_content, encoding="utf-8")
    (dropbox_dir / "checklist.md").write_text(checklist_content, encoding="utf-8")
    print("  ✓ checklist.md")

    # 4. Prompter (scenariusz)
    result = subprocess.run(
        ["python3", str(EXPORT_SCRIPT), video_id],
        capture_output=True, text=True
    )
    PARROT_DIR.mkdir(parents=True, exist_ok=True)
    prompter_src = PARROT_DIR / f"{video_id}_prompter.txt"
    if prompter_src.exists():
        shutil.copy(prompter_src, publish_dir / "prompter.txt")
        shutil.copy(prompter_src, dropbox_dir / "prompter.txt")
        print("  ✓ prompter.txt → Parrot Teleprompter")
    else:
        print("  ✗ prompter.txt — brak scenariusz.md (pomiń lub napisz scenariusz)")

    # 5. Thumbnail (Remotion)
    if no_thumbnail:
        print("  ⟳ thumbnail pominięty (--no-thumbnail)")
    else:
        thumb_path = publish_dir / "thumbnail_base.png"
        ok = render_thumbnail(video_id, thumb_path)
        if ok:
            shutil.copy(thumb_path, dropbox_dir / "thumbnail_base.png")
            print(f"  ✓ thumbnail_base.png → skopiowany do Dropboxa")

    # Podsumowanie
    print(f"\n{'='*50}")
    print(f"Gotowe! Pliki w Dropboxie:")
    print(f"  Scenariusze/{video_id}_publish/")
    for f in sorted(dropbox_dir.iterdir()):
        size = f.stat().st_size
        size_str = f"{size // 1024} KB" if size > 1024 else f"{size} B"
        print(f"    {f.name:<30} {size_str}")
    print()
    print("Następny krok: otwórz Canvę, wgraj thumbnail_base.png, dodaj twarz.")


if __name__ == "__main__":
    main()
