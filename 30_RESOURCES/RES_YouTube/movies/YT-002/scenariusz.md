---
id: YT-002
title: Gemini CLI od zera — AI agent w terminalu
status: SCENARIUSZ
created: 2026-03-18
lokowanie: Hostinger VPS (2 500 PLN) — Demo 1, sekcja na serwerze
długość: ~18 minut
format: prompter + screencasts + animacje Remotion
---

# Scenariusz: YT-002

---

## HOOK (0:00–0:40)

[ANIMACJA: Czarne tło. Pojawia się zielony tekst w stylu terminala — "SSH do serwera... połączono." Efekt pisania, pauza, pojawia się kolejna linia: "gemini" — kursor miga. Zanika powoli.]

Dałem temu narzędziu dostęp do serwera produkcyjnego — podajesz mu zadanie i odchodzisz od klawiatury.

[PAUZA]

Napisałem mu co chcę wdrożyć: API w Pythonie, bazę danych, reverse proxy z SSL. Kiedy wróciłem po kilku minutach, wszystkie pliki były gotowe — Docker Compose, konfiguracja nginx, plik ze zmiennymi środowiskowymi — każdy z komentarzem co robi i dlaczego tak, a nie inaczej.

[PAUZA]

To nie jest demo z konferencji z przygotowanymi odpowiedziami. Za chwilę zrobię to na żywo, na prawdziwym serwerze. Ale najpierw — zanim przejdziemy do konfiguracji i demonstracji — powiem ci czym to narzędzie właściwie jest i dlaczego różni się od wszystkiego co pewnie dotąd widziałeś.

[ANIMACJA: Title card — "GEMINI CLI OD ZERA" — białe litery, ciemne tło z subtelnym gradientem. Logo Gemini w tle, lekko rozmyte. 2 sekundy. Fade out.]

---

## CO TO JEST GEMINI CLI (0:40–3:30)

[ANIMACJA: Schemat — po lewej ikona "Terminal / CLI", strzałka w prawo do "Gemini (Google)" w chmurze, strzałka w dół do "Komputer / Serwer / Pliki". Tekst pod spodem: "ReAct loop — myśl → działaj → obserwuj → myśl". Pojawia się etapami.]

Zacznijmy od podstaw, bo żeby dobrze używać tego narzędzia, musisz rozumieć co tak naprawdę robi.

Gemini CLI to klient konsolowy do modelu Gemini od Google, ale z jedną kluczową różnicą w stosunku do zwykłego chatbota — ma narzędzia. Może czytać i pisać pliki na twoim komputerze albo serwerze, może wykonywać komendy w terminalu, może przeszukiwać web. I robi to w pętli, autonomicznie, bez twojego udziału między krokami.

[PAUZA]

To co właśnie opisałem ma swoją nazwę — ReAct loop. Pochodzi ze świata badań nad agentami AI i skrót pochodzi od Reasoning and Acting, czyli rozumowanie i działanie. W praktyce wygląda to tak: dajesz agentowi zadanie, on analizuje sytuację, wybiera narzędzie i je wykonuje, patrzy co wyszło, na tej podstawie planuje kolejny krok — i powtarza to dopóki zadanie nie jest skończone albo dopóki nie trafi na coś czego nie umie rozwiązać sam.

[ANIMACJA: Lista pojawia się punkt po punkcie: "✓ Czyta i pisze pliki", "✓ Wykonuje komendy shell", "✓ Web search w czasie rzeczywistym", "✓ 1 milion tokenów kontekstu". Każdy punkt slide-in z lewej.]

Żeby to był nie tylko abstrakt — wyobraź sobie że masz junior developera, który jest bardzo sprawny technicznie, ma dostęp do twojego terminala i plików, ale nie zna twojego projektu. Musisz mu powiedzieć co ma zrobić i jaki ma być wynik — ale nie musisz prowadzić go za rękę przez każdy krok. Tyle że ten junior developer pracuje 10 razy szybciej, nie robi przerw i nie zapomina co czytał 20 minut temu, bo ma milion tokenów kontekstu w pamięci.

[PAUZA]

Teraz ważna rzecz — Gemini CLI nie wymaga niczego lokalnie poza Node.js. Model siedzi w infrastrukturze Google, ty masz tylko cienki klient w terminalu który komunikuje się z tym modelem przez API.

[PAUZA]

Projekt jest open source — kod jest na GitHubie. Link wrzucam do opisu. Możesz zajrzeć co robi, jak jest zbudowany, zanim dasz mu dostęp do czegokolwiek. To ważne, bo narzędzia które wykonują komendy na twoim serwerze powinny być przez ciebie zrozumiane przynajmniej na poziomie: skąd to pochodzi i czy mogę sprawdzić co robi.

[PAUZA]

Jeszcze jedna rzecz o cenie zanim przejdziemy dalej. Darmowy klucz API z Google AI Studio daje ci dostęp do modelu i milion tokenów kontekstu — i to wystarczy żeby zacząć i przetestować. Jedyne ograniczenie darmowego planu to limity zapytań na minutę, które przy dłuższych agentowych sesjach mogą sprawić że agent zatrzymuje się i czeka. Do pierwszych testów i nauki nie ma to znaczenia, ale jeśli chcesz używać tego w codziennej pracy bez przestojów, warto podpiąć kartę i przejść na Pay-as-you-go — limity skaczą wielokrotnie w górę, a koszty sesji takich jak te demka to dosłownie kilkanaście centów.

No to zaczynamy — instalacja.

---

## INSTALACJA (3:30–5:30)

[SCREENCAST: Czysty terminal. Kursor na początku linii.]

Instalacja jest na tyle prosta że prawie nie ma o czym mówić, ale dwa słowa zanim zaczniesz.

Potrzebujesz Node.js w wersji 18 lub wyższej — najlepiej 20 plus. Jeśli masz starszą wersję, instalacja nie powiedzie się. Sprawdź szybko:

[SCREENCAST: Kacper wpisuje `node --version`, widać wynik np. "v20.11.0".]

[ANIMACJA: Badge — "Wymagania: Node.js 18+" — pojawia się w rogu, 3 sekundy.]

Dobrze. Teraz właściwa instalacja:

[SCREENCAST: Kacper wpisuje:]
```
npm install -g @google/gemini-cli
```

[SCREENCAST: Instalacja się uruchamia — widać scrollujące się logi npm. Kilka sekund. Zakończenie — "added X packages".]

Globalna instalacja przez npm — po niej masz komendę `gemini` dostępną w każdym katalogu na twoim systemie.

[ANIMACJA: Pro-tip dymek — "Nie chcesz globalnej instalacji? npx @google/gemini-cli — jednorazowo, bez śladu" — pojawia się na 5 sekund]

Jeśli nie lubisz zaśmiecać globalnego środowiska — możesz użyć `npx @google/gemini-cli` i w ogóle nic nie instalować. npx pobierze i odpali jednorazowo, nie zostawi żadnego śladu w systemie. Dobra opcja jeśli chcesz tylko sprawdzić czy to narzędzie jest dla ciebie.

[SCREENCAST: Kacper wpisuje `gemini`. Uruchamia się interfejs — pojawia się prompt logowania albo pole na klucz API.]

Przy pierwszym uruchomieniu Gemini CLI pyta skąd wziąć autoryzację. Możesz zalogować się kontem Google — to najprostsza opcja, bo dostajesz od razu darmowe limity bez konfigurowania czegokolwiek. Alternatywnie podajesz klucz API — wchodzisz na aistudio.google.com, klikasz "Create API key", chwila i masz go. Wklejasz tutaj i gotowe.

[SCREENCAST: Kacper loguje się — widać że interfejs ładuje się w pełni, pojawia się główny prompt Gemini CLI z informacją o modelu i dostępnych poleceniach.]

[PAUZA]

I to naprawdę wszystko. Cała instalacja — bez Dockera, bez Pythona, bez wirtualnych środowisk. Dla kogoś kto przyzwyczaił się do skomplikowanego setupu narzędzi AI — to jest odświeżające.

Ale zanim pokażę ci demka, jest jedna rzecz którą chcę omówić najpierw — jak pisać dobre prompty do Gemini CLI. Bo to jest umiejętność która decyduje o tym czy agent zrobi dokładnie to co chcesz, czy będziesz musiał go poprawiać trzy razy.

---

## JAK PISAĆ PROMPTY (5:30–8:30)

[SCREENCAST: Gemini CLI otwarty, gotowy na input. Kacper zaczyna pisać, ale powoli — komentuje na żywo.]

Gemini CLI zaczyna każdą sesję od zera. Nie wie nic o twoim projekcie, nie pamięta poprzednich rozmów, nie zna twoich preferencji. To oznacza że twój prompt musi być kompletny — agent ma działać autonomicznie na podstawie tego co mu napiszesz, bez konieczności dopytywania cię co chwilę.

[PAUZA]

Dobre prompty do agentów mają cztery elementy. Pokażę ci je na przykładzie tego co za chwilę wpiszę w Demo 1.

[ANIMACJA: Pojawia się lista — "1. Kontekst", "2. Cel", "3. Ograniczenia", "4. Format wyjścia". Każdy punkt slide-in.]

Po pierwsze — kontekst. Opisz sytuację. Co masz, co to jest, jakie środowisko, jakiej wersji używasz. Im więcej agent wie o punkcie startowym, tym lepsze decyzje podejmuje po drodze.

Po drugie — cel. Co ma powstać? Bądź konkretny. "Napraw kod" to zły cel. "Stwórz plik docker-compose.yml z trzema serwisami — app na porcie 3000, postgres na 5432, redis na 6379" — to jest dobry cel.

Po trzecie — ograniczenia. Czego nie robić, jakie konwencje zachować, co jest poza zakresem. Bez tego agent może zrobić coś poprawnego technicznie, ale niezgodnego z twoimi wymaganiami.

Po czwarte — format wyjścia. Co chcesz dostać na końcu? Pliki? Listę? Raport priorytetowy? Powiedz to wprost.

[SCREENCAST: Kacper pisze prompt — wolno, komentując:]

Dobra, to piszemy razem. Mam serwer VPS z API w FastAPI które chcę wdrożyć. Prompt będzie wyglądał tak:

[SCREENCAST: Kacper wpisuje stopniowo:]
```
Mam API w FastAPI które chcę wdrożyć na tym serwerze Ubuntu 22.04.
Potrzebuję:
1. docker-compose.yml dla trzech serwisów: app FastAPI na porcie 8000,
   postgres na 5432, redis na 6379
2. nginx.conf skonfigurowany jako reverse proxy z SSL pass-through
3. .env.example z wszystkimi zmiennymi które aplikacja potrzebuje

Użyj Docker volumes żeby dane przeżyły restart. Dodaj healthchecks.
Na końcu wyjaśnij w punktach co każdy plik robi i w jakiej kolejności
uruchamiać.
```

Widzisz różnicę w porównaniu do "stwórz mi konfigurację dockera"? Masz kontekst — Ubuntu 22.04. Masz konkretny cel — trzy pliki. Masz ograniczenia — volumes, healthchecks. Masz format wyjścia — wyjaśnienie po polsku, kolejność uruchamiania.

[PAUZA]

Jeden błąd który widzę bardzo często — ludzie piszą do agenta tak jak do zwykłego chatbota, jedno zdanie, i liczą że agent "się domyśli". Agent nie domyśla się, agent działa na informacjach które ma. Im lepsza informacja, tym lepsze działanie.

[PAUZA]

Dobra. Mamy zainstalowane narzędzie, mamy dobry prompt. Czas na serwer.

---

## DEMO 1 — SERWER + HOSTINGER (8:30–13:00)

[SCREENCAST: Terminal — sesja SSH. Widać prompt serwera, coś w stylu: `root@vps-123:~#`]

Jestem teraz zalogowany przez SSH na serwerze VPS — to jest Hostinger VPS, link do oferty wrzucam w opis pod filmem. Używam Hostingera do projektów klientów, bo konfiguracja od momentu zamówienia zajmuje pięć minut, mam pełną kontrolę nad środowiskiem i nie muszę się tłumaczyć co instaluję. Żadnego współdzielonego hostingu, żadnych ograniczeń systemowych.

[PAUZA]

Sytuacja jest taka: mam API w FastAPI i chcę je wdrożyć na tym serwerze. Normalnie — godzina pracy, może dwie. Szukasz przykładów docker-compose na Stack Overflow, składasz nginx config z różnych źródeł, debugujesz dlaczego postgres nie łączy się z aplikacją, zapominasz dodać healthcheck. To jest ta część DevOpsu której nikt nie lubi robić ręcznie.

[SCREENCAST: Kacper uruchamia `gemini` na serwerze. Pojawia się interfejs. Kacper wkleja wcześniej napisany prompt.]

Wklejam prompt który przed chwilą napisaliśmy razem.

[SCREENCAST: Gemini CLI zaczyna działać. Widać że agent najpierw wypisuje analizę: sprawdza jakie środowisko, jaka wersja Dockera. Wykonuje `ls -la` — widać strukturę katalogu na serwerze.]

Patrz co robi w pierwszej kolejności — sprawdza co już jest na serwerze zanim zacznie cokolwiek tworzyć. Nikt go nie prosił żeby to zrobił. Sam zdecydował że potrzebuje tego kontekstu. To jest właśnie ta różnica między chatbotem a agentem — chatbot by od razu zaczął generować docker-compose z szablonu, agent najpierw zbiera informacje.

[PAUZA]

Uwaga techniczna dla tych którzy będą to testować — domyślnie Gemini CLI przed wykonaniem każdej komendy w terminalu pyta o pozwolenie. Dostaniesz prompt: "Chcę wykonać tę komendę, czy zgadzasz się?". Ja tu mam włączony tryb YOLO żeby sesja szła płynnie do nagrania, ale normalnie na nowym serwerze dostajesz pełną kontrolę co agent faktycznie wykonuje i możesz każdą komendę zatwierdzić albo odrzucić.

[SCREENCAST: Gemini CLI generuje i zapisuje docker-compose.yml. Widać że pisze pełną zawartość pliku, komentuje każdy serwis.]

Teraz tworzy docker-compose. Widzisz że definiuje trzy serwisy: aplikację, postgres, redis. Każdy ma swoje volumes żeby dane przeżyły restart kontenera. I tu ciekawy detal — dodał healthchecks do postgres i redis zanim aplikacja się do nich połączy. To jest ten szczegół który często się opuszcza przy pisaniu ręcznie, a potem aplikacja crashuje przy starcie bo próbuje połączyć się z bazą zanim ta jest gotowa.

[SCREENCAST: Gemini CLI przechodzi do nginx.conf. Pisze konfigurację reverse proxy.]

Nginx config z SSL pass-through — to znaczy że nginx nie terminuje SSL sam, tylko przekazuje zaszyfrowany ruch do aplikacji. Sensowne jeśli masz certbot zainstalowany poza kontenerem i nie chcesz duplikować zarządzania certyfikatami.

[SCREENCAST: Gemini CLI tworzy .env.example z pełną listą zmiennych. Następnie wypisuje podsumowanie — opis co każdy plik robi, co uzupełnić, kolejność uruchamiania.]

[PAUZA]

I tu jest rzecz którą cenię w tym narzędziu najbardziej — na końcu sam wyjaśnia co zrobił, co trzeba uzupełnić i w jakiej kolejności uruchamiać. Nie musisz się domyślać co masz teraz zrobić. Masz gotową listę kroków.

[SCREENCAST: Kacper wychodzi z Gemini CLI. Wpisuje `cat docker-compose.yml`. Widać pełną zawartość — poprawny, kompletny plik.]

[PAUZA]

Gdybym to pisał ręcznie — ze znajomością tematu — zajęłoby mi to pewnie godzinę, wliczając szukanie dokumentacji i debugowanie pierwszych prób. Z Gemini CLI to jest może kwadrans, i te 15 minut to głównie przejrzenie co wygenerował żeby upewnić się że rozumiem każdą linię, nie samo pisanie.

[ANIMACJA: Grafika porównawcza — po lewej "Ręcznie: ~60 min", po prawej "Gemini CLI: ~15 min". Prosta, 3 sekundy.]

Dobra — to był scenariusz serverowy. Teraz wróćmy lokalnie i pokażę ci coś co stosuję regularnie przed deployem każdego projektu.

---

## DEMO 2 — LOKALNIE: CODE REVIEW (13:00–16:30)

[SCREENCAST: Nowy terminal — lokalnie. Kacper wpisuje `ls`. Widać strukturę projektu Python/FastAPI: `main.py`, `routers/`, `models/`, `dependencies/`, `requirements.txt`, `.env`.]

Mam projekt backendowy — API w FastAPI. Prosty przykład: kilka endpointów, obsługa użytkowników, połączenie z PostgreSQL przez SQLAlchemy. Chcę sprawdzić czy jest bezpieczny zanim go wdrożę na produkcję.

W normalnym świecie masz kilka opcji: code review samodzielnie, co jest żmudne bo sam piszesz ten kod i masz ślepą plamkę na własne błędy. Możesz zatrudnić kogoś z bezpieczeństwa, co jest drogie jeśli robisz to regularnie. Albo masz nadzieję że jest OK — co jest najgorsza opcja, ale statystycznie najczęstsza.

[PAUZA]

Gemini CLI ma dostęp do plików. Niech przejrzy cały projekt. Tym razem piszemy prompt razem, bo tu jest ciekawy niuans — jak poprosić o przegląd bezpieczeństwa żeby dostać coś użytecznego, a nie listę ogólnych porad.

[SCREENCAST: Kacper uruchamia `gemini`. Zaczyna pisać prompt, komentując:]

Znowu cztery elementy. Kontekst — projekt Python, FastAPI, widzisz strukturę obok. Cel — przegląd bezpieczeństwa, ale konkretny, nie "sprawdź bezpieczeństwo". Ograniczenie — chcę realnych znalezisk, nie generycznych porad o używaniu HTTPS. Format — lista priorytetowa, bo nie mam czasu na wszystko naraz i chcę wiedzieć od czego zacząć.

[SCREENCAST: Kacper wpisuje:]
```
Przejrzyj ten projekt Python/FastAPI pod kątem błędów bezpieczeństwa
i potencjalnych bugów. Zacznij od struktury katalogów, potem przejrzyj
kluczowe pliki jeden po drugim — main.py, routers/, models/, dependencies/.

Szukaj konkretnie: brak walidacji inputu (poza Pydantic), surowe zapytania SQL
bez parametryzacji, wrażliwe dane w kodzie, problemy z autoryzacją JWT.

Nie pisz mi o ogólnych best practices — daj mi listę priorytetową
konkretnych znalezisk z nazwą pliku i linią kodu. Zacznij od krytycznych.
```

Widzisz to "nie pisz mi o ogólnych best practices"? To jest ograniczenie które bardzo zmienia jakość odpowiedzi. Bez tego dostaniesz akapit o tym żeby używać HTTPS, co jest bezużyteczne jeśli już to robisz.

[SCREENCAST: Gemini CLI zaczyna działać. Wykonuje `ls -la` żeby zobaczyć strukturę. Następnie czyta pliki — `main.py`, potem pliki w `routers/`, `models/`, `dependencies/`.]

Patrz — czyta plik po pliku, i sam decyduje co czytać jako następne. To nie jest grep po keywordach — to jest analiza kontekstu. Widzi że w routers jest obsługa użytkowników i przechodzi tam.

[SCREENCAST: W trakcie czytania Gemini zaczyna komentować co widzi — np. "W pliku routers/users.py linia 41 — surowe zapytanie SQL przez f-string zamiast parametryzowanego zapytania". Kontynuuje przeglądanie.]

Już widać pierwsze znalezisko — surowe zapytanie SQL sklejane przez f-string. To jest klasyczny SQL injection — zamiast przekazać parametry do silnika bazy, ktoś wkleił wartość od użytkownika bezpośrednio do stringa z zapytaniem. W FastAPI z SQLAlchemy ORM tego się nie robi nigdy — używasz ORM albo parametryzowanych zapytań.

[SCREENCAST: Gemini CLI kończy przeglądanie. Wypisuje listę znalezisk:]

```
KRYTYCZNE:
- SQL injection przez f-string — routers/users.py linia 41, 78
- DATABASE_URL hardcodowany w kodzie — main.py linia 12
- Brak rate limitingu na endpointach /auth/login i /auth/register

ŚREDNIE:
- Brak walidacji Pydantic na jednym endpointcie — routers/items.py linia 23
- Szczegółowe error messages ujawniają stack trace w response body

NISKIE:
- Brak logowania requestów (middleware)
- requirements.txt nie ma przypiętych wersji (tylko pakiety bez ==x.y.z)
```

[PAUZA]

Trzy krytyczne znaleziska. To pierwsze — DATABASE_URL w kodzie — widzę to regularnie w projektach które trafiają do mnie na audyt. Ktoś wkleił connection string z hasłem bezpośrednio w pliku, wrzucił na GitHuba, i od tej chwili każdy kto widzi repozytorium ma dostęp do bazy. To nie jest problem który wymaga hakowania — wystarczy zajrzeć do historii commitów.

[PAUZA]

Gemini CLI to wyłapał — nie dlatego że miał wbudowaną regułę "szukaj haseł w kodzie", ale dlatego że przeczytał db.js i rozumiał co widzi. To jest różnica między narzędziem statycznej analizy a agentem.

[ANIMACJA: Trzy kroki — "1. Prompt z konkretnym zakresem", "2. Agent czyta codebase autonomicznie", "3. Lista priorytetowa z plikiem i linią". Każdy krok osobno.]

Robię to przed każdym wdrożeniem nowego projektu na produkcję. Kwadrans, koszt minimalny, i mam pewność że wyłapałem przynajmniej oczywiste błędy zanim trafi do prawdziwych użytkowników.

---

## KIEDY TEGO UŻYWAĆ (16:30–17:45)

[ANIMACJA: Biały tekst na ciemnym tle — "KIEDY MA SENS?" — 2 sekundy. Fade out.]

Żeby być konkretnym — Gemini CLI nie jest dla każdego, i nie jest rozwiązaniem na wszystko. Ale dla kilku konkretnych przypadków jest bardzo trafiony.

[PAUZA]

Solo developer lub mały zespół bez dedykowanego DevOpsa — to jest prawdopodobnie największa grupa. Masz aplikację, masz serwer, ale nie jesteś ekspertem od infrastruktury i nie chcesz tracić dwóch godzin na konfigurację dockera każdy razem gdy wdrażasz nowy projekt. Gemini CLI robi za ciebie tę żmudną część — generuje, wyjaśnia, i zostawia ci coś co możesz przejrzeć i zrozumieć.

[PAUZA]

Code review przed deployem — to co pokazałem w Demo 2. Nie zastąpi profesjonalnego audytu bezpieczeństwa, ale jako pierwsza linia obrony przed oczywistymi błędami — jest bardzo praktyczne i kosztuje dosłownie kilka minut.

[PAUZA]

Onboarding do nieznanego projektu — Gemini CLI świetnie działa jako przewodnik po cudzym kodzie. Zamiast godziny na czytanie dokumentacji albo pytanie kogoś, pytasz agenta który przeczyta cały codebase i odpowie na konkretne pytania: co robi ten endpoint, dlaczego ta funkcja jest tu a nie tam, jakie są zależności między modułami.

[PAUZA]

Jedna rzecz którą warto powiedzieć wprost — to narzędzie ma dostęp do twoich plików i może wykonywać komendy w terminalu. Oznacza to że zanim użyjesz go na produkcji: wiesz co wpisujesz w prompt, widzisz co agent chce zrobić zanim to zatwierdzi. Nie jest to narzędzie do używania na ślepo. Ale używane świadomie, z dobrze napisanymi promptami — bardzo oszczędza czas na tych rzeczach które dotąd zajmowały nieproporcjonalnie dużo czasu w stosunku do ich trudności.

---

## CTA (17:45–18:30)

[PAUZA]

Jeśli chcesz sprawdzić to u siebie — instalacja to dwie minuty, klucz API jest darmowy, linki wrzuciłem w opis pod filmem: Gemini CLI na GitHubie, Google AI Studio i link do Hostingera jeśli szukasz serwera do tego typu projektów.

[PAUZA]

Jedno pytanie do ciebie — powiedz mi w komentarzu do czego byś to najpierw użył. Konfiguracja serwera jak w Demo 1, code review jak w Demo 2, a może coś całkowicie innego? Czytam każdy komentarz i często z takich odpowiedzi robię pomysły na kolejne filmy.

[PAUZA]

A jeśli interesujesz się automatyzacją AI w firmie szerzej — mam na kanale film o tym jak Gemini CLI wypada w porównaniu z Claude Code na konkretnych zadaniach B2B. Link pojawi się na ekranie. Dzięki za obejrzenie.

[ANIMACJA: End screen — miniatura YT-001 "Gemini CLI vs Claude Code", przycisk Subscribe, logo Dokodu w rogu. 20 sekund.]

---

## NOTATKI PRODUKCYJNE

### Screencasts do przygotowania
- Instalacja od zera na czystym terminalu — sekcja "Instalacja"
- Sprawdzenie `node --version`, pełna instalacja npm, uruchomienie `gemini`, konfiguracja klucza API
- Demo 1: sesja SSH na Hostingerze (zamazać IP), pełna sesja od `gemini` do stworzenia 3 plików
- Demo 2: lokalny projekt Python/FastAPI, pełna sesja od `gemini` do listy znalezisk
- Sekcja "Jak pisać prompty" — kamera na twarz + terminal, piszesz prompt na żywo z komentarzem

### Animacje Remotion (lista)
1. Opener — zielony tekst terminala "SSH... połączono" + "gemini" z kursorem
2. Title card "GEMINI CLI OD ZERA"
3. Schemat ReAct loop (Terminal → Gemini Cloud → Pliki/Serwer)
4. Lista features: czyta/pisze pliki, komendy shell, web search, 1M tokenów
5. Lista struktury dobrego promptu: Kontekst / Cel / Ograniczenia / Format
6. Podsumowanie instalacji: "Node.js 18+ | npm install -g @google/gemini-cli"
7. Porównanie Demo 1: "Ręcznie: ~60 min" vs "Gemini CLI: ~15 min"
8. Diagram Demo 2: Prompt → Agent czyta → Lista priorytetowa (plik + linia)
9. End screen z miniaturą YT-001 + subscribe

### Placement Hostingera
- Czas: ~8:30, otwarcie Demo 1
- Tekst: zawarty w scenariuszu (pierwsze dwa zdania sekcji Demo 1)
- Link w opisie: do uzupełnienia przez Kacpra (link afiliacyjny)

### ⚠️ Uwaga techniczna do nagrania
- Gemini CLI na darmowym planie ma niskie limity RPM dla modeli Pro
- Jeśli agent zatrzyma się i czeka — to jest 429 od API, nie błąd po twojej stronie
- Do nagrania KONIECZNIE podepnij kartę w AI Studio (Tier 1) — limity skaczą dramatycznie

### Opis YouTube

**Akapit 1 (SEO, max 155 zn.):**
Gemini CLI — instalacja od zera, jak pisać prompty, i 2 demo na żywo: konfiguracja serwera i code review projektu Python. Agent AI w terminalu, open source, za darmo.

**Akapit 2:**
W tym filmie pokazuję co to jest Gemini CLI i czym różni się od zwykłego chatbota, jak go zainstalować (npm, 2 minuty), jak pisać prompty które faktycznie działają — i dwa konkretne demo: wdrożenie API (FastAPI + docker-compose, nginx, .env) na VPS i przegląd bezpieczeństwa projektu Python pod kątem SQL injection i typowych błędów. Bez skryptów, na żywo.

**Akapit 3:**
Jeśli jesteś developerem, DevOpsem albo technicznym managerem który szuka narzędzi które oszczędzają czas na żmudnych zadaniach — ten film jest dla ciebie.

**Linki:**
🔗 Gemini CLI na GitHub: https://github.com/google-gemini/gemini-cli
🔗 Google AI Studio (klucz API): https://aistudio.google.com
🔗 Hostinger VPS: [LINK AFILIACYJNY]
🔗 Bezpłatna konsultacja AI dla firmy: https://dokodu.it/kontakt
📺 Gemini CLI vs Claude Code (5 testów): [LINK YT-001 po publikacji]

**Hashtagi:** #GeminiCLI #AIwTerminalu #AutomatyzacjaAI #DevOps #AIwFirmie

**Chapters:**
0:00 Hook — AI agent na serwerze produkcyjnym
0:40 Co to jest Gemini CLI (i czym różni się od chatbota)
3:30 Instalacja — 2 minuty od zera
5:30 Jak pisać prompty do agentów AI
8:30 Demo 1: Serwer VPS — docker-compose, nginx, .env (Hostinger)
13:00 Demo 2: Code review projektu backendowego
16:30 Kiedy warto używać Gemini CLI
17:45 CTA

### Tagi (18)
`gemini cli`, `gemini cli tutorial`, `gemini cli po polsku`, `ai agent terminal`, `ai w firmie`, `automatyzacja ai`, `docker compose ai`, `code review ai`, `devops ai`, `hostinger vps`, `ai dla firm`, `ai coding assistant`, `google gemini`, `agent ai`, `python bezpieczenstwo`, `fastapi tutorial`, `ai developer tools`, `jak pisać prompty`

### Thumbnail Brief
- **Twarz:** skupienie + lekkie zaskoczenie — "to naprawdę działa" — nie hype, bardziej "no dobra, OK"
- **Tekst:** "AI AGENT W TERMINALU" (biały bold, czarny obrys, max 3 linie)
- **Tło:** ciemne (#1C1C1E) z zieloną poświatą sugerującą terminal
- **Element graficzny:** ikonka terminala / komendy `>_` po lewej stronie
- **Logo:** Gemini star logo (Google) w prawym górnym rogu

---

*Scenariusz zaktualizowany: 2026-03-18*
*Długość szacunkowa przy normalnym tempie mówienia: ~17–18 minut*
*Sekcje do nagrania z promptera: Hook, Co to jest, Instalacja (komentarz), Jak pisać prompty, Demo 1 (komentarz), Demo 2 (komentarz), Kiedy używać, CTA*
