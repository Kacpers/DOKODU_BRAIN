---
name: ga-stats
description: Analizuje dane z Google Analytics 4 i wyciąga actionable insights dla dokodu.it. Identyfikuje strony z wysokim bounce rate, źródła ruchu B2B, konwersje na ścieżkach, kliknięcia reklam. Zapisuje wnioski do GA_Insights.md. Trigger: "zanalizuj analytics", "insighty z ga", "co mówi analytics", "stats ga", /ga-stats
---

# Instrukcja: GA Stats

## Działanie

Czyta `GA_Last_Sync.md` i bazę `ga_data.db`, przeprowadza głęboką analizę i zapisuje wnioski do `GA_Insights.md`.

## KROK 1: Wczytaj dane

Przeczytaj:
- `/home/kacper/DOKODU_BRAIN/20_AREAS/AREA_Blog_SEO/GA_Last_Sync.md` — świeży raport

Jeśli plik nie istnieje — powiedz żeby najpierw odpalić `/ga-sync`.

Pobierz też dane z bazy dla głębszej analizy:

```bash
python3 - <<'EOF'
import sqlite3
from pathlib import Path

conn = sqlite3.connect(Path.home() / ".config/dokodu/ga_data.db")
conn.row_factory = sqlite3.Row

# Strony z wysokim bounce ale dużym ruchem
print("=== HIGH BOUNCE (>70%, >30 sesji) ===")
rows = conn.execute("""
    SELECT page, AVG(bounce_rate) as br, SUM(sessions) as s, AVG(avg_duration) as dur
    FROM ga_pages GROUP BY page
    HAVING br > 70 AND s > 30
    ORDER BY s DESC LIMIT 15
""").fetchall()
for r in rows:
    print(f"  {r['page']:<60} bounce:{r['br']:.0f}%  sesje:{r['s']}  czas:{int(r['dur']//60)}m{int(r['dur']%60)}s")

# Źródła ruchu
print("\n=== ŹRÓDŁA RUCHU ===")
rows = conn.execute("""
    SELECT source, medium, SUM(sessions) as s
    FROM ga_sources GROUP BY source, medium ORDER BY s DESC LIMIT 15
""").fetchall()
for r in rows:
    print(f"  {r['source']}/{r['medium']:<30} {r['s']} sesji")

# Ścieżki B2B
print("\n=== SCIEZKI B2B ===")
rows = conn.execute("""
    SELECT page, SUM(sessions) as s FROM ga_pages
    WHERE page LIKE '/sciezki/%' GROUP BY page ORDER BY s DESC
""").fetchall()
for r in rows: print(f"  {r['page']} — {r['s']} sesji")

# Kliknięcia reklam
print("\n=== AD CLICKS ===")
rows = conn.execute("""
    SELECT page, SUM(count) as c FROM ga_events
    WHERE event_name = 'ad_click' GROUP BY page ORDER BY c DESC LIMIT 10
""").fetchall()
for r in rows: print(f"  {r['page']} — {r['c']} kliknięć")

conn.close()
EOF
```

## KROK 2: Analiza

### Metryki ogólne
- Łączne sesje, użytkownicy, odsłony
- Średni bounce rate vs benchmark (blog ~60-70% to norma)
- Główne źródła ruchu — proporcje organic/direct/referral/social

### Top insights (max 5)
- Które strony tracą użytkowników (wysoki bounce + długi czas → czytają ale nie wchodzą głębiej)
- Które strony angażują (niski bounce + długi czas → to wzór do powielenia)
- Nieoczekiwane źródła ruchu (Teams? ChatGPT? — to B2B signal)

### Ścieżki B2B
- Ile sesji trafia na /sciezki/microsoft, /sciezki/google, /sciezki/openai
- Skąd przychodzą (organic? direct? referral?)
- Trend vs poprzedni okres

### Kliknięcia reklam
- Które posty generują kliknięcia w reklamy sciezki_*
- Które reklamy nie klikają (wysoki ruch, 0 kliknięć → zmień copy lub pozycję)

### Content gaps z GA
- Strony z >100 sesjami i bounce >80% → treść nie spełnia oczekiwań
- Strony z krótkim avg_duration (<30s) → user nie znalazł odpowiedzi

## KROK 3: Zapisz wnioski

Zapisz do `GA_Insights.md`:

```markdown
---
last_updated: [DATA]
period: [OKRES]
total_sessions: [N]
---

# GA Insights — dokodu.it

## Kluczowe metryki
...

## Top 5 Insights
...

## Ścieżki B2B — Status
...

## Strony do naprawy (wysoki bounce)
...

## Strony wzorcowe (niski bounce, długi czas)
...

## Rekomendacje
...
```

## KROK 4: Zaproponuj następny krok

- Jeśli bounce >80% na ważnej stronie → zaproponuj `/seo-plan-post` dla nowej wersji
- Jeśli ścieżki B2B mają ruch ale 0 kliknięć w CTA → zaproponuj A/B test copy reklamy
- Jeśli Teams/ChatGPT jako źródło → zaproponuj post skierowany do B2B firm

## ZASADY

- Bounce rate bloga 60-70% to norma — alarm dopiero przy >80%
- Czas na stronie <30s = użytkownik nie przeczytał = problem z treścią lub title (clickbait)
- Ścieżki B2B to priorytet — nawet 5 sesji miesięcznie to potencjalny lead warty 10k PLN
- Porównuj z `SEO_Insights.md` — GSC + GA razem dają pełny obraz
