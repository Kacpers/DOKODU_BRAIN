# Assets — Pierwsze 90 dni z AI w firmie

Placeholdery grafik i wykresów do podmiany przed publikacją.

## Lista wymaganych assetów

| Plik | Typ | Rozdział | Opis | Status |
|---|---|---|---|---|
| `cover_bg.svg` | Generatywne tło | Okładka | Gradient mesh + siatka punktów (dark mode). Patrz `design_system/components/pages1.jsx` `PageCover` | do zrobienia |
| `process_map_sheet.svg` | Diagram | 2.3 | Szkielet arkusza Excel — 8 kolumn, tabela | do zrobienia |
| `pilot_architecture.svg` | Diagram | 4.4 | 3 warstwy (ingest → processing → HITL) — flow poziomy | do zrobienia |
| `cumulative_roi.svg` | Wykres | 7.3 | Krzywa kumulatywna 12 miesięcy, break-even w miesiącu 4 | do zrobienia |
| `portret_mw.jpg` | Zdjęcie | 5.1 | Portret Magdaleny Wiśniewskiej (CFO NovaLogistics) — 180×180 px kwadrat | licencja do załatwienia |
| `imagespread_ch5.jpg` | Full-bleed | 5.3 | Zdjęcie zespołu finansów NovaLogistics — 1240×1754 portrait, low-sat, chłodna tonacja | do wyboru z banku |
| `transformer_diagram.svg` | Diagram (opcjonalny) | — | Może wejść jako alternatywa w rozdziale 4 jeśli Magdalena nie da zgody na portret | opcjonalne |

## Konwencje

- **SVG** — preferowane dla diagramów (skalują się, small file size, łatwo edytować)
- **JPG** — dla zdjęć, min. 300 dpi-eq. przy 1240×1754
- **Nazewnictwo** — snake_case, bez polskich znaków, bez spacji
- **Placeholdery** — w markdown używaj `![diagram:<nazwa>](assets/<nazwa>.svg "caption")` — renderer podmieni na realne pliki
- **Case studies** — zawsze anonimizować lub zebrać pisemną zgodę (LOGO + wypowiedź = szczególnie wymaga zgody pisemnej)

## Stan obecny

Wszystkie asety są jeszcze placeholderami — ebook renderuje się, ale w miejscach diagramów/zdjęć pojawia się ramka z etykietą. To jest OK do review treści i layoutu. Do finalnej publikacji:

1. Zleć grafikowi SVG (`process_map_sheet`, `pilot_architecture`, `cumulative_roi`)
2. Poproś NovaLogistics o zdjęcie zespołu i portret CFO (`case_novalogistics.md` sekcja 5.3)
3. Wygeneruj cover w Remotion albo Canvie (dark mode + gradient mesh) i wyeksportuj jako SVG/PNG 1240×1754

Budżet wstępny: ~2 500 PLN za freelancera SVG + ~800 PLN za zdjęcia stockowe jako fallback.
