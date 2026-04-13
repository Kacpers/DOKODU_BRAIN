---
name: yt-publish-kit
description: Generuje komplet materiałów do publikacji odcinka YouTube — thumbnail base (Remotion), opis, tagi, scenariusz do promptera, checklist. Wrzuca wszystko do Dropboxa. Trigger: "przygotuj kit do publikacji", "generuj materiały do YT", "zrób paczkę do publikacji", /yt-publish-kit
---

# Instrukcja: YT Publish Kit

## Działanie

Generuje komplet materiałów potrzebnych do publikacji odcinka na YouTube i wrzuca je do Dropboxa:

| Plik | Zawartość |
|------|-----------|
| `thumbnail_base.png` | Layer graficzny thumbnails (Remotion) — dodajesz twarz w Canvie |
| `opis_youtube.txt` | Pełny opis do wklejenia w YT Studio |
| `tagi.txt` | Tagi gotowe do wklejenia |
| `prompter.txt` | Scenariusz dla Parrot Promptera |
| `checklist.md` | Co zrobić przed i po publikacji |

## KROK 1: Ustal ID filmu

Zapytaj jeśli nie podano: "Dla którego odcinka? (np. YT-002)"

## KROK 2: Sprawdź gotowość

Przeczytaj `movies/YT-XXX/metadata.md` i potwierdź:
- Czy jest scenariusz (`scenariusz: true` w frontmatter)?
- Czy Remotion ma kompozycję `YT-XXX-Thumbnail`?

Jeśli brak scenariusza — ostrzeż: "Brak scenariusza — prompter.txt zostanie pominięty"
Jeśli brak kompozycji Thumbnail — uruchom z `--no-thumbnail` i powiedz że trzeba dodać

## KROK 3: Uruchom skrypt

```bash
cd /home/kacper/DOKODU_BRAIN/scripts && python3 yt_publish_kit.py YT-XXX
```

Jeśli brak kompozycji Thumbnail:
```bash
cd /home/kacper/DOKODU_BRAIN/scripts && python3 yt_publish_kit.py YT-XXX --no-thumbnail
```

## KROK 4: Pokaż wynik

Po wykonaniu pokaż:
- Co zostało wygenerowane (lista plików)
- Ścieżka Dropbox: `Scenariusze/YT-XXX_publish/`
- Następny krok: "Otwórz Canvę, wgraj thumbnail_base.png, dodaj twarz"

## KROK 5: Zaktualizuj tracker (opcjonalnie)

Jeśli Kacper powie że nagrał lub opublikował — zaktualizuj odpowiednie pola w:
- `metadata.md` (nagranie, opublikowany, link)
- `YT_Videos.md` tracker (✅ w odpowiedniej kolumnie)

## ZASADY

- Uruchamiaj zawsze z katalogu scripts: `cd /home/kacper/DOKODU_BRAIN/scripts`
- Remotion musi być uruchomiony lub nie — skrypt renderuje przez CLI, nie przez studio
- Jeśli render thumbnails trwa długo (>2 min) — sprawdź czy Remotion ma daną kompozycję
- Dropbox musi być dostępny przez `/mnt/c/Users/Kacper/Dropbox/`
