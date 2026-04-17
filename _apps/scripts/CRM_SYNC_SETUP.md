# CRM Sync Setup

## Konfiguracja jednorazowa

1. Zaloguj się do CRM (system.dokodu.it) jako admin
2. Wygeneruj API key: Settings → API Keys → Generate (endpoint: `POST /api/auth/api-key`)
3. Zapisz klucz:
   ```bash
   mkdir -p ~/.config/dokodu
   echo "dk_xxxxx..." > ~/.config/dokodu/crm_api_key
   chmod 600 ~/.config/dokodu/crm_api_key
   ```

## Użycie

```bash
# Status: co jest w CRM vs BRAIN
python scripts/crm_sync.py status

# Push meeting do CRM (ostatnie spotkanie z Meetings.md)
python scripts/crm_sync.py push-meeting "Gibula"

# Push activity (np. po wysłaniu emaila)
python scripts/crm_sync.py push-activity "Gibula" email_sent "Wysłana oferta Q2"

# Push lead jako company do CRM
python scripts/crm_sync.py push-lead "Nowa Firma"

# Pull pipeline z CRM → aktualizacja CRM_Leady_B2B.md
python scripts/crm_sync.py pull-pipeline

# Pull company z CRM → aktualizacja/tworzenie Profile.md
python scripts/crm_sync.py pull-company "Gibula"
```

## Zmienne środowiskowe (opcjonalnie)

- `CRM_API_KEY` — zamiast pliku ~/.config/dokodu/crm_api_key
- `CRM_BASE_URL` — domyślnie https://system.dokodu.it

## Jak działa API key auth

API key jest hashowane SHA-256 i przechowywane jako hash + prefix (8 znaków).
Plain text key jest zwracany TYLKO raz przy generowaniu — zapisz go od razu.
Klucz dziedziczy uprawnienia użytkownika, który go wygenerował.
