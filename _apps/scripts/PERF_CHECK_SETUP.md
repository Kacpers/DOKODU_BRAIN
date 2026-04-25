# Performance Check — Setup

**Skrypt:** `perf_check.sh`
**Cron:** Monday-only (via `daily_sync.sh`)
**Co robi:** PSI mobile dla 12 URL `dokodu.it`, porównuje z poprzednim tygodniem, generuje markdown report w `30_RESOURCES/perf/reports/`, alertuje w `00_INBOX.md` gdy ≥2 stron ma regression ≥10pts.

## Wymagane prerekwizyty

### 1. PSI API key

Wymagany Google Cloud API key z włączonym **PageSpeed Insights API** (free tier 25k req/day).

**Setup:**
1. https://console.cloud.google.com/apis/credentials
2. Create credentials → API key
3. (opcjonalnie) Restrict key → "PageSpeed Insights API"

**Gdzie zapisać klucz na Linux server:**

Opcja A (env var w skrypcie który deployuje):
```bash
export PSI_KEY="AIzaSy..."
```

Opcja B (plik — zalecane, persistent):
```bash
mkdir -p ~/.config/dokodu
echo "AIzaSy..." > ~/.config/dokodu/psi_api_key
chmod 600 ~/.config/dokodu/psi_api_key
```

Skrypt sprawdza najpierw env `PSI_KEY`, potem `~/.config/dokodu/psi_api_key`.

### 2. CLI tools

`curl` i `jq` muszą być w PATH (standardowe na większości distr).

## Jak działa

### Pierwszy run (poniedziałek)
- Brak danych historycznych → tylko zapisuje raw + markdown report bez delty
- Raport w `30_RESOURCES/perf/reports/YYYY-MM-DD.md`
- Raw JSON w `30_RESOURCES/perf/raw/YYYY-MM-DD-{slug}-mobile.json`

### Drugi run (kolejny poniedziałek)
- Porównuje z poprzednim runem
- Δ score (delta PSI score)
- Δ LCP (jeśli się zmieniło)
- Jeśli ≥2 strony spadły ≥10pts → alert w `00_INBOX.md`

### Cleanup
- Raw JSON starsze niż 90 dni są kasowane automatycznie

## Ręczne uruchomienie (test)

```bash
# Z env var:
PSI_KEY="AIzaSy..." bash ~/DOKODU_BRAIN/scripts/perf_check.sh

# Z pliku key:
bash ~/DOKODU_BRAIN/scripts/perf_check.sh
```

## URLs sprawdzane

12 URL-i (te same co w P1+P2 baseline performance):
- `/` (homepage)
- `/automatyzacja-ai`, `/agenci-ai`, `/chatboty`
- `/dla-firm`, `/dla-firm/systemy-dedykowane`, `/dla-firm/szkolenia`
- `/kursy`, `/kursy/n8n`
- `/ebooki/automatyzacja-biznesowa`
- `/kalkulator-roi`
- `/blog`

Aby zmienić listę — edytuj array `URLS` w `perf_check.sh`.

## Caveat: PSI lab simulate variance

PSI lab simulate ma wysoką wariancję run-to-run (obserwowane 0.51-0.96 dla tej samej strony w pojedynczych runach). Single-run weekly to **trend indicator**, nie absolute truth.

**Dla pewności:**
- Użyj **CrUX field data** w GSC Core Web Vitals (28-day window, real users)
- Lub ręcznie odpal local Chrome DevTools Lighthouse — daje bardziej stabilne wyniki niż PSI z Google data center

## Output struktura

```
DOKODU_BRAIN/
├── 30_RESOURCES/
│   └── perf/
│       ├── raw/                          # Raw PSI JSON, kasowany po 90d
│       │   └── 2026-04-26-home-mobile.json
│       └── reports/                      # Markdown reports, persistent
│           └── 2026-04-26.md
└── 00_INBOX.md                           # Alert appended jeśli regression
```

## Hooked w daily_sync.sh

Linia w `daily_sync.sh` (Monday-only block po Link Graph):

```bash
if [ "$(date +%u)" = "1" ]; then
    echo "  → Performance check (poniedziałek)..." >> "$LOG_FILE"
    bash /home/kacper/DOKODU_BRAIN/scripts/perf_check.sh >> "$LOG_FILE" 2>&1
    echo "  ✓ Performance check done" >> "$LOG_FILE"
fi
```
