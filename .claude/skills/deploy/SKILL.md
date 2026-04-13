---
name: deploy
description: Deployuje aplikację Dokodu na serwer produkcyjny. Robi git push do main, co automatycznie triggeruje GitHub Actions (deploy.yml) który odpala deploy.sh na serwerze (backup DB → docker build → migracje → restart → health check). Opcjonalnie sprawdza status Actions i logi z serwera. Używaj gdy: skończyłeś zmiany i chcesz je wdrożyć na produkcję. Trigger: "deploy", "wdróż", "wypchnij na produkcję", "push na serwer", /deploy
---

# deploy — Deploy na produkcję

## Cel
Wypchnąć lokalny kod na serwer produkcyjny przez git push → GitHub Actions → deploy.sh.

## Architektura deploya
```
git push origin main
    → GitHub Actions (.github/workflows/deploy.yml)
        → SSH na deploy@57.128.219.9
            → /srv/dokodu-app/app/deploy.sh
                → backup DB
                → git pull
                → docker build
                → prisma migrate
                → docker compose up
                → health check
                → rollback jeśli fail
```

## Konfiguracja
- **SSH alias:** `dokodu-vps`
- **App dir na serwerze:** `/srv/dokodu-app/app`
- **Branch produkcyjny:** `main`
- **GitHub Actions:** `.github/workflows/deploy.yml`

## Proces

### Krok 1: Sprawdź status lokalny
```bash
git status
git diff --stat origin/main 2>/dev/null || echo "brak remote tracking"
```
Jeśli są niezacommitowane zmiany — zapytaj użytkownika czy commitować (z jakim message).

### Krok 2: Commit jeśli potrzebny
Jeśli użytkownik potwierdzi commit:
```bash
git add -p   # lub konkretne pliki wskazane przez użytkownika
git commit -m "..."
```

### Krok 3: Push
```bash
git push origin main
```

### Krok 4: Pokaż link do GitHub Actions
Po pushu wyświetl:
```
Deploy uruchomiony. Śledź postęp:
https://github.com/[owner]/[repo]/actions
```
Pobierz owner/repo z: `git remote get-url origin`

### Krok 5 (opcjonalny): Sprawdź status serwera po ~3 min
```bash
ssh dokodu-vps "cd /srv/dokodu-app/app && docker ps --format 'table {{.Names}}\t{{.Status}}' | grep -E 'NAME|app|db'"
```

### Krok 6 (opcjonalny): Logi z serwera
```bash
ssh dokodu-vps "docker logs app --tail 50"
```

## Rollback (awaryjny)
Jeśli deploy się wysypał:
```bash
ssh dokodu-vps "cd /srv/dokodu-app/app && docker tag dokodu-next-app:prev dokodu-next-app:latest && docker compose up -d --force-recreate app"
```

## Output
- Potwierdzenie push
- Link do GitHub Actions
- (opcjonalnie) Status kontenerów i logi

## Zasady
- Nigdy nie pushuj bezpośrednio do main bez świadomości użytkownika — zawsze potwierdź
- Jeśli są uncommited zmiany — zawsze zapytaj o commit message, nie generuj go bez pytania
- Deploy.sh ma automatyczny rollback — nie panikuj przy błędach budowania
