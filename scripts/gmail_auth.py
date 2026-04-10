#!/usr/bin/env python3
"""OAuth flow for Gmail + Calendar API — saves token for MCP server."""

import json
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.settings.basic",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events",
]

OAUTH_KEYS = Path.home() / ".gmail-mcp" / "gcp-oauth.keys.json"
CREDENTIALS_OUT = Path.home() / ".gmail-mcp" / "credentials.json"


def main():
    print("=== OAuth: Gmail + Calendar ===")
    print(f"Scopes: {', '.join(s.split('/')[-1] for s in SCOPES)}")
    print(f"OAuth keys: {OAUTH_KEYS}")
    print()
    print("WAŻNE: Zaloguj się na ksieradzinski@gmail.com w przeglądarce!")
    print()

    flow = InstalledAppFlow.from_client_secrets_file(str(OAUTH_KEYS), SCOPES)
    creds = flow.run_local_server(port=8090, open_browser=False)

    token_data = {
        "access_token": creds.token,
        "refresh_token": creds.refresh_token,
        "scope": " ".join(SCOPES),
        "token_type": "Bearer",
        "expiry_date": int(creds.expiry.timestamp() * 1000) if creds.expiry else None,
    }

    CREDENTIALS_OUT.write_text(json.dumps(token_data))
    print(f"\n✅ Token zapisany: {CREDENTIALS_OUT}")
    print(f"Account: ksieradzinski@gmail.com")
    print(f"Scopes: Gmail + Calendar")


if __name__ == "__main__":
    main()
