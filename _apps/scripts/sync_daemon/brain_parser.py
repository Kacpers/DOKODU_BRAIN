"""BRAIN Markdown parser library.

Provides functions to read and write structured data embedded in
DOKODU BRAIN markdown files (PARA format).
"""

from __future__ import annotations

import re
from datetime import date
from io import StringIO
from typing import Any

from ruamel.yaml import YAML

# ---------------------------------------------------------------------------
# Sync section helpers
# ---------------------------------------------------------------------------

def extract_sync_section(content: str, marker: str) -> str:
    """Return text between <!-- SYNC:{marker} --> and <!-- /SYNC:{marker} -->.

    Returns empty string when markers are absent.
    """
    pattern = re.compile(
        r"<!--\s*SYNC:" + re.escape(marker) + r"\s*-->(.*?)<!--\s*/SYNC:" + re.escape(marker) + r"\s*-->",
        re.DOTALL,
    )
    m = pattern.search(content)
    return m.group(1) if m else ""


def update_sync_section(content: str, marker: str, new_content: str) -> str:
    """Replace text between SYNC markers, preserving everything outside them.

    If markers are not found the original content is returned unchanged.
    """
    pattern = re.compile(
        r"(<!--\s*SYNC:" + re.escape(marker) + r"\s*-->)(.*?)(<!--\s*/SYNC:" + re.escape(marker) + r"\s*-->)",
        re.DOTALL,
    )
    replacement = r"\g<1>" + new_content + r"\g<3>"
    result, n = pattern.subn(replacement, content)
    return result if n else content


# ---------------------------------------------------------------------------
# Pipeline table (CRM_Leady_B2B.md)
# ---------------------------------------------------------------------------

def _split_md_row(line: str) -> list[str]:
    """Split a markdown table row into cell values (stripped)."""
    line = line.strip().strip("|")
    return [cell.strip() for cell in line.split("|")]


def parse_pipeline_table(section: str) -> list[dict]:
    """Parse the PIPELINE table from a sync section.

    Expected columns (case-insensitive match):
        # | Firma | Kontakt | Zrodlo | Etap | Wartosc (PLN) | Nastepny krok | Deadline

    Skips:
    - Header row and separator row
    - Rows where firma cell equals "___" (placeholder)
    - Empty rows

    Returns list of dicts with keys:
        nr, firma, kontakt, zrodlo, etap, wartosc, nastepny_krok, deadline
    """
    rows = []
    lines = [l for l in section.splitlines() if l.strip().startswith("|")]

    header_seen = False
    for line in lines:
        cells = _split_md_row(line)
        if not cells:
            continue

        # Detect separator row (contains only dashes/colons)
        if all(re.fullmatch(r"[-:]+", c) for c in cells if c):
            continue

        # First non-separator pipe row is the header
        if not header_seen:
            header_seen = True
            continue

        # Pad / trim to 8 columns
        while len(cells) < 8:
            cells.append("")
        nr, firma, kontakt, zrodlo, etap, wartosc, nastepny_krok, deadline = cells[:8]

        # Skip placeholder rows
        if firma in ("___", "", "_"):
            continue

        rows.append(
            {
                "nr": nr,
                "firma": firma,
                "kontakt": kontakt,
                "zrodlo": zrodlo,
                "etap": etap,
                "wartosc": wartosc,
                "nastepny_krok": nastepny_krok,
                "deadline": deadline,
            }
        )

    return rows


# ---------------------------------------------------------------------------
# Outreach table (Outreach_Tracker.md)
# ---------------------------------------------------------------------------

def parse_outreach_table(section: str) -> list[dict]:
    """Parse the PIPELINE AKTYWNY table from Outreach_Tracker.md.

    Expected columns:
        # | Firma | Osoba | Stanowisko | Score | Data zaproszenia | Status | Następny krok | Follow-up

    Skips:
    - Header and separator rows
    - Note rows: nr ends with "-note" (e.g. "5b-note")
    - Continuation rows: firma starts with "↳"
    - Empty rows

    Returns list of dicts with keys:
        nr, firma, osoba, stanowisko, score, data_zaproszenia, status, nastepny_krok, follow_up
    """
    rows = []
    lines = [l for l in section.splitlines() if l.strip().startswith("|")]

    header_seen = False
    for line in lines:
        cells = _split_md_row(line)
        if not cells:
            continue

        # Separator row
        if all(re.fullmatch(r"[-:]+", c) for c in cells if c):
            continue

        # Header row
        if not header_seen:
            header_seen = True
            continue

        while len(cells) < 9:
            cells.append("")
        nr, firma, osoba, stanowisko, score, data_zaproszenia, status, nastepny_krok, follow_up = cells[:9]

        # Skip note-rows (nr ends with "-note")
        if nr.endswith("-note"):
            continue

        # Skip continuation rows (firma starts with "↳")
        if firma.startswith("↳"):
            continue

        # Skip fully empty rows
        if not nr and not firma and not osoba:
            continue

        rows.append(
            {
                "nr": nr,
                "firma": firma,
                "osoba": osoba,
                "stanowisko": stanowisko,
                "score": score,
                "data_zaproszenia": data_zaproszenia,
                "status": status,
                "nastepny_krok": nastepny_krok,
                "follow_up": follow_up,
            }
        )

    return rows


# ---------------------------------------------------------------------------
# YAML frontmatter (Profile.md)
# ---------------------------------------------------------------------------

_YAML_FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def _get_yaml() -> YAML:
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.default_flow_style = False
    return yaml


def parse_profile_yaml(content: str) -> dict:
    """Extract YAML frontmatter from Profile.md (or any BRAIN markdown file).

    Returns empty dict when no frontmatter is present.
    """
    m = _YAML_FRONTMATTER_RE.match(content)
    if not m:
        return {}
    yaml = _get_yaml()
    data = yaml.load(m.group(1))
    return dict(data) if data else {}


def update_profile_yaml(content: str, updates: dict) -> str:
    """Update specific YAML frontmatter fields, leaving the rest of the file intact.

    If no frontmatter is present the content is returned unchanged.
    """
    m = _YAML_FRONTMATTER_RE.match(content)
    if not m:
        return content

    yaml = _get_yaml()
    data = yaml.load(m.group(1)) or {}
    data.update(updates)

    stream = StringIO()
    yaml.dump(dict(data), stream)
    new_yaml = stream.getvalue().rstrip("\n")

    rest = content[m.end():]
    return f"---\n{new_yaml}\n---\n{rest}"


# ---------------------------------------------------------------------------
# Meeting sections (Meetings.md)
# ---------------------------------------------------------------------------

_MEETING_HEADER_RE = re.compile(r"^## (\d{4}-\d{2}-\d{2}) — (.+)$", re.MULTILINE)


def parse_meeting_sections(content: str) -> list[dict]:
    """Parse ## YYYY-MM-DD — Title sections from Meetings.md.

    Returns list of dicts: {date: str, title: str, content: str}
    sorted newest-first (by date string, lexicographic — ISO 8601 is safe).
    """
    matches = list(_MEETING_HEADER_RE.finditer(content))
    if not matches:
        return []

    sections = []
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        body = content[start:end].strip()
        sections.append(
            {
                "date": m.group(1),
                "title": m.group(2).strip(),
                "content": body,
            }
        )

    sections.sort(key=lambda s: s["date"], reverse=True)
    return sections


def append_meeting_section(content: str, meeting_date: str, title: str, body: str) -> str:
    """Insert a new meeting section after the H1 header (newest-first order).

    Finds the first ## section marker and inserts the new section before it,
    so the new meeting appears at the top of the chronological list.
    If no existing ## section is found, appends to the end.
    """
    new_section = f"\n## {meeting_date} — {title}\n\n{body.strip()}\n"

    # Find insertion point: right before the first ## heading after the H1
    first_h2 = _MEETING_HEADER_RE.search(content)
    if first_h2:
        insert_at = first_h2.start()
        return content[:insert_at] + new_section + "\n" + content[insert_at:]

    # No existing meetings — look for the separator after H1 (---) or just append
    sep_match = re.search(r"^---$", content, re.MULTILINE)
    if sep_match:
        insert_at = sep_match.end()
        return content[:insert_at] + "\n" + new_section + content[insert_at:]

    return content.rstrip() + "\n" + new_section


# ---------------------------------------------------------------------------
# Reminders (REMINDERS.md)
# ---------------------------------------------------------------------------

_REMINDER_RE = re.compile(
    r"^-\s+(\d{4}-\d{2}-\d{2})\s*\|\s*([^|]+?)\s*\|\s*(.+?)\s*$",
    re.MULTILINE,
)
_STRIKETHROUGH_RE = re.compile(r"^-\s+~~", re.MULTILINE)


def parse_reminders(content: str) -> list[dict]:
    """Parse reminder lines from REMINDERS.md.

    Format: `- YYYY-MM-DD | CATEGORY | Text`

    Skips completed (~~strikethrough~~) lines.

    Returns list of dicts: {date: str, category: str, text: str}
    """
    reminders = []
    for line in content.splitlines():
        stripped = line.strip()
        # Skip completed reminders
        if stripped.startswith("- ~~"):
            continue
        m = _REMINDER_RE.match(stripped)
        if m:
            reminders.append(
                {
                    "date": m.group(1),
                    "category": m.group(2).strip(),
                    "text": m.group(3).strip(),
                }
            )
    return reminders
