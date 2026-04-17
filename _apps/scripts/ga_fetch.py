#!/usr/bin/env python3
"""
DOKODU BRAIN — Google Analytics 4 Fetch
Pobiera dane z GA4 Data API i zapisuje do SQLite + Markdown.

Użycie:
  python3 ga_fetch.py --days 28 --save
  python3 ga_fetch.py --days 7 --save
  python3 ga_fetch.py --from-db --mode pages

Dane zapisywane do:
  ~/.config/dokodu/ga_data.db
  BRAIN/20_AREAS/AREA_Blog_SEO/GA_Last_Sync.md
"""

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
CREDENTIALS_FILE = CONFIG_DIR / "gsc_credentials.json"   # ten sam plik OAuth co GSC
TOKEN_FILE       = CONFIG_DIR / "ga_token.pickle"
DB_FILE          = CONFIG_DIR / "ga_data.db"
AREA_SEO_DIR     = BRAIN_DIR / "20_AREAS" / "AREA_Blog_SEO"

PROPERTY_ID = "properties/386471428"

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

# GA4 Data API scope
SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]


# ══════════════════════════════════════════════
# AUTH
# ══════════════════════════════════════════════

def get_credentials():
    creds = None
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                print(f"ERROR: Brak pliku credentials: {CREDENTIALS_FILE}")
                print("Użyj tego samego pliku co GSC (gsc_credentials.json)")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            flow.redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
            auth_url, _ = flow.authorization_url(prompt="consent")
            print(f"\n  Otwórz ten URL w przeglądarce:\n\n  {auth_url}\n")
            code = input("  Wklej kod autoryzacyjny: ").strip()
            flow.fetch_token(code=code)
            creds = flow.credentials
        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)
    return creds


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
        CREATE TABLE IF NOT EXISTS ga_pages (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            fetched_at   TEXT NOT NULL,
            period_start TEXT NOT NULL,
            period_end   TEXT NOT NULL,
            page         TEXT NOT NULL,
            sessions     INTEGER DEFAULT 0,
            users        INTEGER DEFAULT 0,
            new_users    INTEGER DEFAULT 0,
            pageviews    INTEGER DEFAULT 0,
            bounce_rate  REAL DEFAULT 0,
            avg_duration REAL DEFAULT 0,
            scroll_depth REAL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS ga_sources (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            fetched_at   TEXT NOT NULL,
            period_start TEXT NOT NULL,
            period_end   TEXT NOT NULL,
            source       TEXT NOT NULL,
            medium       TEXT NOT NULL,
            sessions     INTEGER DEFAULT 0,
            users        INTEGER DEFAULT 0,
            conversions  INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS ga_events (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            fetched_at   TEXT NOT NULL,
            period_start TEXT NOT NULL,
            period_end   TEXT NOT NULL,
            event_name   TEXT NOT NULL,
            page         TEXT,
            count        INTEGER DEFAULT 0
        );
    """)
    conn.commit()


# ══════════════════════════════════════════════
# FETCH
# ══════════════════════════════════════════════

def fetch_pages(service, start_date: str, end_date: str) -> list[dict]:
    """Pobiera statystyki per strona."""
    response = service.properties().runReport(
        property=PROPERTY_ID,
        body={
            "dateRanges": [{"startDate": start_date, "endDate": end_date}],
            "dimensions": [{"name": "pagePath"}],
            "metrics": [
                {"name": "sessions"},
                {"name": "totalUsers"},
                {"name": "newUsers"},
                {"name": "screenPageViews"},
                {"name": "bounceRate"},
                {"name": "averageSessionDuration"},
            ],
            "orderBys": [{"metric": {"metricName": "sessions"}, "desc": True}],
            "limit": 200,
        }
    ).execute()

    rows = []
    for row in response.get("rows", []):
        dims = row["dimensionValues"]
        mets = row["metricValues"]
        rows.append({
            "page":         dims[0]["value"],
            "sessions":     int(mets[0]["value"]),
            "users":        int(mets[1]["value"]),
            "new_users":    int(mets[2]["value"]),
            "pageviews":    int(mets[3]["value"]),
            "bounce_rate":  round(float(mets[4]["value"]) * 100, 1),
            "avg_duration": round(float(mets[5]["value"]), 0),
        })
    return rows


def fetch_sources(service, start_date: str, end_date: str) -> list[dict]:
    """Pobiera źródła ruchu."""
    response = service.properties().runReport(
        property=PROPERTY_ID,
        body={
            "dateRanges": [{"startDate": start_date, "endDate": end_date}],
            "dimensions": [
                {"name": "sessionSource"},
                {"name": "sessionMedium"},
            ],
            "metrics": [
                {"name": "sessions"},
                {"name": "totalUsers"},
            ],
            "orderBys": [{"metric": {"metricName": "sessions"}, "desc": True}],
            "limit": 50,
        }
    ).execute()

    rows = []
    for row in response.get("rows", []):
        dims = row["dimensionValues"]
        mets = row["metricValues"]
        rows.append({
            "source":   dims[0]["value"],
            "medium":   dims[1]["value"],
            "sessions": int(mets[0]["value"]),
            "users":    int(mets[1]["value"]),
        })
    return rows


def fetch_events(service, start_date: str, end_date: str) -> list[dict]:
    """Pobiera top zdarzenia (kliknięcia CTA, reklamy)."""
    response = service.properties().runReport(
        property=PROPERTY_ID,
        body={
            "dateRanges": [{"startDate": start_date, "endDate": end_date}],
            "dimensions": [
                {"name": "eventName"},
                {"name": "pagePath"},
            ],
            "metrics": [{"name": "eventCount"}],
            "dimensionFilter": {
                "filter": {
                    "fieldName": "eventName",
                    "inListFilter": {
                        "values": ["ad_click", "click", "scroll", "session_start", "page_view"]
                    }
                }
            },
            "orderBys": [{"metric": {"metricName": "eventCount"}, "desc": True}],
            "limit": 100,
        }
    ).execute()

    rows = []
    for row in response.get("rows", []):
        dims = row["dimensionValues"]
        mets = row["metricValues"]
        rows.append({
            "event_name": dims[0]["value"],
            "page":       dims[1]["value"],
            "count":      int(mets[0]["value"]),
        })
    return rows


def fetch_sciezki_conversions(service, start_date: str, end_date: str) -> list[dict]:
    """Pobiera ruch na stronach sciezki (lead generation)."""
    response = service.properties().runReport(
        property=PROPERTY_ID,
        body={
            "dateRanges": [{"startDate": start_date, "endDate": end_date}],
            "dimensions": [
                {"name": "pagePath"},
                {"name": "sessionSource"},
                {"name": "sessionMedium"},
            ],
            "metrics": [
                {"name": "sessions"},
                {"name": "totalUsers"},
            ],
            "dimensionFilter": {
                "filter": {
                    "fieldName": "pagePath",
                    "stringFilter": {
                        "matchType": "BEGINS_WITH",
                        "value": "/sciezki/",
                    }
                }
            },
            "orderBys": [{"metric": {"metricName": "sessions"}, "desc": True}],
        }
    ).execute()

    rows = []
    for row in response.get("rows", []):
        dims = row["dimensionValues"]
        mets = row["metricValues"]
        rows.append({
            "page":     dims[0]["value"],
            "source":   dims[1]["value"],
            "medium":   dims[2]["value"],
            "sessions": int(mets[0]["value"]),
            "users":    int(mets[1]["value"]),
        })
    return rows


# ══════════════════════════════════════════════
# SAVE TO DB
# ══════════════════════════════════════════════

def save_to_db(conn, fetched_at, start_date, end_date, pages, sources, events):
    # Clear old data for same period
    conn.execute("DELETE FROM ga_pages WHERE period_start=? AND period_end=?", (start_date, end_date))
    conn.execute("DELETE FROM ga_sources WHERE period_start=? AND period_end=?", (start_date, end_date))
    conn.execute("DELETE FROM ga_events WHERE period_start=? AND period_end=?", (start_date, end_date))

    for p in pages:
        conn.execute("""
            INSERT INTO ga_pages (fetched_at, period_start, period_end, page, sessions, users, new_users, pageviews, bounce_rate, avg_duration)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """, (fetched_at, start_date, end_date, p["page"], p["sessions"], p["users"],
              p["new_users"], p["pageviews"], p["bounce_rate"], p["avg_duration"]))

    for s in sources:
        conn.execute("""
            INSERT INTO ga_sources (fetched_at, period_start, period_end, source, medium, sessions, users)
            VALUES (?,?,?,?,?,?,?)
        """, (fetched_at, start_date, end_date, s["source"], s["medium"], s["sessions"], s["users"]))

    for e in events:
        conn.execute("""
            INSERT INTO ga_events (fetched_at, period_start, period_end, event_name, page, count)
            VALUES (?,?,?,?,?,?)
        """, (fetched_at, start_date, end_date, e["event_name"], e["page"], e["count"]))

    conn.commit()


# ══════════════════════════════════════════════
# REPORT
# ══════════════════════════════════════════════

def generate_report(pages, sources, events, sciezki, start_date, end_date, days) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total_sessions = sum(p["sessions"] for p in pages)
    total_users    = sum(p["users"] for p in pages)
    total_pv       = sum(p["pageviews"] for p in pages)
    avg_bounce     = round(sum(p["bounce_rate"] for p in pages) / len(pages), 1) if pages else 0

    lines = [
        f"# Google Analytics 4 — dokodu.it",
        f"Pobrano: {now} | Okres: {start_date} → {end_date} ({days} dni)\n",
        "## Podsumowanie",
        "| Metryka | Wartość |",
        "|---------|---------|",
        f"| Łączne sesje | **{total_sessions:,}** |",
        f"| Unikalni użytkownicy | **{total_users:,}** |",
        f"| Odsłony | **{total_pv:,}** |",
        f"| Średni bounce rate | {avg_bounce}% |",
        "",
        "## Top 20 Stron (wg sesji)",
        "| # | Strona | Sesje | Użytkownicy | Bounce | Avg. czas |",
        "|---|--------|-------|-------------|--------|-----------|",
    ]
    for i, p in enumerate(pages[:20], 1):
        dur = f"{int(p['avg_duration']//60)}m {int(p['avg_duration']%60)}s"
        lines.append(f"| {i} | `{p['page']}` | {p['sessions']} | {p['users']} | {p['bounce_rate']}% | {dur} |")

    lines += [
        "",
        "## Źródła Ruchu",
        "| Źródło | Medium | Sesje | Użytkownicy |",
        "|--------|--------|-------|-------------|",
    ]
    for s in sources[:15]:
        lines.append(f"| {s['source']} | {s['medium']} | {s['sessions']} | {s['users']} |")

    if sciezki:
        lines += [
            "",
            "## Ścieżki B2B — Lead Generation",
            "| Strona | Źródło | Medium | Sesje |",
            "|--------|--------|--------|-------|",
        ]
        for s in sciezki:
            lines.append(f"| {s['page']} | {s['source']} | {s['medium']} | {s['sessions']} |")
    else:
        lines += ["", "## Ścieżki B2B — Lead Generation", "_Brak ruchu na /sciezki/ w tym okresie_"]

    ad_clicks = [e for e in events if e["event_name"] == "ad_click"]
    if ad_clicks:
        lines += [
            "",
            "## Kliknięcia Reklam (ad_click)",
            "| Strona | Liczba kliknięć |",
            "|--------|----------------|",
        ]
        for e in ad_clicks[:10]:
            lines.append(f"| `{e['page']}` | {e['count']} |")

    lines += [
        "",
        "## Strony z Wysokim Bounce Rate (>70%)",
        "| Strona | Bounce | Sesje |",
        "|--------|--------|-------|",
    ]
    high_bounce = [p for p in pages if p["bounce_rate"] > 70 and p["sessions"] > 20]
    high_bounce.sort(key=lambda x: x["bounce_rate"], reverse=True)
    for p in high_bounce[:10]:
        lines.append(f"| `{p['page']}` | {p['bounce_rate']}% | {p['sessions']} |")

    lines += [
        "",
        f"---",
        f"*DOKODU BRAIN GA4 Integration | {now}*",
    ]
    return "\n".join(lines)


# ══════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="GA4 fetch dla DOKODU BRAIN")
    parser.add_argument("--days", type=int, default=28, help="Liczba dni wstecz (domyślnie 28)")
    parser.add_argument("--save", action="store_true", help="Zapisz raport do BRAIN")
    parser.add_argument("--from-db", action="store_true", help="Pokaż dane z lokalnej bazy (offline)")
    parser.add_argument("--mode", choices=["pages", "sources", "events", "sciezki"], default="pages")
    args = parser.parse_args()

    if getattr(args, "from_db", False):
        conn = db_connect()
        db_init(conn)
        if args.mode == "pages":
            rows = conn.execute("SELECT page, SUM(sessions) as s, SUM(users) as u, AVG(bounce_rate) as b, AVG(avg_duration) as d FROM ga_pages GROUP BY page ORDER BY s DESC LIMIT 30").fetchall()
            print(f"{'Strona':<55} {'Sesje':>6} {'Użyt':>6} {'Bounce':>7} {'Czas':>7}")
            print("─" * 85)
            for r in rows:
                dur = f"{int(r['d']//60)}m{int(r['d']%60)}s"
                print(f"{r['page']:<55} {r['s']:>6} {r['u']:>6} {r['b']:>6.1f}% {dur:>7}")
        elif args.mode == "sciezki":
            rows = conn.execute("SELECT page, source, medium, SUM(sessions) as s FROM ga_sources WHERE source LIKE '%sciezki%' OR page LIKE '/sciezki%' GROUP BY page ORDER BY s DESC").fetchall()
            for r in rows:
                print(f"{r['page']} | {r['source']} / {r['medium']} | {r['s']} sesji")
        conn.close()
        return

    print(f"\n{'='*50}")
    print(f"GA4 Fetch — dokodu.it")
    print(f"{'='*50}\n")

    end_date   = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=args.days)).strftime("%Y-%m-%d")
    fetched_at = datetime.now().isoformat()

    print("  Autoryzacja Google Analytics...")
    creds   = get_credentials()
    service = build("analyticsdata", "v1beta", credentials=creds)
    print("  ✓ Połączono z GA4\n")

    print("  Pobieranie danych stron...")
    pages = fetch_pages(service, start_date, end_date)
    print(f"  ✓ {len(pages)} stron")

    print("  Pobieranie źródeł ruchu...")
    sources = fetch_sources(service, start_date, end_date)
    print(f"  ✓ {len(sources)} źródeł")

    print("  Pobieranie zdarzeń...")
    events = fetch_events(service, start_date, end_date)
    print(f"  ✓ {len(events)} zdarzeń")

    print("  Pobieranie ścieżek B2B...")
    sciezki = fetch_sciezki_conversions(service, start_date, end_date)
    print(f"  ✓ {len(sciezki)} wpisów\n")

    conn = db_connect()
    db_init(conn)
    save_to_db(conn, fetched_at, start_date, end_date, pages, sources, events)
    conn.close()
    print("  ✓ Zapisano do bazy danych\n")

    report = generate_report(pages, sources, events, sciezki, start_date, end_date, args.days)
    print(report)

    if args.save:
        AREA_SEO_DIR.mkdir(parents=True, exist_ok=True)
        out_file = AREA_SEO_DIR / "GA_Last_Sync.md"
        out_file.write_text(report, encoding="utf-8")
        print(f"\n  ✓ Raport zapisany: {out_file}")


if __name__ == "__main__":
    main()
