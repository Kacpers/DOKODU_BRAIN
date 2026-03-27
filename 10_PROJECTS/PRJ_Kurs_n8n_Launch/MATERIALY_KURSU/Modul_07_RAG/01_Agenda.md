---
type: course-agenda
modul: 07
tytul: "Cyfrowy Mózg Firmy (RAG) i Eliminacja Halucynacji"
czas_total: "3h 00min"
projekt_tygodnia: "Firmowy Asystent Wiedzy (Company Knowledge Assistant)"
status: draft
last_reviewed: 2026-03-27
---

# Modul 07 — Agenda nagrania (3h)

**Tytuł tygodnia:** Cyfrowy Mózg Firmy (RAG) i Eliminacja Halucynacji
**Projekt tygodnia:** Firmowy Asystent Wiedzy — Google Drive → Qdrant → Slack/Email z cytatami

---

## SEGMENT 1: RAG — od teorii do intuicji
**Czas: 0:00 – 0:35 (35 min)**

| Minuty | Zawartość | Format |
|--------|-----------|--------|
| 0:00–0:03 | **Hook** — "Twoja firma ma tysiące dokumentów. Nikt ich nie czyta. Twój AI może." | Kamera na twarz |
| 0:03–0:10 | Przegląd tygodnia: co zbudujemy, dlaczego RAG zmienia wszystko | Slajd agendy |
| 0:10–0:18 | **Czym jest RAG** — definicja, analogia bibliotekarza, diagram pipeline | Slajd + animacja |
| 0:18–0:25 | **Demo kontrastu** — pytanie do GPT bez RAG (halucynacja) vs z RAG (odpowiedź z cytatem) | Demo LIVE |
| 0:25–0:35 | **Embeddings** — jak tekst zamienia się w wektory, intuicyjne wyjaśnienie, przestrzeń semantyczna | Slajd wizualizacja |

---

## SEGMENT 2: Vector Databases i Chunking Strategies
**Czas: 0:35 – 1:10 (35 min)**

| Minuty | Zawartość | Format |
|--------|-----------|--------|
| 0:35–0:48 | **Vector databases** — Pinecone vs Qdrant vs PGVector: tabela porównawcza (koszt, latencja, self-host) | Slajd tabela |
| 0:48–0:55 | **Setup Qdrant lokalnie** — Docker w 3 minutach, dashboard, kolekcje | Demo LIVE |
| 0:55–1:05 | **Chunking strategies** — fixed size vs semantic vs hierarchical, wpływ na jakość retrieval | Slajd diagram |
| 1:05–1:10 | **Chunk overlap** — dlaczego 10% overlap ratuje odpowiedzi na granicy chunków | Demo porównawczy |

---

## PRZERWA: 5 minut
**Czas: 1:10 – 1:15**

---

## SEGMENT 3: n8n Vector Store Nodes — Ingestion Pipeline
**Czas: 1:15 – 1:55 (40 min)**

| Minuty | Zawartość | Format |
|--------|-----------|--------|
| 1:15–1:25 | **n8n Vector Store nodes** — Insert, Retrieve, Query: anatomia każdego | Demo n8n |
| 1:25–1:35 | **Ingestion Workflow #1** — Google Drive trigger → parsowanie PDF/DOCX → chunking → embeddings → Qdrant | Demo n8n LIVE |
| 1:35–1:45 | **Metadane w Qdrant** — jak tagować dokumenty (nazwa pliku, data, typ, strona) | Demo n8n |
| 1:45–1:55 | **Incremental updates** — jak aktualizować bazę bez przebudowy, hash dokumentu, wersjonowanie | Demo n8n |

---

## SEGMENT 4: Retrieval i Query Pipeline — jak pobierać właściwe dane
**Czas: 1:55 – 2:25 (30 min)**

| Minuty | Zawartość | Format |
|--------|-----------|--------|
| 1:55–2:05 | **Similarity search** — cosine, dot product, euclidean: kiedy co wybrać | Slajd |
| 2:05–2:12 | **Hybrid search** — semantic + keyword (BM25), dlaczego samo embeddingowe nie zawsze wystarcza | Slajd + demo |
| 2:12–2:18 | **Reranking** — cross-encoder reranker, top-5 → top-1, kiedy warto | Demo n8n |
| 2:18–2:25 | **Query Workflow #2** — Webhook/Slack → embed pytanie → retrieval → AI z cytatami → odpowiedź | Demo n8n LIVE |

---

## SEGMENT 5: Eliminacja Halucynacji + Ewaluacja RAG
**Czas: 2:25 – 2:55 (30 min)**

| Minuty | Zawartość | Format |
|--------|-----------|--------|
| 2:25–2:33 | **Source citations** — jak zmusić AI do cytowania źródeł (prompt + structured output) | Demo n8n |
| 2:33–2:40 | **Confidence scores i fallback** — "nie wiem" jest lepsze niż zmyślona odpowiedź | Demo n8n |
| 2:40–2:48 | **Ewaluacja RAG** — precision@k, recall@k, RAGAS framework — jak mierzyć czy retrieval działa | Slajd + demo |
| 2:48–2:55 | **Practical optimizations** — embedding model selection (ada-002 vs text-embedding-3-small vs 3-large) + koszt | Slajd tabela |

---

## OUTRO i ćwiczenia
**Czas: 2:55 – 3:00 (5 min)**

| Minuty | Zawartość | Format |
|--------|-----------|--------|
| 2:55–3:00 | **Omówienie ćwiczeń** — setup Qdrant, Knowledge Assistant, zadanie domowe (auto-refresh) + zapowiedź Tygodnia 8 | Kamera na twarz |

---

## Notatki dla reżysera / montażysty

- **Demo kontrastu (Segment 1)** — nagrywać obie wersje (bez/z RAG) bez cięcia — różnica musi być widoczna i uderzająca
- **Segment 3 Ingestion LIVE** — przygotować folder Drive z 5 dokumentami testowymi (regulamin, oferta, FAQ, cennik, onboarding)
- **Segment 4 Query LIVE** — pytanie testowe: "Jakie są warunki płatności w umowie z klientem X?" — powinno zwrócić cytat z PDF
- **Slajdy wizualizacja embeddingów** — użyć scatter plot 2D z t-SNE, podobne zdania = blisko siebie (zrzut z OpenAI Embedding Visualizer)
- **Lower thirds** przy każdym nowym pojęciu: RAG, Embedding, Vector DB, Chunk, Cosine Similarity, Reranker
- **Timestamp chapters** do opisu na platformie kursowej zgodnie z agendą

---

## Materiały do przygotowania przed nagraniem

- [ ] n8n z nodes: Vector Store (Qdrant), Embeddings (OpenAI), AI Agent, HTTP Request, Google Drive
- [ ] Qdrant uruchomiony lokalnie via Docker (`docker run -p 6333:6333 qdrant/qdrant`)
- [ ] Klucz API OpenAI (embeddings: text-embedding-3-small + GPT-4o do generation)
- [ ] Google Drive folder "Demo_Firmowa_Wiedza" z 5 dokumentami (PDF + DOCX)
- [ ] Slack App z scope `chat:write` do prezentacji odpowiedzi z cytatami
- [ ] Przygotowane pytania testowe z oczekiwanymi odpowiedziami do demo ewaluacji
- [ ] Środowisko testowe — oddzielna kolekcja Qdrant "demo_kurs" (nie production)
