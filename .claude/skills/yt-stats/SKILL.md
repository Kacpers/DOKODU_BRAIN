---
name: yt-stats
description: Analizuje dane z YouTube i wyciąga actionable insights. Porównuje filmy, identyfikuje co działa, co nie, i daje konkretne rekomendacje. Zapisuje wnioski do YT_Insights.md. Trigger: "zanalizuj youtube", "insighty z yt", "co działa na kanale", "stats youtube", /yt-stats
---

# Instrukcja: YouTube Stats & Insights

## Działanie

Głęboka analiza danych kanału. Działa jak doświadczony YouTube Strategist.

## KROK 1: Pobierz dane

Najpierw spróbuj z lokalnej bazy (szybko, bez API):
```bash
cd /home/kacper/DOKODU_BRAIN/scripts && python3 youtube_fetch.py --from-db
```

Jeśli dane są starsze niż 24h (sprawdź "Ostatni sync" w nagłówku) — odśwież z API:
```bash
python3 youtube_fetch.py --days 28 --max-videos 30 --save
```

Odczytaj też: `/home/kacper/DOKODU_BRAIN/20_AREAS/AREA_YouTube/YT_Last_Sync.md`

Odczytaj też: `/home/kacper/DOKODU_BRAIN/30_RESOURCES/RES_YouTube/YT_Insights.md` (poprzednie analizy)

## KROK 2: Analiza ilościowa

Na podstawie danych oblicz i zidentyfikuj:

**TOP filmy:**
- Top 3 wg wyświetleń w okresie
- Top 3 wg CTR
- Top 3 wg Avg View Duration (retencja)

**BOTTOM filmy:**
- Bottom 3 wg wyświetleń
- Filmy z CTR < 3% (potencjalne problemy z thumbnailem/tytułem)
- Filmy z retencją < 30% (problem z treścią lub strukturą)

**Benchmarki YouTube (dla kanałów edukacyjnych):**
- CTR: <2% słaby | 2-5% OK | 5-8% dobry | >8% świetny
- Avg retention: <30% słaba | 30-50% OK | 50%+ dobra
- Subskrybenci net w miesiąc: trend wzrostowy czy spadkowy?

## KROK 3: Analiza jakościowa

Porównaj top vs bottom filmy pod kątem:
1. **Tytuł** — długość, styl, liczby vs pytania vs "jak zrobić"
2. **Temat** — tutoriale vs case studies vs opinie vs edukacja
3. **Długość** — krótkie (<10 min) vs długie (>20 min)
4. **Thumbnail** — na podstawie tytułów wnioskuj co mogło działać

Sprawdź poprzednie analizy z YT_Insights.md — czy wzorce się powtarzają?

## KROK 4: Wygeneruj raport

Format:

```
### Analiza YouTube — [DATA]
**Okres:** [start] → [end]

**KANAŁ W SKRÓCIE:**
- Subskrybenci: X (net w okresie: +/-X)
- CTR kanału: X% → [ocena: słaby/OK/dobry/świetny]
- Avg View Duration: X:XX → [ocena]

**TOP 3 FILMY:**
1. "[tytuł]" — X wyśw. | CTR X% | Retention X:XX
2.
3.

**CO DZIAŁA:**
1. [Konkretny wzorzec z dowodami z danych]
2.
3.

**CO NIE DZIAŁA / RYZYKA:**
1. [Konkretny problem z dowodami]
2.

**3 REKOMENDACJE (konkretne, do wdrożenia w tym tygodniu):**
- [ ] [Rekomendacja 1 — co dokładnie zrobić]
- [ ] [Rekomendacja 2]
- [ ] [Rekomendacja 3]

**PYTANIE DO PRZEMYŚLENIA:**
[Jedno trudne pytanie które wyłoniło się z danych — np. "Dlaczego Twój najlepszy film z 3 miesiące temu ma 10x więcej wyświetleń niż ostatnie 5 razem? Co się zmieniło?"]
```

## KROK 5: Zapisz do YT_Insights.md

Dopisz wpis na początku sekcji "Archiwum Analiz" w:
`/home/kacper/DOKODU_BRAIN/30_RESOURCES/RES_YouTube/YT_Insights.md`

Zaktualizuj też sekcje "Wzorce Tytułów", "Wzorce Thumbnails" jeśli wyłoniły się nowe wzorce.

## ZASADY

- Bądź konkretny: zamiast "popraw thumbnails" → "thumbnail w filmie X ma za mały kontrast, spróbuj żółtego tła jak w filmie Y który miał CTR 8%"
- Bazuj TYLKO na danych — nie zgaduj
- Porównuj z poprzednimi analizami z YT_Insights.md — szukaj powtarzających się wzorców
- Jedno trudne pytanie na końcu — nie unikaj nieprzyjemnych wniosków
