# CRM ↔ BRAIN Bidirectional Sync — Design Spec

**Data:** 2026-04-02
**Autor:** Kacper + Claude
**Status:** APPROVED

---

## Problem

Dokodu ma dwa systemy:
- **BRAIN** (DOKODU_BRAIN, git repo, markdown) — Kacper pracuje tu codziennie via Claude Code
- **CRM** (system.dokodu.it, Next.js + PostgreSQL) — web UI dla zespolu (Alina)

Dane zyja glownie w BRAIN. Alina nie ma wgladu w pipeline, outreach, aktywnosc klientow. CRM jest pusty lub niezsynchronizowany. Potrzebny dwukierunkowy sync.

---

## Decyzje architektoniczne

1. **BRAIN = zrodlo prawdy** — Kacper pracuje w Claude Code, CRM jest "ladnym interfejsem"
2. **Dwukierunkowy sync** — zmiany Aliny w CRM trafiaja z powrotem do BRAIN
3. **Near real-time (co 5 min)** — cron na VPS, obie strony
4. **Last-write-wins na poziomie pola** — konflikt rozwiazywany przez timestamp per pole (nie per entity)
5. **GitHub jako posrednik** — sync daemon na VPS klonuje repo, commituje, pushuje. Kacper pulluje na starcie sesji
6. **Zero AI w CRM** — CRM = dane + widocznosc. Analizy, decyzje = Claude Code + BRAIN
7. **Wartosci dealow** — sync przenosi, ale Claude Code NIGDY nie wpisuje bez potwierdzenia Kacpra

---

## Architektura

```
Kacper (WSL)                    VPS (57.128.219.9)
┌─────────────┐                 ┌─────────────────────────┐
│ DOKODU_BRAIN│◄──git push/pull─│ BRAIN clone (bare/work) │
│ (local git) │                 │                         │
└─────────────┘                 │ ┌─────────────────────┐ │
                                │ │   Sync Daemon       │ │
                                │ │  (Python, systemd)  │ │
                                │ │                     │ │
                                │ │ BRAIN→CRM (5 min)   │ │
                                │ │ CRM→BRAIN (5 min)   │ │
                                │ └──────────┬──────────┘ │
                                │            │            │
                                │ ┌──────────▼──────────┐ │
                                │ │   CRM App           │ │
                                │ │  (Next.js + PG)     │ │
                                │ │  system.dokodu.it   │ │
                                │ └─────────────────────┘ │
                                └─────────────────────────┘
                                            │
                                    Alina (przegladarka)
```

### Git flow

1. **Kacper edytuje BRAIN** → commit + push do GitHub
2. **Sync daemon** (co 5 min) → `git pull` na VPS clone → parsuje diff → aktualizuje CRM via API
3. **Alina edytuje w CRM** → zmiana zapisana w PG
4. **Sync daemon** (co 5 min) → pobiera zmiany z CRM API (`/api/changes`) → edytuje pliki MD → commit + push do GitHub
5. **Kacper otwiera sesje** → Claude Code robi `git pull` → widzi zmiany Aliny

---

## Sync Daemon — szczegoly

### Jezyk: Python 3
### Lokalizacja: VPS, systemd service (lub Docker container obok CRM)
### Config: `~/.config/dokodu/sync_config.json`

```json
{
  "brain_repo_path": "/srv/dokodu-brain",
  "crm_base_url": "https://system.dokodu.it",
  "crm_api_key_file": "~/.config/dokodu/crm_api_key",
  "sync_interval_seconds": 300,
  "git_remote": "origin",
  "git_branch": "main",
  "commit_author": "BRAIN Sync Daemon <sync@dokodu.it>"
}
```

### BRAIN → CRM: co parsuje

| Plik BRAIN | Co wyciaga | Endpoint CRM |
|------------|-----------|--------------|
| `CRM_Leady_B2B.md` | Pipeline table: firma, kontakt, etap, wartosc, nastepny krok, deadline | `PUT /api/deals/{id}` lub `POST /api/deals` |
| `Outreach_Tracker.md` | Outreach table (uwaga: multi-row per firma, np. 6a/6b/6c, note-rows, sekcja Kolejka) | `PUT /api/contacts/{id}`, `POST /api/activities` |
| `AREA_Customers/*/Profile.md` | YAML frontmatter + sekcje: firma, kontakty, biznes context | `PUT /api/companies/{id}`, `PUT /api/contacts/{id}` |
| `AREA_Customers/*/Meetings.md` | Nowe sekcje `## YYYY-MM-DD` od ostatniego sync | `POST /api/activities` (type=MEETING) |
| `REMINDERS.md` | Nowe linie z data + tresc | `POST /api/tasks` (z dueDate) |
| `PLAN_TYGODNIA.md` | **Poza scope v1** — nie syncujemy, zbyt zmienny format |

**Logika parsowania:**
- Daemon przechowuje `last_synced_commit` SHA w pliku stanu (`/srv/dokodu-brain/.sync_state.json`)
- Wykrywanie zmian: `git diff {last_synced_sha}..HEAD --name-only` (nie HEAD~1!)
- Parser per typ pliku (markdown table parser, YAML frontmatter parser, meeting section parser)
- **Identity mapping:** kazdy entity w BRAIN ma `crm_id` w YAML frontmatter (Profile.md) lub komentarzu HTML w tabeli MD. CRM przechowuje `brain_path` w metadata. Mapping persystowany w `.sync_mapping.json`
- Jesli firma/deal nie istnieje w CRM → tworzy nowy, zapisuje crm_id do BRAIN
- Jesli istnieje → aktualizuje TYLKO zmienione pola (field-level, nie entity-level)

**Identity mapping (B1 fix):**
- Profile.md: `crm_id: cmp_abc123` w YAML frontmatter
- CRM_Leady_B2B.md: `<!-- crm:deal_xyz -->` komentarz HTML na koncu wiersza (niewidoczny w renderze)
- Outreach_Tracker.md: `<!-- crm:contact_xyz -->` analogicznie
- Fallback: fuzzy name match, ale ZAWSZE zapisz ID po pierwszym match
- `.sync_mapping.json` jako dodatkowy cache: `{"Animex": {"company_id": "cmp_001", "brain_path": "AREA_Customers/Animex"}}`

**Obsluga usuniec (B4 fix):**
- Usuniecie wiersza z BRAIN pipeline → CRM: soft-delete (status=DEFERRED, nie fizyczny delete)
- Usuniecie w CRM → BRAIN: przeniesienie do sekcji "Nurturing" lub "Odlozone" (nie usuwaj wiersza)
- Przeniesienie katalogu klienta do `40_ARCHIVE/` → CRM: status=FORMER_CLIENT
- Daemon NIGDY nie robi fizycznych deletow — tylko zmienia statusy

### CRM → BRAIN: co pisze

| Zmiana w CRM | Co pisze w BRAIN | Plik |
|-------------|-----------------|------|
| Deal stage change (drag & drop) | Aktualizacja wiersza w pipeline table | `CRM_Leady_B2B.md` |
| Deal value/deadline edit | Aktualizacja wiersza | `CRM_Leady_B2B.md` |
| Nowy komentarz (Alina) | Sekcja `### Komentarz (Alina, YYYY-MM-DD)` | `AREA_Customers/*/Meetings.md` |
| Nowa flaga "wymaga uwagi" | Emoji marker w pipeline table + notatka | `CRM_Leady_B2B.md` |
| Nowy kontakt/firma | Nowy wiersz w pipeline | `CRM_Leady_B2B.md` |
| Task completed | `[x]` zamiast `[ ]` | odpowiedni plik |
| Edycja profilu firmy | Aktualizacja sekcji | `AREA_Customers/*/Profile.md` |
| Nowa aktywnosc (call, email) | Nowa sekcja w Meetings.md | `AREA_Customers/*/Meetings.md` |

**Logika zapisu:**
- Pobiera zmiany z `GET /api/changes?since={last_sync_timestamp}&limit=100`
- Dla kazdej zmiany: otwiera odpowiedni plik MD, edytuje TYLKO dotkniety fragment
- **Strategia edycji MD:** uzywa sync markerow w plikach:
  - `CRM_Leady_B2B.md`: tabela pipeline otoczona `<!-- SYNC:PIPELINE -->` ... `<!-- /SYNC:PIPELINE -->`. Daemon regeneruje TYLKO te sekcje, reszta pliku (protokol kwalifikacji, discovery framework, templates) nienaruszona
  - `Outreach_Tracker.md`: analogicznie `<!-- SYNC:OUTREACH -->` ... `<!-- /SYNC:OUTREACH -->`
  - `Profile.md`: YAML frontmatter edytowany przez `ruamel.yaml` (zachowuje formatowanie). Sekcje tekstowe: append-only (komentarze Aliny)
  - `Meetings.md`: nowe sekcje wstawiane chronologicznie na poczatek (najnowsze pierwsze)
- `git add CRM_Leady_B2B.md Outreach_Tracker.md [zmienione pliki] && git commit -m "sync: CRM → BRAIN [auto]" && git push`
- NIE uzywaj `git add -A` — tylko explicite zmienione pliki

**Obsluga bledow sync:**
- Git push conflict → `git pull --rebase`. Jesli rebase fail (merge conflict):
  1. `git rebase --abort`
  2. Log konflikt do `/var/log/dokodu-sync/conflicts.log`
  3. Wyslij notyfikacje do CRM (Notification type=SYNC_CONFLICT)
  4. Skip ten cykl, retry w nastepnym
- Lock file `/tmp/dokodu-sync.lock` — jesli istnieje i PID zyje, skip cykl (zapobiega concurrent runs)

### Nowy endpoint CRM: `/api/changes`

```
GET /api/changes?since=2026-04-02T10:00:00Z

Response:
{
  "changes": [
    {
      "id": "ch_001",
      "entity": "deal",
      "entityId": "deal_123",
      "action": "update",
      "fields": {"stage": "Propozycja", "value": 62000},
      "user": "alina",
      "timestamp": "2026-04-02T10:15:00Z",
      "metadata": {"previousStage": "Discovery"}
    },
    {
      "id": "ch_002",
      "entity": "activity",
      "entityId": "act_456",
      "action": "create",
      "fields": {"type": "COMMENT", "subject": "Wymaga uwagi", "description": "Gibula nie odpowiada na emaile"},
      "user": "alina",
      "timestamp": "2026-04-02T10:20:00Z",
      "relatedCompany": "Adm. Gibula"
    }
  ],
  "syncCursor": "2026-04-02T10:20:00Z"
}
```

**Implementacja:** Change tracking table w PG — trigger na INSERT/UPDATE/DELETE kluczowych tabel, zapisuje do `change_log`. Endpoint czyta z `change_log` filtrujac po `since`.

- Index na `change_log.timestamp` (wydajnosc query)
- Retencja: wpisy starsze niz 30 dni usuwane przez cron
- Paginacja: `limit` + `syncCursor` w response
- Daemon API key: dedykowany user "sync-daemon" z rola ADMIN w CRM (pelne uprawnienia r/w)

---

## Nowe funkcje CRM (web UI)

### 1. Dashboard z pipeline Kanban
- Kolumny = etapy pipeline (Nowy, Kontakt, Discovery, Propozycja, Negocjacje, Wygrana, Przegrana)
- Karty = deale (firma, wartosc, deadline, nastepny krok)
- Drag & drop zmienia etap → loguje Activity → sync do BRAIN
- Sumy per kolumna + total pipeline value + weighted (probability × value)

### 2. Outreach Board
- Tabela/Kanban statusow LinkedIn: zaproszenie → zaakceptowane → DM → odpowiedz → call → propozycja
- Per firma: lista osob z ich statusem
- Follow-up dates z wizualnym alertem (czerwony = przeterminowany)
- Filtr: "do obslugi dzis" (follow-up date = today)

### 3. Unified Timeline per klient
- Chronologiczna lista aktywnosci z obu zrodel (BRAIN + CRM)
- Typy: meeting, call, email, comment, stage_change, value_change, note
- Kazdy wpis: kto (Kacper/Alina/sync), kiedy, co
- Mozliwosc dodania komentarza inline

### 4. Komentarze i flagi
- Na kazdym dealu i firmie: przycisk "Dodaj komentarz"
- Flaga "Wymaga uwagi" (toggle) — widoczna na dashboardzie
- Komentarze synchronizowane do BRAIN jako sekcje w Meetings.md

---

## Data Cleanup (dzien zero)

Przed uruchomieniem sync:
1. Usunac zmyslona wartosc Cichy-Zasada (25 000 PLN) z CRM
2. Usunac niezatwierdzona wycene Corleonis (8 900 PLN) z CRM
3. Odpalic BRAIN → CRM full import (wszystkie pliki, nie tylko diff)
4. Zweryfikowac stan po imporcie z Kacprem

---

## Scope v1 — co budujemy

| # | Komponent | Lokalizacja | Opis |
|---|-----------|-------------|------|
| 1 | Change tracking (DB trigger + table) | CRM app (Prisma migration) | Trigger na deals, companies, contacts, activities, tasks → change_log |
| 2 | Endpoint `/api/changes` | CRM app (API route) | Zwraca change feed od podanego timestamp |
| 3 | Sync daemon: BRAIN→CRM | Nowy skrypt Python, VPS | Parsuje MD diff, pushuje do CRM API |
| 4 | Sync daemon: CRM→BRAIN | Nowy skrypt Python, VPS | Czyta change feed, pisze MD, commituje |
| 5 | Outreach Board (UI) | CRM app (nowa strona) | Kanban/tabela LinkedIn outreach |
| 6 | Komentarze/flagi | CRM app (komponent) | Per deal/firma, z sync do BRAIN |
| 7 | Dashboard Kanban | CRM app (rozbudowa) | Pipeline drag&drop + wartosci |
| 8 | Unified Timeline | CRM app (rozbudowa) | Chronologiczna aktywnosc z obu zrodel |
| 9 | Data cleanup skrypt | Jednorazowy | Czysci CRM + importuje baseline z BRAIN |
| 10 | Auto git pull hook | Claude Code hook | `git pull` na starcie sesji |

## Poza scope (v2+)

- Upload nagran rozmow + Whisper transkrypcja
- Gmail thread sync (wymaga naprawy OAuth token)
- Automatyczne scoringi/raporty w CRM
- Mobile app / PWA

---

## Observability

- Logi daemon: `/var/log/dokodu-sync/sync.log` (rotacja dzienna, 7 dni)
- Konflikty: `/var/log/dokodu-sync/conflicts.log`
- **Endpoint `/api/sync/status`** w CRM — zwraca last successful sync timestamp, errors count, widoczny w UI footer ("Ostatni sync: 2 min temu")
- Notyfikacja w CRM jesli sync nie dzialal >15 min

## Migracja istniejacego crm_sync.py

Obecny `scripts/crm_sync.py` (manual CLI: push-meeting, push-lead, pull-pipeline, pull-company):
- **Zachowaj** jako narzedzie CLI do jednorazowych operacji
- **Wyciagnij** wspolna logike parsowania MD do biblioteki `lib/brain_parser.py` uzytej przez oba
- Daemon uzywa tej samej biblioteki, crm_sync.py staje sie lekkim CLI wrapperem

## Outreach Tracker — specyfikacja parsera

Format Outreach_Tracker.md jest zlozony:
- Multi-row per firma: `6a`, `6b`, `6c`, `6d` = rozni ludzie w tej samej firmie
- Note-rows: `5b-note` = dodatkowy komentarz (nie kontakt)
- Sekcja `## Kolejka` = osobna tabela z innymi kolumnami (nie syncujemy do CRM, to backlog)
- Separator firmowy: numer bez litery (np. `6`) vs sublinie (np. `6a`)

Parser musi:
1. Grupowac wiersze po numerze firmy (1, 2a/2b/2c, 3, 4a/4b/4c itd.)
2. Ignorowac note-rows (suffix `-note`)
3. Parsowac TYLKO sekcje `## Pipeline Aktywny`, ignorowac `## Kolejka`
4. Kazdy kontakt = osobny Contact w CRM, powiazany z Company

## Ryzyko

| Ryzyko | Mitygacja |
|--------|-----------|
| Konflikt edycji (Kacper + Alina rownolegle) | Field-level last-write-wins + audit log. W praktyce: Kacper edytuje pipeline/outreach, Alina dodaje komentarze — male ryzyko kolizji na tym samym polu |
| Parser MD sie psuje na nietypowym formacie | Testy jednostkowe per typ pliku. Fallback: skip wiersz i log warning (nie crash) |
| Sync daemon padnie | systemd restart=always + monitoring (/api/sync/status). Alert jesli >15 min bez sync |
| Git push conflict | Rebase → jesli fail: abort, log, notify, skip cykl |
| Concurrent daemon runs | Lock file /tmp/dokodu-sync.lock z PID check |
| Dane w CRM z dupy (zmyslone wartosci) | Daemon NIGDY nie generuje wartosci — tylko przenosi. Data cleanup przed startem |
