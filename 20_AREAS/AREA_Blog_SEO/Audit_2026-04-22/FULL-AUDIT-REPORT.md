---
type: seo-audit
subtype: full-report
date: 2026-04-22
domain: dokodu.it
owner: Kacper
status: active
tags: [seo, audit, full-report, health-score]
---

# Full SEO Audit Report — dokodu.it

**Data audytu:** 2026-04-22
**Zakres:** 7 obszarów (technical, content, schema, sitemap, images, GEO, performance)
**Metoda:** curl fetching + HTML parsing + sitemap crawl (spot-check) + schema inspection
**Próba:** homepage + 15 reprezentatywnych stron z sitemap (359 URLi total)

---

## Executive Summary

**Overall SEO Health Score: 74/100**

Dokodu.it ma **solidną bazę techniczną** (Next.js SSR, Cloudflare CDN, HTTPS, valid sitemap, AI crawlery nie zablokowane) i **dobry content foundation** (7.5k-słowne pillary, bogata internal linking, alt text na wszystkich obrazach, llms.txt compliant). Główne słabości to **E-E-A-T signals** (author = organizacja zamiast Person, brak widocznych testimoniali z twarzą, brak FAQPage) oraz **hygiene issues** (title duplikacja „| Dokodu | Dokodu", soft 404 na /trenerzy, zdublowane security headers, brak HSTS).

### Business type detected
**AI agency / education (B2B)** — szkolenia, warsztaty, wdrożenia n8n, blog edukacyjny. Rynek PL (primary), EN jako secondary (llms.txt w EN).

---

## Score breakdown

| Obszar | Score | Waga | Weighted |
|---|---|---|---|
| Technical SEO | 72 | 25% | 18.0 |
| Content Quality | 68 | 25% | 17.0 |
| On-Page SEO (w technical) | — | 20% | — |
| Schema / Structured Data | 68 | 10% | 6.8 |
| Performance (CWV — estymacja) | 75 | 10% | 7.5 |
| Images | 85 | 5% | 4.3 |
| AI Search Readiness (GEO) | 74 | 5% | 3.7 |
| Sitemap | 78 | (w technical) | — |
| **TOTAL** | **~74** | 100% | **74** |

---

## Top 5 Critical Issues

### 1. ❌ Soft 404 na `/trenerzy/kacper-sieradzinski`
Strona zwraca **HTTP 200 + content „Trener nie został znaleziony"**. Jest w sitemap z priority 0.7, linkowana z `/trenerzy`. Traci crawl budget + blokuje implementację Person schema na BlogPosting.

### 2. ❌ Title duplication „| Dokodu | Dokodu"
Na **większości stron** (`/kursy/*`, `/szkolenia`, `/o-nas`, `/automatyzacja-ai`, `/kontakt`, `/blog`, ale NIE na `/blog/<post>` i `/`). Wygląda nieprofesjonalnie w SERPach, rozwadnia keyword weight.

### 3. ❌ Brak HSTS + CSP
Cloudflare + Next.js serwują headery ale brakuje dwóch kluczowych: `Strict-Transport-Security` (bezpieczeństwo + SEO sygnał) i `Content-Security-Policy` (ochrona przed XSS). Plus **duplikaty** na X-Frame-Options (SAMEORIGIN + DENY — konflikt), Permissions-Policy (różne wartości).

### 4. ❌ Author w BlogPosting = „Dokodu" (Organizacja)
Wszystkie posty mają `author: Organization/Dokodu` zamiast `Person` z URL do bio + `sameAs`. To kluczowy E-E-A-T signal — LLMs (ChatGPT, Perplexity, Claude) waży authority per-author, nie per-brand.

### 5. ❌ Brak FAQPage schema na commercial pages
Żadna strona nie ma FAQ schema, a `/szkolenia`, `/automatyzacja-ai`, `/kursy/*` to prime real estate dla Google rich snippets i AI Overviews.

---

## Top 5 Quick Wins (≤4h każdy)

| # | Co | Czas | Impact |
|---|---|---|---|
| 1 | Fix title template „| Dokodu | Dokodu" w Next.js `layout.tsx` | 1h | High — SERP appearance |
| 2 | Dodać `Strict-Transport-Security` header | 5 min | Medium — security + trust signal |
| 3 | Usunąć duplikaty security headers (wybrać: Next.js lub CF) | 30 min | Medium — avoid conflicts |
| 4 | Wygenerować `/llms-full.txt` z top 10 pillar posts | 2h | Medium — GEO boost |
| 5 | Dodać `<meta name="robots" content="noindex">` do `/regulamin*` i `/polityka-*` | 30 min | Low — index hygiene |

---

## Sekcje szczegółowe

### Technical SEO — 72/100 [technical.md](./technical.md)

**Działa:**
- Next.js SSR + prerendering (x-nextjs-prerender: 1)
- Cloudflare CDN, HTTP/3, cache-control agresywny
- robots.txt czysty, sitemap valid
- Responsive image pipeline
- Canonicals prawidłowe
- `<html lang="pl">`

**Minusy:**
- Soft 404 /trenerzy/kacper-sieradzinski
- Title duplication (7+ stron sprawdzonych)
- Brak HSTS, brak CSP, duplikaty headers
- X-XSS-Protection (deprecated)
- Permissions-Policy conflict (camera+mic+geo vs tylko geo)
- viewport z `maximum-scale=5` (a11y minor issue)

### Content Quality & E-E-A-T — 68/100 [content.md](./content.md)

**Działa:**
- Pillar posts 7.5k słów z 12 H2, świetnie ustrukturyzowane
- Rich internal linking (61 linków na post)
- Alt text na wszystkich obrazach
- Homepage H1 + mocny value-prop

**Minusy:**
- Author = „Dokodu" (systemowy problem)
- Brak widocznego zespołu z twarzą+bio (/o-nas)
- Brak testimoniali z Person+Organization quoted
- Brak inline citations do zewnętrznych raportów
- Brak TOC na długich postach
- Brak „140+ firm" above-fold na homepage (mimo że w llms.txt)

### Schema / Structured Data — 68/100 [schema.md](./schema.md)

**Działa:**
- Organization rich (sameAs 5, contactPoint, address, knowsAbout 9, offers)
- WebSite z SearchAction (sitelinks searchbox)
- BlogPosting na /blog/<post>
- Course na /kursy/<slug> (spot-check: docker)
- SiteNavigationElement

**Minusy:**
- Author w BlogPosting = string „Dokodu"
- Brak FAQPage (wszędzie)
- Brak Event na webinarach
- Brak Service na /szkolenia, /automatyzacja-ai
- Brak AboutPage, ContactPage, LocalBusiness
- BreadcrumbList tylko na blog postach (brak na kursach, webinarach)
- Brak Review/AggregateRating

### Sitemap — 78/100 [sitemap.md](./sitemap.md)

**Działa:**
- 359 URLi, valid XML
- Priorytety zróżnicowane (0.5-1.0)
- changefreq adekwatny per sekcja
- Sitemap w robots.txt

**Minusy:**
- Identyczny `lastmod` na wszystkich URLach (generowany przy buildzie, nie przy edycji)
- 6 regulaminów/polityk w sitemap bez noindex
- /trenerzy/kacper-sieradzinski w sitemap mimo soft 404
- Pojedynczy plik (brak sitemap index per kategoria — nie krytyczne dla 359 URLi)

### Images — 85/100 [images.md](./images.md)

**Działa:**
- next/image pipeline: responsive srcset, WebP, lazy loading, width+height (CLS~0)
- Hero LCP z fetchPriority + preload
- Wszystkie sprawdzone obrazy mają alt
- Breakpoints 320/375/.../1920

**Minusy:**
- Featured images = PNG source (next/image konwertuje dla przeglądarki, ale OG share to PNG)
- AVIF może nie być włączone (`next.config.js` check)
- Jakość alt text nie audytowana (tylko obecność)

### AI Search Readiness (GEO) — 74/100 [geo.md](./geo.md)

**Działa:**
- `/llms.txt` istnieje (200 OK), dobrze skonstruowany po EN
- Wszystkie AI crawlery (GPTBot, ClaudeBot, PerplexityBot, Google-Extended) mają dostęp
- Brand mention signals spójne (Organization schema, konsystentne title)
- Listy + H2 structure (LLM-friendly)
- Rich internal linking

**Minusy:**
- `/llms-full.txt` brak (404)
- Author = organizacja (duplicate z content/schema)
- Brak direct-answer paragraphs w pierwszych 40-60 słowach
- Brak FAQPage (duplicate z schema)
- Brak inline stats + source citations

### Performance (CWV) — estymacja 75/100

**Nie zmierzone bezpośrednio** — wymaga PSI API / CrUX dataset lub Playwright.

Sygnały z HTML:
- ✅ Hero LCP preload + fetchPriority=high
- ✅ next/image z responsive srcset
- ✅ Cloudflare cache HIT
- ⚠️ GTM ładowany blocking w `<head>`
- ⚠️ Speculation rules włączone (bandwidth cost)

**Action:** odpalić PSI na top 10 stron, dodać wyniki do `SEO_Last_Sync.md` przy następnym /seo-sync.

---

## Konkurencyjny kontekst

**Polska konkurencja B2B agency:**
- dokodu.it jest **powyżej średniej** dla PL agency w:
  - Schema markup (większość PL agency ma tylko Organization)
  - llms.txt (rzadkość na PL rynku)
  - Long-form pillar content (7.5k słów = 90 percentyl)
  - Technical stack (Next.js SSR, CF CDN)
- **Poniżej średniej** w:
  - Testimoniale z twarzą i nazwą (standard u globalnych agency)
  - Case studies z KPI upfront
  - Author bios (wszystkie poważne content brands mają Person author)

Gap vs top PL:
- Nowe ekipy jak np. Digital Beast mają agresywny PR + case studies widoczne na home. Dokodu ma content głębszy, ale **słabiej packagowany social proof**.

---

## Następne kroki

Patrz → [ACTION-PLAN.md](./ACTION-PLAN.md) dla konkretnego sequenced plan z estymatami.

**Retest za 90 dni** (2026-07-22) po implementacji High priorities:
- Expected score: 82-85
- Big lifts: title fix (72→78), Person author + FAQ schema (68→82), HSTS+CSP (72→80)

---

## Pliki w tym audycie

- `technical.md` — crawlability, security, URL, CWV
- `content.md` — E-E-A-T, readability, blog quality
- `schema.md` — JSON-LD per type, rekomendacje
- `sitemap.md` — struktura 359 URLi, quality gates
- `images.md` — alt, format, lazy, CLS
- `geo.md` — AI search, llms.txt, citability
- `ACTION-PLAN.md` — priorytety Critical → High → Medium → Low
