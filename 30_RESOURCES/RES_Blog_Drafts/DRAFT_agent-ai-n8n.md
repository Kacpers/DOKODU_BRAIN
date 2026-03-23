# Jak Zbudować Agenta AI w n8n — Krok po Kroku [2026]

Wyobraź sobie pracownika, który czyta przychodzące maile, ocenia priorytet każdego zgłoszenia, sprawdza status zamówienia w bazie danych, odpowiada na proste pytania sam — a trudne przekazuje do człowieka. Robi to 24 godziny na dobę, 7 dni w tygodniu, bez urlopu. Taki "pracownik" istnieje — to agent AI zbudowany w n8n.

n8n od wersji 1.x ma wbudowany node AI Agent, który łączy model językowy (GPT-4o, Claude, Gemini) z narzędziami i pamięcią w jednym, wizualnym miejscu. Nie piszesz kodu. Nie musisz znać Pythona ani LangChain. Klikasz, łączysz, testujesz.

W tym poradniku pokażę Ci krok po kroku, jak zbudować pierwszego działającego agenta AI w [n8n](/blog/n8n). Zaczniesz od pustego canvas, skończysz na agencie który podejmuje decyzje, używa narzędzi i pamięta kontekst rozmowy. Szacowany czas: 30-60 minut.

---

## Czym jest agent AI w n8n?

Zanim zaczniesz klikać, warto zrozumieć czym agent różni się od zwykłego workflow.

**Zwykłe workflow w n8n** działa jak przepis: krok 1 → krok 2 → krok 3. Kolejność jest stała. Jeśli mail zawiera pytanie o fakturę, workflow zawsze sprawdza faktury. Jeśli zawiera reklamację, nie wie co zrobić — bo schemat jest sztywny.

**Agent AI** działa inaczej. Dostaje zadanie i sam decyduje jak je wykonać. Widzi dostępne narzędzia (tools) — może to być wyszukiwanie w bazie, wysyłanie maila, sprawdzanie API — i autonomicznie wybiera które użyć i w jakiej kolejności. Wynik jednego kroku wpływa na następny. Agent "myśli".

W n8n agent AI to kombinacja trzech elementów:

- **AI Agent node** — centralny mózg, orkiestrator. Odbiera zadanie, planuje działanie, koordynuje narzędzia.
- **Tools (narzędzia)** — to co agent może "zrobić". HTTP Request, Gmail, Google Sheets, Code Node, bazy danych.
- **Memory (pamięć)** — dzięki niej agent pamięta poprzednie wiadomości w rozmowie i nie zaczyna od zera przy każdym pytaniu.

Techniczne podłoże: n8n implementuje AI Agent node na bazie LangChain JS. Pod spodem działa wzorzec ReAct (Reason + Act) — agent naprzemiennie myśli o zadaniu i wykonuje akcje, aż dojdzie do wyniku.

Chcesz pełny kontekst czym są agenci AI jako koncepcja? Przeczytaj nasz [przewodnik po agentach AI](/blog/agenty-ai).

---

## Czego potrzebujesz zanim zaczniesz

Lista krótka, ale każdy punkt jest wymagany:

- **n8n zainstalowane i działające** — lokalnie przez Docker lub n8n Cloud. Jeśli jeszcze nie masz, sprawdź nasz [poradnik instalacji n8n przez Docker](/blog/n8n/docker-instalacja-konfiguracja).
- **Klucz API do modelu AI** — OpenAI (GPT-4o) lub Anthropic (Claude 3.7 Sonnet). Klucz generujesz na platformie dostawcy i dodajesz w n8n jako Credential.
- **Podstawowa znajomość n8n** — powinieneś wiedzieć jak dodać node, połączyć nodes i uruchomić workflow. Nie wiesz? Zacznij od [centrum wiedzy o n8n](/blog/n8n).
- **30-60 minut** — tyle wystarczy na pierwszego działającego agenta.

Opcjonalnie: konto Google (do integracji z Gmail/Sheets) lub inne narzędzie, które agent ma używać jako tool.

---

## Architektura agenta w n8n

Zanim klikniesz pierwszy node, warto narysować (choćby w głowie) co budujesz. Każdy agent w n8n ma tę samą podstawową architekturę:

```
Trigger → AI Agent Node → [Tools] → Output
                ↑
            [Memory]
```

**Trigger** to punkt startowy — skąd agent dostaje zadania. Może to być wiadomość na czacie, webhook od zewnętrznego systemu, albo harmonogram (co godzinę sprawdź nowe zgłoszenia).

**AI Agent Node** to centrum dowodzenia. Dostaje zadanie od triggera, analizuje je, decyduje czy i których tools użyć, interpretuje wyniki i formułuje odpowiedź.

**Tools** to narzędzia agenta — wszystko co może "zrobić" w świecie poza LLM. Przykłady:
- **HTTP Request** — wywołanie dowolnego API (baza klientów, system CRM, zewnętrzny serwis)
- **Code Node** — własna logika w JavaScript lub Python
- **Gmail** — wysyłanie i odczytywanie maili
- **Google Sheets** — zapis i odczyt danych w arkuszu
- **Slack** — wysyłanie wiadomości do kanałów
- **Notion, Airtable, Jira** — setki gotowych integracji n8n

**Memory** to pamięć krótko- lub długoterminowa:
- **Simple Memory (Window Buffer)** — przechowuje ostatnie X wiadomości z rozmowy. Prosto, wystarczy do większości przypadków konwersacyjnych.
- **Vector Store Memory** — indeksuje dokumenty i fragmenty rozmów jako embeddingi. Używasz gdy agent ma mieć dostęp do bazy wiedzy (FAQ, dokumentacja, historia zgłoszeń).

Ważna zasada: agent widzi opisy tools i na podstawie tych opisów decyduje kiedy których użyć. Dobry opis tool to połowa sukcesu.

---

## Krok 1 — Stwórz trigger

Otwórz n8n, kliknij **"New Workflow"**, potem **"+"** żeby dodać pierwszy node.

Masz trzy główne opcje triggera dla agentów:

**Chat Trigger (On New Chat Message)** — najczęściej używany. Tworzy interfejs czatu bezpośrednio w n8n, przez który możesz rozmawiać z agentem. Idealny do testowania i budowania agentów konwersacyjnych (support, doradca, asystent).

**Webhook** — agent startuje gdy zewnętrzny system wyśle żądanie HTTP. Używasz gdy chcesz podpiąć agenta do strony, aplikacji, lub innego workflow.

**Schedule Trigger** — agent uruchamia się automatycznie co określony czas (co 5 minut, co godzinę, codziennie o 8:00). Idealny do agentów monitorujących (sprawdź nowe maile, przeskanuj zgłoszenia).

Na potrzeby tego poradnika wybierz **Chat Trigger** — zobaczysz agenta w akcji od razu.

---

## Krok 2 — Dodaj node AI Agent

Kliknij **"+"** za triggerem, wyszukaj **"AI Agent"** i dodaj node.

Po dodaniu zobaczysz kilka sekcji do skonfigurowania:

### Wybór modelu (Language Model)

Kliknij w sekcję **"Language Model"** i połącz subnode modelu. Dostępne opcje:
- **OpenAI Chat Model** — GPT-4o (zalecany), GPT-4o mini (tańszy)
- **Anthropic Chat Model** — Claude 3.7 Sonnet (bardzo dobry dla złożonych zadań)
- **Google Gemini** — alternatywa, dobra integracja z ekosystemem Google
- **Ollama** — modele lokalne, dla self-hosted bez kosztów API

Przy pierwszym użyciu musisz dodać Credential z kluczem API.

### System Prompt — to jest najważniejsze

System prompt to instrukcja dla agenta: kim jest, co robi, jakie ma zasady. Wiele osób pisze go za ogólnie — to największy błąd.

Dobry system prompt dla agenta obsługi klienta wygląda tak:

```
Jesteś asystentem obsługi klienta firmy [Nazwa].
Twoim zadaniem jest odpowiadanie na pytania klientów dotyczące: zamówień, faktur, statusu dostawy.

Zasady:
- Zawsze sprawdź status zamówienia przez tool "Sprawdź zamówienie" zanim odpiszesz na pytanie o status
- Jeśli pytanie dotyczy zwrotu lub reklamacji, użyj tool "Przekaż do działu obsługi"
- Odpowiadaj po polsku, krótko i konkretnie
- Nie podawaj informacji których nie znasz — powiedz "Sprawdzę i wrócę do Ciebie"

Masz dostęp do narzędzi: [lista tools — n8n wypełnia automatycznie]
```

Kluczowe: system prompt powinien mówić agentowi KIEDY używać konkretnych tools. Agent czyta opisy tools i system prompt razem — im konkretniej, tym lepiej.

---

## Krok 3 — Dodaj narzędzia (tools)

Tools to miejsce gdzie agent zdobywa prawdziwą moc. Bez tools agent to tylko chatbot który odpowiada z pamięci modelu. Z tools — to agent który wykonuje akcje w Twoim systemie.

### Jak podłączyć tool do agenta

Na dole node'a AI Agent zobaczysz złącze **"Tools"**. Kliknij **"+"** i wybierz tool który chcesz dodać.

### Tool 1: HTTP Request — połączenie z dowolnym API

HTTP Request tool pozwala agentowi wywołać dowolny endpoint API. Klient pyta o status zamówienia? Agent wywoła Twój API z numerem zamówienia i zwróci wynik.

Konfiguracja: URL (możesz użyć wyrażeń dynamicznych z danymi od użytkownika), metoda (GET/POST), nagłówki autoryzacyjne.

**Kluczowy szczegół:** każdy tool ma pole **"Description"** — to tekst który agent czyta żeby wiedzieć kiedy go użyć. Napisz np.: *"Użyj tego tool gdy użytkownik pyta o status zamówienia. Przyjmuje numer zamówienia jako parametr order_id."*

### Tool 2: Code Node — własna logika

Code Node jako tool pozwala agentowi wykonać dowolny JavaScript lub Python. Parsowanie tekstu, obliczenia, transformacja danych — cokolwiek czego nie ma w gotowych integracjach.

### Tool 3: Gotowe integracje

n8n ma setki gotowych node'ów które możesz używać jako tools:
- **Gmail** — odczytaj wiadomości, wyślij odpowiedź
- **Google Sheets** — zapisz wynik, sprawdź dane klienta
- **Notion** — przeszukaj bazę wiedzy, dodaj notatkę
- **Slack** — wyślij powiadomienie do kanału
- **Jira** — utwórz ticket, sprawdź status

Dla każdego z nich pamiętaj o dobrym opisie — to instrukcja dla agenta kiedy ma po ten tool sięgnąć.

---

## Krok 4 — Pamięć agenta

Bez pamięci agent traktuje każdą wiadomość jak pierwszą w życiu. Zapytasz "a co z moim poprzednim zamówieniem?" — nie będzie wiedział o czym mówisz.

### Simple Memory (Window Buffer)

To podstawowa opcja — agent zapamiętuje ostatnie X par pytanie-odpowiedź. Wystarczy dla większości agentów konwersacyjnych.

Jak dodać: na złączu **"Memory"** w AI Agent node kliknij **"+"** → wyszukaj **"Simple Memory"** → dodaj. Skonfiguruj **Context Window Length** (np. 10 ostatnich wiadomości).

Ograniczenie: pamięć nie przeżywa restartu n8n i nie działa między różnymi sesjami (różnymi rozmowami).

### Vector Store Memory

Zaawansowana opcja gdy agent musi mieć dostęp do dużej bazy wiedzy: dokumentacja produktu, FAQ, historia setek zgłoszeń.

Dokumenty są indeksowane jako embeddingi, agent wyszukuje semantycznie ("co pasuje do tego pytania?"). Działa z Pinecone, Qdrant, Supabase, lub prostym in-memory store do testów.

Kiedy używać Vector Store: gdy baza wiedzy ma więcej niż kilkadziesiąt dokumentów i musi być dostępna między sesjami.

---

## Praktyczny przykład — Agent obsługi klienta e-commerce

Zbudujmy konkretnego agenta. Scenariusz: sklep internetowy chce agenta który:
1. Odpowiada na pytania o status zamówienia (sprawdza API)
2. Odpowiada na ogólne pytania na podstawie FAQ
3. Trudne sprawy eskaluje — wysyła notatkę do Slacka

### Budowa krok po kroku

**Node 1: Chat Trigger** — punkt wejścia, klient pisze wiadomość.

**Node 2: AI Agent** z tym system promptem:

```
Jesteś asystentem sklepu internetowego TwojSklep.pl.

Obsługujesz pytania klientów. Masz dostęp do trzech narzędzi:
1. "Sprawdź status zamówienia" — gdy klient pyta o zamówienie, ZAWSZE użyj tego tool z numerem zamówienia
2. "Przeszukaj FAQ" — gdy pytanie dotyczy polityki zwrotów, wysyłki, płatności
3. "Eskaluj do supportu" — gdy pytanie jest skomplikowane, dotyczy reklamacji >500 PLN, lub klient jest wyraźnie niezadowolony

Zasady:
- Odpowiadaj po polsku, uprzejmie ale konkretnie
- Nie wymyślaj informacji — jeśli nie znasz odpowiedzi, eskaluj
- Numer zamówienia ma format: ORD-XXXXX
```

**Tool 1: HTTP Request** — GET `https://api.twojsklep.pl/orders/{orderId}` — opis: *"Sprawdza status zamówienia w systemie. Wymagany parametr: orderId (numer zamówienia w formacie ORD-XXXXX)"*

**Tool 2: Vector Store** zaindeksowany FAQ sklepu — opis: *"Przeszukuje bazę FAQ sklepu. Używaj do pytań o politykę zwrotów, czas dostawy, metody płatności, procedury reklamacyjne"*

**Tool 3: Slack node** wysyłający wiadomość do kanału #support — opis: *"Eskaluje sprawę do zespołu obsługi. Używaj gdy pytanie jest zbyt skomplikowane lub klient wymaga indywidualnej pomocy. Podaj streszczenie problemu."*

**Memory: Simple Memory** z window 8 wiadomości.

Cały workflow gotowy. Czas budowy: około 45 minut. Obsługuje ~80% typowych zapytań bez udziału człowieka.

> Chcesz zbudować taki system dla swojej firmy? Sprawdź nasze [warsztaty n8n](/szkolenia/n8n-automatyzacja) — budujemy działającego agenta od zera w ciągu jednego dnia.

---

## Typowe błędy przy budowaniu agentów

### Błąd 1: Za ogólny system prompt

*"Jesteś pomocnym asystentem"* to za mało. Agent nie wie czego się od niego oczekuje, kiedy eskalować, jakim tonem pisać. Skutek: przypadkowe, niespójne zachowanie.

Poprawka: opisz rolę, zakres, zasady używania tools i ton komunikacji.

### Błąd 2: Za dużo tools naraz

Jeśli dasz agentowi 15 tools, będzie się mylił które użyć. Zacznij od 2-3 tools. Dodawaj kolejne gdy agent sprawdza się w podstawowym zakresie.

### Błąd 3: Słabe opisy tools

Opis tool to instrukcja dla agenta — kiedy i jak go użyć. Jeśli opis jest pusty lub ogólnikowy, agent będzie używał tool losowo lub wcale.

### Błąd 4: Brak obsługi błędów

API może nie odpowiedzieć. Tool może zwrócić błąd. Bez obsługi błędów agent się "zawiesi" lub zwróci bezsensowny wynik. Dodaj node **"Error Trigger"** do workflow.

### Błąd 5: Nieskończona pętla

Agent może próbować wielokrotnie wywołać tool który nie działa, wpadając w pętlę. W ustawieniach AI Agent node ustaw **Max Iterations** (np. 10) — po tym limicie agent zakończy działanie z informacją o błędzie.

### Jak testować agenta

Przed wdrożeniem na produkcję:
1. Testuj z Chat Trigger w n8n — możesz rozmawiać bezpośrednio
2. Loguj wszystkie wywołania tools — sprawdzaj czy agent wybiera właściwe
3. Testuj edge cases: puste pytania, błędne dane, emocjonalne wiadomości
4. Sprawdź co się dzieje gdy API tool nie odpowiada

---

## Kiedy agent, a kiedy zwykłe workflow?

To pytanie, które słyszę często. Odpowiedź zależy od tego ile "decyzji" musi być podjętych w procesie.

**Użyj zwykłego workflow gdy:**
- Proces ma stały, przewidywalny schemat (zawsze krok A → B → C)
- Dane wejściowe mają ustaloną strukturę (formularz, webhook z polami)
- Szybkość i koszty są krytyczne (agent kosztuje więcej tokenów)
- Nie potrzebujesz interpretacji języka naturalnego

**Użyj agenta gdy:**
- Dane wejściowe to tekst w języku naturalnym (maile, wiadomości, zgłoszenia)
- Proces wymaga "decyzji" na podstawie treści (kategoria problemu, priorytet, akcja)
- Chcesz interfejs konwersacyjny (chatbot, asystent)
- Nie wiesz z góry jakich narzędzi będzie potrzeba dla danego zapytania

Pełne porównanie z tabelą znajdziesz w naszym artykule o [agentach AI](/blog/agenty-ai).

---

## FAQ

**Czy agent n8n działa 24/7?**

Tak, o ile n8n jest uruchomione non-stop. Na n8n Cloud (plan płatny) workflows i agenci działają bez przerwy. Na self-hosted zależy od Twojej infrastruktury — Docker na VPS/serwerze zapewnia ciągłość działania. Więcej o opcjach hostingu: [licencja i cennik n8n](/blog/n8n/licencja-cennik).

**Ile kosztuje uruchomienie agenta?**

Dwa składniki kosztu: n8n (Cloud od ~$24/msc lub self-hosted za darmo) oraz API modelu AI. Koszt tokenów zależy od modelu i skali. GPT-4o kosztuje ok. $2.50/1M tokenów wejściowych i $10/1M wyjściowych (marzec 2026). Prosty agent obsługi klienta przy 100 rozmowach dziennie to ok. $5-15/msc za tokeny. Claude 3.7 Sonnet ma zbliżone ceny.

**Czy mogę zbudować agenta bez n8n Cloud (self-hosted)?**

Tak, AI Agent node działa identycznie w wersji self-hosted. Potrzebujesz jedynie własnych kluczy API do modeli AI. Self-hosted n8n jest bezpłatny (licencja fair-code). Instalacja zajmuje 15 minut — sprawdź [poradnik Docker](/blog/n8n/docker-instalacja-konfiguracja).

**Jakie modele AI działają w n8n?**

n8n obsługuje: OpenAI (GPT-4o, GPT-4o mini, GPT-3.5), Anthropic (Claude 3.7, 3.5 Sonnet, Haiku), Google (Gemini 2.0 Flash, Gemini 1.5 Pro), Mistral, Cohere oraz lokalne modele przez Ollama. Do większości zastosowań biznesowych polecam GPT-4o lub Claude 3.7 Sonnet — mają najlepszy stosunek jakości do ceny.

---

## Następne kroki

Zbudowałeś pierwszego agenta. Co dalej?

**Źródła inspiracji:**
- [n8n Community Templates](https://n8n.io/workflows/) — setki gotowych workflow i agentów do skopiowania
- Forum n8n Community — rozwiązania problemów, przykłady od społeczności
- Nasz blog z [przykładami workflow i automatyzacji](/blog/n8n/przyklady-workflow-automatyzacji)

**Rozwijaj agenta:**
- Dodaj kolejne tools (kalendarz, CRM, baza danych)
- Zaimplementuj Vector Store z dokumentacją firmy
- Podłącz agenta do zewnętrznego interfejsu przez Webhook

**Zainwestuj w wiedzę:**
Jeśli chcesz wdrożyć agentów AI w firmie i zrobić to raz a porządnie — dołącz do naszego [kursu n8n](/kursy/n8n). Budujesz działające automatyzacje i agentów podczas kursu, nie po.

> Masz pytania dotyczące konkretnego przypadku użycia? Umów **bezpłatną 30-minutową konsultację** — przejdziemy przez Twój proces i pokażemy jak zautomatyzować go agentem AI. [Umów konsultację](/szkolenia/n8n-automatyzacja)
