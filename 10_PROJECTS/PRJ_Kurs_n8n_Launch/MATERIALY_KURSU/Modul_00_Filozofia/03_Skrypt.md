# Moduł 0: Filozofia Automatyzacji — Pełny Skrypt Nagrania

> **Instrukcja:** Tekst piszany kursywą to didaskalia — nie mów ich, ale stosuj. Tekst w nawiasach kwadratowych to oznaczenia akcji. Reszta to dosłowny tekst do powiedzenia (możesz go parafrazować — skrypt to przewodnik, nie więzienie).
>
> Styl: naturalny, bezpośredni, lekki humor tam gdzie oznaczony. Nie korporacyjny.

---

## SEGMENT 0 — INTRO I HOOK (3 minuty)

*[NAGRANIE STARTS — brak intro muzyki, wchodzisz od razu]*

*[SLAJD: Slajd 2 — Liczby]*

Cztery godziny tygodniowo.

*[PAUZA 2 sekundy]*

Tyle mi zajął jeden workflow żeby odzyskać — nie "oszczędzić", właśnie odzyskać — czas który wcześniej szedł na ręczne kopiowanie danych między systemami. Cztery godziny tygodniowo to dwieście osiem godzin rocznie. Dwadzieścia sześć dni roboczych. Cały miesiąc.

Czas na ustawienie tego workflow: dwadzieścia minut.

*[PAUZA 1 sekunda]*

Cześć, jestem Kacper Sieradziński.

*[SLAJD: Slajd 3 — Kim jestem]*

CEO Dokodu, agencja AI automation. Buduję i wdrażam automatyzacje dla polskich firm od kilku lat, kanał YouTube ma prawie pięćdziesiąt tysięcy subskrybentów — głównie ludzi którzy, tak jak Ty, chcą rozumieć jak to naprawdę działa, a nie tylko oglądać "top 10 zapierów".

Pamiętam n8n z wczesnych wersji gdy nie miało jeszcze połowy tego co ma dziś. Widziałem jak rośnie. Wiem gdzie boli i gdzie świeci.

Ten moduł jest darmowy, bo chcę żebyś zanim zainwestujesz w pełny kurs, zobaczył jak pracuję i jak uczę. Zero lania wody. Konkretna wiedza którą możesz użyć dziś.

*[SLAJD: Slajd 4 — Co wyniesiesz]*

W ciągu następnych czterdziestu pięciu minut:

Zrozumiesz czym naprawdę jest automatyzacja procesów — i co ważniejsze, czym NIE jest. Dostaniesz twarde argumenty dlaczego n8n, a nie Zapier czy Make — z cenami, z RODO, ze wszystkim. Nauczysz się frameworku który stosujesz do każdego workflow jaki kiedykolwiek zbudujesz. Uruchomisz n8n na swoim komputerze lub w chmurze. I zbudujesz swój pierwszy działający workflow.

Nie obiecuję, nie straszę. Po prostu zaczynamy.

---

## SEGMENT 1 — CZYM JEST (I NIE JEST) AUTOMATYZACJA (8 minut)

*[SLAJD: Slajd 5 — Definicja]*

Definicja robocza, której używam i której będziemy używać przez cały kurs:

Automatyzacja procesów to sytuacja gdy software robi za Ciebie to, co robisz ręcznie i co można opisać krok po kroku.

Klucz jest tutaj: "można opisać krok po kroku."

Bo to jest granica automatyzacji. Jeśli możesz usiąść i powiedzieć: krok pierwszy to X, krok drugi to Y, jeśli Z to robimy A, jeśli nie Z to robimy B — to możesz to zautomatyzować. Jeśli nie możesz — na razie nie możesz.

Przykład z życia.

Wyobraź sobie że ktoś wypełnia formularz kontaktowy na Twojej stronie. Co robisz ręcznie? Sprawdzasz skrzynkę. Widzisz formularz. Kopiujesz imię, email, firmę do arkusza. Wysyłasz powitalnego emaila. Może dodajesz do CRM. Może informujesz handlowca na Slacku.

To pięć kroków. Każdy można opisać. Każdy można zautomatyzować.

*[SLAJD: Slajd 6 — MIT #1]*

Mity. Zacznijmy od największego.

Automatyzacja wymaga programowania. Nieprawda.

n8n ma ponad czterysta integracji no-code. Drag and drop, klik, uzupełnij formularz, gotowe. Większość tego co buduję dla klientów to zero linii kodu. Jeśli potrafisz obsługiwać Excel — potrafisz obsługiwać n8n.

Oczywiście, im głębiej w las tym więcej drzew. Są rzeczy gdzie JavaScript przyspiesza pracę dziesięciokrotnie. W tym kursie będę czasem pisać kod — ale zawsze będę tłumaczyć co każda linijka robi. To nie jest kurs dla developerów. To jest kurs dla ludzi którzy chcą automatyzować.

*[SLAJD: Slajd 7 — MIT #2]*

Mit drugi: mam ChatGPT, po co mi n8n?

Słyszę to coraz częściej. I rozumiem skąd to pytanie pochodzi — bo AI robi coraz więcej. Ale tu jest fundamentalne nieporozumienie.

AI to składnik. n8n to silnik który nim zarządza.

ChatGPT nie wie kiedy przyszedł Twój formularz. ChatGPT sam z siebie nie zapisze danych do bazy danych. ChatGPT nie wyśle emaila za Ciebie — chyba że zintegrujesz go z czymś co to zrobi. I to właśnie jest n8n.

Lubię taką analogię: AI to silnik. Bardzo dobry, bardzo mocny. Ale silnik bez karoserii, bez skrzyni biegów, bez układu hamulcowego i bez GPS to tylko silnik. n8n jest samochodem w którym AI jest jednym z podzespołów.

Nawiasem mówiąc — Moduł szósty tego kursu jest w całości poświęcony agentom AI działającym wewnątrz n8n. Więc wrócimy do tego.

*[SLAJD: Slajd 8 — MIT #3]*

Mit trzeci, mój ulubiony: automatyzacja to projekt na kwartał.

Absolutnie nie.

*[PYTANIE: zadaj do kamery]* Kiedy ostatnio coś konfigurując zajęło Ci tyle ile się spodziewałeś? Zwykle mniej, co nie?

Email powitalny po formularzu — dwadzieścia minut. Powiadomienie Slack z nowego leada — piętnaście minut. Tygodniowy raport z arkusza — czterdzieści pięć minut. I tu jestem ostrożny — bo te czasy to pierwsze uruchomienie, z debug i zastanawianiem się. Jak robisz to drugi raz, idziesz trzy razy szybciej.

Zanim skończymy ten moduł — masz działający workflow. Nie obiecuję — po prostu tak jest zaplanowane.

*[SLAJD: Slajd 9 — Co automatyzować]*

Jakie procesy warto automatyzować? Te które są powtarzalne i opisywalne.

W kontekście agencji i firm, z którymi pracuję najczęściej w Dokodu, to są:

Powiadomienia — ktoś coś zrobił i Ty musisz wiedzieć. Nowy lead, nowa faktura, termin płatności mija. To jest klasyka.

Emaile — powitalne, przypomnienia, follow-upy. Te same, powtarzane setki razy. Zautomatyzuj raz, działa rok.

Raporty — tygodniowe zestawienie sprzedaży, miesięczny raport dla klienta. Zbierasz dane z kilku miejsc, składasz w całość, wysyłasz. Idealne do automatyzacji.

Synchronizacja danych — między CRM a arkuszem, między formularzem a systemem faktur. Przekopiowywanie danych to praca bez wartości dodanej.

*[SLAJD: Slajd 10 — Czego NIE automatyzować]*

I teraz coś o czym rzadko mówią "guru automatyzacji": czego nie automatyzować.

Decyzje strategiczne. Który klient jest ważniejszy, czy dać rabat, jaką strategię przyjąć — to jest praca dla człowieka z kontekstem i intuicją. n8n może Ci przygotować dane do tej decyzji. Decyzja — Twoja.

Relacje. Jeśli automatyzujesz relację z klientem do stopnia w którym on czuje że rozmawia z robotem — zrobiłeś za dużo. Email z życzeniami urodzinowymi przez automatyzację jest OK. Ale pierwsza rozmowa sprzedażowa przez bota — nie.

Zarządzanie kryzysem. Gdy system się sypie, gdy coś idzie nie tak — człowiek decyduje. Automatyzacja może wysłać alert. Co z nim zrobisz — Ty decydujesz.

To jest dojrzałe podejście do automatyzacji. Nie automatyzujesz wszystkiego. Automatyzujesz to co jest powtarzalne i mechaniczne, żeby mieć więcej czasu na to co wymaga głowy.

---

## SEGMENT 2 — DLACZEGO N8N, A NIE ZAPIER/MAKE (10 minut)

*[SLAJD: Slajd 11 — Porównanie ogólne]*

Dobra, wchodzimy w temat który może być kontrowersyjny.

Dlaczego n8n, a nie Zapier? Dlaczego n8n, a nie Make? Przecież oba te narzędzia istnieją, są popularne, mają tutoriale, mają integracje.

Powiem Ci wprost. Używam n8n od lat. Nie dlatego że jest "hype", nie dlatego że n8n mi płaci za reklamę — nie płaci. Dlatego że po przetestowaniu różnych narzędzi to jest to które wybieram dla siebie i dla klientów w Polsce.

I zaraz dam Ci konkrety.

*[SLAJD: Slajd 12 — Ceny]*

Zacznijmy od pieniędzy, bo to jest najłatwiejsze do policzenia.

Scenariusz: małej-średniej firma, dziesięć tysięcy operacji miesięcznie, jeden użytkownik.

n8n self-hosted na VPS który kosztuje dwadzieścia dolarów miesięcznie — osiemdziesiąt złotych. n8n Cloud w planie Starter — dwadzieścia dolarów, czyli też około osiemdziesiąt złotych. Zapier Professional — czterdzieści dziewięć dolarów, czyli dwa razy tyle. Make — pozornie najtańszy, dziewięć dolarów — ale tu jest pułapka.

I tu muszę się zatrzymać, bo Make to specjalny przypadek.

W Make "operacja" to nie to samo co "task" w Zapier czy "execution" w n8n. W Make każdy krok w workflow to osobna operacja. Masz workflow z pięcioma krokami, który odpala się tysiąc razy? To pięć tysięcy operacji, nie tysiąc. Realne koszty Make są często trzy do pięć razy wyższe niż szacujesz na początku. Zanim podpiszesz — policz wszystkie kroki.

*[SLAJD: Slajd 13 — RODO]*

Temat drugi: RODO i dane klientów.

*[PYTANIE: zadaj do kamery]* Ile razy w ostatnim roku zastanawiałeś się gdzie lądują dane z Twoich formularzy kiedy przechodzą przez Zapiera?

Zapier Terms of Service, rok dwa tysiące dwudziesty czwarty, cytuję: "Zapier processes data on servers located in the United States."

Co to znaczy w praktyce? Dane z Twoich formularzy — imiona, emaile, numery telefonów Twoich klientów — idą na serwery w Stanach Zjednoczonych.

Teraz — to nie jest natychmiastowe łamanie prawa. Zapier oferuje DPA, Data Processing Agreement, który formalnie legalizuje transfer. Ale to jest dodatkowa warstwa umowna, dodatkowa odpowiedzialność, i gdy przyjdzie audyt RODO to Ty musisz to udowodnić.

n8n self-hosted: dane zostają na Twoim serwerze. Na Twoim VPS w Warszawie, we Frankfurcie, gdzie chcesz — ale pod Twoją kontrolą. Koniec historii.

Kara za naruszenie RODO to do czterech procent obrotu globalnego lub dwadzieścia milionów euro. Nie straszę — informuję. Dla agencji która przetwarza dane klientów B2B — to nie jest akademiczne pytanie.

*[SLAJD: Slajd 14 — Vendor lock-in]*

Trzeci argument: vendor lock-in.

Rok dwa tysiące dwudziesty drugi. Zapier zmienił cennik. Usunął multi-step zaps z darmowego planu. Podniósł ceny Professional o mniej więcej pięćdziesiąt procent. Tysiące małych firm i freelancerów musiało albo migrować albo płacić dwa razy więcej.

Co możesz zrobić kiedy n8n zmienia coś co Ci się nie podoba?

n8n jest open source — fair-code license. Możesz pobrać cały kod. Możesz hostować gdzie chcesz. Możesz zmodyfikować do własnych potrzeb. Nawet jeśli n8n jako firma by znikła — narzędzie nadal działa, community nadal je rozwijać.

Twoje workflow, Twoje automatyzacje, Twój majątek. Nie czyiś SaaS.

*[SLAJD: Slajd 17 — Decision tree]*

Jeden uczciwy komentarz zanim skończymy tę część.

Czy n8n jest zawsze najlepszy? Nie. Są scenariusze gdzie Zapier ma sens — jeśli ktoś naprawdę technofobiczny i potrzebuje czegoś gotowego w dziesięć minut bez żadnego setupu, Zapier jest łatwiejszy na start. Make ma świetny wizualny debug który mi się podoba.

Ale dla agencji, dla firm z danymi klientów, dla kogoś kto buduje to na dłuższą metę — n8n wygrywa w każdym wymiarze który ma znaczenie.

---

## SEGMENT 3 — JAK MYŚLEĆ PROCESAMI (8 minut)

*[SLAJD: Slajd 15 — Diagram trigger→akcja→warunek]*

Dobra. Teraz jedna z najważniejszych rzeczy w tym module. Framework który stosuję do każdego workflow — czy to prostego czy złożonego. Trzy słowa: Trigger. Akcja. Warunek.

Trigger — co uruchamia workflow. Co jest sygnałem startowym. Może to być formularz, może to być email, może to być harmonogram, może to być API call, może to być zmiana w bazie danych. Zawsze coś musi "pociągnąć za spust".

Akcja — co workflow robi po uruchomieniu. Wyślij email, zapisz do arkusza, wywołaj API, wyślij powiadomienie, utwórz rekord w CRM. Możesz mieć jedną akcję lub dwadzieścia — nie ma limitu.

Warunek — kiedy workflow robi inaczej. Jeśli budżet klienta jest powyżej dziesięciu tysięcy, idź ścieżką A. Jeśli poniżej, idź ścieżką B. Jeśli email jest z domeny klienta, zrób X. Jeśli z nieznanej domeny, zrób Y.

*[PAUZA]*

To jest cały framework. Trigger. Akcja. Warunek. Każdy workflow jaki kiedykolwiek zbudujesz można opisać tymi trzema słowami.

*[SLAJD: Slajd 16 — Przykład rozbity na T/A/W]*

Przykład konkretny. Obsługa leada z formularza.

TRIGGER: ktoś wypełnia formularz kontaktowy na stronie.

AKCJA pierwsza: zapisz dane do arkusza Google lub CRM.

AKCJA druga: wyślij email powitalny do osoby która wypełniła formularz.

WARUNEK: czy budżet który podała jest powyżej dziesięciu tysięcy złotych?

Jeśli TAK — wyślij powiadomienie na Slack, zaplanuj call w Calendly, oznacz jako priorytetowy lead.

Jeśli NIE — dodaj do sekwencji nurturing w MailerLite, wyślij ebooka, ustaw przypomnienie za siedem dni.

*[PAUZA]*

Powiedz mi — ile osób w Twojej firmie robi to ręcznie teraz? I ile czasu to zajmuje? Bo to jest workflow który budujesz raz, a działa rok.

*[PYTANIE: zadaj do kamery]* Teraz chwila dla Ciebie. Masz dwie minuty. Zatrzymaj film. Weź kartkę. Wpisz jeden proces z Twojej pracy który jest powtarzalny — i rozpisz go na: co go uruchamia, co potem robisz, i kiedy robisz inaczej. Dwie minuty.

*[PAUZA — możesz tu wciąć graficzną planszę z "ĆWICZENIE — 2 minuty"]*

Gotowe?

To właśnie jest specyfikacja workflow. To czego się właśnie nauczyłeś to sposób myślenia który n8n zamienia bezpośrednio w canvas — każdy krok to node, każda strzałka to połączenie, każdy warunek to IF node.

---

## SEGMENT 4 — SETUP ŚRODOWISKA (8 minut)

*[SLAJD: Slajd 17 — Decision tree setup]*

Dobra, czas uruchomić n8n.

Trzy scenariusze:

Testujesz, uczysz się, nie masz jeszcze klientów — Docker lokalnie. Jedna komenda, n8n działa na porcie 5678, zero kosztów, dane zostają na Twoim komputerze.

Masz klientów, piszesz workflow dla prawdziwego biznesu, masz VPS z Linuksem i nie boisz się terminala — self-hosted n8n na VPS. Dwadzieścia dolarów miesięcznie za VPS, pełna kontrola, twoje dane, twoje zasady.

Chcesz zacząć od razu, masz realne dane klientów, nie chcesz się bawić z serwerem — n8n Cloud. Trial darmowy, potem dwadzieścia dolarów miesięcznie, zarządzane przez n8n, aktualizacje automatyczne, wsparcie techniczne.

*[SLAJD: Slajd 18 — Docker komenda]*

Zaczynamy od Docker, bo to jest najszybszy start.

*[DEMO: pokaż terminal]*

Wymagania: Docker Desktop zainstalowany. Jeśli nie masz — docker.com, pobranie, instalacja, pięć minut. Zakładam że masz.

Komenda — kopiuję z pliku, bo po co wpisywać z pamięci:

```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  docker.n8n.io/n8nio/n8n
```

*[DEMO: uruchom komendę w terminalu, pokaż pobieranie obrazu]*

Widzicie — Docker pobiera obraz. Pierwsze pobranie zajmuje minutę-dwie, zależy od łącza. Kolejne uruchomienia — kilka sekund.

*[PAUZA na pobieranie — przyspiesz w edycji lub skomentuj: "Tu czekamy chwilę — przyspieszyłem nagranie"]*

I mamy. Otwieramy przeglądarkę, localhost:5678.

*[DEMO: otwórz przeglądarkę, pokaż formularz rejestracji n8n]*

Pierwsze logowanie — n8n pyta o email i hasło. To jest Twoje lokalne konto, dane nigdzie nie idą. Wpisuję dane testowe.

*[DEMO: zaloguj się, pokaż główny interfejs]*

I jesteśmy w środku.

Jeden komentarz techniczny który jest ważny: ta komenda używa flagi `--rm` co oznacza że po zamknięciu kontenera n8n się usuwa. Ale dane są zapisane w `~/.n8n` na Twoim komputerze, więc następnym razem gdy uruchomisz tę samą komendę — wszystko wróci.

Do prawdziwego use case produkcyjnego — plik z ćwiczeniami ma bardziej rozbudowaną konfigurację z `docker-compose`. Ale na start — ta komenda wystarczy.

---

## SEGMENT 5 — PIERWSZE 15 MINUT W INTERFEJSIE (6 minut)

*[SLAJD: Slajd 19 — Mapa interfejsu]*

Orientacja w interfejsie. Szybko, bo za chwilę budujemy.

Lewa kolumna — sidebar. Lista Twoich workflow, credentials, historia wykonań. Twoje centrum dowodzenia.

Środek — canvas. Tutaj budujesz. Drag and drop, zoom, przesuń. To jest Twoja przestrzeń robocza.

Przycisk plus na canvasie — dodaj nowy node. Kliknij, wyszukaj, konfiguruj.

Prawa strona gdy klikniesz node — konfiguracja tego node'a. Każda integracja ma swój formularz.

Na górze — Run i Save. Uruchom workflow, zapisz workflow.

Analogia która mi pomaga: sidebar to szuflady biurka, canvas to blat, przycisk plus to skrzynka narzędziowa. To nie jest skomplikowane. Naprawdę.

*[DEMO: pokaż n8n na żywo, przejdź przez każdy element]*

*[SLAJD: Slajd 20 — Demo workflow]*

A teraz — budujemy.

Workflow nazywa się Hello Automation. Trzy nody: Webhook, który odbiera dane. Set node albo Code, który przetwarza dane. Gmail, który wysyła email.

Kiedy ktoś wyśle HTTP request na nasz webhook — ta osoba dostaje spersonalizowanego emaila. Proste, działające, prawdziwe.

*[DEMO: tworzenie workflow w n8n — pokaż krok po kroku]*

Zaczynam od kliknięcia "New Workflow". Pusty canvas.

Klikam plus. Szukam "Webhook". Dodaję. W konfiguracji — HTTP Method: POST, ścieżka: hello-automation. Kopiuję URL który generuje n8n — zaraz go użyjemy.

Drugi node — klikam plus na wyjściu Webhooków. Szukam "Set". Set node pozwala nam zdefiniować co chcemy dalej przekazać. Ustawiam: name z `{{ $json.body.name }}`, email z `{{ $json.body.email }}`.

*[ZATRZYMAJ się na chwilę przy expressions]*

To co widzicie w podwójnych nawiasach klamrowych — to są expressions w n8n. Sposób na odwołanie się do danych z poprzedniego noda. Wszystko co przyszło w body requestu jest dostępne przez `$json.body.nazwapola`. W Module 2 będziemy w to wchodzić głęboko. Na razie — to jest składnia, zapamiętaj wygląd.

Trzeci node — Gmail. Szukam "Gmail", wybieram "Send Email". Połączę konto Gmail przez OAuth2.

*[DEMO: pokaż ekran autoryzacji Gmail — zatrzymaj się]*

Tu się zatrzymuję — autoryzacja Gmail wymaga chwili i jest poza zakresem tego szybkiego demo. Pełna instrukcja krok po kroku jest w pliku z ćwiczeniami, który jest dołączony do tego modułu. Konfiguracja zajmuje pięć minut i robisz ją raz.

Zakładając że Gmail jest podłączony: wypełniam "To" jako `{{ $json.email }}`, "Subject" jako "Cześć {{ $json.name }}, witamy Cię!", body — wiadomość powitalna.

Zapisuję workflow. Klikam "Test Workflow" na Webhook node. n8n czeka na dane.

Teraz — terminal, wysyłam test:

```bash
curl -X POST https://[twój-webhook-url] \
  -H "Content-Type: application/json" \
  -d '{"name": "Kacper", "email": "kacper@test.pl"}'
```

*[DEMO: pokaż odpowiedź, pokaż execution log w n8n]*

I mamy wykonanie. Dane przeszły przez każdy node. Email... poszedł.

To jest Twój pierwszy workflow. Nie jest skomplikowany. Ale jest prawdziwy. Robi coś realnego. I teraz wiesz jak to działa.

---

## SEGMENT 6 — OUTRO I CTA (2 minuty)

Dobra — podsumujmy co się wydarzyło przez ostatnie czterdzieści pięć minut.

*[SLAJD: Slajd 21 — Podsumowanie]*

Masz definicję automatyzacji która działa w praktyce. Wiesz które mity odrzucić kiedy ktoś powie "to tylko dla programistów" albo "AI zastąpi workflow".

Masz twarde argumenty za n8n — ceny, RODO, vendor lock-in. Możesz je użyć kiedy szef pyta dlaczego nie Zapier.

Masz framework trigger-akcja-warunek który teraz możesz nałożyć na każdy proces w swojej firmie i od razu zobaczyć co można zautomatyzować.

Masz n8n uruchomione. I masz swój pierwszy workflow.

*[PAUZA]*

To był Moduł zero. Jeden procent kursu.

*[SLAJD: Slajd 22 — CTA]*

Jeśli to było wartościowe — w pełnym kursie idziemy dziesięć razy głębiej.

API REST i webhooks — jak rozmawiać z dowolnym systemem na świecie. AI nodes — GPT, Claude, Whisper wewnątrz workflow. Autonomous agents — workflow które same podejmują decyzje. RAG — systemy które pamiętają. Bezpieczeństwo na produkcji. I dwa moduły bonusowe.

Siedem modułów, osiem godzin materiału, projekty z prawdziwych klientów Dokodu. Dostęp dożywotni. Społeczność na Discordzie.

Link do zapisów — poniżej.

Jeśli masz pytania — napisz w komentarzu. Czytam wszystkie.

Do zobaczenia w Module pierwszym. Tam zaczynamy od API. Serio.

*[KONIEC NAGRANIA — bez długich podziękowań, bez muzyki wyjściowej, po prostu stop]*

---

## Notatki reżyserskie

**Ogólny ton:** mów jakbyś tłumaczył coś znajomemu który jest inteligentny ale nowy w temacie. Bez patronizowania, bez upraszczania, bez korporacyjnej mowy.

**Pauzy:** zaznaczone [PAUZA] są celowe. Nie wypełniaj ich. Cisza sprzedaje.

**Demo:** nagrywaj demo oddzielnie i montuj. Jeśli cokolwiek pójdzie nie tak — możesz nagrać ponownie bez nagrywania całego skryptu.

**Długość vs jakość:** lepiej krótszy film z konkretami niż długi z wypełniaczem. Jeśli segment zajmuje 6 minut zamiast 8 — okej. Nie szukaj słów żeby dobić timing.

**Energia:** segment 1-3 może być spokojniejszy, bardziej "siedzisz i tłumaczysz". Segment 4-5 (demo) powinien być dynamiczny, szybki, z wyraźnym podekscytowaniem. CTA — spokojnie, pewnie.
