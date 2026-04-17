#!/usr/bin/env python3
"""
DOKODU BRAIN — Export scenariusza do Parrot Promptera (Dropbox)

Usuwa tagi [SCREENCAST], [ANIMACJA], [B-ROLL] — zostawia tylko tekst mówiony.
[PAUZA] zamienia na pustą linię (naturalna pauza w prompterze).

Użycie:
  python3 export_prompter.py YT-002
  python3 export_prompter.py YT-001 YT-002   # kilka naraz
  python3 export_prompter.py --all            # wszystkie ze statusem scenariusz=true
"""

import re
import sys
import os
from pathlib import Path

BRAIN_DIR    = Path(__file__).parent.parent
MOVIES_DIR   = BRAIN_DIR / "30_RESOURCES" / "RES_YouTube" / "movies"
DROPBOX_DIR  = Path("/mnt/c/Users/Kacper/Dropbox/Apps/Parrot Teleprompter")

# Tagi które są usuwane razem z zawartością linii
REMOVE_TAGS = re.compile(
    r"^\s*\[(SCREENCAST|ANIMACJA|B-ROLL|PAUZA)[^\]]*\].*$",
    re.MULTILINE | re.IGNORECASE
)

# [PAUZA] → pusta linia (wizualny oddech w prompterze)
PAUZA_TAG = re.compile(r"^\s*\[PAUZA\]\s*$", re.MULTILINE | re.IGNORECASE)

# Nagłówki markdown (## HOOK etc.) → zostawiamy jako separator
HEADING = re.compile(r"^#{1,4}\s+(.+)$", re.MULTILINE)

# Frontmatter YAML
FRONTMATTER = re.compile(r"^---.*?---\s*", re.DOTALL)

# Bloki kodu (```...```) — usuwamy
CODE_BLOCK = re.compile(r"```.*?```", re.DOTALL)

# Linie z samym myślnikiem (separatory)
SEPARATOR = re.compile(r"^-{3,}$", re.MULTILINE)

# Pogrubienie/kursywa
BOLD_ITALIC = re.compile(r"\*{1,2}([^*]+)\*{1,2}")


def clean_script(raw: str) -> str:
    # Usuń frontmatter
    text = FRONTMATTER.sub("", raw)

    # Usuń bloki kodu
    text = CODE_BLOCK.sub("", text)

    # [PAUZA] → pusta linia
    text = PAUZA_TAG.sub("\n", text)

    # Usuń pozostałe tagi [SCREENCAST], [ANIMACJA], [B-ROLL]
    text = REMOVE_TAGS.sub("", text)

    # Nagłówki → CAPS jako separator wizualny
    text = HEADING.sub(lambda m: f"\n--- {m.group(1).upper()} ---\n", text)

    # Usuń linie separatorów ---
    text = SEPARATOR.sub("", text)

    # Usuń bold/italic
    text = BOLD_ITALIC.sub(r"\1", text)

    # Usuń cytaty (>) — hook jest jako cytat w md
    text = re.sub(r"^>\s*", "", text, flags=re.MULTILINE)

    # Wielokrotne puste linie → max 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def export_video(video_id: str) -> bool:
    folder = MOVIES_DIR / video_id
    script_file = folder / "scenariusz.md"

    if not script_file.exists():
        print(f"  ✗ {video_id}: brak scenariusz.md w {folder}")
        return False

    raw = script_file.read_text(encoding="utf-8")
    clean = clean_script(raw)

    DROPBOX_DIR.mkdir(parents=True, exist_ok=True)
    out_file = DROPBOX_DIR / f"{video_id}_prompter.txt"
    out_file.write_text(clean, encoding="utf-8")
    print(f"  ✓ {video_id} → {out_file}")
    return True


def find_all_with_script() -> list[str]:
    ids = []
    if not MOVIES_DIR.exists():
        return ids
    for d in sorted(MOVIES_DIR.iterdir()):
        if d.is_dir() and (d / "scenariusz.md").exists():
            ids.append(d.name)
    return ids


def main():
    args = sys.argv[1:]

    if not args:
        print("Użycie: python3 export_prompter.py YT-002")
        print("        python3 export_prompter.py --all")
        sys.exit(1)

    if "--all" in args:
        ids = find_all_with_script()
        if not ids:
            print("Brak scenariuszy do eksportu.")
            sys.exit(0)
    else:
        ids = [a.upper() if a.upper().startswith("YT-") else f"YT-{a}" for a in args]

    print(f"Eksport do Dropbox: {DROPBOX_DIR}")
    print()
    ok = 0
    for vid_id in ids:
        if export_video(vid_id):
            ok += 1

    print()
    print(f"Gotowe: {ok}/{len(ids)} eksportów")
    if ok:
        print(f"Folder w Dropboxie: Scenariusze/")


if __name__ == "__main__":
    main()
