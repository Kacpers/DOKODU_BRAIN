---
type: kurs-materialy
modul: 01
tytuł: Fundamenty n8n i Pierwsza Automatyzacja
czas_całkowity: 3h 00min
segmentów: 12
created: 2026-03-27
status: gotowe-do-nagrania
---

# Tydzień 1: Fundamenty n8n i Pierwsza Automatyzacja — Plan Nagrania

**Łączny czas:** ~3 godziny
**Projekt tygodnia:** Lead Capture System
**Format:** 12 segmentów po 10–20 minut, przemienne teoria/DEMO

---

## Segmenty

---

### Segment 01 — Witaj w n8n (TEORIA)
**Czas:** 00:00 – 00:12 (12 min)
**Cel:** Ustawić kontekst, pokazać co zbudujesz do końca tygodnia, rozgrzać uczestnika.

**Co pokazujesz na ekranie:**
- Slajd tytułowy z logo n8n
- Gotowy Lead Capture System działający w n8n (end result preview — raz uruchomiony, żeby uczestnik wiedział dokąd zmierza)
- Slajd: "Czym n8n NIE jest" vs "Czym n8n JEST"

**Kluczowe punkty:**
- n8n = automat biznesowy, nie zabawka
- Self-hosted vs cloud — co wybrać i dlaczego
- Co zbudujesz w tym tygodniu (Lead Capture System, live demo)
- Czego NIE będziemy robić: nie omawiamy każdego node'a z listy — uczysz się przez budowanie

**Typ:** TEORIA

---

### Segment 02 — Instalacja i Środowisko (DEMO)
**Czas:** 00:12 – 00:27 (15 min)
**Cel:** Uczestnik ma działające n8n na lokalnej maszynie lub w chmurze.

**Co pokazujesz na ekranie:**
- Terminal: `docker compose up -d` (Docker Compose dla n8n)
- Przeglądarka: pierwsze logowanie do n8n (localhost:5678)
- Szybki tour po interfejsie: menu boczne, przycisk "New Workflow"
- Slajd: wymagania systemowe, Docker vs Railway vs n8n Cloud

**Kluczowe punkty:**
- Docker Compose to gold standard — pokazujesz `docker-compose.yml` z wolumenem
- Dla uczestników bez Dockera: n8n Cloud trial (14 dni za darmo)
- Pierwsze hasło, pierwsza konfiguracja — timezone, email
- Zakładki które warto mieć otwarte: n8n docs, forum n8n community

**Typ:** DEMO
**Pliki pomocnicze:** `docker-compose.yml` z wolumenem na dane

---

### Segment 03 — Anatomia Workflowu (TEORIA + DEMO)
**Czas:** 00:27 – 00:42 (15 min)
**Cel:** Uczestnik rozumie canvas, nodes, connections, executions panel — budulce każdego workflowu.

**Co pokazujesz na ekranie:**
- Slajd: Anatomia node'a (input, output, ustawienia, strzałki)
- n8n canvas: tworzysz prosty 3-nodowy workflow (Manual Trigger → Set → NoOp)
- Panel boczny node'a: zakładki Parameters, Settings, Notes
- Executions panel: co to jest, skąd się bierze, jak czytać logi

**Kluczowe punkty:**
- Node = jeden krok procesu (jak klocek LEGO)
- Connection = rura między klockami
- Każdy node ma: wejście (items), wyjście (items), ustawienia
- Execution = jedno uruchomienie całego workflowu
- Różnica: Workflow vs Execution vs Node Run

**Typ:** TEORIA + DEMO

---

### Segment 04 — Triggery: Kiedy Workflow Startuje (TEORIA + DEMO)
**Czas:** 00:42 – 00:57 (15 min)
**Cel:** Uczestnik zna trzy główne triggery i wie kiedy użyć którego.

**Co pokazujesz na ekranie:**
- Slajd: mapa triggerów (Manual / Schedule / Webhook / App triggers)
- DEMO Manual Trigger: klikasz "Test workflow", widzisz wynik
- DEMO Schedule Trigger: ustawiasz "co 5 minut", pokazujesz cron expression
- DEMO Webhook Trigger: kopiujesz URL, wysyłasz curl z terminala, widzisz dane

**Kluczowe punkty:**
- Manual = do testowania, nigdy w produkcji jako jedyny trigger
- Schedule = raporty, synchronizacje nocne, cykliczne zadania
- Webhook = reaktywny (coś się dzieje → workflow startuje) — najważniejszy dla agencji
- Webhook ma dwa tryby: Test URL vs Production URL — WAŻNA różnica
- Trigger zawsze daje dane do pierwszego node'a

**Typ:** TEORIA + DEMO

---

### Segment 05 — Kluczowe Nodes: Zestaw Startowy (TEORIA + DEMO)
**Czas:** 00:57 – 01:17 (20 min)
**Cel:** Uczestnik umie korzystać z 6 podstawowych nodes, które wystarczą do 80% zadań.

**Co pokazujesz na ekranie:**
- Slajd: lista 6 nodes + jedno zdanie co robi każdy
- DEMO każdego node'a w miniaturowym workflowu:
  - **HTTP Request** — pobierasz dane z publicznego API (JSONPlaceholder)
  - **Set** — zmieniasz/dodajesz pola do danych
  - **IF** — rozgałęziasz przepływ (warunek true/false)
  - **Switch** — wielokrotne rozgałęzienie (jak switch-case)
  - **Code** — JavaScript inline, gdy inne nodes nie wystarczą
  - **NoOp** — "zaślepka", do debugowania i placeholderów

**Kluczowe punkty:**
- HTTP Request to "szwajcarski scyzoryk" — łączy się z 99% API
- Set NIE zastępuje danych — możesz wybrać "Keep Only Set" lub nie
- IF daje dwa wyjścia: `true` i `false` — oba mogą być podłączone
- Code node: używaj tylko gdy musisz — każda linia JavaScript = dług techniczny
- NoOp = "nic nie rób" — przydatny do zrozumienia przepływu

**Typ:** TEORIA + DEMO

---

### Segment 06 — Credential Vault: Klucze API Bezpiecznie (TEORIA + DEMO)
**Czas:** 01:17 – 01:32 (15 min)
**Cel:** Uczestnik rozumie jak n8n przechowuje sekrety i umie dodać credential.

**Co pokazujesz na ekranie:**
- Slajd: mapa typów credentiali (API Key, Basic Auth, OAuth2, Header Auth)
- Slajd: jak n8n szyfruje dane (AES-256, N8N_ENCRYPTION_KEY)
- DEMO: dodajesz credential typu "Header Auth" (np. do fikcyjnego API)
- DEMO: podłączasz credential do HTTP Request node'a
- Pokazujesz że credential nie jest widoczny w danych po uruchomieniu

**Kluczowe punkty:**
- Credentials są szyfrowane — nawet backup bazy danych nie ujawnia kluczy
- N8N_ENCRYPTION_KEY musisz zapisać w bezpiecznym miejscu (utrata = brak dostępu)
- API Key vs Header Auth vs Basic Auth — kiedy co
- OAuth2 = "zaloguj się przez Google/Slack" — n8n robi to automatycznie
- Nigdy nie wklejaj kluczy bezpośrednio w Expression (`={{...}}`)

**Typ:** TEORIA + DEMO

---

### Segment 07 — Error Handling: Workflow Który Nie Pada (TEORIA + DEMO)
**Czas:** 01:32 – 01:52 (20 min)
**Cel:** Uczestnik umie obsługiwać błędy i wie jak zbudować workflow który informuje o problemach.

**Co pokazujesz na ekranie:**
- Slajd: flow diagram error handling (Try/Catch → Error Branch → Powiadomienie)
- DEMO: budujesz workflow z HTTP Request który celowo failuje (zły URL)
- DEMO: dodajesz "Continue on Fail" w Settings node'a
- DEMO: budujesz Error Trigger Workflow (oddzielny workflow łapie błędy)
- DEMO: wysyłasz email/Slack gdy coś się posypie

**Kluczowe punkty:**
- Domyślnie: jeden błąd = cały workflow pada
- "Continue on Fail" = ignoruj błąd, idź dalej (ostrożnie — ukrywa problemy)
- Error Trigger Workflow = dedykowany workflow na błędy (gold standard)
- Zawsze testuj ścieżkę błędu — Murphy's Law działa w automatyzacji podwójnie
- Loguj błędy: minimum timestamp + który node + jaka wiadomość błędu

**Typ:** TEORIA + DEMO

---

### Segment 08 — Debugowanie: Znajdź Błąd w 2 Minuty (TEORIA + DEMO)
**Czas:** 01:52 – 02:07 (15 min)
**Cel:** Uczestnik umie efektywnie debugować workflow używając narzędzi n8n.

**Co pokazujesz na ekranie:**
- DEMO: Execution Log — czytasz co poszło nie tak (czerwony node)
- DEMO: Pin Data — "zamrażasz" dane na wejściu node'a do testowania
- DEMO: "Test Step" — uruchamiasz pojedynczy node bez całego workflowu
- DEMO: Console.log w Code node — podgląd zmiennych
- Slajd: 5-krokowy przepis na debugowanie

**Kluczowe punkty:**
- Zawsze zacznij od Execution Log — tam jest odpowiedź w 90% przypadków
- Pin Data = game changer dla testowania (nie musisz uruchamiać całego workflowu)
- "Test Step" działa tylko jeśli poprzedni node ma pinned data lub był uruchomiony
- Sprawdzaj typ danych: string vs number vs boolean — to źródło połowy bugów
- Dodaj tymczasowy "Set" node żeby podejrzeć co jest w danych

**Typ:** TEORIA + DEMO

---

### Segment 09 — Projekt: Lead Capture System — Architektura (TEORIA)
**Czas:** 02:07 – 02:17 (10 min)
**Cel:** Uczestnik rozumie co zbuduje i dlaczego tak a nie inaczej.

**Co pokazujesz na ekranie:**
- Slajd: flow diagram Lead Capture (ASCII diagram z pliku 05_Workflow_Blueprint.md)
- Slajd: lista nodes których użyjemy i dlaczego
- Pokazujesz przykładowy payload który przyjdzie z formularza
- Slajd: wymagania środowiskowe (Google Sheets ID, Gmail credential, Slack webhook)

**Kluczowe punkty:**
- Omawiasz decyzje architektoniczne: dlaczego Google Sheets nie baza SQL
- Walidacja przed zapisem — nie zapisuj śmieci
- Deduplikacja: sprawdzasz email bo formularz można wysłać dwa razy
- Error handling już na etapie projektu, nie "na koniec"

**Typ:** TEORIA

---

### Segment 10 — Projekt: Budujemy Część 1 — Webhook + Walidacja (DEMO)
**Czas:** 02:17 – 02:35 (18 min)
**Cel:** Uczestnik ma działający webhook z walidacją danych.

**Co pokazujesz na ekranie:**
- Tworzysz nowy workflow od zera
- Dodajesz Webhook Trigger, kopiujesz URL
- Testujesz za pomocą curl/Postman
- Dodajesz IF node do walidacji emaila (wyrażenie regularne)
- Dodajesz IF node do sprawdzania wymaganych pól
- Pokazujesz ścieżkę błędu walidacji (odpowiedź 400 do formularza)

**Typ:** DEMO (budowanie na żywo)

---

### Segment 11 — Projekt: Budujemy Część 2 — Sheets + Email + Slack (DEMO)
**Czas:** 02:35 – 02:52 (17 min)
**Cel:** Uczestnik ma kompletny Lead Capture System działający end-to-end.

**Co pokazujesz na ekranie:**
- HTTP Request do Google Sheets API: sprawdzasz czy email już istnieje (deduplikacja)
- Google Sheets node: zapisujesz nowy lead
- Gmail node: wysyłasz email powitalny (szablon z imienną personalizacją)
- Slack node: powiadomienie dla zespołu (#leady channel)
- Testujesz cały flow od początku do końca z prawdziwymi danymi

**Typ:** DEMO (budowanie na żywo)

---

### Segment 12 — Projekt: Error Handling + Podsumowanie Tygodnia (DEMO + TEORIA)
**Czas:** 02:52 – 03:00 (8 min)
**Cel:** Domknięcie projektu, zadanie domowe, podsumowanie.

**Co pokazujesz na ekranie:**
- Dodajesz Error Trigger Workflow (email do admina gdy coś padnie)
- Pokazujesz gotowy workflow z perspektywy — canvas z opisanymi nodes
- Slajd: co umiemy po tygodniu 1
- Slajd: co będzie w tygodniu 2 (API i Dane — HTTP Request w głąb)

**Kluczowe punkty:**
- Recap: triggery, nodes, credentials, error handling, debugowanie
- Zadanie domowe: rozszerz Lead Capture o filtrowanie spamu
- Gdzie szukać pomocy: forum n8n.io, dokumentacja, Discord Dokodu

**Typ:** DEMO + TEORIA

---

## Podsumowanie czasowe

| Segment | Czas | Typ | Czas trwania |
|---------|------|-----|--------------|
| 01 Witaj w n8n | 00:00 | TEORIA | 12 min |
| 02 Instalacja | 00:12 | DEMO | 15 min |
| 03 Anatomia Workflowu | 00:27 | TEORIA+DEMO | 15 min |
| 04 Triggery | 00:42 | TEORIA+DEMO | 15 min |
| 05 Kluczowe Nodes | 00:57 | TEORIA+DEMO | 20 min |
| 06 Credential Vault | 01:17 | TEORIA+DEMO | 15 min |
| 07 Error Handling | 01:32 | TEORIA+DEMO | 20 min |
| 08 Debugowanie | 01:52 | TEORIA+DEMO | 15 min |
| 09 Architektura Projektu | 02:07 | TEORIA | 10 min |
| 10 Projekt cz.1 | 02:17 | DEMO | 18 min |
| 11 Projekt cz.2 | 02:35 | DEMO | 17 min |
| 12 Error Handling + Recap | 02:52 | DEMO+TEORIA | 8 min |
| **RAZEM** | | | **~180 min** |

---

## Wskazówki nagraniowe

- Nagraj segmenty 9–12 w jednej sesji (projekt musi być ciągły)
- Segmenty 1–8 możesz nagrywać osobno
- Przed nagraniem każdego DEMO: zresetuj stan n8n (usuń test executions)
- Trzymaj terminal otwarty obok n8n — przyda się do curl testów
- Miej gotowe w schowku: przykładowy JSON payload, URL formularza testowego
