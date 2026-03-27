---
type: kurs-materialy
modul: 01
format: skrypt-nagrania
segmentów: 12
szacowany-czas: 3h
created: 2026-03-27
---

# Tydzień 1: Skrypt do Nagrania

> **Legenda:**
> `[SLAJD N]` — zmień slajd
> `[DEMO: opis]` — przełącz na ekran n8n
> `[PAUZA]` — chwila ciszy, uczestnik może przetworzyć
> `[PYTANIE: ...]` — pytanie retoryczne do uczestnika
> `*kursywa*` — akcent głosowy (wolniej, wyraźniej)

---

## Segment 01 — Witaj w n8n (12 min)

[SLAJD 1]

Cześć. Cieszę się że tu jesteś.

Przez następne 3 godziny zbudujesz swój pierwszy system automatyzacji w n8n — taki który naprawdę robi coś przydatnego. Nie "Hello World", nie kliknij przycisk i zobaczysz liczbę. *Prawdziwy* system — Lead Capture, który zbiera leady z formularza, waliduje dane, zapisuje do Google Sheets, wysyła email powitalny i ping na Slacka dla zespołu.

[SLAJD 2]

Ale zanim zacznę — pokaż ci co zbudujesz.

[DEMO: pokaż gotowy Lead Capture System w n8n — uruchom raz z przykładowym payloadem, pokaż że email przyszedł i wpis jest w Sheets]

Widzisz? To nie jest skomplikowane. Za 3 godziny będziesz wiedzieć dokładnie jak to działa — każda strzałka, każdy node, każda decyzja. I będziesz w stanie zmodyfikować to pod konkretny przypadek klienta.

[SLAJD 3]

Zanim wejdziemy w szczegóły — kilka słów o tym czym n8n *jest* i czym *nie jest*.

n8n nie jest kolejnym Zapierem. To nie narzędzie do klikania gotowych integracji. n8n to *silnik automatyzacji* — masz pełną kontrolę nad logiką, możesz pisać JavaScript, wywoływać dowolne API, budować złożone drzewa decyzyjne. Firmy jak Siemens, eBay, McLaren używają n8n w produkcji.

Co ważniejsze dla agencji: n8n jest self-hosted. Twoje dane siedzą na twoim serwerze. Żaden dostawca chmury nie ma do nich dostępu. Dla klientów z branży prawnej, medycznej, finansowej — to często wymóg, nie opcja.

[SLAJD 4]

Self-hosted czy cloud?

[PYTANIE: Jaką masz infrastrukturę?]

Jeśli masz Docker — polecam self-hosted. VPS za 5-10 dolarów miesięcznie wystarczy na 3-4 aktywne workflow dla klienta. Jeśli dopiero zaczynasz i chcesz po prostu sprawdzić o co chodzi — n8n Cloud ma 14 dni próbnych za darmo. Zacznij tam, a jak zasmakujesz — przejdź na własny serwer.

W tym kursie pokażę Docker, bo to standard który skalujesz do produkcji. Ale każda technika którą zobaczysz działa identycznie w Cloud.

---

## Segment 02 — Instalacja i Środowisko (15 min)

Dobra — zaczynamy.

[DEMO: pokaż terminal]

Zakładam że masz Dockera. Jeśli nie — w materiałach kursu jest instrukcja instalacji Dockera na Windows, Mac i Linux. Zajmuje 10 minut.

Stwórzmy katalog dla n8n:

```bash
mkdir n8n-kurs && cd n8n-kurs
```

Teraz plik `docker-compose.yml`. Ten plik jest do pobrania w materiałach — nie musisz go przepisywać.

[SLAJD 5]

[DEMO: pokaż docker-compose.yml w edytorze]

Kilka rzeczy na które zwróć uwagę. Po pierwsze — `N8N_ENCRYPTION_KEY`. To klucz który szyfruje twoje credentiale. *Zapisz go gdzieś bezpiecznego* — w manageru haseł, w sejfie, gdziekolwiek. Jeśli go stracisz i przenosisz n8n na inny serwer — wszystkie credentiale stają się nieczytalne. Musisz je dodać od nowa.

Po drugie — `volumes`. To tutaj n8n zapisuje swoje dane między restartami. Bez tego każdy `docker compose down` kasuje wszystko.

[DEMO: uruchom `docker compose up -d`, poczekaj 20 sekund, otwórz localhost:5678]

I voilà. n8n działa.

Pierwsze logowanie — podajesz email, hasło, nazwa właściciela. Gotowe.

[DEMO: szybki tour po interfejsie n8n — menu boczne, New Workflow, Executions]

Po lewej menu: Workflows, Credentials, Executions, Settings. Na środku canvas — tu budujesz. Na górze przyciski: Test, Save, Activate. Executions panel na dole — historia każdego uruchomienia.

To jest twoje centrum dowodzenia przez następne tygodnie kursu.

---

## Segment 03 — Anatomia Workflowu (15 min)

[SLAJD 6]

Widzisz ten canvas? Biała przestrzeń gdzie przeciągasz klocki. Właśnie tutaj dzieje się magia — i właśnie tutaj można się zgubić jeśli nie rozumiesz podstawowej struktury.

Stwórzmy najprostszy możliwy workflow żebyś zobaczył jak to działa.

[DEMO: stwórz nowy workflow, dodaj Manual Trigger]

Klikam Plus w centrum canvasu, wybieram "Manual Trigger". To trigger który startuje gdy klikasz przycisk — idealny do nauki i testowania.

[SLAJD 7]

Widzisz ten node? Anatomia jest zawsze ta sama.

Wejście — z lewej. Wychodzą tutaj dane z poprzedniego kroku. Wyjście — z prawej. Stąd dane idą dalej. Po kliknięciu — panel boczny z ustawieniami.

[DEMO: kliknij Manual Trigger, pokaż zakładki Parameters, Settings, Notes]

Zakładka Parameters — ustawienia specyficzne dla tego node'a. Settings — opcje globalne: Continue on Fail, Retry. Notes — dokumentacja dla siebie i kolegi który przejmie workflow za 6 miesięcy.

[SLAJD 8]

Teraz najważniejszy koncept w całym n8n: *item*.

Item to jeden rekord danych. Jeśli formularz wysyła dane o jednym leadsie — to jest jeden item. Jeśli Google Sheets zwraca 100 wierszy — to jest 100 itemów.

Każdy node przetwarza każdy item osobno. To jest model który wiele rzeczy wyjaśnia — i jest też źródłem wielu nieporozumień na początku.

[DEMO: dodaj Set node, wpisz kilka pól manualnie, uruchom workflow, pokaż output z itemami]

Widzisz? Jeden item wszedł, jeden wyszedł — z nowymi polami które dodałem. W Set node mogę modyfikować dane, dodawać pola, usuwać pola.

[DEMO: dodaj NoOp node jako ostatni, pokaż że nic nie robi ale dane przepływają]

NoOp — "No Operation". Nic nie robi, ale jest przydatny jako placeholder albo gdy chcesz podejrzeć co dociera do danego miejsca w workflowu.

Mamy trzy node'y, dwa połączenia. To jest kompletny workflow. Nie robi nic użytecznego — ale pokazuje strukturę.

---

## Segment 04 — Triggery: Kiedy Workflow Startuje (15 min)

[SLAJD 9]

Teraz omówimy triggery — bo każdy workflow musi wiedzieć *kiedy* ma wystartować.

Trigger to zawsze pierwszy node w workflowu. Jest dokładnie jeden. Trzy główne typy.

[SLAJD 10]

**Manual Trigger** — klikasz przycisk. Tylko do testowania. Nigdy nie zostawiaj go jako jedynego triggera w produkcji — bo workflow startuje tylko gdy ty ręcznie klikniesz.

**Schedule Trigger** — cyklicznie. Raporty nocne, synchronizacje, przypomnienia. Ustawiasz cron expression albo wybierasz z gotowych presetów.

**Webhook Trigger** — reaguje na zdarzenie zewnętrzne. Formularz wysyła dane → workflow startuje. Stripe płatność przychodzi → workflow startuje. Slack komenda → workflow startuje. *To jest najważniejszy trigger dla agencji.*

[SLAJD 11]

Pokażę ci Webhook w akcji.

[DEMO: stwórz nowy workflow, dodaj Webhook Trigger]

Klikam Test URL — kopiuję adres. Mam go w schowku.

Teraz klikam "Listen for event" w n8n — workflow nasłuchuje.

[DEMO: otwórz terminal, wyślij curl]

```bash
curl -X POST http://localhost:5678/webhook-test/moj-test \
  -H "Content-Type: application/json" \
  -d '{"email":"jan@firma.pl","name":"Jan Kowalski","message":"Chce automatyzacje"}'
```

[PAUZA — czekaj na odpowiedź w n8n]

Widzisz? Dane pojawiły się w n8n. Email, imię, wiadomość — dokładnie to co wysłałem w body requestu.

Ważna rzecz o webhooku. Mamy Test URL i Production URL. Test URL działa tylko gdy klikasz "Listen for event" — idealne do developmentu. Production URL działa gdy workflow jest *Activated* — zielony przełącznik w prawym górnym rogu. W produkcji zawsze Activated + Production URL.

Klasyczny błąd: developer testuje na Production URL bo skopiował nie ten link. Albo odwrotnie — aktywuje workflow ale formularz klienta ma wpisany Test URL. Efekt: zero danych, klient się denerwuje. Unikaj.

---

## Segment 05 — Kluczowe Nodes (20 min)

[SLAJD 12]

6 nodes. Tyle potrzebujesz żeby zacząć. Naprawdę.

[SLAJD 13]

**HTTP Request** — to twój dostęp do całego internetu. Każde API, każdy serwis który ma endpoint HTTP, możesz wywołać z tego node'a.

[DEMO: dodaj HTTP Request node, ustaw GET, URL: https://jsonplaceholder.typicode.com/users/1]

Prosty przykład: pobieram dane użytkownika z testowego API. Klikam Test Step.

Wróciła odpowiedź — imię, email, adres, firma. Te dane możesz teraz użyć w następnym node'zie.

[DEMO: pokaż Expression `{{ $json.email }}`]

Wyrażenia w n8n — podwójne nawiasy klamrowe. Wewnątrz masz dostęp do `$json` — to dane z poprzedniego node'a. `$json.email` — pole email. `$json.company.name` — zagnieżdżone pole.

[SLAJD 14]

To jest Expression — sposób na dynamiczne wartości. Zamiast wpisywać statyczne wartości, pobierasz dane z przepływu.

`$json.email` — pole z poprzedniego node'a.
`$now.toISO()` — aktualny czas.
`$env.SHEETS_ID` — zmienna środowiskowa.

Naucz się wyrażeń — to game changer.

[SLAJD 15]

**IF node** — rozgałęzienie logiczne.

[DEMO: dodaj IF node, warunek: $json.email contains "@"]

Prawa strona node'a — dwa wyjścia: true i false. Jeśli email zawiera "@" — idzie prawą ścieżką. Jeśli nie — lewą.

Zawsze podłącz obie ścieżki. Gałąź false to często "co robimy z błędem". Zostawienie jej pustej w produkcji to jak zostawienie otwartego zaworu z gazem — może długo nie wybuchnąć, ale wybuchnie.

[SLAJD 16]

**Switch node** — gdy masz więcej niż dwie ścieżki.

Wyobraź sobie że masz pole `typ_leadu` — może być "lead", "klient", "partner". IF w IF w IF — brzydkie i trudne w utrzymaniu. Switch node robi to elegancko: trzy wyjścia, każde z regułą.

[SLAJD 17]

**Code node** — JavaScript inline.

[DEMO: dodaj Code node, pokaż walidację emaila regexem]

```javascript
const email = $input.first().json.email;
const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const isValid = regex.test(email);

return [{ json: { ...email, isValid } }];
```

Code node jest potężny ale używaj go ostrożnie. Każda linia kodu to potencjalny bug i coś czego klient nie może edytować w wizualnym interfejsie. Zawsze najpierw sprawdź czy nie da się tego zrobić zwykłym node'em.

---

## Segment 06 — Credential Vault (15 min)

[SLAJD 18]

Teraz coś co wielu ludzi ignoruje na początku i potem tego żałuje — zarządzanie kluczami API.

Klucze API są jak hasła do bankowych kont twoich klientów. Wyciek klucza API do OpenAI to kilka tysięcy złotych faktury. Wyciek klucza do Stripe — możliwe straty finansowe. To nie jest paranoja — to realny scenariusz.

n8n ma wbudowany sejf — Credential Vault. Wszystkie klucze przechowuje zaszyfrowane algorytmem AES-256. Nawet jeśli ktoś ukradnie backup bazy danych — bez `N8N_ENCRYPTION_KEY` to jest bełkot.

[SLAJD 19]

Typy credentiali. Każde API używa innego mechanizmu autoryzacji.

**API Key** — klucz który dodajesz w ustawieniach konta. OpenAI, SendGrid, Airtable — to zazwyczaj ten typ.

**Header Auth** — klucz idzie w nagłówku HTTP. Różni się od API Key tym że samodzielnie definiujesz nazwę nagłówka.

**Basic Auth** — stary standard. Nazwa użytkownika + hasło. Zobaczycie to głównie w starszych API i wewnętrznych systemach firm.

**OAuth2** — standardowy protokół autoryzacji. Google, Slack, GitHub — wszystko to co "Zaloguj się przez...". n8n robi to automatycznie — klikasz przycisk, przeglądarka otwiera stronę logowania, token wraca do n8n.

[SLAJD 20]

[DEMO: dodaj credential typu "Header Auth"]

Klikam Credentials w menu bocznym → New credential → Header Auth. Podaję nazwę nagłówka — na przykład "X-API-Key", podaję wartość. Klikam Save.

[DEMO: podłącz credential do HTTP Request node'a]

Teraz w HTTP Request node, pole Authentication — wybieram "Header Auth", wybieram mój credential. Gotowe. Klucz nigdy nie pojawi się w logach ani w wyeksportowanym JSONie workflowu.

[SLAJD 19 — wróć]

Zasada której musisz się trzymać: *nigdy nie wklejaj klucza API bezpośrednio jako wyrażenia w polu*. `{{ "sk-abc123..." }}` — to jest antywzorzec. Klucz będzie widoczny w historii executions.

---

## Segment 07 — Error Handling (20 min)

[SLAJD 21]

Czas na temat który odróżnia amatorów od profesjonalistów. Error handling.

Domyślnie w n8n: jeden błąd = workflow zatrzymuje się. Node failuje, execution jest oznaczone czerwonym, koniec. Żadnych powiadomień, żadnych informacji. Workflow pada w ciszy.

[PYTANIE: Czy to problem?]

Tak, to bardzo duży problem. Klient nie dostaje leada. Nikt nie wie że formularz przestał działać. Przez tydzień przychodzą leady na które nikt nie odpowiada. To jest scenariusz który niszczy zaufanie.

Dlatego mamy trzy strategie obsługi błędów.

[DEMO: budujesz workflow z HTTP Request który celowo failuje — zły URL]

Uruchamiam workflow. Widzisz? Czerwony node, error message, workflow zatrzymany.

[SLAJD 22]

**Strategia 1: Continue on Fail.**

[DEMO: włącz Continue on Fail w Settings node'a]

Teraz workflow idzie dalej mimo błędu. W danych pojawia się pole `error` z opisem co się stało. Możesz IF nodeem sprawdzić czy `error` istnieje i odpowiednio zareagować.

Kiedy używać: gdy błąd jednego kroku nie blokuje reszty. Na przykład: jeden z 10 emailów jest nieprawidłowy — nie chcesz żeby to zablokowało pozostałe 9.

Kiedy NIE używać: gdy błąd jest krytyczny. Nie zapisałeś leada do Sheets? Nie puszczaj dalej emaila powitalnego — bo nie masz danych do czego send.

**Strategia 2: Error Trigger Workflow.**

[SLAJD 23]

To jest gold standard.

[DEMO: stwórz nowy workflow "Error Handler"]

Nowy workflow, pusty. Jako trigger wybieram "Error Trigger". To specjalny trigger który startuje gdy inny workflow pada.

[DEMO: dodaj Gmail node — email do admina z danymi o błędzie]

```
To: {{ $env.ADMIN_EMAIL }}
Subject: ❌ Błąd workflow: {{ $json.workflow.name }}
Body:
Workflow: {{ $json.workflow.name }}
Node: {{ $json.node.name }}
Błąd: {{ $json.error.message }}
Execution: {{ $json.execution.url }}
```

[DEMO: wróć do głównego workflow, Settings, Error Workflow — wybierz "Error Handler"]

Teraz gdy główny workflow padnie — automatycznie startuje Error Handler. Admin dostaje email z dokładnym opisem problemu.

[PAUZA]

Jedna ważna rzecz: Error Trigger Workflow działa tylko dla aktywowanych workflowów. W trybie testowym — nie triggeruje. Pamiętaj o tym przy testowaniu.

---

## Segment 08 — Debugowanie (15 min)

[SLAJD 24]

Debugowanie. Każdy workflow w końcu nie działa tak jak powinien. Pytanie to nie "czy będziesz debugować" — ale "jak szybko znajdziesz problem".

Moja metoda: pięć kroków, zazwyczaj wystarczają dwa pierwsze.

**Krok 1:** Kliknij czerwony node. Otwiera się panel błędu z dokładną wiadomością. Przeczytaj ją. Serio — przeczytaj całą, nie tylko pierwsze słowo.

**Krok 2:** Sprawdź Input czerwonego node'a. Czy dane w ogóle tam dotarły? Czy mają właściwy format?

[DEMO: pokaż Execution Log — kliknij czerwony execution, nawiguj przez nodes]

Execution Log to historia jednego uruchomienia. Klikasz node — widzisz co weszło i co wyszło (albo co poszło nie tak).

[SLAJD 25]

**Pin Data** — to jest absolutny game changer.

[DEMO: pin data na Webhook Trigger, pokaż jak testować downstream nodes]

Uruchamiam workflow raz — dane pojawiają się w Webhook Trigger. Klikam Output, klikam "Pin". Teraz te dane są zamrożone na tym node'zie.

Teraz mogę "Test Step" na każdym kolejnym node'zie bez wysyłania nowego requestu. Edytuję jeden node, klikam Test Step, widzę wynik. Szybkie iterowanie.

[SLAJD 24 — wróć]

Top 3 przyczyny błędów z mojego doświadczenia.

Po pierwsze: literówka w nazwie pola. `email` vs `Email` vs `e-mail`. n8n jest case-sensitive. Sprawdź dokładnie nazwę w Output poprzedniego node'a.

Po drugie: typ danych. Zamiast liczby przyszedł string `"5"`. Porównanie `"5" > 3` w JavaScript... może dać nieoczekiwany wynik.

Po trzecie: brakujące pole. Coś jest `undefined` bo poprzedni node nie zwrócił tego pola w tym konkretnym przypadku. Dodaj domyślną wartość.

---

## Segment 09 — Architektura Projektu (10 min)

[SLAJD 26]

Okej — teoria za nami. Czas zbudować coś prawdziwego.

Lead Capture System. Pokażę ci diagram i wyjaśnię każdą decyzję projektową.

[SLAJD 26 — diagram]

Formularz na landing page wysyła POST request na webhook. Pierwszy krok to walidacja — czy email ma właściwy format, czy wymagane pola są obecne. Jeśli walidacja failuje — odsyłamy 400 z opisem błędu.

Jeśli walidacja OK — sprawdzamy deduplikację. Czy ten email już jest w Sheets? Jeśli jest — odsyłamy 200 "już zarejestrowany" ale nie robimy nic więcej. Unikamy duplikatów w bazie.

Jeśli nowy lead — zapisujemy do Google Sheets, wysyłamy email powitalny przez Gmail, pingujemy Slack. Na końcu — 200 OK z powrotem do formularza.

[SLAJD 27]

Walidacja.

Dlaczego walidujemy? Formularz może wysłać cokolwiek. Boty wysyłają losowe znaki. Użytkownicy robią literówki. Lepiej odrzucić brudne dane na wejściu niż potem czyścić Sheets.

Walidacja emaila — regex. Nie musimy pisać własnego — jest standardowy wzorzec który sprawdza czy jest znak "@" i domena.

Honeypot — ukryte pole w formularzu które prawdziwy użytkownik nigdy nie wypełni. Boty wypełniają wszystko. Jeśli honeypot jest wypełniony → spam, ignoruj.

[SLAJD 28]

Deduplikacja.

[PYTANIE: Dlaczego?]

Bo formularze można wysłać dwa razy. Użytkownik kliknie submit, strona się wolno ładuje, kliknie jeszcze raz. Albo odświeży stronę. Albo cokolwiek.

Sprawdzamy email w Google Sheets. Jeśli istnieje — nie zapisujemy, odsyłamy uprzejmą informację. To chroni jakość danych.

Potrzebne: ID arkusza, zakres kolumn gdzie trzymasz emaile. Zobaczycie konfigurację zaraz.

---

## Segment 10 — Budujemy: Część 1 (18 min)

Dobra — ręce na klawiaturze. Budujemy.

[DEMO: utwórz nowy workflow "Lead Capture System"]

Nowy workflow. Zapisuję jako "Lead Capture System".

Pierwszy node — Webhook Trigger.

[DEMO: dodaj Webhook Trigger, pokaż URL]

Kopiuję Test URL. Przełączam na "Listen for event".

[DEMO: wyślij testowy payload przez curl]

```bash
curl -X POST [TEST_URL] \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jan@firma.pl",
    "name": "Jan Kowalski",
    "message": "Chce automatyzacje procesow",
    "source": "landing-page"
  }'
```

Dane przyszły. Widzę je w Output Webhook Trigger. Teraz wiemy z czym pracujemy.

[DEMO: dodaj IF node — walidacja emaila]

IF node. Warunek: `$json.email` — String — Matches Regex — `^[^\s@]+@[^\s@]+\.[^\s@]+$`

Gałąź true = email poprawny, idź dalej.
Gałąź false = zwróć błąd.

[DEMO: dodaj Respond to Webhook node na gałęzi false]

Na gałęzi false dodaję "Respond to Webhook" node. Response Code: 400. Body JSON:
```json
{ "success": false, "error": "Nieprawidłowy format emaila" }
```

[DEMO: dodaj drugi IF — czy name jest obecny]

Drugi IF: `$json.name` — nie jest pusty. False gałąź — znów Respond 400 z innym błędem.

[DEMO: test z błędnymi danymi, pokaż że wraca 400]

```bash
curl -X POST [TEST_URL] \
  -H "Content-Type: application/json" \
  -d '{"email": "niejestem-emailem", "name": "Jan"}'
```

Wraca 400. Walidacja działa.

Teraz deduplikacja. Sprawdzamy Google Sheets czy email już jest.

[DEMO: dodaj HTTP Request node do sprawdzenia Sheets]

HTTP Request — GET do Sheets API.
URL: `https://sheets.googleapis.com/v4/spreadsheets/{{ $env.SHEETS_ID }}/values/A:A`
Authentication: Google Sheets OAuth2.

Jeśli ten email jest w zwróconej tablicy — duplikat. IF node sprawdza czy `$json.values` zawiera nasz email.

---

## Segment 11 — Budujemy: Część 2 (17 min)

Mamy walidację i deduplikację. Teraz główna część — zapis i powiadomienia.

[DEMO: dodaj Google Sheets node — Append Row]

Google Sheets node. Operacja: "Append or Update Row". Spreadsheet ID z env var. Sheet: Leads. Kolumny:
- email: `{{ $json.email }}`
- name: `{{ $json.name }}`
- message: `{{ $json.message }}`
- source: `{{ $json.source }}`
- timestamp: `{{ $now.toISO() }}`

[DEMO: test — pokaż że wiersz pojawił się w Sheets]

Wiersz pojawił się w Sheets. Data dodana.

[DEMO: dodaj Gmail node]

Gmail node — Send Email.
To: `{{ $json.email }}`
Subject: `Cześć {{ $json.name.split(' ')[0] }}, witamy w Dokodu! 🎉`

Body HTML:
```html
Cześć {{ $json.name.split(' ')[0] }},

Dziękujemy za kontakt z Dokodu!

Otrzymaliśmy Twoją wiadomość i odezwiemy się w ciągu 24 godzin roboczych.

Jeśli chcesz zobaczyć jak wygląda nasza praca — sprawdź case studies na dokodu.it

Do zobaczenia!
Kacper i Zespół Dokodu
```

Credential: Gmail OAuth2.

[SLAJD 30]

[DEMO: test Gmail — pokaż że email przyszedł na skrzynkę]

Email przyszedł. Personalizacja z imieniem działa.

[DEMO: dodaj Slack node]

Slack node — Post Message.
Channel: `#leady`
Message:
```
🎯 Nowy lead!
*Imię:* {{ $json.name }}
*Email:* {{ $json.email }}
*Źródło:* {{ $json.source || 'formularz' }}
*Czas:* {{ $now.toLocaleString('pl-PL') }}
```

[DEMO: test Slack — pokaż powiadomienie]

Mamy pełny flow. Webhook → Walidacja → Deduplikacja → Sheets → Gmail → Slack.

Teraz ostatni krok — Respond to Webhook z sukcesem.

[DEMO: dodaj Respond to Webhook na końcu — 200 OK]

```json
{ "success": true, "message": "Dziękujemy za zgłoszenie!" }
```

[DEMO: przetestuj cały flow od początku]

Wysyłam nowy, unikalny lead. Lecę krok po kroku... Sheets — wpis. Gmail — email. Slack — powiadomienie. Response — 200 OK.

Działa!

---

## Segment 12 — Error Handling + Podsumowanie (8 min)

Ostatni krok — Error Handling.

[DEMO: stwórz Error Handler workflow, podłącz do głównego]

Tak jak pokazywałem wcześniej — Error Trigger workflow, Gmail do admina z informacją o błędzie.

[DEMO: w głównym workflow — Settings, Error Workflow]

Gotowe. Lead Capture System jest kompletny i odporny na błędy.

[DEMO: pokaż cały canvas z góry — wszystkie nodes widoczne]

Popatrz na to. Webhook. Walidacja emaila. Walidacja wymaganych pól. Odpowiedź błędu dla formularza. Sprawdzenie duplikatu. Zapis do Sheets. Email powitalny. Slack. Odpowiedź sukcesu. I w tle Error Handler.

To jest profesjonalny, produkcyjny system. Możesz go wdrożyć u klienta.

[SLAJD 38]

Co umiasz po tym tygodniu?

Instalować i konfigurować n8n. Orientować się w interfejsie. Tworzyć workflow z triggerami, nodami, połączeniami. Bezpiecznie przechowywać klucze API. Walidować dane wejściowe. Obsługiwać błędy. Debugować gdy coś idzie nie tak.

I przede wszystkim — zbudowałeś coś użytecznego.

[SLAJD 36]

Zadanie domowe. Rozszerz Lead Capture System o filtrowanie spamu.

Sprawdź czy pole `message` zawiera słowa kluczowe: "casino", "crypto", "SEO services", "link building". Jeśli tak — nie zapisuj, nie wysyłaj emaila. Zapisz do osobnego arkusza "Spam" z timestampem.

Wskazówka: IF node z warunkiem "contains" lub Code node z tablicą słów i metodą `.some()`.

45 minut. Zrób to teraz, nie odkładaj.

[SLAJD 37]

W tygodniu 2 wejdziemy głębiej w HTTP Request — paginacja, autoryzacja, rate limiting. Zbudujemy system który agreguje dane z kilku API i generuje raport.

Przygotuj klucz API do OpenAI — będziemy go używać.

Do zobaczenia w tygodniu 2.

---

*[Koniec nagrania — łączny czas: ~180 minut]*
