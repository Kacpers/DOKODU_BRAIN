# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Czym jest ten system

**DOKODU_BRAIN** to Second Brain agencji AI Dokodu (Kacper Sieradzinski, CEO). Nie jest to repozytorium kodu — to system zarządzania wiedzą oparty na metodologii PARA. Wszystkie pliki są w formacie Markdown, język systemu to **polski**.

---

## Orientacja w systemie

**Zawsze zaczynaj od `000_DASHBOARD.md`** — to Mission Control z aktualnymi priorytetami, statusem projektów i KPI.

Struktura PARA:
- `10_PROJECTS/` — aktywne projekty z deadlinem (`PRJ_<Klient>_<Typ>.md`)
- `20_AREAS/` — stałe obszary odpowiedzialności bez deadline (Marketing, Finanse, Legal, n8n, HR)
- `30_RESOURCES/` — biblioteka wiedzy: prompty, blueprinty n8n, playbooki sprzedażowe, szablony
- `40_ARCHIVE/` — zakończone projekty (read-only)
- `00_INBOX.md` — wrzutki nieuporządkowane, przetwarzane w piątek podczas Weekly Review

---

## Dostępne skille (komendy)

Zarządzaj systemem przez skille, nie edytując plików manualnie:

| Skill | Zastosowanie |
| :--- | :--- |
| `/brain-capture` | Szybki zapis do Inboxu (myśl, pomysł, todo) |
| `/brain-status` | Dashboard: projekty, leady, inbox count |
| `/brain-new-customer` | Nowy klient — tworzy katalog + Profile + Meetings + Opportunities |
| `/brain-new-project` | Nowy projekt z YAML frontmatter i fazami |
| `/brain-add-lead` | Lead do CRM + kwalifikacja BANT+ |
| `/brain-lead-research` | Research firmy/leadu pod kątem ICP Dokodu |
| `/brain-meeting-notes` | Przetwarza notatki/transkrypcje ze spotkania |
| `/brain-new-prompt` | Dodaje prompt do `300_BIBLIOTEKA_PROMPTOW.md` |
| `/brain-weekly-review` | Tygodniowy przegląd (piątek) |
| `/brain-archive-project` | Archiwizuje projekt + retrospektywa |
| `/brain-draft-email` | Pisze gotowy email do klienta — na podstawie profilu z BRAIN, w stylu Kacpra |
| `/outreach` | Prospecting LinkedIn krok po kroku — pokazuje firmę, generuje DM/email, śledzi w Outreach_Tracker |
| `/brain-remind` | Reminder z datą → jednocześnie do REMINDERS.md i Google Calendar |
| `/pdf` | Czyta i analizuje PDF — dla umów wyciąga kluczowe klauzule (płatność, zakres, kary, logo) |
| `/brain-new-offer` | Generuje ofertę handlową dla klienta — 2 opcje cenowe, szablon propozycji, zapis w katalogu klienta |
| `/meet-transcribe` | Pobiera nagrania Meet z Drive, paruje z kalendarzem, transkrybuje Whisper PL → `meetings_transcripts/` |
| `/skill-creator` | Tworzy nowe skille — wywiad, SKILL.md, test cases, zapis |
| `/survey-sync` | Pobiera wyniki ankiet poszkoleniowych z dokodu.it API → `Survey_Last_Sync.md` |
| `/survey-stats` | Analizuje wyniki ankiet — insights, cytaty marketingowe, trendy → `Survey_Insights.md` |
| `/mailerlite-sync` | Pobiera dane z MailerLite: subskrybenci, kampanie, open rate, CTR → `Newsletter_Last_Sync.md` |
| `/mailerlite-stats` | Analizuje wyniki newslettera — insights, najlepsze kampanie, rekomendacje |
| `/newsletter-check` | **Pre-send review** — ocenia newsletter przed wysłaniem (subject line, CTA, cel, ton), daje ocenę 1–10, 3 alternatywne subject liny, prognozę OR. Zapisuje do `Reviews/`. |

**Skille YouTube:**

| Skill | Zastosowanie |
| :--- | :--- |
| `/yt-sync` | Pobiera dane z YouTube API → zapisuje do YT_Last_Sync.md |
| `/yt-stats` | Głęboka analiza statystyk → insights → zapisuje do YT_Insights.md |
| `/yt-blueprint` | Pełny pipeline: research YT → analiza top 5 filmów → competitive intel → brief produkcyjny |
| `/yt-plan-video` | Planuje nowy odcinek: SEO tytuł, hook, struktura, opis, tagi, thumbnail brief |
| `/yt-weekly` | Tygodniowy przegląd kanału: pipeline produkcji + metryki + plan |
| `/yt-publish-kit` | Generuje komplet do publikacji: thumbnail (Remotion), opis, tagi, prompter, checklist → Dropbox |

**Skille Blog SEO (dokodu.it):**

| Skill | Zastosowanie |
| :--- | :--- |
| `/seo-sync` | Pobiera dane z Google Search Console → zapisuje do SEO_Last_Sync.md |
| `/seo-stats` | Analizuje GSC: quick wins, content gaps, niski CTR → zapisuje do SEO_Insights.md |
| `/seo-research [temat]` | Keyword research tematu: GSC + web, intent, konkurencja, rekomendacja kąta |
| `/seo-plan-post` | Pełny brief posta: SEO title, slug, meta, H2/H3, hook, CTA, linki wewnętrzne |
| `/seo-weekly` | Tygodniowy przegląd SEO bloga: metryki, pipeline, bottlenecki, plan |
| `/blog-draft` | Pisze kompletny artykuł + wysyła jako draft na blog (przez API) |
| `/blog-publish` | Zarządza postami na blogu: lista, publikacja draftu, aktualizacja |

**Skille SEO Techniczne (claude-seo — zainstalowany):**

| Skill | Zastosowanie |
| :--- | :--- |
| `/seo audit https://dokodu.it` | Pełny audyt strony (7 subagentów, score 0-100, Core Web Vitals) |
| `/seo page [URL]` | Analiza pojedynczej strony (on-page, meta, schema, obrazy) |
| `/seo technical [URL]` | Audyt techniczny: crawlability, robots.txt, sitemap, mobile |
| `/seo content [URL]` | Analiza jakości treści E-E-A-T |
| `/seo schema [URL]` | Walidacja i generowanie structured data (JSON-LD) |
| `/seo geo [URL]` | Optymalizacja pod AI Overviews, ChatGPT, Perplexity |
| `/seo-competitor-pages [URL]` | Generuje strony porównawcze (X vs Y, alternatywy) |

---

## Kluczowe pliki do kontekstu

Przy pracy jako Executive Business Shadow / doradca strategiczny załaduj:
- `000_DASHBOARD.md` — priorytety i zdrowie projektów
- `00_INBOX.md` — otwarte wątki
- `001_VISION.md` — North Star (2028: 2M PLN, 30+ klientów)
- `005_SKILLS.md` — matryca kompetencji Kacpra

Przy pracy sprzedażowej/CRM:
- `20_AREAS/AREA_Marketing_Sales/CRM_Leady_B2B.md` — pipeline
- `30_RESOURCES/RES_Sales_Playbook/Sales_Playbook.md` — ICP, cennik, obiekcje

Przy pracy z klientem:
- `20_AREAS/AREA_Customers/<Klient>/` — profile, meetings, opportunities
- `30_RESOURCES/RES_Industry_Playbooks/` — Playbook_Logistyka.md, Playbook_Produkcja.md

Przy pracy technicznej (n8n, AI):
- `20_AREAS/AREA_n8n_Infrastructure/AREA_n8n_Infrastructure.md` — stack, Docker, Vault
- `30_RESOURCES/RES_n8n_Blueprints/N8N_Blueprints.md` — 8 wzorców workflow
- `30_RESOURCES/RES_Prompt_Library/300_BIBLIOTEKA_PROMPTOW.md` — biblioteka promptów (PROMPT-001 do PROMPT-040+)
- `30_RESOURCES/RES_Templates/Logging_Standard.md` — standard logowania dla n8n Code Nodes

Przy pracy z YouTube (kanał "Kacper Sieradzinski"):
- `20_AREAS/AREA_YouTube/AREA_YouTube.md` — strategia, pillary, KPI
- `20_AREAS/AREA_YouTube/YT_Videos.md` — tracker produkcji (pipeline)
- `20_AREAS/AREA_YouTube/YT_Last_Sync.md` — ostatnie dane z API (generowany przez `/yt-sync`)
- `30_RESOURCES/RES_YouTube/YT_Insights.md` — kumulatywna baza insightów ze statystyk
- `scripts/youtube_fetch.py` — skrypt Python do pobierania danych z YouTube API
- `scripts/YOUTUBE_SETUP.md` — instrukcja konfiguracji API (jednorazowa)

Przy pracy z Blog SEO (dokodu.it/blog/):
- `20_AREAS/AREA_Blog_SEO/AREA_Blog_SEO.md` — strategia SEO, pillary, KPI
- `20_AREAS/AREA_Blog_SEO/SEO_Last_Sync.md` — ostatnie dane z GSC (generowany przez `/seo-sync`)
- `20_AREAS/AREA_Blog_SEO/SEO_Insights.md` — kumulatywna baza insightów SEO
- `20_AREAS/AREA_Blog_SEO/SEO_Ideas_Bank.md` — bank pomysłów na posty (generowany przez `seo_ideas.py export`)
- `scripts/gsc_fetch.py` — skrypt Python do pobierania danych z Google Search Console API
- `scripts/seo_ideas.py` — bank pomysłów na posty (SQLite, analogia do youtube_ideas.py)
- `scripts/blog_publish.py` — klient API bloga (create/update/publish/list postów)
- `scripts/GSC_SETUP.md` — instrukcja konfiguracji GSC API (jednorazowa)
- Blog API key: `~/.config/dokodu/blog_api_key` lub env `EXTERNAL_API_KEY`

Przy pracy ze szkoleniami i ankietami:
- `20_AREAS/AREA_Szkolenia/Survey_Last_Sync.md` — ostatnie wyniki ankiet (generowany przez `/survey-sync`)
- `20_AREAS/AREA_Szkolenia/Survey_Insights.md` — kumulatywna baza insightów (generowany przez `/survey-stats`)
- `scripts/survey_fetch.py` — skrypt pobierający dane z API dokodu.it
- API key: `~/.config/dokodu/dokodu_api_key` lub env `EXTERNAL_API_KEY`

Przy pracy z newsletterem (MailerLite):
- `20_AREAS/AREA_Newsletter/Newsletter_Last_Sync.md` — ostatnie dane z MailerLite (generowany przez `/mailerlite-sync`)
- `scripts/mailerlite_fetch.py` — skrypt pobierający dane z MailerLite API v3
- API key: `~/.config/dokodu/mailerlite_api_key` lub env `MAILERLITE_API_KEY`

Przy pracy prawnej/compliance:
- `20_AREAS/AREA_Legal_Compliance/AI_Act_Tracker.md` — mapa AI Act 2024/1689
- `20_AREAS/AREA_Legal_Compliance/RODO_Checklist.md` — checklist GDPR, standardy PII

---

## Zasady systemu

1. **Capture first, organize later** — nowe informacje trafiają do `00_INBOX.md`, nie kategoryzuj w locie
2. **One source of truth** — informacja może być tylko w jednym miejscu
3. **Projects die without next actions** — każdy projekt musi mieć "Następny krok" z datą
4. **Resources compound** — biblioteka promptów i blueprintów rośnie z każdym projektem; ekstrakcj wiedzę po każdym projekcie
5. **Weekly Review is non-negotiable** — bez przeglądu w piątek system się sypie

---

## Konwencje plików

- Frontmatter YAML w nagłówku każdego pliku (type, status, owner, last_reviewed, tags)
- Projekty: `PRJ_<Klient>_<Typ>.md` z polami: budget, deadline, health (🟢/🟡/🔴)
- Klienci: katalog `<NazwaKlienta>/` z plikami `Profile.md`, `Meetings.md`, `Opportunities.md`
- Prompty: format `PROMPT-NNN` z polami cel, trigger, model, temperatura, treść
- Zarchiwizowane pliki: przenoszone do `40_ARCHIVE/` (nie usuwaj, nie edytuj po archiwizacji)
