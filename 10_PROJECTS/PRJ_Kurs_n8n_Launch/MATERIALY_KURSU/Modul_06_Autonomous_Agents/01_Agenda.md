---
type: course-module
modul: 06
tytul: "Autonomiczne Agenty AI — MASTERCLASS"
czas_total: "~4 godziny"
segmenty: 9
status: draft
last_reviewed: 2026-03-27
---

# Moduł 06: Autonomiczne Agenty AI — MASTERCLASS
## Plan nagrania (~4 godziny)

---

## SEGMENT 1: Czym naprawdę jest agent AI
**Czas: 20 minut**

### 1.1 Hook i wprowadzenie (5 min)
- Historia "stażysty który nigdy nie śpi"
- Co agent AI potrafi, czego nie potrafi zwykły LLM
- Różnica: chatbot vs agent vs multi-agent system
- Przegląd co zbudujesz w tym tygodniu

### 1.2 Architektura agenta: perception → reasoning → action → memory (15 min)
- Perception: skąd agent bierze dane (email, webhook, baza danych)
- Reasoning: jak LLM decyduje co zrobić (chain-of-thought, ReAct pattern)
- Action: tools — search, scrape, API, subworkflow
- Memory: co agent "pamięta" i po co
- Demo LIVE: agent n8n w akcji (10 sekund do pierwszego rezultatu)

---

## SEGMENT 2: Memory — serce agenta
**Czas: 35 minut**

### 2.1 Dlaczego memory to nie opcja, to konieczność (5 min)
- Demo: agent BEZ memory — "zapomina" po każdym turze
- Demo: agent Z memory — kontekst zachowany
- Kiedy brak memory to błąd krytyczny vs kiedy to OK

### 2.2 Simple Memory (Buffer) (10 min)
- Co to jest: wszystkie wiadomości w jednym bloku
- Zalety: proste, zero konfiguracji
- Wady: token limit, koszt rośnie liniowo
- Konfiguracja w n8n: krok po kroku
- Kiedy używać: krótkie sesje, do ~20 wiadomości

### 2.3 Window Buffer Memory (10 min)
- Mechanizm sliding window — ostatnie N wiadomości
- Trade-off: mniej tokenów vs utrata dalekiego kontekstu
- Konfiguracja: jak dobrać N do use case'a
- Pattern: połączenie z sumaryzacją kontekstu

### 2.4 Vector Store Memory — długoterminowa (10 min)
- Jak działa: embeddingi + similarity search
- Pinecone vs Qdrant: porównanie (cena, setup, prędkość)
- Konfiguracja w n8n: Pinecone node + embedding model
- Use case: agent który "pamięta" klientów z poprzednich tygodni

---

## SEGMENT 3: Internet access — agent który widzi świat
**Czas: 30 minut**

### 3.1 SerpAPI — wyszukiwarka dla agenta (10 min)
- Konfiguracja: API key, limity, koszty
- Integracja z n8n: HTTP Request node + tool definition
- Prompt engineering: jak zapytać agenta by szukał mądrze
- Demo: agent szuka najnowszych newsów o firmie

### 3.2 Firecrawl — scraping stron (10 min)
- Co to jest Firecrawl i dlaczego nie zwykły HTTP
- Konfiguracja: API key, rate limits
- n8n + Firecrawl: workflow krok po kroku
- Use case: agent czyta stronę firmy → wyciąga ofertę

### 3.3 Browserless/Puppeteer dla zaawansowanych (10 min)
- Kiedy Firecrawl nie wystarczy (dynamiczne JS, logowanie)
- Self-hosted vs cloud: kalkulacja kosztów
- n8n → HTTP Request → Browserless: przykładowy workflow
- Pułapki: bot detection, rate limiting, legal (robots.txt)

---

## SEGMENT 4: Structured Output — agent który mówi JSON
**Czas: 25 minut**

### 4.1 Problem: agent pisze co chce (5 min)
- Demo: agent bez struktury — chaos w output
- Dlaczego to problem dla dalszego przetwarzania
- Rozwiązanie: JSON schema + function calling

### 4.2 JSON Schema i Function Calling w n8n (15 min)
- Definiowanie schema: pola, typy, required
- Konfiguracja w n8n: Structured Output Parser
- Walidacja: co zrobić gdy agent nie trzyma się schematu
- Retry pattern: auto-naprawa złego JSONa

### 4.3 Pydantic/Zod dla TypeScript (5 min)
- Kiedy wychodzisz z n8n do kodu
- Schema → validacja → error handling
- Przykład: schema raportu B2B lead analyst

---

## SEGMENT 5: Tool Use Advanced — własne tools jako subworkflows
**Czas: 30 minut**

### 5.1 Czym jest tool z perspektywy LLM (5 min)
- Function calling — agent "wywołuje funkcję"
- n8n tools: wbudowane vs custom
- Kiedy pisać własny tool

### 5.2 Subworkflow jako tool (15 min)
- Architektura: main workflow → tool → subworkflow → result
- Konfiguracja w n8n: "Execute Workflow" node jako tool
- Przekazywanie parametrów: input schema
- Error handling: co gdy subworkflow się sypie

### 5.3 Budowanie biblioteki tools (10 min)
- Zasada: jeden tool = jedna odpowiedzialność
- Nazewnictwo: jak opisywać tools żeby LLM ich dobrze używał
- Testowanie tools niezależnie od agenta
- Demo: biblioteka 4 tools dla B2B analyst (search, scrape, KRS, LinkedIn)

---

## SEGMENT 6: Multi-Agent Systems — orkiestra agentów
**Czas: 35 minut**

### 6.1 Kiedy jeden agent nie wystarczy (5 min)
- Limity single-agent: context window, specialization, równoległość
- Pattern: Supervisor + Workers
- Pattern: Agent chains (pipeline)
- Pattern: Peer agents (współpraca)

### 6.2 Supervisor + Worker Pattern (20 min)
- Rola Supervisora: dekompozycja zadania, delegacja, synteza
- Rola Workerów: specjalizacja, izolowany kontekst
- Implementacja w n8n: Main Agent → Sub-agents via HTTP/Execute Workflow
- System prompts: jak pisać dla Supervisora vs Workera
- Demo LIVE: 3 workery + supervisor — live run

### 6.3 Agent Chains (10 min)
- Sequential processing: wynik agenta 1 → input agenta 2
- Use case: Research Agent → Analysis Agent → Report Agent
- Jak przekazywać kontekst między agentami
- Pułapka: error propagation w chainie

---

## SEGMENT 7: Hallucinations i jakość agenta
**Czas: 25 minut**

### 7.1 Skąd biorą się halucynacje w agentach (8 min)
- LLM "wymyśla" fakty gdy brak danych
- Confidence vs accuracy — nie myl pewności z prawdą
- Kategorie: fakty, liczby, cytaty, adresy
- Demo: agent halucynuje dane o firmie

### 7.2 Jak minimalizować halucynacje (12 min)
- Grounding: wymuszaj cytowanie źródeł
- Verification step: drugi agent sprawdza fakty
- Temperature: 0.0-0.3 dla factual tasks
- Prompt: "Jeśli nie masz danych, napisz BRAK DANYCH"
- Structured output: schema wymusza kompletność
- Confidence score: poproś agenta o ocenę pewności

### 7.3 Ewaluacja agenta — jak mierzyć jakość (5 min)
- Metryki: accuracy, completeness, format compliance
- Test suite: 10 znanych firm → sprawdź ręcznie
- LLM-as-judge: użyj GPT-4o do oceny output innego agenta
- Monitoring w produkcji: log każdy run, track errors

---

## SEGMENT 8: Koszty i optymalizacja
**Czas: 25 minut**

### 8.1 Token counting — ile to naprawdę kosztuje (10 min)
- Jak liczyć tokeny: input + output + system prompt + memory
- Live kalkulator: 100 leadów/dzień × koszt per lead
- Porównanie modeli: GPT-4o vs Claude 3.5 Sonnet vs Gemini 1.5 Pro
- Tabela kosztów przy 1000 wywołań

### 8.2 Strategie optymalizacji (10 min)
- Model routing: GPT-4o do reasoning, GPT-3.5 do prostych tasks
- Prompt compression: mniej tokenów = mniej kosztów
- Caching: Anthropic Prompt Cache (60% oszczędności na system prompt)
- Batch processing: poczekaj i uruchom bulk zamiast jeden po jednym

### 8.3 Monitoring i alerty kosztów (5 min)
- OpenAI/Anthropic: ustawianie limitów wydatków
- n8n: logging kosztu do Google Sheets / bazy danych
- Alert: jeśli koszt > X PLN → stop workflow + powiadomienie

---

## SEGMENT 9: Projekt — B2B Lead Analyst
**Czas: 55 minut**

### 9.1 Architektura projektu (10 min)
- Przegląd całości: trigger → supervisor → 3 workery → output
- Decyzje architektoniczne: dlaczego 3 workery, nie 1
- Co każdy worker robi i dlaczego
- Szacunkowy koszt per analiza

### 9.2 Build LIVE: Sub-agents (25 min)
- Worker 1: Research Faktograficzny — SerpAPI + Firecrawl + KRS
- Worker 2: Analiza ICP Fit — scoring 1-10 z uzasadnieniem
- Worker 3: Rekomendacja Sprzedażowa — pitch + pytania discovery
- System prompts dla każdego workera

### 9.3 Build LIVE: Supervisor + Output (15 min)
- Supervisor Agent: synteza 3 raportów
- Structured output: schema finalnego raportu
- Formatowanie: Markdown raport gotowy do wysłania
- Trigger: email + webhook CRM

### 9.4 Test i weryfikacja (5 min)
- Test na 3 firmach (mała, średnia, enterprise)
- Weryfikacja jakości vs ręczny research
- Co poprawić, co zostawić

---

## Podsumowanie i CTA
**Czas: 5 minut**

- Recap: co zbudowałeś
- Ćwiczenia do samodzielnej pracy
- Zapowiedź Tygodnia 7: RAG — Retrieval Augmented Generation
- Zadanie domowe: integracja z CRM

---

## Notatki produkcyjne

- **Nagraj najpierw** demo live (Segment 9) — to benchmark dla reszty
- **Backup**: przygotuj pre-built workflow na wypadek błędów na żywo
- **Ekran**: IntelliJ + n8n side-by-side dla code segments
- **Thumbnail**: Robot z krawatami zarządzający innymi robotami
- **Timestamp chapters**: każdy segment to osobny chapter w YouTube
