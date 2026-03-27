---
type: course-script
modul: 07
tytul: "Cyfrowy Mózg Firmy (RAG) i Eliminacja Halucynacji"
dlugosc_szacowana: "3h 15min"
status: draft
last_reviewed: 2026-03-27
tags: [RAG, embeddings, vector-database, Qdrant, Pinecone, PGVector, chunking, n8n, halucynacje]
---

# Tydzień 7: Cydrowy Mózg Firmy (RAG) — Skrypt do Nagrania

> **Legenda:**
> `[KAMERA]` = mówisz do kamery
> `[DEMO: opis]` = przełącz na ekran / n8n — w nawiasie co konkretnie pokazujesz
> `[SLAJD N]` = zmień na slajd numer N
> `[PAUZA]` = chwila ciszy, uczestnik może przetworzyć
> `[PYTANIE do widzów: ...]` = pytanie retoryczne, zatrzymaj się na 3 sekundy

---

## OTWARCIE (0:00 – 0:10)

`[KAMERA]`

Twoja firma ma tysiące dokumentów.

Regulaminy, umowy, oferty, instrukcje, maile, notatki ze spotkań. Leżą na Google Drive, na serwerze, w skrzynce pocztowej. Nikt ich nie czyta — bo nikt nie ma czasu.

`[PAUZA]`

A kiedy pracownik pyta "jakie są warunki płatności w umowie z Acme?" — ktoś musi grzebać przez pół godziny w folderach, żeby znaleźć odpowiedź.

Twój AI może to zrobić w 3 sekundy.

Ale nie taki AI, któremu po prostu zadajesz pytanie. Bo taki AI ci zmyśli odpowiedź — i zrobi to z pewnością siebie, która jest przerażająca.

Mam na myśli AI wyposażony w **RAG** — Retrieval Augmented Generation. I właśnie temu poświęcony jest cały ten tydzień.

Dzisiaj zbudujesz **Firmowy Asystent Wiedzy** — system który czyta Twoje dokumenty, rozumie ich treść, i odpowiada na pytania z precyzyjnymi cytatami: nazwa pliku, numer strony, fragment tekstu.

Zaczynamy.

---

## SEGMENT 1: Czym jest RAG — od intuicji do architektury (0:10 – 0:35)

### 1.1 Definicja i analogia

`[KAMERA]`

RAG — trzy słowa, trzy etapy.

**Retrieval** — pobierz właściwe fragmenty z bazy wiedzy. **Augmented** — wzbogać prompt o te fragmenty. **Generation** — AI generuje odpowiedź, ale TYLKO na podstawie tych fragmentów.

Najlepsza analogia jaką znam: dobry bibliotekarz.

Bibliotekarz nie zapamiętuje treści każdej książki w bibliotece. Nie potrafi — nikt nie potrafi. Ale bibliotekarz wie dokładnie gdzie szukać. Pytasz go o termin płatności w umowie z Acme — on idzie do właściwej szafy, wyciąga właściwy segregator, otwiera na właściwej stronie i mówi: "§4.2, strona 8, termin to 21 dni".

I co ważniejsze — jeśli tej informacji nie ma w żadnej z dostępnych książek, dobry bibliotekarz powie: "Nie mam takiej pozycji w zbiorach". Nie zmyśli.

To jest właśnie AI z RAG. Nie zapamiętuje całej wiedzy. Ale wie gdzie szukać. I nie zmyśla.

### 1.2 Demo kontrastu — bez RAG

`[DEMO]`

Pozwólcie, że zanim cokolwiek zbuduję, pokażę wam różnicę.

Otwieram ChatGPT albo Claude — dowolny model bez dostępu do zewnętrznych danych.

Pytam: "Jakie są warunki płatności w umowie naszej firmy z klientem Acme?"

`[PAUZA — czekaj na odpowiedź modelu]`

Zobaczcie co dostajecie. "Standardowe warunki płatności wynoszą zazwyczaj 14-30 dni od daty wystawienia faktury. Zaliczki są często stosowane w wysokości 20-50%..." Brzmi sensownie, prawda?

To jest 100% zmyślone. Model nie ma pojęcia o Twojej umowie z Acme. Generuje statystycznie prawdopodobne zdania na temat "warunki płatności". I robi to z absolutną pewnością siebie.

To jest halucynacja. I to jest niebezpieczne.

`[KAMERA]`

Teraz pokażę wam to samo pytanie — ale z RAG. Po drugiej stronie dnia, kiedy zbudujemy nasz system.

### 1.3 Architektura RAG

`[SLAJD: RAG Pipeline — diagram]`

Zanim wejdziemy w szczegóły, zobaczmy pełny obraz.

RAG ma dwie strony:

Lewa strona — **Ingestion Pipeline**. To się dzieje RAZ, dla każdego dokumentu. Bierzesz dokument, dzielisz na małe kawałki — tak zwane chunki — każdy kawałek zamieniasz w wektor liczb, i zapisujesz do bazy wektorowej. Tak budujesz bazę wiedzy.

Prawa strona — **Query Pipeline**. To się dzieje przy KAŻDYM pytaniu użytkownika, w ciągu sekund. Pytanie też zamieniasz w wektor. Szukasz w bazie najpodobniejszych fragmentów. Dajesz te fragmenty do AI razem z pytaniem. AI generuje odpowiedź — ale TYLKO na podstawie tych fragmentów.

I tu jest kluczowy mechanizm: jeśli fragmenty nie zawierają odpowiedzi — AI ma obowiązek powiedzieć "nie wiem". Nie zmyśla.

---

## SEGMENT 2: Embeddings — jak tekst zamienia się w liczby (0:35 – 0:55)

`[KAMERA]`

Teraz musimy porozmawiać o embeddingach. Wiem, że to brzmi technicznie. Obiecuję, że po trzech minutach będzie intuicyjne.

### 2.1 Czym jest embedding

`[SLAJD: Embedding — wektor]`

Embedding to zamiana tekstu na listę liczb. Konkretnymi liczbami. Przykładowo zdanie "termin płatności wynosi 21 dni" zamienia się na wektor o 1536 wymiarach: 0.23, minus 0.87, 0.14... i tak dalej przez 1536 pozycji.

Na pierwszy rzut oka — brzmi absurdalnie. Po co zamieniać tekst na liczby?

Dlatego, że **podobne znaczeniowo zdania produkują podobne wektory**.

### 2.2 Wizualizacja przestrzeni semantycznej

`[SLAJD: Scatter plot 2D]`

Wyobraź sobie mapę. Na tej mapie podobne sklepy stoją obok siebie. Piekarnie przy piekarniach. Banki przy bankach. Restauracje przy restauracjach.

W przestrzeni embeddingów jest tak samo. Wszystkie fragmenty o warunkach płatności stoją obok siebie. Wszystkie fragmenty o polityce HR — w innym miejscu. Techniczne specyfikacje — w jeszcze innym.

Kiedy wpisujesz pytanie "ile mam dni na zapłatę faktury?" — to pytanie też zamieniasz w wektor. I ten wektor ląduje właśnie obok fragmentów o warunkach płatności. Nie obok fragmentów HR.

To jest magia embeddingów. Nie szukasz po słowach kluczowych — szukasz po znaczeniu.

### 2.3 Wybór modelu embeddingowego

`[SLAJD: Tabela modeli]`

Kilka słów o wyborze modelu. Masz trzy podstawowe opcje od OpenAI:

`text-embedding-ada-002` — stary standard, dobry do proof of concept, ale kosztuje 5 razy więcej niż nowsze opcje.

`text-embedding-3-small` — mój rekomendowany wybór dla 95% projektów. Jest 5 razy tańszy od ada-002 przy lepszej jakości. To jest paradoks rynku — nowszy, lepszy i tańszy.

`text-embedding-3-large` — kiedy potrzebujesz absolutnie najwyższej precyzji. Kosztuje 7x więcej niż 3-small. Uzasadnione tylko przy bardzo specjalistycznych domenach.

Jeśli chcesz zero kosztów i self-hosting — jest `nomic-embed-text` przez Ollama. Działa lokalnie, porównywalny z 3-small.

**Rekomendacja: text-embedding-3-small. Nie komplikuj.**

---

## SEGMENT 3: Vector Databases — Pinecone vs Qdrant vs PGVector (0:55 – 1:20)

`[KAMERA]`

Masz wektory. Gdzie je przechowujesz?

Nie w Postgresie domyślnym. Nie w JSONie. Potrzebujesz specjalizowanej bazy wektorowej — czyli silnika zoptymalizowanego pod jeden konkretny cel: znajdź mi najszybciej N najbliższych wektorów dla danego zapytania. To się nazywa Approximate Nearest Neighbor search.

Na rynku jest kilkanaście rozwiązań. Omówię trzy które widzę najczęściej w projektach z klientami.

### 3.1 Przegląd i tabela porównawcza

`[SLAJD 13]`

[PYTANIE do widzów: Gdybyś miał jutro wdrożyć RAG u klienta — co byś wybrał?]

Trzy opcje na jednej tabeli:

| Cecha | Pinecone | Qdrant | PGVector |
|-------|----------|--------|----------|
| **Hosting** | Cloud only | Self-host lub Cloud | Self-host (Postgres) |
| **Setup time** | 5 minut | 10 minut (Docker) | 15 minut |
| **Free tier** | 1 index, 100K wektorów | Open-source, gratis | Gratis z Postgres |
| **Prod koszt (1M wekt.)** | ~$70/mies. | ~$20 cloud / $0 self-host | Koszt VPS |
| **Latencja (local)** | ~50ms | ~5ms | ~10ms |
| **Hybrid search** | Tak | Tak — wbudowany BM25 | Plugin |
| **Filtry metadanych** | Tak | Tak (payload filters) | SQL WHERE |
| **Integracja n8n** | Natywna | Natywna | Natywna |

`[KAMERA]`

Teraz każda opcja z osobna — żeby wiedzieć kiedy co wybrać.

**Pinecone** — najprostszy start, zero devops. Tworzysz konto, tworzysz index, wklejasz klucz API do n8n. Gotowe w 5 minut. Idealne kiedy robisz PoC dla klienta i chcesz pokazać efekt już na pierwszym spotkaniu, a nie konfigurować infrastrukturę.

Problem? Dwa.

Pierwszy — koszty przy skali. $70 miesięcznie za milion wektorów to dużo, jeśli robisz self-hosted n8n za $15 miesięcznie. Przy dużych bazach różnica jest odczuwalna.

Drugi — dane w chmurze zewnętrznej. Dla klientów z sektora finansowego, prawnego, medycznego — to często twardy bloker. "Nasze dokumenty nie mogą wychodzić poza EU ani za firmowy firewall." Pinecone wtedy odpada.

**PGVector** — jeśli Twój klient ma już PostgreSQL, to najprostsza droga. Jedno rozszerzenie (`CREATE EXTENSION vector`), ta sama baza, te same narzędzia backupu i monitorowania. Nie dodajesz nowego elementu do infrastruktury.

Ograniczenia: przy bardzo dużych bazach — powyżej miliona wektorów — wydajność spada względem dedykowanych rozwiązań. Hybrid search wymaga dodatkowej konfiguracji z `tsvector`.

Kiedy warto: klient ma Postgresa, mała-średnia baza wiedzy, chce prostotę.

**Qdrant** — mój faworyt i wybór na ten kurs.

Open-source, napisany w Rust. Stąd ta latencja poniżej 5ms lokalnie. Hybrid search wbudowany od wersji 1.7 — semantyczny plus BM25 keyword w jednym zapytaniu, bez żadnych pluginów. Payload filters — możesz zapytać "szukaj podobnych wektorów tylko wśród dokumentów kategorii Finance i zmodyfikowanych po 2026-01-01." Wszystko w jednym API callu.

I kluczowe: możesz go zmienić na Pinecone w n8n jedną zmianą node'a. Ta sama logika, inne credentials. Nie uzależniasz się.

### 3.2 Qdrant — setup lokalnie

`[DEMO: terminal]`

Jedna komenda:

```bash
docker run -p 6333:6333 -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage \
  qdrant/qdrant
```

Otwieramy `localhost:6333/dashboard`.

[DEMO: pokaż Qdrant Dashboard — utwórz kolekcję "company_knowledge" przez GUI]

Kolekcja to odpowiednik tabeli w relacyjnej bazie. Tworzę `company_knowledge`. Rozmiar wektora: 1536 (dla text-embedding-3-small). Metryka odległości: Cosine.

I tyle. Lokalna baza wektorowa gotowa. Zero kosztów, pełna kontrola.

`[KAMERA]`

Teraz zanim zaczniesz wrzucać dokumenty — musimy porozmawiać o chunkingu. Bo zły chunking jest numerem jeden na liście przyczyn złych wyników RAG. Powtórzę to jeszcze raz — 80% problemów z "AI nie rozumie pytania" to problem chunkingu, nie modelu.

### 3.3 Chunking — dlaczego to ważne

Wyobraź sobie że masz umowę — 20 stron. Mógłbyś wrzucić cały dokument jako jeden chunk. Jeden wektor dla 20 stron tekstu.

Problem: ten wektor stara się reprezentować 200 różnych tematów jednocześnie. Wynikowy wektor jest rozmyty — słaby we wszystkim, silny w niczym.

Drugie ekstremum: każde zdanie jako osobny chunk. Teraz chunk "wynosi 21 dni" bez żadnego kontekstu co "wynosi 21 dni" — jest bezużyteczny.

`[SLAJD: Chunking strategies diagram]`

Trzy strategie:

**Fixed Size** — najprostrzy. Tną co 500 tokenów. Przewidywalny, łatwy w implementacji. Problem: może przeciąć zdanie w połowie.

**Semantic** — inteligentny. Model wykrywa gdzie kończy się jeden temat a zaczyna drugi. Każdy chunk to jeden temat. Lepsza jakość, ale wolniejszy i droży.

**Hierarchical** — najdokładniejszy. Trzy poziomy: cały dokument (summary), rozdziały, chunki. Retrieval może działać na każdym poziomie. Złożona implementacja — dla bardzo dużych baz.

Dla kursu używamy Fixed Size: 500 tokenów, 50 tokenów overlap.

### 3.4 Chunk Overlap — kluczowy szczegół

`[SLAJD: Overlap wizualnie]`

O overlappie muszę powiedzieć osobno, bo to jest często pomijane i bardzo ważne.

Wyobraź sobie że tekst jest pociągiem a chunkowanie to dzielenie go na wagony. Bez overlapu — na granicy między wagonami możesz przeciąć zdanie dokładnie w połowie. Chunk 1 kończy się na "termin płatności wynosi", chunk 2 zaczyna się od "21 dni od daty faktury".

Pytanie o termin płatności — ani chunk 1 ani chunk 2 nie ma pełnej odpowiedzi.

Z overlappem 50 tokenów — chunk 2 zawiera też 50 tokenów z końca chunk 1. "...termin płatności wynosi 21 dni od daty faktury..."

Teraz retrieval działa. Koszt: 10% więcej tokenów. Wartość: dramatycznie lepsza jakość odpowiedzi na pytania o informacje które leżą na granicy chunków.

**Zawsze używaj overlapu. 10% rozmiaru chunka to dobry punkt startowy.**

---

## SEGMENT 4: Budujemy Ingestion Pipeline (1:15 – 1:55)

`[DEMO n8n]`

Czas na pierwsze demo. Budujemy Workflow #1 — Ingestion Pipeline.

Cel jest prosty: kiedy pojawia się nowy plik w Google Drive, albo istniejący plik się zmienia — automatycznie go przetwarzamy i wrzucamy do Qdrant.

### 4.1 Trigger i pobieranie pliku

Zaczynam od triggera. W n8n masz "Google Drive Trigger" — ustawiam na event "File Created or Updated" w konkretnym folderze. Na przykład "Firma_Wiedza".

Ważna rzecz: dodaj filtr na typ pliku. PDF i DOCX obsłużysz inaczej niż Google Sheets. Zacznijmy od PDF i DOCX.

Następny node: Download File. Pobiera zawartość pliku z Drive.

Teraz potrzebujemy wyciągnąć tekst. Dla PDF — używasz node PDF Parser. Dla DOCX — node File Extractor z opcją "Extract Text". Wynik: surowy tekst dokumentu.

### 4.2 Chunking w Code Node

`[KAMERA]`

Chunkowanie to Code Node. n8n nie ma wbudowanego chunksera na poziomie który chcemy — ale napisanie prostego chunksera to 20 linii JavaScript.

`[DEMO — pokaż kod]`

```javascript
// Chunker: 500 tokenów, 50 overlap
const text = $input.first().json.text;
const chunkSize = 500;      // tokenów (aprox: 1 token ≈ 4 znaki)
const overlap = 50;
const charsPerToken = 4;

const chunkChars = chunkSize * charsPerToken;
const overlapChars = overlap * charsPerToken;

const chunks = [];
let start = 0;

while (start < text.length) {
  const end = Math.min(start + chunkChars, text.length);
  const chunkText = text.slice(start, end);

  chunks.push({
    text: chunkText,
    chunkIndex: chunks.length,
    startChar: start,
    endChar: end
  });

  start = end - overlapChars;
  if (start <= 0 || end === text.length) break;
}

return chunks.map(chunk => ({ json: {
  ...chunk,
  fileName: $input.first().json.fileName,
  fileId: $input.first().json.fileId,
  modifiedDate: new Date().toISOString()
}}));
```

Proste. Działa. 500 znaków * 4 = 2000 znaków na chunk, 200 znaków overlap.

### 4.3 Embeddings i zapis do Qdrant

Po Code Node — "Loop Over Items". Każdy chunk procesujemy osobno.

Wewnątrz pętli: node "OpenAI Embeddings" z modelem text-embedding-3-small. Podajesz `{{ $json.text }}` jako input. Dostajesz wektor 1536 wymiarów.

Następnie: "Qdrant Vector Store — Insert". Konfigurujesz credential Qdrant (URL: `http://localhost:6333`). Kolekcja: `company_knowledge`. Content: `{{ $json.text }}`. Metadata: cały obiekt z fileName, fileId, page, chunkIndex, modifiedDate.

Uruchamiam. I teraz... `[PAUZA]`... patrzę na dashboard Qdrant. Kolekcja company_knowledge. Punkt po punkcie pojawiają się chunki z naszego dokumentu.

### 4.4 Incremental updates — hash trick

`[SLAJD]`

Jeden ważny szczegół: co się dzieje kiedy dokument się zmienia?

Bez żadnego mechanizmu — Ingestion Workflow doda nowe chunki do Qdrant, ale stare zostaną. Po tygodniu masz 3 wersje tej samej umowy w bazie. Model nie wie którą wybrać.

Rozwiązanie: hash dokumentu.

Na początku workflow oblicz MD5 hash pliku. Sprawdź w Qdrant czy istnieje punkt z tym fileId i tym hashem. Jeśli tak — pomiń, nic się nie zmieniło. Jeśli nie — najpierw usuń wszystkie punkty z tym fileId, potem dodaj nowe.

W n8n: Code Node na początku oblicza hash, HTTP Request do Qdrant API sprawdza istnienie, If Node decyduje co dalej.

---

## SEGMENT 5: Query Pipeline — jak pytać mądrze (1:55 – 2:25)

`[KAMERA]`

Mamy bazę wiedzy. Czas zbudować drugą stronę — Query Pipeline.

### 5.1 Similarity Search

`[DEMO n8n]`

Workflow #2 zaczyna się od triggera. Może to być Slack Event (użytkownik pisze wiadomość do bota), Webhook od aplikacji webowej, Email Trigger — cokolwiek.

Pytanie użytkownika idzie do node "OpenAI Embeddings". Zamieniamy pytanie w wektor.

Następnie "Qdrant Vector Store — Retrieve". Tutaj konfigurujemy:

- Query: pytanie użytkownika (zostanie automatycznie zembedowane)
- Top K: 5 (pobierz 5 najbardziej podobnych chunków)
- Score Threshold: 0.75

Ten próg 0.75 to granica relevantności. Poniżej — nie wysyłamy do AI. Zamiast tego — fallback do użytkownika.

### 5.2 Reranking (opcjonalny)

`[SLAJD]`

Top-5 z similarity search nie zawsze jest idealnie posortowane. Cosine similarity to dobry ale niedoskonały wskaźnik trafności.

Reranker to osobny model — cross-encoder — który patrzył na parę (pytanie, chunk) i mówi: jak dobrze ten chunk odpowiada na to pytanie?

Zmienia kolejność z: chunk1=0.87, chunk2=0.85... na: chunk3=0.96 (wygrał!), chunk1=0.88...

W n8n możesz użyć Cohere Rerank API — proste HTTP Request. Warte zachodu kiedy masz ponad 1000 pytań dziennie i priorytet to precyzja.

### 5.3 Generowanie odpowiedzi z cytatami

`[KAMERA]`

Teraz serce systemu — instrukcja dla AI.

Kluczowy element: system prompt który WYMUSZA cytowanie i ZAKAZUJE zmyślania:

"Jesteś asystentem firmowym. Odpowiadaj WYŁĄCZNIE na podstawie poniższych fragmentów dokumentów. Każde stwierdzenie faktyczne zakończ przypisem: [Źródło: nazwa pliku, str. numer]. Jeśli odpowiedź nie wynika z dostarczonych fragmentów — napisz dokładnie: 'Nie znalazłem tej informacji w dostępnych dokumentach.' NIE uzupełniaj wiedzą własną."

Trzy zasady: WYŁĄCZNIE na podstawie fragmentów, ZAWSZE cytuj źródło, ZAWSZE powiedz "nie wiem" gdy brak informacji.

`[DEMO]`

Podaję retrieved chunki do AI Message node. Format:

```
[FRAGMENT 1]
Plik: Umowa_Acme_2025.pdf | Strona: 8 | Indeks: 45
Tekst: "Termin płatności wynosi 21 dni od daty wystawienia faktury VAT..."

[FRAGMENT 2]
Plik: Umowa_Acme_2025.pdf | Strona: 8 | Indeks: 46
Tekst: "Odsetki za opóźnienie: 0.5% wartości faktury za każdy dzień..."
```

Uruchamiam. AI odpowiada:

"Zgodnie z umową z Acme Corp (Umowa_Acme_2025.pdf, §4.2, str. 8): termin płatności wynosi **21 dni** od daty faktury [Źródło: Umowa_Acme_2025.pdf, str. 8]. Za opóźnienie naliczane są odsetki w wysokości 0,5% dziennie [Źródło: Umowa_Acme_2025.pdf, str. 8]."

`[PAUZA]`

Porównaj z tym co dostałeś od ChatGPT bez RAG. Różnica jest fundamentalna.

---

## SEGMENT 6: Eliminacja Halucynacji i Ewaluacja (2:25 – 2:55)

### 6.1 Confidence scores i fallback

`[KAMERA]`

Muszę powiedzieć o fallbacku. To jest element który odróżnia "zabawkę" od "narzędzia do pracy".

Kiedy similarity search zwraca maksymalny score 0.58 — żaden z chunków nie jest naprawdę relevantny. Co robisz?

Zły system: wysyła te chunki do AI mimo wszystko. AI generuje "odpowiedź" na podstawie niepowiązanych fragmentów. Użytkownik dostaje bzdurę.

Dobry system: sprawdza score przed wysłaniem do AI. Jeśli max score < 0.65 — zwróć komunikat: "Nie znalazłem tej informacji w dostępnych dokumentach firmowych. Spróbuj przeformułować pytanie lub skontaktuj się z [dział@firma.pl]."

W n8n: Code Node po Retrieve oblicza max_score, If Node decyduje czy iść do AI czy do fallback message.

Brzmi prosto? Tak, bo jest proste. Ale 80% systemów RAG w produkcji nie ma tego mechanizmu. I przez to generują halucynacje właśnie dla pytań spoza zakresu.

### 6.2 Ewaluacja — jak mierzyć czy RAG działa

`[SLAJD: RAGAS]`

Ostatni temat — ewaluacja. Jak wiesz że Twój RAG działa dobrze?

Masz intuicję: "wydaje się że odpowiada poprawnie". Ale intuicja to za mało.

Potrzebujesz **test datasetu** — 20-50 pytań z oczekiwanymi odpowiedziami. Napisz je raz, uruchom raz na tydzień lub przy każdej zmianie systemu.

Cztery metryki które mierzysz:

**Context Precision** — czy chunki które pobrałeś są relevantne? Jeśli pobierasz 5 chunków a 2 są nie na temat — masz precision 60%.

**Context Recall** — czy pobrałeś WSZYSTKIE relevantne chunki? Jeśli w bazie były 4 relevantne chunki ale znalazłeś 3 — recall wynosi 75%.

**Answer Faithfulness** — czy odpowiedź AI wynika z chunków? Czy model wymyślił coś czego nie było w fragmentach?

**Answer Relevance** — czy odpowiedź odpowiada na pytanie? Czy model zmienił temat?

Narzędzie: RAGAS (pip install ragas) — automatyczna ewaluacja z pomocą LLM-as-judge. Możesz uruchamiać z n8n przez Execute Command node albo przez HTTP API.

### 6.3 n8n Vector Store Nodes — live demo insert i query

`[SLAJD 32]`

Zanim zamkniemy temat — pokażę wam w n8n dokładnie jak wyglądają te node'y od środka. Żeby nie było żadnych niespodzianek kiedy sami budujecie.

`[DEMO: n8n — otwórz nowy workflow, wyszukaj w palecie "Vector Store"]`

Trzy node'y w kategorii AI → Vector Stores → Qdrant:

**Vector Store: Insert** — wkładasz wektory. Używasz przy ingestion. Konfigurujesz: collection name, content (tekst chunka), metadata (obiekt JSON), embedding model.

**Vector Store: Retrieve** — pobierasz podobne wektory. Używasz przy query. Konfigurujesz: query (pytanie użytkownika), topK, score threshold, filtry.

**Vector Store: Query** — insert i retrieve w jednym. Do szybkich testów w konsoli. Nie do produkcji.

`[DEMO: pokaż konfigurację Insert Node — zaznacz każde pole]`

```
Node: Qdrant Vector Store (Insert)
────────────────────────────────────────
Credential:   Qdrant API (http://localhost:6333)
Collection:   company_knowledge
Content:      {{ $json.text }}
Metadata:
  {
    "fileName":     "{{ $json.fileName }}",
    "fileId":       "{{ $json.fileId }}",
    "page":         {{ $json.pageNumber }},
    "chunkIndex":   {{ $json.chunkIndex }}
  }
Embedding:    OpenAI Embeddings → text-embedding-3-small
```

`[DEMO: Execute Node z pojedynczym chunkiem — pokaż wynik i dashboard Qdrant]`

Widzisz? Node zwraca ID punktu który właśnie wstawił. Otwieram Qdrant Dashboard — kolekcja company_knowledge, punkt pojawił się z wektorem i metadanymi. Tak to wygląda od środka.

`[DEMO: pokaż konfigurację Retrieve Node]`

```
Node: Qdrant Vector Store (Retrieve)
────────────────────────────────────────
Collection:      company_knowledge
Query:           {{ $json.userQuestion }}
Top K:           5
Score Threshold: 0.75
Return Fields:   text, fileName, page, chunkIndex
```

`[DEMO: Execute z pytaniem "warunki płatności" — pokaż 5 zwróconych chunków z score]`

Pięć chunków, każdy z score cosine similarity. Najwyższy score = najbliższy semantycznie do pytania. Score 0.91 — bardzo trafne. Score 0.76 — jeszcze przydatne. Gdyby były poniżej 0.75 — nie wróciłyby, bo mamy threshold.

To właśnie idzie do AI jako kontekst.

### 6.4 Koszty — 100 dokumentów, 1000 pytań miesięcznie

`[SLAJD 29]`

`[KAMERA]`

Szybko o kosztach, bo to pytanie które zawsze pada.

100 dokumentów, 20 stron każdy, ~300 tokenów na stronę.
To daje 600 000 tokenów do embeddowania przy ingestion.

Model `text-embedding-3-small`: $0.02 za milion tokenów.
600K tokenów × $0.02/1M = **$0.012. Dosłownie grosz. Jednorazowo.**

Storage: Qdrant self-hosted — $0 (VPS masz już dla n8n). Qdrant Cloud free tier — do miliona wektorów gratis.

Miesięcznie, 1000 pytań użytkowników:

- Embed pytań: 1000 × 50 tokenów × $0.02/1M = **$0.001** (nic)
- GPT-4o generation: 1000 × 1500 tokenów = 1.5M × $5/1M = **$7.50**

**Total: ~$7.50/miesiąc** za asystenta który zna całą bazę wiedzy firmy i odpowiada w 3 sekundy z cytatami.

`[SLAJD 30]`

A co przy różnych skalach? Tabela dla GPT-4o-mini (20x tańszy od GPT-4o, 80% jakości):

| Skala | Dokumenty | Pytań/mies. | Koszt/mies. |
|-------|-----------|-------------|-------------|
| Freelancer / startup | 50 | 200 | ~$0.20 |
| Mała firma | 200 | 1 000 | ~$1.00 |
| Średnia firma | 500 | 5 000 | ~$5.00 |
| Enterprise | 5 000 | 50 000 | ~$45 |

*Zakłada text-embedding-3-small + GPT-4o-mini*

`[KAMERA]`

7,5 dolara — a nawet 40 centów przy GPT-4o-mini — za asystenta który zna całą bazę wiedzy firmy, odpowiada w 3 sekundy, cytuje źródła i nigdy nie zmyśla.

Pytanie nie brzmi "czy to się opłaca". Pytanie brzmi "kiedy zaczynam".

---

## OUTRO — Projekt Tygodnia i Zadanie Domowe (3:05 – 3:15)

`[SLAJD 36]`

`[KAMERA]`

Dobra. Masz RAG. Masz Qdrant. Masz dwa workflow — ingestion i query. Masz embeddingi, chunking, source citations, fallback, ewaluację, koszty.

Teraz projektujesz.

**Projekt tygodnia: Firmowy Asystent Wiedzy.**

Kroki:

1. Uruchom Qdrant lokalnie przez Docker. Jedna komenda — nie ma wymówki.
2. Stwórz folder na Google Drive z 5 dokumentami testowymi. Możesz użyć własnych — regulamin pracy, oferta handlowa, FAQ, cennik, cokolwiek.
3. Zbuduj Workflow #1 — Ingestion Pipeline. Drive trigger → Extract text → Code Node chunker → Loop → OpenAI Embeddings → Qdrant Insert.
4. Zbuduj Workflow #2 — Query Pipeline. Webhook lub Slack trigger → Embed pytanie → Qdrant Retrieve → Code Node format → AI Agent z system promptem cytowania → odpowiedź z cytatem.
5. Przetestuj: zadaj 5 pytań które mają odpowiedź w dokumentach. I 2 pytania których NIE ma — sprawdź czy fallback działa.

Kryterium sukcesu: AI odpowiada z cytatem i numerem strony dla pytań z dokumentów, i zwraca fallback message dla pytań spoza zakresu.

Szczegóły kroków są w pliku Ćwiczenia.

`[KAMERA]`

**Zadanie domowe — dla tych co chcą iść dalej:**

Dodaj incremental updates z hash trickiem. Zmień jeden dokument na Drive — workflow powinien automatycznie usunąć stare chunki i wgrać nowe. Zero duplikatów. Kto to zrobi — zostaw komentarz na platformie, sprawdzę i dam feedback osobiście.

[PYTANIE do widzów: Gdzie u Ciebie w firmie albo u klienta jest największy "stóg siana" — dokumenty których nikt nie czyta ale które mają krytyczną wiedzę?]

Wrzuć na Discordzie. Ciekaw co zobaczycie.

---

**Tydzień 8:** RAG + Agenci. Asystent który nie tylko *wie* — ale też *działa*. Wysyła maile, aktualizuje CRM, tworzy zadania w Jirze, rezerwuje spotkania. Na podstawie wiedzy z dokumentów. Największy moduł kursu.

Jeśli po tym tygodniu zrobiłeś jedno — zbuduj ten Knowledge Assistant dla własnych dokumentów. Własnych, nie klienta. Rozumienie od środka to najlepsze przygotowanie do wdrożenia u klienta za tygodnie.

Do zobaczenia w Tygodniu 8.

---

*Skrypt: ~3200 słów | Czas nagrania: ~3h 15min z demami i pauzami*
*Segmenty: 6 głównych + Outro | Liczba slajdów w skrypcie: 36 (zgodne z Prezentacją)*
