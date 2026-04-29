---
type: seo-audit
subtype: images
date: 2026-04-22
domain: dokodu.it
owner: Kacper
status: active
tags: [seo, images, performance, alt-text, cls]
---

# Images Audit — dokodu.it

**Data:** 2026-04-22
**Stack:** Next.js `next/image`, WebP preferred, responsive srcset
**Próba:** homepage + 2 blog posts (prompt-engineering, wdrozenie-ai)

---

## TL;DR

Mocna strona — next/image robi 80% pracy SEO image automatycznie (responsive srcset, WebP, lazy loading, width+height). Wszystkie sprawdzone obrazy mają alt text. Jedyne minusy: **nie audytowano jakości alt text** (tylko obecność), **WebP zamiast AVIF** (AVIF daje ~30% dalszej redukcji), **można rozważyć preload więcej niż tylko hero**.

**Score: 85/100**

---

## 1. Dane z audytu

### Homepage (https://dokodu.it)
- IMG count: 15
- Brak alt attr: 0 ✅
- `alt=""` (decoracyjne): 0 ✅
- Wszystkie obrazy z srcset (next/image): ✅
- Hero: `fetchPriority="high"` + preload ✅
- Breakpoints: 320/375/384/512/640/768/1024/1280/1536/1920 ✅

### /blog/zaawansowane-techniki-prompt-engineeringu
- IMG count: 11
- Brak alt: 0 ✅
- Featured image (OG): `https://dokodu.it/images/posts/zaawansowane-techniki-prompt-engineeringu.png` (PNG, nie WebP)

### /blog/wdrozenie-ai-w-firmie
- IMG count: 13
- Brak alt: 0 ✅

---

## 2. Co działa (stack Next.js)

- ✅ **Responsive srcset** — next/image generuje warianty per breakpoint
- ✅ **WebP format** — `/_next/image?url=...&w=...&q=75` dostarcza WebP jeśli browser wspiera
- ✅ **Width + height** w HTML (Next.js wymaga, CLS ~0)
- ✅ **Lazy loading** by default dla below-fold
- ✅ **Priority + preload** na hero LCP image
- ✅ **`imageSizes`** atrybut dla precyzyjnej selekcji per viewport

Wszystkie obrazy leci przez `/_next/image?url=...` — CDN optymalizacja na starcie.

---

## 3. Problemy i okazje

### ⚠️ Medium: Featured images blog postów to PNG
`og:image` wskazuje na `.../images/posts/*.png`. Next.js te obrazy też przepuszcza przez image pipeline (WebP on-the-fly dla browsera), ale:
- Source file = PNG = duży — generuje większe WebP
- Featured image na Slack/LinkedIn/FB preview = PNG (platformy nie używają `/_next/image` proxy)

**Fix:** konwertować source PNGs do WebP przy zapisie w `public/images/posts/` (+ ewentualnie zachować PNG fallback dla OG gdzie trzeba). Sprawdzić czy new pipeline (Nano Banana z memory) generuje WebP by default.

### ⚠️ Medium: AVIF support
Next.js 14+ może serwować AVIF przez config:
```js
// next.config.js
module.exports = {
  images: {
    formats: ['image/avif', 'image/webp'],
  },
}
```
AVIF daje ~30% mniejszy filesize vs WebP. Support w browserach: ~95% (2026-04). **Nie sprawdzone czy włączone** — `curl -I` na image URL pokaże `content-type: image/avif` lub `image/webp`.

### ⚠️ Low: Jakość alt text nie audytowana
Wszystkie obrazy mają atrybut `alt`, ale nie sprawdziłem **treści**:
- Czy alt opisuje obraz, czy jest generyczny („image", „placeholder")?
- Czy alt dla ilustracji w blogu dodaje kontekst czy tylko duplikuje H2?
- Czy alt dla logo = „Dokodu" czy „Logo Dokodu - agencja AI"?

**Action:** wizualny audit kilku postów, spot-check 20 obrazów — wymaga albo Playwright/screenshotów, albo ręcznego przeglądu.

### ✅ / ⚠️ Hero preload: tylko 2 obrazy
Homepage preload-uje:
1. `/images/homepage/hero.webp` — LCP ✅
2. `/images/logos/copilot-color.png` — sztywno preloaded bez mediazy

Drugi (logo copilot) to prawdopodobnie logo z wall-of-logos. Pytanie czy to pomaga (to nie jest LCP, a zajmuje critical path bandwidth). Można testować — może nie dawać korzyści, tylko kosztować.

### Brak Image sitemap
Nie ma `sitemap-images.xml`. Dla stron edukacyjnych to opcjonalne, ale jeśli blog post images są na tyle wartościowe by trafiać do Google Images, warto dodać.

**Priority:** Low.

---

## 4. Rekomendacje

### Medium
1. Source featured images = WebP (nie PNG) — plus ew. generacja WebP w image gen pipeline
2. Włączyć AVIF w `next.config.js` (jeśli jeszcze nie)
3. Wizualny spot-check jakości alt text na 20 random images

### Low
4. Image sitemap (gdy ruch z Google Images stanie się meaningful)
5. Zrewidować drugi preload (copilot logo) — test A/B czy poprawia LCP czy nie

---

## Image Score: 85/100

Mocna strona dzięki Next.js image pipeline. Poprawki są cosmetic.
