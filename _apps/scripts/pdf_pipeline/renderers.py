"""Component renderers for DOKODU book pipeline.

Each renderer takes raw content string (lines after :::component_name)
and returns HTML string with appropriate CSS classes from base.css.
"""
import html as html_module
import base64
import io
import warnings


def _esc(text: str) -> str:
    """HTML-escape text."""
    return html_module.escape(text.strip())


def render_component(name: str, content: str) -> str:
    """Dispatch to the appropriate renderer. Unknown → plain paragraph."""
    # Handle component arguments (e.g., "tiles 2" → name="tiles", arg="2")
    parts = name.strip().split(None, 1)
    comp_name = parts[0].lower()
    comp_arg = parts[1] if len(parts) > 1 else ''

    renderer = RENDERERS.get(comp_name)
    if renderer is None:
        warnings.warn(f"Unknown component: {comp_name}")
        return f'<p>{_esc(content)}</p>'

    return renderer(content, comp_arg)


def render_callout(content: str, variant: str) -> str:
    variant = variant.strip().lower() or 'tip'
    lines = content.strip().split('\n')

    # First line might be variant if not passed as arg
    if lines[0].strip().lower() in ('tip', 'warning', 'info', 'danger', 'trap'):
        variant = lines[0].strip().lower()
        lines = lines[1:]

    css_class = 'danger' if variant == 'trap' else variant
    title_map = {
        'tip': 'WSKAZOWKA', 'warning': 'UWAGA', 'info': 'INFORMACJA',
        'danger': 'OSTRZEZENIE', 'trap': 'UWAGA NA PULAPKE',
    }
    title = title_map.get(variant, variant.upper())
    body = '\n'.join(lines).strip()

    return (
        f'<div class="callout {css_class}">'
        f'<div class="callout-title">{title}</div>'
        f'<p>{_esc(body)}</p>'
        f'</div>'
    )


def render_stats(content: str, _arg: str) -> str:
    boxes = []
    for line in content.strip().split('\n'):
        if '|' not in line:
            continue
        value, label = line.split('|', 1)
        boxes.append(
            f'<div class="stat-box">'
            f'<div class="stat-number">{_esc(value)}</div>'
            f'<div class="stat-label">{_esc(label)}</div>'
            f'</div>'
        )
    return f'<div class="stat-grid">{"".join(boxes)}</div>'


def render_tiles(content: str, arg: str) -> str:
    lines = content.strip().split('\n')
    # First line might be column count
    cols = '2'
    start = 0
    first = lines[0].strip()
    if first.isdigit():
        cols = first
        start = 1
    elif arg.strip().isdigit():
        cols = arg.strip()

    tiles = []
    for line in lines[start:]:
        if '|' not in line:
            continue
        title, desc = line.split('|', 1)
        tiles.append(
            f'<div class="tile">'
            f'<div class="tile-title">{_esc(title)}</div>'
            f'<div class="tile-desc">{_esc(desc)}</div>'
            f'</div>'
        )
    return f'<div class="tile-grid cols-{cols}">{"".join(tiles)}</div>'


def render_quote(content: str, _arg: str) -> str:
    lines = content.strip().split('\n')
    author = ''
    quote_lines = []
    for line in lines:
        if line.strip().startswith('---'):
            author = line.strip().lstrip('-').strip()
        else:
            quote_lines.append(line)

    quote_text = ' '.join(quote_lines).strip()
    author_html = f'<div class="quote-author">— {_esc(author)}</div>' if author else ''
    return (
        f'<div class="quote-block">'
        f'<blockquote>{_esc(quote_text)}</blockquote>'
        f'{author_html}'
        f'</div>'
    )


def render_process(content: str, _arg: str) -> str:
    steps = []
    for i, line in enumerate(content.strip().split('\n'), 1):
        if '|' not in line:
            continue
        title, desc = line.split('|', 1)
        steps.append(
            f'<div class="process-step">'
            f'<div class="step-number">{i}</div>'
            f'<div class="step-title">{_esc(title)}</div>'
            f'<div class="step-desc">{_esc(desc)}</div>'
            f'</div>'
        )
    return f'<div class="process-flow">{"".join(steps)}</div>'


def render_timeline(content: str, _arg: str) -> str:
    items = []
    for line in content.strip().split('\n'):
        parts = line.split('|')
        if len(parts) < 2:
            continue
        year = parts[0].strip()
        title = parts[1].strip()
        desc = parts[2].strip() if len(parts) > 2 else ''
        desc_html = f'<div class="timeline-desc">{_esc(desc)}</div>' if desc else ''
        items.append(
            f'<div class="timeline-item">'
            f'<div class="timeline-year">{_esc(year)}</div>'
            f'<div class="timeline-title">{_esc(title)}</div>'
            f'{desc_html}'
            f'</div>'
        )
    return f'<div class="timeline">{"".join(items)}</div>'


def render_info(content: str, _arg: str) -> str:
    lines = content.strip().split('\n')
    term = lines[0].strip() if lines else ''
    explanation = ' '.join(lines[1:]).strip()
    return (
        f'<div class="info-box">'
        f'<div class="info-term">{_esc(term)}</div>'
        f'<p>{_esc(explanation)}</p>'
        f'</div>'
    )


def render_highlight(content: str, _arg: str) -> str:
    return f'<div class="highlight-bar">{_esc(content)}</div>'


def render_cta(content: str, _arg: str) -> str:
    lines = content.strip().split('\n')
    heading = lines[0] if lines else ''
    paragraph = lines[1] if len(lines) > 1 else ''
    contact = lines[2] if len(lines) > 2 else ''
    return (
        f'<div class="cta-section">'
        f'<h2>{_esc(heading)}</h2>'
        f'<p>{_esc(paragraph)}</p>'
        f'<span class="cta-contact">{_esc(contact)}</span>'
        f'</div>'
    )


def render_compare(content: str, _arg: str) -> str:
    blocks = content.split('---')
    cards = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        lines = block.split('\n')
        title = lines[0] if lines else ''
        items = [f'<li>{_esc(l)}</li>' for l in lines[1:] if l.strip()]
        cards.append(
            f'<div class="comparison-card">'
            f'<div class="card-title">{_esc(title)}</div>'
            f'<ul>{"".join(items)}</ul>'
            f'</div>'
        )
    return f'<div class="comparison-table">{"".join(cards)}</div>'


def render_value_stack(content: str, _arg: str) -> str:
    lines = content.strip().split('\n')
    items = []
    for line in lines:
        if '|' not in line:
            continue
        name, price = line.split('|', 1)
        items.append(
            f'<div class="value-item">'
            f'<span class="value-name">{_esc(name)}</span>'
            f'<span class="value-price">{_esc(price)}</span>'
            f'</div>'
        )
    # Last item is total
    if items:
        last = items.pop()
        last = last.replace('value-item', 'total')
        items_html = ''.join(items) + last
    else:
        items_html = ''
    return f'<div class="value-stack">{items_html}</div>'


def render_summary(content: str, _arg: str) -> str:
    items = [f'<li>{_esc(line)}</li>' for line in content.strip().split('\n') if line.strip()]
    return (
        f'<div class="chapter-summary">'
        f'<div class="summary-title">Kluczowe wnioski</div>'
        f'<ul>{"".join(items)}</ul>'
        f'</div>'
    )


def render_exercise(content: str, _arg: str) -> str:
    return (
        f'<div class="exercise-box">'
        f'<div class="exercise-title"></div>'
        f'<p>{_esc(content)}</p>'
        f'</div>'
    )


def render_checklist(content: str, _arg: str) -> str:
    items = [f'<li>{_esc(line)}</li>' for line in content.strip().split('\n') if line.strip()]
    return f'<ul class="checklist">{"".join(items)}</ul>'


def render_prerequisites(content: str, _arg: str) -> str:
    items = [f'<li>{_esc(line)}</li>' for line in content.strip().split('\n') if line.strip()]
    return (
        f'<div class="prerequisites-box">'
        f'<div class="prereq-title">Czego potrzebujesz</div>'
        f'<ul>{"".join(items)}</ul>'
        f'</div>'
    )


def render_qr(content: str, url_arg: str) -> str:
    """Render QR code as inline base64 PNG. url_arg comes from :::qr URL."""
    lines = content.strip().split('\n')
    url = url_arg.strip() or (lines[0].strip() if lines else '')
    label = lines[1].strip() if len(lines) > 1 else ''

    try:
        import qrcode
        qr = qrcode.make(url, box_size=6, border=2)
        buf = io.BytesIO()
        qr.save(buf, format='PNG')
        b64 = base64.b64encode(buf.getvalue()).decode()
        img = f'<img src="data:image/png;base64,{b64}" alt="QR: {_esc(url)}">'
    except ImportError:
        img = f'<p>[QR: {_esc(url)}]</p>'

    label_html = f'<div class="qr-label">{_esc(label)}</div>' if label else ''
    return (
        f'<div class="qr-block">'
        f'{img}'
        f'{label_html}'
        f'<div class="qr-url">{_esc(url)}</div>'
        f'</div>'
    )


def render_code(content: str, lang_arg: str) -> str:
    """Render code block with language header and syntax highlighting."""
    lines = content.strip().split('\n')
    # First line might be language
    lang = lang_arg.strip().lower()
    start = 0
    if not lang and lines:
        lang = lines[0].strip().lower()
        start = 1

    code_text = '\n'.join(lines[start:])

    try:
        from pygments import highlight
        from pygments.lexers import get_lexer_by_name, TextLexer
        from pygments.formatters import HtmlFormatter
        try:
            lexer = get_lexer_by_name(lang)
        except Exception:
            lexer = TextLexer()
        formatter = HtmlFormatter(nowrap=True, linenos=False, noclasses=True)
        highlighted = highlight(code_text, lexer, formatter)
    except ImportError:
        highlighted = _esc(code_text)

    return (
        f'<div class="code-block">'
        f'<div class="code-header">{_esc(lang.upper() if lang else "CODE")}</div>'
        f'<pre><code>{highlighted}</code></pre>'
        f'</div>'
    )


def render_pullquote(content: str, _arg: str) -> str:
    return f'<div class="pull-quote">{_esc(content)}</div>'


def render_beforeafter(content: str, _arg: str) -> str:
    parts = content.split('---')
    before = parts[0].strip() if parts else ''
    after = parts[1].strip() if len(parts) > 1 else ''
    return (
        f'<div class="before-after">'
        f'<div class="ba-side ba-before">'
        f'<div class="ba-label">PRZED</div>'
        f'<div class="ba-content">{_esc(before)}</div>'
        f'</div>'
        f'<div class="ba-side ba-after">'
        f'<div class="ba-label">PO</div>'
        f'<div class="ba-content">{_esc(after)}</div>'
        f'</div>'
        f'</div>'
    )


def render_decision(content: str, _arg: str) -> str:
    lines = content.strip().split('\n')
    question = lines[0] if lines else ''
    yes_text = ''
    no_text = ''
    for line in lines[1:]:
        if '|' not in line:
            continue
        label, text = line.split('|', 1)
        label = label.strip().upper()
        if label in ('TAK', 'YES', 'DA'):
            yes_text = text.strip()
        elif label in ('NIE', 'NO'):
            no_text = text.strip()
    return (
        f'<div class="decision-tree">'
        f'<div class="dt-question">{_esc(question)}</div>'
        f'<div class="dt-branches">'
        f'<div class="dt-branch dt-yes">'
        f'<div class="dt-branch-label">TAK</div>'
        f'{_esc(yes_text)}'
        f'</div>'
        f'<div class="dt-branch dt-no">'
        f'<div class="dt-branch-label">NIE</div>'
        f'{_esc(no_text)}'
        f'</div>'
        f'</div>'
        f'</div>'
    )


def render_series(content: str, _arg: str) -> str:
    """Render from raw content. Auto-generation from book.yaml handled in auto_sections.py."""
    lines = content.strip().split('\n')
    title = lines[0] if lines else 'Zobacz takze'
    books = []
    for line in lines[1:]:
        if line.strip():
            books.append(
                f'<div class="series-book">'
                f'<div class="series-book-title">{_esc(line)}</div>'
                f'</div>'
            )
    return (
        f'<div class="series-promo">'
        f'<div class="series-title">{_esc(title)}</div>'
        f'<div class="series-books">{"".join(books)}</div>'
        f'</div>'
    )


# Registry
RENDERERS = {
    'callout': render_callout,
    'stats': render_stats,
    'tiles': render_tiles,
    'quote': render_quote,
    'process': render_process,
    'timeline': render_timeline,
    'info': render_info,
    'highlight': render_highlight,
    'cta': render_cta,
    'compare': render_compare,
    'value-stack': render_value_stack,
    'summary': render_summary,
    'exercise': render_exercise,
    'checklist': render_checklist,
    'prerequisites': render_prerequisites,
    'qr': render_qr,
    'code': render_code,
    'pullquote': render_pullquote,
    'decision': render_decision,
    'beforeafter': render_beforeafter,
    'series': render_series,
}
