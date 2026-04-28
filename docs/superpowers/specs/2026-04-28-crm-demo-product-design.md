---
title: Dokodu CRM — Demo Product Design
date: 2026-04-28
status: design-approved
owner: Kacper Sieradzinski
type: spec
related:
  - /Users/ksieradzinski/Projects/dokodu/crm-new
  - 20_AREAS/AREA_Customers/Pedrollo
  - 20_AREAS/AREA_Customers/HABA
tags: [crm, product, sales-tool, demo, multi-tenant]
---

# Dokodu CRM — Demo Product Design

## Cel produktu

Stworzyć **showroom CRM** sprzedawany jako pakiet 15-20k jednorazowo + miesięczne utrzymanie (~TBD), instalowany na serwerze klienta. Pozycjonowanie: „mniejsze niż Bitrix/Odoo, ale mądrzejsze" — dla średnich firm B2B (50-150 osób) uciekających od overkill rozwiązań.

Pierwsi klienci: **Pedrollo** (pompy, B2B do instalatorów/dystrybutorów), **HABA** (przydomowe oczyszczalnie, B2B+B2C, długie cykle, dokumentacja techniczna).

Model sprzedaży: demo dopasowane do brandu klienta („dam Ci pedrollo.pl, w 5 minut masz ich CRM") → prezentacja na żywo (2-3 osoby decyzyjne) → iteracja na demie → migracja na ich serwer → miesięczny retainer na utrzymanie.

## Strategia

**Model B z brainstormu**: showroom funkcjonalności + custom build per klient. Demo NIE jest produktem off-the-shelf — to bazowy fundament, na którym usiądziemy z klientem i ulepimy z klocków pod ich procesy.

**Filozofia UX**: nie wymyślamy koła na nowo. Opieramy się na sprawdzonych UX (Monday, Linear, Pipedrive, Notion) z polską wisienką: **mocne filtry + galeria zapisanych widoków + AI input layer**.

**Anti-patterns** (czego nie robimy):
- Asana — głębokie zagnieżdżanie projektów w projektach (przerost wyboru)
- Bitrix — 200 ikon w sidebarze, każdy moduł inne UI
- Odoo — wszystko można konfigurować = nic nie jest skonfigurowane
- Salesforce — lokal-firma feeling przez 99 zakładek

## Architektura — 4 fazy lifecycle instancji

```
FAZA 0 — DRAFT DEMO (config-only, monorepo)
  Repo: dokodu/crm-new (master)
  Konfig: clients/{slug}/{theme.json, seed.json, modules.json}
  Deploy: dev.dokodu.it/crm-{slug}
  Cel: pierwsza prezentacja, klient mówi „TAK w 80%"
  Schema: master schema (BEZ MODYFIKACJI)
  Code: master code (BEZ MODYFIKACJI)

         │  /brain-crm-fork-prospekt {slug}
         │  (po pozytywnym pierwszym demie)
         ▼

FAZA 1 — FORK (własny repo)
  Repo: dokodu/crm-{slug} (private GitHub)
  Deploy: ten sam URL dev.dokodu.it/crm-{slug} ale z fork repo
  Cel: iteracja z klientem, schema zmiany OK, własne moduły, własna ścieżka
  Master deploy NIE wpływa na to. Bug fixy cherry-pick'ujemy.

         │  klient podpisuje umowę
         ▼

FAZA 2 — PRODUKCJA
  Repo: dokodu/crm-{slug} (ten sam)
  Deploy: crm.{klient}.pl (ich serwer, ich infra)
  Migracja: pg_dump z dev → restore na prod, theme + config + dane idą razem
  Backup: dzienny do S3/lokalny dysk klienta

         │  ciągły retainer miesięczny
         ▼

FAZA 3 — UTRZYMANIE
  Bug fix w core master? `git cherry-pick` do każdego klient repo
  Klient prosi o nowy moduł? Kopiujemy folder modules/X/ z innego repo, dostosowujemy
```

**Kluczowe decyzje architektoniczne**:

1. **Schema klienta MOŻE się różnić od mastera.** Świadomy wybór typowania/speed nad uniwersalnością. Klient chce „status_kredytu_klienta" jako kolumnę → modyfikujemy schemat. Bez EAV/many-to-many do udawania elastyczności.
2. **Odcięcie pępowiny = real fork** po pierwszym pozytywnym demie. Osobny git repo, osobne PR-y, osobne życie.
3. **Moduły to samodzielne foldery do kopiuj-wklej** (`modules/{nazwa}/`), nie pluginy w plugin-architekturze. Każdy moduł zawiera schema-extension, routes, UI, seed, README.
4. **Drift management**: bug fixy w core warstwach rzadko zmienianych (auth, RBAC, audit log) cherry-pick'ujemy do wszystkich klientów. Zasada: trzymamy core jak najmniejszy. Każda funkcja w wątpliwości → moduł.

### Struktura monorepo (master)

```
crm-new/
├── core/                       # niezmienialny rdzeń (auth, RBAC, framework)
│   ├── prisma/schema.prisma    # core entities
│   ├── lib/                    # auth, audit, validation
│   └── components/ui/          # shadcn (przed modifikacjami)
├── modules/                    # samodzielne moduły
│   ├── allegro/
│   │   ├── schema.prisma       # extensions only
│   │   ├── api/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── seed.ts
│   │   ├── module.config.ts    # registracja: nazwa, ikona, permissions
│   │   └── README.md
│   ├── ifirma/
│   ├── n8n-connector/
│   ├── mailerlite/
│   └── ...
├── themes/                     # generated themes
│   └── pedrollo/
├── seed-bundles/               # pre-built data per branża
│   ├── distribution-b2b/
│   ├── manufacturing/
│   └── installation-services/
├── clients/                    # FAZA 0 only — config per prospekt
│   └── pedrollo/
│       ├── theme.json
│       ├── seed.json
│       └── modules.json
├── scripts/                    # dev tooling
│   └── theme-from-url.ts
└── docs/
    ├── data-map.md             # auto-generated PII inventory
    └── modules/                # per moduł docs
```

### BRAIN skille (operacyjna warstwa)

| Skill | Faza | Co robi |
|---|---|---|
| `/crm-new-demo {url}` | 0 | Fetch brandu, generate seed dla branży, deploy → `dev.dokodu.it/crm-{slug}` |
| `/crm-tweak-theme {slug}` | 0/1 | Otwiera lokalny preview theme, pozwala swapnąć kolory przed pushem |
| `/crm-fork-prospekt {slug}` | 0→1 | Tworzy `dokodu/crm-{slug}` repo, deploy z fork repo |
| `/crm-add-module {slug} {moduł}` | 1/2/3 | Kopiuje moduł z master/innego klienta do klient repo |
| `/crm-migrate-to-prod {slug} {server}` | 1→2 | Push na ich serwer + setup SSL + backup config |
| `/crm-sync-from-master {slug} {commit}` | 2/3 | Cherry-pick'uje commit z mastera (bug fix) |
| `/crm-update {slug}` | 2/3 | Rolling update tej instancji do najnowszego stable |
| `/crm-status` | wszystkie | Listuje aktywne instancje, ich fazy, ostatnie deploye, backupy |

## UX Framework

### Trzy zasady fundamentalne

1. **Never lose context.** Kliknięcie w deal → drawer z prawej (~50% ekranu), nie nowa strona. Tablica widoczna pod spodem. Kolejny deal bez powrotu na listę. Anti-Asana, anti-Pipedrive.
2. **Naucz się raz, używaj wszędzie.** Każda karta encji (deal/projekt/kampania/task) ma identyczny header layout. Każda tablica ma te same 4 widoki, te same skróty, ten sam mechanizm filtrów.
3. **Cmd+K + przycisk jako pierwszy obywatel.** Pasek górny ma JEDNO pole „Szybka akcja / AI" (klikalne i shortcut Cmd+K). Sales rep w Pedrollo nie musi znać shortcutów — primary UX musi działać myszką.

### Layout

```
┌──────────────────────────────────────────────────────────────────────┐
│ [Logo klienta]   [⚡ Szybka akcja / AI (Cmd+K)]              🔔  KS  │
├──────────┬───────────────────────────────────────────────────────────┤
│          │                                                            │
│ 📊 Sales │   [Tytuł tablicy]  Kanban / Lista / Kalendarz / Timeline  │
│  Pipeline│   [Mój] [Q2] [Hot leads] [+]   [Saved view ▼]   [Filtry] │
│  Leady   │                                                            │
│  Klienci │   [Karty drag-droppable w kolumnach pipeline]              │
│          │                                                            │
│ 📣 Mktg  │                                                            │
│  Kampanie│                                                            │
│  Listy   │                                                            │
│          │                                                            │
│ ⚙ Ops    │                                                            │
│  Projekty│                                                            │
│  Faktury │                                                            │
│  Tasks   │                                                            │
│          │                                                            │
│ 👥 Baza  │                                                            │
│  Firmy   │                                                            │
│  Osoby   │                                                            │
│  Produkty│                                                            │
│          │                                                            │
│ ─────    │                                                            │
│ ⚙ Ustaw. │                                                            │
└──────────┴───────────────────────────────────────────────────────────┘
```

Sidebar **organized by department**, nie przez typy danych. Klient widzi „Sales / Marketing / Operations / Baza" — tak jak myśli o swojej firmie. Modular — wyłączasz moduł Marketing, znika cała sekcja.

### Cztery widoki per tablica

- **Kanban** (default dla procesów) — drag-drop, kolumny = stages
- **Lista** — sortable table z konfigurowalnymi kolumnami (à la Monday)
- **Kalendarz** — karty po datach (follow-up date deala, due date taska)
- **Timeline** — Gantt-like, dla projektów i milestones

Filtry persistują przy zmianie widoku.

### Filtry — galeria trzy poziomy

1. **Tab strip nad tablicą** — najczęściej używane filtry jako zakładki, jak w przeglądarce. Klik = natychmiastowa zmiana. Default „Wszystkie" + 5-6 user-pinned.
2. **Sidebar expand** — pod tablicą rozwija się lista *moich* zapisanych widoków (jak Linear). Drag żeby przestawiać.
3. **Galeria w ustawieniach tablicy** — pełne zarządzanie wszystkich widoków (moje + zespołu), share/private toggle.
4. **Smart auto-suggest** — gdy user 3× pod rząd używa tego samego zestawu filtrów, dyskretne „💡 Zapisz ten widok?" w prawym górnym rogu.

### Drawer encji

```
                                    ┌─────────────────────────────┐
                                    │ ▢ Acme sp. z o.o. — Wycena  │
                                    │ KS │ 120k PLN │ 30% │ ★ ABC │
                                    ├─────────────────────────────┤
                                    │ Activity│Taski│Pliki│Powiąz.│
                                    ├─────────────────────────────┤
                                    │ [timeline aktywności]       │
                                    │ [🤖 AI: streszcz / next]    │
                                    │ [+ szybko: notatka, follow] │
                                    └─────────────────────────────┘
```

Edycja inline (klik w pole, wpisz, Tab przechodzi do następnego).

## Showroom — co konkretnie pokazujemy

### CORE (zawsze, w cenie 15-20k)

| Sekcja sidebar | Zawartość | Default tablice/widoki |
|---|---|---|
| **📊 Sales** | Pipeline z customizable stages, leady, karta firmy z timeline, karta osoby z roli (decision maker/champion/blocker), forecast | „Pipeline główny", „Leady → kwalifikacja", „Hot deale Q2" |
| **📣 Marketing** | Tablica kampanii (Plan→Aktywne→Zakończone), listy mailingowe oparte na tagach/segmentach, content calendar | „Kampanie 2026", „Newsletter pipeline" |
| **⚙ Operations** | Tablica projektów (Onboarding→W realizacji→Dostawa→Retainer), milestones, time tracking | „Projekty aktywne", „Onboarding", „Retainery" |
| **✅ Tasks** | Tablica zadań osobista i zespołowa, powtarzalne, „Mój dashboard" | „Mój dzień", „Zaległe", „Tydzień zespołu" |
| **👥 Baza** | Firmy, kontakty, produkty (proste — nazwa/opis/cena/jednostka), dokumenty | (lista, nie tablica) |
| **🤖 AI Center** | Cmd+K input, historia AI promptów, AI insights | (osobny widok) |

### ADD-ON MODUŁY (płatne, znaczone „+", dorzucamy per klient lub upsell)

| Moduł | Dla kogo | Co robi |
|---|---|---|
| Allegro / BaseLinker | Pedrollo, HABA | Sync zamówień, produkty z marketplace'u jako leady |
| iFirma / Fakturownia | Wszyscy | Auto-faktura z deala, status płatności, sync księgowy |
| n8n connector | Klienci pro-automatyzacja | Webhook hub do/z n8n |
| MailerLite / Mailjet | Marketing-heavy | Wysyłka kampanii z segmentów, tracking |
| Slack / Teams | Większe firmy | Notyfikacje deali, daily digest, AI summary |
| WhatsApp Business | Pedrollo (instalatorzy WhatsApp) | Threading rozmów per kontakt |
| Branżowy: Dystrybucja | Pedrollo | Stany magazynowe, RMA, rozliczenia |
| Branżowy: Instalacje | HABA | Harmonogram montaży, ekipy, raporty serwisowe |

### Demo flow podczas prezentacji (15-20 min)

1. **Hook (1 min)** — otwierasz `dev.dokodu.it/crm-pedrollo`, na ekranie LOGO PEDROLLO, kolory pedrollowe, w bazie ich własne dane (8 prawdziwych firm-klientów Pedrollo, próbka produktów). „To jest CRM zrobiony pod Was."
2. **Pipeline + drag-drop (3 min)** — przesuwasz deal, history, forecast.
3. **Cmd+K AI (2 min)** — „Klient X dzwonił, chce spotkanie, przygotuj wycenę 50k" → tworzy deal + task + reminder.
4. **Widoki + filtry (2 min)** — pipeline jako kalendarz, jako lista, filtruj „>100k", zapisujesz widok.
5. **Karta firmy (2 min)** — drawer, timeline aktywności, dokumenty, AI summary.
6. **Cross-team (3 min)** — sales zamyka deal jako Won → automat tworzy Projekt → Operations widzi nowy projekt.
7. **Settings (1 min)** — można edytować stages, dodać kolumnę, włączyć moduł.
8. **Reliability (1 min)** — backupy, monitoring, response time.
9. **Pricing (2 min)** — 15-20k jednorazowo + miesięczne utrzymanie. Add-ony per moduł.

## Theme-from-URL pipeline

### Flow

1. **Fetch + render** — Playwright odpala headless Chromium, czeka na network idle, screenshot strony głównej + 2-3 podstron, zapisuje DOM + computed styles.
2. **Ekstrakcja brandu**:
   - **Logo** — kolejność: `<link rel="icon">` → `og:image` → `<header> img` → największy w nawigacji
   - **Kolory** — parsing CSS variables + k-means na pikselach screenshotu
   - **Fonty** — `font-family` z computed styles dla `h1/h2` i `body`, mapowanie na Google Fonts
3. **AI dopolerowanie** — Claude Haiku dostaje screenshot + dane, zwraca strukturyzowany JSON: walidacja palety, accent color jeśli brak, semantic mapping.
4. **Generate `theme.json`** + zapis do `clients/{slug}/theme.json` (Faza 0) lub `themes/{slug}/` (Faza 1+).
5. **Tweak preview** — `/crm-tweak-theme {slug}` lokalna strona z sample dashboardem, swap kolorów, akceptacja, push.
6. **Runtime** — Next.js czyta `theme.json` z mounted volume na starcie, generuje CSS variables, Tailwind ich używa.

**Decyzja**: skill ZAWSZE przerywa na preview przed deployem (30 sek na sprawdzenie zaoszczędzi embarrassment'u na demo).

### Theme.json shape

```json
{
  "brand": { "name", "logoUrl", "logoDarkUrl", "favicon" },
  "colors": {
    "primary", "accent",
    "neutral": { "50": "...", "900": "..." },
    "semantic": { "success", "warning", "error" }
  },
  "typography": { "heading", "body" },
  "radius": "0.5rem",
  "darkMode": false
}
```

### Edge cases

- White-label strona bez kolorów → AI generuje paletę z dominującego koloru logo
- PNG logo z białym tłem → auto background-removal + dark variant
- Cookie wall blokuje fetch → ręczny fallback (URL logo + 2 kolory ręcznie)
- Multi-brand landing → AI pyta który główny

## LLM layer

### A) Cmd+K AI parser (główny WOW factor)

Flow:

```
User: "Klient ABC chce szkolenie z Gemini w Q2, przypomnij tydzień przed"
  → POST /api/ai/parse-intent { input, context: { board, date, userId, currentEntity? } }
  → Claude Sonnet 4.6 z function calling
    Tools: createDeal | createTask | createReminder | createMeeting |
           addNote | createCompany | createContact | linkToEntity
    (każdy tool ma Zod schema)
  → LLM zwraca array tool calls
  → Frontend pokazuje preview UI (edytowalne karty)
  → User klika [✓ Utwórz wszystkie 3]
  → POST /api/ai/execute-intent → transakcja, audit log, zwraca IDs
```

**Decyzje**:
- **Preview ZAWSZE** — nigdy nie tworzymy bez potwierdzenia
- **Inline edycja w preview** — AI źle zgadł firmę? Klikasz, zmieniasz
- **Structured tools (function calling), nie freeform**
- **Context-aware** — LLM dostaje aktualny widok i datę

### B) AI widgets w kartach encji

W każdej karcie sekcja „🤖 AI" z trzema akcjami:

1. **Streszcz** — czyta aktywności/taski/faktury → 5-zdaniowe summary. Cache 1h.
2. **Napisz follow-up** — generuje email/WhatsApp pod kontekst. Preview → edytuj → wyślij.
3. **Co dalej?** — 1-3 najsensowniejsze następne kroki z argumentami.

### C) Semantic search

`Cmd+K` szukanie z naturalnym językiem („deale gdzie mówiliśmy o reklamacji"):
- Embeddings: `text-embedding-3-large` (OpenAI) lub Voyage AI
- Storage: **pgvector** (Postgres extension)
- Query → embedding → kNN → top 20 → re-ranking po recency
- Wyniki obok klasycznych, oznaczone „🤖 AI match"

### BYOK + privacy

- Settings → AI Configuration: klient wpisuje SWOJE klucze (Anthropic, OpenAI, Voyage), encrypted w `SystemSetting`
- AI calls idą **z serwera klienta bezpośrednio do API**, NIGDY przez Dokodu
- Audit log: każde wywołanie zapisane (kto/kiedy/tool/status), bez treści
- Default dla demo (Faza 0/1): nasze klucze, rate-limited per instance, koszt na nas
- Faza 2 (prod): klient wpisuje swoje klucze, sam płaci

### Koszty transparentne

Settings → AI Usage: tabela z miesięcznym zużyciem tokenów + szacunkowy koszt PLN.

## Reliability stack

### Backupy

- **Daily backup** o 3:00 — `pg_dump` + gzip + AES-256 + upload do storage klienta
- Default storage: lokalny dysk klienta (drugi wolumen). Opcjonalnie: ich S3/Backblaze B2/MinIO
- **Dokodu NIE trzyma ich danych na swoich dyskach**
- **Retention**: 30 dni dziennych + 12 miesięcy snapshotów
- **Quarterly restore drill** — co 3 miesiące skrypt restoruje na temp DB, walidacja, raport. Klient widzi „Ostatni test odzyskiwania: 2026-04-15 ✓"
- Attachments: lokalny dysk + opcjonalnie S3

### Monitoring

- **Uptime** — Uptime Kuma na Dokodu serwerze, ping co 30s, alert do Dokodu Slack w 90s. Target 99.9%.
- **Errors** — self-hosted Sentry (multi-tenant) lub OpenTelemetry → BetterStack
- **Performance** — APM mierzy P50/P95/P99. P95 > 500ms przez 10 min → alert
- Klient w settings widzi: status, uptime mc, P95 latency mc

### Updates

- **Dwa kanały**: `stable` (default, co 2 tyg) + `canary` (master, co tydz)
- **Zero-downtime deploy** — blue/green: nowy kontener obok starego, healthcheck → reverse-nginx swap. Cutover ~3 sek.
- **Migracje Prisma** w pre-deploy step, transaction-wrapped, rollback przy fail
- Email po update z linkiem do changelog

### Security

- SSL Let's Encrypt via Caddy, auto-renewal
- Security headers (CSP, X-Frame-Options, HSTS) w `next.config.ts` defaultowo
- Rate limiting per-IP (100/min) + per-user (1000/min), Redis-backed
- 2FA TOTP (już w schemacie), wymagane dla `admin`
- Audit log wszystkich CRUD + login + AI calls (już jest), retention 7y
- Pen-test raz/rok (od 12+ mc partnership)

### Disaster Recovery

- **RTO**: 4h (1h diagnostyka + 2h restore + 1h walidacja)
- **RPO**: 24h (worst case: ostatni backup z nocy)
- Runbook PDF na ich serwerze + u nas, aktualizowany przy każdej dużej zmianie
- DR drill raz/rok — symulacja awarii, restore, walidacja, lessons learned

### RODO

- **Mapa danych osobowych** — auto-generated z schematu (sekcja niżej)
- `/api/gdpr/delete-user` (już jest) — anonymizuje, audit-loguje
- `/api/gdpr/export` (też jest) — eksport danych usera do JSON
- DPA z klientem — jednorazowy template, podpisywany przed go-live

### Hosting requirements (klient prod)

| Skala | vCPU | RAM | SSD | Komentarz |
|---|---|---|---|---|
| Min (do 25 users) | 4 | 8 GB | 100 GB | Pedrollo/HABA tu |
| Rec (25-100 users) | 8 | 16 GB | 200 GB | Większe firmy |
| Pro (100+ users) | 16 | 32 GB | 500 GB | Postgres replica osobno |

Linux Ubuntu 22+/Debian 12+, Docker + docker-compose. Domain `crm.{klient}.pl`, SSL Caddy. SSH dla nas z whitelist IP.

### Pakiet w cenie miesięcznego retaineru

- Codzienny backup + quarterly restore drill
- 24/7 uptime + error monitoring (response SLA: 4h critical, 1 dzień warn)
- Bezpłatne update'y stable channel (bug fixes, security patches)
- Pen-test raz/rok (od 12+ mc partnership)
- Zmiany konfiguracji do 4h/mc (limit, ponad — billable)
- Email/Slack support

### Co NIE jest w pakiecie (billable osobno)

- Custom development nowych modułów
- Migracje z innych systemów (Bitrix → my, Salesforce → my)
- Szkolenia użytkowników
- Audit zewnętrzny (poza yearly pen-testem)

## Bulletproof Personal Data Inventory

**Zasada**: Prisma schema = source of truth. Mapa PII generowana automatycznie. Drift wykrywany w CI i blokuje merge.

### Annotacja przy każdym polu

```prisma
model ContactPerson {
  /// @pii basic — podstawowe dane kontaktowe; lawful basis: contract
  /// @retention 7y after deletion
  firstName String

  /// @pii basic
  /// @retention 7y after deletion
  email     String?

  /// @pii sensitive — special category jeśli odzwierciedla preferencje
  /// @retention 30d after consent withdrawal
  notes     String?

  /// @no-pii
  isPrimary Boolean @default(false)
}
```

Każde pole MUSI mieć `@pii <level>` (basic/sensitive/special) lub `@no-pii`. Brak adnotacji = CI fail.

### Codegen → `docs/data-map.md`

`pnpm gen:data-map` skrypt:

1. Parsuje `schema.prisma`
2. Czyta każde pole + adnotacje
3. Generuje markdownową tabelę per encja:

```markdown
## ContactPerson — Osoby kontaktowe

| Pole | Kategoria PII | Lawful basis | Retention | Eksport GDPR | Anonimizacja |
|------|---------------|--------------|-----------|--------------|--------------|
| firstName | basic | contract | 7y after del | ✓ | nullify |
| email | basic | contract | 7y after del | ✓ | hash |
| notes | sensitive | consent | 30d post withdraw | ✓ | nullify |
```

4. Dorzuca `lastUpdated`, `commitHash`, `schemaHash`
5. Zapisuje do `docs/data-map.md`

### CI gate

```yaml
- name: Verify data-map is current
  run: |
    pnpm gen:data-map
    if [[ -n $(git status -s docs/data-map.md) ]]; then
      echo "❌ schema.prisma changed but docs/data-map.md not regenerated"
      exit 1
    fi

- name: Verify all fields have PII annotation
  run: pnpm verify:pii-annotations
```

### Pre-commit hook (husky)

```bash
# .husky/pre-commit
pnpm gen:data-map
git add docs/data-map.md
```

### Runtime — Settings → Data Inventory

- Renderowane z generated JSON-a
- Liczba rekordów per encja
- Last refresh timestamp
- Link „Pobierz pełną mapę PDF"

### `/gdpr/export` i `/gdpr/delete` używają tej samej mapy

Endpointy nie mają hardcoded listy pól — czytają wygenerowany JSON. Dodanie nowego pola PII automatycznie pojawia się w eksporcie/anonimizacji.

### DPA klienta odwołuje się do live mapy

Template: „Aktualna mapa danych osobowych: `https://crm.{klient}.pl/settings/data-inventory` (regenerowana automatycznie przy każdym deploy)".

### Schema hash w changelog'u

Release notes każdego deploy: „Schema hash: abc123 (no PII change)" lub „Schema hash: def456 ⚠ NEW PII FIELDS (lista)".

### Rozszerzalność

Ten sam wzorzec można rozszerzyć na inne „bulletproof maps":
- Mapa uprawnień (per role, jakie endpointy)
- Mapa webhooków (skąd przyjmujemy, gdzie wysyłamy)
- Mapa AI prompts (jakie dane wysyłamy do LLM, do którego providera)

## Zasady projektowe (cross-cutting)

1. **Płaskość zamiast głębi** — max 2 poziomy (Tablica → Karta). Karta może mieć subtaski/komentarze/pliki, ale NIE sub-projekty z własnymi pipeline'ami.
2. **Sensowne defaulty zamiast pustego Notion'a** — przy seedzie gotowe pipeline'y per branża. Klient od pierwszej minuty widzi „tu jest Wasz proces wbity".
3. **Filtry pierwszego poziomu** — saved views per user + globalne, persistowane w URL = łatwe udostępnianie kolegom.
4. **Module isolation** — moduły nie importują z innych modułów (tylko z `core/`). Gwarantuje przenośność.
5. **Schema modyfikuje się jawnie, nie udajemy elastyczności EAV-em.**
6. **Każda zmiana schematu wymusza decyzję PII/no-PII.**

## Out of scope (świadomie)

- AI lead scoring z reverse engineering ICP — wymaga zdefiniowania ICP per klient, do późniejszej fazy
- Voicebot / IVR — potencjalny upsell, nie w MVP
- Mobile native app — responsive web wystarczy w MVP
- Public API dla klienta (do integracji custom) — webhooks i `/api/*` wystarczą
- Multi-language UI — najpierw PL only, potem EN

## Open questions

- **Cena miesięcznego retaineru** — TBD; powinna być >= 1500 PLN/mc żeby pokryć koszt monitoringu + 4h zmian + risk
- **Czy default LLM provider to Anthropic czy OpenAI** — sugest Anthropic Claude (Sonnet do parsera, Haiku do summary), ale klient może wybrać
- **Czy demo Phase 0 deploy jest publiczny czy hasłem chroniony** — sugest hasło + expiry 14 dni (link self-destructs jeśli nie ruchu)
- **Pricing add-on modułów** — TBD per moduł (sugest: 2-5k jednorazowo + 100-300 PLN/mc utrzymania)

## Następne kroki

1. Spec zatwierdzony przez Kacpra
2. Plan implementacji (osobna skill `writing-plans`) — milestones, sprinty, kolejność
3. Sprint 0: theme-from-URL pipeline + master demo deploy infra
4. Sprint 1: BRAIN skille (`/crm-new-demo`, `/crm-fork-prospekt`)
5. Sprint 2: Cmd+K AI parser + UX framework refresh
6. Sprint 3: Bulletproof data map + module isolation refactor
7. Sprint 4: Reliability stack (backupy, monitoring, deploy infra)
8. First demo target: Pedrollo (date TBD by Kacper)
