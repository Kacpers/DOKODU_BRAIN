---
type: monitoring
status: active
owner: kacper
created: 2026-04-25
last_reviewed: 2026-04-25
description: Plan SEO Action Triggers — logika "if pozycja/metryka X to akcja Y", monitorowana automatycznie przez /daily-briefing i /seo-stats.
---

# SEO Action Triggers — automatyczny plan reagowania

Plik definiuje **trigger logic** — co Claude ma zrobić automatycznie gdy GSC/DataForSEO pokazuje określone zmiany. Sprawdzany każdego dnia w `/daily-briefing` (sekcja SEO Triggers) oraz w piątkowym `/seo-weekly`.

---

## Jak Claude monitoruje (cadence)

| Co | Częstotliwość | Źródło danych |
|----|---------------|---------------|
| Pozycje fraz w GSC | dziennie (z `/daily-briefing`) | Google Search Console API |
| DataForSEO weekly diff | piątek 8:00 (cron launchd) | DataForSEO API |
| Trigger evaluation | dziennie + piątek | Ten plik |
| Akcja gdy trigger pasuje | natychmiast (proponuje user'owi) | — |

Claude porównuje aktualne metryki z tabelą poniżej. Gdy któryś trigger pasuje → automatycznie sugeruje akcję w briefingu rannym.

---

## TRIGGERS — Klaster Claude Code (33 100 vol/mc)

### 🟢 IF `claude code` wejdzie do top 20 (pozycja 11-20)
**THEN:**
- Działanie: Boost contentu pillara — dodać sekcję "Częste pytania programistów" (long-tail), 2-3 case studies wdrożeń, screenshot UI, transkrypt wideo (jeśli będziesz miał)
- Cel: push do top 10
- Priorytet: WYSOKI (33 100 vol/mc = warto)
- Termin: 1 tydzień od trigger
- Powiadomienie: w daily briefing rano

### 🟢 IF `claude code` w top 10
**THEN:**
- Działanie: Podpinaj pillar w każdym nowym artykule jako wewnętrzny link
- Dodaj do `/blog/n8n` cross-link do Claude Code w sekcji "Co dalej"
- Cel: utrzymanie + push do top 5

### 🟢 IF `claude code` w top 3
**THEN:**
- Działanie: Push agresywnie satelity które jeszcze nie rankują (skills, cli, mcp jeśli któryś poniżej top 30)
- Każdy satelita rozszerz o long-tail sekcje
- Cel: dominacja klastra, top 1

### 🔴 IF `claude code` poza top 50 po 8 tyg
**THEN:**
- Działanie: Audyt — sprawdź indexing w GSC, sprawdź konkurencję (kto rankuje?), porównaj content depth, dodaj 1500+ słów do pillara
- Może też: zmień meta title (CTR test)
- Powiadomienie: alert pilny w briefingu

---

## TRIGGERS — Klaster Agent AI (13 200 vol/mc)

### 🟢 IF `agent ai` lub `ai agent` wejdzie do top 20
**THEN:**
- Działanie: Push case studies — dodać 2-3 nowe (Animex już jest, dorzucić: logistyka/produkcja/usługi)
- Cross-link satelitów do siebie (dziś tylko z pillara)
- Cel: top 10

### 🟢 IF któryś z `agent ai co to`/`agent ai jak stworzyć`/`n8n ai agent` w top 10
**THEN:**
- Działanie: Refresh pillara `/blog/agent-ai-dla-firm` — dodać sekcję "FAQ od czytelników" z nowych pytań w GSC (search terms which trigger this satellite)
- Cel: pillar jako Hub agregujący ruch satelit

### 🔴 IF `ai automation offer` lead-gen CTA klikalność <2%
**THEN:**
- Działanie: A/B test wariantów (zmienić wording, dodać liczby z case study)
- Sprawdź czy CTA pasuje semantycznie do contentu
- Powiadomienie: po 2 tyg od publikacji jeśli <2% CTR

---

## TRIGGERS — Klaster n8n (refreshe)

### 🟢 IF `/blog/n8n` (#3 → ?) awansuje na #1-2
**THEN:**
- Działanie: NAPISZ Hub article "Najlepsze narzędzia automatyzacji 2026" (n8n, Make, Zapier, Activepieces, OpenClaw)
- Cel: złapać też frazy "narzędzia automatyzacji" (HUB pillar)
- Termin: 2 tyg
- Komenda: `/seo-plan-post najlepsze narzędzia automatyzacji 2026` → `/blog-draft`

### 🟢 IF `n8n self-hosted` w top 10
**THEN:**
- Działanie: Nagraj film YT z lokowaniem Hostinger 2 500 PLN — synergiczne wzmocnienie
- Plus: dodaj n8n self-hosted jako satelita do `/blog/n8n` pillara z cross-linkiem
- Cel: utrzymać top 10 + dodać video traffic

### 🔴 IF `n8n` (#3) spadnie poniżej #5
**THEN:**
- Działanie: Pilny audit — sprawdź czy konkurencja wypuściła coś nowego, refresh contentu pillara, sprawdź backlinki, porównaj user signals (CTR, dwell time)
- Powiadomienie: alert pilny

---

## TRIGGERS — Quick wins (Phase 2 refreshe)

### 🟢 IF `tkinter` (#7 → ?) awansuje do top 5
**THEN:**
- Działanie: Eksperymentuj z meta description (CTR optimization)
- Dodaj cross-linki z `/blog/python` pillara
- Cel: top 3

### 🟢 IF `pytest` (#5 → ?) awansuje do top 3
**THEN:**
- Działanie: Napisz satelitę "Pytest fixtures" lub "Pytest parametrize" (long-tail)
- Cel: zbuduj klaster Python testing

### 🔴 IF któryś refresh (Phase 2) NIE awansuje po 8 tyg
**THEN:**
- Działanie: Sprawdź konkretny artykuł — może Google nie zindeksował zmian, sprawdź GSC "URL inspection", request reindexing
- Lub: większy refresh (więcej słów, lepsze H2)

---

## TRIGGERS — Lead gen i monetyzacja

### 🟢 IF KACPER10 reflink generuje pierwszą prowizję
**THEN:**
- Działanie: Audit — który artykuł skonwertował? Boost tego artykułu (więcej featured image, prominentna lokalizacja boxa afiliacyjnego)
- Wzmocnij box afiliacyjny w pozostałych n8n-related artykułach

### 🟢 IF `/kontakt` form submission z UTM `blog`
**THEN:**
- Działanie: Identyfikuj który artykuł wygenerował lead (UTM source/medium/campaign)
- Dorzucaj CTA bardziej prominent w tym artykule
- Plus dodaj do `Outreach_Tracker.md` jako Inbound

### 🔴 IF kurs n8n waitlist signup <5/mies. po 2 tyg od launch
**THEN:**
- Działanie: Refresh AD `kurs-n8n-waitlist` — A/B headline, dodać liczby ROI, więcej social proof
- Albo: Premium plan kursu — niższa cena early bird

---

## TRIGGERS — Cluster Python/SQL (legacy autorytetu)

### 🟢 IF któreś istniejące Python/SQL artykuły mają #2-3 i CTR <3%
**THEN:**
- Działanie: Refresh meta title — sprawdź konkurencję (top 3 rezultaty), zaadaptuj wzorzec
- A/B title test (możesz zmienić raz na 4 tyg)
- Cel: CTR >5%

### 🟢 IF Python keyword zaczyna RISING (>200% w GSC w 4 tyg)
**THEN:**
- Działanie: Refresh artykułu (jeśli istnieje) lub napisz nowy (jeśli nie)
- Cel: złapać momentum trendu

---

## TRIGGERS — DataForSEO weekly diff

### 🟢 Każdy piątek 8:00 (cron) — DataForSEO weekly run
**Akcje automatyczne:**
1. Skanuj raport `2026-W{nr}.md`
2. Compare z poprzednim tygodniem (`2026-W{nr-1}.md`)
3. Powiadom o:
   - Nowe pozycje w top 30 → +1 punkt do "rosnące tematy"
   - Spadki >5 pozycji → alert pilny
   - Nowe gapy w branchy (tematy które się pojawiły) → kandydaci do nowych artykułów

### 🟢 IF nowy gap z DataForSEO ma >500 vol/mc + LOW comp + commercial intent
**THEN:**
- Działanie: Auto-zapis do SEO_Ideas_Bank z priority HIGH
- Sugestia w niedzielnym brainstorm: "Czy warto napisać?"

---

## Format alertu w `/daily-briefing`

Każdy aktywny trigger pokazuje się rano:

```
🚨 SEO TRIGGER — Klaster Claude Code

Fraza: claude code
Pozycja wczoraj: 25 → dziś: 18
Trigger: "IF claude code wejdzie do top 20"
Akcja: Boost pillara (FAQ, case studies, screenshoty)
Termin: 1 tydzień
Komenda: /seo-research claude code → wzmocnić zgodnie z briefem
```

Plus tygodniowy summary w `/seo-weekly`:

```
📊 SEO WEEKLY (2026-W{nr})

Triggers aktywowane: 3
- ✅ claude code → top 20 (action: boost pillar)
- ✅ agent ai → top 30 (action: case studies)
- ⚠️ tkinter → spadek z #7 do #11 (action: pilny audit)

Triggers nieaktywne: 12 (oczekują na metric)
```

---

## Co Kacper musi robić

**Nic ręcznie** dla tego pliku. Claude monitoruje automatycznie przez:
- Codzienny `/daily-briefing` rano (ładuje ten plik + GSC current data)
- Piątek `/seo-weekly` (ładuje + DataForSEO weekly raport)

Gdy trigger się aktywuje → Claude proponuje konkretną akcję w briefingu. Kacper akceptuje (lub odrzuca) — Claude wykonuje.

---

## Aktualizacja pliku

Po publikacji nowych artykułów / refresh-ów Claude **dodaje nowe triggers** do tego pliku. Po wygaśnięciu (np. cel osiągnięty: "claude code w top 3") Claude **dezaktywuje** trigger.

Format dezaktywacji: zachować w pliku ale przekreślić + dodać `[OSIĄGNIĘTE: data]`.

Przykład:

```markdown
### ~~🟢 IF `claude code` wejdzie do top 20~~ [OSIĄGNIĘTE: 2026-06-12]
- Akcja wykonana: boost pillara → 1 200 słów dorzucone
- Wynik: pozycja 18 → 11 w 8 dni
```

---

## Backup logiki — ręczne odpalanie

Gdy chcesz sprawdzić triggers manualnie (poza daily/weekly):

```bash
# Pobierz GSC data + sprawdź triggers
cd ~/Projects/dokodu/brain-public
python3 _apps/scripts/gsc_fetch.py --days 7 --save
# Otwórz SEO_Action_Triggers.md i porównaj z aktualnymi pozycjami
```

Albo w `/daily-briefing` — sekcja "🚨 SEO TRIGGERS" już zawiera świeży check.

---

*Ostatnia aktualizacja: 2026-04-25 — pierwsza wersja po publikacji 13 nowych draftów + 6 refresh-ów Phase 2*

---

## Update 2026-04-26 (sesja Phase 3 — internal linking + cluster authority)

**Co zrobione:**
- ✅ Refactor `/blog/n8n/licencja-cennik` (12. post) — title commercial-intent, +nowa sekcja "Ile kosztuje wdrożenie n8n u agencji" (widełki PL + matryca decyzji mermaid + ROI math), +mermaid 3 warstwy kosztów
- ✅ n8n pillar (33 100 vol/mc, #3) +6 internal links do nowych: claude-code, claude-code/mcp, claude-code/skills, agent-ai-dla-firm, agent-ai-jak-stworzyc, windsurf-vs-cursor
- ✅ claude-code pillar 3→9 internal links: 5 satelitów (/instalacja, /cennik, /cli, /mcp, /skills) + reciprocal /blog/n8n
- ✅ agent-ai-dla-firm: 3 broken linki naprawione (FAQ + content): `/blog/agenty-ai*` → `/blog/agent-ai-co-to`, `/blog/n8n/agent-ai-n8n` → `/blog/n8n/n8n-ai-agent`, `/blog/agenty-ai/wdrozenie-agenta-ai` → `/blog/agent-ai-jak-stworzyc`
- ✅ n8n/n8n-ai-agent satellite naprawiony — dodany pillar back-link do `/blog/n8n`
- ✅ Audit 2026-04-22 verified — wszystkie C1, C2, H2, H3, H4, H5 już zaimplementowane (audyt przeterminowany). H1 zostaje — Cloudflare Managed Transforms duplikują security headers (Kacper user-side fix)
- ✅ Cluster cross-linking 9/9 satelitów linkuje wstecz do pillarów (cluster authority complete)
- ✅ Brief n8n/templates (590 vol/mc, LOW comp) — gotowy do `/blog-draft` w `30_RESOURCES/RES_Blog_Drafts/drafts/BRIEF_n8n-templates_2026-04-26.md`

**Nowe triggery do monitorowania (od 2026-04-26):**

### 🟢 IF licencja-cennik CTR > 4% w 4 tyg (baseline 1.3%)
**THEN:** Refactor sukces potwierdzony → zaplanuj kolejny refactor wg metody (commercial intent rewrite, mermaid, nowa sekcja agencja-pricing) na innym low-CTR pillar
- Termin sprawdzenia: 2026-05-24

### 🔴 IF licencja-cennik CTR < 2% w 4 tyg
**THEN:** Refactor nie zadziałał → A/B test meta description (3 warianty), sprawdź czy SERP feature (np. featured snippet) zabiera klików
- Termin: 2026-05-24

### 🟢 IF któryś z 11 nowych URL ma > 5 impressions/tydz w 2 tyg
**THEN:** Indeksowanie OK → sprawdź pozycję, zaplanuj boost long-tail jeśli w top 30
- Termin: 2026-05-10

### 🔴 IF wszystkie 11 nowych URL bez impresji w 4 tyg
**THEN:** Problem indeksowania → ręczne Submit URL w GSC, sprawdź sitemap, sprawdź robots.txt
- Termin: 2026-05-24

### 🟢 IF n8n/templates draft NIE napisany do piątek 01.05
**THEN:** `/blog-draft BRIEF_n8n-templates_2026-04-26.md` — jeden gap nadal otwarty z W17 weekly
- Termin: 2026-05-01

### 🟢 IF cron DataForSEO weekly piątek 01.05 wykryje nowy gap > 500 vol
**THEN:** `/seo-plan-post [keyword]` → brief w drafts/
- Termin: 2026-05-01

---

*Update 2026-04-26 — Phase 3 (cluster authority + audit cleanup) zakończona. 12 postów na blogu + 3 podlinkowane pillary + 9/9 satelitów linkuje wstecz. Pipeline gotowy na ocenę GSC za 2-4 tyg.*
