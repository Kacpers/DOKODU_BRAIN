---
type: resource
status: active
owner: kacper
created: 2026-04-15
tags: [szkolenia, pain-points, pm, ux, management, jira, sales-intel, workshop-data]
source: warsztat z PM/UX/management (dane zewnętrzne, kontekst Jira, Design System, rekrutacja, PowerBI)
---

# Workshop Intelligence — PM / UX / Management (dane surowe)

> Grupa: Project Managerowie, UX designerzy, managerowie. Kontekst: Jira, Design System, Capex, rekrutacja.
> Kluczowy motyw: trackowanie projektów, dokumentacja, spotkania, walidacja.

---

## Procesy do usprawnienia

### Spotkania & dokumentacja
- Wyszczególnienie kluczowych decyzji, podsumowanie, next stepy
- Redagowanie minutek po spotkaniach
- Akcje po spotkaniach i ich trackowanie
- Podsumowanie spotkań z taskami do zrobienia per osoba
- Formalne dokumenty (np. plan naprawczy)
- Przygotowywanie wzoru dokumentacji do uzupełnienia
- Redagowanie agendy spotkania / planu na narrację
- Generowanie notatek na spotkania cykliczne (statusy, review)
- Tworzenie podsumowań po spotkaniach Z BAZĄ WIEDZY do której zawsze mogę się odnieść, kategoryzowanie spotkań w kontekście jednego tematu = szersza perspektywa

### Analiza & decyzje
- Walidacja koncepcji i łapanie szerszej perspektywy
- Challengowanie wniosków — spojrzenie od innej strony
- Podsumowania dostosowane pod personę (podwładni, management, peers)
- Weryfikacja dokumentów, porównanie, wyszczególnienie najważniejszych aspektów z perspektywy stanowiska
- Copilot w PowerBI
- Analiza wyników ankiet — znajdowanie aspektów które byśmy przeoczyli
- Kontrola opóźnień, blokad i zależności (projektowo)

### UX / Design
- Analizowanie projektów przed handoffem — zgodność z Design Systemem, patterny UX, UX writing
- Wykrywanie braków projektowych

### Operacje / Finanse
- Timesheety godzinowe — zbieranie i pilnowanie wypełnienia
- Automatyczne raporty z podziałem na projekty — ile kto czasu poświęca
- Zbieranie raportów godzinowych do Capex
- Sprawdzenie maili w określonym czasie z określoną nazwą załącznika — agregacja danych + wylistowanie braków (Capex)
- Wyłapywanie aktywności uczestników na spotkaniach

### Zarządzanie
- Agregacja informacji z konta + dzienne taski, ważne maile wymagające odpowiedzi
- Wsparcie w tworzeniu job profile do ogłoszenia rekrutacyjnego
- Koordynacja rekrutacji: 3 źródła CV, 3 zespoły rekrutujące (kalendarz, sloty, rekomendacje)
- Mapowanie wymagań projektowych na taski

### Inne
- Tworzenie tasków w Jirze na podstawie spotkań
- Redagowanie maili
- Walidacja padających propozycji
- Wyszukiwanie benchmarków (ze źródłami do weryfikacji)
- Dobór adekwatnego stylu komunikacji
- Automatyzacje powtarzalnych procesów z agentami
- Opisywanie faktur

---

## Zastosowanie w Dokodu

### Szkolenie
- "AI dla PM-ów" — podsumowania spotkań, Jira automation, Design System review
- "AI w finansach projektowych" — Capex, timesheety, raporty godzinowe
- Baza wiedzy ze spotkań = zaawansowany use case (RAG + kategoryzacja)

### Wdrożenie
- n8n: mail → sprawdź załącznik → aggreguj dane → alert o brakach (Capex use case)
- n8n: spotkanie → transkrypcja → podsumowanie → taski w Jira
- AI agent: Design System compliance checker
