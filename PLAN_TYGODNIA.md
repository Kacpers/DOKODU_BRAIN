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

## Poniedziałek 30.03

- [x] 9:00–11:30 — Deep Work: Skrypt VSL kursu n8n ✅
- [ ] 11:30–12:00 — Dashboard review
- [x] 12:00–12:30 — Animex follow-up ✅ wysłane
- [ ] 13:00–14:00 — LinkedIn Outreach — 5 firm
- [ ] 14:00–14:30 — SEO: sprawdź meta title
- [ ] 14:30–15:00 — MailerLite: wklej 3 maile

## Wtorek 31.03

- [ ] **Platforma LMS** — dokończyć żeby kursanci mogli oglądać (BLOCKER sprzedaży!)
- [ ] **Wrzucić prośbę o testimoniale na Discord PyStart** (tekst w PRJ_Sprzedaz_Kursy_Q2_2026.md)
- [ ] **Napisać email W1** — "Wielkanocna promocja: Python za 599 PLN" → MailerLite draft
- [ ] **Napisać email W2** — "Bundle Python + SQL za 999 PLN" → MailerLite draft
- [ ] **Nagrać Short** — "3 powody żeby nauczyć się Pythona w 2026" (45s)
- [ ] LinkedIn Outreach: sprawdź kto zaakceptował zaproszenia → DM

## Środa 01.04

- [x] **Cichy-Zasada (dealer VW/Audi/Porsche)** — inbound lead, wysłano maila do n8n ws. reseller program. Czekamy na odpowiedź → oddzwonić do Rafała Nawrockiego
- [ ] **Animex: wystawić fakturę za szkolenia** — nr zamówienia: Z1089/10377/1 - [ZAK/2025/002198]
- [ ] **Wysłać email W1** — Wielkanocna promocja PyStart 599 PLN (cała lista 15 404)
- [ ] **Post LinkedIn** — promocja wielkanocna (edu styl)
- [ ] **Opublikować Short** — "3 powody żeby nauczyć się Pythona"

## Czwartek 02.04

- [ ] **Fryzjer 15:30**
- [ ] **Nagranie VSL kursu n8n** (~20:00, po fryzjerze) — tekst w `VSL_Skrypt_v1.md`
- [ ] **Nagranie Moduł 0 n8n** (~20:00+, jeśli starczy czasu) — skrypt gotowy
- [ ] **Nagranie YT: Error Handling w n8n** (opcja, 12-15 min)
- [ ] **Wysłać email W2** — "Bundle Python + SQL za 999 PLN"
- [ ] **Nagrać Short** — "SQL czy Python — czego uczyć się najpierw?" (30s)

## Sobota 04.04

- [ ] 9:30 — **Call z Jakubem Gibulą** (Administratiekantoor Gibula) — omówienie pytań do systemu fakturowego
- [ ] **Wielkanoc 5-6.04** — cisza emailowa, odpoczynek

## Piątek 03.04

- [ ] **DEADLINE: Animex certyfikaty** — wystawić wszystkie certyfikaty (lista w załączniku od Kamila, hasło SMS)
- [ ] **DEADLINE: Animex paczka szkoleniowa** — przygotować paczkę z plikami ze szkolenia do wysyłki
- [ ] **Wysłać email W3** — "Wesołych Świąt + ostatnie 4 dni promocji"
- [ ] **Weekly Review** — `/brain-weekly-review`
- [ ] **SEO Weekly** — `/seo-weekly`
- [ ] **Plan następnego tygodnia:**

### Następny tydzień 7-11.04 (po Wielkanocy)

- [ ] **EPALE — rejestracja i setup** (30 min, darmowe):
  - [ ] Załóż konto na epale.ec.europa.eu
  - [ ] Dodaj kurs n8n + PyStart do Course Catalogue
  - [ ] Opublikuj 1 artykuł (repurposing z bloga, np. "AI w edukacji dorosłych")
  - [ ] Sprawdź Partner Search pod kątem grantów Erasmus+
- [ ] Pon 7.04: Wysłać email W4 (ostatni dzień promocji) + sprawdź LinkedIn akceptacje
- [ ] Wt 8.04: Zamknięcie promocji wielkanocnej o 23:59
- [ ] Śr 9.04: **LAUNCH early bird n8n** — email N1 "999 PLN, 20 miejsc" + post LinkedIn
- [ ] Śr 9.04: Nagrać Short "Ile kosztuje Zapier vs n8n rocznie?"
- [ ] **Pt 10.04: 15:30 Rotunda** — spotkanie organizacyjne Bank&InsurHack (Kamil Bartkowiak)
- [ ] **Sob 11.04:** wolne (Bank&InsurHack — skip dnia 1)
- [ ] **Ndz 12.04: Bank&InsurHack** (9:00–17:00, Rotunda) — pitchowanie MVP od 15:00, jury, nagranie filmu ze zwycięzcami
- [ ] Nagranie BONUS 1 PyStart — przesunąć na inny termin (weekend zajęty hackathonem)

### Tydzień 14-18.04

- [ ] Pon 12.04: Email N2 "Już X osób w early bird"
- [ ] Wt 15.04: Webinar "Automatyzacja firmy w 60 min z n8n" (opcja)
- [ ] Śr 16.04: Email N3 "Ostatnie miejsca early bird" + Short
- [ ] Czw-Pt: **Nagranie Moduły 1-2 n8n** (~6h)
- [ ] Pt: **Nagranie BONUS 2 PyStart** (API OpenAI/Anthropic, ~5h)

### Tydzień 21-25.04

- [ ] Pon 20.04: Email N4 "Early bird zamknięty, od jutra 1490"
- [ ] Wt-Śr: **Nagranie Moduły 3-4 n8n** (~7h)
- [ ] Czw-Pt: **Nagranie BONUS 3 PyStart** (Automatyzacja + AI, ~4h)
- [ ] Pt: Nowa struktura cenowa PyStart na stronie (499/899/999)

### Tydzień 28.04-2.05 (Majówka)

- [ ] Pon 28.04: **PyStart Relaunch** — email M1 + film YT + post LinkedIn
- [ ] Śr 30.04: Email M2 "Majówka za rogiem"
- [ ] Pt 2.05: Email M3 "Siedzisz na kanapie? Zacznij kurs"
- [ ] 1-4.05: Majówka — emaile zaplanowane, ludzie kupują

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
