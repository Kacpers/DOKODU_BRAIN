---
type: backup
source: dokodu.it/blog/n8n/docker-instalacja-konfiguracja
backup_date: 2026-04-25
post_id: cmls1wo8r000mw3hsp24qlefa
title_original: n8n i Docker – instalacja i konfiguracja krok po kroku
metaTitle_original: n8n i Docker – instalacja i konfiguracja krok po kroku
status_original: published
publishedAt_original: 2025-09-10T00:00:00.000Z
note: Backup przed refresh — patrz BRIEF_REFRESH_<slug>.md dla planowanych zmian
---

# BACKUP: n8n i Docker – instalacja i konfiguracja krok po kroku

**URL:** https://dokodu.it/blog/n8n/docker-instalacja-konfiguracja
**Excerpt:** Jak postawić n8n w Dockerze? W tym przewodniku znajdziesz gotowe konfiguracje docker-compose, integracje z PostgreSQL, Redis, Qdrant i Baserow, a także wskazówki dotyczące reverse proxy i SSL. Kompletny poradnik dla początkujących i zaawansowanych.
**Tagi:** ['automatyzacja', 'Docker', 'Devops', 'Baserow', 'n8n', 'postgres', 'redis', 'qdrant']

---

# Original content (Markdown):

Czy zdarza Ci się codziennie wykonywać te same żmudne czynności - kopiować dane między systemami, ręcznie wysyłać powtarzalne e-maile lub aktualizować arkusze kalkulacyjne? Wyobraź sobie, że te rutynowe zadania mogą dziać się automatycznie, a Ty zyskasz czas na ważniejsze rzeczy. Właśnie do tego służy **n8n** - narzędzie do automatyzacji pracy, które pozwala tworzyć przepływy zadań (workflowy) w prosty, wizualny sposób, nawet jeśli nie jesteś programistą. Jeśli chcesz dowiedzieć się więcej o samym n8n - czym jest i jakie daje możliwości - koniecznie zajrzyj do naszego przewodnika: [**N8n – co to jest? Kompletny przewodnik od zera do eksperta w automatyzacji**](/blog/n8n).

W tym artykule skupimy się jednak na praktycznym aspekcie: **jak uruchomić i skonfigurować n8n za pomocą Dockera**. Pokażemy krok po kroku, jak postawić własną instancję n8n w kontenerze Docker, zarówno w podstawowej konfiguracji dla początkujących, jak i w bardziej zaawansowanej wersji produkcyjnej z dodatkowymi usługami wspomagającymi (np. bazą danych PostgreSQL, serwerem proxy Nginx z SSL, bazą danych typu Airtable, a nawet narzędziami do integracji ze sztuczną inteligencją). Dowiesz się też, jak zapewnić bezpieczeństwo dostępu do n8n, jak utrwalić dane i skalować to rozwiązanie wraz ze wzrostem obciążenia. Zaczynajmy\!

<AD:get-ebook>

## Dlaczego warto uruchomić n8n w Dockerze?

**Docker** to platforma do uruchamiania aplikacji w tzw. kontenerach, która zrewolucjonizowała sposób wdrażania oprogramowania. Jakie korzyści daje użycie Dockera w przypadku n8n?

* **Łatwa instalacja i konfiguracja:** Docker eliminuje konieczność ręcznej instalacji wszystkich zależności n8n. Wystarczy pobrać oficjalny obraz kontenera n8n, który zawiera już całe środowisko uruchomieniowe. Unikamy problemów typu „działa u mnie, nie działa u ciebie” - kontener zawiera zawsze tę samą, spójną konfigurację oprogramowania.

* **Izolacja i porządek:** Kontenery są odizolowane od systemu hosta, co oznacza, że uruchomienie n8n w Dockerze nie zaśmieci nam systemu globalnymi pakietami czy usługami. Możemy też łatwo uruchamiać różne wersje n8n lub inne usługi obok siebie bez konfliktów.

* **Łatwe aktualizacje i utrzymanie:** Aktualizacja n8n sprowadza się do podmiany obrazu Dockera na nowy i ponownego uruchomienia kontenera. Dane i konfiguracja mogą być przechowywane w wolumenach (o czym później), więc przy reinstalacji kontenera nie tracimy ustawień ani workflowów. Możemy również łatwo przenosić instalację n8n między serwerami - wystarczy zabrać ze sobą wolumeny z danymi.

* **Skalowalność i dodatkowe usługi:** Docker Compose (narzędzie do orkiestracji wielu kontenerów) pozwala nam uruchomić cały zestaw usług współpracujących z n8n jednym poleceniem. Możemy dodać bazę danych, serwer proxy, cache, czy inne narzędzia i wszystko zarządzać jako jedną całość. W środowisku produkcyjnym to wręcz standard - za chwilę pokażemy, jak takie usługi dołożyć.

W skrócie, korzystając z Dockera, szybciej wdrożysz n8n i zyskasz większą kontrolę nad środowiskiem. **Nie musisz być ekspertem od DevOps** - podstaw Docker można nauczyć się szybko, a jeśli dopiero zaczynasz z konteneryzacją, zajrzyj do naszego [kursu Dockera](https://dokodu.it/kursy/docker), gdzie krok po kroku tłumaczymy, jak działa Docker i jak z niego korzystać w praktyce.

<AD:n8n-hostinger-banner>

## Szybki start: Uruchomienie n8n w Dockerze (dla początkujących)

Zaczniemy od najprostszego scenariusza: uruchomienia n8n lokalnie lub na serwerze przy użyciu pojedynczego kontenera Docker. Załóżmy, że masz już zainstalowanego Dockera na swoim systemie (jeśli nie - wykonaj instalację zgodnie z dokumentacją dla Twojego systemu lub skorzystaj z wspomnianego kursu).

### 1. Pobranie obrazu n8n i pierwsze uruchomienie

Najprostszym sposobem na wypróbowanie n8n jest użycie polecenia docker run. Wystarczy jedno polecenie w terminalu, aby pobrać obraz i uruchomić kontener. Otwórz terminal na swoim serwerze lub komputerze i wykonaj:

```bash
docker run -it --rm
  -p 5678:5678
  -v ~/.n8n:/home/node/.n8n
  n8nio/n8n:latest
```
Omówmy krótko, co robi to polecenie:

* n8nio/n8n:latest - to oficjalny obraz Dockera z aplikacją n8n (wersja „latest” zapewnia najnowszą stabilną wersję n8n).

* \-p 5678:5678 - przekierowuje port 5678 z kontenera na port 5678 hosta. Domyślnie n8n nasłuchuje na porcie 5678 (HTTP). Po uruchomieniu będziesz mógł wejść na interfejs n8n, otwierając przeglądarkę pod adresem http://localhost:5678 (jeśli uruchamiasz lokalnie) lub http://adres-twojego-serwera:5678.

* \-v \~/.n8n:/home/node/.n8n - montuje wolumen (katalog z danymi). Ten parametr zapewnia **utrwalenie danych** n8n. Wszystkie ustawienia, utworzone workflowy, a także plik bazy danych SQLite i klucz szyfrujący do haseł będą zapisane w lokalnym folderze \~/.n8n (w katalogu domowym użytkownika). Dzięki temu po zatrzymaniu czy ponownym uruchomieniu kontenera Twoje dane nie znikną.

* \-it \--rm - uruchamia kontener w trybie interaktywnym i usuwa go po zatrzymaniu (to opcjonalne dla prostego testu; w docelowej instalacji użyjemy innego podejścia).

Po wykonaniu polecenia obraz zostanie pobrany (o ile nie masz go już w cache) i n8n wystartuje. W logach kontenera powinieneś zobaczyć komunikaty uruchamiania. Teraz wejdź na adres http://localhost:5678 (lub odpowiedni adres serwera) - powinna ukazać się strona powitalna n8n.

**Pierwsze uruchomienie n8n - konfiguracja konta:** Przy pierwszym uruchomieniu n8n wyświetla ekran powitalny, w którym możesz opcjonalnie utworzyć konto użytkownika (adres e-mail i hasło) lub kliknąć „Skip setup for now” (pomiń na teraz). **Uwaga:** w celach testowych możesz pominąć zakładanie konta, ale w środowisku produkcyjnym zaleca się **nie pomijać** logowania. Jeśli pominiesz, n8n będzie dostępne bez żadnej autoryzacji, co stanowiłoby ryzyko bezpieczeństwa, gdyby instancja była dostępna publicznie. Za chwilę pokażemy, jak wymusić zabezpieczenie dostępu hasłem.

Na tym etapie masz działające n8n. Możesz już tworzyć pierwsze workflowy, korzystając z intuicyjnego edytora webowego. Dane (workflowy, dane połączeń itp.) są przechowywane w kontenerze, a dzięki montowaniu wolumenu - również na dysku hosta (w folderze \~/.n8n). **Domyślnie n8n korzysta z wbudowanej bazy SQLite** do przechowywania konfiguracji. SQLite to prosta plikowa baza danych, która sprawdza się w początkach, ale ma pewne ograniczenia (o czym później).

<AD:docker>

### 2. Konfiguracja docker-compose (wygodniejsze zarządzanie)

Do codziennego użytku i zwłaszcza do bardziej złożonych konfiguracji warto użyć **Docker Compose**. Compose pozwala opisać konfigurację kontenerów w pliku YAML, dzięki czemu łatwo uruchomisz cały zestaw poleceniem docker-compose up \-d. Przygotujmy prosty plik docker-compose.yml dla n8n.

Utwórz na serwerze katalog (np. n8n), a w nim plik o nazwie docker-compose.yml. Wklej poniższą zawartość:

```bash
services:  
  n8n:  
    image: n8nio/n8n:latest  
    restart: always  
    ports:  
      - "5678:5678"  
    environment:  
      - N8N_BASIC_AUTH_USER=admin  
      - N8N_BASIC_AUTH_PASSWORD=TwojeTrudneHasło123  
      - N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true  
      # - N8N_USER_MANAGEMENT_DISABLED=true   # (nie ustawiaj tego w produkcji, to tylko opcja awaryjna)  
    volumes:  
      - n8n_data:/home/node/.n8n

volumes:  
  n8n_data:
```

Zwróć uwagę na kilka elementów tej konfiguracji:

* **restart: always** - dzięki temu kontener n8n będzie automatycznie uruchamiany przy starcie systemu oraz ponownie uruchamiany w razie awarii.

* **N8N\_BASIC\_AUTH\_USER / PASSWORD** - te zmienne środowiskowe włączają proste uwierzytelnianie HTTP Basic do interfejsu n8n. Ustawiając je, sprawisz, że przy wejściu na interfejs n8n przeglądarka poprosi o podanie loginu i hasła (zdefiniowanych tu jako użytkownik admin i Twoje hasło). Jest to najprostszy sposób zabezpieczenia dostępu, szczególnie przydatny jeśli nie skonfigurowałeś jeszcze kont użytkowników n8n. **Pamiętaj, by użyć silnego hasła**. W razie potrzeby możesz też ustawić nazwę użytkownika inną niż admin. (Zmienna N8N\_BASIC\_AUTH\_PASSWORD powinna być oczywiście ustawiona na trudne, unikalne hasło - w powyższym przykładzie wpisz własne).

* **N8N\_ENFORCE\_SETTINGS\_FILE\_PERMISSIONS=true** - ta flaga dba o prawidłowe uprawnienia do plików konfiguracyjnych n8n wewnątrz kontenera. Jest zalecana, zwłaszcza jeśli uruchamiasz n8n z uprawnieniami użytkownika non-root (co domyślnie ma miejsce w obrazie n8n). W praktyce zapobiega to sytuacjom, w których pliki ustawień lub bazy nie mają właściwych uprawnień po montowaniu wolumenu.

* **N8N\_USER\_MANAGEMENT\_DISABLED** - (skomentowane) ta zmienna służy do całkowitego wyłączenia mechanizmu zarządzania użytkownikami w n8n, co powoduje brak ekranu logowania w ogóle. **Nie zalecamy wyłączać logowania w środowisku produkcyjnym.** Opcję tę podajemy jedynie informacyjnie - może być przydatna w specyficznych sytuacjach (np. gdy chcesz polegać tylko na Basic Auth i nigdy nie tworzyć kont w n8n). Standardowo jednak lepiej pozostawić system użytkowników włączony i utworzyć konto administratora na starcie (lub skorzystać z Basic Auth jako dodatkowej warstwy ochrony).

* **volumes \-\> n8n\_data** - definiujemy named volume n8n\_data, który będzie przechowywał dane n8n (tak jak wcześniej folder \~/.n8n). Dzięki temu dane przetrwają restart kontenera. Docker sam zarządza lokalizacją takiego wolumenu. Alternatywnie możesz zamiast named volume użyć ścieżki na dysku, np. \- ./n8n\_data:/home/node/.n8n - wtedy dane będą trzymane w podkatalogu obok pliku compose.

Aby uruchomić n8n z użyciem Docker Compose, w katalogu z plikiem docker-compose.yml wykonaj polecenie:

```bash
docker-compose up -d
```

Po chwili kontener powinien wystartować w tle (dzięki flagom \-d). Sprawdź, czy działa: docker-compose ps pokaże listę uruchomionych usług. Wejdź w przeglądarce na adres jak poprzednio (http://localhost:5678 lub domena/adres IP serwera). Teraz **powinieneś zobaczyć okienko logowania** wymagające podania nazwy użytkownika i hasła - to nasza skonfigurowana autoryzacja Basic Auth. Po zalogowaniu (użyj admin i swojego hasła) ukaże się panel n8n. Dodatkowo, jeśli wcześniej nie tworzyłeś konta w n8n, nadal zobaczysz wewnątrz n8n opcję konfiguracji użytkownika (chyba że wyłączyłeś ją zmienną, czego nie zalecamy). Możesz więc założyć w n8n konto administratora, co pozwoli korzystać z funkcji wieloużytkownikowych i np. zabezpieczyć instancję 2FA itp.

Gratulacje - masz działającą instancję n8n w Dockerze\! Powyższa konfiguracja jest świetna na początek lub do użytku osobistego. W kolejnych sekcjach zajmiemy się rozbudową tego środowiska do bardziej produkcyjnego zastosowania.

## Utrwalanie danych i wydajność: zewnętrzna baza danych PostgreSQL

Domyślnie n8n korzysta z plikowej bazy SQLite (umieszczonej w wolumenie, dzięki czemu dane nie znikają). SQLite jest prostym rozwiązaniem, ale **nie jest polecana do intensywnego, produkcyjnego użytku**. Przy większej liczbie workflowów i równoległych operacji SQLite może stać się wąskim gardłem (jest jednowątkowa) i istnieje ryzyko uszkodzenia pliku bazy np. przy nagłym wyłączeniu kontenera. Dlatego twórcy n8n zalecają użycie zewnętrznej bazy danych - **PostgreSQL** - do przechowywania danych n8n.

PostgreSQL to potężna, open-source’owa baza danych SQL, znana ze swojej stabilności i wydajności. n8n natywnie wspiera Postgresa - wystarczy odpowiednio ustawić zmienne środowiskowe, by korzystał z bazy zamiast SQLite. Pokażemy teraz, jak dodać serwer Postgres do naszego Docker Compose oraz jak skonfigurować n8n, by z niego korzystał.

### Dodanie usługi PostgreSQL do Docker Compose

Rozszerzmy nasz plik docker-compose.yml o nowy serwis **postgres**. Umieścimy go obok definicji n8n:

```bash
services:  
  postgres:  
    image: postgres:16  
    restart: always  
    environment:  
      - POSTGRES_USER=n8n_user  
      - POSTGRES_PASSWORD=BezpieczneHasloDoBazy  
      - POSTGRES_DB=n8n  
    volumes:  
      - db_storage:/var/lib/postgresql/data  
    networks:  
      - backend

  n8n:  
    image: n8nio/n8n:latest  
    restart: always  
    depends_on:  
      - postgres  
    environment:  
      - DB_TYPE=postgresdb  
      - DB_POSTGRESDB_HOST=postgres  
      - DB_POSTGRESDB_PORT=5432  
      - DB_POSTGRESDB_DATABASE=n8n  
      - DB_POSTGRESDB_USER=n8n_user  
      - DB_POSTGRESDB_PASSWORD=BezpieczneHasloDoBazy  
      ... (pozostałe zmienne jak wcześniej)  
    volumes:  
      - n8n_data:/home/node/.n8n  
    networks:  
      - backend  
      - proxy   # (więcej o tej sieci "proxy" powiemy później)
```

Dodaliśmy:

* **Serwis postgres:** korzystamy z oficjalnego obrazu postgres:16 (wersja 16 Postgresa). Dzięki zmiennym środowiskowym POSTGRES\_USER, POSTGRES\_PASSWORD i POSTGRES\_DB kontener automatycznie utworzy użytkownika, hasło i bazę danych o podanych nazwach przy pierwszym uruchomieniu. W powyższym przykładzie tworzymy użytkownika n8n\_user z hasłem (podaj własne silne hasło) i bazę danych o nazwie n8n. Te dane muszą się pokrywać z konfiguracją w n8n (o tym za chwilę). Montujemy również wolumen db\_storage do /var/lib/postgresql/data - to tam Postgres przechowuje dane bazy na dysku. Dzięki temu baza nie zniknie przy restarcie kontenera.

* **networks.backend:** utworzyliśmy (lub raczej zadeklarowaliśmy, bo definicję sieci damy na dole pliku) sieć Docker o nazwie backend, na której komunikują się usługi wewnętrzne. Umieszczamy w niej Postgresa oraz n8n, aby n8n mógł łączyć się z bazą po wewnętrznej nazwie hosta.

* **Konfiguracja n8n dla Postgresa:** dodaliśmy zmienne środowiskowe DB\_TYPE i DB\_POSTGRESDB\_... zgodnie z dokumentacją[\[4\]](https://docs.n8n.io/hosting/configuration/supported-databases-settings/#:~:text=PostgresDB). Ustawienia w naszym przykładzie:

* DB\_TYPE=postgresdb - informuje n8n, że ma używać bazy postgres (zamiast SQLite).

* DB\_POSTGRESDB\_HOST=postgres - nazwa hosta bazy. Ponieważ nasz kontener Postgres nazywa się postgres i jest w tej samej sieci, n8n może się z nim połączyć używając nazwy kontenera jako hosta (Docker Compose ustawia odpowiedni DNS dla usług w tej samej sieci).

* DB\_POSTGRESDB\_PORT=5432 - domyślny port Postgresa.

* DB\_POSTGRESDB\_DATABASE=n8n - nazwa bazy, której ma używać n8n (tę bazę utworzyliśmy zmienną POSTGRES\_DB).

* DB\_POSTGRESDB\_USER=n8n\_user i DB\_POSTGRESDB\_PASSWORD=... - poświadczenia do bazy (zgodne z POSTGRES\_USER i POSTGRES\_PASSWORD z konfiguracji Postgresa).

* **depends\_on:** dodaliśmy zależność, by n8n startował po uruchomieniu kontenera Postgres (zapewnia to poprawną kolejność przy starcie).

* **networks:** nasz n8n pozostał również w sieci proxy (o niej później), a dodatkowo dołączyliśmy go do sieci backend, aby widział usługę Postgres. Można jedną usługę przypisać do wielu sieci w Docker Compose.

Na końcu pliku należy jeszcze zdefiniować utworzone sieci i wolumeny, np.:

```bash
networks:  
  backend:  
  proxy:

volumes:  
  n8n_data:  
  db_storage:
```

Po wprowadzeniu tych zmian, uruchom (lub przeładuj) całość komendą docker-compose up \-d \--build (jeśli zmieniałeś istniejący plik). Kontener Postgresa zostanie utworzony i zainicjalizowany, a n8n wystartuje tym razem łącząc się z bazą danych Postgres.

**Jak upewnić się, że n8n korzysta z Postgresa?** W praktyce, jeśli konfiguracja jest poprawna, zmiana ta będzie dla Ciebie niewidoczna - n8n działa tak samo, interfejs nie zdradza typu bazy. Możesz jednak zajrzeć do logów kontenera n8n (docker-compose logs n8n) - powinna tam być linijka potwierdzająca połączenie z bazą Postgres (lub ewentualne błędy, jeśli coś poszło nie tak). Dodatkowo możesz spróbować zatrzymać kontener Postgresa - wtedy n8n powinien zgłaszać problemy z połączeniem do bazy, co potwierdzi, że faktycznie z niej korzysta.

**Zalety użycia PostgreSQL:** Teraz Twoje dane n8n (workflowy, historia wykonania, dane uwierzytelnień itp.) są przechowywane w **serwerze bazodanowym**, który lepiej radzi sobie z dużą liczbą operacji równoległych i zapewnia większe bezpieczeństwo przed utratą danych niż pojedynczy plik. PostgreSQL można także łatwo backupować (np. za pomocą narzędzia pg\_dump) i odtwarzać w razie potrzeby. Warto nadmienić, że n8n oficjalnie wspiera obecnie PostgreSQL jako zewnętrzną bazę (dawniej wspierał też MySQL/MariaDB, ale ta opcja została wycofana, więc trzymając się Postgresa zapewniamy zgodność z przyszłymi wersjami n8n.

**Dobra praktyka:** w środowisku produkcyjnym rozważ przechowywanie haseł dostępu do bazy i innych wrażliwych danych w pliku .env, zamiast wpisywać je bezpośrednio w pliku docker-compose. Docker Compose umożliwia użycie env\_file lub referencji do zmiennych z pliku. W ten sposób hasła nie będą od razu widoczne w konfiguracji (łatwiej je też zmienić w jednym miejscu). Upewnij się tylko, że nie publikujesz tego pliku .env. Możesz też skorzystać z mechanizmu Docker Secrets dla jeszcze lepszego zabezpieczenia haseł.

## Dodanie serwera proxy i HTTPS (Nginx + Certbot) - udostępnienie n8n w Internecie

Powyższa konfiguracja n8n \+ Postgres jest w pełni funkcjonalna, ale działa na domyślnym porcie 5678 i protokole HTTP. W praktyce, gdy chcesz korzystać z n8n na własnym serwerze (np. VPS) i udostępnić go publicznie, warto zadbać o dwie rzeczy:

1. **Ładny adres (domena)** - zamiast łączyć się po adresie IP i niestandardowym porcie, lepiej użyć własnej domeny (np. automation.twojadomena.pl czy jakiejkolwiek) i przekierować ruch na n8n. Dzięki temu linki do webhooków i integracji będą wyglądać profesjonalnie, a korzystanie z panelu będzie wygodniejsze.

2. **Szyfrowanie HTTPS** - bezpieczeństwo przede wszystkim. Powinniśmy wystawić nasz serwer n8n po HTTPS (z ważnym certyfikatem SSL), aby zarówno panel, jak i webhooki były szyfrowane. W dzisiejszych czasach uzyskanie certyfikatu jest na szczęście zautomatyzowane dzięki **Let’s Encrypt**.

Do osiągnięcia powyższych celów najpopularniejszym rozwiązaniem jest użycie **reverse proxy** - serwera, który odbierze ruch na standardowych portach web (80 i 443\) i przekaże go do właściwego kontenera n8n. My skorzystamy z **Nginx**, który jest lekki i powszechnie używany jako proxy. W duecie z Nginxem uruchomimy kontener **Certbot**, który zadba o uzyskanie i automatyczne odnawianie certyfikatu SSL z Let’s Encrypt.

### Konfiguracja Nginx jako proxy dla n8n

Dodajmy kolejną usługę do naszego docker-compose.yml:

```bash
services:  
  nginx:  
    image: nginx:latest  
    restart: always  
    depends_on:  
      - n8n  
    volumes:  
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro  
      - certbot-etc:/etc/letsencrypt  
      - certbot-var:/var/lib/letsencrypt  
      - ./html:/var/www/html  
    ports:  
      - "80:80"  
      - "443:443"  
    networks:  
      - proxy
```
Oraz usługę Certbot:
```bash
  certbot:  
    image: certbot/certbot  
    volumes:  
      - certbot-etc:/etc/letsencrypt  
      - certbot-var:/var/lib/letsencrypt  
      - ./html:/var/www/html  
    entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"  
    networks:  
      - proxy
```
Omówmy te elementy:

* **nginx (serwis):** używamy oficjalnego obrazu Nginx. Montujemy do kontenera plik konfiguracyjny nginx.conf (który musimy przygotować obok, w tym samym katalogu). Montujemy również dwa wolumeny certbot-etc i certbot-var oraz katalog ./html. Już wyjaśniamy po co:

* Wolumeny certbot-etc i certbot-var służą do przechowywania uzyskanych certyfikatów Let’s Encrypt oraz danych potrzebnych do ich odnowienia. Będą współdzielone między Nginx a Certbotem. Certbot zapisuje certyfikaty w /etc/letsencrypt/live/... (dlatego montujemy certbot-etc tam), a pewne dane w /var/lib/letsencrypt.

* Katalog ./html to prosty katalog, który posłuży jako tzw. webroot dla wyzwania HTTP-01 Let’s Encrypt. Certbot umieszcza tam plik z wyzwaniem, a Nginx musi go serwować na żądanie podczas weryfikacji domeny. Tworzymy po prostu pusty katalog html lokalnie i montujemy go zarówno w Nginx (/var/www/html) jak i w Certbocie (pod tą samą ścieżką). Dzięki temu mechanizmowi Certbot może potwierdzić, że mamy kontrolę nad domeną (więcej szczegółów za moment).

* depends\_on: \- n8n - upewniamy się, że n8n wystartuje zanim Nginx (co jest istotne, by proxy miało do czego kierować ruch).

* **ports "80:80" i "443:443":** wystawiamy porty HTTP i HTTPS na zewnątrz. Port 80 posłuży do chwilowego przeprowadzania challenge (i ewentualnie przekierowania na HTTPS), a port 443 to docelowy szyfrowany ruch do aplikacji.

* **networks \- proxy:** Nginx jest podłączony do sieci proxy, podobnie n8n (przypięliśmy wcześniej n8n do tej sieci). Dzięki temu Nginx może kierować ruch do kontenera n8n po nazwie hosta.

* **certbot (serwis):** korzystamy z oficjalnego obrazu Certbota (klient Let’s Encrypt). Montujemy te same wolumeny i katalog html. entrypoint został ustawiony w dość sprytny sposób: uruchamiamy w kontenerze pętlę, która co 12 godzin wykonuje certbot renew i czeka. Oznacza to, że kontener będzie na bieżąco odnawiał certyfikat, gdy przyjdzie na to pora (certyfikaty Let’s Encrypt są ważne 3 miesiące, ale zwyczajowo odświeża się je co \~60 dni). **Ważne:** ten kontener w powyższej konfiguracji zakłada, że certyfikat został już wcześniej uzyskany. Musimy więc jeszcze zająć się pierwszym wydaniem certyfikatu (Certbot renew odnawia istniejące certyfikaty, nie wydaje nowych).

**Konfiguracja pliku nginx.conf:** Stwórzmy teraz plik nginx.conf w tym samym katalogu, co docker-compose. Będzie on definiował serwer wirtualny dla naszej domeny. Przykładowa konfiguracja może wyglądać tak (dopasuj ją do swojej domeny\!):

```bash
server {  
    listen 80;  
    server_name twoja.domena.pl;

    # Obsługa challenge Let's Encrypt (ścieżka .well-known):  
    location ^\~ /.well-known/acme-challenge/ {  
        root /var/www/html;  
    }

    # Opcjonalnie przekierowanie HTTP -> HTTPS (po otrzymaniu certyfikatu):  
    location / {  
        return 301 https://$host$request_uri;  
    }  
}

server {  
    listen 443 ssl;  
    server_name twoja.domena.pl;

    ssl_certificate /etc/letsencrypt/live/twoja.domena.pl/fullchain.pem;  
    ssl_certificate_key /etc/letsencrypt/live/twoja.domena.pl/privkey.pem;  
    ssl_trusted_certificate /etc/letsencrypt/live/twoja.domena.pl/chain.pem;  
    include /etc/letsencrypt/options-ssl-nginx.conf;  
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location / {  
        proxy_pass http://n8n:5678;  
        proxy_set_header Host $host;  
        proxy_set_header X-Real-IP $remote_addr;  
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;  
        proxy_set_header X-Forwarded-Proto https;  
        proxy_buffering off;  
    }  
}
```

Co tu się dzieje:

* Pierwszy **server{}** na porcie 80 obsługuje naszą domenę bez SSL. Wewnątrz mamy lokalizację /.well-known/acme-challenge/ wskazującą na katalog /var/www/html - to jest dokładnie miejsce, gdzie Certbot będzie wrzucał pliki wyzwań. Dzięki temu gdy Let’s Encrypt sprawdzi http://twoja.domena.pl/.well-known/acme-challenge/\<token\>, Nginx zaserwuje plik z naszego folderu i weryfikacja przejdzie pomyślnie. Dodatkowo (już po otrzymaniu certyfikatu) ustawiliśmy domyślne przekierowanie wszystkich innych żądań na port 443 (HTTPS) - to poprawia bezpieczeństwo i doświadczenie użytkownika (wszyscy trafią na wersję szyfrowaną).

* Drugi **server{}** słucha na porcie 443 z włączonym SSL. Wskazujemy pliki certyfikatu wygenerowane przez Certbot (będą dostępne w /etc/letsencrypt/live/... w kontenerze Nginx, bo współdzielimy wolumen). Linia include /etc/letsencrypt/options-ssl-nginx.conf; oraz ssl\_dhparam dodają bezpieczne domyślne ustawienia SSL (Certbot generuje ten plik i parametry Diffie-Hellmana przy pierwszym uruchomieniu). W bloku location / definiujemy przekierowanie ruchu do aplikacji n8n:

* proxy\_pass http://n8n:5678; - tutaj ważna rzecz: używamy nazwy hosta n8n, która rozwiązuje się do kontenera n8n wewnątrz sieci proxy. Port docelowy to 5678, czyli dokładnie tam, gdzie n8n nasłuchuje. Dzięki temu każdy URL trafiający do Nginxa na port 443 zostanie przekazany do n8n.

* Ustawiamy też nagłówki Host, X-Real-IP, X-Forwarded-For i X-Forwarded-Proto - to standardowe nagłówki proxy informujące aplikację o oryginalnym adresie IP klienta i protokole. Szczególnie ważny jest X-Forwarded-Proto https, ponieważ n8n musi wiedzieć, że klient używał HTTPS (przyda się to np. do generowania poprawnych linków w webhookach).

* proxy\_buffering off; - wyłączamy buforowanie, aby zapewnić, że odpowiedzi (zwłaszcza streaming, jak w niektórych integracjach) nie będą wstrzymywane przez Nginx.

**Uzyskanie certyfikatu Let’s Encrypt (pierwsze uruchomienie):** Teraz najważniejsze - zanim Nginx będzie mógł serwować HTTPS, musimy zdobyć certyfikat. Jak to zrobić w naszym kontekstie Docker Compose? Mamy kilka opcji: \- Możemy tymczasowo uruchomić kontener Certbot w trybie jednorazowym, by pobrał certyfikat. Np. poleceniem (wykonanym **na hoście**):

```bash
docker compose run --rm certbot certonly --webroot -w /var/www/html -d twoja.domena.pl --email twój-email@example.com --agree-tos --no-eff-email
```

To polecenie uruchomi kontener Certbot (używając definicji z compose) i wykona komendę certonly z odpowiednimi parametrami: \- \--webroot \-w /var/www/html mówi Certbotowi, żeby użył metodę webroot (czyli wrzucił plik do katalogu /var/www/html - który mamy zmapowany na Nginx). \- \-d twoja.domena.pl - podaj swoją domenę (możesz też podać kilka domen/innych subdomen jeśli certyfikat ma być wielodomenowy, dodając kolejne \-d). \- \--email i \--agree-tos są wymagane przy pierwszym rejestracji - akceptujemy warunki usługi Let’s Encrypt i podajemy kontaktowy email (dostaniesz tam ewentualne powiadomienia o odnowieniach). \- \--no-eff-email to opcjonalnie, by nie rejestrować się na newsletter EFF.

Jeśli wszystko jest poprawnie skonfigurowane (domena wskazuje na Twój serwer, port 80 jest dostępny), Certbot umieści plik wyzwania w ./html, Nginx (który już powinien być uruchomiony) go zaserwuje, Let’s Encrypt zweryfikuje i certyfikat zostanie zapisany w wolumenie. W logach powinieneś zobaczyć „Congratulations\!” i ścieżki do wygenerowanych certyfikatów. \- Alternatywnie, możesz przeprowadzić ten proces poza Docker Compose (np. instalując certbot lokalnie lub korzystając z opcji standalone), ale skorzystanie z istniejącego kontenera jak wyżej jest proste i nie wymaga niczego dodatkowego.

Po tym jednorazowym kroku certyfikat jest gotowy. Teraz upewnij się, że kontener Nginx został zrestartowany (aby załadować certyfikat) - w praktyce, jeśli docker-compose run zakończył pracę, nasze Nginx i tak już chodził w tle. Można go zrestartować komendą docker-compose restart nginx. Gdy Nginx wstanie, powinien już używać certyfikatu i obsługiwać ruch HTTPS na Twojej domenie.

**Dostosowanie ustawień n8n do pracy za proxy:** Kiedy n8n działa za reverese proxy pod własną domeną, warto ustawić w n8n dwie zmienne środowiskowe informujące go o swoim zewnętrznym adresie: \- N8N\_HOST - tu wpisujemy nazwę hosta (domenę) pod jaką dostępny jest n8n, **bez protokołu**. Np. N8N\_HOST=twoja.domena.pl. n8n używa tego m.in. przy generowaniu linków w niektórych kontekstach (np. w wysyłanych e-mailach z zaproszeniami użytkowników). \- WEBHOOK\_URL - pełny adres URL do webhooków, jaki ma być używany. Np. WEBHOOK\_URL=https://twoja.domena.pl/. Dlaczego to ważne? Ponieważ gdy tworzysz w n8n workflow wykorzystujący **Webhook** (lub inne triggery sieciowe), n8n musi wiedzieć, jaki publiczny URL ma zgłosić. Domyślnie, jeśli nie ustawimy nic, n8n zgaduje URL na podstawie adresu hosta kontenera i protokołu - co w przypadku proxy nie zadziała poprawnie. Ustawiając WEBHOOK\_URL zapewniasz, że np. link przekazywany zewnętrznym usługom (webhook callback) będzie zawierał Twoją domenę i HTTPS.

Dodaj powyższe zmienne do sekcji environment usługi n8n w compose. W naszym wcześniejszym przykładzie mogłoby to wyglądać tak:

```bash
    environment:  
      - N8N_BASIC_AUTH_USER=admin  
      - N8N_BASIC_AUTH_PASSWORD=TwojeTrudneHasło123  
      - N8N_HOST=twoja.domena.pl 
      - WEBHOOK_URL=https://twoja.domena.pl/  
      - N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true  
      - DB_TYPE=postgresdb  
      ... (reszta zmiennych DB)
```

Po takiej zmianie zrestartuj n8n (docker-compose up \-d ponownie). Od tej pory np. przy tworzeniu nowego **Webhook Trigger** w n8n, zobaczysz w UI pełny URL zaczynający się od https://twoja.domena.pl/... - gotowy do użycia. 🎉

Masz teraz w pełni działającą instancję n8n, zabezpieczoną, z własną domeną i certyfikatem SSL. To już dość profesjonalna konfiguracja, której można używać w realnych projektach. Ale to nie koniec - możemy rozbudować nasz ekosystem o kolejne narzędzia, które zwiększą możliwości platformy.

## Dodatkowe usługi towarzyszące - rozszerzanie możliwości n8n

Jedną z zalet korzystania z Dockera jest łatwość dołączania różnych komplementarnych serwisów. W przypadku n8n istnieje wiele narzędzi, które świetnie uzupełniają jego funkcjonalność. Poniżej opiszemy kilka usług, które możesz rozważyć dodając do swojego stacku z n8n, wraz z wyjaśnieniem, do czego służą i jakie korzyści dają.

### Baserow - self-hosted “Airtable” jako baza danych no-code

**Baserow** to open-source’owa platforma do budowania baz danych i aplikacji bez kodu, pełniąca rolę alternatywy dla Airtable. Mówiąc prościej, Baserow pozwala tworzyć tabele, arkusze i bazy danych poprzez interfejs webowy, współdzielić je i zarządzać danymi w przystępny sposób - a wszystko to możesz hostować samodzielnie.

Dlaczego warto zainteresować się Baserow w kontekście n8n? Ponieważ n8n doskonale integruje się z Baserow - istnieją dedykowane **nody Baserow** w n8n, które pozwalają m.in. odczytywać, dodawać czy aktualizować rekordy w bazach Baserow. Dzięki temu możesz użyć Baserow jako **łatwego backendu do przechowywania danych** dla swoich automatyzacji. Przykłady zastosowań: \- Tworzysz automatyzację, która zbiera dane z różnych źródeł (API, formularzy, plików) i chcesz je zapisać w centralnej bazie - Baserow świetnie się do tego nadaje, bo możesz potem te dane ręcznie przeglądać, filtrować lub edytować przez przyjazny interfejs. \- Chcesz udostępnić pewne dane lub konfiguracje osobom nietechnicznym - zamiast dawać im dostęp do n8n, mogą korzystać z tabel Baserow (np. dział marketingu może edytować listę treści czy słów kluczowych w Baserow, a n8n będzie automatycznie pobierać te dane i wykonywać na nich zaplanowane zadania). \- Baserow może służyć jako źródło wyzwalaczy - np. zmiana danych w Baserow może wywołać webhook do n8n (choć tu trzeba trochę konfiguracji), lub n8n może okresowo sprawdzać nowe rekordy.

Dodanie Baserow do naszego środowiska Docker Compose jest dość proste, ponieważ projekt ten dostarcza oficjalny obraz Dockera. Baserow wymaga jednak również własnej bazy danych (PostgreSQL) oraz usługi Redis (używanej do cache i wsparcia czasu rzeczywistego). W naszym przypadku mamy już uruchomiony serwer Postgres, więc możemy go wykorzystać również dla Baserow (tworząc osobną bazę i użytkownika dla niego). Redis będziemy musieli dodać.

**Konfiguracja Baserow w Docker Compose (przykład):**

```bash
services:  
  redis:  
    image: redis:7-alpine  
    restart: always  
    command: ["redis-server", "--requirepass", "StrongRedisPass123"]  
    volumes:  
      - redis_data:/data  
    networks:  
      - backend

  baserow:  
    image: baserow/baserow:1.31.1  
    restart: unless-stopped  
    environment:  
      - BASEROW_PUBLIC_URL=http://twoja.domena.pl:8081  
      - SECRET_KEY=super_tajny_ciag_znakow  
      - DATABASE_HOST=postgres  
      - DATABASE_USER=n8n_user        # (lub osobny użytkownik, np. baserow_user)  
      - DATABASE_PASSWORD=BezpieczneHasloDoBazy  
      - DATABASE_NAME=baserow_db  
      - REDIS_HOST=redis  
      - REDIS_PASSWORD=StrongRedisPass123  
    volumes:  
      - baserow_data:/baserow/data  
    ports:  
      - "8081:80"  
      - "8444:443"  
    networks:  
      - backend  
      - proxy
```

Co tu robimy: \- **redis:** dodajemy lekką wersję obrazu Redis. Redis to bardzo szybki magazyn klucz-wartość w pamięci, często używany jako cache lub broker komunikatów. Baserow korzysta z niego dla poprawy wydajności i obsługi niektórych funkcji (np. powiadomień w czasie rzeczywistym w interfejsie). W konfiguracji podaliśmy polecenie startowe, by Redis wymagał hasła (dobrze jest zabezpieczyć Redis, choć i tak nie wystawiamy go na świat, tylko działa w sieci wewnętrznej). Hasło ustawiliśmy (pamiętaj podmienić na własne). Montujemy wolumen redis\_data na /data - w razie czego Redis może zapisywać dane na dysk (choć głównie trzyma w pamięci). \- **baserow (serwis):** korzystamy z obrazu baserow w konkretnej wersji (1.31.1 w tym przypadku). W zmiennych środowiskowych konfigurujemy go: \- BASEROW\_PUBLIC\_URL - **ważne**, tutaj podaj adres pod jakim będzie dostępny Baserow. W przykładzie użyliśmy http://twoja.domena.pl:8081 zakładając, że na potrzeby Baserow użyjemy innego portu lub subdomeny. (Można wystawić Baserow też za tym samym Nginx proxy na innej ścieżce lub subdomenie - to zależy od preferencji. Dla uproszczenia używamy portu 8081 w przykładzie, ale docelowo możesz np. ustawić osobną subdomenę i dodać konfigurację do Nginxa). \- SECRET\_KEY - klucz tajny używany przez Baserow (do podpisywania cookies, szyfrowania haseł itp.). Powinien to być długi, unikalny ciąg znaków (losowy). Traktuj go podobnie jak N8N\_ENCRYPTION\_KEY - zachowaj i nie ujawniaj. \- DATABASE\_HOST, DATABASE\_USER, DATABASE\_PASSWORD, DATABASE\_NAME - konfiguracja dostępu do bazy PostgreSQL. Zakładamy tu, że *korzystamy z tego samego kontenera Postgres co n8n*, tworząc w nim nową bazę o nazwie baserow\_db oraz użytkownika (w powyższym przykładzie użyliśmy dla uproszczenia tego samego użytkownika n8n\_user, który ma dostęp do baserow\_db - można jednak lepiej utworzyć osobnego np. baserow\_user z właściwymi prawami tylko do tej bazy). Nasz skrypt inicjalizujący bazę (lub ręczne polecenia) powinny tę bazę i użytkownika utworzyć. **Uwaga:** Zwróć uwagę, że w przykładzie DATABASE\_USER i PASSWORD są takie same jak używane przez n8n - jeśli nie utworzysz osobnego użytkownika, upewnij się że istniejący ma prawa do nowej bazy. Bezpieczniej jest dodać dedykowanego użytkownika dla Baserow. \- REDIS\_HOST i REDIS\_PASSWORD - ustawiamy Baserow, by korzystał z naszego serwisu Redis (wewnątrz sieci backend host nazywa się redis). Podajemy to samo hasło, które skonfigurowaliśmy w Redisie. \- Montujemy wolumen baserow\_data - Baserow może zapisywać pewne pliki (np. załączniki dodane do bazy, eksporty) na dysk, stąd warto to przechować. Dodatkowo Baserow potrafi korzystać z tego do tzw. **świadczenia statycznych plików** (prawdopodobnie jego kontener Nginx - bo obraz Baserow zawiera wbudowany serwer - będzie używał tego katalogu). \- **ports:** wystawiamy port 80 kontenera Baserow na 8081 hosta, a 443 kontenera na 8444 hosta. To tylko przykładowa konfiguracja - jeśli planujesz podpiąć Baserow pod reverse proxy Nginx (tak jak n8n), to nie musisz wystawiać portów na hosta wcale, wystarczy że dodasz go do sieci proxy i skonfigurujesz Nginx dla jego domeny. W naszym przykładzie jednak pokazujemy porty, by można było testowo zajrzeć na Baserow np. przez http://twoja.domena.pl:8081.

Po dodaniu powyższego do Compose, odpal docker-compose up \-d. Baza Postgres już działa, Redis się uruchomi, a Baserow wystartuje i zainicjuje swój system. Inicjalizacja Baserow może chwilę potrwać (pierwsze uruchomienie, migracje bazy itp.). Gdy będzie gotowe, możesz przejść w przeglądarce na wskazany adres (np. http://twoja.domena.pl:8081) i zobaczysz interfejs rejestracji/logowania Baserow. Utwórz tam konto administratora i gotowe - masz własny klon Airtable\!

**Integracja n8n z Baserow:** Teraz Twoje n8n i Baserow siedzą obok siebie w sieci backend, co oznacza, że n8n może komunikować się z Baserow wewnętrznie. n8n udostępnia natywnie *nody* do Baserow (akcje na rzędach, bazach itp.). Aby z nich skorzystać, musisz [dodać poświadczenia Baserow w n8n](https://docs.n8n.io/integrations/baserow/) - zwykle jest to token API. W Baserow (panel administratora) wygeneruj klucz API, a następnie w n8n w sekcji **Credentials** dodaj nowe poświadczenie typu Baserow, podając URL instancji (np. http://baserow:80 jeśli korzystasz z wewnętrznej nazwy kontenera, lub publiczny URL jeśli wolisz) oraz token. Od tego momentu możesz np. tworzyć w n8n workflowy, które dodają rekordy do tabel Baserow, wyzwalają się gdy pojawi się nowy wiersz (Baserow ma też integracje webhook) itp.

Podsumowując, Baserow \+ n8n to świetne połączenie: Baserow daje Ci przyjazne **UI do danych**, a n8n automatyzuje wszystko wokół. Oba narzędzia są self-hosted i pod Twoją kontrolą, co bywa istotne, jeśli zależy Ci na prywatności i unikaniu ograniczeń narzucanych przez komercyjne SaaS.

### Qdrant - wektorowa baza danych dla integracji AI (embeddings)

Kolejnym ciekawym dodatkiem, szczególnie dla osób eksperymentujących z AI w swoich automatyzacjach, jest **Qdrant**. Qdrant to nowoczesna, wydajna baza danych wektorowych (vector database). Bazy wektorowe są używane w obszarach sztucznej inteligencji i uczenia maszynowego do przechowywania i wyszukiwania tzw. **embeddingów** - czyli reprezentacji danych (np. tekstu, obrazów) w postaci wektorów liczbowych w wysokowymiarowej przestrzeni. Brzmi to skomplikowanie, ale praktycznie rzecz biorąc, jeśli budujesz np. chatboty, systemy wyszukiwania semantycznego, rekomendacje czy cokolwiek związanego z **AI i rozumieniem języka** - to narzędzie takie jak Qdrant może być niezwykle przydatne do **szybkiego znajdowania podobnych elementów** (np. podobnych dokumentów do zadanego pytania itp.).

Jak to się ma do n8n? Otóż, n8n od wersji 1.5+ wprowadził integracje z kilkoma bazami wektorowymi, w tym Qdrant, Pinecone, Weaviate i inne. Istnieje oficjalny node **Qdrant Vector Store** w n8n, który pozwala dodawać wektory do bazy, wyszukiwać najbliższe sąsiady, tworzyć kolekcje itp. Dzięki temu możesz w swoich workflowach n8n wykorzystać Qdrant do zadań takich, jak: \- Przechowywanie wiedzy (dokumentów, artykułów, notatek) w postaci embeddingów i budowanie na tym np. inteligentnej wyszukiwarki lub chatbota (tzw. RAG - Retrieval Augmented Generation, czyli generacja odpowiedzi w oparciu o wyszukane informacje). \- Porównywanie elementów (np. znajdowanie produktów podobnych do danego produktu na podstawie ich cech wektorowych). \- Ogólnie, integracja AI: łącząc n8n \+ Qdrant \+ np. API OpenAI możesz zbudować własne rozwiązania AI bez potrzeby korzystania z zewnętrznych narzędzi indeksujących.

Aby w pełni to wykorzystać, możemy postawić instancję Qdrant obok n8n.

**Dodanie Qdrant do Docker Compose:**

```bash
services:  
  qdrant:  
    image: qdrant/qdrant:v1.3.5  
    restart: always  
    volumes:  
      - qdrant_storage:/qdrant/storage  
    ports:  
      - "6333:6333"  
    networks:  
      - backend
```

Tutaj jest dość prosto: \- **qdrant (serwis):** używamy obrazu Qdrant (wersja v1.3.5 w przykładzie - sprawdź najnowszą stabilną). Montujemy wolumen qdrant\_storage - Qdrant przechowuje wektory na dysku (zapewnia persystencję danych, bo wektory mogą zajmować sporo miejsca). Wystawiamy port 6333 na zewnątrz - to domyślny port API Qdrant (HTTP \+ gRPC). Możesz go wystawić jeśli chcesz też spoza Dockera mieć dostęp do Qdrant (np. do konsoli lub innego narzędzia). Jeśli planujesz używać Qdrant tylko z n8n wewnętrznie, nie musisz mapować portu, wystarczy, że n8n widzi go przez sieć backend. \- Qdrant nie wymaga osobnej bazy ani serwisu - to samodzielny serwer.

Po uruchomieniu Qdrant będzie dostępny. W n8n możesz teraz skonfigurować credentialsy do Qdrant (o ile potrzebne - domyślnie Qdrant chyba nie wymaga API key, choć obsługuje tokeny). Adres dla n8n do łączenia się z Qdrantem będzie http://qdrant:6333 (wewnątrz sieci Dockera).

W swoich workflowach możesz użyć nodu **Qdrant** - np. żeby utworzyć kolekcję wektorów, a następnie nodu **AI Embedding** (lub bezpośrednio API OpenAI) by zamienić tekst na embedding i zapisać w Qdrant, a potem nodu **Qdrant»Search (Query)** żeby znaleźć podobne wektory. Twórcy Qdrant opublikowali nawet poradnik, jak połączyć n8n z Qdrant, by robić zaawansowane rzeczy.

Krótko mówiąc, dodanie Qdrant do naszego ekosystemu **uzbraja n8n w zdolności semantycznego przetwarzania danych** - co otwiera drzwi do budowania własnych rozwiązań AI.

### Redis - kolejki i cache (skalowanie n8n)

Wspomnieliśmy już o Redisie przy okazji Baserow, ale Redis może pełnić także inną rolę: pomóc w **skalowaniu n8n**. Standardowo n8n wykonuje wszystkie zadania w jednym procesie (nawet jeśli mamy wiele workflowów, ich uruchamianie odbywa się sekwencyjnie lub współbieżnie w ramach jednego kontenera - lecz ograniczone zasobami pojedynczej maszyny). Gdy potrzebujemy obsłużyć większe obciążenie, n8n oferuje **tryb kolejki (Queue Mode)**. W tym trybie n8n dzieli się na **instancję główną** (main) oraz dowolną liczbę **workerów** (pracowników), a do komunikacji między nimi wykorzystuje właśnie **kolejkę opartą o Redis**.

Jak to działa?  
\- Uruchamiamy jedną instancję n8n w trybie głównym (Main). Ona odpowiada za UI (interfejs webowy), przyjmuje webhooki, harmonogramy, zarządza bazą danych itp., ale **nie wykonuje ciężkich zadań** bezpośrednio. Zamiast tego, każde zadanie (np. uruchomienie workflow) umieszcza w kolejce Redis. \- Osobno uruchamiamy jedną lub wiele instancji n8n jako **worker** (poprzez specjalny tryb uruchomienia). Takie instancje łączą się do tego samego Redisa i „wychwytują” zadania z kolejki, wykonując je w tle. Możemy odpalić wielu workerów (na jednym serwerze lub wielu), aby skalować poziomo liczbę jednoczesnych wykonywanych workflowów. \- Dzięki temu ciężar przetwarzania rozkłada się na wiele procesów, a nawet maszyn, co znacząco zwiększa wydajność i niezawodność (awaria jednego workera nie zatrzymuje systemu - main może przydzielić zadanie innemu).

Aby włączyć tryb kolejki, w konfiguracji n8n potrzebujemy: \- **Bazy danych współdzielonej** (już mamy Postgres, więc OK). \- **Redisa** (już mamy, w naszym compose jest serwis redis). \- Ustawienia środowiskowe w n8n: \- EXECUTIONS\_MODE=queue (domyślnie jest "own" czyli normalny tryb). \- QUEUE\_BULL\_REDIS\_HOST=\<adres Redisa\> (oraz ewentualnie port, hasło jeśli jest). W naszym przypadku QUEUE\_BULL\_REDIS\_HOST=redis i np. QUEUE\_BULL\_REDIS\_PORT=6379, QUEUE\_BULL\_REDIS\_PASSWORD=StrongRedisPass123. \- (opcjonalnie) EXECUTIONS\_PROCESS=either - n8n ma jeszcze tryb mieszany, ale nie wchodźmy w to teraz.

Konfiguracja Compose może wyglądać tak:

```bash
services:  
  n8n-main:  
    image: n8nio/n8n:latest  
    restart: always  
    environment:  
      - EXECUTIONS_MODE=queue  
      - QUEUE_BULL_REDIS_HOST=redis  
      - QUEUE_BULL_REDIS_PORT=6379  
      - QUEUE_BULL_REDIS_PASSWORD=StrongRedisPass123  
      - DB_TYPE=postgresdb ... (i reszta ustawień DB)  
      - N8N_BASIC_AUTH_USER=admin ... (reszta ustawień)  
    depends_on:  
      - postgres  
      - redis  
    networks:  
      - backend  
      - proxy  
    volumes:  
      - n8n\_data:/home/node/.n8n

  n8n-worker:  
    image: n8nio/n8n:latest  
    restart: always  
    environment:  
      - EXECUTIONS_MODE=queue  
      - QUEUE_BULL_REDIS_HOST=redis  
      - QUEUE_BULL_REDIS_PORT=6379  
      - QUEUE_BULL_REDIS_PASSWORD=StrongRedisPass123  
      - DB_TYPE=postgresdb #... (te same ustawienia bazy!)  
      - N8N_SKIP_WEBHOOK_DEREGISTRATION_SHUTDOWN=true  
    # ważne: w trybie worker trzeba dodać komendę:  
    command: n8n worker  
    depends_on:  
      - postgres  
      - redis  
    networks:  
      - backend  
    volumes:  
      - n8n\_data:/home/node/.n8n
```

Tutaj utworzyliśmy dwa serwisy: n8n-main i n8n-worker. Obydwa korzystają z tego samego obrazu n8n, ale: \- n8n-main to nasza główna instancja (z UI). Ona jest podłączona także do sieci proxy i to do niej Nginx będzie kierował ruch (np. w nginx.conf zamiast proxy\_pass http://n8n:5678 dalibyśmy proxy\_pass http://n8n-main:5678). Nie podajemy w niej żadnego specjalnego polecenia, więc domyślnie uruchomi się jako main. \- n8n-worker to instancja pracownika. Tutaj kluczowe jest command: n8n worker - ta komenda uruchamia proces w trybie worker (bez UI, tylko pobiera zadania). Nie dołączamy jej do sieci proxy (bo nie potrzebuje być widoczna z zewnątrz), tylko do backend. Podajemy te same zmienne EXECUTIONS\_MODE i ustawienia do Redisa oraz bazy (ważne, by worker miał dostęp do tej samej bazy i Redisa\!). Dodatkowo ustawiliśmy N8N\_SKIP\_WEBHOOK\_DEREGISTRATION\_SHUTDOWN=true - jest to zalecane w workerach, by uniknąć niepotrzebnych komunikatów przy zamykaniu (to drobny szczegół techniczny, wyjaśnienie wykracza poza ten poradnik).

Możemy uruchomić wiele takich workerów - np. n8n-worker-2, n8n-worker-3 - albo skorzystać z mechanizmu skalowania Compose: docker-compose up \-d \--scale n8n-worker=3 (to utworzy 3 kopie usługi worker). Im więcej workerów, tym więcej równoległych workflowów może być wykonywanych.

Pamiętajmy, że kolejni workerzy mogą obciążać maszynę - każdy to osobny proces Node.js. Dlatego skalowanie powinno iść w parze ze zwiększaniem zasobów (CPU/RAM) i ewentualnie rozdzieleniem na różne hosty (wtedy jednak Docker Compose lokalny nie wystarczy - trzeba by użyć np. Docker Swarm, Kubernetes lub innego orchestratora).

**Czy każdy potrzebuje trybu kolejki?** Nie, to jest dopiero przy dużej skali lub specyficznych potrzebach. Prosta instancja n8n radzi sobie znakomicie z wieloma workflowami sekwencyjnie. Jednak warto wiedzieć, że taka opcja istnieje, bo daje to pewien **future-proofing** - jeśli Twój projekt się rozrośnie, nie osiągniesz sufitu możliwości n8n, zawsze możesz dołożyć workerów.

Na koniec ciekawostka: **n8n w trybie queue mode** architektonicznie przypomina działanie innych systemów jak Kubernetes czy chmurowe kolejki - mamy centralny koordynator (main) i wielu wykonawców zadań, a Redis działa jak **broker wiadomości** między nimi. 

Dzięki temu mechanizmowi, dodając Redis i kilka flag, Twój n8n może urosnąć z pojedynczego kontenera do **klastra kontenerów** obsługujących automatyzacje na skalę dużo większą, zapewniając lepszą wydajność i niezawodność.

## Wskazówki i najlepsze praktyki dla n8n w Dockerze

Na zakończenie zebraliśmy jeszcze kilka porad, które warto mieć na uwadze przy utrzymaniu n8n w środowisku Docker:

* **Regularne backupy:** Pamiętaj, aby robić kopie zapasowe kluczowych danych. W przypadku n8n są to:

* Jeśli używasz SQLite: plik bazy danych (znajdujący się w wolumenie \~/.n8n jako database.sqlite lub podobnie) oraz plik z kluczem szyfrującym (standardowo .n8n/credentials\_backup lub config - zawierający klucz do odszyfrowania credentiali).

* Jeśli używasz Postgresa: regularnie wykonuj backup bazy (np. pg\_dump). Możesz zautomatyzować to też w Dockerze, używając np. kontenera postgres do dumpów lub narzędzi takich jak pg\_dumpall. Backup bazy jest ważny, by nie utracić swoich workflowów i historii.

* Plik \~/.n8n zawiera także klucz szyfrujący (ENV N8N\_ENCRYPTION\_KEY). **Bez tego klucza nie odszyfrujesz poświadczeń (credentials) w razie odtworzenia instancji\!** Dlatego bezpiecznie przechowuj kopię tego klucza. Najlepiej jest **ustawić własny klucz szyfrujący** przez zmienną środowiskową N8N\_ENCRYPTION\_KEY już od początku - wtedy masz pewność co do jego wartości (możesz wygenerować losowy długi ciąg i ustawić). Jeśli tego nie zrobisz, n8n wygeneruje klucz za Ciebie przy pierwszym starcie i zapisze w pliku - wtedy musisz pamiętać, by ten plik zachować.

* **Aktualizacje n8n:** Projekt n8n rozwija się bardzo dynamicznie, regularnie pojawiają się nowe wersje z poprawkami i funkcjami. Aby zaktualizować instancję n8n w Dockerze, wykonaj:

* Backup danych (na wszelki wypadek).

* W pliku docker-compose.yml zmień tag obrazu na nowszy (np. n8nio/n8n:latest zawsze pobiera najnowsze stabilne, ale możesz też wskazać konkretną wersję, np. n8nio/n8n:1.30.0).

* Wykonaj docker-compose pull (pobranie nowego obrazu) oraz docker-compose up \-d. Kontener powinien podnieść się w nowej wersji. W logach sprawdź, czy migracje bazy danych przeszły pomyślnie (n8n automatycznie migruje schemat bazy jeśli to potrzebne).

* Przetestuj, czy wszystko działa (zwłaszcza kluczowe workflowy). Jeśli coś poszło nie tak, masz backup by ewentualnie wrócić.

* **Monitorowanie i logi:** Warto monitorować zużycie zasobów przez kontener n8n. Możesz użyć docker stats aby podejrzeć zużycie CPU/RAM. W razie wycieków pamięci czy obciążających procesów, rozważ skalowanie lub optymalizację workflowów. Logi n8n możesz odczytać przez docker-compose logs \-f n8n (lub n8n-main, n8n-worker zależnie od nazwy usługi). Jeśli zauważysz częste błędy, warto je przeanalizować - czasem mogą to być np. problemy z połączeniami do API (błędy sieci), których obsługę możesz poprawić w swoich workflowach.

* **Bezpieczeństwo:**

* **Dostęp do instancji:** Upewnij się, że n8n zawsze jest zabezpieczony hasłem. Jeśli masz włączony mechanizm użytkowników, nie zostawiaj instancji bez utworzenia konta admina. Jeśli nie chcesz korzystać z multi-user, to co najmniej Basic Auth powinien być włączony. **Nigdy nie wystawiaj n8n niezabezpieczonego do Internetu** - ktoś mógłby przejąć Twoje automatyzacje, klucze API do zewnętrznych serwisów itp.

* **CORS i webhooki:** Jeśli używasz webhooków w n8n, zastanów się nad ograniczeniem CORS (Cross-Origin Resource Sharing) lub weryfikacją źródeł. Domyślnie webhook w n8n jest otwarty dla żądań z dowolnego źródła. Możesz jednak w ustawieniach zaawansowanych n8n (zmienne N8N\_BLOCK\_ENV\_ACCESS\_IN\_NODE, N8N\_BLOCK\_BROWSER\_ACCESS\_TO\_EXECUTIONS) ograniczyć pewne ryzykowne funkcje. W najnowszych wersjach n8n możesz też ustawić listę dozwolonych domen dla CORS, co jest przydatne, jeśli np. wywołujesz webhooki z frontendu przeglądarkowego.

* **Aktualizuj na bieżąco** obrazy kontenerów (nie tylko n8n, ale i np. Postgresa, Nginx) aby mieć najnowsze poprawki bezpieczeństwa.

* **Portainer / GUI do Dockera:** Jeżeli zarządzanie Dockerem przez terminal Cię męczy, możesz rozważyć dodanie narzędzia takiego jak **Portainer** - to webowe GUI do zarządzania kontenerami. Można je również uruchomić w Dockerze. Dzięki Portainerowi łatwo sprawdzisz logi, statystyki i stan swoich usług, a nawet zaktualizujesz obrazy przez kliknięcie. W kontekście n8n nie jest to konieczne, ale bywa wygodne dla mniej doświadczonych użytkowników.

* **Przywracanie danych / migracja:** Gdybyś chciał przenieść instancję n8n na inny serwer (np. zmieniasz VPS), Docker ułatwia to zadanie. Wystarczy przenieść pliki (docker-compose.yml, ewentualnie .env, oraz katalogi/wolumeny z danymi). Jeśli używasz named volumes, możesz je zbackupować poleceniem docker run \--rm \-v nazwavolumenu:/data \-v $(pwd):/backup alpine tar czf /backup/n8n\_data.tar.gz /data (i podobnie dla innych wolumenów). Albo prościej - jeśli to maszyna Linux - zajrzyj gdzie Docker przechowuje wolumeny (np. /var/lib/docker/volumes/) i spakuj stamtąd dane. Po przeniesieniu odtwórz wolumeny i uruchom compose - n8n powinien wystartować tak jak wcześniej. Jeśli korzystasz z Postgresa, możesz także zrobić dump bazy na starym serwerze i odtworzyć na nowym. Kluczowe jest, by **zachować ten sam klucz szyfrujący** i bazę, wtedy wszystkie istniejące workflowy i credentials będą działać na nowej instancji identycznie.

<AD:n8n-kurs-waitlist>

## Podsumowanie

W tym obszernym przewodniku pokazaliśmy, jak krok po kroku uruchomić **n8n w środowisku Docker**, zaczynając od prostej konfiguracji, aż po zaawansowane, produkcyjne wdrożenie z kilkoma współpracującymi usługami. Docker okazał się niezwykle pomocny - pozwolił z łatwością dołączać kolejne elementy układanki: bazę PostgreSQL dla niezawodności, serwer proxy Nginx dla publicznego dostępu po HTTPS, Baserow jako dodatkową bazę no-code, Redis i tryb queue dla skalowania oraz Qdrant dla zastosowań AI.

Oczywiście, nie każde wdrożenie wymaga wszystkich tych komponentów - dopasuj swoją infrastrukturę do potrzeb. Może na start wystarczy Ci sam n8n z SQLite, a z czasem dodasz Postgresa. Może nie potrzebujesz Baserow ani Qdrant, jeśli Twoje automatyzacje są prostsze. Ważne, że masz świadomość możliwości i dróg rozwoju.

**n8n** to narzędzie, które rośnie razem z Twoimi pomysłami - a Docker sprawia, że nadążanie za tym wzrostem jest znacznie łatwiejsze. Trzymając się dobrych praktyk (jak backupy, aktualizacje i zabezpieczenia) możesz cieszyć się solidną platformą automatyzacji, która odciąży Cię od codziennej rutyny i zautomatyzuje wiele zadań.

Na koniec zachęcamy: eksperymentuj z własnymi workflowami, łącz usługi, wyzwalaj kreatywność. Automatyzacja potrafi naprawdę usprawnić pracę i zaoszczędzić mnóstwo czasu - **Twój n8n jest już gotowy, by Ci w tym pomóc\!**

Jeśli chcesz jeszcze lepiej poznać Dockera i konteneryzację (co na pewno przyda się przy dalszym rozwijaniu swojego projektu z n8n), zajrzyj do naszego [kursu Docker](https://dokodu.it/kursy/docker). A w naszym serwisie znajdziesz też inne artykuły i przewodniki dotyczące automatyzacji, integracji oraz narzędzi no-code/low-code. Powodzenia w automatyzowaniu\!
