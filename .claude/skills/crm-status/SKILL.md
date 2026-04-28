---
name: crm-status
description: Pokazuje status wszystkich aktywnych instancji CRM (master + per-prospekt + prod). Listuje slug, URL, status healthchecku, last deploy, container resource usage. Trigger: "status crm", "lista demo", "co stoi na crm", "które instancje", /crm-status.
---

# Instrukcja: CRM Status

## Działanie

Listuje wszystkie aktualnie zdeployowane instancje Dokodu CRM na dev.dokodu.it i ich stan zdrowia.

## KROK 1: Pobierz listę kontenerów

```bash
cd /Users/ksieradzinski/Projects/dokodu/crm-new
./scripts/list-instances.sh 2>&1
```

Skrypt zwraca JSON array — każdy obiekt ma `slug`, `name`, `status`, `image`. Pusty array `[]` = brak instancji.

## KROK 2: Per-instancja: healthcheck + age + resources

Dla każdego slug w wynikach uruchom równolegle:

```bash
SLUG=<slug>
HEALTH=$(curl -s -o /dev/null -w "%{http_code}" "https://dev.dokodu.it/crm-${SLUG}/api/health" --max-time 5 2>/dev/null || echo "000")
LAST_DEPLOY=$(ssh deploy@57.128.219.9 "stat -c %y /home/deploy/crm-instances/${SLUG}/docker-compose.${SLUG}.yml 2>/dev/null | cut -d. -f1" 2>/dev/null || echo "n/a")
RESOURCE=$(ssh deploy@57.128.219.9 "docker stats crm-${SLUG} --no-stream --format 'CPU={{.CPUPerc}} MEM={{.MemUsage}}'" 2>/dev/null || echo "n/a")
```

## KROK 3: Wyświetl tabelę

```
INSTANCE              | STATUS | DEPLOYED            | RESOURCES
────────────────────────────────────────────────────────────────────
master                | ✅ 200 | 2026-04-15 12:30    | CPU=0.5% MEM=180MiB / 8GiB
crm-pedrollo          | ✅ 200 | 2026-04-28 17:42    | CPU=0.2% MEM=145MiB / 8GiB
crm-haba              | ❌ 502 | 2026-04-26 10:15    | down
────────────────────────────────────────────────────────────────────

Total: 3 instances, 2 healthy, 1 down.
```

Mapowanie statusów:
- `200` → ✅ healthy
- `502` → ❌ proxy fail (kontener down lub nie odpowiada)
- `503` → ⚠ unhealthy (DB down)
- `404` → ⚠ no route (brak nginx lub błąd routingu)
- `000` → 💀 timeout / unreachable

## KROK 4: Sugestie dla problemów

Jeśli któraś instancja ma status `down` / `502`:
- Powiedz: "Instancja {slug} jest nieosiągalna — sprawdź logi: `ssh deploy@57.128.219.9 'docker logs crm-{slug} --tail 50'`"
- Jeśli LAST_DEPLOY > 30 dni temu i stale down: zaproponuj `./scripts/destroy-instance.sh {slug}` (martwa demo)

Jeśli wszystkie healthy: pokaż ✅ "Wszystkie instancje działają normalnie."

## Uwagi

- Skrypt nie modyfikuje niczego — tylko czyta stan
- Resource stats wymagają SSH do deploy@57.128.219.9 — jeśli SSH failuje, wyświetl tylko slug + healthcheck
- Master demo (`crm-master`) traktowany tak samo jak per-prospekt — to po prostu osobna instancja
