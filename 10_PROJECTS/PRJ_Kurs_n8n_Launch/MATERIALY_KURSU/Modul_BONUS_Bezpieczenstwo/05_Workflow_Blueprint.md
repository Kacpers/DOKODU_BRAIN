---
type: course-material
modul: BONUS_A
status: ready
owner: kacper
last_reviewed: 2026-03-27
tags: [kurs, n8n, bezpieczenstwo, blueprint, workflow, hmac, rodo, pseudonimizacja, rtbf]
---

# Moduł BONUS A — Workflow Blueprint: Secure n8n Template

> **Cel:** Kompletny szablon bezpiecznego workflow n8n — do skopiowania i adaptacji.
> **Zawiera:** HMAC verification, pseudonimizacja PII, audit log, RTBF handler.
> **Format:** Specyfikacja węzłów + pełny kod JavaScript dla Code Nodes.

---

## ARCHITEKTURA SECURE WORKFLOW TEMPLATE

```
[Webhook: POST /secure-endpoint]
    ↓
[Code: HMAC Signature Verification]  ← WARSTWA 1: Autentyczność
    ↓ (odrzuć jeśli błędny podpis)
[Code: PII Pseudonymization]         ← WARSTWA 2: Prywatność danych
    ↓
[Twoja logika biznesowa...]          ← WARSTWA 3: Przetwarzanie
    ↓
[Code: Audit Log Writer]             ← WARSTWA 4: Rozliczalność
    ↓
[Respond to Webhook: 200 OK]
```

**Równoległy workflow:**
```
[Webhook: RTBF Request]              ← RTBF Handler (osobny workflow)
    → [Verify Identity]
    → [Search All Systems]
    → [Delete / Pseudonymize]
    → [Send Confirmation]
    → [Log to RTBF Registry]
```

---

## BLUEPRINT 1 — HMAC SIGNATURE VERIFICATION

### Węzeł: `Webhook`
```
Type: Webhook (Trigger)
HTTP Method: POST
Path: /secure-endpoint
Authentication: None (weryfikujemy ręcznie w Code Node)
Response Mode: When Last Node Finishes
```

### Węzeł: `Code — HMAC Verification`

```javascript
// ============================================================
// HMAC Webhook Verification — Dokodu Secure Template v1.0
// Kopiuj bez modyfikacji. Zmieniaj tylko HEADER_NAME.
// ============================================================

const crypto = require('crypto');

// --- KONFIGURACJA ---
// Nazwa nagłówka z podpisem (dopasuj do nadawcy)
// GitHub: 'x-hub-signature-256'
// Stripe: 'stripe-signature' (Stripe ma własny format — patrz docs)
// Własny system: 'x-signature'
const HEADER_NAME = 'x-signature';

// --- POBIERZ DANE Z WEBHOOKA ---
const webhookData = $input.first().json;
const headers = webhookData.headers || {};
const body = webhookData.body || webhookData;

// Body jako string (musi być identyczne jak u nadawcy)
const rawBody = JSON.stringify(body);

// --- POBIERZ PODPIS Z NAGŁÓWKA ---
const rawSignature = (headers[HEADER_NAME] || '').trim();

if (!rawSignature) {
  const log = {
    level: 'WARN',
    event: 'webhook.signature.missing',
    message: `Brakujący nagłówek ${HEADER_NAME} — request odrzucony`,
    timestamp: new Date().toISOString(),
    workflow_name: $workflow.name,
    execution_id: $execution.id,
    data: { header_checked: HEADER_NAME }
  };
  console.log(JSON.stringify(log));
  throw new Error(`Missing ${HEADER_NAME} header`);
}

// Normalize: obsługujemy "sha256=abc" i "abc"
const receivedSig = rawSignature.startsWith('sha256=')
  ? rawSignature
  : 'sha256=' + rawSignature;

// --- POBIERZ SEKRET ---
const secret = process.env.WEBHOOK_SECRET;
if (!secret) {
  console.log(JSON.stringify({
    level: 'ERROR',
    event: 'webhook.config.error',
    message: 'WEBHOOK_SECRET nie jest ustawiony w zmiennych środowiskowych',
    timestamp: new Date().toISOString()
  }));
  throw new Error('Server configuration error');
}

// --- OBLICZ OCZEKIWANY PODPIS ---
const expectedSig = 'sha256=' + crypto
  .createHmac('sha256', secret)
  .update(rawBody, 'utf8')
  .digest('hex');

// --- PORÓWNANIE TIMING-SAFE ---
// WAŻNE: NIE używaj === do porównania podpisów!
// Timing attack: atakujący mierzy czas odpowiedzi żeby odgadnąć sekret.
// timingSafeEqual zawsze porównuje przez ten sam czas.
let isValid = false;
try {
  const received = Buffer.from(receivedSig, 'utf8');
  const expected = Buffer.from(expectedSig, 'utf8');

  if (received.length === expected.length) {
    isValid = crypto.timingSafeEqual(received, expected);
  }
  // Jeśli różne długości → isValid pozostaje false
} catch (e) {
  isValid = false;
}

// --- LOG REZULTATU ---
console.log(JSON.stringify({
  level: isValid ? 'INFO' : 'WARN',
  event: isValid ? 'webhook.verified' : 'webhook.rejected',
  message: isValid
    ? 'Webhook HMAC verification: OK'
    : 'Webhook HMAC verification: FAILED — potencjalny atak lub błąd konfiguracji',
  timestamp: new Date().toISOString(),
  workflow_name: $workflow.name,
  execution_id: $execution.id,
  data: {
    body_length: rawBody.length,
    signature_present: true,
    verified: isValid
  }
}));

if (!isValid) {
  throw new Error('401: Invalid webhook signature');
}

// --- PRZEKAŻ DANE DALEJ ---
return [{
  json: {
    _hmac_verified: true,
    _received_at: new Date().toISOString(),
    ...body
  }
}];
```

---

## BLUEPRINT 2 — PSEUDONIMIZACJA DANYCH OSOBOWYCH

### Węzeł: `Code — PII Pseudonymization`

```javascript
// ============================================================
// PII Pseudonymization — Dokodu Secure Template v1.0
// Zastosuj PRZED wysyłką danych do zewnętrznych API (OpenAI, etc.)
// i PRZED zapisem do logów.
// ============================================================

const crypto = require('crypto');

// --- KONFIGURACJA ---
// Salt musi być unikalny per deployment i tajny.
// Przechowuj w zmiennych środowiskowych.
const SALT = process.env.PSEUDONYM_SALT || 'default-salt-change-me';

// Pola które zostaną PSEUDONIMIZOWANE (hash — odwracalne z kluczem mapowania)
const PSEUDONYMIZE_FIELDS = [
  'email', 'phone', 'mobile', 'tel',
  'userId', 'user_id', 'customerId', 'customer_id',
  'leadId', 'lead_id'
];

// Pola które zostaną ANONIMIZOWANE (nieodwracalne zastąpienie)
const ANONYMIZE_FIELDS = [
  'firstName', 'first_name', 'lastName', 'last_name',
  'name', 'fullName', 'full_name',
  'address', 'street', 'city', 'postalCode', 'postal_code',
  'pesel', 'nip', 'ssn', 'passport',
  'dateOfBirth', 'date_of_birth', 'birthdate'
];

// Pola IP — pseudonimizowane (odcinamy ostatni oktet dla częściowej anonimizacji)
const IP_FIELDS = ['ip', 'ipAddress', 'ip_address', 'clientIp', 'client_ip'];

// --- FUNKCJE ---

const pseudonymize = (value) => {
  if (value === null || value === undefined) return null;
  const str = String(value).toLowerCase().trim();
  return crypto
    .createHash('sha256')
    .update(SALT + str)
    .digest('hex')
    .substring(0, 16); // 16 znaków wystarczy, pełne 64 to overkill
};

const anonymizeIp = (ip) => {
  if (!ip) return null;
  // IPv4: 192.168.1.45 → 192.168.1.x
  if (ip.includes('.')) {
    const parts = ip.split('.');
    parts[parts.length - 1] = 'x';
    return parts.join('.');
  }
  // IPv6: skróć do pierwszych 4 grup
  if (ip.includes(':')) {
    const parts = ip.split(':');
    return parts.slice(0, 4).join(':') + ':xxxx:xxxx:xxxx:xxxx';
  }
  return '[IP_REDACTED]';
};

const processObject = (obj, depth = 0) => {
  if (depth > 5) return obj; // Zapobiegaj nieskończonej rekurencji
  if (!obj || typeof obj !== 'object') return obj;
  if (Array.isArray(obj)) return obj.map(item => processObject(item, depth + 1));

  const result = {};

  for (const [key, value] of Object.entries(obj)) {
    const keyLower = key.toLowerCase();

    if (IP_FIELDS.some(f => keyLower === f.toLowerCase())) {
      result[key] = anonymizeIp(value);
      result[`_${key}_pseudonymized`] = true;
    } else if (PSEUDONYMIZE_FIELDS.some(f => keyLower === f.toLowerCase())) {
      result[key] = pseudonymize(value);
      result[`_${key}_pseudonymized`] = true;
    } else if (ANONYMIZE_FIELDS.some(f => keyLower === f.toLowerCase())) {
      result[key] = '[REDACTED]';
      result[`_${key}_anonymized`] = true;
    } else if (typeof value === 'object' && value !== null) {
      result[key] = processObject(value, depth + 1);
    } else {
      result[key] = value;
    }
  }

  return result;
};

// --- PRZETWARZANIE ---
const items = $input.all();

const processedItems = items.map(item => {
  const originalJson = item.json;
  const pseudonymizedJson = processObject(originalJson);

  // Log pseudonimizacji (bez oryginalnych danych!)
  console.log(JSON.stringify({
    level: 'INFO',
    event: 'data.pseudonymized',
    message: 'PII pseudonimizacja zakończona',
    timestamp: new Date().toISOString(),
    workflow_name: $workflow.name,
    execution_id: $execution.id,
    data: {
      fields_processed: Object.keys(originalJson).length,
      pseudonymized: PSEUDONYMIZE_FIELDS.filter(f =>
        Object.keys(originalJson).some(k => k.toLowerCase() === f.toLowerCase())
      ),
      anonymized: ANONYMIZE_FIELDS.filter(f =>
        Object.keys(originalJson).some(k => k.toLowerCase() === f.toLowerCase())
      )
    }
  }));

  return { json: pseudonymizedJson };
});

return processedItems;
```

---

## BLUEPRINT 3 — AUDIT LOG WRITER

### Opis
Węzeł zapisujący strukturalny audit log do Google Sheets (lub innej bazy). Stosuj po każdej ważnej operacji — szczególnie w systemach AI i przy przetwarzaniu danych osobowych.

### Węzeł: `Code — Prepare Audit Log`

```javascript
// ============================================================
// Audit Log Preparation — Dokodu Secure Template v1.0
// Przygotowuje wpis do Google Sheets / zewnętrznej bazy danych.
// WAŻNE: Nie loguj PII — używaj pseudonimów z poprzedniego węzła.
// ============================================================

const items = $input.all();

const auditEntries = items.map(item => {
  const data = item.json;

  return {
    json: {
      // Pola obowiązkowe w audit logu
      timestamp: new Date().toISOString(),
      date: new Date().toLocaleDateString('pl-PL'),

      // Workflow context
      workflow_name: $workflow.name,
      workflow_id: $workflow.id,
      execution_id: $execution.id,

      // Zdarzenie
      event: data._audit_event || 'data.processed',
      event_category: data._audit_category || 'general',
      status: data._audit_status || 'success',

      // Dane (bez PII — tylko pseudonimy i statystyki)
      subject_id: data.userId || data.user_id ||
                  data.customerId || data.customer_id || null,
      // subject_id powinien być już pseudonimem z poprzedniego węzła

      // Metadane operacji
      items_processed: items.length,
      processing_duration_hint: data._duration_ms || null,

      // AI-specific (jeśli to workflow z AI)
      ai_model: data._ai_model || null,
      ai_model_version: data._ai_model_version || null,

      // Dodatkowy kontekst
      source: data._source || 'n8n_workflow',
      environment: process.env.NODE_ENV || 'production',

      // Uwagi (bez PII!)
      notes: data._audit_notes || null
    }
  };
});

return auditEntries;
```

### Węzeł: `Google Sheets — Append Audit Log`

```
Operation: Append
Spreadsheet ID: [ID Twojego arkusza]
Sheet Name: AuditLog
Columns: Automatyczne (mapuj pola z poprzedniego węzła)
```

**Struktura arkusza Google Sheets (nagłówki):**
```
timestamp | date | workflow_name | workflow_id | execution_id |
event | event_category | status | subject_id | items_processed |
processing_duration_hint | ai_model | ai_model_version | source |
environment | notes
```

**Retencja:** Usuń wpisy starsze niż 12 miesięcy (dla high-risk AI: 24 miesiące). Możesz to zautomatyzować osobnym workflow — Trigger co miesiąc → usuń stare wiersze z arkusza.

---

## BLUEPRINT 4 — RTBF (RIGHT TO BE FORGOTTEN) HANDLER

### Opis
Osobny workflow obsługujący wnioski o usunięcie danych (Art. 17 RODO). Uruchamiany przez formularz na stronie lub bezpośredni webhook.

### Architektura RTBF Workflow

```
[Webhook: POST /rtbf-request]
    ↓
[Code: Validate & Rate Limit]        ← Max 1 wniosek per email per 30 dni
    ↓
[HTTP Request: Send Verification Email]  ← Token jednorazowy, ważny 24h
    ↓
[WAIT: Potwierdzenie przez email]
    ↓ (po kliknięciu linku potwierdzającego)
[Code: Search All Systems]
    ↓
[Switch: System Type]
    ├──→ [HTTP: Delete from CRM]
    ├──→ [HTTP: Unsubscribe from Newsletter]
    ├──→ [Google Sheets: Remove rows]
    └──→ [HTTP: Delete from custom DB]
    ↓
[Code: Generate RTBF Report]
    ↓
[HTTP Request: Send Confirmation Email]
    ↓
[Google Sheets: Append to RTBF Registry]  ← Dokumentacja dla UODO
```

### Węzeł: `Code — RTBF Search All Systems`

```javascript
// ============================================================
// RTBF — Search & Pseudonymize All Systems
// Dokodu Secure Template v1.0
// UWAGA: Dostosuj do systemów których używasz!
// ============================================================

const crypto = require('crypto');

const input = $input.first().json;
const subjectEmail = input.email; // Zweryfikowany email z tokenu
const requestId = input.request_id || crypto.randomUUID();

// Oblicz pseudonim żeby wyszukać we wszystkich systemach
const SALT = process.env.PSEUDONYM_SALT;
const subjectPseudonym = crypto
  .createHash('sha256')
  .update(SALT + subjectEmail.toLowerCase().trim())
  .digest('hex')
  .substring(0, 16);

// Log rozpoczęcia (bez emaila!)
console.log(JSON.stringify({
  level: 'INFO',
  event: 'rtbf.search.started',
  message: 'RTBF: Rozpoczęto wyszukiwanie danych we wszystkich systemach',
  timestamp: new Date().toISOString(),
  workflow_name: $workflow.name,
  execution_id: $execution.id,
  data: {
    request_id: requestId,
    subject_pseudonym: subjectPseudonym, // pseudonim, nie email!
    systems_to_check: ['CRM', 'Newsletter', 'Google Sheets', 'n8n Executions']
  }
}));

// Przekaż do kolejnych węzłów
return [{
  json: {
    request_id: requestId,
    subject_email: subjectEmail,       // TYLKO do wysyłki emaila potwierdzającego
    subject_pseudonym: subjectPseudonym, // Do wyszukiwania w systemach
    search_started_at: new Date().toISOString(),
    systems: {
      crm: { status: 'pending' },
      newsletter: { status: 'pending' },
      sheets: { status: 'pending' },
      n8n: { status: 'pending' }
    }
  }
}];
```

### Węzeł: `Code — Generate RTBF Report`

```javascript
// ============================================================
// RTBF — Generate Report & Compliance Record
// ============================================================

const input = $input.first().json;
const results = input.deletion_results || {};

// Zbuduj raport bez PII (email zastąpiony pseudonimem w logu)
const report = {
  request_id: input.request_id,
  subject_pseudonym: input.subject_pseudonym,
  request_received_at: input.search_started_at,
  completed_at: new Date().toISOString(),

  // Wyniki usunięcia per system
  systems_processed: {
    crm: results.crm || { status: 'unknown' },
    newsletter: results.newsletter || { status: 'unknown' },
    google_sheets: results.sheets || { status: 'unknown' },
    n8n_executions: results.n8n || { status: 'skipped', note: 'n8n execution logs retain for 30 days then auto-delete' }
  },

  // Wyjątki — dane których NIE usunięto i dlaczego
  exceptions: [
    {
      system: 'invoices',
      reason: 'Obowiązek prawny — Art. 6(1)(c) RODO. Faktury przechowywane 5 lat zgodnie z Ustawą o rachunkowości.',
      retention_end: new Date(Date.now() + 5 * 365 * 24 * 60 * 60 * 1000).toFullYear + '-12-31'
    }
  ],

  // Podsumowanie dla rejestru RODO (Art. 30)
  compliance_note: 'Wniosek RTBF przetworzony w terminie ustawowym (30 dni). Dane usunięte lub pseudonimizowane we wszystkich systemach z wyjątkiem wymienionych powyżej.',

  // Email do wysyłki potwierdzenia (TYLKO do tego celu)
  _send_confirmation_to: input.subject_email
};

console.log(JSON.stringify({
  level: 'INFO',
  event: 'rtbf.completed',
  message: 'RTBF: Proces usunięcia danych zakończony',
  timestamp: new Date().toISOString(),
  data: {
    request_id: report.request_id,
    subject_pseudonym: report.subject_pseudonym,
    systems_count: Object.keys(report.systems_processed).length,
    exceptions_count: report.exceptions.length
  }
}));

return [{ json: report }];
```

### Węzeł: `Google Sheets — RTBF Registry`

Zapisuj każdy wniosek RTBF do osobnego arkusza "RTBF_Registry" dla dokumentacji UODO.

**Kolumny rejestru:**
```
request_id | request_date | completed_date | subject_pseudonym |
systems_cleared | exceptions | response_within_30_days | notes
```

**Ważne:** Nie zapisuj emaila osoby wnioskującej do rejestru — pseudonim wystarczy do celów dokumentacyjnych. Email możesz zachować tylko tymczasowo do wysłania potwierdzenia.

---

## INSTRUKCJA WDROŻENIA

### Krok 1: Zmienne środowiskowe (`.env`)
```bash
# Wymagane dla Secure Template
N8N_ENCRYPTION_KEY=<openssl rand -hex 32>
WEBHOOK_SECRET=<openssl rand -hex 32>
PSEUDONYM_SALT=<openssl rand -hex 32>

# Różne wartości na dev i prod!
NODE_ENV=production
```

### Krok 2: Kolejność węzłów w workflow
```
1. Webhook (Trigger)
2. Code: HMAC Verification      ← ZAWSZE pierwszy po webhooku
3. Code: PII Pseudonymization   ← PRZED jakimkolwiek logowaniem lub AI
4. [Twoja logika biznesowa]
5. Code: Prepare Audit Log
6. Google Sheets / DB: Write Audit Log
7. Respond to Webhook
```

### Krok 3: Testowanie przed produkcją
```bash
# 1. Test bez podpisu → powinien odrzucić
curl -X POST https://n8n.twoja.domena.pl/webhook/secure-endpoint \
  -H "Content-Type: application/json" \
  -d '{"test": true}'

# 2. Test z prawidłowym podpisem → powinien przepuścić
# (użyj skryptu z Ćwiczenia 2)

# 3. Sprawdź audit log w Google Sheets — powinien mieć wpis
```

### Krok 4: Checklist przed uruchomieniem produkcyjnym
- [ ] `N8N_ENCRYPTION_KEY` ustawiony i silny (min. 32 bajty losowe)
- [ ] `WEBHOOK_SECRET` ustawiony (różny od dev!)
- [ ] `PSEUDONYM_SALT` ustawiony (różny od dev!)
- [ ] n8n za Nginx reverse proxy (nie port 5678 bezpośrednio)
- [ ] TLS/HTTPS aktywne
- [ ] Audit log arkusz Google Sheets skonfigurowany
- [ ] RTBF workflow aktywny (jeśli przetwarzasz dane osobowe)
- [ ] Test wszystkich trzech scenariuszy webhooka (bez podpisu, zły podpis, dobry podpis)

---

## UWAGI DLA ZAAWANSOWANYCH

### Integracja z Microsoft Presidio

Jeśli wysyłasz dane do zewnętrznych LLM (OpenAI, Anthropic) — dodaj Presidio między węzłem pseudonimizacji a węzłem HTTP do API:

```javascript
// W Code Node — wywołanie Presidio Analyzer (lokalny Docker)
const presidioResponse = await fetch('http://presidio-analyzer:5001/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: inputText,
    language: 'pl',
    entities: ['EMAIL_ADDRESS', 'PHONE_NUMBER', 'PERSON', 'PL_PESEL', 'PL_NIP']
  })
});

const entities = await presidioResponse.json();
// Następnie Presidio Anonymizer zastępuje wykryte PII
```

### Rotacja kluczy WEBHOOK_SECRET

Zmień `WEBHOOK_SECRET` co 90 dni. Workflow do automatycznej rotacji:
```
[Cron: co 90 dni]
    → [Generuj nowy sekret: openssl rand -hex 32]
    → [Aktualizuj w Vault lub .env przez SSH]
    → [Wyślij powiadomienie do nadawcy (żeby zaktualizował swój sekret)]
    → [Restart n8n]
```

### Rate Limiting na poziomie n8n

Dodaj do każdego wrażliwego webhooka węzeł sprawdzający czy execution limit nie jest przekraczany:

```javascript
// Sprawdź liczbę wywołań z danego IP w ostatnich 5 minutach
// Wymaga zewnętrznej bazy (Redis) lub Google Sheets jako cache
// Implementacja: patrz Blueprint BP-006 w N8N_Blueprints.md
```

---

## CHECKLIST BEZPIECZNEGO N8N DEPLOYMENT (10 PUNKTÓW)

> Przejdź przez tę listę PRZED każdym uruchomieniem produkcyjnym. Zero wyjątków.

### Sieć i dostęp

- [ ] **1. n8n wystawiony przez reverse proxy (Nginx/Caddy), nie bezpośrednio na port 5678**
  - Port 5678 nigdy nie powinien być dostępny z zewnątrz
  - Nginx terminuje TLS, przekazuje ruch na localhost:5678
  - Sprawdź: `curl http://twoja.domena:5678` powinno zwrócić connection refused

- [ ] **2. TLS/HTTPS aktywne z ważnym certyfikatem (Let's Encrypt lub komercyjnym)**
  - Automatyczne odnowienie certyfikatu skonfigurowane (certbot --standalone lub Caddy auto)
  - HSTS nagłówek ustawiony w Nginx: `add_header Strict-Transport-Security "max-age=31536000"`
  - Sprawdź: `curl -I https://twoja.domena` → `Strict-Transport-Security` w headerach

- [ ] **3. Firewall skonfigurowany — tylko porty 80, 443 (i 22 dla SSH) otwarte**
  - UFW lub iptables: `ufw allow 80/tcp && ufw allow 443/tcp && ufw allow 22/tcp && ufw enable`
  - Sprawdź z zewnątrz: `nmap -p 5678 twoja.domena` → "filtered" lub "closed"

### Zmienne środowiskowe i sekrety

- [ ] **4. `N8N_ENCRYPTION_KEY` ustawiony — silny, losowy, unikalny per deployment**
  - Generuj: `openssl rand -hex 32`
  - Nie używaj tego samego klucza na dev i prod
  - Backup klucza w bezpiecznym miejscu — utrata = utrata wszystkich credentials w n8n

- [ ] **5. `WEBHOOK_SECRET` i `PSEUDONYM_SALT` ustawione i różne od wartości deweloperskich**
  - Każdy sekret generuj osobno: `openssl rand -hex 32`
  - Przechowuj w HashiCorp Vault, AWS Secrets Manager lub zaszyfrowanym `.env` (nie w repo Git)
  - Sprawdź: `grep -r "WEBHOOK_SECRET" .git/` — nie powinno nic zwrócić

- [ ] **6. Plik `.env` wykluczony z repozytorium Git (`.gitignore`)**
  - Sprawdź historię: `git log --all --full-history -- .env` — jeśli cokolwiek zwraca, sekret jest kompromitowany
  - Jeśli już trafił do repo: natychmiast rotuj wszystkie klucze, usuń z historii Gita (`git filter-branch`)

### Uwierzytelnianie i autoryzacja

- [ ] **7. Panel n8n zabezpieczony hasłem lub SSO (nie dostępny publicznie bez logowania)**
  - Opcja A: `N8N_BASIC_AUTH_ACTIVE=true` + silne hasło w `N8N_BASIC_AUTH_USER/PASSWORD`
  - Opcja B: n8n Enterprise z SSO (SAML/OIDC) — polecane dla zespołów
  - Opcja C: n8n dostępny tylko przez VPN (najsilniejsza opcja)
  - Sprawdź: otwórz panel w oknie prywatnym — powinien wymagać logowania

- [ ] **8. Konta użytkowników z minimalnym zakresem uprawnień (zasada least privilege)**
  - Każdy operator ma osobne konto — nie używaj jednego konta "admin" dla wszystkich
  - Konta serwisowe (dla API) mają uprawnienia tylko do potrzebnych workflowów
  - Regularny audyt: usuń konta nieaktywne > 90 dni

### Monitorowanie i backup

- [ ] **9. Automatyczny backup bazy danych n8n (SQLite lub PostgreSQL) — minimum co 24h**
  - SQLite: `cron: 0 2 * * * cp /data/n8n/database.sqlite /backups/n8n_$(date +%Y%m%d).sqlite`
  - PostgreSQL: `pg_dump n8n | gzip > /backups/n8n_$(date +%Y%m%d).sql.gz`
  - Backup wysyłany poza serwer (S3, Dropbox, zewnętrzny SFTP) — backup lokalny to nie backup
  - Test restore raz na miesiąc — backup bez testu restore = brak backupu

- [ ] **10. Audit log aktywny i monitorowany — alerty na anomalie**
  - Workflow Audit Log Writer (Blueprint 3 z tego modułu) aktywny we wszystkich workflow produkcyjnych
  - Alert na > 100 failed executions w ciągu godziny (prawdopodobny atak lub awaria)
  - Alert na nieudaną weryfikację HMAC (potencjalny replay attack)
  - Przegląd logów minimum raz w tygodniu (lub zautomatyzowany raport na email)

---

### Podsumowanie checklisty

| # | Kategoria | Punkt | Status |
|---|-----------|-------|--------|
| 1 | Sieć | Reverse proxy (nie port 5678) | |
| 2 | Sieć | TLS/HTTPS + HSTS | |
| 3 | Sieć | Firewall (tylko 80/443/22) | |
| 4 | Sekrety | N8N_ENCRYPTION_KEY | |
| 5 | Sekrety | WEBHOOK_SECRET + PSEUDONYM_SALT | |
| 6 | Sekrety | .env poza Git | |
| 7 | AuthN | Panel za logowaniem/VPN | |
| 8 | AuthZ | Least privilege + osobne konta | |
| 9 | Backup | Automatyczny backup + test restore | |
| 10 | Monitoring | Audit log + alerty na anomalie | |

**Wynik poniżej 10/10 = nie wdrażaj na produkcję.**
