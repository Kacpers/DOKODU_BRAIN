---
theme: default
titleTemplate: "%s | Dokodu"
highlighter: shiki
lineNumbers: false
drawings:
  persist: false
transition: slide-left
mdc: true
fonts:
  sans: Inter
  mono: Fira Code
css: style.css
---


---
layout: cover
---

<img src="/dokodu_logo.png" style="height:28px;margin-bottom:1.8rem;opacity:0.92" alt="Dokodu" />

<div class="cover-tag">MODUŁ 01 — FUNDAMENTY</div>

# Kurs n8n


<p style="color:#E63946;font-weight:600">Kacper Sieradziński</p>
<p style="color:#8096AA;font-size:0.8rem;margin-top:0.2rem">dokodu.it</p>


---
---

# Co zbudujesz w tym tygodniu

## Lead Capture System — kompletny

<v-clicks>

- Formularz z landing page → webhook
- Walidacja danych + deduplikacja
- Zapis do Google Sheets
- Email powitalny przez Gmail
- Powiadomienie Slack dla zespołu
- Automatyczny alert gdy coś się posypie

</v-clicks>


<!--
Pokaż gotowy workflow działający na ekranie (30 sekund preview). "Tyle zbudujesz do końca tego modułu. Zaczynamy."
-->


---
layout: two-cols-header
---

# Czym n8n NIE jest (i czym jest)

<div class="col-header col-neg">NIE jest</div>

- Kolejnym narzędziem do klikania przycisków
- Zamiennikiem programisty (ale zmniejsza jego rolę o 70%)
- Tylko do prostych zadań

::right::

<div class="col-header col-pos">JEST</div>

- Silnikiem automatyzacji dla serio (Fortune 500 go używa)
- Self-hosted = twoje dane, twój serwer
- 400+ integracji + dowolne API przez HTTP Request
- Logika, rozgałęzienia, pętle, AI — wszystko w jednym miejscu

<!--
"n8n to nie Zapier dla ubogich. To narzędzie które agencje SaaS w Berlinie i Amsterdamie wbudowują w swoje produkty jako infrastructure layer."
-->


---
---

# Self-Hosted vs cloud — decyzja

| | Self-Hosted | n8n Cloud |
|---|---|---|
| **Koszt** | $5-20/mies (VPS) | od $20/mies |
| **Kontrola danych** | 100% Twoja | n8n ma dostęp |
| **Setup** | 30 minut | 2 minuty |
| **Maintenance** | Twój problem | n8n problem |
| **Klienci enterprise** | Wymagają self-hosted | Często blokują |

**Rekomendacja kursu:** Self-hosted Docker (pokazujemy to)

<!--
"Jeśli dopiero zaczynasz i chcesz po prostu spróbować — n8n Cloud trial 14 dni za darmo. Jeśli budujesz coś dla klienta lub chcesz skalować — Docker."
-->


---
---

# Instalacja — Docker compose (2 minuty)

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

<!--
"Ten plik jest do pobrania w materiałach kursu. N8N_ENCRYPTION_KEY zapisz sobie w bezpiecznym miejscu — bez niego nie otworzysz credentiali po migracji."
-->


---
---

# Interfejs n8n — mapa

<div style="background:#0A1628;border-radius:10px;overflow:hidden;border:1px solid rgba(255,255,255,0.08);box-shadow:0 8px 32px rgba(0,0,0,0.4);font-family:Inter,sans-serif;position:relative">

  <!-- Dot grid -->
  <div style="position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,0.04) 1px,transparent 1px);background-size:20px 20px;pointer-events:none"></div>

  <!-- Top bar -->
  <div style="position:relative;background:#0F2137;border-bottom:2px solid #E63946;padding:0.5rem 1rem;display:flex;align-items:center;gap:1.5rem">
    <div style="display:flex;align-items:center;gap:0.4rem">
      <div style="background:#E63946;color:#fff;font-weight:900;font-size:0.65rem;width:18px;height:18px;border-radius:3px;display:flex;align-items:center;justify-content:center">n</div>
      <span style="color:#fff;font-size:0.72rem;font-weight:700">n8n</span>
    </div>
    <div style="display:flex;gap:1rem">
      <span style="color:#A8D8EA;font-size:0.68rem;font-weight:600;border-bottom:2px solid #E63946;padding-bottom:2px">Workflows</span>
      <span style="color:#64748B;font-size:0.68rem">Credentials</span>
      <span style="color:#64748B;font-size:0.68rem">Executions</span>
      <span style="color:#64748B;font-size:0.68rem">Settings</span>
    </div>
    <div style="margin-left:auto;display:flex;gap:0.5rem">
      <span style="background:#1E2D40;color:#8096AA;font-size:0.6rem;padding:0.2rem 0.55rem;border-radius:4px;border:1px solid rgba(255,255,255,0.08)">Save</span>
      <span style="background:#1E2D40;color:#8096AA;font-size:0.6rem;padding:0.2rem 0.55rem;border-radius:4px;border:1px solid rgba(255,255,255,0.08)">Test</span>
      <span style="background:#22C55E;color:#fff;font-size:0.6rem;padding:0.2rem 0.55rem;border-radius:4px;font-weight:700">Activate</span>
    </div>
  </div>

  <!-- Main area -->
  <div style="position:relative;display:flex;gap:0;min-height:160px">

    <!-- Left panel — node library -->
    <div style="width:140px;flex-shrink:0;background:#0F2137;border-right:1px solid rgba(255,255,255,0.07);padding:0.6rem 0.7rem">
      <div style="color:#E63946;font-size:0.6rem;font-weight:700;letter-spacing:0.08em;margin-bottom:0.5rem">BIBLIOTEKA NODÓW</div>
      <div style="display:flex;flex-direction:column;gap:0.3rem">
        <div style="background:#1E2D40;border-radius:4px;padding:0.25rem 0.5rem;font-size:0.62rem;color:#A8D8EA;border-left:2px solid #F97316">⚡ Triggery</div>
        <div style="background:#1E2D40;border-radius:4px;padding:0.25rem 0.5rem;font-size:0.62rem;color:#A8D8EA;border-left:2px solid #3B82F6">⚙ Akcje</div>
        <div style="background:#1E2D40;border-radius:4px;padding:0.25rem 0.5rem;font-size:0.62rem;color:#A8D8EA;border-left:2px solid #8B5CF6">🔀 Logika</div>
        <div style="background:#1E2D40;border-radius:4px;padding:0.25rem 0.5rem;font-size:0.62rem;color:#A8D8EA;border-left:2px solid #64748B">🔗 HTTP / Code</div>
      </div>
    </div>

    <!-- Canvas -->
    <div style="flex:1;padding:1rem 1.2rem;display:flex;align-items:center;gap:0.6rem">
      <div style="background:#1E2D40;border-radius:6px;border:1px solid rgba(255,255,255,0.08);border-top:2px solid #F97316;padding:0.4rem 0.7rem;text-align:center;min-width:72px">
        <div style="font-size:0.6rem;color:#F97316;font-weight:700">WEBHOOK</div>
        <div style="font-size:0.55rem;color:#64748B;margin-top:2px">Trigger</div>
      </div>
      <svg width="28" height="8" viewBox="0 0 28 8"><line x1="0" y1="4" x2="20" y2="4" stroke="#E63946" stroke-width="1.5" stroke-dasharray="3 2"/><polygon points="20,1 28,4 20,7" fill="#E63946"/></svg>
      <div style="background:#1E2D40;border-radius:6px;border:1px solid rgba(255,255,255,0.08);border-top:2px solid #3B82F6;padding:0.4rem 0.7rem;text-align:center;min-width:72px">
        <div style="font-size:0.6rem;color:#3B82F6;font-weight:700">IF NODE</div>
        <div style="font-size:0.55rem;color:#64748B;margin-top:2px">Logika</div>
      </div>
      <svg width="28" height="8" viewBox="0 0 28 8"><line x1="0" y1="4" x2="20" y2="4" stroke="#E63946" stroke-width="1.5" stroke-dasharray="3 2"/><polygon points="20,1 28,4 20,7" fill="#E63946"/></svg>
      <div style="background:#1E2D40;border-radius:6px;border:1px solid rgba(255,255,255,0.08);border-top:2px solid #22C55E;padding:0.4rem 0.7rem;text-align:center;min-width:72px">
        <div style="font-size:0.6rem;color:#22C55E;font-weight:700">GMAIL</div>
        <div style="font-size:0.55rem;color:#64748B;margin-top:2px">Wyślij</div>
      </div>
      <div style="margin-left:auto;background:#0F2137;border-radius:6px;padding:0.5rem 0.8rem;font-size:0.6rem;color:#64748B;border:1px dashed rgba(255,255,255,0.1);text-align:center">
        <div style="color:#A8D8EA;font-weight:600;margin-bottom:2px">CANVAS</div>
        <div>przeciągnij nody</div>
        <div>z biblioteki →</div>
      </div>
    </div>
  </div>

  <!-- Bottom bar -->
  <div style="position:relative;background:#0F2137;border-top:1px solid rgba(255,255,255,0.07);padding:0.4rem 1rem;display:flex;align-items:center;gap:1.5rem">
    <span style="color:#22C55E;font-size:0.62rem;font-weight:600">✓ Executions: 14 total</span>
    <span style="color:#64748B;font-size:0.6rem">Last: 2 min ago</span>
    <div style="margin-left:auto;display:flex;gap:1rem">
      <span style="color:#8096AA;font-size:0.6rem">← Execution log</span>
      <span style="color:#8096AA;font-size:0.6rem">Settings →</span>
    </div>
  </div>
</div>


<!--
"Trzy przyciski w prawym górnym rogu to będzie twoje życie: Test — sprawdź czy działa, Save — zapisz, Activate — włącz produkcję."
-->


---
---

# Anatomia node'a — szczegółowo

<div class="diagram-block">

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

</div>

<!--
"Każdy node to pudełko z wejściem i wyjściem. Co wchodzi, to przetwarza, i wypluwa dalej. Jak maszynka do mielenia — wkładasz mięso, wychodzi mielone."
-->


---
---

# Items — serce n8n

## Item = jeden rekord danych

```json
[
  { "json": { "email": "jan@firma.pl", "name": "Jan" } },
  { "json": { "email": "ala@firma.pl", "name": "Ala" } }
]
```

## Kluczowe zasady
- Node przetwarza **każdy item osobno** (domyślnie)
- Wyjście jednego node'a = wejście następnego
- Możesz mieć 1 item lub 10,000 itemów — workflow działa tak samo

<!--
"To jest najważniejszy koncept w n8n. Jeśli rozumiesz items, rozumiesz 70% n8n. Wróćmy do tego."
-->


---
---

# Triggery — kiedy workflow startuje

<N8nBranch
  :source="{icon: 'mdi:lightning-bolt', label: 'TRIGGER', desc: 'zawsze 1 na workflow'}"
  :branches="[
    {icon: 'mdi:cursor-default-click', label: 'MANUAL', desc: 'Klikasz Test btn', result: 'Testowanie', variant: 'action'},
    {icon: 'mdi:clock-time-four-outline', label: 'SCHEDULE', desc: 'Co 5 min / Każdy pn', result: 'Cykliczne zadania', variant: 'default'},
    {icon: 'mdi:webhook', label: 'WEBHOOK', desc: 'HTTP POST z zewnątrz', result: 'Reaktywne odpowiedzi', variant: 'trigger'},
  ]"
/>

<div style="margin-top:0.8rem;font-size:0.78rem;color:#64748B">
Są też triggery aplikacyjne — np. <strong>nowy email w Gmail</strong>, <strong>nowa karta Trello</strong>. Ale te trzy to fundament.
</div>


<!--
"Są też triggery aplikacyjne — np. 'nowy email w Gmail', 'nowa karta Trello'. Ale te trzy to fundament — wszystko inne jest pochodną."
-->


---
---

# Webhook trigger — detale

## Dwa tryby URL

| | Test URL | Production URL |
|---|---|---|
| Aktywacja | Tylko gdy klikasz "Listen for event" | Gdy workflow jest Activated |
| Użycie | Testowanie, development | Produkcja |
| Dane | Widoczne w canvas | Tylko w Execution Log |

## Curl test
```bash
curl -X POST https://twoj-n8n.com/webhook/moj-webhook \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.pl","name":"Test"}'
```

<!--
"Klasyczny błąd numer jeden: testujesz na Production URL albo odwrotnie — masz Activated workflow ale używasz Test URL. Zapamiętaj: Test URL = klikasz przycisk. Prod URL = workflow jest zielony."
-->


---
---

# Schedule trigger — cron expression

## Gotowe presety

<v-clicks>

- Co godzinę: `0 * * * *`
- Codziennie o 8:00: `0 8 * * *`
- Każdy poniedziałek o 9:00: `0 9 * * 1`
- Co 15 minut: `*/15 * * * *`

</v-clicks>


**Format:** `minuta godzina dzień-miesiąca miesiąc dzień-tygodnia`

**Narzędzie:** crontab.guru — wpisz i sprawdź co znaczy

<!--
"n8n ma też wizualny builder crona — nie musisz znać składni. Ale cron expression warto znać bo będzie wszędzie."
-->


---
---

# 6 kluczowych nodes — przegląd

| Node | Rola | Analogia |
|------|------|---------|
| **HTTP Request** | Wywołuje dowolne API | Kurier wysyłający paczkę |
| **Set** | Modyfikuje/dodaje pola | Edytor tekstu na danych |
| **IF** | Rozgałęzia na true/false | Skrzyżowanie z sygnalizatorem |
| **Switch** | Wiele rozgałęzień | Rondo z wyjściami |
| **Code** | JavaScript inline | Szwajcarski nóż |
| **NoOp** | Nic nie robi | Zaślepka / placeholder |

<!--
"Te 6 nodes + Webhook Trigger + paru integracje = możesz zbudować 80% tego co klienci chcą w pierwszym kwartale."
-->


---
---

# HTTP request Node — szczegółowo

## Najważniejsze pola
- **Method:** GET, POST, PUT, PATCH, DELETE
- **URL:** pełny adres endpointuDo
- **Authentication:** tu podłączasz credential
- **Headers:** Content-Type, Accept
- **Body:** JSON / Form Data / Raw

## Jak czytać odpowiedź
```
Response → data → json → twoje_pole
```
W Expressions: `{{ $json.data.email }}`

<!--
"HTTP Request to twój dostęp do całego internetu. Każde API, każdy webhook, każdy serwis który ma endpoint — możesz z nim rozmawiać."
-->


---
---

# Expressions — język n8n

**Składnia:** `{{ wyrażenie_JavaScript }}`

## Najczęstsze użycia
```javascript
{{ $json.email }}              // pole z poprzedniego node'a
{{ $json.name.toLowerCase() }} // JavaScript na danych
{{ $now.toISO() }}             // aktualny czas (ISO 8601)
{{ $('Webhook').item.json.email }} // pole z konkretnego node'a
{{ $env.SHEETS_ID }}           // zmienna środowiskowa
```

**Uwaga:** Expressions działają w trybie "jednego itemu" — jeśli chcesz listę, użyj Code node.

<!--
"Wyrażenia to supermoc n8n. Zamiast wklepywać stałe wartości — pobierasz dane z poprzednich kroków. Jak formuły w Excelu, tylko dla danych z całego internetu."
-->


---
---

# IF Node — logika warunkowa

**Typy warunków:** String (contains, equals, regex) · Number (>, <, =) · Boolean · Date

<N8nFlow
  :nodes="[
    {icon: 'mdi:database-arrow-right', label: 'INPUT', desc: 'dane z poprzedniego node', variant: 'default'},
    {icon: 'mdi:source-branch', label: 'IF Node', desc: 'warunek spełniony?', variant: 'trigger'},
    {icon: 'mdi:check-circle', label: 'TRUE', desc: 'dalsze działanie', variant: 'output'},
  ]"
/>

<div style="margin-top:0.6rem;display:flex;gap:0.8rem;align-items:center">
  <div style="background:#1E2D40;border-left:3px solid #EF4444;padding:0.4rem 0.8rem;border-radius:0 6px 6px 0;font-size:0.78rem;color:#A8D8EA">
    <strong style="color:#EF4444">FALSE branch</strong> → obsługa błędu / odrzucenie
  </div>
  <div style="font-size:0.72rem;color:#64748B">💡 Zawsze podłącz OBIE gałęzie!</div>
</div>


<!--
"Zawsze podłącz OBIE gałęzie. Gałąź FALSE to często 'co robimy z błędem' — nie zostawiaj jej pustej w produkcji."
-->


---
---

# Switch Node — wielokrotne rozgałęzienie

**Użycie:** gdy masz więcej niż 2 ścieżki. Zawsze dodaj **Default** case.

<N8nBranch
  :source="{icon: 'mdi:source-branch', label: 'Switch Node', desc: 'wartość: typ_leadu'}"
  :branches="[
    {icon: 'mdi:account-plus', label: 'lead', result: 'zapisz lead', variant: 'action'},
    {icon: 'mdi:account-check', label: 'klient', result: 'aktualizuj CRM', variant: 'action'},
    {icon: 'mdi:cancel', label: 'spam', result: 'ignoruj', variant: 'default'},
    {icon: 'mdi:email-alert', label: 'Default', result: 'email do admina', variant: 'trigger'},
  ]"
/>


<!--
"Switch to IF na sterydach. Jeśli masz IF w IF w IF — czas na Switch."
-->


---
---

# Code Node — JavaScript inline

## Kiedy używać
- Transformacje danych których Set nie obsługuje
- Własna logika biznesowa
- Parsowanie skomplikowanych struktur JSON
- Regex, obliczenia, manipulacje tablicami

## Przykład
```javascript
// Walidacja emaila własną regexem
const email = $input.first().json.email;
const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

return [{ json: { email, isValid, message: isValid ? 'OK' : 'Błędny email' } }];
```

<!--
"Code node to ucieczka gdy inne nodes nie dają rady. Używaj oszczędnie — każda linia kodu to potencjalny bug i coś czego klient nie może edytować w wizualnym edytorze."
-->


---
---

# Credential vault — jak działa

<div class="diagram-block">

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

</div>
**Zasada:** 1 credential = 1 konto/API key. Nigdy nie wklejaj kluczy w node'ach!

<!--
"Vault to sejf. Klucze API siedzą tam zaszyfrowane. Gdy workflow ich używa — n8n wstrzykuje je w tle. W logach executions nie widać wartości kluczy."
-->


---
---

# Mapa typów credentiali

| Typ | Kiedy używasz | Przykłady |
|-----|---------------|-----------|
| **API Key** | Serwis daje klucz API | OpenAI, Airtable, SendGrid |
| **Header Auth** | Klucz idzie w nagłówku HTTP | Większość własnych API |
| **Basic Auth** | Login + hasło | Stare API, intranety |
| **Bearer Token** | Token w nagłówku Authorization | GitHub, Stripe |
| **OAuth2** | "Zaloguj przez Google/Slack" | Gmail, Slack, Google Sheets |
| **Service Account** | Konto techniczne Google | Google Sheets, Drive, BigQuery |

<!--
"OAuth2 wygląda strasznie ale n8n robi to automatycznie — klikasz przycisk, loguje się do Google w przeglądarce, token wraca do n8n. Jak SSO."
-->


---
---

# OAuth2 — uproszczony flow

<div class="diagram-block">

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

</div>

**Tip:** Credential OAuth2 dla Gmail = dostęp do tej konkretnej skrzynki. Dla klienta — stwórz oddzielny credential.

<!--
"Tokeny OAuth2 wygasają co godzinę. n8n sam je odświeża w tle — ty tego nie widzisz. To magia."
-->


---
---

# Error handling — 3 strategie

## Strategia 1: Continue on Fail
- Node failuje → workflow idzie dalej z `error` w danych
- Użycie: gdy błąd jednego kroku nie blokuje pozostałych

## Strategia 2: Try/Catch Pattern
- IF node sprawdza czy `$json.error` istnieje
- Ścieżka true = obsługa błędu, ścieżka false = sukces

## Strategia 3: Error Trigger Workflow
- Oddzielny workflow który startuje gdy inny workflow pada
- Gold standard dla produkcji

<!--
"Strategia 1 = szybka, brzydka, działa. Strategia 3 = elegancka, skalowalna, polecam dla każdego workflow który idzie do klienta."
-->


---
---

# Flow error handling — diagram

<N8nFlow
  :nodes="[
    {icon: 'mdi:webhook', label: 'Webhook', variant: 'trigger'},
    {icon: 'mdi:check-circle', label: 'Walidacja', variant: 'default'},
    {icon: 'logos:google-sheets', label: 'Sheets', variant: 'action'},
    {icon: 'logos:gmail', label: 'Gmail', variant: 'action'},
    {icon: 'mdi:source-branch', label: 'IF: error?', variant: 'default'},
  ]"
/>

<div style="margin-top:0.8rem;background:#1E2D40;border-radius:8px;padding:0.8rem 1rem;border-left:3px solid #EF4444;font-size:0.8rem">
  <strong style="color:#EF4444">Error Workflow (oddzielny)</strong>
  <span style="color:#8096AA"> → Error Trigger → </span>
  <span style="color:#A8D8EA">Gmail do admina + Slack #alerty</span>
</div>


<!--
"W tym modelu: błąd nigdy nie ginie bez śladu. Admin zawsze dostaje powiadomienie. Klient nigdy nie widzi surowego błędu."
-->


---
---

# Error trigger workflow — setup

**Krok 1:** Stwórz nowy workflow "Error Handler"
**Krok 2:** Dodaj "Error Trigger" jako trigger
**Krok 3:** Dodaj logikę powiadomień (Gmail + Slack)
**Krok 4:** W głównym workflow → Settings → Error Workflow → wybierz "Error Handler"

## Dane dostępne w Error Trigger
```json
{
  "workflow": { "name": "Lead Capture", "id": "123" },
  "execution": { "id": "456", "url": "..." },
  "node": { "name": "Google Sheets", "type": "n8n-nodes-base.googleSheets" },
  "error": { "message": "The sheet doesn't exist", "stack": "..." }
}
```

<!--
"Jedna robota Error Handler workflow: daj znać co, gdzie i kiedy padło. Dobre powiadomienie zawiera: nazwę workflow, nazwę node'a, wiadomość błędu, link do execution."
-->


---
---

# Debugowanie — 5-krokowy przepis


<v-clicks>

1. **Kliknij czerwony node** — otwiera błąd
2. **Sprawdź Input** czerwonego node'a — czy dane w ogóle tam dotarły?
3. **Sprawdź Output** poprzedniego node'a — czy dane mają właściwy format?
4. **Pin Data** na poprzednim node'ie → "Test Step" tylko na problematycznym
5. **Console.log** w Code node jeśli nadal nie wiesz

</v-clicks>


## Top 3 przyczyny błędów

<v-clicks>

- Literówka w nazwie pola (`email` vs `Email` vs `e-mail`)
- Typ danych: string zamiast number
- Brakujące pole (null/undefined)

</v-clicks>


<!--
"90% bugów to dane. Nie kod, nie logika — po prostu coś nie ma tego co myślisz że ma."
-->


---
---

# Pin data — jak działa

```
NORMALNY FLOW:          PIN DATA FLOW:
[Webhook]               [Webhook] ← PINNED 📌
    ↓                       ↓ (używa zapisanych danych)
[Set]                   [Set]
    ↓                       ↓
[IF]                    [IF] ← "Test Step" uruchamia tylko ten node
```

## Jak pinować

<v-clicks>

1. Uruchom workflow raz (żeby node'y miały dane)
2. Kliknij node → zakładka Output → "Pin"
3. Teraz możesz testować downstream nodes bez triggerowania całości

</v-clicks>


<!--
"Pin Data to cheat code n8n. Nie musisz wysyłać formularza 20 razy żeby przetestować jeden node. Zapisujesz dane raz i testujesz w kółko."
-->


---
---

# Lead capture system — architektura

<N8nFlow
  :nodes="[
    {icon: 'mdi:form-select', label: 'FORMULARZ', desc: 'landing page', variant: 'default'},
    {icon: 'mdi:webhook', label: 'Webhook', desc: 'Trigger', variant: 'trigger'},
    {icon: 'mdi:check-decagram', label: 'Walidacja', desc: 'email + pola', variant: 'default'},
    {icon: 'logos:google-sheets', label: 'Sheets', desc: 'Append Row', variant: 'action'},
    {icon: 'logos:gmail', label: 'Gmail', desc: 'Email powitalny', variant: 'action'},
    {icon: 'logos:slack-icon', label: 'Slack', desc: '#leady notify', variant: 'output'},
  ]"
  caption="Każdy krok ma odpowiedź HTTP — klient nie widzi błędów, admin dostaje alerty"
/>


<!--
"To jest schemat który omawiamy. Każdy krok ma rację bytu — za chwilę zbudujemy go krok po kroku."
-->


---
---

# Walidacja danych — strategia

## Co walidujemy
- Wymagane pola: `email`, `name` (IF: isEmpty)
- Format emaila: regex `/^[^\s@]+@[^\s@]+\.[^\s@]+$/`
- Długość pól: name max 100 znaków
- Honeypot: ukryte pole formularza = bot detection

## Jak odpowiadamy na błąd walidacji
```json
{
  "success": false,
  "error": "Nieprawidłowy format adresu email",
  "field": "email"
}
```
HTTP 400 Bad Request

<!--
"Walidacja jest dla ciebie, nie dla klienta. Lepiej odrzucić śmieciowe dane na wejściu niż potem czyścić Google Sheets."
-->


---
---

# Deduplikacja — jak sprawdzić

**Problem:** Ten sam email może przyjść dwa razy (odświeżenie formularza, błąd użytkownika)

## Rozwiązanie: Google Sheets API
```
HTTP Request (GET):
URL: https://sheets.googleapis.com/v4/spreadsheets/
     {SHEET_ID}/values/A:A

Sprawdź: czy email jest w kolumnie A?
→ Tak: zwróć 200 "Już zarejestrowany"
→ Nie: idź dalej
```

**Alternatywa:** Użyj Google Sheets node z operacją "Read" + filter

<!--
"W większych systemach deduplikację robi baza danych. Dla kursowego projektu Google Sheets wystarczy. W produkcji przemysłowej — Supabase lub Airtable."
-->


---
---

# Google sheets Node — konfiguracja

## Operacja: Append or Update Row

| Pole | Wartość |
|------|---------|
| Credential | Google Sheets OAuth2 |
| Spreadsheet | (wybierz z listy lub ID) |
| Sheet | Leads |
| Matching Column | email |
| Columns to Send | email, name, message, source, timestamp |

## Przykładowy wiersz
```
jan@firma.pl | Jan Kowalski | Chcę automatyzację | Landing | 2026-03-27T10:30:00Z
```

<!--
"Append or Update = jeśli email istnieje to aktualizuje, jeśli nie — dodaje nowy wiersz. Mądrzejsze niż samo Append."
-->


---
---

# Gmail Node — email powitalny

## Konfiguracja
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

<!--
"Personalizacja to minimum — imię w temacie i treści. Różnica w open rate między 'Witamy' a 'Cześć Jan' to kilkanaście procent."
-->


---
---

# Slack Node — powiadomienie zespołu

## Konfiguracja
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

<!--
"Slack notification to dla zespołu. Ktoś musi zadzwonić do leada w ciągu godziny od zgłoszenia — to właśnie ta wiadomość inicjuje ten proces."
-->


---
---

# Zmienne środowiskowe w n8n

## Ustawienie w docker-compose.yml
```yaml
environment:
  - SHEETS_ID=1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms
  - SLACK_CHANNEL=#leady
  - ADMIN_EMAIL=kacper@dokodu.it
  - ENVIRONMENT=production
```

## Użycie w workflow
```javascript
{{ $env.SHEETS_ID }}
{{ $env.ADMIN_EMAIL }}
```

**Dlaczego:** Jeden workflow → wiele środowisk (dev/staging/prod) bez edycji node'ów

<!--
"Env vars to podstawa profesjonalnego n8n. Jeśli masz hardcoded ID arkusza w node'zie — to jest code smell. Wyciągaj do zmiennych."
-->


---
---

# Testing checklist — przed aktywacją

## Scenariusze które musisz przetestować

<v-clicks>

- [ ] Poprawny payload → lead zapisany, email wysłany, Slack powiadomiony
- [ ] Brak pola `email` → odpowiedź 400
- [ ] Błędny format emaila → odpowiedź 400
- [ ] Duplikat emaila → odpowiedź 200 "już istnieje"
- [ ] Google Sheets niedostępny → Error Handler workflow uruchomiony
- [ ] Gmail limit przekroczony → Error Handler workflow uruchomiony

</v-clicks>


<!--
"Test tylko happy path = workflow który pada przy pierwszym prawdziwym kliencie. Test wszystkich ścieżek błędów to różnica między amatorem a profesjonalistą."
-->


---
layout: two-cols-header
---

# Metryki i monitoring

<div class="col-header col-pos">Co śledzić po wdrożeniu</div>

- Execution Success Rate (cel: >99%)
- Average Execution Time (alarm gdy >5s)
- Failed Executions (alerty natychmiastowe)
- Lead Volume per Day (trend)

::right::

<div class="col-header col-neg">Gdzie</div>

- n8n → Executions panel (historia)
- n8n → Settings → Usage → metryki globalne
- Error Handler workflow → arkusz z błędami (loguj!)

<!--
"Nie wdrożysz i zapomnisz. Wdrożysz i monitorujesz. Production to nie test — tam chodzi prawdziwy biznes klienta."
-->


---
---

# Najczęstsze błędy początkujących

| Błąd | Problem | Rozwiązanie |
|------|---------|-------------|
| Klucz API w wyrażeniu | Widoczny w logach | Użyj Credential Vault |
| Brak Error Handling | Workflow pada cicho | Zawsze Error Trigger Workflow |
| Test URL w produkcji | Workflow nie startuje | Aktywuj + użyj Prod URL |
| Hardcoded ID | Nie da się skalować | Env vars |
| IF bez gałęzi false | Dane giną w próżni | Zawsze obsłuż false |

<!--
"Te błędy zrobiłem sam. Każdy je robi. Lepiej nauczyć się teraz niż w środku nocy gdy klient dzwoni że formularz nie działa."
-->


---
---

# Zadanie domowe

## Rozszerz Lead Capture o filtrowanie spamu

<v-clicks>

- Sprawdź czy pole `message` zawiera słowa kluczowe (np. "crypto", "casino", "SEO services")
- Jeśli tak → nie zapisuj, nie wysyłaj emaila
- Zamiast tego → zapisz do osobnego arkusza "Spam" z timestampem
- Opcjonalnie: dodaj własną listę słów kluczowych jako zmienną środowiskową

</v-clicks>


**Wskazówka:** IF node z warunkiem "contains" lub Code node z tablicą słów

<!--
"To nie jest trudne — jeden IF node i jeden dodatkowy arkusz. Ale zmusi cię do samodzielnego myślenia o przepływie danych. 30–45 minut."
-->


---
---

# Co będzie w tygodniu 2

## Tydzień 2: API i Dane

<v-clicks>

- HTTP Request w głąb (pagination, authentication, rate limiting)
- Transformacje danych: Merge, Split, Loop
- Zewnętrzne API: OpenAI, Airtable, Notion
- Projekt: Automatyczny raport z danych (agregacja z kilku źródeł → PDF)

</v-clicks>


<!--
"W tygodniu 2 wychodzimy poza formularze. Będziemy gadać z prawdziwymi API i łączyć dane z wielu źródeł. Przygotuj klucz OpenAI."
-->


---
---

# Podsumowanie tygodnia 1

## Umiesz już

<v-clicks>

- Zainstalować n8n i poruszać się po interfejsie
- Stworzyć workflow z Webhook, Schedule i Manual Trigger
- Używać 6 kluczowych nodes (HTTP Request, Set, IF, Switch, Code, NoOp)
- Bezpiecznie przechowywać klucze API w Credential Vault
- Obsługiwać błędy na 3 poziomach
- Debugować workflow jak profesjonalista

</v-clicks>


**Zbudowałeś:** Lead Capture System — coś co możesz wdrożyć u klienta.

<!--
"To nie jest mały krok. Lead Capture jest prostym przykładem ale wzorzec — webhook, walidacja, deduplikacja, akcja, powiadomienie, error handling — zobaczysz go w każdym poważnym projekcie n8n. Gratulacje."
-->
