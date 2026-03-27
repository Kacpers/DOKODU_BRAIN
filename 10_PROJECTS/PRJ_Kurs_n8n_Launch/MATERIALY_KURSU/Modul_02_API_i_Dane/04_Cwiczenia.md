---
type: kurs-materialy
modul: 02
format: cwiczenia
tytuł: "Tydzień 2: Ćwiczenia — API i Dane"
czas_całkowity: "75 min + zadanie domowe"
last_updated: 2026-03-27
---

# Ćwiczenia — Tydzień 2: API i Dane

> **Instrukcja dla kursanta:** Ćwiczenia wykonujesz samodzielnie, po obejrzeniu nagrań. Masz wszystko czego potrzebujesz — n8n (lokalny lub cloud), dostęp do internetu i ChatGPT/Copilot. Jeśli utkniesz — sprawdź hinty na końcu każdego ćwiczenia, zanim otworzysz rozwiązanie.

---

## Ćwiczenie 1 — JSON Gym (15 min)

**Cel:** Nauczyć się pisać wyrażenia n8n jak z automatu — bez zaglądania do dokumentacji.

**Jak pracować:** Otwórz n8n, utwórz nowy workflow. Dodaj node `Code` z poniższym JSON jako dane testowe (wklej jako Mock Data lub użyj `Set` node w trybie JSON Output). Dla każdego pytania wpisz wyrażenie w Expression Editor i sprawdź czy odpowiedź się zgadza.

**Dane testowe — wklej do Set node (JSON Output):**

```json
{
  "id": 42,
  "status": "active",
  "contact": {
    "email": "jan.kowalski@firma.pl",
    "phone": "+48 500 123 456",
    "address": {
      "city": "Warszawa",
      "zip": "00-001",
      "street": "Marszałkowska 1"
    }
  },
  "company": {
    "name": "Firma Kowalski Sp. z o.o.",
    "nip": "5213016711",
    "employees": 47,
    "premium": true
  },
  "tags": ["automation", "b2b", "manufacturing"],
  "invoices": [
    { "id": "INV-001", "amount": 4900, "paid": true },
    { "id": "INV-002", "amount": 9800, "paid": false },
    { "id": "INV-003", "amount": 2450, "paid": true }
  ],
  "created_at": "2026-01-15T09:30:00.000Z",
  "score": null
}
```

---

### Poziom 1 — Proste pola (zacznij tutaj)

**Pytanie 1.1:** Wyciągnij ID kontaktu (liczba 42).

**Odpowiedź:** `{{ $json.id }}`

---

**Pytanie 1.2:** Pobierz status jako tekst z wielką literą na początku.

**Odpowiedź:** `{{ $json.status.charAt(0).toUpperCase() + $json.status.slice(1) }}`

> **Dlaczego:** JavaScript string methods działają bezpośrednio w Expression Editor. n8n to środowisko JS — wszystkie metody `.toUpperCase()`, `.slice()`, `.replace()` są dostępne.

---

**Pytanie 1.3:** Sprawdź czy kontakt jest premium (zwróć `true` lub `false`).

**Odpowiedź:** `{{ $json.company.premium }}`

---

### Poziom 2 — Zagnieżdżone obiekty

**Pytanie 1.4:** Wyciągnij email z zagnieżdżonego obiektu `contact`.

**Odpowiedź:** `{{ $json.contact.email }}`

---

**Pytanie 1.5:** Pobierz miasto z trójpoziomowej struktury `contact.address.city`.

**Odpowiedź:** `{{ $json.contact.address.city }}`

---

**Pytanie 1.6:** Zbuduj pełny adres jako jeden string: "Marszałkowska 1, 00-001 Warszawa".

**Odpowiedź:** `{{ $json.contact.address.street }}, {{ $json.contact.address.zip }} {{ $json.contact.address.city }}`

---

**Pytanie 1.7:** Pobierz NIP firmy — ale zabezpiecz się na wypadek gdyby pole `company` nie istniało (użyj optional chaining).

**Odpowiedź:** `{{ $json.company?.nip ?? 'brak NIP' }}`

> **Dlaczego `?.` i `??`:** Operator `?.` zwraca `undefined` zamiast rzucać błąd gdy pole nie istnieje. Operator `??` (nullish coalescing) zwraca prawą stronę gdy lewa to `null` lub `undefined`. W produkcyjnych workflow to standard — API nigdy nie zwracają danych w 100% konsekwentnie.

---

### Poziom 3 — Tablice

**Pytanie 1.8:** Pobierz pierwszy tag z tablicy `tags`.

**Odpowiedź:** `{{ $json.tags[0] }}`

---

**Pytanie 1.9:** Policz ile faktur ma ten kontakt.

**Odpowiedź:** `{{ $json.invoices.length }}`

---

**Pytanie 1.10:** Wyfiltruj faktury niezapłacone i zwróć ich łączną kwotę.

**Odpowiedź:** `{{ $json.invoices.filter(inv => !inv.paid).reduce((sum, inv) => sum + inv.amount, 0) }}`

> **Dlaczego to ważne:** `.filter()` + `.reduce()` to najczęściej używana kombinacja przy agregacji danych z API. Zapamiętaj ten wzorzec — wróci w każdym projekcie e-commerce, CRM, ERP.

---

**Bonus — trudniejsze:**

**Pytanie 1.11:** Sprawdź czy kontakt ma tag "b2b" (zwróć `true`/`false`).

**Odpowiedź:** `{{ $json.tags.includes('b2b') }}`

**Pytanie 1.12:** Zwróć ID wszystkich zapłaconych faktur jako string rozdzielony przecinkami: "INV-001, INV-003".

**Odpowiedź:** `{{ $json.invoices.filter(inv => inv.paid).map(inv => inv.id).join(', ') }}`

---

## Ćwiczenie 2 — NIP Lookup (40 min)

**Cel:** Zbudować kompletny workflow produkcyjny: Webhook → HTTP Request → transformacja danych → odpowiedź z danymi firmy.

**API:** `https://api.dane.gov.pl/api/institutions/search` — publiczne API Ministerstwa Cyfryzacji, bez klucza, bez rejestracji.

**Efekt końcowy:** Wyślesz do webhooka `{"nip": "5213016711"}` i dostaniesz z powrotem nazwę firmy, adres, REGON.

---

### Krok 1 — Webhook node (5 min)

1. Dodaj node **Webhook**.
2. HTTP Method: `POST`
3. Path: `nip-lookup`
4. Response Mode: `Last Node` (wyślemy odpowiedź na końcu)
5. Skopiuj URL webhooka — przyda się do testów.

**Jak testować:** Użyj `curl` w terminalu lub Postman/Insomnia:

```bash
curl -X POST https://TWOJ-N8N.com/webhook/nip-lookup \
  -H "Content-Type: application/json" \
  -d '{"nip": "5213016711"}'
```

Możesz też użyć darmowego [webhook.site](https://webhook.site) jako klienta testowego.

---

### Krok 2 — Walidacja NIP (5 min)

Zanim odpytasz API, sprawdź czy NIP jest poprawny.

1. Dodaj node **IF**.
2. Warunek: `{{ $json.body.nip }}` → **Is Not Empty**
3. Dodaj drugi warunek (AND): `{{ $json.body.nip.replace(/[^0-9]/g, '').length }}` → **Equal** → `10`

> **Wyjaśnienie:** Czyścimy NIP z myślników i spacji, sprawdzamy czy ma dokładnie 10 cyfr. Jeśli nie — wracamy od razu z błędem zamiast odpytywać API.

**Na gałęzi FALSE** dodaj node **Respond to Webhook**:
- Response Code: `400`
- Response Body (JSON): `{"error": "Nieprawidłowy NIP — wymagane 10 cyfr"}`

---

### Krok 3 — HTTP Request do API GUS (15 min)

1. Na gałęzi **TRUE** z IF node dodaj **HTTP Request**.
2. Konfiguracja:

| Pole | Wartość |
|------|---------|
| Method | `GET` |
| URL | `https://api.dane.gov.pl/api/institutions/search` |
| Authentication | None |

3. W zakładce **Query Parameters** dodaj:
   - Name: `filters[nip]` → Value: `{{ $json.body.nip.replace(/[^0-9]/g, '') }}`

4. W zakładce **Settings** włącz **Continue On Error: true** (obsłużymy błędy ręcznie).

**Test:** Kliknij "Test Step" — powinieneś zobaczyć odpowiedź z tablicą `data` zawierającą instytucje. Jeśli zwróci pustą tablicę `[]` — NIP nie istnieje w bazie.

---

### Krok 4 — Obsługa "nie znaleziono" (5 min)

1. Dodaj **IF** po HTTP Request.
2. Warunek: `{{ $json.meta.count }}` → **Equal** → `0`

**Na gałęzi TRUE (nie znaleziono)** dodaj **Respond to Webhook**:
- Response Code: `404`
- Body: `{"error": "Nie znaleziono firmy dla podanego NIP", "nip": "{{ $node['Webhook'].json.body.nip }}"}`

---

### Krok 5 — Transformacja danych (8 min)

Na gałęzi **FALSE** (znaleziono) dodaj **Set** node w trybie Manual Mapping:

| Pole wyjściowe | Wyrażenie |
|---------------|-----------|
| `nip` | `{{ $node['Webhook'].json.body.nip }}` |
| `nazwa` | `{{ $json.data[0].attributes.title }}` |
| `regon` | `{{ $json.data[0].attributes.regon }}` |
| `miasto` | `{{ $json.data[0].attributes.city }}` |
| `kod_pocztowy` | `{{ $json.data[0].attributes.zip }}` |
| `ulica` | `{{ $json.data[0].attributes.street }}` |
| `status` | `"found"` |

> **Tip:** Struktura odpowiedzi API może się różnić. Zawsze najpierw przejrzyj surową odpowiedź w panelu Output — dopiero potem mapuj pola.

---

### Krok 6 — Odpowiedź (2 min)

Dodaj **Respond to Webhook**:
- Response Code: `200`
- Response Body: zaznacz **Use Input Data as JSON Body**

**Test końcowy:** Wyślij ponownie `{"nip": "5213016711"}` — powinieneś dostać JSON z danymi firmy Microsoft Poland.

---

### Typowe błędy i jak je naprawić

| Problem | Przyczyna | Rozwiązanie |
|---------|-----------|-------------|
| `403 Forbidden` | Brakujący header `Accept` | Dodaj header `Accept: application/json` |
| Puste `data[]` | NIP z myślnikami lub spacjami | Użyj `.replace(/[^0-9]/g, '')` przed wysłaniem |
| `Cannot read property 'attributes' of undefined` | Dostęp do `$json.data[0]` gdy tablica pusta | Najpierw sprawdź `$json.meta.count > 0` |
| Timeout (10+ sekund) | API GUS ma chwilowe spowolnienia | Zwiększ timeout w HTTP Request → Settings do 30s |

---

## Ćwiczenie 3 — Vibe Coding: Kalkulator VAT (20 min)

**Cel:** Nauczyć się efektywnie współpracować z AI przy pisaniu Code Node. Zrozumieć kiedy Code Node, a kiedy Set node.

**Zadanie:** Zbuduj Code Node który przyjmuje kwotę netto i zwraca:
- kwotę netto
- VAT 23%
- kwotę brutto
- sformatowane stringi do faktury

---

### Krok 1 — Dane wejściowe

Utwórz **Set** node z danymi:

```json
{
  "produkt": "Licencja n8n Pro",
  "kwota_netto": 4900,
  "waluta": "PLN"
}
```

---

### Krok 2 — Prompt do AI (użyj dokładnie tego)

Otwórz ChatGPT lub Copilot i wklej:

```
Napisz kod do n8n Code Node (JavaScript) który:
1. Pobiera kwotę netto z $input.first().json.kwota_netto
2. Liczy VAT 23%
3. Liczy kwotę brutto
4. Zwraca obiekt z polami: kwota_netto, vat_kwota, kwota_brutto (wszystkie jako liczby, zaokrąglone do 2 miejsc po przecinku)
5. Dodaje pola string: kwota_netto_str, kwota_brutto_str w formacie "4 900,00 PLN" (z separatorem tysięcy jako spacja, przecinek dziesiętny)
6. Pole waluta przepisuje z inputu

Zwróć tablicę items zgodnie ze standardem n8n.
Użyj prostego kodu bez zewnętrznych bibliotek.
```

---

### Krok 3 — Kod wynikowy do porównania

Po wygenerowaniu przez AI porównaj z referencyjnym kodem:

```javascript
const item = $input.first().json;
const kwotaNetto = parseFloat(item.kwota_netto);
const vatStawka = 0.23;

const vatKwota = Math.round(kwotaNetto * vatStawka * 100) / 100;
const kwotaBrutto = Math.round((kwotaNetto + vatKwota) * 100) / 100;

function formatujKwote(kwota, waluta) {
  return new Intl.NumberFormat('pl-PL', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(kwota) + ' ' + waluta;
}

return [{
  json: {
    produkt: item.produkt,
    waluta: item.waluta,
    kwota_netto: kwotaNetto,
    vat_kwota: vatKwota,
    kwota_brutto: kwotaBrutto,
    kwota_netto_str: formatujKwote(kwotaNetto, item.waluta),
    kwota_brutto_str: formatujKwote(kwotaBrutto, item.waluta)
  }
}];
```

---

### Krok 4 — Nauka: Code Node vs Set Node

Po przetestowaniu odpowiedz sobie na pytania:

**Kiedy Set node:**
- Proste mapowanie pól (zmień nazwę, skopiuj wartość)
- Łączenie stringów (`{{ $json.imie + ' ' + $json.nazwisko }}`)
- Ustawianie stałych wartości
- Filtrowanie pól (Keep Only Set)

**Kiedy Code Node:**
- Logika warunkowa z wieloma przypadkami (`if/else if/else`)
- Operacje matematyczne z zaokrąglaniem i formatowaniem
- Przetwarzanie tablic (`.map()`, `.filter()`, `.reduce()` na wielu itemach naraz)
- Algorytmy walidacji (np. suma kontrolna NIP)
- Parsowanie niestandardowych formatów (XML → JSON, CSV z escape'ami)

> **Zasada kciuka:** Jeśli potrzebujesz więcej niż 2-3 linii kodu — użyj Code Node. Jeśli wyrażenie mieści się w jednej linii — Set node. Code Node jest czytelniejszy i łatwiejszy do debugowania.

---

### Krok 5 — Debugging (bonus, 5 min)

Dodaj do Code Node linię `console.log()` i znajdź output:

```javascript
console.log('Dane wejściowe:', JSON.stringify(item));
console.log('Kwota brutto:', kwotaBrutto);
```

Gdzie to znaleźć: **Executions** w lewym panelu n8n → kliknij ostatnie wykonanie → otwórz Code Node → zakładka **Logs**.

---

## Zadanie Domowe — Cache dla NIP Lookup

**Czas:** szacunkowo 45–60 min

**Cel:** Rozbuduj workflow NIP Lookup o warstwę cache — jeśli NIP był już wcześniej sprawdzany, zwróć dane z Google Sheets zamiast odpytywać API (szybciej + nie przeciążasz publicznego API).

---

### Architektura rozwiązania

```
Webhook
  ↓
Walidacja NIP
  ↓
[NOWE] Google Sheets "Lookup Row"
  — sprawdź kolumnę NIP
  ↓
IF: znaleziono w cache?
  ├── TAK → zwróć dane z Sheets (bez API call)
  └── NIE → HTTP Request do API GUS
               ↓
             [NOWE] Google Sheets "Append Row"
               — zapisz wynik do cache
               ↓
             Respond to Webhook
```

---

### Wymagania

1. **Arkusz Google Sheets** z kolumnami: `nip`, `nazwa`, `regon`, `miasto`, `kod_pocztowy`, `ulica`, `data_dodania`
2. **Google Sheets "Lookup Row"** — node szuka po kolumnie `nip`
3. **IF node** sprawdza czy Lookup zwrócił wynik — użyj `{{ $json.nip }}` Is Not Empty
4. **Jeśli cache HIT** — workflow zwraca dane z arkusza + dodatkowe pole `source: "cache"`
5. **Jeśli cache MISS** — workflow odpytuje API, zapisuje do arkusza, zwraca dane + pole `source: "api"`
6. **Pole `data_dodania`** — zapisz datę w formacie ISO: `{{ $now.toISO() }}`

---

### Kryteria zaliczenia

Workflow jest zaliczony gdy spełnia wszystkie:

- [ ] Poprawnie odpytuje API przy pierwszym wywołaniu dla nowego NIP
- [ ] Przy ponownym wywołaniu tego samego NIP — zwraca dane z Sheets (bez API call — zweryfikuj w Execution log że HTTP Request node sie nie wykonał)
- [ ] Odpowiedź zawiera pole `source` z wartością `"cache"` lub `"api"`
- [ ] Walidacja NIP działa (błędny NIP → 400, nieznany NIP → 404)
- [ ] Arkusz Sheets jest uzupełniany po każdym nowym NIP

---

### Hinty (odkryj tylko jeśli utkniesz)

<details>
<summary>Hint 1 — jak sprawdzić czy Lookup zwrócił wynik</summary>

Google Sheets Lookup Row zwraca błąd gdy wiersz nie istnieje. Włącz **Continue On Error** w tym nodzie. Następnie sprawdź `{{ $json.error }}` — jeśli istnieje, to cache MISS.

Alternatywnie: użyj wyrażenia `{{ Object.keys($json).length > 0 }}` — jeśli Sheets zwróciło dane, obiekt nie będzie pusty.

</details>

<details>
<summary>Hint 2 — jak dodać pole source do obu ścieżek</summary>

Na obu gałęziach (cache i API) dodaj **Set** node który doda pole `source`. Na gałęzi cache: ustaw stały string `"cache"`. Na gałęzi API: ustaw `"api"`. Następnie obie gałęzie połącz **Merge** node (mode: Combine) przed Respond to Webhook.

</details>

<details>
<summary>Hint 3 — błąd "Cannot read property of undefined" przy Sheets</summary>

Google Sheets Lookup zwraca dane w formacie `$json.nip` (nie `$json.data[0].nip`). Sprawdź surowy output klikając "Test Step" na Sheets nodzie — zawsze rób to zanim zaczniesz mapować.

</details>

---

### Pytania do samodzielnej refleksji

Po ukończeniu zadania zastanów się:

1. Ile requestów do API zaoszczędzisz gdyby workflow obsługiwał 1000 wywołań dziennie dla 50 unikalnych NIP-ów?
2. Jak długo powinien być ważny cache? Dane firm w GUS mogą się zmienić — czy `data_dodania` wystarczy do implementacji TTL (time-to-live)?
3. Co się stanie gdy dwie instancje workflow uruchomią się jednocześnie dla tego samego NIP — czy jest ryzyko duplikatu w Sheets?

> Odpowiedź na pytanie 3 to temat Tygodnia 4 (Idempotność i Mutex w n8n). Zapamiętaj pytanie.

---

## Podsumowanie ćwiczeń

Po ukończeniu wszystkich ćwiczeń potrafisz:

- Pisać dowolne wyrażenia n8n — proste, zagnieżdżone, na tablicach
- Budować workflow z zewnętrznym API od zera (webhook → HTTP → transformacja → odpowiedź)
- Obsługiwać błędy API jak profesjonalista: walidacja wejścia, 404, 400, timeouty
- Używać AI do pisania Code Node (Vibe Coding) i wiedzieć kiedy to ma sens
- Implementować podstawowy cache z Google Sheets

**Wrzuć screenshot swojego workflow do grupy — z polem `source: "cache"` w odpowiedzi.** Pokaż że cache działa.
