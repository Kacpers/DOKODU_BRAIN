---
name: seo-weekly
description: Tygodniowy przegląd SEO bloga dokodu.it — metryki GSC, pipeline postów, bottlenecki, plan na następny tydzień. Analogia do brain-weekly-review ale dla SEO. Trigger: "przegląd seo", "seo weekly", "co z blogiem", "tygodniowe seo", /seo-weekly
---

# Instrukcja: SEO Weekly Review

Cel: co piątek — 15 minut przeglądu stanu SEO bloga, żeby nie tracić momentum.

## KROK 1: Pobierz świeże dane

```bash
cd /home/kacper/DOKODU_BRAIN/scripts && python3 gsc_fetch.py --days 28 --save
```

Jeśli pojawi się błąd autoryzacji → przypomnij o GSC_SETUP.md i skróć przegląd do danych z bazy:
```bash
python3 gsc_fetch.py --from-db --mode opportunities
```

## KROK 2: Wczytaj kontekst

Przeczytaj:
- `DOKODU_BRAIN/20_AREAS/AREA_Blog_SEO/SEO_Last_Sync.md` — aktualne dane
- `DOKODU_BRAIN/20_AREAS/AREA_Blog_SEO/SEO_Insights.md` — poprzednie wnioski
- `DOKODU_BRAIN/20_AREAS/AREA_Blog_SEO/SEO_Ideas_Bank.md` — jeśli istnieje

## KROK 3: Raport tygodniowy

Wygeneruj raport w tym formacie:

---

## SEO Weekly — [data]

### 📊 Metryki (ostatnie 28 dni)
| Metryka | Wartość | vs poprzedni tydzień |
|---------|---------|---------------------|
| Kliknięcia | X | +/- X% |
| Impressions | X | +/- X% |
| Średnia pozycja | X | +/- X |
| CTR | X% | +/- X% |

*(jeśli nie ma danych historycznych — pomiń porównanie)*

### 🟢 Co się udało w tym tygodniu
- [konkretna obserwacja z danych]
- [post który zyskał pozycję / ruch]

### 🔴 Co nie działa / bottlenecki
- [strona/fraza która traci pozycję]
- [content gap bez akcji]

### 🎯 Top 3 Quick Wins na następny tydzień
1. [fraza/strona + konkretna akcja + oczekiwany efekt]
2. ...
3. ...

### 📝 Pipeline Postów
Sprawdź `seo_ideas.py list` mentalnie lub uruchom:
```bash
python3 /home/kacper/DOKODU_BRAIN/scripts/seo_ideas.py list
```

| Status | Liczba | Następna akcja |
|--------|--------|----------------|
| POMYSŁ | X | Zbadać frazy dla top 2 |
| BRIEF | X | Napisać post |
| PISANIE | X | Dokończyć / review |
| REVIEW | X | Opublikować |

### 🔮 Priorytety na następny tydzień
1. [konkretne zadanie z deadline]
2. [konkretne zadanie]
3. [konkretne zadanie]

---

## KROK 4: Trudne pytania (Executive Shadow)

Zadaj użytkownikowi 1-2 trudne pytania, np.:
- "Masz X postów w POMYSŁ od >2 tygodni bez przejścia do BRIEF — co blokuje?"
- "CTR to tylko X% przy dobrej pozycji — kiedy poprawisz meta opisy?"
- "Ostatni post opublikowany X tygodni temu — jaki jest Twój cel publikacji/mies.?"

## KROK 5: Dopisz do SEO_Insights.md

Dopisz skrócony wpis z kluczowymi obserwacjami tego tygodnia do:
`DOKODU_BRAIN/20_AREAS/AREA_Blog_SEO/SEO_Insights.md`

## ZASADY

- Jeśli brak świeżych danych GSC — powiedz to wprost i skróć review do pipeline
- Bądź konkretny: "strona X, fraza Y, akcja Z" — nie ogólniki
- Max 15 minut — to jest weekly review, nie deep dive
- Deep dive → `/seo-stats`
- Nowy post → `/seo-plan-post`
- Audyt techniczny → `/seo audit https://dokodu.it`
