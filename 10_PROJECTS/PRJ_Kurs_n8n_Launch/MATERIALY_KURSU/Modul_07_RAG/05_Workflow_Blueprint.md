---
type: workflow-blueprint
modul: 07
tytul: "Firmowy Asystent Wiedzy — Knowledge Assistant"
projekt: "Company Knowledge Assistant"
status: draft
last_reviewed: 2026-03-27
---

# Workflow Blueprint: Firmowy Asystent Wiedzy

**Cel systemu:** Automatyczny asystent który odpowiada na pytania o dokumenty firmy, cytuje źródła i eliminuje halucynacje.

**Stack:** n8n + Google Drive + Qdrant + OpenAI + Slack

---

## Architektura systemu

```
┌─────────────────────────────────────────────────────────────────┐
│  INGESTION PIPELINE (Workflow #1)                               │
│                                                                 │
│  [Google Drive Trigger]                                         │
│       ↓ (nowy/zmieniony plik)                                   │
│  [Download File] → [Parse Text] → [Chunker (500t/50o)]          │
│       ↓                                                         │
│  [Hash Check] → jeśli znany hash: STOP                          │
│       ↓ nowy/zmieniony                                          │
│  [Delete Old Chunks] → [Loop: Embed + Insert] → [Log]           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  QUERY PIPELINE (Workflow #2)                                   │
│                                                                 │
│  [Slack Trigger / Webhook]                                      │
│       ↓ (pytanie użytkownika)                                   │
│  [Embed Query] → [Qdrant Retrieve (top 5, threshold 0.75)]      │
│       ↓                                                         │
│  [Score Check] → jeśli score < 0.65: FALLBACK                  │
│       ↓ score OK                                                │
│  [Build Context] → [AI Chat: GPT-4o + strict citations prompt]  │
│       ↓                                                         │
│  [Format Response + Drive Links] → [Slack/Email Send]           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Qdrant Collection Schema

**Nazwa kolekcji:** `company_knowledge`

```json
{
  "name": "company_knowledge",
  "vectors": {
    "size": 1536,
    "distance": "Cosine",
    "on_disk": false
  },
  "optimizers_config": {
    "default_segment_number": 2
  },
  "replication_factor": 1
}
```

**Payload Schema (metadane każdego punktu):**

```json
{
  "text": "string",
  "fileName": "string",
  "fileId": "string (Google Drive file ID)",
  "fileMimeType": "string (application/pdf | application/vnd.openxmlformats-officedocument.wordprocessingml.document)",
  "fileWebLink": "string (https://drive.google.com/file/d/...)",
  "chunkIndex": "integer (0-based)",
  "totalChunks": "integer",
  "modifiedDate": "string (ISO 8601: 2026-03-27T14:30:00Z)",
  "ingestedDate": "string (ISO 8601)",
  "hash": "string (MD5 of file content)",
  "category": "string (HR | Finance | Legal | Tech | Sales | General)",
  "language": "string (pl | en)"
}
```

**Przykładowy punkt w Qdrant:**
```json
{
  "id": "a7f3e821-...",
  "version": 1,
  "score": null,
  "payload": {
    "text": "Termin płatności faktury VAT wynosi 21 dni od daty jej wystawienia. W przypadku opóźnienia naliczane są odsetki ustawowe za opóźnienie w transakcjach handlowych.",
    "fileName": "Umowa_Acme_Corp_2025.pdf",
    "fileId": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms",
    "fileWebLink": "https://drive.google.com/file/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms",
    "chunkIndex": 12,
    "totalChunks": 34,
    "modifiedDate": "2026-01-15T10:00:00Z",
    "ingestedDate": "2026-03-27T14:30:00Z",
    "hash": "a1b2c3d4e5f6...",
    "category": "Finance",
    "language": "pl"
  },
  "vector": [0.023, -0.871, 0.144, ...]
}
```

---

## Workflow #1: Ingestion Pipeline — specyfikacja nodes

### Node 1: Google Drive Trigger
```yaml
type: n8n-nodes-base.googleDriveTrigger
config:
  event: fileUpdated
  driveId: "My Drive"
  folderId: "FOLDER_ID_TUTAJ"
  triggerOn: specificFolder
  includeTeamDrives: false
pollInterval: 1  # minuta
```

### Node 2: IF — Filtr typów pliku
```yaml
type: n8n-nodes-base.if
conditions:
  - field: "{{ $json.mimeType }}"
    operation: contains
    values:
      - "application/pdf"
      - "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
      - "application/vnd.google-apps.document"
```

### Node 3: Google Drive — Download File
```yaml
type: n8n-nodes-base.googleDrive
operation: download
fileId: "{{ $json.id }}"
```

### Node 4 (PDF branch): Extract from PDF
```yaml
type: n8n-nodes-base.extractFromFile
operation: pdf
```

### Node 5 (DOCX branch): Extract from File
```yaml
type: n8n-nodes-base.extractFromFile
operation: text
```

### Node 6: Code Node — Merge & Hash
```javascript
const crypto = require('crypto');
const input = $input.first().json;

// Pobierz tekst (z PDF lub DOCX parsera)
const rawText = input.text || input.content || input.data || "";

// Oblicz hash dokumentu
const hash = crypto.createHash('md5').update(rawText).digest('hex');

// Zbierz metadane z Google Drive trigger
const triggerData = $('Google Drive Trigger').first().json;

return [{
  json: {
    rawText,
    hash,
    fileName: triggerData.name,
    fileId: triggerData.id,
    fileMimeType: triggerData.mimeType,
    fileWebLink: triggerData.webViewLink,
    modifiedDate: triggerData.modifiedTime,
    ingestedDate: new Date().toISOString(),
    // Auto-detect category based on filename keywords
    category: detectCategory(triggerData.name)
  }
}];

function detectCategory(name) {
  const lower = name.toLowerCase();
  if (lower.includes('umow') || lower.includes('kontrakt')) return 'Legal';
  if (lower.includes('faktur') || lower.includes('cennik') || lower.includes('platno')) return 'Finance';
  if (lower.includes('hr') || lower.includes('urlop') || lower.includes('pracow')) return 'HR';
  if (lower.includes('tech') || lower.includes('api') || lower.includes('infra')) return 'Tech';
  if (lower.includes('ofert') || lower.includes('sprzedaz') || lower.includes('klient')) return 'Sales';
  return 'General';
}
```

### Node 7: HTTP Request — Sprawdź hash w Qdrant
```yaml
type: n8n-nodes-base.httpRequest
method: POST
url: "http://localhost:6333/collections/company_knowledge/points/scroll"
body:
  filter:
    must:
      - key: fileId
        match:
          value: "{{ $json.fileId }}"
      - key: hash
        match:
          value: "{{ $json.hash }}"
  limit: 1
  with_payload: false
  with_vector: false
```

### Node 8: IF — Hash znany?
```yaml
condition: "{{ $json.result.points.length }}" == 0
# TRUE (nowy/zmieniony) → kontynuuj
# FALSE (brak zmian) → STOP
```

### Node 9: HTTP Request — Usuń stare chunki
```yaml
method: POST
url: "http://localhost:6333/collections/company_knowledge/points/delete"
body:
  filter:
    must:
      - key: fileId
        match:
          value: "{{ $('Code Node — Merge & Hash').item.json.fileId }}"
```

### Node 10: Code Node — Chunker
```javascript
const input = $input.first().json;
const text = input.rawText;

const CHUNK_CHARS = 2000;     // ~500 tokenów (1 token ≈ 4 znaki)
const OVERLAP_CHARS = 200;    // ~50 tokenów

const chunks = [];
let start = 0;

while (start < text.length) {
  const end = Math.min(start + CHUNK_CHARS, text.length);
  const chunkText = text.slice(start, end).trim();

  if (chunkText.length > 100) {
    chunks.push({
      json: {
        chunkText,
        chunkIndex: chunks.length,
        totalChunks: 0,  // uzupełnione po pętli
        fileName: input.fileName,
        fileId: input.fileId,
        fileMimeType: input.fileMimeType,
        fileWebLink: input.fileWebLink,
        modifiedDate: input.modifiedDate,
        ingestedDate: input.ingestedDate,
        hash: input.hash,
        category: input.category,
        language: "pl"
      }
    });
  }

  if (end >= text.length) break;
  start = end - OVERLAP_CHARS;
}

// Uzupełnij totalChunks
const total = chunks.length;
return chunks.map(c => ({
  json: { ...c.json, totalChunks: total }
}));
```

### Node 11: Loop Over Items
```yaml
type: n8n-nodes-base.splitInBatches
batchSize: 10  # przetwarzaj po 10 chunków naraz
```

### Node 12: OpenAI Embeddings
```yaml
type: @n8n/n8n-nodes-langchain.embeddingsOpenAi
model: text-embedding-3-small
inputField: chunkText
```

### Node 13: Qdrant Vector Store — Insert
```yaml
type: @n8n/n8n-nodes-langchain.vectorStoreQdrant
operation: insert
qdrantCollection: company_knowledge
contentField: chunkText
metadata:
  fileName: "{{ $json.fileName }}"
  fileId: "{{ $json.fileId }}"
  fileMimeType: "{{ $json.fileMimeType }}"
  fileWebLink: "{{ $json.fileWebLink }}"
  chunkIndex: "{{ $json.chunkIndex }}"
  totalChunks: "{{ $json.totalChunks }}"
  modifiedDate: "{{ $json.modifiedDate }}"
  ingestedDate: "{{ $json.ingestedDate }}"
  hash: "{{ $json.hash }}"
  category: "{{ $json.category }}"
  language: "{{ $json.language }}"
```

### Node 14: Google Sheets — Log (opcjonalny)
```yaml
operation: appendRow
sheetId: "SHEET_ID"
columns:
  fileName: "{{ $json.fileName }}"
  chunks: "{{ $json.totalChunks }}"
  ingestedAt: "{{ $json.ingestedDate }}"
  status: "OK"
```

---

## Workflow #2: Query Pipeline — specyfikacja nodes

### Node 1A: Slack Trigger
```yaml
type: n8n-nodes-base.slackTrigger
events:
  - message
channel: asystent-wiedzy
# Ignoruj wiadomości od bota (bot_id: undefined)
```

### Node 1B: Webhook Trigger (alternatywa)
```yaml
type: n8n-nodes-base.webhook
httpMethod: POST
path: /ask
responseMode: responseNode
```

### Node 2: Set — Extract Question
```javascript
// Dla Slack:
const question = $json.event?.text?.replace(/<@[A-Z0-9]+>/g, '').trim();
// Dla Webhook:
// const question = $json.body.question;

return [{
  json: {
    question,
    userId: $json.event?.user || "api_user",
    channelId: $json.event?.channel || null,
    timestamp: new Date().toISOString()
  }
}];
```

### Node 3: Qdrant Vector Store — Retrieve
```yaml
type: @n8n/n8n-nodes-langchain.vectorStoreQdrant
operation: retrieve
qdrantCollection: company_knowledge
query: "{{ $json.question }}"
topK: 5
scoreThreshold: 0.70
returnAll: false
# Opcjonalne filtry:
# filter:
#   must:
#     - key: language
#       match:
#         value: pl
```

### Node 3b: Code Node — Rerank (opcjonalny, po Qdrant Retrieve)

```javascript
// Reranker: filtruje niskiej jakości wyniki, deduplikuje po pliku, zostawia top 3
const items = $input.all();

// Sortuj po score (malejąco)
const sorted = items
  .filter(i => (i.json.score || 0) >= 0.70)
  .sort((a, b) => (b.json.score || 0) - (a.json.score || 0));

// Max 2 chunki z tego samego pliku
const seenFiles = {};
const deduplicated = sorted.filter(i => {
  const fid = i.json.payload?.fileId || i.json.fileId;
  if (!seenFiles[fid]) seenFiles[fid] = 0;
  if (seenFiles[fid] < 2) { seenFiles[fid]++; return true; }
  return false;
});

// Top 3 po deduplicacji
return deduplicated.slice(0, 3).map(i => ({ json: i.json }));
```

**Kiedy używać Rerankera:**
- Duże kolekcje (> 5 000 chunków) — wyniki Qdrant mogą zawierać duplikaty z tego samego dokumentu
- Pytania ogólne — top 5 może mieć 4 chunki z jednego pliku, co psuje odpowiedź
- Produkcja — zawsze. W MVP: opcjonalny.

---

### Node 4: Code Node — Score Check + Build Context
```javascript
const items = $input.all();
const question = $('Set — Extract Question').first().json.question;

// Sprawdź czy mamy wystarczająco dobre wyniki
if (!items || items.length === 0) {
  return [{
    json: {
      has_results: false,
      question,
      context: "",
      sources: [],
      max_score: 0,
      fallback_reason: "no_results"
    }
  }];
}

const maxScore = Math.max(...items.map(i => i.json.score || 0));

if (maxScore < 0.65) {
  return [{
    json: {
      has_results: false,
      question,
      context: "",
      sources: [],
      max_score: maxScore,
      fallback_reason: "low_confidence"
    }
  }];
}

// Buduj kontekst dla AI
const contextParts = items
  .filter(i => (i.json.score || 0) > 0.65)
  .map((item, idx) => {
    const p = item.json.payload || {};
    return `[FRAGMENT ${idx + 1}]
Plik: ${p.fileName || "nieznany"} | Chunk: ${p.chunkIndex || 0}/${p.totalChunks || "?"} | Score: ${(item.json.score || 0).toFixed(3)}
Link: ${p.fileWebLink || "brak"}
---
${p.text || item.json.text || ""}`;
  })
  .join("\n\n");

// Lista unikalnych źródeł
const sources = [...new Set(items
  .map(i => ({
    fileName: i.json.payload?.fileName,
    fileWebLink: i.json.payload?.fileWebLink
  }))
  .filter(s => s.fileName)
  .map(s => JSON.stringify(s))
)].map(s => JSON.parse(s));

return [{
  json: {
    has_results: true,
    question,
    context: contextParts,
    sources,
    max_score: maxScore,
    chunk_count: items.length
  }
}];
```

### Node 5: IF — Has Results
```yaml
condition: "{{ $json.has_results }}" == true
```

### Node 6 (TRUE): OpenAI Chat — Generate Answer
```yaml
type: @n8n/n8n-nodes-langchain.lmChatOpenAi
model: gpt-4o-mini  # lub gpt-4o dla wyższej jakości
temperature: 0.1    # niska temperatura = bardziej deterministyczna, mniej "kreatywna"
systemMessage: |
  Jesteś precyzyjnym asystentem firmowym. Odpowiadaj WYŁĄCZNIE na podstawie dostarczonych fragmentów dokumentów.

  BEZWZGLĘDNE ZASADY:
  1. Każde twierdzenie faktyczne MUSI być poparte przypisem: [Źródło: NAZWA_PLIKU, chunk X]
  2. Cytuj dokładne fragmenty tekstu w cudzysłowie gdy to możliwe
  3. Jeśli pytanie wymaga informacji których NIE MA w dostarczonych fragmentach → napisz DOKŁADNIE:
     "Nie znalazłem tej informacji w dostępnych dokumentach firmowych."
  4. NIE uzupełniaj odpowiedzi wiedzą ogólną. NIE zmyślaj. NIE spekuluj.
  5. Jeśli informacja jest częściowa → napisz co wiesz i zaznacz co jest niepewne

  FORMAT ODPOWIEDZI:
  - Zacznij od bezpośredniej odpowiedzi
  - Podaj cytaty i źródła
  - Zakończ listą powiązanych dokumentów
userMessage: |
  PYTANIE: {{ $json.question }}

  DOSTĘPNE FRAGMENTY DOKUMENTÓW:
  {{ $json.context }}
```

### Node 7 (FALSE): Set — Fallback Message
```javascript
const reason = $json.fallback_reason;
const question = $json.question;

const messages = {
  no_results: "Nie znalazłem żadnych dokumentów powiązanych z tym pytaniem. Upewnij się że odpowiednie dokumenty zostały dodane do folderu firmowego.",
  low_confidence: `Znalazłem fragmenty dokumentów, ale ich dopasowanie do pytania jest zbyt niskie (${($json.max_score * 100).toFixed(0)}%). Spróbuj przeformułować pytanie lub podaj więcej kontekstu.`
};

return [{
  json: {
    answer: messages[reason] || messages.no_results,
    is_fallback: true,
    question,
    support_hint: "Jeśli problem się powtarza, skontaktuj się z administratorem systemu."
  }
}];
```

### Node 8: Code Node — Format Final Response
```javascript
const isFromAI = $input.first().json.has_results !== false;
const data = $input.first().json;

if (!isFromAI) {
  return [{
    json: {
      text: `⚠️ ${data.answer}\n\n_${data.support_hint}_`,
      is_fallback: true
    }
  }];
}

const answer = data.message?.content || data.text || "";
const sources = $('Code Node — Score Check').first().json.sources || [];

const sourceLinks = sources.map(s =>
  `• <${s.fileWebLink}|${s.fileName}>`
).join('\n');

const slackMessage = `${answer}

${sources.length > 0 ? `\n📎 *Źródła:*\n${sourceLinks}` : ''}`;

return [{
  json: {
    text: slackMessage,
    is_fallback: false
  }
}];
```

### Node 9A: Slack — Send Response
```yaml
type: n8n-nodes-base.slack
operation: post
channel: "{{ $('Set — Extract Question').item.json.channelId }}"
text: "{{ $json.text }}"
# Opcja thread_ts dla odpowiedzi w wątku:
# thread_ts: "{{ $('Slack Trigger').item.json.event.ts }}"
```

### Node 9B: Webhook Respond (dla API)
```yaml
type: n8n-nodes-base.respondToWebhook
responseBody:
  answer: "{{ $json.text }}"
  is_fallback: "{{ $json.is_fallback }}"
  timestamp: "{{ $now }}"
responseCode: 200
```

---

## Chunking Strategy — uzasadnienie

**Wybrana strategia:** Fixed Size z overlappem
**Parametry:** 500 tokenów (≈2000 znaków), 50 tokenów overlap (≈200 znaków)

**Uzasadnienie:**

| Czynnik | Decyzja | Powód |
|---------|---------|-------|
| Rozmiar chunka: 500 tokenów | Optymalny dla biznesowych dokumentów PDF/DOCX | Zbyt mały (< 200t): traci kontekst; zbyt duży (> 1000t): rozmywa semantykę |
| Overlap: 10% (50 tokenów) | Ratuje informacje na granicy chunków | Kluczowe dla umów gdzie klauzula może być rozbita między chunki |
| Strategia: Fixed Size | Prostota + przewidywalność | Semantic chunking wymaga dodatkowego modelu, +200ms latencji, wyższy koszt |
| Język: PL | Brak specjalnej obsługi | text-embedding-3-small dobrze radzi sobie z polskim |
| Tokenizer: aproksymacja 4 chars/token | Wystarczająca precyzja | Prawdziwy tokenizer (tiktoken) opcjonalny dla precyzyjnego rozliczania |

**Kiedy zmienić strategię:**
- `Hierarchical` → gdy masz >1000 dokumentów i różne typy pytań (ogólne + szczegółowe)
- `Semantic` → gdy dokumenty mają wyraźne sekcje oddzielone nagłówkami (np. instrukcje techniczne)
- Mniejszy chunk (300t) → gdy pytania są bardzo specyficzne ("podaj konkretną liczbę")
- Większy chunk (800t) → gdy pytania wymagają szerokiego kontekstu ("opisz proces X")

---

## Przykładowe Query i Response

### Przykład 1 — Pytanie o warunki umowy

**Input:**
```json
{ "question": "Jakie są warunki płatności w umowie z Acme Corp?" }
```

**Retrieved chunks (top 3):**
```
FRAGMENT 1 | Plik: Umowa_Acme_Corp_2025.pdf | Score: 0.912
"§4.2 Płatność. Wynagrodzenie płatne jest w terminie 21 (dwadzieścia jeden) dni od daty wystawienia prawidłowej faktury VAT. Faktury wystawiane są do 5. dnia każdego miesiąca za miesiąc poprzedni."

FRAGMENT 2 | Plik: Umowa_Acme_Corp_2025.pdf | Score: 0.887
"§4.3 Opóźnienia. W przypadku opóźnienia w zapłacie Wykonawcy przysługują odsetki ustawowe za opóźnienie w transakcjach handlowych, o których mowa w art. 7 ustawy z dnia 8 marca 2013 r."

FRAGMENT 3 | Plik: Umowa_Acme_Corp_2025.pdf | Score: 0.743
"§4.1 Wynagrodzenie. Całkowite wynagrodzenie za realizację przedmiotu umowy wynosi 45 000 PLN netto plus należny podatek VAT."
```

**AI Response:**
```
Zgodnie z umową z Acme Corp:

**Termin płatności:** 21 dni od daty wystawienia prawidłowej faktury VAT [Źródło: Umowa_Acme_Corp_2025.pdf, §4.2].

**Harmonogram fakturowania:** Faktury wystawiane są do 5. dnia każdego miesiąca za miesiąc poprzedni [Źródło: Umowa_Acme_Corp_2025.pdf, §4.2].

**Odsetki za opóźnienie:** Odsetki ustawowe za opóźnienie w transakcjach handlowych zgodnie z ustawą z 8 marca 2013 r. [Źródło: Umowa_Acme_Corp_2025.pdf, §4.3].

**Wartość umowy:** 45 000 PLN netto + VAT [Źródło: Umowa_Acme_Corp_2025.pdf, §4.1].

📎 Źródła:
• Umowa_Acme_Corp_2025.pdf
```

---

### Przykład 2 — Pytanie spoza zakresu

**Input:**
```json
{ "question": "Jaka jest prognoza pogody na jutro w Warszawie?" }
```

**Retrieved chunks (max score: 0.31)**

**Fallback response:**
```
Znalazłem fragmenty dokumentów, ale ich dopasowanie do pytania jest zbyt niskie (31%). Spróbuj przeformułować pytanie lub podaj więcej kontekstu.

Jeśli problem się powtarza, skontaktuj się z administratorem systemu.
```

---

### Przykład 3 — Pytanie o HR

**Input:**
```json
{ "question": "Ile dni urlopu przysługuje mi po 8 latach pracy?" }
```

**AI Response:**
```
Zgodnie z Regulaminem Pracy:

Pracownikowi z **co najmniej 10-letnim stażem pracy** przysługuje **26 dni urlopu wypoczynkowego** rocznie [Źródło: Regulamin_Pracy_2025.pdf, §15.2].

Przy stażu pracy poniżej 10 lat (dotyczy Twojego przypadku — 8 lat) przysługuje **20 dni** urlopu rocznie [Źródło: Regulamin_Pracy_2025.pdf, §15.1].

⚠️ Uwaga: Regulamin nie precyzuje zaokrąglenia w roku uzyskania wyższego wymiaru. W celu potwierdzenia skontaktuj się z Działem HR.

📎 Źródła:
• Regulamin_Pracy_2025.pdf
```

---

## Szacunkowy koszt dla 100 dokumentów / 1000 pytań miesięcznie

### Ingestion (jednorazowy)

| Element | Obliczenie | Koszt |
|---------|------------|-------|
| Dokumenty | 100 plików × 20 stron × 300 tokenów/strona | 600 000 tokenów |
| Model | text-embedding-3-small @ $0.02/1M | **$0.012** (1,2 centa) |
| Qdrant storage | Self-hosted (VPS) lub free tier cloud | **$0** |
| **Łącznie ingestion** | | **~$0.01** |

### Query (miesięczny, 1000 pytań)

| Element | Obliczenie | Koszt |
|---------|------------|-------|
| Embed pytań | 1000 pytań × 50 tokenów × $0.02/1M | $0.001 |
| Qdrant retrieve | Self-hosted | $0 |
| GPT-4o-mini generation | 1000 pytań × 1500 tokenów (prompt+answer) × $0.60/1M output | **$0.90** |
| GPT-4o generation (opcja premium) | 1000 × 1500 × $5/1M output | **$7.50** |
| **Łącznie miesięcznie (mini)** | | **~$1/miesiąc** |
| **Łącznie miesięcznie (gpt-4o)** | | **~$8/miesiąc** |

### Reingest (aktualizacje)

Zakładając 10% dokumentów zmienia się miesięcznie:
- 10 dokumentów × $0.0001 = $0.001 (praktycznie zero)

### Całkowity koszt (12 miesięcy)

| Scenariusz | Koszt/mies. | Koszt/rok |
|------------|-------------|-----------|
| Starter (GPT-4o-mini, 1000 pytań) | ~$1 | ~$12 |
| Standard (GPT-4o, 1000 pytań) | ~$8 | ~$96 |
| Scale (GPT-4o, 5000 pytań) | ~$38 | ~$456 |

**Wniosek:** ROI jest oczywisty. Jeden pracownik oszczędzający 1 godz/dzień × $25/h × 22 dni = $550/mies. vs $38/mies. kosztu systemu.

---

## Checklist wdrożenia

### Infrastruktura
- [ ] Qdrant uruchomiony (Docker lub Qdrant Cloud)
- [ ] Kolekcja `company_knowledge` stworzona z właściwym schematem
- [ ] Credentials n8n: Qdrant, OpenAI, Google Drive, Slack

### Ingestion Pipeline
- [ ] Google Drive Trigger skonfigurowany na właściwy folder
- [ ] Chunker przetestowany na przykładowym dokumencie (sprawdź czy chunks są sensowne)
- [ ] Hash check działa (wrzuć ten sam plik 2 razy — drugi raz powinien być pominięty)
- [ ] Delete old chunks działa (zmień plik, sprawdź czy stare chunki zniknęły z Qdrant)
- [ ] Minimum 5 dokumentów zaindeksowanych

### Query Pipeline
- [ ] Similarity search zwraca relevantne wyniki dla testowych pytań
- [ ] Score threshold ustawiony na 0.70–0.75
- [ ] Fallback działa dla pytań spoza zakresu
- [ ] System prompt wymusza cytowanie (sprawdź odpowiedź — czy ma [Źródło:...])
- [ ] Linki do Drive w odpowiedzi działają

### Monitoring
- [ ] Log w Google Sheets: pytanie, score, data, czy fallback
- [ ] Test dataset: 10 pytań z oczekiwanymi odpowiedziami
- [ ] Wyniki testu bazowego zapisane (precision, recall)

---

*Blueprint: Firmowy Asystent Wiedzy v1.0 | Modul 07 | Kurs n8n + AI dla Agencji i Firm*
