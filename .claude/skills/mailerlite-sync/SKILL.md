---
name: mailerlite-sync
description: Synchronizuje dane z MailerLite do DOKODU_BRAIN. Pobiera liczbę subskrybentów, statystyki kampanii (open rate, CTR), grupy i automatyzacje. Zapisuje raport do Newsletter_Last_Sync.md. Trigger: "zsynchronizuj mailerlite", "pobierz dane z mailerlite", "odśwież newsletter", "ile mam subskrybentów", /mailerlite-sync
---

# Instrukcja: MailerLite Sync

## Działanie

Uruchamia skrypt Python który łączy się z MailerLite API v3 i pobiera aktualne dane newslettera "Pracownik biurowy przyszłości".

## KROK 1: Uruchom skrypt

```bash
cd /home/kacper/DOKODU_BRAIN/scripts && python3 mailerlite_fetch.py --save
```

Jeśli chcesz więcej kampanii (domyślnie 20):
```bash
python3 mailerlite_fetch.py --campaigns 50 --save
```

## KROK 2: Sprawdź czy API key jest ustawiony

Jeśli pojawi się błąd `ERROR: Brak klucza API MailerLite` — powiedz użytkownikowi:

```bash
mkdir -p ~/.config/dokodu
echo 'TUTAJ_WKLEJ_KLUCZ' > ~/.config/dokodu/mailerlite_api_key
```

Klucz API znajdziesz w MailerLite → **Integrations → API → API Tokens** → utwórz token z prawami Read-only lub Full Access.

## KROK 3: Wyświetl podsumowanie

Po udanym wykonaniu powiedz:
- Liczba aktywnych subskrybentów
- Liczba pobranych kampanii
- Avg open rate (jeśli widoczny w output)
- Data synchronizacji

## KROK 4: Zaproponuj następny krok

- `/mailerlite-stats` — jeśli chce analizę wyników i rekomendacje
- Nic więcej jeśli to był doraźny eksport

## ZASADY

- Skrypt używa tylko stdlib Python (urllib) — nie wymaga pip install
- API key: `~/.config/dokodu/mailerlite_api_key` lub env `MAILERLITE_API_KEY`
- Wyniki trafiają do: `DOKODU_BRAIN/20_AREAS/AREA_Newsletter/Newsletter_Last_Sync.md`
- MailerLite API rate limit: 60 req/min — skrypt robi ~4 requestów, bezpieczne
- Jeśli błąd 401 → zły klucz API; jeśli 429 → poczekaj minutę i spróbuj ponownie
