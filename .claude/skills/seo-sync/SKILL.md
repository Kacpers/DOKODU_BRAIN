---
name: seo-sync
description: Synchronizuje dane z Google Search Console do DOKODU_BRAIN. Pobiera kliknięcia, impressions, CTR, pozycje dla zapytań i stron dokodu.it. Zapisuje raport do SEO_Last_Sync.md. Trigger: "zsynchronizuj seo", "pobierz dane z gsc", "odśwież search console", "sync seo", /seo-sync
---

# Instrukcja: SEO Sync (Google Search Console)

## Działanie

Uruchamia skrypt Python który łączy się z Google Search Console API i pobiera aktualne dane organiczne dokodu.it.

## KROK 1: Uruchom skrypt

```bash
cd /home/kacper/DOKODU_BRAIN/scripts && python3 gsc_fetch.py --days 28 --save
```

Jeśli pojawi się błąd o braku bibliotek:
```bash
pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

Jeśli brak `gsc_credentials.json` — powiedz użytkownikowi:
"Brak pliku credentials. Wykonaj instrukcje z: `DOKODU_BRAIN/scripts/GSC_SETUP.md`"
I zakończ.

## KROK 2: Wyświetl podsumowanie

Po udanym wykonaniu wyświetl kluczowe liczby z wyjścia:
- Łączne kliknięcia w okresie
- Łączne impressions
- Średni CTR
- Średnia pozycja
- Liczba unikalnych zapytań

Wskaż 3 najważniejsze obserwacje z tabeli quick wins (jeśli są).

## KROK 3: Potwierdź zapis

Powiedz użytkownikowi że dane zostały zapisane do:
`DOKODU_BRAIN/20_AREAS/AREA_Blog_SEO/SEO_Last_Sync.md`

## KROK 4: Zaproponuj następny krok

Zaproponuj jedną z opcji:
- `/seo-stats` — jeśli chce głębszą analizę i wnioski z danych
- `/seo-weekly` — jeśli to piątkowy przegląd
- `/seo-research [temat]` — jeśli widzi frazę którą chce zbadać

## ZASADY

- Nie interpretuj szczegółowo danych w tym kroku — to robi `/seo-stats`
- GSC ma ~3-dniowy lag — skrypt automatycznie uwzględnia ten offset
- Jeśli 0 wyników → prawdopodobnie błąd autoryzacji lub zła strona, sprawdź GSC_SETUP.md
- Jeśli błąd 403 → sprawdź czy konto ma dostęp Owner/Full User w GSC dla dokodu.it
