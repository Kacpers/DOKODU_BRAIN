---
type: blueprint
modul: "04 — Architektura Modularna"
lekcja: "05 — Workflow Blueprint"
projekt: PRJ_Kurs_n8n_Launch
autor: Kacper Sieradziński / Dokodu
wersja: "1.0"
data: 2026-03-27
status: gotowy
tags: [n8n, subworkflow, routing, ai-classification, gpt4o, ticketing, modular-architecture]
---

# Blueprint: Corporate Request Router

> **Cel:** Jeden punkt wejscia dla wszystkich zglaszen wewnetrznych firmy — AI klasyfikuje zgloszenie i routuje do odpowiedniego subworkflow (IT / HR / Finance / Sales / Other). Kazdy subworkflow dziala autonomicznie z jasno zdefiniowanym kontraktem Input/Output.

---

## 1. Diagram: Master Workflow i Subworkflows

```
                     ┌─────────────────────────────────────┐
                     │        ZGLASZAJACY                   │
                     │  (email / formularz webowy / Slack)  │
                     └────────────────┬────────────────────┘
                                      │
                                      ▼
                     ┌─────────────────────────────────────┐
                     │  [1] Webhook / Email Trigger          │
                     │  MASTER WORKFLOW                      │
                     └────────────────┬────────────────────┘
                                      │
                                      ▼
                     ┌─────────────────────────────────────┐
                     │  [2] AI Classify (GPT-4o mini)        │
                     │  kategoria: IT / HR / Finance /       │
                     │            Sales / Other              │
                     │  + ticket_id (UUID) + priorytet       │
                     └────────────────┬────────────────────┘
                                      │
                                      ▼
                     ┌─────────────────────────────────────┐
                     │  [3] Switch — routing                 │
                     └──┬──────┬──────┬──────┬──────┬──────┘
                        │      │      │      │      │
                       IT     HR   Finance Sales  Other
                        │      │      │      │      │
                        ▼      ▼      ▼      ▼      ▼
               ┌──────┐ ┌────┐ ┌───────┐ ┌─────┐ ┌───────┐
               │ [4]  │ │[5] │ │  [6]  │ │ [7] │ │  [8]  │
               │  IT  │ │ HR │ │Finance│ │Sales│ │ Other │
               │  Sub │ │Sub │ │  Sub  │ │ Sub │ │  Sub  │
               └──────┘ └────┘ └───────┘ └─────┘ └───────┘
                        │      │      │      │      │
                        └──────┴──────┴──────┴──────┘
                                      │
                                      ▼
                     ┌─────────────────────────────────────┐
                     │  [9] Merge wynikow                    │
                     │  (zbierz output ze wszystkich sciezek)│
                     └────────────────┬────────────────────┘
                                      │
                                      ▼
                     ┌─────────────────────────────────────┐
                     │  [10] Email / Slack                   │
                     │  Potwierdzenie dla zglaszajacego      │
                     │  Numer ticketu: {{ ticket_id }}       │
                     └─────────────────────────────────────┘


  SUBWORKFLOWS (odrebne workflow w n8n):
  ─────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────┐
  │  SW-IT: IT Support                                          │
  │  Input → [Jira ticket] → [Slack #it-support] → Output      │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  SW-HR: Human Resources                                     │
  │  Input → [BambooHR ticket] → [Email HR] → Output           │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  SW-Finance: Finance                                        │
  │  Input → [Google Sheets log] → [Email CFO] → Output        │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  SW-Sales: Sales Support                                    │
  │  Input → [CRM opportunity] → [Slack #sales] → Output       │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  SW-Other: Human Queue                                      │
  │  Input → [Google Sheets kolejka] → [Email manager] → Output│
  └─────────────────────────────────────────────────────────────┘
```

---

## 2. Input/Output Contract — JSON Schema

Kazdy subworkflow MUSI przyjmowac i zwracac dane zgodnie z kontraktem. To gwarancja modularnosci — mozna wymieniac subworkflow bez zmiany master workflow.

### Input Schema (wspolny dla wszystkich subworkflows)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SubworkflowInput",
  "type": "object",
  "required": ["ticket_id", "category", "priority", "requester", "request"],
  "properties": {
    "ticket_id": {
      "type": "string",
      "description": "Unikalny identyfikator UUID ticketu",
      "example": "TKT-2026-a3f9e2"
    },
    "category": {
      "type": "string",
      "enum": ["IT", "HR", "Finance", "Sales", "Other"],
      "description": "Kategoria nadana przez AI"
    },
    "priority": {
      "type": "string",
      "enum": ["low", "medium", "high", "critical"],
      "description": "Priorytet nadany przez AI na podstawie tresci"
    },
    "requester": {
      "type": "object",
      "required": ["name", "email"],
      "properties": {
        "name":       { "type": "string" },
        "email":      { "type": "string", "format": "email" },
        "department": { "type": "string" },
        "slack_id":   { "type": "string", "description": "Opcjonalny Slack User ID" }
      }
    },
    "request": {
      "type": "object",
      "required": ["subject", "body"],
      "properties": {
        "subject":  { "type": "string", "description": "Temat zgloszenia" },
        "body":     { "type": "string", "description": "Pelna tresc zgloszenia" },
        "source":   { "type": "string", "enum": ["email", "webhook", "slack"] },
        "received_at": { "type": "string", "format": "date-time" }
      }
    },
    "ai_summary": {
      "type": "string",
      "description": "Krotkie podsumowanie wygenerowane przez AI (1-2 zdania)"
    }
  }
}
```

### Output Schema (wspolny dla wszystkich subworkflows)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SubworkflowOutput",
  "type": "object",
  "required": ["ticket_id", "category", "status", "processed_at"],
  "properties": {
    "ticket_id": {
      "type": "string",
      "description": "Ten sam ticket_id co w Input — niezmieniony"
    },
    "category": {
      "type": "string",
      "enum": ["IT", "HR", "Finance", "Sales", "Other"]
    },
    "status": {
      "type": "string",
      "enum": ["created", "queued", "escalated", "error"],
      "description": "Status przetworzenia przez subworkflow"
    },
    "external_ticket_id": {
      "type": "string",
      "description": "ID ticketu w zewnetrznym systemie (Jira, BambooHR, CRM...)"
    },
    "assigned_to": {
      "type": "string",
      "description": "Osoba lub kolejka do ktorej przypisano ticket"
    },
    "estimated_response_time": {
      "type": "string",
      "description": "Szacowany czas odpowiedzi (np. '4h', '1 dzien roboczy')"
    },
    "confirmation_message": {
      "type": "string",
      "description": "Tresc potwierdzenia do wyslania zglaszajacemu"
    },
    "processed_at": {
      "type": "string",
      "format": "date-time"
    },
    "error": {
      "type": ["string", "null"],
      "description": "Komunikat bledu jezeli status = error"
    }
  }
}
```

---

## 3. Master Workflow — Nodes z Konfiguracja

### [1] Webhook / Email Trigger

```
Opcja A — Webhook:
  Node type:   n8n-nodes-base.webhook
  Method:      POST
  Path:        /request
  Auth:        Header (X-Api-Key)

Opcja B — Email (IMAP):
  Node type:   n8n-nodes-base.emailReadImap
  Mailbox:     zgloszenia@firma.pl
  Check every: 1 minute
  Mark as read: true
```

Po triggerze: normalizuj dane do wspolnego formatu (Code node lub Set node).

---

### [2] AI Classify (GPT-4o mini)

```
Node type:       @n8n/n8n-nodes-langchain.openAi
Model:           gpt-4o-mini
Temperature:     0
Max tokens:      300
Response format: JSON object
```

**System prompt:**

```
Jestes klasyfikatorem zglaszen wewnetrznych firmy.
Na podstawie tresci zgloszenia:
1. Przypisz kategorię: IT | HR | Finance | Sales | Other
2. Okresl priorytety: low | medium | high | critical
3. Napisz krotkie podsumowanie (1-2 zdania) po polsku.

Zasady klasyfikacji:
- IT: problemy z komputerem, oprogramowaniem, dostepem, secia, sprzetem
- HR: urlopy, benefity, rekrutacja, onboarding, wynagrodzenie, zwolnienia
- Finance: faktury, platnosci, budzety, korekty finansowe, koszty
- Sales: leady, oferty, umowy, rabaty, wsparcie pre-sales, klienci
- Other: wszystko inne, wymagajace recznej oceny

Odpowiedz WYLACZNIE w JSON:
{
  "category": "IT",
  "priority": "medium",
  "ai_summary": "Uzytkownik zglosil problem z logowaniem do systemu CRM."
}
```

**User prompt:**

```
Temat: {{ $json.subject }}
Tresc: {{ $json.body }}
Nadawca: {{ $json.requester.name }} ({{ $json.requester.department }})
```

---

### [3] Switch — routing do subworkflows

```
Node type:   n8n-nodes-base.switch
Mode:        Rules

Regula 1:  {{ $json.category }} = "IT"       → output 0
Regula 2:  {{ $json.category }} = "HR"       → output 1
Regula 3:  {{ $json.category }} = "Finance"  → output 2
Regula 4:  {{ $json.category }} = "Sales"    → output 3
Regula 5:  (fallback)                        → output 4
```

---

### [4–8] Execute Workflow — subworkflows

```
Node type:       n8n-nodes-base.executeWorkflow
Source:          Database (wybierz z listy workflow)
Wait for output: true  ← KLUCZOWE — czekaj na wynik subworkflow

[4] workflowId: SW-IT-Support
[5] workflowId: SW-HR-Requests
[6] workflowId: SW-Finance-Requests
[7] workflowId: SW-Sales-Support
[8] workflowId: SW-Other-HumanQueue

Input data: przekaz caly $json (z ticket_id, category, priority, requester, request, ai_summary)
```

---

### [9] Merge wynikow

```
Node type:   n8n-nodes-base.merge
Mode:        Append
```

Zbiera outputy ze wszystkich sciezek Switch (w praktyce zawsze aktywna jest tylko 1 sciezka dla danego zgloszenia).

---

### [10] Email / Slack — potwierdzenie dla zglaszajacego

```
Node type (Email):
  n8n-nodes-base.gmail lub n8n-nodes-base.sendEmail
  To:      {{ $json.requester.email }}
  Subject: [Ticket {{ $json.ticket_id }}] Twoje zgloszenie zostalo przyjete
  Body:    {{ $json.confirmation_message }}
           Szacowany czas odpowiedzi: {{ $json.estimated_response_time }}

Node type (Slack, opcjonalnie):
  n8n-nodes-base.slack
  Channel:  DM do {{ $json.requester.slack_id }}
  Message:  {{ $json.confirmation_message }}
```

---

## 4. Subworkflows — Szczegoly

### SW-IT: IT Support

**Wyzwalacz:** `Execute Workflow Trigger`

| Etap | Akcja | Konfiguracja |
|---|---|---|
| Przyjmij input | Execute Workflow Trigger | pobierz `$json` z Master |
| Utworz ticket | HTTP Request → Jira API | `POST /rest/api/3/issue`, project: `IT`, issuetype: `Service Request` |
| Powiadom zespol | Slack | kanal `#it-support`, mention `@it-team` jesli `priority = high/critical` |
| Zwroc output | Set node | `status: created`, `external_ticket_id: JIRA-ID`, `assigned_to: it-team@firma.pl` |

**Input przyklad:**
```json
{
  "ticket_id": "TKT-2026-a3f9e2",
  "category": "IT",
  "priority": "high",
  "requester": { "name": "Anna Nowak", "email": "anna@firma.pl", "department": "Marketing" },
  "request": { "subject": "Laptop sie nie wlacza", "body": "Od rana laptop nie startuje, mam deadline dzisiaj." },
  "ai_summary": "Uzytkownik zglosil awarie laptopa blokujaca prace."
}
```

**Output przyklad:**
```json
{
  "ticket_id": "TKT-2026-a3f9e2",
  "category": "IT",
  "status": "created",
  "external_ticket_id": "IT-4821",
  "assigned_to": "helpdesk@firma.pl",
  "estimated_response_time": "2h (priorytet HIGH)",
  "confirmation_message": "Twoje zgloszenie IT-4821 zostalo przyjete. Zespol IT skontaktuje sie z Toba w ciagu 2h.",
  "processed_at": "2026-04-15T09:25:00Z"
}
```

---

### SW-HR: Human Resources

**Wyzwalacz:** `Execute Workflow Trigger`

| Etap | Akcja | Konfiguracja |
|---|---|---|
| Przyjmij input | Execute Workflow Trigger | pobierz `$json` |
| Kategoryzuj HR | AI (GPT-4o mini) | podkategoria: urlop / benefity / inne |
| Utworz ticket | BambooHR API lub Google Sheets | dodaj wiersz do arkusza `HR_Requests` |
| Powiadom HR | Email do hr@firma.pl | z danymi zglaszajacego i podsumowaniem AI |
| Zwroc output | Set node | `status: queued`, `assigned_to: hr@firma.pl` |

**Input przyklad:**
```json
{
  "ticket_id": "TKT-2026-b7c1d4",
  "category": "HR",
  "priority": "low",
  "requester": { "name": "Piotr Wisniewski", "email": "piotr@firma.pl", "department": "Sales" },
  "request": { "subject": "Wniosek urlopowy — 5 dni", "body": "Prosze o urlop 21-25 kwietnia 2026." },
  "ai_summary": "Pracownik wnioskuje o 5 dni urlopu w dniach 21-25 kwietnia."
}
```

**Output przyklad:**
```json
{
  "ticket_id": "TKT-2026-b7c1d4",
  "category": "HR",
  "status": "queued",
  "external_ticket_id": "HR-2026-0342",
  "assigned_to": "hr@firma.pl",
  "estimated_response_time": "1-2 dni robocze",
  "confirmation_message": "Twoj wniosek HR-2026-0342 zostal przekazany do dzialu HR. Odpowiedz w ciagu 1-2 dni roboczych.",
  "processed_at": "2026-04-15T10:12:00Z"
}
```

---

### SW-Finance: Finance Requests

**Wyzwalacz:** `Execute Workflow Trigger`

| Etap | Akcja | Konfiguracja |
|---|---|---|
| Przyjmij input | Execute Workflow Trigger | pobierz `$json` |
| Log do Sheets | Google Sheets | arkusz `Finance_Requests`: ticket_id, nadawca, kwota (jesli podana), opis |
| Powiadom CFO | Email do cfo@firma.pl | jesli `priority = high/critical` |
| Powiadom ksiegowosc | Email do finance@firma.pl | zawsze |
| Zwroc output | Set node | `status: queued`, `assigned_to: finance@firma.pl` |

**Input przyklad:**
```json
{
  "ticket_id": "TKT-2026-c5e8f1",
  "category": "Finance",
  "priority": "medium",
  "requester": { "name": "Marta Kowalczyk", "email": "marta@firma.pl", "department": "Operations" },
  "request": { "subject": "Korekta faktury FV/2026/0412", "body": "Proszę o korekte faktury — bledna kwota VAT. Prawidlowa to 23%, naliczono 8%." },
  "ai_summary": "Zgloszenie dotyczace korekty stawki VAT na fakturze FV/2026/0412."
}
```

**Output przyklad:**
```json
{
  "ticket_id": "TKT-2026-c5e8f1",
  "category": "Finance",
  "status": "queued",
  "external_ticket_id": "FIN-2026-0089",
  "assigned_to": "finance@firma.pl",
  "estimated_response_time": "3 dni robocze",
  "confirmation_message": "Zgloszenie FIN-2026-0089 przyjete przez ksiegowosc. Odpowiedz w ciagu 3 dni roboczych.",
  "processed_at": "2026-04-15T11:05:00Z"
}
```

---

### SW-Sales: Sales Support

**Wyzwalacz:** `Execute Workflow Trigger`

| Etap | Akcja | Konfiguracja |
|---|---|---|
| Przyjmij input | Execute Workflow Trigger | pobierz `$json` |
| Dodaj opportunity | CRM (HubSpot / Pipedrive API) | lub Google Sheets jesli brak CRM |
| Powiadom handlowca | Slack `#sales` | mention `@sales-lead` jezeli nowy lead |
| Autoresponse AI | GPT-4o mini | wygeneruj wstepna odpowiedz dla klienta (opcjonalnie) |
| Zwroc output | Set node | `status: created`, `assigned_to: sales@firma.pl` |

**Input przyklad:**
```json
{
  "ticket_id": "TKT-2026-d2a7b9",
  "category": "Sales",
  "priority": "high",
  "requester": { "name": "Tomasz Zielinski", "email": "tomasz@kontrahent.pl", "department": "External" },
  "request": { "subject": "Zapytanie ofertowe — wdrozenie AI", "body": "Dzien dobry, jestesmy firma 200os. Szukamy partnera do wdrozenia AI w dziale obslugi klienta. Prosze o kontakt." },
  "ai_summary": "Zewnetrzny klient pyta o oferte na wdrozenie AI dla firmy 200-osobowej."
}
```

**Output przyklad:**
```json
{
  "ticket_id": "TKT-2026-d2a7b9",
  "category": "Sales",
  "status": "created",
  "external_ticket_id": "CRM-OPP-8821",
  "assigned_to": "kacper@dokodu.it",
  "estimated_response_time": "24h",
  "confirmation_message": "Dziekujemy za zapytanie! Nasz specjalista skontaktuje sie z Panstwem w ciagu 24h. Numer referencyjny: TKT-2026-d2a7b9.",
  "processed_at": "2026-04-15T12:30:00Z"
}
```

---

### SW-Other: Human Queue

**Wyzwalacz:** `Execute Workflow Trigger`

| Etap | Akcja | Konfiguracja |
|---|---|---|
| Przyjmij input | Execute Workflow Trigger | pobierz `$json` |
| Dodaj do kolejki | Google Sheets | arkusz `Human_Queue`: ticket_id, tresc, status `PENDING` |
| Powiadom managera | Email do manager@firma.pl | + podsumowanie AI |
| Zwroc output | Set node | `status: queued`, `assigned_to: manager@firma.pl` |

> Uwaga: ta sciezka sluzy jako "safety net" dla zglaszen, ktorych AI nie potrafi zakwalifikowac lub ktore wymagaja ludzkiej decyzji.

**Input przyklad:**
```json
{
  "ticket_id": "TKT-2026-e6f0c3",
  "category": "Other",
  "priority": "medium",
  "requester": { "name": "Karolina Maj", "email": "karolina@firma.pl", "department": "Legal" },
  "request": { "subject": "Pytanie o compliance AI Act", "body": "Chcialam zapytac jaki jest nasz status pod AI Act — czy nasze narzedzia sa sklasyfikowane?" },
  "ai_summary": "Pytanie prawne dotyczace zgodnosci z AI Act — wymaga oceny specjalisty."
}
```

**Output przyklad:**
```json
{
  "ticket_id": "TKT-2026-e6f0c3",
  "category": "Other",
  "status": "queued",
  "external_ticket_id": "OTH-2026-0031",
  "assigned_to": "manager@firma.pl",
  "estimated_response_time": "2-3 dni robocze",
  "confirmation_message": "Twoje zgloszenie OTH-2026-0031 zostalo przekazane do odpowiedniej osoby. Odpowiedz w ciagu 2-3 dni roboczych.",
  "processed_at": "2026-04-15T14:00:00Z"
}
```

---

## 5. Uwagi Implementacyjne

- **ticket_id** generuj w Master Workflow (Code node lub Set) przez `crypto.randomUUID()` lub format `TKT-{rok}-{random hex 6 znakow}` — przed wywolaniem subworkflow
- **Subworkflows jako odrebne workflow** — w n8n stwórz 5 osobnych workflow z `Execute Workflow Trigger` jako pierwszym nodem. Latwo je testowac, wdrazac i wersjonowac niezaleznie
- **Wait for output = true** — koniecznie wlacz w Execute Workflow nodes, inaczej Master nie poczeka na wynik i Merge nie bedzie miec danych
- **AI Classification** — GPT-4o mini to dobry wybor: szybki, tani (~0.0001 USD/request), wystarczajaco precyzyjny przy prostej klasyfikacji. Przy wiekszej skali warto fine-tuneowac
- **Fallback** — zawsze wlacz fallback w Switch (output "Other"), zeby zadne zgloszenie nie "zginelo" przez brak matchujacego warunku
- **Monitoring** — dodaj licznik w Google Sheets (ile zglaszen dziennie, per kategoria) — to pozwoli optymalizowac routing i identyfikowac przeciazone dzialy
- **Wersjonowanie** — uzyj n8n Tags (`v1.0`, `production`, `staging`) do oznaczania wersji subworkflow; nigdy nie modyfikuj live workflow bez testow na kopii
