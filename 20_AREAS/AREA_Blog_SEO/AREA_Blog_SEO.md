---
type: area
status: active
owner: kacper
last_reviewed: 2026-03-13
tags: [seo, blog, content, marketing, copilot, n8n]
---

# AREA: Blog SEO — dokodu.it/blog/

## Misja

Zwiększenie organicznego ruchu na dokodu.it przez systematyczne tworzenie contentu SEO dla firm rozważających wdrożenie AI (M365 Copilot, n8n, automatyzacja procesów).

**Cel 2026:** 5,000 sesji organicznych / miesiąc | Average position ≤ 15 | 50+ artykułów

---

## Pillary Tematyczne

| Pillar | Target Keyword | Search Intent | Priorytet |
|--------|---------------|---------------|-----------|
| **M365 Copilot** | "microsoft 365 copilot wdrożenie" | commercial / informational | 🔴 HIGH |
| **n8n Automatyzacja** | "n8n automatyzacja procesów" | informational | 🔴 HIGH |
| **AI w firmie** | "wdrożenie AI w firmie" | commercial | 🟡 MED |
| **GitHub Copilot** | "github copilot dla firm" | commercial | 🟡 MED |
| **AI Act / Compliance** | "ai act compliance polska" | informational | 🟢 LOW |
| **Docker / Dev Tools** | "docker kurs po polsku" | informational | 🟢 LOW |

---

## Content Strategy

### Architektura Pillar + Satellite

```
Pillar Page (np. /microsoft-365-copilot)
├── Satellite: "Jak zacząć z M365 Copilot" — top of funnel
├── Satellite: "M365 Copilot vs GitHub Copilot — porównanie"
├── Satellite: "Koszty wdrożenia M365 Copilot w Polsce"
├── Satellite: "M365 Copilot dla działów sprzedaży"
└── Satellite: "M365 Copilot case study — firma produkcyjna"
```

### Typy Contentu

1. **Poradniki How-to** — "Jak wdrożyć X krok po kroku" (informational)
2. **Porównania** — "X vs Y — co wybrać dla firmy" (commercial)
3. **Case studies** — "Jak firma X zaoszczędziła Y dzięki AI" (commercial)
4. **Słownik / Wyjaśnienia** — "Co to jest X" (informational, top funnel)
5. **Checklists** — "Checklist wdrożenia X" (informational, lead magnet)

---

## KPIs

| Metryka | Aktualna | Cel Q2 2026 | Cel EOY 2026 |
|---------|----------|-------------|--------------|
| Kliknięcia / mies. | — | 500 | 2,000 |
| Impressions / mies. | — | 15,000 | 50,000 |
| Średnia pozycja | — | ≤ 20 | ≤ 12 |
| CTR | — | ≥ 3% | ≥ 4% |
| Artykułów opublikowanych | — | 15 | 50 |

*Uzupełnij po pierwszym /seo-sync*

---

## Proces Produkcji

```
/seo-sync → /seo-stats → /seo-research [temat] → /seo-plan-post → Pisanie → Review → Publikacja
```

| Etap | Narzędzie | Output |
|------|-----------|--------|
| Dane GSC | `/seo-sync` | SEO_Last_Sync.md |
| Analiza okazji | `/seo-stats` | SEO_Insights.md |
| Research tematu | `/seo-research` | Brief z kątem i słowami kluczowymi |
| Brief posta | `/seo-plan-post` | Gotowy brief: slug, H2, meta, CTA |
| Audyt strony | `/seo audit dokodu.it` | Techniczny health check |
| Przegląd tygodniowy | `/seo-weekly` | Priorytety na następny tydzień |

---

## Szybkie Komendy

```bash
# Sync danych z GSC
python3 /home/kacper/DOKODU_BRAIN/scripts/gsc_fetch.py --save

# Lista pomysłów
python3 /home/kacper/DOKODU_BRAIN/scripts/seo_ideas.py list

# Eksport ideas bank
python3 /home/kacper/DOKODU_BRAIN/scripts/seo_ideas.py export --save

# Audyt techniczny strony
# Użyj: /seo audit https://dokodu.it
```

---

## Topic Cluster Map (Pillar + Cluster Architecture)

> Adaptacja `content-strategy` (coreyhaines31/marketingskills). Każdy pillar = hub page + cluster artykułów linkowanych wewnętrznie.

### Pillar 1: M365 Copilot (HIGH priority)

```
HUB: /microsoft-365-copilot — pillar page (3000+ słów, comprehensive guide)
├── AWARENESS
│   ├── "Co to jest Microsoft 365 Copilot — wprowadzenie"
│   ├── "Jak działa Copilot w Excel/Word/Outlook"
│   └── "Microsoft 365 Copilot — pierwsze 30 dni dla nietechnicznych"
├── CONSIDERATION
│   ├── "M365 Copilot vs GitHub Copilot — porównanie"
│   ├── "M365 Copilot vs ChatGPT Enterprise"
│   └── "Najlepsze alternatywy dla Microsoft Copilot"
├── DECISION
│   ├── "Koszty wdrożenia M365 Copilot w Polsce 2026"
│   ├── "M365 Copilot E3/E5 vs standalone — który plan"
│   └── "Demo Microsoft 365 Copilot — co realnie zobaczysz"
└── IMPLEMENTATION
    ├── "Checklist wdrożenia M365 Copilot krok po kroku"
    ├── "Top 10 promptów Copilota dla działu sprzedaży"
    └── "Case study: jak [Klient] wdrożył Copilota w 6 tygodni"
```

### Pillar 2: n8n Automatyzacja (HIGH priority)

```
HUB: /n8n-automatyzacja — pillar page
├── AWARENESS
│   ├── "Co to jest n8n — wprowadzenie dla biznesu"
│   ├── "Co możesz zautomatyzować w n8n — 10 pomysłów"
│   └── "n8n po polsku — start"
├── CONSIDERATION
│   ├── "n8n vs Zapier vs Make — porównanie"
│   ├── "n8n self-hosted vs cloud — co wybrać"
│   └── "Alternatywy dla Zapiera dla firm 50-500 prac."
├── DECISION
│   ├── "Cennik n8n cloud vs self-hosted (2026)"
│   ├── "n8n na Hostinger VPS — instrukcja [+ KACPER10 affiliate]"
│   └── "Ile kosztuje wdrożenie n8n w firmie 100-osobowej"
└── IMPLEMENTATION
    ├── "8 wzorców workflow n8n które Ci się przydadzą"
    ├── "Jak debugować n8n — przewodnik"
    └── "Case study: Animex i 40h tygodniowo dzięki n8n"
```

### Pillar 3-6: AI w firmie / GitHub Copilot / AI Act / Docker

(Strukturę powiel wzorzec wyżej. Status dziś: AWARENESS poziom dla większości — uzupełniaj systematycznie.)

### Generowanie clustera dla nowego pillara

Komenda: `/seo-research [temat] -- buyer-stages awareness,consideration,decision,implementation`

Output: brief z 12-20 sub-tematami pomapowanymi na buyer stages.

---

## Keyword Research by Buyer Stage

> Mapuj tematy do buyer journey przez sprawdzone modyfikatory keyword. Bez tego post może rankować, ale NIE poruszać klienta po lejku.

### Awareness (TOFU — top of funnel)

**Modyfikatory PL:** "co to jest", "jak działa", "wprowadzenie do", "przewodnik po", "podstawy"

**Cel:** edukować nowych użytkowników, którzy jeszcze nie wiedzą że potrzebują rozwiązania.

**Przykłady dla Dokodu:**
- "co to jest microsoft 365 copilot"
- "jak działa n8n"
- "podstawy AI w firmie"

**Zasada:** brak pitch, brak CTA do oferty. Linkuj do 2-3 powiązanych postów (consideration stage).

---

### Consideration (MOFU — middle of funnel)

**Modyfikatory PL:** "najlepszy", "porównanie", "vs", "alternatywy", "który wybrać"

**Cel:** czytelnik wie że problem istnieje, porównuje opcje.

**Przykłady:**
- "najlepsze narzędzia automatyzacji 2026"
- "n8n vs zapier vs make"
- "alternatywy dla microsoft copilot"

**Zasada:** uczciwa porównawczość — pokaż gdzie konkurencja jest lepsza. Buduje wiarygodność.

---

### Decision (BOFU — bottom of funnel)

**Modyfikatory PL:** "cennik", "koszt", "recenzja", "demo", "ile kosztuje"

**Cel:** czytelnik gotowy do zakupu, szuka argumentów do uzasadnienia decyzji.

**Przykłady:**
- "cennik n8n self-hosted vs cloud"
- "koszt wdrożenia AI w firmie 100 osobowej"
- "demo m365 copilot — co zobaczysz"

**Zasada:** TUTAJ CTA do oferty Dokodu. Mid-CTA + end-CTA.

---

### Implementation (Post-purchase / AHA stage)

**Modyfikatory PL:** "tutorial", "krok po kroku", "checklist", "szablony", "jak ustawić"

**Cel:** klient (lub prawie-klient) który już wie co kupić — uczy się jak to wdrożyć.

**Przykłady:**
- "checklist wdrożenia copilota"
- "n8n krok po kroku dla początkujących"
- "10 promptów copilota dla sprzedaży"

**Zasada:** to jest "champion content" — czytelnik wewnątrz firmy przekonuje resztę. Linkuj do `/oferta` jako "potrzebujesz pomocy z wdrożeniem".

---

## Prioritizing Content Ideas (Scoring 0-10)

Każdy nowy pomysł oceń przed dodaniem do `seo_ideas.py`:

| Czynnik | Waga | Pytanie |
|---|---|---|
| **Customer Impact** | 40% | Jak często ten temat pojawia się w discovery? Ilu klientów ma ten problem? |
| **Content-Market Fit** | 30% | Czy to mapuje na ofertę Dokodu? Mamy unique insight? Mamy case study? |
| **Search Potential** | 20% | Jakie volume w GSC/DataForSEO? Konkurencja? Trend? |
| **Resources** | 10% | Mamy ekspertyzę? Ile czasu zajmie research/pisanie? |

### Scoring Template

| Idea | Customer Impact (40%) | Market Fit (30%) | Search (20%) | Resources (10%) | Total |
|---|---|---|---|---|---|
| "M365 Copilot cennik 2026" | 9 | 9 | 8 | 7 | 8.5 |
| "AI Act dla firm 50-500" | 6 | 7 | 5 | 6 | 6.2 |
| "Docker dla devops juniora" | 4 | 3 | 9 | 8 | 5.0 |

**Reguła decyzyjna:**
- Total ≥ 8.0 → `priority: P1` w SEO_Ideas_Bank
- 6.5-7.9 → `priority: P2` (write w drugiej kolejności)
- < 6.5 → `parking lot` (revisit w Q+1, może okoliczności się zmienią)

### Implementation w seo_ideas.py

Dodaj do schematu pomysłu pola: `customer_impact`, `market_fit`, `search_score`, `resources_score`, `total_score` (auto-calc).

Komenda: `python3 scripts/seo_ideas.py add --topic "..." --ci 9 --mf 8 --sp 7 --r 6`
Output: total_score = 7.9 → P2

---

## Notatka o źródle

Sekcje **Topic Cluster Map**, **Keyword Research by Buyer Stage**, **Prioritizing Content Ideas** dodane 2026-05-02 z `content-strategy` (coreyhaines31/marketingskills) — przepisane na PL i dostosowane do pillarów Dokodu.

Pełen oryginał (EN, ~370 linii) w: `/tmp/marketingskills/skills/content-strategy/SKILL.md` — wracaj jeśli chcesz głębiej.

---

## Linki

- [SEO_Last_Sync.md](./SEO_Last_Sync.md) — ostatnie dane GSC
- [SEO_Insights.md](./SEO_Insights.md) — kumulatywne insighty
- [SEO_Ideas_Bank.md](./SEO_Ideas_Bank.md) — bank pomysłów
- [GSC_SETUP.md](../../scripts/GSC_SETUP.md) — instrukcja konfiguracji API
