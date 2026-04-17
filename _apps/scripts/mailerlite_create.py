#!/usr/bin/env python3
"""
DOKODU BRAIN — MailerLite Create Campaign (Classic API v2)
Tworzy kampanię jako DRAFT w MailerLite na podstawie subject + treści.

Użycie:
  python3 mailerlite_create.py --subject "Temat" --body "Treść" --groups 111679368
  python3 mailerlite_create.py --subject "Temat" --file tresc.txt --groups 111679368,111682076
  python3 mailerlite_create.py --list-groups        # pokaż wszystkie grupy z ID
  python3 mailerlite_create.py --subject "..." --body "..." --groups 111679368 --send  # wyślij od razu (ostrożnie!)

Kampania zostaje zapisana jako DRAFT — nie jest wysyłana bez --send.
API key: ~/.config/dokodu/mailerlite_api_key
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

CONFIG_DIR   = Path.home() / ".config" / "dokodu"
API_KEY_FILE = CONFIG_DIR / "mailerlite_api_key"
API_BASE     = "https://api.mailerlite.com/api/v2"

FROM_EMAIL = "kacper@dokodu.it"
FROM_NAME  = "Kacper z Dokodu"


# ══════════════════════════════════════════════
# AUTH + HTTP
# ══════════════════════════════════════════════

def get_api_key() -> str:
    key = os.environ.get("MAILERLITE_API_KEY", "").strip()
    if key:
        return key
    if API_KEY_FILE.exists():
        key = API_KEY_FILE.read_text().strip()
        if key:
            return key
    print("ERROR: Brak klucza API MailerLite.")
    sys.exit(1)


def ml_get(path: str) -> dict | list:
    req = urllib.request.Request(
        f"{API_BASE}/{path.lstrip('/')}",
        headers={"X-MailerLite-ApiKey": get_api_key(), "User-Agent": "curl/7.88.1"}
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())


def ml_post(path: str, data: dict, method: str = "POST") -> dict:
    payload = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(
        f"{API_BASE}/{path.lstrip('/')}",
        data=payload,
        headers={
            "X-MailerLite-ApiKey": get_api_key(),
            "User-Agent": "curl/7.88.1",
            "Content-Type": "application/json",
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"ERROR: HTTP {e.code}: {body}")
        sys.exit(1)


# ══════════════════════════════════════════════
# HTML TEMPLATE
# ══════════════════════════════════════════════

def build_html(body_text: str, subject: str) -> str:
    """
    Zamienia plain text na czysty HTML w stylu Kacpra:
    - minimalistyczny, tekstowy, bez grafik
    - akapity z \n\n → <p>
    - linie z \n → <br>
    - zachowuje emoji
    - stopka z unsubscribe
    """
    # Zamień akapity
    paragraphs = body_text.strip().split("\n\n")
    html_parts = []
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        # Wewnętrzne nowe linie → <br>
        para_html = para.replace("\n", "<br>\n")
        html_parts.append(f"<p>{para_html}</p>")

    body_html = "\n".join(html_parts)

    return f"""<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{subject}</title>
  <style>
    body {{ font-family: Georgia, serif; font-size: 16px; line-height: 1.7; color: #1a1a1a; background: #ffffff; margin: 0; padding: 0; }}
    .wrap {{ max-width: 600px; margin: 0 auto; padding: 40px 24px; }}
    p {{ margin: 0 0 18px 0; }}
    a {{ color: #0066cc; }}
    .footer {{ margin-top: 48px; padding-top: 24px; border-top: 1px solid #e5e5e5; font-size: 13px; color: #888; }}
  </style>
</head>
<body>
  <div class="wrap">
    {body_html}
    <div class="footer">
      <p>
        Pozdrawiam,<br>
        <strong>Kacper Sieradziński</strong><br>
        Dokodu sp. z o.o. | <a href="https://dokodu.it">dokodu.it</a>
      </p>
      <p>
        Otrzymujesz ten mail, bo zapisałeś/aś się na listę Dokodu.<br>
        <a href="{{$unsubscribe}}">Wypisz się z listy</a>
      </p>
    </div>
  </div>
</body>
</html>"""


def build_plain(body_text: str) -> str:
    """Plain text wersja z stopką."""
    return f"""{body_text.strip()}

---
Pozdrawiam,
Kacper Sieradziński
Dokodu sp. z o.o. | https://dokodu.it

Aby wypisać się z listy: {{$unsubscribe}}"""


# ══════════════════════════════════════════════
# ACTIONS
# ══════════════════════════════════════════════

def list_groups():
    groups = ml_get("groups?limit=100")
    active = [(g["id"], g.get("active", 0), g["name"])
              for g in groups if g.get("active", 0) > 0]
    active.sort(key=lambda x: -x[1])
    print(f"{'ID':>12}  {'Aktywni':>8}  Nazwa")
    print("-" * 60)
    for gid, cnt, name in active:
        print(f"{gid:>12}  {cnt:>8}  {name}")


def create_campaign(subject: str, body_text: str, group_ids: list[int], send: bool = False) -> dict:
    # 1. Utwórz kampanię
    print(f"Tworzę kampanię: {subject!r}")
    camp = ml_post("campaigns", {
        "type": "regular",
        "name": subject,
        "subject": subject,
        "from": FROM_EMAIL,
        "from_name": FROM_NAME,
        "groups": group_ids,
    })
    cid = camp["id"]
    print(f"  ✓ Kampania ID: {cid}")

    # 2. Ustaw treść
    print("  Ustawiam treść HTML...")
    ml_post(f"campaigns/{cid}/content", {
        "html": build_html(body_text, subject),
        "plain": build_plain(body_text),
    }, method="PUT")
    print("  ✓ Treść ustawiona")

    # 3. Wyślij lub zostaw jako draft
    if send:
        print("  ⚠ Wysyłam kampanię...")
        ml_post(f"campaigns/{cid}/actions/send", {})
        print(f"  ✓ WYSŁANO do {len(group_ids)} grup")
    else:
        print(f"  ✓ Kampania zapisana jako DRAFT")
        print(f"     → Sprawdź i wyślij w MailerLite: https://app.mailerlite.com/campaigns/{cid}")

    return camp


# ══════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Tworzy kampanię w MailerLite")
    parser.add_argument("--subject",     help="Temat maila (subject line)")
    parser.add_argument("--body",        help="Treść maila (plain text)")
    parser.add_argument("--file",        help="Plik .txt z treścią maila")
    parser.add_argument("--groups",      help="ID grup oddzielone przecinkiem, np. 111679368,111682076")
    parser.add_argument("--list-groups", action="store_true", help="Pokaż dostępne grupy z ID")
    parser.add_argument("--send",        action="store_true", help="Wyślij od razu (domyślnie: draft)")
    args = parser.parse_args()

    if args.list_groups:
        list_groups()
        return

    if not args.subject:
        print("ERROR: Podaj --subject")
        sys.exit(1)

    if args.file:
        body = Path(args.file).read_text(encoding="utf-8")
    elif args.body:
        body = args.body
    else:
        print("ERROR: Podaj --body 'treść' lub --file plik.txt")
        sys.exit(1)

    if not args.groups:
        print("ERROR: Podaj --groups ID (np. --groups 111679368)")
        print("Użyj --list-groups żeby zobaczyć dostępne grupy")
        sys.exit(1)

    group_ids = [int(g.strip()) for g in args.groups.split(",")]

    if args.send:
        print("⚠ UWAGA: Flaga --send wysyła email DO PRAWDZIWYCH ODBIORCÓW.")
        confirm = input("Wpisz 'WYSLIJ' żeby potwierdzić: ").strip()
        if confirm != "WYSLIJ":
            print("Anulowano.")
            sys.exit(0)

    create_campaign(args.subject, body, group_ids, send=args.send)


if __name__ == "__main__":
    main()
