#!/usr/bin/env python3
"""
DOKODU BRAIN — Google Trends Fetch
Pobiera dane trendów dla słów kluczowych i zapisuje do SQLite + Markdown.

Użycie:
  python3 trends_fetch.py --keywords "n8n,automatyzacja ai,cursor ai"
  python3 trends_fetch.py --keywords "n8n" --days 90 --save
  python3 trends_fetch.py --from-db --save
  python3 trends_fetch.py --auto-gsc --save   # pobiera keywords z GSC top queries
"""

import argparse
import json
import sqlite3
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

try:
    from pytrends.request import TrendReq
    from pytrends.exceptions import TooManyRequestsError
except ImportError:
    print("ERROR: pip3 install pytrends")
    sys.exit(1)

# ── Ścieżki ─────────────────────────────────────────────────────────────────
BRAIN_DIR   = Path(__file__).parent.parent
DB_FILE     = Path.home() / ".config/dokodu/trends_data.db"
GSC_DB_FILE = Path.home() / ".config/dokodu/gsc_data.db"
OUT_FILE    = BRAIN_DIR / "20_AREAS/AREA_Blog_SEO/Trends_Last_Sync.md"

GEO = "PL"  # Polska
LANG = "pl"


# ── SQLite ───────────────────────────────────────────────────────────────────
def db_connect():
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(str(DB_FILE))


def db_init(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS trends_interest (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            fetched_at  TEXT DEFAULT (datetime('now')),
            keyword     TEXT NOT NULL,
            timeframe   TEXT NOT NULL,
            avg_interest REAL,
            peak_interest REAL,
            recent_interest REAL,
            trend_direction TEXT,
            data_json   TEXT
        );
        CREATE TABLE IF NOT EXISTS trends_related_queries (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            fetched_at  TEXT DEFAULT (datetime('now')),
            keyword     TEXT NOT NULL,
            query_type  TEXT,
            related_kw  TEXT,
            value       REAL
        );
        CREATE TABLE IF NOT EXISTS trends_snapshots (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            fetched_at  TEXT DEFAULT (datetime('now')),
            keywords    TEXT,
            geo         TEXT,
            timeframe   TEXT
        );
    """)
    conn.commit()


def db_save_interest(conn, keyword, timeframe, interest_data):
    if interest_data.empty:
        return
    col = keyword if keyword in interest_data.columns else interest_data.columns[0]
    vals = interest_data[col].tolist()
    if not vals:
        return
    avg = sum(vals) / len(vals)
    peak = max(vals)
    recent = vals[-1] if vals else 0

    # trend: porównaj ostatni tydzień vs wcześniejszy
    mid = len(vals) // 2
    first_half_avg = sum(vals[:mid]) / mid if mid > 0 else 0
    second_half_avg = sum(vals[mid:]) / (len(vals) - mid) if (len(vals) - mid) > 0 else 0
    if second_half_avg > first_half_avg * 1.15:
        direction = "rosnący"
    elif second_half_avg < first_half_avg * 0.85:
        direction = "malejący"
    else:
        direction = "stabilny"

    conn.execute("""
        INSERT INTO trends_interest
            (keyword, timeframe, avg_interest, peak_interest, recent_interest, trend_direction, data_json)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (keyword, timeframe, round(avg, 1), peak, recent, direction, json.dumps(vals)))
    conn.commit()


def db_save_related(conn, keyword, related_dict):
    for query_type, df in related_dict.items():
        if df is None or df.empty:
            continue
        for _, row in df.iterrows():
            value = row.get("value", 0)
            if isinstance(value, str):
                value = 100 if value == "Breakout" else 0
            conn.execute("""
                INSERT INTO trends_related_queries (keyword, query_type, related_kw, value)
                VALUES (?, ?, ?, ?)
            """, (keyword, query_type, row.get("query", ""), float(value)))
    conn.commit()


def db_read_latest(conn):
    fetched_at = conn.execute(
        "SELECT MAX(fetched_at) FROM trends_snapshots"
    ).fetchone()[0]
    if not fetched_at:
        return None, []

    keywords_json = conn.execute(
        "SELECT keywords FROM trends_snapshots WHERE fetched_at = ?", (fetched_at,)
    ).fetchone()[0]
    keywords = json.loads(keywords_json)

    results = []
    for kw in keywords:
        row = conn.execute("""
            SELECT keyword, avg_interest, peak_interest, recent_interest,
                   trend_direction, data_json, fetched_at
            FROM trends_interest
            WHERE keyword = ?
            ORDER BY fetched_at DESC LIMIT 1
        """, (kw,)).fetchone()
        if row:
            related_top = conn.execute("""
                SELECT related_kw, value FROM trends_related_queries
                WHERE keyword = ? AND query_type = 'top'
                ORDER BY value DESC LIMIT 5
            """, (kw,)).fetchall()
            related_rising = conn.execute("""
                SELECT related_kw, value FROM trends_related_queries
                WHERE keyword = ? AND query_type = 'rising'
                ORDER BY value DESC LIMIT 5
            """, (kw,)).fetchall()
            results.append({
                "keyword": row[0], "avg": row[1], "peak": row[2],
                "recent": row[3], "direction": row[4],
                "data": json.loads(row[5]),
                "fetched_at": row[6],
                "related_top": related_top,
                "related_rising": related_rising,
            })
    return fetched_at, results


def load_gsc_top_keywords(limit=20):
    """Pobiera top keywords z GSC bazy."""
    if not GSC_DB_FILE.exists():
        return []
    conn = sqlite3.connect(str(GSC_DB_FILE))
    rows = conn.execute("""
        SELECT query FROM gsc_queries
        ORDER BY clicks DESC LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return [r[0] for r in rows]


# ── Google Trends fetch ───────────────────────────────────────────────────────
def build_timeframe(days: int) -> str:
    end = datetime.now() - timedelta(days=1)
    start = end - timedelta(days=days)
    return f"{start.strftime('%Y-%m-%d')} {end.strftime('%Y-%m-%d')}"


def fetch_trends(keywords: list[str], days: int = 90) -> dict:
    """Pobiera dane trendów dla listy keywords (max 5 na raz)."""
    pytrends = TrendReq(hl=LANG, tz=60, timeout=(10, 25), retries=2, backoff_factor=0.5)
    timeframe = build_timeframe(days)
    results = {}

    # pytrends obsługuje max 5 keywords naraz
    for i in range(0, len(keywords), 5):
        batch = keywords[i:i+5]
        print(f"  📊 Trends batch: {', '.join(batch)}", file=sys.stderr)
        try:
            pytrends.build_payload(batch, cat=0, timeframe=timeframe, geo=GEO, gprop="")
            interest = pytrends.interest_over_time()

            for kw in batch:
                results[kw] = {
                    "interest": interest,
                    "related": {},
                    "timeframe": timeframe,
                }

            # Related queries dla każdego keyword osobno
            for kw in batch:
                time.sleep(1.5)  # rate limiting
                try:
                    pytrends.build_payload([kw], cat=0, timeframe=timeframe, geo=GEO)
                    related = pytrends.related_queries()
                    if kw in related:
                        results[kw]["related"] = related[kw]
                except TooManyRequestsError:
                    print(f"  ⚠️  Rate limit na related queries dla: {kw}", file=sys.stderr)
                    time.sleep(10)
                except Exception as e:
                    print(f"  ⚠️  Related queries błąd ({kw}): {e}", file=sys.stderr)

        except TooManyRequestsError:
            print(f"  ⚠️  Rate limit — czekam 30s...", file=sys.stderr)
            time.sleep(30)
        except Exception as e:
            print(f"  ⚠️  Błąd batch: {e}", file=sys.stderr)

        if i + 5 < len(keywords):
            time.sleep(2)

    return results, timeframe


# ── Markdown report ───────────────────────────────────────────────────────────
def _trend_emoji(direction):
    return {"rosnący": "📈", "malejący": "📉", "stabilny": "➡️"}.get(direction, "❓")


def _sparkline(data, width=20):
    """Prosty sparkline z bloków Unicode."""
    if not data:
        return ""
    blocks = " ▁▂▃▄▅▆▇█"
    max_val = max(data) or 1
    sample = data[-width:] if len(data) > width else data
    return "".join(blocks[min(int(v / max_val * 8), 8)] for v in sample)


def build_markdown_report(fetched_at, results, timeframe):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# Google Trends — dokodu.it",
        f"Pobrano: {now_str} | Okres: {timeframe} | Geo: {GEO}",
        "",
        "## Podsumowanie Trendów",
        "",
        "| Keyword | Avg | Peak | Recent | Trend | Sparkline |",
        "|---------|-----|------|--------|-------|-----------|",
    ]
    for r in sorted(results, key=lambda x: x["recent"], reverse=True):
        emoji = _trend_emoji(r["direction"])
        spark = _sparkline(r["data"])
        lines.append(
            f"| `{r['keyword']}` | {r['avg']} | {r['peak']} | {r['recent']} "
            f"| {emoji} {r['direction']} | `{spark}` |"
        )

    # Related queries sekcja
    lines += ["", "## Rising Queries — Rosnące Frazy", ""]
    for r in results:
        if not r["related_rising"]:
            continue
        lines.append(f"### `{r['keyword']}`")
        lines.append("")
        lines.append("| Fraza | Wartość |")
        lines.append("|-------|---------|")
        for kw, val in r["related_rising"]:
            val_str = "Breakout 🚀" if val == 100 else f"+{int(val)}%"
            lines.append(f"| {kw} | {val_str} |")
        lines.append("")

    lines += ["", "## Top Related Queries", ""]
    for r in results:
        if not r["related_top"]:
            continue
        lines.append(f"### `{r['keyword']}`")
        lines.append("")
        lines.append("| Fraza | Relatywna popularność |")
        lines.append("|-------|-----------------------|")
        for kw, val in r["related_top"]:
            lines.append(f"| {kw} | {int(val)} |")
        lines.append("")

    lines += [
        "---",
        f"*DOKODU BRAIN Trends Integration | {now_str}*",
    ]
    return "\n".join(lines)


def save_to_brain(content):
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(content, encoding="utf-8")
    print(f"✅ Zapisano: {OUT_FILE}", file=sys.stderr)


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    global GEO
    parser = argparse.ArgumentParser(description="DOKODU BRAIN — Google Trends Fetch")
    parser.add_argument("--keywords", type=str, help="Przecinkowa lista keywords")
    parser.add_argument("--days",     type=int, default=90, help="Okres analizy (30|90|365)")
    parser.add_argument("--geo",      type=str, default="PL", help="Kraj (PL/US/...)")
    parser.add_argument("--save",     action="store_true", help="Zapisz do BRAIN")
    parser.add_argument("--from-db",  action="store_true", help="Czytaj z bazy (bez API)")
    parser.add_argument("--auto-gsc", action="store_true", help="Pobierz keywords z GSC top queries")
    parser.add_argument("--json",     action="store_true", dest="as_json")
    parser.add_argument("--limit",    type=int, default=10, help="Max keywords przy --auto-gsc")
    args = parser.parse_args()

    GEO = args.geo
    conn = db_connect()
    db_init(conn)

    if args.from_db:
        print("📂 Czytam z lokalnej bazy...", file=sys.stderr)
        fetched_at, results = db_read_latest(conn)
        if not results:
            print("❌ Baza pusta. Uruchom bez --from-db.", file=sys.stderr)
            sys.exit(1)
        timeframe = ""
    else:
        # Wybierz keywords
        if args.auto_gsc:
            keywords = load_gsc_top_keywords(args.limit)
            if not keywords:
                print("❌ Brak danych GSC. Uruchom gsc_fetch.py najpierw.", file=sys.stderr)
                sys.exit(1)
            print(f"📡 Auto-GSC: {len(keywords)} keywords z GSC top queries", file=sys.stderr)
        elif args.keywords:
            keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]
        else:
            print("❌ Podaj --keywords 'kw1,kw2' lub użyj --auto-gsc", file=sys.stderr)
            sys.exit(1)

        print(f"🔍 Pobieranie trendów dla {len(keywords)} keywords ({args.days} dni, geo={GEO})...", file=sys.stderr)
        raw_results, timeframe = fetch_trends(keywords, args.days)

        # Zapisz do bazy
        fetched_at = datetime.now().isoformat()
        for kw, data in raw_results.items():
            db_save_interest(conn, kw, timeframe, data["interest"])
            db_save_related(conn, kw, data.get("related", {}))

        conn.execute(
            "INSERT INTO trends_snapshots (keywords, geo, timeframe) VALUES (?, ?, ?)",
            (json.dumps(keywords), GEO, timeframe)
        )
        conn.commit()
        print(f"✅ Zapisano do bazy: {DB_FILE}", file=sys.stderr)

        _, results = db_read_latest(conn)

    if args.as_json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return

    report = build_markdown_report(fetched_at, results, timeframe)
    print(report)

    if args.save:
        save_to_brain(report)


if __name__ == "__main__":
    main()
