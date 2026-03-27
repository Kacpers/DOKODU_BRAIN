---
type: kurs-skrypt
modul: 03
słów: ~3200
status: draft
last_reviewed: 2026-03-27
---

# Tydzień 3: Skrypt do nagrania
## Skalowalność, Odporność i Disaster Prevention

> **Instrukcja dla lektora:** Skrypt pisany jest w stylu bezpośredniej rozmowy. Nie czytaj słowo w słowo — używaj go jako mapy. Miejsca oznaczone [PAUZA] to moment na oddech lub zmianę slajdu. Miejsca [DEMO] to przejście do n8n — kamera może przejść na screen share.

---

## CZĘŚĆ 1: OTWARCIE (15 minut)

### 1.1 Hook — Crash produkcyjny

Wyobraźcie sobie taki scenariusz. Piątek, 17:30. Zamknęliście laptopa, idzie weekend. Workflow działa, klient zadowolony, wszystko gra.

Poniedziałek, 8:00. Telefon. Klient mówi: "Słuchaj, moi klienci napisali że nie dostali faktur za zamówienia z weekendu." [PAUZA]

Logujesz się do n8n. 847 wykonań. 147 błędów. I co najgorsze — żadnego alertu. Żadnego emaila. Nic. Dowiedziałeś się o problemie od klienta, nie od systemu.

Byłem w tej sytuacji. Nie osobiście — ale widziałem to u klientów, którzy przyszli do Dokodu po tym jak sami zbudowali "działający workflow". Problem nie był w logice biznesowej. Problem był w tym, że workflow nie był zaprojektowany na niepowodzenie.

I dziś to zmienimy.

### 1.2 Analogia — Most

Pozwólcie że opowiem wam jak buduje się mosty. [PAUZA]

Inżynier, który projektuje most przez rzekę, nie zakłada że most będzie stał wiecznie i nic mu się nie stanie. Wręcz przeciwnie. Zakłada że coś się stanie. Projektuje na to.

Zakłada że będą trzęsienia ziemi — więc dodaje dylatacje. Zakłada że będą powodzie — więc podnosi filary. Zakłada że metal się rozszerza w upale — więc zostawia luz w konstrukcji. Zakłada że trzeba będzie przeprowadzić inspekcję — więc zostawia dostęp serwisowy.

I co najważniejsze — ma plan co robić gdy coś się posypie. Nie panikuje. Ma checklistę.

Wasze workflow to mosty. Łączą systemy, przesyłają dane, wykonują operacje finansowe. I tak jak most, nie pytacie "czy coś się posypie?" Pytacie "kiedy się posypie i co wtedy?" [PAUZA]

To jest właśnie disaster recovery mindset. I to jest fundament całego dzisiejszego tygodnia.

### 1.3 Plan na dziś

W ciągu najbliższych 4 godzin nauczycie się ośmiu rzeczy, które razem składają się na to co nazywam "Armored Workflow" — workflow klasy produkcyjnej.

Batchowanie, idempotency, error handling, retry logic, wait node, monitoring, logging i testowanie. A na końcu złożycie to wszystko w jeden system — Armored Invoicing System. Kompletny, odporny, produkcyjny system wystawiania faktur.

Zacznijmy od tego dlaczego workflow pada.

---

## CZĘŚĆ 2: BATCHING (20 minut)

### 2.1 Problem — Przetwarzanie dużych zbiorów

[DEMO — pokaż Google Sheets z 1000 wierszy]

Mam tu arkusz z tysiącem zamówień. Klasyczne zadanie: przetworz je wszystkie, wygeneruj faktury, zaktualizuj statusy.

Jak większość ludzi to zrobi? [PAUZA] Jeden node "Read Google Sheets", potem pęla przez wszystkie wyniki. Proste, działa na demo z 20 rekordami.

Z tysiącem rekordów? n8n ładuje wszystko do pamięci. Przy 500 — może działać, może nie. Przy 1000 — prawdopodobnie timeout po godzinie. Albo crash procesu. I co się staje z danymi? Żadne nie zostały przetworzone.

Bo n8n traktuje to jako jedno wielkie wykonanie. Albo wszystko, albo nic.

[DEMO — uruchom workflow bez batching, pokaż timeout]

Widzicie co się dzieje. Execution czeka, czeka, i w końcu — błąd. Godzina straconego czasu i zero wyników.

### 2.2 Rozwiązanie — SplitInBatches

Teraz patrzcie jak to zmienić. [DEMO]

Dodaję node SplitInBatches. Parametr Batch Size ustawiam na 100. Co to robi?

Zamiast jednego gigantycznego wykonania, n8n dzieli dane na partie. Pierwsza partia: rekordy 1 do 100. Przetwarza je. Zapisuje. Wraca po kolejne 100. Przetwarza. Zapisuje. I tak dalej.

Kluczowa różnica: jeśli coś się posypie przy partii 7 — partie 1 do 6 są już przetworzone i zapisane. Nie tracisz całości, tracisz jeden chunk.

[DEMO — uruchom z batchingiem, pokaż że działa]

I tutaj jest coś ważnego o czym mało kto mówi. Batching to nie tylko kwestia pamięci. To kwestia checkpoint'ów. Możliwości wznowienia od miejsca awarii.

Jak dobrać rozmiar? Zacznijcie od 50. Jeśli wywoływacie zewnętrzne API — sprawdźcie ich rate limits. Fakturownia ma limit 60 requestów na minutę? Batch size 50 z 2 sekundami przerwy między partiami.

---

## CZĘŚĆ 3: IDEMPOTENCY (20 minut)

### 3.1 Problem — Webhook który przychodzi dwa razy

Teraz temat który jest bardziej subtelny, ale równie ważny. Idempotency.

Zacznę od pytania: kto z was kiedyś wysyłał email, odświeżył stronę i dostał pytanie "czy wysłać ponownie?" [PAUZA] Właśnie — przeglądarka pyta, bo wie że może to być niebezpieczne. Że wyślecie dwa razy.

Wasze workflow mają ten sam problem. Tylko że nikt was nie pyta.

Scenariusz: Shopify wysyła webhook "nowe zamówienie nr 12345". Wasz n8n odbiera, zaczyna wystawiać fakturę. Gdzieś w środku — error. n8n odpowiada Shopify błędem 500. Co robi Shopify? Nie wie czy dostał fakturę czy nie. Więc wysyła webhook ponownie. Za 30 sekund.

Wasz workflow startuje drugi raz z tym samym zamówieniem 12345. I wystawia drugą fakturę. Klient dostaje dwie faktury. [PAUZA]

To jest realne. Wszystkie platformy e-commerce — Shopify, WooCommerce, Stripe — mają automatyczny retry dla webhooków. To feature, nie bug. Ale wasze workflow muszą to obsługiwać.

### 3.2 Rozwiązanie — Deduplication Keys

Rozwiązanie to idempotency pattern. Trzy kroki: Sprawdź, Wykonaj, Oznacz. W tej kolejności, zawsze.

[DEMO — pokaż implementację w n8n]

Pierwszy node po webhook trigger: sprawdź czy order_id 12345 już jest w tabeli "processed_orders" w Google Sheets. Jeśli jest — zwróć "skip: true" i zakończ. Jeśli nie ma — kontynuuj.

Po wykonaniu całej logiki biznesowej — na końcu workflow — dopisz order_id do tabeli processed_orders z timestampem.

[DEMO — wyślij ten sam webhook dwa razy]

Widzicie? Pierwsze wywołanie — przetworzone. Drugie — "already processed, skipping". Zero duplikatów.

Ważna uwaga: gdzie przechowujecie te processed keys. Google Sheets to dobry start — prosty, darmowy, działa. Ale przy dużym ruchu, powyżej kilkuset zamówień dziennie, rozważcie Redis lub Postgres. n8n ma natywny node Redis.

---

## CZĘŚĆ 4: ERROR TRIGGER WORKFLOW (25 minut)

### 4.1 Crash bez error handling — demonstracja

Teraz pokażę wam coś, czego nie chcecie widzieć w środku nocy. [DEMO]

Mam prosty workflow: webhook → HTTP Request do zewnętrznego API → zapis do Sheets. Celowo podaję zły URL — API nie istnieje. Uruchamiam.

[DEMO — workflow crashuje]

Co się stało? Wykonanie failed. I... nic. Cisza. Żadnego alertu, żadnego emaila, żadnego Slacka. Jeśli to jest workflow produkcyjny i macie tysiąc takich błędów przez noc — rano odkryjecie to jako pierwsi. Albo klient odkryje za was.

### 4.2 Error Trigger — architektura

Rozwiązanie jest eleganckie. n8n ma specjalny trigger node: Error Trigger. Działa tak:

Tworzysz osobny workflow — nazwijmy go "Global Error Handler". Ten workflow ma jeden trigger: Error Trigger node. I w ustawieniach każdego produkcyjnego workflow wskazujesz "gdy coś się posypie — uruchom Global Error Handler".

Jeden Error Handler dla wszystkich workflow. Centrum dowodzenia dla błędów.

[DEMO — pokaż tworzenie Error Handler workflow]

Co ma robić Error Handler? Trzy rzeczy. Pierwsza: log do Google Sheets z pełnymi informacjami — kiedy, jaki workflow, jaki błąd, link do wykonania. Druga: alert na Slack z dokładnym linkiem do failed execution. Trzecia (opcjonalnie): ticket w systemie zarządzania zadaniami.

[DEMO — stwórz Error Handler krok po kroku]

Patrzcie na dane dostępne w Error Trigger node. Macie execution.id, workflow.name, error.message i co najważniejsze — execution.url. Bezpośredni link do wykonania, które padło. Klikacie w Slacku i za 2 sekundy widzicie dokładnie co i gdzie się stało.

[DEMO — celowo crashnij workflow, pokaż alert na Slacku]

Teraz wiem o błędzie w 30 sekund, nie rano od klienta.

Jeden ważny szczegół który pominą na 99% tutoriali: Error Workflow sam może mieć błąd. Jeśli Slack jest niedostępny w momencie gdy workflow pada — Error Handler też padnie, cicho. Dlatego w Error Handler zawsze macie minimum dwa kanały — email jako fallback jeśli Slack nie działa.

---

## PRZERWA (10 minut)

[PLANSZA: "Przerwa — wrócimy za 10 minut"]

---

## CZĘŚĆ 5: RETRY LOGIC (20 minut)

### 5.1 Kiedy retry, kiedy fail fast

Zanim zbudujesz retry logic, odpowiedz sobie na jedno pytanie: czy retry cokolwiek zmieni?

Jeśli API zwróciło 401 Unauthorized — retry nic nie zmieni. Credentials są złe i za 2 sekundy nadal będą złe. Fail fast i wyślij alert.

Jeśli API zwróciło 503 Service Unavailable — retry może zadziałać. Serwer był chwilowo przeciążony. Za 2 sekundy może już odpowiada.

Jeśli dostałeś 429 Too Many Requests — retry zadziała, ale musisz poczekać. I tu masz wskazówkę: nagłówek Retry-After powie ci ile sekund czekać.

Mam tutaj tabelę decyzyjną którą stosujemy w Dokodu. [SLAJD — Error Handling Matrix]

Wydrukujcie ją sobie. Przy każdym nowym workflow wróćcie do niej i zaplanujcie co się dzieje przy każdym typie błędu.

### 5.2 Exponential Backoff — dlaczego nie "retry co sekundę"

Wyobraźcie sobie że wasze API padło. Macie 100 workflow które retryują co sekundę. To 100 requestów na sekundę do serwera który właśnie padł. Co się dzieje? Serwer dostaje jeszcze więcej ruchu niż normalnie. Nie wstaje — dostaje DDoS od waszych własnych systemów. [PAUZA]

To się naprawdę zdarza. AWS ma na to nawet nazwę: "thundering herd problem".

Rozwiązanie: exponential backoff z jitter.

Pierwsza próba — poczekaj 1 sekundę. Druga — 2 sekundy. Trzecia — 4 sekundy. Czwarta — 8 sekund. I dodajcie losowy składnik — "jitter" — żeby 100 workflow nie retryowało dokładnie w tej samej sekundzie.

[DEMO — pokaż implementację retry loop w n8n]

Buduję custom retry loop: HTTP Request node → IF node który sprawdza status odpowiedzi → jeśli sukces kontynuuj → jeśli błąd sprawdź counter → jeśli counter < 3 → Code node który liczy czas czekania → Wait node → wróć do HTTP Request.

Pokażę wam kod do obliczania czasu czekania. [SLAJD 31 — kod exponential backoff]

Skopiujcie ten kod. Jest przetestowany w produkcji. Ma jitter, ma cap żeby nie czekać w nieskończoność. Gotowy do użycia.

---

## CZĘŚĆ 6: WAIT NODE (15 minut)

### 6.1 Wait node — trzy tryby

Wait node to jeden z najbardziej niedocenianych node'ów w n8n. Pozwala workflow zapauzować wykonanie i wznowić je później.

Trzy tryby. Fixed amount — poczekaj X sekund lub minut. Używamy tego w retry logic. At specified time — poczekaj do konkretnego momentu. Świetne do "wyślij email o 9 rano". Until webhook call — poczekaj aż zewnętrzny system wyśle sygnał.

Ten trzeci tryb jest absolutnie genialny do Human-in-the-Loop. Wyobraźcie sobie workflow który generuje ofertę handlową, wysyła ją do przełożonego emailem z przyciskiem "Zatwierdź", i czeka. Dopiero gdy przełożony kliknie — workflow kontynuuje i wysyła ofertę do klienta. [PAUZA]

Tym zajmiemy się w Tygodniu 5. Na razie używamy Wait w retry logic.

### 6.2 Uwaga na timeout

Jedna ważna uwaga: n8n domyślnie kończy wykonanie po godzinie. Jeśli masz Wait node który czeka 2 godziny — sprawdź ustawienie `executions.timeout` w konfiguracji n8n.

W n8n Cloud ten limit jest zwykle wyższy, ale sprawdźcie. Nic bardziej frustrującego niż workflow który nie wznawia się po Wait bo timeout go ubił.

---

## CZĘŚĆ 7: MONITORING (20 minut)

### 7.1 Disaster recovery mindset — zmień pytanie

Wróćmy do analogii z mostem. Inżynier nie pyta "czy most spadnie?" Pyta "jak szybko się dowiemy że coś jest nie tak i jak szybko zareagujemy?"

Zmieńcie pytanie. Nie "czy mój workflow padnie?" ale "skąd będę wiedział że padł, zanim klient zadzwoni?"

To jest definicja dojrzałości operacyjnej. I buduję ją w trzech warstwach.

Pierwsza warstwa: Error Trigger który już skonfigurowaliśmy — reaguje natychmiast gdy coś pada.

Druga warstwa: monitoring aktywny — cron job który rano sprawdza czy wszystkie krytyczne workflow działają. Sprawdza nie po błędach, ale po tym że ostatnie wykonanie było za dawno. Jeśli workflow który ma działać co 15 minut, nie działał od godziny — to alarm.

Trzecia warstwa: dzienny raport — liczby. Ile wykonań, ile sukcesów, ile błędów, trend.

### 7.2 Implementacja monitoringu

[DEMO — pokaż dzienny raport workflow]

Cron trigger o 7 rano. Wywołuję n8n API i pobieram statystyki wykonań z ostatnich 24 godzin. Liczę sukces rate. Jeśli poniżej 99% — Slack alert. Zawsze wysyłam raport emailem — krótkie podsumowanie, link do n8n.

[SLAJD 32 — szablon raportu]

Ten template raportu wysyłajcie swoim klientom. Widzą że ich systemy są pod kontrolą. To buduje zaufanie i jest argumentem przy przedłużaniu kontraktów.

---

## CZĘŚĆ 8: LOGGING (15 minut)

### 8.1 Dlaczego zewnętrzne logi

n8n przechowuje historię wykonań. To dobre, ale ma ograniczenia. Po X dniach są czyszczone. Nie można łatwo filtrować po kluczu biznesowym jak order_id. Nie można agregować przez wiele workflow.

Zewnętrzny log rozwiązuje wszystkie te problemy.

### 8.2 Standard Dokodu

[SLAJD 21 — struktura logu]

Każde wykonanie logujemy ze strukturą: timestamp, nazwa workflow, execution_id, status (success/error/partial), klucz biznesowy, czas trwania, opcjonalnie komunikat błędu i numer retry.

Kluczowy element to klucz biznesowy — order_id, client_id, invoice_id. Bez tego możecie odpowiedzieć tylko na pytanie "ile było błędów?" Nie możecie odpowiedzieć na "co się stało z zamówieniem klienta Kowalski?"

### 8.3 Sub-workflow pattern

[DEMO — Log Entry sub-workflow]

Zamiast duplikować kod logowania w każdym workflow, buduję jeden "Sub: Log Entry" sub-workflow. W każdym miejscu gdzie chcę logować — wywołuję go przez Execute Workflow node.

Jeden punkt zmiany. Jutro zmienię backend z Google Sheets na Postgres — zmieniam w jednym miejscu, działa wszędzie.

---

## CZĘŚĆ 9: TESTING I STAGING (15 minut)

### 9.1 Problem z testowaniem na produkcji

Widzę to cały czas. Ktoś buduje workflow i testuje klikając "Execute" na produkcyjnym workflow z prawdziwymi danymi. Wystawia fakturę testową. Wysyła email do prawdziwego klienta.

To nie jest testowanie. To jest rosyjska ruletka.

### 9.2 Techniki testowania w n8n

Cztery techniki, od najprostszej.

Pierwsza: Manual Trigger + statyczny JSON. Zamiast prawdziwego webhooka — trigger manualny z wklejonym przykładowym JSON. Bezpieczne, powtarzalne.

Druga: Pinned Data. To mój ulubiony feature. Prawym przyciskiem na node, "Pin Data" — zamrażasz dane z jednego uruchomienia. Możesz testować dalszą część workflow bez wywoływania poprzednich node'ów. Chcecie przetestować logikę generowania faktury bez wywoływania API Shopify za każdym razem? Pin Data na wyjściu node'a pobierającego dane.

Trzecia: Test webhook. Gdy dodajecie webhook trigger, n8n daje wam dwa URL — jeden produkcyjny, jeden testowy. Testowy działa tylko gdy workflow jest w trybie edycji.

Czwarta: Partial execution. Ctrl+klik na wybranym node — uruchom od tego miejsca. Jeśli trzeci node w łańcuchu się sypie, nie musicie przechodzić przez pierwsze dwa za każdym razem.

### 9.3 Staging — minimum viable

Osobny serwer n8n dla staging to ideał. Ale na początku wystarczy prostszy setup.

Naming convention: prefix [DEV] na workflow testowych. Testowe credentials — "Fakturownia TEST", "Sheets TEST". Testowy kanał Slack: #n8n-staging. I żelazna zasada: nigdy nie deployujesz bez testu na [DEV] wersji.

---

## CZĘŚĆ 10: PROJEKT — ARMORED INVOICING (35 minut)

### 10.1 Architektura

Dobra, czas złożyć to wszystko razem. Budujemy Armored Invoicing System.

[SLAJD — architektura systemu]

Główny workflow zaczyna się od webhooka. Pierwsze co robi — idempotency check. Pobiera order_id z payloadu, sprawdza czy jest w tabeli processed_orders. Jeśli tak — zwraca 200 i kończy. Jeśli nie — kontynuuje.

Następnie pobiera dane klienta i zamówienia. Potem — serce systemu — generuje fakturę przez API. Tu mamy retry logic: 3 próby z exponential backoff.

Jeśli po 3 próbach nadal fail — Error Handler przejmuje kontrolę: alert Slack z detalami, ticket w Sheets do ręcznej weryfikacji.

Jeśli sukces — wysyła email do klienta, aktualizuje CRM/Sheets, oznacza order jako processed (idempotency), i loguje wynik.

### 10.2 Build live

[DEMO — budowa krok po kroku, ~25 minut]

Zaczynam od Webhook Trigger node. Konfiguruję ścieżkę URL i metodę POST.

Dodaję node Set żeby wyciągnąć order_id z $json.body.order_id.

Dodaję Execute Workflow node — wywołuję "Sub: Idempotency Check". Przekazuję order_id.

Dodaję IF node — jeśli skip jest true, kończę workflow. Jeśli false — kontynuuję.

Następnie HTTP Request do API fakturowego. Konfiguruję credentials. Tu dodaję retry logic — kopiuję kod exponential backoff.

Error branch z HTTP Request: IF node sprawdza retryCount < 3. Jeśli tak — Wait node + wróć. Jeśli nie — Execute Workflow "Sub: Alert Slack" + zakończ błędem.

Success branch: Email node do klienta. Sheets Update node dla CRM.

Na końcu: Execute Workflow "Sub: Idempotency Mark" i Execute Workflow "Sub: Log Entry".

[DEMO — test z duplikatem webhooka]

Wysyłam ten sam payload dwa razy. Pierwsze wywołanie — faktury wystawiona. Drugie — "already processed". System działa.

[DEMO — test z niedostępnym API]

Zmieniam URL na nieistniejący serwer. Uruchamiam. Widzicie retry loop — 3 próby, coraz dłuższe czekania. Po trzeciej — Slack alert.

---

## CZĘŚĆ 11: PODSUMOWANIE (5 minut)

Pięć zasad Armored Workflow. Zapamiętajcie je.

Jeden: Idempotency. Każdy workflow który przetwarza zewnętrzne zdarzenia musi mieć deduplication.

Dwa: Error Handler. Każdy workflow produkcyjny musi mieć podpięty Error Workflow.

Trzy: Retry Logic. Dla tymczasowych błędów — retry z backoffem i limitem prób.

Cztery: Logging. Każde wykonanie zostawia ślad z kluczem biznesowym.

Pięć: Monitoring. Wiesz o problemie zanim klient zadzwoni.

Jeśli wasze workflow spełniają te pięć zasad — macie system produkcyjny. Nie demo. Nie POC. System.

Zadanie domowe jest w materiałach — macie tydzień. W przyszłym tygodniu zaczniemy od przeglądu kilku projektów z community.

Tydzień 4 to Architektura Modularna — jak organizować dziesiątki workflow żeby nie zgubić się we własnym systemie. Do zobaczenia.

---

> **Notatka produkcyjna:** Docelowy czas nagrania ~4h 15 minut. Po montażu — 4h. Zalecany podział na dwa pliki wideo: Sesja 1 (Segmenty 1-4, ~90 min) i Sesja 2 (Segmenty 5-11, ~90 min + projekt 35 min). Alternatywnie: jeden plik z chapter markers co 15-20 minut dla YouTube.
