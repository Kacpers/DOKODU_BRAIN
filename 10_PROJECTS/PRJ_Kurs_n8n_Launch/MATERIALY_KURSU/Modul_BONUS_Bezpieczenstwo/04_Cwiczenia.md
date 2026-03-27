---
type: course-material
modul: BONUS_A
status: ready
owner: kacper
last_reviewed: 2026-03-27
tags: [kurs, n8n, bezpieczenstwo, cwiczenia, rodo, hmac]
---

# Moduł BONUS A — Ćwiczenia praktyczne

> **Środowisko:** Twoje własne n8n (lokalny lub VPS)
> **Wymagania wstępne:** Ukończone Moduły 01–03 kursu
> **Łączny czas:** ~50 minut (ćwiczenia) + zadanie domowe

---

## ĆWICZENIE 1 — RODO AUDIT ISTNIEJĄCEGO WORKFLOW (20 minut)

### Cel
Przejść przez swój istniejący workflow i zidentyfikować wszystkie punkty przetwarzania danych osobowych. Wyjście: wypełniona checklista + mapa przepływu danych.

### Zanim zaczniesz
Wybierz jeden workflow który masz już uruchomiony (lub który budujesz aktywnie). Najlepiej taki który:
- Odbiera dane z formularza LUB przetwarza maile LUB integruje CRM
- Ma co najmniej 5 węzłów
- Przetwarza dane kontaktowe jakichkolwiek osób

### Krok 1: Data Flow Diagram (5 minut)

Na kartce (lub Miro / FigJam) narysuj prostokąty dla każdego systemu w workflow i strzałki z opisem danych które przepływają.

**Szablon:**

```
[Źródło danych]
      |
      | (jakie pola?)
      ↓
[n8n Webhook / Trigger Node]
      |
      | (jakie pola przetwarzasz?)
      ↓
[n8n Processing Nodes...]
      |
      ├──→ [System A: np. CRM]       (jakie pola?)
      ├──→ [System B: np. Sheets]    (jakie pola?)
      └──→ [System C: np. OpenAI]    (jakie pola? ← UWAGA!)
```

**Oznacz czerwonym** wszystkie pola które mogą być danymi osobowymi:
- Imię, nazwisko, pseudonim
- Adres email
- Numer telefonu
- Adres IP (!)
- Adres zamieszkania / dostawy
- NIP osoby fizycznej, PESEL
- Data urodzenia
- Informacje o preferencjach / zachowaniu

### Krok 2: RODO Checklist — wypełnij dla swojego workflow (10 minut)

**A. DANE — Inwentaryzacja**

| Pytanie | Odpowiedź | OK? |
|---|---|---|
| Które pola zawierają dane osobowe? | Wpisz pola: | |
| Jaka jest podstawa prawna przetwarzania? (Art. 6 RODO) | Zgoda / Umowa / Uzasadniony interes / Inny | |
| Czy zbierasz TYLKO dane niezbędne do celu? | TAK / NIE — jeśli NIE: które pola możesz pominąć? | |
| Jak długo dane są przechowywane? Gdzie? | Opisz per system | |
| Czy jest zdefiniowana procedura usunięcia? | TAK / NIE | |

**B. TECHNICZNE — Bezpieczeństwo**

| Pytanie | Status | Do poprawki |
|---|---|---|
| Czy PII trafia do logów n8n? (sprawdź "Save Execution Data") | TAK / NIE | |
| Czy dane osobowe są wysyłane do zewnętrznych LLM (OpenAI, Anthropic)? | TAK / NIE | |
| Jeśli TAK — czy jest pseudonimizacja przed wysyłką? | TAK / NIE | |
| Czy sekrety/API keys są w Credentials (nie hardcoded w workflow)? | TAK / NIE | |
| Czy połączenia do zewnętrznych API używają HTTPS? | TAK / NIE | |

**C. UMOWY — Dokumentacja**

| Pytanie | Status |
|---|---|
| Czy masz DPA (Data Processing Agreement) z dostawcami API których używasz? | TAK / NIE / Nie wiem |
| Czy masz umowę powierzenia przetwarzania z klientem dla którego robisz workflow? | TAK / NIE / N/A |
| Czy klient wie że dane trafiają do tych zewnętrznych systemów? | TAK / NIE |

### Krok 3: Priorytetyzacja poprawek (5 minut)

Na podstawie wypełnionej checklisty — wypisz maksymalnie 3 problemy które naprawisz w tym tygodniu.

```
PROBLEM 1: ____________________________________
Jak naprawię: _________________________________
Termin: ______________________________________

PROBLEM 2: ____________________________________
Jak naprawię: _________________________________
Termin: ______________________________________

PROBLEM 3: ____________________________________
Jak naprawię: _________________________________
Termin: ______________________________________
```

### Rezultat ćwiczenia
Po ukończeniu masz:
- Data Flow Diagram swojego workflow
- Wypełnioną RODO Checklist
- Plan poprawek na najbliższy tydzień

---

## ĆWICZENIE 2 — DODAJ HMAC VERIFICATION DO WEBHOOKA (30 minut)

### Cel
Zabezpieczyć istniejący (lub nowy testowy) webhook w n8n weryfikacją podpisu HMAC-SHA256. Po ćwiczeniu: rozumiesz mechanizm i masz działający kod który możesz stosować we wszystkich produkcyjnych webhookach.

### Co przygotować
- Działające środowisko n8n (lokalne na porcie 5678 wystarczy)
- Dostęp do terminala (lub wszelkiego klienta HTTP — Postman, Insomnia, curl)

### Krok 1: Stwórz workflow testowy (5 minut)

W n8n stwórz nowy workflow:
1. Dodaj node **Webhook** jako trigger
   - Authentication: None (będziemy to weryfikować ręcznie)
   - HTTP Method: POST
   - Path: `/test-hmac` (lub dowolny)
   - Response Mode: When Last Node Finishes
2. Dodaj node **Code** (JavaScript)
3. Dodaj node **Respond to Webhook** — zwróci odpowiedź

Aktywuj workflow i skopiuj webhook URL.

### Krok 2: Wygeneruj sekret HMAC (2 minuty)

W terminalu:
```bash
# Wygeneruj losowy sekret (32 bajty = 64 znaki hex)
openssl rand -hex 32
# Przykładowy wynik: a7f3b2c1d4e5f6078910111213141516...

# Zapisz ten sekret — będziesz go potrzebował po obu stronach
```

W n8n: Idź do **Settings → Environment Variables** (lub `.env` jeśli self-hosted):
```
WEBHOOK_SECRET=a7f3b2c1d4e5f607... (Twój sekret)
```

Zrestartuj n8n żeby zmienne środowiskowe się załadowały.

### Krok 3: Implementacja HMAC Verification w Code Node (10 minut)

Wklej poniższy kod do Code Node:

```javascript
// HMAC Webhook Verification — Dokodu Standard v1.0
const crypto = require('crypto');

// Pobierz nagłówki i body z Webhook node
const headers = $input.first().json.headers || {};
const body = $input.first().json.body || $input.first().json;

// Pobierz podpis z nagłówka
// Obsługujemy dwa formaty: "sha256=abc123" i "abc123"
const rawSignature = headers['x-signature'] ||
                     headers['x-hub-signature-256'] ||
                     headers['x-webhook-signature'] ||
                     '';

const receivedSig = rawSignature.startsWith('sha256=')
  ? rawSignature
  : 'sha256=' + rawSignature;

// Pobierz sekret ze zmiennej środowiskowej
const secret = process.env.WEBHOOK_SECRET;
if (!secret) {
  const errLog = {
    level: 'ERROR',
    event: 'webhook.config.missing_secret',
    message: 'WEBHOOK_SECRET not set in environment',
    timestamp: new Date().toISOString(),
    workflow_name: $workflow.name
  };
  console.log(JSON.stringify(errLog));
  throw new Error('Server configuration error: missing webhook secret');
}

// Oblicz oczekiwany podpis
// Użyj raw body jako string (tak jak nadawca go obliczył)
const rawBody = JSON.stringify(body);
const expectedSig = 'sha256=' + crypto
  .createHmac('sha256', secret)
  .update(rawBody, 'utf8')
  .digest('hex');

// Porównanie timing-safe (zapobiega timing attacks!)
let isValid = false;
try {
  isValid = crypto.timingSafeEqual(
    Buffer.from(receivedSig, 'utf8'),
    Buffer.from(expectedSig, 'utf8')
  );
} catch (e) {
  // Jeśli bufory mają różną długość — podpis na pewno nieprawidłowy
  isValid = false;
}

// Log wyniku weryfikacji (bez PII!)
const verifyLog = {
  level: isValid ? 'INFO' : 'WARN',
  event: isValid ? 'webhook.signature.valid' : 'webhook.signature.invalid',
  message: isValid
    ? 'Webhook signature verified successfully'
    : 'Webhook signature verification FAILED — request rejected',
  timestamp: new Date().toISOString(),
  workflow_name: $workflow.name,
  execution_id: $execution.id,
  data: {
    signature_present: rawSignature.length > 0,
    content_length: rawBody.length
  }
};
console.log(JSON.stringify(verifyLog));

if (!isValid) {
  // Zwróć 401 — Respond to Webhook node obsłuży odpowiedź
  // Throw zatrzymuje workflow
  throw new Error('401: Invalid webhook signature');
}

// Podpis prawidłowy — przekaż dane do następnych węzłów
return [{
  json: {
    verified: true,
    payload: body,
    timestamp: new Date().toISOString()
  }
}];
```

### Krok 4: Ustaw Respond to Webhook node (2 minuty)

W węźle "Respond to Webhook":
- Response Code: `200`
- Response Body: `{ "status": "ok", "verified": true }`

Podpnij go po Code Node.

Dla przypadku błędu — n8n pokaże 500. Opcjonalnie dodaj Error Workflow który zwraca 401.

### Krok 5: Test — Request bez podpisu (5 minut)

```bash
# Test 1: Request bez podpisu (powinien być odrzucony)
curl -X POST http://localhost:5678/webhook/test-hmac \
  -H "Content-Type: application/json" \
  -d '{"test": "no signature"}'

# Oczekiwany wynik: błąd / brak odpowiedzi sukcesu
```

### Krok 6: Test — Request z prawidłowym podpisem (6 minut)

Stwórz skrypt generujący podpis (test_hmac.sh lub test_hmac.py):

**Bash:**
```bash
#!/bin/bash
WEBHOOK_URL="http://localhost:5678/webhook/test-hmac"
SECRET="a7f3b2c1d4e5f607..."  # Twój sekret
BODY='{"action":"test","value":42}'

# Oblicz HMAC-SHA256
SIGNATURE="sha256=$(echo -n "$BODY" | openssl dgst -sha256 -hmac "$SECRET" | awk '{print $2}')"
echo "Obliczony podpis: $SIGNATURE"

# Wyślij request z podpisem
curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -H "X-Signature: $SIGNATURE" \
  -d "$BODY"
```

**Python (alternatywnie):**
```python
import hmac
import hashlib
import requests
import json

SECRET = "a7f3b2c1d4e5f607..."  # Twój sekret
WEBHOOK_URL = "http://localhost:5678/webhook/test-hmac"

body = {"action": "test", "value": 42}
body_str = json.dumps(body, separators=(',', ':'))

signature = "sha256=" + hmac.new(
    SECRET.encode('utf-8'),
    body_str.encode('utf-8'),
    hashlib.sha256
).hexdigest()

print(f"Podpis: {signature}")

response = requests.post(
    WEBHOOK_URL,
    json=body,
    headers={"X-Signature": signature}
)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
```

```bash
# Oczekiwany wynik: {"status": "ok", "verified": true}
```

### Krok 7: Test — Request z błędnym podpisem (2 minuty)

```bash
# Test 3: Request z fałszywym podpisem
curl -X POST http://localhost:5678/webhook/test-hmac \
  -H "Content-Type: application/json" \
  -H "X-Signature: sha256=fakesignature123" \
  -d '{"action": "test"}'

# Oczekiwany wynik: błąd — workflow odrzuca request
```

### Weryfikacja ukończenia ćwiczenia

- [ ] Workflow z HMAC verification działa w n8n
- [ ] Request bez podpisu → odrzucony
- [ ] Request z prawidłowym podpisem → przetworzony
- [ ] Request z błędnym podpisem → odrzucony
- [ ] Logi WARN w n8n execution panel dla odrzuconych requestów
- [ ] `WEBHOOK_SECRET` jest w env variable, nie w kodzie

---

## ZADANIE DOMOWE — DATA FLOW DIAGRAM DLA TWOJEGO WORKFLOW

### Cel
Stworzyć pełny Data Flow Diagram (DFD) dla swojego głównego workflow — dokumentację która pokazuje gdzie przepływają dane osobowe i co się z nimi dzieje.

### Dlaczego to ważne
- Wymóg dokumentacyjny RODO (Art. 30 — Rejestr czynności przetwarzania)
- Podstawa do DPIA jeśli projekt wchodzi w high-risk
- Niezbędne przy onboardingu nowej osoby do projektu
- Klient enterprise może o to poprosić

### Co ma zawierać DFD

**1. Lista systemów (Data Stores)**
Wypisz wszystkie systemy gdzie dane trafiają i zostają:
```
□ n8n (execution history)
□ [Twój CRM — nazwa]
□ [Google Sheets / Airtable — nazwa arkusza]
□ [Newsletter — platforma]
□ [OpenAI / Anthropic API] ← zewnętrzne!
□ [Baza danych — typ]
□ [Inne...]
```

**2. Lista przepływów danych (Data Flows)**
Dla każdego przepływu zanotuj:
```
Przepływ: [System A] → [System B]
Dane: [lista pól]
Zawiera PII?: TAK/NIE
Podstawa prawna: [Art. 6 RODO podstawa]
Szyfrowanie: TAK/NIE (TLS/AES)
Umowa DPA z System B: TAK/NIE
```

**3. Punkty retencji danych**
Dla każdego systemu — jak długo dane tam siedzą:
```
n8n execution history: [X] dni (EXECUTIONS_DATA_MAX_AGE)
CRM: [X] lat / do wycofania zgody
Google Sheets: [X] lat / raz na rok czyszczone / brak polityki
OpenAI: dane nie są przechowywane po odpowiedzi (sprawdź DPA!)
```

**4. Procedura RTBF (Right to be Forgotten)**
Napisz (nawet jedno zdanie) jak obsłużysz wniosek o usunięcie danych:
```
Gdy dostanę wniosek o usunięcie danych osoby X:
1. Usunę/pseudonimizuję w: [lista systemów]
2. Czego nie mogę usunąć i dlaczego: [faktury: 5 lat]
3. Jak poinformuję osobę: [email z potwierdzeniem]
4. Termin: 30 dni od wniosku
```

### Format
Możesz użyć dowolnego narzędzia: kartka i zdjęcie, Miro, FigJam, draw.io, Notion, zwykły Markdown. Liczy się treść, nie estetyka.

### Termin
Prześlij na forum kursu lub zachowaj dla siebie — ale naprawdę zrób to. Bez tej mapy nie wiesz czy Twój system jest bezpieczny i zgodny z RODO.

---

## ĆWICZENIE 3 — AUDIT LOG DO GOOGLE SHEETS (20 minut)

### Cel
Dodać do istniejącego workflow mechanizm logowania zdarzeń do Google Sheets — bez żadnych danych osobowych. Po ćwiczeniu: masz działający system audit trail, który możesz pokazać klientowi enterprise jako dowód kontroli procesu.

### Dlaczego audit log?
- Wymóg compliance w projektach enterprise (ISO 27001, SOC2, RODO Art. 5 — rozliczalność)
- Niezbędny do debugowania problemów w produkcji
- Klient widzi "co workflow zrobił z jego danymi" bez oddawania mu dostępu do n8n
- Dowód działania SLA: "workflow przetworzył 1 247 rekordów w marcu, 0 błędów"

### Co przygotować
- Google Sheet: stwórz nowy arkusz o nazwie "n8n_Audit_Log"
- Stwórz dwie zakładki (sheet tabs): `Execution_Log` i `Error_Log`
- Google Credentials w n8n (Service Account lub OAuth2)

### Krok 1: Przygotuj strukturę arkusza (3 minuty)

W zakładce **Execution_Log** dodaj nagłówki w wierszu 1:

```
A1: timestamp
B1: workflow_name
C1: execution_id
D1: action
E1: status
F1: records_processed
G1: duration_ms
H1: notes
```

W zakładce **Error_Log** dodaj nagłówki w wierszu 1:

```
A1: timestamp
B1: workflow_name
C1: execution_id
D1: error_type
E1: error_message
F1: node_name
G1: records_affected
H1: resolved
```

**Zauważ:** żadna kolumna nie zawiera imienia, emaila, telefonu ani żadnego innego PII. To jest zasada — audit log loguje zdarzenia, nie dane osobowe.

### Krok 2: Dodaj Set Node — przygotowanie danych logu (5 minut)

W swoim istniejącym workflow, przed finalnym węzłem (lub po głównej logice), dodaj węzeł **Edit Fields (Set)** o nazwie `Prepare Audit Entry`:

```
Ustaw następujące pola:
- log_timestamp    → {{ $now.toISO() }}
- log_workflow     → {{ $workflow.name }}
- log_execution    → {{ $execution.id }}
- log_action       → "lead.processed"     ← opisz co workflow robi
- log_status       → "success"
- log_records      → {{ $items().length }}
- log_notes        → ""
```

Zmieniaj wartość `log_action` stosownie do kontekstu: `"email.sent"`, `"crm.updated"`, `"invoice.generated"` itp. Używaj formatu `obiekt.czynność` — łatwo filtrować i agregować.

### Krok 3: Dodaj Google Sheets Node — zapis do Execution_Log (5 minut)

Dodaj węzeł **Google Sheets** o nazwie `Write Audit Log`:

```
Operation:    Append Row
Document:     [wybierz swój "n8n_Audit_Log"]
Sheet:        Execution_Log
Column Mapping (tryb ręczny):
  timestamp           → {{ $json.log_timestamp }}
  workflow_name       → {{ $json.log_workflow }}
  execution_id        → {{ $json.log_execution }}
  action              → {{ $json.log_action }}
  status              → {{ $json.log_status }}
  records_processed   → {{ $json.log_records }}
  duration_ms         → (zostaw puste — opcjonalne)
  notes               → {{ $json.log_notes }}
```

Podłącz ten węzeł na końcu głównej gałęzi workflow (po sukcesie).

### Krok 4: Dodaj Error Log (7 minut)

Przejdź do **Settings** workflow → włącz **Error Workflow** lub użyj alternatywnej ścieżki. Dodaj drugi węzeł **Google Sheets** o nazwie `Write Error Log` — podłącz go do Error Workflow lub do gałęzi błędów:

```
Operation:    Append Row
Document:     [ten sam "n8n_Audit_Log"]
Sheet:        Error_Log
Column Mapping:
  timestamp         → {{ $now.toISO() }}
  workflow_name     → {{ $workflow.name }}
  execution_id      → {{ $execution.id }}
  error_type        → {{ $json.error?.name || "UnknownError" }}
  error_message     → {{ $json.error?.message || "No message" }}
  node_name         → {{ $json.error?.node?.name || "Unknown" }}
  records_affected  → 0
  resolved          → FALSE
```

**Ważne:** `error_message` może przypadkowo zawierać fragmenty danych wejściowych jeśli węzeł wyrzucił błąd zawierający payload. Przejrzyj komunikaty błędów n8n w swoim workflow i oceń czy nie wyciekają tam dane osobowe. Jeśli tak — dodaj sanitizację:

```javascript
// W Code Node przed Write Error Log:
const rawMsg = $json.error?.message || '';
// Usuń wzorce wyglądające jak email
const cleanMsg = rawMsg.replace(/[\w.-]+@[\w.-]+\.\w+/g, '[EMAIL_REDACTED]');
return [{ json: { ...($json), error_message_clean: cleanMsg } }];
```

### Weryfikacja ukończenia ćwiczenia

- [ ] Google Sheet "n8n_Audit_Log" z zakładkami Execution_Log i Error_Log
- [ ] Workflow zapisuje wiersz w Execution_Log po każdym udanym wykonaniu
- [ ] Workflow zapisuje wiersz w Error_Log po każdym błędzie
- [ ] Żadna kolumna nie zawiera danych osobowych (email, imię, telefon)
- [ ] Przetestowałem/am: uruchom workflow → sprawdź Sheets → wiersz się pojawił
- [ ] Przetestowałem/am: sprowokuj błąd → Error_Log ma nowy wiersz

### Bonus — Dashboard w Google Sheets

Gdy masz już dane w arkuszu, stwórz trzecią zakładkę `Dashboard` i użyj formuł:

```
Liczba wykonań dziś:
=COUNTIFS(Execution_Log!A:A,">="&TODAY(),Execution_Log!A:A,"<"&TODAY()+1)

Liczba błędów w tym tygodniu:
=COUNTIFS(Error_Log!A:A,">="&(TODAY()-WEEKDAY(TODAY(),2)+1))

Najczęstszy błąd:
=INDEX(Error_Log!D:D,MATCH(MAX(COUNTIF(Error_Log!D:D,Error_Log!D:D)),COUNTIF(Error_Log!D:D,Error_Log!D:D),0))
```

Możesz ten dashboard osadzić jako iFrame w Notion lub pokazać klientowi jako "live monitoring panel".

---

## MATERIAŁY DODATKOWE

- `05_Workflow_Blueprint.md` — gotowe workflow n8n do użycia (HMAC, pseudonimizacja, RTBF)
- Logging Standard: `30_RESOURCES/RES_Templates/Logging_Standard.md`
- RODO Checklist: `20_AREAS/AREA_Legal_Compliance/RODO_Checklist.md`
- AI Act Tracker: `20_AREAS/AREA_Legal_Compliance/AI_Act_Tracker.md`
- Stripe webhook IP list: https://stripe.com/docs/ips (jeśli integrujesz Stripe)
- HmacSHA256 playground: https://www.devglan.com/online-tools/hmac-sha256-online
