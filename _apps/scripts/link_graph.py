#!/usr/bin/env python3
"""
DOKODU BRAIN — Blog Link Graph
Śledzi artykuły, linki między nimi i podpowiada co linkować.

Użycie:
  python3 link_graph.py --init          # inicjalizuj bazę ze znanych artykułów
  python3 link_graph.py --list          # lista wszystkich artykułów
  python3 link_graph.py --suggest "cursor pro cena"    # co linkować w nowym artykule
  python3 link_graph.py --orphans       # artykuły bez linków przychodzących
  python3 link_graph.py --report        # pełny raport Markdown
  python3 link_graph.py --add-article --slug "n8n-co-to" --title "N8N — Co To Jest" \
      --keyword "n8n co to jest" --pillar "n8n Automatyzacja" --url "/blog/n8n/co-to-jest"
  python3 link_graph.py --add-link --from-slug "cursor-pro-cena" \
      --to-slug "cursor-pro-studenci" --anchor "program studencki Cursor Pro"
  python3 link_graph.py --sync          # zsynchronizuj z blog API (wymaga EXTERNAL_API_KEY)
"""

import argparse
import json
import os
import re
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

DB_FILE   = Path.home() / ".config/dokodu/gsc_data.db"
OUT_FILE  = Path(__file__).parent.parent / "20_AREAS/AREA_Blog_SEO/Link_Graph.md"
BLOG_API  = "https://dokodu.it/api"


# ── DB ───────────────────────────────────────────────────────────────────────

def db_connect():
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(str(DB_FILE))


def db_init(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS blog_articles (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            slug        TEXT UNIQUE NOT NULL,
            url         TEXT,
            title       TEXT NOT NULL,
            keyword     TEXT,
            pillar      TEXT,
            summary     TEXT,
            status      TEXT DEFAULT 'published',
            published_at TEXT,
            word_count  INTEGER,
            added_at    TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS blog_links (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            from_slug   TEXT NOT NULL,
            to_slug     TEXT NOT NULL,
            anchor_text TEXT,
            context     TEXT,
            added_at    TEXT DEFAULT (datetime('now')),
            UNIQUE(from_slug, to_slug)
        );
    """)
    conn.commit()


def article_exists(conn, slug):
    return conn.execute(
        "SELECT id FROM blog_articles WHERE slug = ?", (slug,)
    ).fetchone() is not None


def add_article(conn, slug, title, keyword="", pillar="", url="", summary="", status="published", word_count=None):
    url = url or f"/blog/{slug}"
    try:
        conn.execute("""
            INSERT INTO blog_articles (slug, url, title, keyword, pillar, summary, status, word_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (slug, url, title, keyword, pillar, summary, status, word_count))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        conn.execute("""
            UPDATE blog_articles
            SET title=?, keyword=?, pillar=?, url=?, summary=?, status=?
            WHERE slug=?
        """, (title, keyword, pillar, url, summary, status, slug))
        conn.commit()
        return False


def add_link(conn, from_slug, to_slug, anchor_text="", context=""):
    try:
        conn.execute("""
            INSERT INTO blog_links (from_slug, to_slug, anchor_text, context)
            VALUES (?, ?, ?, ?)
        """, (from_slug, to_slug, anchor_text, context))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def get_all_articles(conn):
    return conn.execute("""
        SELECT slug, url, title, keyword, pillar, status, word_count, added_at
        FROM blog_articles
        ORDER BY added_at DESC
    """).fetchall()


def get_links_for(conn, slug):
    outgoing = conn.execute("""
        SELECT b.slug, b.url, b.title, l.anchor_text
        FROM blog_links l
        JOIN blog_articles b ON b.slug = l.to_slug
        WHERE l.from_slug = ?
    """, (slug,)).fetchall()
    incoming = conn.execute("""
        SELECT b.slug, b.url, b.title, l.anchor_text
        FROM blog_links l
        JOIN blog_articles b ON b.slug = l.from_slug
        WHERE l.to_slug = ?
    """, (slug,)).fetchall()
    return outgoing, incoming


def get_orphans(conn):
    """Artykuły które nie mają żadnych linków przychodzących."""
    return conn.execute("""
        SELECT a.slug, a.title, a.pillar
        FROM blog_articles a
        WHERE a.slug NOT IN (SELECT to_slug FROM blog_links)
        AND a.status = 'published'
        ORDER BY a.pillar, a.title
    """).fetchall()


# ── Suggest ──────────────────────────────────────────────────────────────────

def suggest_links(conn, topic: str, current_slug: str = "", limit: int = 8):
    """
    Na podstawie tematu sugeruje artykuły do wewnętrznego linkowania.
    Używa dopasowania po słowach kluczowych i pillarach.
    """
    topic_words = set(re.findall(r'\w+', topic.lower()))
    articles = get_all_articles(conn)

    scored = []
    for row in articles:
        slug, url, title, keyword, pillar, status, word_count, added_at = row
        if slug == current_slug:
            continue

        # Sprawdź czy link już istnieje
        if current_slug:
            exists = conn.execute(
                "SELECT id FROM blog_links WHERE from_slug=? AND to_slug=?",
                (current_slug, slug)
            ).fetchone()
            if exists:
                continue

        candidate_text = f"{title} {keyword or ''} {pillar or ''}".lower()
        candidate_words = set(re.findall(r'\w+', candidate_text))

        overlap = len(topic_words & candidate_words)
        if overlap > 0:
            scored.append((overlap, slug, url, title, keyword, pillar))

    scored.sort(reverse=True)
    return scored[:limit]


# ── Sync z API ───────────────────────────────────────────────────────────────

def sync_from_api(conn):
    """Pobiera artykuły z blog API i dodaje/aktualizuje w bazie."""
    try:
        import urllib.request
        api_key = os.environ.get("EXTERNAL_API_KEY") or _read_api_key()
        if not api_key:
            print("❌ Brak EXTERNAL_API_KEY — nie mogę pobrać z API", file=sys.stderr)
            return 0

        req = urllib.request.Request(
            f"{BLOG_API}/posts?status=all&limit=100",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())

        posts = data.get("posts", data) if isinstance(data, dict) else data
        count = 0
        for post in posts:
            slug = post.get("slug", "")
            title = post.get("title", "")
            if not slug or not title:
                continue
            url = post.get("url", f"/blog/{slug}")
            status = post.get("status", "published")
            word_count = post.get("word_count")
            is_new = add_article(conn, slug, title, url=url, status=status, word_count=word_count)
            if is_new:
                count += 1

        return count
    except Exception as e:
        print(f"❌ Błąd sync z API: {e}", file=sys.stderr)
        return 0


def _read_api_key():
    key_file = Path.home() / ".config/dokodu/blog_api_key"
    if key_file.exists():
        return key_file.read_text().strip()
    return None


# ── Init z znanych artykułów ─────────────────────────────────────────────────

KNOWN_ARTICLES = [
    # slug, title, keyword, pillar, url
    ("n8n-co-to-jest", "N8N — Co To Jest i Do Czego Służy?", "n8n co to jest", "n8n Automatyzacja", "/blog/n8n/co-to-jest"),
    ("n8n-cennik", "N8N — Cennik i Plany (2025)", "n8n cennik", "n8n Automatyzacja", "/blog/n8n/cennik"),
    ("n8n-licencja", "N8N Licencja — Community vs Cloud vs Enterprise", "n8n licencja", "n8n Automatyzacja", "/blog/n8n/licencja-cennik"),
    ("n8n-docker", "N8N na Docker — Instalacja Krok po Kroku", "n8n docker", "n8n Automatyzacja", "/blog/n8n/docker"),
    ("n8n-automatyzacje", "Automatyzacje N8N — Najlepsze Przykłady", "automatyzacje n8n", "n8n Automatyzacja", "/blog/n8n/automatyzacje"),
    ("cursor-ai", "Cursor AI — Recenzja Edytora Kodu z AI", "cursor ai", "AI Tools", "/blog/cursor/cursor-ai"),
    ("cursor-pro", "Cursor Pro — Czy Warto? Recenzja 2025", "cursor pro", "AI Tools", "/blog/cursor/cursor-pro"),
    ("perplexity-vs-chatgpt", "Perplexity vs ChatGPT — Które AI Wybrać?", "perplexity vs chatgpt", "AI Tools", "/blog/ai/perplexity-vs-chatgpt"),
    ("union-vs-union-all", "UNION vs UNION ALL w SQL — Różnice i Przykłady", "union vs union all", "SQL", "/blog/sql/union-vs-union-all"),
    ("docker-podstawy", "Docker — Podstawy dla Programistów", "docker podstawy", "DevOps", "/blog/docker/podstawy"),
    # Planowane (BRIEF)
    ("openclaw-vs-n8n", "OpenClaw vs N8N — Agenty AI czy Automatyzacje?", "openclaw vs n8n", "n8n Automatyzacja", "/blog/n8n/openclaw-vs-n8n"),
    ("n8n-open-source-vs-enterprise", "N8N Open Source vs Enterprise — Który Plan Wybrać?", "n8n open source vs enterprise", "n8n Automatyzacja", "/blog/n8n/open-source-vs-enterprise"),
    ("cursor-pro-cena-plany", "Cursor Pro — Cena i Limity 2025", "cursor pro cena", "AI Tools", "/blog/cursor/cursor-pro-cena-plany"),
    ("cursor-pro-studenci", "Cursor Pro dla Studentów — Jak Aktywować w Polsce", "cursor pro for students", "AI Tools", "/blog/cursor/cursor-pro-studenci"),
]

KNOWN_LINKS = [
    # (from_slug, to_slug, anchor_text)
    # n8n klaster wewnętrzny
    ("n8n-co-to-jest",    "n8n-cennik",       "ile kosztuje n8n"),
    ("n8n-co-to-jest",    "n8n-docker",       "n8n na docker"),
    ("n8n-co-to-jest",    "n8n-automatyzacje","przykłady automatyzacji n8n"),
    ("n8n-cennik",        "n8n-licencja",     "n8n licencja community vs enterprise"),
    ("n8n-licencja",      "n8n-cennik",       "ceny planów n8n"),
    ("n8n-docker",        "n8n-co-to-jest",   "co to jest n8n"),
    ("n8n-automatyzacje", "n8n-co-to-jest",   "n8n co to jest"),
    ("n8n-automatyzacje", "n8n-docker",       "instalacja n8n na docker"),
    # AI Tools klaster
    ("perplexity-vs-chatgpt", "cursor-ai",    "narzędzia AI dla programistów"),
    ("cursor-ai",             "cursor-pro",   "cursor pro plan"),
    ("cursor-pro",            "cursor-ai",    "Cursor AI edytor"),
    # Planowane linki między nowymi artykułami
    ("cursor-pro-cena-plany",   "cursor-pro-studenci",   "program studencki Cursor Pro"),
    ("cursor-pro-studenci",     "cursor-pro-cena-plany", "pełny cennik Cursor Pro"),
    ("n8n-open-source-vs-enterprise", "n8n-cennik",    "cennik planów n8n"),
    ("n8n-open-source-vs-enterprise", "n8n-licencja",  "n8n SUL licencja"),
    ("openclaw-vs-n8n",  "n8n-co-to-jest",   "co to jest n8n"),
    ("openclaw-vs-n8n",  "n8n-automatyzacje","automatyzacje n8n"),
]


def cmd_init(conn):
    new_articles = 0
    new_links = 0

    for slug, title, keyword, pillar, url in KNOWN_ARTICLES:
        status = "brief" if slug in ("openclaw-vs-n8n", "n8n-open-source-vs-enterprise",
                                      "cursor-pro-cena-plany", "cursor-pro-studenci") else "published"
        is_new = add_article(conn, slug, title, keyword=keyword, pillar=pillar, url=url, status=status)
        if is_new:
            new_articles += 1

    for from_slug, to_slug, anchor in KNOWN_LINKS:
        is_new = add_link(conn, from_slug, to_slug, anchor)
        if is_new:
            new_links += 1

    print(f"✅ Inicjalizacja: {new_articles} nowych artykułów, {new_links} nowych linków")


# ── Report ────────────────────────────────────────────────────────────────────

def build_report(conn):
    articles = get_all_articles(conn)
    orphans = get_orphans(conn)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        f"# Blog Link Graph — dokodu.it",
        f"Wygenerowano: {now_str}",
        "",
        f"Artykuły: **{len(articles)}** | Sieroty (brak linków in): **{len(orphans)}**",
        "",
        "## Mapa Artykułów",
        "",
        "| Slug | Tytuł | Fraza | Pillar | Status | Out | In |",
        "|------|-------|-------|--------|--------|-----|-----|",
    ]

    for row in articles:
        slug, url, title, keyword, pillar, status, word_count, added_at = row
        outgoing, incoming = get_links_for(conn, slug)
        status_icon = {"published": "✅", "brief": "📝", "draft": "🔄"}.get(status, "❓")
        lines.append(
            f"| [{slug}]({url or '#'}) | {title[:45]}... | `{keyword or '-'}` "
            f"| {pillar or '-'} | {status_icon} {status} | {len(outgoing)} | {len(incoming)} |"
        )

    lines += ["", "## Szczegóły Linków", ""]
    for row in articles:
        slug, url, title, keyword, pillar, status, word_count, added_at = row
        outgoing, incoming = get_links_for(conn, slug)
        if not outgoing and not incoming:
            continue
        lines.append(f"### {title}")
        lines.append(f"Slug: `{slug}` | URL: `{url}`")
        lines.append("")
        if outgoing:
            lines.append("**Linki wychodzące (→):**")
            for o_slug, o_url, o_title, anchor in outgoing:
                lines.append(f"  - [{anchor or o_title}]({o_url}) → `{o_slug}`")
        if incoming:
            lines.append("**Linki przychodzące (←):**")
            for i_slug, i_url, i_title, anchor in incoming:
                lines.append(f"  - [{anchor or i_title}]({i_url}) ← `{i_slug}`")
        lines.append("")

    if orphans:
        lines += ["## ⚠️ Artykuły Bez Linków Przychodzących (Sieroty)", ""]
        for slug, title, pillar in orphans:
            lines.append(f"- **{title}** (`{slug}`) — Pillar: {pillar or '-'}")
        lines.append("")

    lines += [
        "---",
        f"*DOKODU BRAIN Link Graph | {now_str}*",
    ]
    return "\n".join(lines)


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="DOKODU BRAIN — Blog Link Graph")
    subparsers = parser.add_subparsers(dest="cmd")

    subparsers.add_parser("--init", help="Inicjalizuj bazę ze znanych artykułów")

    p_add = subparsers.add_parser("--add-article", help="Dodaj artykuł")
    p_add.add_argument("--slug",    required=True)
    p_add.add_argument("--title",   required=True)
    p_add.add_argument("--keyword", default="")
    p_add.add_argument("--pillar",  default="")
    p_add.add_argument("--url",     default="")
    p_add.add_argument("--summary", default="")
    p_add.add_argument("--status",  default="published")

    p_link = subparsers.add_parser("--add-link", help="Dodaj link między artykułami")
    p_link.add_argument("--from-slug", required=True, dest="from_slug")
    p_link.add_argument("--to-slug",   required=True, dest="to_slug")
    p_link.add_argument("--anchor",    default="", dest="anchor")
    p_link.add_argument("--context",   default="")

    p_sug = subparsers.add_parser("--suggest", help="Sugeruj linki dla tematu")
    p_sug.add_argument("topic", nargs="?", default="")
    p_sug.add_argument("--slug", default="")

    subparsers.add_parser("--list",    help="Lista artykułów")
    subparsers.add_parser("--orphans", help="Artykuły bez linków przychodzących")
    subparsers.add_parser("--report",  help="Pełny raport Markdown")
    subparsers.add_parser("--sync",    help="Zsynchronizuj z blog API")

    # Obsługa argumentów z dwoma myślnikami jako pierwszy argument
    if len(sys.argv) > 1 and sys.argv[1].startswith("--"):
        cmd_name = sys.argv[1][2:]
        args_rest = sys.argv[2:]

        conn = db_connect()
        db_init(conn)

        if cmd_name == "init":
            cmd_init(conn)

        elif cmd_name == "list":
            articles = get_all_articles(conn)
            print(f"\n{'Slug':<35} {'Pillar':<20} {'Status':<12} {'Out':<5} {'In'}")
            print("-" * 85)
            for row in articles:
                slug, url, title, keyword, pillar, status, word_count, added_at = row
                out, inc = get_links_for(conn, slug)
                print(f"{slug:<35} {(pillar or '-'):<20} {status:<12} {len(out):<5} {len(inc)}")

        elif cmd_name == "orphans":
            orphans = get_orphans(conn)
            if not orphans:
                print("✅ Brak artykułów bez linków przychodzących")
            else:
                print(f"\n⚠️  Artykuły bez linków przychodzących ({len(orphans)}):\n")
                for slug, title, pillar in orphans:
                    print(f"  • {title} ({slug}) — {pillar or '-'}")

        elif cmd_name == "suggest":
            topic = args_rest[0] if args_rest and not args_rest[0].startswith("--") else ""
            current_slug = ""
            for i, a in enumerate(args_rest):
                if a == "--slug" and i + 1 < len(args_rest):
                    current_slug = args_rest[i + 1]
            if not topic:
                print("Podaj temat: python3 link_graph.py --suggest 'cursor pro'")
                sys.exit(1)
            suggestions = suggest_links(conn, topic, current_slug)
            if not suggestions:
                print("❌ Brak pasujących artykułów")
            else:
                print(f"\n🔗 Sugestie linków dla tematu: '{topic}'\n")
                for score, slug, url, title, keyword, pillar in suggestions:
                    print(f"  [{score:2d} pkt] {title}")
                    print(f"         URL: {url} | Keyword: {keyword}")
                    print()

        elif cmd_name == "add-article":
            import shlex
            # Parse remaining args
            sub = argparse.ArgumentParser()
            sub.add_argument("--slug",    required=True)
            sub.add_argument("--title",   required=True)
            sub.add_argument("--keyword", default="")
            sub.add_argument("--pillar",  default="")
            sub.add_argument("--url",     default="")
            sub.add_argument("--summary", default="")
            sub.add_argument("--status",  default="published")
            a = sub.parse_args(args_rest)
            is_new = add_article(conn, a.slug, a.title, a.keyword, a.pillar, a.url, a.summary, a.status)
            action = "Dodano" if is_new else "Zaktualizowano"
            print(f"✅ {action}: {a.slug}")

        elif cmd_name == "add-link":
            sub = argparse.ArgumentParser()
            sub.add_argument("--from-slug", required=True, dest="from_slug")
            sub.add_argument("--to-slug",   required=True, dest="to_slug")
            sub.add_argument("--anchor",    default="")
            sub.add_argument("--context",   default="")
            a = sub.parse_args(args_rest)
            is_new = add_link(conn, a.from_slug, a.to_slug, a.anchor, a.context)
            if is_new:
                print(f"✅ Dodano link: {a.from_slug} → {a.to_slug}")
            else:
                print(f"ℹ️  Link już istnieje: {a.from_slug} → {a.to_slug}")

        elif cmd_name == "report":
            report = build_report(conn)
            print(report)
            OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
            OUT_FILE.write_text(report, encoding="utf-8")
            print(f"\n✅ Zapisano: {OUT_FILE}", file=sys.stderr)

        elif cmd_name == "sync":
            count = sync_from_api(conn)
            print(f"✅ Zsynchronizowano {count} nowych artykułów z API")

        else:
            parser.print_help()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
