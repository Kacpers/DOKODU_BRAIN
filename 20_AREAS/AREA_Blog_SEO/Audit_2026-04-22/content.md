---
type: seo-audit
subtype: content
date: 2026-04-22
domain: dokodu.it
owner: Kacper
status: active
tags: [seo, content, eeat, readability]
---

# Content & E-E-A-T Audit — dokodu.it

**Data:** 2026-04-22
**Próba:** homepage + /o-nas + /szkolenia + /automatyzacja-ai + 3 posty blogowe

---

## TL;DR

Content w większości OK, pillar-posty (7.5k słów, 12 H2) są solidne. Główne słabości: **E-E-A-T — autor „Dokodu"** jako organizacja zamiast konkretnych osób (Kacper, trenerzy), **brak author bios na postach blogowych**, **brak case studies w formie testimoniali** na serwisowych stronach, **generic meta descriptions** na commercial pages.

**Score: 68/100**

---

## 1. Homepage — https://dokodu.it

| Element | Stan |
|---|---|
| H1 | „AI ma pracować na Twój biznes." ✅ (mocny, value-prop) |
| Meta desc | „Pomagamy firmom wyciskać realną wartość z narzędzi, za które już płacą..." ✅ (specyficzna, 147 znaków) |
| H2 count | 7 |
| Word count | ~180 widocznego tekstu (lean landing) |
| CTA | „Porozmawiajmy o współpracy" — jasny |
| Social proof | „140+ firm przeszkolonych" (llms.txt), ale **na home nie widać tej liczby w H1/above-fold** |
| Authority signals | Logo klientów? — do weryfikacji wizualnej |

**Problem:** homepage nie wykorzystuje silnego trust signal „140+ firm przeszkolonych" above-fold. To wprost cytat z llms.txt, powinien być w hero.

---

## 2. /o-nas

- Title: `O nas | Dokodu - Nowoczesne Szkolenia i Wdrożenia AI | Dokodu` (duplikacja brand)
- Brakuje **AboutPage schema**
- Nie sprawdziłem głębi tekstu (wymaga wizualnej analizy), ale z HTML: umiarkowana ilość treści
- **Brak zespołu z twarzami + bio** — klasyczny E-E-A-T fail dla agencji B2B (to jest miejsce na Kacpra, Alinę i innych)

**Fix:** sekcja „Zespół" z 5-10 osobami, każda = Person schema + link do LinkedIn + 2-3 zdania bio + specjalizacja.

---

## 3. /szkolenia (commercial hub)

- Title: `Szkolenia AI dla Firm — Microsoft Copilot, Google Gemini, ChatGPT | Dokodu | Dokodu` (duplikacja)
- H1 prawdopodobnie „Szkolenia AI dla Firm"
- **Schema: Organization + WebSite tylko** — brak `Service` / `Course` / `OfferCatalog`
- Priorytetowa strona konwersji — zasługuje na:
  - Lista konkretnych szkoleń (agenda, godziny, cena/bracket)
  - 3+ testimoniali (Person + Organization quoted)
  - FAQ z FAQPage schema (co obejmuje, dla kogo, jak się zapisać, ile trwa)
  - „Dla kogo to jest" / „Dla kogo to NIE jest" — disqualification copy

---

## 4. /automatyzacja-ai

- Title: `Automatyzacja AI dla Firm - Odzyskaj 40h Miesięcznie | Dokodu | Dokodu` (duplikacja)
- Mocna obietnica („40h"), ale **bez case studies in-line**
- Są 3 linkowane wdrożenia (auto-księgowanie, automatyzacja maili, monitoring cen) — te warto wyciągnąć do formatu card z KPI („-40h/mies, ROI w 3 mies")

---

## 5. Blog — próbka 3 postów

### /blog/zaawansowane-techniki-prompt-engineeringu
- Title: ✅ `Zaawansowane techniki prompt engineering | Dokodu` (50 chars)
- Meta desc: ✅ 115 znaków
- H1: 1 ✅
- H2: sekcje tematyczne ✅
- Word count: ~932 słów (medium-depth)
- Internal links: 61 ✅ (bogata sieć)
- Schema: BlogPosting + Organization + WebSite + SiteNavigationElement + (prawdopodobnie BreadcrumbList)
- Images: 11, wszystkie z alt ✅
- **Author: „Dokodu"** (organizacja) — ❌ powinno być `Person` (Kacper lub konkretny autor)

### /blog/wdrozenie-ai-w-firmie
- Title: ✅ `Automatyzacja AI w firmie - jak wdrożyć sztuczną inteligencję | Dokodu` (nie ma duplikacji — post blogowy template OK)
- Meta desc: ✅ 137 znaków
- H2: 12 ✅
- Word count: **~7454 słów** — flagship pillar post
- Images: 13, z alt
- Author w schema: **„Dokodu"** — znowu organizacja, brak Person

### /blog/wykorzystanie-generative-ai-w-marketingu-i-copywriting
- Nie sprawdzony w detalu, ale pattern wygląda podobnie

### Pattern problemów dla całego bloga
1. ❌ Author = `Dokodu` zamiast `Person` z bio/expertise
2. ❌ Brak „O autorze" na końcu posta (standardowa praktyka E-E-A-T)
3. ❌ Brak dat publikacji/aktualizacji widocznych w treści (są w schema ale brak w UI)
4. ⚠️ Brak cytowanych zewnętrznych źródeł (badań, raportów) — osłabia authoritativeness
5. ✅ Rich internal linking (61 linków na post) — mocne
6. ✅ Długie pillary 7.5k słów — mocne
7. ✅ Listy, H2/H3 structure, scannable — mocne

---

## 6. E-E-A-T Framework — ocena zbiorcza

| Wymiar | Score | Komentarz |
|---|---|---|
| **Experience** | 55 | Kacper ma ogromne doświadczenie (140+ firm), ale to nie widać na postach. Brak „ja, Kacper, wdrożyłem to w X firmach i oto co się potknęło". Tone jest „my Dokodu" zamiast „ja + moja expertise". |
| **Expertise** | 70 | Długie pillary, szczegóły techniczne (n8n, Docker, prompt engineering). Brak formal credentials w bio (certyfikaty AI, publikacje, speaker decks). |
| **Authoritativeness** | 60 | Organization schema z `knowsAbout` + 5 `sameAs` links ✅. Brak: backlinki z authoritative PL (wymaga zewnętrznego tooli), case studies z logo klientów, prasa. |
| **Trust** | 75 | NIP, adres Rumia, email biuro@dokodu.it, SSL ✅. Kontakt schema ✅. Brak: wizualnych testimoniali z twarzą+nazwą+stanowiskiem klienta, Google Reviews embed. |

---

## 7. AI citability (cross-link z /geo.md)

Blog posty mają potencjał ale:
- ✅ Jasne H2 jako pytania (good)
- ✅ Listy i tabele (good — LLM lubi)
- ⚠️ Pierwsze akapity nie zawsze są „direct answer paragraphs" (40-60 słów = samoistna odpowiedź)
- ❌ Brak inline citations do zewnętrznych raportów — LLM chętniej cytuje strony które same cytują

---

## 8. Readability

- ✅ Krótkie akapity (2-4 zdania)
- ✅ Listy wypunktowane
- ✅ Bold na kluczowych słowach (prawdopodobnie — do weryfikacji wizualnej)
- ⚠️ Brak widocznej „Spis treści" / TOC na długich postach (7.5k słów bez TOC = UX fail)

---

## Rekomendacje — Priorities

### High (content E-E-A-T)
1. **Zmienić `author` w schema postów na Person** (Kacper Sieradziński) z URL do bio + sameAs (LinkedIn, YouTube, Twitter/X)
2. **Author box na końcu każdego posta** — zdjęcie + 2 zdania + CTA do kontaktu
3. **Data „aktualizacja"** widoczna nad H1 postów starszych niż 6 miesięcy
4. **Zespół na /o-nas** — 5-10 twarzy z bio (jeśli brak, Kacper+Alina+trenerzy)

### High (commercial pages)
5. **Testimoniale z twarzą, nazwą, firmą** na /szkolenia i /automatyzacja-ai (3+ każda)
6. **FAQ + FAQPage schema** na /szkolenia, /automatyzacja-ai, /kursy (każdy kurs)
7. **Case study cards** inline na /automatyzacja-ai zamiast samych linków

### Medium
8. TOC (spis treści) na postach >2000 słów
9. Inline citations do zewnętrznych raportów/badań (np. McKinsey, Gartner, polskie raporty AI)
10. Direct-answer paragraphs (first 40-60 words = samoistna odpowiedź na headline)

### Low
11. Logo klientów na homepage (wall of logos above-fold)
12. Google Reviews embed na /o-nas lub /kontakt

---

## Content Score: 68/100

Blog ma solidny fundament (volume + internal linking + długie pillary). Commercial pages i E-E-A-T signals to największy downside.
