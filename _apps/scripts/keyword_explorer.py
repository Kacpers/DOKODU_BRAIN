#!/usr/bin/env python3
"""
DOKODU BRAIN — Keyword Explorer
Odkrywa nowe okazje SEO przez Google Trends (pytrends) i cross-referuje
z istniejącymi danymi GSC i ideas bankiem.

Użycie:
  python3 keyword_explorer.py "n8n"
  python3 keyword_explorer.py "n8n" "automatyzacja ai" "fastapi"
  python3 keyword_explorer.py "n8n" --add          # dodaj okazje do ideas bank
  python3 keyword_explorer.py "n8n" --lang en       # angielskie trendy (domyślnie: pl)
  python3 keyword_explorer.py "n8n" --days 90       # trendy z ostatnich 90 dni
  python3 keyword_explorer.py --trending            # co jest HOT w PL dzisiaj

Wyniki:
  🔴 OKAZJA  — rosnący trend, nie rankujemy, nie mamy w ideas bank
  🟡 IDEAS   — mamy w ideas bank, jeszcze nie napisany
  🟢 MAMY    — rankujemy lub mamy opublikowany artykuł
  ⚪ SŁABY   — trend zbyt niski lub nieistotny
"""

import sys
import time
import sqlite3
import argparse
from pathlib import Path
from datetime import datetime

try:
    from pytrends.request import TrendReq
except ImportError:
    print("ERROR: Brak pytrends. Zainstaluj: pip3 install pytrends")
    sys.exit(1)

DB_FILE = Path.home() / ".config" / "dokodu" / "gsc_data.db"

# ══════════════════════════════════════════════
# DATABASE HELPERS
# ══════════════════════════════════════════════

def db_connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def get_gsc_queries() -> dict[str, dict]:
    """Zwraca wszystkie zapytania z GSC jako {query: {clicks, impressions, position}}."""
    try:
        db = db_connect()
        rows = db.execute("""
            SELECT query,
                   SUM(clicks) as clicks,
                   SUM(impressions) as impressions,
                   AVG(position) as position,
                   ROUND(CAST(SUM(clicks) AS REAL) / NULLIF(SUM(impressions), 0) * 100, 2) as ctr
            FROM gsc_queries
            GROUP BY query
        """).fetchall()
        db.close()
        return {r["query"].lower(): dict(r) for r in rows}
    except Exception:
        return {}


def get_ideas_keywords() -> dict[str, dict]:
    """Zwraca słowa kluczowe z ideas bank jako {keyword: {id, title, status}}."""
    try:
        db = db_connect()
        rows = db.execute("""
            SELECT id, title, target_keyword, status, priority
            FROM blog_ideas
            WHERE target_keyword IS NOT NULL AND target_keyword != ''
        """).fetchall()
        db.close()
        result = {}
        for r in rows:
            kw = r["target_keyword"].lower()
            result[kw] = dict(r)
        return result
    except Exception:
        return {}


def get_published_keywords() -> set[str]:
    """Zwraca słowa kluczowe opublikowanych artykułów."""
    try:
        db = db_connect()
        rows = db.execute("SELECT keyword FROM blog_articles WHERE keyword IS NOT NULL").fetchall()
        db.close()
        return {r["keyword"].lower() for r in rows}
    except Exception:
        return set()


def get_seeds_from_blog() -> list[str]:
    """
    Wyciąga seed keywords z opublikowanych artykułów + sitemap dokodu.it.
    Priorytetyzuje artykuły które mają ruch GSC (warte eksploracji powiązanych fraz).
    """
    seeds = []

    # 1. Keywords z blog_articles (lokalna baza)
    try:
        db = db_connect()
        rows = db.execute("""
            SELECT ba.keyword, COALESCE(SUM(gq.impressions), 0) as total_impr
            FROM blog_articles ba
            LEFT JOIN gsc_query_page gqp ON gqp.page LIKE '%' || ba.slug || '%'
            LEFT JOIN gsc_queries gq ON gq.query = ba.keyword
            WHERE ba.keyword IS NOT NULL
            GROUP BY ba.keyword
            ORDER BY total_impr DESC
        """).fetchall()
        db.close()
        seeds = [r["keyword"] for r in rows if r["keyword"]]
    except Exception:
        pass

    # 2. Sitemap dokodu.it — wyciągnij słowa ze slugów
    try:
        import urllib.request
        import xml.etree.ElementTree as ET

        req = urllib.request.urlopen("https://dokodu.it/sitemap-0.xml", timeout=8)
        tree = ET.parse(req)
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = [loc.text for loc in tree.findall(".//sm:loc", ns) if loc.text]

        for url in urls:
            slug = url.rstrip("/").split("/")[-1]
            # Zamień myślniki na spacje, pomiń krótkie i techniczne
            kw = slug.replace("-", " ").replace("_", " ")
            if len(kw) > 4 and kw not in seeds and not kw.startswith("http"):
                seeds.append(kw)
    except Exception:
        pass

    # Deduplikuj i ogranicz do 20 (Google Trends limit)
    seen = set()
    unique = []
    for s in seeds:
        if s.lower() not in seen:
            seen.add(s.lower())
            unique.append(s)
    return unique[:20]


def add_to_ideas(keyword: str, title: str, notes: str, rising_pct: int = 0):
    """Dodaje odkrytą frazę do ideas bank."""
    db = db_connect()
    db.execute("""
        INSERT INTO blog_ideas (title, target_keyword, priority, source, notes, verdict, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        title,
        keyword,
        "high" if rising_pct > 1000 else "medium",
        "keyword-explorer",
        notes,
        "🟡",
        "POMYSŁ",
    ))
    db.commit()
    db.close()


# ══════════════════════════════════════════════
# TRENDS HELPERS
# ══════════════════════════════════════════════

def init_pytrends(lang: str = "pl") -> TrendReq:
    return TrendReq(
        hl=lang, tz=60,
        timeout=(10, 25),
        retries=3,
        backoff_factor=1.0,
        requests_args={
            "headers": {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0.0.0 Safari/537.36"
                ),
                "Accept-Language": "pl-PL,pl;q=0.9,en;q=0.8",
            }
        }
    )


def get_related_queries(pytrends: TrendReq, keywords: list[str], timeframe: str) -> dict:
    """
    Pobiera related queries dla max 5 keywordów naraz (limit Google).
    Zwraca {keyword: {"top": [...], "rising": [...]}}
    """
    results = {}
    # Google Trends przyjmuje max 5 keywordów naraz
    chunks = [keywords[i:i+5] for i in range(0, len(keywords), 5)]

    for chunk in chunks:
        try:
            pytrends.build_payload(chunk, timeframe=timeframe, geo="PL")
            related = pytrends.related_queries()
            for kw in chunk:
                if kw in related and related[kw]:
                    top_df    = related[kw].get("top")
                    rising_df = related[kw].get("rising")
                    results[kw] = {
                        "top":    top_df.to_dict("records")    if top_df    is not None and not top_df.empty    else [],
                        "rising": rising_df.to_dict("records") if rising_df is not None and not rising_df.empty else [],
                    }
                else:
                    results[kw] = {"top": [], "rising": []}
            time.sleep(1.5)  # unikaj rate limit
        except Exception as e:
            print(f"  ⚠ Błąd Google Trends dla {chunk}: {e}")

    return results


def get_trending_now(pytrends: TrendReq) -> list[dict]:
    """Pobiera aktualnie trendy w Polsce (realtime)."""
    try:
        df = pytrends.trending_searches(pn="poland")
        return [{"query": row} for row in df[0].tolist()[:20]]
    except Exception as e:
        print(f"  ⚠ Błąd trending searches: {e}")
        return []


def get_interest(pytrends: TrendReq, keywords: list[str], timeframe: str) -> dict:
    """Pobiera interest over time (0-100) dla keywordów."""
    try:
        chunks = [keywords[i:i+5] for i in range(0, len(keywords), 5)]
        interest = {}
        for chunk in chunks:
            pytrends.build_payload(chunk, timeframe=timeframe, geo="PL")
            df = pytrends.interest_over_time()
            if df is not None and not df.empty:
                for kw in chunk:
                    if kw in df.columns:
                        avg = int(df[kw].mean())
                        recent = int(df[kw].iloc[-4:].mean())  # ostatni miesiąc
                        interest[kw] = {"avg": avg, "recent": recent}
            time.sleep(1.2)
        return interest
    except Exception as e:
        print(f"  ⚠ Błąd interest over time: {e}")
        return {}


# ══════════════════════════════════════════════
# SCORING
# ══════════════════════════════════════════════

def classify(query: str, rising_pct: int,
             gsc: dict, ideas: dict, published: set) -> tuple[str, str]:
    """
    Zwraca (status_emoji, opis):
      🔴 OKAZJA  — hot, nie rankujemy, nie mamy
      🟡 IDEAS   — mamy w ideas bank
      🟢 MAMY    — rankujemy lub opublikowany
      ⚪ SŁABY   — trend < 10
    """
    q = query.lower()

    # Sprawdź opublikowane
    for pub_kw in published:
        if q in pub_kw or pub_kw in q:
            return "🟢", "opublikowany artykuł"

    # Sprawdź GSC (rankujemy)
    for gsc_q, gsc_data in gsc.items():
        if q in gsc_q or gsc_q in q:
            pos = gsc_data.get("position", 99)
            clicks = gsc_data.get("clicks", 0)
            return "🟢", f"GSC: poz #{pos:.0f}, {clicks} klik"

    # Sprawdź ideas bank
    for idea_kw, idea_data in ideas.items():
        if q in idea_kw or idea_kw in q:
            return "🟡", f"ideas bank: #{idea_data['id']} ({idea_data['status']})"

    # Nowa okazja
    if rising_pct > 500 or rising_pct == -1:  # -1 = "Breakout" (>5000%)
        return "🔴", "NOWA OKAZJA — gorący trend, zero treści"
    elif rising_pct > 0:
        return "🔴", f"NOWA OKAZJA — +{rising_pct}% wzrost"
    else:
        return "⚪", "niski trend"


def format_rising(value) -> str:
    if value == -1 or str(value).lower() == "breakout":
        return "🚀 BREAKOUT (>5000%)"
    try:
        v = int(value)
        if v > 1000:
            return f"🔥 +{v:,}%"
        elif v > 100:
            return f"📈 +{v:,}%"
        else:
            return f"+{v}%"
    except Exception:
        return str(value)


# ══════════════════════════════════════════════
# REPORT
# ══════════════════════════════════════════════

def run_analysis(seeds: list[str], timeframe: str, lang: str,
                 auto_add: bool, verbose: bool):
    print(f"\n{'='*60}")
    print(f"Keyword Explorer — DOKODU BRAIN")
    print(f"Seed keywords: {', '.join(seeds)}")
    print(f"Geo: PL | Timeframe: {timeframe} | Lang: {lang}")
    print(f"{'='*60}\n")

    # Załaduj lokalne dane
    print("  Ładuję GSC + ideas bank...")
    gsc       = get_gsc_queries()
    ideas     = get_ideas_keywords()
    published = get_published_keywords()
    print(f"  ✓ GSC: {len(gsc)} zapytań | Ideas: {len(ideas)} | Opublikowane: {len(published)}\n")

    # Pobierz dane z Google Trends
    print("  Pobieram dane z Google Trends (PL)...")
    pytrends = init_pytrends(lang)
    related  = get_related_queries(pytrends, seeds, timeframe)
    interest = get_interest(pytrends, seeds, timeframe)
    print()

    # Zbierz wszystkie odkryte frazy
    opportunities = []  # (status, query, rising_pct, seed, details)

    for seed in seeds:
        seed_data = related.get(seed, {})
        seed_interest = interest.get(seed, {})

        # Interest summary
        if seed_interest:
            avg = seed_interest.get("avg", 0)
            recent = seed_interest.get("recent", 0)
            trend_arrow = "📈" if recent > avg else "📉" if recent < avg else "→"
            print(f"  [{seed}] Popularność: avg={avg}/100, ostatnio={recent}/100 {trend_arrow}")
        else:
            print(f"  [{seed}] Brak danych o popularności")

        # Rising queries (to jest złoto — rosnące frazy)
        rising = seed_data.get("rising", [])
        for item in rising:
            q = item.get("query", "").lower()
            v = item.get("value", 0)
            if not q:
                continue
            status, details = classify(q, v if v != "Breakout" else -1, gsc, ideas, published)
            opportunities.append({
                "status":   status,
                "query":    q,
                "rising":   v,
                "type":     "rising",
                "seed":     seed,
                "details":  details,
            })

        # Top queries (stabilne, duże wolumeny)
        top = seed_data.get("top", [])
        for item in top[:15]:  # top 15
            q = item.get("query", "").lower()
            v = item.get("value", 0)
            if not q:
                continue
            # Sprawdź czy już mamy w rising
            if any(o["query"] == q for o in opportunities):
                continue
            status, details = classify(q, 0, gsc, ideas, published)
            if status not in ("🟢",):  # top queries które nie rankujemy
                opportunities.append({
                    "status":  status,
                    "query":   q,
                    "rising":  v,
                    "type":    "top",
                    "seed":    seed,
                    "details": details,
                })

    # ─── RAPORT ───────────────────────────────────────────
    print(f"\n{'─'*60}")
    print("WYNIKI ANALIZY")
    print(f"{'─'*60}\n")

    # Sortuj: najpierw okazje (🔴), potem ideas (🟡), potem mamy (🟢)
    order = {"🔴": 0, "🟡": 1, "🟢": 2, "⚪": 3}
    opportunities.sort(key=lambda x: (order.get(x["status"], 9), -x["rising"] if isinstance(x["rising"], int) else 0))

    czerwone = [o for o in opportunities if o["status"] == "🔴"]
    zolte    = [o for o in opportunities if o["status"] == "🟡"]
    zielone  = [o for o in opportunities if o["status"] == "🟢"]
    slabe    = [o for o in opportunities if o["status"] == "⚪"]

    # OKAZJE
    if czerwone:
        print("🔴 NOWE OKAZJE (nie rankujesz, gorący trend):\n")
        for o in czerwone:
            rising_str = format_rising(o["rising"]) if o["type"] == "rising" else f"top-{o['rising']}/100"
            print(f"   • {o['query']}")
            print(f"     Trend: {rising_str} | Seed: [{o['seed']}]")
        print()

    # IDEAS BANK
    if zolte:
        print("🟡 JUŻ W IDEAS BANK (napisz artykuł):\n")
        for o in zolte[:10]:
            print(f"   • {o['query']} — {o['details']}")
        print()

    # MAMY
    if zielone and verbose:
        print("🟢 JUŻ POKRYTE:\n")
        for o in zielone[:8]:
            print(f"   • {o['query']} — {o['details']}")
        print()

    # Podsumowanie
    print(f"{'─'*60}")
    print(f"Podsumowanie: {len(czerwone)} okazji | {len(zolte)} w ideas | {len(zielone)} pokrytych | {len(slabe)} słabych")
    print(f"{'─'*60}\n")

    # Auto-add do ideas bank
    if auto_add and czerwone:
        print("Dodaję okazje do ideas bank...")
        added = 0
        for o in czerwone:
            q = o["query"]
            # Zbuduj prosty tytuł
            title = q.capitalize().replace("-", " ") + " — przewodnik 2026"
            rising_str = format_rising(o["rising"])
            notes = f"Odkryto przez keyword-explorer | Trend: {rising_str} | Seed: {o['seed']}"
            add_to_ideas(q, title, notes,
                         rising_pct=o["rising"] if isinstance(o["rising"], int) else 9999)
            print(f"  ✓ Dodano: {q}")
            added += 1
        print(f"\n  Dodano {added} fraz do ideas bank.")
        print("  Uruchom: python3 seo_ideas.py list --status POMYSŁ --priority high\n")

    elif czerwone and not auto_add:
        print("Aby dodać OKAZJE do ideas bank automatycznie:")
        print(f"  python3 keyword_explorer.py {' '.join(seeds)} --add\n")

    return czerwone


def run_gsc_gaps(min_impressions: int = 100, max_position: float = 20.0):
    """
    Tryb offline — analizuje luki w GSC bez Google Trends.
    Szuka fraz z dużą liczbą impresji ale niskim CTR lub słabą pozycją.
    """
    print(f"\n{'='*60}")
    print("GSC Gap Analysis — bez Google Trends")
    print(f"{'='*60}\n")

    gsc   = get_gsc_queries()
    ideas = get_ideas_keywords()
    published = get_published_keywords()

    if not gsc:
        print("Brak danych GSC. Uruchom najpierw: python3 gsc_fetch.py --save")
        return

    rows = []
    for q, data in gsc.items():
        impr = data.get("impressions", 0)
        pos  = data.get("position", 99)
        ctr  = data.get("ctr", 0)
        clicks = data.get("clicks", 0)

        if impr < min_impressions:
            continue

        # CTR w bazie jest w procentach (np. 2.22 = 2.22%)
        # Oczekiwany CTR wg pozycji (przybliżenie): poz 1 ~30%, poz 5 ~7%, poz 10 ~2%
        expected_ctr_pct = max(0.5, 30 - (pos - 1) * 3)
        ctr_gap = expected_ctr_pct - ctr

        status, details = classify(q, 0, {}, ideas, published)

        rows.append({
            "query":    q,
            "impr":     impr,
            "clicks":   clicks,
            "pos":      pos,
            "ctr":      ctr,
            "ctr_gap":  ctr_gap,
            "status":   status,
            "details":  details,
        })

    # Sortuj po największej stracie (impr × ctr_gap)
    rows.sort(key=lambda x: x["impr"] * x["ctr_gap"], reverse=True)

    print(f"{'Fraza':<40} {'Impr':>6} {'Klik':>5} {'Poz':>5} {'CTR':>6}  Status")
    print("─" * 75)

    for r in rows[:30]:
        ctr_str = f"{r['ctr']:.1f}%"
        pos_str = f"#{r['pos']:.1f}"
        flag = ""
        if r["pos"] <= 10 and r["ctr"] < 0.05:
            flag = " ⚡ CTR anomalia"  # top 10 ale słaby CTR
        elif r["pos"] > 10 and r["pos"] <= 20 and r["impr"] > 500:
            flag = " 🎯 optymalizuj"   # strona 2 z dużym popytem

        print(f"{r['query'][:39]:<40} {r['impr']:>6} {r['clicks']:>5} {pos_str:>5} {ctr_str:>6}  {r['status']}{flag}")

    print(f"\nŁącznie: {len(rows)} fraz z >{min_impressions} impresji")
    print("\nLegenda:")
    print("  ⚡ CTR anomalia — strona w top 10 ale mało kliknięć → popraw tytuł/meta")
    print("  🎯 optymalizuj — strona 2, duży popyt → dobry kandydat na rozbudowę")
    print("  🔴 brak artykułu | 🟡 w ideas bank | 🟢 opublikowany\n")


def run_trending(lang: str):
    """Pokazuje co jest HOT w Polsce teraz."""
    print(f"\n{'='*60}")
    print("Trending Searches — Polska (dzisiaj)")
    print(f"{'='*60}\n")

    gsc   = get_gsc_queries()
    ideas = get_ideas_keywords()
    published = get_published_keywords()

    pytrends = init_pytrends(lang)
    trends = get_trending_now(pytrends)

    if not trends:
        print("Brak danych (Google może blokować — spróbuj za chwilę)")
        return

    print(f"{'#':<4} {'Fraza':<40} {'Status'}")
    print("─" * 60)
    for i, t in enumerate(trends, 1):
        q = t["query"].lower()
        status, details = classify(q, 0, gsc, ideas, published)
        print(f"{i:<4} {t['query']:<40} {status} {details}")
    print()


# ══════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Keyword Explorer — odkrywa okazje SEO przez Google Trends")
    parser.add_argument("keywords", nargs="*", help="Seed keywords do analizy, np. 'n8n' 'fastapi'")
    parser.add_argument("--add",      action="store_true", help="Dodaj nowe okazje do ideas bank")
    parser.add_argument("--trending",  action="store_true", help="Pokaż trending searches PL")
    parser.add_argument("--gsc-only",    action="store_true", help="Analiza luk GSC bez Google Trends (offline)")
    parser.add_argument("--from-sitemap",action="store_true", help="Seed keywords z opublikowanych artykułów + sitemap")
    parser.add_argument("--min-impr",   type=int, default=100, help="Min impresji dla --gsc-only (domyślnie: 100)")
    parser.add_argument("--days",     type=int, default=90,  help="Timeframe w dniach (30/90/180/365)")
    parser.add_argument("--lang",     default="pl",           help="Język (pl/en)")
    parser.add_argument("--verbose",  action="store_true",    help="Pokaż też już pokryte frazy")
    args = parser.parse_args()

    # Timeframe dla pytrends
    days_map = {30: "today 1-m", 90: "today 3-m", 180: "today 6-m", 365: "today 12-m"}
    timeframe = days_map.get(args.days, f"today {args.days}-d")

    if args.trending:
        run_trending(args.lang)
        return

    if getattr(args, "gsc_only", False):
        run_gsc_gaps(min_impressions=args.min_impr)
        return

    if getattr(args, "from_sitemap", False):
        print("Wyciągam seed keywords z bloga i sitemapy...")
        seeds = get_seeds_from_blog()
        if not seeds:
            print("Brak artykułów w bazie. Uruchom najpierw /blog-publish żeby zsynchronizować.")
            sys.exit(1)
        print(f"Znaleziono {len(seeds)} seed keywords: {', '.join(seeds[:8])}{'...' if len(seeds) > 8 else ''}\n")
        run_analysis(seeds=seeds, timeframe=timeframe, lang=args.lang,
                     auto_add=args.add, verbose=args.verbose)
        return

    if not args.keywords:
        parser.print_help()
        print("\nPrzykłady:")
        print("  python3 keyword_explorer.py n8n")
        print("  python3 keyword_explorer.py n8n fastapi automatyzacja --add")
        print("  python3 keyword_explorer.py --trending")
        sys.exit(1)

    run_analysis(
        seeds=args.keywords,
        timeframe=timeframe,
        lang=args.lang,
        auto_add=args.add,
        verbose=args.verbose,
    )


if __name__ == "__main__":
    main()
