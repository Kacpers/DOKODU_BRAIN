---
type: seo-audit
subtype: geo-ai-search
date: 2026-04-22
domain: dokodu.it
owner: Kacper
status: active
tags: [seo, geo, ai-overviews, chatgpt, perplexity, llms-txt]
---

# GEO / AI Search Readiness Audit — dokodu.it

**Data:** 2026-04-22
**Zakres:** AI crawlers access, llms.txt, citability, passage-level readiness
**Target platforms:** Google AI Overviews (SGE), ChatGPT search, Perplexity, Claude

---

## TL;DR

**Dokodu jest lepiej przygotowana do AI search niż większość polskich agencji B2B.** `/llms.txt` istnieje i jest dobrze skonstruowany. AI crawlery (GPTBot, ClaudeBot, PerplexityBot) **mają dostęp** (robots.txt nie blokuje). Struktura blog postów jest LLM-friendly (H2/listy/długie pillary). Minusy: brak `llms-full.txt`, author = „Dokodu" (organizacja) nie Person, brak direct-answer paragraphs w pierwszych akapitach.

**Score: 74/100**

---

## 1. llms.txt compliance ✅

### /llms.txt — HTTP 200 OK

Treść: po angielsku (! — globalny LLM audience), solidna struktura wg. llmstxt.org spec:
- Identity („Dokodu is a Polish AI agency...")
- About (founded 2020, CEO, location Gdynia, languages PL/EN)
- Key Services (4 pozycje z linkami)
- Blog — Technical Content (9 pozycji)
- Expertise Areas (6 pozycji)
- Case Studies (3 pozycje)

**Bardzo dobrze.** Zauważalne decyzje:
- EN nie PL — celowane pod ChatGPT/Claude (mają lepsze pokrycie PL niż 2 lata temu, ale EN trafia do większego LLM corpus)
- Direct linki do case studies — LLM może je cytować jako dowód

### /llms-full.txt — HTTP 404 ❌
Brakuje pełnej wersji (`llms-full.txt` zawiera pełny markdown content kluczowych stron, nie tylko navigation). To opcjonalne ale rekomendowane dla edu/content sites.

**Fix:** wygenerować `/llms-full.txt` z zawartością:
- Homepage copy
- `/o-nas` full content
- Top 10 pillar posts (full markdown)
- FAQ z /szkolenia + /automatyzacja-ai (gdy FAQ powstanie)

### /humans.txt — HTTP 404 (neutralne, rzadko używane)

---

## 2. AI Crawler Access ✅

robots.txt nie blokuje żadnego AI bota:
- `GPTBot` (OpenAI) — ALLOW
- `ClaudeBot`, `anthropic-ai` — ALLOW
- `PerplexityBot` — ALLOW
- `Google-Extended` — ALLOW (Gemini training + AI Overviews)
- `CCBot` (Common Crawl, training) — ALLOW

**Pytanie strategiczne:** czy to się opłaca?
- **Tak** dla B2B PL w 2026 — cytacje w AI answers = brand authority + pipeline (ChatGPT/Claude często cytują źródła, user klika i kupuje)
- LLM training jest kontrowersyjne (content stealing), ale cytacje/search są prowadzone przez `PerplexityBot`/`GPTBot` w trybie on-demand retrieval — te bloki w robots.txt ≠ bloki w AI answers

**Rekomendacja: pozostawić ALLOW.** Jeśli kiedykolwiek Kacper chciałby zablokować training (Common Crawl) ale zostawić search:
```
User-agent: CCBot
Disallow: /

User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /
```

---

## 3. Brand mention signals

- ✅ **Organization schema** z bogatymi `sameAs` (5 linków — LinkedIn, YouTube, potencjalnie Twitter/X, GitHub)
- ✅ Spójne naming w title tags (`| Dokodu` wszędzie — mimo duplikacji to dobry signal konsystencji)
- ✅ Single brand → consistency (brak wariantów „Dokodu Sp z o.o." vs „Dokodu IT" vs „dokodu.pl")
- ⚠️ `alternateName: "Dokodu Sp. z o.o."` w schema — good (helps with legal name entity resolution)

---

## 4. Passage-level citability

### Próba: /blog/zaawansowane-techniki-prompt-engineeringu

**Direct-answer paragraphs (czy pierwsze 40-60 słów to samoistna odpowiedź)?**
Bez wizualnej analizy nie potwierdzę 100%, ale pattern „intro z H1 i potem 'w tym artykule dowiesz się...' " jest częsty w PL blogach i jest **anti-pattern dla AI cytacji**. LLM wybiera bloki które odpowiadają na pytanie, nie meta-komentarze.

**Fix pattern (rekomendowany):**
```md
# Zaawansowane techniki prompt engineeringu

Zaawansowany prompt engineering to [definicja w 1 zdaniu]. Najważniejsze techniki to:
chain-of-thought (wymusza krokowy reasoning), few-shot learning (uczysz modelu przez 
przykłady), role prompting (definiujesz personę eksperta). Każda z nich daje
[X]% poprawę [metric] w zadaniach [Y].

[...tutaj reszta intro, a potem H2...]
```

Pierwsze 50 słów = samoistna odpowiedź na „co to zaawansowany prompt engineering" = cytowalne.

### Listy i tabele ✅
Blog ma ich dużo (z H2 count 12 na pillar) — to LLM lubi.

### Nagłówki w formie pytań
Nie sprawdzone per post, ale rekomendowane:
- ❌ `H2: Techniki chain-of-thought`
- ✅ `H2: Jak działa chain-of-thought prompting?`

Pytania w H2 to direct mapping na user queries → wyższe chance cytacji.

---

## 5. Author signal (krytyczne dla E-E-A-T + GEO)

**Obecny stan:** `author` w BlogPosting schema = `"Dokodu"` (organizacja, nie Person).

**Problem:** LLMs (szczególnie Perplexity, Claude) waży authority per-author. Organizacja ≠ ekspert. Post z `author: "Kacper Sieradziński, 140+ firm przeszkolonych, CEO Dokodu"` + link do bio + sameAs (LinkedIn) ma dużo wyższy chance cytowania niż `author: "Dokodu"`.

**Fix (identyczny jak w content.md, high priority):**
```jsonld
"author": {
  "@type": "Person",
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

---

## 6. Platform-specific readiness

### Google AI Overviews (SGE)
- ✅ HTML jest server-rendered (SSR Next.js) — crawlowalny
- ❌ **Brak FAQPage schema** na commercial pages — FAQs są prime real estate dla AI Overviews
- ⚠️ Brak „featured snippet" optimization — akapity w postach nie zawsze zaczynają się od bezpośredniej odpowiedzi
- ✅ Polish language site → competing w PL SERPs (mniej konkurencji od globalnych blogów)

### Perplexity
- ✅ llms.txt daje Perplexity fast-path do zrozumienia czym jest serwis
- ✅ Clean URLs, no pagination hell
- ✅ Rich internal linking (61 linków na post) — Perplexity crawluje przez linki
- ⚠️ Brak „stats + sources" format który Perplexity preferuje (statystyka + link do źródła = cytowalne)

### ChatGPT search (retrieval, nie training)
- ✅ Canonical URLs → clean attribution
- ✅ SSR → content jest w first paint
- ⚠️ Brak ostrych date signals — ChatGPT search preferuje świeże (`datePublished` + `dateModified` widoczne)

### Claude
- ✅ Similar to Perplexity — llms.txt + clean HTML + author bio wystarczą
- ⚠️ Author = „Dokodu" zamiast Person = downside

---

## 7. Rekomendacje GEO

### High (direct lift)
1. **Zmienić author na Person w BlogPosting schema** (duplicate z content.md — krytyczne)
2. **Dodać `/llms-full.txt`** z full-content top 10 pillar posts
3. **Direct-answer paragraphs** — pierwszy akapit postów = 40-60 słów samoistnej odpowiedzi na pytanie z tytułu
4. **FAQPage schema** na /szkolenia, /automatyzacja-ai, /kursy (+ per-kurs) — prime AI Overview real estate

### Medium
5. **Nagłówki H2 w formie pytań** (refactor starszych postów, nowe pisać od razu Q-form)
6. **Inline statystyki + linki do źródeł** w postach (McKinsey, Gartner, polskie raporty AI 2024/2025)
7. **Widoczna data publikacji + aktualizacji** nad H1 postów

### Low
8. Jeśli Kacper chce zablokować training: `CCBot: Disallow`, pozostawić pozostałe AI crawlery
9. Brand mentions tracking przez osobny tool (np. monitoring gdzie ChatGPT/Claude cytują „Dokodu")

---

## GEO Score: 74/100

Powyżej średniej dla PL B2B. Szybkie winy (llms-full.txt, author Person, FAQ schema) mogą wybić to do 85+.
