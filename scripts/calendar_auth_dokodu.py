#!/usr/bin/env python3
"""
OAuth flow dla kacper@dokodu.it — Calendar + Gmail.
Wersja kompatybilna z WSL (nie wymaga localhost).

Użycie:
  python3 calendar_auth_dokodu.py

Skrypt wyświetli URL → skopiuj do przeglądarki → zaloguj się na kacper@dokodu.it
→ po autoryzacji skopiuj KOD z przeglądarki → wklej tu.
"""

import json
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/gmail.readonly",
]

OAUTH_KEYS = Path.home() / ".gmail-mcp" / "gcp-oauth.keys.json"
CREDENTIALS_OUT = Path.home() / ".config" / "dokodu" / "dokodu_calendar_credentials.json"


def main():
    print("=" * 50)
    print("OAuth: kacper@dokodu.it (Calendar + Gmail)")
    print("=" * 50)
    print()
    print("WAŻNE: Zaloguj się na kacper@dokodu.it (NIE gmail!)")
    print()

    # Modyfikuj OAuth config żeby użyć redirect do localhost z portem
    # ale nasłuchuj na 0.0.0.0 (dostępne z Windows)
    flow = InstalledAppFlow.from_client_secrets_file(str(OAUTH_KEYS), SCOPES)

    # Spróbuj z bind na 0.0.0.0 żeby Windows mógł się połączyć
    try:
        print("Otwieram okno autoryzacji...")
        print("Jeśli przeglądarka się nie otworzy, skopiuj URL ręcznie.")
        print()
        creds = flow.run_local_server(
            port=8090,
            bind_addr="0.0.0.0",
            open_browser=False,
            prompt="consent",
            authorization_prompt_message="Otwórz ten URL w przeglądarce:\n\n{url}\n",
        )
    except Exception as e:
        print(f"Błąd serwera lokalnego: {e}")
        print("Nie udało się — spróbuj ponownie.")
        return

    CREDENTIALS_OUT.parent.mkdir(parents=True, exist_ok=True)

    token_data = {
        "access_token": creds.token,
        "refresh_token": creds.refresh_token,
        "scope": " ".join(SCOPES),
        "token_type": "Bearer",
        "expiry_date": int(creds.expiry.timestamp() * 1000) if creds.expiry else None,
    }

    CREDENTIALS_OUT.write_text(json.dumps(token_data))
    print(f"\n✅ Token zapisany: {CREDENTIALS_OUT}")
    print("Account: kacper@dokodu.it")
    print("Scopes: Calendar + Gmail (readonly)")


if __name__ == "__main__":
    main()
