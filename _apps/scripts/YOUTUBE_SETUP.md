---
type: setup
status: active
owner: kacper
last_reviewed: 2026-03-11
tags: [youtube, api, setup, integracja]
---

# YouTube API — Instrukcja Konfiguracji

## Krok 1: Zainstaluj biblioteki Python

```bash
pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## Krok 2: Google Cloud Console

1. Idź na: https://console.cloud.google.com/
2. Stwórz nowy projekt (np. "Dokodu Brain YouTube")
3. Włącz 2 API:
   - **YouTube Data API v3** → APIs & Services → Library → wyszukaj "YouTube Data API v3" → Enable
   - **YouTube Analytics API** → wyszukaj "YouTube Analytics API" → Enable
4. Skonfiguruj ekran zgody OAuth:
   - APIs & Services → OAuth consent screen
   - User Type: **External** → Create
   - App name: "Dokodu Brain" | Support email: Twój email
   - Authorized domains: pomiń (lokalnie)
   - Scopes: pomiń na razie (dodamy przez code)
   - Test users: dodaj swój Gmail
5. Stwórz credentials:
   - APIs & Services → Credentials → Create Credentials → **OAuth 2.0 Client IDs**
   - Application type: **Desktop app**
   - Name: "Dokodu Brain CLI"
   - Download JSON → **zmień nazwę na `yt_credentials.json`**
   - Wgraj plik do: `/home/kacper/DOKODU_BRAIN/scripts/yt_credentials.json`

## Krok 3: Pierwsze uruchomienie (autentykacja)

```bash
cd /home/kacper/DOKODU_BRAIN/scripts
python3 youtube_fetch.py --days 28
```

**Co się stanie:**
- Skrypt wydrukuje URL do przeglądarki (lub otworzy ją automatycznie)
- Zaloguj się na konto Google właściciela kanału "Kacper Sieradzinski"
- Zezwól na dostęp do YouTube i YouTube Analytics
- Skrypt zapisze token do `yt_token.pickle` — następne uruchomienia nie będą wymagać logowania

> Na WSL2: jeśli przeglądarka się nie otworzy, skrypt wydrukuje URL — wklej go ręcznie w Windows.

## Krok 4: Weryfikacja

```bash
python3 youtube_fetch.py --days 7 --max-videos 5
```

Powinieneś zobaczyć tabelę z ostatnimi 5 filmami i statystykami kanału.

## Struktura plików

```
~/.config/dokodu/          ← wspólne miejsce na credentials (poza projektem)
├── yt_credentials.json    ← TY dodajesz (nigdy nie commituj!)
└── yt_token.pickle        ← generowany automatycznie (nigdy nie commituj!)

DOKODU_BRAIN/scripts/
├── youtube_fetch.py       ← główny skrypt
└── YOUTUBE_SETUP.md       ← ten plik
```

> ⚠️ Credentials są celowo poza katalogiem projektu — nigdy nie trafiają do git.

## Komendy skryptu

```bash
# Pełny raport (28 dni), 30 ostatnich filmów
python3 youtube_fetch.py

# Ostatnie 90 dni, 50 filmów, zapisz do BRAIN
python3 youtube_fetch.py --days 90 --max-videos 50 --save

# Tylko statystyki kanału (bez listy filmów)
python3 youtube_fetch.py --mode stats

# Wyjście JSON (do dalszego przetwarzania)
python3 youtube_fetch.py --json
```

## Troubleshooting

**`Error 403: access_denied`** → Upewnij się że Twój email jest w "Test users" na ekranie OAuth Consent Screen.

**`Token has been expired or revoked`** → Usuń `yt_token.pickle` i uruchom ponownie.

**`Quota exceeded`** → YouTube API ma limit 10,000 jednostek/dzień. Normalny sync kosztuje ~150 jednostek. Nie przekroczysz limitu przy normalnym użytkowaniu.

**`HttpError 400: invalidFilters`** → Zbyt wiele video_id w filtrze analytics. Skrypt obsługuje maks. 200 — jeśli masz więcej filmów w jednym sync, podziel na mniejsze batche.
