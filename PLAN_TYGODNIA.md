---
type: plan
status: active
week: 2026-04-07 → 2026-04-13
last_updated: 2026-04-10
---

# Plan Tygodnia — 7–13 kwietnia 2026

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
- [x] **Skrypt VSL kursu n8n** — GOTOWY, zatwierdzony 30.03 → `VSL_Skrypt_v1.md`
- [x] **Animex follow-up** — brief wysłany mailem 30.03. Czekamy na odpowiedź.
- [ ] **LinkedIn Outreach — 5 firm** — `/outreach` (VTS, Rossmann, Capital Service, UNIQA, Media Expert). Przed: zaktualizuj profil wg `LinkedIn_Profile_Optimization.md`

### P2 — Should do
- [ ] **MailerLite: wklej treść 3 maili** — z `Emaile_Launch.md` do MailerLite Drafts
- [ ] **SEO: sprawdź meta title** — n8n + list-comprehension + wdrozenie-ai (wdrożone 29.03 noc)
- [ ] **Blog: zoptymalizuj /blog/wdrozenie-ai-w-firmie** — przebuduj pod "automatyzacja AI dla firm"
- [ ] **Blog: nowy artykuł /blog/automatyzacja** — brief: `Brief_Automatyzacja_Dla_Firm_2026-03-29.md`
- [ ] **Lead magnet: AI Act Checklist** — MD → PDF, wrzuć na stronę z bramką emailową

### PYSTART — Relaunch kursu (nowa inicjatywa)

**Faza 1: Poprawki landing page (ten tydzień)**
- [x] **LP: Naprawić sprzeczność dostępu** — ujednolicone na "1 rok" wszędzie (FAQ, pricing, schema)
- [x] **LP: Dodać badge "14 dni gwarancji zwrotu"** — przy przyciskach zakupu + w hero
- [x] **LP: Wywalić kurs OpenAI Dev z LP** — usunięty z pricing section, Pystart teraz jedyny produkt na stronie
- [x] **LP: Nowy headline** — "Naucz się Pythona i buduj realne projekty — nawet jeśli nigdy nie programowałeś"
- [x] **LP: Raty widoczne przy cenie** — "lub 3 raty × 233 PLN" obok 699 PLN
- [x] **LP: Rozbudować bio Kacpra** — enterprise klienci (Animex, Corleonis), CEO Dokodu, styl nauczania
- [x] **LP: Przeformułować obietnice zarobków** — usunięte kwoty, zamienione na opisy ścieżek bez obietnic finansowych
- [x] **LP: Ujednolicić czas dostępu** — wszędzie "1 rok", usunięta sprzeczność FAQ vs pricing

**Faza 2: Social proof (ten/następny tydzień)**
- [ ] **Zebrać 10-15 prawdziwych testimoniali** — screenshoty Discord, wiadomości, zapytać kursantów
- [ ] **2-3 video testimoniale** — nawet 30s na telefon
- [ ] **Case study "Z X do Y"** — znaleźć kursanta który zmienił karierę i opisać historię

**Faza 3: Moduły AI (2-4 tygodnie)**
- [ ] **Nagrać Moduł BONUS 1: "Python + AI asystent kodowania"** (~3-4h) — Copilot, Claude Code, debugging z AI
- [ ] **Nagrać Moduł BONUS 2: "API OpenAI/Anthropic z Pythona"** (~4-5h) — chatbot, structured outputs, projekt "Asystent CV"
- [ ] **Nagrać Moduł BONUS 3: "Automatyzacja z Pythonem i AI"** (~3-4h) — scraping, Excel+AI, bot cenowy, webhook→n8n

**Faza 4: Pricing i kampania**
- [ ] **Nowa struktura cenowa** — Pystart Classic 499 / Pystart+AI 899 / Bundle 999
- [ ] **Lead magnet: "Python + AI w 15 min"** — darmowa lekcja wideo, zbiera email
- [ ] **Kampania 7 emaili** — pre-launch (3) → launch 5-7 dni (3) → close (1)
- [ ] **Evergreen funnel** — lead magnet → nurture sequence → oferta

### P3 — Nice to have
- [ ] **n8n MCP: podepnij + screenshoty do slajdów** — wygeneruj API Key (n8n.dokodu.it → Settings → n8n API), podaj Claude'owi → skonfiguruje MCP, zaimportuje 3 workflow JSON, zrobi screenshoty
- [ ] **Slidev: review prezentacji Modul_01** — po screenshotach, sprawdź layouty i wizualizacje
- [ ] **Outreach: kolejne 5 firm** — `/outreach` (VW FS, CUK, PZU, Scania, ENEA)
- [ ] **Odśwież leady** — `python3 scripts/pracuj_leads.py --save`
- [ ] **Cold email** do firm z LinkedIn (3 dni po DM)
- [ ] **Dashboard review** — zaktualizuj 000_DASHBOARD.md, sprawdź status Corleonis

---

## Poniedziałek 07.04
*Po Wielkanocy — powrót do pracy*

- [ ] Animex: follow-up do Kamila ws. wdrożenia n8n (security review)
- [ ] Animex: WYŚLIJ certyfikaty + paczkę szkoleniową (wystawione, czekają!)

## Wtorek 08.04

- [x] COP Kartoszyno: zdzwonka WIECZOREM → oferta wysłana (9 999 / 13 900 PLN)
- [x] SayFlu: oferta wysłana Krystianowi (Gemini w Google Workspace)
- [ ] NAGRAJ VSL kursu n8n — tekst w VSL_Skrypt_v1.md

## Środa 09.04

- [ ] LAUNCH early bird n8n — email N1 "999 PLN, 20 miejsc" + post LinkedIn (odłożone?)

## Czwartek 10.04 ← DZIŚ

**📅 Kalendarz:**
- 09:00 — **FOTC: Warsztat "Optymalizacja procesów" — Grupa 1** (AI Hero)
- 11:00 — Rozalia: wizyta u okulisty w Olsztynie (Familijne)
- 13:00 — Przygotuj pliki dla księgowej

**📋 Taski:**
- [x] 📞 Zadzwonić do Kwater Pracowniczych — jak idzie klikanie po prototypie ✅
- [ ] 📧 Odpowiedzieć Aleksandrowi Ambrożkowi (PyStart — chce wrócić do kursu)
- [ ] 📧 Odpowiedzieć Richardowi Thompsonowi (ECS — kurs automation with Python?)
- [ ] 📧 Sprawdzić Passionfroot — kampania reklamowa warta rozważenia?

## Piątek 11.04

**📅 Kalendarz:**
- 09:00 — **Growth Advisors: Warsztat "Codzienna efektywność" — AI dla Trenerów 3/3** (AI Hero)
- Wieczór — **Koncert Friendz** na Euro Arenie w Gdańsku (Familijne)

**📋 Taski:**
- [ ] Szkolenie + koncert z córką. **WOLNE od Dokodu.**

## Sobota 12.04 (niedziela)

**📅 Kalendarz:**
- 09:00–17:00 — **Bank&InsurHack** (Rotunda) — pitchowanie MVP od 15:00, jury

## Niedziela 13.04

**📅 Kalendarz:**
- 10:00 — **DSH: Warsztat Developerzy 1.5/2** (AI Hero, Teams)
- 15:00–20:00 — Slot konsultacyjny (Rezerwacje)

---

### Następny tydzień 14–18.04

**📅 Kalendarz:**
- Pon 14.04: cały dzień — **BNI Orłowo** + Slot konsultacyjny 10:00–15:00
- Wt 15.04: 09:00 — **FOTC: Warsztat "Codzienna efektywność" — AI w researchu** + 13:15 **SayFlu/Krystian — spotkanie** + 16:00 Developerskie synchra + Slot 16:00–21:00
- Śr 16.04: Slot konsultacyjny 12:30–17:30
- Pt 17.04: 14:00–15:00 — **Dokodu × CX Factory** (Dawid Wielec, Teams)

**📋 Taski:**
- [x] Pon 14.04: Odezwij się do Krystiana (SayFlu) — ✅ spotkanie umówione wt 15.04 13:15
- [ ] Pon 14.04: **LinkedIn DM — 3 osoby** (gotowe teksty poniżej):
  - [ ] Agnieszka Zając-Feliczak (RPA + ISO 27001) — pytanie o narzędzia RPA
  - [ ] Tomasz Bystronski (CERI International, Head of Process Automation) — uzupełnienie Blue Prism o AI
  - [ ] Kamil Jagodziński (AIUT, Operations Manager) — automatyzacja procesów biznesowych
- [ ] Śr 16.04 RANO: **TikTok — pierwszy batch nagrań.** Scenariusze od Claude (3 lekkie, wartościowe, BEZ sprzedaży). Nagrać telefonem pionowo, wrzucić MP4 → Claude odpala pipeline (napisy + montaż). Cel: test pipeline + pierwsze 3 klipy gotowe do publikacji.
- [ ] Pt 17.04: Przed callem CX Factory → `/brain-lead-research` Dawid Wielec

### Tydzień 21–25.04

**📅 Kalendarz:**
- Pon 21.04: 09:00 — **FOTC: Warsztat "Optymalizacja procesów" — Grupa 4**
- Wt 22.04: 16:00 — Developerskie synchra
- Śr 23.04: 09:00 — **FOTC: Warsztat "Optymalizacja procesów" — Grupa 5**
- 20 lub 21.04 — **LexLegali: spotkanie** (Alina potwierdza datę)

**📋 Taski:**
- [ ] Przed LexLegali → `/brain-prep-call`

### Tydzień 28.04–02.05

**📅 Kalendarz:**
- Wt 29.04: 16:00 — Developerskie synchra
- Śr 30.04: 09:00 — ~~[anulowane] DSH Warsztat Developerzy 2/2~~
- Czw 01.05: 09:00 — **POWER TEAM IT** (Olaf Pospischil, Teams) — **ODPOWIEDZ NA ZAPROSZENIE!**
- Czw 01.05: 20:00 — **Sanah na Stadionach** (Polsat Plus Arena Gdańsk)

### Tydzień 05–09.05

**📅 Kalendarz:**
- Śr 06.05: 09:00 — **FOTC: Program "Ambasadorzy AI" — Start programu**
- Śr 06.05: 16:00 — Developerskie synchra

---

## Backlog (nieprzypisane do dnia)

### P1 — Must do
- [ ] **NAGRAJ VSL kursu n8n** — tekst w VSL_Skrypt_v1.md. Bez tego nie ma launchu!
- [ ] **Animex: wyślij certyfikaty + paczkę szkoleniową** — gotowe, czekają na wysyłkę
- [ ] **Odpowiedz na zaproszenie POWER TEAM IT (01.05)** — tak/nie?

### P2 — Should do
- [ ] **LinkedIn Outreach — 5 firm** — `/outreach`
- [ ] **Blog: nowy artykuł** — n8n vs Anthropic Managed Agents (temat z daily briefing 10.04)
- [ ] **Bank&InsurHack follow-up** — po 12.04: scorecard, LinkedIn requests, follow-up Tier 1
- [ ] **Dokończ stronę ebooka** — `dokodu.it/ebooki/automatyzacja-biznesowa` (checkout, treść, ebook niedokończony). Potem redirect `lp.dokodu.it/transformacja` → `dokodu.it/ebooki/automatyzacja-biznesowa#kup-pelny-ebook`
- [ ] **Checklista AI → wrzuć na stronę** — `dokodu.it/checklista` z bramką emailową + segment MailerLite
- [ ] **Uporządkuj marketing assets** — mapa: co jest, dla kogo, jaki URL, jaki lejek (ebook / checklista / AI Act / kursy)
- [ ] **MailerLite: Welcome sequence "Newsletter nowa strona"** — 41 osób zapisanych bez żadnego maila! Zaprojektować 3 maile (przedstawienie → wartość → segmentacja). Grupy bez automatyzacji: "Newsletter Nowa strona" (41), "Chcę się uczyć baz danych" (18)
- [ ] **MailerLite: Reactivation Pystart** — 3-mailowa seria do "Chcę się uczyć Pythona" minus klienci Pystart (~2 500 osób). Cel: 75-125 sprzedaży
- [ ] **MailerLite: Ankieta n8n** — "Co automatyzujesz?" do Transformacja (657) + Newsletter AI (80) + Python (4101). Walidacja kursu + tematy na content

### P3 — Nice to have
- [ ] **EPALE — rejestracja** (30 min, darmowe)
- [ ] **Odśwież leady Pracuj** — `python3 scripts/pracuj_leads.py --save`
- [ ] **Dashboard review** — zaktualizuj 000_DASHBOARD.md

---

## Metryki sukcesu tygodnia

- [ ] VSL nagrany
- [ ] Certyfikaty Animex wysłane
- [ ] Bank&InsurHack: 3+ kontaktów Tier 1
- [ ] 2 emaile od klientów obsłużone (Ambrożek, Thompson)
- [ ] CX Factory research przed callem 17.04
