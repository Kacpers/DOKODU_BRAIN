---
type: kurs-agenda
modul: 04
tytul: "Architektura Modularna — Koniec z Chaosem"
czas_total: "~3h 00min"
prowadzacy: Kacper Sieradziński
last_updated: 2026-03-27
---

# Moduł 4: Architektura Modularna — Koniec z Chaosem
## Plan nagrania (~3 godziny)

---

## SEGMENT 1 — Diagnoza problemu (35 min)

### 1.1 Intro + problem "spaghetti workflow" (10 min)
- Przywitanie, co dziś zbudujemy
- Demo: pokaz monolitycznego workflow z ~30 nodami — trudno czytać, trudno debugować
- Pytanie do widza: "Czy twój workflow wygląda tak po miesiącu?"
- Analogia: kod bez funkcji vs kod z funkcjami — każdy programista to wie

### 1.2 Dlaczego monolity są złe (10 min)
- Niemożliwość ponownego użycia: copy-paste logiki = błędy i rozbieżności
- Trudny debugging: gdzie jest błąd w 40-nodowym potworze?
- Brak testowania: nie możesz uruchomić jednej części bez całości
- Problem skali: 5 workflow po 30 nodów = katastrofa zarządzania
- Onboarding: nowy współpracownik widzi workflow i... nie rozumie nic

### 1.3 Architektura modularna — filozofia (15 min)
- Zasada Single Responsibility: jeden workflow = jedna odpowiedzialność
- Zasada DRY w n8n: Don't Repeat Yourself
- Master Workflow pattern: orchestrator + wykonawcy
- Analogia orkiestry: dyrygent (master) vs muzycy (subworkflowy)
- Diagram: jak dane płyną między workflowami
- Kiedy modularyzować? Heurystyki decyzyjne

---

## SEGMENT 2 — Narzędzia architektury (50 min)

### 2.1 Execute Workflow node — demo (20 min)
- Gdzie go znaleźć w n8n
- Parametry: Workflow ID, tryb synchroniczny vs asynchroniczny
- Przekazywanie danych: input JSON → subworkflow
- Odbieranie wyniku: co zwraca subworkflow
- Obsługa błędów z subworkflow
- DEMO NA ŻYWO: prosty master → subworkflow ping-pong

### 2.2 Subworkflows jako funkcje (15 min)
- Trigger: "When Called by Another Workflow"
- Input contracts: definiowanie co przyjmujemy
- Output contracts: definiowanie co zwracamy
- Return node: jak odesłać dane do mastera
- Przykład: subworkflow "Wyślij email z potwierdzeniem" — przyjmuje dane, wysyła, zwraca status

### 2.3 Switch node i intelligent routing (15 min)
- Switch vs If — kiedy co używać
- Routing według wartości pola
- Fallback (default) — zawsze go ustawiaj
- Multi-output: jeden input → do 5+ ścieżek
- Przykład: klasyfikacja zgłoszeń IT/HR/Finance/Sales/Other

---

## SEGMENT 3 — Organizacja i konwencje (30 min)

### 3.1 Naming conventions — konkretne zasady (10 min)
- Konwencja nazewnictwa workflow
- Konwencja nazewnictwa nodów
- Tagging: środowiska, obszary, wersje
- Co NIE robić (anty-wzorce)

### 3.2 Folder structure w n8n (10 min)
- Jak organizować dziesiątki workflow
- Rekomendowana struktura folderów
- Oddzielanie: produkcja / staging / testy
- Archiwum nieaktywnych workflow

### 3.3 Wersjonowanie i backup (10 min)
- Tagi wersji w n8n
- Historia zmian — jak z niej korzystać
- Eksport JSON jako backup
- Git integration (dla zaawansowanych)
- n8n Variables: shared credentials i zmienne środowiskowe

---

## PRZERWA (5 min)

---

## SEGMENT 4 — Projekt tygodnia: Corporate Request Router (55 min)

### 4.1 Omówienie architektury projektu (10 min)
- Diagram całego systemu
- Master workflow: co robi
- 5 subworkflowów: co robi każdy
- Input/output contracts dla każdej ścieżki
- Testowanie: jak weryfikować poprawność

### 4.2 Budowa Master Workflow (20 min)
- Trigger: email / formularz
- AI node: klasyfikacja kategorii
- Switch node: routing do 5 ścieżek
- Execute Workflow dla każdej gałęzi
- Merge wyników + wysyłka potwierdzenia

### 4.3 Budowa subworkflowów (20 min)
- IT Support subworkflow (Jira + email)
- HR subworkflow (Google Sheets + email)
- Finance + Sales subworkflows (szkic)
- Other / Human Review Queue
- Return contracts — co zwracamy do mastera

### 4.4 Testy end-to-end (5 min)
- Test każdej ścieżki osobno
- Test mastera z prawdziwymi danymi
- Weryfikacja potwierdzeń emailowych

---

## SEGMENT 5 — Ćwiczenia i podsumowanie (25 min)

### 5.1 Ćwiczenie 1: Refaktoryzacja Lead Capture (5 min omówienie)
- Zadanie: podziel monolityczny workflow z Tygodnia 1 na master + subworkflows
- Wskazówki
- Czego szukamy w wyniku

### 5.2 Ćwiczenie 2: Request Router — samodzielna budowa (5 min omówienie)
- Zadanie: odtwórz projekt tygodnia samodzielnie
- Kolejność budowania
- Punkty kontrolne

### 5.3 Zadanie domowe (5 min)
- Dodaj 7. kategorię "Urgent" z SMS alertem przez Twilio
- Wskazówka: gdzie w architekturze to dodać
- Gdzie szukać dokumentacji Twilio w n8n

### 5.4 Podsumowanie modułu (10 min)
- 5 kluczowych zasad architektury modularnej
- Checklista przed publikacją workflow
- Zapowiedź Modułu 5: AI + Human in the Loop
- CTA: zadanie domowe, komentarze, pytania

---

## Notatki produkcyjne

| Element | Szczegóły |
|---|---|
| Ekran do nagrania | n8n UI + VS Code (JSON contracts) |
| Slajdy | Segment 1, 3, 5 |
| Demo na żywo | Segment 2, 4 |
| Pliki do przygotowania | Starter workflow (monolith) gotowy do refaktoryzacji |
| B-roll sugestia | Diagram whiteboard architektury |
| Długość docelowa | 175–185 min |
