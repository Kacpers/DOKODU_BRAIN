---
name: crm-fork-prospekt
description: Forkuje instancję CRM z monorepo do osobnego prywatnego repo na GitHubie po pierwszym pozytywnym demie. Trigger: "forkuj prospekta", "odetnij pępowinę", "forkuj demo do osobnego repo", /crm-fork-prospekt {slug}.
---

# Instrukcja: CRM Fork Prospekt

## Działanie

Faza 0 → Faza 1 transition. Po pierwszym demie gdzie klient powiedział "TAK w 80%", forkujemy demo z monorepo `crm-new` do osobnego prywatnego repo `Kacpers/crm-{slug}`. Od teraz instancja klienta ma własne życie — schema/code zmiany u nich nie wpływają na master.

## KROK 1: Wyciągnij slug z prompta

Z prompta wyciągnij slug klienta (np. `pedrollo`, `haba`).

Wyświetl użytkownikowi: "Forkuję `crm-{slug}` do osobnego repo `Kacpers/crm-{slug}`. Od tego momentu zmiany w masterze NIE będą auto-syncować do tej instancji — zmiany trzeba propagować przez `/crm-sync-from-master` (cherry-pick)."

Zapytaj: "Potwierdzasz? (yes/no)"

## KROK 2: Sprawdź gh CLI auth

```bash
gh auth status
```

Jeśli niezalogowany — powiedz: "Zaloguj się do gh: `gh auth login`" i przerwij.

## KROK 3: Uruchom fork script

```bash
cd /Users/ksieradzinski/Projects/dokodu/crm-new
./scripts/crm-fork-prospekt.sh <slug>
```

Skrypt:
1. Sprawdza czy `themes/{slug}/` istnieje
2. Tworzy prywatny repo `Kacpers/crm-{slug}` na GitHubie (jeśli jeszcze nie ma)
3. Klonuje monorepo do temp dir, ustawia origin na fork
4. Scrubuje themes/ innych klientów (żeby nie wycieky do forku)
5. Push initial commit jako baseline forku

Wyświetl wynikowy URL repo (`https://github.com/Kacpers/crm-{slug}`) i ścieżkę temp checkoutu.

## KROK 4: Następne kroki

Powiedz użytkownikowi:
```
✅ Fork done.

Aby zmieniać kod tej instancji — pracuj w nowym repo:
  cd /tmp/dokodu-fork-{slug}-XXXX
  git push origin main
  ./scripts/deploy-instance.sh {slug} --bundle distribution-b2b

Aby propagować bug fix z mastera:
  /crm-sync-from-master {slug} <commit-sha>

Aby migrować na ich produkcję (Faza 2):
  /crm-migrate-to-prod {slug} <client-server>
```

## Uwagi

- Fork NIE zmienia obecnie działającego demo na `dev.dokodu.it/crm-{slug}` — to nadal działa, tylko źródło prawdy się zmienia
- Po fork'u, kolejny `./scripts/crm-update.sh {slug}` zacznie pullować z fork repo, nie z mastera
- Fork repo jest PRIVATE — tylko Dokodu zespół widzi
