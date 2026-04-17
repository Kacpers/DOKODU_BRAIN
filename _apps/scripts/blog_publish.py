#!/usr/bin/env python3
"""
DOKODU BRAIN — Blog Publishing Client
Autor: Kacper Sieradzinski | Dokodu sp. z o.o.

Zarządza postami na dokodu.it/blog/ przez zewnętrzne API.
Integruje się z seo_ideas.py — tworzy drafty bezpośrednio z ideas bank.

Użycie:
  python3 blog_publish.py get --slug n8n-automatyzacja
  python3 blog_publish.py get --id clxxx...
  python3 blog_publish.py list [--status draft|published] [--limit 20]
  python3 blog_publish.py create --title "..." --slug "..." --content "..."
  python3 blog_publish.py create --from-idea 5 --content-file /tmp/post.md
  python3 blog_publish.py update --id clxxx... --content "..." [--status published]
  python3 blog_publish.py publish --id clxxx...
  python3 blog_publish.py delete --id clxxx...   (uwaga: nieodwracalne)
"""

import os
import sys
import json
import sqlite3
import argparse
from datetime import datetime, timezone
from pathlib import Path

try:
    import urllib.request
    import urllib.parse
    import urllib.error
except ImportError:
    pass  # stdlib, zawsze dostępne

CONFIG_DIR   = Path.home() / ".config" / "dokodu"
API_KEY_FILE = CONFIG_DIR / "blog_api_key"
DB_FILE      = CONFIG_DIR / "gsc_data.db"

SITE_URL_PROD = "https://dokodu.it"
SITE_URL_DEV  = "http://localhost:3001"


# ══════════════════════════════════════════════
# CONFIG / AUTH
# ══════════════════════════════════════════════

def get_api_key() -> str:
    """Odczytuje klucz API z pliku lub zmiennej środowiskowej."""
    # 1. Zmienna środowiskowa (priorytet)
    key = os.environ.get("EXTERNAL_API_KEY", "").strip()
    if key:
        return key
    # 2. Plik konfiguracyjny
    if API_KEY_FILE.exists():
        key = API_KEY_FILE.read_text(encoding="utf-8").strip()
        if key:
            return key
    print(f"\n❌ BRAK KLUCZA API!", file=sys.stderr)
    print(f"Ustaw go na jeden z dwóch sposobów:\n", file=sys.stderr)
    print(f"  1. Plik: echo 'twoj_klucz' > {API_KEY_FILE}", file=sys.stderr)
    print(f"  2. Env:  export EXTERNAL_API_KEY=twoj_klucz", file=sys.stderr)
    print(f"\nKlucz znajdziesz w .env bloga jako EXTERNAL_API_KEY.", file=sys.stderr)
    sys.exit(1)


def get_site_url(dev: bool = False) -> str:
    url = os.environ.get("BLOG_SITE_URL", "").strip()
    if url:
        return url.rstrip("/")
    return SITE_URL_DEV if dev else SITE_URL_PROD


# ══════════════════════════════════════════════
# HTTP CLIENT (stdlib only)
# ══════════════════════════════════════════════

def _request(method: str, url: str, api_key: str,
             body: dict | None = None) -> dict:
    data = json.dumps(body).encode("utf-8") if body else None
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (compatible; DokodoBrain/1.0; +https://dokodu.it)",
    }
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8")
        try:
            err = json.loads(raw)
        except Exception:
            err = {"error": raw}
        code = e.code
        if code == 401:
            print(f"❌ 401 Unauthorized — sprawdź EXTERNAL_API_KEY", file=sys.stderr)
        elif code == 404:
            print(f"❌ 404 Not Found — {url}", file=sys.stderr)
        elif code == 409:
            print(f"❌ 409 Conflict — slug już istnieje", file=sys.stderr)
        elif code == 400:
            print(f"❌ 400 Bad Request — {err}", file=sys.stderr)
        else:
            print(f"❌ HTTP {code} — {err}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"❌ Błąd połączenia: {e.reason}", file=sys.stderr)
        print(f"   Sprawdź czy serwer jest dostępny: {url}", file=sys.stderr)
        sys.exit(1)


# ══════════════════════════════════════════════
# API CALLS
# ══════════════════════════════════════════════

def api_list(site_url: str, api_key: str, status: str | None,
             limit: int, offset: int) -> dict:
    params = {"limit": limit, "offset": offset}
    if status:
        params["status"] = status
    qs = urllib.parse.urlencode(params)
    return _request("GET", f"{site_url}/api/external/posts?{qs}", api_key)


def api_get_by_slug(site_url: str, api_key: str, slug: str) -> dict | None:
    try:
        result = _request("GET", f"{site_url}/api/external/posts?slug={urllib.parse.quote(slug)}", api_key)
        return result.get("post")
    except SystemExit:
        # 404 = slug nie istnieje, to normalny stan przy tworzeniu nowego posta
        return None


def api_get_by_id(site_url: str, api_key: str, post_id: str) -> dict:
    result = _request("GET", f"{site_url}/api/external/posts/{post_id}", api_key)
    return result.get("post", result)


def api_create(site_url: str, api_key: str, payload: dict) -> dict:
    return _request("POST", f"{site_url}/api/external/posts", api_key, payload)


def api_update(site_url: str, api_key: str, post_id: str, payload: dict) -> dict:
    return _request("PUT", f"{site_url}/api/external/posts/{post_id}", api_key, payload)


def api_revalidate(site_url: str, api_key: str, slug: str) -> dict:
    """Triggeruje on-demand ISR revalidację dla strony bloga."""
    try:
        return _request("POST", f"{site_url}/api/external/revalidate", api_key, {"slug": slug})
    except SystemExit:
        # Nie przerywaj jeśli revalidacja nie zadziałała (nieblokujące)
        return {}


# ══════════════════════════════════════════════
# IDEAS BANK INTEGRATION
# ══════════════════════════════════════════════

def idea_get(idea_id: int) -> dict | None:
    """Pobiera pomysł z lokalnej bazy seo_ideas."""
    if not DB_FILE.exists():
        return None
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM blog_ideas WHERE id = ?", (idea_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def idea_set_blog_id(idea_id: int, blog_post_id: str) -> None:
    """Zapisuje blog_post_id do wiersza w ideas bank."""
    if not DB_FILE.exists():
        return
    conn = sqlite3.connect(DB_FILE)
    # Dodaj kolumnę jeśli nie istnieje (migracja)
    try:
        conn.execute("ALTER TABLE blog_ideas ADD COLUMN blog_post_id TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        pass  # Kolumna już istnieje
    conn.execute(
        "UPDATE blog_ideas SET blog_post_id = ?, updated_at = ? WHERE id = ?",
        (blog_post_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), idea_id)
    )
    conn.commit()
    conn.close()


def idea_update_status(idea_id: int, status: str) -> None:
    if not DB_FILE.exists():
        return
    conn = sqlite3.connect(DB_FILE)
    try:
        conn.execute("ALTER TABLE blog_ideas ADD COLUMN blog_post_id TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        pass
    conn.execute(
        "UPDATE blog_ideas SET status = ?, updated_at = ? WHERE id = ?",
        (status, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), idea_id)
    )
    conn.commit()
    conn.close()


# ══════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════

def _print_post(post: dict) -> None:
    if not post:
        print("(brak danych)")
        return
    tags = ", ".join(post.get("tags") or []) or "—"
    print(f"""
┌────────────────────────────────────────────────────────────
│ ID:      {post.get('id', '—')}
│ Slug:    {post.get('slug', '—')}
│ Tytuł:   {post.get('title', '—')}
│ Status:  {post.get('status', '—')}  |  Type: {post.get('postType', '—')}  |  Pillar: {post.get('isPillarPage', False)}
│ Author:  {post.get('author', '—')}  |  Category: {post.get('category', '—')}
│ Tags:    {tags}
│ Excerpt: {(post.get('excerpt') or '—')[:80]}
│ Created: {post.get('createdAt', '—')[:19] if post.get('createdAt') else '—'}
│ Updated: {post.get('updatedAt', '—')[:19] if post.get('updatedAt') else '—'}
│ Published: {post.get('publishedAt') or '—'}
└────────────────────────────────────────────────────────────""")
    md = post.get("contentMarkdown") or post.get("content") or ""
    if md:
        preview = md[:300].replace("\n", " ")
        print(f"  Preview: {preview}{'…' if len(md) > 300 else ''}\n")


def _fmt_status(s: str) -> str:
    return {"draft": "📝 draft", "published": "✅ live"}.get(s, s)


# ══════════════════════════════════════════════
# COMMANDS
# ══════════════════════════════════════════════

def cmd_list(args, site_url, api_key):
    result = api_list(site_url, api_key, args.status, args.limit, args.offset)
    posts  = result.get("posts", [])
    total  = result.get("total", len(posts))

    if not posts:
        print("Brak postów.")
        return

    print(f"\n{'ID':26}  {'Status':10}  {'Slug':35}  Tytuł")
    print("─" * 110)
    for p in posts:
        pid    = (p.get("id") or "—")[:24]
        status = _fmt_status(p.get("status") or "")
        slug   = (p.get("slug") or "—")[:35]
        title  = (p.get("title") or "")[:40]
        print(f"{pid:26}  {status:10}  {slug:35}  {title}")
    print(f"\nŁącznie: {total} | Wyświetlono: {len(posts)}")


def cmd_get(args, site_url, api_key):
    if args.id:
        post = api_get_by_id(site_url, api_key, args.id)
    elif args.slug:
        post = api_get_by_slug(site_url, api_key, args.slug)
        if not post:
            print(f"Post o slugu '{args.slug}' nie istnieje.")
            sys.exit(0)
    else:
        print("Podaj --id lub --slug")
        sys.exit(1)
    _print_post(post)
    if args.json:
        print(json.dumps(post, ensure_ascii=False, indent=2))


def cmd_create(args, site_url, api_key):
    payload: dict = {}

    # --- Źródło danych: ideas bank ---
    idea_id = None
    if args.from_idea:
        idea_id = args.from_idea
        idea = idea_get(idea_id)
        if not idea:
            print(f"❌ Nie znaleziono pomysłu #{idea_id} w ideas bank.", file=sys.stderr)
            sys.exit(1)
        # Wypełnij payload z ideas bank (args mają priorytet)
        payload = {
            "title":      idea.get("title") or "",
            "slug":       idea.get("slug") or "",
            "excerpt":    idea.get("meta_description") or "",
            "metaTitle":  idea.get("meta_title") or idea.get("title") or "",
            "category":   idea.get("pillar") or "",
            "tags":       [t.strip() for t in (idea.get("secondary_keywords") or "").split(",") if t.strip()],
            "author":     "Kacper",
            "status":     "draft",
            "postType":   "BLOG",
            "isPillarPage": False,
        }
        if idea.get("target_keyword"):
            kw = idea["target_keyword"]
            if kw not in payload["tags"]:
                payload["tags"].insert(0, kw)

    # --- Override z argumentów CLI ---
    if args.title:        payload["title"]       = args.title
    if args.slug:         payload["slug"]        = args.slug
    if args.excerpt:      payload["excerpt"]     = args.excerpt
    if args.meta_title:   payload["metaTitle"]   = args.meta_title
    if args.author:       payload["author"]      = args.author
    if args.category:     payload["category"]    = args.category
    if args.tags:         payload["tags"]        = [t.strip() for t in args.tags.split(",")]
    if args.status:       payload["status"]      = args.status
    if args.post_type:    payload["postType"]    = args.post_type
    if args.pillar_page:  payload["isPillarPage"] = True
    if args.published_at: payload["publishedAt"] = args.published_at

    # --- Treść ---
    content = ""
    if args.content_file:
        p = Path(args.content_file)
        if not p.exists():
            print(f"❌ Plik nie istnieje: {args.content_file}", file=sys.stderr)
            sys.exit(1)
        content = p.read_text(encoding="utf-8")
    elif args.content:
        content = args.content

    if not content:
        print("❌ Brak treści. Podaj --content 'tekst' lub --content-file plik.md", file=sys.stderr)
        sys.exit(1)

    payload["content"] = content

    # Walidacja
    if not payload.get("title"):
        print("❌ Brak tytułu (--title lub --from-idea)", file=sys.stderr)
        sys.exit(1)
    if not payload.get("slug"):
        print("❌ Brak slugu (--slug lub ustaw w ideas bank)", file=sys.stderr)
        sys.exit(1)

    # Sprawdź czy slug już istnieje
    print(f"🔍 Sprawdzam czy slug '{payload['slug']}' istnieje...", file=sys.stderr)
    existing = api_get_by_slug(site_url, api_key, payload["slug"])
    if existing:
        print(f"⚠️  Post o slugu '{payload['slug']}' już istnieje (id: {existing['id']}).")
        print(f"   Użyj: python3 blog_publish.py update --id {existing['id']} --content-file <plik>")
        sys.exit(1)

    print(f"📤 Tworzę draft: '{payload['title']}'...", file=sys.stderr)
    result = api_create(site_url, api_key, payload)

    if result.get("success"):
        post_id = result["post"]["id"]
        print(f"✅ Utworzono draft!")
        print(f"   ID:   {post_id}")
        print(f"   Slug: {result['post']['slug']}")
        if not args.dev:
            print(f"   URL:  {SITE_URL_PROD}/blog/{result['post']['slug']}")

        # Zapisz blog_post_id do ideas bank
        if idea_id:
            idea_set_blog_id(idea_id, post_id)
            idea_update_status(idea_id, "PISANIE")
            print(f"   💾 Zaktualizowano ideas bank #{idea_id} → blog_post_id={post_id}, status=PISANIE")
    else:
        print(f"❌ Błąd: {result}", file=sys.stderr)
        sys.exit(1)


def cmd_update(args, site_url, api_key):
    payload: dict = {}
    if args.title:        payload["title"]       = args.title
    if args.slug:         payload["slug"]        = args.slug
    if args.excerpt:      payload["excerpt"]     = args.excerpt
    if args.meta_title:   payload["metaTitle"]   = args.meta_title
    if args.author:       payload["author"]      = args.author
    if args.category:     payload["category"]    = args.category
    if args.tags:         payload["tags"]        = [t.strip() for t in args.tags.split(",")]
    if args.status:       payload["status"]      = args.status
    if args.published_at: payload["publishedAt"] = args.published_at

    content = ""
    if args.content_file:
        p = Path(args.content_file)
        if not p.exists():
            print(f"❌ Plik nie istnieje: {args.content_file}", file=sys.stderr)
            sys.exit(1)
        content = p.read_text(encoding="utf-8")
    elif args.content:
        content = args.content

    if content:
        payload["content"] = content

    if not payload:
        print("❌ Brak zmian do wysłania. Podaj przynajmniej jeden parametr.", file=sys.stderr)
        sys.exit(1)

    print(f"📝 Aktualizuję post {args.id}...", file=sys.stderr)
    result = api_update(site_url, api_key, args.id, payload)

    if result.get("success"):
        slug = result['post']['slug']
        print(f"✅ Zaktualizowano!")
        print(f"   ID:   {result['post']['id']}")
        print(f"   Slug: {slug}")

        # On-demand revalidacja ISR
        rev = api_revalidate(site_url, api_key, slug)
        if rev.get("success"):
            print(f"   🔄 Revalidacja: {rev.get('revalidated', [])}")

        # Aktualizuj ideas bank jeśli podano
        if args.idea_id and payload.get("status") == "published":
            idea_update_status(args.idea_id, "OPUBLIKOWANY")
            print(f"   💾 Zaktualizowano ideas bank #{args.idea_id} → OPUBLIKOWANY")
    else:
        print(f"❌ Błąd: {result}", file=sys.stderr)
        sys.exit(1)


def _parse_faq_from_markdown(content: str) -> tuple[list[dict], str, str]:
    """
    Wyciąga sekcję FAQ z contentMarkdown.
    Zwraca (faqs, faq_section_text, remaining_content).
    faqs = [{"question": ..., "answer": ...}, ...]
    Jeśli brak FAQ → zwraca ([], "", content).
    """
    import re

    faq_pattern = re.compile(r'\n## FAQ[^\n]*\n(.*?)(?=\n## |\Z)', re.DOTALL)
    faq_match = faq_pattern.search(content)
    if not faq_match:
        return [], "", content

    faq_section = faq_match.group(0)
    faq_body = faq_match.group(1)
    faqs = []

    # Styl 1: ### Pytanie\nOdpowiedź
    qa_blocks = re.split(r'\n### ', '\n' + faq_body)
    for block in qa_blocks:
        block = block.strip()
        if not block:
            continue
        lines = block.split('\n', 1)
        question = lines[0].strip().strip('#').strip()
        answer = lines[1].strip() if len(lines) > 1 else ''
        if question and answer:
            faqs.append({"question": question, "answer": answer})

    # Styl 2: **Pytanie**\nOdpowiedź (fallback)
    if not faqs:
        qa_blocks2 = re.split(r'\n\*\*', '\n' + faq_body)
        for block in qa_blocks2:
            block = block.strip()
            if not block:
                continue
            end_bold = block.find('**')
            if end_bold == -1:
                continue
            question = block[:end_bold].strip()
            answer = block[end_bold + 2:].strip()
            if question and answer:
                faqs.append({"question": question, "answer": answer})

    new_content = content.replace(faq_section, '').rstrip() + '\n'
    return faqs, faq_section, new_content


def _extract_and_push_faq(post_id: str, site_url: str, api_key: str,
                           verbose: bool = True) -> int:
    """
    Pobiera post, wyciąga FAQ z markdown, wgrywa do DB i czyści contentMarkdown.
    Zwraca liczbę wgranych pytań (0 = brak FAQ lub błąd).
    """
    data = _request("GET", f"{site_url}/api/external/posts/{post_id}", api_key)
    post = data.get("post") or data
    content = post.get("contentMarkdown", "")

    faqs, _section, new_content = _parse_faq_from_markdown(content)

    if not faqs:
        if verbose:
            print(f"   ℹ  Brak sekcji FAQ w treści — pomijam", file=sys.stderr)
        return 0

    if verbose:
        print(f"   📋 FAQ: {len(faqs)} pytań → wgrywam do bazy...", file=sys.stderr)

    result = _request("PUT", f"{site_url}/api/external/posts/{post_id}/faqs",
                      api_key, {"faqs": faqs})
    if not result.get("success"):
        if verbose:
            print(f"   ⚠  Błąd wgrywania FAQ: {result}", file=sys.stderr)
        return 0

    # Usuń sekcję FAQ z contentMarkdown
    _request("PUT", f"{site_url}/api/external/posts/{post_id}",
              api_key, {"content": new_content})

    if verbose:
        for i, f in enumerate(faqs, 1):
            print(f"   {i}. {f['question'][:80]}")
        print(f"   ✅ FAQ wgrane, sekcja usunięta z treści")

    return len(faqs)


def cmd_faq(args, site_url, api_key):
    """Zarządza FAQ dla posta."""
    faq_url = f"{site_url}/api/external/posts/{args.id}/faqs"

    if args.faq_action == "get":
        faqs = _request("GET", faq_url, api_key)
        if isinstance(faqs, list):
            print(f"FAQ dla posta {args.id} ({len(faqs)} pytań):")
            for i, f in enumerate(faqs, 1):
                print(f"\n  {i}. {f['question']}")
                print(f"     {f['answer'][:120]}...")
        else:
            print(faqs)

    elif args.faq_action == "extract":
        count = _extract_and_push_faq(args.id, site_url, api_key, verbose=True)
        if count == 0 and not args.keep:
            print("⚠  Nie wgrano żadnych FAQ.", file=sys.stderr)

    elif args.faq_action == "delete":
        result = _request("DELETE", faq_url, api_key)
        print(f"✅ Usunięto FAQ: {result}")


def cmd_publish(args, site_url, api_key):
    # Auto-extract FAQ from contentMarkdown before publishing
    print(f"🔍 Sprawdzam FAQ w treści...", file=sys.stderr)
    _extract_and_push_faq(args.id, site_url, api_key, verbose=True)

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    payload = {"status": "published", "publishedAt": now_iso}

    print(f"🚀 Publikuję post {args.id}...", file=sys.stderr)
    result = api_update(site_url, api_key, args.id, payload)

    if result.get("success"):
        slug = result['post']['slug']
        print(f"✅ Opublikowano!")
        print(f"   ID:   {result['post']['id']}")
        print(f"   Slug: {slug}")
        if not args.dev:
            print(f"   URL:  {SITE_URL_PROD}/blog/{slug}")
        # On-demand revalidacja ISR
        rev = api_revalidate(site_url, api_key, slug)
        if rev.get("success"):
            print(f"   🔄 Revalidacja: {rev.get('revalidated', [])}")

        if args.idea_id:
            idea_update_status(args.idea_id, "OPUBLIKOWANY")
            print(f"   💾 Zaktualizowano ideas bank #{args.idea_id} → OPUBLIKOWANY")
    else:
        print(f"❌ Błąd: {result}", file=sys.stderr)
        sys.exit(1)


# ══════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="DOKODU BRAIN — Blog Publishing Client")
    parser.add_argument("--dev", action="store_true", help="Użyj localhost:3001 zamiast produkcji")

    sub = parser.add_subparsers(dest="cmd", required=True)

    # LIST
    p_list = sub.add_parser("list", help="Lista postów")
    p_list.add_argument("--status", choices=["draft", "published"], default=None)
    p_list.add_argument("--limit",  type=int, default=20)
    p_list.add_argument("--offset", type=int, default=0)

    # GET
    p_get = sub.add_parser("get", help="Pobierz post")
    p_get.add_argument("--id",   default=None, help="Database ID posta")
    p_get.add_argument("--slug", default=None, help="Slug posta")
    p_get.add_argument("--json", action="store_true", help="Wyjście JSON")

    # CREATE
    p_create = sub.add_parser("create", help="Utwórz nowy draft")
    p_create.add_argument("--title",         default=None)
    p_create.add_argument("--slug",          default=None)
    p_create.add_argument("--content",       default=None, help="Treść Markdown inline")
    p_create.add_argument("--content-file",  default=None, dest="content_file",
                          help="Plik .md z treścią posta")
    p_create.add_argument("--from-idea",     default=None, dest="from_idea", type=int,
                          help="ID pomysłu z seo_ideas (auto-wypełnia metadane)")
    p_create.add_argument("--excerpt",       default=None)
    p_create.add_argument("--meta-title",    default=None, dest="meta_title")
    p_create.add_argument("--author",        default="Kacper")
    p_create.add_argument("--category",      default=None)
    p_create.add_argument("--tags",          default=None, help="Tagi csv: 'tag1,tag2'")
    p_create.add_argument("--status",        choices=["draft", "published"], default="draft")
    p_create.add_argument("--post-type",     choices=["BLOG", "FEED"], default="BLOG",
                          dest="post_type")
    p_create.add_argument("--pillar-page",   action="store_true", dest="pillar_page")
    p_create.add_argument("--published-at",  default=None, dest="published_at")

    # UPDATE
    p_update = sub.add_parser("update", help="Aktualizuj post")
    p_update.add_argument("--id",           required=True)
    p_update.add_argument("--title",        default=None)
    p_update.add_argument("--slug",         default=None)
    p_update.add_argument("--content",      default=None)
    p_update.add_argument("--content-file", default=None, dest="content_file")
    p_update.add_argument("--excerpt",      default=None)
    p_update.add_argument("--meta-title",   default=None, dest="meta_title")
    p_update.add_argument("--author",       default=None)
    p_update.add_argument("--category",     default=None)
    p_update.add_argument("--tags",         default=None)
    p_update.add_argument("--status",       choices=["draft", "published"], default=None)
    p_update.add_argument("--published-at", default=None, dest="published_at")
    p_update.add_argument("--idea-id",      default=None, dest="idea_id", type=int,
                          help="ID w ideas bank do synchronizacji statusu")

    # FAQ
    p_faq = sub.add_parser("faq", help="Zarządzaj FAQ posta")
    p_faq.add_argument("--id",      required=True, help="ID posta")
    p_faq.add_argument("faq_action", choices=["get", "extract", "delete"],
                       help="get=pokaż, extract=wyciągnij z markdown i wgraj do DB, delete=usuń wszystkie")
    p_faq.add_argument("--keep", action="store_true",
                       help="Przy extract: zostaw sekcję FAQ w contentMarkdown (nie usuwaj)")

    # PUBLISH
    p_pub = sub.add_parser("publish", help="Opublikuj draft (status=published)")
    p_pub.add_argument("--id",      required=True)
    p_pub.add_argument("--idea-id", default=None, dest="idea_id", type=int,
                       help="ID w ideas bank do synchronizacji statusu")

    args = parser.parse_args()
    api_key  = get_api_key()
    site_url = get_site_url(args.dev)

    cmds = {
        "list":    cmd_list,
        "get":     cmd_get,
        "create":  cmd_create,
        "update":  cmd_update,
        "publish": cmd_publish,
        "faq":     cmd_faq,
    }
    cmds[args.cmd](args, site_url, api_key)


if __name__ == "__main__":
    main()
