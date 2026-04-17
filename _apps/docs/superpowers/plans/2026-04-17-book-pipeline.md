# Book Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Markdown → PDF book pipeline that reuses the existing DOKODU design system, with extended Markdown components, auto-generated sections, and professional publishing features.

**Architecture:** Python converter (`md_to_html.py`) parses extended Markdown (:::component syntax) into HTML with CSS classes from existing `base.css`. Orchestrator (`build_book.py`) chains converter → Playwright PDF renderer. New CSS components extend `base.css`. Test book validates all features end-to-end.

**Tech Stack:** Python 3, python-markdown, PyYAML, Pygments, qrcode[pil], Playwright (all installed except qrcode)

**Spec:** `_apps/docs/superpowers/specs/2026-04-17-book-pipeline-design.md`

**Key paths:**
- Existing pipeline: `_apps/scripts/pdf_pipeline/`
- Existing CSS: `_apps/scripts/pdf_pipeline/templates/base.css` (773 lines)
- Existing builder: `_apps/scripts/pdf_pipeline/build_pdf.py`
- Existing template: `_apps/scripts/pdf_pipeline/templates/chapter.html`
- Books content: `30_RESOURCES/RES_Ebook/books/<slug>/`
- Build output: `_apps/scripts/pdf_pipeline/build/`

---

## File Structure

| File | Action | Responsibility |
|------|--------|---------------|
| `_apps/scripts/pdf_pipeline/md_to_html.py` | CREATE | Extended Markdown parser → HTML with base.css classes |
| `_apps/scripts/pdf_pipeline/build_book.py` | CREATE | CLI orchestrator: finds book, calls md_to_html, calls Playwright |
| `_apps/scripts/pdf_pipeline/renderers.py` | CREATE | Component renderer functions (one per :::component type) |
| `_apps/scripts/pdf_pipeline/auto_sections.py` | CREATE | Auto-generated pages: cover, legal, TOC, glossary, resources, back cover |
| `_apps/scripts/pdf_pipeline/templates/base.css` | MODIFY | Add new CSS components (drop cap, summary, exercise, etc.) |
| `_apps/scripts/pdf_pipeline/templates/book.html` | CREATE | Book HTML template (simpler than chapter.html, str.replace) |
| `_apps/scripts/pdf_pipeline/tests/test_renderers.py` | CREATE | Unit tests for each component renderer |
| `_apps/scripts/pdf_pipeline/tests/test_md_to_html.py` | CREATE | Integration tests for MD→HTML conversion |
| `_apps/scripts/pdf_pipeline/tests/test_build_book.py` | CREATE | End-to-end test: build test book → PDF exists |
| `30_RESOURCES/RES_Ebook/books/test-ai/book.yaml` | CREATE | Test book metadata |
| `_apps/scripts/pdf_pipeline/tests/conftest.py` | CREATE | Adds parent dir to sys.path for imports |
| `30_RESOURCES/RES_Ebook/books/test-ai/01_wstep.md` | CREATE | Test chapter 1 |
| `30_RESOURCES/RES_Ebook/books/test-ai/02_czym_jest_ai.md` | CREATE | Test chapter 2 |
| `30_RESOURCES/RES_Ebook/books/test-ai/03_ai_w_firmie.md` | CREATE | Test chapter 3 |

---

## Task 1: Install qrcode dependency + create book.html template

**Files:**
- Create: `_apps/scripts/pdf_pipeline/templates/book.html`

- [ ] **Step 1: Install qrcode**

```bash
pip install "qrcode[pil]"
```

- [ ] **Step 2: Create conftest.py for tests**

File: `_apps/scripts/pdf_pipeline/tests/conftest.py`

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
```

- [ ] **Step 3: Create book.html template**

```html
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Plus+Jakarta+Sans:wght@700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    </style>
    <link rel="stylesheet" href="STYLESHEET_PATH">
</head>
<body>
CONTENT_PLACEHOLDER
</body>
</html>
```

Note: `STYLESHEET_PATH` and `CONTENT_PLACEHOLDER` are replaced via `str.replace()` at build time. No Jinja2.

- [ ] **Step 4: Commit**

```bash
git add _apps/scripts/pdf_pipeline/templates/book.html _apps/scripts/pdf_pipeline/tests/conftest.py
git commit -m "feat(book-pipeline): add book.html template and test conftest"
```

---

## Task 2: Add new CSS components to base.css

**Files:**
- Modify: `_apps/scripts/pdf_pipeline/templates/base.css` (append after line 773)

- [ ] **Step 1: Append new component styles to base.css**

Add the following CSS at the end of `base.css`:

```css
/* ============================================================
   BOOK PIPELINE — NEW COMPONENTS v6
   ============================================================ */

/* --- Drop Cap --- */
.drop-cap::first-letter {
    float: left;
    font-size: 3.8em;
    line-height: 0.8;
    font-weight: 800;
    color: var(--color-primary);
    margin: 0.05em 0.12em 0 0;
    font-family: var(--font-heading);
    padding-top: 0.05em;
}

/* --- Chapter Summary --- */
.chapter-summary {
    background: var(--color-bg-light);
    border-top: 3px solid var(--color-primary);
    border-radius: 0 0 var(--radius) var(--radius);
    padding: 26px 28px;
    margin: 2em 0;
    page-break-inside: avoid;
}

.chapter-summary .summary-title {
    font-family: var(--font-heading);
    font-weight: 700;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: var(--color-primary);
    margin-bottom: 12px;
}

.chapter-summary ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.chapter-summary li {
    padding: 6px 0 6px 24px;
    position: relative;
    font-size: 0.92rem;
    line-height: 1.5;
}

.chapter-summary li::before {
    content: '✓';
    position: absolute;
    left: 0;
    color: var(--color-success);
    font-weight: 700;
}

/* --- Exercise Box --- */
.exercise-box {
    border: 2px dashed var(--color-info);
    border-radius: var(--radius);
    padding: 22px 24px;
    margin: 1.5em 0;
    page-break-inside: avoid;
    position: relative;
}

.exercise-box .exercise-title {
    font-family: var(--font-heading);
    font-weight: 700;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: var(--color-info);
    margin-bottom: 10px;
}

.exercise-box .exercise-title::before {
    content: 'SPROBUJ SAM';
}

/* --- Checklist --- */
.checklist {
    list-style: none;
    padding: 0;
    margin: 1.2em 0;
}

.checklist li {
    padding: 8px 0 8px 34px;
    position: relative;
    border-bottom: 1px solid var(--color-border);
    font-size: 0.92rem;
}

.checklist li:last-child {
    border-bottom: none;
}

.checklist li::before {
    content: '';
    position: absolute;
    left: 0;
    top: 10px;
    width: 18px;
    height: 18px;
    border: 2px solid var(--color-border);
    border-radius: 3px;
    background: white;
}

/* --- Prerequisites Box --- */
.prerequisites-box {
    background: var(--color-bg-warm);
    border-left: 4px solid var(--color-accent-gold);
    border-radius: 0 var(--radius) var(--radius) 0;
    padding: 20px 24px;
    margin: 1.5em 0;
    page-break-inside: avoid;
}

.prerequisites-box .prereq-title {
    font-family: var(--font-heading);
    font-weight: 700;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: var(--color-accent-gold);
    margin-bottom: 10px;
}

.prerequisites-box ul {
    margin: 0;
    padding-left: 1.2em;
}

.prerequisites-box li {
    margin-bottom: 4px;
    font-size: 0.9rem;
}

/* --- QR Block --- */
.qr-block {
    text-align: center;
    margin: 1.5em 0;
    page-break-inside: avoid;
}

.qr-block img {
    width: 120px;
    height: 120px;
}

.qr-block .qr-label {
    font-size: 0.78rem;
    color: var(--color-text-muted);
    margin-top: 8px;
}

.qr-block .qr-url {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    color: var(--color-text-muted);
}

/* --- Code Block with Language Header --- */
.code-block {
    margin: 1.2em 0;
    border-radius: var(--radius);
    overflow: hidden;
    page-break-inside: avoid;
}

.code-block .code-header {
    background: var(--color-primary);
    color: #8d9bb0;
    padding: 8px 16px;
    font-family: var(--font-mono);
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.code-block pre {
    margin: 0;
    border-radius: 0;
}

.code-block .linenos {
    color: #4a5568;
    user-select: none;
    padding-right: 12px;
    border-right: 1px solid #2d3748;
    margin-right: 12px;
}

/* --- Pull Quote --- */
.pull-quote {
    font-family: var(--font-heading);
    font-size: 1.35rem;
    font-weight: 600;
    font-style: italic;
    text-align: center;
    color: var(--color-primary);
    padding: 28px 40px;
    margin: 2em 0;
    border-top: 2px solid var(--color-primary);
    border-bottom: 2px solid var(--color-primary);
    line-height: 1.5;
    page-break-inside: avoid;
}

/* --- Before/After --- */
.before-after {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0;
    margin: 1.5em 0;
    border-radius: var(--radius-lg);
    overflow: hidden;
    page-break-inside: avoid;
}

.before-after .ba-side {
    padding: 24px;
}

.before-after .ba-before {
    background: #fef2f2;
    border-right: 2px solid var(--color-border);
}

.before-after .ba-after {
    background: #f0fdf4;
}

.before-after .ba-label {
    font-family: var(--font-heading);
    font-weight: 700;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 10px;
}

.before-after .ba-before .ba-label {
    color: var(--color-danger);
}

.before-after .ba-after .ba-label {
    color: var(--color-success);
}

.before-after .ba-content {
    font-size: 0.88rem;
    line-height: 1.5;
}

/* --- Decision Tree --- */
.decision-tree {
    background: var(--color-bg-light);
    border-radius: var(--radius-lg);
    padding: 28px;
    margin: 1.5em 0;
    page-break-inside: avoid;
}

.decision-tree .dt-question {
    background: var(--color-primary);
    color: white;
    padding: 14px 20px;
    border-radius: var(--radius);
    font-weight: 600;
    font-size: 0.95rem;
    text-align: center;
    margin-bottom: 16px;
}

.decision-tree .dt-branches {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
}

.decision-tree .dt-branch {
    padding: 14px 18px;
    border-radius: var(--radius);
    font-size: 0.85rem;
}

.decision-tree .dt-yes {
    background: #f0fdf4;
    border: 2px solid var(--color-success);
}

.decision-tree .dt-no {
    background: #fef2f2;
    border: 2px solid var(--color-danger);
}

.decision-tree .dt-branch-label {
    font-weight: 700;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
}

.decision-tree .dt-yes .dt-branch-label { color: var(--color-success); }
.decision-tree .dt-no .dt-branch-label { color: var(--color-danger); }

/* --- Series Promo --- */
.series-promo {
    background: var(--color-bg-light);
    border-radius: var(--radius-lg);
    padding: 30px;
    margin: 2em 0;
    page-break-inside: avoid;
}

.series-promo .series-title {
    font-family: var(--font-heading);
    font-weight: 700;
    font-size: 1.1rem;
    color: var(--color-primary);
    margin-bottom: 16px;
}

.series-promo .series-books {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
}

.series-promo .series-book {
    background: white;
    border: 1px solid var(--color-border);
    border-radius: var(--radius);
    padding: 16px;
}

.series-promo .series-book-title {
    font-weight: 700;
    font-size: 0.9rem;
    color: var(--color-primary);
}

/* --- Legal Page --- */
.legal-page {
    page-break-after: always;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    min-height: 80vh;
    font-size: 0.8rem;
    color: var(--color-text-muted);
    line-height: 1.8;
}

/* --- How-to-read Page --- */
.how-to-read {
    page-break-after: always;
    padding: 40px var(--page-padding);
}

.how-to-read h2 {
    display: block;
}

.how-to-read .icon-legend {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 14px 20px;
    align-items: start;
    margin-top: 1.5em;
}

.how-to-read .icon-sample {
    padding: 8px 14px;
    border-radius: var(--radius);
    font-size: 0.8rem;
    font-weight: 600;
    text-align: center;
    min-width: 100px;
}

.how-to-read .icon-desc {
    font-size: 0.9rem;
    padding-top: 8px;
}

/* --- TOC Page --- */
.toc-page {
    page-break-after: always;
    padding: 60px var(--page-padding);
}

.toc-page h2 {
    display: block;
    margin-bottom: 1.5em;
}

.toc-entry {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    padding: 10px 0;
    border-bottom: 1px solid var(--color-border);
}

.toc-entry .toc-number {
    font-weight: 700;
    color: var(--color-accent);
    min-width: 36px;
}

.toc-entry .toc-title {
    font-weight: 600;
    color: var(--color-primary);
    flex: 1;
}

/* --- Reading Time Badge --- */
.reading-time {
    font-size: 0.72rem;
    color: #7c8da0;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-top: 14px;
}

/* --- Mini TOC (chapter opener) --- */
.mini-toc {
    margin-top: 24px;
    padding-top: 16px;
    border-top: 1px solid rgba(255,255,255,0.15);
}

.mini-toc ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.mini-toc li {
    color: #8d9bb0;
    font-size: 0.85rem;
    padding: 3px 0;
}

/* --- Back Cover --- */
.back-cover {
    page: fullbleed;
    page-break-before: always;
    width: 100%;
    min-height: 297mm;
    background: var(--color-primary);
    color: white;
    padding: 60px 50px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.back-cover .bc-description {
    font-size: 1.05rem;
    line-height: 1.7;
    color: #b8c4d4;
    max-width: 80%;
    margin-bottom: 40px;
}

.back-cover .bc-testimonial {
    border-left: 3px solid var(--color-accent);
    padding-left: 20px;
    margin: 20px 0;
    font-style: italic;
    color: #b8c4d4;
}

.back-cover .bc-testimonial-author {
    font-style: normal;
    font-weight: 600;
    color: var(--color-accent);
    font-size: 0.85rem;
    margin-top: 8px;
}

.back-cover .bc-brand {
    margin-top: auto;
    font-size: 1.2rem;
    font-weight: 800;
    letter-spacing: 2px;
    color: var(--color-accent);
}

/* --- Cover from Image --- */
.cover-image-page {
    page: fullbleed;
    page-break-after: always;
    width: 100%;
    height: 100vh;
    min-height: 297mm;
    padding: 0;
    margin: 0;
}

.cover-image-page img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

/* --- Resources Page --- */
.resources-page {
    page-break-before: always;
}

.resources-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-top: 1.5em;
}

.resource-card {
    background: var(--color-bg-light);
    border-radius: var(--radius);
    padding: 20px;
    text-align: center;
    page-break-inside: avoid;
}

.resource-card img {
    width: 100px;
    height: 100px;
    margin-bottom: 10px;
}

.resource-card .resource-title {
    font-weight: 600;
    font-size: 0.88rem;
    color: var(--color-primary);
    margin-bottom: 4px;
}

.resource-card .resource-url {
    font-family: var(--font-mono);
    font-size: 0.68rem;
    color: var(--color-text-muted);
    word-break: break-all;
}

/* --- Glossary --- */
.glossary-page {
    page-break-before: always;
}

.glossary-entry {
    padding: 10px 0;
    border-bottom: 1px solid var(--color-border);
    page-break-inside: avoid;
}

.glossary-term {
    font-weight: 700;
    color: var(--color-primary);
    font-size: 0.95rem;
}

.glossary-def {
    font-size: 0.88rem;
    color: var(--color-text-muted);
    margin-top: 2px;
    line-height: 1.5;
}

/* --- Figure Caption --- */
.figure {
    margin: 1.5em 0;
    page-break-inside: avoid;
}

.figure-caption {
    font-size: 0.78rem;
    color: var(--color-text-muted);
    font-style: italic;
    text-align: center;
    margin-top: 8px;
}
```

- [ ] **Step 2: Verify CSS is valid by opening a test HTML**

Create a minimal HTML that links the updated `base.css`, open in browser and check for CSS parse errors in dev tools.

- [ ] **Step 3: Commit**

```bash
git add _apps/scripts/pdf_pipeline/templates/base.css
git commit -m "feat(book-pipeline): add new CSS components (drop cap, summary, exercise, checklist, QR, etc.)"
```

---

## Task 3: Build component renderers

**Files:**
- Create: `_apps/scripts/pdf_pipeline/renderers.py`
- Create: `_apps/scripts/pdf_pipeline/tests/test_renderers.py`

- [ ] **Step 1: Create tests directory**

```bash
mkdir -p _apps/scripts/pdf_pipeline/tests
touch _apps/scripts/pdf_pipeline/tests/__init__.py
```

- [ ] **Step 2: Write tests for core renderers**

File: `_apps/scripts/pdf_pipeline/tests/test_renderers.py`

```python
"""Tests for book pipeline component renderers."""
import pytest
from renderers import render_component


def test_callout_tip():
    result = render_component('callout', 'tip\nThis is a tip.')
    assert 'class="callout tip"' in result
    assert 'This is a tip.' in result


def test_callout_trap():
    result = render_component('callout', 'trap\nWatch out!')
    assert 'class="callout danger"' in result
    assert 'UWAGA NA PULAPKE' in result.upper() or 'Watch out!' in result


def test_stats():
    result = render_component('stats', '67% | firm wdraza AI\n3x | szybciej')
    assert 'stat-grid' in result
    assert 'stat-box' in result
    assert '67%' in result
    assert 'firm wdraza AI' in result


def test_tiles_2col():
    result = render_component('tiles', '2\nAnaliza | Raporty\nCRM | Integracje')
    assert 'cols-2' in result
    assert 'tile-title' in result
    assert 'Analiza' in result


def test_quote_with_author():
    result = render_component('quote', 'AI zmieni swiat.\n--- Kacper Sieradzinski')
    assert 'quote-block' in result
    assert 'quote-author' in result
    assert 'Kacper' in result


def test_process():
    result = render_component('process', 'Start | Begin\nEnd | Finish')
    assert 'process-flow' in result
    assert 'process-step' in result
    assert 'Start' in result


def test_timeline():
    result = render_component('timeline', '2024 | GPT-4 | Multimodal AI')
    assert 'timeline' in result
    assert 'timeline-item' in result
    assert '2024' in result


def test_info():
    result = render_component('info', 'LLM\nLarge Language Model to...')
    assert 'info-box' in result
    assert 'info-term' in result
    assert 'LLM' in result


def test_summary():
    result = render_component('summary', 'AI jest wazne\nTrzeba wdrazac')
    assert 'chapter-summary' in result
    assert 'summary-title' in result


def test_exercise():
    result = render_component('exercise', 'Otworz ChatGPT i wpisz...')
    assert 'exercise-box' in result


def test_checklist():
    result = render_component('checklist', 'Konto OpenAI\nKlucz API\nPrzegladarka')
    assert 'checklist' in result
    assert result.count('<li>') == 3


def test_prerequisites():
    result = render_component('prerequisites', 'Python 3.10+\nKonto OpenAI')
    assert 'prerequisites-box' in result
    assert 'Python 3.10+' in result


def test_highlight():
    result = render_component('highlight', 'Wazna informacja!')
    assert 'highlight-bar' in result
    assert 'Wazna informacja!' in result


def test_pullquote():
    result = render_component('pullquote', 'AI to nie przyszlosc — to terazniejszosc.')
    assert 'pull-quote' in result


def test_beforeafter():
    result = render_component('beforeafter', 'Reczne raporty co tydzien\n---\nAutomatyczne raporty codziennie')
    assert 'before-after' in result
    assert 'ba-before' in result
    assert 'ba-after' in result


def test_decision():
    result = render_component('decision', 'Czy masz dane?\nTAK | Uzyj RAG\nNIE | Zacznij od fine-tuningu')
    assert 'decision-tree' in result
    assert 'dt-question' in result
    assert 'dt-yes' in result
    assert 'dt-no' in result


def test_code_python():
    result = render_component('code', 'python\nprint("hello")')
    assert 'code-block' in result
    assert 'code-header' in result
    assert 'PYTHON' in result.upper()


def test_unknown_component():
    result = render_component('nonexistent', 'some content')
    assert '<p>' in result  # fallback to paragraph


def test_empty_content():
    result = render_component('callout', 'tip\n')
    assert 'callout' in result
```

- [ ] **Step 3: Run tests to verify they fail**

```bash
cd _apps/scripts/pdf_pipeline && python -m pytest tests/test_renderers.py -v
```
Expected: ImportError — `renderers` module not found.

- [ ] **Step 4: Implement renderers.py**

File: `_apps/scripts/pdf_pipeline/renderers.py`

```python
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
```

- [ ] **Step 5: Run tests**

```bash
cd _apps/scripts/pdf_pipeline && python -m pytest tests/test_renderers.py -v
```
Expected: all tests PASS.

- [ ] **Step 6: Commit**

```bash
git add _apps/scripts/pdf_pipeline/renderers.py _apps/scripts/pdf_pipeline/tests/
git commit -m "feat(book-pipeline): add component renderers with tests (21 components)"
```

---

## Task 4: Build auto-generated sections module

**Files:**
- Create: `_apps/scripts/pdf_pipeline/auto_sections.py`

- [ ] **Step 1: Write auto_sections.py**

This module generates HTML for: cover page (from JPG), legal page, "how to read" page, TOC, chapter openers with mini-TOC + reading time, glossary, resources, series promo, back cover.

```python
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
```

- [ ] **Step 2: Commit**

```bash
git add _apps/scripts/pdf_pipeline/auto_sections.py
git commit -m "feat(book-pipeline): add auto-generated sections module"
```

---

## Task 5: Build Markdown-to-HTML converter

**Files:**
- Create: `_apps/scripts/pdf_pipeline/md_to_html.py`
- Create: `_apps/scripts/pdf_pipeline/tests/test_md_to_html.py`

- [ ] **Step 1: Write integration tests**

File: `_apps/scripts/pdf_pipeline/tests/test_md_to_html.py`

```python
"""Integration tests for md_to_html converter."""
import pytest
import tempfile
from pathlib import Path
from md_to_html import convert_book


@pytest.fixture
def book_dir(tmp_path):
    """Create a minimal test book."""
    # book.yaml
    (tmp_path / 'book.yaml').write_text(
        'title: Test Book\n'
        'subtitle: A test\n'
        'author: Tester\n'
        'author_role: QA\n'
        'brand: TEST\n'
        'version: "1.0"\n'
        'date: "2026"\n'
        'cover: dark\n'
        'auto_sections:\n'
        '  how_to_read: true\n'
        '  glossary: true\n'
        '  legal: true\n',
        encoding='utf-8'
    )
    # Chapter 1
    (tmp_path / '01_intro.md').write_text(
        '---\n'
        'chapter: 1\n'
        'title: Intro\n'
        'subtitle: Getting started\n'
        'reading_time: 5 min\n'
        '---\n\n'
        '## First Section\n\n'
        'Some text here.\n\n'
        ':::callout tip\n'
        'This is a tip.\n'
        ':::\n\n'
        ':::info\n'
        'LLM\n'
        'Large Language Model\n'
        ':::\n\n'
        '## Second Section\n\n'
        'More text.\n',
        encoding='utf-8'
    )
    return tmp_path


def test_convert_produces_html(book_dir):
    html = convert_book(book_dir)
    assert '<html' in html
    assert 'Test Book' in html


def test_convert_has_cover(book_dir):
    html = convert_book(book_dir)
    assert 'cover-page' in html


def test_convert_has_legal(book_dir):
    html = convert_book(book_dir)
    assert 'legal-page' in html


def test_convert_has_toc(book_dir):
    html = convert_book(book_dir)
    assert 'toc-page' in html
    assert 'Intro' in html


def test_convert_has_chapter_opener(book_dir):
    html = convert_book(book_dir)
    assert 'chapter-opener' in html
    assert 'Rozdzial 1' in html


def test_convert_has_mini_toc(book_dir):
    html = convert_book(book_dir)
    assert 'mini-toc' in html
    assert 'First Section' in html


def test_convert_has_drop_cap(book_dir):
    html = convert_book(book_dir)
    assert 'drop-cap' in html


def test_convert_has_components(book_dir):
    html = convert_book(book_dir)
    assert 'callout tip' in html
    assert 'info-box' in html


def test_convert_collects_glossary(book_dir):
    html = convert_book(book_dir)
    assert 'glossary-page' in html
    assert 'LLM' in html


def test_convert_has_how_to_read(book_dir):
    html = convert_book(book_dir)
    assert 'how-to-read' in html
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd _apps/scripts/pdf_pipeline && python -m pytest tests/test_md_to_html.py -v
```
Expected: ImportError.

- [ ] **Step 3: Implement md_to_html.py**

File: `_apps/scripts/pdf_pipeline/md_to_html.py`

```python
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
                parts = comp_name.split(None, 1)
                url = parts[1] if len(parts) > 1 else comp_content.strip().split('\n')[0]
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
```

- [ ] **Step 4: Run tests**

```bash
cd _apps/scripts/pdf_pipeline && python -m pytest tests/test_md_to_html.py -v
```
Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add _apps/scripts/pdf_pipeline/md_to_html.py _apps/scripts/pdf_pipeline/tests/test_md_to_html.py
git commit -m "feat(book-pipeline): add Markdown-to-HTML converter with tests"
```

---

## Task 6: Build orchestrator (build_book.py)

**Files:**
- Create: `_apps/scripts/pdf_pipeline/build_book.py`
- Create: `_apps/scripts/pdf_pipeline/tests/test_build_book.py`

- [ ] **Step 1: Write end-to-end test**

File: `_apps/scripts/pdf_pipeline/tests/test_build_book.py`

```python
"""End-to-end test for build_book orchestrator."""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from build_book import build_book


@pytest.fixture
def test_book(tmp_path):
    """Create minimal test book."""
    (tmp_path / 'book.yaml').write_text(
        'title: E2E Test\nsubtitle: Test\nauthor: Bot\n'
        'author_role: QA\nbrand: TEST\ncover: dark\n'
        'version: "1.0"\ndate: "2026"\n'
        'auto_sections:\n  legal: true\n',
        encoding='utf-8'
    )
    (tmp_path / '01_test.md').write_text(
        '---\nchapter: 1\ntitle: Test Chapter\n---\n\n'
        'Hello world.\n',
        encoding='utf-8'
    )
    return tmp_path


def test_build_generates_html(test_book, tmp_path):
    """Test that build produces an HTML file."""
    output = tmp_path / 'output'
    output.mkdir()
    html_path = build_book(test_book, output_dir=output, pdf=False)
    assert html_path.exists()
    assert html_path.suffix == '.html'
    content = html_path.read_text()
    assert 'E2E Test' in content
    assert 'Test Chapter' in content
```

- [ ] **Step 2: Implement build_book.py**

```python
#!/usr/bin/env python3
"""DOKODU Book Pipeline — Orchestrator.

Usage:
    python build_book.py <book-slug>                    # build PDF
    python build_book.py <book-slug> --html-only        # HTML only (no PDF)
    python build_book.py <book-slug> --preview          # open after build
"""
import argparse
import sys
from pathlib import Path

# Ensure sibling modules are importable regardless of CWD
sys.path.insert(0, str(Path(__file__).parent))

# Resolve paths
SCRIPT_DIR = Path(__file__).parent
BOOKS_DIR = SCRIPT_DIR.parent.parent.parent / '30_RESOURCES' / 'RES_Ebook' / 'books'
BUILD_DIR = SCRIPT_DIR / 'build'
CSS_PATH = str((SCRIPT_DIR / 'templates' / 'base.css').resolve())


def build_book(book_dir: Path, output_dir: Path | None = None,
               pdf: bool = True) -> Path:
    """Build a book from Markdown to HTML (and optionally PDF).

    Returns path to the generated file (HTML or PDF).
    """
    from md_to_html import convert_book

    out = output_dir or BUILD_DIR
    out.mkdir(parents=True, exist_ok=True)

    slug = book_dir.name
    html_path = out / f'{slug}.html'

    # Convert MD → HTML
    print(f"Converting: {book_dir.name}")
    html_content = convert_book(book_dir, css_path=CSS_PATH)
    html_path.write_text(html_content, encoding='utf-8')
    print(f"  HTML: {html_path} ({html_path.stat().st_size // 1024} KB)")

    if not pdf:
        return html_path

    # HTML → PDF via Playwright
    pdf_path = out / f'{slug}.pdf'
    print(f"Rendering PDF...")
    from build_pdf import build_with_playwright
    build_with_playwright([html_path], pdf_path)
    return pdf_path


def main():
    parser = argparse.ArgumentParser(description="DOKODU Book Pipeline")
    parser.add_argument('slug', help='Book directory name (slug)')
    parser.add_argument('--html-only', action='store_true', help='Generate HTML only, no PDF')
    parser.add_argument('--preview', action='store_true', help='Open PDF after build')
    parser.add_argument('--books-dir', type=Path, default=BOOKS_DIR,
                        help=f'Books directory (default: {BOOKS_DIR})')
    args = parser.parse_args()

    book_dir = args.books_dir / args.slug
    if not book_dir.exists():
        print(f"Error: Book directory not found: {book_dir}")
        print(f"Available books: {[d.name for d in args.books_dir.iterdir() if d.is_dir()]}")
        sys.exit(1)

    result = build_book(book_dir, pdf=not args.html_only)

    if args.preview and result.suffix == '.pdf':
        import subprocess
        subprocess.run(['xdg-open', str(result)], check=False)

    print(f"Done! Output: {result}")


if __name__ == '__main__':
    main()
```

- [ ] **Step 3: Run test**

```bash
cd _apps/scripts/pdf_pipeline && python -m pytest tests/test_build_book.py -v
```

- [ ] **Step 4: Commit**

```bash
git add _apps/scripts/pdf_pipeline/build_book.py _apps/scripts/pdf_pipeline/tests/test_build_book.py
git commit -m "feat(book-pipeline): add build_book orchestrator"
```

---

## Task 7: Create test book and end-to-end validation

**Files:**
- Create: `30_RESOURCES/RES_Ebook/books/test-ai/book.yaml`
- Create: `30_RESOURCES/RES_Ebook/books/test-ai/01_wstep.md`
- Create: `30_RESOURCES/RES_Ebook/books/test-ai/02_czym_jest_ai.md`
- Create: `30_RESOURCES/RES_Ebook/books/test-ai/03_ai_w_firmie.md`

- [ ] **Step 1: Create books directory and book.yaml**

```bash
mkdir -p 30_RESOURCES/RES_Ebook/books/test-ai
```

```yaml
title: "AI Praktycznie"
subtitle: "Przewodnik wdrazania sztucznej inteligencji w firmie"
author: "Kacper Sieradzinski"
author_role: "CEO Dokodu | AI Trainer"
brand: "DOKODU"
version: "0.1"
date: "kwiecien 2026"
badge: "PRZEWODNIK 2026"
cover: dark

back_cover:
  description: "Praktyczny przewodnik po wdrazaniu AI w polskich firmach. Od pierwszego chatbota po pelna automatyzacje procesow."
  testimonials:
    - text: "Najbardziej praktyczna publikacja o AI, jaka czytalem."
      author: "Jan Kowalski, CTO TechCorp"

series:
  name: "Dokodu AI Library"
  other_books:
    - title: "Automatyzacja z n8n"
      slug: automatyzacja-n8n
    - title: "Agenci AI w Praktyce"
      slug: ai-agenci

auto_sections:
  how_to_read: true
  glossary: true
  resources: true
  legal: true
```

- [ ] **Step 2: Create chapter 1 — uses: callout, stats, info, prerequisites**

File: `30_RESOURCES/RES_Ebook/books/test-ai/01_wstep.md`

```markdown
---
chapter: 1
title: Wprowadzenie do AI
subtitle: Dlaczego teraz jest najlepszy moment na wdrozenie
reading_time: 5 min
---

## Rewolucja, ktora juz trwa

Sztuczna inteligencja przestala byc technologia przyszlosci. W 2026 roku jest narzedziem, ktore polskie firmy wdrazaja na co dzien — od automatyzacji obslugi klienta po analize dokumentow prawnych.

:::callout tip
Nie musisz byc programista, zeby wdrozyc AI w swojej firmie. Wystarczy zrozumiec, jakie problemy AI rozwiazuje najlepiej.
:::

:::stats
67% | polskich firm planuje wdrozenie AI do 2027
3x | szybszy czas reakcji na zapytania klientow
42% | redukcja kosztow operacyjnych po wdrozeniu
:::

## Dla kogo jest ta ksiazka

Ta publikacja jest dla decydentow, managerow i specjalistow, ktorzy chca zrozumiec AI od strony praktycznej — bez kodu, bez teorii, z konkretnymi przykladami z polskiego rynku.

:::prerequisites
Otwarta glowa na nowe technologie
Dostep do internetu i przegladarki
30 minut dziennie na cwiczenia praktyczne
:::

## Kluczowe pojecia

:::info
LLM (Large Language Model)
Duzy model jezykowy — to silnik stojacy za ChatGPT, Claude i Gemini. Trenowany na miliardach tekstow, potrafi generowac, analizowac i transformowac tekst w sposob zblizony do ludzkiego.
:::

:::info
RAG (Retrieval-Augmented Generation)
Technika laczaca wyszukiwanie informacji z generowaniem tekstu. Pozwala AI odpowiadac na pytania na podstawie Twoich wlasnych dokumentow — bez koniecznosci trenowania modelu od zera.
:::

:::summary
AI w 2026 to narzedzie dostepne dla kazdej firmy, nie tylko korporacji
Nie potrzebujesz zespolu programistow — wystarczy zrozumienie problemu
Kluczowe technologie to LLM i RAG — poznasz je w kolejnych rozdzialach
:::
```

- [ ] **Step 3: Create chapter 2 — uses: quote, process, timeline, exercise, code, decision**

File: `30_RESOURCES/RES_Ebook/books/test-ai/02_czym_jest_ai.md`

```markdown
---
chapter: 2
title: Czym jest AI
subtitle: Od buzzwordu do narzedzia pracy
reading_time: 8 min
---

## Definicja, ktora ma sens

Zapomnij o filmowych wizjach robotow. Sztuczna inteligencja w biznesie to oprogramowanie, ktore uczy sie z danych i podejmuje decyzje — lub pomaga je podejmowac.

:::quote
AI to nie magia — to statystyka na sterydach. Im lepsze dane, tym lepsze wyniki.
--- Kacper Sieradzinski
:::

## Jak dziala AI w praktyce

:::process
Dane wejsciowe | Dokumenty, emaile, formularze, bazy danych
Przetwarzanie | Model AI analizuje, klasyfikuje, wyciaga informacje
Decyzja | Rekomendacja, klasyfikacja lub automatyczna akcja
Wynik | Raport, odpowiedz, zaktualizowany rekord w CRM
:::

## Historia w pigulce

:::timeline
2020 | GPT-3 | Poczatek ery generatywnej — pierwsza wersja zdolna do sensownego pisania
2022 | ChatGPT | Demokratyzacja AI — 100M uzytkownikow w 2 miesiace
2023 | GPT-4 | Enterprise-grade — multimodal, reasoning, tool use
2024 | Agenci AI | Autonomiczne systemy podejmujace decyzje i wykonujace zadania
2026 | AI natywne firmy | Firmy projektowane wokol AI od pierwszego dnia
:::

## Sprobuj sam

:::exercise
Otworz ChatGPT lub Claude i wpisz nastepujacy prompt:

"Przeanalizuj ten tekst i wyciagnij 3 kluczowe informacje: [wklej dowolny artykul]"

Zwroc uwage na:
1. Jakosc wyciagnietych informacji
2. Czy AI poprawnie zidentyfikowalo najwazniejsze punkty
3. Ile czasu zaoszczedziles vs manualna analiza
:::

## Prosty przyklad kodu

:::code python
from anthropic import Anthropic

client = Anthropic()
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Czym jest AI?"}]
)
print(response.content[0].text)
:::

## Czy AI jest dla mojej firmy?

:::decision
Czy masz powtarzalne procesy, ktore zajmuja >2h tygodniowo?
TAK | AI moze je zautomatyzowac — zacznij od rozdzialu 3
NIE | Skup sie na identyfikacji procesow — uzyj checklisty z rozdzialu 3
:::

:::summary
AI to oprogramowanie uczace sie z danych, nie magia z filmow
W praktyce: dane → model → decyzja → wynik
Historia AI przyspieszyla dramatycznie od 2020
Nawet prosty prompt moze zaoszczedzic godziny pracy
:::
```

- [ ] **Step 4: Create chapter 3 — uses: tiles, beforeafter, checklist, highlight, pullquote, compare, qr, cta**

File: `30_RESOURCES/RES_Ebook/books/test-ai/03_ai_w_firmie.md`

```markdown
---
chapter: 3
title: AI w Twojej firmie
subtitle: Praktyczny plan wdrozenia krok po kroku
reading_time: 10 min
---

## Gdzie AI daje najwiecej wartosci

Nie kazdy proces nadaje sie do automatyzacji. Oto cztery obszary, w ktorych AI przynosi najszybszy zwrot z inwestycji:

:::tiles 2
Obsluga klienta | Chatboty, klasyfikacja zgloszen, automatyczne odpowiedzi na FAQ
Analiza dokumentow | Ekstrakcja danych z faktur, umow, formularzy — bez recznego przepisywania
Sprzedaz i marketing | Scoring leadow, personalizacja ofert, analiza sentymentu
Raportowanie | Automatyczne raporty z danych, dashboardy, alerty o anomaliach
:::

## Przed i po wdrozeniu

:::beforeafter
Reczne przetwarzanie faktur: 15 minut na fakture, 3 bledy na 100 dokumentow, frustracja zespolu
---
Automatyczne przetwarzanie: 30 sekund na fakture, 0.1% bledow, zespol skupiony na wyjatkach
:::

:::pullquote
Firmy, ktore wdroza AI w 2026, beda mialy 3-letnia przewage nad tymi, ktore zaczna w 2029.
:::

## Checklist gotowosci

:::checklist
Zidentyfikowales min. 3 procesy do automatyzacji
Masz dostep do danych (Excel, CRM, email)
Wyznaczyles osobe odpowiedzialna za projekt
Masz budzet na narzedzia (min. 500 PLN/mies.)
Zespol jest otwarty na zmiany
:::

:::highlight
80% udanych wdrozen AI zaczyna sie od jednego, prostego procesu — nie od rewolucji.
:::

## Porownanie narzedzi

:::compare
ChatGPT (OpenAI)
Najlepsza generacja tekstu
Swietne do konwersacji
Plugin ecosystem
Od 20 USD/mies.
---
Claude (Anthropic)
Najlepszy reasoning i analiza
200K kontekst — cale dokumenty
Bezpieczniejszy (Constitutional AI)
Od 20 USD/mies.
:::

## Zasoby

:::qr https://dokodu.it/ai
Strona Dokodu — szkolenia i wdrozenia AI
:::

:::qr https://youtube.com/@KacperSieradzinski
Kanal YouTube — praktyczne tutoriale AI
:::

## Nastepne kroki

:::cta
Gotowy na wdrozenie AI?
Umow sie na bezplatna konsultacje — pokaze Ci, od czego zaczac w Twojej firmie.
kontakt@dokodu.it | dokodu.it/konsultacja
:::

:::summary
Najlepsze obszary na start: obsluga klienta, dokumenty, sprzedaz, raportowanie
Zacznij od jednego procesu, nie od rewolucji
Porownaj narzedzia: ChatGPT vs Claude — oba maja swoje mocne strony
Uzyj checklisty gotowosci zanim zaczniesz
:::
```

- [ ] **Step 5: Build HTML (without PDF first)**

```bash
cd _apps/scripts/pdf_pipeline && python build_book.py test-ai --html-only --books-dir ../../30_RESOURCES/RES_Ebook/books
```

Open the HTML file in browser and visually inspect all components.

- [ ] **Step 6: Build full PDF**

```bash
cd _apps/scripts/pdf_pipeline && python build_book.py test-ai --books-dir ../../30_RESOURCES/RES_Ebook/books
```

Verify PDF exists and has correct page count (~12-15 pages).

- [ ] **Step 7: Visual check — screenshot key pages**

Use Playwright to take PNG screenshots of pages 1-5 for quick review:

```bash
cd _apps/scripts/pdf_pipeline && python -c "
from playwright.sync_api import sync_playwright
from pathlib import Path
p = sync_playwright().start()
browser = p.chromium.launch()
page = browser.new_page()
page.goto(Path('build/test-ai.html').resolve().as_uri())
page.screenshot(path='build/test-ai-preview.png', full_page=True)
browser.close()
p.stop()
print('Screenshot: build/test-ai-preview.png')
"
```

- [ ] **Step 8: Commit test book**

```bash
git add 30_RESOURCES/RES_Ebook/books/test-ai/
git commit -m "feat(book-pipeline): add test book with all component examples"
```

---

## Task 8: Run all tests + final validation

- [ ] **Step 1: Run full test suite**

```bash
cd _apps/scripts/pdf_pipeline && python -m pytest tests/ -v
```
Expected: all tests PASS.

- [ ] **Step 2: Verify PDF output**

Check `_apps/scripts/pdf_pipeline/build/test-ai.pdf` exists and visually inspect:
- Cover page (CSS-generated, dark theme)
- Legal page
- "Jak czytac" page with icon legend
- Table of Contents with 3 chapters
- Chapter 1 opener with mini-TOC + reading time
- Drop cap on first paragraph
- Stats, callouts, prerequisites, info boxes
- Chapter 2: quote, process flow, timeline, exercise, code block, decision tree
- Chapter 3: tiles, before/after, checklist, highlight, pull quote, compare, QR codes, CTA
- Glossary (LLM, RAG — collected from chapter 1)
- Resources page (QR codes from chapter 3)
- Series promo
- Back cover with testimonial

- [ ] **Step 3: Commit all remaining changes**

```bash
git add -A _apps/scripts/pdf_pipeline/
git commit -m "feat(book-pipeline): complete pipeline — all tests passing, test book generated"
```

---

## Deferred Features

These features from the spec are intentionally deferred from this implementation:

- **Running headers** (`@page :left/:right`) — Playwright has limited support for CSS `string()` function. Revisit with WeasyPrint engine.
- **Auto-numbered figures** (Rysunek X.N) — add when books actually use figures
- **`--chapter` single-chapter build** — add when the full pipeline is proven and there's a need for partial builds
- **Cover from external JPG** — works in code (auto_sections.py), but test book uses CSS fallback. Test with real JPG when first real book cover is designed.
