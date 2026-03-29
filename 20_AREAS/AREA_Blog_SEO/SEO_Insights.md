---
type: insights
status: active
generated_by: seo-stats skill
last_updated: 2026-03-29
---

# SEO Insights — dokodu.it

> Kumulatywna baza insightów z analiz Google Search Console.
> Uzupełniany przez `/seo-stats` po każdej synchronizacji.

---

## Insights — 2026-03-29

**Okres danych:** 2026-02-26 → 2026-03-26 (28 dni)
**Kliknięcia:** 1 384 | **Impressions:** 50 178 | **Avg CTR:** 12.51% | **Avg pozycja:** #5.6

---

### Quick Wins (pozycje 4-15, duże impressions)

| Fraza | Impressions | Poz. | CTR | Akcja |
|-------|-------------|------|-----|-------|
| `pytest` | 919 | #4.5 | 2.5% | Przebuduj H1 + dodaj "szybki start" — bounce 88.4% w GA, 23s avg! |
| `cursor pro` | 545 | #4.1 | 2.4% | Mocna konkurencja, bounce 88% — unikalne kąt (PL-specyfika) lub odpuścić |
| `python co to` | 448 | #4.3 | 2.0% | Popraw meta description pod intencję informacyjną |
| `automatyzacje dla firm` | 132 | #11.0 | 1.5% | **Commercial intent + ICP Dokodu** — brak dedykowanej strony! |
| `agenci ai` | 120 | #13.9 | 1.7% | Rosnący temat, pozycja 14 → dedykowany pillar page |

### Niski CTR przy dobrej pozycji — pilne

| Fraza | Impressions | Poz. | CTR | Problem |
|-------|-------------|------|-----|---------|
| `n8n` | 19 655 | #3.0 | **2.2%** | Meta title `/blog/n8n` — największa strata kliknięć w całym serwisie |
| `python list comprehension` | 3 623 | **#2.1** | **0.2%** | Poz. 2 i tylko 9 kliknięć — featured snippet zjada ruch, lub tytuł odpycha |
| `sql` | 2 148 | #3.2 | 0.4% | Fraza broad, trudna do poprawy CTR |
| `llm co to` | 679 | **#1.9** | **0.1%** | Poz. 2, 1 kliknięcie — featured snippet monopolizuje SERP |
| `sql co to` | 988 | #3.2 | 1.5% | Popraw meta description |

**🔴 Krytyczne:** `n8n` na poz. 3 z CTR 2.2% to ~17k impressions miesięcznie. Poprawa CTR z 2.2% → 5% dałaby +560 kliknięć/miesiąc. To priorytet #1.

### Content Gaps (impressions, zero kliknięć)

| Strona | Impressions | Poz. | Ocena |
|--------|-------------|------|-------|
| `/blog/prompt-engineering/co-to-jest-prompt` | 531 | #8.6 | Przebudowa tytułu, za słaba pozycja |
| `/blog/python/nauka/czy-python-jest-trudny` | 453 | #3.6 | Poz. 3.6 i 0 kliknięć — tytuł nie odpowiada intencji |
| `/blog/python/praktyka/refaktoryzacja-kodu-w-pythonie` | 411 | #9.7 | Zbyt niska pozycja, thin content? |
| `/blog/wdrozenie-ai-w-firmie/chatboty-ai-obsluga-klienta` | 185 | #23.8 | ICP-zgodna strona ale za nisko — wzmocnić linkowaniem |

### Top Performers — co rozbudować

| Strona | Kliknięcia | CTR | Potencjał |
|--------|-----------|-----|-----------|
| `/blog/n8n` | 634 | 2.4% | Hub n8n — dodaj CTA do kursu, sekcję "od czego zacząć" |
| `/blog/sql/zadania-sql-poziom-podstawowy` | 119 | **9.6%** | Świetny CTR — dodaj linki do kursu SQL, CTA |
| `/blog/sql/sql-interview-pytania` | 110 | **10.2%** | Świetny CTR — to lead magnet dla juniorów |
| `/blog/sql/normalizacja-baz-danych` | 91 | 2.3% | 4k impressions — popraw CTR meta |
| `/blog/n8n/przyklady-workflow-automatyzacji` | 62 | 2.4% | Engaged users (2m43s w GA) — warto rozbudować |

### Nowe tematy do napisania (content gaps z intencją)

1. **"automatyzacje dla firm"** / "automatyzacja AI w firmie" — 132 impressions poz. #11, commercial intent, bezpośredni ICP Dokodu. Brak dedykowanego posta.
2. **"agenci ai"** — 120 impressions poz. #13.9, rosnący trend. Obecny post `/blog/agenci-ai/claude-code-agent` jest zbyt wąski — potrzebny pillar page.
3. **"automatyzacja ai"** — 208 impressions poz. #11.2, bliska frazie wyżej — można skierować na ten sam post.

---

### Quick Actions (top 5 priorytetów)

1. **Popraw meta title `/blog/n8n`** — z obecnego na coś jak "n8n — co to jest, jak działa i od czego zacząć [PL]". Potencjał: +300-500 kliknięć/miesiąc.
2. **Napraw `/blog/python/podstawy/list-comprehension`** — poz. #2.1 z CTR 0.2% to skandal. Dodaj cheatsheet na górze, zmień title pod featured snippet. Połącz z GA: bounce 94.5%, 14s.
3. **Nowy post: "Automatyzacja AI w firmie — od czego zacząć"** — commercial intent, ICP, poz. 11 dla "automatyzacje dla firm".
4. **Przebuduj `/blog/python/testowanie/testowanie-z-pytest`** — `pytest` (919 impressions, poz. #4.5) ale bounce 88.4% i 23s w GA — treść nie dostarcza wartości.
5. **Pillar page: Agenci AI** — "agenci ai" poz. #13.9, 120 impressions — rosnący temat, Dokodu ma tu przewagę ekspercką.

---

### Komendy do Ideas Bank (skopiuj i uruchom)

```bash
python3 /home/kacper/DOKODU_BRAIN/scripts/seo_ideas.py add "Automatyzacja AI w firmie — przewodnik wdrożenia" \
  --keyword "automatyzacje dla firm" --pillar "automatyzacja" --priority high --source gsc-sync

python3 /home/kacper/DOKODU_BRAIN/scripts/seo_ideas.py add "Agenci AI — co to jest i jak wdrożyć w firmie" \
  --keyword "agenci ai" --pillar "ai" --priority high --source gsc-sync

python3 /home/kacper/DOKODU_BRAIN/scripts/seo_ideas.py add "Pytest — kompletny przewodnik dla programistów Python" \
  --keyword "pytest" --pillar "python" --priority medium --source gsc-sync
```

---

*DOKODU BRAIN SEO Insights | 2026-03-29*
