---
type: agenda
status: ready
owner: kacper
last_reviewed: 2026-03-25
tags: [n8n, ai, automatyzacja, m365, szkolenie, agenda, flagship]
---

# Szkolenie: Automatyzacja Procesów Biznesowych (n8n + AI Agenci + Microsoft 365)

**Źródło:** Załącznik nr 1 do umowy Animex (zrealizowane 5 grup × 15 os., marzec 2026)
**Format:** 2 dni × 7h (9:00–16:00, przerwy wliczone)
**Dla kogo:** Działy BOK, Operations, IT, Administracja — pracownicy biurowi i techniczni
**Technologie:** n8n, Microsoft Graph API (Outlook/Teams/SharePoint), Azure OpenAI / Local LLM, SAP (opcja)
**Wynik:** Uczestnicy wychodzą z działającymi automatyzacjami, gotowymi do wdrożenia produkcyjnego
**Cena:** od 8 000 PLN netto / grupa do 15 osób
**Status:** ✅ Zrealizowane 5× | Ocena 4.8/5 | Trener 4.9/5 | 75 uczestników

---

## DZIEŃ 1 — Fundamenty Automatyzacji i Optymalizacja Pracy Biurowej

### Moduł 1: Wstęp do platformy n8n i mapa procesów
**Realizowane workflow:** "Hello Teams" — pierwsze połączenie z komunikatorem M365

- Analiza specyfiki pracy grupy (wstęp diagnostyczny)
- Architektura n8n: interfejs, węzły (Nodes), połączenia, credentials
- Jak identyfikować zadania do automatyzacji — "Mapa Oszczędności Czasu"
- Tworzenie pierwszego workflow krok po kroku
- Integracja z Microsoft Teams — wysłanie pierwszej wiadomości

### Moduł 2: Inteligentna Skrzynka Odbiorcza — Auto-CRM i Dokumenty
**Realizowany workflow:** "Lead Capture" — wyłapanie maila, deduplikacja, zapis do Excel/SharePoint

- Integracja z Microsoft Outlook — monitorowanie skrzynki, filtrowanie
- Zarządzanie danymi: zapisywanie z maili do Excel Online / SharePoint Lists
- Generowanie dokumentów tekstowych na podstawie danych z maila
- Logika IF / Merge — obsługa duplikatów i warunków
- Tworzenie notatek na SharePoint automatycznie

### Moduł 3: Raportowanie Cykliczne i Integracja z BI
**Realizowany workflow:** "Poranny Raport Managerski" — automat agreguje statusy → Teams

- Triggery czasowe (Cron) — harmonogramowanie zadań cyklicznych
- Agregacja danych z wielu źródeł w jednym miejscu
- Przygotowanie danych pod import do Power BI (struktura danych)
- Zbiorcze podsumowanie wysyłane o ustalonej godzinie

### Moduł 4: Interaktywne Procesy Decyzyjne i Webhooki
**Realizowany workflow:** "Obieg Akceptacji" — formularz Zatwierdź/Odrzuć w Teams/Slack

- Logika biznesowa: warunki i rozgałęzienia procesu
- Wysyłanie danych na zewnątrz przez webhooki
- Komunikacja między systemami (webhook → n8n → webhook)
- Interaktywny formularz decyzji dla przełożonego

---

## DZIEŃ 2 — Agenci AI, SAP i Bezpieczeństwo Danych

### Moduł 5: Wdrożenie Agentów AI — Teoria i Praktyka
**Realizowany workflow:** "Osobisty Asystent" — agent AI z dostępem do kalendarza i maila

- Fundamenty AI: tradycyjny chatbot vs. inteligentny agent (autonomia, narzędzia)
- Przegląd zastosowań: HR, Sprzedaż, Finanse, Administracja
- Narzędzia agenta (Tools): Calendar, Email, HTTP Request, Internet
- Agent rozumiejący język naturalny → akcje w kalendarzu
- Multi-agent pipeline: zbieranie → przetwarzanie → raportowanie

### Moduł 6: Integracja Enterprise — System SAP
**Realizowany workflow:** "Weryfikator Kontrahenta" — NIP z Teams → SAP → status faktur

- Łączenie systemów przez HTTP Request (REST API)
- Komunikacja z SAP/ERP — pobieranie danych o kontrahentach i zamówieniach
- Symulacja lub środowisko testowe SAP (zależnie od klienta)
- Weryfikacja statusu płatności w czasie rzeczywistym

### Moduł 7: Bezpieczeństwo, DevOps i Lokalne AI
**Realizowany workflow:** "Bezpieczny Analizator Umów" — PDF z danymi wrażliwymi → local LLM

- DevOps w n8n: wersjonowanie, tagowanie workflowów, Error Handling
- Zarządzanie danymi wrażliwymi: bezpieczne przechowywanie credentials
- Lokalne AI (Privacy First): Ollama — dane nie wychodzą do chmury
- Przetwarzanie dokumentów PDF bez wysyłania do Azure/OpenAI

### Moduł 8: Warsztat Praktyczny — Własny Proces
**Finał szkolenia:** Uczestnicy budują i prezentują własne rozwiązanie

- Praca własna: uczestnicy wybierają realny problem ze swojej pracy
- Konsultacje 1:1 z trenerem przy budowie logiki
- Prezentacja rozwiązań na forum grupy
- Plan wdrożenia na tydzień po szkoleniu

---

## Informacje organizacyjne

**Wymagania wstępne:** Brak — szkolenie no-code, dostępne dla każdego pracownika biurowego
**Środowisko:** Instancja n8n udostępniana przez Dokodu (osobne konta dla uczestników)
**Materiały:** PDF z agendą + gotowe JSON workflows do importu
**Wsparcie po szkoleniu:** 30 dni kanału Q&A
**Integracje:** Dostosowywane do ekosystemu klienta (M365 / Google / Inne)
