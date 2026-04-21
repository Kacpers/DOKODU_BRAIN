---
name: brain-new-ebook
description: Tworzy ebook w systemie 11 szablonów stron Dokodu (light paper, navy ink, pomarańczowy akcent). Prowadzi przez plan (temat, ToC, audience), generuje strukturę book.yaml + rozdziały markdown, składa HTML wg design systemu z `30_RESOURCES/RES_Ebook/design_system/`. NIE myl z `brain-new-offer` (to jest oferta handlowa) — ten skill jest wyłącznie do publikacji edukacyjnych. Trigger słowa — "nowy ebook", "napisz ebook", "stwórz książkę", "przygotuj publikację", "ebook o", /brain-new-ebook.
---

# brain-new-ebook — Generator Ebooków Dokodu

## Cel

Wygenerować gotowy ebook w estetyce dokodu.it (ciepły kremowy papier, deep-navy tekst, pomarańczowy akcent) wykorzystując 11-szablonowy design system. Output: HTML + docelowo PDF przez Playwright. Treść uzupełniana z plików Markdown — nigdy nie używamy Canvy.

**To NIE jest skill od ofert** — do ofert handlowych używaj `/brain-new-offer`. Ten skill służy tylko ebookom, przewodnikom, compendiom, whitepaperom.

## Kiedy używać / Kiedy NIE używać

**Używaj gdy:**
- Tworzysz nowy ebook / przewodnik / whitepaper dla Dokodu
- Masz gotowy szkic treści i chcesz go złożyć w wizualnie spójny dokument
- Chcesz rozbić duży materiał na rozdziały i szablony (case, cheat, infografika)

**NIE używaj gdy:**
- Piszesz ofertę handlową → `/brain-new-offer`
- Piszesz post na blog → `/blog-draft`
- Piszesz newsletter → edytuj plik w `20_AREAS/AREA_Newsletter/`
- Przetwarzasz nagrania do ebooka (najpierw `/meet-transcribe` lub `/yt-repurpose`)

---

## KROK 1: Zbierz dane o ebooku

Zapytaj (maksymalnie 7 pytań naraz):

1. **Tytuł** — roboczy / finalny? (np. "Sztuczna inteligencja w praktyce")
2. **Podtytuł** — jedno zdanie, co czytelnik dostaje
3. **Slug** — skrót do folderu (np. `ai-praktyka`, `agenci-ai`)
4. **Audience** — dla kogo? (CEO MŚP, devopsi, prawnicy, sprzedaż?)
5. **Format** — A4 portrait 1240×1754 (default) / inny?
6. **Liczba rozdziałów** — orientacyjnie (8 jest optymalne)
7. **Status startu** — od zera (potrzebuję pomóc z TOC) / mam gotowe rozdziały MD?

Jeśli rozdziały są gotowe → zapytaj o ścieżkę do plików markdown.

---

## KROK 2: Zaproponuj strukturę (TOC)

Na podstawie tematu i audience zaproponuj 6–10 rozdziałów z:
- numerem (01–10)
- tytułem
- abstraktem (1 zdanie)
- orientacyjną liczbą stron (4–20)
- liczbą sekcji (3–6)

Przykład wzorcowy — patrz `30_RESOURCES/RES_Ebook/design_system/preview.html` sekcja TOC (chapters).

Po zatwierdzeniu przez Kacpra → przejdź dalej.

---

## KROK 3: Zaproponuj mapę szablonów

Dla każdego rozdziału zaproponuj, które z **11 typów stron** użyjemy:

| # | Template | Kiedy użyć |
|---|---|---|
| 01 | `cover` | Okładka — raz na cały ebook (dark + bleed) |
| 02 | `toc` | Spis treści — raz, zaraz po okładce |
| 03 | `chapter` | Otwarcie rozdziału — przed każdym rozdziałem (dark + bleed) |
| 04 | `standard` | Strona tekstowa — 2 kolumny + sidenotes, "workhorse" wnętrza |
| 05 | `case` | Case study / wywiad — Q&A + 4 KPI cards + pull-quote |
| 06 | `info` | Infografika / wykres SVG — architektura, flow |
| 07 | `cheat` | Cheat sheet — 6 kart z szablonami / listami kontrolnymi |
| 08 | `code` | Code deep-dive — listing 2:1 + callouts do linii |
| 09 | `data` | Tabela + bar chart — benchmarks, porównania |
| 10 | `image` | Spread pull-quote — full-bleed dark, przełamanie rytmu |
| 11 | `back` | Zamknięcie + kolofon + CTA — raz, ostatnia strona |

Zasada: **tylko okładka, otwarcie rozdziału i spread zdjęciowy są dark-mode** — reszta jest light (kremowy papier). Tak działa kontrapunkt.

Pokaż mapę jako tabelę `rozdział × typ stron`. Czekaj na OK.

---

## KROK 4: Utwórz strukturę plików

Lokalizacja: `/home/kacper/DOKODU_BRAIN/30_RESOURCES/RES_Ebook/books/<slug>/`

Struktura:
```
books/<slug>/
├── book.yaml           ← metadata + TOC + mapa szablonów
├── chapters/
│   ├── 01_<slug>.md
│   ├── 02_<slug>.md
│   └── ...
├── assets/             ← obrazy, wykresy SVG (placeholdery OK)
└── build/              ← generowane HTML + PDF (gitignore)
```

### Szablon `book.yaml`

```yaml
title: "<Tytuł>"
subtitle: "<Podtytuł>"
slug: <slug>
author: "Kacper Sieradziński"
author_role: "CEO Dokodu | AI Trainer"
brand: "DOKODU"
version: "0.1"
date: "<miesiąc rok>"
edition: "PL / Vol. 01"
badge: "<PRZEWODNIK 2026>"
isbn: "978-83-XXXX-XXX-X"
pages_target: 284

audience:
  primary: "<np. CEO MŚP 50-500 prac.>"
  level: "<początkujący | średniozaawansowany | ekspert>"

design_system: "30_RESOURCES/RES_Ebook/design_system"
palette: light   # tylko cover/chapter/image-led są dark
format:
  w: 1240
  h: 1754
  margin: 72
  cols: 12
  gutter: 24

chapters:
  - n: "01"
    title: "<Tytuł rozdziału>"
    abstract: "<1 zdanie — co czytelnik zyska>"
    slug: <slug>
    file: chapters/01_<slug>.md
    pages: 12
    parts: 4
    templates: [chapter, standard, standard, info, standard]

  - n: "02"
    title: "..."
    # ...

back_cover:
  description: "<opis back cover>"
  testimonials:
    - text: "<cytat>"
      author: "<imię, stanowisko, firma>"

cta:
  primary:
    label: "Umów bezpłatną konsultację"
    url: "dokodu.it/konsultacje"
  secondary:
    label: "Kontynuuj na blogu"
    url: "dokodu.it/blog"

colophon:
  publisher: "Dokodu sp. z o.o."
  address: "ul. Kosynierów 76/22, 84-230 Rumia"
  email: "biuro@dokodu.it"
  krs: "0000925166"
  typography: "Inter + JetBrains Mono"
  paper: "120 g, matowy"
  print: "Poligrafia Gdańsk"
```

### Szablon pojedynczego rozdziału `01_<slug>.md`

Każdy rozdział ma front-matter, który informuje renderer jaki szablon użyć dla którego bloku:

```markdown
---
n: "01"
title: "Wstęp do LLM"
abstract: "Jak modele językowe widzą świat. Tokeny, wektory, uwaga."
reading_time: "42 min"
level: "Średniozaawansowany"
sections: "1.1 – 1.5"
---

<!-- template: chapter -->
# Wstęp do LLM

<!-- template: standard -->
## 1.1 Dlaczego kontekst jest ważniejszy niż instrukcja

> **†** przypis 01: Termin "prompt engineering" został spopularyzowany w 2022.

Model językowy nie "wie" nic o Twoim projekcie, dopóki tego nie powiesz...

<!-- template: info -->
## 1.2 Architektura Transformer

![diagram:transformer](assets/transformer.svg "Uproszczona reprezentacja przepływu tokenów")

<!-- template: code -->
## 1.3 RAG w 40 liniach

```python
# rag_pipeline.py
from openai import OpenAI
# ...
```

<!-- template: cheat -->
## 1.4 Cheat Sheet — 6 zasad dobrego promptu

1. Bądź konkretny → "Napisz 3 akapity o X, styl formalny, 200 słów."
2. Daj przykłady → few-shot działa
3. Nadaj rolę → "Jesteś senior DevOps z 10-letnim stażem"
...
```

Konwencje markdownu:
- `<!-- template: <id> -->` — przełącza typ strony dla poniższego bloku
- `> **†** przypis N:` — sidenote / przypis
- `![diagram:<nazwa>](...)` — placeholder na generatywną grafikę
- Callout block: `> [!tip]` / `[!warning]` / `[!info]` (ikony SVG)

---

## KROK 5: Wygeneruj preview HTML

Skrypt renderujący `build_ebook.py` — TODO, póki co:

1. Otwórz `30_RESOURCES/RES_Ebook/design_system/preview.html` w przeglądarce żeby zobaczyć wszystkie 11 szablonów "na żywo"
2. Dla MVP — podmień dane w komponentach React (`chapters` w `pages1.jsx PageTOC`, treść w `LOREM`) na treść z rozdziałów
3. Finalny pipeline: markdown → HTML per szablon → złożenie w jeden długi HTML → Playwright → PDF

**Uwaga o czcionkach** (krytyczne, per `feedback_book_pipeline.md`):
- Używaj self-hosted woff2 (Inter + JetBrains Mono) z `templates/fonts/`
- NIGDY `@import` Google Fonts w plikach do PDF — Playwright nie czeka na fonty z sieci
- Code block: Pygments `style='monokai'`, `noclasses=True`

**Polskie znaki** — obowiązkowe, nigdy nie wycinaj diakrytyków (ą, ę, ć, ś, ź, ż, ó, ł, ń). Dotyczy też hardcoded stringów w rendererach.

---

## KROK 6: Checklist jakości

Zanim oznaczysz ebook jako "gotowy do wysyłki":

- [ ] `book.yaml` — wszystkie pola wypełnione
- [ ] Każdy rozdział ma frontmatter (n, title, abstract, reading_time, level, sections)
- [ ] Mapa szablonów — dla każdego rozdziału wybrany odpowiedni mix
- [ ] Okładka, otwarcie rozdziału i spread zdjęciowy zostają dark — reszta light
- [ ] Polskie znaki w całej treści (ą ę ć ś ź ż ó ł ń) — NIE wycinaj
- [ ] Znaki zapytania w nagłówkach-pytaniach
- [ ] Brak orphan headings (nagłówek nie zostaje sam na dole strony)
- [ ] Fonty self-hosted (Inter, JetBrains Mono) — nie Google Fonts
- [ ] Code blocks: Pygments monokai
- [ ] Ikony callout: inline SVG via CSS mask (nie emoji)
- [ ] Placeholdery w `assets/` podmienione lub jawnie oznaczone jako `[PLACEHOLDER]`
- [ ] CTA w back cover — `dokodu.it/konsultacje` + `dokodu.it/blog`
- [ ] Kolofon: email `biuro@dokodu.it`, KRS `0000925166`

---

## KROK 7: Zaktualizuj indeks

Po zapisaniu ebooka:
1. Dodaj wpis do `30_RESOURCES/RES_Ebook/README.md` (jeśli istnieje) lub pozostaw w `books/<slug>/book.yaml`
2. Jeśli ebook to lead magnet → dodaj do planu promocji newslettera
3. Jeśli to publikacja płatna → odnotuj w `001_VISION.md` / `000_DASHBOARD.md`

---

## Design system — skrót

Pełny opis: `30_RESOURCES/RES_Ebook/design_system/README.md`

**Paleta (light):**
- Paper: `#FAF7F0` (warm cream)
- Ink: `#141B2D` (deep navy)
- Orange: `oklch(0.70 0.17 50)` (Dokodu accent)
- Hairline: `rgba(20,25,45,0.10)`

**Paleta (dark — tylko cover/chapter/image-led):**
- Bg: `#0B1120`
- Text: `#F5F1E6`
- Orange accent zachowany

**Typografia:**
- `Inter` (sans): 200–800
- `JetBrains Mono` (mono): 400–600
- H1: 88–132 px, letter-spacing -0.035em
- Body: 13.5–14 px, line-height 1.6–1.7
- Meta mono: 10–11 px, letter-spacing 0.18–0.25em, UPPERCASE

**11 szablonów stron:** cover, toc, chapter, standard, case, info, cheat, code, data, image, back.

Preview wszystkich: `open 30_RESOURCES/RES_Ebook/design_system/preview.html`

---

## Zasady wyniku

- **Treść w polszczyźnie** — zawsze pełne diakrytyki, znaki zapytania, interpunkcja
- **Forma grzecznościowa** — "Państwo" nie "Wy" (feedback `pastwo_form`)
- **Aktualny rok 2026** — nie 2025 (feedback `current_year`)
- **Praktyk, nie marketer** — styl zgodny z `TOV_Dokodu.md` (30_RESOURCES/RES_Templates/)
- **Jeden source of truth** — treść tylko w `chapters/*.md`, nie duplikuj w book.yaml
- **Każdy rozdział kończy się call-to-think** — pytanie, ćwiczenie lub cheat sheet (nie pusty akapit)
