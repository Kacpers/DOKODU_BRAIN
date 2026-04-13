---
name: ga-sync
description: Synchronizuje dane z Google Analytics 4 do DOKODU_BRAIN. Pobiera sesje, użytkowników, bounce rate, źródła ruchu, zdarzenia i ruch na ścieżkach B2B. Zapisuje raport do GA_Last_Sync.md. Trigger: "zsynchronizuj analytics", "pobierz dane z ga", "odśwież analytics", "sync ga", /ga-sync
---

# Instrukcja: GA Sync (Google Analytics 4)

## Działanie

Uruchamia skrypt Python który łączy się z GA4 Data API i pobiera dane analityczne dokodu.it.

## KROK 1: Uruchom skrypt

```bash
cd /home/kacper/DOKODU_BRAIN/scripts && python3 ga_fetch.py --days 28 --save
```

Dla krótszego okresu (ostatni tydzień):
```bash
python3 ga_fetch.py --days 7 --save
```

## KROK 2: Sprawdź czy token jest ważny

Jeśli pojawi się błąd autoryzacji — token wygasł. Wygeneruj nowy URL:

```bash
python3 - <<'PYEOF'
import json, pickle, secrets, hashlib, base64, urllib.parse
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "dokodu"
CREDENTIALS_FILE = CONFIG_DIR / "gsc_credentials.json"
creds_data = json.loads(CREDENTIALS_FILE.read_text())["installed"]

code_verifier = secrets.token_urlsafe(64)
code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(code_verifier.encode()).digest()
).rstrip(b"=").decode()
(CONFIG_DIR / "ga_pkce_verifier.txt").write_text(code_verifier)

params = {
    "response_type": "code",
    "client_id": creds_data["client_id"],
    "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
    "scope": "https://www.googleapis.com/auth/analytics.readonly",
    "code_challenge": code_challenge,
    "code_challenge_method": "S256",
    "access_type": "offline",
    "prompt": "consent",
}
print(creds_data["auth_uri"] + "?" + urllib.parse.urlencode(params))
PYEOF
```

Pokaż URL użytkownikowi, poczekaj na kod, potem wymień:

```bash
python3 - <<'PYEOF'
import json, pickle, requests
from pathlib import Path
from google.oauth2.credentials import Credentials

CONFIG_DIR = Path.home() / ".config" / "dokodu"
creds_data = json.loads((CONFIG_DIR / "gsc_credentials.json").read_text())["installed"]
code_verifier = (CONFIG_DIR / "ga_pkce_verifier.txt").read_text().strip()

# ZASTĄP poniższy kod kodem od użytkownika
CODE = "WKLEJ_KOD_TUTAJ"

resp = requests.post(creds_data["token_uri"], data={
    "code": CODE,
    "client_id": creds_data["client_id"],
    "client_secret": creds_data["client_secret"],
    "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
    "grant_type": "authorization_code",
    "code_verifier": code_verifier,
})
data = resp.json()
creds = Credentials(
    token=data["access_token"],
    refresh_token=data.get("refresh_token"),
    token_uri=creds_data["token_uri"],
    client_id=creds_data["client_id"],
    client_secret=creds_data["client_secret"],
    scopes=["https://www.googleapis.com/auth/analytics.readonly"],
)
with open(CONFIG_DIR / "ga_token.pickle", "wb") as f:
    pickle.dump(creds, f)
print("✓ Token zapisany")
(CONFIG_DIR / "ga_pkce_verifier.txt").unlink(missing_ok=True)
PYEOF
```

## KROK 3: Wyświetl podsumowanie

Po udanym wykonaniu powiedz:
- Łączne sesje i użytkownicy w okresie
- Top 3 strony wg sesji
- Główne źródła ruchu
- Sesje na ścieżkach B2B (/sciezki/*)

## KROK 4: Zaproponuj następny krok

- `/ga-stats` — głęboka analiza: bounce rate, konwersje, ścieżki B2B
- `/seo-sync` + `/ga-sync` razem w piątek → pełny obraz

## ZASADY

- Token zapisany w: `~/.config/dokodu/ga_token.pickle`
- Dane w: `~/.config/dokodu/ga_data.db`
- Raport w: `BRAIN/20_AREAS/AREA_Blog_SEO/GA_Last_Sync.md`
- GA4 ma ~1-dniowy lag — dane z wczoraj są już dostępne
- Property ID: `properties/386471428`
