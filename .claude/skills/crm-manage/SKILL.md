---
name: crm-manage
description: Zarzadza Dokodu CRM — dodaje firmy, kontakty, deale, zmienia etapy pipeline, loguje aktywnosci. Uzywa serwera MCP (dokodu-crm) polaczonego z produkcyjna baza. Trigger slowa: "dodaj do crm", "crm", "dodaj firme", "nowy deal", "zmien etap", "pipeline", "zaloguj aktywnosc", "dodaj kontakt do crm", /crm-manage
---

# Instrukcja: Zarzadzanie Dokodu CRM

## KONTEKST

CRM Dokodu to oddzielna aplikacja na produkcji (system.dokodu.it).
Dostep przez serwer MCP `dokodu-crm` — 14 tooli do pelnego CRUD.
Kazdy tool przyjmuje parametr `action` + parametry specyficzne dla akcji.

## DOSTEPNE TOOLE MCP

| Tool | Akcje | Opis |
|------|-------|------|
| `companies` | list, get, create, update, delete | Firmy |
| `contacts` | list, get, create, update, delete | Osoby kontaktowe |
| `deals` | list, get, create, update, delete, change_stage | Szanse sprzedazowe |
| `pipeline` | list, get_stages | Pipeline i etapy |
| `tasks` | list, get, create, update, delete, complete | Zadania |
| `activities` | list, create | Aktywnosci (append-only) |
| `projects` | list, get, create, update, delete | Projekty |
| `milestones` | list, create, update | Kamienie milowe |
| `invoices` | list, get, create, update, delete, summary | Faktury |
| `timelogs` | list, create, update, delete, start, stop | Czas pracy |
| `calendar` | list, get, create, update, delete | Kalendarz |
| `tags` | list, create, delete | Tagi |
| `search` | query | Wyszukiwanie globalne |
| `audit_log` | list | Log audytowy |

## OPERACJE

### 1. Dodawanie firmy

```json
Tool: companies
{
  "action": "create",
  "data": {
    "name": "Firma Sp. z o.o.",
    "source": "LINKEDIN",
    "website": "https://firma.pl",
    "industry": "IT",
    "icpScore": "B",
    "consentType": "LEGITIMATE_INTEREST"
  }
}
```

Wymagane: `name`, `source` (WEBSITE_FORM, PRACUJ, LINKEDIN, REFERRAL, CONFERENCE, COLD_CALL, BUSINESS_CARD, MANUAL, OTHER)
Opcjonalne: `nip` (10 cyfr), `industry`, `size` (MICRO/SMALL/MEDIUM/LARGE), `website`, `city`, `icpScore` (A/B/C/X), `consentType`

### 2. Dodawanie kontaktu

```json
Tool: contacts
{
  "action": "create",
  "data": {
    "firstName": "Jan",
    "lastName": "Kowalski",
    "email": "jan@firma.pl",
    "phone": "+48500000000",
    "position": "CTO",
    "companyId": "<companyId>",
    "isPrimary": true
  }
}
```

### 3. Tworzenie deala

Najpierw znajdz etap pipeline:
```json
Tool: pipeline
{ "action": "get_stages", "pipelineId": "<pipelineId>" }
```

Potem stworz deal:
```json
Tool: deals
{
  "action": "create",
  "data": {
    "title": "Firma — Szkolenie AI",
    "value": 25000,
    "companyId": "<companyId>",
    "stageId": "<stageId>",
    "pipelineId": "<pipelineId>",
    "serviceType": "TRAINING",
    "source": "LINKEDIN"
  }
}
```

ServiceType: DIAGNOSIS, WORKSHOP, AUDIT, TRAINING, MVP_IMPLEMENTATION, ENTERPRISE_IMPLEMENTATION, RETAINER, COURSE_ONLINE, OTHER

### 4. Zmiana etapu deala

```json
Tool: deals
{ "action": "change_stage", "id": "<dealId>", "stageId": "<newStageId>" }
```

Dla etapu LOST (Przegrana) — wymagany powod:
```json
Tool: deals
{
  "action": "change_stage",
  "id": "<dealId>",
  "stageId": "<lostStageId>",
  "lostReasonCategory": "PRICE",
  "lostReasonDetails": "Za drogo wg klienta"
}
```

LostReasonCategory: PRICE, TIMING, COMPETITOR, NO_BUDGET, NO_NEED, WENT_SILENT, INTERNAL_CHANGE, SCOPE_MISMATCH, OTHER

Automatyka: WON tworzy projekt + milestones, LOST wymaga powodu.

### 5. Logowanie aktywnosci

```json
Tool: activities
{
  "action": "create",
  "data": {
    "type": "MEETING",
    "subject": "Discovery call z Jan Kowalski",
    "description": "Omowilismy potrzeby automatyzacji. Zainteresowani szkoleniem AI.",
    "dealId": "<dealId>",
    "companyId": "<companyId>",
    "durationMinutes": 45
  }
}
```

Typy: CALL, EMAIL_SENT, EMAIL_RECEIVED, MEETING, NOTE, LINKEDIN_MESSAGE, SMS

### 6. Sprawdzanie stanu pipeline

```json
Tool: pipeline
{ "action": "get_stages" }
```

Zwraca etapy z dealami, wartosciami i weighted values.

### 7. Wyszukiwanie

```json
Tool: search
{ "action": "query", "q": "dokodu" }
```

Szuka po firmach (name, nip), kontaktach (imie, nazwisko, email), dealach (tytul).

### 8. Zarzadzanie zadaniami

```json
Tool: tasks
{
  "action": "create",
  "data": {
    "title": "Follow-up po discovery call",
    "priority": "HIGH",
    "type": "FOLLOW_UP",
    "dueDate": "2026-04-03",
    "dealId": "<dealId>",
    "companyId": "<companyId>"
  }
}
```

Zamykanie: `{ "action": "complete", "id": "<taskId>" }`

## LISTY Z FILTRAMI

Wszystkie listy wspieraja paginacje (`page`, `pageSize`) i filtry:

- **companies**: search, status, icpScore, assignedToId, source
- **contacts**: companyId, search, roleType
- **deals**: pipelineId, stageId, companyId, assignedToId, search
- **tasks**: status, assignedToId, dealId, companyId, priority, dueDateFrom, dueDateTo
- **activities**: type, dealId, companyId, contactPersonId, dateFrom, dateTo
- **invoices**: status, companyId, dealId, projectId

## ZASADY

1. **Kazdy kontakt B2B → CRM.** Nawet jesli "za malo danych" — dodaj jako CONTACT z source.
2. **Nie duplikuj.** Przed dodaniem uzyj `search` aby sprawdzic czy firma/kontakt juz istnieje.
3. **Consent RODO.** Kazda firma musi miec `consentType`. LinkedIn/wizytowka = LEGITIMATE_INTEREST. Formularz = FORM_SUBMISSION.
4. **Aktywnosc po kazdym kontakcie.** Po rozmowie, mailu, spotkaniu — zaloguj Activity.
5. **PLAN_TYGODNIA sync.** Gdy dodajesz deal lub zmieniasz etap, sprawdz czy trzeba dodac follow-up do PLAN_TYGODNIA.md.
