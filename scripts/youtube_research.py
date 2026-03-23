#!/usr/bin/env python3
"""
DOKODU BRAIN — YouTube Topic Research
Szuka filmów na dany temat, analizuje co działa, identyfikuje luki i kąty.

Użycie:
  python3 youtube_research.py "Claude Code vs Gemini CLI"
  python3 youtube_research.py "automatyzacja AI" --lang pl --max 15
  python3 youtube_research.py "n8n tutorial" --days 180 --save
"""

import sys
import json
import pickle
import argparse
import re
import sqlite3
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "dokodu"
TOKEN_FILE = CONFIG_DIR / "yt_token.pickle"
DB_FILE = CONFIG_DIR / "yt_data.db"
BRAIN_DIR = Path(__file__).parent.parent
RESEARCH_DIR = BRAIN_DIR / "30_RESOURCES" / "RES_YouTube"

try:
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
except ImportError:
    print("ERROR: pip3 install google-api-python-client google-auth-oauthlib", file=sys.stderr)
    sys.exit(1)


# ═══════════════════════════════════════════════════
# AUTH
# ═══════════════════════════════════════════════════

def get_youtube():
    with open(TOKEN_FILE, "rb") as f:
        import pickle as _p
        creds = _p.load(f)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return build("youtube", "v3", credentials=creds)


# ═══════════════════════════════════════════════════
# SEARCH
# ═══════════════════════════════════════════════════

def search_videos(youtube, query: str, max_results: int = 20,
                  lang: str | None = None, days: int | None = None) -> list[dict]:
    """Szuka filmów na YouTube i zwraca listę z metadanymi."""
    kwargs = dict(
        part="snippet",
        q=query,
        type="video",
        maxResults=min(max_results, 50),
        order="viewCount",
        videoDefinition="high",
    )
    if lang:
        kwargs["relevanceLanguage"] = lang
    if days:
        published_after = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
        kwargs["publishedAfter"] = published_after

    resp = youtube.search().list(**kwargs).execute()
    items = resp.get("items", [])

    if not items:
        return []

    # Pobierz statystyki dla znalezionych filmów
    video_ids = [item["id"]["videoId"] for item in items]
    stats_resp = youtube.videos().list(
        part="statistics,contentDetails",
        id=",".join(video_ids)
    ).execute()

    stats_map = {}
    for v in stats_resp.get("items", []):
        stats_map[v["id"]] = {
            "views": int(v["statistics"].get("viewCount", 0)),
            "likes": int(v["statistics"].get("likeCount", 0)),
            "comments": int(v["statistics"].get("commentCount", 0)),
            "duration": _parse_duration(v["contentDetails"].get("duration", "")),
        }

    results = []
    for item in items:
        vid_id = item["id"]["videoId"]
        snippet = item["snippet"]
        s = stats_map.get(vid_id, {})
        results.append({
            "video_id": vid_id,
            "title": snippet["title"],
            "channel": snippet["channelTitle"],
            "channel_id": snippet["channelId"],
            "published_at": snippet["publishedAt"][:10],
            "description": snippet.get("description", "")[:300],
            "url": f"https://youtube.com/watch?v={vid_id}",
            "views": s.get("views", 0),
            "likes": s.get("likes", 0),
            "comments": s.get("comments", 0),
            "duration": s.get("duration", "—"),
        })

    # Sortuj po wyświetleniach
    results.sort(key=lambda x: x["views"], reverse=True)
    return results


def _parse_duration(iso: str) -> str:
    if not iso:
        return "—"
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso)
    if not m:
        return "—"
    h, mi, s = (int(x) if x else 0 for x in m.groups())
    return f"{h}:{mi:02d}:{s:02d}" if h else f"{mi}:{s:02d}"


def _fmt(n: int) -> str:
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)


# ═══════════════════════════════════════════════════
# ANALIZA
# ═══════════════════════════════════════════════════

def analyze_topics(videos: list[dict], query: str) -> dict:
    """Wyciąga wzorce tytułów, tematy, luki."""

    # Słowa kluczowe z tytułów (bez stop words)
    stop_words = {
        "the", "a", "an", "and", "or", "in", "on", "at", "to", "for",
        "of", "with", "how", "why", "what", "is", "vs", "i", "w", "z",
        "do", "na", "jak", "co", "że", "nie", "się", "po", "czy", "to",
        "you", "your", "my", "this", "that", "it", "be", "are", "was",
    }

    all_words = []
    title_patterns = {
        "question": [],      # tytuły z pytaniem
        "number": [],        # tytuły z liczbą
        "comparison": [],    # tytuły porównawcze
        "tutorial": [],      # tutoriale
        "opinion": [],       # opinie / "dlaczego"
        "news": [],          # nowości
    }

    channels_views = {}
    durations = {"short": 0, "medium": 0, "long": 0}

    for v in videos:
        title = v["title"]
        words = re.findall(r"\b[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]{3,}\b", title.lower())
        all_words.extend([w for w in words if w not in stop_words])

        # Klasyfikuj tytuł
        if "?" in title:
            title_patterns["question"].append(title)
        if re.search(r"\b\d+\b", title):
            title_patterns["number"].append(title)
        if re.search(r"\b(vs|versus|czy|porównan|kontra)\b", title, re.I):
            title_patterns["comparison"].append(title)
        if re.search(r"\b(tutorial|kurs|jak|guide|nauka|learn|getting started|poradnik)\b", title, re.I):
            title_patterns["tutorial"].append(title)
        if re.search(r"\b(dlaczego|why|opinia|honest|prawda|truth|review)\b", title, re.I):
            title_patterns["opinion"].append(title)
        if re.search(r"\b(nowy|new|update|release|2025|2026|latest|właśnie)\b", title, re.I):
            title_patterns["news"].append(title)

        # Kanały
        ch = v["channel"]
        channels_views[ch] = channels_views.get(ch, 0) + v["views"]

        # Długość
        dur = v["duration"]
        if dur == "—":
            pass
        elif ":" in dur:
            parts = dur.split(":")
            total_min = int(parts[0]) * 60 + int(parts[1]) if len(parts) == 3 else int(parts[0])
            if total_min < 10:
                durations["short"] += 1
            elif total_min < 20:
                durations["medium"] += 1
            else:
                durations["long"] += 1

    top_words = Counter(all_words).most_common(15)
    top_channels = sorted(channels_views.items(), key=lambda x: x[1], reverse=True)[:5]

    return {
        "top_words": top_words,
        "title_patterns": {k: v for k, v in title_patterns.items() if v},
        "top_channels": top_channels,
        "durations": durations,
        "total_views": sum(v["views"] for v in videos),
        "avg_views": sum(v["views"] for v in videos) // len(videos) if videos else 0,
    }


# ═══════════════════════════════════════════════════
# REPORT
# ═══════════════════════════════════════════════════

def build_report(query: str, videos: list[dict], analysis: dict,
                 lang: str | None, days: int | None) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    period_str = f"ostatnie {days} dni" if days else "wszystkie czasy"
    lang_str = f" | Język: {lang}" if lang else ""

    lines = [
        f"# Research: \"{query}\"",
        f"Wygenerowano: {now} | Okres: {period_str}{lang_str} | Filmów: {len(videos)}\n",
    ]

    # --- TOP FILMY ---
    lines += [
        "## Top Filmy (wg wyświetleń)\n",
        "| # | Tytuł | Kanał | Wyśw. | Likes | Dług. | Data |",
        "|---|-------|-------|-------|-------|-------|------|",
    ]
    for i, v in enumerate(videos[:15], 1):
        title = v["title"]
        if len(title) > 50:
            title = title[:49] + "…"
        lines.append(
            f"| {i} | [{title}]({v['url']}) | {v['channel']} | "
            f"{_fmt(v['views'])} | {_fmt(v['likes'])} | {v['duration']} | {v['published_at']} |"
        )
    lines.append("")

    # --- DOMINUJĄCE KANAŁY ---
    lines += ["## Dominujące Kanały\n"]
    for ch, views in analysis["top_channels"]:
        lines.append(f"- **{ch}** — łączne wyśw. w wynikach: {_fmt(views)}")
    lines.append("")

    # --- WZORCE TYTUŁÓW ---
    lines += ["## Wzorce Tytułów (co wybija)\n"]
    pattern_labels = {
        "question": "Pytania (?)",
        "number": "Z liczbą",
        "comparison": "Porównania (vs)",
        "tutorial": "Tutoriale / Jak zrobić",
        "opinion": "Opinie / Dlaczego",
        "news": "Nowości / Update",
    }
    for pattern, titles in analysis["title_patterns"].items():
        lines.append(f"**{pattern_labels.get(pattern, pattern)}** ({len(titles)} filmów):")
        for t in titles[:3]:
            lines.append(f"  - {t}")
    lines.append("")

    # --- DŁUGOŚĆ FILMÓW ---
    d = analysis["durations"]
    total_dur = sum(d.values()) or 1
    lines += [
        "## Długość Filmów\n",
        f"- Short (<10 min): {d['short']} ({d['short']*100//total_dur}%)",
        f"- Medium (10-20 min): {d['medium']} ({d['medium']*100//total_dur}%)",
        f"- Long (>20 min): {d['long']} ({d['long']*100//total_dur}%)",
        "",
    ]

    # --- SŁOWA KLUCZOWE ---
    lines += [
        "## Najczęstsze Słowa w Tytułach\n",
        ", ".join(f"`{w}` ({c}x)" for w, c in analysis["top_words"]),
        "",
    ]

    # --- ŚREDNIE STATYSTYKI ---
    lines += [
        "## Statystyki\n",
        f"- Łączne wyświetlenia top filmów: {_fmt(analysis['total_views'])}",
        f"- Średnie wyświetlenia na film: {_fmt(analysis['avg_views'])}",
        f"- Najlepszy film: {_fmt(videos[0]['views'])} wyśw. — \"{videos[0]['title']}\" ({videos[0]['channel']})" if videos else "",
        "",
    ]

    # --- LUKI I KĄTY (meta-analiza) ---
    lines += [
        "## Luki i Kąty do Zagospodarowania\n",
        "> Sekcja do uzupełnienia przez `/yt-research` skill na podstawie powyższych danych.\n",
    ]

    lines += ["---", f"*DOKODU BRAIN Topic Research | {now}*"]
    return "\n".join(lines)


# ═══════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="YouTube Topic Research")
    parser.add_argument("query", help="Temat do zbadania")
    parser.add_argument("--lang", choices=["pl", "en"], help="Język filmów")
    parser.add_argument("--max", type=int, default=20, dest="max_results")
    parser.add_argument("--days", type=int, help="Tylko filmy z ostatnich N dni")
    parser.add_argument("--save", action="store_true", help="Zapisz raport do BRAIN")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    print(f"🔍 Szukam: \"{args.query}\"...", file=sys.stderr)
    youtube = get_youtube()

    # Szukaj po polsku i po angielsku jeśli nie podano języka
    if args.lang:
        videos = search_videos(youtube, args.query, args.max_results, args.lang, args.days)
    else:
        pl_videos = search_videos(youtube, args.query, args.max_results // 2 + 1, "pl", args.days)
        en_videos = search_videos(youtube, args.query, args.max_results // 2 + 1, "en", args.days)
        # Połącz, deduplikuj, posortuj
        seen = set()
        videos = []
        for v in pl_videos + en_videos:
            if v["video_id"] not in seen:
                seen.add(v["video_id"])
                videos.append(v)
        videos.sort(key=lambda x: x["views"], reverse=True)
        videos = videos[:args.max_results]

    print(f"✅ Znaleziono {len(videos)} filmów.", file=sys.stderr)

    if not videos:
        print("Brak wyników.", file=sys.stderr)
        sys.exit(0)

    if args.as_json:
        print(json.dumps(videos, ensure_ascii=False, indent=2))
        return

    analysis = analyze_topics(videos, args.query)
    report = build_report(args.query, videos, analysis, args.lang, args.days)
    print(report)

    if args.save:
        slug = re.sub(r"[^\w]", "_", args.query.lower())[:40]
        out_file = RESEARCH_DIR / f"YT_Research_{slug}.md"
        out_file.write_text(report, encoding="utf-8")
        print(f"\n✅ Zapisano: {out_file}", file=sys.stderr)
        _update_index(args.query, slug, videos, args.lang)


def _update_index(query: str, slug: str, videos: list[dict], lang: str | None) -> None:
    """Dopisuje wpis do YT_Research_Index.md."""
    index_file = RESEARCH_DIR / "YT_Research_Index.md"
    if not index_file.exists():
        return

    date = datetime.now().strftime("%Y-%m-%d")
    top_video = videos[0] if videos else None
    avg_views = sum(v["views"] for v in videos) // len(videos) if videos else 0
    lang_note = f" [{lang.upper()}]" if lang else ""
    top_note = f"Top: {_fmt(top_video['views'])} wyśw. ({top_video['channel']})" if top_video else "—"
    filename = f"YT_Research_{slug}.md"

    new_row = f"| {date} | {query}{lang_note} | 🟡 | {top_note} | [{filename}](./{filename}) |"

    content = index_file.read_text(encoding="utf-8")
    # Wstaw nowy wpis po nagłówku tabeli
    marker = "|------|-------|---------|-----------------------------------|------|\n"
    if marker in content:
        updated = content.replace(marker, marker + new_row + "\n", 1)
        index_file.write_text(updated, encoding="utf-8")
        print(f"✅ Zaktualizowano indeks: {index_file}", file=sys.stderr)


if __name__ == "__main__":
    main()
