#!/usr/bin/env python3
"""
DOKODU BRAIN — Survey Fetch
Pobiera wyniki ankiet poszkoleniowych z dokodu.it API.
Wyniki trafiają do DOKODU_BRAIN/20_AREAS/AREA_Szkolenia/.

Użycie:
  python3 survey_fetch.py                   # wszystkie ankiety → Markdown
  python3 survey_fetch.py --save            # zapisz do Survey_Last_Sync.md
  python3 survey_fetch.py --token ACME-XK   # konkretna ankieta
  python3 survey_fetch.py --json            # surowy JSON
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

SCRIPT_DIR    = Path(__file__).parent.resolve()
BRAIN_DIR     = SCRIPT_DIR.parent
CONFIG_DIR    = Path.home() / ".config" / "dokodu"
API_KEY_FILE  = CONFIG_DIR / "dokodu_api_key"
AREA_DIR      = BRAIN_DIR / "20_AREAS" / "AREA_Szkolenia"
OUTPUT_FILE   = AREA_DIR / "Survey_Last_Sync.md"

API_BASE = "https://dokodu.it/api/external/surveys/export"


# ══════════════════════════════════════════════
# AUTH
# ══════════════════════════════════════════════

def get_api_key() -> str:
    """Odczytuje klucz API z pliku lub zmiennej środowiskowej."""
    key = os.environ.get("EXTERNAL_API_KEY", "").strip()
    if key:
        return key

    if API_KEY_FILE.exists():
        key = API_KEY_FILE.read_text().strip()
        if key:
            return key

    print("ERROR: Brak klucza API.")
    print(f"  Ustaw zmienną środowiskową EXTERNAL_API_KEY, lub zapisz klucz do:")
    print(f"  {API_KEY_FILE}")
    print(f"  mkdir -p {CONFIG_DIR} && echo 'TWOJ_KLUCZ' > {API_KEY_FILE}")
    sys.exit(1)


# ══════════════════════════════════════════════
# FETCH
# ══════════════════════════════════════════════

def fetch_surveys(token: str | None, fmt: str) -> str | dict:
    """Pobiera dane z API. Zwraca string (MD) lub dict (JSON)."""
    try:
        import urllib.request
        import urllib.parse
        import urllib.error
    except ImportError:
        pass  # always available

    params = {}
    if token:
        params["token"] = token
    if fmt == "json":
        params["format"] = "json"

    url = API_BASE
    if params:
        url += "?" + urllib.parse.urlencode(params)

    api_key = get_api_key()

    req = urllib.request.Request(url, headers={
        "x-api-key": api_key,
        "User-Agent": "Mozilla/5.0 (compatible; DokuduBrain/1.0)",
    })

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read().decode("utf-8")
            if fmt == "json":
                return json.loads(content)
            return content
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        if e.code == 401:
            print("ERROR: Nieprawidłowy klucz API (401 Unauthorized)")
            print(f"  Sprawdź wartość w {API_KEY_FILE} lub zmienną EXTERNAL_API_KEY")
        elif e.code == 404:
            print(f"ERROR: Token nie znaleziony (404) — {body}")
        else:
            print(f"ERROR: HTTP {e.code} — {body}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Nie można połączyć się z API: {e}")
        print("  Sprawdź czy serwer dokodu.it jest dostępny i czy masz dostęp do internetu.")
        sys.exit(1)


# ══════════════════════════════════════════════
# SAVE
# ══════════════════════════════════════════════

def save_to_brain(content: str) -> None:
    AREA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(content, encoding="utf-8")
    print(f"✓ Zapisano do: {OUTPUT_FILE}")


# ══════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Pobiera wyniki ankiet z dokodu.it")
    parser.add_argument("--token",  help="Konkretny token ankiety (np. ACME-XK7P2Q)")
    parser.add_argument("--json",   action="store_true", help="Zwróć surowy JSON")
    parser.add_argument("--save",   action="store_true", help="Zapisz wyniki do BRAIN")
    args = parser.parse_args()

    fmt = "json" if args.json else "markdown"

    print(f"Pobieram ankiety z {API_BASE}...")
    if args.token:
        print(f"  Token: {args.token}")

    result = fetch_surveys(args.token, fmt)

    if args.json:
        data = result if isinstance(result, dict) else {}
        surveys = data.get("surveys", [])
        total_responses = sum(len(s.get("responses", [])) for s in surveys)
        print(f"✓ Pobrano {len(surveys)} tokenów | {total_responses} odpowiedzi")
        print()
        print(json.dumps(data, indent=2, ensure_ascii=False, default=str))
        return

    # Markdown mode
    md = result if isinstance(result, str) else ""
    # Quick summary from first lines
    lines = md.splitlines()
    for line in lines[:5]:
        if line.startswith(">"):
            print(line.lstrip("> "))

    print()

    if args.save:
        save_to_brain(md)
        print()
        print("Następny krok: /survey-stats — analiza i wnioski")
    else:
        print(md)


if __name__ == "__main__":
    main()
