---
type: kurs-materialy
modul: 02
format: prezentacja
slajdow: 28
last_updated: 2026-03-27
---

# Prezentacja — Tydzień 2: Język Sieci, API i Transformacje Danych

> **Format slajdów:** Ciemne tło (#1a1a2e lub black), accent kolor n8n orange (#FF6D5A). Font: Inter lub Geist. Bullet pointy — max 4 na slajd.

---

## Slajd 1: Tytuł

**Tydzień 2: Język Sieci, API i Transformacje Danych**
**n8n + AI dla Agencji i Firm**

*Podtytuł: "Naucz się rozmawiać z API — zanim API przestanie odbierać twoje połączenia"*

> 🎙️ NOTATKA: "W poprzednim tygodniu zbudowałeś swój pierwszy workflow. Teraz nauczymy się rozmawiać z resztą internetu. Każde API, każda usługa — to rozmowa. Dziś nauczysz się właściwego języka."

---

## Slajd 2: Co zbudujesz w tym tygodniu

**Projekt tygodnia: Data Enrichment z GUS REGON API**

- Webhook przyjmuje NIP firmy
- Zapytanie do GUS REGON → nazwa, adres, PKD, forma prawna
- Cache: nie odpytujesz API dwa razy dla tego samego NIP-u
- Wynik: JSON z pełnymi danymi firmy w Google Sheets

> 🎙️ NOTATKA: "To workflow, który możesz sprzedać klientowi za 500 zł. Poważnie — firmy płacą za enrichment danych. Dziś go zbudujesz."

---

## Slajd 3: HTTP Methods — Cheatsheet

### CHEATSHEET: HTTP Methods

| Metoda | Co robi | Analogia |
|--------|---------|---------|
| **GET** | Pobiera dane | Patrzysz na półkę w magazynie |
| **POST** | Tworzy nowy zasób | Kładziesz nową paczkę na półce |
| **PUT** | Zastępuje cały zasób | Wymieniasz paczkę na nową |
| **PATCH** | Modyfikuje część zasobu | Przyklejasz nową etykietę |
| **DELETE** | Usuwa zasób | Zdejmujesz paczkę z półki |

**Złota zasada:** GET = bezpieczne (bez efektów ubocznych). Reszta = zmienia stan serwera.

> 🎙️ NOTATKA: "Większość automatyzacji używa GET i POST. PUT/PATCH/DELETE pojawia się gdy integrujesz się z CRM, ERP — tam gdzie zarządzasz zasobami. Pamiętaj — nie ma POST zamiast GET bo 'tak wygodniej'. API tego nie wybaczy."

---

## Slajd 4: HTTP Headers — Co Mówisz Oprócz Treści

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

> 🎙️ NOTATKA: "Headers to metadane requestu. Dokumentacja API zawsze mówi jakich headerów wymaga. Jeśli dostajesz 401 — prawdopodobnie brakuje ci Authorization."

---

## Slajd 5: HTTP Response Codes — Mapa Statusów

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

> 🎙️ NOTATKA: "4xx = twój problem, napraw request. 5xx = ich problem, czekaj i retry. 429 = zwolnij, dodaj Wait node. To najważniejsza mapa w całym tygodniu."

---

## Slajd 6: Rate Limiting — Jak Nie Zbanować Się w API

### Dlaczego API Cię Blokuje

**Problem:** Wysyłasz 1000 requestów w ciągu sekundy → API blokuje IP/token

**Sygnały:**
- HTTP 429 Too Many Requests
- Header `Retry-After: 60` (czekaj 60 sekund)
- Header `X-RateLimit-Remaining: 0`

**Rozwiązania w n8n:**

1. **Wait node** — pauza między requestami (np. 1 sek)
2. **Batch size** — przetwarzaj 10 itemów naraz, nie 1000
3. **Exponential backoff** — retry po 1s → 2s → 4s → 8s
4. **Cache** — nie pytaj dwa razy o to samo

> 🎙️ NOTATKA: "Rate limiting to nie wróg — to umowa. API mówi ci: 'tyle możemy obsłużyć'. Twój workflow musi to respektować. Wait node to twój najlepszy przyjaciel przy masowych operacjach."

---

## Slajd 7: JSON — Szafa z Szufladami

### JSON = Szafa z Szufladami

```
Szafa = obiekt {}
Szuflada = klucz : wartość
Zawartość szuflady = string / number / boolean / null / tablica / inny obiekt
```

**Przykład:**
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

> 🎙️ NOTATKA: "Zapamiętaj tę szafę. Kiedy będziesz pisał expression `$json.adres.miasto` — to dosłownie 'otwórz szufladę adres, wyjmij szufladę miasto'. Jeśli szuflady nie ma — dostaniesz undefined, nie błąd. To ważne."

---

## Slajd 8: Obiekty vs Tablice — Kiedy Co

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

> 🎙️ NOTATKA: "90% problemów początkujących z n8n pochodzi z nierozumienia kiedy mają obiekt a kiedy tablicę. Jeśli expression zwraca '[object Object]' — masz tablicę, nie obiekt. Zaraz pokażę jak to rozgryźć."

---

## Slajd 9: n8n Expressions — Reference Card (część 1)

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

> 🎙️ NOTATKA: "To jest połowa tego co będziesz używał przez 80% czasu. `$json.pole` — proste. `$input.all().map()` — gdy masz wiele itemów i chcesz wyciągnąć jedno pole ze wszystkich."

---

## Slajd 10: n8n Expressions — Reference Card (część 2)

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

> 🎙️ NOTATKA: "Daty to osobny ból głowy. n8n używa biblioteki Luxon — jeśli potrzebujesz manipulacji datami, szukaj dokumentacji Luxon, nie n8n. To ta sama składnia."

---

## Slajd 11: n8n Expressions — Reference Card (część 3)

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

> 🎙️ NOTATKA: "Expressions to JavaScript. Dosłownie. Możesz użyć każdej metody JS — split, trim, replace, includes. Jedyne ograniczenie: jeden wyrażenie = jedna linia. Jeśli potrzebujesz więcej — Code Node."

---

## Slajd 12: Code Node — Kiedy Expressions Nie Wystarczą

### Kiedy Code Node, kiedy Expression?

**Expression wystarczy gdy:**
- Prosta transformacja jednego pola
- Warunkowe przypisanie wartości
- Formatowanie daty/stringa
- Filtrowanie tablicy

**Code Node gdy:**
- Logika wielostopniowa (if/else/switch)
- Pętla przez items z mutacją stanu
- Parsowanie XML, CSV, niestandardowych formatów
- Wywołanie zewnętrznej biblioteki npm (self-hosted)
- Skomplikowane obliczenia biznesowe

**Struktura Code Node (JavaScript):**
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

> 🎙️ NOTATKA: "Kluczowy pattern: wejście to `$input.all()`, wyjście to tablica obiektów z kluczem `json`. Jeśli zapomnisz zwrócić `{ json: ... }` — n8n wyrzuci błąd."

---

## Slajd 13: Vibe Coding — Flow AI + n8n

### Vibe Coding Flow: AI jako Junior Developer

```
┌─────────────────────────────────────────────────────┐
│                                                      │
│  1. OPISZ PROBLEM                                    │
│     "Mam obiekt z NIP-em, chcę go zwalidować        │
│      i znormalizować (usunąć spacje/myślniki)"       │
│                                                      │
│           ↓                                          │
│                                                      │
│  2. ZAPYTAJ AI                                       │
│     "Napisz funkcję dla n8n Code Node która..."      │
│     Podaj: przykładowe wejście + oczekiwane wyjście  │
│                                                      │
│           ↓                                          │
│                                                      │
│  3. WKLEJ I PRZETESTUJ                               │
│     Code Node → "Test Step" → sprawdź Output        │
│                                                      │
│           ↓                                          │
│                                                      │
│  4. ITERUJ                                           │
│     "Błąd: Cannot read property 'nip' of undefined"  │
│     → Wklej błąd do AI → popraw → testuj ponownie   │
│                                                      │
└─────────────────────────────────────────────────────┘
```

> 🎙️ NOTATKA: "Vibe Coding to nie lenistwo — to efektywność. Nie musisz znać każdej funkcji JS na pamięć. Musisz wiedzieć co chcesz osiągnąć i umieć to opisać. AI jest szybszy od Stack Overflow i nie ocenia głupich pytań."

---

## Slajd 14: Vibe Coding — Prompty które Działają

### Skuteczny Prompt do Code Node

**Szablon:**
```
Jestem w n8n Code Node (JavaScript).
Moje wejście: [opisz lub wklej przykładowy JSON]
Chcę osiągnąć: [opisz co ma się stać]
Moje wyjście powinno wyglądać: [przykładowy JSON]

Napisz kompletną funkcję Code Node.
Nie używaj zewnętrznych bibliotek.
Obsłuż przypadek gdy pole nie istnieje.
```

**Przykład:**
```
Jestem w n8n Code Node (JavaScript).
Wejście: { "nip": "521-30-16-711" }
Chcę: usunąć wszystkie spacje i myślniki z NIP,
       zwalidować że ma 10 cyfr,
       zwrócić { nip_clean: "5213016711", valid: true/false }
```

> 🎙️ NOTATKA: "Im bardziej konkretny prompt, tym lepszy kod. 'Napisz coś z NIPem' dostaniesz losowy kod. 'Wejście to X, wyjście to Y, obsłuż przypadek Z' — dostaniesz coś co działa za pierwszym razem."

---

## Slajd 15: Set Node — Reshaping Danych

### Set Node: Fabryka Struktury

**Tryby:**

**Manual Mapping** — masz kontrolę nad każdym polem:
```
output.firma_nazwa = input.company.legal_name
output.nip         = input.tax_id
output.data        = now()
```

**JSON Output** — wpisujesz surowy JSON (dobry do statycznych wartości)

**Add Fields** — dodajesz pola do istniejącej struktury (nie usuwasz)

**Pro tip:** Set node z opcją "Keep Only Set" usuwa wszystkie pola których nie zdefiniowałeś — idealne do czyszczenia odpowiedzi API przed zapisem do bazy.

> 🎙️ NOTATKA: "Set node to twój 'mapper'. Masz odpowiedź z GUS API z 40 polami, chcesz zachować 8 — Set node z 'Keep Only Set' i masz czysty output."

---

## Slajd 16: Item Lists — Split, Aggregate, Merge

### Item Lists: Zarządzanie Przepływem Danych

**Split Out** — jeden item z tablicą → wiele itemów:
```
[{ "firmy": ["Dokodu", "ACME", "Contoso"] }]
         ↓ Split Out (field: firmy)
{ "firmy": "Dokodu" }
{ "firmy": "ACME" }
{ "firmy": "Contoso" }
```

**Aggregate** — wiele itemów → jeden item z tablicą:
```
{ "nip": "521..." }
{ "nip": "701..." }  →  [{ "nips": ["521...", "701..."] }]
{ "nip": "899..." }
```

**Kiedy potrzebujesz Split:**
- API zwraca tablicę → przetwarzasz każdy element
- HTTP Request po każdym elemencie z listy

**Kiedy potrzebujesz Aggregate:**
- Zbierasz wyniki z wielu requestów
- Wysyłasz batch do jednego API

> 🎙️ NOTATKA: "Split i Aggregate to jak suwak — rozszerzasz dane żeby je przetworzyć, potem zwijasz z powrotem. To najczęstszy pattern w automatyzacjach masowych."

---

## Slajd 17: Pagination — Kiedy API Nie Daje Wszystkiego

### Pagination: Strony w Internecie

**Dlaczego istnieje paginacja:**
API nie chce wysłać ci 10 000 rekordów naraz. Wysyła strony po 100.

**Typy paginacji:**

1. **Page number:** `?page=1&per_page=100` → `?page=2&per_page=100`
2. **Offset:** `?offset=0&limit=100` → `?offset=100&limit=100`
3. **Cursor/Token:** odpowiedź zawiera `next_cursor`, używasz go w następnym requeście
4. **Link header:** odpowiedź zawiera `Link: <url>; rel="next"`

**W n8n HTTP Request:**
- Zakładka "Pagination"
- "Return All" — n8n automatycznie iteruje (jeśli API obsługuje standardowe paginacje)
- "Limit" — maksymalna liczba rekordów

> 🎙️ NOTATKA: "Jeśli API zwraca np. 100 rekordów ale wiesz że jest ich 5000 — sprawdź dokumentację paginacji. Brak obsługi paginacji to najczęstszy powód dla którego workflow 'działa ale nie ma wszystkich danych'."

---

## Slajd 18: GUS REGON API — Co to i Dlaczego

### GUS REGON API: Bezpłatna Baza Polskich Firm

**Co daje:**
- Pełna nazwa firmy i forma prawna
- Adres siedziby
- Kody PKD (główna działalność + dodatkowe)
- Status działalności (aktywna/zawieszona/wykreślona)
- Data rejestracji, REGON, KRS

**Dostęp:**
- Rejestracja na: `https://api.stat.gov.pl/Home/RegonApi`
- Klucz API: bezpłatny (do zastosowań komercyjnych wymaga umowy)
- Środowisko testowe: dostępne od razu

**Protokół:** SOAP/XML (nie REST/JSON) — ale n8n obsługuje

**Limit:** ~10 000 zapytań/miesiąc w wersji darmowej

> 🎙️ NOTATKA: "GUS REGON API to 'must know' dla każdego kto automatyzuje polskie firmy. KYC, onboarding klientów, walidacja NIP — wszędzie tam to się przydaje. I jest za darmo."

---

## Slajd 19: Architektura Projektu — Data Enrichment

### Workflow: NIP → Dane Firmy

```
[Webhook]
    │  POST { "nip": "5213016711" }
    ↓
[Normalize NIP]   ← Code Node: usuń spacje/myślniki, waliduj 10 cyfr
    │
    ↓
[Cache Check]     ← Google Sheets Lookup: czy ten NIP już był?
    │
   YES ──→ [Return Cache]  ← zwróć dane z Sheets
    │
   NO
    ↓
[GUS API Session] ← HTTP Request: pobierz klucz sesji
    ↓
[GUS GetFullReport] ← HTTP Request: zapytaj o NIP
    ↓
[Parse Response]  ← Code Node: XML → JSON, wyciągnij kluczowe pola
    ↓
[Save to Sheets]  ← Google Sheets Append
    ↓
[Respond Webhook] ← zwróć JSON z danymi firmy
```

> 🎙️ NOTATKA: "To jest produkcyjny workflow. Cache to nie luksus — to konieczność. GUS API ma limity. Bez cache jeden formularz wypełniany przez tę samą firmę 10 razy = 10 zapytań. Z cache = 1."

---

## Slajd 20: Error Handling — Nie Ufaj API

### Obrona przed Rzeczywistością

**Co może pójść nie tak:**
- NIP nie istnieje w GUS → pusty wynik
- GUS API timeout → 30 sek bez odpowiedzi
- Sieć pada w połowie → przerwany transfer
- Rate limit → 429
- Zła odpowiedź XML → błąd parsowania

**Twoje linie obrony w n8n:**

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

> 🎙️ NOTATKA: "Workflow bez obsługi błędów to tykająca bomba. Pierwsze uruchomienie działa. Drugie też. Trzydzieste — wywala się o 3 w nocy i budzisz się na ping z n8n. Obsługa błędów to miłość własna."

---

## Slajd 21: Debugging w n8n — Twoje Narzędzia

### Jak Debugować Workflow

**1. Execution Log**
Lewy panel → Executions → kliknij wykonanie → zobacz każdy node

**2. "Test Step" w edytorze**
Otwórz node → "Test Step" → dane wchodzą i wychodzą na żywo

**3. Pin Data**
Prawym na node → "Pin Data" → dane zamrożone, nie pobierają się z API przy testach

**4. console.log w Code Node**
```javascript
console.log('Debug:', JSON.stringify($input.first().json));
```
Widoczne w: Executions → [node] → Output → `console`

**5. Sticky Notes**
Dodaj notatkę do Canvas żeby pamiętać co robi dany node za 3 miesiące

> 🎙️ NOTATKA: "Pin Data to game changer. Nie musisz za każdym razem czekać na webhook albo odpytywać API przy testach. Zamrażasz dane i testujesz logikę transformacji w izolacji."

---

## Slajd 22: Zmienne i Sekrety w n8n

### Gdzie Trzymać Klucze API

**Nigdy nie wpisuj klucza API bezpośrednio w node!**

**Opcja 1: n8n Credentials** (rekomendowana)
- Settings → Credentials → New
- Używasz: zakładka "Credential" w HTTP Request node

**Opcja 2: n8n Variables**
- Settings → Variables
- Dostęp: `{{ $vars.NAZWA_ZMIENNEJ }}`
- Do wartości statycznych (nie sekretów)

**Opcja 3: Environment Variables** (self-hosted)
- `.env` plik lub docker-compose environment
- Dostęp: `{{ $env.NAZWA }}`

**Dlaczego to ważne:**
- Credentials są szyfrowane w bazie n8n
- Nie trafiają do logów wykonań
- Przy klonowaniu workflow — credentials nie są kopiowane

> 🎙️ NOTATKA: "Widziałem workflow na GitHubie z kluczami API wpisanymi w JSON. Dosłownie. Ludzie publikują workflow z sekretami. Nie bądź tą osobą."

---

## Slajd 23: Performance — Kiedy Workflow Zwalnia

### Optymalizacja Wolnych Workflowów

**Diagnoza:**
- Execution Log → czas każdego node'a
- Gdzie jest największy czas? API call? Pętla? Zapis do bazy?

**Typowe wąskie gardła:**

| Problem | Rozwiązanie |
|---------|-------------|
| 1000 HTTP requestów po kolei | Batch: 50 naraz + Wait node |
| Brak cache dla powtarzalnych danych | Google Sheets lookup / Redis |
| Ciężki Code Node na każdym itemie | Przenieś logikę do Set node jeśli możesz |
| Zapis po jednym rekordzie do bazy | Batch insert (Sheets: Append Many) |

**Reguła:** Jeden workflow, jeden cel. Nie rób w jednym workflow 15 rzeczy — podziel na sub-workflows.

> 🎙️ NOTATKA: "Subworkflows to temat Tygodnia 3. Ale zapamiętaj zasadę teraz: workflow powinien być jak funkcja w kodzie — robi jedną rzecz i robi ją dobrze."

---

## Slajd 24: Checklist — Przed Wdrożeniem na Produkcję

### Gotowość Produkcyjna

- [ ] Obsługa błędów: każdy HTTP Request ma "Continue On Error" lub Retry
- [ ] Walidacja wejścia: sprawdzasz czy dane mają sens zanim je przetworzyś
- [ ] Sekrety: wszystkie klucze API w Credentials, nie w node'ach
- [ ] Logging: Respond Webhook zawiera status + błąd w razie niepowodzenia
- [ ] Cache: nie odpytujesz zewnętrznych API bez powodu
- [ ] Rate limiting: Wait node tam gdzie API ma limity
- [ ] Testowanie: workflow przeszedł przez happy path + 3 edge case'y
- [ ] Dokumentacja: Sticky Notes opisują co robi workflow i dlaczego

> 🎙️ NOTATKA: "To jest lista którą sprawdzam przed każdym wdrożeniem u klienta. Workflow który nie ma tych rzeczy — nie wchodzi na produkcję. Zapisz to."

---

## Slajd 25: Vibe Coding — Zaawansowane Techniki

### Jak Pracować z AI Efektywnie

**Podaj kontekst, nie tylko pytanie:**
```
Pracuję z n8n (self-hosted, wersja 1.x).
Używam Code Node (JavaScript).
Dane wchodzące: [przykład JSON]
Problem: [konkretny opis]
```

**Iteruj z błędami:**
```
Dostałem błąd: "TypeError: Cannot read properties
of undefined (reading 'nip')"

Mój kod:
[wklej kod]

Moje dane wejściowe:
[wklej przykładowe dane]
```

**Poproś o refaktor:**
```
Ten kod działa, ale chcę żeby:
- Obsługiwał przypadek gdy pole X nie istnieje
- Był bardziej czytelny
- Zwracał błąd z sensowną wiadomością
```

> 🎙️ NOTATKA: "AI nie czyta w myślach. Im więcej kontekstu mu dasz, tym lepszy kod dostaniesz. Kopiuj i wklejaj — błędy, dane, kod. Nie parafrazuj."

---

## Slajd 26: Podsumowanie — Twój Nowy Arsenał

### Czego Nauczyłeś Się w Tym Tygodniu

**HTTP:**
- GET/POST/PUT/DELETE/PATCH — wiesz kiedy co
- Headers — Content-Type, Authorization, custom
- Kody statusów — 2xx/4xx/5xx i ich znaczenie

**JSON:**
- Obiekty vs tablice — czytasz każdą strukturę
- Zagnieżdżanie — dotrzesz do każdego pola

**n8n Expressions:**
- `$json`, `$input`, `$node`, `$now`, `$workflow` — pełny arsenał
- Manipulacja stringami, datami, tablicami inline

**Kod:**
- Code Node — kiedy i jak
- Vibe Coding — AI jako junior developer
- Debugging — Execution Log, Pin Data, console.log

**Transformacje:**
- Set node — reshaping danych
- Item Lists — Split/Aggregate
- Pagination — nie gubisz danych z dużych API

> 🎙️ NOTATKA: "To jest fundamenty. Reszta kursu to stosowanie tych narzędzi w coraz bardziej zaawansowanych scenariuszach. Jeśli cokolwiek jest niejasne — jest ćwiczenie 'JSON Gym'. Zrób je zanim przejdziesz do Tygodnia 3."

---

## Slajd 27: Ćwiczenia i Projekt

### Twoje Zadania na Ten Tydzień

**Ćwiczenie 1 — JSON Gym (15 min)**
10 wyrażeń do napisania w Expression Editor
Plik: `04_Cwiczenia.md`

**Ćwiczenie 2 — Mini Data Enrichment (40 min)**
Zbuduj uproszczony workflow NIP → dane GUS
Używa: Webhook + HTTP Request + Set + Google Sheets

**Zadanie Domowe — Error Handling (otwarte)**
Dodaj do projektu:
- Obsługa nieistniejącego NIP-u
- Timeout po 10 sek
- Logowanie błędów do osobnego Sheets

> 🎙️ NOTATKA: "Projekt tygodnia to real-world workflow. Nie tutorial-hello-world. Zachowaj go — przyda się przy wdrożeniu u pierwszego klienta który pyta o weryfikację kontrahentów."

---

## Slajd 28: Do Zobaczenia w Tygodniu 3

### Tydzień 3: Skalowanie i Odporność

**Co nas czeka:**
- Sub-Workflows — modularność i reużywalność
- Error handling na poziomie enterprise
- Monitoring i alerty
- Retry strategie i idempotentność
- Kolejkowanie (Queue Mode w n8n)

**Twoje zadanie przed Tygodniem 3:**
1. Dokończ projekt Data Enrichment
2. Dodaj obsługę błędów (zadanie domowe)
3. Wrzuć workflow JSON do komentarzy

> 🎙️ NOTATKA: "Tydzień 3 to gdzie oddzielamy amatorów od profesjonalistów. Każdy może zbudować workflow który działa w demo. Nieliczni budują workflow który działa w piątek o 23:00 kiedy klient wysyła 500 NIP-ów naraz. Do zobaczenia."
