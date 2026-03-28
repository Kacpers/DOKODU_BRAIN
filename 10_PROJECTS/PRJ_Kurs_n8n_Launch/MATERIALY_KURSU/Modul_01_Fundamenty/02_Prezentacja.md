---
type: kurs-materialy
modul: 01
format: prezentacja
slajdów: 38
created: 2026-03-27
---

# Tydzień 1: Fundamenty n8n — Prezentacja (38 slajdów)

---

## Slajd 1: Tytuł Modułu
**n8n + AI dla Agencji i Firm**
**Tydzień 1: Fundamenty i Pierwsza Automatyzacja**
*Kacper Sieradziński | Dokodu*

> 🎙️ NOTATKA: Krótkie intro — "Witaj w kursie. W tym tygodniu zbudujemy coś co realnie możesz wdrożyć u klienta już w poniedziałek. Nie teoria dla teorii — zacznij mieć działający system przed końcem weekendu."

---

## Slajd 2: Co Zbudujesz w Tym Tygodniu
**Lead Capture System — kompletny:**
- Formularz z landing page → webhook
- Walidacja danych + deduplikacja
- Zapis do Google Sheets
- Email powitalny przez Gmail
- Powiadomienie Slack dla zespołu
- Automatyczny alert gdy coś się posypie

> 🎙️ NOTATKA: Pokaż gotowy workflow działający na ekranie (30 sekund preview). "Tyle zbudujesz do końca tego modułu. Zaczynamy."

---

## Slajd 3: Czym n8n NIE Jest (i Czym Jest)
**NIE jest:**
- Kolejnym narzędziem do klikania przycisków
- Zamiennikiem programisty (ale zmniejsza jego rolę o 70%)
- Tylko do prostych zadań

**JEST:**
- Silnikiem automatyzacji dla serio (Fortune 500 go używa)
- Self-hosted = twoje dane, twój serwer
- 400+ integracji + dowolne API przez HTTP Request
- Logika, rozgałęzienia, pętle, AI — wszystko w jednym miejscu

> 🎙️ NOTATKA: "n8n to nie Zapier dla ubogich. To narzędzie które agencje SaaS w Berlinie i Amsterdamie wbudowują w swoje produkty jako infrastructure layer."

---

## Slajd 4: Self-Hosted vs Cloud — Decyzja
| | Self-Hosted | n8n Cloud |
|---|---|---|
| **Koszt** | $5-20/mies (VPS) | od $20/mies |
| **Kontrola danych** | 100% Twoja | n8n ma dostęp |
| **Setup** | 30 minut | 2 minuty |
| **Maintenance** | Twój problem | n8n problem |
| **Klienci enterprise** | Wymagają self-hosted | Często blokują |

**Rekomendacja kursu:** Self-hosted Docker (pokazujemy to)

> 🎙️ NOTATKA: "Jeśli dopiero zaczynasz i chcesz po prostu spróbować — n8n Cloud trial 14 dni za darmo. Jeśli budujesz coś dla klienta lub chcesz skalować — Docker."

---

## Slajd 5: Instalacja — Docker Compose (2 minuty)
```yaml
services:
  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=twoje-haslo
      - N8N_ENCRYPTION_KEY=losowy-klucz-32-znaki
    volumes:
      - n8n_data:/home/node/.n8n
volumes:
  n8n_data:
```
`docker compose up -d` → http://localhost:5678

> 🎙️ NOTATKA: "Ten plik jest do pobrania w materiałach kursu. N8N_ENCRYPTION_KEY zapisz sobie w bezpiecznym miejscu — bez niego nie otworzysz credentiali po migracji."

---

## Slajd 6: Interfejs n8n — Mapa
```
┌─────────────────────────────────────────────────────┐
│  [☰ Menu]  Workflows | Credentials | Settings       │
├─────────────────────────────────────────────────────┤
│                                                     │
│              CANVAS (płótno)                        │
│   ┌──────┐       ┌──────┐       ┌──────┐           │
│   │ Node │──────▶│ Node │──────▶│ Node │           │
│   └──────┘       └──────┘       └──────┘           │
│                                                     │
├─────────────────────────────────────────────────────┤
│  [▶ Test Workflow]  [Save]  [Activate]              │
│  Executions: 14 total | Last: 2 min ago | ✅       │
└─────────────────────────────────────────────────────┘
```

> 🎙️ NOTATKA: "Trzy przyciski w prawym górnym rogu to będzie twoje życie: Test — sprawdź czy działa, Save — zapisz, Activate — włącz produkcję."

---

## Slajd 7: Anatomia Node'a — Szczegółowo
```
┌────────────────────────────────────────────────────┐
│  ⬤ HTTP Request                          [⚙]  [✕]  │
├──────────────┬─────────────────────────────────────┤
│              │                                     │
│  INPUT       │  PARAMETRY                          │
│  ────────    │  Method: GET / POST / PUT           │
│  {item 1}    │  URL: https://api.example.com       │
│  {item 2}    │  Headers: Authorization: Bearer ... │
│              │  Body: { "key": "value" }           │
│              │                                     │
│              │  SETTINGS                           │
│              │  ✓ Continue on Fail                 │
│              │  Retry on Fail: 3x                  │
│              │  Notes: "Pobieram dane kontaktu"    │
├──────────────┴─────────────────────────────────────┤
│  OUTPUT: {item 1 z odpowiedzią}, {item 2...}       │
└────────────────────────────────────────────────────┘
```

> 🎙️ NOTATKA: "Każdy node to pudełko z wejściem i wyjściem. Co wchodzi, to przetwarza, i wypluwa dalej. Jak maszynka do mielenia — wkładasz mięso, wychodzi mielone."

---

## Slajd 8: Items — Serce n8n
**Item = jeden rekord danych**

```json
[
  { "json": { "email": "jan@firma.pl", "name": "Jan" } },
  { "json": { "email": "ala@firma.pl", "name": "Ala" } }
]
```

**Kluczowe zasady:**
- Node przetwarza **każdy item osobno** (domyślnie)
- Wyjście jednego node'a = wejście następnego
- Możesz mieć 1 item lub 10,000 itemów — workflow działa tak samo

> 🎙️ NOTATKA: "To jest najważniejszy koncept w n8n. Jeśli rozumiesz items, rozumiesz 70% n8n. Wróćmy do tego."

---

## Slajd 9: Triggery — Kiedy Workflow Startuje
```
                    ┌─────────────────┐
                    │   TRIGGER       │
                    │   (zawsze 1)    │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
   ┌─────▼──────┐     ┌──────▼─────┐    ┌───────▼──────┐
   │  MANUAL    │     │ SCHEDULE   │    │   WEBHOOK    │
   │  Klikasz   │     │ Co 5 min   │    │  HTTP POST   │
   │  Test btn  │     │ Każdy pn   │    │  z zewnątrz  │
   └────────────┘     └────────────┘    └──────────────┘
        ↓                   ↓                  ↓
   Testowanie         Cykliczne          Reaktywne
                      zadania            odpowiedzi
```

> 🎙️ NOTATKA: "Są też triggery aplikacyjne — np. 'nowy email w Gmail', 'nowa karta Trello'. Ale te trzy to fundament — wszystko inne jest pochodną."

---

## Slajd 10: Webhook Trigger — Detale
**Dwa tryby URL:**

| | Test URL | Production URL |
|---|---|---|
| Aktywacja | Tylko gdy klikasz "Listen for event" | Gdy workflow jest Activated |
| Użycie | Testowanie, development | Produkcja |
| Dane | Widoczne w canvas | Tylko w Execution Log |

**Curl test:**
```bash
curl -X POST https://twoj-n8n.com/webhook/moj-webhook \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.pl","name":"Test"}'
```

> 🎙️ NOTATKA: "Klasyczny błąd numer jeden: testujesz na Production URL albo odwrotnie — masz Activated workflow ale używasz Test URL. Zapamiętaj: Test URL = klikasz przycisk. Prod URL = workflow jest zielony."

---

## Slajd 11: Schedule Trigger — Cron Expression
**Gotowe presety:**
- Co godzinę: `0 * * * *`
- Codziennie o 8:00: `0 8 * * *`
- Każdy poniedziałek o 9:00: `0 9 * * 1`
- Co 15 minut: `*/15 * * * *`

**Format:** `minuta godzina dzień-miesiąca miesiąc dzień-tygodnia`

**Narzędzie:** crontab.guru — wpisz i sprawdź co znaczy

> 🎙️ NOTATKA: "n8n ma też wizualny builder crona — nie musisz znać składni. Ale cron expression warto znać bo będzie wszędzie."

---

## Slajd 12: 6 Kluczowych Nodes — Przegląd
| Node | Rola | Analogia |
|------|------|---------|
| **HTTP Request** | Wywołuje dowolne API | Kurier wysyłający paczkę |
| **Set** | Modyfikuje/dodaje pola | Edytor tekstu na danych |
| **IF** | Rozgałęzia na true/false | Skrzyżowanie z sygnalizatorem |
| **Switch** | Wiele rozgałęzień | Rondo z wyjściami |
| **Code** | JavaScript inline | Szwajcarski nóż |
| **NoOp** | Nic nie robi | Zaślepka / placeholder |

> 🎙️ NOTATKA: "Te 6 nodes + Webhook Trigger + paru integracje = możesz zbudować 80% tego co klienci chcą w pierwszym kwartale."

---

## Slajd 13: HTTP Request Node — Szczegółowo
**Najważniejsze pola:**
- **Method:** GET, POST, PUT, PATCH, DELETE
- **URL:** pełny adres endpointuDo
- **Authentication:** tu podłączasz credential
- **Headers:** Content-Type, Accept
- **Body:** JSON / Form Data / Raw

**Jak czytać odpowiedź:**
```
Response → data → json → twoje_pole
```
W Expressions: `{{ $json.data.email }}`

> 🎙️ NOTATKA: "HTTP Request to twój dostęp do całego internetu. Każde API, każdy webhook, każdy serwis który ma endpoint — możesz z nim rozmawiać."

---

## Slajd 14: Expressions — Język n8n
**Składnia:** `{{ wyrażenie_JavaScript }}`

**Najczęstsze użycia:**
```javascript
{{ $json.email }}              // pole z poprzedniego node'a
{{ $json.name.toLowerCase() }} // JavaScript na danych
{{ $now.toISO() }}             // aktualny czas (ISO 8601)
{{ $('Webhook').item.json.email }} // pole z konkretnego node'a
{{ $env.SHEETS_ID }}           // zmienna środowiskowa
```

**Uwaga:** Expressions działają w trybie "jednego itemu" — jeśli chcesz listę, użyj Code node.

> 🎙️ NOTATKA: "Wyrażenia to supermoc n8n. Zamiast wklepywać stałe wartości — pobierasz dane z poprzednich kroków. Jak formuły w Excelu, tylko dla danych z całego internetu."

---

## Slajd 15: IF Node — Logika Warunkowa
**Struktura:**
```
         ┌──────────────┐
INPUT ──▶ │   IF Node    │──▶ TRUE branch
         │  email musi  │
         │  mieć @       │──▶ FALSE branch
         └──────────────┘
```

**Typy warunków:**
- String: contains, equals, starts with, regex
- Number: greater than, less than, equals
- Boolean: is true, is false
- Date: before, after, between

> 🎙️ NOTATKA: "Zawsze podłącz OBIE gałęzie. Gałąź FALSE to często 'co robimy z błędem' — nie zostawiaj jej pustej w produkcji."

---

## Slajd 16: Switch Node — Wielokrotne Rozgałęzienie
**Użycie:** gdy masz więcej niż 2 ścieżki

```
              ┌─────────────┐
              │  Switch     │──▶ Case: "lead"    →  [zapisz lead]
INPUT ───────▶│  typ_leadu  │──▶ Case: "klient"  →  [aktualizuj CRM]
              │             │──▶ Case: "spam"    →  [ignoruj]
              └─────────────┘──▶ Default         →  [email do admina]
```

**Tip:** Zawsze dodaj "Default" case — obsługuje nieoczekiwane wartości

> 🎙️ NOTATKA: "Switch to IF na sterydach. Jeśli masz IF w IF w IF — czas na Switch."

---

## Slajd 17: Code Node — JavaScript Inline
**Kiedy używać:**
- Transformacje danych których Set nie obsługuje
- Własna logika biznesowa
- Parsowanie skomplikowanych struktur JSON
- Regex, obliczenia, manipulacje tablicami

**Przykład:**
```javascript
// Walidacja emaila własną regexem
const email = $input.first().json.email;
const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

return [{ json: { email, isValid, message: isValid ? 'OK' : 'Błędny email' } }];
```

> 🎙️ NOTATKA: "Code node to ucieczka gdy inne nodes nie dają rady. Używaj oszczędnie — każda linia kodu to potencjalny bug i coś czego klient nie może edytować w wizualnym edytorze."

---

## Slajd 18: Credential Vault — Jak Działa
```
┌──────────────────────────────────────────┐
│           CREDENTIAL VAULT               │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │  Gmail OAuth2                      │  │
│  │  Slack API Token: ░░░░░░░░░░░░░░░  │  │
│  │  Google Sheets Service Account     │  │
│  └────────────────────────────────────┘  │
│                                          │
│  Szyfrowanie: AES-256                    │
│  Klucz: N8N_ENCRYPTION_KEY (twój!)      │
│  Widoczność: tylko w tym n8n            │
└──────────────────────────────────────────┘
```
**Zasada:** 1 credential = 1 konto/API key. Nigdy nie wklejaj kluczy w node'ach!

> 🎙️ NOTATKA: "Vault to sejf. Klucze API siedzą tam zaszyfrowane. Gdy workflow ich używa — n8n wstrzykuje je w tle. W logach executions nie widać wartości kluczy."

---

## Slajd 19: Mapa Typów Credentiali
| Typ | Kiedy używasz | Przykłady |
|-----|---------------|-----------|
| **API Key** | Serwis daje klucz API | OpenAI, Airtable, SendGrid |
| **Header Auth** | Klucz idzie w nagłówku HTTP | Większość własnych API |
| **Basic Auth** | Login + hasło | Stare API, intranety |
| **Bearer Token** | Token w nagłówku Authorization | GitHub, Stripe |
| **OAuth2** | "Zaloguj przez Google/Slack" | Gmail, Slack, Google Sheets |
| **Service Account** | Konto techniczne Google | Google Sheets, Drive, BigQuery |

> 🎙️ NOTATKA: "OAuth2 wygląda strasznie ale n8n robi to automatycznie — klikasz przycisk, loguje się do Google w przeglądarce, token wraca do n8n. Jak SSO."

---

## Slajd 20: OAuth2 — Uproszczony Flow
```
n8n Canvas
│
├─ Klikasz "Connect OAuth2"
│
└──▶ Google Login Page (nowe okno)
          │
          └──▶ Akceptujesz uprawnienia
                    │
                    └──▶ Token wraca do n8n
                              │
                              └──▶ Credential zapisany ✅
                                   (token odświeżany automatycznie)
```

**Tip:** Credential OAuth2 dla Gmail = dostęp do tej konkretnej skrzynki. Dla klienta — stwórz oddzielny credential.

> 🎙️ NOTATKA: "Tokeny OAuth2 wygasają co godzinę. n8n sam je odświeża w tle — ty tego nie widzisz. To magia."

---

## Slajd 21: Error Handling — 3 Strategie
**Strategia 1: Continue on Fail**
- Node failuje → workflow idzie dalej z `error` w danych
- Użycie: gdy błąd jednego kroku nie blokuje pozostałych

**Strategia 2: Try/Catch Pattern**
- IF node sprawdza czy `$json.error` istnieje
- Ścieżka true = obsługa błędu, ścieżka false = sukces

**Strategia 3: Error Trigger Workflow**
- Oddzielny workflow który startuje gdy inny workflow pada
- Gold standard dla produkcji

> 🎙️ NOTATKA: "Strategia 1 = szybka, brzydka, działa. Strategia 3 = elegancka, skalowalna, polecam dla każdego workflow który idzie do klienta."

---

## Slajd 22: Flow Error Handling — Diagram
```
GŁÓWNY WORKFLOW
─────────────────────────────────────────────────────
[Webhook] → [Walidacja] → [Sheets] → [Gmail] → [Slack]
                              │           │
                        ❌ Error     ❌ Error
                              │           │
                              └─────┬─────┘
                                    │
                             Continue on Fail
                                    │
                              [IF: error?]
                               True │
                                    ▼
                         [Set: error details]
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │  ERROR WORKFLOW (oddzielny)   │
                    │  Error Trigger                │
                    │  → Gmail do admina            │
                    │  → Slack #alerty              │
                    └───────────────────────────────┘
```

> 🎙️ NOTATKA: "W tym modelu: błąd nigdy nie ginie bez śladu. Admin zawsze dostaje powiadomienie. Klient nigdy nie widzi surowego błędu."

---

## Slajd 23: Error Trigger Workflow — Setup
**Krok 1:** Stwórz nowy workflow "Error Handler"
**Krok 2:** Dodaj "Error Trigger" jako trigger
**Krok 3:** Dodaj logikę powiadomień (Gmail + Slack)
**Krok 4:** W głównym workflow → Settings → Error Workflow → wybierz "Error Handler"

**Dane dostępne w Error Trigger:**
```json
{
  "workflow": { "name": "Lead Capture", "id": "123" },
  "execution": { "id": "456", "url": "..." },
  "node": { "name": "Google Sheets", "type": "n8n-nodes-base.googleSheets" },
  "error": { "message": "The sheet doesn't exist", "stack": "..." }
}
```

> 🎙️ NOTATKA: "Jedna robota Error Handler workflow: daj znać co, gdzie i kiedy padło. Dobre powiadomienie zawiera: nazwę workflow, nazwę node'a, wiadomość błędu, link do execution."

---

## Slajd 24: Debugowanie — 5-Krokowy Przepis
1. **Kliknij czerwony node** — otwiera błąd
2. **Sprawdź Input** czerwonego node'a — czy dane w ogóle tam dotarły?
3. **Sprawdź Output** poprzedniego node'a — czy dane mają właściwy format?
4. **Pin Data** na poprzednim node'ie → "Test Step" tylko na problematycznym
5. **Console.log** w Code node jeśli nadal nie wiesz

**Top 3 przyczyny błędów:**
- Literówka w nazwie pola (`email` vs `Email` vs `e-mail`)
- Typ danych: string zamiast number
- Brakujące pole (null/undefined)

> 🎙️ NOTATKA: "90% bugów to dane. Nie kod, nie logika — po prostu coś nie ma tego co myślisz że ma."

---

## Slajd 25: Pin Data — Jak Działa
```
NORMALNY FLOW:          PIN DATA FLOW:
[Webhook]               [Webhook] ← PINNED 📌
    ↓                       ↓ (używa zapisanych danych)
[Set]                   [Set]
    ↓                       ↓
[IF]                    [IF] ← "Test Step" uruchamia tylko ten node
```

**Jak pinować:**
1. Uruchom workflow raz (żeby node'y miały dane)
2. Kliknij node → zakładka Output → "Pin"
3. Teraz możesz testować downstream nodes bez triggerowania całości

> 🎙️ NOTATKA: "Pin Data to cheat code n8n. Nie musisz wysyłać formularza 20 razy żeby przetestować jeden node. Zapisujesz dane raz i testujesz w kółko."

---

## Slajd 26: Lead Capture System — Architektura
```
FORMULARZ (landing page)
        │  HTTP POST
        ▼
[Webhook Trigger]
        │
[Walidacja: Set + IF]    ← email format, wymagane pola
        │
   ✅ Valida    ❌ Invalid
        │              │
        │         [Respond: 400]
        │
[HTTP Request: Sheets]   ← sprawdź deduplikację
        │
   Nowy lead    Duplikat
        │              │
        │         [Respond: 200 "już zapisany"]
        │
[Google Sheets: Append]  ← zapisz lead
        │
[Gmail: Send]            ← email powitalny
        │
[Slack: Post Message]    ← powiadom zespół
        │
[Respond: 200 "OK"]
```

> 🎙️ NOTATKA: "To jest schemat który omawiamy. Każdy krok ma rację bytu — za chwilę zbudujemy go krok po kroku."

---

## Slajd 27: Walidacja Danych — Strategia
**Co walidujemy:**
- Wymagane pola: `email`, `name` (IF: isEmpty)
- Format emaila: regex `/^[^\s@]+@[^\s@]+\.[^\s@]+$/`
- Długość pól: name max 100 znaków
- Honeypot: ukryte pole formularza = bot detection

**Jak odpowiadamy na błąd walidacji:**
```json
{
  "success": false,
  "error": "Nieprawidłowy format adresu email",
  "field": "email"
}
```
HTTP 400 Bad Request

> 🎙️ NOTATKA: "Walidacja jest dla ciebie, nie dla klienta. Lepiej odrzucić śmieciowe dane na wejściu niż potem czyścić Google Sheets."

---

## Slajd 28: Deduplikacja — Jak Sprawdzić
**Problem:** Ten sam email może przyjść dwa razy (odświeżenie formularza, błąd użytkownika)

**Rozwiązanie: Google Sheets API**
```
HTTP Request (GET):
URL: https://sheets.googleapis.com/v4/spreadsheets/
     {SHEET_ID}/values/A:A

Sprawdź: czy email jest w kolumnie A?
→ Tak: zwróć 200 "Już zarejestrowany"
→ Nie: idź dalej
```

**Alternatywa:** Użyj Google Sheets node z operacją "Read" + filter

> 🎙️ NOTATKA: "W większych systemach deduplikację robi baza danych. Dla kursowego projektu Google Sheets wystarczy. W produkcji przemysłowej — Supabase lub Airtable."

---

## Slajd 29: Google Sheets Node — Konfiguracja
**Operacja: Append or Update Row**

| Pole | Wartość |
|------|---------|
| Credential | Google Sheets OAuth2 |
| Spreadsheet | (wybierz z listy lub ID) |
| Sheet | Leads |
| Matching Column | email |
| Columns to Send | email, name, message, source, timestamp |

**Przykładowy wiersz:**
```
jan@firma.pl | Jan Kowalski | Chcę automatyzację | Landing | 2026-03-27T10:30:00Z
```

> 🎙️ NOTATKA: "Append or Update = jeśli email istnieje to aktualizuje, jeśli nie — dodaje nowy wiersz. Mądrzejsze niż samo Append."

---

## Slajd 30: Gmail Node — Email Powitalny
**Konfiguracja:**
```
To: {{ $json.email }}
Subject: Cześć {{ $json.name }}, witamy w Dokodu!
Body (HTML):
  Cześć {{ $json.name }},

  Otrzymaliśmy Twoje zgłoszenie. Odezwiemy się w ciągu 24h.

  Zespół Dokodu
```

**Credential:** Gmail OAuth2 (konto z którego wysyłasz)

**Tip:** Użyj zmiennej `{{ $json.name.split(' ')[0] }}` żeby mieć tylko imię

> 🎙️ NOTATKA: "Personalizacja to minimum — imię w temacie i treści. Różnica w open rate między 'Witamy' a 'Cześć Jan' to kilkanaście procent."

---

## Slajd 31: Slack Node — Powiadomienie Zespołu
**Konfiguracja:**
```
Channel: #leady
Message:
🎯 Nowy lead!
*Imię:* {{ $json.name }}
*Email:* {{ $json.email }}
*Źródło:* {{ $json.source || 'formularz' }}
*Czas:* {{ $now.toLocaleString('pl-PL') }}
```

**Credential:** Slack API (Bot Token lub Webhook URL)

> 🎙️ NOTATKA: "Slack notification to dla zespołu. Ktoś musi zadzwonić do leada w ciągu godziny od zgłoszenia — to właśnie ta wiadomość inicjuje ten proces."

---

## Slajd 32: Zmienne Środowiskowe w n8n
**Ustawienie w docker-compose.yml:**
```yaml
environment:
  - SHEETS_ID=1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms
  - SLACK_CHANNEL=#leady
  - ADMIN_EMAIL=kacper@dokodu.it
  - ENVIRONMENT=production
```

**Użycie w workflow:**
```javascript
{{ $env.SHEETS_ID }}
{{ $env.ADMIN_EMAIL }}
```

**Dlaczego:** Jeden workflow → wiele środowisk (dev/staging/prod) bez edycji node'ów

> 🎙️ NOTATKA: "Env vars to podstawa profesjonalnego n8n. Jeśli masz hardcoded ID arkusza w node'zie — to jest code smell. Wyciągaj do zmiennych."

---

## Slajd 33: Testing Checklist — Przed Aktywacją
**Scenariusze które musisz przetestować:**
- [ ] Poprawny payload → lead zapisany, email wysłany, Slack powiadomiony
- [ ] Brak pola `email` → odpowiedź 400
- [ ] Błędny format emaila → odpowiedź 400
- [ ] Duplikat emaila → odpowiedź 200 "już istnieje"
- [ ] Google Sheets niedostępny → Error Handler workflow uruchomiony
- [ ] Gmail limit przekroczony → Error Handler workflow uruchomiony

> 🎙️ NOTATKA: "Test tylko happy path = workflow który pada przy pierwszym prawdziwym kliencie. Test wszystkich ścieżek błędów to różnica między amatorem a profesjonalistą."

---

## Slajd 34: Metryki i Monitoring
**Co śledzić po wdrożeniu:**
- Execution Success Rate (cel: >99%)
- Average Execution Time (alarm gdy >5s)
- Failed Executions (alerty natychmiastowe)
- Lead Volume per Day (trend)

**Gdzie:**
- n8n → Executions panel (historia)
- n8n → Settings → Usage → metryki globalne
- Error Handler workflow → arkusz z błędami (loguj!)

> 🎙️ NOTATKA: "Nie wdrożysz i zapomnisz. Wdrożysz i monitorujesz. Production to nie test — tam chodzi prawdziwy biznes klienta."

---

## Slajd 35: Najczęstsze Błędy Początkujących
| Błąd | Problem | Rozwiązanie |
|------|---------|-------------|
| Klucz API w wyrażeniu | Widoczny w logach | Użyj Credential Vault |
| Brak Error Handling | Workflow pada cicho | Zawsze Error Trigger Workflow |
| Test URL w produkcji | Workflow nie startuje | Aktywuj + użyj Prod URL |
| Hardcoded ID | Nie da się skalować | Env vars |
| IF bez gałęzi false | Dane giną w próżni | Zawsze obsłuż false |

> 🎙️ NOTATKA: "Te błędy zrobiłem sam. Każdy je robi. Lepiej nauczyć się teraz niż w środku nocy gdy klient dzwoni że formularz nie działa."

---

## Slajd 36: Zadanie Domowe
**Rozszerz Lead Capture o filtrowanie spamu:**
- Sprawdź czy pole `message` zawiera słowa kluczowe (np. "crypto", "casino", "SEO services")
- Jeśli tak → nie zapisuj, nie wysyłaj emaila
- Zamiast tego → zapisz do osobnego arkusza "Spam" z timestampem
- Opcjonalnie: dodaj własną listę słów kluczowych jako zmienną środowiskową

**Wskazówka:** IF node z warunkiem "contains" lub Code node z tablicą słów

> 🎙️ NOTATKA: "To nie jest trudne — jeden IF node i jeden dodatkowy arkusz. Ale zmusi cię do samodzielnego myślenia o przepływie danych. 30–45 minut."

---

## Slajd 37: Co Będzie w Tygodniu 2
**Tydzień 2: API i Dane**
- HTTP Request w głąb (pagination, authentication, rate limiting)
- Transformacje danych: Merge, Split, Loop
- Zewnętrzne API: OpenAI, Airtable, Notion
- Projekt: Automatyczny raport z danych (agregacja z kilku źródeł → PDF)

> 🎙️ NOTATKA: "W tygodniu 2 wychodzimy poza formularze. Będziemy gadać z prawdziwymi API i łączyć dane z wielu źródeł. Przygotuj klucz OpenAI."

---

## Slajd 38: Podsumowanie Tygodnia 1
**Umiesz już:**
- Zainstalować n8n i poruszać się po interfejsie
- Stworzyć workflow z Webhook, Schedule i Manual Trigger
- Używać 6 kluczowych nodes (HTTP Request, Set, IF, Switch, Code, NoOp)
- Bezpiecznie przechowywać klucze API w Credential Vault
- Obsługiwać błędy na 3 poziomach
- Debugować workflow jak profesjonalista

**Zbudowałeś:** Lead Capture System — coś co możesz wdrożyć u klienta.

> 🎙️ NOTATKA: "To nie jest mały krok. Lead Capture jest prostym przykładem ale wzorzec — webhook, walidacja, deduplikacja, akcja, powiadomienie, error handling — zobaczysz go w każdym poważnym projekcie n8n. Gratulacje."
