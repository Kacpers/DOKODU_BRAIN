---
type: resource
status: active
owner: kacper
last_reviewed: 2026-03-06
tags: [n8n, blueprints, workflows, automatyzacja, reusable]
---

# n8n BLUEPRINTS — Dokodu Reusable Workflows
> **Zasada:** Kazdy workflow, ktory zbudujesz dla klienta i moze byc ponownie uzyty — trafia tutaj.
> **Format:** Opis + Architektura (ASCII) + Kluczowe konfiguracje + JSON export path

---

## INDEKS BLUEPRINTOW

| ID | Nazwa | Kategoria | Uzycie u klienta | Status |
| :- | :--- | :--- | :--- | :---: |
| BP-001 | Email Lead Capture → CRM | Sales Automation | Dokodu wewnetrzne | Produkcja |
| BP-002 | Email BOK → Klasyfikacja AI | Customer Service | Animex | Produkcja |
| BP-003 | Document Parser PDF → ERP | Document Processing | Corleonis | Produkcja |
| BP-004 | Server-Side Event Tracking | Analytics | Dokodu wewnetrzne | Produkcja |
| BP-005 | Weekly Report Generator | Reporting | — | Szablon |
| BP-006 | Lead Enrichment (LinkedIn) | Sales Automation | — | Draft |
| BP-007 | n8n Error Alerting | Infrastructure | Wszystkie | Produkcja |
| BP-008 | AI Agent: RAG na Google Drive | AI Agent | — | Prototyp |

---

## BP-001: Email Lead Capture → CRM + Slack Alert

**Problem:** Formularz na stronie wyslany → reczne przepisywanie do CRM.
**Rozwiazanie:** Webhook → walidacja → CRM API → Slack powiadomienie.

**Architektura:**
```
[Webhook — formularz strony]
    ↓
[Code Node: Walidacja danych]
    (sprawdz email format, wymagane pola)
    ↓
[Decision: czy lead spelnia ICP?]
    ├── TAK → [HTTP: CRM API (HubSpot/Pipedrive)]
    │          [Slack: #leady — alert dla CEO]
    │          [Email: auto-reply do leada (30 sek.)]
    └── NIE → [Google Sheets: lista niespełnionych + powód]
               [Slack: #leady-niskie — info]
```

**Kluczowe ustawienia:**
```javascript
// Code Node: Walidacja + ICP Check
const lead = $input.item.json;

// Walidacja podstawowa
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
if (!emailRegex.test(lead.email)) throw new Error('Invalid email');
if (!lead.firma || lead.firma.length < 2) throw new Error('Brak nazwy firmy');

// ICP Check (dostosuj do swoich kryteriow)
const niespelnione = [];
if (!lead.stanowisko?.match(/CEO|Dyrektor|Manager|CTO|COO/i)) {
  niespelnione.push('Stanowisko poza ICP');
}
if (lead.liczba_pracownikow && parseInt(lead.liczba_pracownikow) < 20) {
  niespelnione.push('Firma za mala (<20 prac.)');
}

return {
  ...lead,
  icp_score: niespelnione.length === 0 ? 'HIGH' : 'LOW',
  icp_issues: niespelnione,
  timestamp: new Date().toISOString()
};
```

**JSON Export:** `/blueprints/BP-001_EmailLeadCapture_v1.json`

---

## BP-002: Email BOK → Klasyfikacja AI → Routing

**Problem:** Duzde wolumeny emaili do BOK bez priorytetu, bez kategorii.
**Rozwiazanie:** IMAP trigger → AI klasyfikacja → routing do wlasciwych kolejek.

**Architektura:**
```
[IMAP Trigger: nowy email na bok@firma.pl]
    ↓
[Code Node: Anonimizacja PII]
    (usuwa imiona, emaile, numery z tresci)
    ↓
[HTTP: OpenAI/Gemini API]
    (System: PROMPT-002 z biblioteki)
    ↓
[Code Node: Parse JSON response]
    ↓
[Decision: category + priority]
    ├── REKLAMACJA priority>=4 → [Gmail: wyzwolij "urgent reply" workflow]
    │                             [Airtable: ticket HIGH]
    │                             [Slack: #bok-urgent]
    ├── PYTANIE priority<=3 → [Airtable: ticket NORMAL]
    │                          [Email: auto-reply z FAQ linkiem]
    ├── ZAMOWIENIE → [Webhook: ERP system notification]
    └── SPAM → [Gmail: archive + label SPAM_AI]

[n8n Execution Log: wszystkie zdarzenia + czas]
```

**Kluczowe konfiguracje:**
- Anonimizacja PII PRZED wyslaniem do AI (patrz: [[RODO_Checklist]])
- Retry logic: 3 proby z exponential backoff (1s, 5s, 30s)
- Jezeli AI API niedostepna: fallback do kolejki manualnej z alertem

**Metryki do monitorowania:**
- Czas klasyfikacji (cel: <10 sek.)
- Accuracy (co tydzien porownaj 20 losowych emaili z faktyczna kategoria)
- False positive SPAM rate (cel: <1%)

**JSON Export:** `/blueprints/BP-002_EmailBOKClassification_v2.json`

---

## BP-003: Document Parser PDF → Structured JSON → ERP

**Problem:** Reczne przepisywanie faktur/dokumentow do ERP.
**Rozwiazanie:** Email z zalacznikiem → AI ekstrakcja → ERP API → archiwum.

**Architektura:**
```
[IMAP Trigger: email na dokumenty@firma.pl]
    ↓
[n8n: Extract Attachments]
    (filtruj: tylko PDF, max 10MB)
    ↓
[n8n: Binary → Base64]
    ↓
[HTTP: Gemini 1.5 Pro API (vision)]
    (System: PROMPT-001 lub PROMPT-003)
    ↓
[Code Node: Walidacja JSON]
    (sprawdz NIP, sumy, wymagane pola)
    ↓
[Decision: valid?]
    ├── TAK → [HTTP: ERP API — POST /invoice]
    │          [HTTP: MinIO S3 — upload PDF + metadata]
    │          [Email: potwierdzenie do nadawcy]
    │          [Slack: #dokumenty — sukces]
    └── NIE → [Email: zwrot do nadawcy z lista problemow]
               [Airtable: manual_review_queue]
               [Slack: #dokumenty-bledy — alert]
```

**Idempotency Check (krytyczne!):**
```javascript
// Sprawdz, czy dokument nie byl juz przetworzony
const docHash = crypto.createHash('md5')
  .update($binary.data)
  .digest('hex');

const existing = await $node['Airtable: Sprawdz hash'].json;
if (existing.records.length > 0) {
  return { skip: true, reason: 'Duplicate document', hash: docHash };
}
return { skip: false, hash: docHash };
```

**JSON Export:** `/blueprints/BP-003_DocumentParser_v3.json`

---

## BP-004: Server-Side Event Tracking (RODO Compliant)

**Problem:** Meta Pixel i Google Tag bezposrednio na stronie = wyciek PII, problemy RODO.
**Rozwiazanie:** Strona wysyla zdarzenia do n8n, n8n przetwarza i wyslaje zanonimizowane dane do platform.

**Architektura:**
```
[Strona www: zdarzenie (np. form_submit)]
    ↓ (fetch do n8n webhook — HTTPS)
[n8n Webhook: receive event]
    ↓
[Code Node: Anonimizacja]
    - Hash email (SHA-256, salted) — matching bez PII
    - IP → GEO region (nie pelne IP)
    - User agent → device type
    ↓
[Parallel:
    [HTTP: Meta Conversions API (CAPI)]
    [HTTP: Google Analytics 4 Measurement Protocol]
    [HTTP: LinkedIn Insight Tag API (jezeli B2B)]
]
    ↓
[Code Node: Logowanie sukcesu/bledu]
    ↓
[Google Sheets: dzienny log eventow (dla audytu)]
```

**Kluczowe: hashing emaila zgodnie z Meta CAPI wymogami:**
```javascript
const crypto = require('crypto');

const hashValue = (value) => {
  return crypto.createHash('sha256')
    .update(value.trim().toLowerCase())
    .digest('hex');
};

return {
  em: hashValue($json.email),  // hashed email
  ph: $json.phone ? hashValue($json.phone.replace(/\D/g, '')) : undefined,
  // Nie wysylaj: IP, full name, raw email
};
```

**JSON Export:** `/blueprints/BP-004_ServerSideTracking_v1.json`

---

## BP-005: Weekly Report Generator (Szablon)

**Problem:** Reczne tworzenie tygodniowych raportow dla klienta.
**Rozwiazanie:** Scheduled trigger → pobierz dane → AI synthesis → wyslij email.

**Architektura:**
```
[Schedule Trigger: Piatek 08:00]
    ↓
[Parallel data fetch:
    [HTTP: CRM API — leady tego tygodnia]
    [HTTP: Google Analytics — ruch]
    [Google Sheets — KPI tracker]
]
    ↓
[Code Node: Agregacja danych]
    ↓
[HTTP: Claude/GPT — synteza narracyjna]
    Prompt: "Jestes analitykiem biznesowym. Na podstawie danych
    napisz 5-zdaniowe podsumowanie tygodnia dla CEO. Wskazaz
    1 sukces, 1 problem i 1 rekomendacje na nastepny tydzien."
    ↓
[Gmail/SMTP: Wyslij raport do CEO + COO]
    (Template HTML z tabelami + narracja AI)
    ↓
[Slack: #raporty — krótkie summary]
```

**Dostosuj:** Zrodla danych, odbiorcy, format raportu do kazdego klienta.

**JSON Export:** `/blueprints/BP-005_WeeklyReport_Template_v1.json`

---

## BP-007: n8n Error Alerting (Wymagany na prod!)

**Zastosowanie:** Podlacz jako "Error Workflow" do KAZDEGO workflow produkcyjnego.

**Architektura:**
```
[Error Trigger — automatycznie wywolany przy awarii]
    ↓
[Code Node: Format error message]
    {
      workflow_name, node_name, error_message,
      execution_id, timestamp, environment: "PROD"
    }
    ↓
[Parallel:
    [Slack: #n8n-errors — natychmiastowy alert]
    [Gmail: kacper@dokodu.it — email summary]
    [Airtable: error_log — dla trendów]
]
```

**Setup:**
1. Stworz ten workflow jako "Error Handler"
2. W kazdym workflow PROD: Settings → Error Workflow → wybierz ten
3. Sprawdz, ze Slack channel #n8n-errors istnieje i Kacper jest w nim

**JSON Export:** `/blueprints/BP-007_ErrorAlerting_v1.json`

---

## BP-008: AI Agent RAG na Google Drive (Prototyp)

**Problem:** Agent AI bez dostepu do wiedzy firmowej jest generyczny i niebezpieczny.
**Rozwiazanie:** n8n AI Agent z podlaczeniem do Google Drive jako baza wiedzy.

**Architektura:**
```
[Chat Trigger / Webhook]
    ↓
[n8n AI Agent Node]
    Tools:
    ├── [Google Drive: search — wyszukaj dokumenty]
    ├── [Google Docs: read — przeczytaj dokument]
    ├── [HTTP: External API — jezeli potrzebne dane na zywo]
    └── [Code: Calculator — obliczenia]

    System Prompt:
    "Jestes asystentem biznesowym firmy [KLIENT].
     Odpowiadasz WYLACZNIE na podstawie dokumentow
     z Google Drive. Jezeli nie znajdziesz odpowiedzi
     w dokumentach — powiedz wprost. NIE zgaduj."

    Model: Claude Sonnet 4.6 lub GPT-4o
    ↓
[Response → Chat / Email / Slack]
```

**Status:** Prototyp — testowanie u 1 klienta beta w Q2 2026.

---

## ZARZADZANIE BLUEPRINTAMI

### Jak dodac nowy blueprint
1. Zbuduj i przetestuj workflow na dev
2. Uzupelnij powyzszy template (problem / architektura / konfiguracje)
3. Eksportuj JSON: n8n → Workflows → Export → zapisz w `/blueprints/`
4. Dodaj do indeksu powyzej
5. Oznacz wersje (v1, v2 przy zmianach breaking)

### Kiedy aktualizowac
- Po waznej zmianie n8n API (sprawdzaj changelog po kazdej aktualizacji)
- Po odkryciu bugu w produkcji
- Po optymalizacji wydajnosci

### Folder struktura (fizyczna)
```
/blueprints/
├── BP-001_EmailLeadCapture_v1.json
├── BP-002_EmailBOKClassification_v2.json
├── BP-003_DocumentParser_v3.json
├── BP-004_ServerSideTracking_v1.json
├── BP-005_WeeklyReport_Template_v1.json
├── BP-007_ErrorAlerting_v1.json
└── BP-008_RAGAgent_prototype.json
```
