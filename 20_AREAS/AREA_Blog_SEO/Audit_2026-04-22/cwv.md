# Core Web Vitals — dokodu.it (Lighthouse 13.1)

Mierzone: 2026-04-24 przez Lighthouse lokalnie (mobile, headless Chrome).
Lab data — symulacja slow 4G + mobile CPU. Dla real users (CrUX) sprawdź GSC → Core Web Vitals report.

## Score overview (lower = pilniejsze)

| URL | Score | LCP | CLS | TBT | FCP |
|-----|-------|-----|-----|-----|-----|
| `/blog/wdrozenie-ai-w-firmie` | **35** | ❌ 13.6s | ✅ 0.003 | ❌ 1506ms | 4.7s |
| `/blog/sql` | **42** | ❌ 18.5s | ✅ 0.003 | ❌ 765ms | 4.5s |
| `/automatyzacja-ai` | **59** | ❌ 11.7s | ✅ 0.003 | ✅ 116ms | 5.3s |
| `/blog` | **60** | ❌ 12.9s | ✅ 0.003 | ✅ 131ms | 4.6s |
| `/kontakt` | **60** | ❌ 10.9s | ✅ 0.003 | ⚠️ 213ms | 4.1s |
| `/kursy` | **60** | ❌ 12.1s | ✅ 0.003 | ✅ 115ms | 4.2s |
| `/szkolenia` | **60** | ❌ 12.8s | ✅ 0.003 | ✅ 149ms | 4.4s |
| `/konsultacje` | **61** | ❌ 11.9s | ✅ 0.003 | ✅ 102ms | 4.2s |
| `/o-nas` | **62** | ❌ 10.8s | ✅ 0.003 | ✅ 156ms | 4.1s |
| `/` | **63** | ❌ 11.5s | ✅ 0.003 | ✅ 109ms | 3.8s |

## Summary

- **Średni score:** 56/100
- Strony Good (score ≥90): 0/10
- Strony Poor (score <50): 2/10

## Thresholdy (Google Core Web Vitals)

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP    | ≤2.5s | ≤4.0s | >4.0s |
| INP    | ≤200ms | ≤500ms | >500ms |
| CLS    | ≤0.1 | ≤0.25 | >0.25 |
| TBT    | ≤200ms | ≤600ms | >600ms |

## Priorytet fix

### ❌ LCP > 4s (poor)
- `/blog/wdrozenie-ai-w-firmie` — LCP 13.6s
- `/blog/sql` — LCP 18.5s
- `/automatyzacja-ai` — LCP 11.7s
- `/blog` — LCP 12.9s
- `/kontakt` — LCP 10.9s
- `/kursy` — LCP 12.1s
- `/szkolenia` — LCP 12.8s
- `/konsultacje` — LCP 11.9s
- `/o-nas` — LCP 10.8s
- `/` — LCP 11.5s

**Typowe przyczyny LCP >4s:**
- Hero image nie-preloaded lub bez `fetchPriority=high`
- Duży font file ładowany synchronously
- Render-blocking CSS/JS w `<head>`
- Server response time (TTFB) >800ms

### ❌ TBT > 600ms (poor)
- `/blog/wdrozenie-ai-w-firmie` — TBT 1506ms
- `/blog/sql` — TBT 765ms

**Typowe przyczyny:** JS bundle too big, non-split chunks, third-party scripts blocking.

## Root cause analysis (homepage)

**Total payload: 1409 KiB.** Główne obciążenie to JavaScript, nie obrazy.

### Top opportunities (savings)
| Problem | Potencjalne oszczędności |
|---------|--------------------------|
| Reduce unused JavaScript | **3520ms / 707 KiB** |
| Reduce unused CSS | 300ms / 37 KiB |

### Najciężsi ofenderzy (bytes)
- **417 KB** — `/_next/static/chunks/bbfe2e9f02535723.js` (main bundle)
- **166 KB** — `/67az/?id=G-13P0PPECK5` (Google Analytics proxy)
- **140 KB** — `/67az/` (GTM loader)
- **135 KB** — `googletagmanager.com/gtm.js`
- **96 KB** — `facebook.net/en_US/fbevents.js` (Facebook Pixel)
- **69 KB** — `/_next/static/chunks/3062a34437f6f565.js`
- **65 KB** — `/images/homepage/hero.webp` (OK, mały)

Razem **~950 KB JavaScript** trzeba pobrać, sparsować i wykonać zanim LCP nastąpi. Na mobile 4G + 4× CPU slowdown = 10+ sekund.

## Rekomendacje (priorytet)

### 🔴 Critical — dziś/ten tydzień
1. **Defer Google Tag Manager** — załadować po `DOMContentLoaded` (obecnie blocks render)
2. **Defer Facebook Pixel** — ładować tylko po user interaction albo lazy
3. **Dynamic imports Next.js** — lazy-load komponenty pod fold (ContactBubble, CookieConsent, etc.)
4. **`next/dynamic` dla heavy components** (np. animacje, modale, wykresy) z `ssr: false`

### 🟠 High — ten miesiąc
5. **Tree shake** — `@next/bundle-analyzer` pokaże konkretne deps do usunięcia. 707 KiB unused JS = jest co.
6. **Route-based code splitting** — Next.js robi to automatycznie, ale sprawdź że nie ładujesz wszystkich features w global layout
7. **Font optimization** — użyj `display: swap` + preload tylko critical weights
8. **Preload LCP image** — już jest (`fetchPriority=high` w layout), ale upewnij się że działa po deploy

### 🟡 Medium
9. **Server-side rendering timing** — TTFB na Cloudflare edge powinno być <200ms
10. **Image sitemap** — dla /blog/ w GSC
11. **CrUX field data** — sprawdź real user experience w GSC → Core Web Vitals report (3-6 miesięcy danych)

## Co zweryfikować w GSC
GSC → Core Web Vitals pokazuje **real user data** z ostatnich 28 dni. Lighthouse to lab (slow 4G + 4x CPU emulation) — może być gorszy niż realny experience z szybszymi urządzeniami. Jeśli GSC pokazuje "Good" dla większości stron, priorytet CWV spada. Jeśli "Poor" — to priorytet absolutny, duży SEO lift po fixie.

## Retest po fixach
Po implementacji defer GTM/Pixel + dynamic imports:
```bash
# Repeat this measurement:
bash /tmp/lh_batch.sh
# Regenerate report and diff with cwv.md baseline.
```
Expected: LCP spadnie o 4-6s (z 11.5s → 5-7s), score z 63 → 85+.
