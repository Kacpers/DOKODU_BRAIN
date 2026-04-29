---
name: crm-sync-from-master
description: Cherry-pickuje konkretny commit z master crm-new repo do forku prospekta (Faza 1+). Używane do propagacji bug fixów z mastera do klientów bez ręcznego copy-paste. Trigger: "syncuj fix do pedrollo", "cherry-pick {commit} do {slug}", /crm-sync-from-master {slug} {commit}.
---

# Instrukcja: CRM Sync From Master

## Działanie

Po Fazie 1 (fork) instancja klienta ma własne życie — zmiany w masterze nie auto-syncują. Gdy mamy bug fix w masterze (np. security patch, regression fix), używamy cherry-pick żeby propagować do każdego forku.

## KROK 1: Sprawdź dane wejściowe

Z prompta wyciągnij:
- `slug` — który prospekt (forked)
- `commit` — SHA commita z mastera (full lub prefix 7-10 znaków)

Jeśli nie podane — zapytaj.

## KROK 2: Sprawdź czy fork istnieje

```bash
gh repo view Kacpers/crm-<slug>
```

Jeśli 404 — powiedz "Brak forku — uruchom najpierw /crm-fork-prospekt {slug}" i przerwij.

## KROK 3: Sprawdź commit w masterze

```bash
cd /Users/ksieradzinski/Projects/dokodu/crm-new
git show <commit> --stat | head -10
```

Pokaż użytkownikowi co ten commit robi. Zapytaj: "Cherry-pick'ujemy ten commit do `crm-{slug}`?"

## KROK 4: Uruchom sync

```bash
./scripts/crm-sync-from-master.sh <slug> <commit>
```

Skrypt:
1. Klonuje fork do temp dir
2. Adds master jako remote
3. Fetches master commit
4. `git cherry-pick <commit>` (z `--strategy-option=theirs` na konflikty)
5. Push do fork main

Jeśli cherry-pick ma konflikty — skrypt zatrzymuje się, pokazuje gdzie je rozwiązać.

## KROK 5: Deploy

Po udanym cherry-picku zaproponuj:
```
Cherry-pick OK. Deploy zmiany do działającej instancji?
  /crm-update {slug}
```

## Uwagi

- Skrypt używa `--strategy-option=theirs` przy konfliktach — fork wygrywa. Jeśli dotykamy plików które klient zmodyfikował, ich zmiany zostają nadpisane. Dla bezpieczeństwa, sprawdź `git log {slug}@{1}..main` po cherry-picku zanim zrobisz update.
- Bug fixy w core-warstwach rzadko zmienianych (auth, audit, RBAC) cherry-pick'ują się czysto
- Bug fixy w warstwach modyfikowanych per-klient mogą wymagać ręcznego mergeu
- Po cherry-picku deploy do działającej instancji NIE jest automatyczny — wymaga jawnego `/crm-update`
