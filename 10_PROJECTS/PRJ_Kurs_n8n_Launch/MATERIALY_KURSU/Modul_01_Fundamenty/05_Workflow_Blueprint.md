---
type: blueprint
module: "01 — Fundamenty n8n"
title: "Lead Capture System"
difficulty: beginner
estimated_time: 45 min
author: Kacper Sieradziński / Dokodu
last_reviewed: 2026-03-27
tags: [n8n, webhook, google-sheets, gmail, slack, lead-capture, walidacja, duplikaty]
---

# Blueprint 05 — Lead Capture System

> Automatyczny system przechwytywania leadów z formularza WWW: walidacja, deduplicacja, zapis do arkusza, email powitalny i powiadomienie zespołu.

---

## Architektura workflow (ASCII)

```
                         ┌──────────────────────────┐
                         │   Webhook Trigger (POST)  │
                         │   /webhook/lead           │
                         └────────────┬─────────────┘
                                      │
                         ┌────────────▼─────────────┐
                         │  IF — Walidacja email     │
                         │  (regex: RFC 5322)        │
                         └────────┬────────┬─────────┘
                                  │        │
                              TRUE│        │FALSE
                                  │        │
              ┌───────────────────▼┐      ┌▼──────────────────────┐
              │ Google Sheets      │      │ Gmail — błąd admina   │
              │ Sprawdź duplikat   │      │ "Błędny email w leadzie"│
              │ (VLOOKUP po email) │      └──────────┬────────────┘
              └──────────┬─────────┘                 │
                         │                ┌──────────▼────────────┐
              ┌──────────▼─────────┐      │ Respond — błąd 400    │
              │ IF — Duplikat?     │      │ { "error": "..." }    │
              │ (dane znalezione?) │      └───────────────────────┘
              └───┬────────────┬───┘
                  │            │
              TRUE│            │FALSE
                  │            │
  ┌───────────────▼┐          ┌▼────────────────────┐
  │ Respond — info │          │ Google Sheets        │
  │ "already exists"│         │ Zapisz nowy lead     │
  └────────────────┘          │ (Append Row)         │
                              └──────────┬───────────┘
                                         │
                              ┌──────────▼───────────┐
                              │ Gmail                 │
                              │ Wyślij email powitalny│
                              │ (template + name)     │
                              └──────────┬────────────┘
                                         │
                              ┌──────────▼───────────┐
                              │ Slack                 │
                              │ Powiadom #leady       │
                              │ (link do Sheets)      │
                              └──────────┬────────────┘
                                         │
                              ┌──────────▼───────────┐
                              │ Respond to Webhook    │
                              │ { "status": "ok" }    │
                              └──────────────────────┘
```

---

## Lista nodes z konfiguracją

### Node 1 — Webhook Trigger

| Parametr | Wartość |
|---|---|
| **Typ** | Webhook |
| **Nazwa** | `Webhook — Nowy Lead` |
| **HTTP Method** | POST |
| **Path** | `lead` |
| **Respond** | Immediately |
| **Response Code** | 200 |
| **Authentication** | None (lub Header Auth w produkcji) |

> Pełny URL produkcyjny: `https://<twoja-domena>/webhook/lead`
> URL testowy (n8n Cloud): `https://<workspace>.app.n8n.cloud/webhook-test/lead`

---

### Node 2 — IF: Walidacja email

| Parametr | Wartość |
|---|---|
| **Typ** | IF |
| **Nazwa** | `IF — Walidacja email` |
| **Condition type** | String |
| **Value 1** | `{{ $json.email }}` |
| **Operation** | Matches Regex |
| **Value 2** | `^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$` |

**Gałęzie:**
- `TRUE` → Google Sheets (sprawdź duplikat)
- `FALSE` → Gmail do admina + Respond 400

---

### Node 3 — Google Sheets: Sprawdź duplikat

| Parametr | Wartość |
|---|---|
| **Typ** | Google Sheets |
| **Nazwa** | `Sheets — Sprawdź duplikat` |
| **Operation** | Lookup |
| **Credential** | `Google Sheets OAuth2` |
| **Spreadsheet ID** | `{{ $env.LEADS_SHEET_ID }}` |
| **Sheet Name** | `Leady` |
| **Lookup Column** | `Email` |
| **Lookup Value** | `{{ $json.email }}` |
| **Return All Matches** | false |
| **Options → Continue If Empty** | true |

> Jeśli rekord istnieje — node zwraca dane wiersza. Jeśli brak — zwraca pustą tablicę `[]`.

---

### Node 4 — IF: Duplikat?

| Parametr | Wartość |
|---|---|
| **Typ** | IF |
| **Nazwa** | `IF — Duplikat?` |
| **Condition type** | Array |
| **Value 1** | `{{ $json }}` |
| **Operation** | Is Not Empty |

**Gałęzie:**
- `TRUE` (rekord znaleziony) → Respond "already exists"
- `FALSE` (brak rekordu) → Google Sheets Append

---

### Node 5 — Google Sheets: Zapisz nowy lead

| Parametr | Wartość |
|---|---|
| **Typ** | Google Sheets |
| **Nazwa** | `Sheets — Zapisz lead` |
| **Operation** | Append |
| **Credential** | `Google Sheets OAuth2` |
| **Spreadsheet ID** | `{{ $env.LEADS_SHEET_ID }}` |
| **Sheet Name** | `Leady` |
| **Mapping** | Manual |

**Mapowanie kolumn:**

| Kolumna w Sheets | Wartość n8n |
|---|---|
| `Timestamp` | `{{ $now.toISO() }}` |
| `Imię` | `{{ $('Webhook — Nowy Lead').item.json.name }}` |
| `Email` | `{{ $('Webhook — Nowy Lead').item.json.email }}` |
| `Telefon` | `{{ $('Webhook — Nowy Lead').item.json.phone }}` |
| `Źródło` | `{{ $('Webhook — Nowy Lead').item.json.source ?? 'www' }}` |
| `Status` | `Nowy` |

---

### Node 6 — Gmail: Email powitalny

| Parametr | Wartość |
|---|---|
| **Typ** | Gmail |
| **Nazwa** | `Gmail — Email powitalny` |
| **Operation** | Send |
| **Credential** | `Gmail OAuth2` |
| **To** | `{{ $('Webhook — Nowy Lead').item.json.email }}` |
| **Subject** | `Cześć {{ $('Webhook — Nowy Lead').item.json.name }}! Twoje zgłoszenie dotarło do Dokodu` |
| **Email Type** | HTML |
| **Message** | (patrz template poniżej) |

**Template wiadomości powitalnej:**

```html
<p>Cześć {{ $('Webhook — Nowy Lead').item.json.name }},</p>

<p>Dziękujemy za zainteresowanie Dokodu! Twoje zgłoszenie zostało odebrane.</p>

<p>Nasz zespół skontaktuje się z Tobą w ciągu <strong>24 godzin</strong> roboczych.</p>

<p>W międzyczasie zapraszamy na naszego bloga:<br>
<a href="https://dokodu.it/blog">dokodu.it/blog</a></p>

<p>Pozdrawiamy,<br>
<strong>Kacper Sieradziński</strong><br>
CEO, Dokodu<br>
<a href="https://dokodu.it">dokodu.it</a></p>
```

---

### Node 7 — Slack: Powiadom zespół

| Parametr | Wartość |
|---|---|
| **Typ** | Slack |
| **Nazwa** | `Slack — Powiadom #leady` |
| **Operation** | Send Message |
| **Credential** | `Slack OAuth2` |
| **Channel** | `#leady` |
| **Message** | (patrz poniżej) |

**Treść wiadomości Slack:**

```
:rocket: *Nowy lead!*

*Imię:* {{ $('Webhook — Nowy Lead').item.json.name }}
*Email:* {{ $('Webhook — Nowy Lead').item.json.email }}
*Telefon:* {{ $('Webhook — Nowy Lead').item.json.phone ?? 'brak' }}
*Źródło:* {{ $('Webhook — Nowy Lead').item.json.source ?? 'www' }}
*Czas:* {{ $now.toFormat('dd.MM.yyyy HH:mm') }}

:link: <https://docs.google.com/spreadsheets/d/{{ $env.LEADS_SHEET_ID }}|Otwórz arkusz>
```

---

### Node 8 — Respond to Webhook: Sukces

| Parametr | Wartość |
|---|---|
| **Typ** | Respond to Webhook |
| **Nazwa** | `Respond — sukces` |
| **Response Code** | 200 |
| **Response Body** | JSON |

**Response JSON:**

```json
{
  "status": "ok",
  "message": "Lead zapisany pomyślnie",
  "lead_id": "{{ $('Sheets — Zapisz lead').item.json.updatedRange }}"
}
```

---

### Node 9a — Gmail: Błąd do admina (error path)

| Parametr | Wartość |
|---|---|
| **Typ** | Gmail |
| **Nazwa** | `Gmail — Błąd admina` |
| **Operation** | Send |
| **Credential** | `Gmail OAuth2` |
| **To** | `{{ $env.ADMIN_EMAIL }}` |
| **Subject** | `[n8n] Błąd walidacji leada — {{ $now.toISO() }}` |
| **Message** | `Błędne zgłoszenie z webhookiem. Email: {{ $json.email }}. Payload: {{ JSON.stringify($json) }}` |

---

### Node 9b — Respond to Webhook: Błąd

| Parametr | Wartość |
|---|---|
| **Typ** | Respond to Webhook |
| **Nazwa** | `Respond — błąd 400` |
| **Response Code** | 400 |

**Response JSON:**

```json
{
  "status": "error",
  "message": "Nieprawidłowy adres email",
  "field": "email"
}
```

---

## Przykładowy payload wejściowy

```json
{
  "name": "Anna Kowalska",
  "email": "anna.kowalska@example.com",
  "phone": "+48 601 234 567",
  "source": "landing-kurs-n8n",
  "message": "Chcę dowiedzieć się więcej o automatyzacji."
}
```

---

## Przykładowe dane wyjściowe kluczowych nodes

### Po Webhook Trigger:

```json
{
  "name": "Anna Kowalska",
  "email": "anna.kowalska@example.com",
  "phone": "+48 601 234 567",
  "source": "landing-kurs-n8n",
  "message": "Chcę dowiedzieć się więcej o automatyzacji."
}
```

### Po Google Sheets Lookup (brak duplikatu):

```json
[]
```

### Po Google Sheets Append:

```json
{
  "spreadsheetId": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms",
  "updatedRange": "Leady!A15",
  "updatedRows": 1,
  "updatedColumns": 6,
  "updatedCells": 6
}
```

### Po Gmail Send:

```json
{
  "id": "18a3c2f4d5e6b7a8",
  "threadId": "18a3c2f4d5e6b7a8",
  "labelIds": ["SENT"]
}
```

### Po Slack Send:

```json
{
  "ok": true,
  "channel": "C04ABCDEF12",
  "ts": "1711533600.123456",
  "message": {
    "type": "message",
    "text": ":rocket: *Nowy lead!*..."
  }
}
```

### Respond to Webhook — ostateczna odpowiedź:

```json
{
  "status": "ok",
  "message": "Lead zapisany pomyślnie",
  "lead_id": "Leady!A15"
}
```

---

## Zmienne środowiskowe i credentials

### Credentials (konfiguracja w n8n Settings → Credentials)

| Credential | Typ | Co skonfigurować |
|---|---|---|
| `Google Sheets OAuth2` | Google Sheets OAuth2 API | Client ID + Secret z Google Cloud Console (Sheets API v4 włączone) |
| `Gmail OAuth2` | Gmail OAuth2 API | Client ID + Secret (Gmail API włączone, scope: send) |
| `Slack OAuth2` | Slack API | Bot Token (`xoxb-...`), scope: `chat:write` |

### Zmienne środowiskowe (`.env` w instalacji n8n)

```bash
# Plik: ~/.n8n/.env  lub  /etc/n8n/.env

LEADS_SHEET_ID=1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms
ADMIN_EMAIL=kacper@dokodu.it
```

> W n8n możesz też ustawić zmienne w: **Settings → Variables** (n8n Cloud) lub przez `N8N_VARIABLES` (self-hosted).

### Struktura arkusza Google Sheets

Utwórz arkusz `Leady` z nagłówkami w wierszu 1:

| A | B | C | D | E | F |
|---|---|---|---|---|---|
| Timestamp | Imię | Email | Telefon | Źródło | Status |

---

## Instrukcja testowania

### 1. Aktywacja webhookaTest

W n8n kliknij **Test Workflow** — webhook będzie nasłuchiwał przez 2 minuty na URL testowym.

### 2. Test z poprawnym leadem (curl)

```bash
curl -X POST https://<twoja-domena>/webhook-test/lead \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Anna Kowalska",
    "email": "anna.kowalska@example.com",
    "phone": "+48 601 234 567",
    "source": "test-curl"
  }'
```

**Oczekiwana odpowiedź:**

```json
{"status": "ok", "message": "Lead zapisany pomyślnie", "lead_id": "Leady!A..."}
```

### 3. Test duplikatu

```bash
# Wyślij ten sam payload drugi raz — powinien zwrócić odpowiedź bez zapisu
curl -X POST https://<twoja-domena>/webhook-test/lead \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Anna Kowalska",
    "email": "anna.kowalska@example.com",
    "source": "test-curl"
  }'
```

### 4. Test błędnego emaila

```bash
curl -X POST https://<twoja-domena>/webhook-test/lead \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test",
    "email": "nie-to-email",
    "source": "test-curl"
  }'
```

**Oczekiwana odpowiedź (400):**

```json
{"status": "error", "message": "Nieprawidłowy adres email", "field": "email"}
```

### 5. Weryfikacja po teście

- [ ] Nowy wiersz w Google Sheets (arkusz `Leady`)
- [ ] Email powitalny w skrzynce `anna.kowalska@example.com`
- [ ] Wiadomość w kanale Slack `#leady`
- [ ] Brak duplikatu po ponownym wysłaniu tego samego emaila
- [ ] Wiadomość o błędzie do admina przy złym emailu

---

## Typowe błędy i rozwiązania

| Błąd | Przyczyna | Rozwiązanie |
|---|---|---|
| `403 Forbidden` w Sheets | Brak uprawnień do arkusza | Dodaj email konta serwisowego jako edytor arkusza |
| `Invalid grant` w Gmail | Token OAuth wygasł | Odśwież credential w n8n Settings → Credentials |
| Webhook nie odpowiada | Workflow nieaktywny | Przejdź do workflow → kliknij `Activate` (przełącznik) |
| Slack `channel_not_found` | Błędna nazwa kanału | Użyj ID kanału zamiast nazwy (`C04ABCDEF12`) |
| Sheets Lookup zwraca błąd | Brak nagłówka `Email` | Sprawdź czy wiersz 1 zawiera nagłówek "Email" (wielkość liter) |

---

## Rozszerzenia (następne kroki)

Po opanowaniu podstaw możesz rozbudować workflow o:
- **HubSpot / Pipedrive node** — sync leadu do CRM
- **AI node (OpenAI)** — kwalifikacja leadu i scoring automatyczny
- **Wait node + Follow-up** — sekwencja emailowa po 24h/72h
- **Twilio node** — SMS powitalny na numer z formularza
- **Error Trigger** — globalny handler błędów dla całego workflow
