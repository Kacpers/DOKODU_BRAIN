---
type: kurs-materialy
modul: 03
tytuł: "Tydzień 3: Skalowalność, Odporność i Disaster Prevention"
czas_total: 4h
status: draft
last_reviewed: 2026-03-27
---

# Tydzień 3: Skalowalność, Odporność i Disaster Prevention
## Plan nagrania — 4 godziny materiału

> **Uwaga produkcyjna:** Moduł 4h wymaga podziału na dwie sesje nagraniowe (2h + 2h) z przerwą. Przed nagraniem: zamknij wszystkie niepotrzebne aplikacje, przygotuj n8n z działającym ngrok/webhook, sprawdź połączenie z Slackiem i Sheets.

---

## SESJA 1 (2h) — Teoria + Podstawy Odporności

### Segment 1: Otwarcie i Kontekst (15 min)
**Format:** Kamera + slajdy
- Intro: dlaczego 80% workflow produkcyjnych pada po 3 miesiącach
- Analogia do budowania mostu — zakładasz że się posypie
- Przegląd tygodnia: co zbudujesz (Armored Invoicing System)
- Demonstracja: pokaż crash zwykłego workflow bez error handling (live demo)

### Segment 2: Batching — SplitInBatches (20 min)
**Format:** Slajdy (5 min) + Demo live (15 min)
- Teoria: czym jest batching i kiedy jest niezbędny
- SplitInBatches node — parametry, chunk size, loop mechanics
- **DEMO:** Przetwórz 1000 rekordów z Google Sheets — najpierw bez batching (timeout), potem z batchingiem
- Tipsy: optimal batch size (50–200 rekordów), progress tracking

### Segment 3: Idempotency — Workflow które można uruchomić 2x (20 min)
**Format:** Slajdy (8 min) + Demo live (12 min)
- Teoria: co to jest idempotency i dlaczego webhook może przyjść 2x
- Deduplication keys — strategie (order_id, timestamp+source, hash)
- Diagram: Sprawdź → Wykonaj → Oznacz (flow idempotentny)
- **DEMO:** Webhook przyjmuje to samo zamówienie 2 razy — pokaż co się dzieje bez i z idempotency check
- Narzędzia: Google Sheets jako lock table, Redis, zewnętrzna baza

### Segment 4: Error Trigger Workflow — Globalny Handler Błędów (25 min)
**Format:** Slajdy (10 min) + Demo live (15 min)
- Teoria: architektura "główny workflow + error workflow"
- Konfiguracja Error Trigger node w n8n
- Co powinien robić error workflow: log → alert → ticket
- **DEMO:** Stwórz globalny Error Handler krok po kroku
  - Odczytaj $execution i $workflow z context
  - Wyślij alert Slack z linkiem do wykonania
  - Zapisz do Google Sheets error log
- Pułapka: error workflow też może mieć błąd — zabezpieczenie

### Przerwa (10 min)
> **Marker montażowy:** Wstaw planszę "PRZERWA — wrócimy za chwilę" lub przyspiesz. Na żywo: 10 minut przerwy dla uczestników webinaru.

---

## SESJA 2 (2h) — Retry Logic, Monitoring i Projekt

### Segment 5: Retry Logic z Exponential Backoff (20 min)
**Format:** Slajdy (8 min) + Demo live (12 min)
- Teoria: kiedy retry, kiedy fail fast, kiedy dead letter queue (tabela decyzyjna)
- Retry w n8n: natywny retry w node settings vs custom loop
- Exponential backoff — dlaczego random jitter jest ważny
- **DEMO:** HTTP Request z retry loop — 3 próby, 1s → 2s → 4s czekania
- Wait node: jak używać do scheduled retries

### Segment 6: Wait Node — Pauzy i Scheduled Retries (15 min)
**Format:** Slajdy (5 min) + Demo live (10 min)
- Wait node: typy (fixed, webhook, scheduled)
- Przypadki użycia: czekaj na zatwierdzenie, scheduled retry, rate limiting
- **DEMO:** Workflow z Wait który sprawdza status API co 30 sekund (polling)
- Uwaga na timeouty wykonania w n8n (domyślnie 1h)

### Segment 7: Monitoring — Wiesz że coś się posypało (20 min)
**Format:** Slajdy (8 min) + Demo live (12 min)
- Disaster recovery mindset: zakładasz że coś padnie, pytanie kiedy
- Monitoring w n8n: execution history, failed executions
- Alert email vs Slack — kiedy który
- **DEMO:** Skonfiguruj dzienny digest z licznikiem sukcesów/błędów
  - Cron trigger rano
  - Odczytaj statystyki z n8n API lub external log
  - Wyślij raport emailem

### Segment 8: Logging — Zapisywanie Execution Logs (15 min)
**Format:** Slajdy (5 min) + Demo live (10 min)
- Dlaczego warto logować do zewnętrznej bazy (n8n execution log jest ulotny)
- Struktura logu: timestamp, workflow_name, execution_id, status, error_message, duration_ms
- **DEMO:** Dodaj "logging sub-workflow" wywoływany przez Execute Workflow node
  - Zapisz do Google Sheets / Airtable / Postgres
- Standard Dokodu Logging (nawiązanie do Logging_Standard.md)

### Segment 9: Testing — Jak Testować bez Produkcyjnych Danych (15 min)
**Format:** Slajdy (8 min) + Demo live (7 min)
- Staging vs produkcja w n8n: różne credentials, różne środowiska
- Mock data: jak symulować webhook bez prawdziwego ruchu
- Test cases: happy path, error path, edge cases (null, empty, duplicate)
- **DEMO:** Użyj "Manual Trigger + statyczny JSON" zamiast prawdziwego webhooka

### Segment 10: Projekt — Armored Invoicing System (35 min)
**Format:** Demo live (build step by step)
- Przegląd architektury (slajd 2 min)
- Build: Main Invoicing Workflow
  - Webhook trigger → Idempotency check → Pobierz dane → Generuj fakturę → Wyślij email → Update CRM
- Build: Error Handler dla fakturowania
  - 3x retry z backoffem → Slack alert → Ticket w Sheets
- Build: Batch mode dla 1000 zamówień
  - SplitInBatches → wywołaj sub-workflow per rekord
- Test: pokaż co się dzieje gdy API fakturowe nie odpowiada
- Test: wyślij ten sam webhook 2x — idempotency check działa

### Segment 11: Podsumowanie i Zadanie Domowe (5 min)
**Format:** Kamera
- Recap: 5 zasad armored workflow
- Zadanie domowe: dodaj dzienny raport monitoringowy do swojego Armored Invoicing
- Zapowiedź Tygodnia 4: Architektura Modularna i Sub-workflows

---

## Mapa czasu (summary)

| # | Temat | Czas | Format |
|---|-------|------|--------|
| 1 | Otwarcie + Kontekst | 15 min | Kamera + slajdy |
| 2 | Batching (SplitInBatches) | 20 min | Slajdy + Demo |
| 3 | Idempotency | 20 min | Slajdy + Demo |
| 4 | Error Trigger Workflow | 25 min | Slajdy + Demo |
| — | **PRZERWA** | **10 min** | — |
| 5 | Retry + Exponential Backoff | 20 min | Slajdy + Demo |
| 6 | Wait Node | 15 min | Slajdy + Demo |
| 7 | Monitoring | 20 min | Slajdy + Demo |
| 8 | Logging | 15 min | Slajdy + Demo |
| 9 | Testing + Staging | 15 min | Slajdy + Demo |
| 10 | Projekt: Armored Invoicing | 35 min | Demo |
| 11 | Podsumowanie + HW | 5 min | Kamera |
| **TOTAL** | | **~4h 15 min** | |

> Naddatek 15 min celowy — montaż skróci do 4h.
