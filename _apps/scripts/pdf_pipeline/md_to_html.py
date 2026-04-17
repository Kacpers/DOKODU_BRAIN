"""DOKODU Book Pipeline — Markdown to HTML converter.

Parses extended Markdown (:::component blocks) into HTML
using CSS classes from base.css. Generates auto-sections.
"""
import re
import sys
import warnings
from pathlib import Path

# Ensure sibling modules are importable regardless of CWD
sys.path.insert(0, str(Path(__file__).parent))

import markdown
import yaml

from renderers import render_component
from auto_sections import (
    generate_cover, generate_legal, generate_how_to_read,
    generate_toc, generate_chapter_opener, generate_glossary,
    generate_resources, generate_series, generate_back_cover,
)


def convert_book(book_dir: Path, css_path: str | None = None) -> str:
    """Convert a book directory to a single HTML string.

    Args:
        book_dir: Path to book directory containing book.yaml + *.md
        css_path: Path to base.css (resolved at template time)

    Returns:
        Complete HTML document string.
    """
    book_dir = Path(book_dir)

    # 1. Read book.yaml
    yaml_path = book_dir / 'book.yaml'
    if not yaml_path.exists():
        raise FileNotFoundError(f"book.yaml not found in {book_dir}")
    meta = yaml.safe_load(yaml_path.read_text(encoding='utf-8'))

    auto = meta.get('auto_sections', {})

    # 2. Find and sort chapter files
    chapter_files = sorted(book_dir.glob('[0-9]*.md'))
    if not chapter_files:
        raise FileNotFoundError(f"No chapter .md files found in {book_dir}")

    # 3. Parse all chapters
    chapters_data = []
    glossary_terms = []
    qr_items = []

    for md_file in chapter_files:
        ch_data = _parse_chapter(md_file, glossary_terms, qr_items)
        if ch_data:
            chapters_data.append(ch_data)

    # 4. Assemble HTML
    parts = []

    # Front matter
    parts.append(generate_cover(book_dir, meta))

    if auto.get('legal', False):
        parts.append(generate_legal(meta))

    if auto.get('how_to_read', False):
        parts.append(generate_how_to_read())

    # TOC
    toc_entries = [{'number': ch['meta']['chapter'], 'title': ch['meta']['title']}
                   for ch in chapters_data]
    parts.append(generate_toc(toc_entries))

    # Chapters
    for ch in chapters_data:
        parts.append(ch['html'])

    # Back matter
    if auto.get('glossary', False) and glossary_terms:
        parts.append(generate_glossary(glossary_terms))

    if auto.get('resources', False) and qr_items:
        parts.append(generate_resources(qr_items))

    series_html = generate_series(meta)
    if series_html:
        parts.append(series_html)

    back = generate_back_cover(meta)
    if back:
        parts.append(back)

    # 5. Wrap in template
    content = '\n'.join(parts)
    template = _get_template(css_path)
    return template.replace('CONTENT_PLACEHOLDER', content)


def _get_template(css_path: str | None) -> str:
    """Load book.html template."""
    tmpl_dir = Path(__file__).parent / 'templates'
    tmpl_file = tmpl_dir / 'book.html'
    if tmpl_file.exists():
        tmpl = tmpl_file.read_text(encoding='utf-8')
    else:
        tmpl = (
            '<!DOCTYPE html><html lang="pl"><head><meta charset="UTF-8">'
            '<style>@import url("https://fonts.googleapis.com/css2?'
            'family=DM+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400'
            '&family=Plus+Jakarta+Sans:wght@700;800'
            '&family=JetBrains+Mono:wght@400;500&display=swap");</style>'
            '<link rel="stylesheet" href="STYLESHEET_PATH">'
            '</head><body>CONTENT_PLACEHOLDER</body></html>'
        )

    if css_path:
        tmpl = tmpl.replace('STYLESHEET_PATH', css_path)
    else:
        default_css = str(tmpl_dir / 'base.css')
        tmpl = tmpl.replace('STYLESHEET_PATH', default_css)

    return tmpl


def _parse_chapter(md_file: Path, glossary_terms: list, qr_items: list) -> dict | None:
    """Parse a single chapter .md file.

    Returns dict with 'meta' and 'html' keys.
    Mutates glossary_terms and qr_items lists (collecting :::info and :::qr).
    """
    raw = md_file.read_text(encoding='utf-8')
    if not raw.strip():
        warnings.warn(f"Empty chapter: {md_file.name}")
        return None

    # Extract YAML frontmatter
    meta = {}
    content = raw
    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', raw, re.DOTALL)
    if fm_match:
        meta = yaml.safe_load(fm_match.group(1)) or {}
        content = raw[fm_match.end():]

    # Extract H2 titles for mini-TOC
    h2_titles = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)

    # Chapter opener
    opener = generate_chapter_opener(meta, h2_titles)

    # Parse content: split into regular MD and :::component blocks
    html_parts = []
    is_first_paragraph = True

    blocks = _split_blocks(content)
    for block_type, block_content in blocks:
        if block_type == 'markdown':
            md_html = _render_markdown(block_content)
            # Add drop-cap to first <p>
            if is_first_paragraph and '<p>' in md_html:
                md_html = md_html.replace('<p>', '<p class="drop-cap">', 1)
                is_first_paragraph = False
            html_parts.append(md_html)
        elif block_type == 'component':
            comp_name, comp_content = block_content
            comp_html = render_component(comp_name, comp_content)
            html_parts.append(comp_html)

            # Collect glossary terms from :::info
            if comp_name.startswith('info'):
                lines = comp_content.strip().split('\n')
                if len(lines) >= 2:
                    glossary_terms.append({
                        'term': lines[0].strip(),
                        'definition': ' '.join(lines[1:]).strip(),
                    })

            # Collect QR items
            if comp_name.startswith('qr'):
                name_parts = comp_name.split(None, 1)
                url = name_parts[1] if len(name_parts) > 1 else comp_content.strip().split('\n')[0]
                label = comp_content.strip().split('\n')[1] if '\n' in comp_content else ''
                qr_items.append({
                    'url': url.strip(),
                    'label': label.strip(),
                    'qr_html': comp_html,
                })

    chapter_html = (
        f'{opener}'
        f'<div class="content">'
        f'{"".join(html_parts)}'
        f'</div>'
    )

    return {'meta': meta, 'html': chapter_html}


def _split_blocks(content: str) -> list[tuple]:
    """Split content into ('markdown', text) and ('component', (name, content)) blocks."""
    blocks = []
    current_md = []
    in_component = False
    component_name = ''
    component_lines = []

    for line in content.split('\n'):
        stripped = line.strip()

        if not in_component and stripped.startswith(':::') and stripped != ':::':
            # Flush current markdown
            if current_md:
                blocks.append(('markdown', '\n'.join(current_md)))
                current_md = []
            # Start component
            component_name = stripped[3:].strip()
            component_lines = []
            in_component = True
        elif in_component and stripped == ':::':
            # End component
            blocks.append(('component', (component_name, '\n'.join(component_lines))))
            in_component = False
            component_name = ''
            component_lines = []
        elif in_component:
            component_lines.append(line)
        else:
            current_md.append(line)

    # Handle unclosed component
    if in_component:
        warnings.warn(f"Unclosed :::component block: {component_name}")
        blocks.append(('component', (component_name, '\n'.join(component_lines))))

    # Flush remaining markdown
    if current_md:
        blocks.append(('markdown', '\n'.join(current_md)))

    return blocks


def _render_markdown(text: str) -> str:
    """Render standard Markdown to HTML."""
    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'codehilite', 'attr_list'])
    return md.convert(text)
