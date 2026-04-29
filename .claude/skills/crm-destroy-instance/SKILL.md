---
name: crm-destroy-instance
description: Tear down instancji CRM — zatrzymuje kontenery, usuwa wolumeny (DB), kasuje katalog instancji na serwerze. Używać dla martwych demo (klient odrzucił po 30+ dniach) lub przy testowaniu. Trigger: "skasuj instancję", "destroy crm", "tear down demo", /crm-destroy-instance {slug}.
---

# Instrukcja: CRM Destroy Instance

## Działanie

Trwale usuwa instancję CRM z serwera Dokodu. Kontenery + wolumeny (włącznie z bazą danych!) + katalog instancji są kasowane. **NIE odzyskasz danych po tym** — używać świadomie.

## KROK 1: Potwierdź slug

Z prompta wyciągnij slug. Pokaż co zostanie usunięte:

```bash
cd /Users/ksieradzinski/Projects/dokodu/crm-new
./scripts/list-instances.sh | jq '.[] | select(.slug == "<slug>")'
```

Wyświetl użytkownikowi:
```
⚠️  POTWIERDZENIE — TO USUNIE BEZPOWROTNIE:

Instancja: crm-<slug>
URL: https://dev.dokodu.it/crm-<slug>
Containers: crm-<slug>, crm-db-<slug>, crm-migrate-<slug>
Volumes: crm-pgdata-<slug> (cała baza!), uploads-<slug>
Theme dir: /home/deploy/crm-instances/<slug>/

Potwierdzasz? (TAK/nie)
```

Jeśli nie wpisze "TAK" — przerwij.

## KROK 2: Uruchom destroy

```bash
./scripts/destroy-instance.sh <slug>
```

Skrypt:
1. `docker compose down -v` — kasuje containers + wolumeny (anonymous + named)
2. `rm -rf /home/deploy/crm-instances/<slug>` — kasuje wszystko związane z instancją

## KROK 3: Verify cleanup

```bash
./scripts/list-instances.sh | jq '.[] | select(.slug == "<slug>")'
```

Powinno zwrócić pustą listę.

```bash
ssh deploy@57.128.219.9 "ls /home/deploy/crm-instances/ | grep -c <slug> || echo 'cleaned'"
```

Powinno zwrócić "cleaned" (lub pustą linię).

## KROK 4: Cofnij nginx routing (opcjonalne)

Domyślnie nginx ma generic regex match dla `/crm-{slug}/*`. Po destroy żaden upstream nie istnieje, więc requesty zwracają 502. To jest OK na demo — jeśli klient próbuje wrócić, dostanie 502 a nie 404. Zostawić.

Jeśli chcesz BARDZO czyste — można usunąć cały `/srv/reverse-proxy/conf.d/smartmatch.conf` location dla destroyowanego slug, ale to overkill.

## Uwagi

- Fork repo na GitHubie (Faza 1+) NIE jest usuwany. Jeśli chcesz kompletny cleanup po klientcie który nie wrócił — manualnie skasuj `Kacpers/crm-{slug}` repo
- Backup theme'u na laptopie (themes/{slug}/) zostaje — możesz odtworzyć demo szybko
- Jeśli klient wrócił po destroyu — uruchom `/crm-new-demo {url}` od początku, theme się odtworzy i seed bundle się ponownie zaaplikuje
