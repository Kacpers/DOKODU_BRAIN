---
type: resource
status: active
owner: kacper
created: 2026-04-15
tags: [szkolenia, pain-points, fotc, it-services, google-workspace, jira, sales-intel, workshop-data]
source: warsztat wewnętrzny firmy IT/services (dane zewnętrzne, kontekst FOTC, Google Workspace, Jira, HubSpot, Pipedrive, eRecruiter)
---

# Workshop Intelligence — Firma IT/Services (FOTC-like) (dane surowe)

> Wewnętrzny warsztat firmy IT/usługowej. Kontekst: Google Workspace, Jira, HubSpot, Pipedrive, SalesForce, n8n.
> Zespoły: Enterprise Sales, Emerging Sales, Emerging CS, Delivery, Growth, Operations, Finance.
> UWAGA: Kontekst "FOTC" — blacklist reference_fotc_blacklist.md. Te dane to intelligence o procesach firm IT/services, NIE kontaktuj FOTC.

---

## BIG BETS (wysoka wartość / trudne)

### Baza wiedzy o kliencie
- Podsumowanie na podstawie danych z CRM, Jiry itp.
- Szukanie klientów — "aktualnie mamy coś w HubSpot, coś w Pipedrive, coś w FOTCnet, coś w Jirze"
- Enterprise Sales, Emerging Sales, Emerging CS

### Baza wiedzy o produktach
- Wyszukiwanie informacji o szkoleniach/produktach, cenniki
- Propozycja oferty na podstawie danych + analiza historii supportu
- Wyszukiwanie info o planach, upgrade, renewal, produktach klienta

### Monitoring statusów projektów
- Analiza statusów zadań, terminów i raportów → podsumowanie
- Zbieranie danych o postępach w Jira / Google Workspace

### Przygotowanie ofert
- Monitorowanie postępu tworzenia i zatwierdzania ofert w Google Docs/Sheets
- Śledzenie terminów w Google Calendar
- Agent skanuje foldery na Google Drive szukając dokumentów ofertowych

### Wycena
- Budowanie diagramów architektury, oferta, harmonogram, zespół
- TL w techu (4-5 osób), w zależności od wyceny: 1-100h

### Fakturowanie (ZŁOŻONY)
- 2 osoby do fakturowania, reselling + usługi własne, 3 spółki
- Kilkanaście "plików" zaciąganych do aplikacji pośredniczącej między CSV a ERP
- Weryfikacja kompletności usług własnych
- Skala: ponad 4000 faktur/miesiąc!
- Pliki importowane nie są gotowcami — trzeba przygotować
- Ręczna weryfikacja pod kątem niestandardowych warunków
- "Potencjał AI widzę raczej w wyłapywaniu braków, reszta to raczej automatyzacje"

### Automatyzacja pozyskiwania leadów
- Outreach klientów, pozyskiwanie danych finansowych
- 3 osoby → docelowo 10 osób
- Sygnały zakupowe, gotowy opis (link do Google Doc)
- "AI first sales → MQL w CRM z opisem, potencjalnymi pain pointami, sales playbookiem"

### Inne BIG BETS
- Algorytm przewidujący opóźnienia płatności na podstawie historycznych zachowań i trendów
- Rozliczanie godzin projektu z Jiry
- Standaryzacja tworzenia automatyzacji w n8n z użyciem AI
- Chatbot / voicebot
- Automatyzacja wyceny migracji
- Obsługa ticketów przez gen AI

---

## QUICK WINS (wysoka wartość / łatwe)

### Spotkania
- Podsumowania spotkań — notatki dla klientów i dokumentacji (8 osób × X/tydzień)
- Podsumowanie statusów projektów (8 osób × 1/tydzień)

### CRM / Growth
- Uzupełnianie danych w CRM — growth team 10 osób, codziennie
- Odszukanie opiekuna organizacji — growth team + inne, 5-25 min codziennie
- Weryfikowanie historii korespondencji z klientem — 10 osób, codziennie, 10-15 min
- Szukanie i weryfikowanie "błędów" w deal w CRM
- Oferta odnowieniowa (bundle) — Growth team 10 osób, codziennie, +/- 10-15 min
- Onboarding nowych klientów (analiza sprzedanych produktów + mail) — 10 osób, co tydzień

### Projekty
- Bieżący stan lejka sprzedażowego — 6 osób, 2x/tydzień
- Zasoby projektowe: planned vs worked vs invoiced — 8 osób, 2x/tydzień + 1 osoba codziennie
- Monitoring spalania budżetów projektów — 8 osób, 2x/tydzień
- Analiza ryzyk projektowych — 1 osoba, codziennie
- Resource planning — przydzielanie ludzi do projektów (TL i PM, min 2 osoby, 1h/tydzień)

### Asystenty AI (propozycje z warsztatu)
- ASYSTENT OFERTOWANIA SZKOLEŃ — 2x/tydzień, 2h/3 osoby. Porównanie potrzeb klienta z dostępnymi agendami.
- ASYSTENT PROPONUJĄCY KOLEJNE USŁUGI NA BAZIE ANKIET — na bazie wyzwań z warsztatów płatnych, zaproponuj kolejne usługi
- ASYSTENT ŁĄCZĄCY KLIENTA Z ODPOWIEDNIM PARTNEREM — 2x/tydzień, 15 min/2 osoby. Katalog partnerski.
- ASYSTENT WYSZUKUJĄCY POTENCJALNYCH NOWYCH PARTNERÓW — 2x/tydzień, 2h/1 osoba. Na bazie NIP/CEIDG sprawdź wartość klienta jako partnera.
- Bot oparty na procedurach — odpowiada działom sprzedaży na powtarzające się pytania

### Inne
- Przygotowywanie i wysyłka raportów rotacji i exit interview (co kwartał, do liderów)
- Proces zamknięcia miesiąca — raporty finansowe i zarządcze
- Porównywanie raportów z uzgodnieniami sald na payroll — 1 osoba, raz/miesiąc
- Szukanie case study i referencji

---

## FILL-INS (niska wartość / łatwe)

- Projektowanie ogłoszeń rekrutacyjnych
- Poszukiwanie informacji na KB o benefitach — 2 osoby na zmianę
- Pisanie feedbacków po rekrutacji do kandydatów
- Onboarding dla zespołu
- Pozyskiwanie tematów do agendy na Leaders Update + wklejenie do prezentacji
- Proces zgłaszania inicjatyw wewnętrznych (kilka razy/miesiąc)
- Postowanie rocznic na kanale czat — 1 osoba, 1x/miesiąc

---

## Inne pomysły z warsztatu

- Automat do analizy zgłoszeń z chatu → tworzenie internalowych projektów/zadań w Jira
- Gemy (Gemini) do usprawnienia tworzenia procesów
- "Usługa admin na godziny z zadaniami obsługiwanymi przez agentów"
- Asystent wspierający tworzenie usług własnych
- Przydzielanie zespołów tech do presales — zbieranie wymagań klienta i kategoryzacja
- Security audit — automatyzacja zadania
- Operation health review — automatyzacja
- Obieg dokumentów zakupowych
- Zbiorcze podsumowanie dłuższych wdrożeń u klienta
- Tworzenie zasobów projektowych w narzędziach
- Generowanie zaległej dokumentacji
- VDR
- Aktualizacja CRM, PA, Jiry
- "Sales play ongoing"

---

## Zastosowanie w Dokodu

### Intelligence o firmach IT/services
- Tak wygląda wewnętrzna kuchnia firmy IT: 4000 faktur/mies., dane w 4 systemach, 10-osobowe teamy sales
- Potwierdza ICP Dokodu: rozproszone narzędzia + brak automatyzacji = ogromna strata czasu
- "AI first sales → MQL w CRM" = dokładnie to co Kacper buduje w n8n

### Potencjał produktowy
- "Asystent ofertowania szkoleń" — to jest usługa którą Dokodu mógłby oferować!
- "Bot na procedurach" — klasyczny use case n8n + RAG
- "Monitoring spalania budżetów" — n8n + Jira API + alerty

### Content
- "Dlaczego Twoja firma IT ma dane w 4 systemach i nikt tego nie ogarnia"
- "4000 faktur miesięcznie — jak AI wyłapuje braki których ludzie nie widzą"
- "AI first sales — jak zbudować pipeline leadów z sygnałami zakupowymi"
