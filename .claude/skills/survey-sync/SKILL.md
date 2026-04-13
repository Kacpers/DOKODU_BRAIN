---
name: survey-sync
description: Pobiera wyniki ankiet poszkoleniowych z dokodu.it i zapisuje do DOKODU_BRAIN. Trigger: "pobierz ankiety", "zsynchronizuj ankiety", "wyniki ankiet", /survey-sync
---

# Instrukcja: Survey Sync

## Działanie

Uruchamia skrypt Python który pobiera wyniki ankiet poszkoleniowych z API dokodu.it
i zapisuje je jako Markdown do `DOKODU_BRAIN/20_AREAS/AREA_Szkolenia/Survey_Last_Sync.md`.

## KROK 1: Uruchom skrypt

Wykonaj Bash:
```bash
cd /home/kacper/DOKODU_BRAIN/scripts && python3 survey_fetch.py --save
```

Jeśli chcesz tylko jedną konkretną ankietę (np. po tokenie):
```bash
python3 survey_fetch.py --token ACME-XK7P2Q --save
```

## KROK 2: Sprawdź czy API key jest ustawiony

Jeśli pojawi się błąd `ERROR: Brak klucza API` — powiedz użytkownikowi:

```bash
mkdir -p ~/.config/dokodu
echo 'TUTAJ_WKLEJ_KLUCZ' > ~/.config/dokodu/dokodu_api_key
```

Klucz API (`EXTERNAL_API_KEY`) jest w pliku `.env` projektu Dokodu_nextjs.

## KROK 3: Wyświetl podsumowanie

Po udanym wykonaniu powiedz:
- Ile tokenów pobrano
- Ile łącznie odpowiedzi
- Data synchronizacji

## KROK 4: Zaproponuj następny krok

Zaproponuj jedną z opcji:
- `/survey-stats` — analiza wyników, wnioski, trendy, cytaty
- Nic więcej jeśli to był doraźny eksport

## ZASADY

- Skrypt używa stdlib Python (urllib) — nie wymaga pip install
- Klucz API: `~/.config/dokodu/dokodu_api_key` lub env `EXTERNAL_API_KEY`
- Wyniki trafiają do: `DOKODU_BRAIN/20_AREAS/AREA_Szkolenia/Survey_Last_Sync.md`
- Jeśli serwer niedostępny → sprawdź czy dokodu.it działa
