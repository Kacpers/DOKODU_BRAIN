#!/usr/bin/env python3
"""
OAuth flow dla Google Drive (Meet Recordings) — kacper@dokodu.it
Wersja kompatybilna z WSL (bind 0.0.0.0).

Użycie:
  python3 meet_auth.py

Skrypt otworzy URL → zaloguj się na kacper@dokodu.it → token zapisany.
"""

import json
import pickle
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/calendar.readonly",
]

OAUTH_KEYS = Path.home() / ".config" / "dokodu" / "gdrive_credentials.json"
TOKEN_OUT = Path.home() / ".config" / "dokodu" / "meet_token.pickle"


def main():
    print("=" * 50)
    print("OAuth: Google Drive + Calendar (Meet Transcribe)")
    print("=" * 50)
    print()
    print("WAŻNE: Zaloguj się na kacper@dokodu.it")
    print()

    flow = InstalledAppFlow.from_client_secrets_file(str(OAUTH_KEYS), SCOPES)

    try:
        print("Otwieram okno autoryzacji...")
        print("Jeśli przeglądarka się nie otworzy, skopiuj URL ręcznie.")
        print()
        creds = flow.run_local_server(
            port=8095,
            bind_addr="0.0.0.0",
            open_browser=False,
            prompt="consent",
            authorization_prompt_message="Otwórz ten URL w przeglądarce:\n\n{url}\n",
        )
    except Exception as e:
        print(f"Błąd: {e}")
        return

    TOKEN_OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(TOKEN_OUT, "wb") as f:
        pickle.dump(creds, f)

    print(f"\n✅ Token zapisany: {TOKEN_OUT}")
    print("Scopes: Drive (read + file) + Calendar (read)")
    print("Teraz możesz uruchomić: python3 meet_transcribe.py")


if __name__ == "__main__":
    main()
