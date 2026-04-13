---
name: mailerlite-stats
description: Analizuje dane newslettera z MailerLite i wyciąga actionable insights. Ocenia open rate vs benchmark, identyfikuje najlepsze i najgorsze kampanie, rekomenduje co poprawić w subject line i częstotliwości wysyłki. Trigger: "zanalizuj newsletter", "insighty z mailerlite", "jak radzi sobie newsletter", "statystyki newslettera", /mailerlite-stats
---

# Instrukcja: MailerLite Stats

## Działanie

Czyta `Newsletter_Last_Sync.md` i przeprowadza głęboką analizę wyników newslettera "Pracownik biurowy przyszłości".

## KROK 1: Wczytaj dane

Przeczytaj plik:
`/home/kacper/DOKODU_BRAIN/20_AREAS/AREA_Newsletter/Newsletter_Last_Sync.md`

Jeśli plik nie istnieje lub jest pusty — powiedz użytkownikowi żeby najpierw odpalił `/mailerlite-sync`.

## KROK 2: Analiza

### Metryki bazowe
- Aktywni subskrybenci — trend wzrostu (jeśli są dane historyczne)
- Avg Open Rate vs benchmark SaaS/Edukacja PL (25–35%)
- Avg CTR vs benchmark (3–5%)
- Unsubscribe rate (benchmark: <0.5%)

### Top 3 najlepsze kampanie
Które kampanie miały najwyższy open rate? Co je łączy? (typ tematu, pora wysyłki, długość subject line?)

### Bottom 3 kampanie
Które miały najniższy open rate? Co poszło nie tak?

### Wzorce subject line
Czy są wzorce w najlepiej otwieranych wiadomościach?
- Pytania vs twierdzenia
- Liczby vs brak liczb
- Długość subject line
- Personalizacja

### Stan list i segmentów
- Ile grup — czy są dobrze używane?
- Proporcja aktywni/wypisani — czy jest problem z higieną listy?

### Automatyzacje
- Czy welcome sequence istnieje?
- Czy jest nurturing dla leadów ze szkoleń/kursu?

## KROK 3: Top 5 Insights + Rekomendacje

Wygeneruj 5 konkretnych rekomendacji:

```markdown
## Insights i rekomendacje

1. **[Tytuł insightu]** — [obserwacja] → [konkretna akcja]
2. ...
```

## KROK 4: Zaproponuj następny krok

- Jeśli open rate < 25% → zaproponuj A/B test subject lines
- Jeśli brak welcome sequence → zaproponuj stworzenie 3-mailowego onboardingu
- Jeśli lista ma >20% nieaktywnych → zaproponuj kampanię reaktywacyjną
- Jeśli kampanie z liczbami/pytaniami wygrywają → zaproponuj dostosowanie stylu subject lines

## ZASADY

- Benchmarki dla branży edukacja/SaaS w Polsce: Open Rate 25–35%, CTR 3–5%
- Nie oceniaj kampanii jeśli mniej niż 100 odbiorców — zbyt mała próba
- Insights muszą być actionable — nie opisuj, tylko rekomenduj
- Newsletter Kacpra: "Pracownik biurowy przyszłości" — ton praktyczny, co-tygodniowy, 764 sub (stan z marca 2026)
