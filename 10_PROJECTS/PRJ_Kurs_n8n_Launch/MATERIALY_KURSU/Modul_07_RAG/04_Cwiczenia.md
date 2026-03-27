---
type: course-exercises
modul: 07
tytul: "Cydrowy Mózg Firmy (RAG) i Eliminacja Halucynacji"
liczba_cwiczen: 2
zadanie_domowe: true
status: draft
last_reviewed: 2026-03-27
---

# Modul 07 — Ćwiczenia

---

## Ćwiczenie 1: Setup Qdrant + pierwsze embeddingi
**Czas: ~20 minut | Poziom: podstawowy**

### Cel
Uruchomisz Qdrant lokalnie, stworzysz pierwszą kolekcję i wrzucisz 10 fragmentów tekstu ręcznie z n8n. Sprawdzisz czy similarity search faktycznie zwraca właściwe wyniki.

### Wymagania
- Docker zainstalowany lokalnie
- n8n działające lokalnie lub w chmurze
- Klucz API OpenAI (do text-embedding-3-small)

---

### Krok 1: Uruchom Qdrant przez Docker (3 min)

Otwórz terminal i uruchom:

```bash
docker run -d \
  --name qdrant \
  -p 6333:6333 \
  -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage \
  qdrant/qdrant
```

Sprawdź czy działa:
```bash
curl http://localhost:6333/healthz
# Oczekiwana odpowiedź: {"title":"qdrant - vector search engine"}
```

Otwórz dashboard: `http://localhost:6333/dashboard`

Powinnaś/powinieneś zobaczyć interfejs Qdrant z pustą listą kolekcji.

---

### Krok 2: Stwórz kolekcję przez API (2 min)

W terminalu (lub Postmanie, lub node HTTP Request w n8n):

```bash
curl -X PUT 'http://localhost:6333/collections/test_kurs' \
  -H 'Content-Type: application/json' \
  -d '{
    "vectors": {
      "size": 1536,
      "distance": "Cosine"
    }
  }'
```

Odśwież dashboard — kolekcja `test_kurs` powinna się pojawić.

---

### Krok 3: Zbuduj workflow "Ćwiczenie 1 — Insert" w n8n (10 min)

Zbuduj prosty workflow:

```
[Manual Trigger]
      ↓
[Code Node: "Dane testowe"]
      ↓
[Loop Over Items]
      ↓ (dla każdego)
[OpenAI Embeddings]        ← model: text-embedding-3-small
      ↓
[Qdrant Insert]            ← kolekcja: test_kurs
```

**Kod w Code Node (dane testowe — 10 fragmentów o różnych tematach):**

```javascript
return [
  { json: { id: 1, text: "Termin płatności faktury wynosi 21 dni od daty wystawienia.", kategoria: "finanse" } },
  { json: { id: 2, text: "Odsetki za opóźnienie w płatności wynoszą 0,5% dziennie.", kategoria: "finanse" } },
  { json: { id: 3, text: "Urlop wypoczynkowy przysługuje pracownikom po 6 miesiącach zatrudnienia.", kategoria: "hr" } },
  { json: { id: 4, text: "Pracownik ma prawo do 26 dni urlopu rocznie po 10 latach pracy.", kategoria: "hr" } },
  { json: { id: 5, text: "Serwery produkcyjne działają na Ubuntu 22.04 LTS w środowisku Docker.", kategoria: "tech" } },
  { json: { id: 6, text: "Backup bazy danych wykonywany jest codziennie o godzinie 3:00 UTC.", kategoria: "tech" } },
  { json: { id: 7, text: "Klient ACME Corp podpisał umowę na wdrożenie systemu CRM za 45 000 PLN.", kategoria: "sprzedaz" } },
  { json: { id: 8, text: "Propozycja dla firmy Kowalski sp. z o.o. opiewa na 12 miesięcy wsparcia.", kategoria: "sprzedaz" } },
  { json: { id: 9, text: "Dane osobowe klientów przechowywane są przez 5 lat zgodnie z RODO.", kategoria: "legal" } },
  { json: { id: 10, text: "Przetwarzanie danych osobowych wymaga podstawy prawnej z art. 6 RODO.", kategoria: "legal" } }
];
```

**Konfiguracja Qdrant Insert node:**
- Credential: Qdrant (URL: `http://localhost:6333`)
- Collection: `test_kurs`
- Content Field: `text`
- Metadata: `{ "id": "{{ $json.id }}", "kategoria": "{{ $json.kategoria }}" }`

Uruchom workflow. Sprawdź dashboard — kolekcja powinna mieć 10 punktów.

---

### Krok 4: Przetestuj similarity search (5 min)

Zbuduj drugi mini-workflow:

```
[Manual Trigger z polem "query"]
      ↓
[Qdrant Retrieve]
  - Collection: test_kurs
  - Query: {{ $json.query }}
  - Top K: 3
      ↓
[Set: Pokaż wyniki]
```

Przetestuj z pytaniami:
1. `"ile mam czasu na zapłatę faktury?"` → powinno zwrócić fragmenty #1 i #2
2. `"kiedy dostanę urlop?"` → powinno zwrócić fragmenty #3 i #4
3. `"na jakim systemie operacyjnym działają serwery?"` → fragment #5

**Sprawdź:** Czy wyniki są intuicyjnie poprawne? Czy blisko znaczeniowo powiązane fragmenty wychodzą na górę?

---

### Czego nauczyłeś się w tym ćwiczeniu
- Qdrant działa lokalnie w Dockerze bez żadnej konfiguracji
- Similarity search rozumie semantykę — nie szuka po słowach kluczowych
- Pytanie "ile mam czasu na zapłatę" i fragment "termin płatności 21 dni" — to są inne słowa, ale to samo znaczenie

---

## Ćwiczenie 2: Firmowy Asystent Wiedzy — kompletny build
**Czas: ~70 minut | Poziom: zaawansowany**

### Cel
Zbudujesz kompletny, działający Knowledge Assistant dla własnych dokumentów firmowych. Po tym ćwiczeniu będziesz miał system gotowy do wdrożenia.

### Wymagania
- Qdrant działający lokalnie (z Ćwiczenia 1) lub Qdrant Cloud (free tier)
- n8n z dostępem do internetu
- Google Drive z min. 5 dokumentami (PDF lub DOCX)
- Klucz API OpenAI (embeddings + chat)
- Slack workspace z Botem lub email do odbierania odpowiedzi

---

### Przygotuj dokumenty (5 min)

Stwórz folder w Google Drive: `Asystent_Wiedzy_Demo`

Wrzuć do niego 5 dokumentów. Jeśli nie masz firmowych dokumentów, użyj przykładowych:
- Regulamin pracy (pobierz przykładowy ze strony kursu)
- Cennik usług firmy (stwórz prosty DOCX z 10 pozycjami)
- FAQ dla klientów (10 pytań i odpowiedzi)
- Polityka bezpieczeństwa IT (możesz pobrać szablon online)
- Umowa o współpracy (przykładowy template)

**Ważne:** dokumenty muszą mieć konkretne, sprawdzalne fakty. "Termin płatności: 30 dni", "Kara za anulację: 20% wartości" — takie rzeczy. Za chwilę będziesz zadawać do nich pytania.

---

### WORKFLOW #1: Ingestion Pipeline (30 min)

Zbuduj workflow wg schematu:

```
[Google Drive Trigger]
  Event: "File Created or Updated"
  Folder: ID folderu "Asystent_Wiedzy_Demo"
      ↓
[Google Drive: Download File]
      ↓
[Switch Node: Typ pliku]
  PDF → [PDF Parser]
  DOCX → [File Extractor (Extract Text)]
      ↓ (oba wyjścia zbiegają się)
[Code Node: Chunker]
      ↓
[Loop Over Items]
      ↓
[OpenAI Embeddings]
      ↓
[Qdrant Insert]
      ↓ (po pętli)
[Google Sheets: Log] (opcjonalnie)
```

**Kod Chunkera (wklej do Code Node):**

```javascript
const text = $input.first().json.text || $input.first().json.content || "";
const fileName = $input.first().json.name || "unknown";
const fileId = $input.first().json.id || "unknown";

if (!text || text.length < 50) {
  return [{ json: { error: "Za krótki tekst", fileName } }];
}

const CHUNK_CHARS = 2000;     // ~500 tokenów
const OVERLAP_CHARS = 200;    // ~50 tokenów overlap

const chunks = [];
let start = 0;
let chunkIndex = 0;

while (start < text.length) {
  const end = Math.min(start + CHUNK_CHARS, text.length);
  const chunkText = text.slice(start, end).trim();

  if (chunkText.length > 50) {
    chunks.push({
      json: {
        chunkText,
        chunkIndex,
        fileName,
        fileId,
        totalLength: text.length,
        modifiedDate: new Date().toISOString()
      }
    });
    chunkIndex++;
  }

  if (end === text.length) break;
  start = end - OVERLAP_CHARS;
}

return chunks;
```

**Konfiguracja Qdrant Insert:**
```
Collection: company_knowledge
Content: {{ $json.chunkText }}
Metadata:
  fileName: {{ $json.fileName }}
  fileId: {{ $json.fileId }}
  chunkIndex: {{ $json.chunkIndex }}
  modifiedDate: {{ $json.modifiedDate }}
```

Uruchom trigger, wrzuć jeden plik do folderu Drive. Poczekaj 30 sekund. Sprawdź Qdrant dashboard — kolekcja `company_knowledge` powinna mieć nowe punkty.

**Przetestuj z wszystkimi 5 dokumentami.** Możesz je dodać ręcznie (wrzuć kolejno do folderu i obserwuj jak punkty przyrastają w Qdrant).

---

### WORKFLOW #2: Query Pipeline (30 min)

Zbuduj workflow:

```
[Webhook Trigger]
  Method: POST
  Path: /ask
      ↓
[Set: question = {{ $json.body.question }}]
      ↓
[Qdrant Retrieve]
  Collection: company_knowledge
  Query: {{ $json.question }}
  Top K: 5
  Score Threshold: 0.70
      ↓
[Code Node: "Sprawdź score i przygotuj kontekst"]
      ↓
[If Node: has_results == true]
  TRUE → [OpenAI Chat Model]
  FALSE → [Set: fallback_message]
      ↓                    ↓
[Set: format answer]  [Set: format fallback]
      ↓                    ↓
     [Webhook Respond] (oba wyjścia zbiegają się)
```

**Code Node "Sprawdź score":**

```javascript
const items = $input.all();
const hasResults = items.length > 0 && items[0].json.score > 0.65;

if (!hasResults) {
  return [{
    json: {
      has_results: false,
      context: "",
      max_score: 0
    }
  }];
}

// Przygotuj kontekst dla AI
const contextParts = items.map((item, i) => {
  const meta = item.json.payload || {};
  return `[FRAGMENT ${i+1}]
Plik: ${meta.fileName || "nieznany"} | Indeks: ${meta.chunkIndex || 0}
Score: ${(item.json.score || 0).toFixed(3)}
---
${item.json.payload?.text || item.json.text || ""}`;
}).join("\n\n");

return [{
  json: {
    has_results: true,
    context: contextParts,
    max_score: items[0].json.score,
    sources: items.map(i => i.json.payload?.fileName).filter(Boolean)
  }
}];
```

**System prompt dla OpenAI Chat:**

```
Jesteś asystentem firmowym Dokodu. Odpowiadaj WYŁĄCZNIE na podstawie poniższych fragmentów dokumentów.

ZASADY (przestrzegaj bezwzględnie):
1. Każde stwierdzenie faktyczne zakończ przypisem: [Źródło: {fileName}]
2. Cytuj dokładne fragmenty tekstu gdy to możliwe (w cudzysłowie)
3. Jeśli fragmenty nie zawierają odpowiedzi → napisz DOKŁADNIE: "Nie znalazłem tej informacji w dostępnych dokumentach firmowych."
4. NIE uzupełniaj wiedzą ogólną. NIE zmyślaj.

FRAGMENTY DOKUMENTÓW:
{{ $json.context }}
```

**User message:**
```
{{ $('Webhook Trigger').item.json.body.question }}
```

---

### Test końcowy (5 min)

Wyślij request do webhoooka:

```bash
curl -X POST https://twoj-n8n.com/webhook/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Jakie są warunki płatności?"}'
```

Sprawdź odpowiedź. Powinna zawierać:
- Konkretne warunki z Twoich dokumentów
- Cytat lub parafrazę z zaznaczonym źródłem
- Nazwę pliku z którego pochodzi odpowiedź

Zadaj pytanie spoza zakresu dokumentów (np. "Jaka jest pogoda w Warszawie?") — system powinien zwrócić fallback message.

---

### Dodaj integrację ze Slackiem (opcjonalnie, +10 min)

Zamień Webhook Trigger na Slack Trigger (event: message w kanale #asystent-wiedzy).

Na końcu dodaj node Slack: Send Message z odpowiedzią i linkiem do dokumentu w Drive.

Teraz możesz pytać asystenta bezpośrednio ze Slacka.

---

### Kryteria zaliczenia ćwiczenia
- [ ] Qdrant ma punkty z minimum 5 dokumentów
- [ ] Zapytanie o fakty z dokumentów zwraca odpowiedź z cytatem
- [ ] Zapytanie spoza zakresu zwraca fallback message (nie zmyślenie)
- [ ] Odpowiedź zawiera nazwę pliku źródłowego

---

## Zadanie domowe: Auto-Refresh przy zmianie dokumentu
**Czas: ~60 minut | Poziom: zaawansowany**

### Zadanie
Rozbuduj Workflow #1 o mechanizm incremental updates. Jeśli plik w Google Drive jest modyfikowany — system powinien:

1. Wykryć że plik się zmienił (hash MD5 content)
2. Usunąć stare chunki z Qdrant (filter: fileId)
3. Zembeddować zaktualizowany plik
4. Zapisać nowe chunki z nowym hashem w metadanych

### Wskazówki

**Obliczanie hasha w n8n (Code Node):**
```javascript
const crypto = require('crypto');
const content = $input.first().json.content || "";
const hash = crypto.createHash('md5').update(content).digest('hex');
return [{ json: { ...($input.first().json), hash } }];
```

**Sprawdzenie czy hash istnieje w Qdrant (HTTP Request):**
```
POST http://localhost:6333/collections/company_knowledge/points/scroll
Body:
{
  "filter": {
    "must": [
      { "key": "fileId", "match": { "value": "{{ $json.fileId }}" } },
      { "key": "hash", "match": { "value": "{{ $json.hash }}" } }
    ]
  },
  "limit": 1
}
```

Jeśli wynik `points` jest pustą tablicą → plik zmieniony, trzeba re-embeddować.

**Usunięcie starych chunków (HTTP Request):**
```
POST http://localhost:6333/collections/company_knowledge/points/delete
Body:
{
  "filter": {
    "must": [
      { "key": "fileId", "match": { "value": "{{ $json.fileId }}" } }
    ]
  }
}
```

### Sukces zadania domowego

Zmodyfikuj jeden z dokumentów w Drive (zmień "21 dni" na "30 dni"). Po 2 minutach zapytaj asystenta o termin płatności — powinien zwrócić nową wartość (30 dni), nie starą.

**Podziel się wynikiem na platformie kursowej** z krótkim opisem co zrobiłeś.

---

## Materiały dodatkowe

- [Qdrant Documentation](https://qdrant.tech/documentation/) — szczególnie sekcja Payload Filtering
- [RAGAS GitHub](https://github.com/explodinggradients/ragas) — framework ewaluacji RAG
- [LlamaIndex Chunking Guide](https://docs.llamaindex.ai/en/stable/module_guides/loading/node_parsers/) — zaawansowane strategie chunkowania
- [OpenAI Embeddings Docs](https://platform.openai.com/docs/guides/embeddings) — wszystko o modelach embeddingowych
- `scripts/rag_eval.py` w repozytorium kursu — gotowy skrypt RAGAS do ewaluacji Twojego systemu
