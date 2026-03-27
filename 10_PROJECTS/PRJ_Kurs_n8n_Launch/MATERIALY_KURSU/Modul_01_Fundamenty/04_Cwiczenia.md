---
type: kurs-materialy
modul: 01
format: cwiczenia
ćwiczeń: 2
zadanie-domowe: tak
created: 2026-03-27
status: gotowe
---

# Tydzień 1: Ćwiczenia Praktyczne

> **Jak korzystać z tych ćwiczeń:**
> Rób je po obejrzeniu segmentów kursu, przy otwartym n8n.
> Nie kopiuj — wpisuj samodzielnie. Błędy są częścią nauki.
> Masz problem? Sprawdź sekcję Troubleshooting na końcu tego dokumentu.

---

## Ćwiczenie 1 — Ping-Pong

**Czas:** ok. 20 minut
**Poziom:** Starter
**Czego się uczysz:** Webhook Trigger, Respond to Webhook node, wyrażenia `{{ }}`, podstawowa manipulacja JSON

**Cel:** Zbuduj workflow, który przyjmuje zapytanie HTTP z JSON-em i zwraca zmodyfikowaną odpowiedź — z dodanym polem i zamienioną wartością. Klasyczny "ping-pong" — wysyłasz, dostajesz echo z przeróbką.

---

### Krok 1 — Stwórz nowy workflow

1. Kliknij **+ New Workflow** w n8n.
2. Zmień nazwę workflow na `01-ping-pong` (ikona ołówka przy tytule).

---

### Krok 2 — Dodaj Webhook Trigger

1. Kliknij `+` na canvasie → wpisz `Webhook` → wybierz **Webhook**.
2. W ustawieniach node'a:
   - **HTTP Method:** `POST`
   - **Path:** `ping`
   - **Response Mode:** `Using 'Respond to Webhook' Node` ← ważne, bez tego workflow odpowie zanim przetworzy dane
3. Kliknij **Listen for Test Event** — n8n czeka na pierwsze wywołanie.

---

### Krok 3 — Wyślij testowy request

Otwórz terminal lub Postman i wyślij:

```bash
curl -X POST http://localhost:5678/webhook-test/ping \
  -H "Content-Type: application/json" \
  -d '{"name": "Kacper", "action": "ping", "timestamp": 1700000000}'
```

Jeśli używasz n8n Cloud, zamień `localhost:5678` na swój subdomain.

Wróć do n8n — powinieneś zobaczyć zielony kolor na Webhook node i dane w Output.

---

### Krok 4 — Dodaj Set node (modyfikacja danych)

1. Kliknij `+` za Webhook node → wybierz **Edit Fields (Set)**.
2. Dodaj trzy pola (przycisk **Add field** dla każdego):

| Field Name | Value |
|---|---|
| `response` | `pong` |
| `received_from` | `{{ $json.name }}` |
| `processed_at` | `{{ $now.toISO() }}` |

3. Zostaw **Include Other Input Fields** wyłączone — chcemy zwrócić tylko te trzy pola.

---

### Krok 5 — Dodaj Respond to Webhook node

1. Kliknij `+` za Set node → wpisz `Respond` → wybierz **Respond to Webhook**.
2. Ustaw:
   - **Respond With:** `All Incoming Items`
   - **Response Code:** `200`

---

### Krok 6 — Przetestuj cały flow

1. Kliknij **Test Workflow** (górny pasek).
2. Wróć do terminala i wyślij request ponownie.
3. Powinieneś otrzymać odpowiedź:

```json
[
  {
    "response": "pong",
    "received_from": "Kacper",
    "processed_at": "2026-03-27T10:00:00.000Z"
  }
]
```

Jeśli odpowiedź przyszła — gratulacje, masz działający webhook.

---

### Częste błędy w tym ćwiczeniu

**Błąd:** `Workflow could not be started` — workflow nie jest aktywowany.
**Rozwiązanie:** Upewnij się że kliknąłeś **Listen for Test Event** PRZED wysłaniem requesta. W trybie testowym webhook nasłuchuje tylko przez ~2 minuty.

**Błąd:** Odpowiedź zawiera `{"message": "Workflow was started"}` zamiast Twoich danych.
**Rozwiązanie:** W Webhook node masz ustawione `Response Mode: Immediately`. Zmień na `Using 'Respond to Webhook' Node`.

**Błąd:** Pole `processed_at` jest puste lub null.
**Rozwiązanie:** Wyrażenie `$now` zwraca obiekt DateTime. Użyj `{{ $now.toISO() }}` (z nawiasami) — metoda `toISO()` zamienia go na string.

**Błąd:** Curl zwraca `Connection refused`.
**Rozwiązanie:** n8n nie działa lub nasłuchuje na innym porcie. Sprawdź `docker ps` — czy kontener jest uruchomiony.

---

## Ćwiczenie 2 — Lead Capture System

**Czas:** ok. 45 minut
**Poziom:** Podstawowy
**Czego się uczysz:** Pełny pipeline produkcyjny — walidacja danych, Google Sheets, Gmail, Slack, obsługa błędów, Execution Log

**Cel:** Zbuduj kompletny system przechwytywania leadów: formularz wysyła dane → n8n waliduje → zapisuje do Google Sheets → wysyła email powitalny do leada → pinguje Slack.

---

### Dane testowe (skopiuj przed startem)

Miej te dane gotowe w schowku — będziesz je wysyłać kilka razy:

**Poprawny lead:**
```json
{
  "first_name": "Anna",
  "last_name": "Kowalska",
  "email": "anna.kowalska@example.com",
  "company": "Kowalska Sp. z o.o.",
  "phone": "+48 600 123 456",
  "source": "webinar"
}
```

**Lead z błędem (brak emaila):**
```json
{
  "first_name": "Jan",
  "last_name": "Nowak",
  "company": "Nowak Industries"
}
```

---

### Krok 1 — Webhook Trigger

1. Nowy workflow, nazwij `02-lead-capture`.
2. Dodaj **Webhook** node:
   - **HTTP Method:** `POST`
   - **Path:** `lead-capture`
   - **Response Mode:** `Using 'Respond to Webhook' Node`

---

### Krok 2 — Walidacja emaila (IF node)

1. Za Webhook dodaj **IF** node.
2. Skonfiguruj warunek:
   - **Value 1:** `{{ $json.email }}`
   - **Operation:** `Matches Regex`
   - **Value 2:** `^[^\s@]+@[^\s@]+\.[^\s@]+$`

   Ten regex sprawdza czy `email` wygląda jak adres email. Nie jest idealny — ale wystarczy na walidację podstawową.

3. Gałąź **true** idzie dalej do zapisu.
4. Gałąź **false** — podłącz osobny **Respond to Webhook** z kodem `400` i treścią:
   ```json
   { "error": "Invalid or missing email address" }
   ```

---

### Krok 3 — Sprawdzenie wymaganych pól (IF node #2)

Za pierwszym IF (gałąź `true`) dodaj drugi **IF** node:

- **Value 1:** `{{ $json.first_name }}`
- **Operation:** `Is Not Empty`

Dodaj drugi warunek (przycisk **Add Condition**):
- **Value 1:** `{{ $json.company }}`
- **Operation:** `Is Not Empty`
- **Combine:** `AND`

Gałąź `false` → **Respond to Webhook** z kodem `422`:
```json
{ "error": "first_name and company are required" }
```

---

### Krok 4 — Normalizacja danych (Set node)

Za drugim IF (gałąź `true`) dodaj **Edit Fields (Set)** node.
Cel: oczyść dane przed zapisem — ustandaryzuj format.

Włącz **Include Other Input Fields**, a następnie dodaj lub nadpisz:

| Field Name | Value |
|---|---|
| `email` | `{{ $json.email.toLowerCase().trim() }}` |
| `full_name` | `{{ $json.first_name + ' ' + $json.last_name }}` |
| `created_at` | `{{ $now.toISO() }}` |
| `lead_status` | `new` |

---

### Krok 5 — Zapis do Google Sheets

1. Dodaj **Google Sheets** node.
2. Kliknij **Credential to connect with** → **Create New** → zaloguj się przez OAuth (kliknij Connect, zaloguj na konto Google, autoryzuj).
3. W ustawieniach:
   - **Operation:** `Append or Update Row`
   - **Document:** *(wybierz swój arkusz z listy lub wklej ID)*
   - **Sheet:** `Leady`
   - **Matching Columns:** *(zostaw puste — dodajemy nowy wiersz za każdym razem)*
4. W sekcji **Values** zmapuj kolumny:
   - `email` → `{{ $json.email }}`
   - `full_name` → `{{ $json.full_name }}`
   - `company` → `{{ $json.company }}`
   - `phone` → `{{ $json.phone }}`
   - `source` → `{{ $json.source }}`
   - `status` → `{{ $json.lead_status }}`
   - `created_at` → `{{ $json.created_at }}`

> **Przygotowanie arkusza:** Stwórz plik Google Sheets z arkuszem `Leady` i nagłówkami w pierwszym wierszu: `email`, `full_name`, `company`, `phone`, `source`, `status`, `created_at`.

---

### Krok 6 — Email powitalny (Gmail node)

1. Dodaj **Gmail** node.
2. **Credential:** utwórz nowe (OAuth przez konto Gmail).
3. Ustaw:
   - **Operation:** `Send`
   - **To:** `{{ $json.email }}`
   - **Subject:** `Cześć {{ $json.first_name }}, dziękujemy za zainteresowanie!`
   - **Email Type:** `HTML`
   - **Message:**

```html
<p>Cześć {{ $json.first_name }},</p>
<p>Dziękujemy za kontakt. Otrzymaliśmy Twoje zgłoszenie i odezwiemy się w ciągu 24 godzin.</p>
<p>Pozdrawiamy,<br>Zespół Dokodu</p>
```

---

### Krok 7 — Powiadomienie Slack

1. Dodaj **Slack** node.
2. **Credential:** Slack API (OAuth lub Bot Token — zależy od konfiguracji workspace).
3. Ustaw:
   - **Resource:** `Message`
   - **Operation:** `Send`
   - **Channel:** `#leady` *(lub inny kanał który masz)*
   - **Text:**
   ```
   Nowy lead: *{{ $json.full_name }}* z firmy *{{ $json.company }}* ({{ $json.email }})
   Źródło: {{ $json.source }} | {{ $json.created_at }}
   ```

---

### Krok 8 — Odpowiedź sukces (Respond to Webhook)

Na końcu łańcucha po Slack dodaj **Respond to Webhook**:
- **Response Code:** `200`
- **Respond With:** `JSON`
- **Response Body:**
```json
{ "status": "ok", "message": "Lead received" }
```

---

### Krok 9 — Test end-to-end

1. Kliknij **Test Workflow** w n8n.
2. Wyślij poprawny lead (curl poniżej):

```bash
curl -X POST http://localhost:5678/webhook-test/lead-capture \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Anna",
    "last_name": "Kowalska",
    "email": "anna.kowalska@example.com",
    "company": "Kowalska Sp. z o.o.",
    "phone": "+48 600 123 456",
    "source": "webinar"
  }'
```

---

### Checkpointy — sprawdź czy działa

Zanim przejdziesz dalej, zweryfikuj każdy punkt:

- [ ] Webhook przyjął request i widać dane w Output (zielony node)
- [ ] IF walidacja emaila przepuściła poprawny lead gałęzią `true`
- [ ] Wyślij lead bez emaila — powinieneś dostać odpowiedź 400
- [ ] Wyślij lead bez `first_name` — powinieneś dostać 422
- [ ] W Google Sheets pojawił się nowy wiersz z poprawnymi danymi
- [ ] Na podany email przyszła wiadomość powitalna (sprawdź Spam jeśli nie ma w Inbox)
- [ ] Na kanale Slack widać powiadomienie
- [ ] Curl zwrócił `{"status": "ok", "message": "Lead received"}`

---

### Debugowanie: jak używać Execution Log

Gdy coś nie działa — nie zgaduj. Otwórz **Execution Log**:

1. Kliknij **Executions** w lewym menu (ikona listy).
2. Znajdź ostatnie uruchomienie — czerwony = błąd, zielony = sukces.
3. Kliknij w wykonanie — zobaczysz każdy node po kolei.
4. Kliknij na czerwony node — w panelu po prawej zobaczysz dokładny komunikat błędu.

**Najczęstsze pytania przy debugowaniu:**
- *Dlaczego IF node idzie złą gałęzią?* — Kliknij IF node w Execution Log i sprawdź wartość `Value 1`. Często problem to `undefined` bo pole ma inną nazwę niż myślisz.
- *Gmail nie wysyła?* — Sprawdź czy credential jest połączony (zielona ikona przy nazwie). Jeśli credential ma czerwony znak — OAuth wygasł, odnów go.
- *Google Sheets daje 403?* — Upewnij się że konto Google którym się zalogowałeś ma dostęp do arkusza jako edytor.
- *Slack nie wysyła?* — Sprawdź czy bot ma uprawnienia `chat:write` i czy jest zaproszony do kanału (`/invite @TwojaAplikacja`).

---

## Zadanie Domowe — Filtr Antyspamowy

**Termin:** Przed sesją live w następnym tygodniu
**Czas szacowany:** 30–45 minut

### Co masz zbudować

Rozszerz workflow Lead Capture o filtr antyspamowy: jeśli email pochodzi z domeny znajdującej się na czarnej liście (np. `guerrillamail.com`, `mailinator.com`, `tempmail.com`) — nie zapisuj leada do Sheets, nie wysyłaj emaila, zwróć odpowiedź z kodem `403`.

### Podpowiedź: struktura rozwiązania

Za walidacją emaila (ale przed normalizacją) wstaw nowy **IF** node:

1. Wyciągnij domenę z emaila wyrażeniem:
   ```
   {{ $json.email.split('@')[1] }}
   ```

2. Sprawdź czy domena jest na liście blokowanych. Użyj warunków `OR`:
   - `{{ $json.email.split('@')[1] }}` **equals** `guerrillamail.com`
   - `{{ $json.email.split('@')[1] }}` **equals** `mailinator.com`
   - `{{ $json.email.split('@')[1] }}` **equals** `tempmail.com`

   Możesz też użyć jednego warunku z `Matches Regex` i wzorca `(guerrillamail|mailinator|tempmail)\.com`.

3. Gałąź `true` (domena na czarnej liście) → **Respond to Webhook** z kodem `403`:
   ```json
   { "error": "Email domain not allowed" }
   ```

4. Gałąź `false` (domena czysta) → reszta workflow bez zmian.

### Kryteria zaliczenia

Twój workflow musi:
- [ ] Przyjąć email z dozwolonej domeny i zapisać do Sheets (workflow działa normalnie)
- [ ] Odrzucić email `test@mailinator.com` z odpowiedzią HTTP 403
- [ ] Odrzucić email `test@guerrillamail.com` z odpowiedzią HTTP 403
- [ ] Przepuszczać wszystkie inne domeny bez zmian

### Jak wysłać do sprawdzenia

Na sesji live: udostępnij ekran z n8n (Execution Log) i przejdź przez każdy z powyższych testów na żywo. Możesz też wyeksportować workflow (⋯ → Export → JSON) i wkleić do kanału Discord kursu.

---

## Troubleshooting — Top 5 Błędów Tygodnia 1

### Błąd 1: Webhook nie odpowiada / timeout

**Objaw:** Curl czeka i czeka, po 30 sekundach zwraca `curl: (28) Operation timed out`.

**Przyczyna:** Workflow testowy w n8n nasłuchuje tylko przez ~2 minuty po kliknięciu "Listen for Test Event". Po tym czasie przestaje reagować.

**Rozwiązanie:**
1. Wróć do n8n i kliknij **Listen for Test Event** ponownie.
2. Wyślij curl w ciągu 2 minut.
3. W trybie produkcyjnym (aktywny toggle) webhook działa stale bez klikania.

---

### Błąd 2: "Cannot read property 'email' of undefined"

**Objaw:** Workflow pada na IF node lub Set node z błędem o `undefined`.

**Przyczyna:** Dane przyszły w nieprawidłowej strukturze. Najczęstsza przyczyna: curl bez nagłówka `Content-Type: application/json`, więc n8n potraktował body jako tekst, nie JSON.

**Rozwiązanie:**
1. Upewnij się że curl ma flagę `-H "Content-Type: application/json"`.
2. W Execution Log kliknij Webhook node → Output i sprawdź jak wyglądają dane. Jeśli całe body jest w polu `body` jako string — n8n nie sparsował JSON-a.
3. Możesz też sprawdzić strukturę: dostęp do emaila może być `$json.body.email` zamiast `$json.email` — zależy od konfiguracji Webhook node (opcja **Binary Data** musi być wyłączona).

---

### Błąd 3: IF node zawsze idzie gałęzią "false"

**Objaw:** Walidacja emaila odrzuca wszystkie emaile, nawet poprawne.

**Przyczyna:** Najczęściej błąd w nazwie pola (np. `Email` z wielką literą zamiast `email`) lub regex jest niepoprawnie wklejony.

**Rozwiązanie:**
1. Kliknij IF node w Execution Log → sprawdź wartość `Value 1`. Jeśli widzisz `undefined` — pole ma inną nazwę.
2. W Webhook Output (kliknij Webhook node w Execution Log) sprawdź dokładne nazwy pól w JSON.
3. Jeśli regex, sprawdź czy nie ma zbędnych spacji na początku lub końcu wyrażenia.

---

### Błąd 4: Google Sheets zwraca 403 Forbidden

**Objaw:** Workflow pada na Google Sheets node z błędem `403`.

**Przyczyna:** Konto Google które autoryzowałeś nie ma uprawnień do arkusza, lub arkusz jest w trybie "Tylko do wyświetlania".

**Rozwiązanie:**
1. Otwórz arkusz Google Sheets w przeglądarce.
2. Kliknij **Udostępnij** i upewnij się że konto z credentiala n8n ma dostęp **Edytor** (nie tylko Przeglądający).
3. Jeśli arkusz jest firmowy (Google Workspace) — może blokować zewnętrzne aplikacje. Sprawdź ustawienia administratora lub użyj prywatnego konta Gmail.

---

### Błąd 5: Workflow działa w teście, ale nie działa po aktywacji

**Objaw:** W trybie testowym (kliknięty "Listen for Test Event") wszystko gra. Po aktywacji workflow (toggle "Active") webhook nie odpowiada lub zachowuje się inaczej.

**Przyczyna:** W trybie testowym n8n używa URL `webhook-test/...`. Po aktywacji URL zmienia się na `webhook/...` (bez `-test`).

**Rozwiązanie:**
1. Po aktywacji workflow skopiuj URL z zakładki **Production URL** w Webhook node (nie Test URL).
2. Zaktualizuj URL w swoim formularzu lub curlu: `localhost:5678/webhook/lead-capture`.
3. Pamiętaj: każda zmiana w aktywnym workflow wymaga ponownego zapisania (Ctrl+S) — toggle "Active" nie zawsze odświeża automatycznie.

---

> **Pytania?** Wrzuć na kanał `#tydzien-1` na Discordzie kursu. Dołącz screenshot Execution Log i opis co próbowałeś — szybciej znajdziemy rozwiązanie.
