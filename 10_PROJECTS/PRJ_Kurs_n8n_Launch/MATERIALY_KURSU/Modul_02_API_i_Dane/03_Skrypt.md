---
type: kurs-materialy
modul: 02
format: skrypt
dlugosc_szacunkowa: "2h 05min"
last_updated: 2026-03-27
---

# Skrypt — Tydzień 2: Język Sieci, API i Transformacje Danych

> **Legenda:**
> `[SLAJD N]` — przełącz na slajd N
> `[DEMO]` — przejdź do ekranu n8n
> `[PYTANIE]` — pauza retoryczna, daj chwilę na odpowiedź mentalną
> `[KAMERA]` — patrz w kamerę, nie w ekran

---

## INTRO (2 min)

`[KAMERA]`

Hej, witaj w Tygodniu 2 kursu n8n + AI dla Agencji i Firm.

W poprzednim tygodniu zbudowałeś swój pierwszy workflow. Trochę magii, dużo klikania, i coś — może nawet — zadziałało. Świetnie.

`[PYTANIE]`

Ale co tak naprawdę się dzieje kiedy n8n wysyła request do zewnętrznego API? Skąd wie jak zapytać? Co znaczy ten `$json` który wszędzie widzisz? I dlaczego czasem dostajesz odpowiedź, a czasem 401 i nic?

`[KAMERA]`

Odpowiedź brzmi: HTTP. JSON. Expressions. Trzy rzeczy, które jak je rozumiesz — zamieniasz n8n z "narzędzia do klikania" w "narzędzie do automatyzowania firm".

Ten tydzień to gramatyka internetu. Nie nudy — fundament.

Zaczynamy.

---

## SEGMENT 1: HTTP — Gramatyka Internetu

`[SLAJD 3]`

### Metody HTTP

Wyobraź sobie, że API to magazyn. Duży magazyn z tysiącami półek. Ty jesteś kurierem.

Kiedy przychodzisz do magazynu, nie krzyczysz po prostu "NIP 5213016711!" — magazynier nie wie co z tym zrobić.

Musisz powiedzieć co chcesz zrobić:

- **GET**: "Pokaż mi co masz na półce 5213016711."
- **POST**: "Mam nową paczkę, połóż ją na półce."
- **PUT**: "Wymień całą zawartość tej półki na tę nową."
- **PATCH**: "Zmień tylko etykietę na tej paczce."
- **DELETE**: "Zdejmij tę paczkę z półki."

`[PYTANIE]`

Kiedy ostatnio zalogowałeś się do jakiegoś serwisu — to był POST. Kiedy otworzyłeś stronę z listą klientów — to był GET. Dzieje się to miliardy razy dziennie i większość ludzi w ogóle o tym nie myśli.

My myślimy, bo musimy.

`[SLAJD 4]`

### Headers — Koperta Listu

Oprócz metody, każdy request ma headers. Myśl o nich jak o kopercie.

Treść listu to body — co wysyłasz. Koperta to headers — instrukcje dla poczty.

**Content-Type** mówi API: "Wysyłam ci JSON, nie formularz HTML." Jeśli wysyłasz JSON bez `Content-Type: application/json` — część API po prostu nie zrozumie co im przysłałeś.

**Authorization** to twój przepustka. Najczęściej `Bearer <token>`. Bez niego — 401. Z nieprawidłowym — też 401.

**Accept** mówi: "Chcę odpowiedź w JSON, nie XML." Nie zawsze respektowane, ale dobra praktyka.

`[DEMO]`

Dobra, dość teorii. Otwieramy n8n.

Tworzę nowy workflow. Dodaję HTTP Request node.

Wpisuję URL: `https://jsonplaceholder.typicode.com/users/1`

To jest testowe publiczne API — zero kluczy, zero rejestracji. Idealne do nauki.

Metoda: GET. Klikam "Test Step".

`[PAUZA — pokaż output]`

Widzisz? Mam JSON z danymi użytkownika. Imię, email, adres, firma. Teraz przełączam na zakładkę "Input" — tu widzisz co n8n wysłał. Zakładka "Output" — co dostał.

A teraz zmieniam na POST. Dodaję Body:
```json
{
  "title": "foo",
  "body": "bar",
  "userId": 1
}
```

Klikam Test Step. Dostałem 201 Created — zasób "stworzony". W realnym API to by był nowy rekord w bazie. Tutaj to fake, ale mechanizm identyczny.

---

## SEGMENT 2: HTTP Response Codes — Czytaj Odpowiedzi API

`[SLAJD 5]`

### Mapa Statusów

`[PYTANIE]`

Ile razy widziałeś w n8n czerwony node z napisem "Error"? I co robiłeś? Klikałeś retry bez czytania kodu błędu?

Zatrzymaj się. Kod HTTP to diagnoza. Jak numer błędu w warsztacie samochodowym.

Prosta zasada:

**2xx** — zielone światło. Masz co chciałeś.

**4xx** — twój błąd. Napraw request. 400 to zły JSON. 401 to brak tokena. 403 to dobry token, ale za mało uprawnień. 404 to go nie ma. 429 to za szybko.

**5xx** — ich błąd. Czekaj i retry. 500 to coś się posypało u nich. 503 to serwer wyłączony.

`[DEMO]`

Celowo wywołam błąd. Zmieniam URL na `https://jsonplaceholder.typicode.com/users/99999`.

Użytkownik 99999 nie istnieje. Klikam Test Step.

`[PAUZA — pokaż 404]`

404 Not Found. n8n pokazuje błąd czerwonym tłem. Ale to nie jest koniec świata.

`[SLAJD 6]`

### Rate Limiting

Specjalnie omówimy 429. Bo to najczęstszy problem przy masowych automatyzacjach.

Wyobraź sobie, że API to jeden kasjer w Biedronce. Ty masz 500 produktów. Jeśli rzucasz wszystkie na taśmę jednocześnie — kasjer się wywala.

API mówi ci "za szybko" przez 429 i często dołącza header `Retry-After: 60` — "wróć za minutę".

W n8n masz dwa narzędzia: **Wait node** i **Batch processing**. Pokażę to w projekcie tygodnia, ale zapamiętaj regułę: jeśli przetwarzasz więcej niż 50 elementów z requestem do zewnętrznego API — dodaj Wait node z 1 sekundą przerwy. Zawsze.

---

## SEGMENT 3: JSON — Szafa z Szufladami

`[SLAJD 7]`

### JSON przez Analogię

Teraz JSON. I obiecuję — po tym fragmencie już nigdy więcej nie będziesz się gubić w strukturze danych.

`[PYTANIE]`

Masz szafę w sypialni. Wyobraź sobie, że każda szuflada ma etykietę i coś w środku.

```json
{
  "imię": "Kacper",
  "wiek": 35,
  "firma": {
    "nazwa": "Dokodu",
    "miasto": "Warszawa"
  },
  "projekty": ["n8n Kurs", "AI Wdrożenie", "YouTube"]
}
```

Szafa to `{}`. Szuflada "imię" zawiera "Kacper". Szuflada "firma" zawiera... inną szafę. Szuflada "projekty" zawiera listę.

W n8n kiedy piszę `$json.firma.miasto` — to dosłownie: otwórz główną szafę, wyjmij szufladę "firma", z tej szafy wyjmij szufladę "miasto". Wynik: "Warszawa".

`[SLAJD 8]`

### Obiekty vs Tablice

`[PYTANIE]`

Co jeśli masz listę firm, nie jedną firmę?

```json
[
  { "nip": "5213016711", "nazwa": "Dokodu" },
  { "nip": "7010012211", "nazwa": "Kontrahent" }
]
```

To nie jest szafa. To jest regał z szafami. Każda szafa ma numer (0, 1, 2...).

`$json[0].nazwa` — regał, szafa numer 0, szuflada "nazwa". Wynik: "Dokodu".

**Dlaczego to ważne w n8n:** Kiedy HTTP Request zwraca tablicę — n8n domyślnie traktuje ją jako jeden item. Musisz użyć Item Lists → Split Out żeby każdy element tablicy stał się osobnym itemem w workflow. Inaczej przetworzysz tylko pierwszy albo w ogóle się wywalisz.

`[DEMO]`

Pokażę ci to na żywo. Robię GET do `https://jsonplaceholder.typicode.com/users` — zwraca tablicę 10 użytkowników.

`[PAUZA — pokaż output]`

Widzisz? Jeden item, a w nim tablica. Nie 10 itemów. Jeden.

Teraz dodaję Item Lists node w trybie "Split Out". Pole: tutaj n8n automatycznie to wykryje.

`[PAUZA — pokaż split output]`

Teraz 10 itemów. Każdy użytkownik jako osobny item. Dopiero teraz mogę przetwarzać każdego z osobna.

---

## SEGMENT 4: n8n Expressions — Twój Szwajcarski Scyzoryk

`[SLAJD 9]`

### Expressions Reference Card

Czas na mój ulubiony fragment. n8n Expressions to JavaScript w nawiasach klamrowych. I jest kilka zmiennych które musisz znać na pamięć.

**`$json`** — dane aktualnego item'a. To używasz 80% czasu.

**`$input.all()`** — wszystkie itemy wchodzące do node'a jako tablica.

**`$input.first()`** — pierwszy item. Przydatne kiedy wiesz że masz tylko jeden.

`[SLAJD 10]`

**`$node["NazwaNode"].json`** — dane z konkretnego wcześniejszego node'a. Niezbędne kiedy workflow się rozgałęzia i musisz sięgnąć wstecz.

**`$now`** — czas teraźniejszy jako obiekt Luxon. Możesz robić z nim cuda:
- `$now.toISO()` → "2026-03-27T14:30:00Z"
- `$now.minus({days: 7})` → tydzień temu
- `$now.toFormat('yyyy-MM-dd')` → "2026-03-27"

`[SLAJD 11]`

I moje ulubione — inline JavaScript w expressions:

```javascript
// Uppercase
{{ $json.name.toUpperCase() }}

// Usuń spacje i myślniki z NIP
{{ $json.nip.replace(/[\s-]/g, '') }}

// Wartość domyślna gdy null
{{ $json.company ?? 'Brak firmy' }}

// Prosty if/else
{{ $json.status === 'active' ? 'Aktywna' : 'Nieaktywna' }}
```

`[PYTANIE]`

Expressions to JavaScript. Dosłownie. Każda metoda JS działa. Split, trim, includes, startsWith. Jedyne ograniczenie — jedna linia. Jeśli masz więcej logiki — Code Node.

`[DEMO]`

Otwieramy Set node. Dodaję pole "nip_clean".

W wartości wpisuję: `{{ $json.nip.replace(/[\s-]/g, '') }}`

Wchodzę w expression editor — widzę live preview. Wpisuję testowe dane. Działa.

Teraz `$now.toFormat('yyyy-MM-dd')` — widzę dzisiejszą datę. To wejdzie w pole "data_weryfikacji" przy zapisie do bazy.

---

## SEGMENT 5: Code Node i Vibe Coding

`[SLAJD 12]`

### Kiedy Code Node

Wyrazy to jedno zdanie. Code Node to esej.

Kiedy masz prostą transformację — Expression. Kiedy masz:
- Kilka warunków naraz
- Pętlę przez items z mutacją stanu
- Parsowanie XML czy CSV
- Skomplikowane obliczenia

— to Code Node.

Struktura jest zawsze taka sama:

```javascript
const items = $input.all();
const result = [];

for (const item of items) {
  // twoja logika
  result.push({
    json: {
      ...item.json,    // zachowaj stare pola
      nowePole: "wartość"  // dodaj nowe
    }
  });
}

return result;
```

Wejście: `$input.all()`. Wyjście: tablica obiektów z kluczem `json`. Zawsze.

`[SLAJD 13]`

### Vibe Coding

`[KAMERA]`

Muszę ci powiedzieć jak naprawdę pracuję z Code Node.

Nie piszę kodu z pamięci. Współpracuję z AI. I to nie jest lenistwo — to efektywność.

Mam problem. Opisuję go AI. Dostaję kod. Wklejam. Testuję. Iteruję.

Nazywam to Vibe Coding. I pokażę ci jak to wygląda w praktyce.

`[SLAJD 14]`

Kluczowe w promptowaniu AI:
1. Powiedz że jesteś w n8n Code Node (JavaScript)
2. Daj przykładowe dane wejściowe — dosłownie wklej JSON
3. Opisz co chcesz dostać — też pokaż przykład outputu
4. Wspomnij edge case'y: "co jeśli pole nie istnieje"

`[DEMO]`

Otwieram ChatGPT. Wpisuję:

```
Jestem w n8n Code Node (JavaScript).
Moje wejście: { "nip": "521-30-16-711" }
Chcę: usunąć wszystkie spacje i myślniki z NIP,
sprawdzić że ma dokładnie 10 cyfr,
zwrócić { nip_clean: "5213016711", valid: true }.
Jeśli NIP ma złą długość, zwróć valid: false.
Nie używaj zewnętrznych bibliotek.
```

`[PAUZA — pokaż ChatGPT generuje kod]`

Dostałem kod. Kopiuję. Wklejam w Code Node. Klikam "Test Step".

`[PAUZA — pokaż że działa]`

Działa. 30 sekund od opisania problemu do działającego kodu.

`[KAMERA]`

Teraz celowo wpisuję zły NIP — za krótki. "12345". Test Step.

`[PAUZA — pokaż valid: false]`

valid: false. Edge case obsłużony.

Właśnie tak pracuję. Codziennie. Bez wstydu.

`[SLAJD 15]`

### Vibe Coding z Błędem

A co kiedy kod nie działa? Wklejam błąd z powrotem do AI.

```
Dostałem błąd: "TypeError: Cannot read properties
of undefined (reading 'replace')"

Mój kod:
[wklej kod]

Moje dane:
[wklej przykład]
```

AI poprawia. Wklejam poprawkę. Testuję. 90% przypadków — rozwiązane w jednej iteracji.

---

## SEGMENT 6: Transformacje i Pagination

`[SLAJD 16]`

### Item Lists

Wracamy do Split i Aggregate.

`[PYTANIE]`

Masz listę 100 NIP-ów w jednym item. Chcesz zapytać GUS API o każdy z osobna. Co robisz?

Split Out. Jeden item z tablicą → 100 osobnych itemów. Teraz workflow przetwarza każdy z osobna — HTTP Request dla każdego, Set node dla każdego, zapis dla każdego.

A potem? Chcesz zebrać wyniki w jeden JSON do wysłania w emailu. Aggregate. 100 itemów → jeden item z tablicą wyników.

`[DEMO]`

`[PAUZA — pokaż Item Lists w akcji]`

Widzisz jak dane "rozszerzają się" przez Split a potem "zwijają" przez Aggregate? To jest najczęstszy pattern w automatyzacjach masowych. Zapamiętaj.

`[SLAJD 17]`

### Pagination

Ostatnia rzecz przed projektem — pagination.

`[PYTANIE]`

API Allegro ma 5000 twoich ofert. Zwraca je po 100 naraz. Co robisz?

Albo robisz paginację ręcznie (IF node sprawdza czy jest `next_page`, Loop back), albo używasz wbudowanej paginacji HTTP Request node'a.

`[DEMO]`

W HTTP Request — zakładka "Pagination".

Mam do wyboru kilka trybów. Cursor based — wpisuję gdzie w odpowiedzi jest następny token. Page number — n8n automatycznie zwiększa numer strony.

Opcja "Return All" — n8n iteruje automatycznie do końca. Uwaga: przy dużych danych możesz trafić w timeout workflow. Wtedy lepiej przetwarzać stronicowo z pośrednim zapisem.

---

## PROJEKT TYGODNIA: Data Enrichment z GUS REGON API

`[SLAJD 19]`

### Architektura

Dobra, czas na projekt. To nie jest tutorial-toy. To jest workflow, który możesz wdrożyć u klienta.

Scenariusz: masz formularz onboardingowy. Klient wpisuje NIP. Automatycznie pobierasz pełne dane firmy z GUS — nazwa, adres, PKD, forma prawna.

Architektura:

1. Webhook przyjmuje NIP
2. Code Node normalizuje i waliduje NIP
3. Google Sheets lookup — może ten NIP już mamy? (cache)
4. Jeśli cache — zwróć dane z cache, nie pytaj GUS
5. Jeśli brak cache — zapytaj GUS REGON API
6. Code Node parsuje odpowiedź XML
7. Zapisz do Google Sheets
8. Zwróć JSON z danymi firmy

`[DEMO]`

`[KAMERA]`

Buduję to krok po kroku. Nie spiesz się oglądając — to jest dłuższy segment i celowo pokazuję każdy krok z detalami.

**Krok 1 — Webhook**

Dodaję Webhook node. Metoda: POST. Path: `/enrich-company`.

Klikam "Listen for test event". W Postman wysyłam:
```json
{ "nip": "521-30-16-711" }
```

Webhook łapie. Mam dane.

**Krok 2 — Normalize NIP**

Code Node. Kod (wygenerowałem wcześniej przez Vibe Coding):

```javascript
const items = $input.all();
const result = [];

for (const item of items) {
  const rawNip = String(item.json.nip || '');
  const cleanNip = rawNip.replace(/[\s\-\.]/g, '');
  const isValid = /^\d{10}$/.test(cleanNip);

  result.push({
    json: {
      ...item.json,
      nip_raw: rawNip,
      nip: cleanNip,
      nip_valid: isValid
    }
  });
}

return result;
```

**Krok 3 — Cache Check**

IF node: `{{ $json.nip_valid === false }}` → gałąź błędu (Respond Webhook z błędem "Invalid NIP").

Gałąź "true" (valid) → Google Sheets node, operacja "Lookup Row". Szukam NIP w arkuszu cache.

IF node: "Row found" → gałąź cache hit → Respond Webhook z danymi z Sheets.

Gałąź "no row" → idziemy do GUS.

`[SLAJD 18]`

**Krok 4 — GUS REGON API**

`[SLAJD 20]`

GUS REGON to SOAP API — starszy protokół, ale działa i jest bezpłatny.

Najpierw potrzebujemy sesji. HTTP Request do:
`https://Wyszukiwarkaregon.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc`

To SOAP — body jest XML. Pokażę to szczegółowo w blueprincie workflow (plik `05_Workflow_Blueprint.md`).

`[SLAJD 21]`

**Krok 5 — Debug**

Używam Pin Data żeby zamrozić odpowiedź GUS i testować parsowanie bez odpytywania API za każdym razem.

Prawy klik na node → "Pin Data". Teraz przy każdym Test Step — używa zamrożonych danych.

**Krok 6 — Parse Response**

Code Node. GUS zwraca XML → parsujemy do JSON, wyciągamy kluczowe pola.

Szczegółowy kod w blueprincie.

**Krok 7 — Save i Respond**

Google Sheets "Append Row" — zapisuje dane.

Respond Webhook — zwraca JSON z danymi firmy.

`[KAMERA]`

Testuję end-to-end. Wysyłam NIP przez Postman. Widzę jak każdy node zmienia kolor na zielony. Odpowiedź: pełne dane firmy w JSON.

Wysyłam ten sam NIP drugi raz. Tym razem — cache hit. Odpowiedź szybsza, bez zapytania do GUS.

To jest produkcyjny workflow.

---

## PODSUMOWANIE (2 min)

`[SLAJD 26]`

`[KAMERA]`

Co zrobiłeś w tym tygodniu:

HTTP — mówisz właściwym językiem do API. GET, POST, headers, kody statusów — to twój podstawowy słownik.

JSON — czytasz każdą strukturę danych. Obiekty, tablice, zagnieżdżenia — szafa z szufladami.

n8n Expressions — `$json`, `$input`, `$node`, `$now` — pełny arsenał gotowy do użycia.

Code Node i Vibe Coding — wiesz kiedy i jak. AI jest twoim junior developerem.

Transformacje — Set, Split, Aggregate, Pagination — reshapujesz dane jak chcesz.

Projekt — masz działający Data Enrichment z GUS API z cache.

`[SLAJD 27]`

Twoje zadania:

Ćwiczenie 1 — JSON Gym. 10 wyrażeń. 15 minut. Zrób to.

Ćwiczenie 2 — uproszczona wersja projektu. Bez GUS API — użyj mockowego endpointu. 40 minut.

Zadanie domowe — dodaj obsługę błędów. To co odróżnia workflow amatorski od produkcyjnego.

`[SLAJD 28]`

W Tygodniu 3: Sub-Workflows, monitoring, retry strategie, Queue Mode.

Wrzuć swój workflow JSON do komentarzy. Napiszę co poprawić.

Do zobaczenia.

---

> **Całkowita długość:** ~2h 05min (przy normalnym tempie mówienia, z pauzami na DEMO)
> **Liczba słów skryptu (mówiony tekst):** ~1800 słów
