---
type: kurs-materialy
modul: 02
tytuł: "Tydzień 2: Język Sieci, API i Transformacje Danych"
czas_całkowity: "2h 05min"
format: nagranie + ćwiczenia
last_updated: 2026-03-27
---

# Agenda — Tydzień 2: Język Sieci, API i Transformacje Danych

> **Dla prowadzącego:** Nagrasz 6 segmentów, edytor skleja w jeden film. Każdy segment kończy się cliffhangerem do następnego — kursant ma powód, żeby nie wyłączać.

---

## SEGMENT 1 — HTTP: Gramatyka Internetu (12 min)

**Cel:** Kursant rozumie czym są metody HTTP i dlaczego ma to znaczenie w n8n.

| Czas | Co robisz | Typ |
|------|-----------|-----|
| 0:00–1:30 | Hook: "Każde API to rozmowa. Jeśli mówisz 'GET' kiedy trzeba powiedzieć 'POST', API cię zignoruje." | TEORIA |
| 1:30–4:00 | Slajd: HTTP Methods cheatsheet (GET/POST/PUT/DELETE/PATCH) — analogia do CRUD w magazynie | SLAJD |
| 4:00–6:00 | Slajd: Headers — Content-Type, Authorization, Accept, custom headers | SLAJD |
| 6:00–10:00 | DEMO: HTTP Request node w n8n — GET do `https://jsonplaceholder.typicode.com/users/1`, pokaż request/response w lewym panelu | DEMO |
| 10:00–12:00 | DEMO: Zmień na POST, dodaj body JSON, pokaż różnicę w zachowaniu | DEMO |

**Ekran podczas DEMO:**
- n8n Canvas → HTTP Request node
- Lewy panel: zakładka "Input" i "Output"
- Pokaż nagłówki odpowiedzi (F12 nie — tylko n8n)

---

## SEGMENT 2 — HTTP Response Codes: Kod Błędu to nie Koniec Świata (10 min)

**Cel:** Kursant potrafi obsłużyć błędy API zamiast się ich bać.

| Czas | Co robisz | Typ |
|------|-----------|-----|
| 0:00–2:00 | Slajd: Mapa kodów HTTP (2xx/4xx/5xx) — analogia do sygnalizacji świetlnej | SLAJD |
| 2:00–5:00 | DEMO: Celowo wywołaj 404 (złe ID), 401 (brak Authorization), 429 (za dużo requestów — symulacja) | DEMO |
| 5:00–8:00 | DEMO: Error handling w n8n — "Continue On Error", IF node po HTTP Request, sprawdzenie `$response.statusCode` | DEMO |
| 8:00–10:00 | Teoria: Rate limiting — dlaczego API cię banuje i jak to obejść (Wait node, batch size) | TEORIA |

**Ekran podczas DEMO:**
- HTTP Request → Settings → "Continue On Error: true"
- IF node: `{{ $json.error }}` exists
- Pokaż obie ścieżki (success/error) w Canvas

---

## SEGMENT 3 — JSON Mastery: Twoje Dane Mają Strukturę (18 min)

**Cel:** Kursant biegle czyta i pisze JSON, rozumie tablice vs obiekty.

| Czas | Co robisz | Typ |
|------|-----------|-----|
| 0:00–3:00 | Slajd: JSON jako szafa z szufladami — wyjaśnienie przez analogię | SLAJD |
| 3:00–6:00 | Slajd: Obiekty `{}` vs tablice `[]` — kiedy co i dlaczego to ważne w n8n | SLAJD |
| 6:00–10:00 | DEMO: n8n Expression Editor — wpisz ręcznie JSON, pokaż podgląd na żywo | DEMO |
| 10:00–14:00 | DEMO: Zagnieżdżone JSON — `$json.company.address.city`, opcjonalne chainowanie `?.` | DEMO |
| 14:00–18:00 | DEMO: Tablica użytkowników z JSONPlaceholder — jak wejść w każdy element, `.map()`, `.filter()` w Expression Editor | DEMO |

**Ekran podczas DEMO:**
- Expression Editor w n8n (ikona `{}` przy polu)
- Live preview po prawej stronie editora
- Kolorowanie składni — pokaż różnicę string vs number vs null

---

## SEGMENT 4 — n8n Expressions: Twój Szwajcarski Scyzoryk (20 min)

**Cel:** Kursant zna wszystkie kluczowe zmienne n8n i umie je łączyć.

| Czas | Co robisz | Typ |
|------|-----------|-----|
| 0:00–3:00 | Slajd: n8n Expressions reference card — `$json`, `$items()`, `$node`, `$now`, `$workflow`, `$execution` | SLAJD |
| 3:00–7:00 | DEMO: `$json` — podstawowe użycie, różnica między `$json.field` a `{{ $json.field }}` | DEMO |
| 7:00–11:00 | DEMO: `$node["NazwaNode"].json` — pobieranie danych z wcześniejszego node'a | DEMO |
| 11:00–15:00 | DEMO: `$now` i manipulacja datami — `.toISO()`, `.minus({days: 7})`, formatowanie | DEMO |
| 15:00–18:00 | DEMO: `$items()` — kiedy masz wiele itemów i chcesz agregować | DEMO |
| 18:00–20:00 | Tip: Expression Debugger — jak sprawdzić co expression zwraca zanim zapiszesz workflow | TEORIA |

**Ekran podczas DEMO:**
- Workflow z 3 nodami: Trigger → Set → HTTP Request
- Expression Editor otwarty — wpisuj na żywo
- Pokaż "Formula mode" vs "Text mode"

---

## SEGMENT 5 — Code Node i Vibe Coding: Kiedy Expressions Nie Wystarczą (22 min)

**Cel:** Kursant wie kiedy i jak używać Code Node oraz jak współpracować z AI przy pisaniu kodu.

| Czas | Co robisz | Typ |
|------|-----------|-----|
| 0:00–3:00 | Teoria: Code Node — kiedy go używasz (logika biznesowa, transformacje niemożliwe w Expressions, zewnętrzne biblioteki) | TEORIA |
| 3:00–5:00 | Slajd: Vibe Coding flow — AI → kod → testuj → n8n | SLAJD |
| 5:00–10:00 | DEMO: Otwórz ChatGPT/Copilot, wpisz prompt: "Napisz funkcję n8n Code Node która..." — skopiuj, wklej, przetestuj | DEMO |
| 10:00–15:00 | DEMO: Praktyczny przykład — Code Node normalizujący numer NIP (usuwa myślniki, spacje, waliduje długość) | DEMO |
| 15:00–19:00 | DEMO: Pętla przez items w Code Node — `for (const item of $input.all())` pattern | DEMO |
| 19:00–22:00 | Tip: Debugging Code Node — `console.log()` i gdzie to znaleźć w n8n (Execution Log) | DEMO |

**Ekran podczas DEMO:**
- ChatGPT w przeglądarce + n8n obok (split screen)
- Code Node: zakładka JavaScript, "Test Step" button
- Execution Log (lewy panel → Executions)

---

## SEGMENT 6 — Transformacje Danych: Set, Item Lists i Pagination (15 min)

**Cel:** Kursant potrafi reshapować dane i obsłużyć paginację API.

| Czas | Co robisz | Typ |
|------|-----------|-----|
| 0:00–4:00 | DEMO: Set node — dodaj pole, zmień nazwę, usuń pole, mapuj z innego node'a | DEMO |
| 4:00–8:00 | DEMO: Item Lists — Split (jeden item → wiele), Aggregate (wiele → jeden), Merge | DEMO |
| 8:00–12:00 | DEMO: Pagination w HTTP Request node — "Return All" vs manual pagination, `nextPage` token | DEMO |
| 12:00–15:00 | Teoria: Kiedy paginacja zabija flow — timeouty, limit rozmiaru, strategia "fetch → store → process" | TEORIA |

**Ekran podczas DEMO:**
- Set node: tryby "Manual Mapping" i "JSON Output"
- Item Lists: wizualizacja wejście/wyjście
- HTTP Request: zakładka "Pagination" → "Response Contains Next URL"

---

## PROJEKT TYGODNIA — Data Enrichment z GUS REGON API (28 min)

**Cel:** Kursant buduje kompletny, produkcyjny workflow krok po kroku.

| Czas | Co robisz | Typ |
|------|-----------|-----|
| 0:00–3:00 | Architektura projektu na tablicy/slajdzie — Webhook → Cache Check → GUS API → Transform → Save | SLAJD |
| 3:00–8:00 | DEMO: Webhook node + przykładowy payload `{"nip": "5213016711"}` | DEMO |
| 8:00–13:00 | DEMO: Cache check — Google Sheets "Lookup Row" sprawdza czy NIP już istnieje | DEMO |
| 13:00–20:00 | DEMO: HTTP Request do GUS REGON API (sesja SOAP) — autoryzacja, zapytanie GetFullReport | DEMO |
| 20:00–24:00 | DEMO: Code Node — parsowanie odpowiedzi XML/JSON z GUS, normalizacja pól | DEMO |
| 24:00–28:00 | DEMO: Zapis do Google Sheets + Response Webhook z danymi firmy | DEMO |

**Ekran podczas DEMO:**
- Pełny canvas z wszystkimi nodami
- Każdy node otwierany osobno i konfigurowany
- Test end-to-end: wklej NIP w Postman/Webhook.site → obserwuj flow

---

## Podsumowanie materiału (2 min)

**Co zrobiłeś w tym tygodniu:**
- HTTP methods i headers — znasz gramatykę API
- JSON — rozumiesz strukturę danych
- Expressions — masz pełen arsenał n8n
- Code Node — wiesz kiedy i jak
- Vibe Coding — AI to twój junior developer
- Transformacje — Set, Item Lists, paginacja
- Projekt: Data Enrichment z GUS API

**Co dalej (Tydzień 3):** Skalowanie — błędy, retry, monitorowanie, Sub-Workflows.

---

## Notatki produkcyjne

- **Thumbnail:** Kacper przy tablicy z diagramem HTTP request/response + logo n8n
- **Intro muzyka:** max 5 sekund, wycisz do 20% pod mówienie
- **Chaptery YouTube:** każdy segment = osobny chapter
- **Materiały do pobrania:** workflow JSON z projektu tygodnia (plik osobno)
- **CTA końcowe:** "Wrzuć swój workflow do komentarzy — dam znać co poprawić"
