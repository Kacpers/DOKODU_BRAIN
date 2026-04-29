---
type: seo-audit
subtype: action-plan
date: 2026-04-22
domain: dokodu.it
owner: Kacper
status: active
tags: [seo, action-plan, priorities]
---

# Action Plan — dokodu.it SEO Audit 2026-04-22

Priorytety wg wpływu × pilności × kosztu implementacji. Sequenced — każda sekcja do zrobienia w kolejności.

**Expected lift po High:** 74 → 82-85.

---

## 🔴 Critical — zrobić w tym tygodniu

### C1. Fix soft 404 na `/trenerzy/kacper-sieradzinski`
- **Problem:** strona zwraca 200 + „Trener nie został znaleziony", priority 0.7 w sitemap
- **Fix:**
  - Naprawić dynamic route `/trenerzy/[slug]/page.tsx` (data source?)
  - ALBO zwracać prawdziwy 404 (`notFound()` w Next.js) + usunąć z sitemap
  - **Preferowane:** naprawić — bo to prereq do Person schema na blog postach
- **Estymata:** 2-4h (zależy czy dane trenerów są w DB/CMS czy trzeba stworzyć)
- **Blocker dla:** H3 (Person author)

### C2. Fix title duplication „| Dokodu | Dokodu"
- **Problem:** kilkanaście stron ma podwojony brand w title
- **Fix:** w Next.js `app/layout.tsx`:
  ```tsx
  export const metadata = {
    title: {
      template: '%s | Dokodu',
      default: 'Dokodu - AI ma pracować na Twój biznes',
    }
  }
  ```
  Następnie w każdym `page.tsx` używać samego tytułu bez `| Dokodu`:
  ```tsx
  export const metadata = {
    title: 'Docker od podstaw - Twórz stabilne środowiska',
  }
  ```
- **Estymata:** 1h (1 edit w layout + find&replace w `page.tsx`)
- **Verify:** `curl -s https://dokodu.it/kursy/docker | grep -oE '<title>[^<]+'`

---

## 🟠 High — zrobić w tym miesiącu

### H1. Usunąć duplikaty security headers + dodać HSTS
- **Problem:**
  - `X-Frame-Options: SAMEORIGIN` **+** `DENY` (konflikt)
  - `Permissions-Policy` duplikat z różnymi wartościami
  - `X-XSS-Protection` deprecated, x2
  - Brak `Strict-Transport-Security`
- **Fix:** zdecydować jedno źródło (Next.js `next.config.js` albo Cloudflare Transform Rules):
  ```js
  // next.config.js — jeśli Next.js jest źródłem
  async headers() {
    return [{
      source: '/:path*',
      headers: [
        { key: 'Strict-Transport-Security', value: 'max-age=63072000; includeSubDomains; preload' },
        { key: 'X-Frame-Options', value: 'SAMEORIGIN' },
        { key: 'X-Content-Type-Options', value: 'nosniff' },
        { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
        { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
      ],
    }];
  }
  ```
  Jeśli CF też dodaje — wyłączyć w CF (Rules → Managed Transforms → Add security headers = off).
- **Estymata:** 30 min
- **Verify:** `curl -sI https://dokodu.it` — każdy header tylko raz, HSTS obecny
- Note: **CSP jako osobny, większy ticket** (M4)

### H2. Dodać FAQPage schema na 4 commercial pages
- **Problem:** brak FAQ rich snippets
- **Strony:** `/szkolenia`, `/automatyzacja-ai`, `/kursy`, `/konsultacje` + per-kurs (`/kursy/docker`, `/kursy/pystart`, etc.)
- **Fix:**
  1. Napisać 5-10 Q&A per stronę (użyj `/brain-capture` albo zasady E-E-A-T)
  2. Wyrenderować w UI (Accordion komponent)
  3. Dodać JSON-LD:
  ```tsx
  const faqJsonLd = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: faqs.map(f => ({
      '@type': 'Question',
      name: f.question,
      acceptedAnswer: { '@type': 'Answer', text: f.answer },
    })),
  };
  ```
- **Estymata:** 2h per strona (copy + UI + schema) → 8-16h dla 4-8 stron
- **Impact:** duży na AI Overviews + rich snippets

### H3. Fix author w BlogPosting → Person
- **Prereq:** C1 (routing trenerów działa)
- **Problem:** wszystkie posty mają `author: "Dokodu"`
- **Fix:** w `app/blog/[slug]/page.tsx`:
  ```tsx
  author: {
    '@type': 'Person',
    '@id': `https://dokodu.it/trenerzy/${post.authorSlug}#person`,
    name: post.authorName,
    url: `https://dokodu.it/trenerzy/${post.authorSlug}`,
    sameAs: [post.authorLinkedin, post.authorYoutube].filter(Boolean),
    jobTitle: post.authorRole,
    worksFor: { '@id': 'https://dokodu.it/#org' },
  }
  ```
- **Data backfill:** każdy post w CMS/markdown musi mieć pole `author_slug` (domyślnie `kacper-sieradzinski`)
- **Estymata:** 4-6h (schema + backfill wszystkich 313 postów)
- **Equivalent:** dodać widoczny „Author box" na końcu każdego posta z twarzą + bio + CTA

### H4. Wygenerować `/llms-full.txt`
- **Problem:** `llms-full.txt` 404 (brakuje pełnej wersji llms.txt)
- **Fix:** stworzyć endpoint `/app/llms-full.txt/route.ts` który zwraca:
  - Homepage copy (full markdown)
  - `/o-nas` copy
  - Top 10 pillar posts (full markdown content)
  - FAQ z commercial pages (po H2)
- **Estymata:** 2-3h (endpoint + content pipeline)
- **Verify:** `curl https://dokodu.it/llms-full.txt` = 200 z markdown

### H5. Dodać `noindex` na regulaminy i polityki
- **Problem:** 6 regulaminów w sitemap, bez noindex — rozwadniają authority
- **Fix:** w `app/regulamin*/page.tsx` i `app/polityka-*/page.tsx`:
  ```tsx
  export const metadata = {
    robots: { index: false, follow: true },
  }
  ```
- **Estymata:** 30 min
- **Verify:** `curl -s URL | grep -oE 'name="robots"[^>]+'`

---

## 🟡 Medium — zrobić w tym kwartale

### M1. Event schema na `/webinary/<slug>`
- `EducationEvent` z startDate, endDate, VirtualLocation, organizer, offers
- Estymata: 3h (template + backfill danych)

### M2. BreadcrumbList na wszystkich podstronach (kursy, webinary, dla-firm, automatyzacja-ai)
- Uniwersalny komponent + schema w layoutach
- Estymata: 2h

### M3. Service schema na `/szkolenia` i `/automatyzacja-ai`
- `Service` z provider, areaServed, hasOfferCatalog
- Estymata: 2h

### M4. CSP (Content-Security-Policy) w trybie Report-Only
- Zacząć od `Content-Security-Policy-Report-Only` żeby nie zepsuć produkcji
- Monitor reportów 2 tyg., naprawić violations, potem enforce
- Estymata: 4-6h (first pass) + 2 tyg monitoring

### M5. AboutPage + ContactPage + LocalBusiness schema
- `/o-nas`: AboutPage
- `/kontakt`: ContactPage + LocalBusiness (adres, geo, openingHours, telephone)
- Estymata: 2h

### M6. Zespół na /o-nas z Person schema
- 5-10 trenerów z twarzą + bio + LinkedIn
- Estymata: 4-6h (copy + layout + schema)

### M7. Testimoniale z twarzą na /szkolenia i /automatyzacja-ai
- 3+ per strona, Person + Organization, cytat, KPI
- Estymata: zbiórka (1-2 tyg outreach) + 2h implementacji

### M8. Case study cards na /automatyzacja-ai
- Wyjąć 3 istniejące wdrożenia do in-line cards z KPI, zamiast samych linków
- Estymata: 2-3h

### M9. Sitemap lastmod = faktyczny timestamp modyfikacji
- Generator powinien czytać `git log` lub `updated_at` z CMS, nie używać build time
- Estymata: 2h

### M10. Włączyć AVIF w next.config.js (jeśli off)
- `images.formats: ['image/avif', 'image/webp']`
- Estymata: 30 min test

---

## 🟢 Low — backlog

### L1. TOC (spis treści) na postach >2000 słów
- Komponent z sticky sidebar
- Estymata: 4h

### L2. Inline citations do zewnętrznych raportów
- McKinsey State of AI, Gartner, polskie raporty
- 2-3 cytacje per pillar post
- Estymata: ongoing w content pipeline

### L3. Direct-answer paragraphs na starszych postach
- Pierwsze 40-60 słów = samoistna odpowiedź
- Refactor przy okazji content updates
- Estymata: ongoing

### L4. Nagłówki H2 w formie pytań
- „Jak działa X?" zamiast „X"
- Refactor przy content updates
- Estymata: ongoing

### L5. Image sitemap
- `/sitemap-images.xml`
- Gdy ruch z Google Images stanie się meaningful
- Estymata: 2h

### L6. Book schema na /ebooki/<slug>
- Estymata: 1h

### L7. Review / AggregateRating
- Tylko po zbiórce realnych reviews (Google, Clutch, Capterra)
- Wymóg Google: Review schema musi referować widoczną recenzję

### L8. Featured images source = WebP zamiast PNG
- Poprawić image gen pipeline (Nano Banana) żeby domyślnie WebP
- Estymata: 30 min konfiguracji

### L9. Audyt jakości alt text (wizualny, 20 obrazów)
- Spot check czy nie generic („image", „photo")
- Estymata: 2h

---

## Sequencing — rekomendowany flow

### Tydzień 1 (ten tydzień)
- ✅ C1 (trenerzy routing) + C2 (title fix) — 3-5h pracy

### Tydzień 2-4 (kwiecień-maj)
- ✅ H1 (HSTS + deduplikacja headers) — 30 min
- ✅ H5 (noindex regulaminy) — 30 min
- ✅ H4 (llms-full.txt) — 2-3h
- ⚠️ H3 (Person author) — 4-6h (po C1)
- ⚠️ H2 (FAQPage) — zacząć od 2 stron (`/szkolenia`, `/automatyzacja-ai`)

### Miesiąc 2 (maj-czerwiec)
- M1 (Event schema webinary) — 3h
- M2 (BreadcrumbList) — 2h
- M3 (Service schema) — 2h
- M5 (AboutPage/ContactPage/LocalBusiness) — 2h
- M9 (sitemap lastmod) — 2h
- M10 (AVIF) — 30 min

### Miesiąc 3 (lipiec)
- M4 (CSP report-only) — 4-6h
- M6 (zespół /o-nas) — 4-6h
- M7 (testimoniale outreach + impl) — ongoing
- M8 (case studies cards) — 3h

### Retest: 2026-07-22
- Uruchomić ten sam audyt
- Expected score: **82-85**
- Fokus: confirm że title fix + Person author + HSTS + FAQ schema zadziałały

---

## Metryki do trackingu

W `SEO_Last_Sync.md` i `SEO_Insights.md` po każdym `/seo-sync` monitoruj:
- Impressions (z GSC) — baseline przed audytem vs +30 dni po fixach
- CTR na pages z nowymi FAQ/rich snippets
- Rich results w Google Search Console → Enhancements
- Pozycje na long-tail queries (rich snippet = position 0)
- Bounce rate na pages z FAQ (GA4)
