---
type: index
status: active
owner: kacper
last_reviewed: 2026-03-06
tags: [index, nawigacja, system, para]
---

# DOKODU BRAIN — Second Brain Agencji AI
> Metodologia PARA ztuningowana pod realia agencji automatyzacji AI.
> Wlasciciel: Kacper Sieradzinski | CEO Dokodu sp. z o.o.

---

## ZASADA JEDNEGO OKNA

Zacznij zawsze od [[000_DASHBOARD.md]]. Koniec. Wszystko inne linkuje stąd.

---

## MAPA SYSTEMU

```
DOKODU_BRAIN/
│
├── 000_DASHBOARD.md          ← START DNIA. Mission Control. KPI. Priorytety.
├── 00_INBOX.md               ← Wrzutki. Przetwarzaj w piatek. Nie mysl — wrzucaj.
├── 001_VISION.md             ← North Star. Kim jestesmy za 3 lata. Czytaj gdy masz watpliwosci.
├── 005_SKILLS.md             ← Lead AI Architect 2026 — matryca kompetencji, roadmapa
├── TODO.md                   ← Roadmap rozwoju firmy. Fazy 0-5 + moonshots.
│
├── 10_PROJECTS/              ← Aktywne projekty z deadlinem i wlascicielem
│   ├── PRJ_Animex_Szkolenie/
│   │   └── PRJ_Animex_Szkolenie.md       Szkolenie BOK — 18k PLN | Deadline: 20.03
│   ├── PRJ_Corleonis_Wdrozenie/
│   │   └── PRJ_Corleonis_Wdrozenie.md    Obieg dokumentow — 35k + 3k/mies | Deadline: 15.04
│   └── PRJ_Kurs_n8n_Launch/
│       └── PRJ_Kurs_n8n_Launch.md        Kurs online — cel 120k PLN | CZERWONY — blokada VSL
│
├── 20_AREAS/                 ← Stale obszary odpowiedzialnosci (bez deadline)
│   ├── AREA_Marketing_Sales/
│   │   ├── AREA_Marketing_Sales.md       Index obszaru. Metryki. Aktywne inicjatywy.
│   │   ├── 100_MARKETING_ADS.md          Budzety, kreacje, ICP, tracking
│   │   ├── CRM_Leady_B2B.md              Pipeline, BANT+, discovery framework
│   │   └── Newsletter_Dokodu_Brief.md    Strategia newslettera, szablony, sekwencja
│   ├── AREA_Legal_Compliance/
│   │   ├── AREA_Legal_Compliance.md      Index obszaru. Kalendarz prawny. Zadania.
│   │   ├── AI_Act_Tracker.md             Mapa AI Act, daty krytyczne, klasyfikacja ryzyka
│   │   └── RODO_Checklist.md             Checklist RODO, standardy n8n, PII
│   ├── AREA_n8n_Infrastructure/
│   │   └── AREA_n8n_Infrastructure.md    Stack, docker, vault, standardy, troubleshooting
│   ├── AREA_Finanse/
│   │   └── AREA_Finanse.md               Cashflow, fakturowanie, windykacja, KPI 2026
│   └── AREA_HR_Kultura/
│       └── AREA_HR_Kultura.md            Wartosci, zespol, rekrutacja, spotkania, dobrostan
│
├── 30_RESOURCES/             ← Biblioteka wiedzy (nie ginie, komplikuje sie z kazdym projektem)
│   ├── RES_Prompt_Library/
│   │   └── 300_BIBLIOTEKA_PROMPTOW.md    15+ promptow prod. (ekstrakcja, sales, legal, AI Shadow)
│   ├── RES_n8n_Blueprints/
│   │   └── N8N_Blueprints.md             8 wzorcow workflowow z kodem i architektura ASCII
│   ├── RES_AI_Act_Notes/
│   │   └── AI_Act_Notes.md               Notatki robocze z AI Act, definicje, wytyczne EROD
│   ├── RES_Sales_Playbook/
│   │   └── Sales_Playbook.md             Cennik, ICP, etapy sprzedazy, obiekcje, oferty
│   ├── RES_Client_Onboarding/
│   │   └── Client_Onboarding.md          Kickoff, komunikacja, odbiory, change request
│   ├── RES_Templates/
│   │   ├── Templates.md                  12 gotowych szablonow (emaile, DPIA, CR, retro)
│   │   ├── Schema_Faktura_v1.md          JSON Schema faktury VAT + walidator NIP
│   │   └── Logging_Standard.md           Standard logowania dla n8n Code Nodes
│   ├── RES_Market_Intelligence/
│   │   └── Competitor_Landscape.md       Mapa rynku, analiza konkurencji, white space
│   ├── RES_Industry_Playbooks/
│   │   ├── Playbook_Logistyka.md         Bole, systemy, pytania discovery, ROI (Corleonis)
│   │   └── Playbook_Produkcja.md         Bole, systemy, pytania discovery, DRAFT (Animex)
│   ├── RES_Content_Calendar/
│   │   └── Content_Calendar.md           Miesięczny plan LinkedIn + blog + bank tematow
│   └── RES_Partners/
│       └── Partners.md                   Rejestr partnerow, program referralowy, networking
│
└── 40_ARCHIVE/               ← Zakonczone projekty i zasoby (read-only)
    └── README.md                         Instrukcja archiwizacji i polityka retencji
```

---

## SKILLS — KOMENDY DO ZARZADZANIA BRAIN

Nie edytuj plikow recznie. Uzyj odpowiedniego skilla:

| Komenda | Co robi |
| :--- | :--- |
| `/brain-new-customer` | Tworzy nowego klienta (katalog + 3 pliki) |
| `/brain-new-project` | Tworzy nowy projekt z templatemem |
| `/brain-add-lead` | Dodaje lead do CRM + kwalifikacja BANT+ |
| `/brain-lead-research` | Bada firme/lead pod katem ICP Dokodu |
| `/brain-meeting-notes` | Przetwarza notatki/transkrypcje ze spotkania |
| `/brain-capture` | Szybki capture do Inboxa (mysli, pomysly, todo) |
| `/brain-weekly-review` | Tygodniowy przeglad z analizą (piątek) |
| `/brain-status` | Szybki przeglad stanu brain (projekty, leady, inbox) |
| `/brain-new-prompt` | Dodaje prompt do Biblioteki Promptow |
| `/brain-archive-project` | Archiwizuje zakonczony projekt + retrospektywa |

**Skills zainstalowane w:** `~/.claude/skills/`

---

## RYTM UZYWANIA

| Czestotliwosc | Co robisz |
| :--- | :--- |
| **Codziennie (rano)** | Otwierasz [[000_DASHBOARD.md]], patrzysz na P1/P2/P3 |
| **Codziennie (na biezaco)** | Wrzucasz do [[00_INBOX.md]] — bez kategoryzowania |
| **Tygodniowo (piatek)** | Weekly Review: Inbox → przetworzenie, Projekty → update |
| **Miesiecznie** | Finanse, Marketing wyniki, Skills review |
| **Po projekcie** | Archiwizacja + retrospektywa + update Blueprintow |

---

## FILOZOFIA SYSTEMU

1. **Capture first, organize later** — najpierw wrzuc do Inboxu, nie trwa kategoryzowac w locie
2. **Projects die without next actions** — kazdy projekt musi miec "Nastepny krok" z deadline
3. **Resources compound** — biblioteka promptow i blueprintow rosnie z kazdym projektem
4. **Weekly Review is non-negotiable** — bez piatku caly system sie sypie
5. **One source of truth** — jezeli informacja jest w 2 miejscach, jest w zadnym

---

## WSKAZOWKA DLA AI (Executive Business Shadow)

Jezeli uzywasz AI do pracy z tym systemem, zaladuj prompt:
[[30_RESOURCES/RES_Prompt_Library/300_BIBLIOTEKA_PROMPTOW]] → PROMPT-040

Daj AI dostep do:
- [[000_DASHBOARD.md]] — priorytety i status projektow
- [[00_INBOX.md]] — otwarte watki
- [[005_SKILLS.md]] — gdzie jestes, dokad zmierzasz

Pytaj: "Co widze, czego nie widze? Gdzie tracę energie? Co usunac?"

---

*System zbudowany: Marzec 2026 | Aktualizuj, nie archiwizuj. Zyjacy dokument.*
