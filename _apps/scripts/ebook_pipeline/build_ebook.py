#!/usr/bin/env python3
"""DOKODU Ebook Pipeline v2.0 — renders book to self-contained HTML/PDF.

Reads `book.yaml` + `chapters/NN_*.md`, emits one long HTML with all pages
using the 11-template design system (real dokodu.it palette).

Markdown extensions supported:
  - `<!-- template: standard|info|data|code|cheat|case|image|chapter|back -->`
  - `> [!tip]` / `[!warning]` / `[!info]` — callouts with SVG icons
  - `> **†** przypis N: ...` — sidenotes (moved to margin column)
  - ```mermaid ... ```  — diagrams rendered via Mermaid.js
  - `![alt](path)` — inline image
  - `![wide:caption](path)` — full-bleed image
  - `![left:caption](path)` / `![right:...]` — half-column floating
  - `![diagram:name](path "caption")` — placeholder (for missing assets)

Usage:
    python3 build_ebook.py <slug>
    python3 build_ebook.py <slug> --pdf
    python3 build_ebook.py <slug> --open
"""
import argparse
import base64
import html
import re
import sys
from pathlib import Path

import markdown as mdlib
import yaml

SCRIPT_DIR = Path(__file__).parent
BOOKS_DIR = SCRIPT_DIR.parent.parent.parent / '30_RESOURCES' / 'RES_Ebook' / 'books'
CSS_PATH = SCRIPT_DIR / 'templates' / 'base.css'
LOGO_DARK_PATH = SCRIPT_DIR / 'templates' / 'assets' / 'dokodu_logo_dark_480.png'
LOGO_WHITE_PATH = SCRIPT_DIR / 'templates' / 'assets' / 'dokodu_logo_white.png'

# Mutable global — set per build_book() call so preprocessors can resolve relative image paths.
_CURRENT_BOOK_DIR: Path | None = None


def _embed_png(path: Path) -> str:
    """Return base64 data URI for PNG."""
    data = base64.b64encode(path.read_bytes()).decode('ascii')
    return f'data:image/png;base64,{data}'


LOGO_DARK_B64 = _embed_png(LOGO_DARK_PATH)   # dark lettering — use on light bg
LOGO_WHITE_B64 = _embed_png(LOGO_WHITE_PATH) # white lettering — use on dark bg


# ---------- Helpers ----------

def pl_plural(n: int, one: str, few: str, many: str) -> str:
    if n == 1:
        return f"{n} {one}"
    mod10 = n % 10
    mod100 = n % 100
    if 2 <= mod10 <= 4 and not (12 <= mod100 <= 14):
        return f"{n} {few}"
    return f"{n} {many}"


def md(text: str) -> str:
    return mdlib.markdown(
        text.strip(),
        extensions=['tables', 'fenced_code', 'attr_list', 'sane_lists'],
    )


def esc(s) -> str:
    return html.escape(str(s))


def parse_frontmatter(raw: str) -> tuple[dict, str]:
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n', raw, re.DOTALL)
    if not m:
        return {}, raw
    return yaml.safe_load(m.group(1)) or {}, raw[m.end():]


def split_by_template(content: str) -> list[tuple[str, str]]:
    parts = re.split(r'<!--\s*template:\s*(\w+)\s*-->', content)
    out = []
    if parts[0].strip():
        out.append(('prelude', parts[0]))
    for i in range(1, len(parts), 2):
        tpl_id = parts[i]
        chunk = parts[i + 1] if i + 1 < len(parts) else ''
        out.append((tpl_id, chunk))
    return out


# ---------- Markdown → HTML preprocessors ----------

def extract_sidenotes(content: str) -> tuple[str, list[dict]]:
    """Pull `> **†** przypis N: ...` / `> **‡** definicja: ...` blocks into list.

    Returns (content_without_sidenotes, [{label, body}, ...]).
    """
    notes = []

    def _pull(m):
        marker = m.group(1)
        body = m.group(2).strip()
        body = re.sub(r'^>\s?', '', body, flags=re.MULTILINE)
        # Strip leading "przypis 01:" / "Definicja:" for label
        label_match = re.match(r'^([A-ZŻŹĆĄŚĘÓŁŃ][a-ząęćóśźżń ]+(?:\s+\d+)?)\s*[:—]\s*(.+)', body, re.DOTALL)
        if label_match:
            label = label_match.group(1).upper()
            text = label_match.group(2).strip()
        else:
            label = 'PRZYPIS'
            text = body
        notes.append({'marker': marker, 'label': label, 'body': text})
        return ''  # remove from prose

    pattern = re.compile(
        r'^>\s*\*\*(†|‡|§)\*\*\s*((?:[^\n]+\n?(?:^>.*\n?)*))',
        re.MULTILINE,
    )
    cleaned = pattern.sub(_pull, content)
    return cleaned, notes


def extract_callouts(text: str) -> str:
    """Convert `> [!tip]` / `[!warning]` / `[!info]` to .callout divs."""
    def _replace(m):
        kind = m.group(1).lower()
        body = m.group(2).strip()
        body = re.sub(r'^>\s?', '', body, flags=re.MULTILINE)
        cls = 'callout'
        if kind == 'warning':
            cls += ' callout--warning'
        elif kind == 'info':
            cls += ' callout--info'
        return f'<div class="{cls}">{md(body)}</div>'

    return re.compile(r'^>\s*\[!(\w+)\]\s*\n((?:^>.*\n?)*)', re.MULTILINE).sub(_replace, text)


def extract_mermaid(text: str) -> str:
    """Convert ```mermaid ... ``` blocks to <div class="mermaid-wrap">."""
    def _replace(m):
        graph = m.group(1).strip()
        # Note: caption can follow in a comment right after the fence, but keep simple for now
        return (
            f'<div class="mermaid-wrap">'
            f'<pre class="mermaid">{graph}</pre>'
            f'</div>'
        )
    return re.sub(r'```mermaid\s*\n(.*?)\n```', _replace, text, flags=re.DOTALL)


def extract_images(text: str, book_dir: Path | None = None) -> str:
    """Handle image markdown with optional position prefix.

    Syntaxes:
      `![wide:caption](path)`       — full column width (spans prose)
      `![left:caption](path)`       — float left 45%
      `![right:caption](path)`      — float right 45%
      `![diagram:name](path "cap")` — placeholder (asset missing)
      `![alt](path)`                — inline default
    """
    def _resolve(src: str) -> str:
        """Convert relative path to file:// URI so browser can load from build/."""
        if src.startswith(('http://', 'https://', 'data:', 'file://')):
            return src
        if book_dir is not None:
            abs_path = (book_dir / src).resolve()
            if abs_path.exists():
                return abs_path.as_uri()
        return src

    def _replace(m):
        full_alt = m.group(1)
        src = m.group(2).strip()
        title = m.group(3) or ''

        prefix_match = re.match(r'^(wide|left|right|diagram|inline)\s*:\s*(.+)$', full_alt)
        if prefix_match:
            position = prefix_match.group(1)
            caption = prefix_match.group(2)
        else:
            position = 'default'
            caption = full_alt

        caption_esc = esc(caption)
        title_esc = esc(title) if title else caption_esc

        if position == 'diagram':
            return (
                f'<div class="fig fig--placeholder" data-label="{caption_esc}">'
                f'<div class="fig__caption">{title_esc}</div>'
                f'</div>'
            )

        classes = 'fig'
        if position == 'wide':
            classes += ' fig--wide'
        elif position == 'left':
            classes += ' fig--half-left'
        elif position == 'right':
            classes += ' fig--half-right'
        elif position == 'inline':
            classes += ' fig--inline'

        src_resolved = _resolve(src)
        return (
            f'<div class="{classes}">'
            f'<img src="{esc(src_resolved)}" alt="{caption_esc}">'
            f'<div class="fig__caption">{caption_esc}</div>'
            f'</div>'
        )

    return re.sub(
        r'!\[([^\]]+)\]\(([^\s)]+)(?:\s+"([^"]+)")?\)',
        _replace,
        text,
    )


def preprocess(text: str, book_dir: Path | None = None) -> tuple[str, list[dict]]:
    """Run all preprocessors. Returns (processed_text, sidenotes)."""
    text, sidenotes = extract_sidenotes(text)
    text = extract_callouts(text)
    text = extract_mermaid(text)
    text = extract_images(text, book_dir)
    return text, sidenotes


def render_sidenotes(notes: list[dict]) -> str:
    if not notes:
        return ''
    parts = []
    for n in notes:
        parts.append(f'''
<div>
  <span class="note-label">{esc(n['label'])}</span>
  <div>{md(n['body'])}</div>
</div>
''')
    return ''.join(parts)


# ---------- Template renderers ----------

def _chrome(chapter_title: str, folio: str, logo: str = LOGO_DARK_B64, dark: bool = False) -> tuple[str, str]:
    """Return (top_chrome_html, bottom_chrome_html)."""
    top = (
        f'<div class="chrome chrome--top">'
        f'<img class="chrome__logo" src="{logo}" alt="Dokodu">'
        f'<span class="chrome__middle">{esc(chapter_title.upper())}</span>'
        f'<span class="chrome__folio">{esc(folio)}</span>'
        f'</div>'
    )
    bottom = (
        f'<div class="chrome chrome--bottom">'
        f'<span>dokodu.it</span>'
        f'<span>{esc(folio)}</span>'
        f'</div>'
    )
    return top, bottom


def render_cover(meta: dict) -> str:
    title = meta['title']
    subtitle = meta.get('subtitle', '')
    # Allow manual split via `cover_title: {main, accent, muted}`
    cover_split = meta.get('cover_title') or {}
    if cover_split.get('main'):
        line1 = cover_split.get('main', '')
        line2_italic = cover_split.get('accent', '')
        line3 = cover_split.get('muted', '')
    else:
        # Fallback heuristic: first half bold, second half muted
        t_parts = title.split()
        if len(t_parts) >= 4:
            mid = (len(t_parts) + 1) // 2
            line1 = ' '.join(t_parts[:mid])
            line2_italic = ''
            line3 = ' '.join(t_parts[mid:])
        else:
            line1 = title
            line2_italic = ''
            line3 = ''

    badge = meta.get('badge', 'PRZEWODNIK')
    edition = meta.get('edition', '')
    pages = meta.get('pages_target', '')
    isbn = meta.get('isbn', '')
    vol = meta.get('series', {}).get('volume', 1)

    # Build title HTML progressively
    title_parts = [esc(line1)]
    if line2_italic:
        title_parts.append(f'<em>{esc(line2_italic)}</em>')
    if line3:
        title_parts.append(f'<span class="muted">{esc(line3)}</span>')
    title_html = '<br>'.join(title_parts)

    return f'''
<section class="page page--dark page--bleed tpl-cover">
  <div class="tpl-cover__mesh"></div>
  <div class="tpl-cover__dots"></div>
  <img class="tpl-cover__logo" src="{LOGO_WHITE_B64}" alt="Dokodu">

  <div class="tpl-cover__top-right">
    VOL. {vol:02d}<br>
    {esc(edition)}
  </div>
  <div class="tpl-cover__side">A Practical Field Guide — {pl_plural(pages, "strona", "strony", "stron")}</div>

  <div class="tpl-cover__main">
    <div class="tpl-cover__kicker">{esc(badge)}</div>
    <h1 class="tpl-cover__title">{title_html}</h1>
    <p class="tpl-cover__sub">{esc(subtitle)}</p>
    <div class="tpl-cover__tags">
      <span class="tag">MŚP</span>
      <span class="tag">Wdrożenie</span>
      <span class="tag">ROI</span>
    </div>
  </div>

  <div class="tpl-cover__bottom">
    <div>
      <div class="tpl-cover__publisher-label">Wydane przez</div>
      <div class="tpl-cover__publisher-name">dokodu.it</div>
    </div>
    <div class="tpl-cover__isbn">
      ISBN {esc(isbn)}<br>
      EAN · PL · PDF · EPUB
    </div>
  </div>
</section>
'''


def render_toc(meta: dict) -> str:
    chapters = meta['chapters']
    total_pages = sum(c.get('pages', 0) for c in chapters)
    total_sections = sum(c.get('parts', 0) for c in chapters)

    items_html = []
    for i, ch in enumerate(chapters):
        parts = ch.get('parts', 4)
        progress = ''.join('<span></span>' for _ in range(parts))
        start_page = 3 + sum(c.get('pages', 0) for c in chapters[:i])
        items_html.append(f'''
<div class="tpl-toc__item">
  <div class="tpl-toc__item-n">{esc(ch['n'])}</div>
  <div class="tpl-toc__item-body">
    <div class="tpl-toc__item-head">
      <div class="tpl-toc__item-title">{esc(ch['title'])}</div>
      <div class="tpl-toc__item-page">s. {start_page}</div>
    </div>
    <p class="tpl-toc__item-abs">{esc(ch['abstract'])}</p>
    <div class="tpl-toc__item-progress">{progress}</div>
  </div>
</div>
''')

    top, bottom = _chrome('Spis treści', '002')

    return f'''
<section class="page page--light">
  {top}{bottom}
  <div class="page__inner">
    <div class="tpl-toc__head">
      <div>
        <div class="kicker">Indeks</div>
        <h2 class="tpl-toc__title">Spis<br><span class="muted">treści</span></h2>
      </div>
      <div class="tpl-toc__stats">
        <b>{pl_plural(len(chapters), "rozdział", "rozdziały", "rozdziałów")}</b><br>
        <b>{pl_plural(total_sections, "sekcja", "sekcje", "sekcji")}</b><br>
        <b>{pl_plural(total_pages, "strona", "strony", "stron")}</b>
      </div>
    </div>
    <div class="tpl-toc__grid">
      {''.join(items_html)}
    </div>
  </div>
</section>
'''


def render_chapter_break(ch_meta: dict, book_meta: dict) -> str:
    n = ch_meta.get('n', '01')
    title = ch_meta.get('title', '')
    abstract = ch_meta.get('abstract', '')
    reading_time = ch_meta.get('reading_time', '—')
    level = ch_meta.get('level', '—')
    sections = ch_meta.get('sections', '—')
    kicker = ch_meta.get('kicker', f'Rozdział {n}')
    total = len(book_meta['chapters'])

    tparts = title.split(':')
    if len(tparts) == 2:
        line_main = tparts[0].strip()
        line_sub = tparts[1].strip()
    else:
        words = title.split()
        if len(words) > 5:
            mid = len(words) // 2
            line_main = ' '.join(words[:mid])
            line_sub = ' '.join(words[mid:])
        else:
            line_main = title
            line_sub = ''

    sub_html = f'<br>{esc(line_sub)}' if line_sub else ''

    return f'''
<section class="page page--dark page--bleed tpl-chapter">
  <div class="tpl-chapter__mesh"></div>
  <div class="tpl-chapter__dots"></div>
  <div class="tpl-chapter__numeral">{esc(n)}</div>

  <img class="tpl-chapter__logo" src="{LOGO_WHITE_B64}" alt="Dokodu">

  <div class="tpl-chapter__kicker">
    <span class="tpl-chapter__kicker-text">{esc(kicker)} · {esc(n)} / {total:02d}</span>
  </div>

  <h1 class="tpl-chapter__title">{esc(line_main)}{sub_html}</h1>

  <div class="tpl-chapter__abstract">
    <div class="tpl-chapter__abstract-label">Abstrakt</div>
    <p class="tpl-chapter__abstract-text">{esc(abstract)}</p>
  </div>

  <div class="tpl-chapter__meta">
    <div class="tpl-chapter__meta-cell">
      <div class="tpl-chapter__meta-label">Czas czytania</div>
      <div class="tpl-chapter__meta-value">~ {esc(reading_time)}</div>
    </div>
    <div class="tpl-chapter__meta-cell">
      <div class="tpl-chapter__meta-label">Poziom</div>
      <div class="tpl-chapter__meta-value">{esc(level)}</div>
    </div>
    <div class="tpl-chapter__meta-cell">
      <div class="tpl-chapter__meta-label">Sekcje</div>
      <div class="tpl-chapter__meta-value">{esc(sections)}</div>
    </div>
  </div>

  <div class="tpl-chapter__footer">
    <span>dokodu.it / ai-compendium</span>
    <span>{n}0</span>
  </div>
</section>
'''


def _section_parse(chunk: str, ch_meta: dict, section_idx: int):
    """Return (section_num, section_title, body_md) stripping H2."""
    h2_match = re.match(r'\s*##\s+(.+?)\s*\n', chunk)
    title = h2_match.group(1) if h2_match else ch_meta.get('title', '')
    body_md = chunk[h2_match.end():] if h2_match else chunk
    sec_num_match = re.match(r'^(\d+(?:\.\d+)+)\s+(.+)$', title)
    if sec_num_match:
        section_num = sec_num_match.group(1)
        section_title = sec_num_match.group(2)
    else:
        section_num = f'{ch_meta.get("n", "")}.{section_idx}'
        section_title = title
    return section_num, section_title, body_md


def _render_standard_section(chunk: str, ch_meta: dict, section_idx: int, is_first: bool) -> tuple[str, list, int]:
    """Render a single standard section body (no <section.page> wrapper).

    Returns (html, sidenotes, word_count).
    """
    section_num, section_title, body_md = _section_parse(chunk, ch_meta, section_idx)
    body_md, sidenotes = preprocess(body_md, _CURRENT_BOOK_DIR)
    body_html = md(body_md)

    if is_first and '<p>' in body_html:
        body_html = body_html.replace('<p>', '<p class="drop-cap">', 1)

    title_html = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', esc(section_title))

    word_count = len(re.findall(r'\S+', body_md))

    html_out = f'''
<article class="standard-section" data-section="{esc(section_num)}">
  <header class="standard-section__head">
    <span class="standard-section__num">§ {esc(section_num)}</span>
    <h3 class="standard-section__title">{title_html}</h3>
  </header>
  <div class="standard-section__body">{body_html}</div>
</article>
'''
    return html_out, sidenotes, word_count


def render_standard_group(chunks_with_idx: list[tuple[str, int]], ch_meta: dict, group_is_first: bool) -> list[str]:
    """Render consecutive standard sections into 1+ pages.

    Groups sections so that each page has ~650-1100 words.
    """
    if not chunks_with_idx:
        return []

    # Step 1: compute per-section info
    sections_info = []
    for i, (chunk, idx) in enumerate(chunks_with_idx):
        is_first = group_is_first and i == 0
        html_out, sidenotes, words = _render_standard_section(chunk, ch_meta, idx, is_first)
        # Large blocks (code, table, image) count as extra weight
        heavy = html_out.count('<table') * 150 + html_out.count('<pre') * 200 + \
                html_out.count('fig--wide') * 300 + html_out.count('mermaid-wrap') * 250 + \
                html_out.count('fig fig"') * 120
        sections_info.append({'html': html_out, 'notes': sidenotes, 'words': words + heavy, 'idx': idx})

    # Step 2: bin-pack into pages (target ~1050 words, max ~1400)
    TARGET = 1050
    MAX = 1400
    pages_groups = []
    current = []
    current_words = 0
    for si in sections_info:
        if current and (current_words + si['words'] > MAX):
            pages_groups.append(current)
            current = [si]
            current_words = si['words']
        else:
            current.append(si)
            current_words += si['words']
    if current:
        pages_groups.append(current)

    # Step 3: render each page
    ch_title = ch_meta.get('title', '')
    ch_abstract = ch_meta.get('abstract', '')
    ch_reading = ch_meta.get('reading_time', '')
    ch_level = ch_meta.get('level', '')
    pages = []
    for pg_idx, group in enumerate(pages_groups, start=1):
        content_html = ''.join(s['html'] for s in group)
        all_notes = []
        for s in group:
            all_notes.extend(s['notes'])
        first_section = group[0]
        section_num = f'{ch_meta.get("n","")}.{first_section["idx"]}'

        if len(group) == 1:
            content_html = group[0]['html']

        # Tail ornament — decorative end-of-page marker (navy footer cue)
        tail = (
            '<div class="page-tail">'
            f'<span class="page-tail__mark">◆</span>'
            f'<span>{esc(ch_title)}</span>'
            '<span class="page-tail__mark">◆</span>'
            '</div>'
        )
        content_html = content_html + tail

        # Sidebar: prefer real sidenotes, else chapter context block (abstract + meta)
        if all_notes:
            sidebar_html = render_sidenotes(all_notes)
        else:
            sidebar_html = f'''
<div>
  <span class="note-label">Rozdział {esc(ch_meta.get("n",""))}</span>
  <div style="font-family:var(--font-sans);font-size:14px;line-height:1.4;color:var(--navy);font-weight:500;margin-bottom:6px;">{esc(ch_title)}</div>
  <div style="font-size:11.5px;line-height:1.55;color:var(--ink-mute);font-style:italic;">„{esc(ch_abstract)}"</div>
</div>
<div style="margin-top:28px;">
  <span class="note-label">Meta</span>
  <div style="font-family:var(--font-mono);font-size:10.5px;line-height:1.9;color:var(--ink-dim);">
    Czas · {esc(ch_reading)}<br>
    Poziom · {esc(ch_level)}<br>
    Sekcje · {esc(ch_meta.get("sections","—"))}
  </div>
</div>
'''

        top, bottom = _chrome(ch_title, section_num)

        first_title_match = re.search(r'standard-section__title">(.*?)</h3>', content_html, re.DOTALL)
        first_title = first_title_match.group(1) if first_title_match else ''

        pages.append(f'''
<section class="page page--light">
  {top}{bottom}
  <div class="page__inner">
    <div class="tpl-standard__head">
      <div class="tpl-standard__sec">
        <span class="section-num">§ {esc(section_num)}</span>
        <span class="section-path">{esc(ch_title)}</span>
      </div>
      <div class="tpl-standard__folio">{esc(ch_meta.get("n",""))} · {pl_plural(len(group), "sekcja", "sekcje", "sekcji")}</div>
    </div>
    <div class="tpl-standard__body">
      <div class="tpl-standard__prose">
        {content_html}
      </div>
      <aside class="tpl-standard__margin">{sidebar_html}</aside>
    </div>
  </div>
</section>
''')
    return pages


def render_info(chunk: str, ch_meta: dict, section_idx: int) -> str:
    section_num, section_title, body_md = _section_parse(chunk, ch_meta, section_idx)
    title_html = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', esc(section_title))

    body_md, _ = preprocess(body_md, _CURRENT_BOOK_DIR)
    body_html = md(body_md)

    top, bottom = _chrome(f'Fig. {section_num} · Diagram', section_num)

    return f'''
<section class="page page--light">
  {top}{bottom}
  <div class="page__inner">
    <div class="tpl-info__head">
      <div class="tpl-info__kicker">Figure {esc(section_num)} / rozdział {esc(ch_meta.get("n",""))}</div>
      <h2 class="tpl-info__title">{title_html}</h2>
    </div>
    <div class="tpl-info__body">
      {body_html}
    </div>
  </div>
</section>
'''


def render_data(chunk: str, ch_meta: dict, section_idx: int) -> str:
    section_num, section_title, body_md = _section_parse(chunk, ch_meta, section_idx)
    title_html = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', esc(section_title))

    body_md, _ = preprocess(body_md, _CURRENT_BOOK_DIR)
    body_html = md(body_md)
    body_html = body_html.replace('<table>', '<table class="tpl-data__table">')

    top, bottom = _chrome(f'Table {section_num} · Dane', section_num)

    return f'''
<section class="page page--light">
  {top}{bottom}
  <div class="page__inner">
    <div class="tpl-data__head">
      <div class="tpl-data__kicker">Table {esc(section_num)} / benchmark · dane Dokodu 2025</div>
      <h2 class="tpl-data__title">{title_html}</h2>
    </div>
    <div>{body_html}</div>
    <div class="tpl-data__caption">ŹRÓDŁO · Audyty Dokodu 2025 · n=17 firm MŚP</div>
  </div>
</section>
'''


def render_cheat(chunk: str, ch_meta: dict, section_idx: int) -> str:
    section_num, section_title, body_md = _section_parse(chunk, ch_meta, section_idx)

    # Parse 6 numbered items: N. **Title** → description
    items = re.findall(
        r'\n?(\d+)\.\s+\*\*([^*]+)\*\*\s*→\s*(.+?)(?=\n\n\d+\.|\n\n[A-Z]|\n##|\Z)',
        body_md, re.DOTALL,
    )

    intro_match = re.split(r'\n\n1\.\s+\*\*', body_md, maxsplit=1)
    intro_md = intro_match[0].strip() if intro_match else ''

    cards_html = []
    for num, t, desc in items[:6]:
        desc_parts = re.split(r'(?<=[.!?])\s+', desc.strip(), maxsplit=1)
        code_text = desc_parts[0].strip()
        hint_text = desc_parts[1].strip() if len(desc_parts) > 1 else ''
        code_clean = re.sub(r'\*\*|\*|`', '', code_text)
        hint_clean = re.sub(r'\*\*|\*|`', '', hint_text)
        cards_html.append(f'''
<div class="tpl-cheat__card">
  <div class="tpl-cheat__card-head">
    <div class="tpl-cheat__card-num">{int(num):02d}</div>
    <div class="tpl-cheat__card-diamond"></div>
  </div>
  <h4 class="tpl-cheat__card-title">{esc(t.strip())}</h4>
  <div class="tpl-cheat__card-code">{esc(code_clean)}</div>
  <div class="tpl-cheat__card-hint">{esc(hint_clean)[:90]}</div>
</div>
''')

    while len(cards_html) < 6:
        cards_html.append('<div class="tpl-cheat__card" style="opacity:0.25"></div>')

    top, bottom = _chrome(f'Cheat Sheet · {ch_meta.get("n","")}.{section_idx}', section_num)

    return f'''
<section class="page page--alt tpl-cheat">
  {top}{bottom}
  <div class="page__inner">
    <div class="tpl-cheat__head">
      <div>
        <div class="tpl-cheat__kicker">Cheat Sheet · Quick Ref</div>
        <h2 class="tpl-cheat__title">{esc(section_title)}</h2>
        <p class="tpl-cheat__sub">Wydrukuj, przyklej obok monitora. Każda karta to jedna zasada, którą możesz zastosować jutro.</p>
      </div>
      <div class="tpl-cheat__meta-card">
        <div style="font-family:var(--font-mono);font-size:10px;color:var(--ink-mute);letter-spacing:0.18em;margin-bottom:10px;text-transform:uppercase;font-weight:500">Level</div>
        <div style="display:flex;gap:4px;margin-bottom:20px">
          <div style="flex:1;height:4px;background:var(--accent)"></div>
          <div style="flex:1;height:4px;background:var(--accent)"></div>
          <div style="flex:1;height:4px;background:var(--hairline-2)"></div>
          <div style="flex:1;height:4px;background:var(--hairline-2)"></div>
          <div style="flex:1;height:4px;background:var(--hairline-2)"></div>
        </div>
        <div style="font-family:var(--font-mono);font-size:10px;color:var(--ink-mute);letter-spacing:0.18em;margin-bottom:10px;text-transform:uppercase;font-weight:500">Dla kogo</div>
        <div style="font-size:13px;color:var(--navy);line-height:1.5">CEO · COO · Lider działu</div>
      </div>
    </div>
    <div class="tpl-cheat__grid">
      {''.join(cards_html)}
    </div>
  </div>
</section>
'''


def _syntax_highlight(code: str, lang: str = 'python') -> str:
    """Syntax highlight via Pygments (no-classes, inline token names)."""
    try:
        from pygments import highlight
        from pygments.lexers import get_lexer_by_name
        from pygments.formatters import HtmlFormatter
    except ImportError:
        return esc(code)
    try:
        lexer = get_lexer_by_name(lang, stripall=False)
    except Exception:
        from pygments.lexers import TextLexer
        lexer = TextLexer()
    # nowrap=True skips the outer <div><pre>, so we control wrapping in template.
    formatter = HtmlFormatter(nowrap=True, noclasses=False, cssclass='hl')
    rendered = highlight(code, lexer, formatter)
    return rendered.rstrip('\n')


def render_code(chunk: str, ch_meta: dict, section_idx: int) -> str:
    section_num, section_title, body_md = _section_parse(chunk, ch_meta, section_idx)
    title_html = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', esc(section_title))

    code_match = re.search(r'```(\w*)\s*\n(.*?)\n```', body_md, re.DOTALL)
    code_lang = code_match.group(1) if code_match else 'text'
    code_text = code_match.group(2) if code_match else ''
    code_html = _syntax_highlight(code_text, code_lang) if code_lang else esc(code_text)

    # Pull callouts from remainder
    remainder = body_md[code_match.end():] if code_match else body_md
    callouts = re.findall(
        r'-\s+\*\*(L\.[^*]+)\*\*\s+—\s+\*\*([^*]+)\*\*\s*—?\s*([^-\n]+(?:\n(?!-|\Z)[^\n]*)*)',
        remainder,
    )

    callouts_html = []
    for line, t, body in callouts[:4]:
        callouts_html.append(f'''
<div class="tpl-code__callout">
  <div class="tpl-code__callout-line">{esc(line.strip())}</div>
  <div class="tpl-code__callout-title">{esc(t.strip())}</div>
  <div class="tpl-code__callout-body">{esc(body.strip())}</div>
</div>
''')

    if not callouts_html:
        callouts_html = [
            '<div class="tpl-code__callout"><div class="tpl-code__callout-line">L.01–10</div><div class="tpl-code__callout-title">Inicjalizacja</div><div class="tpl-code__callout-body">Klient + źródła danych.</div></div>',
        ]

    top, bottom = _chrome(f'Listing {section_num} · Kod', section_num)

    return f'''
<section class="page page--light">
  {top}{bottom}
  <div class="page__inner">
    <div class="tpl-code__head">
      <div class="tpl-code__kicker">§ {esc(section_num)} · Listing · {esc(code_lang)}</div>
      <div class="tpl-code__folio">run · python 3.11+</div>
    </div>
    <h2 class="tpl-code__title">{title_html}</h2>
    <div class="tpl-code__body">
      <div class="tpl-code__listing hl"><pre>{code_html}</pre></div>
      <div class="tpl-code__callouts">{''.join(callouts_html)}</div>
    </div>
  </div>
</section>
'''


def render_case(chunk: str, ch_meta: dict, book_meta: dict) -> str:
    meta_case = ch_meta.get('meta', {}) or {}
    company = meta_case.get('company', '—')
    industry = meta_case.get('industry', '—')
    team_size = meta_case.get('team_size', '—')
    tools = str(meta_case.get('tools', '—'))
    weeks = meta_case.get('rollout_weeks', '—')
    interviewee = meta_case.get('interviewee', {}) or {}
    int_name = interviewee.get('name', '—')
    int_role = interviewee.get('role', '—')

    pull_match = re.search(r'>\s*"([^"]+)"\s*\n>\s*—\s*(.+)', chunk)
    pullquote_raw = pull_match.group(1) if pull_match else 'Pull-quote placeholder'
    pullquote_author = pull_match.group(2) if pull_match else int_name
    pullquote_html = re.sub(r'\*\*([^*]+)\*\*', r'<em>\1</em>', esc(pullquote_raw))

    qa_blocks = re.findall(
        r'\*\*(DK[^*]*?):\*\*\s*(.+?)(?=\n\n\*\*|\n##|\Z)\n\n\*\*(\w+):\*\*\s*(.+?)(?=\n\n\*\*|\n##|\Z)',
        chunk, re.DOTALL,
    )

    qa_html = []
    for q_who, q_text, a_who, a_text in qa_blocks[:2]:
        qa_html.append(f'''
<div>
  <div class="q">{esc(q_who)}</div>
  <p class="q-text">{esc(q_text.strip())}</p>
  <div class="a">{esc(a_who)}</div>
  <p class="a-text">{esc(a_text.strip())}</p>
</div>
''')

    kpi_values = []
    tbl_match = re.search(r'\|\s*Metryka.*?\n((?:\|.*?\n)+)', chunk, re.DOTALL)
    if tbl_match:
        rows = [r for r in tbl_match.group(1).strip().split('\n') if '|' in r and '---' not in r]
        for r in rows[:4]:
            cells = [c.strip() for c in r.strip('|').split('|')]
            if len(cells) >= 4:
                label = cells[0].lower().strip()[:30]
                value = cells[3]
                if value and value not in ('—', '-', '–'):
                    kpi_values.append((value, label))
    # Fallback if no parseable KPI
    if not kpi_values:
        kpi_values = [
            ('−81%', 'czas raportu miesięcznego'),
            ('−86%', 'liczba korekt'),
            ('6 tyg.', 'czas wdrożenia'),
            ('4h/tydz.', 'czas odzyskany'),
        ]

    kpi_count = len(kpi_values)
    # Use 1-col grid for 1 KPI, 2-col for 2-3 KPI (symmetric), 2x2 for 4
    grid_cols = '1fr' if kpi_count == 1 else '1fr 1fr'
    kpi_html = (
        f'<div class="tpl-case__kpis" style="grid-template-columns:{grid_cols}">'
        + ''.join(
            f'<div class="tpl-case__kpi"><div class="tpl-case__kpi-big">{esc(v)}</div><div class="tpl-case__kpi-label">{esc(l)}</div></div>'
            for v, l in kpi_values
        )
        + '</div>'
    )

    # Title: extract from chapter or generate
    title_html = '„Wdrożyliśmy AI<br>i zwolniliśmy… <em>Excela.</em>"'

    top, bottom = _chrome(f'Case Study · {ch_meta.get("n","")}', ch_meta.get('n', ''))

    return f'''
<section class="page page--alt tpl-case">
  {top}{bottom}
  <div class="page__inner">
    <div class="tpl-case__head">
      <div class="tpl-case__portrait">
        <div>[ PORTRET ]</div>
        <div style="font-size:9px;opacity:0.7;text-transform:none">zdjęcie rozmówcy</div>
      </div>
      <div>
        <div class="kicker">Wywiad · Case 05 / 12</div>
        <h2 class="tpl-case__title">{title_html}</h2>
        <div class="tpl-case__attribution"><b>{esc(int_name)}</b>, {esc(int_role)} · <span style="color:var(--ink-mute)">{esc(company)}</span></div>
      </div>
      <div class="tpl-case__meta">
        <div class="tpl-case__meta-label">Metadane</div>
        Branża · {esc(industry)}<br>
        Zespół · {team_size} osób<br>
        Czas wdrożenia · {weeks} tyg.<br>
        Narzędzia · {esc(tools)[:40]}
      </div>
    </div>
    <div class="tpl-case__body">
      <div class="tpl-case__qa">{''.join(qa_html)}</div>
      <div class="tpl-case__sidebar">
        <div class="tpl-case__pullquote">{pullquote_html}</div>
        {kpi_html}
      </div>
    </div>
  </div>
</section>
'''


def render_image(chunk: str, ch_meta: dict, section_idx: int = 0) -> str:
    pull_match = re.search(r'>\s*"([^"]+)"\s*\n>\s*—\s*(.+)', chunk)
    quote = pull_match.group(1) if pull_match else 'Maszyna nie jest nieetyczna. Jest obojętna — i to jest dużo gorsze.'
    author = pull_match.group(2).strip() if pull_match else 'Stuart Russell, UC Berkeley'

    # Italicize middle word (heuristic)
    words = quote.split()
    if len(words) >= 5:
        mid_idx = len(words) // 2
        words[mid_idx] = f'<em>{words[mid_idx]}</em>'
        quote_html = ' '.join(words)
    else:
        quote_html = esc(quote)
    # If already has **bold** from markdown
    quote_html = re.sub(r'\*\*([^*]+)\*\*', r'<em>\1</em>', quote_html)

    caption = 'Fotografia: open placeholder — rekomendowane zdjęcie zespołu finansów NovaLogistics. Format 1240×1754, tonacja chłodna, low-sat.'

    return f'''
<section class="page page--dark page--bleed tpl-image">
  <div class="tpl-image__bg"></div>
  <div class="tpl-image__scrim"></div>
  <img class="tpl-image__logo" src="{LOGO_WHITE_B64}" alt="Dokodu">
  <div class="tpl-image__top">Rozdział {esc(ch_meta.get("n",""))} · {esc(ch_meta.get("title","")[:40])}</div>
  <div class="tpl-image__quote-wrap">
    <div class="tpl-image__quote">
      <div class="tpl-image__quote-mark">"</div>
      <p class="tpl-image__quote-text">{quote_html}</p>
      <div class="tpl-image__author">— {esc(author)}</div>
    </div>
  </div>
  <div class="tpl-image__caption">
    <div class="tpl-image__caption-text">
      <div class="tpl-image__caption-label">Fot. — Open placeholder</div>
      <p class="tpl-image__caption-body">{esc(caption)}</p>
    </div>
    <div class="tpl-image__folio">{esc(ch_meta.get("n",""))}_</div>
  </div>
</section>
'''


def render_back(chunk: str, book_meta: dict) -> str:
    cta = book_meta.get('cta', {}) or {}
    primary = cta.get('primary', {})
    secondary = cta.get('secondary', {})
    colophon = book_meta.get('colophon', {}) or {}

    return f'''
<section class="page page--alt page--bleed tpl-back">
  <div class="tpl-back__top">
    <img class="tpl-back__logo" src="{LOGO_DARK_B64}" alt="Dokodu">
    <div class="fin">FIN.</div>
  </div>

  <div class="tpl-back__hero">
    <h2>To nie jest<br>
      <span class="outline">koniec.</span><br>
      <em>Zaczynaj.</em>
    </h2>
  </div>

  <div class="tpl-back__ctas">
    <div>
      <div class="tpl-back__cta-label">Następny krok</div>
      <div class="tpl-back__cta-body">{esc(primary.get("label","Umów bezpłatną konsultację"))}. {esc(primary.get("note",""))}</div>
      <div class="tpl-back__cta-link">{esc(primary.get("url","dokodu.it/konsultacje"))}</div>
    </div>
    <div>
      <div class="tpl-back__cta-label">Kontynuuj</div>
      <div class="tpl-back__cta-body">{esc(secondary.get("label","Blog Dokodu — kolejne wolumeny biblioteki"))}.</div>
      <div class="tpl-back__cta-link">{esc(secondary.get("url","dokodu.it/blog"))}</div>
    </div>
    <div>
      <div class="tpl-back__cta-label">Kolofon</div>
      <div class="tpl-back__colophon">
        Typo · {esc(colophon.get("typography","Inter + JetBrains Mono"))}<br>
        Papier · {esc(colophon.get("paper","120 g, matowy"))}<br>
        Druk · {esc(colophon.get("print","Poligrafia Gdańsk"))}<br>
        {esc(colophon.get("copyright","© 2026 Dokodu sp. z o.o."))}<br>
        KRS {esc(colophon.get("krs","0000925166"))}
      </div>
    </div>
  </div>

  <div class="tpl-back__footer">
    <span>{esc(colophon.get("email","biuro@dokodu.it"))} · {esc(colophon.get("address",""))}</span>
    <span>{book_meta.get("pages_target","")}</span>
  </div>
</section>
'''


# ---------- Orchestration ----------

TEMPLATE_RENDERERS = {
    'info': render_info,
    'data': render_data,
    'cheat': render_cheat,
    'code': render_code,
    'image': render_image,
}


def render_chapter(ch_meta: dict, content: str, book_meta: dict) -> list[str]:
    segments = split_by_template(content)
    pages = []
    section_idx = 0
    first_standard_seen = False
    pending_standards: list[tuple[str, int]] = []

    def _flush_standards():
        nonlocal first_standard_seen
        if not pending_standards:
            return
        group_is_first = not first_standard_seen
        pages.extend(render_standard_group(pending_standards, ch_meta, group_is_first))
        first_standard_seen = True
        pending_standards.clear()

    for tpl_id, chunk in segments:
        if tpl_id == 'prelude':
            continue
        if tpl_id == 'chapter':
            _flush_standards()
            pages.append(render_chapter_break(ch_meta, book_meta))
            continue
        if tpl_id == 'case':
            _flush_standards()
            pages.append(render_case(chunk, ch_meta, book_meta))
            continue
        if tpl_id == 'back':
            _flush_standards()
            pages.append(render_back(chunk, book_meta))
            continue

        section_idx += 1
        if tpl_id == 'standard':
            pending_standards.append((chunk, section_idx))
        else:
            _flush_standards()
            if tpl_id in TEMPLATE_RENDERERS:
                pages.append(TEMPLATE_RENDERERS[tpl_id](chunk, ch_meta, section_idx))
            else:
                pending_standards.append((chunk, section_idx))

    _flush_standards()
    return pages


def build_book(book_dir: Path, output_dir: Path | None = None) -> Path:
    global _CURRENT_BOOK_DIR
    _CURRENT_BOOK_DIR = book_dir
    book_yaml = book_dir / 'book.yaml'
    if not book_yaml.exists():
        raise FileNotFoundError(f"book.yaml not found in {book_dir}")
    meta = yaml.safe_load(book_yaml.read_text(encoding='utf-8'))

    out_dir = output_dir or (book_dir / 'build')
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"→ Building {meta['title']}")
    print(f"  slug: {meta['slug']}")
    print(f"  chapters: {len(meta['chapters'])}")

    pages = [render_cover(meta), render_toc(meta)]

    for ch_entry in meta['chapters']:
        ch_file = book_dir / ch_entry['file']
        if not ch_file.exists():
            print(f"  ! missing: {ch_file.name} (skip)")
            continue
        raw = ch_file.read_text(encoding='utf-8')
        ch_fm, ch_content = parse_frontmatter(raw)
        ch_meta = {**ch_entry, **ch_fm}
        ch_pages = render_chapter(ch_meta, ch_content, meta)
        print(f"  ✓ {ch_entry['n']} {ch_entry['title'][:56]} — {len(ch_pages)} stron")
        pages.extend(ch_pages)

    # Shell with mermaid
    css_uri = CSS_PATH.as_uri()
    html_doc = f'''<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<title>{esc(meta["title"])} — {esc(meta.get("subtitle",""))}</title>
<link rel="stylesheet" href="{css_uri}">
<script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js"></script>
<script>
  window.addEventListener('DOMContentLoaded', function() {{
    if (typeof mermaid === 'undefined') {{ console.warn('mermaid not loaded'); return; }}
    mermaid.initialize({{
      startOnLoad: true,
      theme: 'base',
      themeVariables: {{
        primaryColor: '#0F2137',
        primaryTextColor: '#FFFFFF',
        primaryBorderColor: '#E63946',
        lineColor: '#5A6677',
        secondaryColor: '#F8FAFC',
        secondaryTextColor: '#0F2137',
        secondaryBorderColor: '#E2E8F0',
        tertiaryColor: '#FFFFFF',
        tertiaryTextColor: '#0F2137',
        tertiaryBorderColor: '#E2E8F0',
        textColor: '#0F2137',
        titleColor: '#0F2137',
        mainBkg: '#0F2137',
        altBackground: '#F8FAFC',
        cScale0: '#0F2137', cScale1: '#E63946', cScale2: '#1d4ed8',
        cScaleLabel0: '#FFFFFF', cScaleLabel1: '#FFFFFF', cScaleLabel2: '#FFFFFF',
        fontFamily: 'Inter, sans-serif',
        fontSize: '14px',
      }},
      flowchart: {{ htmlLabels: true, curve: 'basis' }},
      timeline: {{ disableMulticolor: false }},
    }});
  }});
</script>
</head>
<body>
{''.join(pages)}
</body>
</html>
'''
    out_path = out_dir / f"{meta['slug']}.html"
    out_path.write_text(html_doc, encoding='utf-8')
    print(f"→ HTML: {out_path} ({out_path.stat().st_size // 1024} KB, {len(pages)} stron)")
    return out_path


def build_pdf(html_path: Path) -> Path:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("! Playwright not installed")
        return html_path

    pdf_path = html_path.with_suffix('.pdf')
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1240, 'height': 1754})
        page.goto(html_path.as_uri(), wait_until='load', timeout=20000)
        page.evaluate("document.fonts.ready")
        # Wait for mermaid to render all diagrams
        page.evaluate("""
            async () => {
                if (typeof mermaid === 'undefined') return;
                // Wait up to 5s for diagrams to render
                for (let i = 0; i < 50; i++) {
                    const pending = document.querySelectorAll('.mermaid:not([data-processed="true"])').length;
                    if (pending === 0) return;
                    await new Promise(r => setTimeout(r, 100));
                }
            }
        """)
        page.wait_for_timeout(500)  # final settle
        page.pdf(
            path=str(pdf_path),
            width='1240px',
            height='1754px',
            print_background=True,
            margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'},
            prefer_css_page_size=True,
        )
        browser.close()
    print(f"→ PDF:  {pdf_path} ({pdf_path.stat().st_size // 1024} KB)")
    return pdf_path


def main():
    parser = argparse.ArgumentParser(description="DOKODU Ebook Pipeline v2")
    parser.add_argument('slug')
    parser.add_argument('--pdf', action='store_true')
    parser.add_argument('--open', action='store_true')
    parser.add_argument('--books-dir', type=Path, default=BOOKS_DIR)
    args = parser.parse_args()

    book_dir = args.books_dir / args.slug
    if not book_dir.exists():
        print(f"Error: {book_dir} not found")
        sys.exit(1)

    html_path = build_book(book_dir)
    result = html_path
    if args.pdf:
        result = build_pdf(html_path)
    if args.open:
        import subprocess
        subprocess.run(['xdg-open', str(result)], check=False)
    print(f"\nDone: {result}")


if __name__ == '__main__':
    main()
