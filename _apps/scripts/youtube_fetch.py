#!/usr/bin/env python3
"""
DOKODU BRAIN — YouTube Integration Script
Autor: Kacper Sieradzinski | Dokodu sp. z o.o.

Pobiera dane z YouTube Data API v3 + YouTube Analytics API.
Wyniki trafiają do DOKODU_BRAIN/20_AREAS/AREA_YouTube/.

Użycie:
  python3 youtube_fetch.py               # pełny raport (28 dni)
  python3 youtube_fetch.py --days 90     # ostatnie 90 dni
  python3 youtube_fetch.py --mode stats  # tylko statystyki kanału
  python3 youtube_fetch.py --mode videos # tylko lista filmów
  python3 youtube_fetch.py --json        # surowy JSON zamiast Markdown
"""

import os
import sys
import json
import pickle
import sqlite3
import argparse
import re
from datetime import datetime, timedelta
from pathlib import Path

# --- Ścieżki ---
SCRIPT_DIR = Path(__file__).parent.resolve()
BRAIN_DIR = SCRIPT_DIR.parent
CONFIG_DIR = Path.home() / ".config" / "dokodu"
CREDENTIALS_FILE = CONFIG_DIR / "yt_credentials.json"
TOKEN_FILE = CONFIG_DIR / "yt_token.pickle"
DB_FILE = CONFIG_DIR / "yt_data.db"
AREA_YT_DIR = BRAIN_DIR / "20_AREAS" / "AREA_YouTube"


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
        CREATE TABLE IF NOT EXISTS channel_snapshots (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            fetched_at  TEXT NOT NULL,
            channel_id  TEXT NOT NULL,
            title       TEXT,
            subscribers INTEGER,
            total_views INTEGER,
            video_count INTEGER
        );

        CREATE TABLE IF NOT EXISTS videos (
            video_id     TEXT PRIMARY KEY,
            title        TEXT,
            published_at TEXT,
            duration     TEXT,
            tags         TEXT
        );

        CREATE TABLE IF NOT EXISTS video_stats (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            fetched_at TEXT NOT NULL,
            video_id   TEXT NOT NULL,
            views      INTEGER,
            likes      INTEGER,
            comments   INTEGER,
            UNIQUE(fetched_at, video_id)
        );

        CREATE TABLE IF NOT EXISTS channel_analytics (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            fetched_at       TEXT NOT NULL,
            period_start     TEXT NOT NULL,
            period_end       TEXT NOT NULL,
            views            INTEGER,
            watch_time_min   REAL,
            avg_view_dur_sec REAL,
            subs_gained      INTEGER,
            subs_lost        INTEGER,
            UNIQUE(period_start, period_end)
        );

        CREATE TABLE IF NOT EXISTS video_analytics (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            fetched_at       TEXT NOT NULL,
            period_start     TEXT NOT NULL,
            period_end       TEXT NOT NULL,
            video_id         TEXT NOT NULL,
            views            INTEGER,
            watch_time_min   REAL,
            avg_view_dur_sec REAL,
            subs_gained      INTEGER,
            UNIQUE(period_start, period_end, video_id)
        );
    """)
    conn.commit()


def db_save(conn: sqlite3.Connection, channel: dict, videos: list,
            video_details: dict, analytics: dict, video_analytics_data: dict,
            start_date: str, end_date: str) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_today = datetime.now().strftime("%Y-%m-%d")

    # Channel snapshot
    conn.execute("""
        INSERT INTO channel_snapshots (fetched_at, channel_id, title, subscribers, total_views, video_count)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (now, channel["channel_id"], channel["title"],
          channel["subscribers"], channel["total_views"], channel["video_count"]))

    # Videos + stats
    for v in videos:
        vid_id = v["video_id"]
        det = video_details.get(vid_id, {})
        conn.execute("""
            INSERT OR REPLACE INTO videos (video_id, title, published_at, duration, tags)
            VALUES (?, ?, ?, ?, ?)
        """, (vid_id, v["title"], v["published_at"],
              det.get("duration", ""), json.dumps(det.get("tags", []))))

        conn.execute("""
            INSERT OR REPLACE INTO video_stats (fetched_at, video_id, views, likes, comments)
            VALUES (?, ?, ?, ?, ?)
        """, (date_today, vid_id, det.get("views", 0),
              det.get("likes", 0), det.get("comments", 0)))

    # Channel analytics
    if analytics:
        conn.execute("""
            INSERT OR REPLACE INTO channel_analytics
            (fetched_at, period_start, period_end, views, watch_time_min, avg_view_dur_sec, subs_gained, subs_lost)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (now, start_date, end_date,
              int(analytics.get("views", 0)),
              analytics.get("estimatedMinutesWatched", 0),
              analytics.get("averageViewDuration", 0),
              int(analytics.get("subscribersGained", 0)),
              int(analytics.get("subscribersLost", 0))))

    # Per-video analytics
    for vid_id, van in video_analytics_data.items():
        conn.execute("""
            INSERT OR REPLACE INTO video_analytics
            (fetched_at, period_start, period_end, video_id, views, watch_time_min, avg_view_dur_sec, subs_gained)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (now, start_date, end_date, vid_id,
              int(van.get("views", 0)),
              van.get("estimatedMinutesWatched", 0),
              van.get("averageViewDuration", 0),
              int(van.get("subscribersGained", 0))))

    conn.commit()
    print(f"✅ Zapisano do bazy: {DB_FILE}", file=sys.stderr)


def db_read_latest(conn: sqlite3.Connection) -> dict:
    """Czyta najnowsze dane z bazy (bez odpytywania API)."""
    channel = dict(conn.execute(
        "SELECT * FROM channel_snapshots ORDER BY fetched_at DESC LIMIT 1"
    ).fetchone() or {})

    analytics = conn.execute(
        "SELECT * FROM channel_analytics ORDER BY fetched_at DESC LIMIT 1"
    ).fetchone()
    analytics = dict(analytics) if analytics else {}

    videos_rows = conn.execute("""
        SELECT v.video_id, v.title, v.published_at, v.duration,
               vs.views, vs.likes, vs.comments,
               van.avg_view_dur_sec, van.watch_time_min
        FROM videos v
        LEFT JOIN video_stats vs ON v.video_id = vs.video_id
            AND vs.fetched_at = (SELECT MAX(fetched_at) FROM video_stats WHERE video_id = v.video_id)
        LEFT JOIN video_analytics van ON v.video_id = van.video_id
            AND van.fetched_at = (SELECT MAX(fetched_at) FROM video_analytics WHERE video_id = v.video_id)
        ORDER BY v.published_at DESC
        LIMIT 50
    """).fetchall()

    return {
        "channel": channel,
        "analytics": analytics,
        "videos": [dict(r) for r in videos_rows],
    }

# --- Sprawdzenie zależności ---
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

# --- Scopes OAuth ---
SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
]


# ══════════════════════════════════════════════
# AUTH
# ══════════════════════════════════════════════

def authenticate() -> object:
    """OAuth 2.0 — obsługuje WSL2 przez flow konsolowy."""
    creds = None

    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Token wygasł i nie można odświeżyć: {e}", file=sys.stderr)
                creds = None

        if not creds:
            if not CREDENTIALS_FILE.exists():
                print(f"\n❌ BRAK PLIKU CREDENTIALS!\n")
                print(f"Oczekiwany plik: {CREDENTIALS_FILE}")
                print("\nJak go uzyskać:")
                print("  1. Google Cloud Console → APIs & Services → Credentials")
                print("  2. Create Credentials → OAuth 2.0 Client ID → Desktop app")
                print("  3. Pobierz JSON → zmień nazwę na 'yt_credentials.json'")
                print(f"  4. Wgraj do: {SCRIPT_DIR}/")
                print("\nSzczegóły: DOKODU_BRAIN/scripts/YOUTUBE_SETUP.md")
                sys.exit(1)

            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES
            )
            # WSL2: nie otwieramy przeglądarki automatycznie — drukujemy URL
            print("\n" + "="*60, file=sys.stderr)
            print("🌐 WYMAGANA AUTORYZACJA GOOGLE", file=sys.stderr)
            print("="*60, file=sys.stderr)
            print("Za chwilę zobaczysz URL — otwórz go w przeglądarce Windows.", file=sys.stderr)
            print("Po zalogowaniu wróć tutaj (token zapisze się automatycznie).", file=sys.stderr)
            print("="*60 + "\n", file=sys.stderr)
            creds = flow.run_local_server(port=0, open_browser=False)

        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)
        print("✅ Token zapisany.", file=sys.stderr)

    return creds


# ══════════════════════════════════════════════
# FETCH FUNCTIONS
# ══════════════════════════════════════════════

def get_channel_info(youtube) -> dict:
    resp = youtube.channels().list(
        part="snippet,statistics,contentDetails,brandingSettings",
        mine=True
    ).execute()

    if not resp.get("items"):
        raise ValueError("Nie znaleziono kanału YouTube dla tego konta.")

    ch = resp["items"][0]
    stats = ch["statistics"]
    return {
        "channel_id": ch["id"],
        "title": ch["snippet"]["title"],
        "description": ch["snippet"].get("description", "")[:300],
        "subscribers": int(stats.get("subscriberCount", 0)),
        "total_views": int(stats.get("viewCount", 0)),
        "video_count": int(stats.get("videoCount", 0)),
        "uploads_playlist": ch["contentDetails"]["relatedPlaylists"]["uploads"],
        "country": ch["snippet"].get("country", "PL"),
        "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }


def get_videos(youtube, uploads_playlist_id: str, max_results: int = 30) -> list:
    videos = []
    next_page_token = None

    while len(videos) < max_results:
        batch_size = min(50, max_results - len(videos))
        resp = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=batch_size,
            pageToken=next_page_token
        ).execute()

        for item in resp.get("items", []):
            videos.append({
                "video_id": item["contentDetails"]["videoId"],
                "title": item["snippet"]["title"],
                "published_at": item["snippet"]["publishedAt"][:10],
                "thumbnail": item["snippet"]["thumbnails"].get("high", {}).get("url", ""),
            })

        next_page_token = resp.get("nextPageToken")
        if not next_page_token:
            break

    return videos


def get_video_details(youtube, video_ids: list) -> dict:
    """Statystyki + długość dla listy video_id (batch po 50)."""
    details = {}

    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i + 50]
        resp = youtube.videos().list(
            part="statistics,contentDetails,snippet",
            id=",".join(batch)
        ).execute()

        for item in resp.get("items", []):
            vid_id = item["id"]
            s = item["statistics"]
            details[vid_id] = {
                "views": int(s.get("viewCount", 0)),
                "likes": int(s.get("likeCount", 0)),
                "comments": int(s.get("commentCount", 0)),
                "duration": _parse_duration(item["contentDetails"].get("duration", "")),
                "tags": item["snippet"].get("tags", []),
            }

    return details


def get_channel_analytics(yt_analytics, channel_id: str, start_date: str, end_date: str) -> dict:
    """Analytics na poziomie kanału za podany okres."""
    try:
        resp = yt_analytics.reports().query(
            ids=f"channel=={channel_id}",
            startDate=start_date,
            endDate=end_date,
            metrics="views,estimatedMinutesWatched,averageViewDuration,"
                    "subscribersGained,subscribersLost",
            dimensions="day",
            sort="day",
        ).execute()
        return _aggregate_analytics(resp)
    except HttpError as e:
        print(f"⚠️  Analytics error: {e}", file=sys.stderr)
        return {}


def get_video_analytics(yt_analytics, channel_id: str, video_ids: list,
                        start_date: str, end_date: str) -> dict:
    """Analytics per video dla podanego okresu."""
    if not video_ids:
        return {}
    try:
        resp = yt_analytics.reports().query(
            ids=f"channel=={channel_id}",
            startDate=start_date,
            endDate=end_date,
            metrics="views,estimatedMinutesWatched,averageViewDuration,subscribersGained",
            dimensions="video",
            filters=f"video=={','.join(video_ids[:200])}",
            sort="-views",
            maxResults=50,
        ).execute()

        result = {}
        headers = [h["name"] for h in resp.get("columnHeaders", [])]
        for row in resp.get("rows", []):
            vid_id = row[0]
            result[vid_id] = {h: row[i] for i, h in enumerate(headers[1:], 1)}
        return result
    except HttpError as e:
        print(f"⚠️  Video analytics error: {e}", file=sys.stderr)
        return {}


# ══════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════

def _parse_duration(iso: str) -> str:
    if not iso:
        return "—"
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso)
    if not m:
        return "—"
    h, mi, s = (int(x) if x else 0 for x in m.groups())
    if h:
        return f"{h}:{mi:02d}:{s:02d}"
    return f"{mi}:{s:02d}"


def _aggregate_analytics(resp: dict) -> dict:
    headers = [h["name"] for h in resp.get("columnHeaders", [])]
    totals: dict = {}
    for row in resp.get("rows", []):
        for i, h in enumerate(headers[1:], 1):
            totals[h] = totals.get(h, 0) + (row[i] or 0)
    # CTR jest średnią, nie sumą
    if "impressionClickThroughRate" in totals and resp.get("rows"):
        ctr_vals = [row[headers.index("impressionClickThroughRate")]
                    for row in resp.get("rows", [])
                    if row[headers.index("impressionClickThroughRate")]]
        totals["impressionClickThroughRate"] = sum(ctr_vals) / len(ctr_vals) if ctr_vals else 0
    return totals


def _fmt(n, suffix="") -> str:
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M{suffix}"
    if n >= 1_000:
        return f"{n/1_000:.1f}K{suffix}"
    return f"{int(n)}{suffix}"


def _fmt_duration_sec(seconds) -> str:
    s = int(seconds or 0)
    return f"{s // 60}:{s % 60:02d}"


# ══════════════════════════════════════════════
# OUTPUT
# ══════════════════════════════════════════════

def build_markdown_report(channel: dict, analytics: dict, videos: list,
                          video_details: dict, video_analytics: dict,
                          start_date: str, end_date: str) -> str:
    lines = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines += [
        f"# YouTube — {channel['title']}",
        f"Pobrano: {now} | Okres analytics: {start_date} → {end_date}",
        "",
        "## Kanał",
        f"| Metryka | Wartość |",
        f"|---------|---------|",
        f"| Subskrybenci | **{_fmt(channel['subscribers'])}** |",
        f"| Łączne wyświetlenia | {_fmt(channel['total_views'])} |",
        f"| Liczba filmów | {channel['video_count']} |",
        f"| Pobrano | {channel['fetched_at']} |",
        "",
    ]

    if analytics:
        views = analytics.get("views", 0)
        wt_min = analytics.get("estimatedMinutesWatched", 0)
        avg_dur = analytics.get("averageViewDuration", 0)
        subs_g = analytics.get("subscribersGained", 0)
        subs_l = analytics.get("subscribersLost", 0)
        net_subs = subs_g - subs_l
        period_days = (datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days

        lines += [
            f"## Analytics (ostatnie {period_days} dni)",
            "| Metryka | Wartość |",
            "|---------|---------|",
            f"| Wyświetlenia | **{_fmt(views)}** |",
            f"| Watch time | {_fmt(wt_min)} min ({wt_min/60:.0f} godz.) |",
            f"| Avg view duration | {_fmt_duration_sec(avg_dur)} |",
            f"| Nowi subskrybenci | +{int(subs_g):,} / -{int(subs_l):,} = **{int(net_subs):+,}** |",
            "",
        ]

    # Tabela filmów
    lines += [
        f"## Ostatnie {len(videos)} filmów",
        "",
        "| # | Tytuł | Data | Wyśw. | Avg dur | Likes | Dług. |",
        "|---|-------|------|-------|---------|-------|-------|",
    ]

    for i, v in enumerate(videos, 1):
        vid_id = v["video_id"]
        det = video_details.get(vid_id, {})
        van = video_analytics.get(vid_id, {})

        title = v["title"]
        if len(title) > 45:
            title = title[:44] + "…"

        url = f"https://youtube.com/watch?v={vid_id}"
        views = _fmt(det.get("views", 0))
        avg_dur_str = _fmt_duration_sec(van.get("averageViewDuration", 0)) if van.get("averageViewDuration") else "—"
        likes = _fmt(det.get("likes", 0))
        duration = det.get("duration", "—")

        lines.append(
            f"| {i} | [{title}]({url}) | {v['published_at']} | {views} | {avg_dur_str} | {likes} | {duration} |"
        )

    lines += ["", "---", f"*DOKODU BRAIN YouTube Integration | {now}*"]
    return "\n".join(lines)


def save_to_brain(report_md: str, channel: dict) -> None:
    """Zapisuje raport do AREA_YouTube."""
    out_file = AREA_YT_DIR / "YT_Last_Sync.md"
    out_file.write_text(report_md, encoding="utf-8")
    print(f"✅ Zapisano: {out_file}", file=sys.stderr)


# ══════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="DOKODU BRAIN — YouTube Fetch")
    parser.add_argument("--mode", choices=["stats", "videos", "all"], default="all")
    parser.add_argument("--days", type=int, default=28, help="Ile dni wstecz dla analytics")
    parser.add_argument("--max-videos", type=int, default=30, help="Ile ostatnich filmów")
    parser.add_argument("--json", action="store_true", help="Wyjście w JSON zamiast Markdown")
    parser.add_argument("--save", action="store_true", help="Zapisz raport MD do BRAIN")
    parser.add_argument("--from-db", action="store_true", help="Czytaj z lokalnej bazy (bez API)")
    args = parser.parse_args()

    conn = db_connect()
    db_init(conn)

    # Tryb offline — czytaj z bazy bez odpytywania API
    if args.from_db:
        print("📂 Czytam z lokalnej bazy danych...", file=sys.stderr)
        data = db_read_latest(conn)
        if not data["channel"]:
            print("❌ Baza jest pusta. Uruchom najpierw bez --from-db.", file=sys.stderr)
            sys.exit(1)
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            ch = data["channel"]
            an = data["analytics"]
            vids = data["videos"]
            # Buduj uproszczony raport z bazy
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            lines = [
                f"# YouTube — {ch.get('title', 'N/A')} (z bazy danych)",
                f"Ostatni sync: {ch.get('fetched_at', 'N/A')} | Dane lokalne\n",
                "## Kanał",
                "| Metryka | Wartość |", "|---------|---------|",
                f"| Subskrybenci | **{_fmt(ch.get('subscribers', 0))}** |",
                f"| Łączne wyświetlenia | {_fmt(ch.get('total_views', 0))} |",
                f"| Liczba filmów | {ch.get('video_count', 0)} |", "",
            ]
            if an:
                lines += [
                    f"## Analytics (okres: {an.get('period_start')} → {an.get('period_end')})",
                    "| Metryka | Wartość |", "|---------|---------|",
                    f"| Wyświetlenia | **{_fmt(an.get('views', 0))}** |",
                    f"| Watch time | {_fmt(an.get('watch_time_min', 0))} min |",
                    f"| Avg view duration | {_fmt_duration_sec(an.get('avg_view_dur_sec', 0))} |",
                    f"| Nowi subskrybenci | +{an.get('subs_gained', 0):,} / -{an.get('subs_lost', 0):,} = **{an.get('subs_gained', 0) - an.get('subs_lost', 0):+,}** |",
                    "",
                ]
            lines += [
                f"## Filmy ({len(vids)} z bazy)",
                "| # | Tytuł | Data | Wyśw. | Avg dur | Likes | Dług. |",
                "|---|-------|------|-------|---------|-------|-------|",
            ]
            for i, v in enumerate(vids, 1):
                title = (v.get("title") or "")[:44] + ("…" if len(v.get("title") or "") > 44 else "")
                url = f"https://youtube.com/watch?v={v['video_id']}"
                avg_dur = _fmt_duration_sec(v.get("avg_view_dur_sec", 0)) if v.get("avg_view_dur_sec") else "—"
                lines.append(f"| {i} | [{title}]({url}) | {v.get('published_at', '')} | {_fmt(v.get('views', 0))} | {avg_dur} | {_fmt(v.get('likes', 0))} | {v.get('duration', '—')} |")
            lines += ["", "---", f"*DOKODU BRAIN — dane z bazy lokalnej | {now}*"]
            print("\n".join(lines))
        conn.close()
        return

    # Tryb online — odpytaj API i zapisz do bazy
    print("🔐 Logowanie do Google...", file=sys.stderr)
    creds = authenticate()

    youtube = build("youtube", "v3", credentials=creds)
    yt_analytics = build("youtubeAnalytics", "v2", credentials=creds)

    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=args.days)).strftime("%Y-%m-%d")

    print("📡 Pobieranie danych kanału...", file=sys.stderr)
    channel = get_channel_info(youtube)

    videos = []
    video_details = {}
    video_analytics_data = {}
    analytics = {}

    if args.mode in ("videos", "all"):
        print(f"🎬 Pobieranie {args.max_videos} ostatnich filmów...", file=sys.stderr)
        videos = get_videos(youtube, channel["uploads_playlist"], max_results=args.max_videos)
        video_ids = [v["video_id"] for v in videos]

        print("📊 Pobieranie szczegółów filmów...", file=sys.stderr)
        video_details = get_video_details(youtube, video_ids)

        print("📈 Pobieranie analytics per film...", file=sys.stderr)
        video_analytics_data = get_video_analytics(
            yt_analytics, channel["channel_id"], video_ids, start_date, end_date
        )

    if args.mode in ("stats", "all"):
        print("📉 Pobieranie analytics kanału...", file=sys.stderr)
        analytics = get_channel_analytics(yt_analytics, channel["channel_id"], start_date, end_date)

    # Zawsze zapisuj do bazy
    db_save(conn, channel, videos, video_details, analytics, video_analytics_data, start_date, end_date)
    conn.close()

    if args.json:
        output = {
            "channel": channel,
            "period": {"start": start_date, "end": end_date, "days": args.days},
            "analytics": analytics,
            "videos": [
                {**v, **video_details.get(v["video_id"], {}),
                 "analytics": video_analytics_data.get(v["video_id"], {})}
                for v in videos
            ],
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    report = build_markdown_report(
        channel, analytics, videos, video_details, video_analytics_data, start_date, end_date
    )
    print(report)

    if args.save:
        save_to_brain(report, channel)


if __name__ == "__main__":
    main()
