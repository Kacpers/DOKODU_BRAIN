---
type: playbook
status: active
owner: kacper
last_reviewed: 2026-05-02
tags: [newsletter, mailerlite, lifecycle, automation, welcome, nurture]
---

# NEWSLETTER PLAYBOOK — Dokodu

> **Cel:** Skalowalna, powtarzalna sekwencja emaili lifecycle (welcome, nurture, re-engagement) — bez konieczności ręcznego planowania każdej kampanii.
>
> **Filozofia:** One Email = One Job. Wartość przed pytaniem. Mniej, lepszych maili wygrywa z więcej i przeciętnych. Adaptacja `email-sequence` (coreyhaines31/marketingskills) do TOV Kacpra i specyfiki MailerLite.

---

## ZASADY STAŁE (apply do każdego maila)

1. **Jedno zadanie per email** — nigdy newsletter + sales + event w jednym
2. **Wartość przed pytaniem** — w pierwszych 3 mailach NIE pitch'uj, edukuj
3. **Subject line patterns Kacpra** (z analizy historii):
   - ✅ Działa: osobiste ("Przełom w moim studiu"), pytania ("Ile pomysłów dziś zapomniałeś?"), intryga ("Programista 2.0")
   - ❌ Nie działa: sprzedażowe ("🛑 STOP -30%"), pumpowane emoji, ALL CAPS
   - 30-50 znaków, max 60 (mobile cuts)
4. **CTA: maksymalnie 1, opcjonalnie 2** — PS NIE może sabotować głównego CTA
5. **Pre-send review:** ZAWSZE przepuść przez `/newsletter-check` przed wysyłką (lub dla niskich-stakes mailów co najmniej Anti-Pattern Quick Check)
6. **TOV:** bezpośredni, ciepły, autentyczny, praktyczny, anty-hype

---

## SEKWENCJA #1 — Welcome Series (Day 0/1/3/7/14)

**Trigger:** ktoś dołącza do listy "Dokodu Newsletter" (group `111679368` — "Dostał o mnie")

**Cel:** zbudować relację, dostarczyć quick win, w 14 dni wprowadzić w temat AI/automatyzacja, na końcu zaproponować rozmowę / produkt / kurs.

### Day 0 — Welcome + Lead Magnet Delivery

**Subject (test 3 warianty):**
- "Cześć — wszedłeś, więc obiecane materiały"
- "Mam dla Ciebie 3 rzeczy"
- "Witaj w Dokodu — start tutaj"

**Body (struktura):**
- Powitanie osobiste (1 zdanie, "z imienia jeśli masz")
- Dostarczenie tego co obiecane (link do PDFa / ebooka / co skłoniło do zapisu)
- Set expectations: "Będę pisał ~1x tygodniowo. Jeśli kiedyś nie pasuje — `unsubscribe` na dole, bez urazy."
- 1 mała next action ("kliknij i pobierz" — krótkie potwierdzenie zaangażowania)

**Główny cel:** dostarczyć wartość + ustanowić rytm. NIE sprzedawaj.

---

### Day 1-2 — Quick Win

**Subject:**
- "Co możesz zrobić w 10 minut z [tematem]"
- "[Konkretne narzędzie] — najmniejszy krok do automatyzacji"
- "1 prompt który u mnie zaoszczędził godzinę"

**Body:**
- Konkretny, mały win (1 prompt / 1 workflow / 1 narzędzie)
- Step-by-step (3-5 kroków, max)
- Link do filmu/blog posta jeśli chcą głębiej
- CTA: "Spróbuj i odpisz mi co Ci wyszło — czytam każdy mail" (start dialogu)

**Główny cel:** small success → confidence że Twój kontent jest wartościowy.

---

### Day 3-4 — Twoja Historia / Mission

**Subject:**
- "Czemu w ogóle zaczynamy ten newsletter"
- "Jak doszedłem do automatyzacji (prawie przypadkiem)"
- "Mała opowieść — i co z tego dla Ciebie"

**Body:**
- Origin story Dokodu / Twoja (skąd, czemu, dla kogo)
- Connection: "wiem co czujesz, sam tam byłem" (jeśli prawdziwe)
- Co Twoja perspektywa zmienia w sposobie myślenia o AI
- CTA: linkuj do filmu YT albo bloga "Manifest"

**Główny cel:** emocjonalna kotwica — czytelnik widzi w Tobie człowieka, nie firmę.

---

### Day 5-7 — Social Proof / Case

**Subject:**
- "Jak Animex zaoszczędził 40h tygodniowo"
- "Co się stało gdy [Klient] wdrożył pierwszy workflow"
- "Konkretne efekty — bez przesady"

**Body:**
- Konkretny klient (z zgodą) — Animex, Corleonis, lub aktualny case
- Problem → rozwiązanie → wynik (z liczbami)
- Subtelnie: pokaż że dałbyś radę u nich też, bez explicit pitch
- CTA: "Chcesz pogadać o Twojej firmie? Odpisz" lub link do `/oferta`

**Główny cel:** wiarygodność. Pokażesz że to działa, że nie sprzedajesz powietrza.

---

### Day 9-11 — Objection / Reframe

**Subject:**
- "AI tylko dla dużych firm? Sprawdziliśmy"
- "Boisz się że AI Cię zastąpi? Niewłaściwa myśl"
- "'Nie mam na to czasu' — często słyszę. Mam na to odpowiedź"

**Body:**
- Common objection (bo prawdopodobnie i Twój czytelnik tak myśli)
- Reframe: pokaż dlaczego to obstacja jest błędna albo z innej perspektywy
- Easy path forward (małe pierwsze kroki)
- CTA: konkretny resource (post bloga, ebook, kurs)

**Główny cel:** usuń psychologiczne blokery zanim dojdziesz do oferty.

---

### Day 12-14 — Conversion / Soft Pitch

**Subject:**
- "Gdybyś chciał spróbować — propozycja"
- "Co dokładnie oferuję — w 30 sekund"
- "Następny krok jeśli to ma sens"

**Body:**
- Summary value (3 max highlights z dotychczasowej sekwencji)
- Konkretna oferta (kurs / warsztat / 30-min konsultacja)
- Risk reversal: "30 min, bez umowy, bez pitch"
- Klarowny CTA — link do calendly / formularza

**Główny cel:** konwersja — ale lekka. Część subskrybentów konwertuje, część zostaje na liście jako edukowani.

---

## SEKWENCJA #2 — Post-Lead Magnet (po pobraniu ebooka/checklisty)

**Trigger:** download konkretnego lead magneta (np. "Ebook: AI dla działu HR")

**Cel:** edukacja głębsza w temacie magneta + pokazanie jak Dokodu rozwiązuje TEN konkretny problem.

| Day | Cel | Co w mailu |
|---|---|---|
| 0 | Delivery | Link do PDF + 1 "skup się na X stronie" hint |
| 2 | Deeper insight | Konkretna sekcja z ebooka rozwinięta + link do filmu YT/blog posta |
| 5 | Apply | "Jak Animex użył dokładnie tej metody" — case study |
| 8 | Reframe objection | "Mówisz: u nas to inaczej. Tutaj 3 firmy które tak myślały" |
| 12 | Soft pitch | "Jeśli chcesz pogadać jak to zrobić u Was — 30 min" |

**Reguła:** Sequence stops gdy ktoś:
- Odpisał na maila → handover do Kacpra (`/brain-meeting-notes` po rozmowie)
- Klika CTA z calendly → handover do calla
- Nie otwiera 3 maili z rzędu → przenieś do "cold" segment (pause)

---

## SEKWENCJA #3 — Re-engagement (Win-back)

**Trigger:** subscriber nie otworzył nic w ostatnich 60 dniach

**Cel:** odzyskać uwagę albo wyczyścić listę (lepiej mniej + zaangażowani niż dużo + martwi)

### Mail 1: "Czy jesteśmy się rozstać?"

**Subject:**
- "Może już nie pasuje?"
- "Jedno pytanie — szczerze"

**Body:**
- "Widzę że nie otwierasz moich maili — to OK"
- "Powiedz: czy mam pisać dalej? Odpisz: TAK / NIE / PISZ RZADZIEJ"
- "Bez urazy — wolę mniej osób ale tych którzy się angażują"

**CTA:** odpowiedź (3 opcje, friction = 0)

### Mail 2 (po 7 dniach jeśli brak reakcji): Final

**Subject:**
- "Ostatni mail — wypisuję Cię jutro"

**Body:**
- "Brak reakcji = wypisuję jutro, żeby moja lista była zdrowa"
- "Drzwi otwarte — możesz wrócić w każdej chwili"
- Link do: dokodu.it/newsletter (re-subscribe)

**Akcja:** Po 24h auto-unsubscribe przez MailerLite automation

---

## SEKWENCJA #4 — Single Topic Campaign (np. n8n Launch)

Patrz: `Newsletters/Kampania_n8n_Launch_2026-05-06.md` jako wzór.

**Struktura kampanii 1-time:**
1. **Teaser** (Day -7) — "Coś szykuję"
2. **Reveal** (Day 0) — "Ruszamy: [produkt/event]"
3. **Deep dive** (Day 3) — "Co dokładnie dostajesz"
4. **Last call** (Day 6) — "Jutro koniec / startuje"
5. **Post-event recap** (Day 8) — "Co wyszło" lub "Dlaczego (ne) do nas"

---

## QUICK CHECKLIST przed każdą wysyłką

- [ ] Subject: 30-50 znaków, lowercase preferowane (z wyjątkiem nazw firm)
- [ ] One Job rule: jeden cel, max 2 CTA
- [ ] CTA above the fold (nie tylko w PS)
- [ ] TOV: bezpośredni, "Ty" focused, anty-hype
- [ ] Anti-pattern check: brak "leverage", "kompleksowy", "innowacyjny", brak "🛑", brak "STOP"
- [ ] Risk reversal jeśli sales mail (bez zobowiązań / unsubscribe / 30 min nie 60)
- [ ] Personal sender (Kacper, nie "Zespół Dokodu")
- [ ] **`/newsletter-check`** przed wysłaniem (mandatory dla launch / sales mailów)

---

## METRYKI BENCHMARKI (Kacper, Q1 2026)

- **Średni OR Kacpra:** 37.7%
- **Benchmark PL B2B newsletter:** 25-35%
- **Top maile (>42% OR):** osobiste subject, pytania, intryga
- **Słabe maile (<30% OR):** sprzedażowe z emoji, "ostatnie godziny", promo

Pełne raporty + insighty — `/mailerlite-stats`

---

## LINKI

- Pre-send review: `/newsletter-check`
- Sync danych z MailerLite: `/mailerlite-sync` → `Newsletter_Last_Sync.md`
- Analiza historyczna: `/mailerlite-stats`
- Konkretne kampanie: `Newsletters/`
- Reviews: `Reviews/`

---

## NOTATKA O ŹRÓDLE

Sekwencje (Welcome / Lead Magnet / Re-engagement) zaadaptowane 2026-05-02 z `email-sequence/references/sequence-templates.md` (coreyhaines31/marketingskills) — przepisane do PL, dostosowane do TOV Kacpra (anty-hype), benchmarków historycznych Dokodu z MailerLite, i workflow z `newsletter-check` skill.

Pełen oryginał (EN, ~7 typów sekwencji) w: `/tmp/marketingskills/skills/email-sequence/` — wracaj jeśli chcesz dodać onboarding / post-purchase / event-based.
