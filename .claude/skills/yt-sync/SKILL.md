---
name: yt-sync
description: Synchronizuje dane z YouTube API do DOKODU_BRAIN. Pobiera statystyki kanału, listę ostatnich filmów i analytics. Zapisuje raport do YT_Last_Sync.md. Trigger: "zsynchronizuj youtube", "pobierz dane z yt", "odśwież youtube", /yt-sync
---

# Instrukcja: YouTube Sync

## Działanie

Uruchamia skrypt Python który łączy się z YouTube API i pobiera aktualne dane kanału.

## KROK 1: Uruchom skrypt

Wykonaj Bash:
```bash
cd /home/kacper/DOKODU_BRAIN/scripts && python3 youtube_fetch.py --days 28 --max-videos 30 --save
```

Jeśli pojawi się błąd o braku bibliotek:
```bash
pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

Jeśli brak `yt_credentials.json` — powiedz użytkownikowi:
"Brak pliku credentials. Wykonaj instrukcje z: `DOKODU_BRAIN/scripts/YOUTUBE_SETUP.md`"
I zakończ.

## KROK 2: Wyświetl podsumowanie

Po udanym wykonaniu wyświetl kluczowe liczby z wyjścia skryptu:
- Liczba subskrybentów
- Wyświetlenia w okresie
- CTR
- Avg View Duration
- Net subskrybenci

## KROK 3: Potwierdź zapis

Powiedz użytkownikowi że dane zostały zapisane do:
`DOKODU_BRAIN/20_AREAS/AREA_YouTube/YT_Last_Sync.md`

## KROK 4: Zaproponuj następny krok

Zaproponuj jedną z opcji:
- `/yt-stats` — jeśli chce głębszą analizę i wnioski
- `/yt-weekly` — jeśli to piątkowy przegląd kanału
- `/yt-plan-video` — jeśli chce zaplanować nowy odcinek

## ZASADY

- Nie interpretuj danych w tym kroku — to robi `/yt-stats`
- Jeśli skrypt zwróci błąd 403 → prawdopodobnie problem z OAuth, odsyłaj do YOUTUBE_SETUP.md
- Jeśli quota exceeded → informuj że limit API wróci następnego dnia (10,000 jednostek/dzień)
