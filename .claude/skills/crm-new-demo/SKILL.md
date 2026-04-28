---
name: crm-new-demo
description: Tworzy nową instancję demo CRM dla prospektu — pobiera brand z URL klienta (Playwright + AI palette), buduje image, deployuje na dev.dokodu.it/crm-{slug}, ładuje seed danych branżowych. Trigger: "stwórz demo crm dla", "nowa instancja crm", "demo dla pedrollo", /crm-new-demo {url}.
---

# Instrukcja: CRM New Demo

## Działanie

End-to-end deployment nowej instancji CRM dla prospektu Dokodu. Pipeline:
1. Pobranie brandu z URL prospektu (Playwright + k-means colors + AI palette via Claude Haiku)
2. Lokalny preview do swap'owania kolorów
3. Build image z `BUILD_BASE_PATH=/crm-{slug}`
4. Deploy do `dev.dokodu.it/crm-{slug}`
5. Załadowanie seed danych branżowych

Końcowy efekt: live demo URL gotowy do prezentacji dla klienta. Czas: ~5-7 min.

## KROK 1: Wyciągnij URL i slug

Z prompta użytkownika wyciągnij URL prospektu (np. `pedrollo.pl`, `https://haba.pl`).

```bash
cd /Users/ksieradzinski/Projects/dokodu/crm-new
pnpm exec tsx -e "import { slugFromUrl } from './scripts/lib/slug-from-url'; console.log(slugFromUrl('<URL>'))"
```

Wyświetl użytkownikowi: "Tworzę demo dla **{slug}** (URL: {url}). Szacowany czas: 4-6 minut."

## KROK 2: Generuj theme z URL

```bash
cd /Users/ksieradzinski/Projects/dokodu/crm-new
ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY:-$(cat ~/.config/anthropic_api_key 2>/dev/null)}" \
  pnpm theme:from-url "<URL>" 2>&1
```

Jeśli brak `ANTHROPIC_API_KEY` w env i braku pliku `~/.config/anthropic_api_key`:
- Użyj `--skip-ai`: `pnpm theme:from-url --skip-ai <URL>` (gorsza paleta — bierze 2 najsilniejsze kolory mechanicznie, ale działa).
- Powiedz użytkownikowi że AI polish był skipped i może po prezentacji ręcznie dotweakować przez Krok 3.

Po zakończeniu: `themes/{slug}/theme.json` istnieje + `themes/{slug}/logo.{ext}`.

## KROK 3: Preview + tweak (interaktywnie)

```bash
pnpm theme:tweak <slug>
```

Otwiera browser na `http://localhost:3099`. Zapytaj użytkownika:
- "Otworzyłem podgląd theme'u. Akceptujesz kolory czy chcesz je doprecyzować przed deployem?"
- Jeśli akceptuje "tak jak jest": w UI klikają "Save & exit" — proces sam się zamknie.
- Jeśli chce zmieniać: powiedz mu żeby kliknął kolor, wybrał nowy w pickerze, kliknął "Save & exit".

Czekaj aż proces się zakończy (czyli plik został zapisany lub user kliknął Save). Jeśli user mówi "skip preview, jedźmy" — przerwij proces tweak (Ctrl+C) i przejdź do Kroku 4.

## KROK 4: Deploy na serwer

```bash
./scripts/deploy-instance.sh <slug> --bundle distribution-b2b
```

(Dla Pedrollo / HABA / podobne dystrybucja-B2B: `--bundle distribution-b2b`. Dla innych branż: bez flagi `--bundle` (instancja będzie pusta poza domyślnym seed) lub przyszłe bundle z innych branż.)

Skrypt:
1. Wgrywa theme + source na serwer (deploy@57.128.219.9)
2. Buduje image z `BUILD_BASE_PATH=/crm-{slug}` (~2-3 min)
3. Migruje DB + ładuje seed bundle
4. Startuje kontenery (`crm-{slug}` + `crm-db-{slug}`)
5. Czeka na healthcheck `/api/health` (do 60s)
6. Wypisuje finalny URL

Jeśli skrypt zwróci błąd: pokaż użytkownikowi:
```
ssh deploy@57.128.219.9 'cd /home/deploy/crm-instances/{slug} && docker compose -f docker-compose.{slug}.yml logs --tail 50'
```
i zaproponuj debug.

## KROK 5: Smoke test + raport

```bash
SLUG=<slug>
curl -s -o /dev/null -w "%{http_code}\n" "https://dev.dokodu.it/crm-${SLUG}/api/health"
```

Oczekiwane: `200`.

Następnie wypisz raport dla użytkownika:

```
✅ DEMO READY

URL: https://dev.dokodu.it/crm-{slug}
Login: admin@dokodu.it / haslo z prisma seed (zwykle "admin123" — zmień po pierwszej prezentacji)

Co dostajesz w demie:
- Brand z {url} (logo + kolory + Plus Jakarta Sans typography)
- 8 sample companies (industry: distribution-b2b)
- 8 deali w 5 etapach pipeline (Nowy Lead → Wygrana / Przegrana)
- 16-24 aktywności (maile, telefony, spotkania)

Co dalej:
- Otwórz URL i przeklikaj zanim pokażesz klientowi
- Jeśli coś nie pasuje, edytuj manualnie:
  ssh deploy@57.128.219.9 'cd /home/deploy/crm-instances/{slug} && docker compose -f docker-compose.{slug}.yml exec crm npx prisma studio'
- Po prezentacji: jeśli klient zaakceptował, /crm-fork-prospekt {slug} (Plan 3, niedługo)
- Jeśli odrzucił: ./scripts/destroy-instance.sh {slug}
```

## Uwagi techniczne

- Każda instancja ma własną bazę i własny container — ~250 MB RAM + 100 MB dysk per instancja
- TTL: zalecam manual destroy po 30 dniach jeśli klient nie wraca (Plan 3 doda auto-destroy)
- Browser cache: jeśli klient zobaczy starą wersję, hard reload Ctrl+Shift+R
- Jeśli SSL klienta jest zepsuty (np. self-signed), Playwright fetch może failnąć — wtedy dodaj `ignoreHTTPSErrors: true` ad-hoc lub spróbuj URL z http://
