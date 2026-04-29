---
name: crm-add-module
description: Dodaje moduł (Allegro, MailerLite, n8n, etc.) do istniejącej instancji CRM. Aktualizuje MODULES_ENABLED env, kopiuje folder modułu do build context, rebuild + restart. Trigger: "dodaj modul allegro do pedrollo", "włącz mailerlite na crm", "doinstaluj moduł", /crm-add-module {slug} {module}.
---

# Instrukcja: CRM Add Module

## Działanie

Aktywuje moduł na istniejącej instancji CRM. Każdy moduł to samodzielny folder w `modules/{name}/` (Plan 1 architektura) — schema-extension, api routes, components, seed, README.

## KROK 1: Wyciągnij slug + nazwę modułu

Z prompta wyciągnij:
- `slug` — która instancja (np. pedrollo)
- `module` — nazwa modułu (np. allegro, mailerlite, n8n-connector)

Jeśli niejasne — zapytaj użytkownika.

## KROK 2: Pokaż dostępne moduły

```bash
cd /Users/ksieradzinski/Projects/dokodu/crm-new
ls modules/
```

Jeśli żądany moduł nie istnieje — pokaż listę i zapytaj który zamiast.

## KROK 3: Uruchom add-module

```bash
./scripts/crm-add-module.sh <slug> <module>
```

Skrypt:
1. Weryfikuje że `modules/{module}/` istnieje
2. Aktualizuje `MODULES_ENABLED=...` w `.env` instancji na serwerze (idempotent — nie duplikuje)
3. Regeneruje `docker-compose.{slug}.yml` z nowego env
4. Kopiuje sources `modules/{module}/` do build context na serwerze
5. Wywołuje `crm-update.sh` żeby przebudować + restartować

## KROK 4: Verify w UI

Po update:
```
✅ Module {module} active on crm-{slug}

URL: https://dev.dokodu.it/crm-{slug}
W Settings → Modules powinno teraz pokazywać "{module}: ✓ aktywny"
```

## Uwagi

- Dla Faza 0 instancji (config-only): moduł zostaje w monorepo, tylko env flag się zmienia
- Dla Faza 1+ (forked): moduł musi być TAKŻE skopiowany do fork repo (skrypt to robi przez sync do build context, ale nie commituje do fork repo — to manualnie zrobi user gdy będzie chciał persistencji)
- Niektóre moduły wymagają konfiguracji (np. Allegro = OAuth tokens) — skrypt tylko aktywuje moduł, klient potem konfiguruje w UI
- Add-on moduły są oznaczone w UI ikoną „+" — klient widzi że to płatny add-on
