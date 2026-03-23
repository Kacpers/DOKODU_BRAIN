#!/usr/bin/env python3
"""
Podpina reklamy ścieżek B2B do kluczowych postów bloga.
Uruchom PO deployu nowej wersji (obsługa pola 'ads' w PUT API).

Użycie:
  python3 attach_sciezki_ads.py
"""
import json
import urllib.request
import urllib.error
from pathlib import Path

SITE_URL = "https://dokodu.it"
API_KEY_FILE = Path.home() / ".config/dokodu/dokodu_api_key"
API_KEY = API_KEY_FILE.read_text().strip()

def api_put(post_id: str, payload: dict) -> dict:
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{SITE_URL}/api/external/posts/{post_id}",
        data=data,
        headers={
            "x-api-key": API_KEY,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (compatible; DokodoBrain/1.0; +https://dokodu.it)",
        },
        method="PUT",
    )
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode()}

# Post ID → reklamy do podpięcia
# Format ads: {"pozycja": "klucz_reklamy"}
# Pozycje: ad_1 (wysoko w artykule), ad_2 (środek), ad_bottom (na końcu)
ASSIGNMENTS = [
    {
        "id": "cmls06rq90012i3hswx678sox",
        "slug": "co-to-jest-llm",
        "ads": {
            "ad_1": "sciezka_openai",       # LLM → OpenAI ścieżka
        }
    },
    {
        "id": "cmls06rjs000fi3hsndpedtry",
        "slug": "automatyzacja-procesow",
        "ads": {
            "ad_1": "sciezka_openai",       # Automatyzacja → OpenAI
        }
    },
    {
        "id": "cmls06u7x009ti3hsbrhnrh6k",
        "slug": "wdrozenie-ai-w-firmie",
        "ads": {
            "ad_1": "sciezka_openai",       # Wdrożenie AI → OpenAI
            "ad_2": "sciezka_microsoft",    # Też Microsoft
        }
    },
    {
        "id": "cmls1wogl000vw3hscrrqwj6j",
        "slug": "n8n",
        "ads": {
            "ad_1": "sciezka_openai",       # n8n/automatyzacja → OpenAI
        }
    },
    {
        "id": "cmls06rno000ui3hsiisfob4e",
        "slug": "chatgpt-vs-perplexity-porownanie",
        "ads": {
            "ad_1": "sciezka_openai",       # ChatGPT comparison → OpenAI
        }
    },
]

def main():
    print("Podpinanie reklam ścieżek B2B do postów...\n")
    for post in ASSIGNMENTS:
        result = api_put(post["id"], {"ads": post["ads"]})
        if result.get("success"):
            print(f"  ✓ {post['slug']}")
        else:
            print(f"  ✗ {post['slug']} — {result}")
    print("\nGotowe! Pamiętaj o revalidacji cache.")

if __name__ == "__main__":
    main()
