---
name: crm-update
description: Rolling update instancji CRM do najnowszej wersji z mastera lub forku. Rebuild image + restart container + healthcheck. Trigger: "zaktualizuj crm", "redeploy crm", "deploy najnowsze", /crm-update {slug}.
---

# Instrukcja: CRM Update

## Działanie

Aktualizuje wybraną instancję CRM (master demo lub konkretny prospekt) do najnowszego kodu — rebuild Docker image, prisma migrate (idempotent), restart kontenera, czeka na healthcheck.

Krótki downtime ~5s podczas restart'u (zero-downtime blue/green deploy będzie w Plan 7).

## KROK 1: Sprawdź instancje

```bash
cd /Users/ksieradzinski/Projects/dokodu/crm-new
./scripts/list-instances.sh
```

Jeśli użytkownik nie podał konkretnego slug — pokaż listę i zapytaj którą zaktualizować.

## KROK 2: Uruchom update

```bash
./scripts/crm-update.sh <slug>
```

Skrypt:
1. Sync źródła z lokalnego checkout do `$REMOTE_BASE/build/` na serwerze
2. Sync prospect's themes/{slug}/ do build context
3. Rebuild image z odpowiednimi build args (BUILD_BASE_PATH, BUILD_THEME_CONFIG_PATH, BUILD_NEXTAUTH_URL, BUILD_BRAND_LOGO_URL)
4. Run prisma migrations (idempotent — `db push`)
5. `docker compose up -d --force-recreate crm-{slug}`
6. Wait healthcheck `/api/health` → 200 (max 60s)

## KROK 3: Verify + raport

Wyświetl:
```
✅ Updated crm-{slug}

URL: https://dev.dokodu.it/crm-{slug}
Build time: ~2 min
Health: ✓
```

Jeśli healthcheck failuje:
```
❌ Update failed — check logs
ssh deploy@57.128.219.9 'docker logs crm-{slug} --tail 50'
```

## Uwagi

- Update NIE robi backupu DB. Dla produkcji klient (Faza 2) backup jest dzienny automatyczny (Plan 7)
- Zmiany schematu Prismy są stosowane via `db push` (NIE `db migrate`) — bezpieczne dla demo, dla prod dodamy proper migracje w Plan 7
- Rolling update potrafi failnąć jeśli prisma migracja jest niezgodna z istniejącymi danymi — wtedy `crm-{slug}-db` ma poprzedni stan, można wrócić
