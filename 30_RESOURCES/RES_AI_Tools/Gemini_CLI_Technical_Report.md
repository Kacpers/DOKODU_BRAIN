# **Gemini CLI: Architektura, Narzędzia Agentowe i Inżynieria Kontekstu. Dogłębny Raport Techniczny**

Ewolucja interfejsów programistycznych weszła w fazę, w której środowisko wiersza poleceń (CLI) przestaje być jedynie statycznym narzędziem do wykonywania skryptów, a staje się autonomicznym, rezonującym ekosystemem operacyjnym. Wraz z rynkową premierą otwartego oprogramowania Gemini CLI, zasilanego modelami z rodziny Gemini 2.5 Pro oraz najnowszym Gemini 3.1 Pro, inżynieria oprogramowania zyskuje dostęp do agenta terminalowego o niespotykanych dotąd możliwościach.1 W odróżnieniu od klasycznych asystentów opartych na interfejsach czatowych w przeglądarce, natywna integracja agenta z powłoką systemu operacyjnego, systemem plików oraz zdalnymi serwerami pozwala na delegowanie złożonych, wieloetapowych przepływów pracy.

Niniejszy raport stanowi wyczerpującą dekonstrukcję narzędzia Gemini CLI, analizując jego mechanizmy wewnętrzne, architekturę zarządzania gigantycznym kontekstem, implementację pętli decyzyjnych oraz protokoły integracyjne. Dokument ten został przygotowany z myślą o zaawansowanych inżynierach automatyzacji, programistach ekosystemu Python oraz architektach systemów, którzy poszukują empirycznych dowodów na przewagę tego rozwiązania nad konkurencyjnymi platformami, takimi jak Claude Code czy Cursor.4

## **1\. Architektura i "Context King" (1M+ Tokenów)**

Zrozumienie fundamentalnej przewagi Gemini CLI wymaga przenalizowania sposobu, w jaki nowoczesne modele językowe przetwarzają informacje o strukturze projektu. W przypadku większości rynkowych rozwiązań programistycznych, głównym wąskim gardłem jest limitowana pojemność okna kontekstowego (zazwyczaj oscylująca w granicach od 128 do 200 tysięcy tokenów).6

### **Zmierzch tradycyjnego RAG na rzecz natywnego przetwarzania**

Dotychczasowym standardem radzenia sobie z rozległymi repozytoriami kodu była technika Retrieval-Augmented Generation (RAG). W architekturze tej, narzędzie programistyczne indeksuje lokalne pliki, przetwarza je na osadzenia wektorowe (embeddings) i przechowuje w lokalnej bazie danych. Gdy użytkownik zadaje pytanie, system wykonuje wyszukiwanie semantyczne (często wspierane mechanizmami BM25 lub TF-IDF), wyciągając jedynie te fragmenty kodu (chunks), które algorytm uzna za najbardziej zbliżone matematycznie do zapytania, a następnie ładuje je do okna kontekstowego modelu.

Choć RAG jest wysoce wydajny pod kątem zużycia tokenów, drastycznie zawodzi w złożonych zadaniach inżynieryjnych.8 Architektura oprogramowania rzadko opiera się na liniowych zależnościach. Przykładem mogą być rozbudowane projekty oparte na architekturze mikroserwisów, gdzie interfejsy zdefiniowane w jednym pliku TypeScript są implementowane w innym, konsumowane w trzecim, a testowane w czwartym. Wyszukiwarki wektorowe regularnie gubią ten "ukryty kontekst", co prowadzi do generowania przez AI kodu, który używa nieistniejących metod lub łamie globalne konwencje projektowe.10

Gemini CLI rozwiązuje ten problem poprzez brutalną siłę obliczeniową, zyskując miano "Context King". Natywna obsługa 1 miliona tokenów (z perspektywą rozszerzenia w kolejnych iteracjach modeli) pozwala na całkowite pominięcie bazy RAG.1 Jeden milion tokenów to równowartość około 50 000 linii gęstego kodu źródłowego, 1500 stron dokumentacji A4 w formacie Markdown lub pełnej historii zmian z systemu kontroli wersji.1 Model Gemini 3.1 Pro jest w stanie "pochłonąć" całe repozytorium za jednym zamachem, wczytując do pamięci operacyjnej każdy plik, każdy komentarz i każdą zależność. Pozwala to na mapowanie architektury w sposób holistyczny – agent widzi projekt dokładnie tak, jak widziałby go doświadczony architekt przeglądający całe drzewo plików.12

Aby zoptymalizować tak potężne zapotrzebowanie na przepustowość, architektura wykorzystuje zaawansowany mechanizm **Context Caching** (jawnego buforowania). Zamiast przetwarzać milion tokenów przy każdym kolejnym zapytaniu w tej samej sesji terminalowej, infrastruktura Google Cloud serializuje przetworzony stan początkowy repozytorium. Koszt zapisu do cache wynosi około 2,00$ za milion tokenów (wersja standardowa), ale odczyt z niego spada do zaledwie 0,50$ (redukcja o 75%), a koszt magazynowania to jedyne 4,50$ za godzinę.14 Dzięki temu kolejne iteracje rozmowy z agentem charakteryzują się niezwykle niskim opóźnieniem (Time-To-First-Token), mimo operowania na gigantycznym zbiorze danych.16

### **Anatomia pętli ReAct (Reasoning and Acting) w terminalu**

Zdolność do "rozumienia" kodu to tylko połowa sukcesu. Prawdziwa autonomia Gemini CLI wynika z implementacji wzorca ReAct (Reasoning \+ Acting), który przekształca pasywny model generujący tekst w aktywnego agenta potrafiącego modyfikować środowisko.17 Mechanika ta realizowana jest w architekturze dwupakietowej: packages/cli obsługuje interfejs, strumieniowanie i autoryzację, natomiast packages/core zarządza wykonawcą agentowym (AgentExecutor), rejestrem narzędzi oraz planowaniem.19

Prześledźmy dekonstrukcję tego procesu krok po kroku na podstawie polecenia, które stanowi marzenie każdego specjalisty od utrzymania systemów:

gemini "Przeanalizuj logi błędów i napraw kod"

1. **Inicjalizacja i wstrzyknięcie narzędzi:** Po zatwierdzeniu polecenia w terminalu, funkcja submitQuery przesyła prompt do chmury. Wraz z tekstem, wysyłany jest pełen schemat JSON-RPC zadeklarowanych w systemie narzędzi (np. operacje na plikach, komendy powłoki) oraz zawartość instrukcji z plików konfiguracyjnych.20  
2. **Krok 1: Rozumowanie (Thought):** Model Gemini przetwarza zapytanie. Zamiast natychmiastowo generować odpowiedź tekstową dla użytkownika, wchodzi w tryb wewnętrznego dialogu. Emituje ukryty znacznik myślowy: *"Użytkownik prosi o naprawę błędu. Nie mam w kontekście żadnych logów. Najpierw muszę zlokalizować pliki logów w obecnym katalogu roboczym."*.21  
3. **Krok 2: Akcja (Action) \- Rozpoznanie:** Model podejmuje decyzję o użyciu narzędzia. Generuje odpowiedź w formacie ustrukturyzowanym (Function Calling): wywołanie run\_shell\_command(command="find. \-name '\*.log' \-mtime \-1") lub glob(pattern="\*\*/\*.log").23  
4. **Przechwycenie przez CLI:** Funkcja processGeminiStreamEvents w kliencie przechwytuje żądanie wywołania narzędzia. Zatrzymuje strumieniowanie tekstu do użytkownika i przekazuje kontrolę do CoreToolScheduler.20 Jeśli włączony jest tryb bezpieczny, na ekranie pojawia się prośba o autoryzację komendy find. Po zatwierdzeniu, proces Node.js wykonuje komendę bezpośrednio w powłoce systemu.  
5. **Krok 3: Obserwacja (Observation):** CLI chwyta wynik standardowego wyjścia (stdout), np. src/logs/app\_error.log i odsyła go do API jako wynik wywołania funkcji.25  
6. **Krok 4: Rozumowanie i Akcja (Pętla 2):** Model analizuje ścieżkę. Generuje kolejne wywołanie: read\_file(path="src/logs/app\_error.log").24 Otrzymuje w odpowiedzi zrzut stosu (stack trace) wskazujący na błąd np. KeyError: 'payment\_id' w linii 142 pliku webhook\_handler.py.  
7. **Krok 5: Akcja mutacyjna:** Model wywołuje read\_file(path="webhook\_handler.py"). Analizuje błędną logikę (brak walidacji klucza w słowniku JSON). Następnie wywołuje narzędzie replace lub write\_file, przesyłając diff ze zmienionym kodem wprowadzającym np. metodę .get('payment\_id') z obsługą błędu.23  
8. **Krok 6: Weryfikacja (Self-Correction):** Dobrze zaprojektowany system prompt w Gemini CLI wymusza na agencie weryfikację swojej pracy.12 Agent autonomicznie wywołuje run\_shell\_command(command="pytest tests/test\_webhook\_handler.py").27 Jeśli test przejdzie, pętla ulega zamknięciu. Jeśli nie – agent analizuje wynik błędu kompilacji lub testu i generuje kolejną poprawkę.29  
9. **Zakończenie zadania:** Model formułuje ostateczną odpowiedź tekstową do użytkownika, streszczając wykonane działania. Pętla ReAct zamyka swój cykl.

Cały ten proces, oparty na iteracyjnym odkrywaniu, badaniu i modyfikowaniu środowiska, dzieje się w tle, uwalniając inżyniera od konieczności manualnego kopiowania i wklejania logów pomiędzy IDE a oknem czatu w przeglądarce.

### **Architektura Integracji z MCP (Model Context Protocol)**

To, co czyni Gemini CLI rozwiązaniem wysoce adaptowalnym w zaawansowanych sieciach deweloperskich, to natywna, zintegrowana w rdzeniu obsługa Model Context Protocol (MCP).30 Zainicjowany początkowo przez firmę Anthropic (twórców Claude), MCP stał się niepisanym standardem branżowym, porównywanym do "USB-C dla sztucznej inteligencji".32

W kontekście automatyzacji i inżynierii, MCP to otwartoźródłowy protokół typu klient-serwer, który definiuje, w jaki sposób modele LLM mogą bezpiecznie i przewidywalnie odkrywać nowe narzędzia, konteksty i źródła danych spoza własnego środowiska lokalnego.30

Moduł integracyjny w Gemini CLI (packages/core/src/tools/mcp-client.ts) zarządza trzema podstawowymi wektorami komunikacji 31:

1. **Discovery Layer (Odkrywanie narzędzi):** Kiedy uruchamiasz Gemini CLI, system analizuje plik konfiguracji .gemini/settings.json. Jeśli napotka w nim definicje serwerów w bloku mcpServers, inicjuje połączenie. Następnie wysyła żądanie odkrycia narzędzi, na które serwer odpowiada ustandaryzowanym schematem formatu JSON (opisującym np. jakie parametry przyjmuje zapytanie SQL do zewnętrznej bazy).31  
2. **Warstwy Transportowe:** Architektura wspiera trzy typy połączeń 31:  
   * **Stdio (Standard Input/Output):** Dla serwerów uruchamianych lokalnie jako procesy potomne powłoki (np. skrypt Python z modułem fastmcp uruchamiany przez uvx).33  
   * **SSE (Server-Sent Events) oraz HTTP:** Dla serwerów zdalnych, hostowanych w infrastrukturze chmurowej.31  
3. **Execution Layer (Wykonanie i autoryzacja):** Po przypisaniu narzędzia z serwera MCP do instancji agenta, klasa DiscoveredMCPTool opakowuje logikę wykonania, rygorystycznie sprawdzając zgodność z polityką bezpieczeństwa (np. wymagając każdorazowej zgody operatora na wywołanie zdalnego API).31

**Znaczenie MCP dla twórców infrastruktury:** Zamiast ograniczać się do wbudowanych narzędzi plikowych, programista może wpiąć do Gemini CLI dedykowany serwer mcp-github, umożliwiając modelowi bezproblemowe listowanie Pull Requestów, analizę komentarzy z review oraz autonomiczne aplikowanie łatek (narzędzia: github.list\_repositories, github.create\_issue).35 Istnieją również oficjalne serwery obsługujące bazy Google Cloud SQL, co zamienia agenta w inteligentnego inżyniera danych i DevOpsa w jednym.36 Ta standaryzacja jest krytycznym argumentem w debacie z modelem Claude Code, udowadniającym, że narzędzia Google oferują równorzędną – o ile nie bardziej transparentną – obsługę protokołów integracyjnych.

## **2\. Narzędzia "Agentic" (Możliwości Wykonawcze)**

To, co napędza mechanikę działania Gemini CLI, to wbudowany arsenał wyspecjalizowanych narzędzi zdefiniowanych w module ToolRegistry.19 Obejmują one pełne spektrum od manipulacji plikami systemowymi po pobieranie danych ze świata zewnętrznego. Poniżej znajduje się głęboka analiza techniczna najważniejszych modułów.

### **Google Search: Mechanizm decyzyjny i minimalizacja halucynacji (Grounding)**

Tradycyjne modele LLM cierpią na tzw. zamrożenie wiedzy (knowledge cutoff). Próba wygenerowania przez nie konfiguracji dla najnowszej, dopiero co zaktualizowanej biblioteki często kończy się halucynacją zdezaktualizowanych metod. Wbudowane narzędzie google\_web\_search radykalnie zmienia tę dynamikę.

Logika decyzyjna modelu została ukierunkowana systemowym promptem tak, aby agent traktował wyszukiwarkę jako narzędzie ostatecznego ugruntowania (Grounding). Jeśli deweloper nakazuje integrację z zewnętrznym API, model podczas analizy rozpoznaje lukę w swoim stanie wiedzy. Zamiast improwizować parametry, zawiesza wykonywanie logiki i odpala operację wyszukiwania.38 Po otrzymaniu wycinków wyników z wyszukiwarki Google, ewaluuje ich jakość, syntetyzuje niezbędne definicje typów i dopiero wtedy wraca do pisania kodu.39 Zapewnia to odporność agenta na gwałtownie zmieniające się środowisko technologii webowych (np. ciągłe aktualizacje ekosystemu React czy narzędzi w chmurze).

### **Web Fetch: Ekstrakcja surowych treści a renderowanie JavaScript**

Podczas gdy wyszukiwarka dostarcza zagregowanych odpowiedzi (podsumowań), narzędzie web\_fetch obsługiwane przez interfejs urlContext 40, stanowi dla agenta precyzyjny wenflon, którym model może zaabsorbować surową treść dokumentacji technicznej bezpośrednio ze strony internetowej.38 Gdy napotkasz trudny błąd w bibliotece, wystarczy wpisać: gemini "Przeczytaj instrukcje pod adresem https://strona.pl/docs i zastosuj podane tam rozwiązania w pliku config.ts."

Model pobierze stronę z pominięciem reklam i elementów nawigacyjnych, zamieni ją na czytelną dla siebie postać i wstrzyknie do okna kontekstowego.38 **Wyzwania techniczne i blokady:** Poważnym ograniczeniem wbudowanego modułu web\_fetch jest jego architektura bazująca na czystych żądaniach HTTP z poziomu chmury. W dobie wszechobecnych rozwiązań takich jak Cloudflare Turnstile, zabezpieczeń anty-botowych oraz nowoczesnych aplikacji SPA (Single Page Applications) ładowanych wyłącznie za pomocą mechanizmów JavaScript po stronie klienta, naiwny fetch często zwraca pusty szkielet HTML lub ekran blokady.42 Z radzeniem sobie ze standardowymi stronami statycznymi mechanizm ten jest wysoce skuteczny, niemniej w profesjonalnych projektach powszechną praktyką jest pomijanie go na rzecz wpięcia dedykowanych serwerów MCP, takich jak np. browser\_use lub instancji opartych na silniku Puppeteer/Playwright w trybie "headless Chrome".44 Te alternatywne moduły nie tylko renderują JavaScript, co pozwala na pełne zbudowanie struktury DOM, ale także potrafią symulować naturalne środowisko przeglądarki, wykonując zrzuty ekranu, które trafiają bezpośrednio do wielomodalnego rdzenia (multimodal core) modelu Gemini.46

### **Shell Execution: Weryfikacja i obrona przed komendami pokroju rm \-rf**

Możliwość wykonywania poleceń systemowych przez LLM to obosieczny miecz. Narzędzie run\_shell\_command pozwala agentowi m.in. klonować repozytoria, instalować pakiety czy stawiać środowiska testowe.23 Ponieważ model potrafi generować własne ciągi komend, Google musiało zaimplementować wysoce restrykcyjny silnik weryfikacji i bezpieczeństwa (Policy Engine).48

Architektura kontroli dostępu powłoki (Shell Execution Security) bazuje na kilku filarach:

1. **Zakaz łańcuchowania komend (Command Chaining Disabled):** Podatność wielu starszych agentów leży w braku głębokiego parsowania komend. Jeśli blokada obejmuje komendę rm, model mógłby złośliwie wygenerować echo "test" && rm \-rf /. W Gemini CLI narzędzie automatycznie rozbija ciągi wykorzystujące konstrukcje &&, ||, |, czy średniki ;.49 Każdy fragment łańcucha walidowany jest oddzielnie – jeśli jakikolwiek ułamek ciągu znajduje się na czarnej liście, blokowana jest cała komenda.49  
2. **Bezwzględny priorytet Blocklist (tools.exclude):** Silnik bazuje na dopasowywaniu prefiksów. Administrator może skonfigurować tablicę tools.exclude w pliku .gemini/settings.json. Konfiguracja zapisu \["run\_shell\_command(rm)"\] blokuje permanentnie każde odwołanie zaczynające się od usunięcia pliku (rm \-rf / czy rm file.txt), nadpisując wszelkie inne mechanizmy autoryzacji. Nawet jeśli model w swej usilnej dedukcji będzie domagał się skasowania błędnego artefaktu, zderzy się z twardą, lokalną barierą bezpieczeństwa o najwyższym priorytecie (100).18  
3. **Sandboxing i ograniczenia katalogów (Directory Restriction):** Dla bezkompromisowej izolacji kodu ze źródeł trzecich (np. instalowania paczek NPM z potencjalnymi trojanami), system wywołań powłoki obsługuje uruchamianie środowisk w izolacji (Sandboxing) wyzwalanych przełącznikiem \--sandbox lub środowiskową konfiguracją Docker.51 Gemini wspiera technologię Bubblewrap na maszynach wirtualnych (gVisor/runsc), która tworzy twarde granice przestrzeni nazw w systemie Linux (namespaces) oraz blokuje potoki sieciowe. Na urządzeniach z macOS wykorzystywany jest mechanizm jądra "Seatbelt" z profilem permissive-open, twardo blokującym możliwość nadpisywania struktur poza drzewem zdefiniowanych i zaufanych katalogów.52

### **Tryb YOLO (--yolo / \-y): Psychologia i ryzyko pełnej autonomii**

Domyślna praca w Gemini CLI bazuje na cyklu Human-in-the-Loop (HITL), w którym każda modyfikacja dysku czy wywołanie komendy wymaga podjęcia akcji ze strony użytkownika – ręcznego naciśnięcia klawisza akceptacji (Allow once / Allow always).48 Tryb ten chroni, ale przerywa przepływ skupienia (flow state) programisty. Rozwiązaniem tego wyzwania jest agresywny tryb przełącznika \--yolo (You Only Live Once).56

Wprowadzenie tej flagi w terminalu eliminuje prośby o autoryzację. Agent otrzymuje autorytarną władzę decyzyjną do modyfikowania, czytania i testowania całości wskazanego środowiska aż do pełnego osiągnięcia sformułowanego celu.55

**Wyjaśnienie psychologii i potencjału:**

Mechanika ta buduje całkowicie nową interakcję z kodem. Wyobraź sobie sytuację tworzenia narzędzia webowego od podstaw. Wpisujesz komendę:

gemini \-y "Stwórz skrypt NodeJS do przetwarzania obrazków i uruchom go."

Agent wygeneruje skrypt używający popularnej biblioteki sharp i natychmiast go wywoła (node script.js). Środowisko Node odrzuci wykonanie wypluwając ogromny błąd: Error: Cannot find module 'sharp'. W normalnym warunkach proces zakończyłby się niepowodzeniem. W trybie YOLO model odczytuje treść błędu przez przechwycenie strumienia błędów z systemu (stderr), przeprowadza błyskawiczną iterację analizy ("Aha, użyłem zewnętrznej paczki, ale jej nie ma w środowisku"), po czym całkowicie sam wpisuje w powłokę komendę weryfikacyjną środowisko pakietów npm install sharp. Śledzi poprawność budowania biblioteki C++, a gdy instalacja kończy się sukcesem (kod wyjścia 0), agent powraca do komendy node script.js. Generuje odpowiedź: "Wykryłem brak niezbędnych bibliotek, doinstalowałem je na nowo przez npm. Skrypt przetwarza obrazy." Ten auto-leczący się (self-healing) ciąg zdarzeń zmienia asystenta w kompetentnego, autonomicznego pracownika.21

**Ryzyko:** Tryb ten to prosta droga do katastrofy w środowiskach produkcyjnych (ang. *yoloing straight into production*). Z powodu halucynacji model może wpaść w pętlę nieskończoną – poszukując rozwiązania problemu ze zbugowanym procesem, agent potrafi rekurencyjnie usuwać poprawne pliki konfiguracyjne, czy pobierać zakażone literówkami złośliwe paczki.55 Stosowanie YOLO bez dodatkowej wirtualizacji powłoki (--sandbox) jest wysoce niezalecane przy inżynierii z użyciem obcych, nieudokumentowanych repozytoriów.

## **3\. Konfiguracja "Pro" i Plik GEMINI.md**

Sukces systemów agentowych leży w precyzji wstrzykniętych ograniczeń. Metodologia Context Engineering w przypadku Gemini CLI odchodzi od przerośniętych, spuchniętych promptów na rzecz inteligentnej i hierarchicznej konfiguracji struktury plików instruktarzowych.59

### **Architektura plików GEMINI.md**

Pliki te stanowią bazę "długoterminowej pamięci" systemu. Ich rozkład w strukturze katalogów nie jest przypadkowy. Mechanizm ContextManager w pakiecie core CLI stosuje potężną architekturę dziedziczenia.60 Poszukiwania rozpoczynają się od globalnego pliku użytkownika ulokowanego na najwyższym poziomie (\~/.gemini/GEMINI.md). Zapewnia on rdzenny, niezmienny styl pracy (np. dla konkretnego inżyniera). W następnej kolejności weryfikowany jest plik w katalogu głównym projektu, dopełniany opcjonalnymi podzbiorami plików GEMINI.md ukrytych niżej w komponentach aplikacji (JIT Context Files). Najbardziej szczegółowe polecenia podkatalogów bezlitośnie nadpisują polecenia ogólne.61 Pozwala to utrzymać doskonałą organizację i zabezpiecza LLM przed przeciążeniem i zjawiskiem tzw. "Context Rot", w którym wielowątkowe dyrektywy mieszają się i prowadzą do osłabienia możliwości rozumowania modelu.64

W potężnych, rozproszonych ekosystemach wczytywanie jednego monolitu konfiguracji byłoby fatalne w skutkach. Dlatego inżynierowie mogą też zastosować operatory wstrzyknięcia. Składnia oparta o słowo kluczowe ze znakiem małpy (np. @./shared/styleguide.md) umożliwia dynamiczne i rekursywne dodawanie podzbiorów markdowów, a inteligentne algorytmy pilnują pułapek cyrkulacji blokując pętle nieskończone na piątym zagnieżdżeniu struktury.65

### **Wzorzec: Idealny plik GEMINI.md dla automatyzacji w Pythonie**

Oto przykład kompleksowego pliku, który w brutalny sposób eliminuje błędy związane z pisaniem kodu w Pythonie, formatując model do poziomu inżyniera "Senior":

# **Project: Automatyzacja n8n i mikroserwisy**

## **General Guidelines**

* Zawsze traktuj mnie jako zaawansowanego Senior Developera. Nie marnuj czasu na wyjaśnianie banałów ani dokumentacji podstawowej.68  
* Używamy wyłącznie Pythona w wersji 3.12 lub nowszej.69

## **Dependency Management**

* Bezwzględnie korzystaj z narzędzia uv do zarządzania pakietami. Jeśli zajdzie konieczność postawienia skryptu, użyj uv pip install wewnątrz środowiska wirtualnego, a dla jednorazowych egzekucji globalnych narzędzi korzystaj z uvx.68

## **Code Standards**

* **Type Hinting**: Funkcje, klasy i zmienne MUST posiadać statyczne i ścisłe adnotacje typów (Type Hints) wyciągnięte ze standardowej biblioteki Pythona (typing).71  
* **Testy**: Uznaj implementację za niezakończoną, dopóki nie zostanie poparta strukturą testów jednostkowych. Pisz testy korzystając wyłącznie z frameworka pytest. Gwarantuj przynajmniej 80% pokrycia dla nowej logiki (Code Coverage).72

## **Edycja i Komentarze (Kluczowe)**

* **Oszczędne komentarze**: Dodawaj nowe komentarze z ogromną powściągliwością. Komentarz ma tłumaczyć "dlaczego" (logika i uzasadnienie decyzji), a nie "co robi" dana linijka kodu.12  
* ZAKAZ usuwania: **Nigdy, pod żadnym pozorem**, nie modyfikuj, nie usuwaj, ani nie formatuj starych i istniejących już komentarzy, docstringów, ani kodu w obszarach, które nie podlegają bezpośrednio implementacji wymaganej przeze mnie cechy.12

### **Różnica w autoryzacji: Google AI Studio vs Vertex AI**

Dla przeciętnego użytkownika, wybór ścieżki uwierzytelniania diametralnie wpływa na tempo pracy i architekturę prywatności. Gemini CLI umożliwia autoryzację z wykorzystaniem zarówno deweloperskiego klucza z Google AI Studio, jak i infrastruktury Enterprise Google Cloud opartej na platformie Vertex AI.2

**Google AI Studio (Klucz API):** Rozwiązanie ukierunkowane dla indywidualistów, pasjonatów i błyskawicznego powoływania prototypów. Skonfigurowanie tego zajmuje ułamek sekundy przez prosty export środowiskowy zmiennej poleceniem export GEMINI\_API\_KEY="....2 *Zalety:* Oferuje potężny i darmowy (Free Tier) próg użycia. Jako przeciętny power-user otrzymujesz do dyspozycji nawet do 1000 zapytań dziennie, odświeżanych w ramach modeli takich jak szybki Gemini Flash (60 na minutę). Idealne, dopóki tworzysz oprogramowanie Open Source lub projekty po godzinach.2 W płatnym trybie koszty są fenomenalnie tanie dla programisty niezależnego – za Gemini 3.1 Pro płacimy jedynie $2,00 za milion tokenów wejściowych i $12,00 za milion wyjściowych (w standardowym rozmiarze okna do 200 tysięcy, powyżej kwoty podwajają się).15 *Wady (Prywatność):* Opcja darmowa z Google AI Studio skrywa "ciemną stronę" – klauzule Terms of Service otwarcie deklarują, iż Google zastrzega sobie bezwarunkowe prawo, aby analizować twoje promptowane kody i używać przesłanych poleceń do przyszłego ulepszania i treningu mechanicznych wag swoich modeli.14 Tylko płatna subskrypcja wyklucza te zapisy.77

**Vertex AI (Enterprise):** Skierowany ku dużym jednostkom, zespołom deweloperskim z umowami NDA. Agent weryfikuje się tu zmienną GOOGLE\_GENAI\_USE\_VERTEXAI oraz identyfikatorem projektu GOOGLE\_CLOUD\_PROJECT.2 *Zalety:* Pełna zgodność prawna i prywatności z ramami zarządzania (AI Governance). Wyklucza to przetwarzanie kodu własnego korporacji do poprawy globalnego modelu – system podlega pod architekturę chmurową o wysokich standardach (np. SOC2, HIPAA), objętą ścisłą umową o gwarantowanym poziomie świadczenia usług (SLA) i brakiem użycia logów klienta.77 Umożliwia wybór globalnego regionu przetwarzania, co minimalizuje ping zapytania od twojego terminala do Data Center Google.77 *Wady:* Wymaga skrupulatnej konfiguracji z gcloud CLI i posiadania ról typu "Vertex AI User" na instancji GCP.

**Która opcja jest lepsza?** Dla przeciętnego power-usera tworzącego automatyzacje w systemach, wybór Google AI Studio (wersja Pay-As-You-Go podpięta z drobnym kredytem) jest obiektywnie najszybszą i najtańszą platformą wejścia. Gwarantuje ochronę przesyłanego kodu przed treningami modeli bez żmudnej konfiguracji korporacyjnej GCP, minimalizując tym samym koszt operacyjny (TCO).

## **4\. Scenariusze "YouTube Gold" (Clickbaitowe Case Studies)**

Demonstracja na żywo siły narzędzia wymaga wyjścia poza oklepane generowanie "kalkulatora" i ukazanie złożonego strumienia roboczego (agentic workflows). Wszystkie demonstracje powinny być odpalane ze wstrzykniętą flagą pełnej swobody decyzyjnej \--yolo (-y).

### **Scenariusz A (Fix My Automation)**

*Kontekst:* W starszym, ręcznie sklejanym automatycznym pobieraczu ofert cenowych nagle przestają wpadać zyski, ponieważ struktura strony z cennikiem zmieniła się wizualnie. Skrypt sypie błędem Selenium "Element Not Found".

*Komenda:*

gemini \-y "Mój stary skrypt scraper.py wykorzystujący Selenium przestał działać dla strony https://example-target.com/prices. Użyj narzędzia web\_fetch, aby wyciągnąć i ocenić najnowszy kod HTML tej strony. Porównaj stary schemat DOM ukryty w scraperze z nowym, napraw selektory lokalnie, podmień je i uruchom testowo skrypt pythonem by zweryfikować czy plik pobiera prawidłowo zawartość JSON z nową architekturą."

*Przewidywany Flow agenta:*

1. Agent wywoła systemowe read\_file analizując zmienne selektorów ukryte w scraper.py (np. .product-box h2).  
2. Rozpocznie ekstrakcję przez wbudowane API, ładując na zrzut okna URL z zadania przy pomocy wbudowanego bloku web\_fetch.41  
3. Dedukując niezgodności między strukturami DOM (stare kontenery div stały się teraz np. znacznikami .grid-price-card), połączy fakty, tworząc abstrakcyjne drzewo modyfikacji.  
4. Skorzysta z mutacyjnej operacji w tle wykonując komendę wymiany bloków przez narzędzie replace, a na koniec wykorzysta run\_shell\_command i upewni się uruchamiając kompilator Pythona, aby zademonstrować użytkownikowi w zaledwie ułamek sekundy magiczny napis terminala Status 200, items extracted: 14\. Twórca obserwuje pełną, samouzdrawiającą się architekturę deweloperską.

### **Scenariusz B (Repo Architect)**

*Kontekst:* Rozwiązanie, w którym klasyczne ChatGPT natychmiastowo gubi wątek po zderzeniu z wieloma odniesieniami do kodu. Widz dostarcza gigantyczny archiwum (200 niekompletnych i starych plików Java lub C++) z wyzerowaną dokumentacją.

*Komenda:*

gemini \-y "Mam tu obce repozytorium z wieloma skryptami bez wiedzy o architekturze. Skorzystaj z narzędzia codebase\_investigator w celu prześwietlenia pełnego repozytorium. Następnie stwórz centralny README.md oraz wygeneruj schemat architektury Mermaid obrazujący ścieżki i serwisy na nim. Ostatecznie, gdy skończysz, wylistuj mi z powrotem 3 luki bezpieczeństwa ukryte na twardo w plikach źródłowych."

*Przewidywany Flow agenta:*

1. Wykorzystanie 1 miliona tokenów natywnego wejścia poprzez podprogram codebase\_investigator, wyspecjalizowany pod systemową, głęboką mapę struktury oprogramowania.28 Prześwietli on kilkaset tysięcy linii tekstu i kodu w tle.  
2. Zrozumienie abstrakcyjnych powiązań między warstwami systemu, co zaskutkuje uruchomieniem modyfikacji pliku z poziomu OS'a zapisując zbadaną konfigurację systemu Mermaid dla wizualizacji.81  
3. Pomyślna analiza statyczna w poszukiwaniu zakodowanych na sztywno kluczy lub niebezpiecznych metod uwierzytelniania, wydrukowana prosto i bezpośrednio przed oczami programisty. Brak RAG'ów. Czysta potęga okna pamięci.59

### **Scenariusz C (n8n Power User)**

*Kontekst:* Specjaliści automatyzacji platform no-code jak n8n notorycznie borykają się z wyzwaniami własnego backendu, gdyż logika wizualna często blokuje ciężkie zadania operacyjne.

*Komenda:*

gemini \-y "Stwórz lokalny, minimalny serwer na bazie FastAPI, pełniący funkcję potężnego i wydajnego endpointa POST, który n8n wykorzysta do webhooków. Logika ma parsnąć wpisy do pliku SQLite przy pomocy Type Hinting z biblioteki Pydantic. Przygotuj plik z zależnościami pod standardowe środowisko dla dockera, oraz skompiluj Dockerfile gotowy na natychmiastowy i produkcyjny deploy, bez zapytań o modyfikację."

*Przewidywany Flow agenta:*

1. Seria iteracyjnych zapisów przez program: Generacja i stworzenie pliku skryptowego API opartego o architekturę Pydantic oraz instancji FastAPI.  
2. Konstrukcja zarysu tabeli dla lekkiej relacyjnej bazy SQLite i mechanizmów zapisu.  
3. Operacyjne wygenerowanie przez system gotowego środowiska requirements.txt lub konfiguracyjnego uv, oraz optymalnego wagi skryptu kompilacyjnego bazowego kontenera (Dockerfile, wariant slim). Użytkownik n8n dostaje produkcyjnie gotowe i kompletne repozytorium, po czym może je uruchomić jedną komendą na VPS bez pisania jednej linijki kodu.23

## **5\. Gemini CLI vs Claude Code (Bezpośrednie Starcie)**

W branży zaawansowanych systemów powłok systemowych, konfrontacja między gigantami roku 2026 – Anthropic a Google, budzi niezrównane emocje. Ostatnie zestawienia pokazują zderzenie asystentów Claude Code, obsługiwanego najnowszym silnikiem Claude 4.6 (Sonnet/Opus) z opisywanym narzędziem Gemini CLI opartym o Gemini 3.1 Pro.85

Tabela "No-Bullshit" konfrontująca te rozwiązania z bezlitosną logiką deweloperską:

| Analiza / Kategoria | Gemini CLI (Gemini 3.1 Pro) | Claude Code (Claude 4.6 Sonnet/Opus) | Merytoryczny Werdykt Inżyniera |
| :---- | :---- | :---- | :---- |
| **Cena (Optymalizacja Kosztów)** | Niezrównany i rozbudowany model dostępu darmowego (do 1000 zapytań na 24h w AI Studio). Niskie koszty eksploatacji masowej przy API (ok. $2,00 na 1M wejścia, $12,00 na wyjściu). Z potężnym cięciem ceny rzędu 75% przy korzystaniu z buforowanego kontekstu (cache).14 | Narzędzie premium przeznaczone dla komercji, obłożone wyłącznie barierą stałych subskrypcji lub potężnego wydatku na płatne API. Cennik dla wybitnego i topowego modelu Opus jest obarczony cennikiem rzędu $15/1M in oraz $75/1M out.76 | **Gemini CLI** to absolutny lider, bezlitośnie miażdżąc w testach próg wejścia w zaawansowane środowiska dla startupów i zespołów developerskich.86 Koszt tokenów outputowych w Claude jest w niektórych zastosowaniach aż siedmiokrotnie wyższy.86 |
| **Kontekst (Pojemność operacyjna i repozytoria)** | Gigantyczne architektonicznie natywne wchłanianie powyżej 1 miliona do nawet 2 milionów tokenów (Context King). Natychmiastowa ocena projektów w całości bez wycinkowania (RAG).1 | Solidne i potężne, ale mocno dławione architekturą 200 tysięcy tokenów wyjściowych okno kontekstowe.6 Doskonale zoptymalizowane pod kątem buforowania, ale zawodne przy analizowaniu rozbudowanych monolitów Legacy.88 | **Gemini** wychodzi z tego jako zdecydowany zwycięzca tam, gdzie konieczna jest potężna analiza wielkiej liczby plików równocześnie. |
| **Narzędzia i Przeszukiwanie Internetu** | Narzędzie do ugruntowania google\_web\_search potrafi precyzyjnie operować wiedzą w czasie rzeczywistym wspartą rozbudowanym, bezpośrednim formatowaniem strony i wysysaniem witryny. Ekosystem poszerzony jest darmową implementacją oficjalnych rozszerzeń MCP.31 | Słabsza implementacja integracji real-time internetowych, jednak system z wybitnym, organicznym wsparciem precyzji edycji środowiskowych poleceń shellowych. Mechanizmy decyzyjne i uodpornienie na błędy (Error handling) oceniane na nieco wyższe i mocniejsze niż konkurencja.87 | **Remis zależny od potrzeb.** W pracy n8n i API, kiedy szukasz na gwałt rozwiązań z nową, nieznaną dotąd dokumentacją, wbudowany Google w Gemini zadziała szybciej.38 Claude za to bywa lepszy w izolowanych zamkniętych kodach, oferując wysoce głęboką precyzję napraw na skomplikowanym poziomie trudności.4 |
| **Szybkość (Latencja Outputów)** | Skupia się na błyskawicznym (flash / vibe coding) prototypowaniu, szybciej przelewając do bufora terminala duże obiekty abstrakcji systemowych i bloki plikowe. Z prędkością wyprowadzania do 105.8 tokenów na sekundę, miażdży pod kątem wyścigu tworzenia masywnego boilerplate.89 | Claude Sonnet skupia się z niezwykłą dozą pedantyzmu na wyłapywaniu mrocznych bugów i krawędzi (Edge Case) logicznego rozumowania (Deep Think). W przypadku trudnych algorytmów deklasuje Gemini swoją inteligencją w tworzeniu czystego logowania (Output: ok. 72.2 t/s).89 | **Gemini** to król deweloperskiego sprintu do rzucania dużych brył kodu. Claude to precyzyjny architekt do analitycznego debuggingu i powolnych interwencji nad krytycznym modułem produkcyjnym. |

## **6\. Ograniczenia i "Ciemna Strona"**

Prowadząc profesjonalny warsztat narzędzi nie wolno zamazywać ryzyk. Środowisko Gemini to bardzo awangardowa architektura pociągająca ze sobą mroczniejsze elementy rzemiosła cyfrowego, które dla infrastruktury mogą stać się niezwykle destrukcyjne.

1. **Halucynacje Architektoniczne w ścieżkach i Gnicie Kontekstu (Context Rot):** Gigantyczny bufor pamięci potrafi doprowadzić do przedawkowania informacji. Agenty bywają nieostrożne i zapychają pliki setkami instrukcji. Następuje powolna zapaść (tzw. "Gnicie Kontekstu" – rot). Ślepota agentowa polega w takich przypadkach na uporczywym wzywaniu funkcji read\_file z absurdalnymi literówkami lub błędnymi, kompletnie nieistniejącymi podkatalogami w systemie bez sprawnie uprzedniego zastosowania weryfikującego polecenia powłoki ls. Następuje przez to bolesna pętla błędów uderzających w terminal i brak poprawnej konkluzji programu.64  
2. **Kaganiec przepustowości systemowej (Rate Limits):** Limity operacyjne bywają niekiedy zbyt mocnym tłumikiem dla szybkich iteracji. Chociaż 1000 żądań bezpłatnych robi powalające wrażenie na papierze, to realne okno 60 wywołań w przeciągu jednej minuty potrafi być bardzo szybko spalone przez pętlę narzędziową. Posiadając zadanie dla podmodułu codebase\_investigator, który błyskawicznie emituje powłokom potężne sterty żądań w systemie na analizie i iteruje się rekursyjnie przez pliki, inżynier doświadcza momentalnego uderzenia w "szklany sufit" przesyłu limitów bazy API, co zamraża system i zmusza do wstrzymania procesów powłoki systemowej.75  
3. **Prywatność i Wektory Ataku Cichych Zależności:** Jednym z najbardziej drażliwych mankamentów architektury są tzw. wektory ataku zdefiniowane na ukrytych podzbiorach uśpionego wektora w promptowaniu wejściowym (tzw. zjawisko *Prompt Injection*). Eksperci ds. ataków cybernetycznych i bezpieczeństwa, m.in. pracownicy zespołów badawczych Tracebit odkryli tzw. ukrytą metodologię przejęcia wiersza w Gemini CLI, polegającą na przemyceniu ukrytego "zatrutego" pliku konfiguracyjnego GEMINI.md na etapie zaciągania przez niczego niespodziewającego się programistę do dysku, obcego folderu z otwartego systemu GitHub. Agresywna pętla odczytu pliku może omijać zasady weryfikacji manualnej HITL, sprowadzając maszynę lokalną do niezauważonej ekstrakcji ukrytych systemowo zaszyfrowanych tokenów prywatnych np. usług AWS do agresorów i po kryjomu niszczyć ślady ukrywając wynik zrzutu błędu, poprzez sprytne wyłuskanie komend formatujących.93 Dla zniwelowania i całkowitego powstrzymania katastrof naturalnych u dewelopera, wymagane jest stosowanie hermetycznych komend Docker/gVisor w terminalu izolacji dla wywoływanego powłokowo API i kontenerów przez bezwarunkową zaporę \--sandbox dla testowych integracji.52  
4. **Klauzula treningowa i ryzyko dla firmy:** Mrok prywatności tkwi w niuansach darmowych kont (Google AI Studio z logowaniem OAuth). W tym trybie logi deweloperskie kodów programisty – wszystkie struktury i instrukcje ukryte – powędrują bezpowrotnie prosto do globalnej pralki uczenia modeli Google (żeby wspomagać rozwój narzędzi).77 Taki proces dla specyfikacji objętej srogą tajemnicą handlową (Enterprise/NDA) oznacza momentalne zwolnienie dyscyplinarne. Remedium wymaga obligatoryjnego przełączenia powłoki CLI na rygorystyczny tryb pracy uwierzytelniający z subskrypcyjnego API korporacji z usług Google Vertex AI, w którym wywoływania API bezwzględnie zostają wyłączone ze żniw zapytań szkoleniowych bazy danych centralnej wyszukiwarki i zapewniają zgodność RODO / CDPA.77

### **Metoda montażu YouTube: Rzeźnia Okna Kontekstowego**

Zasugerowany test do montażu "Igła w stogu siana" (Needle in a Haystack) udowodni namacalnie wartość rozwiązania. Przerzuć dziesiątki skompresowanych tysięcy linii baz konfiguracyjnych i dokumentów na obszar katalogów. Następnie wpisz we wnętrzu setnej kartki pliku na samym jej dnie absurdalnie mylący "sekretny klucz" i poproś by Gemini znalazł go dla celów zmiany. Pokazując ekran na żywo użytkownikom Youtube, jak błyskawicznie Gemini CLI wchłania cały zrzut bez cięcia tekstu na fragmenty (RAG), podczas gdy starsze technologie dławią się na braku bufora, osiągasz moment prawdziwej "magii", po którym wszyscy specjaliści przejdą z czatów do narzędzia terminala CLI w codziennym użytku operacyjnym.96

#### **Cytowane prace**

1. Long context | Gemini API \- Google AI for Developers, otwierano: marca 11, 2026, [https://ai.google.dev/gemini-api/docs/long-context](https://ai.google.dev/gemini-api/docs/long-context)  
2. google-gemini/gemini-cli: An open-source AI agent that brings the power of Gemini directly into your terminal. \- GitHub, otwierano: marca 11, 2026, [https://github.com/google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli)  
3. Gemini 3.1 Pro: A smarter model for your most complex tasks \- The Keyword, otwierano: marca 11, 2026, [https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-pro/](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-pro/)  
4. Claude Code vs. Gemini CLI vs. Cursor vs. Qwen Code — Comparing Top AI Coding Assistant | by Fendy Feng | Medium, otwierano: marca 11, 2026, [https://medium.com/@fendylike/top-ai-coding-assistants-claude-code-vs-gemini-cli-vs-cursor-vs-qwen-code-0bc759fc9d45](https://medium.com/@fendylike/top-ai-coding-assistants-claude-code-vs-gemini-cli-vs-cursor-vs-qwen-code-0bc759fc9d45)  
5. Top 5 CLI Coding Agents in 2026 \- DEV Community, otwierano: marca 11, 2026, [https://dev.to/lightningdev123/top-5-cli-coding-agents-in-2026-3pia](https://dev.to/lightningdev123/top-5-cli-coding-agents-in-2026-3pia)  
6. Claude Sonnet 4.6 (Non-reasoning, Low Effort) vs Gemini 2.5 Pro: Model Comparison, otwierano: marca 11, 2026, [https://artificialanalysis.ai/models/comparisons/claude-sonnet-4-6-non-reasoning-low-effort-vs-gemini-2-5-pro](https://artificialanalysis.ai/models/comparisons/claude-sonnet-4-6-non-reasoning-low-effort-vs-gemini-2-5-pro)  
7. Gemini 3.1 Pro Preview vs Claude Opus 4.6 (Non-reasoning, High Effort) \- Artificial Analysis, otwierano: marca 11, 2026, [https://artificialanalysis.ai/models/comparisons/gemini-3-1-pro-preview-vs-claude-opus-4-6](https://artificialanalysis.ai/models/comparisons/gemini-3-1-pro-preview-vs-claude-opus-4-6)  
8. SWE-Pruner: Self-Adaptive Context Pruning for Coding Agents \- arXiv.org, otwierano: marca 11, 2026, [https://arxiv.org/html/2601.16746v1](https://arxiv.org/html/2601.16746v1)  
9. RAG vs Large Context Models: A Gemini overview : r/LocalLLaMA \- Reddit, otwierano: marca 11, 2026, [https://www.reddit.com/r/LocalLLaMA/comments/1c0iea2/rag\_vs\_large\_context\_models\_a\_gemini\_overview/](https://www.reddit.com/r/LocalLLaMA/comments/1c0iea2/rag_vs_large_context_models_a_gemini_overview/)  
10. Optimize your prompt size for long context window LLMs | by Karl Weinmeister \- Medium, otwierano: marca 11, 2026, [https://medium.com/google-cloud/optimize-your-prompt-size-for-long-context-window-llms-0a5c2bab4a0f](https://medium.com/google-cloud/optimize-your-prompt-size-for-long-context-window-llms-0a5c2bab4a0f)  
11. Gemini 3.1 Pro | Generative AI on Vertex AI \- Google Cloud Documentation, otwierano: marca 11, 2026, [https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-1-pro](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-1-pro)  
12. Gemini-cli System Prompt \- Discover gists · GitHub, otwierano: marca 11, 2026, [https://gist.github.com/chigkim/9547badac809e356b0ed005d8a35f7c1](https://gist.github.com/chigkim/9547badac809e356b0ed005d8a35f7c1)  
13. Retrieval-Augmented Code Generation: A Survey with Focus on Repository-Level Approaches \- arXiv.org, otwierano: marca 11, 2026, [https://arxiv.org/html/2510.04905v1](https://arxiv.org/html/2510.04905v1)  
14. Gemini Developer API pricing, otwierano: marca 11, 2026, [https://ai.google.dev/gemini-api/docs/pricing](https://ai.google.dev/gemini-api/docs/pricing)  
15. Gemini 3.1 Pro Pricing in 2026: Token Costs, Caching, Thinking Tokens & How to Avoid Bill Shock \- Verdent, otwierano: marca 11, 2026, [https://www.verdent.ai/guides/gemini-3-1-pro-pricing](https://www.verdent.ai/guides/gemini-3-1-pro-pricing)  
16. Context caching overview | Generative AI on Vertex AI \- Google Cloud Documentation, otwierano: marca 11, 2026, [https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview)  
17. Gemini CLI | Gemini Code Assist \- Google for Developers, otwierano: marca 11, 2026, [https://developers.google.com/gemini-code-assist/docs/gemini-cli](https://developers.google.com/gemini-code-assist/docs/gemini-cli)  
18. Building Effective AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned \- arXiv, otwierano: marca 11, 2026, [https://arxiv.org/html/2603.05344v2](https://arxiv.org/html/2603.05344v2)  
19. Gemini CLI Architecture Overview \- GitHub Pages, otwierano: marca 11, 2026, [https://google-gemini.github.io/gemini-cli/docs/architecture.html](https://google-gemini.github.io/gemini-cli/docs/architecture.html)  
20. Beyond the Command Line: Unpacking the AI Agent Power of Gemini CLI \- Oreate AI Blog, otwierano: marca 11, 2026, [https://www.oreateai.com/blog/beyond-the-command-line-unpacking-the-ai-agent-power-of-gemini-cli/eeb93628aa2dfa9fd89ae1acdbf9c53e](https://www.oreateai.com/blog/beyond-the-command-line-unpacking-the-ai-agent-power-of-gemini-cli/eeb93628aa2dfa9fd89ae1acdbf9c53e)  
21. How to Get Started and Build with Gemini CLI (Powered by Gemini 3 Flash) \- Dev.to, otwierano: marca 11, 2026, [https://dev.to/leslysandra/how-to-get-started-and-build-with-gemini-cli-powered-by-gemini-3-flash-2j11](https://dev.to/leslysandra/how-to-get-started-and-build-with-gemini-cli-powered-by-gemini-3-flash-2j11)  
22. How to Use Gemini CLI: Complete Guide for Developers and Beginners \- MPG ONE, otwierano: marca 11, 2026, [https://mpgone.com/how-to-use-gemini-cli-complete-guide-for-developers-and-beginners/](https://mpgone.com/how-to-use-gemini-cli-complete-guide-for-developers-and-beginners/)  
23. The run shell command is cause a loop · Issue \#13977 · google-gemini/gemini-cli \- GitHub, otwierano: marca 11, 2026, [https://github.com/google-gemini/gemini-cli/issues/13977](https://github.com/google-gemini/gemini-cli/issues/13977)  
24. Gemini CLI \- Google's Free AI Agent for Developers \- CSNAINC, otwierano: marca 11, 2026, [https://csnainc.io/introduction-to-gemini-cli/](https://csnainc.io/introduction-to-gemini-cli/)  
25. Prioritize and Expose the Experimental Agent Framework · google-gemini gemini-cli · Discussion \#12832 \- GitHub, otwierano: marca 11, 2026, [https://github.com/google-gemini/gemini-cli/discussions/12832](https://github.com/google-gemini/gemini-cli/discussions/12832)  
26. Recording of AI book club session of 'Hands-On Large Language Models: Language Understanding and Generation', by Jay Alammar and Maarten Grootendorst \- I'd Rather Be Writing blog, otwierano: marca 11, 2026, [https://idratherbewriting.com/blog/book-club-hands-on-llms](https://idratherbewriting.com/blog/book-club-hands-on-llms)  
27. Applied AI Skills Explorer \- Frontier Firm Assessment & Development Velocity, otwierano: marca 11, 2026, [https://www.openagentschool.org/ai-skills](https://www.openagentschool.org/ai-skills)  
28. gemini-3.1-pro-preview 100% Error Rate \- Infinite loading/Timeout (Windows/v0.32.1), otwierano: marca 11, 2026, [https://github.com/google-gemini/gemini-cli/issues/21937](https://github.com/google-gemini/gemini-cli/issues/21937)  
29. zamalali/langchain-code: Gemini-cli or claude code? Why not both? LangCode combines all CLI capabilities and models in one place ☂️\! \- GitHub, otwierano: marca 11, 2026, [https://github.com/zamalali/langchain-code](https://github.com/zamalali/langchain-code)  
30. How to Build an MCP Server with Gemini CLI and Go | Google Codelabs, otwierano: marca 11, 2026, [https://codelabs.developers.google.com/cloud-gemini-cli-mcp-go](https://codelabs.developers.google.com/cloud-gemini-cli-mcp-go)  
31. MCP servers with the Gemini CLI, otwierano: marca 11, 2026, [https://geminicli.com/docs/tools/mcp-server/](https://geminicli.com/docs/tools/mcp-server/)  
32. Announcing official MCP support for Google services | Google Cloud Blog, otwierano: marca 11, 2026, [https://cloud.google.com/blog/products/ai-machine-learning/announcing-official-mcp-support-for-google-services](https://cloud.google.com/blog/products/ai-machine-learning/announcing-official-mcp-support-for-google-services)  
33. Building MCP Servers the Right Way: Security, Standards, and Cross-Platform Design, otwierano: marca 11, 2026, [https://crunchtools.com/building-mcp-servers-the-right-way-security-standards-and-cross-platform-design/](https://crunchtools.com/building-mcp-servers-the-right-way-security-standards-and-cross-platform-design/)  
34. Gemini CLI Tutorial Series — Part 8: Building your own MCP Server \- Medium, otwierano: marca 11, 2026, [https://medium.com/google-cloud/gemini-cli-tutorial-series-part-8-building-your-own-mcp-server-74d6add81cca](https://medium.com/google-cloud/gemini-cli-tutorial-series-part-8-building-your-own-mcp-server-74d6add81cca)  
35. Gemini CLI Deep-Dive | Google Codelabs, otwierano: marca 11, 2026, [https://codelabs.developers.google.com/gemini-cli-deep-dive](https://codelabs.developers.google.com/gemini-cli-deep-dive)  
36. Gemini CLI \+ Google MCPs: Migrate & deploy full stack apps, otwierano: marca 11, 2026, [https://www.youtube.com/watch?v=SeuhYVg8-AU](https://www.youtube.com/watch?v=SeuhYVg8-AU)  
37. \[Subagents\] Add mechanism for isolating the tools of subagents from the main agent. · Issue \#21901 · google-gemini/gemini-cli \- GitHub, otwierano: marca 11, 2026, [https://github.com/google-gemini/gemini-cli/issues/21901](https://github.com/google-gemini/gemini-cli/issues/21901)  
38. Web search and fetch | Gemini CLI, otwierano: marca 11, 2026, [https://geminicli.com/docs/cli/tutorials/web-tools/](https://geminicli.com/docs/cli/tutorials/web-tools/)  
39. Practical Gemini CLI: A Deep Dive into AI Planning — Part 1 \- Medium, otwierano: marca 11, 2026, [https://medium.com/google-cloud/practical-gemini-cli-a-deep-dive-into-ai-planning-2ece2f8ed369](https://medium.com/google-cloud/practical-gemini-cli-a-deep-dive-into-ai-planning-2ece2f8ed369)  
40. A Guide to Tool Calling with the TypeScript AI SDK \- Telerik.com, otwierano: marca 11, 2026, [https://www.telerik.com/blogs/guide-tool-calling-typescript-ai-sdk](https://www.telerik.com/blogs/guide-tool-calling-typescript-ai-sdk)  
41. Web Fetch Tool (web\_fetch) | gemini-cli \- GitHub Pages, otwierano: marca 11, 2026, [https://google-gemini.github.io/gemini-cli/docs/tools/web-fetch.html](https://google-gemini.github.io/gemini-cli/docs/tools/web-fetch.html)  
42. gemini-research-browser-use | Skills... \- LobeHub, otwierano: marca 11, 2026, [https://lobehub.com/fr/skills/neversight-skills\_feed-gemini-research-browser-use](https://lobehub.com/fr/skills/neversight-skills_feed-gemini-research-browser-use)  
43. Best Gemini URL Context Tool Alternative for AI Agents \- ScrapeGraphAI, otwierano: marca 11, 2026, [https://scrapegraphai.com/blog/gemini-url-context-alternative](https://scrapegraphai.com/blog/gemini-url-context-alternative)  
44. agentforce/adk \- NPM, otwierano: marca 11, 2026, [https://www.npmjs.com/package/@agentforce/adk](https://www.npmjs.com/package/@agentforce/adk)  
45. github-mcp-setup | Skills Marketplace · LobeHub, otwierano: marca 11, 2026, [https://lobehub.com/it/skills/kingdon-skills-github-mcp-setup](https://lobehub.com/it/skills/kingdon-skills-github-mcp-setup)  
46. Generative AI \- MATLAB Central Discussions \- MathWorks, otwierano: marca 11, 2026, [https://www.mathworks.com/matlabcentral/discussions/ai.html](https://www.mathworks.com/matlabcentral/discussions/ai.html)  
47. Make Gemini less of a sycophant · Issue \#4556 \- GitHub, otwierano: marca 11, 2026, [https://github.com/google-gemini/gemini-cli/issues/4556](https://github.com/google-gemini/gemini-cli/issues/4556)  
48. Execute shell commands | Gemini CLI, otwierano: marca 11, 2026, [https://geminicli.com/docs/cli/tutorials/shell-commands/](https://geminicli.com/docs/cli/tutorials/shell-commands/)  
49. gemini-cli/docs/tools/shell.md at main \- GitHub, otwierano: marca 11, 2026, [https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/shell.md](https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/shell.md)  
50. Shell tool (\`run\_shell\_command\`) | Gemini \- Gemini CLI, otwierano: marca 11, 2026, [https://geminicli.com/docs/tools/shell/](https://geminicli.com/docs/tools/shell/)  
51. gemini-cli/docs/cli/sandbox.md at main \- GitHub, otwierano: marca 11, 2026, [https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/sandbox.md](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/sandbox.md)  
52. Sandboxing in the Gemini CLI, otwierano: marca 11, 2026, [https://geminicli.com/docs/cli/sandbox/](https://geminicli.com/docs/cli/sandbox/)  
53. AI coding at the command line with Gemini CLI \- InfoWorld, otwierano: marca 11, 2026, [https://www.infoworld.com/article/4025916/ai-coding-at-the-command-line-with-gemini-cli.html](https://www.infoworld.com/article/4025916/ai-coding-at-the-command-line-with-gemini-cli.html)  
54. Building Sandboxes into OpenCode: If You Give an LLM a Shell, You Lose (Part 2), otwierano: marca 11, 2026, [https://dev.to/uenyioha/building-sandboxes-into-opencode-if-you-give-an-llm-a-shell-you-lose-part-2-4f5o](https://dev.to/uenyioha/building-sandboxes-into-opencode-if-you-give-an-llm-a-shell-you-lose-part-2-4f5o)  
55. "Always Approve" Tool Permission Not Persisting Across Terminal Sessions · Issue \#4340 · google-gemini/gemini-cli \- GitHub, otwierano: marca 11, 2026, [https://github.com/google-gemini/gemini-cli/issues/4340](https://github.com/google-gemini/gemini-cli/issues/4340)  
56. Gemini sandbox | Docker Docs, otwierano: marca 11, 2026, [https://docs.docker.com/ai/sandboxes/agents/gemini/](https://docs.docker.com/ai/sandboxes/agents/gemini/)  
57. What is agentic coding? How it works and use cases | Google Cloud, otwierano: marca 11, 2026, [https://cloud.google.com/discover/what-is-agentic-coding](https://cloud.google.com/discover/what-is-agentic-coding)  
58. Gemini caught violating system instructions and responds with "you did it first" \- Reddit, otwierano: marca 11, 2026, [https://www.reddit.com/r/vibecoding/comments/1ron1np/gemini\_caught\_violating\_system\_instructions\_and/](https://www.reddit.com/r/vibecoding/comments/1ron1np/gemini_caught_violating_system_instructions_and/)  
59. Master Context Engineering with Gemini CLI: How to Build Smarter AI-Powered Workflows, otwierano: marca 11, 2026, [https://faraazmohdkhan.medium.com/master-context-engineering-with-gemini-cli-how-to-build-smarter-ai-powered-workflows-3445814f5968](https://faraazmohdkhan.medium.com/master-context-engineering-with-gemini-cli-how-to-build-smarter-ai-powered-workflows-3445814f5968)  
60. Refactor Hierarchical Memory Loading: Implement Dynamic, Just-in-Time Context · Issue \#11488 · google-gemini/gemini-cli \- GitHub, otwierano: marca 11, 2026, [https://github.com/google-gemini/gemini-cli/issues/11488](https://github.com/google-gemini/gemini-cli/issues/11488)  
61. Provide context with GEMINI.md files \- Gemini CLI, otwierano: marca 11, 2026, [https://geminicli.com/docs/cli/gemini-md/](https://geminicli.com/docs/cli/gemini-md/)  
62. Google Gemini CLI Cheatsheet \- Philschmid, otwierano: marca 11, 2026, [https://www.philschmid.de/gemini-cli-cheatsheet](https://www.philschmid.de/gemini-cli-cheatsheet)  
63. Gemini CLI configuration, otwierano: marca 11, 2026, [https://geminicli.com/docs/reference/configuration/](https://geminicli.com/docs/reference/configuration/)  
64. Practical Gemini CLI: Structured approach to bloated GEMINI.md | by Prashanth Subrahmanyam | Google Cloud \- Medium, otwierano: marca 11, 2026, [https://medium.com/google-cloud/practical-gemini-cli-structured-approach-to-bloated-gemini-md-360d8a5c7487](https://medium.com/google-cloud/practical-gemini-cli-structured-approach-to-bloated-gemini-md-360d8a5c7487)  
65. \[bug\] Gemini CLI tries to "import" any file / folder with a "@" symbol in the GEMINI.md file · Issue \#6952 \- GitHub, otwierano: marca 11, 2026, [https://github.com/google-gemini/gemini-cli/issues/6952](https://github.com/google-gemini/gemini-cli/issues/6952)  
66. Memory Import Processor \- Gemini CLI, otwierano: marca 11, 2026, [https://geminicli.com/docs/reference/memport/](https://geminicli.com/docs/reference/memport/)  
67. Use the Data Engineering Agent to build and modify data pipelines | BigQuery, otwierano: marca 11, 2026, [https://docs.cloud.google.com/bigquery/docs/data-engineering-agent-pipelines](https://docs.cloud.google.com/bigquery/docs/data-engineering-agent-pipelines)  
68. What's your Gemini CLI setup & settings.json look like? Need some inspiration : r/GeminiCLI, otwierano: marca 11, 2026, [https://www.reddit.com/r/GeminiCLI/comments/1oh61ts/whats\_your\_gemini\_cli\_setup\_settingsjson\_look/](https://www.reddit.com/r/GeminiCLI/comments/1oh61ts/whats_your_gemini_cli_setup_settingsjson_look/)  
69. GEMINI.md \- ShaojieJiang/orcheo \- GitHub, otwierano: marca 11, 2026, [https://github.com/ShaojieJiang/orcheo/blob/main/GEMINI.md](https://github.com/ShaojieJiang/orcheo/blob/main/GEMINI.md)  
70. Using Gemini CLI to Create a Gemini CLI Config Repo | by Dazbo (Darren Lester) | Google Cloud \- Medium, otwierano: marca 11, 2026, [https://medium.com/google-cloud/using-gemini-cli-to-create-a-gemini-cli-config-repo-519399e25d9a](https://medium.com/google-cloud/using-gemini-cli-to-create-a-gemini-cli-config-repo-519399e25d9a)  
71. Agentverse \- The Shadowblade's Codex \- Vibecoding with Gemini CLI | Google Codelabs, otwierano: marca 11, 2026, [https://codelabs.developers.google.com/agentverse-developer/instructions](https://codelabs.developers.google.com/agentverse-developer/instructions)  
72. pytest-brightest/GEMINI.md at main · AstuteSource/pytest-brightest, otwierano: marca 11, 2026, [https://github.com/AstuteSource/pytest-brightest/blob/main/GEMINI.md](https://github.com/AstuteSource/pytest-brightest/blob/main/GEMINI.md)  
73. html-to-markdown/GEMINI.md at main · Goldziher/html-to-markdown, otwierano: marca 11, 2026, [https://github.com/Goldziher/html-to-markdown/blob/main/GEMINI.md](https://github.com/Goldziher/html-to-markdown/blob/main/GEMINI.md)  
74. Gemini CLI \- Simon Willison's Weblog, otwierano: marca 11, 2026, [https://simonwillison.net/2025/Jun/25/gemini-cli/](https://simonwillison.net/2025/Jun/25/gemini-cli/)  
75. Gemini CLI: Quotas and pricing, otwierano: marca 11, 2026, [https://geminicli.com/docs/resources/quota-and-pricing/](https://geminicli.com/docs/resources/quota-and-pricing/)  
76. Gemini 3.1 Pro vs Claude Opus 4.6 Comprehensive Comparison: 10 Benchmark Test Results Reveal the Best Choice, otwierano: marca 11, 2026, [https://help.apiyi.com/en/gemini-3-1-pro-preview-vs-claude-opus-4-6-comparison-en.html](https://help.apiyi.com/en/gemini-3-1-pro-preview-vs-claude-opus-4-6-comparison-en.html)  
77. Migrate from Google AI Studio to Vertex AI | Generative AI on Vertex AI | Google Cloud Documentation, otwierano: marca 11, 2026, [https://docs.cloud.google.com/vertex-ai/generative-ai/docs/migrate/migrate-google-ai](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/migrate/migrate-google-ai)  
78. Run Gemini CLI \- GitHub Marketplace, otwierano: marca 11, 2026, [https://github.com/marketplace/actions/run-gemini-cli](https://github.com/marketplace/actions/run-gemini-cli)  
79. What is the difference between AI Studio and Vertex ? : r/Bard \- Reddit, otwierano: marca 11, 2026, [https://www.reddit.com/r/Bard/comments/1oq4tfb/what\_is\_the\_difference\_between\_ai\_studio\_and/](https://www.reddit.com/r/Bard/comments/1oq4tfb/what_is_the_difference_between_ai_studio_and/)  
80. Hands-on with Gemini CLI \- Google Codelabs, otwierano: marca 11, 2026, [https://codelabs.developers.google.com/gemini-cli-hands-on](https://codelabs.developers.google.com/gemini-cli-hands-on)  
81. c4-architect | Skills Marketplace \- LobeHub, otwierano: marca 11, 2026, [https://lobehub.com/nl/skills/yuniorglez-gemini-elite-core-c4-architect](https://lobehub.com/nl/skills/yuniorglez-gemini-elite-core-c4-architect)  
82. c4-architect | Skills Marketplace \- LobeHub, otwierano: marca 11, 2026, [https://lobehub.com/vi-VN/skills/yuniorglez-gemini-elite-core-c4-architect](https://lobehub.com/vi-VN/skills/yuniorglez-gemini-elite-core-c4-architect)  
83. Gemini CLI vs Claude Code: A Practical Guide for AI Hackathons Tutorial \- Lablab.ai, otwierano: marca 11, 2026, [https://lablab.ai/ai-tutorials/gemini-cli-vs-claude-code-for-ai-hackathons](https://lablab.ai/ai-tutorials/gemini-cli-vs-claude-code-for-ai-hackathons)  
84. Claude Code Vs Gemini CLI \- Initial Agentic Impressions : r/ClaudeAI \- Reddit, otwierano: marca 11, 2026, [https://www.reddit.com/r/ClaudeAI/comments/1lkew5x/claude\_code\_vs\_gemini\_cli\_initial\_agentic/](https://www.reddit.com/r/ClaudeAI/comments/1lkew5x/claude_code_vs_gemini_cli_initial_agentic/)  
85. Claude 4 vs Claude 3.7 Sonnet vs Gemini 2.5 Pro Coding Comparison \- DEV Community, otwierano: marca 11, 2026, [https://dev.to/sweet\_benzoic\_acid/claude-4-vs-claude-37-sonnet-vs-gemini-25-pro-coding-comparison-59ap](https://dev.to/sweet_benzoic_acid/claude-4-vs-claude-37-sonnet-vs-gemini-25-pro-coding-comparison-59ap)  
86. Gemini 3.1 Pro vs Claude Opus 4.6 vs GPT-5.2: Best AI Model Comparison (2026) | NxCode, otwierano: marca 11, 2026, [https://www.nxcode.io/resources/news/gemini-3-1-pro-vs-claude-opus-4-6-vs-gpt-5-comparison-2026](https://www.nxcode.io/resources/news/gemini-3-1-pro-vs-claude-opus-4-6-vs-gpt-5-comparison-2026)  
87. Claude Code vs Gemini CLI: Who's the Real Dev Co-Pilot? \- Milvus Blog, otwierano: marca 11, 2026, [https://milvus.io/blog/claude-code-vs-gemini-cli-which-ones-the-real-dev-co-pilot.md](https://milvus.io/blog/claude-code-vs-gemini-cli-which-ones-the-real-dev-co-pilot.md)  
88. Gemini vs Claude (2026): Pricing, Context Window & Verdict | Prompt Builder, otwierano: marca 11, 2026, [https://promptbuilder.cc/compare/gemini-vs-claude](https://promptbuilder.cc/compare/gemini-vs-claude)  
89. Gemini 3.1 Pro: Benchmarks, Pricing & Features | Google DeepMind \- Vertu, otwierano: marca 11, 2026, [https://vertu.com/ai-tools/gemini-3-1-pro-review-2026-features-benchmarks-pricing-how-it-compares/](https://vertu.com/ai-tools/gemini-3-1-pro-review-2026-features-benchmarks-pricing-how-it-compares/)  
90. Gemini CLI is impressive, but Claude Code is acting like the real senior engineer \- Reddit, otwierano: marca 11, 2026, [https://www.reddit.com/r/ClaudeCode/comments/1pdyq6z/gemini\_cli\_is\_impressive\_but\_claude\_code\_is/](https://www.reddit.com/r/ClaudeCode/comments/1pdyq6z/gemini_cli_is_impressive_but_claude_code_is/)  
91. Major regression as of 0.15.3 · Issue \#13168 · google-gemini/gemini-cli \- GitHub, otwierano: marca 11, 2026, [https://github.com/google-gemini/gemini-cli/issues/13168](https://github.com/google-gemini/gemini-cli/issues/13168)  
92. codebase\_investigator Agent Times Out on Comprehensive Codebase Review · Issue \#16928 · google-gemini/gemini-cli \- GitHub, otwierano: marca 11, 2026, [https://github.com/google-gemini/gemini-cli/issues/16928](https://github.com/google-gemini/gemini-cli/issues/16928)  
93. Code Execution Through Deception: Gemini AI CLI Hijack \- Tracebit, otwierano: marca 11, 2026, [https://tracebit.com/blog/code-exec-deception-gemini-ai-cli-hijack](https://tracebit.com/blog/code-exec-deception-gemini-ai-cli-hijack)  
94. Ransomware Attacks Soar 30% in 2026: Inside the Unprecedented Surge, otwierano: marca 11, 2026, [https://breached.company/ransomware-attacks-soar-30-in-2026-inside-the-unprecedented-surge/](https://breached.company/ransomware-attacks-soar-30-in-2026-inside-the-unprecedented-surge/)  
95. How Gemini for Google Cloud uses your data, otwierano: marca 11, 2026, [https://docs.cloud.google.com/gemini/docs/discover/data-governance](https://docs.cloud.google.com/gemini/docs/discover/data-governance)  
96. Testing Gemini 3.0 Pro's Actual Context Window in the Web App: My Results Show \~32K (Not 1M) : r/GeminiAI \- Reddit, otwierano: marca 11, 2026, [https://www.reddit.com/r/GeminiAI/comments/1q6viir/testing\_gemini\_30\_pros\_actual\_context\_window\_in/](https://www.reddit.com/r/GeminiAI/comments/1q6viir/testing_gemini_30_pros_actual_context_window_in/)