#!/usr/bin/env python3
"""
reddit_scout.py — Skanuje subreddity pod kątem tematów na filmy YT / blog / leady

Pobiera top posty (24h) z ~15 subredditów AI/automatyzacja/dev/biznes.
Filtruje po score i komentarzach. Wypisuje Markdown na stdout.

Użycie:
    # Standardowy skan (top 24h, min 20 upvotes lub 15 komentarzy)
    python3 reddit_scout.py

    # Niższy próg (więcej wyników)
    python3 reddit_scout.py --min-score 10 --min-comments 8

    # Inne okno czasowe
    python3 reddit_scout.py --timeframe week

    # Limit wyników
    python3 reddit_scout.py --limit 30

    # JSON zamiast Markdown
    python3 reddit_scout.py --json

Podejście techniczne:
    Reddit udostępnia JSON na każdym URL-u po dodaniu .json
    Zero auth potrzebne do read-only. Rate limit: ~60 req/min bez tokenu.

Wymagania:
    - requests (pip install requests)
"""

import argparse
import json
import sys
import time
import random
from datetime import datetime

import requests

# ---------------------------------------------------------------------------
# Konfiguracja
# ---------------------------------------------------------------------------

SUBREDDITS = [
    # AI / Tech
    "artificial",
    "ChatGPT",
    "OpenAI",
    "LocalLLaMA",
    "MachineLearning",
    "ClaudeAI",
    # Automatyzacja
    "n8n",
    "selfhosted",
    "automation",
    "nocode",
    # Dev
    "Python",
    "dataengineering",
    "programming",
    # Biznes
    "smallbusiness",
    "entrepreneur",
    "SaaS",
]

HEADERS = {
    "User-Agent": "DOKODU-ContentRadar/1.0 (content research bot; kontakt: kacper@dokodu.it)",
}

# Słowa kluczowe do tagowania relevance dla Dokodu
DOKODU_KEYWORDS = {
    "high": [
        "n8n", "workflow", "automat", "zapier", "make.com", "self-host",
        "ai agent", "business process", "invoice", "crm", "erp",
        "compliance", "gdpr", "rodo", "ai act", "enterprise ai",
        "python script", "api integrat", "webhook",
    ],
    "medium": [
        "chatgpt", "claude", "openai", "llm", "gpt", "gemini",
        "copilot", "prompt", "rag", "vector", "embedding",
        "small business", "startup", "saas", "no-code", "low-code",
        "docker", "vps", "deploy", "hosting",
    ],
}


# ---------------------------------------------------------------------------
# Reddit JSON API
# ---------------------------------------------------------------------------

def fetch_subreddit_top(subreddit: str, timeframe: str = "day", limit: int = 25) -> list[dict]:
    """Pobiera top posty z subreddita przez JSON API."""
    url = f"https://www.reddit.com/r/{subreddit}/top.json"
    params = {"t": timeframe, "limit": limit}

    try:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=15)
        if resp.status_code == 429:
            print(f"  WARN: rate limit na r/{subreddit}, czekam 5s...", file=sys.stderr)
            time.sleep(5)
            resp = requests.get(url, headers=HEADERS, params=params, timeout=15)
        if resp.status_code != 200:
            print(f"  WARN: HTTP {resp.status_code} dla r/{subreddit}", file=sys.stderr)
            return []

        data = resp.json()
        children = data.get("data", {}).get("children", [])
        return [c["data"] for c in children if c.get("kind") == "t3"]

    except (requests.RequestException, json.JSONDecodeError) as e:
        print(f"  WARN: błąd r/{subreddit}: {e}", file=sys.stderr)
        return []


def fetch_top_comments(permalink: str, limit: int = 3) -> list[str]:
    """Pobiera top N komentarzy z posta."""
    url = f"https://www.reddit.com{permalink}.json"
    params = {"limit": limit, "sort": "top"}

    try:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=10)
        if resp.status_code != 200:
            return []

        data = resp.json()
        if len(data) < 2:
            return []

        comments = []
        for c in data[1].get("data", {}).get("children", []):
            if c.get("kind") != "t1":
                continue
            body = c["data"].get("body", "").strip()
            if body and len(body) > 20:
                # Skróć do 200 znaków
                comments.append(body[:200] + ("..." if len(body) > 200 else ""))
            if len(comments) >= limit:
                break
        return comments

    except (requests.RequestException, json.JSONDecodeError):
        return []


# ---------------------------------------------------------------------------
# Scoring i filtrowanie
# ---------------------------------------------------------------------------

def calculate_relevance(post: dict) -> str:
    """Taguje post jako high/medium/low relevance dla Dokodu."""
    text = (post.get("title", "") + " " + post.get("selftext", "")[:500]).lower()

    for kw in DOKODU_KEYWORDS["high"]:
        if kw in text:
            return "high"
    for kw in DOKODU_KEYWORDS["medium"]:
        if kw in text:
            return "medium"
    return "low"


def filter_posts(posts: list[dict], min_score: int, min_comments: int) -> list[dict]:
    """Filtruje posty po score LUB komentarzach."""
    return [
        p for p in posts
        if p.get("score", 0) >= min_score or p.get("num_comments", 0) >= min_comments
    ]


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def format_markdown(all_posts: list[dict], fetch_comments: bool = True) -> str:
    """Formatuje posty jako Markdown na stdout."""
    lines = [
        f"# Reddit Scout — {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Przeskanowano {len(SUBREDDITS)} subredditów | Znaleziono {len(all_posts)} postów\n",
    ]

    # Sortuj: high relevance first, potem po score
    relevance_order = {"high": 0, "medium": 1, "low": 2}
    all_posts.sort(key=lambda p: (relevance_order.get(p.get("_relevance", "low"), 2), -p.get("score", 0)))

    # Grupuj po relevance
    for rel_label, rel_emoji in [("high", "🔴"), ("medium", "🟡"), ("low", "🟢")]:
        group = [p for p in all_posts if p.get("_relevance") == rel_label]
        if not group:
            continue

        lines.append(f"\n## {rel_emoji} Relevance: {rel_label.upper()} ({len(group)} postów)\n")

        for p in group:
            score = p.get("score", 0)
            comments = p.get("num_comments", 0)
            sub = p.get("subreddit", "?")
            title = p.get("title", "").strip()
            url = f"https://reddit.com{p.get('permalink', '')}"
            selftext = p.get("selftext", "")[:300].strip()

            lines.append(f"### [{title}]({url})")
            lines.append(f"**r/{sub}** | ⬆️ {score} | 💬 {comments}")

            if selftext:
                lines.append(f"> {selftext}{'...' if len(p.get('selftext', '')) > 300 else ''}")

            # Top komentarze
            top_comments = p.get("_top_comments", [])
            if top_comments:
                lines.append("\n**Top komentarze:**")
                for i, tc in enumerate(top_comments, 1):
                    lines.append(f"{i}. {tc}")

            lines.append("")

    return "\n".join(lines)


def format_json(all_posts: list[dict]) -> str:
    """Formatuje posty jako JSON."""
    clean = []
    for p in all_posts:
        clean.append({
            "subreddit": p.get("subreddit"),
            "title": p.get("title"),
            "score": p.get("score"),
            "num_comments": p.get("num_comments"),
            "url": f"https://reddit.com{p.get('permalink', '')}",
            "selftext_preview": p.get("selftext", "")[:300],
            "relevance": p.get("_relevance", "low"),
            "top_comments": p.get("_top_comments", []),
            "created_utc": p.get("created_utc"),
        })
    return json.dumps(clean, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Skanuje subreddity pod kątem tematów na filmy YT / blog / leady"
    )
    parser.add_argument(
        "--min-score", type=int, default=20,
        help="Minimalny score posta (domyślnie: 20)"
    )
    parser.add_argument(
        "--min-comments", type=int, default=15,
        help="Minimalna liczba komentarzy (domyślnie: 15)"
    )
    parser.add_argument(
        "--timeframe", type=str, default="day",
        choices=["hour", "day", "week", "month"],
        help="Okno czasowe (domyślnie: day)"
    )
    parser.add_argument(
        "--limit", type=int, default=25,
        help="Max postów na subreddit (domyślnie: 25)"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output w formacie JSON zamiast Markdown"
    )
    parser.add_argument(
        "--no-comments", action="store_true",
        help="Nie pobieraj top komentarzy (szybciej)"
    )
    parser.add_argument(
        "--subreddits", type=str, default=None,
        help='Nadpisz subreddity: "n8n,Python,ChatGPT"'
    )
    args = parser.parse_args()

    # Parse subreddits
    subs = SUBREDDITS
    if args.subreddits:
        subs = [s.strip() for s in args.subreddits.split(",") if s.strip()]

    print(f"Reddit Scout — skan {len(subs)} subredditów (top/{args.timeframe})...", file=sys.stderr)

    all_posts = []
    for sub in subs:
        posts = fetch_subreddit_top(sub, args.timeframe, args.limit)
        filtered = filter_posts(posts, args.min_score, args.min_comments)

        for p in filtered:
            p["_relevance"] = calculate_relevance(p)

            # Pobierz top komentarze dla high/medium relevance
            if not args.no_comments and p["_relevance"] in ("high", "medium"):
                p["_top_comments"] = fetch_top_comments(p.get("permalink", ""), limit=3)
                time.sleep(random.uniform(0.3, 0.8))
            else:
                p["_top_comments"] = []

        all_posts.extend(filtered)
        print(f"  r/{sub}: {len(posts)} postów → {len(filtered)} po filtrze", file=sys.stderr)
        time.sleep(random.uniform(0.5, 1.5))

    if not all_posts:
        print("Brak postów spełniających kryteria.", file=sys.stderr)
        sys.exit(0)

    # Deduplikacja (ten sam URL)
    seen = set()
    unique = []
    for p in all_posts:
        url = p.get("permalink", "")
        if url not in seen:
            seen.add(url)
            unique.append(p)
    all_posts = unique

    # Output
    if args.json:
        print(format_json(all_posts))
    else:
        print(format_markdown(all_posts))

    print(f"\nGotowe: {len(all_posts)} postów z {len(subs)} subredditów.", file=sys.stderr)


if __name__ == "__main__":
    main()
