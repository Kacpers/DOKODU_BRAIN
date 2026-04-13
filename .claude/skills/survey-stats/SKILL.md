---
name: survey-stats
description: Analizuje wyniki ankiet poszkoleniowych z DOKODU_BRAIN i wyciąga actionable insights. Identyfikuje co uczestnicy cenią, co wymaga poprawy, najlepsze cytaty, trendy. Zapisuje wnioski do Survey_Insights.md. Trigger: "zanalizuj ankiety", "insighty z ankiet", "co mówią uczestnicy", "wnioski ze szkoleń", /survey-stats
---

# Instrukcja: Survey Stats

## Działanie

Czyta `Survey_Last_Sync.md` i przeprowadza głęboką analizę wyników ankiet.
Wyniki zapisuje do `DOKODU_BRAIN/20_AREAS/AREA_Szkolenia/Survey_Insights.md`.

## KROK 1: Wczytaj dane

Przeczytaj plik:
`/home/kacper/DOKODU_BRAIN/20_AREAS/AREA_Szkolenia/Survey_Last_Sync.md`

Jeśli plik nie istnieje lub jest pusty — powiedz użytkownikowi żeby najpierw odpalił `/survey-sync`.

## KROK 2: Analiza

Przeanalizuj dane i wyciągnij:

### Metryki ogólne
- Średnia ocena szkoleń (wszystkie / per klient)
- Średnia ocena trenera
- % poleceń (wouldRecommend >= 4)
- Rozkład tempa — czy szkolenia są za szybkie?

### Top insights (max 5 bullet points)
Co najczęściej powtarza się w odpowiedziach otwartych? Jakie wzorce?

### Cytaty do wykorzystania (marketing)
Wybierz 3-5 najlepszych cytatów (tylko te z `publishConsent = true`).
Format: > "Cytat..." — [Firma, data]

### Obszary do poprawy
Co uczestnicy najczęściej wymieniają jako do poprawy?

### Pomysły automatyzacyjne uczestników
Lista unikalnych pomysłów na automatyzację — potencjalnie tematy na nowe szkolenia.

### Trendy vs poprzednia synchronizacja
Jeśli istnieje poprzedni `Survey_Insights.md` — porównaj z poprzednim raportem.

## KROK 3: Zapisz wnioski

Napisz i zapisz plik `Survey_Insights.md`:

```markdown
---
last_updated: [DATA]
total_responses: [N]
avg_rating: [X.X]
---

# Survey Insights — Dokodu Szkolenia

> Ostatnia aktualizacja: [DATA]

## Kluczowe metryki
...

## Top 5 Insights
...

## Cytaty (zgoda na publikację)
...

## Obszary do poprawy
...

## Pomysły automatyzacyjne uczestników
...
```

## KROK 4: Zaproponuj następny krok

- Jeśli są cytaty z zgodą → zaproponuj dodanie do strony dokodu.it/o-nas lub materiałów sprzedażowych
- Jeśli powtarzają się pomysły na automatyzację → zaproponuj `/yt-plan-video` na ten temat
- Jeśli oceny są niskie w jakiejś kategorii → zaproponuj action item do INBOX

## ZASADY

- Cytaty pokazuj TYLKO jeśli `publishConsent = true` w danych
- Nie podawaj imion ani pełnych nazw firm w cytatach (chyba że dane mają token grupowy — wtedy firma jest ok)
- Insights muszą być actionable — nie opisuj, tylko rekomenduj
