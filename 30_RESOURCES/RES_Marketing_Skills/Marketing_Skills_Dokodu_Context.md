---
type: resource
status: active
owner: kacper
last_reviewed: 2026-05-02
tags: [skille, marketing, dokodu-context, popup, sales, paid-ads, competitor]
---

# Marketing Skills — Dokodu Context Bridge

> 5 skilli zaadaptowanych z [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) (2026-05-02). Pliki SKILL.md zostały **niezmodyfikowane** żeby łatwo było pull'ować updates z upstream. Ten dokument tłumaczy KIEDY i JAK używać każdego z nich w kontekście Dokodu.

---

## /popup-cro

**Skill po angielsku, ale przydatny dla Dokodu w jednym konkretnym scenariuszu:**

### Główny use case dla Kacpra

**Newsletter capture na dokodu.it/blog/** — niskie konwersje email signups z bloga to znaną luka. Skill pokrywa:
- Exit-intent triggers (gdy ktoś chce wyjść z postu)
- Scroll-trigger (np. po 60% scrolla artykułu)
- Frequency capping (max 1x/tydzień, nie spam)
- Mobile vs desktop strategy
- Copy patterns dla email capture

### Kiedy użyć
- Planujesz dodać newsletter popup na blogu (1-time setup)
- Audyt istniejących popupów (jeśli kiedykolwiek dodasz)
- Kampania promocji ebooka jako lead magnet (popup z propozycją download)

### Kiedy NIE używać
- Nie planujesz nigdy popup na dokodu.it (jeśli decyzja UX = zero popupów ever)
- Dla pricing page lub /oferta — to nie jest skill o tym

### Linkuj do
- `Newsletter_Playbook.md` (welcome series po capture)
- `mailerlite-sync` skill (dla list management)

---

## /sales-enablement

**Skill ENG, używany jako uzupełnienie polskiego `Sales_Playbook.md`.**

### Co już masz w Dokodu (NIE duplikuj)
- `Sales_Playbook.md` — Objection Library + Buyer Persona Cards + Pitch Deck Framework (już dodane z tego skilla, 2026-05-02)
- `brain-new-offer` — generator ofert z 2 opcjami cenowymi

### Co skill dodatkowo daje (sięgaj jeśli)
- Tworzysz pełny pitch deck (10-12 slajdów) z slide-by-slide guidance — patrz `references/deck-frameworks.md`
- Piszesz one-pager / leave-behind po spotkaniu — patrz `references/one-pager-templates.md`
- Onboardujesz nowego handlowca w 2026 (Klosin partnership) — pełen skill jako materiał szkoleniowy
- Demo script structure dla CRM Demo Product (prospekt-specific)

### Kiedy użyć
- "Stwórz pitch deck dla Pedrollo" → uruchom skill
- "Napisz one-pager z naszej rozmowy z Animex" → uruchom skill
- Onboarding handlowca: jako reference dla obiekcji, person, pitch decku

### Linkuj do
- `Sales_Playbook.md` jako primary source dla PL kontekstu
- `brain-new-offer` dla generowania ofert

---

## /competitor-profiling

**Skill ENG, do strukturalnego dossier konkurencji/prospektów.**

### Główne use cases dla Dokodu

**1. Pre-step do `/crm-new-demo`**
Przed buildowaniem demo CRM dla prospekta (np. Pedrollo), uruchom najpierw `/competitor-profiling [prospekt-url]`. Output:
- Firmographic (rozmiar, branża, geografia)
- Positioning (jak się prezentują)
- Pricing model (jeśli widoczny publicznie)
- Content strategy (blog, LinkedIn, conferences)
- SEO strength (kluczowe frazy które rankują)
- Słabości (co możesz wykorzystać w demo / pitch)

To zasili lepszy seed danych w demo + da Kacprowi pitch angle.

**2. Analiza konkurencji Dokodu w PL B2B AI**
Profilowanie competitorów typu:
- n8n.io (tool, nie agencja)
- Make / Zapier (tools)
- Polskie agencje AI (jeśli zidentyfikowane jako konkurencyjne)
- AppMaster / no-code agencies

Output: dossier które zasila content strategy (`AREA_Blog_SEO`) + pitch decks (`Sales_Playbook`).

### Kiedy użyć
- Przed `/crm-new-demo` (zawsze, jeśli prospekt jest enterprise)
- Co kwartał: refresh profili top 5 konkurentów Dokodu
- Przed dużym call'em z prospektem (deep dive na nim)

### Kiedy NIE używać
- Dla małych leadów (overkill — wystarczy `/brain-lead-research`)
- Dla rapid kwalifikacji (BANT score wystarczy)

### Linkuj do
- `crm-new-demo` skill (jako pre-step)
- `brain-lead-research` (lżejszy, dla prospect kwalifikacji)
- `Sales_Playbook.md` (dla pitchowania konkurencyjnego)

---

## /paid-ads

**Skill ENG. KEY context: Dokodu jeszcze nie odpalił płatnych kampanii.**

### Status w Dokodu (2026-05-02)
- **Phase B (CAPI server-side tracking) odłożona do pierwszej kampanii płatnej** (memory: `project_social_stack`)
- Nie ma jeszcze ani jednej kampanii Google Ads / Meta / LinkedIn
- Postiz + Kutt postawione pod organic posting na razie

### Kiedy zacząć używać
- Decyzja "odpalamy pierwszą kampanię" → ten skill jest TWOIM playbookiem
- Audyt potencjalnych kampanii zanim wydasz pierwsze 5k zł
- Strategia targetingu / budget allocation

### Co skill pokrywa
- Google Ads (search + display)
- Meta Ads (Facebook + Instagram)
- LinkedIn Ads (kluczowe dla Dokodu — B2B)
- Twitter/X Ads
- Targeting strategies, audience building
- Bidding, ROAS, CPA, retargeting

### Sequence rekomendowanego startu (gdy odpalasz)

1. Najpierw **`/competitor-profiling`** dla 2-3 polskich konkurentów (jak oni reklamują)
2. Potem **`/paid-ads`** dla strategii kampanii
3. Potem **`/ad-creative`** dla generowania wariantów copy
4. **Zanim wydasz pieniądze:** ustaw Phase B trackingu (CAPI) + UTM strategy w GA
5. Pierwsza kampania = mały budżet (1-2k zł) jako learning, nie scale

### Linkuj do
- `ad-creative` (sibling skill dla copy generation)
- `ga-stats` (po kampanii — analiza)
- `Newsletter_Playbook.md` (dla landing page sequence po conversion)

---

## /ad-creative

**Skill ENG. Sibling do `/paid-ads`. Generowanie ad copy at scale.**

### Główne use cases dla Dokodu

**1. Hostinger affiliate KACPER10**
Pisanie wariantów ad copy dla afiliacji Hostinger (n8n self-hosted, VPS dla AI):
- RSA headlines dla Google Ads (wariantów + testowanie)
- LinkedIn ad text (bardziej formalne, B2B)
- Carousel copy dla LinkedIn

**2. Promo szkoleń otwartych**
Gdy odpalasz cykliczne szkolenia (M365 Copilot, n8n basics), skill generuje:
- 10-15 wariantów headline'ów
- A/B test pairs
- Long-form vs short-form copy
- Creative testing methodology

**3. Future: paid ads dla CRM Demo Product**
Gdy CRM Demo dojrzeje do skalowania:
- Multi-variant ad copy dla różnych branż (Pedrollo, HABA, etc.)
- Industry-specific value props

### Kiedy użyć
- Tworzenie nowej kampanii ads (po `/paid-ads` strategii)
- Iteracja istniejących reklam (gdy CTR słaby)
- Bulk generowanie wariantów dla A/B testów
- Affiliate creative (Hostinger KACPER10)

### TOV adapter dla Dokodu
Skill ma defaultowo US-style salesy copy. **Zaadaptuj** do TOV Kacpra:
- Bezpośredni, ciepły, anti-hype (memory: `feedback_linkedin_tone`)
- Konkretne PL liczby (nie ekstrapolować z USD — memory: `feedback_grounded_numbers`)
- Reflinki z kontekstem (Hostinger w postach n8n/VPS — memory: `project_hostinger_affiliate`)

### Linkuj do
- `paid-ads` (strategia campaign)
- `Affiliate_Links.md` (Hostinger / inne affiliates)
- `seo-research` (jeśli chcesz użyć tych samych keywords w paid + organic)

---

## Workflow rekomendowany — pełen pipeline marketingowy

Gdy zaczniesz nową inicjatywę marketingową (np. promocja kursu n8n / launch ebooka / nowa usługa):

```
1. /seo-research [temat]                  — co działa w SEO/PL?
2. /competitor-profiling [konkurenci]     — jak konkurencja podchodzi?
3. /content-strategy (już w AREA_Blog_SEO) — pillar + buyer stage mapping
4. /seo-plan-post + /blog-draft           — content (organic)
5. /popup-cro (1-time setup)              — capture na blogu
6. Newsletter_Playbook                    — welcome series po capture
7. /sales-enablement                      — pitch deck/one-pager
8. /paid-ads + /ad-creative               — kampania płatna (jeśli budżet)
9. /ga-stats + /seo-stats                 — pomiar
```

Nie wszystko naraz. Wybierasz subset wg fazy i budżetu.

---

## Update strategy

Gdy upstream `coreyhaines31/marketingskills` zaktualizuje skille:

```bash
cd /tmp && rm -rf marketingskills && git clone --depth 1 https://github.com/coreyhaines31/marketingskills.git
# Per skill diff:
diff -r /tmp/marketingskills/skills/popup-cro .claude/skills/popup-cro
# Cherry-pick zmiany ręcznie albo replace całość:
cp -r /tmp/marketingskills/skills/popup-cro .claude/skills/
```

Sprawdź `VERSIONS.md` w upstream repo dla changelog.

---

## Co świadomie SKIP (zgodnie z audytem 2026-05-02)

Te skille z marketingskills **nie pasują** do Dokodu — nie kopiowałem ich:

| Skip | Powód |
|---|---|
| `paywall-upgrade-cro`, `signup-flow-cro`, `onboarding-cro`, `churn-prevention` | Dokodu = projekty na umowach, nie freemium SaaS |
| `directory-submissions`, `launch-strategy`, `free-tool-strategy` | Agencja usługowa, nie produkt |
| `community-marketing` | Strategia = LinkedIn-influence Kacpra, nie Discord/Slack |
| `revops` | 1-osobowy pipeline, MQL/SQL routing = overkill |
| `aso-audit` | NiebieskiKalendarz to projekt żony, poza systemem |
| `video` (AI gen) | Konflikt z TOV — Kacper nagrywa twarzą do kamery, nie chce HeyGen avatars |
| `product-marketing-context` | `001_VISION.md` + `Sales_Playbook.md` to są — duplikat SoT |
| `ai-seo`, `schema-markup`, `seo-audit`, `programmatic-seo`, `page-cro`, `site-architecture`, `ab-test-setup`, `analytics-tracking` | Już pokryte przez `seo-*` stack Dokodu |

Pełen audyt + powody w transkrypcji rozmowy z 2026-05-02 (lub spawn nowej rozmowy z `/brain-capture`).
