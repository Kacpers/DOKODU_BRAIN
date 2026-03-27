---
type: blueprint
modul: "03 — Skalowalnosc i Error Handling"
lekcja: "05 — Workflow Blueprint"
projekt: PRJ_Kurs_n8n_Launch
autor: Kacper Sieradziński / Dokodu
wersja: "1.0"
data: 2026-03-27
status: gotowy
tags: [n8n, error-handling, invoice, idempotency, webhook, gmail, google-sheets, slack]
---

# Blueprint: Armored Invoicing System

> **Cel:** Automatyczne generowanie i wysyłka faktur po odebraniu zamowienia przez Webhook — z pelnym error handlingiem, idempotency check i dead letter queue.

---

## 1. Diagram ASCII

```
                        ┌──────────────────────────────┐
                        │    ZEWNETRZNY SYSTEM          │
                        │   (sklep / CRM / formularz)   │
                        └──────────────┬───────────────┘
                                       │ POST /webhook/invoice
                                       ▼
                        ┌──────────────────────────────┐
                        │   [1] Webhook Trigger          │
                        │   POST /webhook/invoice        │
                        └──────────────┬───────────────┘
                                       │
                                       ▼
                        ┌──────────────────────────────┐
                        │  [2] Code — Idempotency Check  │
                        │  hash zamowienia → sprawdz     │
                        │  w Google Sheets               │
                        └──────┬───────────────┬────────┘
                               │               │
                         NOWE  │          DUPLIKAT
                               │               │
                               │               ▼
                               │   ┌───────────────────────┐
                               │   │  [7] Sheets — log skip │
                               │   │  status: DUPLICATE     │
                               │   └───────────────────────┘
                               ▼
                  ┌─────────────────────────────┐
                  │  [3] SplitInBatches          │
                  │  (dla list zamowien, batch=1)│
                  └──────────────┬──────────────┘
                                 │
                                 ▼
                  ┌─────────────────────────────┐
                  │  [4] HTTP Request            │
                  │  API fakturowe               │
                  │  retry: 3x, interval: 2s     │
                  │  (exponential backoff)        │
                  └──────┬──────────────┬────────┘
                         │              │
                   200 OK│        ERROR │ (po 3 retries)
                         │              │
                         ▼              ▼
          ┌──────────────────┐  ┌───────────────────────────┐
          │  [5] IF — sukces? │  │  [8] Error Trigger        │
          └──────┬───────────┘  │  Workflow (globalny)       │
                 │              │  → dead letter queue        │
          SUKCES │   BLAD       │  → Slack admin alert        │
                 │     │        └───────────────────────────┘
                 │     ▼
                 │  ┌──────────────────────────────┐
                 │  │  [9] Slack — alert dla admina │
                 │  │  kanal: #faktury-bledy         │
                 │  └──────────────────────────────┘
                 ▼
  ┌──────────────────────────────────┐
  │  [6] Gmail — wyslij fakture      │
  │  do klienta (retry: 2x)          │
  └──────────────┬───────────────────┘
                 │
    SUKCES EMAIL │     BLAD EMAIL
                 │          │
                 │          ▼
                 │  ┌──────────────────────────────┐
                 │  │  [9] Slack — alert admina     │
                 │  │  "Blad wysylki email"          │
                 │  └──────────────────────────────┘
                 ▼
  ┌──────────────────────────────────┐
  │  [7] Google Sheets               │
  │  aktualizuj status → SENT        │
  └──────────────────────────────────┘
```

---

## 2. Error Handling Matrix

| Typ bledu | Co sie dzieje | Alert |
|---|---|---|
| **API timeout** (fakturowe API nie odpowiada) | Retry 3x z exponential backoff (2s → 4s → 8s). Po 3 probach: Error Trigger | Slack `#faktury-bledy`: "API fakturowe nie odpowiada — zamowienie X w kolejce" |
| **Zduplikowane zamowienie** (ten sam hash w Sheets) | Skip — workflow konczy bez wykonania akcji, log w Sheets jako `DUPLICATE` | Brak alertu. Log w Sheets: status `DUPLICATE`, timestamp |
| **Blad wysylki emaila** (Gmail error) | Retry 2x z opoznieniem 5s. Po 2 probach: Slack admin alert + status `EMAIL_FAILED` w Sheets | Slack `#faktury-bledy`: "Nie mozna wyslac faktury do {email klienta} — zamowienie {ID}" |
| **Nieznany blad** (nieoczekiwany wyjatek) | Error Trigger Workflow przejmuje kontrole → wrzuca do dead letter queue (Sheets: arkusz `DEAD_LETTERS`) | Slack `#faktury-bledy` (priorytet HIGH): "UNKNOWN ERROR — wymagana reczna interwencja. Dane: {JSON}" |

---

## 3. Lista Nodes z Konfiguracja

### [1] Webhook Trigger

```
Node type:   n8n-nodes-base.webhook
HTTP Method: POST
Path:        /webhook/invoice
Auth:        Header Auth (X-Webhook-Secret)
Response:    "Immediately" — zwraca 200 OK natychmiast
```

Webhook zwraca odpowiedz natychmiast (nie czeka na zakonczenie workflow), zeby zewnetrzny system nie timeoutal.

---

### [2] Code — Idempotency Check

```
Node type:   n8n-nodes-base.code
Language:    JavaScript
```

Logika: oblicz hash zamowienia → sprawdz czy juz istnieje w Google Sheets → jezeli tak: zwroc flage `duplicate: true`.

Pelny snippet — patrz Sekcja 5.

---

### [3] SplitInBatches

```
Node type:    n8n-nodes-base.splitInBatches
Batch Size:   1
Reset:        false
```

Uzywany gdy Webhook dostarcza tablice zamowien (`orders: [...]`). Przy pojedynczym zamowieniu mozna polaczyc z [2] bez tego node.

---

### [4] HTTP Request — API fakturowe

```
Node type:      n8n-nodes-base.httpRequest
Method:         POST
URL:            {{ $env.INVOICE_API_URL }}/invoices
Auth:           Bearer Token (z n8n Credentials)

Body (JSON):
{
  "order_id":    "{{ $json.order_id }}",
  "customer":    "{{ $json.customer }}",
  "items":       "{{ $json.items }}",
  "amount":      "{{ $json.amount }}",
  "currency":    "PLN"
}

Retry on Fail:  true
Max Tries:      3
Wait Between:   2000 ms
Backoff:        Exponential (wlacz "Exponential backoff")
```

---

### [5] IF — sukces/blad?

```
Node type:   n8n-nodes-base.if
Condition:   {{ $json.status }} equals "success"
             OR
             {{ $response.statusCode }} equals 200
```

- **True** → przejdz do [6] Gmail
- **False** → przejdz do [9] Slack alert

---

### [6] Gmail — wyslij fakture klientowi

```
Node type:     n8n-nodes-base.gmail
Operation:     Send Email
To:            {{ $json.customer.email }}
Subject:       Faktura {{ $json.invoice_number }} — zamowienie {{ $json.order_id }}
Body:          HTML z linkiem do PDF faktury
Attachments:   {{ $json.invoice_pdf_url }} (opcjonalnie pobierz i zalacz)

Retry on Fail: true
Max Tries:     2
Wait Between:  5000 ms
```

---

### [7] Google Sheets — aktualizuj status

```
Node type:    n8n-nodes-base.googleSheets
Operation:    Update Row
Spreadsheet:  {{ $env.INVOICES_SHEET_ID }}
Sheet:        Faktury
Match Column: order_id
Update:
  - status:        SENT / DUPLICATE / EMAIL_FAILED
  - invoice_id:    {{ $json.invoice_id }}
  - sent_at:       {{ $now.toISO() }}
  - invoice_url:   {{ $json.invoice_url }}
```

---

### [8] Error Trigger Workflow — globalny handler

```
Node type:     n8n-nodes-base.errorTrigger
```

Osobny workflow (np. `WF_Error_Handler`) ustawiony jako "Error Workflow" w ustawieniach glownego workflow (`Settings → Error Workflow`).

Handler wykonuje:
1. Loguje blad do Sheets (arkusz `DEAD_LETTERS`): timestamp, workflow name, node name, error message, input JSON
2. Wyslij Slack alert do `#faktury-bledy` (priorytet HIGH)
3. Opcjonalnie: wyslij email do admin@dokodu.it

---

### [9] Slack — alert dla admina

```
Node type:   n8n-nodes-base.slack
Operation:   Post Message
Channel:     #faktury-bledy
Text:        :rotating_light: *Blad fakturowania*
             Zamowienie: {{ $json.order_id }}
             Blad: {{ $json.error.message }}
             Czas: {{ $now.toFormat('yyyy-MM-dd HH:mm') }}
             Dane: {{ JSON.stringify($json, null, 2) }}
```

---

## 4. Przykladowy Payload Zamowienia

```json
{
  "order_id": "ORD-2026-04891",
  "customer": {
    "name": "Jan Kowalski",
    "email": "jan.kowalski@firma.pl",
    "company": "Firma Kowalski Sp. z o.o.",
    "nip": "1234567890",
    "address": {
      "street": "ul. Przykładowa 12",
      "city": "Warszawa",
      "zip": "00-001",
      "country": "PL"
    }
  },
  "items": [
    {
      "name": "Kurs n8n + AI — Pakiet Pro",
      "quantity": 1,
      "unit_price": 1497.00,
      "vat_rate": 23,
      "vat_amount": 344.31,
      "gross": 1841.31
    }
  ],
  "amount": {
    "net": 1497.00,
    "vat": 344.31,
    "gross": 1841.31,
    "currency": "PLN"
  },
  "payment_method": "card",
  "payment_status": "paid",
  "ordered_at": "2026-04-15T09:23:11Z",
  "source": "website"
}
```

---

## 5. Code Snippet: Idempotency Check

```javascript
// Node: [2] Code — Idempotency Check
// Cel: sprawdz czy zamowienie bylo juz przetworzone (ochrona przed duplikatami)

const crypto = require('crypto');

// Pobierz dane zamowienia
const order = $input.first().json;

// Wygeneruj deterministyczny hash zamowienia
// Uzywamy order_id + amount + customer.email jako klucza
const hashInput = `${order.order_id}:${order.amount.gross}:${order.customer.email}`;
const orderHash = crypto
  .createHash('sha256')
  .update(hashInput)
  .digest('hex')
  .substring(0, 16); // skrocony hash do 16 znakow

// Pobierz liste przetworzonych haszy z Google Sheets
// (poprzedni node powinien zaladowac dane z arkusza)
const processedHashes = $('Google Sheets - Get Processed').all()
  .map(item => item.json.order_hash);

// Sprawdz czy hash juz istnieje
const isDuplicate = processedHashes.includes(orderHash);

// Zwroc wzbogacone dane
return [{
  json: {
    ...order,
    _meta: {
      order_hash: orderHash,
      is_duplicate: isDuplicate,
      checked_at: new Date().toISOString(),
    }
  }
}];
```

**Jak uzyc w workflow:**

1. Przed tym node dodaj `Google Sheets — Get All Rows` z arkusza `Faktury` (kolumna `order_hash`)
2. Podlacz wynik do powyzszego Code node
3. Po Code node dodaj `IF` sprawdzajacy `{{ $json._meta.is_duplicate }}`:
   - **true** → `Google Sheets — log DUPLICATE` → END
   - **false** → kontynuuj do `SplitInBatches`

---

## 6. Uwagi Implementacyjne

- **Zmienne srodowiskowe** (`$env.INVOICE_API_URL`, `$env.INVOICES_SHEET_ID`) — ustaw w `n8n Settings → Environment Variables` lub przez `.env` w Docker Compose
- **Credentials** — wszystkie tokeny i klucze API trzymaj w `n8n Credentials`, nie hardkoduj w nodach
- **Webhook Secret** — dodaj naglowek `X-Webhook-Secret` i weryfikuj go w pierwszym Code node przed przetwarzaniem
- **Rate limiting** — jezeli API fakturowe ma limity, dodaj `Wait` node miedzy batch iteracjami
- **Monitorowanie** — wlacz `Execution Data` w ustawieniach workflow; przechowuj ostatnie 100 wykonan do debugowania
