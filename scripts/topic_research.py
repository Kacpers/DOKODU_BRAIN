#!/usr/bin/env python3
"""
DOKODU BRAIN — Topic Research & Scoring
Łączy dane z GSC + Google Trends i scoruje tematy pod kątem:
- potencjału ruchu (impressions, volume)
- trendu (rosnący/malejący)
- potencjału monetyzacyjnego (linki do produktów, afiliacja)
- luki treści (content gap)

Użycie:
  python3 topic_research.py                          # pełna analiza z GSC + Trends (z bazy)
  python3 topic_research.py --fetch-trends           # pobierz świeże Trends przed analizą
  python3 topic_research.py --add-to-ideas           # dodaj top tematy do seo_ideas.py
  python3 topic_research.py --min-score 60           # filtruj wg min score
  python3 topic_research.py --focus monetization     # tylko tematy z potencjałem produktowym
"""

import argparse
import json
import re
import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# ── Ścieżki ─────────────────────────────────────────────────────────────────
BRAIN_DIR     = Path(__file__).parent.parent
GSC_DB        = Path.home() / ".config/dokodu/gsc_data.db"
TRENDS_DB     = Path.home() / ".config/dokodu/trends_data.db"
IDEAS_DB      = Path.home() / ".config/dokodu/gsc_data.db"
OUT_FILE      = BRAIN_DIR / "20_AREAS/AREA_Blog_SEO/Topic_Research.md"
SCRIPTS_DIR   = Path(__file__).parent


# ── Sygnały monetyzacyjne ─────────────────────────────────────────────────────
# Wzorce sugerujące możliwość wstawienia linku do produktu/narzędzia/kursu

PRODUCT_SIGNALS = {
    # Porównania → artykuł z linkami do obu narzędzi
    "comparison": [
        r"\bvs\b", r"\bversus\b", r"porównan", r"porównanie", r"różni", r"lepszy",
        r"alternatyw", r"zamiast",
    ],
    # Narzędzia z planami płatnymi → link afiliacyjny lub review
    "tool_review": [
        r"cursor", r"copilot", r"chatgpt", r"claude", r"perplexity", r"n8n",
        r"make\.com", r"zapier", r"notion", r"airtable", r"vercel", r"railway",
        r"supabase", r"planetscale", r"datadog", r"sentry", r"linear",
        r"github actions", r"docker", r"kubernetes",
    ],
    # Cena / koszt / opłacalność → commercial intent
    "pricing": [
        r"cena", r"cennik", r"koszt", r"opłat", r"darm", r"płatn", r"pro plan",
        r"enterprise", r"licencj", r"subskrypcj", r"ile kosztuje",
    ],
    # Najlepsze / top listy → linki do wielu narzędzi
    "best_of": [
        r"najlepsz", r"top \d+", r"\d+ najlepsz", r"ranking", r"rekomendacj",
        r"które wybrać", r"jaki wybrać",
    ],
    # Kursy / nauka → link do kursu lub materiałów
    "learning": [
        r"kurs", r"nauka", r"tutorial", r"przewodnik", r"jak zacząć", r"dla początkujących",
        r"od podstaw", r"certyfikat", r"szkolenie",
    ],
    # Wdrożenie / setup → usługi Dokodu
    "implementation": [
        r"wdrożen", r"instalacj", r"konfiguracja", r"setup", r"integracja",
        r"automatyzacj", r"deploy", r"docker",
    ],
}

PILLAR_MAP = {
    "n8n": "n8n Automatyzacja",
    "automatyzacj": "n8n Automatyzacja",
    "workflow": "n8n Automatyzacja",
    "cursor": "AI Tools",
    "copilot": "AI Tools",
    "chatgpt": "AI Tools",
    "claude": "AI Tools",
    "perplexity": "AI Tools",
    "llm": "AI Tools",
    "ai": "AI Tools",
    "sql": "SQL",
    "baz danych": "SQL",
    "database": "SQL",
    "python": "Python",
    "pytest": "Python",
    "flask": "Python",
    "fastapi": "Python",
    "docker": "DevOps",
    "kubernetes": "DevOps",
    "git": "DevOps",
    "pgvector": "AI Tools",
    "vector": "AI Tools",
    "rag": "AI Tools",
    "embedding": "AI Tools",
}


def detect_pillar(keyword: str) -> str:
    kw_lower = keyword.lower()
    for pattern, pillar in PILLAR_MAP.items():
        if pattern in kw_lower:
            return pillar
    return "Inne"


def monetization_score(keyword: str) -> tuple[int, list[str]]:
    """Zwraca score 0-100 i listę powodów monetyzacyjnych."""
    kw_lower = keyword.lower()
    score = 0
    reasons = []

    for category, patterns in PRODUCT_SIGNALS.items():
        for p in patterns:
            if re.search(p, kw_lower):
                match category:
                    case "comparison":  points, label = 30, "🔄 Porównanie narzędzi"
                    case "tool_review": points, label = 25, "🛠️ Review narzędzia"
                    case "pricing":     points, label = 35, "💰 Intent zakupowy"
                    case "best_of":     points, label = 20, "📋 Lista narzędzi"
                    case "learning":    points, label = 15, "📚 Link do kursu"
                    case "implementation": points, label = 20, "⚙️ Usługi Dokodu"
                    case _:             points, label = 10, "?"
                score = min(score + points, 100)
                if label not in reasons:
                    reasons.append(label)
                break

    return score, reasons


def suggested_article_type(keyword: str, mono_reasons: list[str]) -> str:
    kw_lower = keyword.lower()
    if re.search(r"\bvs\b|versus|porównan", kw_lower):
        return "Porównanie (X vs Y)"
    if re.search(r"top \d+|najlepsz|\d+ najlepsz|ranking", kw_lower):
        return "Lista (Top N)"
    if re.search(r"jak |tutorial|przewodnik|krok po kroku|setup|instalacj", kw_lower):
        return "Tutorial / How-to"
    if re.search(r"co to jest|co to|czym jest|definicja", kw_lower):
        return "Explainer (Co to jest)"
    if re.search(r"cena|cennik|ile kosztuje|opłaci", kw_lower):
        return "Review cenowy"
    if re.search(r"błąd|problem|nie działa|fix|rozwiązanie", kw_lower):
        return "Troubleshooting"
    if "📚 Link do kursu" in mono_reasons:
        return "Kurs / Nauka"
    return "Artykuł informacyjny"


# ── Ładowanie danych ─────────────────────────────────────────────────────────
def load_gsc_data():
    if not GSC_DB.exists():
        return [], []
    conn = sqlite3.connect(str(GSC_DB))
    queries = conn.execute("""
        SELECT q.query, q.clicks, q.impressions, q.ctr, q.position
        FROM gsc_queries q
        INNER JOIN (
            SELECT query, MAX(fetched_at) as max_at
            FROM gsc_queries GROUP BY query
        ) latest ON q.query = latest.query AND q.fetched_at = latest.max_at
        ORDER BY q.impressions DESC
    """).fetchall()
    pages = conn.execute("""
        SELECT p.page, p.clicks, p.impressions, p.ctr, p.position
        FROM gsc_pages p
        INNER JOIN (
            SELECT page, MAX(fetched_at) as max_at
            FROM gsc_pages GROUP BY page
        ) latest ON p.page = latest.page AND p.fetched_at = latest.max_at
        ORDER BY p.impressions DESC
    """).fetchall()
    conn.close()
    return queries, pages


def load_trends_data():
    if not TRENDS_DB.exists():
        return {}
    conn = sqlite3.connect(str(TRENDS_DB))
    rows = conn.execute("""
        SELECT t.keyword, t.avg_interest, t.peak_interest, t.recent_interest, t.trend_direction
        FROM trends_interest t
        INNER JOIN (
            SELECT keyword, MAX(fetched_at) as max_at
            FROM trends_interest GROUP BY keyword
        ) latest ON t.keyword = latest.keyword AND t.fetched_at = latest.max_at
    """).fetchall()

    rising = conn.execute("""
        SELECT r.keyword, r.related_kw, r.value
        FROM trends_related_queries r
        INNER JOIN (
            SELECT keyword, MAX(fetched_at) as max_at
            FROM trends_related_queries GROUP BY keyword
        ) latest ON r.keyword = latest.keyword AND r.fetched_at = latest.max_at
        WHERE r.query_type = 'rising'
    """).fetchall()
    conn.close()

    trends = {}
    for row in rows:
        trends[row[0]] = {
            "avg": row[1], "peak": row[2], "recent": row[3], "direction": row[4],
            "rising_queries": []
        }
    for kw, related_kw, value in rising:
        if kw in trends:
            trends[kw]["rising_queries"].append(related_kw)

    return trends


def load_existing_ideas():
    if not IDEAS_DB.exists():
        return set()
    conn = sqlite3.connect(str(IDEAS_DB))
    rows = conn.execute("SELECT target_keyword FROM blog_ideas").fetchall()
    conn.close()
    return {r[0] for r in rows if r[0]}


# ── Scoring ───────────────────────────────────────────────────────────────────
def score_topic(query, clicks, impressions, ctr, position, trends_data, existing_ideas):
    kw = query

    # 1. Traffic potential (0-30): impressions z GSC
    if impressions >= 5000:   traffic_score = 30
    elif impressions >= 1000: traffic_score = 22
    elif impressions >= 500:  traffic_score = 15
    elif impressions >= 100:  traffic_score = 8
    else:                      traffic_score = 3

    # 2. Content gap score (0-25): wysoka poz ale niski CTR, lub brak artykułu
    if ctr < 0.02 and impressions > 200:   gap_score = 25
    elif ctr < 0.05 and impressions > 100: gap_score = 15
    elif clicks == 0 and impressions > 50: gap_score = 20
    else:                                   gap_score = 5

    # 3. Position opportunity (0-20): poz 4-15 = quick win
    if 4 <= position <= 10:   pos_score = 20
    elif 10 < position <= 15: pos_score = 12
    elif 15 < position <= 25: pos_score = 6
    elif position <= 3:        pos_score = 5   # już rankuje dobrze
    else:                      pos_score = 2

    # 4. Trend score (0-15): z Google Trends
    trend_score = 0
    trend_dir = "brak danych"
    trend_data = trends_data.get(kw, {})
    if trend_data:
        direction = trend_data.get("direction", "stabilny")
        trend_dir = direction
        recent = trend_data.get("recent", 0)
        avg = trend_data.get("avg", 0) or 1
        if direction == "rosnący":    trend_score = 15
        elif direction == "stabilny": trend_score = 8
        else:                          trend_score = 2
        if recent > avg * 1.5:        trend_score = min(trend_score + 5, 15)

    # 5. Monetization (0-30): potencjał produktowy
    mono_score, mono_reasons = monetization_score(kw)
    mono_score = int(mono_score * 0.3)  # skaluj do 0-30

    total = traffic_score + gap_score + pos_score + trend_score + mono_score
    mono_raw, mono_reasons_full = monetization_score(kw)

    return {
        "keyword": kw,
        "clicks": clicks,
        "impressions": impressions,
        "ctr": ctr,
        "position": round(position, 1),
        "score": min(total, 100),
        "traffic_score": traffic_score,
        "gap_score": gap_score,
        "pos_score": pos_score,
        "trend_score": trend_score,
        "mono_score": mono_raw,
        "mono_reasons": mono_reasons_full,
        "trend_direction": trend_dir,
        "pillar": detect_pillar(kw),
        "article_type": suggested_article_type(kw, mono_reasons_full),
        "already_in_ideas": kw in existing_ideas,
    }


def score_rising_query(related_kw, parent_kw, trends_data):
    """Scoruje rosnące frazy z Trends których nie ma w GSC."""
    mono_score, mono_reasons = monetization_score(related_kw)
    # Rising query = high potential ale brak GSC data
    total = 10 + int(mono_score * 0.3) + 15  # base + mono + trend bonus
    return {
        "keyword": related_kw,
        "source": f"Trends rising (powiązane z '{parent_kw}')",
        "clicks": 0,
        "impressions": 0,
        "ctr": 0,
        "position": 999,
        "score": min(total, 70),
        "mono_score": mono_score,
        "mono_reasons": mono_reasons,
        "trend_direction": "rosnący 🚀",
        "pillar": detect_pillar(related_kw),
        "article_type": suggested_article_type(related_kw, mono_reasons),
        "already_in_ideas": False,
    }


# ── Markdown report ───────────────────────────────────────────────────────────
def _score_bar(score, width=10):
    filled = int(score / 100 * width)
    return "█" * filled + "░" * (width - filled)


def _pos_str(pos):
    if pos >= 999:
        return "brak"
    return f"#{pos:.0f}"


def build_report(scored, rising_extras, focus=None, min_score=0):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Filtruj
    all_topics = scored + rising_extras
    filtered = [t for t in all_topics if t["score"] >= min_score]
    if focus == "monetization":
        filtered = [t for t in filtered if t["mono_score"] >= 20]
    elif focus == "traffic":
        filtered = [t for t in filtered if t["impressions"] >= 200]
    elif focus == "quick_wins":
        filtered = [t for t in filtered if 4 <= t["position"] <= 15 and t["impressions"] >= 100]

    filtered.sort(key=lambda x: x["score"], reverse=True)
    top = filtered[:30]

    lines = [
        f"# Topic Research — dokodu.it",
        f"Wygenerowano: {now_str} | Źródła: GSC + Google Trends",
        "",
        "## Ranking Tematów",
        "",
        f"Łącznie przeanalizowano: **{len(all_topics)}** fraz | Pokazuję top **{len(top)}**",
        "",
        "| # | Keyword | Score | Poz. | Impr. | Trend | Mono | Typ artykułu | Pillar |",
        "|---|---------|-------|------|-------|-------|------|-------------|--------|",
    ]

    for i, t in enumerate(top, 1):
        score_bar = _score_bar(t["score"])
        mono_bar  = "💰" * (t["mono_score"] // 25 + 1) if t["mono_score"] > 0 else "—"
        trend_icon = {"rosnący": "📈", "malejący": "📉", "stabilny": "➡️"}.get(
            t.get("trend_direction", ""), "❓"
        )
        already = " ✓" if t.get("already_in_ideas") else ""
        lines.append(
            f"| {i} | `{t['keyword']}`{already} | {t['score']} `{score_bar}` | "
            f"{_pos_str(t['position'])} | {t['impressions']:,} | "
            f"{trend_icon} | {mono_bar} | {t['article_type']} | {t['pillar']} |"
        )

    # Szczegóły monetyzacji
    lines += [
        "",
        "## Top 10 — Potencjał Produktowy (szczegóły)",
        "",
    ]
    mono_top = sorted(filtered, key=lambda x: x["mono_score"], reverse=True)[:10]
    for t in mono_top:
        if not t["mono_reasons"]:
            continue
        lines.append(f"### `{t['keyword']}` (mono score: {t['mono_score']})")
        lines.append("")
        for r in t["mono_reasons"]:
            lines.append(f"- {r}")
        lines.append(f"- **Sugerowany typ:** {t['article_type']}")
        if t.get("impressions"):
            lines.append(f"- **Dane GSC:** {t['impressions']:,} wyświetleń, poz. {_pos_str(t['position'])}")
        lines.append("")

    # Rosnące frazy z Trends bez pokrycia w GSC
    if rising_extras:
        lines += [
            "## Nowe Frazy z Google Trends (brak w GSC)",
            "> Tematy które rosną — możliwość wejścia przed konkurencją",
            "",
            "| Fraza | Powiązana z | Mono | Typ |",
            "|-------|-------------|------|-----|",
        ]
        for t in sorted(rising_extras, key=lambda x: x["mono_score"], reverse=True)[:15]:
            mono_bar = "💰" * (t["mono_score"] // 25 + 1) if t["mono_score"] > 0 else "—"
            lines.append(
                f"| `{t['keyword']}` | {t.get('source','')} | {mono_bar} | {t['article_type']} |"
            )

    # Breakdown per pillar
    lines += ["", "## Breakdown per Pillar", ""]
    from collections import Counter
    pillar_counts = Counter(t["pillar"] for t in top)
    for pillar, count in pillar_counts.most_common():
        avg_mono = sum(t["mono_score"] for t in top if t["pillar"] == pillar) / count
        lines.append(f"- **{pillar}**: {count} tematów, avg mono score: {avg_mono:.0f}")

    lines += [
        "",
        "## Legenda",
        "- **Score**: łączny score 0-100 (traffic + gap + pozycja + trend + monetyzacja)",
        "- **Mono**: potencjał monetyzacyjny (linki do produktów, afiliacja, usługi Dokodu)",
        "- **✓**: już istnieje w Ideas Bank",
        "- **📈/📉/➡️**: trend z Google Trends",
        "- **💰**: każda ikona = ~25 punktów mono score",
        "",
        "---",
        f"*DOKODU BRAIN Topic Research | {now_str}*",
    ]
    return "\n".join(lines), top


def add_to_ideas(topics, dry_run=False):
    """Dodaje top tematy do seo_ideas.py SQLite."""
    if not IDEAS_DB.exists():
        # Zainicjalizuj bazę przez seo_ideas.py
        subprocess.run([sys.executable, str(SCRIPTS_DIR / "seo_ideas.py"), "list"],
                      capture_output=True)

    conn = sqlite3.connect(str(IDEAS_DB))
    existing = {r[0] for r in conn.execute("SELECT target_keyword FROM blog_ideas").fetchall()}
    added = 0

    for t in topics:
        if t["keyword"] in existing:
            continue
        if t["score"] < 30:
            continue

        priority = "high" if t["score"] >= 65 else "medium" if t["score"] >= 45 else "low"
        intent = "commercial" if t["mono_score"] >= 30 else "informational"

        if dry_run:
            print(f"  [dry-run] Dodałbym: {t['keyword']} (score={t['score']}, priority={priority})")
            added += 1
            continue

        title = t["keyword"].title()
        conn.execute("""
            INSERT INTO blog_ideas
                (title, target_keyword, search_intent, pillar, status, priority,
                 source, current_position, monthly_volume, notes)
            VALUES (?, ?, ?, ?, 'POMYSŁ', ?, 'topic-research', ?, ?, ?)
        """, (
            title,
            t["keyword"],
            intent,
            t["pillar"],
            priority,
            round(t["position"], 1) if t["position"] < 900 else None,
            t["impressions"] if t["impressions"] else None,
            f"Score: {t['score']} | Mono: {t['mono_score']} | {', '.join(t['mono_reasons'][:2])}",
        ))
        added += 1

    conn.commit()
    conn.close()
    return added


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="DOKODU BRAIN — Topic Research & Scoring")
    parser.add_argument("--fetch-trends",  action="store_true", help="Pobierz świeże dane z Trends (auto-gsc)")
    parser.add_argument("--min-score",     type=int, default=0, help="Minimalny score (0-100)")
    parser.add_argument("--focus",         choices=["monetization", "traffic", "quick_wins"],
                                           help="Filtr tematyczny")
    parser.add_argument("--add-to-ideas",  action="store_true", help="Dodaj top tematy do Ideas Bank")
    parser.add_argument("--dry-run",       action="store_true", help="Pokaż co zostałoby dodane (bez zapisu)")
    parser.add_argument("--save",          action="store_true", help="Zapisz raport do BRAIN")
    parser.add_argument("--json",          action="store_true", dest="as_json")
    parser.add_argument("--top",           type=int, default=30, help="Ile tematów w raporcie")
    args = parser.parse_args()

    # Opcjonalnie: pobierz świeże Trends
    if args.fetch_trends:
        print("📡 Pobieranie danych Google Trends (auto-gsc)...", file=sys.stderr)
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "trends_fetch.py"), "--auto-gsc", "--days", "90"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"⚠️  Trends fetch error: {result.stderr[:200]}", file=sys.stderr)

    print("📂 Ładowanie danych GSC...", file=sys.stderr)
    queries, pages = load_gsc_data()
    if not queries:
        print("❌ Brak danych GSC. Uruchom: python3 gsc_fetch.py --save", file=sys.stderr)
        sys.exit(1)

    print("📂 Ładowanie danych Trends...", file=sys.stderr)
    trends_data = load_trends_data()
    existing_ideas = load_existing_ideas()

    print(f"🔬 Scoruję {len(queries)} fraz...", file=sys.stderr)
    scored = []
    for q in queries:
        query, clicks, impressions, ctr, position = q
        scored.append(score_topic(query, clicks, impressions, ctr, position,
                                   trends_data, existing_ideas))

    # Dodaj rosnące frazy z Trends których nie ma w GSC
    gsc_keywords = {q[0] for q in queries}
    rising_extras = []
    for kw_data in trends_data.values():
        for rising_kw in kw_data.get("rising_queries", []):
            if rising_kw and rising_kw not in gsc_keywords:
                parent_kw = next(
                    (k for k, v in trends_data.items() if rising_kw in v.get("rising_queries", [])),
                    "Trends"
                )
                rising_extras.append(score_rising_query(rising_kw, parent_kw, trends_data))
    gsc_keywords |= {r["keyword"] for r in rising_extras}

    if args.as_json:
        all_sorted = sorted(scored + rising_extras, key=lambda x: x["score"], reverse=True)
        print(json.dumps(all_sorted[:args.top], ensure_ascii=False, indent=2))
        return

    report, top_topics = build_report(scored, rising_extras, args.focus, args.min_score)
    print(report)

    if args.save:
        OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        OUT_FILE.write_text(report, encoding="utf-8")
        print(f"\n✅ Zapisano: {OUT_FILE}", file=sys.stderr)

    if args.add_to_ideas or args.dry_run:
        print(f"\n{'[DRY RUN] ' if args.dry_run else ''}Dodaję tematy do Ideas Bank...", file=sys.stderr)
        added = add_to_ideas(top_topics, dry_run=args.dry_run)
        print(f"✅ {'Dodano by' if args.dry_run else 'Dodano'}: {added} nowych tematów", file=sys.stderr)


if __name__ == "__main__":
    main()
