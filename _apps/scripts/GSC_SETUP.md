---
type: setup
status: active
owner: kacper
last_reviewed: 2026-03-13
tags: [gsc, seo, api, setup, integracja]
---

# Google Search Console API — Instrukcja Konfiguracji

## Krok 1: Zainstaluj biblioteki Python

```bash
pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

(Jeśli masz już YouTube API — biblioteki są te same, możesz pominąć)

## Krok 2: Włącz Search Console API w Google Cloud Console

1. Idź na: https://console.cloud.google.com/
2. Wybierz **ten sam projekt** co dla YouTube API (np. "Dokodu Brain YouTube")
3. APIs & Services → Library → wyszukaj **"Google Search Console API"** → **Enable**

## Krok 3: Skonfiguruj OAuth (jeśli nowy projekt)

Jeśli użyłeś już istniejącego projektu z YouTube — ekran OAuth jest już skonfigurowany. Pomiń.

Jeśli nowy projekt:
- APIs & Services → OAuth consent screen
- User Type: **External** → Create
- App name: "Dokodu Brain SEO" | Support email: Twój email
- Test users: dodaj swój Gmail
- Credentials → Create Credentials → **OAuth 2.0 Client ID** → Desktop app
- Pobierz JSON

## Krok 4: Skopiuj credentials

```bash
# Możesz użyć tych samych credentials co YouTube lub osobnych
cp ~/.config/dokodu/yt_credentials.json ~/.config/dokodu/gsc_credentials.json
```

**Lub** pobierz nowe credentials JSON i skopiuj jako:
```
~/.config/dokodu/gsc_credentials.json
```

## Krok 5: Pierwsze uruchomienie (autentykacja)

```bash
cd /home/kacper/DOKODU_BRAIN/scripts
python3 gsc_fetch.py --days 28
```

**Co się stanie:**
- Skrypt wydrukuje URL OAuth — otwórz w przeglądarce Windows
- Zaloguj się na konto Google z GSC dla dokodu.it
- Zezwól na dostęp do **Google Search Console** (webmasters.readonly)
- Token zapisze się do `~/.config/dokodu/gsc_token.pickle`
- Następne uruchomienia nie wymagają logowania

> Na WSL2: jeśli przeglądarka się nie otworzy, skrypt wydrukuje URL — wklej go ręcznie.

## Krok 6: Weryfikacja

```bash
python3 gsc_fetch.py --days 7 --mode queries
```

Powinieneś zobaczyć tabelę z top zapytaniami i kliknięciami z GSC.

## Struktura plików

```
~/.config/dokodu/
├── gsc_credentials.json   ← TY dodajesz (nigdy nie commituj!)
├── gsc_token.pickle       ← generowany automatycznie (nigdy nie commituj!)
└── gsc_data.db            ← SQLite z historią danych GSC

DOKODU_BRAIN/scripts/
├── gsc_fetch.py           ← główny skrypt GSC
├── seo_ideas.py           ← bank pomysłów na posty (SQLite)
└── GSC_SETUP.md           ← ten plik
```

> ⚠️ Credentials są celowo poza katalogiem projektu — nigdy nie trafiają do git.

## Komendy skryptu gsc_fetch.py

```bash
# Pełny raport (28 dni) — queries + pages + opportunities
python3 gsc_fetch.py

# Ostatnie 90 dni, zapisz do BRAIN
python3 gsc_fetch.py --days 90 --save

# Tylko quick wins i okazje SEO
python3 gsc_fetch.py --mode opportunities

# Tylko zapytania (top keywords)
python3 gsc_fetch.py --mode queries

# Tylko strony (top URLs)
python3 gsc_fetch.py --mode pages

# Wyjście JSON (do dalszego przetwarzania)
python3 gsc_fetch.py --json

# Czytaj z lokalnej bazy (bez API)
python3 gsc_fetch.py --from-db

# Inna strona (domyślnie: https://dokodu.it/)
python3 gsc_fetch.py --site https://dokodu.it/
```

## Komendy skryptu seo_ideas.py

```bash
# Dodaj pomysł na post
python3 seo_ideas.py add "Jak wdrożyć Microsoft 365 Copilot w firmie" \
  --keyword "microsoft 365 copilot wdrożenie" \
  --pillar "M365 Copilot" \
  --intent informational \
  --priority high

# Lista aktywnych pomysłów
python3 seo_ideas.py list

# Filtrowanie
python3 seo_ideas.py list --pillar "M365 Copilot" --status POMYSŁ

# Szczegóły
python3 seo_ideas.py show 1

# Aktualizacja statusu
python3 seo_ideas.py update 1 --status BRIEF --slug "wdrozenie-m365-copilot-firma"

# Eksport do Markdown
python3 seo_ideas.py export --save
```

## Skrypty Topic Research

```bash
# Google Trends — pobierz trendy dla top keywords z GSC
python3 trends_fetch.py --auto-gsc --days 90 --save

# Trends dla konkretnych fraz
python3 trends_fetch.py --keywords "n8n,cursor ai,automatyzacja" --save

# Czytaj z bazy (bez API)
python3 trends_fetch.py --from-db --save

# Topic Research — pełna analiza GSC + Trends z scoringiem monetyzacji
python3 topic_research.py --save

# Tylko tematy z potencjałem produktowym (linki do produktów)
python3 topic_research.py --save --focus monetization

# Quick wins (pozycje 4-15, >100 impressions)
python3 topic_research.py --save --focus quick_wins

# Dodaj top tematy do Ideas Bank
python3 topic_research.py --add-to-ideas --min-score 40

# Podgląd co zostałoby dodane (bez zapisu)
python3 topic_research.py --dry-run --min-score 40

# Pobierz świeże Trends PRZED analizą
python3 topic_research.py --fetch-trends --save --focus monetization
```

## Blog Link Graph (`link_graph.py`)

Graf wewnętrznych linków bloga — baza artykułów i powiązań między nimi. Używany automatycznie przez seo-plan-post do sugestii linków wewnętrznych.

```bash
# Inicjalizuj / zresetuj bazę ze znanych artykułów
python3 link_graph.py --init

# Lista artykułów z liczbą linków in/out
python3 link_graph.py --list

# Sugestie linków wewnętrznych dla nowego tematu
python3 link_graph.py --suggest "cursor pro cena"

# Artykuły bez linków przychodzących (sieroty)
python3 link_graph.py --orphans

# Pełny raport Markdown → AREA_Blog_SEO/Link_Graph.md
python3 link_graph.py --report

# Dodaj nowy artykuł do grafu
python3 link_graph.py --add-article \
  --slug "n8n-webhooks" \
  --title "N8N Webhooks — Jak Działają?" \
  --keyword "n8n webhooks" \
  --pillar "n8n Automatyzacja" \
  --url "/blog/n8n/webhooks"

# Zarejestruj link między artykułami
python3 link_graph.py --add-link \
  --from-slug "n8n-co-to-jest" \
  --to-slug "n8n-webhooks" \
  --anchor "n8n webhooks"

# Zsynchronizuj z blog API (wymaga EXTERNAL_API_KEY)
python3 link_graph.py --sync
```

### Struktura pliku

```
~/.config/dokodu/gsc_data.db  ← tabele: blog_articles, blog_links (w tej samej bazie co GSC)
AREA_Blog_SEO/Link_Graph.md   ← raport generowany przez --report
```

### Workflow z seo-plan-post

Przy planowaniu nowego artykułu **zawsze** uruchom przed pisaniem briefu:
```bash
python3 link_graph.py --suggest "twój temat lub fraza"
```
Wynik pokaże artykuły do wewnętrznego linkowania z wagą dopasowania.

Po opublikowaniu artykułu zaktualizuj graf:
```bash
python3 link_graph.py --add-article --slug "slug-artykulu" ...
python3 link_graph.py --add-link --from-slug "nowy" --to-slug "istniejacy" --anchor "tekst"
```

## Troubleshooting

**`Error 403: access_denied`** → Dodaj swój email do "Test users" w OAuth Consent Screen.

**`Site not found`** → Upewnij się że `https://dokodu.it/` (z trailing slash) jest zweryfikowaną własnością w GSC.

**`Token has been expired or revoked`** → Usuń `gsc_token.pickle` i uruchom ponownie.

**`Empty results`** → GSC ma opóźnienie ~3 dni w danych. Skrypt automatycznie odejmuje 3 dni od end_date.

**`403 Forbidden: User does not have sufficient permissions`** → Konto Google musi mieć dostęp jako Owner lub Full User w GSC dla dokodu.it.
