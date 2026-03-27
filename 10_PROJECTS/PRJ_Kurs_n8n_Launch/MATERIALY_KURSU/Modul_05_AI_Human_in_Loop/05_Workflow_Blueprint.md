---
type: course-material
module: "05 — AI + Human-in-the-Loop"
topic: Slack Approval Bot
author: Kacper Sieradzinski / Dokodu
last_reviewed: 2026-03-27
tags: [n8n, slack, human-in-the-loop, approval, ai-agent, webhook]
---

# Blueprint: Slack Approval Bot

## Cel i kontekst

Automatyzacja, która zanim wykona działanie (np. wysłanie oferty, usunięcie rekordu, wdrożenie zmiany), prosi człowieka o zatwierdzenie bezpośrednio w Slacku. AI interpretuje żądanie i proponuje konkretną akcję — człowiek klika "Zatwierdź" lub "Anuluj" bez konieczności wchodzenia w żaden system.

**Przykład zastosowania:** pracownik pisze do bota `@approvalbot wyślij ofertę do klienta ABC na 12 000 PLN`. Bot interpretuje intencję, formatuje wiadomość do menedżera z przyciskami i czeka na decyzję.

---

## Architektura: 3 powiązane workflows

```
┌─────────────────────────────────────────────────────────────┐
│  WORKFLOW 1: Listener                                        │
│  Slack Event → AI Agent → wywołuje Workflow 2               │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  WORKFLOW 2: Approval Sender                                 │
│  Formatuje wiadomość Slack z przyciskami → Wait Node        │
└─────────────────────────────────────────────────────────────┘
                          │
              (callback po kliknięciu przycisku)
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  WORKFLOW 3: Approval Handler                               │
│  Przyjmuje callback → Wykonaj / Anuluj → Powiadom           │
└─────────────────────────────────────────────────────────────┘
```

---

## Workflow 1: Listener

### Węzły w kolejności

| # | Węzeł | Typ | Opis |
|---|-------|-----|------|
| 1 | Slack Trigger | Trigger | Nasłuchuje `app_mention` events |
| 2 | Normalize Input | Set | Wyciąga `text`, `user`, `channel`, `ts` |
| 3 | AI Agent | LangChain Agent | Interpretuje intencję, ustala akcję |
| 4 | Route Decision | IF | Czy akcja wymaga zatwierdzenia? |
| 5 | Execute Workflow | Execute Workflow | Wywołuje Workflow 2 z danymi |
| 6 | Auto-Execute | HTTP Request | Dla akcji niewymagających zgody |

### Konfiguracja węzła Slack Trigger

```
Event: app_mention
Bot Token: {{ $env.SLACK_BOT_TOKEN }}
```

### Dane przekazywane do Workflow 2

```json
{
  "request_id": "{{ $now.toISO() }}-{{ $randomString(8) }}",
  "requester_slack_id": "U0123456789",
  "requester_name": "Jan Kowalski",
  "channel_id": "C0987654321",
  "original_message": "wyślij ofertę do klienta ABC na 12 000 PLN",
  "proposed_action": {
    "type": "send_offer",
    "params": {
      "client_name": "ABC Sp. z o.o.",
      "amount_pln": 12000,
      "template": "standard_offer_v2"
    }
  },
  "approver_slack_id": "U0000000001",
  "timeout_hours": 24
}
```

---

## Workflow 2: Approval Sender

### Węzły w kolejności

| # | Węzeł | Typ | Opis |
|---|-------|-----|------|
| 1 | Webhook (wejście) | Webhook | Odbiera dane z Workflow 1 |
| 2 | Format Message | Set | Buduje Block Kit payload |
| 3 | Send DM to Approver | Slack | Wysyła wiadomość z przyciskami |
| 4 | Wait Node | Wait | Czeka na callback (max 24h) |
| 5 | Handle Timeout | Set | Jeśli brak odpowiedzi → "TIMEOUT" |
| 6 | Respond to Workflow | Respond to Webhook | Zwraca wynik do Workflow 1 |

### Konfiguracja Wait Node

```
Resume: On Webhook Call
Webhook URL: https://twoja-instancja.n8n.io/webhook/approval-callback/{{ $json.request_id }}
Timeout: 24 hours
On Timeout: Continue (z wartością "TIMEOUT")
```

**Ważne:** URL webhooka Wait Node jest dynamiczny — każda instancja zatwierdzenia ma unikatowy URL z `request_id`. Ten URL trafia do wiadomości Slack jako `value` przycisków.

### Block Kit payload — wiadomość z przyciskami

```json
{
  "channel": "{{ $json.approver_slack_id }}",
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "Prośba o zatwierdzenie akcji"
      }
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*Zgłaszający:*\n<@{{ $json.requester_slack_id }}>"
        },
        {
          "type": "mrkdwn",
          "text": "*Akcja:*\nWysyłka oferty"
        },
        {
          "type": "mrkdwn",
          "text": "*Klient:*\nABC Sp. z o.o."
        },
        {
          "type": "mrkdwn",
          "text": "*Kwota:*\n12 000 PLN"
        }
      ]
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Oryginalna wiadomość:*\n_{{ $json.original_message }}_"
      }
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": {
            "type": "plain_text",
            "text": "Zatwierdz"
          },
          "style": "primary",
          "value": "APPROVED",
          "action_id": "approval_yes",
          "url": "{{ $json.wait_webhook_url }}?decision=APPROVED"
        },
        {
          "type": "button",
          "text": {
            "type": "plain_text",
            "text": "Anuluj"
          },
          "style": "danger",
          "value": "REJECTED",
          "action_id": "approval_no",
          "url": "{{ $json.wait_webhook_url }}?decision=REJECTED"
        }
      ]
    },
    {
      "type": "context",
      "elements": [
        {
          "type": "mrkdwn",
          "text": "Prośba wygasa za 24 godziny ({{ $json.expires_at }}) | ID: `{{ $json.request_id }}`"
        }
      ]
    }
  ]
}
```

---

## Workflow 3: Approval Handler

### Węzły w kolejności

| # | Węzeł | Typ | Opis |
|---|-------|-----|------|
| 1 | Webhook | Webhook | Odbiera callback z przycisku Slack |
| 2 | Parse Decision | Set | Wyciąga `decision` i `request_id` |
| 3 | Route | Switch | APPROVED / REJECTED / TIMEOUT |
| 4a | Execute Action | HTTP Request | Wywołuje właściwą akcję (send_offer) |
| 4b | Log Rejection | Set | Rejestruje odmowę |
| 4c | Log Timeout | Set | Rejestruje brak odpowiedzi |
| 5 | Notify Requester | Slack | Informuje osobę zgłaszającą o wyniku |
| 6 | Update Audit Log | Google Sheets / Airtable | Zapis do rejestru decyzji |

### Payload callback z Slack

Gdy użytkownik kliknie przycisk, Slack wysyła POST na URL webhooka:

```json
{
  "type": "block_actions",
  "user": {
    "id": "U0000000001",
    "username": "anna.nowak"
  },
  "actions": [
    {
      "action_id": "approval_yes",
      "value": "APPROVED",
      "type": "button"
    }
  ],
  "message": {
    "ts": "1710000000.000000"
  }
}
```

---

## Konfiguracja Slack App

### Wymagane OAuth Scopes (Bot Token)

| Scope | Zastosowanie |
|-------|-------------|
| `chat:write` | Wysyłanie wiadomości przez bota |
| `chat:write.public` | Wysyłanie na publiczne kanały bez dołączania |
| `channels:read` | Odczyt listy kanałów |
| `im:write` | Otwieranie DM z użytkownikami |
| `users:read` | Pobieranie profili użytkowników |
| `commands` | Opcjonalnie: slash commands |

### Event Subscriptions

```
Enable Events: ON
Request URL: https://twoja-instancja.n8n.io/webhook/slack-events

Subscribe to bot events:
  - app_mention      (bot wspomniany @approvalbot)
  - message.im       (opcjonalnie: wiadomości DM do bota)
```

### Interactivity & Shortcuts

```
Interactivity: ON
Request URL: https://twoja-instancja.n8n.io/webhook/slack-interactivity
```

Ten URL odbiera zdarzenia z kliknięcia przycisków (Block Actions). W n8n: osobny Webhook node w Workflow 3.

### Weryfikacja Slack Signing Secret

W n8n, w węźle Slack Trigger lub Webhook, dodaj nagłówek weryfikacji:

```
Header Name: X-Slack-Signature
Secret: {{ $env.SLACK_SIGNING_SECRET }}
```

---

## System Prompt dla AI Agent (Workflow 1)

```
Jesteś asystentem aprobat firmowych. Interpretuj wiadomości pracowników i rozpoznaj, jaką akcję chcą wykonać.

## Twoja rola
Analizujesz wiadomości wysłane do bota @approvalbot i:
1. Identyfikujesz intencję (co chce zrobić pracownik)
2. Wyciągasz parametry akcji (klient, kwota, typ dokumentu itp.)
3. Decydujesz, czy akcja wymaga zatwierdzenia menedżera
4. Zwracasz ustrukturyzowane dane JSON

## Akcje wymagające zatwierdzenia (requires_approval: true)
- Wysyłanie ofert handlowych (kwota dowolna)
- Udzielanie rabatów > 5%
- Anulowanie zamówień
- Zmiany w danych klienta
- Wysyłanie komunikatów zewnętrznych w imieniu firmy

## Akcje niewymagające zatwierdzenia (requires_approval: false)
- Sprawdzanie statusu zamówienia
- Odczyt danych
- Generowanie raportów wewnętrznych
- Ustawianie przypomnień

## Format odpowiedzi (zawsze JSON, bez komentarzy)
{
  "intent": "nazwa_intencji",
  "requires_approval": true/false,
  "proposed_action": {
    "type": "typ_akcji",
    "description": "Opis akcji po polsku dla menedżera (1-2 zdania)",
    "params": {
      // parametry specyficzne dla akcji
    }
  },
  "approver_role": "manager" | "ceo" | "finance",
  "urgency": "normal" | "urgent",
  "confidence": 0.0-1.0,
  "clarification_needed": null | "pytanie do użytkownika jeśli brakuje danych"
}

## Przykład
Wiadomość: "wyślij ofertę do Kowalski SA na 15 tysięcy za wdrożenie n8n"
Odpowiedź:
{
  "intent": "send_offer",
  "requires_approval": true,
  "proposed_action": {
    "type": "send_offer",
    "description": "Wysłanie oferty wdrożenia n8n do firmy Kowalski SA na kwotę 15 000 PLN",
    "params": {
      "client_name": "Kowalski SA",
      "amount_pln": 15000,
      "service_type": "wdrożenie n8n",
      "template": "standard_offer_v2"
    }
  },
  "approver_role": "manager",
  "urgency": "normal",
  "confidence": 0.92,
  "clarification_needed": null
}
```

---

## Przykładowe interakcje — JSON payloads

### 1. Żądanie od pracownika (Slack Event)

```json
{
  "type": "app_mention",
  "event_id": "Ev0123456789",
  "event_time": 1710000000,
  "event": {
    "type": "app_mention",
    "user": "U0123456789",
    "text": "<@U_BOT_ID> wyślij ofertę do klienta ABC na 12 000 PLN",
    "ts": "1710000000.000000",
    "channel": "C0987654321",
    "team": "T0000000001"
  }
}
```

### 2. Wiadomość zatwierdzenia wysłana do menedżera (Slack Block Kit)

```json
{
  "channel": "U0000000001",
  "text": "Prośba o zatwierdzenie: wysyłka oferty do ABC Sp. z o.o. na 12 000 PLN",
  "blocks": [
    {
      "type": "header",
      "text": { "type": "plain_text", "text": "Prośba o zatwierdzenie akcji" }
    },
    {
      "type": "section",
      "fields": [
        { "type": "mrkdwn", "text": "*Zgłaszający:*\n<@U0123456789>" },
        { "type": "mrkdwn", "text": "*Akcja:*\nWysyłka oferty" },
        { "type": "mrkdwn", "text": "*Klient:*\nABC Sp. z o.o." },
        { "type": "mrkdwn", "text": "*Kwota:*\n12 000 PLN" }
      ]
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": { "type": "plain_text", "text": "Zatwierdz" },
          "style": "primary",
          "value": "APPROVED",
          "action_id": "approval_yes"
        },
        {
          "type": "button",
          "text": { "type": "plain_text", "text": "Anuluj" },
          "style": "danger",
          "value": "REJECTED",
          "action_id": "approval_no"
        }
      ]
    }
  ]
}
```

### 3. Callback po kliknięciu "Zatwierdz" (Slack → n8n Webhook)

```json
{
  "type": "block_actions",
  "team": { "id": "T0000000001", "domain": "twoja-firma" },
  "user": {
    "id": "U0000000001",
    "username": "anna.nowak",
    "name": "Anna Nowak"
  },
  "api_app_id": "A0000000001",
  "token": "verification_token_here",
  "trigger_id": "13345224609.738474920.8088930838d88f008e0",
  "channel": { "id": "D0000000001" },
  "message": {
    "type": "message",
    "ts": "1710000000.000000",
    "text": "Prośba o zatwierdzenie akcji"
  },
  "actions": [
    {
      "action_id": "approval_yes",
      "block_id": "actions_block",
      "action_ts": "1710000005.000000",
      "type": "button",
      "value": "APPROVED",
      "style": "primary"
    }
  ],
  "response_url": "https://hooks.slack.com/actions/T00000000/0000000/xxxx"
}
```

---

## Konfiguracja Wait Node — szczegóły

### Ustawienia w n8n

```
Node Type: Wait
Resume: On Webhook Call

Webhook URL: automatycznie generowany
Format: https://<twoja-instancja>/webhook-waiting/<workflow-id>/<execution-id>

Limit Wait Time: ON
Limit Type: After time interval
After: 24 Hours

On Timeout: Continue workflow
  (dane wyjściowe będą miały pustą wartość — obsłuż w węźle IF)
```

### Jak działa Wait Node z dynamicznym URL

1. Workflow 2 startuje → Wait Node generuje unikalny URL dla tej konkretnej egzekucji
2. URL jest wstrzykiwany do wiadomości Slack (w przyciskach lub jako link)
3. Workflow 2 "zasypia" i zwalnia zasoby serwera
4. Gdy menedżer klika przycisk → Slack wysyła GET/POST na ten URL
5. n8n budzi egzekucję i kontynuuje od węzła po Wait Node

```javascript
// Jak wyciągnąć URL Wait Node w Code Node
const waitUrl = $execution.resumeUrl;
// Zapisz do zmiennej i użyj w bloku Slack
```

---

## Zmienne środowiskowe (n8n Environment)

```
SLACK_BOT_TOKEN=xoxb-xxx-xxx-xxx
SLACK_SIGNING_SECRET=xxxxxxxxxxxxxxxxxxxxxxxx
SLACK_APPROVER_USER_ID=U0000000001
OPENAI_API_KEY=sk-xxx
```

---

## Wskazówki implementacyjne

1. **Testuj najpierw Workflow 3** — możesz ręcznie wysłać payload do webhooka i sprawdzić, czy akcje są wykonywane poprawnie.
2. **Wait Node URL jest jednorazowy** — po odebraniu callback lub timeout URL wygasa. Nie można go użyć ponownie.
3. **Slack URL buttons vs interactivity** — prostsze podejście to użycie `url` w przycisku (otwiera link, nie wysyła interactivity payload). Zaawansowane podejście: włącz Interactivity i odbieraj POST z pełnym payloadem.
4. **Audit log** — zawsze zapisuj decyzje (kto, co, kiedy, jaka decyzja) do arkusza lub bazy danych.
5. **Escalation** — jeśli menedżer nie odpowie po 20h, wyślij reminder. Drugi timeout po 24h = automatyczna odmowa.
