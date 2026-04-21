---
type: design-system
status: v1.0
owner: dokodu
last_reviewed: 2026-04-17
tags: [ebook, design-system, dokodu, inter, jetbrains-mono]
---

# Dokodu Ebook Design System (v1.0)

11-szablonowy system stron dla ebooków AI — zaprojektowany przez Claude Design, zainspirowany dokodu.it.

## Paleta (light paper)

| Token | Hex / OKLCH | Zastosowanie |
|---|---|---|
| `paper` | `#FAF7F0` | Ciepły kremowy papier — główne tło |
| `paperAlt` | `#F2ECDF` | Lekko ciemniejszy pas, tinted surface |
| `paperElev` | `#FFFFFF` | Karta elevated, code block |
| `surfaceTint` | `#EFE8D6` | Tło callout |
| `ink` | `#141B2D` | Deep navy — body text |
| `inkDim` | `#3A4560` | Drugorzędny tekst |
| `inkMute` | `#7A8299` | Meta / chrome |
| `orange` | `oklch(0.70 0.17 50)` | Akcent Dokodu (primary) |
| `orangeDeep` | `oklch(0.58 0.18 45)` | Akcent hover / emfaza |
| `navy` | `#141B2D` | Heading color |
| `blueInk` | `oklch(0.45 0.12 250)` | Link / subtelny emphasis |

## Paleta (dark — tylko cover, chapter break, image-led)

| Token | Hex | Zastosowanie |
|---|---|---|
| `bg` | `#0B1120` | Dark background |
| `bgElev` | `#111A30` | Dark elevated |
| `text` | `#F5F1E6` | Off-white tekst |

## Typografia

- **Sans**: `Inter` (200, 300, 400, 500, 600, 700, 800) — headings + body
- **Mono**: `JetBrains Mono` (400, 500, 600) — code, meta, numerologia
- H1 hero: 88–132px / 0.92 lh / -0.035em tracking
- H2 section: 40–52px / 1.0 lh / -0.025em
- Body: 13.5–14px / 1.6–1.7 lh
- Meta mono: 10–11px / 0.18–0.25em letter-spacing / UPPERCASE

## Format strony

- 1240 × 1754 px (A4 portrait, 150 dpi-eq.)
- 12 kolumn, 24 px gutter, 72 px margin
- Export: HTML (preview) + PDF

## 11 typów stron

| # | ID | Nazwa | Wariant | Użycie |
|---|---|---|---|---|
| 01 | `cover` | Okładka / Hero | dark, bleed | 1× na ebook — strona tytułowa |
| 02 | `toc` | Spis treści | light | 1× — po okładce |
| 03 | `chapter` | Otwarcie rozdziału | dark, bleed | 1× przed każdym rozdziałem |
| 04 | `standard` | Strona tekstowa | light | Większość wnętrza — 2 kol + sidenotes |
| 05 | `case` | Case study / wywiad | paperAlt | Q&A + KPI cards + pull-quote |
| 06 | `info` | Infografika / wykres | light | SVG diagramy, schematy |
| 07 | `cheat` | Cheat sheet | paperAlt | 6 kart 3×2 z szablonami |
| 08 | `code` | Code deep-dive | light | Listing 2:1 + callouts L.xx-yy |
| 09 | `data` | Tabela + wykres | light | Benchmark, dane, bar chart |
| 10 | `image` | Spread zdjęciowy | dark, bleed | Pull-quote full-bleed |
| 11 | `back` | Zamknięcie / kolofon | paperAlt | 1× — ostatnia strona |

## Struktura plików

```
design_system/
├── README.md                 ← ten plik
├── preview.html              ← podgląd wszystkich 11 szablonów w React
└── components/
    ├── tokens.jsx            ← design tokens + Page shell + helpers
    ├── pages1.jsx            ← Cover, TOC, Chapter
    ├── pages2.jsx            ← Standard, Case, Info, Cheat
    └── pages3.jsx            ← Code, Data, Image, Back
```

## Jak używać

1. `/brain-new-ebook` — skill prowadzi przez wybór tematu, TOC, treść
2. Otwórz `preview.html` w przeglądarce żeby zobaczyć wszystkie 11 szablonów
3. Kopiuj komponent React z wybranym szablonem, podmieniaj treści
4. Output: `books/<slug>/` z `book.yaml` + `chapters/*.md` + wyrenderowane HTML/PDF

## Źródło

- Design: Claude Design handoff (2026-04-17), paleta inspirowana dokodu.it
- Adaptacja: warm cream paper zamiast pure white (ciepły, matowy look książki)
- Akcent: pomarańczowy Dokodu jako primary — spójny z brandingiem
