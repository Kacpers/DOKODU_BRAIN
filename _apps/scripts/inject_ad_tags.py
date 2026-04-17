#!/usr/bin/env python3
"""
Wstawia tagi <AD:key> do contentMarkdown postów w bazie danych.
Tagi umieszczane są przed ostatnią sekcją ## (Podsumowanie).
"""
import subprocess
import re
import json
import urllib.request
import urllib.parse
from pathlib import Path

API_KEY = (Path.home() / ".config/dokodu/blog_api_key").read_text().strip()
API_BASE = "https://dokodu.it/api/external"
HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json",
    "User-Agent": "DokodoBrain/1.0 (+https://dokodu.it)",
}

# Konfiguracja: slug → [(ad_key, insertion: 'before_last' | 'before_second_to_last')]
POSTS_CONFIG = {
    "n8n": [("sciezka_openai", "before_last")],
    "co-to-jest-llm": [("sciezka_openai", "before_last")],
    "automatyzacja-procesow": [("sciezka_openai", "before_last")],
    "chatgpt-vs-perplexity-porownanie": [("sciezka_openai", "before_last")],
    "wdrozenie-ai-w-firmie": [
        ("sciezka_openai", "before_second_to_last"),
        ("sciezka_microsoft", "before_last"),
    ],
}


def get_content_from_db(slug: str) -> tuple[str, str]:
    """Pobiera id i contentMarkdown z bazy przez SSH — używa base64 żeby uniknąć problemów z kodowaniem."""
    # Wyciągamy id i content osobno, żeby uniknąć problemów z separatorem w treści
    result_id = subprocess.run(
        ["ssh", "dokodu-vps",
         f"""docker exec app-db psql -U dokodu_user -d dokodu_prod -t -A -c "SELECT id FROM \\"Post\\" WHERE slug='{slug}' LIMIT 1;" """],
        capture_output=True, text=True, timeout=30
    )
    post_id = result_id.stdout.strip()
    if not post_id:
        raise ValueError(f"Brak posta dla slug={slug}")

    # Pobierz content przez base64 żeby uniknąć problemów z polskimi znakami i separatorami
    result_content = subprocess.run(
        ["ssh", "dokodu-vps",
         f"""docker exec app-db psql -U dokodu_user -d dokodu_prod -t -A -c "SELECT encode(convert_to(\\"contentMarkdown\\", 'UTF8'), 'base64') FROM \\"Post\\" WHERE id='{post_id}' LIMIT 1;" """],
        capture_output=True, text=True, timeout=60
    )
    b64 = result_content.stdout.strip().replace("\n", "").replace(" ", "")
    if not b64:
        raise ValueError(f"Brak contentu dla slug={slug}")

    import base64
    content = base64.b64decode(b64).decode("utf-8")
    return post_id, content


def insert_ad_before_section(content: str, ad_key: str, position: str) -> str:
    """Wstawia <AD:key> przed odpowiednią sekcją ## (pomija ###)."""
    # Znajdź wszystkie pozycje nagłówków H2 (## ale nie ###)
    h2_positions = [(m.start(), m.group()) for m in re.finditer(r'^## .+', content, re.MULTILINE)]

    if not h2_positions:
        # Brak H2 — wstaw przed ostatnim akapitem
        return content + f"\n\n<AD:{ad_key}>\n"

    if position == "before_last":
        insert_at = h2_positions[-1][0]
    elif position == "before_second_to_last":
        if len(h2_positions) >= 2:
            insert_at = h2_positions[-2][0]
        else:
            insert_at = h2_positions[-1][0]
    else:
        insert_at = h2_positions[-1][0]

    tag = f"<AD:{ad_key}>\n\n"
    return content[:insert_at] + tag + content[insert_at:]


def update_post_content(post_id: str, content: str) -> bool:
    """Aktualizuje contentMarkdown przez external API."""
    url = f"{API_BASE}/posts/{post_id}"
    data = json.dumps({"content": content}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="PUT")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            return result.get("success", False)
    except Exception as e:
        print(f"  ✗ API error: {e}")
        return False


def main():
    for slug, insertions in POSTS_CONFIG.items():
        print(f"\n→ {slug}")
        try:
            post_id, content = get_content_from_db(slug)
            print(f"  ID: {post_id}, content: {len(content)} znaków")

            # Sprawdź czy już ma sciezka_* tagi (inne AD tagi OK — dodajemy obok)
            existing_sciezka = re.findall(r'<AD:sciezka_[^>]+>', content)
            if existing_sciezka:
                print(f"  ⚠ Już ma sciezka tagi: {existing_sciezka} — pomijam")
                continue
            existing_tags = re.findall(r'<AD:[^>]+>', content)
            if existing_tags:
                print(f"  ℹ Ma inne tagi: {existing_tags} — dodaję sciezka obok")

            # Wstaw tagi w kolejności (od końca żeby nie przesuwać pozycji)
            # Najpierw second_to_last, potem last
            modified = content
            for ad_key, position in insertions:
                modified = insert_ad_before_section(modified, ad_key, position)
                print(f"  + <AD:{ad_key}> ({position})")

            # Update przez API
            ok = update_post_content(post_id, modified)
            if ok:
                print(f"  ✓ Zaktualizowano")
            else:
                print(f"  ✗ Błąd aktualizacji")
        except Exception as e:
            print(f"  ✗ Error: {e}")


if __name__ == "__main__":
    main()
