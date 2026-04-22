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
SITE      = "https://dokodu.it"


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
        CREATE TABLE IF NOT EXISTS blog_external_links (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            from_slug   TEXT NOT NULL,
            target_url  TEXT NOT NULL,
            anchor_text TEXT,
            UNIQUE(from_slug, target_url)
        );
    """)
    # Additive schema migrations (SQLite doesn't support IF NOT EXISTS on ADD COLUMN;
    # fall back to checking the existing column list and ignoring duplicates).
    existing = {row[1] for row in conn.execute("PRAGMA table_info(blog_articles)")}
    for col, ddl in [
        ("is_pillar",      "ALTER TABLE blog_articles ADD COLUMN is_pillar INTEGER DEFAULT 0"),
        ("category_name",  "ALTER TABLE blog_articles ADD COLUMN category_name TEXT"),
        ("tags_csv",       "ALTER TABLE blog_articles ADD COLUMN tags_csv TEXT"),
        ("content_hash",   "ALTER TABLE blog_articles ADD COLUMN content_hash TEXT"),
        ("last_synced_at", "ALTER TABLE blog_articles ADD COLUMN last_synced_at TEXT"),
    ]:
        if col not in existing:
            try:
                conn.execute(ddl)
            except sqlite3.OperationalError:
                pass
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

def _read_api_key():
    key_file = Path.home() / ".config/dokodu/blog_api_key"
    if key_file.exists():
        return key_file.read_text().strip()
    return None


def _fetch_all_posts(api_key, limit=500):
    """Pobiera wszystkie posty z /api/external/posts (jeden request z limit=500)."""
    import urllib.request
    req = urllib.request.Request(
        f"{BLOG_API}/external/posts?status=published&limit={limit}",
        headers={
            "x-api-key": api_key,
            "User-Agent": "Dokodu-Brain-LinkGraph/1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    return data.get("posts", data) if isinstance(data, dict) else data


# Markdown link pattern: [anchor](url)  — also tolerates title attribute: [a](url "title")
_MD_LINK_RE = re.compile(r'\[([^\]\n]+?)\]\(\s*([^\s)]+)(?:\s+"[^"]*")?\s*\)')


def _url_to_slug(url: str) -> str | None:
    """Extract blog slug from an internal URL. Returns None for non-blog URLs."""
    u = url.strip()
    # Strip anchors and query params
    u = u.split("#", 1)[0].split("?", 1)[0]
    # Absolute form
    if u.startswith(SITE):
        u = u[len(SITE):]
    # Must start with /blog/
    if not u.startswith("/blog/"):
        return None
    slug = u[len("/blog/"):].strip("/")
    return slug or None


def _is_internal(url: str) -> bool:
    return url.startswith("/") or url.startswith(SITE)


def parse_markdown_links(content: str):
    """
    Parses markdown content and returns:
      - internal_links: list of (anchor, target_slug) — targets that match known slugs
      - external_links: list of (anchor, target_url)
      - blog_but_unknown: list of (anchor, target_slug)  — /blog/* targets to be verified later
    """
    internals = []
    externals = []
    blog_candidates = []
    for anchor, url in _MD_LINK_RE.findall(content):
        if not _is_internal(url):
            # External https://... or mailto:
            externals.append((anchor.strip(), url.strip()))
            continue
        slug = _url_to_slug(url)
        if slug is None:
            # Internal but not /blog/* — skip (we only care about blog graph here)
            continue
        blog_candidates.append((anchor.strip(), slug))
    return blog_candidates, externals


def sync_full(conn):
    """
    Pełny sync:
    1) Pobiera wszystkie opublikowane posty z API (z contentMarkdown)
    2) Upsertuje metadata do blog_articles (+ is_pillar, category_name, tags_csv, word_count)
    3) Parsuje contentMarkdown i odbudowuje blog_links per-article
    """
    import hashlib

    api_key = os.environ.get("EXTERNAL_API_KEY") or _read_api_key()
    if not api_key:
        print("❌ Brak EXTERNAL_API_KEY (ani ~/.config/dokodu/blog_api_key)", file=sys.stderr)
        return 0, 0, 0

    print("→ Pobieranie postów z /api/external/posts…", file=sys.stderr)
    try:
        posts = _fetch_all_posts(api_key)
    except Exception as e:
        print(f"❌ Błąd fetch: {e}", file=sys.stderr)
        return 0, 0, 0

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_articles = 0
    total_articles = 0

    # Pass 1: upsert all articles (so we have full slug → title map before linking)
    for post in posts:
        slug = post.get("slug")
        title = post.get("title")
        if not slug or not title:
            continue
        total_articles += 1

        content = post.get("contentMarkdown") or ""
        word_count = len(content.split()) if content else None
        chash = hashlib.md5(content.encode("utf-8")).hexdigest() if content else None

        category = ""
        if isinstance(post.get("category"), dict):
            category = post["category"].get("name", "") or ""
        elif isinstance(post.get("postCategory"), dict):
            category = post["postCategory"].get("name", "") or ""

        folder = ""
        if isinstance(post.get("folderStructure"), dict):
            folder = post["folderStructure"].get("name", "") or ""
        pillar = category or folder

        tags = post.get("tags") or []
        tag_names = []
        for t in tags:
            if isinstance(t, dict):
                inner = t.get("tag") if isinstance(t.get("tag"), dict) else t
                if isinstance(inner, dict) and inner.get("name"):
                    tag_names.append(inner["name"])
                elif t.get("name"):
                    tag_names.append(t["name"])
            elif isinstance(t, str):
                tag_names.append(t)
        tags_csv = ",".join(tag_names)

        url = f"/blog/{slug}"
        published_at = post.get("publishedAt") or ""
        is_pillar = 1 if post.get("isPillarPage") else 0

        existed = article_exists(conn, slug)
        add_article(
            conn, slug, title, keyword="",
            pillar=pillar, url=url,
            summary=post.get("excerpt") or "",
            status=post.get("status") or "published",
            word_count=word_count,
        )
        conn.execute("""
            UPDATE blog_articles
            SET is_pillar = ?, category_name = ?, tags_csv = ?,
                content_hash = ?, published_at = ?, last_synced_at = ?
            WHERE slug = ?
        """, (is_pillar, category, tags_csv, chash, published_at, now, slug))
        if not existed:
            new_articles += 1

    conn.commit()

    # Pass 2: rebuild link graph from markdown content.
    # Clear existing auto-parsed links and re-populate (we don't want stale links).
    known_slugs = {row[0] for row in conn.execute("SELECT slug FROM blog_articles")}

    conn.execute("DELETE FROM blog_links")
    conn.execute("DELETE FROM blog_external_links")

    total_links = 0
    broken_links = 0
    for post in posts:
        from_slug = post.get("slug")
        content = post.get("contentMarkdown") or ""
        if not from_slug or not content:
            continue

        candidates, externals = parse_markdown_links(content)

        for anchor, to_slug in candidates:
            if to_slug == from_slug:
                continue  # self-link
            # Try exact match first; then progressive suffix (e.g. "n8n/cennik" vs "cennik")
            resolved = to_slug if to_slug in known_slugs else None
            if not resolved:
                # Try tail match (some links use last-path-segment style)
                tail = to_slug.rstrip("/").split("/")[-1]
                if tail in known_slugs:
                    resolved = tail
            if resolved:
                try:
                    conn.execute("""
                        INSERT OR IGNORE INTO blog_links (from_slug, to_slug, anchor_text)
                        VALUES (?, ?, ?)
                    """, (from_slug, resolved, anchor[:200]))
                    total_links += 1
                except sqlite3.IntegrityError:
                    pass
            else:
                broken_links += 1
                # Still record as external target for audit purposes
                conn.execute("""
                    INSERT OR IGNORE INTO blog_external_links (from_slug, target_url, anchor_text)
                    VALUES (?, ?, ?)
                """, (from_slug, f"/blog/{to_slug}", anchor[:200]))

        for anchor, ext_url in externals:
            conn.execute("""
                INSERT OR IGNORE INTO blog_external_links (from_slug, target_url, anchor_text)
                VALUES (?, ?, ?)
            """, (from_slug, ext_url[:500], anchor[:200]))

    conn.commit()

    print(f"✅ Sync: {total_articles} postów ({new_articles} nowych)", file=sys.stderr)
    print(f"✅ Linki: {total_links} internal, {broken_links} broken /blog/* (target nieistnieje)", file=sys.stderr)

    return total_articles, new_articles, total_links


def sync_from_api(conn):
    """Compat wrapper — teraz deleguje do sync_full."""
    total, new, _ = sync_full(conn)
    return new


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


# ── GSC integration ──────────────────────────────────────────────────────────

def get_gsc_stats_for_slug(conn, slug, period_days=90):
    """Aggregated clicks/impressions/CTR/position from gsc_pages for a blog slug."""
    pattern = f"%/blog/{slug}%"
    row = conn.execute("""
        SELECT SUM(clicks), SUM(impressions), AVG(ctr), AVG(position)
        FROM gsc_pages
        WHERE page LIKE ?
          AND period_start >= date('now', ?)
    """, (pattern, f'-{period_days} days')).fetchone()
    if not row or row[1] is None:
        return None
    return {
        'clicks': int(row[0] or 0),
        'impressions': int(row[1] or 0),
        'ctr': float(row[2] or 0),
        'position': float(row[3] or 0),
    }


# ── Recommend ─────────────────────────────────────────────────────────────────

def _split_tags(csv):
    return {t.strip().lower() for t in (csv or "").split(",") if t.strip()}


def recommend_inbound_links(conn, target_slug, limit=8):
    """
    For a target post, find posts that SHOULD link to it but currently don't.
    Ranked by (tag_overlap, same_category, pillar_bonus).
    Returns list of dicts with rationale.
    """
    target = conn.execute("""
        SELECT slug, title, pillar, category_name, tags_csv, is_pillar
        FROM blog_articles WHERE slug = ?
    """, (target_slug,)).fetchone()
    if not target:
        return []

    t_slug, t_title, t_pillar, t_category, t_tags_csv, t_is_pillar = target
    t_tags = _split_tags(t_tags_csv)
    t_title_words = set(re.findall(r'\w+', (t_title or "").lower()))

    # Posts already linking to target — skip them
    already = {row[0] for row in conn.execute(
        "SELECT from_slug FROM blog_links WHERE to_slug = ?", (t_slug,)
    )}

    candidates = conn.execute("""
        SELECT slug, title, pillar, category_name, tags_csv, is_pillar, word_count
        FROM blog_articles
        WHERE status = 'published' AND slug != ?
    """, (t_slug,)).fetchall()

    scored = []
    for c_slug, c_title, c_pillar, c_category, c_tags_csv, c_is_pillar, c_word_count in candidates:
        if c_slug in already:
            continue
        c_tags = _split_tags(c_tags_csv)

        tag_overlap = len(t_tags & c_tags)
        same_cat = 1 if (t_category and c_category == t_category) else 0
        same_pillar = 1 if (t_pillar and c_pillar == t_pillar) else 0
        title_overlap = len(t_title_words & set(re.findall(r'\w+', (c_title or "").lower())))

        # Score: tags worth most, then category, then pillar, then title overlap
        score = tag_overlap * 3 + same_cat * 2 + same_pillar * 1 + min(title_overlap, 4)
        if score <= 0:
            continue

        # Extra weight if the candidate is long-form (more likely to have a natural link slot)
        if c_word_count and c_word_count > 800:
            score += 1

        reasons = []
        if tag_overlap:
            reasons.append(f"{tag_overlap} wspólnych tagów")
        if same_cat:
            reasons.append(f"ta sama kategoria ({c_category})")
        if same_pillar and not same_cat:
            reasons.append(f"ten sam pillar ({c_pillar})")
        if title_overlap:
            reasons.append(f"{title_overlap} wspólnych słów w tytule")

        scored.append({
            "slug": c_slug,
            "title": c_title,
            "score": score,
            "word_count": c_word_count,
            "reason": "; ".join(reasons),
        })

    scored.sort(key=lambda x: -x["score"])
    return scored[:limit]


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


# ── Batch recommendations for quick wins ─────────────────────────────────────

def _quick_win_slugs(conn, period_days=90, min_impressions=500, max_incoming=1):
    """Returns list of (slug, title, url, impressions, incoming) for posts
    meeting the quick-win criteria."""
    rows = conn.execute("""
        SELECT a.slug, a.title, a.url,
               (SELECT COUNT(*) FROM blog_links WHERE to_slug = a.slug) AS inc
        FROM blog_articles a
        WHERE a.status = 'published'
    """).fetchall()
    result = []
    for slug, title, url, inc in rows:
        if inc > max_incoming:
            continue
        gsc = get_gsc_stats_for_slug(conn, slug, period_days)
        if gsc and gsc["impressions"] >= min_impressions:
            result.append((slug, title, url, gsc["impressions"], gsc["clicks"], inc))
    result.sort(key=lambda r: -r[3])
    return result


def build_batch_recommendations(conn, period_days=90):
    """
    Dla wszystkich quick wins generuje listę postów które powinny je linkować,
    plus konkretne sugestie anchor text.
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    quick_wins = _quick_win_slugs(conn, period_days)

    lines = [
        f"# Link Graph Recommendations — dokodu.it",
        f"Wygenerowano: {now} | Zakres GSC: ostatnie {period_days} dni",
        "",
        f"Rekomendacje dla **{len(quick_wins)} quick winów** (posty z ≥500 impressions ale ≤1 incoming link).",
        "",
        "Każda sekcja zawiera top 5-8 postów które **powinny linkować** do tego quick wina.",
        "Dodaj link w treści tych postów z kontekstem (nie forced), używając sugerowanego anchor text.",
        "",
        "---",
        "",
    ]

    for i, (slug, title, url, impr, clicks, inc) in enumerate(quick_wins, 1):
        recs = recommend_inbound_links(conn, slug, limit=8)
        target = conn.execute(
            "SELECT tags_csv, category_name, pillar FROM blog_articles WHERE slug = ?",
            (slug,)
        ).fetchone()
        tags_csv, cat, pillar = target or ("", "", "")
        t_tags = _split_tags(tags_csv)
        # Use first tag as suggested anchor fallback
        suggested_anchor = title[:50]
        if t_tags:
            # Pick the most meaningful tag (skip generic ones)
            for tag in sorted(t_tags, key=len, reverse=True):
                if len(tag) > 3 and tag.lower() not in {"ai", "it", "co", "jak", "dla"}:
                    suggested_anchor = tag
                    break

        lines.append(f"## {i}. {title}")
        lines.append(f"**URL:** `{url}` · **GSC:** {impr:,} impr / {clicks:,} clicks · **Incoming:** {inc}")
        if pillar or cat:
            lines.append(f"**Pillar/kategoria:** {pillar or cat}")
        lines.append(f'**Sugerowany anchor:** *„{suggested_anchor}"*')
        lines.append("")

        if not recs:
            lines.append("_Brak kandydatów w DB — sprawdź czy są posty o podobnych tagach._")
            lines.append("")
            continue

        lines.append("| Score | Z tego posta | Powód |")
        lines.append("|-------|--------------|-------|")
        for r in recs:
            lines.append(
                f"| {r['score']} | [{r['title'][:60]}](/blog/{r['slug']}) | {r['reason']} |"
            )
        lines.append("")
        lines.append("---")
        lines.append("")

    lines += [
        "## Jak stosować",
        "",
        '1. Wejdź w admina bloga dla każdego posta z kolumny „Z tego posta"',
        "2. Znajdź naturalne miejsce w treści (np. paragraph o temacie związanym z targetem)",
        "3. Dodaj Markdown link: `[sugerowany anchor](/blog/<target-slug>)`",
        "4. Variuj anchor text — nie używaj tego samego 5 razy na tej samej stronie",
        "5. Regeneruj raport: `python3 scripts/link_graph.py --sync-full && --analyze`",
        "",
        "## Priorytet wykonania",
        "",
        "- **Tier 1 (top 5)** — najwyższy GSC traffic, zrób w tym tygodniu",
        "- **Tier 2 (6-15)** — w tym miesiącu",
        "- **Tier 3 (reszta)** — jak będzie czas",
        "",
        f"*Recommendations | {now}*",
    ]
    return "\n".join(lines)


# ── Broken links checker ─────────────────────────────────────────────────────

def check_broken_links(conn, timeout=8):
    """
    Dla każdego broken internal link (/blog/* target nie w DB) wykonuje HTTP HEAD
    żeby sklasyfikować: 404 (totally missing), 200 (actually exists — slug mismatch bug),
    301/302 (redirected). Returns grouped report.
    """
    import urllib.request
    import urllib.error

    broken = conn.execute("""
        SELECT DISTINCT target_url, COUNT(*) as refs
        FROM blog_external_links
        WHERE target_url LIKE '/blog/%'
        GROUP BY target_url
        ORDER BY refs DESC
    """).fetchall()

    results = []
    for target_url, refs in broken:
        full_url = f"{SITE}{target_url}"
        # Count referring posts for context
        refs_list = [r[0] for r in conn.execute(
            "SELECT from_slug FROM blog_external_links WHERE target_url = ? LIMIT 10",
            (target_url,)
        ).fetchall()]

        status = None
        final_url = None
        error = None
        try:
            req = urllib.request.Request(
                full_url, method="HEAD",
                headers={"User-Agent": "Dokodu-Brain-LinkGraph/1.0"}
            )
            with urllib.request.urlopen(req, timeout=timeout) as r:
                status = r.status
                final_url = r.url
        except urllib.error.HTTPError as e:
            status = e.code
        except Exception as e:
            error = str(e)[:60]

        results.append({
            "target_url": target_url,
            "refs_count": refs,
            "refs_from": refs_list,
            "status": status,
            "final_url": final_url,
            "error": error,
        })
    return results


def build_broken_report(conn):
    """Markdown report of broken internal links with classification."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    print("→ Sprawdzam HTTP status każdego broken target…", file=sys.stderr)
    results = check_broken_links(conn)

    # Classify
    real_404 = [r for r in results if r["status"] == 404]
    actually_ok = [r for r in results if r["status"] == 200]
    redirects = [r for r in results if r["status"] in (301, 302, 307, 308)]
    errors = [r for r in results if r["error"] or (r["status"] and r["status"] >= 500)]

    lines = [
        f"# Broken Internal Links — dokodu.it",
        f"Wygenerowano: {now}",
        "",
        f"Łącznie unikalnych broken targets: **{len(results)}**",
        f"- 🚫 Prawdziwe 404: **{len(real_404)}** (trzeba naprawić lub usunąć linki)",
        f"- 🟢 Actually 200 OK: **{len(actually_ok)}** (slug w DB out of sync, samo się naprawi po sync-full)",
        f"- ↪️ Redirecty 3xx: **{len(redirects)}** (działają, ale update linków byłby lepszy)",
        f"- ⚠️ Errors: **{len(errors)}**",
        "",
        "---",
        "",
    ]

    if real_404:
        lines += [
            "## 🚫 Prawdziwe 404 — DO NAPRAWY",
            "",
            "Linki w treści postów wskazujące na nieistniejące URLe. **3 opcje:**",
            "1. **Usunąć link** z treści linkujących postów (jeśli content był kiedyś, teraz nie ma)",
            "2. **Opublikować target** (jeśli to draft który był planowany)",
            "3. **Podmienić na inny post** (jeśli content przeniesiony/rebranded)",
            "",
            "| Target | Refs | Z tych postów |",
            "|--------|------|---------------|",
        ]
        for r in real_404:
            refs_str = ", ".join(f"`{s}`" for s in r["refs_from"][:5])
            if r["refs_count"] > 5:
                refs_str += f" *+{r['refs_count'] - 5}*"
            lines.append(f"| `{r['target_url']}` | {r['refs_count']} | {refs_str} |")
        lines.append("")

    if actually_ok:
        lines += [
            "## 🟢 Actually OK (200) — Slug Mismatch w DB",
            "",
            "Target URL zwraca 200 — czyli strona istnieje. Nasz `blog_articles` DB nie ma tego sluga",
            "(prawdopodobnie inna struktura folderów). Najbliższy sync-full powinien to wyłapać.",
            "",
            "| Target | Refs |",
            "|--------|------|",
        ]
        for r in actually_ok:
            lines.append(f"| `{r['target_url']}` | {r['refs_count']} |")
        lines.append("")

    if redirects:
        lines += [
            "## ↪️ Redirecty",
            "",
            "Target redirectuje. Działa, ale update do final URL usuwa extra hop (lepszy UX + SEO).",
            "",
            "| From | → Do (final) | Refs |",
            "|------|-------------|------|",
        ]
        for r in redirects:
            final = r["final_url"] or "?"
            lines.append(f"| `{r['target_url']}` | `{final}` | {r['refs_count']} |")
        lines.append("")

    if errors:
        lines += [
            "## ⚠️ Errors / Timeouts",
            "",
            "| Target | Error |",
            "|--------|-------|",
        ]
        for r in errors:
            lines.append(f"| `{r['target_url']}` | {r['error'] or r['status']} |")
        lines.append("")

    lines += [
        "---",
        f"*Broken Links Report | {now}*",
    ]
    return "\n".join(lines)


# ── Content gaps (new articles to write) ─────────────────────────────────────

def _existing_urls_covering(conn, query, period_days=90):
    """Return list of (page, impressions, position) where this GSC query appears."""
    rows = conn.execute("""
        SELECT page, SUM(impressions), AVG(position)
        FROM gsc_query_page
        WHERE query = ?
          AND period_start >= date('now', ?)
        GROUP BY page
        ORDER BY SUM(impressions) DESC
    """, (query, f'-{period_days} days')).fetchall()
    return [(r[0], int(r[1] or 0), float(r[2] or 0)) for r in rows]


def find_keyword_demand_gaps(conn, period_days=90, min_impressions=500, min_avg_position=10):
    """
    GSC queries with high impressions but poor average position, indicating
    no existing page is ranking well. Candidates for new dedicated posts.
    """
    rows = conn.execute("""
        SELECT query, SUM(impressions) AS total_impr, AVG(position) AS avg_pos,
               SUM(clicks) AS total_clicks
        FROM gsc_queries
        WHERE period_start >= date('now', ?)
        GROUP BY query
        HAVING total_impr >= ? AND avg_pos > ?
        ORDER BY total_impr DESC
        LIMIT 40
    """, (f'-{period_days} days', min_impressions, min_avg_position)).fetchall()

    gaps = []
    for query, impr, pos, clicks in rows:
        # Check what pages Google picked for this query (if any)
        pages = _existing_urls_covering(conn, query, period_days)
        # If top page position > 10 → no page is ranking well = real gap
        top_page_pos = pages[0][2] if pages else 999
        if top_page_pos <= 8:
            continue  # Some existing page ranks OK-ish, not a gap
        gaps.append({
            "query": query,
            "impressions": int(impr),
            "clicks": int(clicks or 0),
            "avg_position": float(pos),
            "top_existing_page": pages[0][0] if pages else None,
            "top_existing_pos": top_page_pos,
        })
    return gaps


def find_tag_pillars_missing(conn, min_posts_per_tag=5):
    """
    Tags used by many posts but WITHOUT a pillar post covering the topic.
    Identifies clusters waiting for an introductory hub article.
    """
    # Aggregate tags from tags_csv
    tag_posts = {}
    tag_slugs = {}  # tag → list of (slug, is_pillar, title, word_count)
    rows = conn.execute("""
        SELECT slug, title, tags_csv, is_pillar, word_count
        FROM blog_articles
        WHERE status = 'published' AND tags_csv IS NOT NULL AND tags_csv != ''
    """).fetchall()
    for slug, title, tags_csv, is_pillar, wc in rows:
        for tag in _split_tags(tags_csv):
            tag_posts.setdefault(tag, 0)
            tag_posts[tag] += 1
            tag_slugs.setdefault(tag, []).append((slug, bool(is_pillar), title, wc or 0))

    missing = []
    for tag, count in tag_posts.items():
        if count < min_posts_per_tag:
            continue
        posts = tag_slugs[tag]
        has_pillar = any(is_pillar for (_, is_pillar, _, _) in posts)
        # Also consider a "de facto pillar": long (>2000 words) post with the tag word in the URL
        has_defacto_pillar = any(
            wc > 2000 and tag.lower() in slug.lower()
            for (slug, _, _, wc) in posts
        )
        if has_pillar or has_defacto_pillar:
            continue
        missing.append({
            "tag": tag,
            "post_count": count,
            "sample_slugs": [s for (s, _, _, _) in posts[:5]],
        })
    missing.sort(key=lambda m: -m["post_count"])
    return missing


def build_content_gaps_report(conn, period_days=90):
    """
    Consolidated "what to write next" report pulling three signals:
      A. Planned drafts — /blog/* targets referenced in content but returning 404
      B. Keyword demand gaps — high-impression GSC queries with no well-ranking page
      C. Tag clusters missing a pillar — many posts share a tag, no hub exists
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Section A: reuse broken link classification
    print("→ A. Checking broken link targets (HTTP HEAD)…", file=sys.stderr)
    broken = check_broken_links(conn)
    real_404 = [r for r in broken if r["status"] == 404]
    # Enrich with anchor texts for outline hints
    for r in real_404:
        anchors = [row[0] for row in conn.execute(
            "SELECT DISTINCT anchor_text FROM blog_external_links WHERE target_url = ? LIMIT 5",
            (r["target_url"],)
        ).fetchall() if row[0]]
        r["anchors"] = anchors

    # Section B: GSC demand
    print("→ B. Analyzing GSC keyword demand…", file=sys.stderr)
    keyword_gaps = find_keyword_demand_gaps(conn, period_days)

    # Section C: tag-based pillar gaps
    print("→ C. Detecting tag clusters without pillar…", file=sys.stderr)
    tag_gaps = find_tag_pillars_missing(conn)

    lines = [
        f"# Content Gaps — dokodu.it",
        f"Wygenerowano: {now} | Zakres GSC: ostatnie {period_days} dni",
        "",
        "## Podsumowanie",
        "",
        f"- **A. Planowane drafty** (linki 404 w treści postów): **{len(real_404)}**",
        f"- **B. Keyword demand gaps** (GSC impr ≥500, brak dobrego targetu): **{len(keyword_gaps)}**",
        f"- **C. Tagi bez pillara** (≥5 postów, brak huba): **{len(tag_gaps)}**",
        "",
        "---",
        "",
        "## A. Planowane drafty",
        "",
        "Linki `/blog/*` w treści istniejących postów wskazujące na **nieistniejące URL**.",
        "Hub post już zrobił kontekst i anchor text — wystarczy napisać content. Najszybsza droga.",
        "",
    ]

    if not real_404:
        lines.append("_Brak._")
    else:
        lines.append("| Sugerowany URL | Z huba | Anchor z treści (hint na outline) |")
        lines.append("|----------------|--------|-----------------------------------|")
        for r in real_404:
            refs = ", ".join(f"`{s}`" for s in r["refs_from"][:3])
            if r["refs_count"] > 3:
                refs += f" *+{r['refs_count'] - 3}*"
            anchors = "; ".join(a[:60] for a in (r.get("anchors") or []))
            lines.append(f"| `{r['target_url']}` | {refs} | {anchors or '—'} |")

    lines += [
        "",
        "---",
        "",
        "## B. Keyword demand gaps (z GSC)",
        "",
        "Frazy z wysokim impressions (≥500) i średnią pozycją > 10 — "
        "Google pokazuje strony, ale żadna nie rankuje dobrze (top page pos > 8).",
        "Dedykowany post na tę frazę zazwyczaj szybko zabiera ruch.",
        "",
    ]

    if not keyword_gaps:
        lines.append(
            "_Brak danych lub wszystkie frazy mają już dobrze rankujące URLe. "
            "Uruchom `python3 scripts/gsc_fetch.py --days 90 --save` żeby odświeżyć._"
        )
    else:
        lines.append("| Query | Impr | Clicks | Pozycja | Obecny top URL |")
        lines.append("|-------|------|--------|---------|-----------------|")
        for g in keyword_gaps:
            top_pg = g["top_existing_page"] or "—"
            # Trim to just path
            if top_pg.startswith("https://"):
                top_pg = top_pg.replace("https://dokodu.it", "")
            lines.append(
                f"| {g['query']} | {g['impressions']:,} | {g['clicks']} | "
                f"{g['avg_position']:.1f} | `{top_pg[:50]}` |"
            )

    lines += [
        "",
        "---",
        "",
        "## C. Tagi bez pillara",
        "",
        "Tagi używane przez ≥5 postów, ale bez dedicated pillar post (oznaczenie `isPillarPage=true`) "
        "i bez długiego (>2000 słów) posta zawierającego tag w URL.",
        '**Akcja:** napisać pillar post typu „<tag> — kompletny przewodnik" '
        "który linkuje do wszystkich postów z tym tagiem.",
        "",
    ]

    if not tag_gaps:
        lines.append("_Brak — każdy rozbudowany klaster ma już pillara._")
    else:
        lines.append("| Tag | Postów | Przykładowe slugi |")
        lines.append("|-----|--------|--------------------|")
        for t in tag_gaps[:25]:
            sample = ", ".join(f"`{s}`" for s in t["sample_slugs"][:3])
            lines.append(f"| **{t['tag']}** | {t['post_count']} | {sample} |")

    lines += [
        "",
        "---",
        "",
        "## Priorytet wykonania",
        "",
        "1. **A. Planowane drafty** — zacznij tu (outline już istnieje, masz anchor z hub post)",
        "2. **B. Keyword demand** — top 5 po impressions — wysokie ROI",
        "3. **C. Tagi bez pillara** — strategiczne (pillar redefiniuje cluster na dłużej)",
        "",
        f"*Content Gaps | {now}*",
    ]
    return "\n".join(lines)


# ── Analyze (rich report) ────────────────────────────────────────────────────

def build_analyze_report(conn, period_days=90):
    """
    Full analytical report that cross-references the link graph with GSC data.
    Saved to OUT_FILE as Markdown. Focus on actionable insights, not just stats.
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    total_articles = conn.execute(
        "SELECT COUNT(*) FROM blog_articles WHERE status = 'published'"
    ).fetchone()[0]

    total_links = conn.execute("SELECT COUNT(*) FROM blog_links").fetchone()[0]

    # Top 10 hub posts (highest incoming)
    hubs = conn.execute("""
        SELECT a.slug, a.title, a.url, a.is_pillar,
               (SELECT COUNT(*) FROM blog_links WHERE to_slug = a.slug) as inc,
               (SELECT COUNT(*) FROM blog_links WHERE from_slug = a.slug) as out
        FROM blog_articles a
        WHERE a.status = 'published'
        ORDER BY inc DESC, out DESC
        LIMIT 10
    """).fetchall()

    # Orphans with GSC enrichment
    orphans_raw = conn.execute("""
        SELECT a.slug, a.title, a.url, a.pillar, a.category_name, a.is_pillar, a.word_count
        FROM blog_articles a
        WHERE a.status = 'published'
          AND NOT EXISTS (SELECT 1 FROM blog_links WHERE to_slug = a.slug)
    """).fetchall()

    orphans = []
    for slug, title, url, pillar, cat, is_pillar, wc in orphans_raw:
        gsc = get_gsc_stats_for_slug(conn, slug, period_days)
        orphans.append({
            "slug": slug, "title": title, "url": url,
            "pillar": pillar or cat or "",
            "is_pillar": bool(is_pillar),
            "word_count": wc or 0,
            "gsc": gsc,
        })
    # Sort by GSC impressions desc, then word_count desc
    orphans.sort(key=lambda o: (-(o["gsc"]["impressions"] if o["gsc"] else 0), -o["word_count"]))

    # Dead-ends
    dead_ends = conn.execute("""
        SELECT a.slug, a.title, a.url, a.word_count
        FROM blog_articles a
        WHERE a.status = 'published'
          AND NOT EXISTS (SELECT 1 FROM blog_links WHERE from_slug = a.slug)
        ORDER BY a.word_count DESC
        LIMIT 30
    """).fetchall()

    # Quick wins: >=500 impressions AND incoming <= 1
    quick_wins = []
    all_pub = conn.execute("""
        SELECT a.slug, a.title, a.url,
               (SELECT COUNT(*) FROM blog_links WHERE to_slug = a.slug) as inc
        FROM blog_articles a
        WHERE a.status = 'published'
    """).fetchall()
    for slug, title, url, inc in all_pub:
        gsc = get_gsc_stats_for_slug(conn, slug, period_days)
        if gsc and gsc["impressions"] >= 500 and inc <= 1:
            quick_wins.append({
                "slug": slug, "title": title, "url": url,
                "incoming": inc, "gsc": gsc,
            })
    quick_wins.sort(key=lambda q: -q["gsc"]["impressions"])
    quick_wins = quick_wins[:20]

    # Broken internal /blog/* links
    broken = conn.execute("""
        SELECT from_slug, target_url, anchor_text
        FROM blog_external_links
        WHERE target_url LIKE '/blog/%'
        ORDER BY from_slug
    """).fetchall()

    # Per-category summary
    cat_stats = conn.execute("""
        SELECT COALESCE(NULLIF(category_name,''), NULLIF(pillar,''), '(brak)') as cat,
               COUNT(*) as posts,
               SUM(CASE WHEN is_pillar = 1 THEN 1 ELSE 0 END) as pillars
        FROM blog_articles
        WHERE status = 'published'
        GROUP BY cat
        ORDER BY posts DESC
    """).fetchall()

    # Mermaid for top 25 most-linked posts (hubs) showing their inbound edges
    top_slugs = [row[0] for row in hubs[:15]]
    mermaid_edges = []
    if top_slugs:
        rows = conn.execute(f"""
            SELECT from_slug, to_slug FROM blog_links
            WHERE to_slug IN ({",".join("?" * len(top_slugs))})
            LIMIT 100
        """, top_slugs).fetchall()
        for f, t in rows:
            mermaid_edges.append((f, t))

    lines = [
        f"# Blog Link Graph — dokodu.it",
        f"Wygenerowano: {now} | Zakres GSC: ostatnie {period_days} dni",
        "",
        "## Podsumowanie",
        "",
        f"- Opublikowanych postów: **{total_articles}**",
        f"- Internal linki (markdown): **{total_links}**",
        f"- Średnia linków wychodzących/post: **{total_links / max(1, total_articles):.1f}**",
        f"- Sieroty (0 incoming): **{len(orphans)}**",
        f"- Dead-ends (0 outgoing): **{len(dead_ends)}**",
        f"- Broken internal /blog/* links: **{len(broken)}**",
        f"- Quick wins (GSC impr ≥ 500 ∧ incoming ≤ 1): **{len(quick_wins)}**",
        "",
        "## Hub Posts (Top 10 by Incoming Links)",
        "",
        "Posty które naturalnie pełnią rolę pillarów — dużo innych postów na nie linkuje.",
        "",
        "| # | Post | Pillar? | In | Out |",
        "|---|------|---------|----|----|",
    ]
    for i, (slug, title, url, is_pillar, inc, out) in enumerate(hubs, 1):
        pill = "⭐" if is_pillar else ""
        lines.append(f"| {i} | [{title[:60]}]({url}) | {pill} | {inc} | {out} |")

    lines += [
        "",
        "## 🎯 Quick Wins — Orphan Hits z Traffic",
        "",
        "Posty z impressions ≥ 500 (GSC) ALE ≤ 1 incoming link. Dodanie linków daje najszybszy lift.",
        "",
        "| Post | Impr | Clicks | Pos | In |",
        "|------|------|--------|-----|----|",
    ]
    if not quick_wins:
        lines.append("| — | — | — | — | — |")
        lines.append("")
        lines.append("*Brak quick winów — możliwe że nie masz jeszcze pobranych danych GSC (`/seo-sync`) lub wszystkie high-traffic posty są już dobrze podlinkowane.*")
    else:
        for q in quick_wins:
            g = q["gsc"]
            lines.append(
                f"| [{q['title'][:55]}]({q['url']}) | {g['impressions']} | "
                f"{g['clicks']} | {g['position']:.1f} | {q['incoming']} |"
            )

    lines += [
        "",
        "## ⚠️ Sieroty (0 incoming)",
        f"Łącznie: **{len(orphans)}**. Top 30 posortowane po GSC impressions:",
        "",
        "| Post | Pillar | Słów | Impr |",
        "|------|--------|------|------|",
    ]
    for o in orphans[:30]:
        impr = o["gsc"]["impressions"] if o["gsc"] else 0
        pill_badge = "⭐ " if o["is_pillar"] else ""
        lines.append(
            f"| {pill_badge}[{(o['title'] or o['slug'])[:55]}]({o['url']}) | {o['pillar'][:20]} "
            f"| {o['word_count']} | {impr} |"
        )

    lines += [
        "",
        "## 🚫 Dead-ends (0 outgoing)",
        "Posty które nie wysyłają link juice dalej. Top 15:",
        "",
        "| Post | Słów |",
        "|------|------|",
    ]
    for slug, title, url, wc in dead_ends[:15]:
        lines.append(f"| [{(title or slug)[:60]}]({url}) | {wc or 0} |")

    lines += [
        "",
        "## 🔗 Broken Internal Links",
        "Linki `/blog/*` w treści postów wskazujące na **nieistniejące sluge**.",
        "",
    ]
    if broken:
        lines.append("| Z posta | Anchor | Target (404?) |")
        lines.append("|---------|--------|---------------|")
        for f, t, a in broken[:50]:
            lines.append(f"| `{f}` | {(a or '')[:40]} | `{t}` |")
        if len(broken) > 50:
            lines.append(f"| … | | *(+{len(broken) - 50} więcej)* |")
    else:
        lines.append("Brak — wszystkie internal links wskazują na istniejące posty ✅")

    lines += [
        "",
        "## 📊 Struktura per kategoria",
        "",
        "| Kategoria | Posty | Pillar |",
        "|-----------|-------|--------|",
    ]
    for cat, posts, pills in cat_stats:
        lines.append(f"| {cat} | {posts} | {pills or 0} |")

    if mermaid_edges:
        lines += [
            "",
            "## 🕸️ Graf Top Hubs (Mermaid)",
            "",
            "```mermaid",
            "graph LR",
        ]
        # Safe ID mapping (mermaid id must be alnum)
        def mmid(s): return re.sub(r'[^a-z0-9]+', '_', s.lower())[:40]
        nodes_seen = set()
        for f, t in mermaid_edges:
            fid, tid = mmid(f), mmid(t)
            if fid not in nodes_seen:
                lines.append(f'    {fid}["{f[:30]}"]')
                nodes_seen.add(fid)
            if tid not in nodes_seen:
                lines.append(f'    {tid}["{t[:30]}"]:::hub')
                nodes_seen.add(tid)
            lines.append(f"    {fid} --> {tid}")
        lines.append("    classDef hub fill:#fde2e4,stroke:#e63946,color:#0F2137;")
        lines.append("```")

    lines += [
        "",
        "---",
        "## Jak używać",
        "",
        "- `python3 scripts/link_graph.py --sync-full` — odśwież dane (co tydzień / po publikacji)",
        "- `python3 scripts/link_graph.py --analyze` — regeneruj ten raport",
        "- `python3 scripts/link_graph.py --recommend <slug>` — znajdź posty które powinny linkować do X",
        "- `python3 scripts/link_graph.py --orphans` — lista sierot",
        "",
        f"*Link_Graph | {now}*",
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

        elif cmd_name == "sync-full":
            total, new, links = sync_full(conn)
            print(f"✅ Sync-full: {total} postów ({new} nowych), {links} internal links z markdown")

        elif cmd_name == "analyze":
            # Optional --period N (days); defaults to 90
            period = 90
            for i, a in enumerate(args_rest):
                if a == "--period" and i + 1 < len(args_rest):
                    try:
                        period = int(args_rest[i + 1])
                    except ValueError:
                        pass
            report = build_analyze_report(conn, period_days=period)
            OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
            OUT_FILE.write_text(report, encoding="utf-8")
            # Only print a summary to stdout (full report is in the file)
            for line in report.splitlines()[:30]:
                print(line)
            print(f"\n✅ Pełny raport zapisany: {OUT_FILE}", file=sys.stderr)

        elif cmd_name == "batch-recommend":
            period = 90
            for i, a in enumerate(args_rest):
                if a == "--period" and i + 1 < len(args_rest):
                    try:
                        period = int(args_rest[i + 1])
                    except ValueError:
                        pass
            out_path = OUT_FILE.parent / "Link_Graph_Recommendations.md"
            report = build_batch_recommendations(conn, period_days=period)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(report, encoding="utf-8")
            # Preview top sections
            for line in report.splitlines()[:25]:
                print(line)
            print(f"\n✅ Zapisano: {out_path}", file=sys.stderr)

        elif cmd_name == "content-gaps":
            period = 90
            for i, a in enumerate(args_rest):
                if a == "--period" and i + 1 < len(args_rest):
                    try:
                        period = int(args_rest[i + 1])
                    except ValueError:
                        pass
            out_path = OUT_FILE.parent / "Link_Graph_Content_Gaps.md"
            report = build_content_gaps_report(conn, period_days=period)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(report, encoding="utf-8")
            for line in report.splitlines()[:25]:
                print(line)
            print(f"\n✅ Zapisano: {out_path}", file=sys.stderr)

        elif cmd_name == "check-broken":
            out_path = OUT_FILE.parent / "Link_Graph_Broken.md"
            report = build_broken_report(conn)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(report, encoding="utf-8")
            for line in report.splitlines()[:20]:
                print(line)
            print(f"\n✅ Zapisano: {out_path}", file=sys.stderr)

        elif cmd_name == "recommend":
            target_slug = args_rest[0] if args_rest and not args_rest[0].startswith("--") else ""
            if not target_slug:
                print("Podaj slug: python3 link_graph.py --recommend n8n-co-to-jest")
                sys.exit(1)
            recs = recommend_inbound_links(conn, target_slug)
            target = conn.execute(
                "SELECT title, url FROM blog_articles WHERE slug = ?", (target_slug,)
            ).fetchone()
            if not target:
                print(f"❌ Nie znaleziono posta: {target_slug}")
                sys.exit(1)
            t_title, t_url = target
            print(f"\n🎯 Posty które POWINNY linkować do: {t_title}")
            print(f"   URL: {t_url}\n")
            if not recs:
                print("   (brak kandydatów — wszystkie topicalnie bliskie posty już linkują)")
            for r in recs:
                print(f"  [{r['score']:2d}] {r['title'][:70]}")
                print(f"       /blog/{r['slug']}  ·  {r['reason']}")
                print()

        else:
            parser.print_help()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
