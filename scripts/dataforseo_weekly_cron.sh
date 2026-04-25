#!/bin/bash
# Odpalany przez launchd co piątek 08:00.
# Pobiera weekly DataForSEO research i commituje raport do repo.
set -e

cd /Users/ksieradzinski/Projects/dokodu/brain-public

echo "===== $(date '+%Y-%m-%d %H:%M:%S') ====="
echo "Running DataForSEO weekly..."

/usr/bin/env python3 scripts/dataforseo_fetch.py weekly

WEEK=$(date +%G-W%V)
REPORT_DIR="20_AREAS/AREA_Blog_SEO/dataforseo/weekly"

if [ -f "${REPORT_DIR}/${WEEK}.md" ]; then
    git add "${REPORT_DIR}/" || true
    if ! git diff --cached --quiet; then
        git commit -m "feat(seo): DataForSEO weekly ${WEEK} (auto)"
        git push origin main 2>&1 || echo "git push failed (will retry next week)"
    else
        echo "No changes to commit."
    fi
else
    echo "Report ${WEEK}.md not generated — check errors above."
    exit 1
fi

echo "Done."
