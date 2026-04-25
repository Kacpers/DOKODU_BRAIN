#!/usr/bin/env bash
# DOKODU BRAIN — Weekly Performance Check
# Pobiera PSI mobile dla 12 URL-i dokodu.it, porównuje z poprzednim tygodniem,
# generuje markdown report i alertuje w INBOX gdy ≥2 stron ma regression ≥10pts.
#
# Uruchamiane Monday-only z daily_sync.sh.
# PSI_KEY: env var PSI_KEY OR plik ~/.config/dokodu/psi_api_key

set -u

# ==== Config ====
PSI_KEY="${PSI_KEY:-$(cat "$HOME/.config/dokodu/psi_api_key" 2>/dev/null || echo)}"
BRAIN_DIR="${BRAIN_DIR:-$HOME/DOKODU_BRAIN}"
DATE=$(date +%Y-%m-%d)
PERF_DIR="$BRAIN_DIR/30_RESOURCES/perf"
RAW_DIR="$PERF_DIR/raw"
REPORTS_DIR="$PERF_DIR/reports"

mkdir -p "$RAW_DIR" "$REPORTS_DIR"

if [ -z "$PSI_KEY" ]; then
  echo "ERROR: PSI_KEY missing. Set env PSI_KEY OR file ~/.config/dokodu/psi_api_key" >&2
  exit 1
fi

# 12 URL-i (te same co w P1+P2 baseline)
URLS=(
  "home|/"
  "automatyzacja-ai|/automatyzacja-ai"
  "agenci-ai|/agenci-ai"
  "chatboty|/chatboty"
  "dla-firm|/dla-firm"
  "dla-firm-systemy|/dla-firm/systemy-dedykowane"
  "dla-firm-szkolenia|/dla-firm/szkolenia"
  "kursy|/kursy"
  "kursy-n8n|/kursy/n8n"
  "ebook-automatyzacja|/ebooki/automatyzacja-biznesowa"
  "kalkulator-roi|/kalkulator-roi"
  "blog|/blog"
)

# ==== 1. Fetch PSI for all URLs ====
echo "[$DATE] perf_check: fetching PSI mobile for ${#URLS[@]} URLs..."
declare -A scores_now
declare -A lcp_now
for entry in "${URLS[@]}"; do
  slug="${entry%%|*}"; path="${entry#*|}"
  url="https://dokodu.it${path}"
  out="$RAW_DIR/${DATE}-${slug}-mobile.json"

  curl -sS "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=${url}&strategy=mobile&category=PERFORMANCE&key=${PSI_KEY}" -o "$out"

  err=$(jq -r '.error.message // empty' "$out")
  if [ -n "$err" ]; then
    echo "  ✗ $slug: $err"
    scores_now["$slug"]="ERR"
    lcp_now["$slug"]="-"
    continue
  fi

  scores_now["$slug"]=$(jq -r '.lighthouseResult.categories.performance.score // "ERR"' "$out")
  lcp_now["$slug"]=$(jq -r '.lighthouseResult.audits["largest-contentful-paint"].displayValue // "-"' "$out")
  echo "  ✓ $slug: ${scores_now[$slug]} (LCP ${lcp_now[$slug]})"
done

# ==== 2. Find previous week's data for comparison ====
LAST_DATE=$(ls "$RAW_DIR" 2>/dev/null | grep -oE "^[0-9]{4}-[0-9]{2}-[0-9]{2}" | sort -u | grep -v "$DATE" | tail -1)

declare -A scores_last
declare -A lcp_last
if [ -n "$LAST_DATE" ]; then
  for entry in "${URLS[@]}"; do
    slug="${entry%%|*}"
    last_file="$RAW_DIR/${LAST_DATE}-${slug}-mobile.json"
    if [ -f "$last_file" ]; then
      scores_last["$slug"]=$(jq -r '.lighthouseResult.categories.performance.score // empty' "$last_file" 2>/dev/null)
      lcp_last["$slug"]=$(jq -r '.lighthouseResult.audits["largest-contentful-paint"].displayValue // empty' "$last_file" 2>/dev/null)
    fi
  done
fi

# ==== 3. Generate markdown report ====
report="$REPORTS_DIR/${DATE}.md"
cat > "$report" <<HEADER
# Performance check — $DATE

**Tryb:** mobile, single run, PSI Google API (lab simulate ma high variance — używaj jako trend wskaźnik)

**Porównanie do:** ${LAST_DATE:-brak danych historycznych}

| URL | Score | LCP | Δ score | Δ LCP |
|---|---|---|---|---|
HEADER

regressions=0
improvements=0
for entry in "${URLS[@]}"; do
  slug="${entry%%|*}"; path="${entry#*|}"
  now="${scores_now[$slug]}"
  now_lcp="${lcp_now[$slug]}"
  last="${scores_last[$slug]:-}"
  last_lcp="${lcp_last[$slug]:-}"

  if [ -n "$last" ] && [ "$now" != "ERR" ]; then
    delta_score=$(awk -v a="$last" -v b="$now" 'BEGIN { printf "%+.2f", b-a }')
    abs=$(awk -v d="$delta_score" 'BEGIN { d=d+0; print (d < 0 ? -d : d) }')
    if awk -v d="$abs" 'BEGIN { exit !(d >= 0.10) }'; then
      [ "${delta_score:0:1}" = "-" ] && regressions=$((regressions + 1)) || improvements=$((improvements + 1))
    fi
  else
    delta_score="—"
  fi

  delta_lcp=""
  [ -n "$last_lcp" ] && [ -n "$now_lcp" ] && [ "$last_lcp" != "$now_lcp" ] && delta_lcp="$last_lcp → $now_lcp"

  echo "| \`${path}\` | ${now} | ${now_lcp} | ${delta_score} | ${delta_lcp:-=} |" >> "$report"
done

cat >> "$report" <<FOOTER

---

**Summary:** $regressions regression(s) ≥10pts, $improvements improvement(s) ≥10pts.

**Notes:**
- PSI lab simulate ma wysoką wariancję run-to-run (range 0.51-0.96 obserwowane dla tej samej strony). Pojedyncze spadki <10pts ignorowane.
- Real-world signal: CrUX field data (28d window) w GSC Core Web Vitals — bardziej miarodajne.
- Raw JSON: \`30_RESOURCES/perf/raw/${DATE}-*-mobile.json\`

FOOTER

echo "[$DATE] perf_check: report saved $report"

# ==== 4. Alert in INBOX if ≥2 regressions ====
if [ "$regressions" -ge 2 ]; then
  inbox="$BRAIN_DIR/00_INBOX.md"
  if [ -w "$inbox" ] || [ -w "$(dirname "$inbox")" ]; then
    {
      echo ""
      echo "## ⚠️ Performance regression — $DATE"
      echo "**$regressions stron** ze spadkiem ≥10pts vs $LAST_DATE (PSI mobile)."
      echo "Sprawdź raport: \`30_RESOURCES/perf/reports/${DATE}.md\`"
      echo ""
      echo "**Najbardziej dotknięte:**"
      for entry in "${URLS[@]}"; do
        slug="${entry%%|*}"; path="${entry#*|}"
        now="${scores_now[$slug]}"
        last="${scores_last[$slug]:-}"
        if [ -n "$last" ] && [ "$now" != "ERR" ]; then
          delta=$(awk -v a="$last" -v b="$now" 'BEGIN { printf "%+.2f", b-a }')
          if [ "${delta:0:1}" = "-" ]; then
            abs=$(awk -v d="$delta" 'BEGIN { d=d+0; print (d < 0 ? -d : d) }')
            if awk -v d="$abs" 'BEGIN { exit !(d >= 0.10) }'; then
              echo "- \`${path}\`: ${last} → ${now} ($delta)"
            fi
          fi
        fi
      done
    } >> "$inbox"
    echo "[$DATE] perf_check: alert appended to INBOX (regressions=$regressions)"
  fi
fi

# ==== 5. Cleanup raw older than 90 days ====
find "$RAW_DIR" -name "*.json" -mtime +90 -delete 2>/dev/null

echo "[$DATE] perf_check: done"
