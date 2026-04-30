---
type: product_brainstorm
status: draft_idea
owner: kacper
last_reviewed: 2026-04-29
maturity: validation_needed
tags: [product, n8n, workflow, meetings, automation, universal]
---

# Meeting Loop Automator — szkic produktu

> **Status:** Pomysł produktowy do walidacji. **Najsilniejszy sygnał z 3 warsztatów Workshop Intelligence** — pętla "spotkanie → zadania → status → przypomnienie" pojawia się w **każdym** warsztacie niezależnie od branży i ról.

---

## Problem (potwierdzony 3/3 warsztatów)

Zespoły tracą 4-6h tygodniowo na manualne zarządzanie pętlą:

1. **Spotkanie** — agenda, dyskusja, ustalenia
2. **Podsumowanie** — kto co ustalił, co dalej
3. **Rozsyłanie** — email do uczestników z notatką
4. **Przydział zadań** — wpisanie do Redmine / Planner / Trello / Jira
5. **Statusowanie** — śledzenie czy ktoś wykonał
6. **Przypomnienia** — follow-up jeśli nie

W każdym kroku jest manualna praca, która **nie wymaga ludzkiego osądu** poza pierwszym (samym spotkaniem).

## Wzorzec z warsztatów

| Warsztat | Forma pain pointu |
| :--- | :--- |
| #1 (marketing/sales B2B) | "Podsumowania spotkań + follow-up emaile" |
| #2 (retail/e-commerce, 15 osób) | "Podsumowania spotkań — postanowienia, kroki, zadania" + "Pilnowanie innych działów o terminy" |
| #3 (marketplace/PPC, 14 osób) | "Sprytne TODO — listowanie i delegowanie" + "Sprawdzanie realizacji zadań zgodnie z podsumowaniami" + "Wyznaczanie kolejnych kroków, podział, timeline" |

## Architektura (szkic)

```
[Spotkanie Google Meet/Teams/Zoom]
    ↓ (transkrypcja: Whisper / native)
[Transkrypt]
    ↓ (LLM ekstrakcja)
[Strukturalny output: Postanowienia / Zadania / Pytania / Timeline]
    ↓
    ├─ [Email do uczestników] (Gmail/Outlook MCP)
    ├─ [Zadania → Redmine / Planner / Trello / Jira] (API)
    └─ [Cron: status check + follow-up] (n8n schedule)
        ↓
        [Email/Slack do osoby z zadaniem jeśli przeterminowane]
```

## Stack proponowany
- **n8n** — orchestrator (Dokodu już ma infra)
- **Whisper / OpenAI Whisper API** — transkrypcja PL
- **LLM (Claude/GPT-4)** — ekstrakcja strukturalna (postanowienia, zadania, timeline)
- **Adaptery:** Redmine, Planner, Trello, Jira, Asana, Linear (API REST)
- **Email/notification:** Gmail/Outlook + Slack/Teams

## Modele biznesowe (do wyboru)

### A) Wdrożenie per klient (B2B custom)
- 15-25k PLN za wdrożenie + integrację z konkretnym task managerem klienta
- Maintenance 1-2k PLN/mies
- Margin: wysoka, ale skalowanie liniowe

### B) SaaS / mikroservis
- 99-299 PLN/mies/zespół, samoobsługa
- Wymaga: UI, billing, multi-tenancy, support
- Margin: skalowanie wykładnicze, ale wysoki koszt wejścia

### C) Template w bibliotece n8n + szkolenie
- Szablon n8n + 1-dniowe szkolenie wdrożeniowe (3-5k)
- Klient utrzymuje sam
- Margin: niska na egzemplarz, ale zero-touch po wdrożeniu

**Rekomendacja do walidacji:** Zaczynać od (A) na 2-3 klientach z Workshop Intelligence (już znają temat z warsztatów), potem decyzja o (B) lub (C).

## Walidacja — kogo zapytać

**Z dotychczasowych 3 warsztatów (~37 osób z 3 firm) — co najmniej 12 osób wprost wskazało ten klaster.** Następne kroki:

1. **Wybrać 3 firmy** z dotychczasowych warsztatów, gdzie pain pojawił się najmocniej
2. **Discovery call (15 min):** ile czasu zespół traci tygodniowo? Jaki task manager? Jaki tool do meetingów?
3. **POC u 1 firmy:** 2 tygodnie, integracja z ich stackiem, mierzony efekt
4. **Decyzja go/no-go** po POC

## Konkurencja / inspiracje

- **Fireflies.ai, Otter.ai, Read.ai** — robią transkrypcję + summary, ale **kończą na summary**. Nie zamykają pętli zadania → status → follow-up.
- **Microsoft Copilot for Teams** — robi summary, ale enterprise-only, drogi, brak integracji z Redmine/Trello.
- **Zapier/Make templates** — istnieją podobne workflow, ale wymagają DIY. Nie są produktem.

**Differentiator Dokodu:** zamykanie pętli (POtransGenericAuto: status check + follow-up + przypomnienia, nie tylko summary).

## Open questions
- [ ] Czy to ma być produkt białej marki (Dokodu), czy mikroservis pod marką klienta?
- [ ] Jak rozwiązać prywatność transkryptów spotkań (cloud vs on-prem)? — łączy się z Zero-Trust AI positioning
- [ ] Czy w pierwszym wdrożeniu mocniej iść w "podsumowanie + zadania" (proste) czy "status check + follow-up" (mocniejsze, trudniejsze)?
- [ ] Jak to się ma do `/meet-transcribe` skill? Skill = prywatne use, produkt = klient. Może wspólny core.

## Następny krok

**Walidacja na Weekly Review (najbliższy piątek):** wybrać 3 firmy z dotychczasowych warsztatów do discovery call. Cel: zweryfikować czy to faktycznie pain wart 15-25k PLN, czy "nice to have".
