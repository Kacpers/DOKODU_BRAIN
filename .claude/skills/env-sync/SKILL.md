---
name: env-sync
description: Synchronizuje plik .env między lokalnym projektem a serwerem produkcyjnym Dokodu (deploy@57.128.219.9). Pobiera zdalny .env, scala z lokalnym (serwer wygrywa przy konfliktach, lokalne uzupełnia braki), naprawia bugi i wysyła scalony plik z powrotem. Używaj gdy: zmieniłeś .env lokalnie i chcesz zsynchronizować z serwerem, lub gdy serwer ma nowsze wartości których lokalnie nie masz. Trigger: "zsynchronizuj env", "sync .env", "env na serwer", "pobierz env z serwera", /env-sync
---

# env-sync — Synchronizacja .env lokalny ↔ serwer

## Cel
Scalić lokalne `.env` z wersją na serwerze produkcyjnym, tak żeby żadne klucze nie zginęły.

## Konfiguracja serwera
- **SSH alias:** `dokodu-vps` (zdefiniowany w `~/.ssh/config`)
- **Host:** `57.128.219.9`
- **User:** `deploy`
- **Ścieżka projektu:** `/srv/dokodu-app/app`
- **Plik .env:** `/srv/dokodu-app/app/.env`

## Strategia mergowania
**Serwer wygrywa** przy konflikcie tej samej zmiennej — zakładamy, że serwer ma prawdziwe wartości produkcyjne.
**Lokalne uzupełnia** — zmienne istniejące tylko lokalnie (nie na serwerze) są dodawane do wyniku.

Wyjątki (zawsze napraw, nawet jeśli "serwer wygrywa"):
- Zduplikowane klucze — zostaw tylko pierwsze wystąpienie
- `AUTH_SECRET=AUTH_SECRET=...` — usuń podwójny prefix
- `NEXT_PUBLIC_SITE_URL=http://localhost:*` — zastąp `https://dokodu.it`
- `NEXT_PUBLIC_APP_URL=http://localhost:*` — zastąp `https://dokodu.it`
- `EMAIL_PROVIDER=smtpDobra` → `EMAIL_PROVIDER=smtp`

## Proces

### Krok 1: Pobierz zdalny .env
```bash
ssh dokodu-vps "cat /srv/dokodu-app/app/.env"
```

### Krok 2: Wczytaj lokalny .env
Read `/home/kacper/DOKODU/STRONA/Dokodu_nextjs/.env`

### Krok 3: Analiza różnic
Wypisz użytkownikowi:
- Zmienne **tylko na serwerze** (do dodania lokalnie)
- Zmienne **tylko lokalnie** (do dodania na serwer)
- Zmienne **z różnymi wartościami** (serwer wygrywa — zaznacz)
- **Bugi** do naprawienia (duplikaty, złe URL-e)

### Krok 4: Zbuduj scalony plik
Zastosuj strategię mergowania. Zachowaj sekcje i komentarze z lokalnego pliku.
Oznacz `# ⚠ WYMAGA UZUPEŁNIENIA` przy zmiennych z wartościami-placeholderami.

### Krok 5: Zapisz lokalnie i wyślij na serwer
```bash
# Zapisz lokalnie
Write do /home/kacper/DOKODU/STRONA/Dokodu_nextjs/.env

# Wyślij na serwer
scp /home/kacper/DOKODU/STRONA/Dokodu_nextjs/.env dokodu-vps:/srv/dokodu-app/app/.env
```

### Krok 6: Weryfikacja
```bash
ssh dokodu-vps "wc -l /srv/dokodu-app/app/.env && echo 'OK'"
```

## Output
- Zaktualizowany lokalny `.env`
- Zaktualizowany `.env` na serwerze
- Raport diff (co dodano, co naprawiono, co nadal wymaga uzupełnienia)

## Zasady bezpieczeństwa
- Nigdy nie loguj pełnych wartości sekretów w odpowiedzi — maskuj (np. `sk_live_51Sk6...***`)
- Nie commituj `.env` do gita (jest w `.gitignore`)
- Nie wysyłaj .env mailem ani przez inne kanały
