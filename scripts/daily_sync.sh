#!/bin/bash
# DOKODU BRAIN — Daily Sync
# Odpala się co godzinę, ale wykonuje pracę tylko raz dziennie.
# Logika: sprawdza czy dziś już był sync, jeśli nie — odpala wszystkie skrypty.

LOCK_FILE="/tmp/dokodu_daily_sync.lock"
LOG_FILE="/tmp/dokodu_cron.log"
TODAY=$(date +%Y-%m-%d)

# Sprawdź czy dziś już był sync
if [ -f "$LOCK_FILE" ]; then
    LAST_RUN=$(cat "$LOCK_FILE")
    if [ "$LAST_RUN" = "$TODAY" ]; then
        exit 0  # Już dzisiaj uruchomiony — nic nie rób
    fi
fi

echo "[$TODAY $(date +%H:%M)] Dzienny sync start" >> "$LOG_FILE"

# GSC
echo "  → GSC..." >> "$LOG_FILE"
python3 /home/kacper/DOKODU_BRAIN/scripts/gsc_fetch.py --days 28 --save >> "$LOG_FILE" 2>&1
echo "  ✓ GSC done" >> "$LOG_FILE"

# GA4
echo "  → GA4..." >> "$LOG_FILE"
python3 /home/kacper/DOKODU_BRAIN/scripts/ga_fetch.py --days 28 --save >> "$LOG_FILE" 2>&1
echo "  ✓ GA4 done" >> "$LOG_FILE"

# MailerLite
echo "  → MailerLite..." >> "$LOG_FILE"
python3 /home/kacper/DOKODU_BRAIN/scripts/mailerlite_fetch.py --save >> "$LOG_FILE" 2>&1
echo "  ✓ MailerLite done" >> "$LOG_FILE"

# YT — tylko w poniedziałek
if [ "$(date +%u)" = "1" ]; then
    echo "  → YouTube (poniedziałek)..." >> "$LOG_FILE"
    python3 /home/kacper/DOKODU_BRAIN/scripts/youtube_fetch.py --save >> "$LOG_FILE" 2>&1
    echo "  ✓ YT done" >> "$LOG_FILE"
fi

# Sprawdź REMINDERS.md i wstrzyknij do INBOX jeśli termin nadszedł
REMINDERS_FILE="/home/kacper/DOKODU_BRAIN/REMINDERS.md"
INBOX_FILE="/home/kacper/DOKODU_BRAIN/00_INBOX.md"

if [ -f "$REMINDERS_FILE" ]; then
    DUE=$(grep -E "^- $TODAY \|" "$REMINDERS_FILE" 2>/dev/null)
    if [ -n "$DUE" ]; then
        echo "  → Reminders do INBOX..." >> "$LOG_FILE"
        echo "" >> "$INBOX_FILE"
        echo "## Przypomnienia z $TODAY" >> "$INBOX_FILE"
        echo "$DUE" | while IFS= read -r line; do
            # Usuń datę z początku: "- YYYY-MM-DD | KAT | Treść" → "- [KAT] Treść"
            entry=$(echo "$line" | sed 's/^- [0-9-]* | \([A-Z]*\) | /- [\1] /')
            echo "$entry" >> "$INBOX_FILE"
        done
        echo "  ✓ Reminders wstrzyknięte do INBOX" >> "$LOG_FILE"
    fi
fi

# Gmail
echo "  → Gmail..." >> "$LOG_FILE"
python3 /home/kacper/DOKODU_BRAIN/scripts/gmail_fetch.py --days 2 >> "$LOG_FILE" 2>&1
echo "  ✓ Gmail done" >> "$LOG_FILE"

# Git commit & push
echo "  → Git push..." >> "$LOG_FILE"
cd /home/kacper/DOKODU_BRAIN
git add -A
git diff --cached --quiet || git commit -m "sync: dzienny update $TODAY [auto]" >> "$LOG_FILE" 2>&1
git push origin main >> "$LOG_FILE" 2>&1
echo "  ✓ Git push done" >> "$LOG_FILE"

# Zapisz datę wykonania
echo "$TODAY" > "$LOCK_FILE"
echo "[$TODAY $(date +%H:%M)] Dzienny sync zakończony" >> "$LOG_FILE"
