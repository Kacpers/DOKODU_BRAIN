---
type: kurs-materialy
modul: 03
tytuł: "Tydzień 3: Ćwiczenia praktyczne — Skalowalność i Disaster Prevention"
czas_total: ~105 min
status: draft
last_reviewed: 2026-03-27
---

# Tydzień 3: Ćwiczenia praktyczne

> **Zanim zaczniesz:** Upewnij się, że masz działające n8n (lokalnie lub chmurowo), dostęp do Slacka z prawami do tworzenia webhooków, oraz konto Google z uprawnieniami do Sheets. Te ćwiczenia realizujesz bezpośrednio po obejrzeniu materiału wideo — najlepiej tego samego dnia, póki kontekst jest świeży.

---

## Ćwiczenie 1 — Crash Test (20 min)

**Cel:** Celowo zepsuj workflow i obserwuj, jak Error Trigger wychwytuje błąd w czasie rzeczywistym.

To ćwiczenie ma jeden cel: przekonać cię, że błędy *będą* się zdarzać. Zamiast się tego bać, budujesz system, który cię o tym poinformuje zanim zrobi to klient.

### Krok 1: Stwórz "kruchy" workflow bez error handling

1. Utwórz nowy workflow o nazwie `[TEST] Kruchy Workflow`.
2. Dodaj **Manual Trigger** jako punkt startowy.
3. Dodaj node **HTTP Request**:
   - Method: `GET`
   - URL: `https://api.nieistniejaca-domena-xyz-12345.com/data`
   - Timeout: 5000 ms
4. Za HTTP Request dodaj **Set** node z dowolną wartością (symuluje dalsze przetwarzanie).
5. Uruchom workflow ręcznie. Zaobserwuj błąd w execution log — n8n zatrzyma się na HTTP Request, reszta nie wykona się.

> **Co widzisz?** Workflow "cicho" pada. Żadne powiadomienie. Nie wiesz kiedy to nastąpiło, jeśli nie zaglądasz do n8n ręcznie.

### Krok 2: Skonfiguruj Error Trigger Workflow (globalny handler)

1. Utwórz **nowy workflow** o nazwie `[SYSTEM] Error Handler Global`.
2. Dodaj node **Error Trigger** — znajdziesz go w zakładce "Trigger" przy tworzeniu nowego workflow.
3. Zapisz workflow (nie musisz go jeszcze aktywować — wrócimy do tego w kroku 3).
4. Wróć do `[TEST] Kruchy Workflow`.
5. Otwórz **Settings** workflow (ikona koła zębatego w prawym górnym rogu).
6. W polu **Error Workflow** wybierz `[SYSTEM] Error Handler Global`.
7. Zapisz zmiany.

> **Ważne:** Error Trigger działa tylko wtedy, gdy workflow jest **aktywny** (przełącznik Active = ON). Dla workflow uruchamianych ręcznie błąd jest przekazywany natychmiast przy wykonaniu.

### Krok 3: Uruchom i obserwuj co Error Trigger łapie

1. Aktywuj `[SYSTEM] Error Handler Global` (przełącz na Active).
2. Wróć do `[TEST] Kruchy Workflow` i uruchom go ręcznie.
3. Przejdź do execution log `[SYSTEM] Error Handler Global` — powinieneś zobaczyć nowe wykonanie.
4. Kliknij w wykonanie i sprawdź dane wyjściowe Error Trigger node. Zanotuj co widzisz w `$json`:
   - `execution.id` — unikalny ID wykonania
   - `execution.url` — bezpośredni link do błędnego wykonania w n8n
   - `workflow.name` — nazwa workflow który padł
   - `error.message` — treść błędu
   - `error.node.name` — node w którym błąd wystąpił

### Krok 4: Dodaj alert na Slacka z detalami błędu

1. W `[SYSTEM] Error Handler Global`, za Error Trigger dodaj node **Slack** (akcja: Send a Message).
2. Skonfiguruj wiadomość. W polu **Text** wklej:

```
:rotating_light: *Błąd w workflow n8n*

*Workflow:* {{ $json.workflow.name }}
*Node:* {{ $json.error.node.name }}
*Błąd:* {{ $json.error.message }}
*Czas:* {{ $now.toFormat('yyyy-MM-dd HH:mm:ss') }}
*Link:* {{ $json.execution.url }}
```

3. Wybierz kanał Slack (np. `#n8n-errors` lub dowolny testowy kanał).
4. Zapisz i uruchom ponownie `[TEST] Kruchy Workflow`.

**Expected output:** Na Slacku pojawia się wiadomość zawierająca nazwę workflow (`[TEST] Kruchy Workflow`), nazwę node (`HTTP Request`), treść błędu (timeout lub connection refused) oraz timestamp i link do wykonania w n8n.

**Checkpoint:** Jeśli wiadomość dotarła na Slacka — gratulacje. Masz działający globalny handler błędów. Od tej pory każdy workflow, który przypisuje ten Error Handler, automatycznie powiadomi cię o problemie.

---

## Ćwiczenie 2 — Armored Invoicing Lite (60 min)

**Cel:** Zbuduj uproszczony, odporny system fakturowania z retry logic, idempotency check i logiem w Sheets.

To jest mini-wersja projektu "Armored Invoicing System" z lekcji. Celowo uproszczona — nie ma prawdziwej integracji z systemem fakturowym — ale mechanizmy odporności są prawdziwe i gotowe do użycia w produkcji.

### Architektura

```
Webhook → Idempotency Check (Sheets) → Generuj fakturę (mock) → Wyślij email (z retry 3x) → Zapisz log (Sheets)
```

### Przygotowanie: Google Sheets

Stwórz arkusz Google Sheets o nazwie `Armored Invoicing Log` z dwoma zakładkami:

**Zakładka 1: `processed_orders`**
| Kolumna A | Kolumna B |
|-----------|-----------|
| order_id  | processed_at |

**Zakładka 2: `execution_log`**
| A: timestamp | B: order_id | C: status | D: email | E: error |
|---|---|---|---|---|

### Krok 1: Webhook Trigger

1. Utwórz nowy workflow: `Armored Invoicing Lite`.
2. Dodaj node **Webhook**:
   - HTTP Method: `POST`
   - Path: `invoice-lite`
   - Response Mode: `Immediately`
3. Skopiuj URL webhooka — użyjesz go do testów.

### Krok 2: Idempotency Check

Sprawdzamy, czy to zamówienie było już przetworzone.

1. Dodaj node **Google Sheets** (akcja: Read Rows):
   - Spreadsheet: `Armored Invoicing Log`
   - Sheet: `processed_orders`
   - Filters: kolumna `order_id` równa `{{ $json.body.order_id }}`
2. Dodaj node **IF**:
   - Condition: `{{ $json.order_id }}` is not empty
   - True branch: zamówienie już przetworzone → **Stop and Error** node z komunikatem `Duplicate order: {{ $json.body.order_id }}`
   - False branch: kontynuuj przetwarzanie

> **Tip:** Zamiast Stop and Error możesz użyć Set node który zwraca `{ "status": "skipped", "reason": "duplicate" }`. To zależy od tego czy chcesz traktować duplikat jako błąd czy jako normalną sytuację.

### Krok 3: Generuj "fakturę" (mock)

1. Na gałęzi False (nowe zamówienie) dodaj node **Set**:
   - Ustaw zmienne:
     - `invoice_number`: `INV-{{ $now.toFormat('yyyyMMdd') }}-{{ $json.body.order_id }}`
     - `invoice_amount`: `{{ $json.body.amount }}`
     - `customer_email`: `{{ $json.body.email }}`
     - `invoice_created_at`: `{{ $now.toISO() }}`

### Krok 4: Wyślij email z retry 3x

W n8n nie ma natywnego retry per-node, więc budujesz pętlę manualnie:

1. Dodaj node **Set** o nazwie `Retry Counter`:
   - `attempt`: `{{ $json.attempt ?? 1 }}`
2. Dodaj node **Gmail** lub **Send Email**:
   - To: `{{ $json.customer_email }}`
   - Subject: `Faktura {{ $json.invoice_number }}`
   - Body: `Dziękujemy za zamówienie. Kwota: {{ $json.invoice_amount }} PLN. Numer faktury: {{ $json.invoice_number }}.`
   - Włącz opcję **Continue On Fail** w ustawieniach node
3. Dodaj node **IF** o nazwie `Email Sent?`:
   - Condition: `{{ $json.error }}` is empty (brak błędu = sukces)
   - True: przejdź do logowania (krok 5)
   - False: sprawdź liczbę prób
4. Na gałęzi False dodaj kolejny **IF** o nazwie `Max Retries?`:
   - Condition: `{{ $json.attempt }}` >= 3
   - True: **Slack** node z alertem o nieudanym emailu + przejdź do logowania ze statusem ERROR
   - False: **Wait** node (5 sekund) → wróć do `Retry Counter` z `attempt + 1`

> **Uwaga na pętlę:** W n8n możesz połączyć wyjście Wait node z powrotem do Retry Counter — tworzy się pętla. Działa to poprawnie, ale uważaj żeby warunek wyjścia był zawsze osiągalny.

### Krok 5: Zapisz log w Sheets

Niezależnie od wyniku (sukces lub błąd po 3 próbach), zapisz log.

1. Dodaj node **Google Sheets** (akcja: Append Row) do zakładki `execution_log`:
   - `timestamp`: `{{ $now.toISO() }}`
   - `order_id`: `{{ $json.order_id ?? $('Webhook').item.json.body.order_id }}`
   - `status`: `{{ $json.error ? 'ERROR' : 'SUCCESS' }}`
   - `email`: `{{ $json.customer_email }}`
   - `error`: `{{ $json.error?.message ?? '' }}`
2. Jeśli status SUCCESS: dodaj node **Google Sheets** do zakładki `processed_orders` (Append Row):
   - `order_id`: `{{ $json.order_id }}`
   - `processed_at`: `{{ $now.toISO() }}`

### Test: idempotency w akcji

1. Wyślij webhook z testowymi danymi:
```json
{
  "order_id": "ORD-001",
  "amount": 1500,
  "email": "test@example.com"
}
```
2. Sprawdź zakładkę `processed_orders` — powinien pojawić się 1 wpis.
3. Wyślij **ten sam webhook ponownie** (identyczny order_id).
4. Sprawdź zakładkę `processed_orders` — nadal powinien być **1 wpis**, nie 2.
5. Sprawdź zakładkę `execution_log` — zobaczysz dwa wpisy: jeden SUCCESS, drugi z informacją o duplikacie.

**Expected output:** Po dwóch identycznych żądaniach — 1 wpis w `processed_orders` (idempotency działa), 2 wpisy w `execution_log` (każde żądanie jest logowane), 1 email do klienta (nie 2).

---

## Ćwiczenie 3 — Batch Processing (25 min)

**Cel:** Przetwórz listę 50 rekordów z Google Sheets partiami po 10, obserwując różnicę w execution log.

Bez batching: n8n pobiera wszystkie dane naraz i próbuje przetworzyć je równolegle. Przy dużych wolumenach kończy się to timeoutem lub przeciążeniem zewnętrznego API. SplitInBatches rozwiązuje ten problem.

### Przygotowanie: dane testowe

1. Stwórz nową zakładkę w Google Sheets o nazwie `produkty_do_wyceny`.
2. Wypełnij 50 wierszy danymi:
   - Kolumna A: `product_id` (P001, P002, ... P050)
   - Kolumna B: `name` (dowolne nazwy produktów)
   - Kolumna C: `price` (dowolne liczby)

   > **Szybkie wypełnienie:** W A2 wpisz `P001`, zaznacz A2 i przeciągnij lub użyj formuły `="P"&TEXT(ROW()-1,"000")`.

### Krok 1: Workflow BEZ batching (punkt odniesienia)

1. Utwórz workflow `[TEST] Batch Comparison`.
2. Dodaj **Manual Trigger**.
3. Dodaj **Google Sheets** (Read Rows) — pobierz wszystkie 50 wierszy z `produkty_do_wyceny`.
4. Dodaj **HTTP Request** (mock API wyceny):
   - URL: `https://httpbin.org/delay/0` (echo API, odpowiada natychmiast)
   - Method: POST
   - Body: `{ "product_id": "{{ $json.product_id }}", "price": {{ $json.price }} }`
5. Uruchom workflow. Zanotuj czas wykonania w execution log (górny prawy róg po zakończeniu).

### Krok 2: Workflow Z SplitInBatches

1. W tym samym workflow, między Google Sheets a HTTP Request, wstaw node **SplitInBatches**:
   - Batch Size: `10`
   - Options: zostaw domyślnie
2. Upewnij się, że HTTP Request jest podłączony za SplitInBatches (nie bezpośrednio za Sheets).
3. Za HTTP Request dodaj **Set** node (opcjonalnie — może agregować wyniki).
4. Uruchom workflow. Zanotuj czas wykonania.

### Krok 3: Obserwuj execution log

Po uruchomieniu obu wersji wejdź w szczegóły wykonania (kliknij w execution w historii):

**Bez batching:** zobaczysz jeden masywny "krok" — Google Sheets zwraca 50 elementów, HTTP Request jest wywołany 50 razy równolegle. W execution log jest 50 items w jednym node.

**Z SplitInBatches:** zobaczysz wyraźne "pętle" — SplitInBatches pokazuje numer batcha (1/5, 2/5, ... 5/5). HTTP Request jest wywołany 10 razy per iteracja. W execution log widać sekwencyjne przejścia przez pętle.

**Co zanotować:**
- Czas wykonania obu wersji (przy 50 rekordach różnica będzie mała, ale widoczna)
- Liczba "iterations" w SplitInBatches node (powinna być 5 dla 50 rekordów z batch size 10)
- Jak wygląda node execution count w historii

> **Dlaczego to ważne w produkcji?** Przy 1000 rekordach i API z rate limit 100 req/min — bez batching dostaniesz 429 Too Many Requests. Z SplitInBatches możesz dodać **Wait** node między batchami (np. 10 sekund) i nigdy nie przekroczysz limitu.

### Bonus: dodaj Wait między batchami

1. Za HTTP Request dodaj **IF** node: sprawdź czy `{{ $runIndex }}` mod 10 === 0 (co 10 rekordów).
2. True branch: **Wait** node (2 sekundy) → wróć do pętli.
3. False branch: bezpośrednio wróć do SplitInBatches.

---

## Zadanie Domowe — Dzienny Raport Monitoringowy

**Cel:** Rozszerz Armored Invoicing Lite o automatyczny dzienny raport emailowy.

Raport powinien zawierać:
- Ilu zamówień zostało pomyślnie przetworzonych w ostatnich 24h
- Ilu nie (status ERROR)
- Łączna wartość przetworzonych zamówień
- Lista zamówień z błędem (order_id + komunikat błędu)

### Wskazówki do implementacji

**Trigger:** Użyj **Cron** node z harmonogramem `0 8 * * *` (codziennie o 8:00 rano).

**Pobierz dane z Sheets:**
- Google Sheets (Read Rows) z zakładki `execution_log`
- Filtruj po kolumnie `timestamp` — chcesz tylko rekordy z ostatnich 24h
- W n8n możesz to zrobić w **Code** node: `items.filter(i => new Date(i.json.timestamp) > new Date(Date.now() - 86400000))`

**Oblicz statystyki w Code node:**
```javascript
const items = $input.all();
const successful = items.filter(i => i.json.status === 'SUCCESS');
const failed = items.filter(i => i.json.status === 'ERROR');
const totalValue = successful.reduce((sum, i) => sum + (parseFloat(i.json.amount) || 0), 0);

return [{
  json: {
    date: new Date().toISOString().split('T')[0],
    total_orders: items.length,
    successful: successful.length,
    failed: failed.length,
    total_value: totalValue,
    failed_orders: failed.map(i => ({ order_id: i.json.order_id, error: i.json.error }))
  }
}];
```

**Wyślij email/Slack** z obliczonymi statystykami. Przykładowy format raportu:

```
Dzienny raport n8n — {{ $json.date }}

Zamówienia przetworzone: {{ $json.successful }} / {{ $json.total_orders }}
Błędy: {{ $json.failed }}
Łączna wartość: {{ $json.total_value }} PLN

{{ $json.failed > 0 ? '⚠️ Zamówienia z błędem:' : '✅ Brak błędów' }}
{{ $json.failed_orders.map(o => `- ${o.order_id}: ${o.error}`).join('\n') }}
```

**Kryterium zaliczenia:** Raport wysyła się automatycznie o wyznaczonej godzinie i zawiera poprawne dane z dnia poprzedniego. Przetestuj go uruchamiając ręcznie (Manual Trigger zamiast Cron) po uzupełnieniu kilku wpisów w execution_log.

---

## Checklist po Tygodniu 3

Przed przejściem do Tygodnia 4 upewnij się, że:

- [ ] Ćwiczenie 1: Error Trigger działa i wysyła alerty na Slack
- [ ] Ćwiczenie 2: Armored Invoicing Lite odrzuca duplikaty (idempotency)
- [ ] Ćwiczenie 2: Retry 3x działa przy błędzie emaila
- [ ] Ćwiczenie 2: Każde wykonanie jest logowane w Sheets
- [ ] Ćwiczenie 3: Zidentyfikowałeś różnicę w execution log między wersją z i bez SplitInBatches
- [ ] Zadanie domowe: Dzienny raport wysyła się automatycznie z poprawnymi statystykami

> **Problemy?** Najczęstszy błąd: Error Trigger nie odpalał się, bo workflow nie był ustawiony jako Active. Drugi częsty problem: idempotency check zwraca błąd gdy tabela `processed_orders` jest pusta — dodaj obsługę pustego wyniku w IF node (sprawdź czy `$items().length > 0`, nie tylko czy `$json.order_id` istnieje).
