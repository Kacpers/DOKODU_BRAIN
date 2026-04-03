# PDF Pipeline — Design Notes

## Konfiguracja per ebook
Każdy ebook/oferta może mieć `config.json` z ustawieniami:
- `cover_style`: "light" (biała) lub "dark" (ciemna z gradientem)
- `cover_bg_image`: ścieżka do obrazu tła (opcjonalne)
- `accent_color`: override koloru akcentu (domyślnie #E63946)

## Wnioski z iteracji (2026-04-01)

### Czerwień — używać oszczędnie
- Accent #E63946 tylko do: kluczowych statystyk, CTA, jednego elementu na stronę
- Nagłówki h2: border-bottom zmienić na subtelniejszy (navy, nie czerwony)
- Diagramy: nie wszystko czerwone, używać navy jako bazę, czerwień tylko na highlight
- Timeline: oś w navy/szarym, tylko kropki w accent

### Żółty (#f0a500) — nie używać w timeline
- Gold/żółty irytujący w kontekście timeline, zarezerwować wyłącznie do stat boxów "gold variant"

### Emoji jako ikony — nie działają w PDF
- Playwright nie renderuje wszystkich emoji poprawnie
- Zamiast emoji użyć: SVG inline icons lub proste CSS shapes

### Podziały stron — kluczowe
- Każda sekcja h2 powinna zaczynać się na nowej stronie jeśli zostało <30% strony
- Nigdy nie zostawiać nagłówka bez minimum 3 linii tekstu pod spodem
- Kafelki/gridy: wymuszać page-break-inside: avoid na kontenerze, nie tylko elementach

### Font "I" problem
- Plus Jakarta Sans ma wąskie "I" które wygląda dziwnie w "AI"
- Rozwiązanie: użyć font-feature-settings lub zmienić font na Inter/DM Sans dla body
