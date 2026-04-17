# DOKODU Book Pipeline — Design Spec

## Problem

Kacper chce budowac biblioteke e-bookow Dokodu (darmowe lead magnety + platne). Istniejacy pipeline (`scripts/pdf_pipeline/`) wymaga recznego pisania HTML. Potrzeba warstwy Markdown → HTML ktora pozwoli szybko pisac i generowac profesjonalne PDF-y na poziomie wydawnictw (Helion, O'Reilly, Manning).

## Solution

Dwuwarstwowy system:
1. **Extended Markdown converter** (Python) — zamienia MD z rozszerzeniami (`:::component`) na HTML z klasami z istniejacego `base.css`
2. **AI layout layer** — Claude analizuje rozdzialy na biezaco, pilnuje rytmu wizualnego, wstawia komponenty, generuje auto-sekcje (glossary, summary, TOC)

## Architecture

### File Structure

```
30_RESOURCES/RES_Ebook/books/
  <book-slug>/
    book.yaml          # metadane (tytul, autor, cover, seria)
    cover.jpg          # cover zaprojektowany zewnetrznie (Canva/Figma)
    01_chapter.md       # rozdzialy w Markdown
    02_chapter.md
    assets/             # obrazki, diagramy

scripts/pdf_pipeline/
    build_book.py       # NEW: orchestrator (MD → HTML → PDF)
    md_to_html.py       # NEW: extended Markdown parser
    templates/
        base.css        # EXISTING + nowe komponenty (drop cap, running headers, etc.)
        book.html       # NEW: HTML template wrapper
```

### book.yaml Schema

```yaml
title: "Tytul Ksiazki"
subtitle: "Podtytul z opisem"
author: "Kacper Sieradzinski"
author_role: "CEO Dokodu | AI Trainer"
brand: "DOKODU"
version: "1.0"                    # wersjonowanie (AI sie szybko zmienia)
date: "kwiecien 2026"
cover_image: cover.jpg            # zewnetrzny JPG (fullbleed pierwsza strona)
badge: "PRZEWODNIK 2026"

# Back cover
back_cover:
  description: "Krotki opis ksiazki na tylna okladke"
  testimonials:
    - text: "Swietna publikacja"
      author: "Jan Kowalski, CTO FirmaX"

# Seria (cross-sell)
series:
  name: "Dokodu AI Library"
  other_books:
    - title: "Agenci AI w Praktyce"
      slug: ai-agenci
    - title: "Automatyzacja z n8n"
      slug: automatyzacja-n8n

# Sekcje auto-generowane
auto_sections:
  how_to_read: true       # strona "Jak czytac te ksiazke"
  glossary: true           # slowniczek terminow AI (auto z :::info)
  resources: true          # strona z zasobami + QR kody
  legal: true              # strona prawna (copyright, wersja)
```

### Extended Markdown Syntax

Standard Markdown works as-is (`#`, `**`, `-`, `>`, code blocks, tables, links).

Custom components use `:::name` fenced blocks. All end with `:::` on own line.

#### Chapter Frontmatter (YAML in each .md file)
```yaml
---
chapter: 1
title: Czym jest AI
subtitle: Od buzzwordu do narzedzia pracy
reading_time: 8 min
prerequisites:
  - Konto OpenAI (darmowe)
  - Przegladarka Chrome
---
```
Generates: `.chapter-opener` full-page spread with chapter number, title, subtitle, reading time, mini-TOC (auto from H2s in chapter).

#### Core Components (existing CSS)

| Syntax | CSS Class | Description |
|--------|-----------|-------------|
| `:::callout tip` | `.callout.tip` | Callout box (tip/warning/info/danger) |
| `:::callout trap` | `.callout.danger` | "Uwaga na pulapke" — czesty blad |
| `:::stats` | `.stat-grid > .stat-box` | 3-column stat boxes. `value \| label` per line |
| `:::tiles N` | `.tile-grid.cols-N` | Tile grid (2/3 cols). `Title \| Description` per line |
| `:::quote` | `.quote-block` | Quote block. Last `--- Author` = attribution |
| `:::process` | `.process-flow` | Horizontal process steps. `Title \| Description` per line |
| `:::timeline` | `.timeline` | Vertical timeline. `Year \| Title \| Description` per line |
| `:::info` | `.info-box` | Info/glossary term. First line = term, rest = explanation |
| `:::highlight` | `.highlight-bar` | Highlighted bar (centered, accent bg) |
| `:::cta` | `.cta-section` | CTA section. Lines: heading, paragraph, contact |
| `:::compare` | `.comparison-table` | Comparison cards. Blocks separated by `---` |
| `:::value-stack` | `.value-stack` | Value stack (Hormozi). `name \| price`, last = total |

#### New Components (require new CSS)

| Syntax | CSS Class | Description |
|--------|-----------|-------------|
| `:::summary` | `.chapter-summary` | Podsumowanie rozdzialu — "Kluczowe wnioski" box na koncu |
| `:::exercise` | `.exercise-box` | "Sprobuj sam" — cwiczenie z instrukcja |
| `:::checklist` | `.checklist` | Lista z checkboxami (czytelnik moze odhaczyc w druku) |
| `:::prerequisites` | `.prerequisites-box` | "Czego potrzebujesz" box |
| `:::qr URL` | `.qr-block` | QR kod generowany z URL + opis |
| `:::code LANG` | `.code-block.lang-X` | Blok kodu z naglowkiem jezyka + numeracja linii |
| `:::pullquote` | `.pull-quote` | Duzy dekoracyjny cytat wyrwany z tekstu |
| `:::decision` | `.decision-tree` | Diagram decyzyjny (tak/nie flowchart w CSS) |
| `:::beforeafter` | `.before-after` | Porownanie "Przed" vs "Po" side-by-side |
| `:::series` | `.series-promo` | Promo innych ksiazek z serii (auto z book.yaml) |

#### Auto-generated Sections

Te sekcje generuja sie automatycznie — nie trzeba ich pisac recznie:

| Section | Source | Description |
|---------|--------|-------------|
| Cover page | `cover.jpg` | Fullbleed JPG z zewnetrznego pliku |
| Legal page | `book.yaml` | Copyright, wersja, rok, autor |
| "Jak czytac" | `book.yaml` | Objasnienie oznaczeń (ikony tip/warning/exercise) |
| Table of Contents | chapter titles | Auto z tytulow rozdzialow |
| Mini-TOC per chapter | H2 headings | Lista sekcji na chapter opener |
| Chapter summary | AI-generated | "Kluczowe wnioski" na koncu rozdzialu |
| Glossary | `:::info` blocks | Zbiera wszystkie :::info w slowniczek na koncu |
| Resources + QR | `:::qr` blocks | Zbiera linki + generuje strone z QR kodami |
| "Zobacz takze" | `book.yaml.series` | Promo innych ksiazek z serii |
| Back cover | `book.yaml.back_cover` | Opis + testimoniale + logo |

### AI Layout Layer

Claude analizuje rozdzialy podczas pisania i pilnuje:

1. **Rytm wizualny** — max 2 strony czystego tekstu pod rzad, potem komponent wizualny (stat box, callout, diagram, quote)
2. **Roznorodnosc komponentow** — nie powtarza tego samego komponentu 2x pod rzad
3. **Auto-summary** — po napisaniu rozdzialu generuje 3-5 bullet pointow jako `:::summary`
4. **Auto-glossary** — terminy z `:::info` zbiera do slowniczka na koncu ksiazki
5. **Auto-resources** — linki z `:::qr` zbiera na strone zasobow
6. **Sugestie** — "tu by pasował stat box", "za duzo tekstu, wstaw callout"
7. **Numeracja figur** — auto-numeruje rysunki per rozdział (Rysunek 1.1, 1.2...)

To nie jest osobny skrypt — to jest **workflow w skillu `/book write`** ktory Claude wykonuje podczas pisania.

### Data Flow

```
book.yaml + cover.jpg
      |
      v
  Claude (AI layout layer)
  - Pisze rozdzialy w extended MD
  - Analizuje rytm wizualny
  - Wstawia komponenty
  - Generuje auto-sekcje
      |
      v
  *.md files (rozdzialy)
      |
      v
  md_to_html.py
  - cover.jpg → fullbleed cover page
  - Legal page, "Jak czytac", TOC (auto-generated)
  - Parse chapters: YAML frontmatter → chapter openers
  - Standard MD → HTML (python-markdown)
  - :::component blocks → HTML with base.css classes
  - Collect :::info → glossary, :::qr → resources page
  - Generate back cover from book.yaml
  - Wrap in book.html template
      |
      v
  Combined HTML file
      |
      v
  build_book.py → Playwright → PDF
      |
      v
  scripts/pdf_pipeline/build/<book-slug>.pdf
```

### md_to_html.py — Parser Design

Python module (~350 lines). Core logic:

1. **Read book.yaml** → store metadata
2. **Generate front matter pages:**
   a. Cover page (fullbleed `cover.jpg`)
   b. Legal page (copyright, version, date)
   c. "Jak czytac te ksiazke" page (icon legend)
   d. Table of Contents (from chapter titles)
3. **For each chapter .md** (sorted by filename):
   a. Extract YAML frontmatter → generate `.chapter-opener` with mini-TOC + reading time
   b. Split content into blocks: regular markdown vs `:::component` blocks
   c. Regular markdown → `python-markdown` with `tables`, `fenced_code`, `codehilite` extensions
   d. Component blocks → custom renderer per component type
   e. First paragraph gets drop cap CSS class
   f. Collect `:::info` terms for glossary, `:::qr` URLs for resources
   g. Auto-number figures (Rysunek X.N)
   h. Wrap chapter content in `<div class="content">`
4. **Generate back matter pages:**
   a. Glossary (alphabetical, from collected :::info terms)
   b. Resources page (collected :::qr links with inline QR images)
   c. "Zobacz takze" series page (from book.yaml.series)
   d. Back cover (description, testimonials, logo)
5. **Assemble** front matter + chapters + back matter into single HTML
6. **Wrap** in `book.html` template

Component renderers:
```python
RENDERERS = {
    # Existing CSS
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
    # New CSS
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

### build_book.py — Orchestrator

CLI interface:
```bash
python build_book.py ai-praktycznie                    # build specific book
python build_book.py ai-praktycznie --preview          # open PDF after build
python build_book.py ai-praktycznie --chapter 02       # single chapter (with cover + opener)
```

Steps:
1. Find book dir in `30_RESOURCES/RES_Ebook/books/<slug>/`
2. Call `md_to_html.py` to generate combined HTML
3. Import and call `build_with_playwright()` from `build_pdf.py` directly (no subprocess)
4. Output to `scripts/pdf_pipeline/build/<slug>.pdf`

### New CSS Components (additions to base.css)

```css
/* Drop Cap */
.drop-cap::first-letter {
    float: left; font-size: 3.8em; line-height: 0.8;
    font-weight: 800; color: var(--color-primary);
    margin: 0.05em 0.12em 0 0; font-family: var(--font-heading);
}

/* Running Headers */
@page :left { @top-left { content: string(book-title); } }
@page :right { @top-right { content: string(chapter-title); } }

/* Chapter Summary */
.chapter-summary { background: var(--color-bg-light); border-top: 3px solid var(--color-primary); padding: 24px; }

/* Exercise Box */
.exercise-box { border: 2px dashed var(--color-info); padding: 22px; }

/* Checklist */
.checklist li::before { content: '☐'; }

/* Pull Quote */
.pull-quote { font-size: 1.4rem; text-align: center; border-top/bottom: 2px solid var(--color-primary); }

/* Before/After */
.before-after { display: grid; grid-template-columns: 1fr 1fr; }

/* QR Block */
.qr-block { text-align: center; }
.qr-block img { width: 120px; }

/* Code Block with Language Header */
.code-block .code-header { background: var(--color-primary); color: white; padding: 8px 16px; }

/* Reading Time Badge */
.reading-time { font-size: 0.75rem; color: var(--color-text-muted); }

/* Series Promo */
.series-promo { background: var(--color-bg-light); }
```

### book.html Template

```html
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="templates/base.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@700;800&family=JetBrains+Mono&display=swap');
    </style>
</head>
<body>
    CONTENT_PLACEHOLDER
</body>
</html>
```

Template uses simple `str.replace('CONTENT_PLACEHOLDER', html_content)` — no Jinja2 needed.

### Error Handling

- Unknown `:::component_name` → warning printed, content rendered as plain paragraph
- Unclosed `:::` block → treat EOF as implicit close + warning
- Missing `book.yaml` → error with helpful message
- Missing `cover.jpg` → fallback to CSS-generated cover (existing dark/light)
- Empty chapter file → skip with warning

## Dependencies

- `python-markdown` — standard Markdown → HTML (pip install markdown)
- `pyyaml` — YAML parsing (pip install pyyaml)
- `qrcode[pil]` — QR code generation (pip install qrcode[pil])
- `Pygments` — syntax highlighting for code blocks (pip install Pygments)
- `playwright` — already installed (used by existing build_pdf.py)

## Test Plan

1. Create test book `30_RESOURCES/RES_Ebook/books/test-ai/` with 3 short chapters
2. Include `cover.jpg` (placeholder)
3. Each chapter uses different components to test all renderers
4. Build PDF, verify:
   - Cover page renders JPG fullbleed
   - Legal page, "Jak czytac", TOC auto-generated
   - Chapter openers show mini-TOC + reading time
   - Drop cap on first paragraph of each chapter
   - All components render correctly
   - Glossary collects :::info terms
   - Resources page collects :::qr links
   - QR codes render inline
   - Code blocks have language headers + syntax highlighting
   - Page breaks work (no orphaned headings)
   - Running headers show book/chapter titles
   - Back cover with testimonials
   - "Zobacz takze" with series books

## Out of Scope (for now)

- AI-generated cover images (covers designed externally)
- EPUB output
- Interactive/web version
- Migration of existing ebook_moj.txt
- ISBN assignment
