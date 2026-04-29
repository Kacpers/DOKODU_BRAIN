---
type: seo-audit
subtype: technical
date: 2026-04-22
domain: dokodu.it
owner: Kacper
status: active
tags: [seo, technical, crawlability, security, cwv]
---

# Technical SEO Audit — dokodu.it

**Data:** 2026-04-22
**Stack:** Next.js (SSR, x-nextjs-prerender: 1), Cloudflare CDN
**Zakres:** homepage + 8 reprezentatywnych stron

---

## TL;DR

Technicznie solidna baza (Next.js SSR, CF cache, HTTPS, prawidłowy robots+sitemap, AI crawlery mają dostęp). Poważne minusy: **brak HSTS**, **brak CSP**, **podwojone headers** (Next.js + Cloudflare tłoczą te same nagłówki z konfliktami), **soft 404 na /trenerzy/kacper-sieradzinski** (200 + „Trener nie został znaleziony"), **title duplication** „| Dokodu | Dokodu" na kilkunastu stronach.

**Score: 72/100**

---

## 1. Crawlability

### robots.txt ✅
```
User-Agent: *
Allow: /
Disallow: /admin/
Disallow: /api/
Disallow: /checkout
Disallow: /ankieta/
Disallow: /certyfikat/
Disallow: /application/learn/
Disallow: /auth/
Disallow: /register
Disallow: /login
Host: https://dokodu.it
Sitemap: https://dokodu.it/sitemap.xml
```

- ✅ Blokuje tylko legitne privacy/ops paths
- ✅ Nie blokuje GPTBot, ClaudeBot, PerplexityBot, Google-Extended (AI crawling: open)
- ⚠️ `Host:` directive jest nieoficjalny (Yandex-only), Google go ignoruje — można usunąć
- ⚠️ Brak sekcji per-bot (opcjonalne, ale typical dla PL serwisów)

### sitemap.xml ✅
- 359 URLi, XML valid, lastmod ISO8601
- Priorytety realistyczne (1.0 home, 0.9 kluczowe, 0.7 branded)
- ⚠️ Wszystkie `lastmod: 2026-04-21T22:37:17.675Z` — identyczny timestamp to sygnał „regenerowane bez realnej zmiany" (cue dla Google że nie można ufać lastmod)

---

## 2. Indexability

### Canonical tags ✅
Homepage i blog post mają `<link rel="canonical" href="https://dokodu.it/...">` — poprawnie samo-referencyjne.

### Lang attribute ✅
`<html lang="pl">` na każdej stronie.

### Meta robots
Nie sprawdzono per-page — needs spot check dla regulaminów i konkursów (często powinny mieć `noindex`).

### ❌ CRITICAL: Soft 404 — /trenerzy/kacper-sieradzinski
```
HTTP 200 OK, page content: "Trener nie został znaleziony"
```
- Strona jest w sitemap z priority 0.7
- Wraca 200 OK zamiast 404
- Trafia do Google i marnuje crawl budget / authority
- **Fix:** naprawić routing w Next.js (dynamic route `/trenerzy/[slug]`) albo zwracać prawdziwy 404 / 410

---

## 3. Security headers

### Faktyczne headery (z `curl -sI https://dokodu.it`)

| Header | Value | Status |
|---|---|---|
| `Strict-Transport-Security` | — | ❌ **MISSING** |
| `Content-Security-Policy` | — | ❌ **MISSING** |
| `X-Frame-Options` | `SAMEORIGIN` **+** `DENY` | ⚠️ **DUPLICATED + CONFLICTING** |
| `X-Content-Type-Options` | `nosniff` **x2** | ⚠️ duplicated (bezpieczne) |
| `X-XSS-Protection` | `1; mode=block` **x2** | ⚠️ deprecated, do usunięcia |
| `Referrer-Policy` | `strict-origin-when-cross-origin` **x2** | ✅ wartość OK, duplikat bezpieczny |
| `Permissions-Policy` | `camera=(), microphone=(), geolocation=()` **+** `geolocation=()` | ⚠️ **DUPLICATED + DIFFERENT VALUES** |

### Analiza

Duplikaty wynikają z podwójnego źródła:
- Next.js `next.config.js` ustawia headers
- Cloudflare (transform rules albo managed headers) dodaje swoje

Browsery przy conflicting values zwykle biorą **pierwszy** (X-Frame-Options: SAMEORIGIN wygrywa), ale to niezdefiniowane zachowanie. **Jeden source of truth** — wybrać albo Next.js config albo CF.

### Rekomendacje (High)
1. **Dodać HSTS:** `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload`
2. **Dodać CSP (report-only najpierw):** zacząć od `Content-Security-Policy-Report-Only` z restrykcyjną polityką, monitorować przez 2 tyg., potem enforce
3. **Usunąć duplikaty** — zdecydować czy headers idą z Next.js czy z CF, drugie miejsce wyczyścić
4. **X-XSS-Protection usunąć** — przestarzały, nowoczesne browsery go ignorują/uznają za anti-pattern
5. Naprawić `Permissions-Policy` conflict — zachować wersję z camera+microphone+geolocation (bardziej restrykcyjna)

---

## 4. URL structure & redirects

- ✅ HTTPS wymuszone (HTTP→HTTPS, choć bez HSTS brak preload)
- ✅ Clean URLs bez `.html`, `.php`
- ✅ Konsekwentny non-www (dokodu.it, nie www.dokodu.it)
- ⚠️ Nie sprawdzono trailing-slash consistency — spot check pokazał że canonicals są bez trailing slash, to OK
- ✅ Polskie slugi bez diakrytyków (np. `wdrozenie-ai-w-firmie`)

---

## 5. On-page meta (próbka 8 stron)

### ❌ HIGH: Duplicated brand in title „| Dokodu | Dokodu"

Na wielu stronach title kończy się `| Dokodu | Dokodu` zamiast `| Dokodu`:

| URL | Title |
|---|---|
| `/kursy/docker` | `Docker od podstaw - Twórz stabilne środowiska \| Dokodu \| Dokodu` |
| `/szkolenia` | `Szkolenia AI dla Firm — Microsoft Copilot, Google Gemini, ChatGPT \| Dokodu \| Dokodu` |
| `/o-nas` | `O nas \| Dokodu - Nowoczesne Szkolenia i Wdrożenia AI \| Dokodu` |
| `/automatyzacja-ai` | `Automatyzacja AI dla Firm - Odzyskaj 40h Miesięcznie \| Dokodu \| Dokodu` |
| `/kontakt` | `Kontakt - Dokodu (adres, email, telefon) \| Dokodu` |
| `/kursy/pystart` | `Kurs Python - Pystart \| Dokodu \| Dokodu` |
| `/blog` | `Dokodu - Blog o Technologii: Programowanie, Automatyzacja, AI \| Dokodu` |

Strony niezadowolone:
- `/` (homepage): OK — `Dokodu - AI ma pracować na Twój biznes | Wdrożenia AI & Szkolenia`
- `/blog/<post>`: OK — `Zaawansowane techniki prompt engineering | Dokodu`
- `/trenerzy/kacper-sieradzinski`: używa fallback title (soft 404)

**Przyczyna:** layout.tsx ma `title: { template: '%s | Dokodu' }` ale poszczególne `page.tsx` już mają `| Dokodu` w stringu, więc template doubluje.

**Fix:**
- W `layout.tsx` użyć template `'%s | Dokodu'`
- Usunąć ręczne `| Dokodu` z `page.tsx` na podstronach
- Albo zostawić ręczne i usunąć template

### Meta descriptions ✅
Sprawdzone 4 strony — wszystkie mają meta description, długości 115-147 znaków (w sweet spot).

### Heading structure ✅
- Każda sprawdzona strona ma 1x H1 (compliant)
- Homepage: 1 H1 + 7 H2
- Blog post: 1 H1 + 12 H2 (long-form 7.5k słów — dobrze ustrukturyzowany)

---

## 6. Mobile & responsive ✅

- ✅ `<meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=5, user-scalable=yes">`
  - ⚠️ `maximum-scale=5` + `user-scalable=yes` jest OK, ale `maximum-scale` czasem flagowany przez accessibility audits — rozważ usunięcie
- ✅ Responsive image srcset (next/image) z breakpointami 320/375/384/512/640/768/1024/1280/1536/1920
- ✅ Preload hero image jako high priority

---

## 7. Core Web Vitals

Bez dostępu do PSI API / CrUX nie mogę podać dokładnych wartości. Sygnały z HTML:
- ✅ Hero LCP image ma `fetchPriority="high"` i preload
- ✅ next/image z proper srcset
- ✅ Fonts preloaded (Poppins)
- ⚠️ GTM ładowany blocking w `<head>` — można defer
- ⚠️ Cloudflare speculation-rules włączone (`"/cdn-cgi/speculation"`) — dobra dla nawigacji ale może zwiększać bandwidth

**Action:** odpalić PSI manualnie na top 10 stronach, dodać do `SEO_Last_Sync.md`.

---

## 8. Caching & performance (CDN)

- ✅ Cloudflare cache HIT (homepage: `cf-cache-status: HIT`, `age: 9041s`)
- ✅ `cache-control: max-age=14400, s-maxage=31536000` na home (agresywne CDN caching + umiarkowane browser caching)
- ✅ Stale-while-revalidate na blog (dobre UX)
- ✅ `alt-svc: h3=":443"` — HTTP/3 włączone
- ✅ Speculation rules dla prefetch

---

## Podsumowanie — Technical SEO

| Obszar | Score | Status |
|---|---|---|
| Crawlability (robots, sitemap) | 90 | ✅ |
| Indexability | 65 | ⚠️ soft 404 na /trenerzy/ |
| Security headers | 45 | ❌ brak HSTS+CSP, duplikaty |
| URL structure | 95 | ✅ |
| Meta tags | 55 | ❌ title duplication |
| Mobile | 90 | ✅ |
| CWV (podejrzenie) | 75 | ⚠️ needs PSI confirm |
| CDN & caching | 95 | ✅ |

**Technical SEO Score: 72/100**

## Quick wins (ten tydzień)
1. Fix title template „| Dokodu | Dokodu" (1h w Next.js)
2. Fix routing /trenerzy/[slug] lub zwróć 404 (2h)
3. Dodać HSTS header (5 min)
4. Usunąć duplikaty headers — jedno source of truth (30 min)
