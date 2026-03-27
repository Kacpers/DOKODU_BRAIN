---
type: course-material
module: "06 — Autonomous Agents"
topic: B2B Lead Analyst (Multi-Agent)
author: Kacper Sieradzinski / Dokodu
last_reviewed: 2026-03-27
tags: [n8n, multi-agent, supervisor, lead-analysis, b2b, gpt-4o, langchain]
---

# Blueprint: B2B Lead Analyst (Multi-Agent)

## Cel i kontekst

System wielu współpracujących agentów AI, który na podstawie nazwy firmy lub domeny generuje pełny raport kwalifikacji leadu B2B. Supervisor koordynuje pracę trzech wyspecjalizowanych agentów, agreguje wyniki i zwraca gotowy raport do CRM lub Slacka.

**Przykład użycia:** Trafia lead "Logistyczna Polska Sp. z o.o." → system w ~90 sekund generuje raport: czym się zajmują, jak pasują do ICP, jak do nich podejść.

---

## Architektura: Supervisor + 3 Worker Agents

```
                    ┌─────────────────────┐
                    │     TRIGGER         │
                    │  (Webhook / Form /  │
                    │   CRM New Lead)     │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │     SUPERVISOR      │
                    │   (Orchestrator)    │
                    │  Planuje zadania,   │
                    │  zbiera wyniki,     │
                    │  pisze raport       │
                    └──┬──────┬──────┬───┘
                       │      │      │
             ┌─────────▼─┐ ┌──▼────┐ ┌▼──────────────┐
             │  RESEARCH  │ │  ICP  │ │     PITCH     │
             │   AGENT    │ │ANALYST│ │    ADVISOR    │
             │            │ │       │ │               │
             │ Zbiera fakty│ │Ocenia │ │ Rekomenduje  │
             │ o firmie   │ │  fit  │ │  podejście   │
             └─────────┬──┘ └──┬────┘ └──────┬────────┘
                       │       │              │
                    ┌──▼───────▼──────────────▼──┐
                    │         REPORT NODE         │
                    │  Łączy wyniki → Markdown    │
                    │  Zapisuje do CRM / Slack    │
                    └─────────────────────────────┘
```

### Przepływ danych

1. Trigger dostarcza `company_name`, `domain` (opcjonalnie), `contact_name`
2. Supervisor uruchamia równolegle Research Agent + ICP Analyst
3. Research Agent zwraca `company_profile` JSON
4. ICP Analyst dostaje `company_profile` i zwraca `icp_score` + `icp_reasoning`
5. Supervisor uruchamia Pitch Advisor z danymi z kroków 3-4
6. Supervisor agreguje wszystko i generuje raport Markdown
7. Raport trafia do Slacka + CRM (HubSpot / Pipedrive)

---

## Agent 1: Research Agent

### Rola i cel

Zbiera publicznie dostępne fakty o firmie: czym się zajmuje, jak duża jest, gdzie działa, co sprzedaje, jaka jest struktura. Nie ocenia — tylko zbiera fakty.

### System Prompt

```
Jesteś ekspertem od business intelligence B2B. Zbierasz obiektywne fakty o firmach polskich i europejskich.

## Twoja rola
Na podstawie nazwy firmy i/lub domeny zbierz i ustrukturyzuj informacje o firmie. Korzystaj z dostępnych narzędzi (wyszukiwarka, Clearbit, LinkedIn). Nie oceniaj — tylko zbieraj fakty.

## Co zbierasz (w kolejności priorytetu)
1. Podstawowe dane: pełna nazwa, NIP/KRS (jeśli PL), forma prawna, rok założenia
2. Działalność: główna branża (kod PKD), produkty/usługi, rynki docelowe
3. Skala: liczba pracowników (przedział), szacowane przychody, liczba lokalizacji
4. Technologia: stack technologiczny (Wappalyzer, BuiltWith), używane CRM/ERP, obecność w chmurze
5. Aktywność cyfrowa: strona www, LinkedIn followers, ostatnie posty, aktywność rekrutacyjna
6. Wiadomości: ostatnie 3 miesiące — fundraising, ekspansja, zmiany kadrowe, przetargi

## Format odpowiedzi (JSON, bez komentarzy)
{
  "company_name": "pełna oficjalna nazwa",
  "domain": "domena.pl",
  "industry": "nazwa branży",
  "pkd_code": "kod PKD lub null",
  "founded_year": 2010,
  "employees_range": "50-200",
  "revenue_estimate_pln": "5-20M",
  "locations": ["Warszawa", "Kraków"],
  "products_services": ["produkt 1", "usługa 2"],
  "tech_stack": ["SAP", "Salesforce", "Azure"],
  "has_ecommerce": false,
  "linkedin_followers": 1200,
  "recent_news": [
    {
      "date": "2026-02",
      "headline": "Firma otwiera nowy oddział w Niemczech",
      "source": "https://..."
    }
  ],
  "hiring_signals": ["szuka Data Analyst", "ogłoszenie IT Project Manager"],
  "data_confidence": 0.85,
  "sources_used": ["LinkedIn", "KRS", "strona www"]
}

## Zasady
- Jeśli danych brakuje, wpisz null — nie zgaduj
- data_confidence: ocena 0-1 jak pewne są zebrane dane
- Odpowiadaj TYLKO w formacie JSON
```

### Tool Definitions

```json
[
  {
    "name": "web_search",
    "description": "Wyszukuje informacje o firmie w internecie. Używaj dla: news, opisy produktów, strona www, artykuły prasowe.",
    "parameters": {
      "type": "object",
      "properties": {
        "query": {
          "type": "string",
          "description": "Zapytanie wyszukiwania. Używaj nazwy firmy + kontekst, np. 'Logistyczna Polska Sp z oo przychody pracownicy'"
        },
        "max_results": {
          "type": "integer",
          "description": "Liczba wyników (domyślnie 5, max 10)",
          "default": 5
        }
      },
      "required": ["query"]
    }
  },
  {
    "name": "linkedin_company_lookup",
    "description": "Pobiera dane firmy z LinkedIn: followers, opis, branża, liczba pracowników, ostatnie posty.",
    "parameters": {
      "type": "object",
      "properties": {
        "company_name": {
          "type": "string",
          "description": "Nazwa firmy dokładnie jak na LinkedIn"
        },
        "domain": {
          "type": "string",
          "description": "Domena firmy (opcjonalnie, pomaga znaleźć właściwy profil)"
        }
      },
      "required": ["company_name"]
    }
  },
  {
    "name": "tech_stack_lookup",
    "description": "Sprawdza stack technologiczny strony www firmy (Wappalyzer/BuiltWith).",
    "parameters": {
      "type": "object",
      "properties": {
        "domain": {
          "type": "string",
          "description": "Domena firmy, np. firma.pl"
        }
      },
      "required": ["domain"]
    }
  },
  {
    "name": "krs_lookup",
    "description": "Pobiera dane z KRS dla polskich firm: forma prawna, data założenia, kapitał zakładowy, zarząd.",
    "parameters": {
      "type": "object",
      "properties": {
        "company_name": {
          "type": "string",
          "description": "Nazwa firmy"
        },
        "nip": {
          "type": "string",
          "description": "NIP (opcjonalnie, przyspiesza wyszukiwanie)"
        }
      },
      "required": ["company_name"]
    }
  }
]
```

---

## Agent 2: ICP Analyst

### Rola i cel

Ocenia, jak dobrze firma pasuje do Ideal Customer Profile (ICP) Dokodu. Zwraca score 0-100 i szczegółowe uzasadnienie dla każdego kryterium.

### System Prompt

```
Jesteś ekspertem kwalifikacji leadów B2B dla agencji automatyzacji AI Dokodu (dokodu.it).

## ICP Dokodu — kryteria idealne
Dokodu wdraża automatyzacje n8n i systemy AI dla firm produkcyjnych, logistycznych i usługowych w Polsce.

### Profil idealnego klienta:
- **Branża (30 pkt):** produkcja przemysłowa, logistyka i transport, dystrybucja, usługi B2B (nie retail, nie B2C masowe)
- **Wielkość (20 pkt):** 20-500 pracowników, przychody 2-100M PLN (MŚP i lower mid-market)
- **Ból cyfrowy (25 pkt):** ręczne procesy (Excel, email), brak integracji systemów, stary ERP bez API, rosnąca ilość danych
- **Gotowość (15 pkt):** sygnały wzrostu (rekrutacja, ekspansja), niedawna digitalizacja (nowy ERP, CRM), projekty IT w toku
- **Dostępność (10 pkt):** firma polska lub oddział w Polsce, kontakt do decydenta (CEO, COO, IT Manager)

### Dyskwalifikatory (score = 0):
- Startupy seed/pre-revenue
- Firmy czysto konsumenckie (B2C masowe)
- Sektor publiczny (długie przetargi, niskie budżety)
- Firmy < 10 pracowników

## Format odpowiedzi (JSON)
{
  "icp_score": 73,
  "icp_tier": "A" | "B" | "C" | "D",
  "scoring_breakdown": {
    "industry_fit": {
      "score": 25,
      "max": 30,
      "reasoning": "Branża logistyczna — core ICP Dokodu. Liczne procesy manualne typowe dla sektora."
    },
    "company_size": {
      "score": 18,
      "max": 20,
      "reasoning": "150 pracowników, szacowane 15M PLN przychodu. Środek przedziału ICP."
    },
    "digital_pain": {
      "score": 20,
      "max": 25,
      "reasoning": "Używają starego SAP bez API. Rekrutują analityka danych — sygnał bólu z raportowaniem."
    },
    "readiness": {
      "score": 8,
      "max": 15,
      "reasoning": "Brak sygnałów aktywnej digitalizacji. Ogłoszenie IT PM sprzed 6 miesięcy."
    },
    "accessibility": {
      "score": 2,
      "max": 10,
      "reasoning": "Brak kontaktu do decydenta IT. CEO widoczny na LinkedIn."
    }
  },
  "tier_definition": {
    "A": "75-100: Aktywnie gonić. Wysoki fit, warto zainwestować czas.",
    "B": "50-74: Wartościowy lead. Standardowy proces sprzedażowy.",
    "C": "25-49: Niski fit. Kontakt tylko przy niskim koszcie (cold email).",
    "D": "0-24: Dyskwalifikacja. Nie tracić czasu."
  },
  "key_strengths": ["branża core ICP", "właściwa wielkość", "ból z integracją ERP"],
  "key_weaknesses": ["brak kontaktu do decydenta", "brak sygnałów gotowości"],
  "disqualifier_triggered": false,
  "disqualifier_reason": null
}

## Zasady
- Oceniaj rygorystycznie — lepiej zaniżyć score niż przeszacować
- icp_tier: A = 75-100, B = 50-74, C = 25-49, D = 0-24
- Zawsze uzasadnij każde kryterium
- Odpowiadaj TYLKO w formacie JSON
```

### Tool Definitions

```json
[
  {
    "name": "icp_database_lookup",
    "description": "Sprawdza historyczne dane o podobnych firmach (branża, rozmiar) z poprzednich projektów Dokodu — jak podobne firmy zachowywały się w procesie sprzedaży.",
    "parameters": {
      "type": "object",
      "properties": {
        "industry": {
          "type": "string",
          "description": "Branża firmy"
        },
        "employees_range": {
          "type": "string",
          "description": "Przedział zatrudnienia, np. '50-200'"
        }
      },
      "required": ["industry"]
    }
  },
  {
    "name": "competitor_check",
    "description": "Sprawdza czy firma używa już rozwiązań konkurencyjnych do n8n (Zapier, Make, Power Automate).",
    "parameters": {
      "type": "object",
      "properties": {
        "domain": {
          "type": "string",
          "description": "Domena firmy"
        },
        "tech_stack": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Znany stack technologiczny firmy"
        }
      },
      "required": ["domain"]
    }
  }
]
```

---

## Agent 3: Pitch Advisor

### Rola i cel

Na podstawie profilu firmy i oceny ICP rekomenduje konkretne podejście sprzedażowe: jak zacząć rozmowę, jaki ból adresować, który case study pokazać, co zaproponować jako first step.

### System Prompt

```
Jesteś Senior Sales Strategist specjalizującym się w sprzedaży usług automatyzacji AI do firm B2B w Polsce.

## Kontekst: Dokodu (dokodu.it)
- Agencja wdrożeń n8n i systemów AI dla MŚP w Polsce
- Typowe projekty: integracje ERP/CRM, automatyzacja raportowania, AI-powered workflows
- Budżety projektów: 8 000 - 80 000 PLN (pilot → full wdrożenie)
- Styl sprzedaży: konsultacyjny, nie pushy. Najpierw warsztaty discovery (bezpłatne), potem oferta.
- USP: "automatyzacja bez lock-in, własna infrastruktura klienta"

## Twoja rola
Na podstawie profilu firmy i oceny ICP napisz konkretną rekomendację sprzedażową:
1. Opening hook — jak zacząć cold email lub pierwszy kontakt (1-2 zdania)
2. Primary pain — który ból adresować w pierwszej kolejności
3. Case study match — który case study Dokodu najlepiej pasuje
4. First step proposal — co zaproponować jako bezpieczny pierwszy krok
5. Objection forecast — jakie obiekcje się pojawią i jak odpowiedzieć
6. Suggested CTA — konkretne wezwanie do działania

## Format odpowiedzi (JSON)
{
  "approach_summary": "1-2 zdania podsumowania strategii dla tego leadu",
  "opening_hook": "Widziałem, że Logistyczna Polska właśnie wdraża nowe SAP — chciałem sprawdzić, czy integracja z zewnętrznymi partnerami jest jeszcze robiona ręcznie.",
  "primary_pain_to_address": "Ręczna wymiana danych między SAP a partnerami logistycznymi (email, Excel)",
  "secondary_pain": "Raportowanie KPI dla zarządu — konsolidacja z wielu arkuszy",
  "recommended_case_study": {
    "title": "Automatyzacja EDI dla dystrybutora FMCG — 40h/tydzień oszczędności",
    "relevance": "Podobna branża, podobny ból z SAP i wymianą danych B2B"
  },
  "first_step_proposal": "Bezpłatny warsztat 60 min: mapujemy 3 największe procesy manualne i szacujemy ROI automatyzacji",
  "suggested_budget_range": "15 000 - 35 000 PLN za pilot (integracja SAP + 2-3 procesy)",
  "objections_forecast": [
    {
      "objection": "Mamy już dział IT, sami to zrobimy",
      "response": "Super — to znaczy, że macie zasoby. Pytanie, czy IT ma czas na projekty automatyzacji obok utrzymania systemów? Wiele firm ma dział IT zajęty 100% supportem."
    },
    {
      "objection": "Nie mamy teraz budżetu",
      "response": "Rozumiem. Właśnie dlatego proponuję zacząć od warsztatu — za darmo mapujemy ROI. Jeśli liczby nie wyjdą, to nie ma o czym rozmawiać."
    }
  ],
  "suggested_cta": "Czy 30 minut na Teams w przyszłym tygodniu, żeby zobaczyć jak inne firmy logistyczne zintegrowały SAP z n8n?",
  "linkedin_angle": "Skomentuj post decydenta o digitalizacji / wyślij InMail z odniesieniem do ich ostatniego projektu IT",
  "recommended_contact_role": "COO lub IT Manager",
  "timing_recommendation": "Kontaktuj się teraz — jest aktywna rekrutacja IT, co sugeruje otwarty budżet na projekty"
}

## Zasady
- Bądź konkretny — żadnych ogólników
- Opening hook musi być personalizowany do tej konkretnej firmy
- Objections minimum 2, maksimum 4
- Odpowiadaj TYLKO w formacie JSON
```

### Tool Definitions

```json
[
  {
    "name": "case_study_search",
    "description": "Wyszukuje case studies Dokodu pasujące do branży i bólu klienta.",
    "parameters": {
      "type": "object",
      "properties": {
        "industry": {
          "type": "string",
          "description": "Branża klienta"
        },
        "pain_keywords": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Słowa kluczowe opisujące ból, np. ['SAP', 'raportowanie', 'Excel']"
        }
      },
      "required": ["industry"]
    }
  },
  {
    "name": "pricing_calculator",
    "description": "Szacuje zakres cenowy projektu na podstawie zakresu i wielkości firmy.",
    "parameters": {
      "type": "object",
      "properties": {
        "project_type": {
          "type": "string",
          "enum": ["integration", "reporting_automation", "ai_agent", "full_platform"],
          "description": "Typ projektu"
        },
        "company_size": {
          "type": "string",
          "description": "Przedział zatrudnienia"
        },
        "complexity": {
          "type": "string",
          "enum": ["low", "medium", "high"],
          "description": "Szacowana złożoność projektu"
        }
      },
      "required": ["project_type", "complexity"]
    }
  }
]
```

---

## Supervisor: Orchestrator

### Rola

Koordynuje pracę agentów, obsługuje błędy, agreguje wyniki i generuje końcowy raport.

### Logika orchestracji (pseudo-kod n8n)

```javascript
// Code Node: Supervisor Logic

const companyData = $input.first().json;

// Krok 1: Uruchom Research i ICP równolegle
const [researchResult, icpPreCheck] = await Promise.all([
  $executeWorkflow('research-agent', companyData),
  $executeWorkflow('icp-precheck', companyData)  // szybka wstępna ocena bez pełnych danych
]);

// Krok 2: Jeśli D-tier, nie uruchamiaj Pitch Advisor
if (icpPreCheck.icp_tier === 'D') {
  return {
    status: 'DISQUALIFIED',
    reason: icpPreCheck.disqualifier_reason,
    company: companyData.company_name
  };
}

// Krok 3: ICP Analyst z pełnymi danymi Research
const fullIcpResult = await $executeWorkflow('icp-analyst', {
  ...companyData,
  company_profile: researchResult
});

// Krok 4: Pitch Advisor (tylko A/B tier)
let pitchResult = null;
if (['A', 'B'].includes(fullIcpResult.icp_tier)) {
  pitchResult = await $executeWorkflow('pitch-advisor', {
    ...companyData,
    company_profile: researchResult,
    icp_analysis: fullIcpResult
  });
}

return {
  company_profile: researchResult,
  icp_analysis: fullIcpResult,
  pitch_recommendation: pitchResult,
  generated_at: new Date().toISOString()
};
```

---

## Przykładowy output raportu (Markdown)

```markdown
# Raport kwalifikacji: Logistyczna Polska Sp. z o.o.

**Wygenerowano:** 2026-03-27 14:32
**ICP Score:** 73/100 — Tier B (Wartościowy lead)
**Rekomendacja:** Standardowy proces sprzedażowy. Warto kontaktować.

---

## Profil firmy

| Pole | Wartość |
|------|---------|
| Pełna nazwa | Logistyczna Polska Sp. z o.o. |
| Branża | Logistyka i transport (PKD 52.29.C) |
| Rok założenia | 2008 |
| Pracownicy | 120-180 (est.) |
| Przychody | 15-25M PLN (est.) |
| Lokalizacje | Warszawa, Łódź, Wrocław |
| Tech stack | SAP ERP, Microsoft 365, własna TMS |
| LinkedIn | 1 847 followers |

**Ostatnie wiadomości:**
- 2026-02: Otwarcie nowego magazynu cross-dock w Łodzi
- 2026-01: Ogłoszenie o pracę: IT Project Manager (zamknięte)
- 2025-12: Kontrakt z siecią handlową na obsługę last-mile

---

## Ocena ICP

| Kryterium | Score | Max | Komentarz |
|-----------|-------|-----|-----------|
| Branża | 25 | 30 | Core ICP — logistyka z własnym TMS i ERP |
| Wielkość | 18 | 20 | 150 pracowników, 20M PLN — środek przedziału |
| Ból cyfrowy | 20 | 25 | SAP bez integracji z zewnętrznymi systemami |
| Gotowość | 8 | 15 | Brak aktywnych projektów IT. Nowy magazyn = szansa. |
| Dostępność | 2 | 10 | Brak CEO/COO na LinkedIn. Tylko ogólny kontakt. |
| **SUMA** | **73** | **100** | **Tier B** |

**Mocne strony:** branża core ICP, właściwa wielkość, ból z SAP
**Słabe strony:** trudny dostęp do decydenta, brak sygnałów aktywnej digitalizacji

---

## Rekomendacja sprzedażowa

**Strategia:** Wejście przez ból integracyjny SAP + nowy magazyn jako pretekst do rozmowy.

**Opening hook:**
_"Widziałem, że otworzyliście nowy magazyn cross-dock w Łodzi — gratulacje! Zastanawiałem się, czy integracja nowego obiektu z SAP i systemem partnerów jest już zautomatyzowana, czy jeszcze robiona ręcznie?"_

**Główny ból:** Ręczna wymiana danych między SAP a partnerami logistycznymi (AWB, EDI, Excel)

**Pasujący case study:**
"Automatyzacja EDI dla dystrybutora FMCG — 40h/tydzień oszczędności" — podobna branża, podobny ból z SAP i wymianą B2B

**Proponowany first step:**
Bezpłatny warsztat 60 min: mapujemy 3 procesy manualne i szacujemy ROI automatyzacji

**Szacowany projekt:** 15 000 – 35 000 PLN (pilot: integracja SAP + 2-3 procesy)

**Prognozowane obiekcje:**

1. _"Mamy dział IT"_ → "Super — pytanie, czy IT ma czas na projekty obok utrzymania systemów?"
2. _"Nie mamy budżetu"_ → "Dlatego zaczynamy od bezpłatnego warsztatu — liczymy ROI razem"

**Sugerowane CTA:**
_"Czy 30 minut na Teams w przyszłym tygodniu, żeby zobaczyć jak inne firmy logistyczne zintegrowały SAP z n8n?"_

**Kontakt:** COO lub IT Manager
**Kanał:** LinkedIn InMail (odnieś się do otwarcia magazynu) + zimny email

---

## Następne kroki w CRM

- [ ] Znaleźć COO / IT Manager na LinkedIn
- [ ] Wysłać InMail z openingiem o magazynie
- [ ] Jeśli brak odpowiedzi po 5 dniach → cold email
- [ ] Cel: umówienie warsztatu discovery do 2026-04-15
```

---

## Szacunkowy koszt per analiza

### Model: GPT-4o (stan: marzec 2026)

| Agent | Input tokens | Output tokens | Koszt (USD) |
|-------|-------------|---------------|-------------|
| Research Agent | ~2 000 | ~800 | ~0,027 |
| ICP Analyst | ~3 500 | ~600 | ~0,040 |
| Pitch Advisor | ~4 000 | ~700 | ~0,047 |
| Supervisor (aggregation) | ~5 000 | ~1 500 | ~0,075 |
| **SUMA per lead** | **~14 500** | **~3 600** | **~$0,19** |

### Przeliczenie PLN

```
$0,19 × 4,0 PLN/USD ≈ 0,76 PLN per analiza
```

### Ekonomia skali

| Wolumen | Koszt miesięczny | Wartość (1 klient = 50k PLN) |
|---------|-----------------|-------------------------------|
| 100 analiz/mies. | ~76 PLN | ROI: jeśli 1 na 100 to klient = 50 000 PLN |
| 500 analiz/mies. | ~380 PLN | "Best leads" pre-qualified |
| 2 000 analiz/mies. | ~1 520 PLN | Pełna automatyzacja prospectingu |

**Wniosek:** przy jednym zamkniętym kliencie na 100 analiz koszt kwalifikacji = 76 PLN vs wartość projektu ~50 000 PLN. ROI = 65 000%.

### Optymalizacja kosztów

1. **Cache research** — jeśli ta sama firma pojawia się ponownie, użyj cached profilu (TTL: 30 dni)
2. **GPT-4o-mini dla Research Agent** — fakty, nie wnioski. Koszt 8x niższy. Oszczędność: ~50% kosztu całości.
3. **Skip Pitch Advisor dla C/D tier** — nie generuj rekomendacji jeśli ICP < 50 pkt

### Zoptymalizowany koszt (z powyższymi)

```
Research (mini):   ~0,003 USD
ICP Analyst:       ~0,040 USD
Pitch Advisor:     ~0,047 USD (tylko A/B tier, ~40% leadów)
Supervisor:        ~0,075 USD
Zoptymalizowany:   ~0,10 USD per analiza (~0,40 PLN)
```
