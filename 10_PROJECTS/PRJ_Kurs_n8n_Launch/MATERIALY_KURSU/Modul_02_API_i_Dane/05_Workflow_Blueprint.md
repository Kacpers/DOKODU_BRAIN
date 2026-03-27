---
type: blueprint
module: "02 — API i Dane"
title: "Data Enrichment NIP → Dane firmy (GUS REGON API)"
difficulty: intermediate
estimated_time: 60 min
author: Kacper Sieradziński / Dokodu
last_reviewed: 2026-03-27
tags: [n8n, webhook, GUS, REGON, NIP, enrichment, cache, google-sheets, code-node, SOAP]
---

# Blueprint 05 — Data Enrichment NIP → Dane firmy (GUS REGON API)

> Workflow pobiera dane firmy z rejestru GUS REGON na podstawie numeru NIP. Zawiera walidację (cyfry + suma kontrolna), cache w Google Sheets i pełne parsowanie odpowiedzi SOAP.

---

## Architektura workflow (ASCII)

```
                    ┌──────────────────────────────┐
                    │   Webhook Trigger (POST)      │
                    │   /webhook/enrich-nip         │
                    └─────────────┬────────────────┘
                                  │
                    ┌─────────────▼────────────────┐
                    │  Code Node — Walidacja NIP    │
                    │  (10 cyfr + suma kontrolna)   │
                    └──────────┬───────┬────────────┘
                               │       │
                           VALID│       │INVALID
                               │       │
            ┌──────────────────▼┐     ┌▼──────────────────────┐
            │ Google Sheets      │     │ Respond — błąd 400    │
            │ Sprawdź cache      │     │ { "error": "..." }    │
            │ (Lookup po NIP)    │     └───────────────────────┘
            └──────────┬─────────┘
                       │
            ┌──────────▼──────────┐
            │ IF — Cache hit?     │
            │ (dane znalezione?)  │
            └───┬─────────────┬───┘
                │             │
            HIT │             │ MISS
                │             │
  ┌─────────────▼──┐         ┌▼────────────────────────┐
  │ Respond        │         │ HTTP Request             │
  │ (dane z cache) │         │ GUS REGON API (SOAP)     │
  └────────────────┘         │ Pobierz dane po NIP      │
                             └──────────┬───────────────┘
                                        │
                             ┌──────────▼───────────────┐
                             │ Code Node                 │
                             │ Parsuj XML + normalizuj   │
                             └──────────┬───────────────┘
                                        │
                             ┌──────────▼───────────────┐
                             │ Google Sheets             │
                             │ Zapisz do cache           │
                             └──────────┬───────────────┘
                                        │
                             ┌──────────▼───────────────┐
                             │ Respond to Webhook        │
                             │ Zwróć dane firmy (JSON)   │
                             └──────────────────────────┘
```

---

## Lista nodes z konfiguracją

### Node 1 — Webhook Trigger

| Parametr | Wartość |
|---|---|
| **Typ** | Webhook |
| **Nazwa** | `Webhook — Enrich NIP` |
| **HTTP Method** | POST |
| **Path** | `enrich-nip` |
| **Respond** | Using 'Respond to Webhook' Node |
| **Authentication** | Header Auth (produkcja: `X-API-Key`) |

**Przykładowy payload wejściowy:**

```json
{
  "nip": "5213003600"
}
```

---

### Node 2 — Code Node: Walidacja NIP

| Parametr | Wartość |
|---|---|
| **Typ** | Code |
| **Nazwa** | `Code — Walidacja NIP` |
| **Language** | JavaScript |
| **Mode** | Run Once for All Items |

**Kod JavaScript (walidacja + suma kontrolna):**

```javascript
// Walidacja NIP: 10 cyfr + algorytm sumy kontrolnej
const items = $input.all();

for (const item of items) {
  const rawNip = String(item.json.nip ?? '').replace(/[\s\-]/g, '');

  // Sprawdź czy dokładnie 10 cyfr
  if (!/^\d{10}$/.test(rawNip)) {
    item.json._valid = false;
    item.json._error = `NIP musi zawierać dokładnie 10 cyfr. Podano: "${rawNip}"`;
    continue;
  }

  // Algorytm sumy kontrolnej NIP (wagi: 6,5,7,2,3,4,5,6,7)
  const weights = [6, 5, 7, 2, 3, 4, 5, 6, 7];
  const digits = rawNip.split('').map(Number);

  const sum = weights.reduce((acc, w, i) => acc + w * digits[i], 0);
  const checkDigit = sum % 11;

  // Suma kontrolna 10 jest nieprawidłowa (NIP nie może mieć cyfry kontrolnej 10)
  if (checkDigit === 10) {
    item.json._valid = false;
    item.json._error = `NIP "${rawNip}" ma nieprawidłową sumę kontrolną (wynik: 10).`;
    continue;
  }

  if (checkDigit !== digits[9]) {
    item.json._valid = false;
    item.json._error = `NIP "${rawNip}" ma błędną cyfrę kontrolną. Oczekiwano: ${checkDigit}, podano: ${digits[9]}.`;
    continue;
  }

  item.json._valid = true;
  item.json._nip_clean = rawNip;
}

// Rozdziel na valid / invalid
const valid = items.filter(i => i.json._valid);
const invalid = items.filter(i => !i.json._valid);

// Wyrzuć błąd dla pierwszego nieprawidłowego (workflow trafi do error path)
if (invalid.length > 0) {
  throw new Error(invalid[0].json._error);
}

return valid;
```

> Jeśli walidacja rzuci błąd (`throw new Error(...)`), n8n automatycznie kieruje do gałęzi błędu lub zatrzymuje workflow. Dodaj **Error Trigger** node lub obsłuż błąd przez `Try/Catch` w Settings node.

**Alternatywa z IF zamiast throw:**
Jeśli chcesz rozgałęzić flow zamiast rzucać błąd, zmień logikę: nie rzucaj `throw`, zwróć wszystkie items z polem `_valid`, a następnie podłącz **IF node** sprawdzający `{{ $json._valid === true }}`.

---

### Node 3 — Google Sheets: Sprawdź cache

| Parametr | Wartość |
|---|---|
| **Typ** | Google Sheets |
| **Nazwa** | `Sheets — Cache NIP` |
| **Operation** | Lookup |
| **Credential** | `Google Sheets OAuth2` |
| **Spreadsheet ID** | `{{ $env.NIP_CACHE_SHEET_ID }}` |
| **Sheet Name** | `Cache` |
| **Lookup Column** | `NIP` |
| **Lookup Value** | `{{ $json._nip_clean }}` |
| **Return All Matches** | false |
| **Options → Continue If Empty** | true |

---

### Node 4 — IF: Cache hit?

| Parametr | Wartość |
|---|---|
| **Typ** | IF |
| **Nazwa** | `IF — Cache hit?` |
| **Condition type** | Object |
| **Value 1** | `{{ $json.NIP }}` |
| **Operation** | Is Not Empty |

**Gałęzie:**
- `TRUE` → Respond (dane z cache, bez wywołania GUS)
- `FALSE` → HTTP Request do GUS REGON API

---

### Node 5 — HTTP Request: GUS REGON API (SOAP)

| Parametr | Wartość |
|---|---|
| **Typ** | HTTP Request |
| **Nazwa** | `HTTP — GUS REGON API` |
| **Method** | POST |
| **URL** | `https://wyszukiwarkaregon.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc` (produkcja) |
| **URL testowa** | `https://wyszukiwarkaregon.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc` (sandbox: patrz niżej) |
| **Authentication** | None (auth przez SOAP header) |
| **Content Type** | Raw / Custom |
| **Body Content Type** | `text/xml; charset=utf-8` |

**Headers:**

| Nagłówek | Wartość |
|---|---|
| `Content-Type` | `text/xml; charset=utf-8` |
| `SOAPAction` | `http://CIS/BIR/PUBL/2014/07/IUslugaBIRzewnPubl/DaneSzukajPodmioty` |

**Body (SOAP envelope — wyszukiwanie po NIP):**

```xml
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope
  xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
  xmlns:ns="http://CIS/BIR/PUBL/2014/07">
  <soap:Header>
    <ns:SessionHeader>
      <ns:SessionKey>{{ $env.GUS_SESSION_KEY }}</ns:SessionKey>
    </ns:SessionHeader>
  </soap:Header>
  <soap:Body>
    <ns:DaneSzukajPodmioty>
      <ns:pParametryWyszukiwania>
        <ns:Nip>{{ $json._nip_clean }}</ns:Nip>
      </ns:pParametryWyszukiwania>
    </ns:DaneSzukajPodmioty>
  </soap:Body>
</soap:Envelope>
```

> **UWAGA:** GUS REGON API wymaga najpierw wywołania `Zaloguj` (login), które zwraca `SessionKey`. W pełnej implementacji dodaj node `HTTP — GUS Login` przed tym krokiem (patrz sekcja "Instrukcja rejestracji").

**Przykładowa odpowiedź SOAP (XML):**

```xml
<?xml version="1.0" encoding="utf-8"?>
<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope">
  <s:Body>
    <DaneSzukajPodmiotyResponse xmlns="http://CIS/BIR/PUBL/2014/07">
      <DaneSzukajPodmiotyResult>
        <![CDATA[<?xml version="1.0" encoding="utf-8"?>
        <root>
          <dane>
            <Regon>015249924</Regon>
            <Nip>5213003600</Nip>
            <StatusNip/>
            <Nazwa>ASSECO POLAND SPÓŁKA AKCYJNA</Nazwa>
            <Województwo>PODKARPACKIE</Województwo>
            <Powiat>rzeszowski</Powiat>
            <Gmina>Rzeszów</Gmina>
            <Miejscowosc>Rzeszów</Miejscowosc>
            <KodPocztowy>35-322</KodPocztowy>
            <Ulica>ul. Olchowa</Ulica>
            <NrNieruchomosci>14</NrNieruchomosci>
            <NrLokalu/>
            <Typ>P</Typ>
            <SilosID>6</SilosID>
            <DataZakonczeniaDzialalnosci/>
            <MiejscowoscPoczty>Rzeszów</MiejscowoscPoczty>
          </dane>
        </root>]]>
      </DaneSzukajPodmiotyResult>
    </DaneSzukajPodmiotyResponse>
  </s:Body>
</s:Envelope>
```

---

### Node 6 — Code Node: Parsuj i normalizuj odpowiedź GUS

| Parametr | Wartość |
|---|---|
| **Typ** | Code |
| **Nazwa** | `Code — Parsuj GUS response` |
| **Language** | JavaScript |
| **Mode** | Run Once for All Items |

**Kod JavaScript:**

```javascript
// Parsowanie odpowiedzi SOAP z GUS REGON API
const items = $input.all();
const results = [];

for (const item of items) {
  const rawXml = item.json.data ?? '';

  // Wyciągnij CDATA z DaneSzukajPodmiotyResult
  const cdataMatch = rawXml.match(/<DaneSzukajPodmiotyResult[^>]*>([\s\S]*?)<\/DaneSzukajPodmiotyResult>/);

  if (!cdataMatch) {
    throw new Error('Nie znaleziono DaneSzukajPodmiotyResult w odpowiedzi GUS');
  }

  // Usuń otoczkę CDATA jeśli obecna
  let innerXml = cdataMatch[1].replace(/<!\[CDATA\[/g, '').replace(/\]\]>/g, '').trim();

  // Sprawdź czy odpowiedź nie jest pusta (NIP nie znaleziony)
  if (!innerXml || innerXml.includes('<root/>') || innerXml.includes('<root></root>')) {
    throw new Error(`Nie znaleziono podmiotu dla NIP: ${item.json._nip_clean ?? 'brak'}`);
  }

  // Pomocnicza funkcja do wyciągania wartości tagów XML
  const getTag = (xml, tag) => {
    const match = xml.match(new RegExp(`<${tag}>([^<]*)<\/${tag}>`));
    return match ? match[1].trim() : '';
  };

  // Mapowanie pól GUS → znormalizowany obiekt
  const firma = {
    nip:           getTag(innerXml, 'Nip'),
    regon:         getTag(innerXml, 'Regon'),
    nazwa:         getTag(innerXml, 'Nazwa'),
    typ:           getTag(innerXml, 'Typ') === 'P' ? 'Prawna' : 'Fizyczna',
    adres: {
      ulica:       getTag(innerXml, 'Ulica'),
      nr_nieruch:  getTag(innerXml, 'NrNieruchomosci'),
      nr_lokalu:   getTag(innerXml, 'NrLokalu'),
      kod_pocztowy:getTag(innerXml, 'KodPocztowy'),
      miejscowosc: getTag(innerXml, 'Miejscowosc'),
      gmina:       getTag(innerXml, 'Gmina'),
      powiat:      getTag(innerXml, 'Powiat'),
      wojewodztwo: getTag(innerXml, 'Województwo'),
    },
    status_nip:    getTag(innerXml, 'StatusNip') || 'aktywny',
    aktywna:       !getTag(innerXml, 'DataZakonczeniaDzialalnosci'),
    zrodlo:        'GUS_REGON',
    pobrano_at:    new Date().toISOString(),
  };

  // Pełny adres jako string (dla cache)
  firma.adres_pelny = [
    firma.adres.ulica,
    firma.adres.nr_nieruch,
    firma.adres.nr_lokalu,
    firma.adres.kod_pocztowy,
    firma.adres.miejscowosc,
  ].filter(Boolean).join(' ');

  results.push({ json: firma });
}

return results;
```

**Przykładowe dane wyjściowe po parsowaniu:**

```json
{
  "nip": "5213003600",
  "regon": "015249924",
  "nazwa": "ASSECO POLAND SPÓŁKA AKCYJNA",
  "typ": "Prawna",
  "adres": {
    "ulica": "ul. Olchowa",
    "nr_nieruch": "14",
    "nr_lokalu": "",
    "kod_pocztowy": "35-322",
    "miejscowosc": "Rzeszów",
    "gmina": "Rzeszów",
    "powiat": "rzeszowski",
    "wojewodztwo": "PODKARPACKIE"
  },
  "adres_pelny": "ul. Olchowa 14 35-322 Rzeszów",
  "status_nip": "aktywny",
  "aktywna": true,
  "zrodlo": "GUS_REGON",
  "pobrano_at": "2026-03-27T10:30:00.000Z"
}
```

---

### Node 7 — Google Sheets: Zapisz do cache

| Parametr | Wartość |
|---|---|
| **Typ** | Google Sheets |
| **Nazwa** | `Sheets — Zapisz cache` |
| **Operation** | Append |
| **Credential** | `Google Sheets OAuth2` |
| **Spreadsheet ID** | `{{ $env.NIP_CACHE_SHEET_ID }}` |
| **Sheet Name** | `Cache` |

**Mapowanie kolumn:**

| Kolumna | Wartość n8n |
|---|---|
| `NIP` | `{{ $json.nip }}` |
| `REGON` | `{{ $json.regon }}` |
| `Nazwa` | `{{ $json.nazwa }}` |
| `Typ` | `{{ $json.typ }}` |
| `Adres` | `{{ $json.adres_pelny }}` |
| `Kod_pocztowy` | `{{ $json.adres.kod_pocztowy }}` |
| `Miejscowosc` | `{{ $json.adres.miejscowosc }}` |
| `Wojewodztwo` | `{{ $json.adres.wojewodztwo }}` |
| `Aktywna` | `{{ $json.aktywna }}` |
| `Pobrano_at` | `{{ $json.pobrano_at }}` |

**Struktura arkusza Cache (nagłówki wiersz 1):**

| A | B | C | D | E | F | G | H | I | J |
|---|---|---|---|---|---|---|---|---|---|
| NIP | REGON | Nazwa | Typ | Adres | Kod_pocztowy | Miejscowosc | Wojewodztwo | Aktywna | Pobrano_at |

---

### Node 8 — Respond to Webhook: Zwróć dane firmy

| Parametr | Wartość |
|---|---|
| **Typ** | Respond to Webhook |
| **Nazwa** | `Respond — dane firmy` |
| **Response Code** | 200 |
| **Response Body** | JSON |

**Response JSON (z cache lub świeże z GUS):**

```json
{
  "status": "ok",
  "source": "{{ $json.zrodlo ?? 'CACHE' }}",
  "data": {
    "nip": "{{ $json.nip }}",
    "regon": "{{ $json.regon }}",
    "nazwa": "{{ $json.nazwa }}",
    "typ": "{{ $json.typ }}",
    "adres_pelny": "{{ $json.adres_pelny }}",
    "aktywna": "{{ $json.aktywna }}"
  }
}
```

---

## Zmienne środowiskowe i credentials

### Credentials (n8n Settings → Credentials)

| Credential | Typ | Co skonfigurować |
|---|---|---|
| `Google Sheets OAuth2` | Google Sheets OAuth2 API | Client ID + Secret z Google Cloud Console |

### Zmienne środowiskowe

```bash
# Plik: ~/.n8n/.env  lub  /etc/n8n/.env

NIP_CACHE_SHEET_ID=1xYzABC123exampleSpreadsheetId456
GUS_API_KEY=abcdef1234567890abcdef1234567890
# GUS_SESSION_KEY jest dynamiczny — generowany przez Login node w czasie runtime
```

---

## Instrukcja rejestracji w GUS REGON API

### Krok 1 — Rejestracja konta

1. Wejdź na: [https://api.stat.gov.pl/Home/RegonApi](https://api.stat.gov.pl/Home/RegonApi)
2. Kliknij **Zarejestruj się** (sekcja "API BIR1.1")
3. Wypełnij formularz: imię, nazwisko, email, cel użytkowania
4. Zatwierdź email rejestracyjny

### Krok 2 — Pobranie klucza API

1. Zaloguj się w panelu klienta GUS
2. W sekcji **"Klucze dostępu"** wygeneruj nowy klucz
3. Klucz wygląda tak: `abcdef1234567890abcdef1234567890` (32 znaki hex)
4. Zapisz klucz jako `GUS_API_KEY` w `.env`

### Krok 3 — Środowisko testowe (piaskownica)

GUS udostępnia środowisko sandbox:
- **URL:** `https://wyszukiwarkaregon.stat.gov.pl/wsBIRtest/UslugaBIRzewnPubl.svc`
- **Klucz testowy:** `abcde12345abcde12345` (publiczny, bez rejestracji)
- Testowe NIPy: `0000000000` (zawsze zwraca przykładowe dane)

### Krok 4 — Logowanie (pobierz SessionKey)

Przed każdym zapytaniem `DaneSzukajPodmioty` musisz wywołać `Zaloguj`:

**Dodaj node `HTTP — GUS Login` PRZED node'em `HTTP — GUS REGON API`:**

```
Method: POST
URL: https://wyszukiwarkaregon.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc
SOAPAction: http://CIS/BIR/PUBL/2014/07/IUslugaBIRzewnPubl/Zaloguj
```

**Body SOAP:**

```xml
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope
  xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
  xmlns:ns="http://CIS/BIR/PUBL/2014/07">
  <soap:Body>
    <ns:Zaloguj>
      <ns:pKluczUzytkownika>{{ $env.GUS_API_KEY }}</ns:pKluczUzytkownika>
    </ns:Zaloguj>
  </soap:Body>
</soap:Envelope>
```

**Wyciągnij SessionKey z odpowiedzi** (dodaj Set node lub Code node):

```javascript
// Wyciągnij ZalogujResult z odpowiedzi XML
const xml = $json.data;
const match = xml.match(/<ZalogujResult>([^<]+)<\/ZalogujResult>/);
if (!match) throw new Error('Logowanie GUS nie powiodło się');
return [{ json: { ...$json, _session_key: match[1] } }];
```

> W blueprincie uproszczono flow do jednego node'a GUS dla czytelności. W produkcji SessionKey jest ważny przez 60 minut — możesz go cache'ować w zmiennej statycznej lub n8n Global Variables.

### Krok 5 — Testowanie przez UI GUS

GUS oferuje przeglądarkę SOAP: [https://wyszukiwarkaregon.stat.gov.pl/wsBIR/wsdl/UslugaBIRzewnPubl-ver11-prod.wsdl](https://wyszukiwarkaregon.stat.gov.pl/wsBIR/wsdl/UslugaBIRzewnPubl-ver11-prod.wsdl)

Narzędzia do testowania SOAP: **SoapUI**, **Postman** (obsługa SOAP), lub **curl** (poniżej).

---

## Instrukcja testowania (curl)

### Test 1 — Poprawny NIP (świeże zapytanie)

```bash
curl -X POST https://<twoja-domena>/webhook-test/enrich-nip \
  -H "Content-Type: application/json" \
  -d '{"nip": "5213003600"}'
```

**Oczekiwana odpowiedź:**

```json
{
  "status": "ok",
  "source": "GUS_REGON",
  "data": {
    "nip": "5213003600",
    "regon": "015249924",
    "nazwa": "ASSECO POLAND SPÓŁKA AKCYJNA",
    "typ": "Prawna",
    "adres_pelny": "ul. Olchowa 14 35-322 Rzeszów",
    "aktywna": true
  }
}
```

### Test 2 — Drugi request tego samego NIP (cache hit)

```bash
# Ten sam NIP — powinien zwrócić dane z cache (bez wywołania GUS)
curl -X POST https://<twoja-domena>/webhook-test/enrich-nip \
  -H "Content-Type: application/json" \
  -d '{"nip": "5213003600"}'
```

**Oczekiwana odpowiedź (pole source = CACHE):**

```json
{
  "status": "ok",
  "source": "CACHE",
  "data": { ... }
}
```

### Test 3 — Błędna suma kontrolna NIP

```bash
curl -X POST https://<twoja-domena>/webhook-test/enrich-nip \
  -H "Content-Type: application/json" \
  -d '{"nip": "5213003601"}'
```

**Oczekiwana odpowiedź (400):**

```json
{
  "status": "error",
  "message": "NIP \"5213003601\" ma błędną cyfrę kontrolną. Oczekiwano: 0, podano: 1."
}
```

### Test 4 — NIP z myślnikami (format ludzki)

```bash
curl -X POST https://<twoja-domena>/webhook-test/enrich-nip \
  -H "Content-Type: application/json" \
  -d '{"nip": "521-300-36-00"}'
```

> Kod walidacji automatycznie usuwa myślniki i spacje przed walidacją.

### Test 5 — Za krótki NIP

```bash
curl -X POST https://<twoja-domena>/webhook-test/enrich-nip \
  -H "Content-Type: application/json" \
  -d '{"nip": "12345"}'
```

**Oczekiwana odpowiedź (400):**

```json
{
  "status": "error",
  "message": "NIP musi zawierać dokładnie 10 cyfr. Podano: \"12345\""
}
```

### Checklist weryfikacji po testach

- [ ] Poprawny NIP zwraca dane firmy z GUS
- [ ] Powtórny request tego samego NIP trafia do cache (brak wywołania GUS w logach)
- [ ] Błędny NIP (zła cyfra kontrolna) zwraca 400 z opisem błędu
- [ ] Nowy rekord pojawia się w arkuszu Google Sheets (zakładka `Cache`)
- [ ] NIP z myślnikami jest poprawnie normalizowany

---

## Typowe błędy i rozwiązania

| Błąd | Przyczyna | Rozwiązanie |
|---|---|---|
| `SessionKey` wygasły | GUS session ważna 60 min | Dodaj node logowania przed każdym zapytaniem lub cache'uj key z timestampem |
| `SOAP 500` od GUS | Błędny format envelope | Sprawdź SOAPAction header — musi dokładnie odpowiadać metodzie |
| Puste `DaneSzukajPodmiotyResult` | NIP nie istnieje w REGON | Dodaj obsługę pustej odpowiedzi (sprawdź `<root/>`) |
| Cache zwraca stare dane | Brak TTL w cache | Dodaj kolumnę `Pobrano_at` i sprawdzaj czy < 7 dni w IF node |
| `403` z GUS | Przekroczony limit API | Darmowe konto: 1000 zapytań/dzień — cache jest kluczowy |
| Sheets Lookup nie działa | Formatowanie NIP w cache | Upewnij się że NIP jest zapisywany jako tekst (apostrofe w Sheets: `'5213003600`) |

---

## Rozszerzenia (następne kroki)

Po opanowaniu blueprintu możesz rozbudować workflow o:
- **TTL dla cache** — IF node sprawdzający czy `Pobrano_at` < 7 dni (odśwież jeśli starsze)
- **Pobierz pełne dane PKD** — wywołanie `DanePobierzPelnyRaport` po REGON (szczegółowe dane branżowe)
- **VIES node (EU VAT)** — weryfikacja aktywności VAT UE dla kontrahentów zagranicznych
- **HubSpot/Pipedrive enrichment** — automatyczny update firmy w CRM po wzbogaceniu NIP
- **Batch mode** — przetwarzanie listy NIPów z pliku CSV (SplitInBatches node)
- **OpenAI node** — AI scoring: czy firma to potencjalny klient Dokodu na podstawie danych GUS
