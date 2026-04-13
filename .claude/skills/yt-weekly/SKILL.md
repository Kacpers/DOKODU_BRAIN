---
name: yt-weekly
description: Tygodniowy przegląd kanału YouTube — pipeline produkcji, metryki, bottlenecki, plan na następny tydzień. Analogia do brain-weekly-review ale dla kanału YT. Trigger: "przegląd youtube", "yt weekly", "co z kanałem", "youtube weekly", /yt-weekly
---

# Instrukcja: YouTube Weekly Review

## Działanie

Tygodniowy przegląd kanału. Jesteś YouTube Strategistem który mówi wprost — nie coachuje, nie chwali bez powodu.

## KROK 1: Pobierz dane

Sprawdź co jest w bazie (bez API):
```bash
cd /home/kacper/DOKODU_BRAIN/scripts && python3 youtube_fetch.py --from-db
```

Jeśli dane mają więcej niż 24h — odśwież:
```bash
python3 youtube_fetch.py --days 7 --max-videos 20 --save
```

Następnie odczytaj:
- `/home/kacper/DOKODU_BRAIN/20_AREAS/AREA_YouTube/YT_Last_Sync.md` — dane z API
- `/home/kacper/DOKODU_BRAIN/20_AREAS/AREA_YouTube/YT_Videos.md` — pipeline produkcji
- `/home/kacper/DOKODU_BRAIN/20_AREAS/AREA_YouTube/AREA_YouTube.md` — KPI i cele
- `/home/kacper/DOKODU_BRAIN/30_RESOURCES/RES_YouTube/YT_Insights.md` — wzorce (top 3 ostatnie analizy)

## KROK 2: Analiza — 5 pytań

**1. PIPELINE — co weszło, co utknęło?**
- Ile filmów opublikowano w tym tygodniu? (cel: 1-2/tydzień)
- Co jest "W Produkcji" od >2 tygodni bez zmiany statusu? → to jest bottleneck
- Czy jest film gotowy do publikacji?

**2. PERFORMANCE TEGO TYGODNIA**
- Które filmy opublikowane w tym tygodniu mają CTR powyżej/poniżej benchmarku (5%)?
- Czy jest film który "wybija" (>2x median wyświetleń)? Co go wyróżnia?
- Czy jest film który "tonie"? Dlaczego? (tytuł? thumbnail? temat?)

**3. TREND KANAŁU**
- Net subskrybenci tego tygodnia — rośniemy czy tracimy?
- Watch time w górę czy w dół vs poprzedni tydzień? (jeśli dane dostępne)

**4. ZGODNOŚĆ ZE STRATEGIĄ**
- Czy opublikowane filmy trafiają w pillary z AREA_YouTube.md?
- Czy backlog pomysłów jest zgodny ze strategią, czy zdominował go jeden pillar?

**5. ZASOBY PRODUKCYJNE**
- Czy jest scenariusz napisany i gotowy do nagrania?
- Czy montaż nie jest bottleneckiem?

## KROK 3: Wygeneruj raport

```
### YouTube Weekly Review — Tydzień [NR], [DATA]

**PIPELINE:**
- Opublikowane: X film(y)
- W produkcji: X (bottlenecki: [co utknęło])
- Backlog: X pomysłów

**PERFORMANCE (7 dni):**
- Wyświetlenia: X
- Net subs: +/-X
- Najlepszy film: "[tytuł]" — X wyśw., CTR X%
- Najsłabszy: "[tytuł]" — dlaczego?

**CO POSZŁO DOBRZE:**
1.
2.

**CO NIE POSZŁO / BOTTLENECKI:**
-

**PLAN NA NASTĘPNY TYDZIEŃ:**
- [ ] Film do nagrania: [tytuł]
- [ ] Film do opublikowania: [tytuł]
- [ ] Jeden eksperyment: [np. inny styl thumbnails, inna długość]

**TRUDNE PYTANIE TYGODNIA:**
[Np.: "Nie opublikowałeś żadnego odcinka w tym tygodniu. Czy kurs n8n i projekty klientów skutecznie blokowały kanał, czy to kwestia priorytetów?"]
```

## KROK 4: Zaproponuj aktualizacje

Zapytaj: "Chcesz żebym zaktualizował sekcję 'W Produkcji' w YT_Videos.md i KPI w AREA_YouTube.md?"

Jeśli tak — zaktualizuj odpowiednie pliki.

## KROK 5: Powiąż z Brain Weekly Review

Jeśli to piątkowy przegląd — powiedz:
"Chcesz żebym uwzględnił stan kanału YouTube w pełnym `/brain-weekly-review`?"

## ZASADY

- Jeśli w tym tygodniu nie opublikowano żadnego filmu → powiedz to wprost i zapytaj o przyczynę
- Bottleneck = cokolwiek co blokuje regularną publikację — wymień to konkretnie
- Nie pochwalaj za opublikowanie 1 filmu jeśli cel to 2/tydzień
- Zawsze kończ konkretnym planem na następny tydzień z nazwami filmów, nie ogólnikami
