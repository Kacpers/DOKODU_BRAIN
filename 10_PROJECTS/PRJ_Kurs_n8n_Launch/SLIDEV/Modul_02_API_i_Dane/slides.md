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
transition: fade
layout: cover
---

<img src="/dokodu_logo.png" style="height:28px;margin-bottom:1.8rem;opacity:0.92" alt="Dokodu" />

<div class="cover-tag">MODUŁ 02 — API I DANE</div>

# > Format slajdów: Ciemne tło (#1a1a2e lub black), accent kolor n8n orange (#FF6D5A). Font: Inter lub Geist. Bullet pointy — max 4 na slajd.


<p style="color:#E63946;font-weight:600">Kacper Sieradziński</p>
<p style="color:#8096AA;font-size:0.8rem;margin-top:0.2rem">dokodu.it</p>


---
---

# Tytuł

## Tydzień 2: Język Sieci, API i Transformacje Danych
## n8n + AI dla Agencji i Firm

*Podtytuł: "Naucz się rozmawiać z API — zanim API przestanie odbierać twoje połączenia"*

<!--
"W poprzednim tygodniu zbudowałeś swój pierwszy workflow. Teraz nauczymy się rozmawiać z resztą internetu. Każde API, każda usługa — to rozmowa. Dziś nauczysz się właściwego języka."
-->


---
---

# Co zbudujesz w tym tygodniu

## Projekt tygodnia: Data Enrichment z GUS REGON API


<v-clicks>

- Webhook przyjmuje NIP firmy
- Zapytanie do GUS REGON → nazwa, adres, PKD, forma prawna
- Cache: nie odpytujesz API dwa razy dla tego samego NIP-u
- Wynik: JSON z pełnymi danymi firmy w Google Sheets

</v-clicks>


<!--
"To workflow, który możesz sprzedać klientowi za 500 zł. Poważnie — firmy płacą za enrichment danych. Dziś go zbudujesz."
-->


---
---

# HTTP methods — cheatsheet

### CHEATSHEET: HTTP Methods

| Metoda | Co robi | Analogia |
|--------|---------|---------|
| **GET** | Pobiera dane | Patrzysz na półkę w magazynie |
| **POST** | Tworzy nowy zasób | Kładziesz nową paczkę na półce |
| **PUT** | Zastępuje cały zasób | Wymieniasz paczkę na nową |
| **PATCH** | Modyfikuje część zasobu | Przyklejasz nową etykietę |
| **DELETE** | Usuwa zasób | Zdejmujesz paczkę z półki |

**Złota zasada:** GET = bezpieczne (bez efektów ubocznych). Reszta = zmienia stan serwera.

<!--
"Większość automatyzacji używa GET i POST. PUT/PATCH/DELETE pojawia się gdy integrujesz się z CRM, ERP — tam gdzie zarządzasz zasobami. Pamiętaj — nie ma POST zamiast GET bo 'tak wygodniej'. API tego nie wybaczy."
-->


---
---

# HTTP headers — co mówisz oprócz treści

### Headers = Koperta Listu

**Content-Type** — "Co ci wysyłam"
```
Content-Type: application/json
Content-Type: multipart/form-data
```

**Authorization** — "Kim jestem"
```
Authorization: Bearer eyJhbGciOiJ...
Authorization: Basic dXNlcjpwYXNz
```

**Accept** — "W jakim formacie chcę odpowiedź"
```
Accept: application/json
```

**Custom headers** — "Wszystko co API wymaga specjalnie"
```
X-API-Key: twoj-sekretny-klucz
X-Request-ID: unique-id-do-tracowania
```

<!--
"Headers to metadane requestu. Dokumentacja API zawsze mówi jakich headerów wymaga. Jeśli dostajesz 401 — prawdopodobnie brakuje ci Authorization."
-->


---
---

# HTTP response codes — mapa statusów

### Mapa Kodów HTTP

```
2xx — Wszystko OK
  200 OK            → Masz to czego chciałeś
  201 Created       → Zasób został stworzony
  204 No Content    → Sukces, ale brak treści odpowiedzi

4xx — Twój błąd
  400 Bad Request   → Wysłałeś bzdury (zły JSON, brakuje pól)
  401 Unauthorized  → Brak lub zły token
  403 Forbidden     → Token OK, ale nie masz dostępu
  404 Not Found     → Tego zasobu nie ma
  422 Unprocessable → Format OK, ale dane nielogiczne
  429 Too Many Req. → Za szybko! Rate limit.

5xx — Ich błąd
  500 Server Error  → Coś się posypało po ich stronie
  502 Bad Gateway   → Proxy/load balancer problem
  503 Unavailable   → Serwer chwilowo wyłączony
```

<!--
"4xx = twój problem, napraw request. 5xx = ich problem, czekaj i retry. 429 = zwolnij, dodaj Wait node. To najważniejsza mapa w całym tygodniu."
-->


---
---

# Rate limiting — jak nie zbanować się w API

### Dlaczego API Cię Blokuje

**Problem:** Wysyłasz 1000 requestów w ciągu sekundy → API blokuje IP/token

## Sygnały
- HTTP 429 Too Many Requests
- Header `Retry-After: 60` (czekaj 60 sekund)
- Header `X-RateLimit-Remaining: 0`

## Rozwiązania w n8n

1. **Wait node** — pauza między requestami (np. 1 sek)
2. **Batch size** — przetwarzaj 10 itemów naraz, nie 1000
3. **Exponential backoff** — retry po 1s → 2s → 4s → 8s
4. **Cache** — nie pytaj dwa razy o to samo

<!--
"Rate limiting to nie wróg — to umowa. API mówi ci: 'tyle możemy obsłużyć'. Twój workflow musi to respektować. Wait node to twój najlepszy przyjaciel przy masowych operacjach."
-->


---
---

# JSON — szafa z szufladami

### JSON = Szafa z Szufladami

```
Szafa = obiekt {}
Szuflada = klucz : wartość
Zawartość szuflady = string / number / boolean / null / tablica / inny obiekt
```

## Przykład
```json
{
  "firma": "Dokodu",
  "nip": "5213016711",
  "adres": {
    "ulica": "Mokotowska 15",
    "miasto": "Warszawa"
  },
  "pracownicy": [
    {"imie": "Kacper", "rola": "CEO"},
    {"imie": "Alina",  "rola": "COO"}
  ],
  "aktywna": true
}
```

**Zasada:** Szuflady w szufladach = zagnieżdżanie. Listy = tablice `[]`.

<!--
"Zapamiętaj tę szafę. Kiedy będziesz pisał expression `$json.adres.miasto` — to dosłownie 'otwórz szufladę adres, wyjmij szufladę miasto'. Jeśli szuflady nie ma — dostaniesz undefined, nie błąd. To ważne."
-->


---
---

# Obiekty vs tablice — kiedy co

### Obiekt `{}` vs Tablica `[]`

**Obiekt** — jeden rekord, nazwane pola:
```json
{ "nip": "5213016711", "nazwa": "Dokodu sp. z o.o." }
```
Dostęp: `$json.nip` → `"5213016711"`

**Tablica** — lista rzeczy tego samego typu:
```json
["5213016711", "7010012211", "8990012345"]
```
Dostęp: `$json[0]` → `"5213016711"`

**Tablica obiektów** — lista rekordów:
```json
[
  { "nip": "5213016711", "nazwa": "Dokodu" },
  { "nip": "7010012211", "nazwa": "Kontrahent X" }
]
```
Dostęp: `$json[0].nazwa` → `"Dokodu"`

**Dlaczego ważne w n8n:** HTTP Response często zwraca tablicę → musisz zrobić Split Items żeby n8n przetworzył każdy element osobno.

<!--
"90% problemów początkujących z n8n pochodzi z nierozumienia kiedy mają obiekt a kiedy tablicę. Jeśli expression zwraca '[object Object]' — masz tablicę, nie obiekt. Zaraz pokażę jak to rozgryźć."
-->


---
---

# n8n expressions — reference card (część 1)

### Reference Card: Dane i Items

| Expression | Co zwraca | Przykład |
|-----------|-----------|---------|
| `$json` | Dane aktualnego item'a | `$json.email` |
| `$json?.pole` | Bezpieczne odczytanie (null zamiast błędu) | `$json?.company?.name` |
| `$input.first().json` | Dane pierwszego item'a | `$input.first().json.id` |
| `$input.all()` | Wszystkie itemy jako tablica | `$input.all().length` |
| `$input.item` | Aktualny item | `$input.item.json` |

### Filtrowanie i mapowanie

```javascript
// Wszystkie emaile z listy kontaktów
$input.all().map(i => i.json.email)

// Tylko aktywni
$input.all().filter(i => i.json.status === 'active')
```

<!--
"To jest połowa tego co będziesz używał przez 80% czasu. `$json.pole` — proste. `$input.all().map()` — gdy masz wiele itemów i chcesz wyciągnąć jedno pole ze wszystkich."
-->


---
---

# n8n expressions — reference card (część 2)

### Reference Card: Poprzednie Node'y i Workflow

| Expression | Co zwraca |
|-----------|-----------|
| `$node["NazwaNode"].json` | Dane z konkretnego node'a |
| `$node["NazwaNode"].json.pole` | Konkretne pole z node'a |
| `$('NazwaNode').item.json` | Alternatywna składnia |
| `$workflow.id` | ID bieżącego workflow |
| `$workflow.name` | Nazwa workflow |
| `$execution.id` | ID bieżącego wykonania |
| `$execution.resumeUrl` | URL do wznowienia (wait workflows) |

### Daty i czas

| Expression | Co zwraca |
|-----------|-----------|
| `$now` | Teraźniejszość (Luxon DateTime) |
| `$now.toISO()` | ISO 8601: `2026-03-27T14:30:00.000Z` |
| `$now.toFormat('yyyy-MM-dd')` | `2026-03-27` |
| `$now.minus({days: 7}).toISO()` | Tydzień temu |
| `$today` | Dziś o północy |

<!--
"Daty to osobny ból głowy. n8n używa biblioteki Luxon — jeśli potrzebujesz manipulacji datami, szukaj dokumentacji Luxon, nie n8n. To ta sama składnia."
-->


---
---

# n8n expressions — reference card (część 3)

### Reference Card: Triggersy i Env

| Expression | Co zwraca |
|-----------|-----------|
| `$trigger` | Dane z node'a triggera |
| `$vars.NAZWA` | Zmienna z n8n Variables (Settings → Variables) |
| `$env.NAZWA` | Zmienna środowiskowa serwera |
| `$secrets.NAZWA` | Secret z External Secrets (dla self-hosted) |

### Przydatne transformacje inline

```javascript
// Uppercase
{{ $json.name.toUpperCase() }}

// Trim whitespace
{{ $json.nip.replace(/\s|-/g, '') }}

// Conditional
{{ $json.status === 'active' ? 'Tak' : 'Nie' }}

// Fallback jeśli null
{{ $json.company ?? 'Brak firmy' }}
```

<!--
"Expressions to JavaScript. Dosłownie. Możesz użyć każdej metody JS — split, trim, replace, includes. Jedyne ograniczenie: jeden wyrażenie = jedna linia. Jeśli potrzebujesz więcej — Code Node."
-->


---
---

# Code Node — kiedy expressions nie wystarczą

### Kiedy Code Node, kiedy Expression?

## Expression wystarczy gdy
- Prosta transformacja jednego pola
- Warunkowe przypisanie wartości
- Formatowanie daty/stringa
- Filtrowanie tablicy

## Code Node gdy
- Logika wielostopniowa (if/else/switch)
- Pętla przez items z mutacją stanu
- Parsowanie XML, CSV, niestandardowych formatów
- Wywołanie zewnętrznej biblioteki npm (self-hosted)
- Skomplikowane obliczenia biznesowe

## Struktura Code Node (JavaScript)
```javascript
// Input: $input.all() — tablica itemów
// Output: zwróć tablicę itemów

const items = $input.all();
const result = [];

for (const item of items) {
  result.push({
    json: {
      ...item.json,
      nowePoler: "wartość"
    }
  });
}

return result;
```

<!--
"Kluczowy pattern: wejście to `$input.all()`, wyjście to tablica obiektów z kluczem `json`. Jeśli zapomnisz zwrócić `{ json: ... }` — n8n wyrzuci błąd."
-->


---
transition: fade
---

# Vibe coding — flow AI + n8n

<N8nFlow
  :nodes="[
    {icon: 'mdi:text-box-outline', label: 'OPISZ PROBLEM', desc: 'co chcesz osiągnąć', variant: 'default'},
    {icon: 'mdi:robot-outline', label: 'ZAPYTAJ AI', desc: 'wejście + wyjście + kontekst', variant: 'action'},
    {icon: 'mdi:play-circle-outline', label: 'WKLEJ I TESTUJ', desc: 'Code Node → Test Step', variant: 'output'},
    {icon: 'mdi:refresh', label: 'ITERUJ', desc: 'wklej błąd → popraw', variant: 'error'},
  ]"
  caption="Vibe Coding: AI jako junior developer — opisujesz, AI pisze, ty testujesz i iterujesz"
/>


<!--
"Vibe Coding to nie lenistwo — to efektywność. Nie musisz znać każdej funkcji JS na pamięć. Musisz wiedzieć co chcesz osiągnąć i umieć to opisać. AI jest szybszy od Stack Overflow i nie ocenia głupich pytań."
-->


---
---

# Vibe coding — prompty które działają

### Skuteczny Prompt do Code Node

## Szablon
```
Jestem w n8n Code Node (JavaScript).
Moje wejście: [opisz lub wklej przykładowy JSON]
Chcę osiągnąć: [opisz co ma się stać]
Moje wyjście powinno wyglądać: [przykładowy JSON]

Napisz kompletną funkcję Code Node.
Nie używaj zewnętrznych bibliotek.
Obsłuż przypadek gdy pole nie istnieje.
```

## Przykład
```
Jestem w n8n Code Node (JavaScript).
Wejście: { "nip": "521-30-16-711" }
Chcę: usunąć wszystkie spacje i myślniki z NIP,
       zwalidować że ma 10 cyfr,
       zwrócić { nip_clean: "5213016711", valid: true/false }
```

<!--
"Im bardziej konkretny prompt, tym lepszy kod. 'Napisz coś z NIPem' dostaniesz losowy kod. 'Wejście to X, wyjście to Y, obsłuż przypadek Z' — dostaniesz coś co działa za pierwszym razem."
-->


---
---

# Set Node — reshaping danych

### Set Node: Fabryka Struktury

## Tryby

**Manual Mapping** — masz kontrolę nad każdym polem:
```
output.firma_nazwa = input.company.legal_name
output.nip         = input.tax_id
output.data        = now()
```

**JSON Output** — wpisujesz surowy JSON (dobry do statycznych wartości)

**Add Fields** — dodajesz pola do istniejącej struktury (nie usuwasz)

**Pro tip:** Set node z opcją "Keep Only Set" usuwa wszystkie pola których nie zdefiniowałeś — idealne do czyszczenia odpowiedzi API przed zapisem do bazy.

<!--
"Set node to twój 'mapper'. Masz odpowiedź z GUS API z 40 polami, chcesz zachować 8 — Set node z 'Keep Only Set' i masz czysty output."
-->


---
transition: fade
---

# Item lists — split, aggregate, merge

<N8nBranch
  :source="{icon: 'mdi:database', label: 'DANE', desc: '1 item z tablicą'}"
  :branches="[
    {icon: 'mdi:arrow-split-vertical', label: 'Split Out', result: '1 → wiele itemów', variant: 'action'},
    {icon: 'mdi:arrow-collapse-vertical', label: 'Aggregate', result: 'wiele → 1 item', variant: 'output'},
  ]"
/>

<div style="margin-top:0.8rem;background:#1E2D40;border-radius:8px;padding:0.8rem 1rem;border-left:3px solid #3B82F6;font-size:0.8rem">
  <strong style="color:#3B82F6">Pattern:</strong>
  <span style="color:#A8D8EA"> Split → przetwórz każdy element → Aggregate → wyślij batch</span>
</div>


<!--
"Split i Aggregate to jak suwak — rozszerzasz dane żeby je przetworzyć, potem zwijasz z powrotem. To najczęstszy pattern w automatyzacjach masowych."
-->


---
---

# Pagination — kiedy API nie daje wszystkiego

### Pagination: Strony w Internecie

## Dlaczego istnieje paginacja
API nie chce wysłać ci 10 000 rekordów naraz. Wysyła strony po 100.

## Typy paginacji

1. **Page number:** `?page=1&per_page=100` → `?page=2&per_page=100`
2. **Offset:** `?offset=0&limit=100` → `?offset=100&limit=100`
3. **Cursor/Token:** odpowiedź zawiera `next_cursor`, używasz go w następnym requeście
4. **Link header:** odpowiedź zawiera `Link: <url>; rel="next"`

## W n8n HTTP Request
- Zakładka "Pagination"
- "Return All" — n8n automatycznie iteruje (jeśli API obsługuje standardowe paginacje)
- "Limit" — maksymalna liczba rekordów

<!--
"Jeśli API zwraca np. 100 rekordów ale wiesz że jest ich 5000 — sprawdź dokumentację paginacji. Brak obsługi paginacji to najczęstszy powód dla którego workflow 'działa ale nie ma wszystkich danych'."
-->


---
transition: fade
layout: two-cols-header
---

# GUS REGON API — co to i dlaczego

<div class="col-header col-pos">Co daje</div>

- Pełna nazwa firmy i forma prawna
- Adres siedziby
- Kody PKD (główna działalność + dodatkowe)
- Status działalności (aktywna/zawieszona/wykreślona)
- Data rejestracji, REGON, KRS

::right::

<div class="col-header col-neg">Dostęp</div>

- Rejestracja na: `https://api.stat.gov.pl/Home/RegonApi`
- Klucz API: bezpłatny (do zastosowań komercyjnych wymaga umowy)
- Środowisko testowe: dostępne od razu

<!--
"GUS REGON API to 'must know' dla każdego kto automatyzuje polskie firmy. KYC, onboarding klientów, walidacja NIP — wszędzie tam to się przydaje. I jest za darmo."
-->


---
transition: fade
---

# Architektura projektu — data enrichment

<N8nFlow
  :nodes="[
    {icon: 'mdi:webhook', label: 'Webhook', desc: 'POST {nip}', variant: 'trigger'},
    {icon: 'mdi:text-search', label: 'Normalize NIP', desc: 'Code Node', variant: 'default'},
    {icon: 'mdi:cached', label: 'Cache Check', desc: 'Sheets Lookup', variant: 'action'},
    {icon: 'mdi:api', label: 'GUS API', desc: 'HTTP Request', variant: 'action'},
    {icon: 'mdi:code-braces', label: 'Parse XML→JSON', desc: 'Code Node', variant: 'default'},
    {icon: 'logos:google-sheets', label: 'Save', desc: 'Sheets Append', variant: 'output'},
  ]"
  caption="Cache sprawdza czy NIP już był — jeśli tak, zwraca dane z Sheets bez odpytywania GUS"
/>


<!--
"To jest produkcyjny workflow. Cache to nie luksus — to konieczność. GUS API ma limity. Bez cache jeden formularz wypełniany przez tę samą firmę 10 razy = 10 zapytań. Z cache = 1."
-->


---
---

# Error handling — nie ufaj API

### Obrona przed Rzeczywistością

## Co może pójść nie tak
- NIP nie istnieje w GUS → pusty wynik
- GUS API timeout → 30 sek bez odpowiedzi
- Sieć pada w połowie → przerwany transfer
- Rate limit → 429
- Zła odpowiedź XML → błąd parsowania

## Twoje linie obrony w n8n

```
1. Walidacja wejścia (Code Node przed requestem)
   → nie odpytuj GUS jeśli NIP ma złą długość

2. HTTP Request → Settings → "On Error: Continue"
   → workflow nie pada, przekazuje błąd dalej

3. IF node po każdym API call
   → ścieżka success / ścieżka error

4. Retry on Fail
   → HTTP Request → "Retry on Fail: 3 razy, co 5 sek"

5. Respond Webhook z błędem
   → { error: "NIP not found", code: "GUS_NOT_FOUND" }
```

<!--
"Workflow bez obsługi błędów to tykająca bomba. Pierwsze uruchomienie działa. Drugie też. Trzydzieste — wywala się o 3 w nocy i budzisz się na ping z n8n. Obsługa błędów to miłość własna."
-->


---
---

# Debugging w n8n — twoje narzędzia

### Jak Debugować Workflow

## 1. Execution Log
Lewy panel → Executions → kliknij wykonanie → zobacz każdy node

## 2. "Test Step" w edytorze
Otwórz node → "Test Step" → dane wchodzą i wychodzą na żywo

## 3. Pin Data
Prawym na node → "Pin Data" → dane zamrożone, nie pobierają się z API przy testach

## 4. console.log w Code Node
```javascript
console.log('Debug:', JSON.stringify($input.first().json));
```
Widoczne w: Executions → [node] → Output → `console`

## 5. Sticky Notes
Dodaj notatkę do Canvas żeby pamiętać co robi dany node za 3 miesiące

<!--
"Pin Data to game changer. Nie musisz za każdym razem czekać na webhook albo odpytywać API przy testach. Zamrażasz dane i testujesz logikę transformacji w izolacji."
-->


---
---

# Zmienne i sekrety w n8n

### Gdzie Trzymać Klucze API

## Nigdy nie wpisuj klucza API bezpośrednio w node!

**Opcja 1: n8n Credentials** (rekomendowana)
- Settings → Credentials → New
- Używasz: zakładka "Credential" w HTTP Request node

## Opcja 2: n8n Variables
- Settings → Variables
- Dostęp: `{{ $vars.NAZWA_ZMIENNEJ }}`
- Do wartości statycznych (nie sekretów)

**Opcja 3: Environment Variables** (self-hosted)
- `.env` plik lub docker-compose environment
- Dostęp: `{{ $env.NAZWA }}`

## Dlaczego to ważne
- Credentials są szyfrowane w bazie n8n
- Nie trafiają do logów wykonań
- Przy klonowaniu workflow — credentials nie są kopiowane

<!--
"Widziałem workflow na GitHubie z kluczami API wpisanymi w JSON. Dosłownie. Ludzie publikują workflow z sekretami. Nie bądź tą osobą."
-->


---
---

# Performance — kiedy workflow zwalnia

### Optymalizacja Wolnych Workflowów

## Diagnoza
- Execution Log → czas każdego node'a
- Gdzie jest największy czas? API call? Pętla? Zapis do bazy?

## Typowe wąskie gardła

| Problem | Rozwiązanie |
|---------|-------------|
| 1000 HTTP requestów po kolei | Batch: 50 naraz + Wait node |
| Brak cache dla powtarzalnych danych | Google Sheets lookup / Redis |
| Ciężki Code Node na każdym itemie | Przenieś logikę do Set node jeśli możesz |
| Zapis po jednym rekordzie do bazy | Batch insert (Sheets: Append Many) |

**Reguła:** Jeden workflow, jeden cel. Nie rób w jednym workflow 15 rzeczy — podziel na sub-workflows.

<!--
"Subworkflows to temat Tygodnia 3. Ale zapamiętaj zasadę teraz: workflow powinien być jak funkcja w kodzie — robi jedną rzecz i robi ją dobrze."
-->


---
---

# Checklist — przed wdrożeniem na produkcję

### Gotowość Produkcyjna


<v-clicks>

- [ ] Obsługa błędów: każdy HTTP Request ma "Continue On Error" lub Retry
- [ ] Walidacja wejścia: sprawdzasz czy dane mają sens zanim je przetworzyś
- [ ] Sekrety: wszystkie klucze API w Credentials, nie w node'ach
- [ ] Logging: Respond Webhook zawiera status + błąd w razie niepowodzenia
- [ ] Cache: nie odpytujesz zewnętrznych API bez powodu
- [ ] Rate limiting: Wait node tam gdzie API ma limity
- [ ] Testowanie: workflow przeszedł przez happy path + 3 edge case'y
- [ ] Dokumentacja: Sticky Notes opisują co robi workflow i dlaczego

</v-clicks>


<!--
"To jest lista którą sprawdzam przed każdym wdrożeniem u klienta. Workflow który nie ma tych rzeczy — nie wchodzi na produkcję. Zapisz to."
-->


---
---

# Vibe coding — zaawansowane techniki

### Jak Pracować z AI Efektywnie

## Podaj kontekst, nie tylko pytanie
```
Pracuję z n8n (self-hosted, wersja 1.x).
Używam Code Node (JavaScript).
Dane wchodzące: [przykład JSON]
Problem: [konkretny opis]
```

## Iteruj z błędami
```
Dostałem błąd: "TypeError: Cannot read properties
of undefined (reading 'nip')"

Mój kod:
[wklej kod]

Moje dane wejściowe:
[wklej przykładowe dane]
```

## Poproś o refaktor
```
Ten kod działa, ale chcę żeby:
- Obsługiwał przypadek gdy pole X nie istnieje
- Był bardziej czytelny
- Zwracał błąd z sensowną wiadomością
```

<!--
"AI nie czyta w myślach. Im więcej kontekstu mu dasz, tym lepszy kod dostaniesz. Kopiuj i wklejaj — błędy, dane, kod. Nie parafrazuj."
-->


---
class: layout-takeaway
---

# Podsumowanie — twój nowy arsenał

### Czego Nauczyłeś Się w Tym Tygodniu

## HTTP
- GET/POST/PUT/DELETE/PATCH — wiesz kiedy co
- Headers — Content-Type, Authorization, custom
- Kody statusów — 2xx/4xx/5xx i ich znaczenie

## JSON
- Obiekty vs tablice — czytasz każdą strukturę
- Zagnieżdżanie — dotrzesz do każdego pola

## n8n Expressions
- `$json`, `$input`, `$node`, `$now`, `$workflow` — pełny arsenał
- Manipulacja stringami, datami, tablicami inline

## Kod
- Code Node — kiedy i jak
- Vibe Coding — AI jako junior developer
- Debugging — Execution Log, Pin Data, console.log

## Transformacje
- Set node — reshaping danych
- Item Lists — Split/Aggregate
- Pagination — nie gubisz danych z dużych API

<!--
"To jest fundamenty. Reszta kursu to stosowanie tych narzędzi w coraz bardziej zaawansowanych scenariuszach. Jeśli cokolwiek jest niejasne — jest ćwiczenie 'JSON Gym'. Zrób je zanim przejdziesz do Tygodnia 3."
-->


---
---

# Ćwiczenia i projekt

### Twoje Zadania na Ten Tydzień

## Ćwiczenie 1 — JSON Gym (15 min)
10 wyrażeń do napisania w Expression Editor
Plik: `04_Cwiczenia.md`

## Ćwiczenie 2 — Mini Data Enrichment (40 min)
Zbuduj uproszczony workflow NIP → dane GUS
Używa: Webhook + HTTP Request + Set + Google Sheets

## Zadanie Domowe — Error Handling (otwarte)
Dodaj do projektu:
- Obsługa nieistniejącego NIP-u
- Timeout po 10 sek
- Logowanie błędów do osobnego Sheets

<!--
"Projekt tygodnia to real-world workflow. Nie tutorial-hello-world. Zachowaj go — przyda się przy wdrożeniu u pierwszego klienta który pyta o weryfikację kontrahentów."
-->


---
---

# Do zobaczenia w tygodniu 3

### Tydzień 3: Skalowanie i Odporność

## Co nas czeka
- Sub-Workflows — modularność i reużywalność
- Error handling na poziomie enterprise
- Monitoring i alerty
- Retry strategie i idempotentność
- Kolejkowanie (Queue Mode w n8n)

## Twoje zadanie przed Tygodniem 3
1. Dokończ projekt Data Enrichment
2. Dodaj obsługę błędów (zadanie domowe)
3. Wrzuć workflow JSON do komentarzy

<!--
"Tydzień 3 to gdzie oddzielamy amatorów od profesjonalistów. Każdy może zbudować workflow który działa w demo. Nieliczni budują workflow który działa w piątek o 23:00 kiedy klient wysyła 500 NIP-ów naraz. Do zobaczenia."
-->


---
class: layout-exercise
---

# Ćwiczenia praktyczne

Czas na praktykę! Otwórz n8n i zrób ćwiczenia samodzielnie.


---
class: layout-exercise
---

# Ćwiczenie 1 — JSON gym (15 min)


Nauczyć się pisać wyrażenia n8n jak z automatu — bez zaglądania do dokumentacji.


---
class: layout-exercise
---

# Ćwiczenie 2 — NIP lookup (40 min)


Zbudować kompletny workflow produkcyjny: Webhook → HTTP Request → transformacja danych → odpowiedź z danymi firmy.

## Kroki

<v-clicks>

- Webhook node (5 min)
- Walidacja NIP (5 min)
- HTTP Request do API GUS (15 min)
- Obsługa "nie znaleziono" (5 min)
- Transformacja danych (8 min)
- Odpowiedź (2 min)

</v-clicks>



---
class: layout-exercise
---

# Ćwiczenie 3 — vibe coding: kalkulator VAT (20 min)


Nauczyć się efektywnie współpracować z AI przy pisaniu Code Node. Zrozumieć kiedy Code Node, a kiedy Set node.

## Kroki

<v-clicks>

- Dane wejściowe
- Prompt do AI (użyj dokładnie tego)
- Kod wynikowy do porównania
- Nauka: Code Node vs Set Node
- Debugging (bonus, 5 min)

</v-clicks>



---
class: layout-exercise
---

# Zadanie domowe — cache dla NIP lookup

**Czas:** szacunkowo 45–60 min

Rozbuduj workflow NIP Lookup o warstwę cache — jeśli NIP był już wcześniej sprawdzany, zwróć dane z Google Sheets zamiast odpytywać API (szybciej + nie przeciążasz publicznego API).

## Checkpointy

<v-clicks>

- Poprawnie odpytuje API przy pierwszym wywołaniu dla nowego NIP
- Przy ponownym wywołaniu tego samego NIP — zwraca dane z Sheets (bez API call — zweryfikuj w Execution log że HTTP Request node sie nie wykonał)
- Odpowiedź zawiera pole `source` z wartością `"cache"` lub `"api"`
- Walidacja NIP działa (błędny NIP → 400, nieznany NIP → 404)
- Arkusz Sheets jest uzupełniany po każdym nowym NIP

</v-clicks>



---
class: layout-exercise
---

# Podsumowanie ćwiczeń


