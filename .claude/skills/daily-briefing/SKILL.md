---
name: daily-briefing
description: Codzienny briefing dla Kacpra — skanuje Reddit + HackerNews, krzyżuje z leadami Pracuj i danymi SEO, generuje temat na film YT (15 min, jeden take), pomysły na Shorts, blog post idea i sygnały leadowe. Trigger: "co na dziś", "zaczynamy dzień", "daily briefing", "dzień dobry", "rano", /daily-briefing
---

# Instrukcja: Daily Briefing — Content Radar

Codziennie rano Kacper pyta "co na dziś". Odpowiadasz jednym briefingiem z tematem na film, shortsami, blogiem i leadami.

**ZASADA #1: NIE PYTAJ — RÓB.** Zbierz wszystkie dane w jednym batchu tool calli i wygeneruj briefing. Zero pytań do Kacpra w trakcie zbierania danych.

## Flow

### 1. Zbierz WSZYSTKO w jednym batchu (równolegle)

Odpal WSZYSTKO naraz w jednej turze tool calli — maksymalizuj równoległość:

**Bash (równolegle):**
```bash
# Reddit — top 24h z 16 subredditów
python3 ~/DOKODU_BRAIN/scripts/reddit_scout.py --no-comments --min-score 15

# HackerNews — top 100 stories
python3 ~/DOKODU_BRAIN/scripts/hn_scout.py --no-comments

# Sync GSC/GA4/YT w tle jeśli stare (>24h GSC/GA4, >7 dni YT) — run_in_background=true
python3 ~/DOKODU_BRAIN/scripts/gsc_fetch.py --days 28 --save
python3 ~/DOKODU_BRAIN/scripts/ga_fetch.py --days 28 --save
python3 ~/DOKODU_BRAIN/scripts/youtube_fetch.py --save
```

**MCP Calendar (równolegle z Bash):**
```
list_events(calendarId="kacper@dokodu.it", startTime="DZIŚ", endTime="+7 dni", timeZone="Europe/Warsaw")
list_events(calendarId="c_b27c1b0b637a314c3b94cccb15fffef29efda3ef3f94c4a0eac61532c8a213f6@group.calendar.google.com", ...)
```

**MCP Gmail (równolegle):**
```
gmail_search_messages(q="is:unread newer_than:2d -category:promotions -category:social -category:updates", maxResults=15)
```

**Read (równolegle z powyższymi):**
- `PLAN_TYGODNIA.md` — zadania na dziś + rytuały + kalendarz
- `REMINDERS.md` — przypomnienia na dziś/jutro
- `20_AREAS/AREA_YouTube/YT_Videos.md` — pipeline (nie powtarzaj tematów)
- `20_AREAS/AREA_Blog_SEO/SEO_Ideas_Bank.md` — istniejące pomysły (nie duplikuj)
- `20_AREAS/AREA_Blog_SEO/SEO_Action_Triggers.md` — **SEO trigger logic** ("if pozycja X then akcja Y")
- `20_AREAS/AREA_Blog_SEO/SEO_Last_Sync.md` — ostatnie pozycje GSC (pobrane przez `/seo-sync`)

**SEO Triggers — sprawdzanie automatyczne:**

Dla każdego aktywnego triggera w `SEO_Action_Triggers.md`:
1. Sprawdź aktualną pozycję frazy w `SEO_Last_Sync.md` (jeśli stale >24h → odpal `python3 scripts/gsc_fetch.py --days 7 --save`)
2. Porównaj z warunkiem triggera (np. "fraza w top 20")
3. Jeśli pasuje → **dorzuć sekcję "🚨 SEO TRIGGER" do briefingu** z konkretną akcją do podjęcia

Format alertu w briefingu (przykład):
```
🚨 SEO TRIGGER ACTIVE
Fraza: claude code (33 100 vol/mc)
Pozycja: 18 (wczoraj 25)
Akcja: Boost pillara — FAQ od czytelników, 2-3 case studies, screenshot UI
Termin: 1 tydzień
Komenda: /seo-research claude code
```

Jeśli ŻADEN trigger nie pasuje → pomiń sekcję (nie pokazuj "no triggers").

**Zasady planowania dnia (nie pytaj, sam stosuj):**
- Szkolenia AI Hero / FOTC / BNI = cały dzień zajęty, NIE sugeruj nagrywania
- Developerskie synchra = 16:00 (1h)
- Jeśli dzień ma warsztat od 9:00 → sugeruj taski tylko na wieczór lub inny dzień

### 2. Wybierz temat na film i generuj briefing

Kryteria wyboru (w kolejności priorytetu):
1. **Viralowość** — score + komentarze na Reddit/HN
2. **Dokodu relevance** — n8n/automatyzacja/AI w firmach
3. **Pokazywalność** — da się pokazać na ekranie
4. **Hostinger fit** — naturalnie wpleść self-hosted VPS
5. **Lead gen** — rezonuje z firmami ICP
6. **Świeżość** — 24h > starsze

Wybierz JEDEN temat + 2 alternatywy. Format odpowiedzi:

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

### 3. Zasady

- Bullet pointy, nie scenariusz — Kacper nagrywa bez promptera
- Jeden film = jeden temat
- Nie powtarzaj tematów z YT_Videos.md
- Hostinger naturalnie albo wcale
- Shorts: 1-3, ile wyjdzie
- Blog idea musi mieć potencjał SEO (evergreen > news)
- Gmail: NIGDY nie wysyłaj emaili — tylko pokaż co przyszło

### 4. Auto-capture (nie pytaj, po prostu zapisz)

Gdy Kacper wspomni spotkanie/zadanie → od razu wpisz do PLAN_TYGODNIA.md + REMINDERS.md z datą absolutną. Potwierdź jednym zdaniem.

### 5. Po nagraniu

Kacper daje plik → zaproponuj `/yt-transcribe`.
