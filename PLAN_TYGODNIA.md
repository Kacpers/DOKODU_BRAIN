---
type: plan
status: active
week: 2026-03-30 → 2026-04-04
last_updated: 2026-03-29
---

# Plan Tygodnia — 30 marca – 4 kwietnia 2026

---

## INICJATYWY — ciągłe cele (nie zadania, a kierunki)

Gdy Kacper pyta "co robimy?" → sprawdź która inicjatywa ma najwyższy priorytet i zaproponuj konkretny następny krok.

### 🔴 1. LAUNCH KURSU N8N (deadline: 6 maja)
**Cel:** Przedsprzedaż kursu n8n + AI, 200 kursantów × 599 PLN
**Stan:** Skrypt VSL = blokada #1. Platforma = niezadecydowana. Emaile = gotowe. Prezentacje = gotowe.
**Następny krok:** Skrypt VSL → nagranie → strona sprzedażowa → webinar → launch
**Skill:** —

### 🟡 2. PROSPECTING B2B (ciągły)
**Cel:** 2-4 discovery calls tygodniowo z firm ICP
**Stan:** 30 firm Score A zakwalifikowanych, Outreach Kit gotowy, skrypt Pracuj.pl działa
**Następny krok:** LinkedIn outreach do kolejnych 5 firm → follow-up → cold email → call
**Skill:** `/outreach` — prowadzi krok po kroku, pyta tylko o imię osoby z LinkedIn
**Odświeżanie:** Co tydzień `python3 scripts/pracuj_leads.py --save` → nowe firmy

### 🟡 3. SEO CONTENT MACHINE (ciągły)
**Cel:** +500 kliknięć/mies. z bloga, artykuły celujące w ICP
**Stan:** Meta title wdrożone (3 strony), brief artykułu gotowy, artykuł o automatyzacji istnieje ale rankuje słabo
**Następny krok:** Optymalizacja istniejących artykułów → nowe artykuły pod commercial intent
**Skill:** `/seo-stats` → `/seo-plan-post` → `/blog-draft` → `/blog-publish`

### 🟢 4. ANIMEX → UPSELL (jednorazowy)
**Cel:** Z jednorazowego szkolenia zrobić stałego klienta (konsultacje, kolejne szkolenia, wdrożenie)
**Stan:** Szkolenie zakończone, ankiety 4.81/5, case study gotowy
**Następny krok:** Follow-up call → propozycja kontynuacji
**Skill:** `/brain-draft-email` do napisania maila, case study w `Case_Study_Animex_2026.md`

### 🟢 5. BUDOWA MARKI (ciągły, tło)
**Cel:** LinkedIn profil + lead magnet + newsletter = pipeline inbound
**Stan:** LinkedIn optimization gotowy, AI Act Checklist gotowy, newsletter brief gotowy
**Następny krok:** Zaktualizuj profil LinkedIn → wrzuć lead magnet na stronę → pierwszy newsletter
**Skill:** `/newsletter-check` przed wysyłką

---

## CODZIENNIE — rytuały powtarzane każdego dnia roboczego

*Ta sekcja nie zmienia się z tygodnia na tydzień. Claude odpala ją automatycznie gdy Kacper zaczyna dzień.*

### ☀️ Rano (8:00–9:00) — "co na dziś"

Claude robi automatycznie (skill `/daily-briefing`):
1. **Data sync check** — sprawdza świeżość GSC, GA4, YouTube. Jeśli stare → odpala sync w tle
2. **Content Radar** — odpala `reddit_scout.py` + `hn_scout.py`, krzyżuje z leadami Pracuj + SEO + GA → daje:
   - 🎬 **Film YT** na dziś (15 min, jeden take, OBS) — temat, co mieć na ekranie, bullet pointy, lokowanie Hostingera
   - 🩳 **Shorts** (2-3 pomysły)
   - 📝 **Blog post idea** (z potencjałem SEO)
   - 🎯 **Lead signal** (Reddit × Pracuj — jeśli temat dnia pasuje do firmy z pipeline)
3. **Plan dnia** — zadania z harmonogramu poniżej + przeniesione z wczoraj
4. **Outreach check** — follow-upy do wysłania (dzień 3 po DM = cold email, dzień 10 = follow-up)

Kacper nagrywa film 8:00–9:00, reszta dnia wg planu.

### 🌙 Wieczór (20:00–20:30) — publikacja

Kacper daje plik nagrania → Claude odpala `/yt-transcribe` (Whisper) → generuje:
- Napisy SRT
- Opis YouTube + tagi
- Post LinkedIn (opcjonalnie)

Publikacja o 20:30.

---

## BACKLOG — cele do zrealizowania w tym tygodniu

*Nie przypisane do godziny. Przesuwamy na bieżąco z backlogu do dnia.*

### P1 — Must do
- [ ] **Skrypt VSL kursu n8n** — 800-1100 słów gotowego tekstu do nagrania (deadline: 31.03!)
- [ ] **Animex follow-up** — zadzwoń/napisz: podziękuj za szkolenie, zapytaj o dalsze konsultacje. Draft case study: `Case_Study_Animex_2026.md`
- [ ] **LinkedIn Outreach — 5 firm** — `/outreach` (VTS, Rossmann, Capital Service, UNIQA, Media Expert). Przed: zaktualizuj profil wg `LinkedIn_Profile_Optimization.md`

### P2 — Should do
- [ ] **MailerLite: wklej treść 3 maili** — z `Emaile_Launch.md` do MailerLite Drafts
- [ ] **SEO: sprawdź meta title** — n8n + list-comprehension + wdrozenie-ai (wdrożone 29.03 noc)
- [ ] **Blog: zoptymalizuj /blog/wdrozenie-ai-w-firmie** — przebuduj pod "automatyzacja AI dla firm"
- [ ] **Blog: nowy artykuł /blog/automatyzacja** — brief: `Brief_Automatyzacja_Dla_Firm_2026-03-29.md`
- [ ] **Lead magnet: AI Act Checklist** — MD → PDF, wrzuć na stronę z bramką emailową

### P3 — Nice to have
- [ ] **n8n MCP: podepnij + screenshoty do slajdów** — wygeneruj API Key (n8n.dokodu.it → Settings → n8n API), podaj Claude'owi → skonfiguruje MCP, zaimportuje 3 workflow JSON, zrobi screenshoty
- [ ] **Slidev: review prezentacji Modul_01** — po screenshotach, sprawdź layouty i wizualizacje
- [ ] **Outreach: kolejne 5 firm** — `/outreach` (VW FS, CUK, PZU, Scania, ENEA)
- [ ] **Odśwież leady** — `python3 scripts/pracuj_leads.py --save`
- [ ] **Cold email** do firm z LinkedIn (3 dni po DM)
- [ ] **Dashboard review** — zaktualizuj 000_DASHBOARD.md, sprawdź status Corleonis

---

## Poniedziałek 30.03

- [ ] 9:00–11:30 — Deep Work: Skrypt VSL kursu n8n
- [ ] 11:30–12:00 — Dashboard review
- [ ] 12:00–12:30 — Animex follow-up
- [ ] 13:00–14:00 — LinkedIn Outreach — 5 firm
- [ ] 14:00–14:30 — SEO: sprawdź meta title
- [ ] 14:30–15:00 — MailerLite: wklej 3 maile

## Wtorek 31.03

*Uzupełnij na koniec poniedziałku — co nie weszło + nowe.*

## Środa 01.04

## Czwartek 02.04

## Piątek 03.04

- [ ] **Weekly Review** — `/brain-weekly-review`
- [ ] **SEO Weekly** — `/seo-weekly`
- [ ] **Plan następnego tygodnia**

---

## Zrobione w weekend (29.03)

- [x] GSC + GA4 sync + GA Insights + SEO Insights
- [x] Meta title /blog/n8n + list-comprehension — wdrożone
- [x] Meta title /blog/wdrozenie-ai-w-firmie — optymalizacja
- [x] 158 leadów zakwalifikowanych → `Lead_Qualification_Full_2026-03-29.md`
- [x] Outreach Kit top 5 firm + Outreach Tracker
- [x] Skill `/outreach` z buying signals
- [x] Skrypt `pracuj_leads.py`
- [x] LinkedIn Profile Optimization
- [x] AI Act Checklist lead magnet
- [x] MailerLite cleanup (11 pustych draftów usunięte)
- [x] 3 emaile kursu n8n → `Emaile_Launch.md`
- [x] Slidev: Vue wizualizacje, animacje, Key Takeaway + Exercise layouts
- [x] Case Study Animex draft
- [x] PLAN_TYGODNIA.md + memory

---

## Metryki sukcesu tygodnia

- [ ] Skrypt VSL gotowy do nagrania
- [ ] 5 zaproszeń LinkedIn wysłanych
- [x] 3 meta title wdrożone
- [ ] 3 emaile wklejone w MailerLite
- [ ] 1 rozmowa z Animex o kontynuacji
- [ ] Profil LinkedIn zaktualizowany
