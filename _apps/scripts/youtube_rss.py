#!/usr/bin/env python3
"""
DOKODU BRAIN — YouTube Competitive Intelligence (RSS)
Śledzi kanały konkurencji i trendy z rynku US bez zużywania API quota.

Użycie:
  python3 youtube_rss.py                  # fetch wszystkich kanałów
  python3 youtube_rss.py --group pl       # tylko polskie kanały
  python3 youtube_rss.py --group us       # tylko US kanały
  python3 youtube_rss.py --days 7         # filmy z ostatnich 7 dni
  python3 youtube_rss.py --report         # raport Markdown
"""

import sys
import sqlite3
import argparse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.request import urlopen, Request as URLRequest
from urllib.error import URLError

CONFIG_DIR = Path.home() / ".config" / "dokodu"
DB_FILE = CONFIG_DIR / "yt_data.db"

# ═══════════════════════════════════════════════════
# KONFIGURACJA KANAŁÓW
# ═══════════════════════════════════════════════════

CHANNELS = {
    # --- Polska konkurencja ---
    "UCsheAU3SGQuZcKyx_tdZR-Q": {"name": "Robert Szewczyk",    "group": "pl", "priority": "high"},
    "UCOW67Wpaa7elCGoLAB9HTrw": {"name": "Mikołaj Abramczuk",  "group": "pl", "priority": "high"},
    "UC55Xsy8GIzfeO7CuxTwtYkg": {"name": "Startuj AI",         "group": "pl", "priority": "high"},
    "UCPvezjwY1202MbxkTKibdmw": {"name": "Norbert Uselis",     "group": "pl", "priority": "high"},
    # --- US trendsetting ---
    "UChpleBmo18P08aKCIgti38g": {"name": "Matt Wolfe",         "group": "us", "priority": "high"},
    "UCNJ1Ymd5yFuUPtn21xtRbbw": {"name": "AI Explained",       "group": "us", "priority": "high"},
    "UCsBjURrPoezykLs9EqgamOA": {"name": "Fireship",           "group": "us", "priority": "medium"},
    "UCvKRFNawVcuz4b9ihUTApCg": {"name": "David Shapiro",      "group": "us", "priority": "medium"},
    "UCawZsQWqfGSbCI5yjkdVkTA": {"name": "Matthew Berman",     "group": "us", "priority": "medium"},
}

RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
NS = {"yt": "http://www.youtube.com/xml/schemas/2015",
      "media": "http://search.yahoo.com/mrss/",
      "atom": "http://www.w3.org/2005/Atom"}


# ═══════════════════════════════════════════════════
# DATABASE
# ═══════════════════════════════════════════════════

def db_connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def db_init_competitive(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS competitor_channels (
            channel_id   TEXT PRIMARY KEY,
            name         TEXT,
            group_tag    TEXT,
            priority     TEXT,
            added_at     TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS competitor_videos (
            video_id     TEXT PRIMARY KEY,
            channel_id   TEXT NOT NULL,
            title        TEXT,
            published_at TEXT,
            views        INTEGER DEFAULT 0,
            fetched_at   TEXT DEFAULT (datetime('now')),
            adapt_flag   INTEGER DEFAULT 0,
            adapt_notes  TEXT
        );
    """)
    # Zapisz kanały
    for channel_id, meta in CHANNELS.items():
        conn.execute("""
            INSERT OR IGNORE INTO competitor_channels (channel_id, name, group_tag, priority)
            VALUES (?, ?, ?, ?)
        """, (channel_id, meta["name"], meta["group"], meta["priority"]))
    conn.commit()


# ═══════════════════════════════════════════════════
# RSS FETCH
# ═══════════════════════════════════════════════════

def fetch_rss(channel_id: str) -> list[dict]:
    url = RSS_URL.format(channel_id=channel_id)
    try:
        req = URLRequest(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=10) as resp:
            xml_data = resp.read()
    except URLError as e:
        print(f"⚠️  RSS error ({channel_id}): {e}", file=sys.stderr)
        return []

    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        print(f"⚠️  XML parse error ({channel_id}): {e}", file=sys.stderr)
        return []

    entries = []
    for entry in root.findall("atom:entry", NS):
        video_id = entry.findtext("yt:videoId", namespaces=NS) or ""
        title = entry.findtext("atom:title", namespaces=NS) or ""
        published = entry.findtext("atom:published", namespaces=NS) or ""
        published_date = published[:10] if published else ""

        # View count z media:statistics
        media_group = entry.find("media:group", NS)
        views = 0
        if media_group is not None:
            stats = media_group.find("media:community/media:statistics", NS)
            if stats is not None:
                views = int(stats.get("views", 0))

        if video_id and title:
            entries.append({
                "video_id": video_id,
                "title": title,
                "published_at": published_date,
                "views": views,
            })

    return entries


def save_videos(conn: sqlite3.Connection, channel_id: str, videos: list[dict]) -> int:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_count = 0
    for v in videos:
        cur = conn.execute(
            "SELECT video_id FROM competitor_videos WHERE video_id = ?", (v["video_id"],)
        )
        is_new = cur.fetchone() is None
        conn.execute("""
            INSERT OR REPLACE INTO competitor_videos (video_id, channel_id, title, published_at, views, fetched_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (v["video_id"], channel_id, v["title"], v["published_at"], v["views"], now))
        if is_new:
            new_count += 1
    conn.commit()
    return new_count


# ═══════════════════════════════════════════════════
# REPORT
# ═══════════════════════════════════════════════════

def build_report(conn: sqlite3.Connection, days: int, group: str | None) -> str:
    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        f"# Competitive Intelligence — YouTube",
        f"Wygenerowano: {now_str} | Okres: ostatnie {days} dni\n",
    ]

    groups = ["pl", "us"] if not group else [group]
    group_labels = {"pl": "🇵🇱 Polska Konkurencja", "us": "🇺🇸 US Trendsetting"}

    for g in groups:
        lines.append(f"## {group_labels.get(g, g)}\n")

        channels_in_group = [
            (cid, meta) for cid, meta in CHANNELS.items() if meta["group"] == g
        ]

        for channel_id, meta in sorted(channels_in_group, key=lambda x: x[1]["priority"]):
            videos = conn.execute("""
                SELECT title, published_at, views, video_id, adapt_flag, adapt_notes
                FROM competitor_videos
                WHERE channel_id = ? AND published_at >= ?
                ORDER BY published_at DESC
            """, (channel_id, since)).fetchall()

            lines.append(f"### {meta['name']}")
            if not videos:
                lines.append("*Brak nowych filmów w tym okresie.*\n")
                continue

            lines.append("| Data | Tytuł | Wyśw. | Adaptować? |")
            lines.append("|------|-------|-------|-----------|")
            for v in videos:
                url = f"https://youtube.com/watch?v={v['video_id']}"
                title = v["title"]
                if len(title) > 55:
                    title = title[:54] + "…"
                views_str = f"{v['views']:,}" if v['views'] else "—"
                adapt = "✅ TAK" if v["adapt_flag"] else "—"
                lines.append(f"| {v['published_at']} | [{title}]({url}) | {views_str} | {adapt} |")
            lines.append("")

    lines += ["---", f"*DOKODU BRAIN Competitive Intelligence | {now_str}*"]
    return "\n".join(lines)


# ═══════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="YouTube RSS Competitive Intel")
    parser.add_argument("--group", choices=["pl", "us"], help="Filtruj grupę kanałów")
    parser.add_argument("--days", type=int, default=14, help="Okres raportu (dni)")
    parser.add_argument("--report", action="store_true", help="Tylko raport, bez fetchu")
    parser.add_argument("--save", action="store_true", help="Zapisz raport do BRAIN")
    args = parser.parse_args()

    conn = db_connect()
    db_init_competitive(conn)

    if not args.report:
        channels_to_fetch = {
            cid: meta for cid, meta in CHANNELS.items()
            if not args.group or meta["group"] == args.group
        }

        print(f"📡 Fetchuję RSS dla {len(channels_to_fetch)} kanałów...", file=sys.stderr)
        total_new = 0
        for channel_id, meta in channels_to_fetch.items():
            videos = fetch_rss(channel_id)
            new = save_videos(conn, channel_id, videos)
            total_new += new
            status = f"+{new} nowych" if new else "bez zmian"
            print(f"  {'🇵🇱' if meta['group'] == 'pl' else '🇺🇸'} {meta['name']}: {len(videos)} filmów ({status})", file=sys.stderr)

        print(f"\n✅ Łącznie nowych filmów: {total_new}", file=sys.stderr)

    report = build_report(conn, args.days, args.group)
    conn.close()

    print(report)

    if args.save:
        brain_dir = Path(__file__).parent.parent
        out_file = brain_dir / "30_RESOURCES" / "RES_YouTube" / "YT_Competitive.md"
        out_file.write_text(report, encoding="utf-8")
        print(f"\n✅ Zapisano: {out_file}", file=sys.stderr)


if __name__ == "__main__":
    main()
