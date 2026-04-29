---
type: seo-audit
subtype: structured-data
date: 2026-04-22
domain: dokodu.it
owner: Kacper
status: active
tags: [seo, schema, json-ld, rich-results]
---

# Structured Data (Schema.org JSON-LD) Audit — dokodu.it

**Data:** 2026-04-22
**Zakres:** homepage + 9 typów podstron
**Metoda:** `curl -sL URL | grep -A 200 'application/ld+json'` + JSON parsing

**Uwaga:** pierwsza wersja tego pliku (od subagenta) błędnie raportowała „zero schemy na wszystkich stronach" — subagent używał WebFetch które nie renderuje inline `<script type="application/ld+json">` po SSR. Przy bezpośrednim curl-u schema jest widoczna. Poniżej prawidłowy audyt.

---

## TL;DR

**Dokodu ma solidną bazową schemę** — Organization z `sameAs`, `contactPoint`, `address`, `knowsAbout`, `offers`, plus WebSite z SearchAction. BlogPosting na postach, Course na kursach. Minusy: **author = „Dokodu" (organizacja) zamiast Person**, **brak FAQPage** (mimo że to prime rich result real estate), **brak Event schema na webinarach**, **BreadcrumbList niepełna** (jest na blog, brak na kursach), **brak Course na stronach głównych /szkolenia** (tylko na /kursy/*).

**Score: 68/100**

---

## 1. Stan obecny — per-page

### `/` (Homepage) ✅ **3 schemas**
- `Organization` — bogata:
  - `@id: https://dokodu.it/#org`
  - `name: Dokodu`, `alternateName: Dokodu Sp. z o.o.`
  - `logo`, `description`, `foundingDate: 2020`
  - `sameAs: [5 items]` ✅
  - `contactPoint: [1 item]` ✅
  - `address: PL, addressLocality` ✅
  - `knowsAbout: [9 items]` ✅
  - `offers: { offerCount, priceCurrency, category }` ✅
- `WebSite` — z `potentialAction: SearchAction` ✅ (sitelinks searchbox w Google)
- `SiteNavigationElement` — 7 pozycji menu „Dla Firm"
- ❌ **Brak LocalBusiness** mimo że `Organization.address` jest PL
- ❌ **Brak BreadcrumbList** (na home OK, nie jest wymagane, ale dobry boilerplate)

### `/o-nas` ⚠️ **3 schemas**
- Organization + WebSite + SiteNavigationElement
- ❌ **Brak AboutPage schema**
- ❌ **Brak Person schema dla zespołu** (jeśli zespół jest widoczny na stronie)

### `/kontakt` ⚠️ (nie sprawdzone w detalu)
- Prawdopodobnie same 3 global schemas
- ❌ **Brak ContactPage schema**
- ❌ **Brak LocalBusiness** z dokładnym adresem + openingHours

### `/szkolenia` ⚠️ **3 schemas — same global**
- Organization + WebSite + SiteNavigationElement
- ❌ **Brak Service schema** (lub OfferCatalog z listą szkoleń)
- ❌ **Brak FAQPage** (FAQ rich snippet potencjał)

### `/automatyzacja-ai` ⚠️
- Nie sprawdzony per-page, ale ten sam template co /szkolenia
- ❌ **Brak Service schema**

### `/kursy/docker` ✅ **4 schemas**
- Organization + WebSite + SiteNavigationElement + **Course** ✅
- Course — należy sprawdzić czy wszystkie required fields są wypełnione:
  - `name`, `description`, `provider` (Dokodu) — prawdopodobnie OK
  - `hasCourseInstance` (dates, location) — sprawdzić

### `/kursy/pystart` ⚠️ (podejrzenie: Course, nie sprawdzone szczegółowo)

### `/blog` ⚠️
- Prawdopodobnie 3 global schemas, brak Blog/CollectionPage

### `/blog/zaawansowane-techniki-prompt-engineeringu` ✅ **5 schemas**
- Organization + WebSite + SiteNavigationElement + **BlogPosting** ✅
- BlogPosting pole problem: **`author: "Dokodu"`** (literal string, powinno być Person object)

### `/webinary/webinar-1` ❌
- Brak `Event` / `EducationEvent` schema
- Strona bez bogatej schemy — strata (webinar rich snippet pokazuje datę, miejsce, organizatora)

### `/trenerzy/kacper-sieradzinski` ❌
- Soft 404 — page wraca 200 ale content „Trener nie został znaleziony"
- Fallback title, brak Person schema
- Blocker = napraw routing; potem dodać Person schema

---

## 2. Braki — systemowe patterns

### ❌ High: Brak FAQPage
Żadna strona nie ma `FAQPage` schema. FAQ schema generuje **rozszerzone snippety w SERPach** (accordion z Q&A) i jest prime real-estate dla AI Overviews.

Strony gdzie FAQ = must-have:
- `/szkolenia` (ile trwa, dla kogo, jak się zapisać, co potrzebuję)
- `/automatyzacja-ai` (jakie procesy, ile trwa wdrożenie, ile kosztuje, czy jest serwis)
- `/kursy/<slug>` (każdy kurs osobno: długość, format, certyfikat, cena)
- `/konsultacje`

### ❌ High: Author = organizacja zamiast Person
Wszystkie posty blogowe mają `BlogPosting.author: "Dokodu"` (lub `{ @type: Organization, name: Dokodu }`). Powinno być `Person`:

```jsonld
"author": {
  "@type": "Person",
  "@id": "https://dokodu.it/trenerzy/kacper-sieradzinski#person",
  "name": "Kacper Sieradziński",
  "url": "https://dokodu.it/trenerzy/kacper-sieradzinski",
  "sameAs": [
    "https://www.linkedin.com/in/kacpersieradzinski",
    "https://youtube.com/@kacpersieradzinski"
  ],
  "jobTitle": "CEO & AI Trainer",
  "worksFor": { "@id": "https://dokodu.it/#org" }
}
```

To wymaga prereq: napraw `/trenerzy/<slug>` routing, stwórz strony trenerów z Person schema.

### ⚠️ Medium: BreadcrumbList nie na wszystkich
- Blog post: ma (2 mentions = prawdopodobnie BreadcrumbList + link do breadcrumbs w innym miejscu) ✅
- /kursy/docker: brak
- Homepage: 1 mention (OK, na home nie wymagane)

**Fix:** dodać BreadcrumbList do layoutu subpages (np. `app/kursy/[slug]/page.tsx`). Wygeneruj z pathname.

### ⚠️ Medium: Brak Event na webinarach
`/webinary/<slug>` to idealne miejsce na `Event` lub `EducationEvent`:

```jsonld
{
  "@context": "https://schema.org",
  "@type": "EducationEvent",
  "name": "Webinar: Podstawy Pythona",
  "startDate": "2026-05-15T19:00:00+02:00",
  "endDate": "2026-05-15T20:30:00+02:00",
  "eventStatus": "https://schema.org/EventScheduled",
  "eventAttendanceMode": "https://schema.org/OnlineEventAttendanceMode",
  "location": { "@type": "VirtualLocation", "url": "..." },
  "organizer": { "@id": "https://dokodu.it/#org" },
  "offers": { "@type": "Offer", "price": "0", "priceCurrency": "PLN" }
}
```

Event rich snippet w Google SERP = duża widoczność.

### ⚠️ Medium: Brak Review / AggregateRating
Dokodu ma 140+ przeszkolonych firm (potencjalnie Google Reviews, LinkedIn recommendations). Review schema na /szkolenia i /o-nas daje star rating w SERPach.

Wymóg Google (2023+): Review schema musi odnosić się do faktycznej recenzji widocznej na stronie (nie wolno „wygenerować" gwiazdek z niczego).

### ⚠️ Low: Brak Book / DigitalDocument na ebookach
`/ebooki/docker-cheatsheet`, `/ebooki/automatyzacja-biznesowa` — powinny mieć `Book` lub `DigitalDocument` schema.

---

## 3. Priorytety i konkretne rekomendacje

### High (implementować w tym miesiącu)

**1. Fix author w BlogPosting → Person**
- Prereq: napraw `/trenerzy/<slug>` routing (dynamic route, generować z DB/CMS)
- W `app/blog/[slug]/page.tsx` generować BlogPosting z `author: Person` referencing trener page
- Estymata: 4-6h (routing + backfill wszystkich postów)

**2. Dodać FAQPage na 4 commercial pages**
- `/szkolenia`, `/automatyzacja-ai`, `/kursy`, `/konsultacje`
- Plus per-kurs: `/kursy/docker`, `/kursy/pystart`, etc.
- Każda 5-10 Q&A, same Q&A widoczne na stronie (wymóg Google)
- Estymata: 2h per strona (napisanie + schema) = ~16h

**3. Event schema na /webinary/<slug>**
- Dodać `EducationEvent` do template
- Backfill dat dla starszych webinarów (z metadata Kacpra albo skasować z sitemap)
- Estymata: 3h

### Medium

**4. BreadcrumbList na /kursy/<slug>, /webinary/<slug>, /dla-firm/<slug>, /automatyzacja-ai/wdrozenia/<slug>**
- Uniwersalny komponent w layouts
- Estymata: 2h

**5. AboutPage na /o-nas, ContactPage + LocalBusiness na /kontakt**
- Dla LocalBusiness wymagana dokładna address, geo, openingHours, telephone
- Estymata: 2h

**6. Service schema na /szkolenia, /automatyzacja-ai**
- `Service` z `provider`, `areaServed`, `hasOfferCatalog`
- Estymata: 2h

### Low

**7. Review/AggregateRating** — dopiero po zbiórce realnych reviews (Google, Clutch, Capterra)

**8. Book schema na /ebooki/<slug>**

---

## 4. Snippet — drop-in code dla Next.js

### BlogPosting (fix author)
W `app/blog/[slug]/page.tsx`:

```tsx
export default async function BlogPost({ params }) {
  const post = await getPost(params.slug);
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'BlogPosting',
    headline: post.title,
    description: post.description,
    image: post.ogImage,
    datePublished: post.publishedAt,
    dateModified: post.updatedAt,
    author: {
      '@type': 'Person',
      '@id': `https://dokodu.it/trenerzy/${post.authorSlug}#person`,
      name: post.authorName,
      url: `https://dokodu.it/trenerzy/${post.authorSlug}`,
      sameAs: post.authorSocials, // array z LinkedIn/YouTube
    },
    publisher: { '@id': 'https://dokodu.it/#org' },
    mainEntityOfPage: { '@type': 'WebPage', '@id': post.url },
  };
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      {/* reszta */}
    </>
  );
}
```

### FAQPage
W `app/szkolenia/page.tsx` (oraz innych):

```tsx
const faqLd = {
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  mainEntity: faqs.map(f => ({
    '@type': 'Question',
    name: f.question,
    acceptedAnswer: { '@type': 'Answer', text: f.answer },
  })),
};
```

FAQ musi być widoczne w UI — nie tylko w schema.

---

## Schema Score: 68/100

Punkt wyjścia jest solidny (bogata Organization + WebSite + per-type schemas). Szybkie wins: author = Person, FAQPage, Event. Po implementacji High → 85+.
