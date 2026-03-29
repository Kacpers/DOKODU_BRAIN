#!/usr/bin/env python3
"""
hn_scout.py — Skanuje HackerNews pod kątem tematów AI/automatyzacja/dev

Pobiera top stories z HackerNews API, filtruje po słowach kluczowych
relevantnych dla Dokodu. Wypisuje Markdown na stdout.

Użycie:
    # Standardowy skan (top 50 stories, filtr AI/automation)
    python3 hn_scout.py

    # Więcej stories
    python3 hn_scout.py --limit 100

    # Niższy próg score
    python3 hn_scout.py --min-score 30

    # JSON zamiast Markdown
    python3 hn_scout.py --json

    # Pokaż też "new" stories (nie tylko top)
    python3 hn_scout.py --include-new

Podejście techniczne:
    HackerNews API: https://hacker-news.firebaseio.com/v0/
    Publiczne, zero auth, zero rate limit.

Wymagania:
    - requests (pip install requests)
"""

import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

import requests

# ---------------------------------------------------------------------------
# Konfiguracja
# ---------------------------------------------------------------------------

HN_API = "https://hacker-news.firebaseio.com/v0"

# Słowa kluczowe — post musi zawierać min. 1 żeby przejść filtr
KEYWORDS = [
    # AI / LLM
    "ai", "artificial intelligence", "llm", "gpt", "chatgpt", "claude",
    "openai", "anthropic", "gemini", "copilot", "machine learning",
    "deep learning", "neural", "transformer", "rag", "agent",
    "local llm", "ollama", "llama", "mistral",
    # Automatyzacja
    "automat", "workflow", "n8n", "zapier", "make.com",
    "rpa", "no-code", "low-code", "integration",
    # Dev / narzędzia
    "python", "api", "self-host", "docker", "deploy",
    "open source", "developer tool", "cli tool",
    # Biznes
    "startup", "saas", "enterprise", "business", "productivity",
    "small business", "freelanc",
    # Compliance / prawo
    "gdpr", "compliance", "regulation", "eu ai act", "privacy",
]

# Słowa kluczowe high-relevance dla Dokodu
HIGH_RELEVANCE = [
    "n8n", "workflow", "automat", "self-host", "ai agent",
    "business process", "enterprise ai", "compliance", "gdpr",
    "rpa", "zapier", "make.com", "no-code", "python api",
]

HEADERS = {
    "User-Agent": "DOKODU-ContentRadar/1.0",
}


# ---------------------------------------------------------------------------
# HackerNews API
# ---------------------------------------------------------------------------

def fetch_story_ids(endpoint: str = "topstories", limit: int = 50) -> list[int]:
    """Pobiera listę ID top/new stories."""
    url = f"{HN_API}/{endpoint}.json"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        ids = resp.json()
        return ids[:limit]
    except (requests.RequestException, json.JSONDecodeError) as e:
        print(f"  WARN: błąd pobierania {endpoint}: {e}", file=sys.stderr)
        return []


def fetch_item(item_id: int) -> dict | None:
    """Pobiera pojedynczy item (story/comment)."""
    url = f"{HN_API}/item/{item_id}.json"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            return resp.json()
    except (requests.RequestException, json.JSONDecodeError):
        pass
    return None


def fetch_stories_parallel(ids: list[int], max_workers: int = 10) -> list[dict]:
    """Pobiera stories równolegle."""
    stories = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(fetch_item, sid): sid for sid in ids}
        for future in as_completed(futures):
            result = future.result()
            if result and result.get("type") == "story" and not result.get("dead") and not result.get("deleted"):
                stories.append(result)
    return stories


def fetch_top_comments(story: dict, limit: int = 3) -> list[str]:
    """Pobiera top N komentarzy ze story."""
    kid_ids = story.get("kids", [])[:limit * 2]  # pobierz więcej, filtruj
    if not kid_ids:
        return []

    comments = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(fetch_item, cid): cid for cid in kid_ids}
        for future in as_completed(futures):
            item = future.result()
            if item and item.get("text") and not item.get("dead") and not item.get("deleted"):
                # Wyczyść HTML
                text = item["text"].replace("<p>", " ").replace("</p>", "")
                text = text.replace("<i>", "").replace("</i>", "")
                text = text.replace("<b>", "").replace("</b>", "")
                text = text.replace("<a href=", "[").replace("</a>", "")
                text = text.replace("&#x27;", "'").replace("&amp;", "&").replace("&gt;", ">").replace("&lt;", "<").replace("&quot;", '"')
                text = text.strip()[:200]
                if len(text) > 30:
                    comments.append(text + ("..." if len(item.get("text", "")) > 200 else ""))
            if len(comments) >= limit:
                break

    return comments


# ---------------------------------------------------------------------------
# Filtrowanie i scoring
# ---------------------------------------------------------------------------

def matches_keywords(story: dict) -> bool:
    """Sprawdza czy story pasuje do słów kluczowych."""
    title = (story.get("title") or "").lower()
    text = (story.get("text") or "").lower()
    combined = title + " " + text

    return any(kw in combined for kw in KEYWORDS)


def calculate_relevance(story: dict) -> str:
    """Taguje story jako high/medium/low relevance."""
    title = (story.get("title") or "").lower()
    text = (story.get("text") or "").lower()
    combined = title + " " + text

    for kw in HIGH_RELEVANCE:
        if kw in combined:
            return "high"
    return "medium"  # Jeśli przeszedł filtr KEYWORDS, to min. medium


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def format_markdown(stories: list[dict]) -> str:
    """Formatuje stories jako Markdown."""
    lines = [
        f"# HackerNews Scout — {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Przeskanowano {len(stories)} relevantnych stories\n",
    ]

    # Sortuj: high first, potem po score
    relevance_order = {"high": 0, "medium": 1, "low": 2}
    stories.sort(key=lambda s: (relevance_order.get(s.get("_relevance", "medium"), 1), -s.get("score", 0)))

    for rel_label, rel_emoji in [("high", "🔴"), ("medium", "🟡")]:
        group = [s for s in stories if s.get("_relevance") == rel_label]
        if not group:
            continue

        lines.append(f"\n## {rel_emoji} Relevance: {rel_label.upper()} ({len(group)} stories)\n")

        for s in group:
            title = s.get("title", "").strip()
            url = s.get("url", "")
            hn_url = f"https://news.ycombinator.com/item?id={s.get('id', '')}"
            score = s.get("score", 0)
            comments = s.get("descendants", 0)

            lines.append(f"### [{title}]({hn_url})")
            if url:
                lines.append(f"🔗 {url}")
            lines.append(f"⬆️ {score} | 💬 {comments}")

            # Top komentarze
            top_comments = s.get("_top_comments", [])
            if top_comments:
                lines.append("\n**Top komentarze:**")
                for i, tc in enumerate(top_comments, 1):
                    lines.append(f"{i}. {tc}")

            lines.append("")

    return "\n".join(lines)


def format_json(stories: list[dict]) -> str:
    """Formatuje stories jako JSON."""
    clean = []
    for s in stories:
        clean.append({
            "title": s.get("title"),
            "score": s.get("score"),
            "num_comments": s.get("descendants", 0),
            "url": s.get("url", ""),
            "hn_url": f"https://news.ycombinator.com/item?id={s.get('id', '')}",
            "relevance": s.get("_relevance", "medium"),
            "top_comments": s.get("_top_comments", []),
            "time": s.get("time"),
        })
    return json.dumps(clean, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Skanuje HackerNews pod kątem AI/automatyzacja/dev tematów"
    )
    parser.add_argument(
        "--limit", type=int, default=100,
        help="Max stories do przeskanowania (domyślnie: 100)"
    )
    parser.add_argument(
        "--min-score", type=int, default=30,
        help="Minimalny score (domyślnie: 50)"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output w formacie JSON zamiast Markdown"
    )
    parser.add_argument(
        "--no-comments", action="store_true",
        help="Nie pobieraj komentarzy (szybciej)"
    )
    parser.add_argument(
        "--include-new", action="store_true",
        help="Dołącz też 'new' stories oprócz top"
    )
    args = parser.parse_args()

    print(f"HN Scout — skan top {args.limit} stories...", file=sys.stderr)

    # Pobierz story IDs
    ids = fetch_story_ids("topstories", args.limit)
    if args.include_new:
        new_ids = fetch_story_ids("newstories", args.limit // 2)
        ids = list(dict.fromkeys(ids + new_ids))  # deduplikacja zachowująca kolejność

    # Pobierz stories równolegle
    stories = fetch_stories_parallel(ids)
    print(f"  Pobrano {len(stories)} stories", file=sys.stderr)

    # Filtruj po keywordach i score
    filtered = [
        s for s in stories
        if matches_keywords(s) and s.get("score", 0) >= args.min_score
    ]
    print(f"  Po filtrze: {len(filtered)} relevantnych stories", file=sys.stderr)

    if not filtered:
        print("Brak stories spełniających kryteria.", file=sys.stderr)
        sys.exit(0)

    # Taguj relevance i pobierz komentarze
    for s in filtered:
        s["_relevance"] = calculate_relevance(s)
        if not args.no_comments and s["_relevance"] == "high":
            s["_top_comments"] = fetch_top_comments(s, limit=3)
        else:
            s["_top_comments"] = []

    # Output
    if args.json:
        print(format_json(filtered))
    else:
        print(format_markdown(filtered))

    print(f"\nGotowe: {len(filtered)} relevantnych stories.", file=sys.stderr)


if __name__ == "__main__":
    main()
