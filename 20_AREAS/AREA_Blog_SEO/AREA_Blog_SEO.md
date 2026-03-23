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

## Linki

- [SEO_Last_Sync.md](./SEO_Last_Sync.md) — ostatnie dane GSC
- [SEO_Insights.md](./SEO_Insights.md) — kumulatywne insighty
- [SEO_Ideas_Bank.md](./SEO_Ideas_Bank.md) — bank pomysłów
- [GSC_SETUP.md](../../scripts/GSC_SETUP.md) — instrukcja konfiguracji API
