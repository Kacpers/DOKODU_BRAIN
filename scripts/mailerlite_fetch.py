#!/usr/bin/env python3
"""
DOKODU BRAIN — MailerLite Fetch (Classic API v2)
Pobiera dane z MailerLite Classic API: subskrybenci, kampanie, grupy, automatyzacje.
Wyniki trafiają do DOKODU_BRAIN/20_AREAS/AREA_Newsletter/.

Użycie:
  python3 mailerlite_fetch.py                   # pełny raport → Markdown
  python3 mailerlite_fetch.py --save            # zapisz do Newsletter_Last_Sync.md
  python3 mailerlite_fetch.py --json            # surowy JSON (debug)
  python3 mailerlite_fetch.py --campaigns 30    # ostatnie 30 kampanii (domyślnie 20)

Dokumentacja: https://developers-classic.mailerlite.com/docs/
API key: ~/.config/dokodu/mailerlite_api_key lub env MAILERLITE_API_KEY
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime
from pathlib import Path

SCRIPT_DIR   = Path(__file__).parent.resolve()
BRAIN_DIR    = SCRIPT_DIR.parent
CONFIG_DIR   = Path.home() / ".config" / "dokodu"
API_KEY_FILE = CONFIG_DIR / "mailerlite_api_key"
AREA_DIR     = BRAIN_DIR / "20_AREAS" / "AREA_Newsletter"
OUTPUT_FILE  = AREA_DIR / "Newsletter_Last_Sync.md"

API_BASE = "https://api.mailerlite.com/api/v2"


# ══════════════════════════════════════════════
# AUTH
# ══════════════════════════════════════════════

def get_api_key() -> str:
    key = os.environ.get("MAILERLITE_API_KEY", "").strip()
    if key:
        return key
    if API_KEY_FILE.exists():
        key = API_KEY_FILE.read_text().strip()
        if key:
            return key
    print("ERROR: Brak klucza API MailerLite.")
    print(f"  echo 'TWOJ_KLUCZ' > {API_KEY_FILE}")
    print("  Klucz API: MailerLite Classic → Integrations → Developer API")
    sys.exit(1)


def ml_get(path: str, params: dict = None) -> dict | list:
    """GET request do MailerLite Classic API v2."""
    api_key = get_api_key()
    url = f"{API_BASE}/{path.lstrip('/')}"
    if params:
        url += "?" + urllib.parse.urlencode(params)

    req = urllib.request.Request(url, headers={
        "X-MailerLite-ApiKey": api_key,
        # User-Agent musi być curl-like — MailerLite blokuje Python-urllib
        "User-Agent": "curl/7.88.1",
    })

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        if e.code == 401:
            print(f"ERROR: Nieprawidłowy klucz API (401). Sprawdź {API_KEY_FILE}")
        elif e.code == 403:
            print(f"ERROR: Brak dostępu (403) do {path}. Sprawdź uprawnienia API key.")
        elif e.code == 429:
            print("ERROR: Limit zapytań API (429). Poczekaj chwilę.")
        else:
            print(f"ERROR: HTTP {e.code} dla {path}: {body[:200]}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Nie można połączyć się z MailerLite: {e}")
        sys.exit(1)


# ══════════════════════════════════════════════
# FETCH
# ══════════════════════════════════════════════

def fetch_subscriber_count() -> int:
    r = ml_get("subscribers/count")
    return r.get("count", 0)


def fetch_campaigns(limit: int = 20) -> list:
    """Ostatnie wysłane kampanie z open/click rate."""
    return ml_get("campaigns/sent", {"limit": limit}) or []


def fetch_groups() -> list:
    """Grupy subskrybentów z liczbą aktywnych."""
    return ml_get("groups", {"limit": 100}) or []


def fetch_automations() -> list:
    """Automatyzacje (workflows)."""
    try:
        result = ml_get("automations", {"limit": 25})
        return result if isinstance(result, list) else []
    except SystemExit:
        return []


def fetch_all(campaigns_limit: int = 20) -> dict:
    print("  → Liczba subskrybentów...", end=" ", flush=True)
    count = fetch_subscriber_count()
    print(f"✓ ({count:,} total)")

    print("  → Kampanie...", end=" ", flush=True)
    camps = fetch_campaigns(campaigns_limit)
    print(f"✓ ({len(camps)} kampanii)")

    print("  → Grupy...", end=" ", flush=True)
    groups = fetch_groups()
    print(f"✓ ({len(groups)} grup)")

    print("  → Automatyzacje...", end=" ", flush=True)
    autos = fetch_automations()
    print(f"✓ ({len(autos)} automatyzacji)")

    return {
        "fetched_at": datetime.now().isoformat(),
        "subscriber_count": count,
        "campaigns": camps,
        "groups": groups,
        "automations": autos,
    }


# ══════════════════════════════════════════════
# FORMAT
# ══════════════════════════════════════════════

def num(val) -> str:
    if val is None:
        return "—"
    try:
        return f"{int(val):,}".replace(",", " ")
    except (ValueError, TypeError):
        return str(val)


def pct(val) -> str:
    if val is None:
        return "—"
    try:
        return f"{float(val):.1f}%"
    except (ValueError, TypeError):
        return str(val)


def shorten(text: str, max_len: int = 50) -> str:
    if not text:
        return "—"
    text = str(text)
    return text[:max_len] + "…" if len(text) > max_len else text


def format_markdown(data: dict) -> str:
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    count   = data.get("subscriber_count", 0)
    camps   = data.get("campaigns", [])
    groups  = data.get("groups", [])
    autos   = data.get("automations", [])

    lines = []

    # Frontmatter
    lines += [
        "---",
        f"last_updated: {now_str}",
        f"subscriber_count: {count}",
        f"campaigns_fetched: {len(camps)}",
        "source: mailerlite_classic_v2",
        "---",
        "",
        "# Newsletter — MailerLite Sync",
        f"> Ostatnia synchronizacja: {now_str}",
        "",
        "---",
        "",
        "## Subskrybenci",
        "",
        f"**Łączna liczba subskrybentów:** {num(count)}",
        "",
    ]

    # Grupy
    if groups:
        lines += [
            "## Grupy / Segmenty",
            "",
            "| Nazwa grupy | Aktywni | Wypisani | Sent | Opened | Clicked |",
            "|-------------|---------|----------|------|--------|---------|",
        ]
        for g in groups:
            gname  = g.get("name", "—")
            active = g.get("active", 0)
            unsub  = g.get("unsubscribed", 0)
            sent   = g.get("sent", 0)
            opened = g.get("opened", 0)
            clicked= g.get("clicked", 0)
            lines.append(f"| {gname} | {num(active)} | {num(unsub)} | {num(sent)} | {num(opened)} | {num(clicked)} |")
        lines.append("")

    # Automatyzacje
    if autos:
        lines += [
            "## Automatyzacje",
            "",
            "| Nazwa | Status |",
            "|-------|--------|",
        ]
        for a in autos:
            aname   = shorten(a.get("name", "—"), 50)
            astatus = str(a.get("status", a.get("enabled", "—")))
            lines.append(f"| {aname} | {astatus} |")
        lines.append("")

    # Kampanie
    if camps:
        lines += [
            "## Kampanie (ostatnie wysłane)",
            "",
            "| Kampania | Wysłane | Open Rate | CTR | Data wysyłki |",
            "|----------|---------|-----------|-----|--------------|",
        ]

        open_rates  = []
        click_rates = []

        for c in camps:
            cname  = shorten(c.get("name", "—"), 45)
            csent  = c.get("total_recipients", "?")
            cdate  = (c.get("date_send") or c.get("date_created") or "")[:10]

            opened  = c.get("opened", {})
            clicked = c.get("clicked", {})

            o_rate = opened.get("rate") if isinstance(opened, dict) else opened
            c_rate = clicked.get("rate") if isinstance(clicked, dict) else clicked

            lines.append(f"| {cname} | {num(csent)} | {pct(o_rate)} | {pct(c_rate)} | {cdate} |")

            if o_rate is not None:
                try:
                    open_rates.append(float(o_rate))
                except (ValueError, TypeError):
                    pass
            if c_rate is not None:
                try:
                    click_rates.append(float(c_rate))
                except (ValueError, TypeError):
                    pass

        lines.append("")

        if open_rates:
            avg_open  = sum(open_rates) / len(open_rates)
            avg_click = sum(click_rates) / len(click_rates) if click_rates else 0
            best_camp = max(camps, key=lambda c: float(c.get("opened", {}).get("rate", 0) if isinstance(c.get("opened"), dict) else 0))
            lines += [
                "### Podsumowanie statystyk",
                "",
                f"- **Avg Open Rate:** {avg_open:.1f}% *(benchmark SaaS/Edu PL: 25–35%)*",
                f"- **Avg CTR:** {avg_click:.1f}% *(benchmark: 3–5%)*",
                f"- **Najlepsza kampania:** {shorten(best_camp.get('name',''), 60)} ({pct(best_camp.get('opened',{}).get('rate'))} open rate)",
                f"- **Kampanie w próbie:** {len(camps)}",
                "",
            ]

    lines += [
        "---",
        f"*Wygenerowano: {now_str} | mailerlite_fetch.py (Classic API v2)*",
    ]

    return "\n".join(lines)


# ══════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Pobiera dane z MailerLite Classic API v2")
    parser.add_argument("--save",      action="store_true", help="Zapisz do BRAIN")
    parser.add_argument("--json",      action="store_true", help="Surowy JSON (debug)")
    parser.add_argument("--campaigns", type=int, default=20, help="Liczba kampanii (domyślnie 20)")
    args = parser.parse_args()

    api_key = get_api_key()
    print(f"MailerLite Fetch (Classic API v2) — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"API key: {'*' * 8}{api_key[-4:]}")
    print()

    data = fetch_all(args.campaigns)

    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False, default=str))
        return

    md = format_markdown(data)

    if args.save:
        AREA_DIR.mkdir(parents=True, exist_ok=True)
        OUTPUT_FILE.write_text(md, encoding="utf-8")
        print()
        print(f"✓ Zapisano do: {OUTPUT_FILE}")
        print()
        print(f"  Subskrybenci:     {num(data.get('subscriber_count', '?'))}")
        print(f"  Kampanie pobrane: {len(data.get('campaigns', []))}")
        print()
        print("Następny krok: /mailerlite-stats — analiza i rekomendacje")
    else:
        print(md)


if __name__ == "__main__":
    main()
