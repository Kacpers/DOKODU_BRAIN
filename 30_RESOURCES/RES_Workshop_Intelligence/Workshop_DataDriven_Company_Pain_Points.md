---
type: resource
status: active
owner: kacper
created: 2026-04-15
tags: [szkolenia, pain-points, data-driven, ecommerce, retail, sales-intel, workshop-data]
source: warsztat z firmą data-driven (dane zewnętrzne, prawdopodobnie retail/ecommerce — kontekst PUCCINI, GS1, sklepy, NPI)
---

# Workshop Intelligence — Firma data-driven / retail (dane surowe)

> Surowe odpowiedzi uczestników. Firma z kontekstem retail/ecommerce (marka PUCCINI, sklepy, NPI, GS1).
> Grupa bardziej techniczna niż typowi managerowie — mówią o PBI, DAX, SQL, API, data pipelines.
> Uczestnicy: Marcin, Magda SH, Damian Z, Agnieszka M, Sebastian, Agnieszka B, Marzena S, BZ, Agnieszka A, Karol, Ola O., Ola L, Daniel, Łukasz, Artur Woźny
> Prowadzący: Alek + Michał. Format: 8-16, dużo przerw, spokojne tempo, "Jesteśmy tu dla Was".
>
> **UPDATE 2026-04-15 (druga edycja):** Nowe elementy:
> - voice-to-tasks: "mówienie i przetwarzanie na zapis i zadania (pomysły w sposób zorganizowany)"
> - "Wielu agentów na rynku — który wybrać do jakich zadań?"
> - GEO/AIO awareness: "Pisanie tekstów idealnych pod LLM (w tym AIO)"
> - GEO use case: "jak sprawić, że PUCCINI będzie najczęściej sugerowaną marką na konkretne zapytania"

---

## Co ich frustruje / zabiera czas (bez AI)

### Analityka / BI / Dane
- Tworzenie raportów bez konieczności zlecania zadania — "rozmowa o wyniku z czatem jak z modelem językowym"
- Pisanie ad hoc kodu w M (Power Query) / DAX / SQL
- Odpytywanie baz danych
- Ściąganie danych po API z PBI i walidowanie sum vs query z SQL
- Walidacja danych BI — testowanie, flow do dynamicznej walidacji, alertowanie o brakach
- Walidacja danych między systemami
- Weryfikacja poprawności danych w BI oraz SQL Serverze
- Pilnowanie zgodności danych w różnych raportach
- Analiza anomalii na kontach (saldo a nie powinno być, zapis nie po tej stronie)
- Analiza wyników i wnioski biznesowe
- Określanie wąskich gardeł w procesach i zakładanie walidatorów

### Sprzedaż / Commercial
- Monitorowanie sprzedaży i wyłapywanie szans (trendujący produkt, zbliżające się niedostępności)
- Na bieżąco wyłapywanie anomalii w sprzedaży, stocku
- Wskazywanie obszarów wymagających decyzji (spadek sprzedaży, wolna rotacja, out of stock)
- Analiza sprzedaży i generowanie wniosków do dalszego pogłębienia
- Rozliczanie efektów — realizacja targetów, analiza składowych (średnie ceny, średni paragon, efektywność kampanii, efektywność sklepów/sprzedawców)
- Analiza wyników pod kątem zagrożeń (sklep odbiega od średniej) i szans (nowy bestseller) → alert + działanie
- Obliczanie ilości do zamówień, forecast
- Przygotowanie trade plan — gotowy plan na miesiąc na podstawie wytycznych
- Estymacje ilościowe zakupów, wizualizacje produktowe
- Modelowanie biznesu — szukanie zależności i prawidłowości czyniących biznes "sterowalnym, powtarzalnym"

### Supply chain / Logistyka
- Weryfikacja złożonych zamówień — ilości, timing produkcyjny, zasadność
- Poszukiwanie optymalizacji procesów logistycznych
- Przyspieszenie kalkulacji (ceny sprzedaży w oparciu o koszty transportu, cła)
- Wyznaczanie cen dla produktu
- Określanie i monitoring harmonogramów — np. w NPI

### Finanse / Księgowość
- Raporty płatności — bardzo duża różnorodność, różne formaty, różne dane od operatorów
- Przekazywanie faktur do rozliczenia
- Opisywanie faktur do rozliczenia
- Codzienne przygotowywanie przelewów, płatności
- Pilnowanie terminów zamknięcia miesiąca/roku
- Pilnowanie czy wszystkie koszty wpłynęły do księgowania
- Prowadzenie dochodzeń bo faktury są błędnie opisane, brak szczegółów
- Analiza księgowań i dokumentacji finansowej
- Planowanie cash flow w organizacji
- Raportowanie np. do GS1

### Marketing / E-commerce
- Tworzenie harmonogramu tematów na bloga, koncepcja i struktura wpisów, dobór fraz
- Tworzenie konceptu newslettera na podstawie slotu promocyjnego / danych sprzedażowych
- Bieżąca analiza sprzedaży, cyklu życia klienta, współkupowania → workflow marketing automation
- Schemat poruszania się klientów na stronie sklepu (co klikają, czemu nie konwertują)
- Research rynkowy — konkurencyjne marki, kierunki rozwoju, nowe współprace, konkursy, loterie
- Monitorowanie konkurencji (ceny, akcje marketingowe)
- Wyszukiwanie nowych fraz do pozyskiwania ruchu
- Pisanie tekstów idealnych pod LLM (w tym AIO)
- "Jak sprawić, że PUCCINI będzie najczęściej sugerowaną marką na konkretne zapytania"
- Więcej kontentu wysokiej jakości w korelacji z założeniami
- Trendwatching

### Produkt / R&D
- Praca nad produktem — szukanie kontekstów podróżowania, definiowanie problemów i potrzeb klientów
- Tworzenie założeń produktowych
- Inspiracja przy kreowaniu nowych produktów
- Tworzenie specyfikacji dla produktów
- Tworzenie projektów graficznych z użyciem zdjęć produktowych + wymiary + logotypy klientów
- Dodawanie swatchy i opisywanie struktury materiałów

### Operacje / Zarządzanie
- Podsumowanie spotkań — postanowienia, kolejne kroki, przypisane zadania (x5 powtórzeń!)
- Odpowiedzi na maile, podsumowania (x3)
- Pilnowanie listy zadań, rozliczanie czasu (x3)
- Tworzenie list to-do, przypomnienia o terminach
- Dzielenie zadań na etapy i priorytetyzacja
- Organizacja procesów, planowanie
- Harmonogramowanie zadań
- Bieżący monitoring wykonania zadań/projektów, sprawdzanie postępu, co wymaga decyzji
- Upominanie o dostarczenie kosztów, odpowiedź na maila, umowy — "automat który pilnuje tego za mnie"
- Pytanie współpracowników z poza działu o status zadań
- Pisanie briefów (do projektów, kampanii)
- Pisanie długich technicznych emaili odzwierciedlających specyfikę przedsiębiorstwa
- Pisanie dokumentacji wewnętrznej
- Tworzenie baz klientów z informacjami kontaktowymi — legit data, osoby decyzyjne
- Podsumowania dużych dokumentów, pism, instrukcji

### Prawo / Compliance / BHP
- Wprowadzanie zapytań od strony prawnej w obszarze BHP i Ochrony środowiska
- Analiza aspektów prawnych
- Niezgodne z przepisami odpowiedzi, brak wiary bez wiedzy eksperckiej
- Ocena bezpieczeństwa rozwiązania
- Pisanie polis

### IT / Infrastruktura
- Tworzenie CRUDów w Pythonie do wrzucania danych do SQL
- Pisanie data pipelines
- Poszukiwanie nowych rozwiązań, R&D
- Rozwijanie infrastruktury sieciowej
- Walidacja możliwości usług i narzędzi (bez przeglądania dokumentacji)
- Definiowanie i budowanie nowych procesów
- Usprawnianie procesów operacyjnych — wykrywanie obszarów do automatyzacji
- Sprawdzanie jak coś można wykonać w systemach
- Automatyzacja procesów

---

## Problemy z AI (bariery adopcji)

### Halucynacje / Zaufanie (DOMINUJĄCY PROBLEM)
- "analiza wyników i BŁĘDNE wnioski lub niepewność w decyzjach"
- "brak weryfikacji wypluwanych danych — tworzenie baz danych z bullshit data"
- "fałszywe dane, zmyślone informacje, błędne wnioskowania, niepoprawne formuły"
- "niepotwierdzone dane, sprzeczność informacji"
- "niezgodne z przepisami odpowiedzi, brak wiary bez wiedzy eksperckiej"
- "Stare dane, konieczność prostowania oczywistych błędów, brak wiedzy z jakich lat dane"
- "niedopasowanie odpowiedzi, wymyślanie nieprawdziwych odpowiedzi"
- "weryfikacja poprawności danych otrzymywanych z AI"
- "sprawdzanie poprawności funkcji i formuł użytych w zapytaniu — kontekst ich użycia i poprawność"

### Gubienie kontekstu
- "Gubienie wątku — przy kolejnych zapytaniach AI gubi fragment wcześniejszego rozwiązania lub go modyfikuje"
- "Zapominanie wcześniejszych wytycznych lub wręcz przeciwnie — kurczowe trzymanie się myśli mimo zmiany koncepcji"
- "gubienie kontekstu, promptowanie, za dużo ogólności"

### Jakość outputu
- "Oklepane i banalne copy"
- "Zbyt pobieżna analiza (mało wniosków) za to dużo treści do przeskrolowania"
- "Im bardziej rozbudowany prompt tym gorszy wynik"
- "niezrozumienie, generowanie nie tego o co dokładnie prosimy, nie zwracanie uwagi na szczegóły"
- "Niewłaściwe struktury materiałów produktów na generowanych zdjęciach"
- "nieprawidłowe grafiki generowane na podstawie dokładnych opisów i wymiarów"

### Deterministyczność / Powtarzalność
- "Brak deterministyczności outputu — każdy kod muszę mocno walidować mimo SOTA modeli. Czy warto walidować kilkoma agentami?"
- "Wpływ NASZYCH sugestii na odpowiedzi AI — czy można ograniczyć wpływ sugestii aby wynik odzwierciedlał rzeczywistość?"
- "optymalizacja promptu do poszczególnych modeli AI, praca etapowo nad materiałem"

### Bezpieczeństwo
- "Bezpieczeństwo danych — cloud a on premise"
- "bezpieczeństwo danych, koszt, halucynacje (zwłaszcza przy dłuższym tekście/tłumaczeniu — model sam przełącza język)"
- "Pozyskiwanie nowych źródeł danych — dostawcy, partnerzy, dostępne technologie"

### Meta-problemy
- "Wielu agentów na rynku — który wybrać do jakich zadań?"
- "nieznajomość wykorzystania AI i jego potencjału"
- "Skrócenie czasu nauki AI aby dawał jak najlepsze dane"
- "rozwiązywanie problemów po fakcie, zamiast zapytanie przed działaniem"
- "procesy które robię ręcznie mógłby obsłużyć automatyczny inteligentny workflow"
- "rozproszone narzędzia — przy integracji dają możliwość szybkiego dotarcia do informacji"

---

## Ramy refleksji (szablon — lekko zmodyfikowany vs pierwsza grupa)

1. Jaki problem chcę rozwiązać?
2. Jak to zrobić?
3. Co się udało / co się nie udało?
4. Jakie są z tego wnioski?
5. Jak mogę się tym podzielić z resztą zespołu / organizacji?

---

## Zastosowanie w Dokodu

### Sprzedaż / Outreach do firm retail/ecommerce
- Pitch: "Czy Wasz zespół BI nadal pisze ad-hoc SQL zamiast rozmawiać z danymi?"
- Pitch: "Ile czasu tracicie na walidację danych między PBI a SQL Serverem?"
- Hook na LinkedIn: "Brak deterministyczności AI to #1 problem w firmach data-driven"

### Content (blog / YT)
- "AI w analizie danych — dlaczego halucynuje przy liczbach i jak temu zapobiec"
- "Automatyczny monitoring anomalii sprzedażowych — n8n + AI"
- "Cloud vs on-premise AI — co jest bezpieczniejsze dla Twoich danych firmowych"
- "Jak rozmawiać z danymi bez SQL — AI jako interfejs do BI"

### Szkolenia (design)
- Ta grupa WYMAGA: hands-on z danymi, nie ogólniki
- Pokaż: walidacja outputu AI, multi-agent verification, deterministyczność
- Adresuj: "Im bardziej rozbudowany prompt tym gorszy wynik" — technika chain-of-thought
- Case study: monitoring sprzedaży + alerty przez n8n workflow
