---
name: daily-briefing
description: Codzienny briefing dla Kacpra — skanuje Reddit + HackerNews, krzyżuje z leadami Pracuj i danymi SEO, generuje temat na film YT (15 min, jeden take), pomysły na Shorts, blog post idea i sygnały leadowe. Trigger: "co na dziś", "zaczynamy dzień", "daily briefing", "dzień dobry", "rano", /daily-briefing
---

# Instrukcja: Daily Briefing — Content Radar

Codziennie rano Kacper pyta "co na dziś". Odpowiadasz jednym briefingiem z tematem na film, shortsami, blogiem i leadami.

## Flow

### 0. Sprawdź świeżość danych analitycznych

Zanim zaczniesz — sprawdź czy dane GSC, GA4 i YouTube są aktualne (cron mógł nie zadziałać jeśli WSL był wyłączony):

```bash
# Sprawdź datę "Pobrano:" w plikach sync
head -2 ~/DOKODU_BRAIN/20_AREAS/AREA_Blog_SEO/SEO_Last_Sync.md
head -2 ~/DOKODU_BRAIN/20_AREAS/AREA_Blog_SEO/GA_Last_Sync.md
head -2 ~/DOKODU_BRAIN/20_AREAS/AREA_YouTube/YT_Last_Sync.md
```

Jeśli którykolwiek plik jest starszy niż 24h (GSC/GA4) lub 7 dni (YouTube) — **odpal sync w tle** równolegle z resztą:

```bash
# GSC (jeśli stare >24h)
python3 ~/DOKODU_BRAIN/scripts/gsc_fetch.py --days 28 --save

# GA4 (jeśli stare >24h)
python3 ~/DOKODU_BRAIN/scripts/ga_fetch.py --days 28 --save

# YouTube (jeśli stare >7 dni, lub poniedziałek)
python3 ~/DOKODU_BRAIN/scripts/youtube_fetch.py --save
```

Nie czekaj na zakończenie synców — odpowiedz Kacprowi od razu z danymi które masz (Reddit/HN + stare synce). Gdy synce się skończą, uzupełnij briefing o aktualne dane.

### 0.5. Pobierz kalendarz z OBU kont Google

**KRYTYCZNE** — bez tego zaproponujesz nagrywanie na dzień z warsztatem od 9:00.

Pobierz wydarzenia na dziś + jutro + najbliższe 7 dni z **wszystkich kalendarzy**:

**Konto kacper@dokodu.it** — przez Cloud MCP Calendar:
```
gcal_list_events(calendarId="primary", timeMin="DZIŚ", timeMax="+7 dni")
gcal_list_events(calendarId="c_b27c1b0b637a314c3b94cccb15fffef29efda3ef3f94c4a0eac61532c8a213f6@group.calendar.google.com", ...)  # Rezerwacje - Konsultacje
```

**Konto ksieradzinski@gmail.com** — przez API z tokenem `~/.gmail-mcp/credentials.json`:
```python
# Token wygasa — ZAWSZE rób refresh przed zapytaniem!
# Kalendarze do sprawdzenia:
# - primary (ksieradzinski@gmail.com) — prywatne przypomnienia
# - k.sieradzinski@aihero.pl — SZKOLENIA AI Hero (FOTC, Growth Advisors, DSH)
# - "Dokodu - akcje" (20a8cd86...) — akcje Dokodu
# - "Familijne" (family07240...) — sprawy rodzinne
# - "Dzieci" (2qc2lcd1...) — sprawy dzieci
```

```python
import json, requests
from pathlib import Path

creds_path = Path.home() / '.gmail-mcp/credentials.json'
oauth_path = Path.home() / '.gmail-mcp/gcp-oauth.keys.json'
creds = json.loads(creds_path.read_text())
oauth = json.loads(oauth_path.read_text())
client_info = oauth.get('installed', oauth.get('web', {}))

# Refresh token
resp = requests.post('https://oauth2.googleapis.com/token', data={
    'client_id': client_info['client_id'],
    'client_secret': client_info['client_secret'],
    'refresh_token': creds['refresh_token'],
    'grant_type': 'refresh_token'
})
new_token = resp.json()['access_token']
creds['access_token'] = new_token
creds_path.write_text(json.dumps(creds))

# Pobierz z każdego kalendarza
calendars = {
    'Prywatny': 'ksieradzinski@gmail.com',
    'AI Hero': 'k.sieradzinski@aihero.pl',
    'Dokodu akcje': '20a8cd86fd13303182c55b034bc9ae8194783399b96765caedfe827a45373914@group.calendar.google.com',
    'Familijne': 'family07240530149553983419@group.calendar.google.com',
    'Dzieci': '2qc2lcd1f7uvqvir3j7tedf3ls@group.calendar.google.com',
}
for name, cal_id in calendars.items():
    r = requests.get(f'https://www.googleapis.com/calendar/v3/calendars/{cal_id}/events',
        headers={'Authorization': f'Bearer {new_token}'},
        params={'timeMin': '...', 'timeMax': '...', 'singleEvents': True, 'orderBy': 'startTime', 'timeZone': 'Europe/Warsaw'})
    # ...wyświetl wydarzenia
```

**Zasady planowania dnia:**
- Szkolenia AI Hero = typowo 09:00–~16:00 (cały dzień zajęty, NIE sugeruj nagrywania!)
- BNI = cały dzień
- Developerskie synchra = 16:00 (1h)
- Jeśli dzień ma warsztat od 9:00 → sugeruj taski tylko na wieczór lub inny dzień

### 1. Zbierz dane (równolegle)

Odpal **równolegle** przez Bash (+ kalendarz z kroku 0.5):

```bash
# Reddit — top 24h z 16 subredditów
python3 ~/DOKODU_BRAIN/scripts/reddit_scout.py --no-comments --min-score 15

# HackerNews — top 100 stories
python3 ~/DOKODU_BRAIN/scripts/hn_scout.py --no-comments
```

Jednocześnie wczytaj przez Read:
- `DOKODU_BRAIN/PLAN_TYGODNIA.md` — zadania na dziś + rytuały
- `DOKODU_BRAIN/20_AREAS/AREA_YouTube/YT_Videos.md` — co już jest w pipeline (nie powtarzaj)
- Najnowszy `DOKODU_BRAIN/20_AREAS/AREA_Marketing_Sales/Leads_Pracuj_*.csv` lub `Raport_Prospecting_Pracuj_*.md` — sygnały leadowe
- `DOKODU_BRAIN/20_AREAS/AREA_Blog_SEO/SEO_Ideas_Bank.md` — istniejące pomysły na posty (nie duplikuj)
- `DOKODU_BRAIN/20_AREAS/AREA_Blog_SEO/SEO_Last_Sync.md` — frazy z GSC (krzyżuj z Reddit tematami)
- `DOKODU_BRAIN/20_AREAS/AREA_Blog_SEO/GA_Last_Sync.md` — ruch na blogu, bounce rate, źródła

### 2. Wybierz temat na film

Kryteria wyboru (w kolejności priorytetu):
1. **Viralowość** — score + komentarze na Reddit/HN (im więcej, tym bardziej potwierdzony temat)
2. **Dokodu relevance** — high relevance = bezpośrednio o n8n/automatyzacji/AI w firmach
3. **Pokazywalność** — da się pokazać coś na ekranie (n8n workflow, kod, narzędzie, stronę)
4. **Hostinger fit** — czy da się naturalnie wspomnieć self-hosted n8n na VPS
5. **Lead gen** — czy temat rezonuje z firmami ICP (produkcja, logistyka, finanse 50-500 prac.)
6. **Świeżość** — temat z ostatnich 24h ma przewagę nad starszym

Wybierz JEDEN temat na film. Daj 2-3 alternatywy gdyby główny nie podchodził.

### 3. Generuj briefing

Format odpowiedzi (DOKŁADNIE ten format, nie zmieniaj):

```
═══════════════════════════════════════════════
DAILY BRIEFING — [DATA] ([dzień tygodnia])
═══════════════════════════════════════════════

🎬 FILM NA DZIŚ (15 min, jeden take, OBS)
─────────────────────────────────────────

Temat: [tytuł filmu — jak Kacper powiedziałby to na YT]
Źródło: [r/subreddit lub HN] — [score] upvotes, [komentarze] komentarzy
Link: [URL do posta]

Co mieć otwarte na ekranie:
  1. [tab/okno 1 — np. post na Reddit]
  2. [tab/okno 2 — np. n8n.dokodu.it z workflow]
  3. [tab/okno 3 — np. strona narzędzia]

Gadaj o:
  • [bullet 1 — co pokazać/powiedzieć]
  • [bullet 2]
  • [bullet 3]
  • [bullet 4 opcjonalnie]

Lokowanie Hostingera: [jedno zdanie jak naturalnie wpleść]

CTA: [co widz ma zrobić — link w opisie, subskrypcja, komentarz]

Alternatywy (gdyby główny nie podchodził):
  1. [temat 2] — źródło, dlaczego dobry
  2. [temat 3] — źródło, dlaczego dobry

🩳 SHORTS (nagraj przy okazji)
─────────────────────────────

  1. [Tytuł shorta] — [źródło, score] — [co pokazać w 30-60s]
  2. [Tytuł shorta] — [źródło, score] — [co pokazać]
  3. [Tytuł shorta] — [źródło, score] — [co pokazać]

📝 BLOG POST IDEA
─────────────────

Temat: [tytuł artykułu — SEO friendly]
Źródło: [Reddit/HN post który to inspiruje]
Potencjał SEO: [fraza z GSC jeśli się pokrywa, albo "nowa fraza do zbadania"]
Następny krok: `/seo-plan-post` żeby zrobić pełny brief

🎯 LEAD SIGNAL
──────────────

[Krzyżowanie Reddit tematów z leadami Pracuj — np.]
  • [Firma X] szuka [stanowisko] — dziś mówisz o [temat] który pasuje → wyślij im link
  • Na r/[subreddit] ktoś pyta o [temat] — rozważ komentarz z linkiem do kanału
[Lub: "Brak sygnałów leadowych dziś" jeśli nic nie pasuje]

📬 SKRZYNKA (ważne emaile)
──────────────────────────

[Sprawdź Gmail MCP — nieprzeczytane od klientów/leadów z ostatnich 24h]
  • [Nadawca] — [temat] — [czy wymaga akcji dziś?]
[Lub: "Czysto — brak pilnych emaili"]

📊 PIPELINE HEALTH
──────────────────

[Z CRM_Leady_B2B.md + Outreach_Tracker.md:]
  • Leadów w pipeline: [X] | Czekają na follow-up: [X]
  • Propozycje bez odpowiedzi: [X] (najstarsza: [X] dni)
  • Najbliższy deadline: [projekt/klient] — [data]
[Gdy CRM Notion będzie gotowy — dane stąd zamiast z plików MD]

⏰ PRZYPOMNIENIA
────────────────

[Z REMINDERS.md — co jest na dziś i jutro]
  • [przypomnienie 1]
  • [przypomnienie 2]
[Lub: "Brak przypomnień na dziś"]

📋 PLAN DNIA
────────────

[Zadania z PLAN_TYGODNIA.md na dzisiejszy dzień tygodnia]
[+ przeniesione z wczoraj jeśli niezrobione]
[+ spotkania/calle wpisane w ten dzień]
[+ follow-upy outreach do wysłania (dzień 3/10/21)]

⚠️ INICJATYWA DO PCHNIĘCIA
───────────────────────────

[Która inicjatywa z PLAN_TYGODNIA jest najbardziej zaniedbana/zablokowana?]
[Np. "Kurs n8n — skrypt VSL blokuje cały pipeline, deadline za 5 dni. Dzisiaj poświęć 2h."]
```

### 4. Co z czym zrobić — mapa downstream actions

Każdy element briefingu ma jasne przeznaczenie i następny krok. Podpowiadaj Kacprowi co dalej.

| Element briefingu | Przeznaczenie | Następny krok (skill/akcja) | Gdzie trafia wynik |
|---|---|---|---|
| 🎬 **Film YT** | YouTube — budowa kanału + lokowanie Hostingera + lead gen | Kacper nagrywa → daje plik → `/yt-transcribe` → napisy + opis + tagi → publikacja 20:30 | `YT_Videos.md` (dodaj wpis), `movies/YT-XXX/publish/` |
| 🩳 **Shorts** | YouTube Shorts — viralowość, zasięg | Kacper nagrywa przy okazji głównego filmu | `YT_Videos.md` |
| 📝 **Blog post idea** | Blog dokodu.it — SEO, ruch organiczny, lead gen z Google | `/seo-plan-post` → brief → `/blog-draft` → draft → `/blog-publish` | `SEO_Ideas_Bank.md` → blog API |
| 🎯 **Lead signal (firma)** | Outreach B2B — kontakt z konkretną firmą z Pracuj | `/outreach` → DM LinkedIn → cold email dzień 3 → follow-up dzień 10 | `CRM_Leady_B2B.md`, `Outreach_Tracker.md` |
| 🎯 **Lead signal (Reddit)** | Community presence — odpowiedź na Reddit z linkiem do kanału/bloga | Kacper odpowiada ręcznie (nie automatyzuj!) | — |
| 📬 **Gmail check** | Nie przegap ważnego emaila od klienta/leada | Jeśli wymaga odpowiedzi → `/brain-draft-email` | Draft w Gmail (nigdy nie wysyłaj!) |
| 📊 **Pipeline health** | Kontrola czy nic nie gnije w pipeline B2B | Jeśli propozycja >5 dni bez odpowiedzi → follow-up `/outreach` | `CRM_Leady_B2B.md`, `Outreach_Tracker.md` |
| ⏰ **Przypomnienia** | Spotkania, calle, deadliny z REMINDERS.md | Jeśli call dziś → `/brain-prep-call` przygotuj strategię | `REMINDERS.md`, PLAN_TYGODNIA |
| 📊 **GSC data** | SEO monitoring — pozycje, CTR, impressions | Jeśli coś spadło → `/seo-stats` → optymalizacja strony → `/blog-publish` update | `SEO_Insights.md` |
| 📊 **GA4 data** | Ruch na stronie — bounce rate, źródła, konwersje | Jeśli wysoki bounce → sprawdź stronę → poprawki UX/treści | `GA_Insights.md` |
| 📊 **YouTube data** | Metryki kanału — retention, CTR, najlepsze filmy | Raz w tygodniu → `/yt-stats` → wnioski do produkcji | `YT_Insights.md` |
| 📋 **Outreach follow-up** | Pipeline B2B — systematyczny kontakt z firmami | `/outreach` → kolejny krok w sekwencji (DM → email → follow-up → call) | `Outreach_Tracker.md` |
| ⚠️ **Inicjatywa do pchnięcia** | Najbardziej zaniedbany priorytet z PLAN_TYGODNIA | Zaproponuj konkretny 2h blok na dziś | PLAN_TYGODNIA |
| 🔮 **CRM (Notion)** | *PLACEHOLDER — po postawieniu CRM* | Sprawdź statusy dealów, follow-upy, pipeline value | CRM Notion |

#### Schemat dnia:

```
RANO (8:00)
  Briefing → Kacper wybiera temat → nagrywa film (8:00–9:00)

DZIEŃ (9:00–17:00)
  Zadania z PLAN DNIA:
  - Blog: jeśli blog idea zatwierdzona → `/seo-plan-post` → `/blog-draft`
  - Outreach: `/outreach` → kolejne firmy lub follow-upy
  - Leady: jeśli lead signal → `/brain-draft-email` lub DM LinkedIn
  - SEO: jeśli dane GSC pokazują problem → `/seo-stats` → fix
  - Kurs/projekty: zadania z backlogu tygodnia

WIECZÓR (20:00)
  Kacper daje plik nagrania → `/yt-transcribe` → opis + tagi → publikacja 20:30
```

#### Gdy Kacper mówi "zróbmy X z briefingu":

- "ten blog post" → odpal `/seo-plan-post` z tematem z sekcji 📝
- "ten lead" → odpal `/outreach` lub `/brain-draft-email` z firmą z sekcji 🎯
- "nagraj to" → potwierdź temat, dodaj do `YT_Videos.md` jako POMYSŁ
- "opublikuj" → odpal `/yt-transcribe` jeśli ma plik, potem opis/tagi
- "co z SEO" → odpal `/seo-stats` z najnowszymi danymi

### 5. Ważne zasady

- **Nie generuj scenariusza** — Kacper nagrywa bez promptera, potrzebuje tylko bullet pointy
- **Jeden film = jeden temat** — nie łącz 3 tematów w jeden film
- **Pokaż źródło** — Kacper zaczyna film od "Widziałem dziś na Reddicie..." lub "Na HackerNews jest gorący temat..."
- **Nie powtarzaj tematów** — sprawdź YT_Videos.md czy już nie nagrywał czegoś podobnego
- **Lokowanie Hostingera musi być naturalne** — nie wciskaj na siłę jeśli temat nie pasuje
- **Shorts to bonus** — jeśli nic dobrego na short, daj 1-2 zamiast na siłę 3
- **Blog post idea musi mieć potencjał SEO** — nie pisz o newsie który za tydzień będzie nieaktualny
- **Gmail: NIGDY nie wysyłaj emaili** — tylko pokaż co przyszło. Draft przez `/brain-draft-email`.

### 6. Auto-capture spotkań i pierdół

Gdy Kacper mówi coś w stylu "jutro o 10 mam rozmowę z Alkiem", "w czwartek call z Animex", "przypomnij mi o fakturze" — **natychmiast**:

1. **Wpisz do PLAN_TYGODNIA.md** w odpowiedni dzień (przelicz datę na absolutną!)
2. **Wpisz do REMINDERS.md** z datą absolutną
3. **Potwierdź jednym zdaniem:** "Wpisałem: wtorek 31.03 10:00 — rozmowa z Alkiem"

Nie pytaj "czy mam to zapisać?" — po prostu zapisz. Kacper bez tego zapomni.

Jeśli spotkanie jest z klientem/leadem — dodatkowo:
- Sprawdź czy jest profil w `AREA_Customers/` → jeśli tak, dodaj do `Meetings.md`
- Rano w dniu spotkania zaproponuj `/brain-prep-call` żeby przygotować strategię

### 7. Po nagraniu

Gdy Kacper da plik nagrania → zaproponuj `/yt-transcribe` do generowania napisów + opisu + tagów na publikację o 20:30.
