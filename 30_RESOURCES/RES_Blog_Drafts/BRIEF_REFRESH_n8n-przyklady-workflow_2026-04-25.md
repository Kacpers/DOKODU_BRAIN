---
type: refresh_brief
status: BRIEF
target_url: /blog/n8n/przyklady-workflow-automatyzacji
existing_words: 7525
existing_keyword: n8n workflow / przykłady (nieznany ranking, sprawdź GSC)
new_target_keyword: n8n templates (590 vol) + n8n workflow (480 vol)
total_target_volume: 1070
priority: high
effort: 1 dzień
risk: low (URL bez zmian)
created: 2026-04-25
target_publish: 2026-05-03
---

# REFRESH BRIEF: `/blog/n8n/przyklady-workflow-automatyzacji`

> Cel: rozszerzyć istniejący artykuł żeby celował dodatkowo w "n8n templates" (590 vol) i "n8n workflow" (480 vol) — łącznie 1 070 vol/mc.

---

## Status istniejącego artykułu

- **URL:** https://dokodu.it/blog/n8n/przyklady-workflow-automatyzacji
- **H1:** "Przykłady workflow w n8n – od prostych do zaawansowanych"
- **Słów:** 7 525
- **Istniejące H2:**
  1. Skąd brać gotowe workflow n8n?
  2. Jak zaimportować gotowy workflow do n8n?
  3. Komunikacja i powiadomienia
  4. Zarządzanie mediami społecznościowymi
  5. Marketing i generowanie leadów (CRM & Sales)
  6. Przetwarzanie danych i integracje z arkuszami/bazami
  7. Tworzenie treści i AI

## Co zmienić — patch list

### 1. Title + Meta + nazewnictwo (KRYTYCZNE)

| Pole | OBECNIE | NOWY |
|------|---------|------|
| **H1** | Przykłady workflow w n8n – od prostych do zaawansowanych | **n8n Templates — 25+ gotowych workflow do skopiowania (2026)** |
| **SEO Title** | (sprawdź) | **n8n Templates — 25+ gotowych workflow + jak zaimportować \| Dokodu** |
| **Meta Description** | (sprawdź) | n8n templates — 25+ gotowych workflow do skopiowania w 1 klik. Marketing, sprzedaż, AI agenty. Pełny tutorial importu. Zacznij dziś. |
| **Slug** | przyklady-workflow-automatyzacji | **NIE ZMIENIAĆ** |

W treści: zamień "przykłady workflow" → "templates / gotowe workflow / templates n8n" (mix). Nie wszędzie — ważne żeby brzmiało naturalnie.

### 2. Dodać 5 nowych templates 2026 (~1 500 słów)

Każdy template = nowa H3 z tym samym schematem:
- **Nazwa template + 1 zdanie wyjaśnienia**
- **Use case:** (kto / kiedy / dlaczego)
- **Stack:** (jakie node'y, jakie integracje)
- **Screenshot workflow** (z mojego n8n.dokodu.it lub gallery)
- **Link do JSON-a** (jeśli udostępniasz w GitHubie / gist)

#### Template 1: Claude Code + n8n — automatyzacja code review
- Webhook (GitHub PR) → Claude Code API → komentarze do PR → Slack notification
- Use case: zespół developerów chcący auto-review przed merge'em

#### Template 2: Gemini 2.5 + n8n — generator treści marketingowych
- Schedule trigger → RSS feed (industry news) → Gemini Pro (przepisz pod TOV firmy) → publikacja LinkedIn
- Use case: marketing manager bez czasu na codzienny content

#### Template 3: AI Agent klasyfikator maili B2B
- Gmail trigger → Claude → klasyfikacja (lead/spam/support/internal) → routing do Slacka/CRM
- Use case: SDR / account manager z 200+ maili dziennie

#### Template 4: n8n + Notion CRM — automatyczna kwalifikacja leada
- Form submit → enrichment (Hunter.io + LinkedIn API) → AI scoring → Notion CRM z BANT
- Use case: agencja B2B (np. Dokodu — pokaż własny use case)

#### Template 5: AI Voice Agent — telefoniczny lead qualifier
- Twilio webhook → Whisper STT → Claude → ElevenLabs TTS → kalendarz Google
- Use case: SaaS który chce automatyzować qualification calls

### 3. Dodać sekcję "Jak zbudować własny template" (~400 słów)

Nowa H2 przed "Podsumowaniem":

**"Jak zbudować własny n8n template — checklista"**
- 6-7 kroków od pomysłu do działającego workflow
- Wskazówki: error handling, logging, naming convention, dokumentacja w sticky notes
- Link wewn.: `/blog/n8n/docker-instalacja-konfiguracja` ("najpierw postaw n8n self-hosted →")
- Link wewn.: `/blog/n8n/node-code` ("custom Code Node — kiedy to ma sens →")
- Link wewn.: `/blog/n8n/webhook-bezpieczenstwo-throttling` ("zabezpiecz swoje webhooki →")

### 4. Dodać KACPER10 box (1 miejsce)

W sekcji "Skąd brać gotowe workflow" lub na początku artykułu (po intro):

```markdown
> 💡 **Potrzebujesz hostingu pod swoje workflow?**
>
> Wszystkie te templates uruchomisz na własnym n8n self-hosted. Postawisz go w 30 min na
> [Hostinger VPS](https://www.hostinger.com/kacper10) — z kodem **KACPER10** masz -10%.
>
> Tutorial: [n8n self-hosted z Dockerem — krok po kroku](/blog/n8n/docker-instalacja-konfiguracja)
>
> *Disclosure: link afiliacyjny — używam tego sam.*
```

### 5. Cross-linki — dodaj 4 outgoing + zachęć backlinki

**Z tego refreshed article DO innych:**
- `/blog/n8n/docker-instalacja-konfiguracja` — "najpierw postaw n8n →"
- `/blog/n8n/openclaw-vs-n8n` — "kiedy n8n a kiedy OpenClaw →"
- `/blog/n8n/node-code` — "custom code w workflow →"
- `/blog/n8n/przyklady-biznesowe` — "więcej case studies B2B →"

**Backlinki DO tego artykułu** (dodać w):
- `/blog/n8n` (pillar) — "25+ gotowych templates do startu →"
- `/blog/n8n/docker-instalacja-konfiguracja` (refreshed) — "po setupie zaimportuj template →"

---

## Featured image

Refresh:
```bash
python3 scripts/generate_image.py \
  --prompt "n8n workflow templates collection, modular cards layout, dark navy + orange accent, 25 connected nodes, editorial tech style, 16:9" \
  --variant pro \
  --output public/blog/n8n-templates-2026.webp
```

---

## KPI

- **"n8n templates":** wejść do top 10 w 6 tyg
- **"n8n workflow":** wejść do top 10 w 8 tyg
- **Zachować pozycje obecne** (sprawdź GSC przed publikacją żeby nie popsuć)
- **Konwersja KACPER10:** 3+ rejestracji/mies. z tego artykułu
