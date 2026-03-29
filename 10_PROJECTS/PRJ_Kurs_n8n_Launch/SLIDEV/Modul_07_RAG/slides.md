---
theme: default
titleTemplate: "%s | Dokodu"
highlighter: shiki
lineNumbers: false
drawings:
  persist: false
transition: slide-left
mdc: true
fonts:
  sans: Inter
  mono: Fira Code
css: style.css
---


---
transition: fade
layout: cover
---

<img src="/dokodu_logo.png" style="height:28px;margin-bottom:1.8rem;opacity:0.92" alt="Dokodu" />

<div class="cover-tag">MODUŁ 07 — RAG</div>

# Kurs n8n


<p style="color:#E63946;font-weight:600">Kacper Sieradziński</p>
<p style="color:#8096AA;font-size:0.8rem;margin-top:0.2rem">dokodu.it</p>


---
---

# Tytuł tygodnia

## Tydzień 7: Cydrowy Mózg Firmy
## RAG i Eliminacja Halucynacji

*Kacper Sieradziński | n8n + AI dla Agencji i Firm*

<!--
Ekran startowy, 3 sekundy przed rozmową — cisza, potem wchodzisz z hookiem.
-->


---
---

# Hook — problem

## Twoja firma ma tysiące dokumentów.
## Nikt ich nie czyta.

- Regulaminy, oferty, umowy, maile, instrukcje — leżą na Drive
- Pracownicy pytają zamiast szukać
- AI bez dostępu do tych danych — zmyśla

<!--
Powiedz to wolno. "Tysiące dokumentów. Nikt ich nie czyta." Pauza. "Ale Twój AI może." Tutaj przechodzisz do slajdu 3.
-->


---
---

# Co zbudujemy dzisiaj

## Firmowy Asystent Wiedzy

```
Google Drive → Qdrant → Slack
     ↓              ↓         ↓
 dokumenty    wektory    odpowiedź
   firmy      + meta     z cytatem
```


<v-clicks>

- Workflow 1: Ingestion Pipeline (nowy dokument → baza wektorowa)
- Workflow 2: Query Pipeline (pytanie → odpowiedź z numerem strony)
- Wynik: AI który NIE zmyśla i zawsze pokazuje źródło

</v-clicks>


<!--
Pokaż slajd przez 10 sekund, powiedz "dziś robimy to od zera". Przejdź do wyjaśnienia RAG.
-->


---
---

# Co to jest RAG?

## RAG = Retrieval Augmented Generation

Trzy słowa, trzy etapy:

<v-clicks>

1. **Retrieval** — pobierz właściwe fragmenty z bazy wiedzy
2. **Augmented** — wzbogać prompt o te fragmenty
3. **Generation** — AI generuje odpowiedź NA BAZIE tych fragmentów

</v-clicks>


<!--
Nie wchodź jeszcze w techniczne szczegóły — to jest definicja "w jednym zdaniu". Zaraz dasz analogię.
-->


---
---

# Analogia — dobry bibliotekarz

## AI bez RAG = student który wszystko zapamiętał, ale pamięć go zawodzi

## AI z RAG = bibliotekarz który
- Nie pamięta treści każdej książki
- Ale wie dokładnie gdzie szukać
- Przynosi Ci właściwy fragment
- I mówi: "to jest na stronie 47, rozdział 3"

<!--
Ta analogia działa rewelacyjnie. Podkreśl: "bibliotekarz nie zmyśla — jeśli nie ma książki, mówi że nie wie". To jest klucz do eliminacji halucynacji.
-->


---
transition: fade
---

# RAG pipeline — pełny diagram

<div style="display:flex;gap:1.2rem;align-items:flex-start">
  <div style="flex:1">
    <div style="color:#F97316;font-weight:700;font-size:0.78rem;margin-bottom:0.5rem">INGEST (jednorazowo)</div>
    <N8nFlow
      :nodes="[
        {icon: 'mdi:file-document', label: 'Dokumenty', variant: 'default'},
        {icon: 'mdi:content-cut', label: 'Chunking', desc: '500 tokenów', variant: 'action'},
        {icon: 'mdi:vector-point', label: 'Embeddings', desc: 'ada-002', variant: 'action'},
        {icon: 'mdi:database', label: 'Qdrant', desc: 'Vector DB', variant: 'output'},
      ]"
    />
  </div>
  <div style="flex:1">
    <div style="color:#3B82F6;font-weight:700;font-size:0.78rem;margin-bottom:0.5rem">QUERY (każde pytanie)</div>
    <N8nFlow
      :nodes="[
        {icon: 'mdi:help-circle', label: 'Pytanie', variant: 'trigger'},
        {icon: 'mdi:magnify', label: 'Search', desc: 'Top-K chunks', variant: 'action'},
        {icon: 'mdi:brain', label: 'LLM', desc: 'prompt + chunks', variant: 'action'},
        {icon: 'mdi:message-text', label: 'Odpowiedź', desc: 'z cytatami!', variant: 'output'},
      ]"
    />
  </div>
</div>


<!--
Przejdź przez diagram wolno, wskazując każdy krok. "Lewa strona to robi się RAZ — budujemy bazę wiedzy. Prawa strona — to się dzieje przy KAŻDYM pytaniu, w ciągu sekund."
-->


---
---

# Demo kontrastu — bez RAG

**Pytanie:** "Jakie są warunki płatności w naszej umowie z klientem Acme?"

## GPT-4o bez RAG
> "Standardowe warunki płatności wynoszą zazwyczaj 14-30 dni od daty wystawienia faktury. Wiele firm stosuje również zaliczki w wysokości 20-50% wartości umowy..."

**Problem:** To jest zmyślone. GPT nie ma dostępu do Twojej umowy.

<!--
Tutaj możesz przełączyć się na LIVE demo — otwórz ChatGPT i zadaj pytanie o "wewnętrzne dokumenty firmy". Pokaż jak AI zmyśla z pewnością siebie.
-->


---
---

# Demo kontrastu — z RAG

**Pytanie:** "Jakie są warunki płatności w naszej umowie z klientem Acme?"

## AI z RAG
> "Zgodnie z umową z Acme Corp (plik: Umowa_Acme_2025.pdf, §4.2, str. 8): płatność w ciągu **21 dni** od daty faktury, zaliczka **30%** przy podpisaniu, kara za opóźnienie **0,5% dziennie**."

**Różnica:** Konkretne dane. Źródło. Numer paragrafu.

<!--
Mocne uderzenie. "To samo pytanie, dwie odpowiedzi. Jedna z nich możesz wysłać do prawnika. Druga może Cię wpakować w kłopoty."
-->


---
---

# Embeddings — co to jest?

## Embedding = zamiana tekstu na listę liczb (wektor)

```
"Termin płatności: 21 dni"
        ↓
[0.23, -0.87, 0.14, 0.56, ..., -0.31]
      (1536 wymiarów dla ada-002)
```

## Kluczowa właściwość
Podobne znaczeniowo zdania = blisko siebie w przestrzeni wektorowej

<!--
Powiedz "wyobraź sobie mapę miasta, gdzie podobne sklepy stoją obok siebie — piekarnie przy piekarniach, banki przy bankach. Embeddingi to mapa Twojego tekstu."
-->


---
---

# Wizualizacja przestrzeni wektorowej

```
                  DOKUMENTY FINANSOWE
            ●umowa_acme    ●faktura_2024
                 ●warunki_platnosci

    ●regulamin_pracy
    ●polityka_urlopow              ●specyfikacja_techniczna
                                   ●dokumentacja_api
         HR DOKUMENTY                  TECH DOKUMENTY
```

*(wizualizacja t-SNE 2D — w rzeczywistości 1536 wymiarów)*

**Twoje pytanie "warunki płatności"** → ląduje blisko dokumentów finansowych → retrieval wyciąga właściwe chunki

<!--
"Oczywiście nie ma 2 wymiarów tylko 1536 — t-SNE to projekcja żebyś mógł to zobaczyć. Ale zasada jest ta sama: podobne = blisko."
-->


---
---

# Embedding models — porównanie

| Model | Wymiary | Koszt / 1M tokenów | Jakość | Uwagi |
|-------|---------|---------------------|--------|-------|
| `text-embedding-ada-002` | 1536 | $0.10 | ★★★☆ | Legacy, dobry do PoC |
| `text-embedding-3-small` | 1536 | $0.02 | ★★★★ | **Polecany: 5x tańszy od ada-002** |
| `text-embedding-3-large` | 3072 | $0.13 | ★★★★★ | Do najwyższej precyzji |
| Cohere Embed v3 | 1024 | $0.10 | ★★★★ | Dobry hybrid search |
| `nomic-embed-text` | 768 | free (self-host) | ★★★☆ | Lokalnie przez Ollama |

**Rekomendacja kursu:** `text-embedding-3-small` — najlepszy stosunek jakości do ceny

<!--
"Dla 95% projektów text-embedding-3-small wystarczy. Nie przepłacaj za large jeśli nie masz konkretnego powodu."
-->


---
---

# Vector databases — przegląd

## 3 opcje które widzisz najczęściej


<v-clicks>

- **Pinecone** — managed cloud, zero devops, drogi przy skali
- **Qdrant** — open-source, self-host lub cloud, najlepszy performance
- **PGVector** — rozszerzenie PostgreSQL, masz DB → masz vector store

</v-clicks>


**Pytanie wyboru:** gdzie jesteś na osi "czas vs pieniądze"?

<!--
Nie deprecjonuj żadnego — każdy ma swoje miejsce. Pokaż tabelę na następnym slajdzie.
-->


---
---

# Tabela porównawcza — vector databases

| Cecha | Pinecone | Qdrant | PGVector |
|-------|----------|--------|----------|
| **Hosting** | Cloud only | Self-host / Cloud | Self-host (Postgres) |
| **Setup time** | 5 min | 10 min (Docker) | 15 min (jeśli masz PG) |
| **Koszt (free tier)** | 1 index, 100K vec. | Open-source gratis | Gratis (Postgres) |
| **Koszt (prod, 1M vec.)** | ~$70/mies. | ~$20/mies. (cloud) / gratis (self-host) | Koszt serwera |
| **Latencja** | ~50ms | ~5ms (local) | ~10ms (local) |
| **Hybrid search** | Tak | Tak (BM25 wbudowany) | Plugin (pgvector + tsvector) |
| **Filtry metadanych** | Tak | Tak (payload filters) | Tak (SQL WHERE) |
| **Integracja n8n** | Natywna | Natywna | Natywna |
| **Rekomendacja** | SaaS, szybki start | Self-host, performance | Masz już Postgres |

<!--
"W tym kursie używamy Qdrant — jest darmowy, szybki i masz pełną kontrolę. Pinecone możesz zamienić w n8n jedną zmianą node'a."
-->


---
---

# Chunking — dlaczego to ważne?

## Chunk = fragment dokumentu który wchodzi do bazy wektorowej

## Problem zbyt dużych chunków
- Embedding rozmywa się — za dużo tematów w jednym wektorze
- Retrieval zwraca mniej precyzyjne wyniki

## Problem zbyt małych chunków
- Brak kontekstu — fragment "21 dni" bez reszty zdania jest bezużyteczny
- Więcej chunkow = więcej tokenów = wyższy koszt

**Sweet spot:** 300–600 tokenów z 10–15% overlap

<!--
"Dobry chunking to 80% sukcesu w RAG. Większość problemów z 'AI nie rozumie pytania' to w rzeczywistości problem złego chunkingu."
-->


---
---

# Chunking strategies — diagram porównawczy

<div class="diagram-block">

```
FIXED SIZE (najprostszy)
[──────500──────][──────500──────][──────500──────]
                 ←50 overlap→

Zaleta: prosty, przewidywalny
Wada: może przeciąć zdanie w połowie

─────────────────────────────────────────────────────

SEMANTIC (inteligentny)
[── temat A ────────][── temat B ──][─── temat C ───]

Zaleta: każdy chunk = jeden temat
Wada: wymaga modelu do segmentacji, wolniejszy

─────────────────────────────────────────────────────

HIERARCHICAL (najdokładniejszy)
[────── cały dokument (summary) ──────────────────]
  [── rozdział 1 (summary) ──][── rozdział 2 ──]
    [chunk 1.1][chunk 1.2]      [chunk 2.1][chunk 2.2]

Zaleta: retrieval na wielu poziomach szczegółowości
Wada: złożona implementacja, więcej embeddings
```

</div>

<!--
"Dla 90% projektów Fixed Size z overlappem wystarczy. Semantic kiedy dokumenty mają wyraźne sekcje. Hierarchical dla bardzo dużych baz (1000+ dokumentów, różne typy pytań)."
-->


---
---

# Chunk overlap — wizualnie

<div class="diagram-block">

```
Dokument: "...Termin płatności wynosi 21 dni [KONIEC CHUNK 1]
[POCZĄTEK CHUNK 2] od daty wystawienia faktury. Odsetki..."

BEZ OVERLAP:
Chunk 1: "...Termin płatności wynosi 21 dni"    ← urwane!
Chunk 2: "od daty wystawienia faktury. Odsetki..." ← bez kontekstu!

Z OVERLAP (50 tokenów):
Chunk 1: "...Termin płatności wynosi 21 dni"
Chunk 2: "wynosi 21 dni od daty wystawienia faktury. Odsetki..."
           ↑─────────── overlap ──────────────↑
```

</div>

**Pytanie "ile dni na płatność?"** → poprawnie trafi do Chunk 2 ✓

<!--
"Overlap to ubezpieczenie na granicy chunków. Koszt: ~10% więcej tokenów. Wartość: drastycznie mniej odpowiedzi 'nie znalazłem'."
-->


---
---

# n8n vector store nodes

## 3 podstawowe nodes

```
[Vector Store: Insert]     → wstawia wektory + metadane
[Vector Store: Retrieve]   → pobiera podobne wektory (top-K)
[Vector Store: Query]      → insert + retrieve w jednym (do testów)
```

## Konfiguracja Insert
- Credential: Qdrant API
- Collection: nazwa kolekcji
- Data: tekst chunka
- Metadata: `{ fileName, page, chunkIndex, date }`

<!--
Przejdź teraz do n8n i pokaż te nodes w palecie. "Są w kategorii AI → Vector Stores."
-->


---
transition: fade
---

# Ingestion workflow #1 — architektura

<N8nFlow
  :nodes="[
    {icon: 'logos:google-drive', label: 'Drive Trigger', desc: 'nowy plik', variant: 'trigger'},
    {icon: 'mdi:download', label: 'Download', desc: 'pobierz plik', variant: 'default'},
    {icon: 'mdi:file-document-outline', label: 'Extract Text', desc: 'PDF/DOCX → text', variant: 'action'},
    {icon: 'mdi:content-cut', label: 'Chunker', desc: '500 tok, 50 overlap', variant: 'action'},
    {icon: 'mdi:vector-point', label: 'Embeddings', desc: 'text-embedding-3-small', variant: 'action'},
    {icon: 'mdi:database-plus', label: 'Qdrant Insert', desc: '+ metadane', variant: 'output'},
  ]"
  caption="Automatyczny pipeline: nowy plik na Drive → chunki + embeddingi → baza wektorowa"
/>


<!--
"Workflow #1 jest JEDNORAZOWY na każdy dokument — odpala się automatycznie gdy nowy plik trafia na Drive lub istniejący jest zmodyfikowany."
-->


---
---

# Incremental updates — hash trick

**Problem:** dokument się zmienił → stare chunki w Qdrant są nieaktualne

## Rozwiązanie: hash dokumentu jako wersja

```
1. Oblicz MD5 hash nowego pliku
2. Sprawdź czy hash istnieje w Qdrant (filter: fileId + hash)
3. Jeśli taki sam → pomiń (oszczędność ~100% kosztów embeddings)
4. Jeśli różny:
   a. Usuń stare chunki (filter: fileId = X)
   b. Zembedduj nowy plik
   c. Zapisz z nowym hashem
```

<!--
"Bez tego mechanizmu każda zmiana w dokumencie duplikuje dane w Qdrant. Po 3 miesiącach masz chaos — 5 wersji tej samej umowy w bazie."
-->


---
---

# Qdrant collection schema

## Kolekcja: `company_knowledge`

```json
{
  "vectors": {
    "size": 1536,
    "distance": "Cosine"
  },
  "payload": {
    "text": "string",
    "fileName": "string",
    "fileId": "string",
    "fileType": "pdf|docx|sheet",
    "page": "integer",
    "chunkIndex": "integer",
    "totalChunks": "integer",
    "modifiedDate": "string (ISO 8601)",
    "hash": "string (MD5)",
    "category": "string (HR|Finance|Legal|Product)"
  }
}
```

<!--
"Metadane to złoto. Dzięki nim możesz filtrować — 'szukaj tylko w dokumentach HR' albo 'tylko pliki z ostatniego miesiąca'. Bez metadanych masz tylko chaotyczną zupę wektorów."
-->


---
transition: fade
---

# Query workflow #2 — architektura

<N8nFlow
  :nodes="[
    {icon: 'logos:slack-icon', label: 'Slack / Webhook', desc: 'pytanie', variant: 'trigger'},
    {icon: 'mdi:vector-point', label: 'Embed pytanie', desc: 'text-emb-3-small', variant: 'default'},
    {icon: 'mdi:database-search', label: 'Qdrant Retrieve', desc: 'top 5, score > 0.75', variant: 'action'},
    {icon: 'mdi:sort-ascending', label: 'Reranker', desc: 'opcjonalny', variant: 'default'},
    {icon: 'mdi:brain', label: 'AI Agent', desc: 'TYLKO z fragmentów', variant: 'action'},
    {icon: 'logos:slack-icon', label: 'Odpowiedź', desc: 'z cytatami + źródło', variant: 'output'},
  ]"
  caption="Guardrail: score < 0.65 → 'Nie znalazłem tej informacji' (bez halucynacji)"
/>


<!--
"Zwróć uwagę na system prompt — kluczowe są trzy rzeczy: 'TYLKO na podstawie', cytowanie źródła, i 'powiedz że nie wiesz'. To są guardrails przeciw halucynacjom."
-->


---
---

# Similarity search — metryki

## Jak mierzyć podobieństwo dwóch wektorów?

| Metryka | Zasada | Kiedy używać |
|---------|--------|--------------|
| **Cosine Similarity** | Kąt między wektorami (0–1) | Teksty — standard |
| **Dot Product** | Iloczyn skalarny | Gdy wektory znormalizowane (szybszy) |
| **Euclidean** | Odległość w przestrzeni | Obrazy, dane numeryczne |

**Dla RAG z tekstem:** zawsze Cosine Similarity

**Threshold:** > 0.75 = relevantny, < 0.6 = pomiń

<!--
"Nie wchodź głęboko w matematykę. Ważna zasada: 'im bliżej 1, tym bardziej podobne'. Próg 0.75 jest dobrym startem — możesz go podnieść jeśli masz za dużo szumu."
-->


---
---

# Hybrid search

## Problem z samymi embeddingami
- Embedding "LLM" i "Large Language Model" → podobne ✓
- Embedding "GPT-4" i "GPT-3" → bardzo podobne (ale to różne modele!)
- Embedding rzadkich słów (nazwy własne, kody produktów) → słabe

## Hybrid Search = Semantic + Keyword (BM25)

```
Score_final = α × Score_semantic + (1-α) × Score_BM25
```

Typowo: α = 0.7 (70% semantyczny, 30% keyword)

<!--
"Qdrant ma hybrid search wbudowany od wersji 1.7. Dla korporacyjnych dokumentów z kodami produktów, numerami umów, nazwami klientów — hybrid jest niezbędny."
-->


---
---

# Reranking — po co i jak

**Problem:** top-5 chunków z similarity search nie zawsze są w dobrej kolejności

## Reranker = model który ponownie ocenia trafność każdego chunka do pytania

```
Similarity Search → [C1: 0.87] [C2: 0.85] [C3: 0.84] [C4: 0.82] [C5: 0.81]

Cross-Encoder Reranker:
→ [C3: 0.96] ← WYGRAŁ (bardziej precyzyjnie odpowiada na pytanie)
  [C1: 0.88]
  [C5: 0.71]
  [C2: 0.63]
  [C4: 0.41]
```

**Opcje w n8n:** Cohere Rerank API, Jina Reranker, lokalne modeli Sentence Transformers

<!--
"Reranking dodaje ~200ms latencji ale znacząco poprawia jakość odpowiedzi. Opłaca się gdy masz >1000 pytań dziennie i musisz być precyzyjny."
-->


---
---

# Source citations — jak zmusić AI do cytowania

## System prompt (kluczowy fragment)

```
Jesteś asystentem firmowym. Odpowiadaj WYŁĄCZNIE na podstawie
poniższych fragmentów dokumentów.

ZASADY:
1. Każde stwierdzenie oparte na danych musisz zakończyć: [Źródło: {fileName}, str. {page}]
2. Jeśli odpowiedź nie wynika z dostarczonych fragmentów → napisz:
   "Nie znalazłem tej informacji w dostępnych dokumentach."
3. NIE uzupełniaj wiedzy własną pamięcią.

FRAGMENTY:
{retrieved_chunks}
```

<!--
"To jest serce eliminacji halucynacji. Nie 'staraj się cytować' — TYLKO na podstawie, NIE uzupełniaj. Bezwzględne zasady, nie prośby."
-->


---
---

# Confidence scores i fallback

## Kiedy AI powinno powiedzieć "nie wiem"?

```
Jeśli max(similarity_scores) < 0.65:
   → zwróć "Nie znalazłem tej informacji w dostępnych dokumentach.
             Skontaktuj się z [email]."
   → NIE wysyłaj do LLM (oszczędność kosztów + brak halucynacji)

Jeśli max(similarity_scores) ∈ [0.65, 0.75]:
   → dodaj do promptu: "Uwaga: poniższe fragmenty mogą być nieidealne.
                        Zaznacz jeśli nie jesteś pewien odpowiedzi."
```

**W n8n:** Code Node po Retrieve, If Node na podstawie score

<!--
"Ten mechanizm to różnica między narzędziem któremu ufasz a narzędziem które boisz się użyć. 'Nie wiem' jest zawsze lepsze niż zmyślona pewność."
-->


---
---

# Ewaluacja RAG — RAGAS framework

## Jak zmierzyć czy Twój RAG działa?

| Metryka | Co mierzy | Jak liczyć |
|---------|-----------|------------|
| **Context Precision** | Czy pobrane chunki są relevantne? | relevantne / wszystkie pobrane |
| **Context Recall** | Czy pobrałeś wszystkie relevantne chunki? | pobrane relevantne / wszystkie relevantne |
| **Answer Faithfulness** | Czy odpowiedź wynika z chunków? | brak halucynacji |
| **Answer Relevance** | Czy odpowiedź odpowiada na pytanie? | nie zmienia tematu |

**Narzędzie:** RAGAS (pip install ragas) — automatyczna ewaluacja z LLM-as-judge

<!--
"Bez ewaluacji optymalizujesz w ciemno. Masz 20 pytań testowych z oczekiwanymi odpowiedziami? Uruchom RAGAS. Zobaczysz dokładnie gdzie system się sypie."
-->


---
---

# Ewaluacja — praktyczna implementacja w n8n

## Test dataset: 20 pytań z oczekiwanymi odpowiedziami

```
Q: "Jaki jest termin płatności w umowie Acme?"
Expected: "21 dni od daty faktury" (§4.2, str. 8)

Q: "Ile wynosi kara za opóźnienie?"
Expected: "0.5% dziennie" (§4.3, str. 8)
```

## Workflow ewaluacyjny
1. Loop przez test dataset
2. Dla każdego pytania: uruchom Query workflow
3. Compare: answer vs expected (Code Node + GPT-4o jako judge)
4. Zapisz wyniki do Google Sheets (precision, recall, pass/fail)

<!--
"Zalecam robić taki test przed każdą większą zmianą w systemie — nowy model embeddingów, nowe chunki, nowy prompt. To Twój 'unit test' dla RAG."
-->


---
---

# Koszty — 100 dokumentów

## Szacunek kosztów dla typowej polskiej firmy

```
INGESTION (jednorazowo):
100 dokumentów × średnio 20 stron × ~300 tokenów/strona = 600K tokenów
text-embedding-3-small: 600K × $0.02/1M = $0.012 (~5 groszy)

STORAGE:
Qdrant self-hosted: $0 (VPS ~$10/mies. dla innych rzeczy)
Qdrant Cloud free tier: do 1M wektorów gratis

QUERIES (miesięcznie, 1000 pytań):
Embed pytania: 1000 × 50 tokenów × $0.02/1M = $0.001
GPT-4o generation: 1000 × ~1500 tokenów = 1.5M × $5/1M = $7.50

TOTAL: ~$7.50/miesiąc dla 1000 pytań
```

<!--
"Siedem i pół dolara miesięcznie za asystenta który zna całą bazę wiedzy firmy i nie halucynuje. Pytanie nie brzmi 'czy to się opłaca' tylko 'kiedy zaczynam'."
-->


---
---

# Koszty — skalowanie

| Skala | Dokumenty | Pytania/mies. | Koszt/mies. |
|-------|-----------|----------------|-------------|
| Startup | 50 | 200 | ~$2 |
| Mała firma | 200 | 1 000 | ~$8 |
| Średnia firma | 500 | 5 000 | ~$35 |
| Enterprise | 5 000 | 50 000 | ~$300 |

*Zakłada text-embedding-3-small + GPT-4o-mini (tańszy model produkcyjny)*

**Tip:** Użyj GPT-4o-mini zamiast GPT-4o do generation — 20x tańszy, 80% jakości

<!--
"Przy skali enterprise zacznij patrzeć na self-hosted modele embeddingowe (nomic-embed-text przez Ollama). Retrieval jest zawsze tańszy niż generation."
-->


---
---

# Optymalizacje — top 5

## 1. Chunk size tuning
Zacznij od 500 tokenów, 50 overlap. Przetestuj 300 i 800. Użyj RAGAS.

## 2. Metadata filtering
Zawsze filtruj po kategorii ("szukaj w HR, nie w całej bazie") — szybciej i precyzyjniej.

## 3. Cache popularnych pytań
20% pytań to 80% wolumenu. Cache w Redis lub Sheets — zero kosztów embeddingu.

## 4. Async ingestion
Nie blokuj użytkownika podczas ingestion — osobny workflow, powiadomienie gdy gotowe.

## 5. Monitoring
Loguj każde pytanie, score, odpowiedź. Po 100 pytaniach masz złoto do optymalizacji.

<!--
"Żadna z tych optymalizacji nie jest skomplikowana. Razem mogą obniżyć koszty o 60% i podwoić jakość. Wprowadzaj je iteracyjnie, mierz każdą."
-->


---
---

# n8n vector store — pełna konfiguracja (insert)

<div class="diagram-block">

```
Node: Qdrant Vector Store (Insert)
─────────────────────────────────
Credential:   Qdrant API (URL + API key)
Collection:   company_knowledge
Operation:    Insert Documents

Data to Insert:
  Content:    {{ $json.chunkText }}
  Metadata: {
    "fileName":     "{{ $json.fileName }}",
    "fileId":       "{{ $json.fileId }}",
    "page":         {{ $json.pageNumber }},
    "chunkIndex":   {{ $json.chunkIndex }},
    "modifiedDate": "{{ $json.modifiedDate }}",
    "hash":         "{{ $json.fileHash }}"
  }

Embedding Model: OpenAI Embeddings
  Model: text-embedding-3-small
  Dimensions: 1536
```

</div>

<!--
Pokaż to w n8n — "Mamy tekst chunka, mamy metadane, mamy model embeddingów. Klikamy Execute. Qdrant zwraca ID punktu — sukces."
-->


---
---

# n8n vector store — pełna konfiguracja (retrieve)

<div class="diagram-block">

```
Node: Qdrant Vector Store (Retrieve)
─────────────────────────────────────
Collection:  company_knowledge
Operation:   Retrieve Documents

Query:       {{ $json.userQuestion }}
Top K:       5
Score Threshold: 0.75

Filters (opcjonalne):
  category = "Finance"    ← szukaj tylko w finansach
  modifiedDate > "2025-01-01"  ← tylko aktualne dokumenty

Return Fields:
  text, fileName, page, chunkIndex, fileId
```

</div>

<!--
"Score Threshold 0.75 — to jest granica 'relevantny'. Poniżej tego score — nie wysyłamy do AI. Zamiast tego: fallback message do użytkownika."
-->


---
---

# Odpowiedź z cytatami — przykład

**Pytanie:** "Czy możemy wysłać dane klientów do USA?"

## Odpowiedź Asystenta Wiedzy

> Na podstawie Polityki RODO (RODO_Policy_v2.pdf, str. 4):
>
> "Dane osobowe klientów mogą być przekazywane do państw spoza EOG wyłącznie na podstawie standardowych klauzul umownych zatwierdzonych przez KE lub decyzji o adekwatności."
>
> Stany Zjednoczone posiadają decyzję o adekwatności dla firm certyfikowanych w ramach **Data Privacy Framework** (RODO_Policy_v2.pdf, str. 5).
>
> **Odpowiedź:** Tak, jeśli dostawca posiada certyfikat DPF. Zweryfikuj listę na: privacyshield.gov.
>
> 📎 Źródło: [RODO_Policy_v2.pdf](drive.google.com/...)

<!--
"To jest cel. Konkretna odpowiedź, cytat z dokumentu, numer strony, link do pliku. Prawnik może to zweryfikować w 30 sekund."
-->


---
transition: fade
layout: two-cols-header
---

# Kiedy RAG NIE wystarczy

<div class="col-header col-pos">RAG jest świetny gdy</div>

- Masz statyczne lub rzadko zmieniające się dokumenty
- Pytania mają konkretne odpowiedzi w dokumentach
- Potrzebujesz audytowalności (źródła!)

::right::

<div class="col-header col-neg">RAG NIE wystarczy gdy</div>

- Potrzebujesz agregacji (np. "zsumuj wszystkie faktury z Q1") → użyj SQL/code tool
- Dane są strukturalne (tabele) → lepiej SQL agent
- Potrzebujesz rozumowania wielokrokowego → RAG + Agent + Tools

<!--
"W przyszłym tygodniu połączymy RAG z agentem. Asystent który nie tylko WIE ale też DZIAŁA — wysyła maile, aktualizuje CRM, tworzy zadania."
-->


---
class: layout-takeaway
---

# Podsumowanie tygodnia

## Co opanowałeś

<v-clicks>

- RAG pipeline: ingest → store → retrieve → generate
- Embeddings: tekst jako wektor, przestrzeń semantyczna
- Qdrant: setup, kolekcje, metadane, filtry
- Chunking: 500 tokenów, 50 overlap, overlap ratuje granice
- Eliminca halucynacji: strict prompt + source citations + fallback
- Ewaluacja: RAGAS, test dataset, iteracja

</v-clicks>


**Projekt tygodnia:** Firmowy Asystent Wiedzy działa na Twoim Google Drive

**Tydzień 8:** RAG + Agenci — asystent który wie i działa

<!--
"Jeśli po tym tygodniu zrobiłeś jedno — zbuduj Knowledge Assistant dla swoich własnych dokumentów. To jest ten jeden workflow który możesz sprzedać każdemu klientowi."
-->


---
class: layout-exercise
---

# Ćwiczenia praktyczne

Czas na praktykę! Otwórz n8n i zrób ćwiczenia samodzielnie.


---
class: layout-exercise
---

# Ćwiczenie 1: setup qdrant + pierwsze embeddingi




---
class: layout-exercise
---

# Ćwiczenie 2: firmowy asystent wiedzy — kompletny build


## Checkpointy

<v-clicks>

- Qdrant ma punkty z minimum 5 dokumentów
- Zapytanie o fakty z dokumentów zwraca odpowiedź z cytatem
- Zapytanie spoza zakresu zwraca fallback message (nie zmyślenie)
- Odpowiedź zawiera nazwę pliku źródłowego

</v-clicks>



---
class: layout-exercise
---

# Zadanie domowe: auto-refresh przy zmianie dokumentu




---
class: layout-exercise
---

# Materiały dodatkowe


