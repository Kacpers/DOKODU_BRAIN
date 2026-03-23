---
type: resource
status: active
owner: kacper
last_reviewed: 2026-03-06
tags: [n8n, logging, standard, infrastruktura, debugging]
related: [[N8N_Blueprints]], [[AREA_n8n_Infrastructure]]
---

# LOGGING STANDARD — Dokodu n8n v1.0
> Obowiazkowy dla wszystkich workflowow produkcyjnych.
> Cel: logi muszą pozwolić odtworzyc CO sie stalo, KIEDY i DLACZEGO — bez dostępu do systemu zrodlowego.

---

## ZASADY FUNDAMENTALNE

1. **NIE loguj PII** — imiona, emaile, NIPy, telefony zastap hashem lub placeholder'em (`[EMAIL]`, `[NIP]`)
2. **Loguj zamiary, nie tylko bledy** — dobry log mowi co system PROBOWAŁ zrobic, nie tylko kiedy padl
3. **Strukturalny JSON zawsze** — nigdy czysty string. Maszyny czytaja logi, nie ludzie.
4. **Poziomy logowania przestrzegaj** — INFO dla flow, WARN dla anomalii, ERROR dla awarii
5. **Kazdy log musi miec execution_id** — bez tego nie możesz korelowac zdarzen

---

## FORMAT STANDARDOWY

```javascript
// Dokodu Log Entry v1.0
{
  // WYMAGANE
  "level": "INFO",                           // INFO | WARN | ERROR | DEBUG
  "timestamp": "2026-03-06T10:30:00.123Z",  // ISO 8601, zawsze UTC
  "workflow_name": "CORLEONIS_DOCS_InvoiceParser_v2",
  "workflow_id": "abc123",                   // n8n internal ID
  "execution_id": "exec_789xyz",             // n8n execution ID
  "node_name": "Validate Invoice JSON",      // nazwa node'a w n8n

  // KONTEKST OPERACJI
  "event": "invoice.validation.start",       // zdarzenie (dot-notation)
  "message": "Rozpoczeto walidacje faktury", // czytelny opis dla czlowieka

  // DANE (BEZ PII)
  "data": {
    "items_count": 1,                        // ile rekordow przetwarza
    "document_id": "doc_a1b2c3",             // wewnetrzny ID (nie PII)
    "document_type": "FAKTURA_VAT",
    "source": "email_inbox"
  },

  // OPCJONALNE
  "duration_ms": 245,                        // czas wykonania node'a
  "error": null,                             // obiekt bledu jezeli level=ERROR
  "tags": ["corleonis", "production"]        // tagi dla filtrowania
}
```

---

## POZIOMY LOGOWANIA

| Level | Kiedy uzywac | Przyklad |
| :--- | :--- | :--- |
| `DEBUG` | Tylko podczas developmentu — NIGDY na prod | Wartosci zmiennych posrednich |
| `INFO` | Normalny flow — start, koniec, kluczowe kroki | "Faktura zaladowana", "Zatwierdzono do ERP" |
| `WARN` | Anomalia, ale workflow kontynuuje | "NIP nie przeszedl walidacji — manual review", "Niska pewnosc AI (0.6)" |
| `ERROR` | Workflow nie moze kontynuowac | "API ERP zwrocilo 500", "Brak zalacznika PDF" |

---

## KONWENCJA NAZW EVENTOW

Format: `[encja].[akcja].[status]`

```
# Dokumenty
document.received          - email/webhook z zalacznikiem odebrany
document.parsed.success    - AI sparsowala dokument
document.parsed.failure    - AI nie moga sparsowac
document.validated.pass    - walidacja JSON przeszla
document.validated.fail    - walidacja JSON nie przeszla
document.sent_to_erp       - wyslano do systemu ERP
document.archived          - zapisano w storage
document.manual_review     - przekierowano do kolejki recznej

# Emaile
email.received             - nowy email triggerowal workflow
email.classified           - AI sklasyfikowala email
email.replied              - auto-reply wyslany
email.escalated            - eskalacja do czlowieka

# Leady
lead.captured              - formularz webowy odebrany
lead.qualified             - ICP check: pozytywny
lead.disqualified          - ICP check: negatywny
lead.crm_created           - wpis w CRM

# Systemy
workflow.started           - workflow sie zaczal
workflow.completed         - workflow skonczyl sie sukcesem
workflow.failed            - workflow padl
api.request.sent           - HTTP request wyslany
api.response.received      - HTTP response odebrany
api.error                  - API zwrocilo blad
```

---

## IMPLEMENTACJA W CODE NODE

### Funkcja pomocnicza (dodaj na poczatku kazdego Code Node)

```javascript
// Dokodu Logger v1.0
// Wklej na gorze Code Node lub uzyj jako osobny "Set" node przed logowaniem

const log = (level, event, message, data = {}) => {
  const entry = {
    level: level.toUpperCase(),
    timestamp: new Date().toISOString(),
    workflow_name: $workflow.name,
    workflow_id: $workflow.id,
    execution_id: $execution.id,
    node_name: $node.name,
    event,
    message,
    data: sanitizePII(data),
  };

  // Wypisz do console (pojawia sie w n8n execution log)
  console.log(JSON.stringify(entry));

  return entry;
};

// Usuwanie PII przed logowaniem
const sanitizePII = (obj) => {
  if (!obj || typeof obj !== 'object') return obj;

  const PII_FIELDS = ['email', 'phone', 'name', 'surname', 'pesel', 'address'];
  const sanitized = { ...obj };

  for (const key of Object.keys(sanitized)) {
    if (PII_FIELDS.some(f => key.toLowerCase().includes(f))) {
      sanitized[key] = '[REDACTED]';
    } else if (typeof sanitized[key] === 'object') {
      sanitized[key] = sanitizePII(sanitized[key]);
    }
  }

  return sanitized;
};

// UZYCIE:
log('INFO', 'document.received', 'Odebrany plik PDF do przetworzenia', {
  items_count: $input.all().length,
  source: 'email_inbox',
  document_type: 'unknown'
});
```

---

### Logowanie bledu (w bloku catch)

```javascript
try {
  // ... logika ...
  log('INFO', 'document.parsed.success', 'Faktura sparsowana pomyslnie', {
    document_id: result.document_id,
    nip_valid: result.sprzedawca?.nip_valid,
    items_count: result.pozycje?.length,
    confidence: result._meta?.confidence
  });
} catch (error) {
  log('ERROR', 'document.parsed.failure', 'Blad parsowania faktury', {
    error_message: error.message,
    error_type: error.constructor.name,
    stack_truncated: error.stack?.substring(0, 200)
    // NIE loguj zawartosci dokumentu - moze zawierac PII!
  });

  // Re-throw aby Error Workflow sie uruchomil
  throw error;
}
```

---

### Logowanie wydajnosci (dla operacji dluzszych niz 1s)

```javascript
const startTime = Date.now();

// ... operacja ...

const durationMs = Date.now() - startTime;
log('INFO', 'api.response.received', 'Odpowiedz ERP API', {
  duration_ms: durationMs,
  status_code: response.statusCode,
  slow: durationMs > 3000  // oznacz jako wolny jezeli >3s
});

if (durationMs > 5000) {
  log('WARN', 'api.slow_response', 'Wolna odpowiedz ERP API — moze wymagac optymalizacji', {
    duration_ms: durationMs,
    threshold_ms: 5000
  });
}
```

---

## GDZIE TRAFIAJA LOGI

### Poziom 1: n8n Console (zawsze)
- Widoczne w panelu n8n → Executions → [execution] → Output
- Retencja: zalezy od ustawienia `EXECUTIONS_DATA_MAX_AGE` (domyslnie 30 dni)

### Poziom 2: External Log Aggregator (dla prod)
Dla kazdego projektu klienckiego rozwazyc wysylke logow do zewnetrznego systemu:

```javascript
// Po zalogowaniu do console — wyslij do zewnetrznego systemu
// Uzyj HTTP Request node lub wywolaj wewnatrz Code Node
const logEntry = log('INFO', 'workflow.completed', 'Workflow zakonczony');

// Opcja A: Loki (self-hosted, free)
// Opcja B: Papertrail (SaaS, prosty)
// Opcja C: Google Sheets (dla malych projektow)
// Opcja D: Airtable (latwa analiza)
```

### Poziom 3: Alert na bledy (obowiazek na prod)
→ Patrz BP-007 w [[N8N_Blueprints]] — Error Alerting Workflow

---

## CHECKLIST PRZED PUSZCZENIEM NA PROD

- [ ] Kazdy wazny krok ma log `INFO`
- [ ] Kazdy blok `catch` ma log `ERROR`
- [ ] Zadne PII nie jest logowane (imiona, emaile, numery)
- [ ] Kazdy log ma `event` w formacie `encja.akcja.status`
- [ ] Workflow ma podlaczony Error Workflow (BP-007)
- [ ] Przetestowano ze log pojawia sie w n8n Execution panel

---

## CHANGELOG

| Wersja | Data | Zmiana |
| :--- | :---: | :--- |
| v1.0 | 2026-03 | Inicjalizacja standardu |
