---
type: course-script
modul: 06
tytul: "Autonomiczne Agenty AI — MASTERCLASS"
prowadzacy: Kacper Sieradziński
czas_total: "~4 godziny"
slowa: "~3500"
status: draft
last_reviewed: 2026-03-27
---

# Moduł 06: Skrypt nagrania — Autonomiczne Agenty AI

> **Jak czytać ten skrypt:**
> - Tekst normalny = mówisz to na ekran
> - `[SLAJD N]` = przełącz slajd
> - `[DEMO: opis]` = przełącz na n8n, pokaż live
> - `[PYTANIE do widzów]` = pauza retoryczna, daj 2-3 sekundy
> - `[PAUZA]` = chwila oddechu, pozwól widzowi przetrawić
> - *kursywa w nawiasach* = notatka produkcyjna, nie mów tego

---

## SEGMENT 1: Czym naprawdę jest agent AI
*Czas segmentu: ~20 minut*

---

`[SLAJD 1]`

*(3 sekundy ciszy. Patrz w kamerę.)*

Wyobraź sobie że masz stażystę który nigdy nie śpi.

`[SLAJD 2]`

[PAUZA]

Pracuje 24/7. Nie narzeka. Nie prosi o podwyżkę po trzech miesiącach. Może jednocześnie sprawdzić 50 firm zanim zdążysz wypić kawę. A kosztuje — dosłownie — dwa złote za godzinę pracy.

To nie jest metafora. Za chwilę zobaczysz live kalkulator i sam policzysz.

[PAUZA]

Ten moduł jest inny niż poprzednie. Do tej pory budowałeś automatyzacje które wykonują to, co im każesz. Krok po kroku, sekwencyjnie, przewidywalnie. To było dobre. To jest fundament.

Ale agent AI to coś innego. Agent AI *podejmuje decyzje*. Dostaje cel, nie instrukcję. Dostaje pytanie, nie odpowiedź. I sam — na podstawie dostępnych narzędzi — wymyśla jak ten cel osiągnąć.

`[SLAJD 3]`

Dzisiaj zbudujemy razem **Wirtualnego Analityka B2B Leadów**. System trzech agentów, który bierze nazwę firmy i w ciągu 90 sekund generuje pełny raport: profil firmy, ocenę dopasowania do twojego ICP i gotowy pitch sprzedażowy.

Kosztem 80 groszy za analizę.

Czas budowania: 90 minut.

Zanim dojdziemy do projektu — musisz zrozumieć jak to działa pod spodem. Bo jeśli nie rozumiesz architektury, to gdy coś się posypie — i *zawsze* coś się posypie w produkcji — nie będziesz wiedział gdzie patrzeć.

---

### 1.2 Architektura: perception → reasoning → action → memory

`[SLAJD 4]`

Każdy agent AI, niezależnie od frameworka, działa według tego samego cyklu czterech kroków.

**Perception.** Agent musi skądś dostać dane. Email, webhook, zapytanie użytkownika, wynik poprzedniego agenta. To jest wejście. Bez wejścia agent jest ślepy.

**Reasoning.** To jest część gdzie działa LLM — GPT-4o, Claude, Gemini, co tam podłączyłeś. Model patrzy na dane wejściowe, patrzy na dostępne narzędzia, i decyduje: co teraz zrobić? Wywołać narzędzie? Zapytać o więcej danych? Wygenerować odpowiedź końcową?

[PYTANIE do widzów] Jak myślisz, ile iteracji tej pętli wykonuje agent zanim da ci odpowiedź?

Może jedna. Może dziesięć. Nie wiesz z góry. Agent sam decyduje kiedy skończyć.

**Action.** Wywołanie narzędzia. Search, scrape, API call, zapis do bazy, wysłanie emaila. To jest moment gdzie agent dotyka świata zewnętrznego.

**Memory.** Agent zapamiętuje wyniki i wraca do Reasoning. Czy mam już dość danych? Czy odpowiedź jest kompletna? Jeśli nie — kolejna iteracja.

`[SLAJD 5]`

[DEMO: Pokaż w n8n gotowy prosty agent — trigger, AI Agent node, narzędzie HTTP, response. Uruchom na żywo pytanie "jaka jest strona firmy Dokodu?" i pokaż jak agent sam wywołuje search tool i odpowiada.]

Patrzcie na logi po prawej. Widzicie to? Agent najpierw zdecydował że potrzebuje narzędzia search. Wywołał je. Dostał wynik. Zdecydował że ma dość danych. Wygenerował odpowiedź.

Cały czas decyzji: zero sekund. My go nie pytaliśmy "czy użyć searcha". On sam to wiedział — bo miał odpowiedni opis narzędzia.

To jest kluczowe. Wrócę do tego w segmencie o tools.

---

## SEGMENT 2: Memory — serce agenta
*Czas segmentu: ~35 minut*

---

`[SLAJD 6]`

Okej, porozmawiajmy o memory. I od razu zacznę od czegoś, co widziałem u dziesiątek osób zaczynających z agentami AI.

[DEMO: Pokaż agenta BEZ skonfigurowanej pamięci. Zadaj mu pytanie, potem drugie pytanie nawiązujące do pierwszego. Agent nie pamięta kontekstu — traktuje każde pytanie jak nowe.]

Widzisz to? Zapytałem "kim jesteś" a potem "co mi przed chwilą powiedziałeś" — i agent odpowiada jakbyśmy się pierwszy raz spotkali.

To nie jest bug. To jest domyślne zachowanie. LLM jest bezstanowy. Każde wywołanie to czysta karta.

[PYTANIE do widzów] Wyobraź sobie, że twój pracownik co rano przychodzi do pracy i nie pamięta nic z poprzedniego dnia. Ilu klientów byś stracił?

Memory to nie feature. Memory to konieczność dla każdego agenta który ma prowadzić dialog lub pracować w sesjach.

---

### 2.1 Simple Memory (Buffer)

`[SLAJD 7]`

Najprostszy typ. Wszystkie wiadomości z sesji wpadają do jednego bloku tekstu i są doklejane do każdego zapytania.

Zalety: zero konfiguracji. Działa od razu. Agent "wie" co mówiłeś od początku rozmowy.

Wady: każda wiadomość powiększa blok. Po 20 wiadomościach twój system prompt + historia to już kilka tysięcy tokenów. Przy 50 wiadomościach — możesz przekroczyć context window modelu. A koszt rośnie liniowo.

[DEMO: Pokaż konfigurację Simple Memory w n8n — AI Agent node, zakładka Memory, wybór "Simple Memory", brak dodatkowych ustawień. Uruchom kilka wiadomości, pokaż jak rośnie rozmiar kontekstu w logach.]

Kiedy używać Simple Memory? Do krótkich sesji. Chatboty gdzie użytkownik zadaje 5-10 pytań i kończy. Procesy gdzie historia musi być kompletna. Na przykład workflow który analizuje emaila i odpowiada — tam masz góra 10 wymian.

---

### 2.2 Window Buffer Memory

`[SLAJD 8]`

Jeśli twój agent prowadzi dłuższe rozmowy, potrzebujesz okna.

Window Buffer Memory to sliding window — zapamiętuje ostatnie N wiadomości. Wiadomości starsze niż N — wypadają.

[PAUZA]

Trade-off jest jasny. Mniej tokenów, niższy koszt, mniejsze ryzyko przekroczenia limitu. Ale tracisz daleki kontekst. Agent nie będzie pamiętał co powiedziałeś 30 wiadomości temu.

Jak dobrać N? Praktyczna zasada: policz ile wiadomości to średnia sesja twojego użytkownika. Ustaw N na 150% tej liczby. Masz margines bezpieczeństwa bez marnowania tokenów.

[DEMO: Pokaż konfigurację Window Buffer w n8n, zmień wartość N, pokaż jak agent "zapomina" wiadomość gdy okno przesuwa się dalej.]

Jest jeden zaawansowany pattern który bardzo lubię — połączenie Window Buffer z sumaryzacją. Zamiast całkowicie tracić starsze wiadomości, uruchamiasz co jakiś czas subworkflow który je sumaryzuje i dokłada jako "kontekst historyczny" na początku okna.

To wymaga więcej konfiguracji, ale daje najlepszy stosunek jakości do kosztu. Wrócimy do tego przy projekcie.

---

### 2.3 Vector Store Memory — długoterminowa

`[SLAJD 9]`

I tutaj wchodzimy w poważne tematy.

Vector Store Memory to baza danych do której agent może pisać i z której może czytać — przez semantic search. Nie szuka "po słowach kluczowych". Szuka "po sensie".

Jak to działa technicznie: każda wiadomość jest zamieniana na wektor — listę liczb reprezentującą jej znaczenie — i zapisywana w bazie wektorowej. Gdy agent potrzebuje przypomnienia, generuje wektor z bieżącego kontekstu i szuka K najbardziej podobnych wektorów. Dostaje z powrotem "wspomnienia" semantycznie związane z aktualną rozmową.

`[SLAJD 10]`

Dwie główne opcje w n8n: Pinecone i Qdrant.

Pinecone: cloud-only, płatny, ale zero konfiguracji serwera. Bezpłatny tier daje ci jeden indeks i 100k wektorów — wystarczy na start. Koszt: $70/miesięcznie za płatny plan.

Qdrant: open-source, możesz postawić self-hosted na tym samym VPS co n8n. Za darmo poza kosztem serwera. Trochę więcej konfiguracji na początku.

Moja rekomendacja: zaczaj od Pinecone dla prototypu, przejdź na self-hosted Qdrant gdy projekt trafi do produkcji i wiesz że zostanie.

[DEMO: Pokaż w n8n węzeł Pinecone Vector Store, konfigurację, przykład zapisu i odczytu wektorów. Uruchom agenta który "pamięta" klienta z poprzedniej sesji — podaj nazwę klienta, agent automatycznie przywołuje historię z bazy wektorowej.]

Kiedy używasz Vector Store Memory? Agent obsługi klienta który rozmawiał z setkami ludzi. Asystent sprzedaży który pamięta każdy kontakt z leadem. Każdy system gdzie "długoterminowe wspomnienia" zwiększają jakość pracy agenta.

---

## SEGMENT 3: Internet access — agent który widzi świat
*Czas segmentu: ~30 minut*

---

`[SLAJD 11]`

Twój agent jest tak dobry jak dane które dostaje. LLM ma wiedzę do daty treningowej — dla GPT-4o to gdzieś połowa 2024. Jeśli pytasz o firmę, konkurencję, aktualny cennik — model może wymyślać.

Rozwiązanie: daj agentowi dostęp do internetu.

---

### 3.1 SerpAPI — wyszukiwarka dla agenta

`[SLAJD 12]`

SerpAPI to API które tłumaczy zapytania do Google na ustrukturyzowany JSON. Agent nie otwiera przeglądarki — wysyła HTTP request, dostaje listę wyników z tytułami, URL-ami, fragmentami.

Koszt: od $50/miesięcznie za 5000 zapytań. Przelicz: przy 100 analiz leadów dziennie, każda analiza robi 5-10 zapytań. Miesięcznie to 15-30 tysięcy zapytań. Plan $50 nie wystarczy — potrzebujesz $140. Wlicz to w koszt per analiza.

[DEMO: Pokaż konfigurację SerpAPI w n8n — HTTP Request node, parametry q i api_key, parse JSONa, wyciągnij top 5 wyników. Uruchom przykładowe zapytanie "Dokodu AI Warszawa" i pokaż wyniki.]

Jeden niuans który oszczędzi ci bólu głowy: opisz narzędzie dla agenta tak żeby wiedział KIEDY go używać i JAKIE pytania zadawać.

Zły opis narzędzia: "Search the internet for information."

Dobry opis: "Search Google for factual information about companies: official website, contact details, recent news, LinkedIn profile. Use when you need current, verifiable facts about a specific company. Always search in Polish first, then in English if results are insufficient."

Różnica? Przy złym opisie agent będzie używał searcha do wszystkiego, generując nadmiarowe koszty. Przy dobrym — używa go precyzyjnie i efektywnie.

---

### 3.2 Firecrawl — scraping stron

`[SLAJD 13]`

SerpAPI daje ci linki i fragmenty. Ale co jeśli chcesz przeczytać całą stronę? Wyciągnąć ofertę, cennik, opis usług?

Tu wchodzi Firecrawl.

Firecrawl to API które bierze URL, renderuje stronę (łącznie z JavaScript), i zwraca czysty Markdown. Bez HTML-owego syfu. Bez CSS. Czysty tekst gotowy dla LLM.

[DEMO: Pokaż live — podaj URL dokodu.it/oferta. Firecrawl zwraca Markdown z opisem usług. Agent czyta Markdown, wyciąga informacje o usługach, cenach i segmencie klientów. Pokaż jak wynik trafia do kolejnego kroku pipeline'u.]

Pułapki z Firecrawl:

Pierwsza: rate limits. Bezpłatny plan to 500 stron miesięcznie. Przy intensywnym użytkowaniu płacisz — około $16 miesięcznie za 3000 stron. Wlicz to.

Druga: strony z logowaniem. Firecrawl nie przejdzie przez login. Do tego potrzebujesz Browserless — za chwilę.

Trzecia: robots.txt. Sprawdzaj go przed scraping. Niektóre firmy explicite zabraniają scrapingu i możesz mieć problem prawny. W Polsce to szara strefa, ale zachowaj ostrożność.

---

### 3.3 Live demo: agent bada firmę

`[SLAJD 14]`

[DEMO: Pokaz end-to-end — weź fikcyjną firmę "TechLogistic sp. z o.o. Kraków". Agent:
1. SerpAPI: szuka firmy w Google — dostaje URL strony i LinkedIn
2. Firecrawl: czyta stronę główną — dostaje opis działalności
3. SerpAPI: szuka newsów o firmie z ostatnich 6 miesięcy
4. Agreguje wyniki i generuje 3-zdaniowe podsumowanie
Pokaż jak długo to trwa (15-30 sekund) i ile tokenów zużył (log z n8n)]

Czas: 22 sekundy. Koszt tokenów: około 15 groszy. Do tego koszt SerpAPI i Firecrawl: powiedzmy 3 grosze. Całość: 18 groszy za research który ręcznie zajął by mi 20 minut.

[PAUZA]

Teraz pomnóż przez 50 leadów tygodniowo.

---

## SEGMENT 4: Structured Output i Function Calling
*Czas segmentu: ~25 minut*

---

`[SLAJD 15]`

Mamy agenta który potrafi szukać, czytać strony, zbierać dane. Teraz problem: co robi z wynikami?

[DEMO: Pokaż agenta BEZ structured output — dostaje dane o firmie i generuje odpowiedź w wolnym tekście. Raz pisze "Firma X zajmuje się...", inny raz "Na podstawie analizy stwierdzam że...", jeszcze inny raz robi listę punktowaną. Każda odpowiedź inaczej sformatowana.]

To jest piękna demonstracja problemu. Jeśli chcesz te dane wziąć i wrzucić do Excela, CRM, wysłać emailem — musisz parsować tekst. A parsowanie tekstu to droga do szaleństwa.

Rozwiązanie: JSON Schema i Function Calling.

---

### 4.1 JSON Schema w n8n

`[SLAJD 16]`

Definiujesz schema — strukturę danych którą chcesz dostać. Agent jest zmuszony wypełnić tę strukturę. Albo zwraca poprawny JSON, albo dostajesz błąd.

Przykład schema dla raportu lead analyst:

```json
{
  "company_name": "string",
  "website": "string",
  "industry": "string",
  "employee_count": "number lub null",
  "description": "string, max 200 słów",
  "icp_score": "number 1-10",
  "icp_reasoning": "string",
  "recommended_service": "string",
  "next_step": "string",
  "confidence": "number 0.0-1.0"
}
```

[DEMO: Pokaż Structured Output Parser node w n8n. Wklej schema. Uruchom agenta na tej samej firmie co wcześniej. Teraz dostaje poprawny JSON. Pokaż że każde pole jest wypełnione, typy się zgadzają.]

`[SLAJD 17]`

Jeden pattern który musisz znać: **retry przy błędzie walidacji**.

Agent czasem zwraca JSON który jest prawie poprawny. Brakuje cudzysłowu. Dodatkowy przecinek. Pole jest stringiem zamiast numbera.

Zamiast crashować workflow, dodaj retry loop: jeśli walidacja JSON się nie powiodła, wróć do agenta z wiadomością "Twój output nie był poprawnym JSONem. Oto błąd: [błąd]. Spróbuj ponownie, tym razem zwróć TYLKO JSON, bez żadnego tekstu przed ani po."

W 95% przypadków agent poprawia się przy drugim podejściu.

---

## SEGMENT 5: Tool Use Advanced
*Czas segmentu: ~30 minut*

---

`[SLAJD 18]`

Wbudowane tools n8n — SerpAPI, Calculator, Wikipedia — to dobry start. Ale prawdziwa moc jest w custom tools.

Custom tool to subworkflow. Jakikolwiek workflow w n8n może stać się narzędziem agenta.

---

### 5.1 Subworkflow jako tool

`[SLAJD 19]`

Architektura jest prosta: Main Workflow zawiera AI Agent node. Agent ma dostęp do listy tools. Jeden z tools to "Execute Workflow" — wywołanie innego workflowa.

Konfiguracja: w "Execute Workflow" node definiujesz input schema (co agent może przekazać) i output schema (co wraca do agenta). Opisujesz narzędzie: kiedy go używać, co robi, jakie parametry przyjmuje.

[DEMO: Pokaż budowanie custom tool "sprawdź_krs" — subworkflow który bierze NIP firmy, wywołuje API KRS, i zwraca datę rejestracji, formę prawną, adres i status. Zintegruj z głównym agentem. Uruchom — agent sam decyduje że dla polskiej firmy warto sprawdzić KRS i wywołuje tool.]

`[SLAJD 20]`

Zasada którą stosuję do każdego projektu: **jeden tool, jedna odpowiedzialność**.

Zły design: tool "zbierz_dane_o_firmie" który robi SerpAPI, Firecrawl, KRS i LinkedIn naraz.

Dobry design: cztery osobne tools, każdy robi jedno. Agent sam decyduje których użyć i w jakiej kolejności.

Dlaczego? Bo LLM znacznie lepiej dobiera narzędzia gdy każde ma wąską, precyzyjną funkcję. I bo możesz testować tools niezależnie od agenta.

---

### 5.2 Biblioteka tools — naming conventions

`[SLAJD 21]`

Jak opisywać tools żeby LLM ich dobrze używał?

Trzy zasady:

**Nazwa**: zacznij od czasownika. `search_web`, `scrape_page`, `check_krs`, `send_email`. Nie "WebSearch" ani "Crawler". Czasownik mówi agentowi co tool *robi*.

**Opis**: jedno zdanie — kiedy używać. Jedno zdanie — co zwraca. Ewentualnie: czego NIE robi. Na przykład: "Searches Google for information about a company. Returns top 5 results with title, URL, and snippet. Does NOT read the full content of pages — use scrape_page for that."

**Parametry**: nazwy oczywiste, typy jasne, dodaj description do każdego pola.

[DEMO: Pokaż bibliotekę czterech tools które zbudujesz w projekcie — search_web, scrape_page, check_krs, analyze_linkedin. Każdy ma nazwę, opis, parametry. Pokaż jak agent w logach wybiera właściwy tool do właściwego zadania.]

---

## SEGMENT 6: Multi-Agent Systems — orkiestra agentów
*Czas segmentu: ~35 minut*

---

`[SLAJD 22]`

Jeden agent jest świetny. Ale jeden agent ma limity.

Limit pierwszy: context window. Im więcej zadań, tym więcej kontekstu, tym drożej i wolniej.

Limit drugi: specjalizacja. Agent który robi wszystko jest gorszy w każdym zadaniu niż agent który robi jedno. Tak samo jak w świecie ludzi.

Limit trzeci: równoległość. Jeden agent robi jedno zadanie na raz. Trzy agenty mogą pracować jednocześnie.

`[SLAJD 23]`

Trzy wzorce multi-agent które powinieneś znać.

**Supervisor + Workers**: Supervisor dostaje zadanie, dekompozuje je, deleguje do specjalistycznych Workerów, syntezuje wyniki. To budujesz dzisiaj.

**Agent Chain (Pipeline)**: Wynik agenta 1 staje się inputem agenta 2. Research Agent → Analysis Agent → Report Agent. Prosty, przewidywalny, łatwy do debugowania.

**Peer Agents**: Agenty współpracują równorzędnie, dzielą się informacjami, każdy ma swój zakres. Bardziej złożone — na razie omijaj.

---

### 6.1 Supervisor + Worker Pattern

`[SLAJD 24]`

Supervisor ma jeden job: **dekompozycja i synteza**.

System prompt Supervisora NIE opisuje szczegółów poszczególnych zadań. Opisuje:
- Jakich Workerów ma do dyspozycji
- Co każdy Worker potrafi
- Jak podzielić zadanie między nich
- Jak złożyć wyniki w spójną całość

Worker ma jeden job: **wykonaj swoją specjalizację perfekcyjnie**.

System prompt Workera jest bardzo szczegółowy w swojej dziedzinie. Worker Research wie dokładnie jak szukać, weryfikować, cytować. Worker ICP Fit wie dokładnie jak oceniać i argumentować scoring.

`[SLAJD 25]`

[DEMO: Pokaż główny workflow z Supervisor Agent i trzema Workers połączonymi przez "Execute Workflow" nodes. Uruchom na fikcyjnej firmie "AutoParts Logistics Gdańsk sp. z o.o.". Pokaż w logach jak:
1. Supervisor dostaje firmę i dekomponuje zadanie
2. Research Worker zbiera dane
3. ICP Fit Worker ocenia dopasowanie
4. Sales Strategy Worker tworzy pitch
5. Supervisor syntezuje i zwraca raport
Pokaż czas całościowy i koszty per worker.]

30 sekund. Trzy agenty pracowały równolegle. Żaden nie wiedział co robi drugi.

[PYTANIE do widzów] Jak długo zabrałoby ci zrobienie tego ręcznie? Tylko szczerze.

---

## SEGMENT 7: Halucynacje — jak z nimi walczyć
*Czas segmentu: ~25 minut*

---

`[SLAJD 26]`

Dobra. Czas na trudną rozmowę.

Agenty AI halucynują. Nie pytaj czy. Pytaj kiedy i jak często.

[DEMO: Pokaż agenta który dostał pytanie o fikcyjną firmę "Nexo Technologies Katowice sp. z o.o." — firma nie istnieje. BEZ narzędzi agent spokojnie wymyśla: "Firma zatrudnia 120 pracowników, działa od 2015 roku, specjalizuje się w integracji systemów ERP." Wszystko fałszywe. Powiedzone z pełną pewnością.]

Widzisz to? Model nie powiedział "nie wiem". Powiedział "firma zatrudnia 120 pracowników." Skąd to wziął? Z niczego. Z rozkładu prawdopodobieństwa tokenów.

To jest najgroźniejsze zachowanie LLM w systemach produkcyjnych.

---

### 7.1 Strategie minimalizacji halucynacji

`[SLAJD 27]`

**Grounding przez narzędzia.** Zamiast pytać agenta "co wiesz o tej firmie", każ mu *znaleźć* dane o tej firmie. Każdy fakt musi mieć źródło. W system prompcie: "Używaj wyłącznie informacji z narzędzi search i scrape. Nigdy nie dodawaj informacji z własnej wiedzy."

**Verification step.** Dodaj drugiego agenta który ma jedno zadanie: zweryfikować fakty pierwszego agenta. Porównuje każde stwierdzenie z dostarczonymi źródłami. Jeśli nie ma źródła — flaguje jako unverified.

**Temperature na zero.** Dla factual tasks ustaw temperature na 0.0-0.3. Niższa temperatura = mniej "kreatywności" = mniej halucynacji. Wyższa temperatura przydaje się do pisania tekstów marketingowych, nie do research.

`[SLAJD 28]`

**Explicit fallback w systemie prompcie.** To jest najprostszy i najefektywniejszy trick. Dodaj do systemu prompcie:

"Jeśli nie masz pewnych danych — nie zgaduj. Wpisz dokładnie: BRAK DANYCH. To jest lepsze niż nieprawdziwa informacja."

Modele bardzo dobrze reagują na explicit permission do "nie wiedzenia". Bez tej instrukcji model myśli że jego zadaniem jest dać odpowiedź — cokolwiek.

**Confidence score.** Poproś agenta o ocenę pewności przy każdym polu structured output. Pole `confidence: 0.0-1.0`. Gdy confidence < 0.7 — automatycznie flaguj dane do manualnej weryfikacji.

[DEMO: Pokaż tę samą fikcyjną firmę ale teraz z grounding instructions i fallback. Agent próbuje znaleźć firmę, search nie daje wyników, Firecrawl zwraca 404. Agent odpowiada: employee_count: null, confidence: 0.0, notes: "BRAK DANYCH — firma nie znaleziona w publicznych źródłach."]

Różnica jest kolosalna.

---

### 7.2 Ewaluacja — jak mierzyć jakość agenta

`[SLAJD 29]`

Nie wdrażaj agenta do produkcji bez test suite.

Moja metoda: 10 znanych firm, 3 "firmy pułapki" (nie istnieją lub mają minimalne info w necie). Uruchom agenta na wszystkich. Porównaj output z tym co wiesz o firmach.

Metryki:
- **Accuracy**: procent faktów które są prawdziwe
- **Completeness**: procent pól wypełnionych wartościami (nie BRAK DANYCH)
- **Format compliance**: procent outputów które przeszły walidację JSON schema
- **Hallucination rate**: procent pól gdzie agent wymyślił zamiast powiedzieć BRAK DANYCH

Cel produkcyjny: Accuracy > 85%, Hallucination rate < 5%.

Jeśli nie osiągasz tych liczb — nie wdrażaj. Wróć do debugowania systemu promptów i narzędzi.

---

## SEGMENT 8: Koszty i optymalizacja
*Czas segmentu: ~25 minut*

---

`[SLAJD 30]`

Wiemy już jak budować agenty. Czas porozmawiać o kasie.

Bo nic nie zabija projektu AI szybciej niż rachunek na koniec miesiąca który cię zaskakuje.

[DEMO: Otwórz live kalkulator tokenów — arkusz Google Sheets z formułami. Wypełnij parametry: model GPT-4o, system prompt 500 tokenów, memory window 2000 tokenów, input 300 tokenów, output 400 tokenów. Koszt per wywołanie: 0.018 USD.]

Na wywołanie: 2 grosze. Spoko.

Ale agent robi 8 iteracji zanim skończy. Każda iteracja to wywołanie. Osiem razy dwa grosze: 16 groszy na agenta.

Do tego trzy agenty w systemie multi-agent: 48 groszy na pełną analizę leada.

Plus SerpAPI i Firecrawl: jeszcze 20 groszy.

Razem: 68 groszy na analizę.

[PAUZA]

100 analiz dziennie: 68 PLN. Miesięcznie: 2040 PLN.

To nadal jest taniej niż jeden junior analityk. Ale musisz to wiedzieć zanim zaproponujesz to klientowi.

---

### 8.1 Strategie optymalizacji kosztów

`[SLAJD 31]`

**Model routing.** GPT-4o za reasoning i syntezę — gdzie potrzebujesz jakości. GPT-4o-mini lub Claude Haiku za proste taski — klasyfikacja, formatowanie, ekstrakcja danych z dobrze ustrukturyzowanego inputu. Różnica kosztu: 10-20x. Mądrze zdecyduj gdzie potrzebujesz "premium" a gdzie wystarczy "economy".

**Prompt Compression.** System prompt 500 tokenów vs 200 tokenów to różnica 60% kosztu na każde wywołanie. Usuń redundancje. Nie powtarzaj instrukcji które LLM i tak wie. Testuj — często krótszy prompt daje lepsze wyniki.

**Anthropic Prompt Cache.** Jeśli używasz Claude — Anthropic oferuje Prompt Caching. Jeśli system prompt i stałe części kontekstu się nie zmieniają między wywołaniami, możesz je cachować. Koszt cached tokenów: 10% normalnej ceny. 90% oszczędności na system prompcie.

**Batch Processing.** Zamiast uruchamiać agenta dla każdego leada z osobna natychmiast — zbieraj leady przez godzinę i puszczaj batch. Mniej overhead, możesz używać batch API Anthropic (50% taniej, wyniki w ciągu 24h). Sprawdza się świetnie dla non-urgent use casów.

---

### 8.2 Monitoring kosztów w produkcji

`[SLAJD 32]`

[DEMO: Pokaż workflow w n8n gdzie po każdym wywołaniu agenta Code Node wyciąga usage.prompt_tokens i usage.completion_tokens z response, mnoży przez cenę modelu i zapisuje do Google Sheets. Pokaż arkusz z historią kosztów per run.]

Dodaj alert: jeśli koszt w ciągu godziny przekroczy X PLN — wyślij Slacka i zatrzymaj workflow. Nigdy więcej niespodzianek na fakturze.

---

## SEGMENT 9: Projekt — Wirtualny Analityk B2B Leadów
*Czas segmentu: ~55 minut*

---

`[SLAJD 33]`

Czas na projekt. To nie jest zabawka. To jest system który możesz jutro wdrożyć u klienta.

Architektura którą zaraz zbudujesz:

```
Email / Webhook CRM
        ↓
[Supervisor Agent]
   "Analizuj lead: {nazwa_firmy}"
        ↓
  ┌─────┼─────┐
  ↓     ↓     ↓
[W1]  [W2]  [W3]
Research ICP  Sales
        ↓
[Supervisor: synteza]
        ↓
Raport Markdown → Email + CRM
```

Trzy decyzje architektoniczne które podjąłem i chcę żebyś rozumiał dlaczego:

Dlaczego 3 Workers zamiast 1? Bo każdy Worker ma inny system prompt, inny cel, inną perspektywę. Research Worker wie że jego zadaniem jest zbieranie faktów — nie ocena. ICP Fit Worker ocenia bez bias faktograficzny. Sales Worker tworzy pitch bez bias oceny dopasowania.

Dlaczego Supervisor zamiast Chain? Bo Workers mogą pracować równolegle. Chain byłby sekwencyjny — trzy razy dłużej.

Dlaczego raport w Markdown? Bo możesz go wysłać emailem, wrzucić do CRM jako notatkę, wyświetlić w aplikacji webowej — bez konwersji.

---

### Build LIVE: Trzy Workers

`[SLAJD 34]`

[DEMO: Zacznij od Worker 1 — Research Faktograficzny.

Pokaż budowanie krok po kroku:
- Trigger: Execute Workflow
- Input: company_name, country
- AI Agent node z modelem GPT-4o
- System prompt (pokaż na ekranie pełną treść)
- Tools: search_web (SerpAPI), scrape_page (Firecrawl), check_krs
- Structured Output Parser z schema
- Return node

Uruchom na "Softlab SA Warszawa" — pokaż jak agent zbiera dane, wywołuje narzędzia, zwraca JSON.]

`[SLAJD 35]`

[DEMO: Worker 2 — Analiza ICP Fit.

Ten Worker NIE ma dostępu do internetu. Dostaje tylko wynik Worker 1 — dane o firmie — i ocenia dopasowanie do ICP.

System prompt: "Jesteś ekspertem sprzedaży B2B w agencji AI. Twoje ICP to polskie firmy 50-500 pracowników z branży produkcji, logistyki lub finansów, które mają procesy powtarzalne i pracowników przeprowadzających ręczne operacje na danych. Oceń firmę w skali 1-10."

Structured output: icp_score (1-10), strengths (lista), concerns (lista), icp_reasoning (string).]

`[SLAJD 36]`

[DEMO: Worker 3 — Rekomendacja Sprzedażowa.

Ten Worker dostaje dane o firmie (W1) I ocenę ICP (W2). Generuje:
- recommended_service: jaką usługę Dokodu zaproponować
- pitch_opening: pierwsze zdanie rozmowy sprzedażowej
- discovery_questions: 3 pytania do zadania w discovery call
- pain_points: zidentyfikowane bóle na podstawie danych o firmie

Model: GPT-4o. Temperatura: 0.7 — tu trochę więcej kreatywności jest ok.]

---

### Build LIVE: Supervisor i output

`[SLAJD 37]`

[DEMO: Supervisor Agent.

Main workflow:
1. Webhook trigger — odbiera {company_name}
2. Uruchamia równolegle Worker 1, 2 i 3 (tylko W1 nie potrzebuje wyników innych, W2 i W3 muszą poczekać na W1)
3. Właściwie: W1 → równolegle W2 i W3 → Supervisor
4. Supervisor dostaje: research_data, icp_analysis, sales_rec
5. Generuje finalny raport Markdown

Pokaż system prompt Supervisora — jego zadanie to TYLKO synteza, nie powtarzanie.

Uruchom pełny flow na "Apator SA Torun" — znana firma produkcyjna. Pokaż czas (około 30 sekund), pokaż finalny raport w Markdown.]

`[SLAJD 38]`

Raport który właśnie wygenerowałeś w 30 sekund normalnie wymaga 45 minut research analityka.

Koszt: 68 groszy.

Koszt 45 minut analityka przy polskiej stawce: około 60 PLN.

ROI tego systemu: 88x. Nie 88 procent. 88 razy.

[PAUZA]

I to jest liczba którą możesz postawić klientowi na stole podczas discovery call.

---

### Test i weryfikacja

`[SLAJD 39]`

[DEMO: Uruchom na trzech firmach:
1. Duża znana firma: KGHM — pełne dane, wysoki confidence
2. Mała mało znana firma: "Zakład Produkcji Okien Bąk sp.j. Rzeszów" — częściowe dane, BRAK DANYCH w kilku polach
3. Firma pułapka: fikcyjna "DigitalFlow Solutions sp. z o.o. Kraków" — agent zwraca BRAK DANYCH bez halucynacji]

Trzy przypadki, trzy różne wyniki, wszystkie poprawne zachowania.

Systemy AI w produkcji muszą dobrze radzić sobie nie tylko z happy path, ale szczególnie z edge casami. Test suite to nie opcja.

---

## PODSUMOWANIE I CTA
*Czas: ~5 minut*

---

`[SLAJD 40]`

Dobra. Co zbudowałeś w tym tygodniu?

System trzech agentów który analizuje leady B2B. Który korzysta z internetu w czasie rzeczywistym. Który pamięta kontekst między sesjami. Który generuje ustrukturyzowane, weryfikowalne raporty.

I który kosztuje mniej niż jedna kawa na analizę.

`[SLAJD 41]`

**Zadanie domowe na ten tydzień:**

Podłącz system do swojego CRM. Trigger: nowy lead dodany do Pipedrive lub HubSpot. Output: raport zapisany jako nota do kontaktu.

Brzmi prosto. Ale wymaga od ciebie przejścia przez autentykację OAuth, mapowanie pól, error handling dla CRM który nie odpowiada. To są rzeczy których nauczyłeś się w Tygodniu 1 i 3. Teraz je połączysz.

`[SLAJD 42]`

**W Tygodniu 7** wejdziemy w RAG — Retrieval Augmented Generation.

Wyobraź sobie agenta który ma dostęp do całej Twojej dokumentacji, wszystkich umów z klientami, wszystkich poprzednich projektów. I może z tej wiedzy korzystać w czasie rzeczywistym.

To jest ważniejsze niż internet access. Bo wewnętrzna wiedza firmy jest zwykle cenniejsza niż publiczne dane.

[PAUZA]

**Jeśli zbudujesz projekt tego tygodnia** — wrzuć screenshot systemu i wyniki testu na grupy n8n Polska lub Discord kursu. Będę komentował.

I ostatnia rzecz: jeśli to jest moduł który chciałeś pokazać szefowi, klientowi, współpracownikowi żeby przekonać ich do automatyzacji AI — ten projekt jest na to idealny. 88x ROI to liczba która przemawia do każdego.

Do zobaczenia w Tygodniu 7.

`[SLAJD 43]`

[PAUZA — outro music]

---

## Notatki produkcyjne do tego skryptu

- **Czas całości**: ~4 godziny nagrania. Segment 9 nagraj oddzielnie jako pierwszy — to benchmark jakości.
- **Demo backup**: przygotuj pre-built workflow dla każdego demo na wypadek błędów na żywo. Nic nie psuje przepływu tak jak debugowanie live przez 5 minut.
- **Kalkulator tokenów**: przygotuj Google Sheet z formułami przed nagraniem Segmentu 8. Wypełnij realistycznymi liczbami.
- **Fikcyjne firmy w demo**: używaj nazw które brzmią realistycznie ale na pewno nie istnieją ("TechLogistic sp. z o.o." może istnieć — sprawdź KRS wcześniej).
- **Chaptery YouTube**: każdy segment = osobny chapter. Timestamps generuj z Agendą jako bazą.
- **Screen recording**: n8n + ewentualnie IDE side-by-side dla Code Node examples w Segmencie 4.
- **B-roll**: nagraj osobno ujęcia samych flows w n8n bez komentarza — przydadzą się do montażu.
