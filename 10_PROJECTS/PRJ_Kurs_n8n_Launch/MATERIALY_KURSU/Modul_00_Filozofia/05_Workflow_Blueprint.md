---
type: kurs-material
module: "00 — Filozofia Automatyzacji"
status: ready
owner: Kacper Sieradziński
last_reviewed: 2026-03-27
tags: [n8n, workflow, blueprint, webhook, gmail, demo]
---

# Moduł 0: Blueprint Workflow — "Hello Automation: Email Powitalny"

> **Cel dydaktyczny:** Pokazać uczestnikom kompletny, działający workflow od trigerowania przez HTTP do wysłania spersonalizowanego emaila. Każdy node ma jasną rolę — to fundament wzorca, który będzie się powtarzał przez cały kurs.
>
> **Czas omawiania na nagraniu:** 12–15 minut
>
> **Poziom:** Beginner

---

## Diagram ASCII — Przepływ Danych

```
                        ┌─────────────────────────────────────┐
  HTTP POST             │                                     │
  /webhook/hello  ──►   │   [1] WEBHOOK TRIGGER               │
  application/json      │   Nasłuchuje na żądania POST        │
                        │   Path: hello-automation            │
                        └────────────────┬────────────────────┘
                                         │
                                         │  { name, email, source }
                                         ▼
                        ┌─────────────────────────────────────┐
                        │                                     │
                        │   [2] IF — Walidacja email          │
                        │   Sprawdza czy email zawiera "@"    │
                        │                                     │
                        └────────────┬────────────┬───────────┘
                                     │            │
                              TRUE   │            │  FALSE
                    (email jest OK)  │            │  (email niepoprawny)
                                     ▼            ▼
                        ┌────────────────┐    ┌───────────────────────┐
                        │                │    │                       │
                        │  [3] SET DATA  │    │  [4] SET ERROR MSG    │
                        │  Przygotowanie │    │  Odpowiedź z błędem   │
                        │  danych emaila │    │  (brak dalszych       │
                        │                │    │   akcji)              │
                        └───────┬────────┘    └───────────────────────┘
                                │
                                │  { recipientName, recipientEmail,
                                │    subject, body, timestamp }
                                ▼
                        ┌─────────────────────────────────────┐
                        │                                     │
                        │   [5] GMAIL — SEND MESSAGE          │
                        │   Wysyłka spersonalizowanego emaila │
                        │   OAuth2: konto Gmail               │
                        │                                     │
                        └─────────────────────────────────────┘
```

**Legenda:**
- `►` — przepływ danych (strzałka połączenia)
- `[N]` — numer node na canvasie
- `TRUE/FALSE` — gałęzie warunkowe node'a IF

---

## Node 1: Webhook Trigger

**Typ node:** `n8n-nodes-base.webhook`

**Rola:** Punkt wejścia workflow — odbiera dane z zewnętrznego systemu przez HTTP.

### Konfiguracja

| Pole | Wartość |
| :--- | :--- |
| HTTP Method | `POST` |
| Path | `hello-automation` |
| Response Mode | `Last Node` |
| Authentication | `None` (dla demo) |

### Wynikowy URL (Production)
```
http://localhost:5678/webhook/hello-automation
```

### Wynikowy URL (Test / Listen mode)
```
http://localhost:5678/webhook-test/hello-automation
```

### Output — dane wychodzące z node'a

```json
{
  "headers": {
    "content-type": "application/json",
    "user-agent": "curl/7.81.0",
    "accept": "*/*"
  },
  "params": {},
  "query": {},
  "body": {
    "name": "Anna Kowalska",
    "email": "anna@firma.pl",
    "source": "strona-kontaktowa"
  },
  "webhookUrl": "http://localhost:5678/webhook/hello-automation",
  "executionMode": "production"
}
```

> **Uwaga:** W trybie testowym (`webhook-test`) dane wchodzą identycznie, ale n8n nie czeka na drugą stronę — odpowiada natychmiast po odbiorze. W trybie produkcyjnym odpowiedź wraca po zakończeniu całego workflow (przez `Response Mode: Last Node`).

---

## Node 2: IF — Walidacja Adresu Email

**Typ node:** `n8n-nodes-base.if`

**Rola:** Walidacja wejściowych danych zanim cokolwiek wyślemy. Blokuje przepływ jeśli email nie wygląda poprawnie.

### Konfiguracja

| Pole | Wartość |
| :--- | :--- |
| Condition | String |
| Value 1 | `{{ $json.body.email }}` |
| Operation | `Contains` |
| Value 2 | `@` |

### Pełna konfiguracja (JSON parameters view)

```json
{
  "conditions": {
    "string": [
      {
        "value1": "={{ $json.body.email }}",
        "operation": "contains",
        "value2": "@"
      }
    ]
  }
}
```

### Output — gałąź TRUE (email poprawny)

```json
{
  "headers": { ... },
  "body": {
    "name": "Anna Kowalska",
    "email": "anna@firma.pl",
    "source": "strona-kontaktowa"
  }
}
```

*(dane przechodzą bez zmian — IF tylko kieruje przepływ)*

### Output — gałąź FALSE (email bez "@")

Te same dane, ale płyną do Node 4 (SET ERROR MSG), a nie do Node 3.

---

## Node 3: Set Data — Przygotowanie Danych

**Typ node:** `n8n-nodes-base.set`

**Rola:** "Czysta" warstwa przetwarzania — wyciąga potrzebne pola, buduje treść emaila i znacznik czasu. Oddziela logikę przygotowania danych od logiki wysyłki.

### Konfiguracja

| Nazwa zmiennej | Typ | Wartość (expression) |
| :--- | :--- | :--- |
| `recipientName` | String | `{{ $json.body.name }}` |
| `recipientEmail` | String | `{{ $json.body.email }}` |
| `source` | String | `{{ $json.body.source \|\| "nieznane" }}` |
| `subject` | String | `Cześć {{ $json.body.name }}, witamy Cię!` |
| `timestamp` | String | `{{ $now.toISO() }}` |
| `emailBody` | String | (patrz niżej) |

### Wartość pola `emailBody` (expression multiline)

```
Hej {{ $json.body.name }}!

Dziękujemy za kontakt. Twoja wiadomość dotarła do nas ze źródła: {{ $json.body.source || "naszej strony" }}.

Właśnie uruchomiłeś swój pierwszy email wysłany przez automatyczny workflow w n8n.

Wkrótce odezwiemy się z dalszymi informacjami.

Pozdrawiam,
Kacper Sieradziński
Dokodu — AI Automation
https://dokodu.it
```

### Output — dane wychodzące z node'a

```json
{
  "recipientName": "Anna Kowalska",
  "recipientEmail": "anna@firma.pl",
  "source": "strona-kontaktowa",
  "subject": "Cześć Anna Kowalska, witamy Cię!",
  "timestamp": "2026-03-27T14:32:05.123Z",
  "emailBody": "Hej Anna Kowalska!\n\nDziękujemy za kontakt. Twoja wiadomość dotarła do nas ze źródła: strona-kontaktowa.\n\nWłaśnie uruchomiłeś swój pierwszy email..."
}
```

---

## Node 4: Set — Error Response (gałąź FALSE)

**Typ node:** `n8n-nodes-base.set`

**Rola:** Zwraca czytelną odpowiedź błędu gdy email nie przeszedł walidacji. Zapobiega cichemu ignorowaniu złych danych.

### Konfiguracja

| Nazwa zmiennej | Wartość |
| :--- | :--- |
| `status` | `error` |
| `message` | `Niepoprawny adres email: {{ $json.body.email }}` |
| `receivedPayload` | `{{ JSON.stringify($json.body) }}` |

### Output

```json
{
  "status": "error",
  "message": "Niepoprawny adres email: anna-bez-malpy",
  "receivedPayload": "{\"name\":\"Anna\",\"email\":\"anna-bez-malpy\"}"
}
```

---

## Node 5: Gmail — Send Message

**Typ node:** `n8n-nodes-base.gmail`

**Rola:** Wysyłka emaila używając OAuth2 credentials powiązanych z kontem Gmail.

### Konfiguracja

| Pole | Wartość |
| :--- | :--- |
| Credential | `Gmail OAuth2` (skonfigurowane wcześniej) |
| Resource | `Message` |
| Operation | `Send` |
| To | `{{ $json.recipientEmail }}` |
| Subject | `{{ $json.subject }}` |
| Email Type | `Text` |
| Message | `{{ $json.emailBody }}` |

### Opcje dodatkowe (warto pokazać uczestnikom)

| Opcja | Wartość | Opis |
| :--- | :--- | :--- |
| `Reply To` | `kacper@dokodu.it` | Odpowiedzi trafiają na właściwy adres |
| `BCC` | *(opcjonalnie)* | Kopia ukryta dla audytu |

### Output — dane zwrócone przez Gmail API

```json
{
  "id": "18f4a2b3c1d5e6f7",
  "threadId": "18f4a2b3c1d5e6f7",
  "labelIds": ["SENT"],
  "snippet": "Hej Anna Kowalska! Dziękujemy za kontakt..."
}
```

---

## Dane Wejściowe do Testowania

### Przykładowy payload — dane poprawne

```json
{
  "name": "Anna Kowalska",
  "email": "anna@firma.pl",
  "source": "strona-kontaktowa"
}
```

### Przykładowy payload — brakujące pole

```json
{
  "name": "Marek",
  "email": "marek@test.pl"
}
```

*(pole `source` nie istnieje — node Set użyje fallback `|| "nieznane"`)*

### Przykładowy payload — niepoprawny email (testowanie gałęzi FALSE)

```json
{
  "name": "Test Błędu",
  "email": "to-nie-jest-email",
  "source": "test"
}
```

---

## Instrukcja Testowania

### Metoda A — curl (macOS / Linux / WSL)

**Test 1 — dane poprawne:**
```bash
curl -X POST http://localhost:5678/webhook-test/hello-automation \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Anna Kowalska",
    "email": "TWOJ_EMAIL@gmail.com",
    "source": "strona-kontaktowa"
  }'
```

**Test 2 — niepoprawny email (testowanie IF node):**
```bash
curl -X POST http://localhost:5678/webhook-test/hello-automation \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Błędu",
    "email": "to-nie-jest-email",
    "source": "test"
  }'
```

**Test 3 — Production URL (po aktywowaniu workflow):**
```bash
curl -X POST http://localhost:5678/webhook/hello-automation \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Produkcja Test",
    "email": "TWOJ_EMAIL@gmail.com",
    "source": "test-produkcyjny"
  }'
```

### Metoda B — PowerShell (Windows)

```powershell
# Test 1 — dane poprawne
$body = '{"name": "Anna Kowalska", "email": "TWOJ_EMAIL@gmail.com", "source": "strona-kontaktowa"}'
Invoke-RestMethod -Uri "http://localhost:5678/webhook-test/hello-automation" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body

# Test 2 — niepoprawny email
$body = '{"name": "Test Bledu", "email": "to-nie-jest-email", "source": "test"}'
Invoke-RestMethod -Uri "http://localhost:5678/webhook-test/hello-automation" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

### Metoda C — Postman / Bruno (GUI)

1. Nowa kolekcja: `n8n Kurs Demo`
2. Nowy request:
   - Method: `POST`
   - URL: `http://localhost:5678/webhook-test/hello-automation`
   - Headers: `Content-Type: application/json`
   - Body → Raw → JSON:
     ```json
     {
       "name": "Anna Kowalska",
       "email": "anna@firma.pl",
       "source": "postman-test"
     }
     ```
3. Kliknij Send
4. Sprawdź Response — powinnaś zobaczyć dane z ostatniego node'a

### Jak aktywować tryb testowy przed wysłaniem requestu

> W n8n musisz kliknąć "Listen for test event" na node Webhook **zanim** wyślesz curl/Postman. Workflow czeka max 120 sekund. Po wysłaniu requestu — dane pojawią się w panelu Output node'a i możesz krokować dalej.

---

## Credentials i Zmienne

### Wymagane credentials

| Credential | Typ | Gdzie skonfigurować |
| :--- | :--- | :--- |
| `Gmail OAuth2` | OAuth2 | n8n → Credentials → Add → Gmail OAuth2 |

### Kroki konfiguracji Gmail OAuth2

1. Google Cloud Console → nowy projekt
2. APIs & Services → Library → włącz "Gmail API"
3. APIs & Services → Credentials → Create OAuth client ID
   - Application type: Web application
   - Authorized redirect URIs: `http://localhost:5678/rest/oauth2-credential/callback`
4. Skopiuj Client ID + Client Secret
5. Wklej w n8n → Credentials → Gmail OAuth2 → Sign in with Google

### Zmienne środowiskowe (opcjonalnie — dla wersji zaawansowanej)

Jeśli uruchamiasz n8n przez Docker z własnym plikiem `.env`:

```bash
# .env file dla Docker Compose
N8N_BASIC_AUTH_ACTIVE=false
N8N_HOST=localhost
N8N_PORT=5678
N8N_PROTOCOL=http
WEBHOOK_URL=http://localhost:5678/
```

Nie są wymagane dla lokalnego demo, ale warto pokazać uczestnikom że istnieją.

---

## Punkty Dydaktyczne — Co Omówić Przy Tym Workflow

### Punkt 1: Separacja odpowiedzialności (SRP w workflow)

**Dlaczego mamy oddzielny node SET zamiast wpisać treść emaila bezpośrednio w Gmail node?**

Ponieważ każdy node powinien robić jedną rzecz. Gmail node "wie" jak wysłać email. SET node "wie" jak przygotować dane. Jeśli jutro zmienisz dostawcę emaila z Gmail na SendGrid — zmienisz jeden node, nie przebudowujesz całości. To wzorzec który będzie wracał w każdym module kursu.

**Analogia do powiedzenia na nagraniu:** "SET node to jak sekretarka która przygotowuje pismo zanim wejdzie do szefa. Gmail node to szef który to pismo wysyła. Każde z nich ma swoją rolę."

---

### Punkt 2: Test URL vs Production URL — dwa tryby działania

**To jest najczęstszy błąd początkujących.** Dwa URLe to dwa tryby:

| | Test URL | Production URL |
| :--- | :--- | :--- |
| Adres | `/webhook-test/[path]` | `/webhook/[path]` |
| Kiedy działa | Tylko gdy klikniesz "Listen for test event" | Zawsze gdy workflow jest "Active" |
| Dla kogo | Ty — podczas budowania | Zewnętrzne systemy — w produkcji |
| Timeout | 120 sekund | Brak |

**Co pokazać:** wysłać curl na oba URL-e — jeden zadziała (ten właściwy dla aktualnego trybu), drugi nie.

---

### Punkt 3: IF node jako "bramkarz" danych

**Walidacja danych to nie opcja — to konieczność.** Jeśli Twój workflow dostanie `email: null` i bez IF node bezpośrednio trafi do Gmaila — dostaniesz błąd w środku execution. Trudniejszy do debugowania, wysyłający do uczestnika błędną informację o stanie systemu.

IF node robi jedną rzecz: decyduje czy dane są wystarczająco dobre żeby iść dalej. Jeśli nie — daje inną, kontrolowaną ścieżkę.

**Rozszerzenie dla bardziej zaawansowanych:** zamiast prostego `contains "@"` możesz użyć regex: `/^[^\s@]+@[^\s@]+\.[^\s@]+$/` — prawdziwa walidacja email. W tym module pokażemy prostszą wersję, żeby nie odciągać uwagi od koncepcji.

---

## Checklist przed omówieniem na nagraniu

- [ ] n8n uruchomiony lokalnie (`localhost:5678`)
- [ ] Gmail OAuth2 credentials skonfigurowane i testowo działające
- [ ] Workflow "Hello Automation" zaimportowany lub odbudowany (4 aktywne nody + 1 error)
- [ ] Workflow w trybie INACTIVE (pokażemy aktywowanie na żywo)
- [ ] Terminal gotowy z komendami curl (wklejone, ale nie uruchomione)
- [ ] Skrzynka Gmail otwarta w osobnej zakładce (widok "Inbox" — zobaczymy email jak dochodzi)
- [ ] Execution log widoczny w n8n (sidebar → Executions)

---

## Warianty Workflow (dla uczestników bardziej zaawansowanych)

Poniższe warianty to "co dalej" po opanowaniu podstawowego workflow. Nie omawiamy ich w Module 0, ale warto wspomnieć że istnieją.

| Wariant | Dodatkowy node | Opis |
| :--- | :--- | :--- |
| + Zapis do Sheets | Google Sheets → Append Row | Każdy kontakt ląduje w arkuszu |
| + Powiadomienie Slack | Slack → Send Message | Handlowiec dostaje ping na kanale |
| + Walidacja regex | Code node / IF z regex | Dokładniejsza walidacja email |
| + HTML email | Gmail → Email Type: HTML | Ładniejszy email z logo |
| + Error workflow | Error Trigger | Jeśli cokolwiek padnie — email do admina |
