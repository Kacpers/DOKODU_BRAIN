---
type: seo-audit
subtype: sitemap
date: 2026-04-22
domain: dokodu.it
owner: Kacper
status: active
tags: [seo, sitemap, structure]
---

# Sitemap Audit — dokodu.it

**URL:** https://dokodu.it/sitemap.xml
**Data:** 2026-04-22
**Total URLs:** 359

---

## TL;DR

Pojedynczy `sitemap.xml` z 359 URLami, XML valid. Rozkład zdrowy — 313 postów blogowych + 46 innych stron. Minusy: **identyczny `lastmod` na wszystkich URLach**, **brak sitemap index** (mimo że jeszcze nie obowiązkowy), **brak osobnych sitemaps per kategoria** (utrudnia monitoring GSC per sekcja), **6 regulaminów w sitemap** (powinny mieć noindex lub nie być w sitemap).

**Score: 78/100**

---

## 1. Rozkład URLi per kategoria

| Kategoria | Count | Priorytet |
|---|---|---|
| `/blog/<post>` | 313 | 0.6-0.8 |
| `/webinary/<slug>` | 7 | 0.8 |
| `/regulamin*, /polityka-*` | 6 | 0.5 |
| `/automatyzacja-ai/*` | 5 | 0.7-0.9 |
| `/kursy/<slug>` | 5 | 0.8 |
| `/dla-firm/<slug>` | 4 | 0.8-0.9 |
| `/szkolenia*` | 3 | 0.8 |
| `/ebooki/<slug>` | 3 | 0.6 |
| `/trenerzy/<slug>` | 2 | 0.7 |
| `/newslettery/<slug>` | 2 | 0.6 |
| `/blog` (index) | 1 | 0.9 |
| `/kursy` (index) | 1 | 0.8 |
| `/slownik-ai` | 1 | — |
| Homepage | 1 | 1.0 |
| Inne | 5 | — |

**Razem: 359**

Proporcje są zdrowe dla agencji edukacyjnej — gros wolumenu to blog content, reszta to commercial hubs i resources.

---

## 2. Problemy

### ⚠️ Medium: Identyczny `lastmod` na wszystkich URLach
Wszystkie URLe mają `<lastmod>2026-04-21T22:37:17.675Z</lastmod>`. To sygnał dla Google, że sitemap jest regenerowany batchem (przy każdym deployu), a nie per-change. Google może zacząć ignorować `lastmod`.

**Fix:** generator sitemap w Next.js powinien używać:
- Dla postów blogowych: `lastmod` = faktyczna data `updated_at` z API/CMS
- Dla statycznych stron: `lastmod` tylko gdy content się naprawdę zmienił (git log na plik page.tsx)

### ⚠️ Medium: Regulaminy i polityki w sitemap
6 URLi to `/regulamin*`, `/polityka-prywatnosci-i-cookies`:
- `/polityka-prywatnosci-i-cookies`
- `/regulamin`
- `/regulamin-konkursu-aixn8n`
- `/regulamin-newslettera`
- `/regulamin-szkolenia-online`
- `/regulamin-zakupow`

Takie strony nie generują organic traffic, rozwadniają sitemap. Dwa podejścia:
1. **Zostaw w sitemap + dodaj `<meta name="robots" content="noindex, follow">`** — wtedy Google je zna ale nie indeksuje
2. **Wyrzucić z sitemap** — prostsze, wystarczy aby były linkowane ze stopki

Pierwsze rekomendowane (noindex + follow z sitemap).

### ⚠️ Medium: Brak sitemap index / osobnych sub-sitemaps

Próg krytyczny to 50k URLi — ale dla 359 nie jest krytyczne. Co to by dało:
- `sitemap-blog.xml` (313 URLi)
- `sitemap-kursy.xml` (6)
- `sitemap-webinary.xml` (7)
- `sitemap-static.xml` (~20)
- `sitemap-legal.xml` (6, z noindex)

Benefit: w GSC widać „Indexed" per sitemap, łatwiej debugować który segment ma problem (np. „80% blog index vs 50% kursy" = problem z kursami).

**Priority:** niska teraz, podnieść gdy blog przekroczy 1000 postów.

### ❌ High: `/trenerzy/kacper-sieradzinski` w sitemap ale **soft 404**
Zgłoszone w `technical.md`. Fix = napraw routing lub usuń z sitemap.

---

## 3. Pozytywy

- ✅ XML valid, UTF-8, `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">`
- ✅ Priorytety są uzasadnione i zróżnicowane (0.5–1.0)
- ✅ `changefreq` zróżnicowany (`daily` dla /blog indexu, `weekly` dla głównych stron, `monthly` dla postów i statycznych)
- ✅ Wszystkie URLe to `https://`
- ✅ Spot-check 5 URLi = wszystkie 200 OK (oprócz sygnalizowanego soft 404 na trenerze)
- ✅ Sitemap zgłoszony w `robots.txt`: `Sitemap: https://dokodu.it/sitemap.xml`

---

## 4. Rekomendacje

### High
1. Usunąć `/trenerzy/kacper-sieradzinski` z sitemap **lub** naprawić routing (preferowane drugie)
2. Dodać `noindex, follow` na stronach `/regulamin*` i `/polityka-*` (lub wyrzucić z sitemap)

### Medium
3. Sitemap lastmod = faktyczny timestamp modyfikacji, nie build time
4. Gdy blog przekroczy 500 postów: podzielić na sitemap index + sub-sitemaps

### Low
5. Dodać `<changefreq>` bardziej konserwatywnie na statycznych stronach (`yearly` na regulaminach zamiast `monthly`)

---

## Sitemap Score: 78/100
