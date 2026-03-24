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
import sqlite3
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
DB_FILE      = SCRIPT_DIR / "mailerlite_history.db"

API_BASE = "https://api.mailerlite.com/api/v2"


# ══════════════════════════════════════════════
# HISTORY (SQLite)
# ══════════════════════════════════════════════

def db_connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS snapshots (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            fetched_at  TEXT NOT NULL,
            total       INTEGER NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS group_snapshots (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            snapshot_id INTEGER NOT NULL REFERENCES snapshots(id),
            group_name  TEXT NOT NULL,
            active      INTEGER NOT NULL
        )
    """)
    conn.commit()
    return conn


def save_snapshot(data: dict) -> int:
    """Zapisuje snapshot do SQLite. Zwraca ID snapshotu."""
    conn = db_connect()
    cur = conn.execute(
        "INSERT INTO snapshots (fetched_at, total) VALUES (?, ?)",
        (data["fetched_at"], data["subscriber_count"])
    )
    snap_id = cur.lastrowid
    for g in data.get("groups", []):
        conn.execute(
            "INSERT INTO group_snapshots (snapshot_id, group_name, active) VALUES (?, ?, ?)",
            (snap_id, g.get("name", ""), g.get("active", 0))
        )
    conn.commit()
    conn.close()
    return snap_id


def get_previous_snapshot(current_snap_id: int) -> dict:
    """Zwraca dict {group_name: active} z poprzedniego snapshotu."""
    conn = db_connect()
    row = conn.execute(
        "SELECT id FROM snapshots WHERE id < ? ORDER BY id DESC LIMIT 1",
        (current_snap_id,)
    ).fetchone()
    if not row:
        conn.close()
        return {}
    prev_id = row[0]
    rows = conn.execute(
        "SELECT group_name, active FROM group_snapshots WHERE snapshot_id = ?",
        (prev_id,)
    ).fetchall()
    conn.close()
    return {r[0]: r[1] for r in rows}


def get_history_table(limit: int = 30) -> list[dict]:
    """Zwraca historię snapshots z delta total."""
    conn = db_connect()
    rows = conn.execute(
        "SELECT id, fetched_at, total FROM snapshots ORDER BY id DESC LIMIT ?",
        (limit,)
    ).fetchall()
    conn.close()
    result = []
    for i, (sid, fetched_at, total) in enumerate(rows):
        prev_total = rows[i + 1][2] if i + 1 < len(rows) else None
        delta = (total - prev_total) if prev_total is not None else None
        result.append({"date": fetched_at[:10], "total": total, "delta": delta})
    return result


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

    data = {
        "fetched_at": datetime.now().isoformat(),
        "subscriber_count": count,
        "campaigns": camps,
        "groups": groups,
        "automations": autos,
    }

    print("  → Zapisuję snapshot...", end=" ", flush=True)
    snap_id = save_snapshot(data)
    data["snap_id"] = snap_id
    data["prev_groups"] = get_previous_snapshot(snap_id)
    print(f"✓ (snapshot #{snap_id})")

    return data


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
    count       = data.get("subscriber_count", 0)
    camps       = data.get("campaigns", [])
    groups      = data.get("groups", [])
    autos       = data.get("automations", [])
    prev_groups = data.get("prev_groups", {})

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

    # Historia subskrybentów
    history = get_history_table(10)
    if len(history) > 1:
        lines += [
            "## Historia subskrybentów",
            "",
            "| Data | Łącznie | Zmiana |",
            "|------|---------|--------|",
        ]
        for h in history:
            delta_str = "—"
            if h["delta"] is not None:
                sign = "+" if h["delta"] >= 0 else ""
                delta_str = f"{sign}{h['delta']:,}".replace(",", " ")
            lines.append(f"| {h['date']} | {num(h['total'])} | {delta_str} |")
        lines.append("")

    # Grupy
    if groups:
        has_prev = bool(prev_groups)
        header = "| Nazwa grupy | Aktywni | Zmiana | Sent | Opened | Clicked |" if has_prev else "| Nazwa grupy | Aktywni | Wypisani | Sent | Opened | Clicked |"
        sep    = "|-------------|---------|--------|------|--------|---------|" if has_prev else "|-------------|---------|----------|------|--------|---------|"
        lines += [
            "## Grupy / Segmenty",
            "",
            header,
            sep,
        ]
        for g in groups:
            gname  = g.get("name", "—")
            active = g.get("active", 0)
            sent   = g.get("sent", 0)
            opened = g.get("opened", 0)
            clicked= g.get("clicked", 0)
            if has_prev:
                prev_active = prev_groups.get(gname)
                if prev_active is not None:
                    d = active - prev_active
                    sign = "+" if d >= 0 else ""
                    delta_str = f"{sign}{d}"
                else:
                    delta_str = "nowa"
                lines.append(f"| {gname} | {num(active)} | {delta_str} | {num(sent)} | {num(opened)} | {num(clicked)} |")
            else:
                unsub = g.get("unsubscribed", 0)
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
    parser.add_argument("--history",   type=int, default=0,  metavar="N", help="Pokaż historię N ostatnich snapshotów bez fetchowania")
    args = parser.parse_args()

    if args.history:
        rows = get_history_table(args.history)
        print(f"{'Data':<12} {'Łącznie':>8} {'Zmiana':>8}")
        print("-" * 32)
        for h in rows:
            delta_str = "—"
            if h["delta"] is not None:
                sign = "+" if h["delta"] >= 0 else ""
                delta_str = f"{sign}{h['delta']}"
            print(f"{h['date']:<12} {h['total']:>8,} {delta_str:>8}")
        return

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
