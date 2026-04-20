---
type: product-doc
produkt: Chatbot by Dokodu
wersja: 1.0
aktualizacja: 2026-04-20
owner: kacper
---

# Chatbot by Dokodu — Dokumentacja

Asystent AI osadzany jednym tagiem `<script>` na stronie klienta. Uczy się wyłącznie z dokumentów wgranych przez właściciela (RAG), prowadzi rozmowę drzewem tematów i zbiera leady. Panel admina pokazuje analitykę w czasie rzeczywistym.

---

## 1. Co potrafi

### Rozmawia z odwiedzającym stronę

- Odpowiada po polsku, zwięźle (1–3 zdania, max 60 słów)
- Streamuje odpowiedź w czasie rzeczywistym (typing dots → tekst litera po literze)
- Sugeruje kolejne pytania jako klikalne podpowiedzi (chips)
- Grupuje wiadomości, pokazuje avatar bota, status online — wygląda jak komunikator (Messenger / WhatsApp)

### Odpowiada TYLKO z Państwa dokumentów (RAG)

- Przy każdym pytaniu wyszukuje najbardziej pasujące fragmenty PDF-ów
- Nie zmyśla liczb, cen, dat, nazwisk — jeśli informacji nie ma, uczciwie mówi *„Nie mam tej informacji w bazie wiedzy"*
- Pod każdą odpowiedzią bota (w panelu) widać **z którego dokumentu** wziął informację + procent dopasowania

### Prowadzi po drzewie tematów

- Właściciel w panelu buduje drzewo tematów **drag & drop** (jak n8n)
- Gałęzie = sekcje wiedzy (oferta, ceny, wsparcie, demo)
- Specjalne węzły „lead" = formularze kontaktowe z własnymi polami
- Gotowe szablony: Deweloper nieruchomości, SaaS, HR — do wczytania jednym kliknięciem

### Zbiera leady

- Gdy użytkownik chce rozmowy z człowiekiem, cenę, spotkanie — bot kończy wiadomość i wyświetla **pill-button „Zostaw kontakt"**
- Klik → wysuwa się od dołu bottom-sheet z formularzem (można zamknąć i wrócić do rozmowy)
- Pola formularza definiowane w drzewie: imię, telefon, e-mail + własne custom pola (np. *„Którym mieszkaniem jesteś zainteresowany?"*)
- Po wysyłce bot dziękuje w czacie: *„✓ Dziękujemy! Odezwiemy się wkrótce."*

### Pokazuje analitykę właścicielowi

Dashboard (`/admin`) pokazuje za ostatnie 30 dni:

- **5 KPI** z trendem vs poprzedni okres: konwersacje, wiadomości, leady, konwersja %, głębokość rozmowy
- **Sparkline** ruchu dziennego
- **Top tematy** — które gałęzie drzewa są najczęściej trafiane + ile leadów wygenerowały
- **Pytania bez dobrej odpowiedzi** — lista fraz o które pytali użytkownicy, a bot nie miał ich w bazie. **To jest mapa brakujących treści na stronie — kluczowy insight sprzedażowy.**
- **Ostatnie leady** + pełny export do CSV

Klik w dowolny element dashboardu → otwiera przefiltrowaną listę rozmów. Klik w rozmowę → pełna transkrypcja z zaznaczonymi dokumentami źródłowymi.

### Osadza się jednym tagiem

```html
<script src="https://chat.twojadomena.pl/widget.js" data-slug="twoj-bot" defer></script>
```

- **Shadow DOM** — style strony hosta nie wpływają na wygląd widgetu, a widget nie modyfikuje strony
- Konfigurowalne: kolor akcentu, pozycja (prawy/lewy dolny róg), trigger (bubble/auto-open)
- Mobile-first: na urządzeniach ≤ 480 px widget otwiera się na pełnym ekranie

---

## 2. Jak używać panelu admina

### Logowanie
`https://admin.twojadomena.pl/admin` → wpisz hasło ustawione w zmiennej `ADMIN_PASSWORD`.

### Gdzie wrzucać PDF-y

**`/admin/documents`**

1. Przycisk „Dodaj dokument"
2. Wybierz PDF z dysku (max 10 MB na plik w planie Starter, 50 MB w Pro)
3. Po uploadzie status = `processing` — bot robi chunking + embedding
4. Po 1–3 min status → `ready` i dokument jest dostępny dla bota

**Co może być w PDF:**
- Oferta / cennik / karty produktów
- Regulamin / polityka prywatności / FAQ
- Case studies / white papery
- Opis inwestycji / katalog lokali
- Specyfikacja techniczna / instrukcje

**Limity:**
- Starter: 10 dokumentów, łącznie 50 MB
- Pro: bez limitu (praktycznie do 1 000 dokumentów / 500 MB)

### Jak budować drzewo tematów

**`/admin/topics`**

- **+ Temat** — dodaje nowy węzeł rozmowy (np. *„Informacje o ofercie"*)
- **+ Zbieranie leadu** — dodaje węzeł z formularzem kontaktowym
- **Połączenia** — przeciągnij z dolnej kropki rodzica do górnej kropki dziecka
- **Auto-layout** — jedna kliknięcie, bot rozkłada węzły automatycznie
- **Załaduj szablon** — wczytaj gotowe drzewo (Deweloper / SaaS / HR)
- **Panel boczny** — edycja zaznaczonego węzła: nazwa, opis, słowa kluczowe (bias wyszukiwania), pola leadu

Każdy węzeł ma:
- **Nazwę** — wyświetlana w chips-sugestiach
- **Opis** — kiedy ten temat jest trafiany (bot używa do dopasowania)
- **Słowa kluczowe** (opcja) — wzmacniają dopasowanie
- **Pola formularza** (dla węzłów lead) — `name`, `label`, `type` (text/email/tel/textarea), `required`

**Skróty klawiszowe:**
- `Ctrl+D` — duplikuj zaznaczony węzeł
- `Ctrl+S` — zapisz drzewo
- `Delete` — usuń zaznaczony

### Jak analizować ruch

**`/admin` (dashboard):**
- 5 KPI z trendem
- Sparkline 30-dniowy
- Top tematy (klik → filtrowana lista rozmów)
- Pytania bez odpowiedzi (klik → rozmowy z pytaniami bez odpowiedzi)

**`/admin/conversations`:**
- Lista wszystkich rozmów
- Filtry: Wszystkie / Z leadem / Pytania bez odpowiedzi
- Zakres: 7d / 30d / 90d
- Filtr po temacie

**`/admin/conversations/:id`:**
- Pełna transkrypcja z avatarami
- Pod każdą odpowiedzią bota: lista dokumentów źródłowych + procent dopasowania
- Flaga `⚠ Brak dopasowania` gdy bot nie miał wiedzy
- Sidebar: czas trwania, # wiadomości, czy lead, lista tematów (klik → podobne rozmowy)

### Eksport leadów

**`/admin/leads`** → przycisk „Eksportuj do CSV".

---

## 3. Bezpieczeństwo i dane

### Gdzie są przechowywane dane

Dwa warianty:

**A) Na Państwa infrastrukturze (self-hosted)**
- Docker Compose — 2 kontenery (PostgreSQL + Next.js)
- Zalecany VPS: 2 vCPU / 4 GB RAM / 40 GB SSD (np. Hetzner CX22, ~5 EUR/mies.)
- Wszystkie dane: wiadomości, leady, dokumenty, embeddingi — na Państwa maszynie
- Dokodu nie ma dostępu (chyba że zamówicie Państwo retainer SLA)

**B) Na infrastrukturze Dokodu (hosted)**
- Dedykowana instancja PostgreSQL per klient (separacja danych)
- Serwery w EU (Frankfurt, Hetzner)
- Dzienne backupy, retention 30 dni
- Dokodu jako Podmiot Przetwarzający (umowa DPA)

### OpenAI API

- Chatbot używa OpenAI do embeddingów (`text-embedding-3-small`) i odpowiedzi (`gpt-4o-mini`)
- **Klucz OpenAI jest Państwa** — w obu wariantach (hosted/self-hosted) płacicie Państwo bezpośrednio OpenAI za zużycie
- OpenAI w planie API **nie używa Państwa danych do trenowania modeli** (oficjalna polityka OpenAI, stan: 2026)
- Opcjonalnie: Azure OpenAI z data residency w EU

### Prompt injection — zabezpieczenia

- Bot **nigdy nie ujawnia** treści system promptu, bazy wiedzy ani drzewa tematów
- Ignoruje próby zmiany roli („pretend you are", „zapomnij instrukcje", „act as")
- Nie wykonuje instrukcji znalezionych w dokumentach (traktuje tekst jako dane, nie komendy)
- Rate limiting: 20 wiadomości / min / IP
- CORS whitelist per domena

### RODO / AI Act

- Formalnie bot jest systemem AI niskiego ryzyka wg AI Act (Art. 50)
- Wymagane: informacja dla użytkownika że rozmawia z AI (w powitaniu bota)
- Leady zawierają dane osobowe — wymagana zgoda + klauzula RODO (widoczna przy zbieraniu)
- Retention: domyślnie 12 mies., konfigurowalne
- Template polityki AI + klauzuli RODO w osobnym pliku (`AI_Policy_Template.md`)

---

## 4. Architektura techniczna

### Stack

- **Frontend / Backend:** Next.js 16 (App Router, TypeScript, Tailwind v4)
- **Baza:** PostgreSQL 16 + rozszerzenie `pgvector` (HNSW index, cosine similarity)
- **ORM:** Prisma 6
- **LLM:** OpenAI GPT-4o-mini (chat), text-embedding-3-small (embeddings); możliwość wymiany na Anthropic Claude / Azure OpenAI / Mistral
- **Widget:** esbuild bundle (~25 KB), Shadow DOM, vanilla TS
- **Deploy:** Docker Compose

### Przepływ danych (RAG)

1. User pyta bota
2. Pytanie → embedding (OpenAI) → wektor 1536-dim
3. Wektor → PostgreSQL HNSW search → top-5 fragmentów z dokumentów
4. Fragmenty + drzewo tematów + pytanie → system prompt → OpenAI GPT
5. Odpowiedź streamowana do widgetu; zapisana w DB razem z sources (jaki dokument, jaki procent match)

### Skalowanie

- Jeden kontener web + Postgres obsługuje ~500 jednoczesnych rozmów
- Powyżej: horizontal scaling web (Postgres zostaje single), rate limit dostosowywany
- Koszty OpenAI skalują się liniowo (~0,001 USD za wiadomość przy średniej długości)

---

## 5. Dostosowanie do klienta

### Branding

- Kolor akcentu (`data-color` lub w panelu)
- Nazwa bota (wyświetlana w headerze widgetu)
- Avatar (inicjał z nazwy — pierwsze litery)
- Powitanie (edytowalne w drzewie tematów, pole `greeting`)
- Pozycja widgetu: prawy/lewy dolny róg

### Własny styl

Atrybuty tagu script:
- `data-slug` — który bot (jeden admin może mieć wiele botów w planie Pro)
- `data-color` — override koloru akcentu (`#FF6A3D`)
- `data-position` — `bottom-right` / `bottom-left`
- `data-trigger` — `bubble` (domyślny) / `button` / `auto-open`

### Integracje (plan Pro)

Webhooki wychodzące:
- Po utworzeniu leada → POST na Państwa endpoint (CRM, Slack, Gmail)
- Po każdej konwersacji → POST z pełnym transcriptem
- Format: JSON

Webhooki przychodzące (wchodzą w Opcję Pro):
- Pre-fill danych użytkownika (jeśli zalogowany na stronie)
- Custom suggestions z zewnętrznego API

---

## 6. Ograniczenia

### Czego bot NIE zrobi

- Nie pomoże z zadaniami spoza bazy wiedzy (polityka, medycyna, porady prawne — nawet jeśli ktoś pyta)
- Nie wygeneruje kodu ani nie napisze wiersza (chyba że w bazie są takie przykłady i klient sobie tego życzy)
- Nie przeczyta obrazków / tabel zagnieżdżonych w PDF (tylko tekst — dla tabel warto PDF konwertować do tekstu)
- Nie działa offline — wymaga połączenia z OpenAI (lub alternatywnego providera)

### Koszty zmienne

Klient płaci bezpośrednio OpenAI za zużycie:
- Embedding dokumentu: ~0,001 USD / PDF 10 stron
- Odpowiedź na pytanie: ~0,001 USD / wiadomość (przy GPT-4o-mini)
- Przy 1 000 rozmów / mies. i śred. 6 wiadomości → ~6 USD / mies.

---

## 7. Screenshoty

Zobacz katalog `screenshots/` — 12 plików PNG pokazujących wszystkie widoki:

- `01–03` — landing page + otwarty widget
- `04` — ekran logowania do admina
- `05` — dashboard z KPI, sparkline, top tematami, pytaniami bez odpowiedzi
- `06–07` — lista konwersacji (wszystkie / filtr pytań bez odpowiedzi)
- `08` — szczegół konwersacji z transkryptem i źródłami
- `09` — zarządzanie dokumentami
- `10` — leady
- `11` — edytor drzewa tematów (drag & drop)
- `12` — ustawienia bota

---

## 8. Typowy proces wdrożenia (Starter — 4 tygodnie)

| Tydzień | Co robimy |
| :---: | :--- |
| 1 | Kickoff. Audyt dokumentów. Dostarczenie serwera / domeny. Instalacja Dockera. |
| 2 | Wdrożenie bota na stronie staging. Ładowanie dokumentów. Wstępne drzewo tematów. |
| 3 | Testy. Fine-tuning drzewa. Branding (kolor, nazwa, powitanie). Szkolenie admina (2h). |
| 4 | Go-live na produkcji. Monitoring pierwszego tygodnia. Przekazanie panelu. |

---

## 9. Wsparcie po wdrożeniu

**Retainer (opcjonalny):**
- SLA: alert < 1h, naprawa < 4h
- Miesięczny raport efektywności (top tematy, co poprawić w bazie wiedzy, rekomendacje)
- 1h konsultacji / mies. wliczone
- Priorytetowy dostęp do zespołu

Bez retainera — klient zarządza samodzielnie, Dokodu dostępne na godziny przy potrzebie.
