---
type: workshop_notes
status: active
owner: kacper
last_reviewed: 2026-04-29
workshop_date: 2026-04-29
workshop_topic: Copilot Studio
participants_count: 14
industry: marketplace_agency_ppc
tags: [workshop, copilot-studio, marketplace, ppc, intelligence, anonymized]
---

# Warsztat — zespół marketplace/PPC, Copilot Studio (2026-04-29)

> **Zasada Workshop Intelligence:** Tylko wzorce, statystyki i klastry. **Bez imion, bez nazw firm, bez cytatów dosłownych.**

---

## Profil grupy

- **Liczebność:** ~14 osób
- **Branża:** agencja marketplace + PPC (Allegro/Amazon)
- **Tematyka warsztatu:** Copilot Studio
- **Mix ról:**
  - PPC specialists (kampanie ADS, optymalizacja, raportowanie) — 3
  - Marketplace specialists / e-commerce ops — 3
  - Project managers — 3
  - Data analysts / BI — 2
  - Zarządzanie zespołem / CEO — 3

## Stack i narzędzia

**LLM-y w użyciu (sygnał: multi-LLM bez governance):**
- Copilot — dominujący default, wymieniony przez 8/14 jako pierwszy/jedyny
- ChatGPT — wymieniony przez 5/14
- Gemini — 3/14
- Claude — 2/14
- n8n — 2/14 (świadomi operatorzy)

**Stack analityczny / operacyjny:**
- Excel + VBA + Power Query
- Power BI (analityka, raportowanie, dashboards)
- SQL (kilka osób, w tym data analysts)
- Python (data analyst, automatyzacje, ETL)
- Allegro Analytics, Perpetua (panele PPC marketplace)
- Looker (jako źródło danych, nie default BI)
- Redmine (project management)
- Jira (PM)
- Planner / Trello (taski)
- Local AI — wymienione wprost (opentranscribe + lokalna baza)

**Sygnał:** zespół ma kompetencje techniczne wyższe niż średnia w warsztatach #1 i #2 (Python, SQL, ETL, lokalne AI obecne).

---

## Pain pointy / zadania powtarzalne (klastry)

### Klaster #1 — PPC client onboarding & operations (5+ wzmianek)
- Audyt kampanii nowego klienta → dokument gotowy do wysłania
- Setup Google Ads (przede wszystkim faza setup, nie sama optymalizacja)
- Analiza raportów PPC + rekomendacje optymalizacji
- Scalanie danych z paneli reklamowych (Excel z różnych źródeł)
- Weryfikacja wyników kampanii

**Insight:** Setup nowego klienta to dominujący use case w agencji PPC — manualny, powtarzalny, krytyczny dla pierwszego wrażenia. Idealny target dla automatyzacji.

### Klaster #2 — Meeting → zadania → status (4+ wzmianek)
- Podsumowania spotkań + rozsyłanie podsumowań i przypisanych zadań
- Sprawdzanie realizacji zadań zgodnie z wcześniejszymi podsumowaniami
- Wyznaczanie kolejnych kroków, podział zadań, timeline
- "Sprytne TODO" — listowanie zadań i delegowanie na Copilot / zespół / siebie
- Statusowanie w Redmine / Planner / Trello + dystrybucja zadań
- Follow-upy

**Insight:** Klaster występuje w 3/3 warsztatach, niezależnie od branży. Najsilniejszy sygnał uniwersalny.

### Klaster #3 — Knowledge management z retirement (3+ wzmianek)
- Zarządzanie wiedzą o projekcie: założenia → realizacja → optymalizacja
- Gromadzenie wiedzy, jej odświeżanie, format przechowywania, **retirement**
- Wiedza branżowa vs projektowa vs firmowa — różne cykle życia
- Dokumentacja raportowania i zaszytej logiki biznesowej z wielu źródeł (Redmine/Teams/mail)
- Baza wiedzy jako część workflow analitycznego

**Insight:** Koncepcja "retirement" wiedzy — rzadko spotykana, sygnał dojrzałości operacyjnej. Niszowy ale głęboki temat.

### Klaster #4 — Client communication sequences (3+ wzmianek)
- Komunikacja mailowa z klientami
- Follow-upy po pierwszej próbie kontaktu, po wysłanej ofercie (sekwencje)
- Przygotowywanie ofert

### Klaster #5 — File-to-structure / data extraction
- Rozpoznawanie plików PDF → dane ustrukturyzowane
- Pobieranie raportów z zewnętrznych źródeł (np. Looker) na dysk sieciowy
- Integracja z zasobami lokalnymi (Redmine, baza danych, opentranscribe)

### Klaster #6 — Industry news scraping
- Scraper nowinek PPC z kanałów YouTube w skondensowanej treści
- Nowinki AI / lojalność / programy uruchomione przez konkurencję

### Klaster #7 — Reporting & analytics
- Analiza raportów Power BI / Excel
- Raporty sprzedażowe + analityka, project management, analiza ofert
- Scenariusze testowe, dokumentacja biznesowa funkcjonalności, harmonogramy
- Raporty finansowe spółki + analizy odchyleń

### Klaster #8 — Sales/finance operations
- Fakturowanie + windykacja miękka
- Tworzenie plików rozliczeniowych
- Raporty sprzedażowe i mediowe
- Sprawdzanie wystawionej bazy klientów (zgody, warunki)

### Klaster #9 — Team & business operations
- Rozliczanie celów dla zespołów + cele dla członków zespołu
- Analiza efektów pracy i czasu spędzonego nad obszarami
- Rozliczenia między spółkowe
- Regularne analizy rynku, graczy, klientów

### Klaster #10 — Content & social
- Generowanie treści do publikacji na LinkedIn
- Przygotowywanie prezentacji z wnioskami
- Prezentacje z analizami

### Klaster #11 — Business development signals
- Analiza i rekomendacja eventów pod kątem potencjału do pozyskania nowego biznesu

---

## Big bets (aspiracyjne)

- **Local AI w stacku marketplace** — Redmine + baza danych + opentranscribe lokalnie. Zespół świadomie unika cloud dla danych operacyjnych.
- **Knowledge retirement** — świadomość że wiedza ma datę wygaśnięcia. Rzadko spotykana, dojrzała koncepcja.
- **Orchestrator delegacji zadań** ("sprytne TODO") — codzienny triaż gdzie zadanie powinno trafić: Copilot / ja / zespół.

---

## Meta-sygnały / dilematy zespołu

- **"Power Automate vs Copilot Studio"** — pytanie zadane wprost. Sygnał, że nawet zaawansowany zespół Microsoft nie ma jasności w decyzji narzędziowej. Treść warsztatu = Copilot Studio, ale uczestnicy wprost pytają o granicę z Power Automate.
- **Multi-LLM bez governance** — zespół używa 4 różnych modeli równolegle, bez wskazówki "którego do czego". Wzorzec występuje w każdym warsztacie.
- **Marketplace = branża z niedoborem narzędzi do scalania danych** — Allegro Analytics + Perpetua + panele reklamowe = manualna sklejka w Excelu. Otwarta nisza dla automatyzacji.

---

## Implikacje dla Dokodu

### Oferta szkoleniowa
- **Decision framework: Power Automate vs Copilot Studio** — moduł szkoleniowy specyficzny dla Microsoft stack. Realne pytanie z rynku, brak dobrych odpowiedzi w polskim necie.
- **Multi-LLM governance** — moduł "którego LLM do czego" + audyt narzędzi w firmie.

### Produkty / wdrożenia
- **PPC Onboarding Automator** — szablon audytu nowego klienta + automatyzacja setupu Google Ads. Specyficzne dla agencji marketplace/PPC.
- **Meeting Loop Automator** — uniwersalny workflow podsumowanie → zadania → status → przypomnienie z integracją Redmine/Planner/Trello. Top kandydat na produkt boxowy (3/3 warsztatów).
- **PPC Content Radar** — scraper nowinek z YouTube/blogów branżowych w skondensowanej treści. Mikroprodukt dla agencji reklamowych.

### Positioning
- **Zero-Trust AI = Local AI dla danych operacyjnych** — branża marketplace ma świadomych operatorów, którzy już wybierają local AI. Argument do wdrożeń (opentranscribe + Redmine + baza on-prem).

---

## Kąty do contentu (wygenerowane z tego warsztatu)

1. **"Power Automate vs Copilot Studio — to nie jest ten sam wybór, co Wam się wydaje"** — łapie ludzi w Microsoft stack, niedocenione w polskim necie
2. **"Setup nowego klienta = 60% pracy agencji PPC. Dlaczego nikt tego nie automatyzuje?"** — branżowo specyficzne, ale konkretne
3. **"Wiedza projektowa ma datę wygaśnięcia. Co to znaczy knowledge retirement?"** — niszowy, ale dla dojrzałych zespołów
4. **"Pętla, która zjada zespołom 6h tygodniowo: spotkanie → zadania → status → przypomnienie"** — uniwersalny, potwierdzony 3/3 warsztatami
5. **"Zespół z 4 różnymi LLM bez governance. Klasyczny obraz 2026."** — multi-LLM chaos jako trend
6. **"Local AI dla zespołu danych: Redmine + opentranscribe + baza, bez chmury"** — Zero-Trust AI w wersji infra
7. **"Scraper nowinek PPC z YouTube — narzędzie, które każdy zespół reklamowy buduje na kolanie"** — niszowo ale konkretnie
8. **"Marketplace operations = manualna sklejka Excela. Co z tym zrobić?"** — pain point branżowy
