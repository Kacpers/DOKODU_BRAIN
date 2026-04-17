"""Auto-generated book sections: cover, legal, TOC, glossary, resources, back cover."""
import html as html_module
import base64
from pathlib import Path


def _esc(text: str) -> str:
    return html_module.escape(str(text).strip())


def generate_cover(book_dir: Path, meta: dict) -> str:
    """Cover from external JPG (fullbleed) or fallback to CSS cover."""
    cover_img = meta.get('cover_image', '')
    cover_path = book_dir / cover_img if cover_img else None

    if cover_path and cover_path.exists():
        # Inline base64 for portability
        b64 = base64.b64encode(cover_path.read_bytes()).decode()
        ext = cover_path.suffix.lstrip('.').replace('jpg', 'jpeg')
        return (
            f'<div class="cover-image-page">'
            f'<img src="data:image/{ext};base64,{b64}" alt="Cover">'
            f'</div>'
        )

    # Fallback: CSS-based cover
    style = meta.get('cover', 'dark')
    light_class = ' light' if style == 'light' else ''
    return (
        f'<div class="cover-page{light_class}">'
        f'<div class="cover-content">'
        f'<div class="cover-badge">{_esc(meta.get("badge", ""))}</div>'
        f'<h1>{_esc(meta.get("title", ""))}</h1>'
        f'<div class="subtitle">{_esc(meta.get("subtitle", ""))}</div>'
        f'<div class="cover-meta">'
        f'<div><div class="author-name">{_esc(meta.get("author", ""))}</div>'
        f'<div class="author-role">{_esc(meta.get("author_role", ""))}</div></div>'
        f'<div class="brand-logo">{_esc(meta.get("brand", "DOKODU"))}</div>'
        f'</div></div></div>'
    )


def generate_legal(meta: dict) -> str:
    return (
        f'<div class="legal-page content">'
        f'<div>'
        f'<p><strong>{_esc(meta.get("title", ""))}</strong></p>'
        f'<p>{_esc(meta.get("subtitle", ""))}</p>'
        f'<br>'
        f'<p>Autor: {_esc(meta.get("author", ""))}</p>'
        f'<p>{_esc(meta.get("author_role", ""))}</p>'
        f'<br>'
        f'<p>Wersja {_esc(meta.get("version", "1.0"))}, {_esc(meta.get("date", "2026"))}</p>'
        f'<p>&copy; {_esc(meta.get("brand", "Dokodu"))}. Wszelkie prawa zastrzezone.</p>'
        f'<br>'
        f'<p>Niniejsza publikacja jest chroniona prawem autorskim. '
        f'Reprodukcja lub rozpowszechnianie bez pisemnej zgody autora jest zabronione.</p>'
        f'</div>'
        f'</div>'
    )


def generate_how_to_read() -> str:
    """Static page explaining the book's visual conventions."""
    return (
        '<div class="how-to-read content">'
        '<h2>Jak czytac te ksiazke</h2>'
        '<p>W tej publikacji uzyto kilku wizualnych oznaczen, ktore pomagaja w nawigacji:</p>'
        '<div class="icon-legend">'
        #
        '<div class="icon-sample" style="background:#f0fdf4;color:#22c55e;border:1px solid #22c55e;">WSKAZOWKA</div>'
        '<div class="icon-desc">Praktyczna rada lub sprawdzony sposob — cos, co warto zastosowac od razu.</div>'
        #
        '<div class="icon-sample" style="background:#fffbeb;color:#f59e0b;border:1px solid #f59e0b;">UWAGA</div>'
        '<div class="icon-desc">Potencjalna pulapka lub ograniczenie, o ktorym warto wiedziec.</div>'
        #
        '<div class="icon-sample" style="background:#eef2ff;color:#6366f1;border:1px solid #6366f1;">INFORMACJA</div>'
        '<div class="icon-desc">Definicja terminu lub dodatkowe wyjasnienie pojecia.</div>'
        #
        '<div class="icon-sample" style="background:#eef2ff;color:#6366f1;border:2px dashed #6366f1;">SPROBUJ SAM</div>'
        '<div class="icon-desc">Cwiczenie praktyczne — krok po kroku do samodzielnego wykonania.</div>'
        #
        '<div class="icon-sample" style="background:#f8fafc;color:#0F2137;border-top:3px solid #0F2137;">KLUCZOWE WNIOSKI</div>'
        '<div class="icon-desc">Podsumowanie najwazniejszych punktow rozdzialu.</div>'
        '</div>'
        '</div>'
    )


def generate_toc(chapters: list[dict]) -> str:
    """TOC from chapter metadata. chapters = [{'number': 1, 'title': '...'}]"""
    entries = []
    for ch in chapters:
        entries.append(
            f'<div class="toc-entry">'
            f'<span class="toc-number">{ch["number"]:02d}</span>'
            f'<span class="toc-title">{_esc(ch["title"])}</span>'
            f'</div>'
        )
    return (
        f'<div class="toc-page content">'
        f'<h2>Spis tresci</h2>'
        f'{"".join(entries)}'
        f'</div>'
    )


def generate_chapter_opener(meta: dict, h2_titles: list[str]) -> str:
    """Full-page chapter opener with mini-TOC and reading time."""
    num = meta.get('chapter', 0)
    title = meta.get('title', '')
    subtitle = meta.get('subtitle', '')
    reading_time = meta.get('reading_time', '')

    mini_toc = ''
    if h2_titles:
        items = ''.join(f'<li>{_esc(t)}</li>' for t in h2_titles)
        mini_toc = f'<div class="mini-toc"><ul>{items}</ul></div>'

    time_badge = ''
    if reading_time:
        time_badge = f'<div class="reading-time">{_esc(reading_time)} czytania</div>'

    return (
        f'<div class="chapter-opener">'
        f'<div class="chapter-number">Rozdzial {num}</div>'
        f'<h1>{_esc(title)}</h1>'
        f'<div class="chapter-subtitle">{_esc(subtitle)}</div>'
        f'{time_badge}'
        f'{mini_toc}'
        f'<div class="chapter-bg-number">{num:02d}</div>'
        f'</div>'
    )


def generate_glossary(terms: list[dict]) -> str:
    """terms = [{'term': 'LLM', 'definition': '...'}], sorted alphabetically."""
    if not terms:
        return ''
    sorted_terms = sorted(terms, key=lambda t: t['term'].lower())
    entries = []
    for t in sorted_terms:
        entries.append(
            f'<div class="glossary-entry">'
            f'<div class="glossary-term">{_esc(t["term"])}</div>'
            f'<div class="glossary-def">{_esc(t["definition"])}</div>'
            f'</div>'
        )
    return (
        f'<div class="glossary-page content">'
        f'<h2>Slowniczek</h2>'
        f'{"".join(entries)}'
        f'</div>'
    )


def generate_resources(qr_items: list[dict]) -> str:
    """qr_items = [{'url': '...', 'label': '...', 'qr_html': '...'}]"""
    if not qr_items:
        return ''
    cards = []
    for item in qr_items:
        cards.append(
            f'<div class="resource-card">'
            f'{item.get("qr_html", "")}'
            f'<div class="resource-title">{_esc(item.get("label", ""))}</div>'
            f'<div class="resource-url">{_esc(item["url"])}</div>'
            f'</div>'
        )
    return (
        f'<div class="resources-page content">'
        f'<h2>Zasoby</h2>'
        f'<p>Zeskanuj kody QR, aby przejsc do zasobow online:</p>'
        f'<div class="resources-grid">{"".join(cards)}</div>'
        f'</div>'
    )


def generate_series(meta: dict) -> str:
    """Series promo from book.yaml."""
    series = meta.get('series', {})
    if not series:
        return ''
    books = series.get('other_books', [])
    if not books:
        return ''
    cards = []
    for book in books:
        cards.append(
            f'<div class="series-book">'
            f'<div class="series-book-title">{_esc(book.get("title", ""))}</div>'
            f'</div>'
        )
    return (
        f'<div class="series-promo content page-break">'
        f'<div class="series-title">Zobacz takze w serii {_esc(series.get("name", ""))}</div>'
        f'<div class="series-books">{"".join(cards)}</div>'
        f'</div>'
    )


def generate_back_cover(meta: dict) -> str:
    bc = meta.get('back_cover', {})
    if not bc:
        return ''
    desc = bc.get('description', '')
    testimonials = bc.get('testimonials', [])

    test_html = ''
    for t in testimonials:
        test_html += (
            f'<div class="bc-testimonial">'
            f'<p>{_esc(t.get("text", ""))}</p>'
            f'<div class="bc-testimonial-author">{_esc(t.get("author", ""))}</div>'
            f'</div>'
        )

    return (
        f'<div class="back-cover">'
        f'<div class="bc-description">{_esc(desc)}</div>'
        f'{test_html}'
        f'<div class="bc-brand">{_esc(meta.get("brand", "DOKODU"))}</div>'
        f'</div>'
    )
