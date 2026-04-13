---
name: brain-status
description: Wyswietla szybki przeglad stanu DOKODU_BRAIN — aktywne projekty, otwarte leady, inbox count, kluczowe deadliny. Dashboard w jednym spojrzeniu. Trigger slowa: "status brain", "co mam aktywnego", "co sie dzieje", "pokaz status", /brain-status
---

# Instrukcja: Brain Status Overview

Szybki, estetyczny przeglad stanu DOKODU_BRAIN. Nie analizuj glęboko — po prostu pokaz co jest.

## Odczytaj i wyswietl

### 1. Wczytaj dane
- `/home/kacper/DOKODU_BRAIN/000_DASHBOARD.md` — priorytety i projekty
- `/home/kacper/DOKODU_BRAIN/00_INBOX.md` — policz elementy z `- [ ]`
- `/home/kacper/DOKODU_BRAIN/10_PROJECTS/` — przejrzyj pliki projektow (health z frontmatter)
- `/home/kacper/DOKODU_BRAIN/20_AREAS/AREA_Marketing_Sales/CRM_Leady_B2B.md` — otwarte leady

### 2. Wyswietl w tym formacie

```
DOKODU BRAIN — STATUS [DATA DZISIAJ]
════════════════════════════════════

PROJEKTY AKTYWNE
  Animex Szkolenie     [ZOLTY]  Deadline: 20.03  Nastepny krok: ...
  Corleonis Wdrozenie  [ZIELONY] Deadline: 15.04  Nastepny krok: ...
  Kurs n8n Launch      [CZERWONY] Deadline: 31.03  Nastepny krok: ...

INBOX
  Elementow do przetworzenia: [X]
  Najstarsza notatka: [X] dni temu
  Status: [OK / Wymaga uwagi (>10) / Krytyczny (>20)]

CRM — PIPELINE
  Aktywnych leadow: [X]
  W fazie Discovery: [X]
  Propozycje wyslane: [X]
  Pipeline value: [X] PLN

KLIENCI
  Aktywni: [lista]
  Retainery: Corleonis — 3 000 PLN/mies.

NAJBLIZSZE DEADLINY (7 dni)
  [data] — [co]
  [data] — [co]

ALERTY (jezeli sa)
  ⚠️ [opis problemu]
```

### 3. Zaproponuj akcje

Na koncu dodaj max 2 rekomendacje:
- "Najwazniejsza rzecz teraz: [co]"
- "Jezeli masz 30 minut: [co]"

## ZASADY

- Jezeli projekt health=red → pokazuj jako PILNE
- Jezeli inbox > 15 elementow → ostrzez
- Jezeli lead czeka na odpowiedz > 48h → oznacz
- Format kolumnowy — czytelny w terminalu
- Nie analizuj — tylko prezentuj fakty
