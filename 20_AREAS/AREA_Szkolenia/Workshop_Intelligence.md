---
type: knowledge_base
status: active
owner: kacper
last_reviewed: 2026-04-29
tags: [szkolenia, workshop, audience, patterns, insights, content-ideas]
---

# Workshop Intelligence

> **Co to jest:** Anonimizowana baza wzorców bólów, use case'ów i pomysłów zebranych podczas warsztatów AI z klientami. **Bez imion, bez nazw firm, bez cytatów dosłownych** — tylko patterns i statystyki.
>
> **Po co:** Materiał do postów LinkedIn, blogów, ofert, produktów, positioning. Każdy warsztat = darmowy market research dla Dokodu.
>
> **Zasada:** Wzorce pojawiające się w 2+ warsztatach dostają priorytet — to znak rynkowy, nie pojedynczy szum.

---

## Meta-wzorce (powtarzalne między warsztatami)

### Top 5 bólów w pracy z AI (ranking zbiorczy)
1. **Halucynacje + brak transparentności** — AI zmyśla zamiast powiedzieć "nie umiem". Pojawia się w **każdym** warsztacie jako #1 lub #2 ból.
2. **Gubienie kontekstu / zapominanie wytycznych** — w dłuższych konwersacjach AI gubi fragmenty wcześniejszych ustaleń lub kurczowo trzyma się starej koncepcji.
3. **Sycophancy / wpływ sugestii użytkownika** — AI przytakuje, wymusza zadowolenie, odpowiedź odzwierciedla sugestię zamiast rzeczywistości.
4. **Brak centralnego ToV i Gemów na zespół** — każdy konfiguruje solo, nie ma wspólnego standardu.
5. **Walidacja outputu wymaga wiedzy eksperckiej** — użytkownik nie wie, czy AI mówi prawdę, bo nie zna dziedziny.

### Top 5 powtarzalnych use case'ów (cross-branżowe)
1. **Podsumowania spotkań + follow-upy + zadania** (dominujący use case)
2. **Automatyzacja raportów i analiz** (wnioski biznesowe, anomalie, alerty)
3. **Email writing** (długie, techniczne, w stylu użytkownika)
4. **Content ops** (oferty, onepagery, newslettery, LP, bannery)
5. **Research** (rynkowy, konkurencji, nowych szans biznesowych)

---

## Warsztat #1 — marketing/sales/CS w B2B (2026-04-21, 8 osób)

**Kontekst:** zespół marketing + sprzedaż + CS, stack Workspace + Gemini + marketing automation.

### Pain pointy
- Halucynacje + brak transparentności (dominujący ból, 3/8)
- Sycophancy kosztem logiki
- Brak centralnego ToV/Gemów dla zespołu — każdy marketer konfiguruje solo
- Ograniczenia Workspace/Gemini: brak tłumaczenia Slides, brak kontroli fontu w Docs, brak flow źródło→docs→sheets→prez, literówki w NotebookLM
- Tool limitation masking — AI halucynuje obejścia w marketing automation zamiast powiedzieć "tego nie da się zrobić"
- Poprawianie całego tekstu przy prośbie o drobną zmianę
- Brak możliwości udostępnienia całego chatu innym w zespole

### Use cases (quick wins)
- Podsumowania spotkań + follow-up emaile
- Transkrypcje webinarów
- Przygotowywanie ofert + komunikacja wokół
- Onepagery i prezentacje BOFU
- Bannery reklamowe w 20 formatach
- Automatyzacje email marketing (szablony, tytuły, tagi, segmenty, flow)
- Rewriting pod brand voice firmy
- Segmentacja klientów do akcji (konferencje, nowe produkty, upsell)
- LP z Figma exportu
- Tłumaczenia EN/RO/HU
- Copy pod social/newsletter/LP
- Brainstorm tytułów eventów

### Big bets
- Weryfikacja projektów marketingowych pod kątem strategii
- Customer Education dopasowane do indywidualnych potrzeb klienta
- Channel Partnerships w istniejącym kliencie

---

## Warsztat #2 — zespół mieszany w retail/e-commerce (2026-04-21, 15 osób)

**Kontekst:** duża grupa, role: BI/analytics, finanse/księgowość, e-commerce, marketing, IT, legal/BHP. Branża: retail/e-commerce (perfumy/kosmetyki). Stack: BI, SQL, Excel/Power Query/DAX, Python, cloud vs on-premise.

### Pain pointy
- **Halucynacje i zmyślone dane** — tworzenie baz z "bullshit data", niepotwierdzone dane, sprzeczność informacji
- **Gubienie kontekstu** w dłuższych konwersacjach — AI modyfikuje wcześniej ustalone rozwiązania przy kolejnych zapytaniach
- **Wpływ sugestii użytkownika na output** — echo chamber, AI potwierdza zamiast weryfikować
- **Brak deterministyczności** — każdy kod od AI wymaga walidacji, nawet z SOTA modelami
- **"Im bardziej rozbudowany prompt, tym gorszy wynik"** — nieliniowa relacja jakości prompta i outputu
- **Bezpieczeństwo danych** — niepewność cloud vs on-premise, zwłaszcza dla danych finansowych
- **Stare/nieaktualne dane** — konieczność prostowania oczywistych błędów, nieznajomość dat źródłowych
- **Nieznajomość potencjału AI w zespole** — zespół nie wie co da się automatyzować
- **Wybór agenta** — "którego agenta do jakiego zadania?"
- **Nieprawidłowe grafiki** mimo dokładnych opisów i wymiarów — struktury materiałów, wymiary produktów
- **Oklepane i banalne copy** + pobieżna analiza z dużą ilością treści do skrolowania
- **Niezgodne z przepisami odpowiedzi** — brak wiary w output bez wiedzy eksperckiej (legal, BHP, ochrona środowiska)
- **Czas promptowania** — za dużo ogólności, brak jasnej metody budowania kontekstu

### Use cases — FINANSE/KSIĘGOWOŚĆ
- Raporty płatności (różne formaty od różnych operatorów)
- Przekazywanie i opisywanie faktur do rozliczenia
- Dochodzenia przy błędnie opisanych fakturach — analiza merytoryczna okresu
- Analiza anomalii na kontach (saldo niezgodne, zapisy po złej stronie)
- Planowanie cash flow w organizacji
- Pilnowanie zamknięcia miesiąca/roku — kto zatwierdza dokumenty, terminy FS, potwierdzenia
- Analiza księgowań i dokumentacji finansowej
- Przygotowywanie przelewów i płatności codziennie

### Use cases — SPRZEDAŻ/RETAIL
- Monitorowanie sprzedaży, wyłapywanie szans (trendujące produkty, zbliżające się out of stock)
- Forecast ilościowy zakupów
- Analiza anomalii w sprzedaży/stocku (wynik sklepu odbiega od średniej)
- Realizacja targetów — składowe wpływające na wynik (średnie ceny, paragon, efektywność kampanii/sklepów)
- Analiza sprzedaży i wnioski do pogłębienia
- Cykl życia klienta, współkupowania — workflow do marketing automation
- Research rynkowy, monitoring konkurencji (ceny, akcje, nowe współprace, udział w loteriach)
- Trendwatching
- Kalkulacje cen sprzedaży (koszty transportu, cła)
- Wskazywanie obszarów wymagających decyzji (spadek sprzedaży, wolna rotacja, out of stock)
- Trade plan — propozycja planu na miesiąc do modyfikacji

### Use cases — OPERACJE/PROCESY
- Organizacja procesów (akceptacja faktur)
- Walidacja danych między systemami
- Podsumowania spotkań — postanowienia, kroki, zadania
- Harmonogramowanie i śledzenie postępów
- Pilnowanie innych działów o terminy mające wpływ na zamknięcie miesiąca
- Briefy do projektów i kampanii
- Dokumentacja wewnętrzna
- Wyznaczanie cen produktu
- Tworzenie list to-do, przypomnień, priorytetyzacja
- Upominanie automatyczne o dostarczenie kosztów/odpowiedzi/umów
- Definiowanie i budowanie nowych procesów
- Tworzenie specyfikacji produktów

### Use cases — DEV/BI
- Ad-hoc kod w M (Power Query) / DAX / SQL
- CRUDy w Pythonie do SQL
- Data pipelines
- Walidacja danych BI — testowanie, flow dynamicznie alertujący
- Odpytywanie baz danych
- Ściąganie danych po API z Power BI i walidacja sum względem "modelowych" query SQL
- Formuły w Excelu
- Weryfikacja poprawności danych w BI i SQL Server

### Use cases — MARKETING/CONTENT
- Harmonogram tematów na bloga
- Koncepcja i struktura wpisu
- Dobór fraz kluczowych + wyszukiwanie nowych fraz
- Newsletter na podstawie slotu promocyjnego / danych sprzedażowych
- Pisanie tekstów pod LLM (w tym AIO / AI Overviews)
- **Jak moja marka ma być częściej sugerowana przez LLM na konkretne zapytania** (GEO/AIO positioning)

### Use cases — GRAFIKA/PRODUKT
- Projekty graficzne z użyciem zdjęć produktowych, wymiarów i logotypów klientów
- Swatche i opisywanie struktury materiałów
- Retusz w programie graficznym gdy AI nie ogarnia

### Use cases — LEGAL/BHP
- Zapytania prawne w obszarze BHP i ochrony środowiska
- Analiza aspektów prawnych
- Pisanie polis
- Podsumowania dużych dokumentów, pism, instrukcji

### Use cases — PRACA WŁASNA
- Speech-to-text — mówienie i przetwarzanie na zapis (pomysły w sposób zorganizowany)
- Pisanie maili biznesowych w stylu użytkownika (ENG) i specyfiki firmy
- Skrócenie czasu nauki AI (ile trzeba "nakarmić" model, żeby dawał dobre dane)

### Big bets
- Określanie wąskich gardeł w procesach i zakładanie na nich walidatorów
- Modelowanie biznesu — szukanie zależności, które pozwalają uczynić biznes "sterowalnym" i powtarzalnym
- Bieżący monitoring + alertowanie kluczowych procesów z rekomendacjami działań
- Research R&D i nowych rozwiązań
- Określanie i monitoring harmonogramów w NPI
- Schemat poruszania się klientów na stronie sklepu (co klikają, czemu nie konwertują)
- Poszukiwanie nowych szans biznesowych (firmy do współpracy, produkty)

### Meta-pytania zespołu
- Jak mogę się tym podzielić z resztą zespołu/organizacji?
- Co się udało / co się nie udało?
- Jaki problem chcę rozwiązać?
- Jak to zrobić?
- Jakie są z tego wnioski?

---

## Warsztat #3 — zespół marketplace/PPC (2026-04-29, ~14 osób, Copilot Studio)

**Kontekst:** zespół specjalistów marketplace + PPC + project management + analytics. Stack: Copilot dominuje (8/14 wymienia jako główne), uzupełnione ChatGPT, Gemini, Claude, n8n, Excel, Power BI, SQL, Python, Allegro Analytics, Perpetua, Redmine. Branża: agencja/zespół obsługujący marketplace (Allegro/Amazon). Tematyka warsztatu: Copilot Studio.

### Profil tooli (sygnał rynkowy)
- **Copilot jako default** — większość zespołu wymienia jako pierwszy lub jedyny LLM
- **Multi-LLM bez konsolidacji** — w jednym zespole działa Copilot + ChatGPT + Gemini + Claude bez wspólnego standardu
- **n8n obecny u 2/14** — nieoczywiste w marketplace, sygnał dla świadomych operatorów
- **Power BI + Excel + SQL trzymają trzon analityki** — Looker tylko jako źródło do wyciągania

### Pain pointy / use cases (klastry)

**1. PPC client onboarding & operations (klaster #1, 5+ wzmianek)**
- Audyt kampanii nowego klienta → dokument gotowy do wysłania
- Setup Google Ads (przede wszystkim setup, nie optymalizacja)
- Analiza raportów PPC + rekomendacje optymalizacji
- Scalanie danych z paneli reklamowych (Excel z różnych źródeł)
- Weryfikacja wyników kampanii

**2. Meeting → zadania → status loop (klaster #2, 4+ wzmianek)**
- Podsumowania spotkań + rozsyłanie podsumowań i zadań
- Sprawdzanie realizacji zadań zgodnie z wcześniejszymi podsumowaniami
- Wyznaczanie kolejnych kroków, podział zadań, timeline
- "Sprytne TODO" — listowanie zadań i delegowanie na Copilot / zespół / siebie
- Statusowanie w Redmine / Planner / Trello + dystrybucja zadań
- Follow-upy

**3. Knowledge management z retirement (klaster #3, 3+ wzmianek)**
- Zarządzanie wiedzą o projekcie: założenia → realizacja → optymalizacja
- Gromadzenie wiedzy, jej odświeżanie, format przechowywania, **retirement**
- Wiedza branżowa vs projektowa vs firmowa — różne cykle życia
- Dokumentacja raportowania i zaszytej logiki biznesowej z różnych źródeł (Redmine/Teams/mail)
- Baza wiedzy jako część workflow analitycznego

**4. Client communication sequences (klaster #4, 3+ wzmianek)**
- Komunikacja mailowa z klientami
- Follow-upy po pierwszej próbie kontaktu, po wysłanej ofercie (sekwencje)
- Przygotowywanie ofert

**5. File-to-structure / data extraction**
- Rozpoznawanie plików PDF → dane ustrukturyzowane
- Pobieranie raportów z zewnętrznych źródeł (np. Looker) na dysk sieciowy
- Integracja z zasobami lokalnymi (Redmine, baza danych, opentranscribe)

**6. Industry news scraping**
- Scraper nowinek PPC z kanałów YouTube w skondensowanej treści
- Nowinki AI / lojalność / programy uruchomione przez konkurencję

**7. Reporting & analytics**
- Analiza raportów Power BI / Excel
- Raporty sprzedażowe + analityka, project management, analiza ofert
- Scenariusze testowe, dokumentacja biznesowa funkcjonalności, harmonogramy
- Raporty finansowe spółki + analizy odchyleń

**8. Sales/finance operations**
- Fakturowanie + windykacja miękka
- Tworzenie plików rozliczeniowych
- Raporty sprzedażowe i mediowe
- Sprawdzanie wystawionej bazy klientów (zgody, warunki)

**9. Team & business operations**
- Rozliczanie celów dla zespołów + cele dla członków zespołu
- Analiza efektów pracy i czasu spędzonego nad obszarami
- Rozliczenia między spółkowe
- Regularne analizy rynku, graczy, klientów

**10. Content & social**
- Generowanie treści do publikacji na LinkedIn
- Przygotowywanie prezentacji z wnioskami
- Prezentacje z analizami

**11. Business development signals**
- Analiza i rekomendacja eventów pod kątem potencjału do pozyskania nowego biznesu

### Big bets
- **Local AI w stacku marketplace** — Redmine + baza danych + opentranscribe lokalnie, zespół świadomie unika cloud
- **Knowledge retirement jako koncepcja** — świadomość że wiedza ma datę wygaśnięcia, rzadko spotykana
- **Orchestrator delegacji zadań** ("sprytne TODO") — codzienny triaż gdzie zadanie powinno trafić: Copilot / ja / zespół

### Meta-sygnały / dilematy zespołu
- **"Power Automate vs Copilot Studio"** — pytanie zadane wprost. Sygnał, że nawet zaawansowany zespół Microsoft nie ma jasności w decyzji narzędziowej.
- **Multi-LLM bez governance** — zespół używa 4 różnych modeli równolegle, bez wskazówki "którego do czego"
- **Marketplace jako branża z niedoborem narzędzi do scalania danych** — Allegro Analytics + Perpetua + panele to manualna sklejka w Excelu

---

## Aktualizacja meta-wzorców (po 3 warsztatach)

### Top use case'y występujące w **każdym** warsztacie (3/3)
1. **Podsumowania spotkań → zadania → follow-up** — uniwersalny, niezależnie od branży i roli
2. **Analizy raportów + wnioski** — finanse, sprzedaż, PPC, BI — różny kontekst, ten sam problem
3. **Pisanie maili + content ops** — oferty, follow-upy, newslettery, LP

### Top pain pointy występujące w **każdym** warsztacie (3/3)
1. **Halucynacje + brak transparentności** (utrzymuje #1)
2. **Multi-LLM/multi-tool chaos bez governance** — w warsztacie #1 to brak Gemów, w #2 wybór agenta, w #3 Power Automate vs Copilot Studio + 4 LLM równolegle

### Nowe wzorce z warsztatu #3 (warte obserwacji w kolejnych)
- **Knowledge retirement** — nikt z poprzednich warsztatów nie nazwał tego wprost
- **Setup nowego klienta jako #1 use case dla agencji PPC/marketplace**
- **Local AI dla danych operacyjnych** — opentranscribe + Redmine + baza, zespół świadomie wybiera offline

---

## Kąty do contentu (LinkedIn, blog)

Wzorce z warsztatów → pomysły na posty/artykuły:

- **"AI, który mówi «nie umiem»"** — Zero-Trust AI positioning, halucynacje vs transparentność
- **"Dlaczego Twój zespół marketingowy potrzebuje wspólnego Gema"** — centralny ToV, koniec solo-konfiguracji
- **"Gdy AI halucynuje obejścia w marketing automation"** — tool limitation masking jako anty-wzorzec
- **"Bullshit data: jak AI tworzy bazy z wymyślonymi danymi"** — walidacja przed zaufaniem
- **"Im dłuższy prompt, tym gorszy wynik — paradoks promptowania"** — kontra-intuicyjna prawda
- **"Echo chamber w chat-GPT: jak Twoje sugestie psują odpowiedzi"** — sycophancy jako ryzyko decyzyjne
- **"Mapa ciepła use case'ów AI w firmie B2B"** — framework quick wins vs big bets
- **"AI dla zamknięcia miesiąca — workflow, który pilnuje terminów za Ciebie"** — finanse
- **"Jak sprawić, żeby Twoja marka była częściej sugerowana przez LLM"** — GEO/AIO positioning
- **"Cloud czy on-premise dla AI w firmie produkcyjnej?"** — bezpieczeństwo danych
- **"Którego agenta do jakiego zadania — decision tree dla zespołu"** — agent selection
- **"Walidacja kodu AI: gdzie jest granica między kosztem a efektywnością?"** — dla tech leaderów
- **"Power Automate vs Copilot Studio — to nie jest ten sam wybór, co Wam się wydaje"** — z warsztatu #3, pytanie wprost
- **"Setup nowego klienta = 80% pracy agencji PPC. Dlaczego nikt tego nie automatyzuje?"** — klaster #1 z warsztatu #3
- **"Wiedza projektowa ma datę wygaśnięcia. Co to znaczy knowledge retirement?"** — koncepcja z warsztatu #3, niszowa ale głęboka
- **"Pętla, która zjada zespołom 6h tygodniowo: spotkanie → zadania → status → przypomnienie"** — występuje w 3/3 warsztatach
- **"Zespół z 4 różnymi LLM bez governance. Klasyczny obraz 2026."** — multi-LLM chaos jako trend
- **"Local AI dla zespołu danych: Redmine + opentranscribe + baza, bez chmury"** — Zero-Trust AI w wersji infra
- **"Scraper nowinek PPC z YouTube — narzędzie, które każdy zespół reklamowy buduje na kolanie"** — niszowo ale konkretnie

---

## Implikacje dla Dokodu (positioning + produkty)

### Potwierdzone twardo
- **Zero-Trust AI** — halucynacje + sycophancy to #1 ból w **każdym** warsztacie. Nie niszowy argument.
- **Content ops w ofercie** — oferty, podsumowania, newslettery, LP, bannery, segmentacja to powtarzalny core.
- **Branże docelowe** — retail/e-commerce (ogromny pakiet use case'ów: trade plan, stock, cycle klienta) i marketing B2B (ToV, content).

### Niedoceniony rynek
- **Centralny ToV + Gemy/GPTs udostępnione zespołowi** — każdy marketer konfiguruje solo, nikt nie robi tego na poziomie firmy.
- **Walidatory na wąskich gardłach procesów** — automatyzacja + kontrola jakości, nie tylko "szybciej".
- **Zamknięcie miesiąca** — twardy, powtarzalny, czasochłonny proces w każdej firmie z księgowością.
- **GEO/AIO positioning** — "jak moja marka ma być sugerowana przez LLM" to rosnące zapytanie.

### Argumenty sprzedażowe
- "Halucynacje + przytakiwanie" → Zero-Trust AI
- "Każdy konfiguruje solo" → Enterprise AI Integration Boutique
- "Walidacja wymaga wiedzy eksperckiej" → wdrożenia z domain experts, nie tylko chatbot
- "Im dłuższy prompt, tym gorszy wynik" → szkolenia z promptowania + biblioteka promptów jako produkt

### Nowe argumenty z warsztatu #3
- **"4 LLM, zero governance"** → produkt: Audyt AI w firmie + standaryzacja narzędzi (przed wdrożeniem czegokolwiek)
- **"Setup nowego klienta zjada 60% czasu"** → produkt dla agencji marketplace/PPC: szablon onboardingu + automatyzacja audytu
- **"Power Automate vs Copilot Studio"** → szkolenie / decision framework: kiedy które narzędzie (Microsoft stack)
- **"Spotkanie → zadania → status → przypomnienie"** → produkt: workflow n8n/Make + integracja z Redmine/Planner/Trello (uniwersalny across branż)
- **"Scraper nowinek PPC z YouTube"** → mikroprodukt: content radar dla agencji reklamowych (analogia do daily-briefing)
