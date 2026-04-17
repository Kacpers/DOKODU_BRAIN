#!/usr/bin/env python3
"""
DOKODU BRAIN — Google Search Console Integration
Autor: Kacper Sieradzinski | Dokodu sp. z o.o.

Pobiera dane z Google Search Console API.
Wyniki trafiają do DOKODU_BRAIN/20_AREAS/AREA_Blog_SEO/.

Użycie:
  python3 gsc_fetch.py                        # pełny raport (28 dni)
  python3 gsc_fetch.py --days 90              # ostatnie 90 dni
  python3 gsc_fetch.py --mode queries         # tylko zapytania
  python3 gsc_fetch.py --mode pages           # tylko strony
  python3 gsc_fetch.py --mode opportunities   # tylko low-hanging fruit
  python3 gsc_fetch.py --save                 # zapisz do BRAIN
  python3 gsc_fetch.py --from-db              # czytaj z lokalnej bazy (bez API)
  python3 gsc_fetch.py --json                 # surowy JSON
"""

import os
import sys
import json
import pickle
import sqlite3
import argparse
from datetime import datetime, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
BRAIN_DIR  = SCRIPT_DIR.parent
CONFIG_DIR = Path.home() / ".config" / "dokodu"
CREDENTIALS_FILE = CONFIG_DIR / "gsc_credentials.json"
TOKEN_FILE       = CONFIG_DIR / "gsc_token.pickle"
DB_FILE          = CONFIG_DIR / "gsc_data.db"
AREA_SEO_DIR     = BRAIN_DIR / "20_AREAS" / "AREA_Blog_SEO"

SITE_URL = "https://dokodu.it/"

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("ERROR: Brak wymaganych bibliotek Google. Zainstaluj je:")
    print("  pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
    sys.exit(1)

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]


# ══════════════════════════════════════════════
# DATABASE
# ══════════════════════════════════════════════

def db_connect() -> sqlite3.Connection:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def db_init(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS gsc_queries (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            fetched_at   TEXT NOT NULL,
            period_start TEXT NOT NULL,
            period_end   TEXT NOT NULL,
            query        TEXT NOT NULL,
            clicks       INTEGER,
            impressions  INTEGER,
            ctr          REAL,
            position     REAL,
            UNIQUE(period_start, period_end, query)
        );

        CREATE TABLE IF NOT EXISTS gsc_pages (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            fetched_at   TEXT NOT NULL,
            period_start TEXT NOT NULL,
            period_end   TEXT NOT NULL,
            page         TEXT NOT NULL,
            clicks       INTEGER,
            impressions  INTEGER,
            ctr          REAL,
            position     REAL,
            UNIQUE(period_start, period_end, page)
        );

        CREATE TABLE IF NOT EXISTS gsc_query_page (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            fetched_at   TEXT NOT NULL,
            period_start TEXT NOT NULL,
            period_end   TEXT NOT NULL,
            query        TEXT NOT NULL,
            page         TEXT NOT NULL,
            clicks       INTEGER,
            impressions  INTEGER,
            ctr          REAL,
            position     REAL,
            UNIQUE(period_start, period_end, query, page)
        );

        CREATE TABLE IF NOT EXISTS gsc_snapshots (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            fetched_at   TEXT NOT NULL,
            period_start TEXT NOT NULL,
            period_end   TEXT NOT NULL,
            total_clicks INTEGER,
            total_impressions INTEGER,
            avg_ctr      REAL,
            avg_position REAL
        );
    """)
    conn.commit()


def db_save(conn, queries, pages, query_pages, start_date, end_date):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for q in queries:
        conn.execute("""
            INSERT OR REPLACE INTO gsc_queries
            (fetched_at, period_start, period_end, query, clicks, impressions, ctr, position)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (now, start_date, end_date, q["query"], q["clicks"],
              q["impressions"], q["ctr"], q["position"]))

    for p in pages:
        conn.execute("""
            INSERT OR REPLACE INTO gsc_pages
            (fetched_at, period_start, period_end, page, clicks, impressions, ctr, position)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (now, start_date, end_date, p["page"], p["clicks"],
              p["impressions"], p["ctr"], p["position"]))

    for qp in query_pages:
        conn.execute("""
            INSERT OR REPLACE INTO gsc_query_page
            (fetched_at, period_start, period_end, query, page, clicks, impressions, ctr, position)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (now, start_date, end_date, qp["query"], qp["page"],
              qp["clicks"], qp["impressions"], qp["ctr"], qp["position"]))

    if queries:
        total_clicks = sum(q["clicks"] for q in queries)
        total_impressions = sum(q["impressions"] for q in queries)
        avg_ctr = sum(q["ctr"] for q in queries) / len(queries) if queries else 0
        avg_pos = sum(q["position"] for q in queries) / len(queries) if queries else 0
        conn.execute("""
            INSERT INTO gsc_snapshots
            (fetched_at, period_start, period_end, total_clicks, total_impressions, avg_ctr, avg_position)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (now, start_date, end_date, total_clicks, total_impressions, avg_ctr, avg_pos))

    conn.commit()
    print(f"✅ Zapisano do bazy: {DB_FILE}", file=sys.stderr)


def db_read_latest(conn) -> dict:
    snap = conn.execute(
        "SELECT * FROM gsc_snapshots ORDER BY fetched_at DESC LIMIT 1"
    ).fetchone()
    if not snap:
        return {}

    start = snap["period_start"]
    end   = snap["period_end"]

    queries = conn.execute("""
        SELECT * FROM gsc_queries
        WHERE period_start = ? AND period_end = ?
        ORDER BY clicks DESC LIMIT 100
    """, (start, end)).fetchall()

    pages = conn.execute("""
        SELECT * FROM gsc_pages
        WHERE period_start = ? AND period_end = ?
        ORDER BY clicks DESC LIMIT 50
    """, (start, end)).fetchall()

    return {
        "snapshot": dict(snap),
        "queries": [dict(r) for r in queries],
        "pages":   [dict(r) for r in pages],
        "start": start,
        "end": end,
    }


# ══════════════════════════════════════════════
# AUTH
# ══════════════════════════════════════════════

def authenticate():
    creds = None

    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Token wygasł: {e}", file=sys.stderr)
                creds = None

        if not creds:
            if not CREDENTIALS_FILE.exists():
                print(f"\n❌ BRAK PLIKU CREDENTIALS!")
                print(f"Oczekiwany plik: {CREDENTIALS_FILE}")
                print("\nSzczegóły: DOKODU_BRAIN/scripts/GSC_SETUP.md")
                sys.exit(1)

            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            print("\n" + "="*60, file=sys.stderr)
            print("🌐 WYMAGANA AUTORYZACJA GOOGLE SEARCH CONSOLE", file=sys.stderr)
            print("="*60, file=sys.stderr)
            print("Otwórz URL w przeglądarce Windows i zaloguj się.", file=sys.stderr)
            print("="*60 + "\n", file=sys.stderr)
            creds = flow.run_local_server(port=0, open_browser=False)

        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)
        print("✅ Token zapisany.", file=sys.stderr)

    return creds


# ══════════════════════════════════════════════
# FETCH FUNCTIONS
# ══════════════════════════════════════════════

def fetch_search_analytics(service, start_date: str, end_date: str,
                           dimensions: list, row_limit: int = 1000) -> list:
    try:
        resp = service.searchanalytics().query(
            siteUrl=SITE_URL,
            body={
                "startDate": start_date,
                "endDate":   end_date,
                "dimensions": dimensions,
                "rowLimit":  row_limit,
                "startRow":  0,
            }
        ).execute()
        return resp.get("rows", [])
    except HttpError as e:
        print(f"⚠️  GSC API error ({dimensions}): {e}", file=sys.stderr)
        return []


def parse_rows(rows: list, dimensions: list) -> list:
    result = []
    for row in rows:
        entry = {}
        for i, dim in enumerate(dimensions):
            entry[dim] = row["keys"][i]
        entry["clicks"]      = int(row.get("clicks", 0))
        entry["impressions"] = int(row.get("impressions", 0))
        entry["ctr"]         = round(row.get("ctr", 0) * 100, 2)   # jako procent
        entry["position"]    = round(row.get("position", 0), 1)
        result.append(entry)
    return result


# ══════════════════════════════════════════════
# ANALYSIS — OPPORTUNITIES
# ══════════════════════════════════════════════

def find_opportunities(queries: list, pages: list) -> dict:
    """Identyfikuje low-hanging fruit i content gaps."""

    # Zapytania na pozycjach 4-15 z wysokimi impressions → warto optymalizować
    quick_wins = [
        q for q in queries
        if 4 <= q["position"] <= 15 and q["impressions"] >= 50
    ]
    quick_wins.sort(key=lambda x: x["impressions"], reverse=True)

    # Zapytania z dobrą pozycją ale niskim CTR (poniżej 3%) → problem z tytułem/meta
    low_ctr = [
        q for q in queries
        if q["position"] <= 10 and q["ctr"] < 3.0 and q["impressions"] >= 30
    ]
    low_ctr.sort(key=lambda x: x["impressions"], reverse=True)

    # Zapytania na poz. 1-3 — co już dominujemy
    top_performers = [q for q in queries if q["position"] <= 3 and q["clicks"] > 0]
    top_performers.sort(key=lambda x: x["clicks"], reverse=True)

    # Strony bez ruchu z wysokimi impressions → potencjał SEO
    pages_no_clicks = [
        p for p in pages
        if p["clicks"] == 0 and p["impressions"] >= 20
    ]
    pages_no_clicks.sort(key=lambda x: x["impressions"], reverse=True)

    # Strony z wysokim ruchem → evergreen content
    top_pages = sorted(pages, key=lambda x: x["clicks"], reverse=True)[:10]

    return {
        "quick_wins":      quick_wins[:20],
        "low_ctr":         low_ctr[:15],
        "top_performers":  top_performers[:10],
        "pages_no_clicks": pages_no_clicks[:10],
        "top_pages":       top_pages,
    }


# ══════════════════════════════════════════════
# OUTPUT
# ══════════════════════════════════════════════

def _pct(ctr: float) -> str:
    return f"{ctr:.1f}%"


def _pos(p: float) -> str:
    return f"#{p:.1f}"


def _short_url(url: str) -> str:
    return url.replace(SITE_URL.rstrip("/"), "") or "/"


def build_markdown_report(queries: list, pages: list, opportunities: dict,
                          start_date: str, end_date: str, mode: str) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    days = (datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days

    total_clicks      = sum(q["clicks"] for q in queries)
    total_impressions = sum(q["impressions"] for q in queries)
    avg_ctr = (sum(q["ctr"] for q in queries) / len(queries)) if queries else 0
    avg_pos = (sum(q["position"] for q in queries) / len(queries)) if queries else 0

    lines = [
        f"# Google Search Console — dokodu.it",
        f"Pobrano: {now} | Okres: {start_date} → {end_date} ({days} dni)",
        "",
        "## Podsumowanie",
        "| Metryka | Wartość |",
        "|---------|---------|",
        f"| Łączne kliknięcia | **{total_clicks:,}** |",
        f"| Łączne wyświetlenia | {total_impressions:,} |",
        f"| Średni CTR | {avg_ctr:.2f}% |",
        f"| Średnia pozycja | #{avg_pos:.1f} |",
        f"| Unikalne zapytania | {len(queries)} |",
        f"| Unikalne strony | {len(pages)} |",
        "",
    ]

    if mode in ("all", "queries"):
        lines += [
            "## Top 30 Zapytań (wg kliknięć)",
            "",
            "| # | Zapytanie | Kliknięcia | Impressions | CTR | Pozycja |",
            "|---|-----------|-----------|-------------|-----|---------|",
        ]
        for i, q in enumerate(queries[:30], 1):
            lines.append(
                f"| {i} | {q['query']} | {q['clicks']:,} | {q['impressions']:,} | "
                f"{_pct(q['ctr'])} | {_pos(q['position'])} |"
            )
        lines.append("")

    if mode in ("all", "pages"):
        lines += [
            "## Top 20 Stron (wg kliknięć)",
            "",
            "| # | Strona | Kliknięcia | Impressions | CTR | Pozycja |",
            "|---|--------|-----------|-------------|-----|---------|",
        ]
        for i, p in enumerate(pages[:20], 1):
            lines.append(
                f"| {i} | `{_short_url(p['page'])}` | {p['clicks']:,} | {p['impressions']:,} | "
                f"{_pct(p['ctr'])} | {_pos(p['position'])} |"
            )
        lines.append("")

    if mode in ("all", "opportunities"):
        opp = opportunities

        lines += [
            "## Quick Wins — Pozycje 4-15 z potencjałem (≥50 impressions)",
            "> Małe poprawki on-page mogą przesunąć te frazy na top 3",
            "",
            "| Zapytanie | Impressions | Kliknięcia | CTR | Pozycja |",
            "|-----------|-------------|-----------|-----|---------|",
        ]
        for q in opp["quick_wins"][:15]:
            lines.append(
                f"| {q['query']} | {q['impressions']:,} | {q['clicks']:,} | "
                f"{_pct(q['ctr'])} | {_pos(q['position'])} |"
            )
        lines.append("")

        lines += [
            "## Niski CTR — Dobra Pozycja, Słaby Tytuł/Meta",
            "> Te frazy są w top 10, ale nikt nie klika — popraw tytuł strony lub meta description",
            "",
            "| Zapytanie | Impressions | Kliknięcia | CTR | Pozycja |",
            "|-----------|-------------|-----------|-----|---------|",
        ]
        for q in opp["low_ctr"][:10]:
            lines.append(
                f"| {q['query']} | {q['impressions']:,} | {q['clicks']:,} | "
                f"{_pct(q['ctr'])} | {_pos(q['position'])} |"
            )
        lines.append("")

        if opp["top_performers"]:
            lines += [
                "## Top Performers — Dominujące Frazy (poz. 1-3)",
                "",
                "| Zapytanie | Kliknięcia | Impressions | CTR | Pozycja |",
                "|-----------|-----------|-------------|-----|---------|",
            ]
            for q in opp["top_performers"][:10]:
                lines.append(
                    f"| {q['query']} | {q['clicks']:,} | {q['impressions']:,} | "
                    f"{_pct(q['ctr'])} | {_pos(q['position'])} |"
                )
            lines.append("")

        if opp["pages_no_clicks"]:
            lines += [
                "## Strony z Impressions ale bez Kliknięć — Content Gap",
                "> Te strony są widoczne w Google ale nikt nie klika — wymagają optymalizacji",
                "",
                "| Strona | Impressions | Pozycja |",
                "|--------|-------------|---------|",
            ]
            for p in opp["pages_no_clicks"][:10]:
                lines.append(
                    f"| `{_short_url(p['page'])}` | {p['impressions']:,} | {_pos(p['position'])} |"
                )
            lines.append("")

    lines += ["---", f"*DOKODU BRAIN GSC Integration | {now}*"]
    return "\n".join(lines)


def save_to_brain(report_md: str) -> None:
    out_file = AREA_SEO_DIR / "SEO_Last_Sync.md"
    out_file.write_text(report_md, encoding="utf-8")
    print(f"✅ Zapisano: {out_file}", file=sys.stderr)


# ══════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="DOKODU BRAIN — GSC Fetch")
    parser.add_argument("--mode", choices=["queries", "pages", "opportunities", "all"],
                        default="all")
    parser.add_argument("--days",      type=int, default=28, help="Ile dni wstecz")
    parser.add_argument("--row-limit", type=int, default=500, help="Max wierszy na wymiar")
    global SITE_URL
    parser.add_argument("--site",      default=SITE_URL, help="URL strony w GSC")
    parser.add_argument("--save",      action="store_true", help="Zapisz do BRAIN")
    parser.add_argument("--from-db",   action="store_true", help="Czytaj z bazy (bez API)")
    parser.add_argument("--json",      action="store_true", dest="as_json")
    args = parser.parse_args()

    SITE_URL = args.site

    conn = db_connect()
    db_init(conn)

    end_date   = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")  # GSC ma 3-dniowy lag
    start_date = (datetime.now() - timedelta(days=args.days + 3)).strftime("%Y-%m-%d")

    # Tryb offline
    if args.from_db:
        print("📂 Czytam z lokalnej bazy...", file=sys.stderr)
        data = db_read_latest(conn)
        conn.close()
        if not data:
            print("❌ Baza jest pusta. Uruchom bez --from-db.", file=sys.stderr)
            sys.exit(1)
        if args.as_json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            opp = find_opportunities(data["queries"], data["pages"])
            print(build_markdown_report(
                data["queries"], data["pages"], opp,
                data["start"], data["end"], args.mode
            ))
        return

    # Tryb online
    print("🔐 Logowanie do Google Search Console...", file=sys.stderr)
    creds   = authenticate()
    service = build("searchconsole", "v1", credentials=creds)

    print(f"📡 Pobieranie danych za {args.days} dni ({start_date} → {end_date})...", file=sys.stderr)

    queries     = []
    pages       = []
    query_pages = []

    print("🔍 Zapytania...", file=sys.stderr)
    raw_queries = fetch_search_analytics(service, start_date, end_date,
                                         ["query"], args.row_limit)
    queries = parse_rows(raw_queries, ["query"])
    queries.sort(key=lambda x: x["clicks"], reverse=True)

    print("📄 Strony...", file=sys.stderr)
    raw_pages = fetch_search_analytics(service, start_date, end_date,
                                       ["page"], args.row_limit)
    pages = parse_rows(raw_pages, ["page"])
    pages.sort(key=lambda x: x["clicks"], reverse=True)

    print("🔗 Zapytania × Strony...", file=sys.stderr)
    raw_qp = fetch_search_analytics(service, start_date, end_date,
                                    ["query", "page"], min(args.row_limit, 500))
    query_pages = parse_rows(raw_qp, ["query", "page"])

    db_save(conn, queries, pages, query_pages, start_date, end_date)
    conn.close()

    if args.as_json:
        print(json.dumps({
            "period": {"start": start_date, "end": end_date, "days": args.days},
            "queries": queries,
            "pages":   pages,
        }, ensure_ascii=False, indent=2))
        return

    opportunities = find_opportunities(queries, pages)
    report = build_markdown_report(queries, pages, opportunities,
                                   start_date, end_date, args.mode)
    print(report)

    if args.save:
        save_to_brain(report)


if __name__ == "__main__":
    main()
