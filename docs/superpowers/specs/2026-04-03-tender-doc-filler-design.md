# TenderScope Document Filler — MVP Design Spec

**Data:** 2026-04-03
**Cel:** Działające demo do oferty szacunkowej dla TenderScope sp. z o.o. (Borys Kowalik)
**Deadline:** 09.04.2026 godz. 10:00
**Kontekst:** Wycena modułu półautomatycznego uzupełniania danych wykonawcy w dokumentach przetargowych (DOCX). Projekt unijny FEPW "Platforma startowa HugeTECH Revolution".

---

## Problem

TenderScope potrzebuje modułu, który automatycznie wypełnia dane firmy (NIP, nazwa, adres itd.) w formularzach przetargowych DOCX. Pola nie mają placeholderów — rozpoznawanie "na podstawie treści".

## Walidacja POC

Przetestowano na 7 prawdziwych dokumentach od Borysa:
- **Regułowe (regex + tabele):** 24 pola wypełnione w 5/7 dokumentach (~70%)
- **2 dokumenty wymagają AI:** pola w paragrafach z opisami w nawiasach, wielokropki bez etykiet
- **Wniosek:** Podejście hybrydowe (reguły + AI fallback) pokrywa 100%

## Architektura

```
┌─────────────────────────────────────┐
│  Frontend (Next.js)                 │
│  Upload → Podgląd z highlight → DL  │
│  Toggle: [Regułowy] [AI] [Hybrid]   │
└──────────────┬──────────────────────┘
               │ REST API
┌──────────────▼──────────────────────┐
│  Backend (FastAPI)                   │
│  ┌────────────┐  ┌────────────────┐ │
│  │ Rule Engine │  │  AI Engine     │ │
│  │ python-docx │  │  Claude API    │ │
│  │ regex/table │  │  structured    │ │
│  └────────────┘  └────────────────┘ │
│  Profil użytkownika (JSON)          │
└──────────────────────────────────────┘
```

## API Endpoints

| Method | Path | Opis |
|--------|------|------|
| POST | `/api/upload` | Upload DOCX, zwraca document_id |
| POST | `/api/analyze/{doc_id}` | Analizuje pola (query param: mode=rule/ai/hybrid) |
| GET | `/api/preview/{doc_id}` | Lista wypełnionych pól z metadanymi |
| POST | `/api/fill/{doc_id}` | Generuje wypełniony DOCX do pobrania |
| GET | `/api/profile` | Dane firmy z profilu |
| PUT | `/api/profile` | Aktualizacja profilu |

## Rule Engine

Dwie strategie rozpoznawania:

1. **Table cell matching** — skanuje tabele, szuka etykiet w col0 (NIP, Firma, Adres...), wypełnia pustą col1
2. **Paragraph dot matching** — szuka wielokropków/kropek w paragrafach z rozpoznawalną etykietą przed nimi

Mapowanie: ~20 znanych etykiet (case-insensitive, z wariantami) → pola profilu.

## AI Engine

- **Model:** Claude Sonnet (szybki, ~$0.01/dokument)
- **Input:** Treść dokumentu z oznaczeniami pozycji ([P0], [T0R1] itd.) + profil firmy
- **Output:** Structured JSON — lista pól z location_id, label, suggested_value, confidence
- **Fallback:** Uruchamiany tylko dla pól nieznalezionych przez Rule Engine (tryb hybrid)

## Frontend UI

Jedna strona, 3 kroki:

### Krok 1 — Upload
- Drag & drop DOCX
- Karta "Profil firmy" z edytowalnymi polami (pre-filled)

### Krok 2 — Analiza + Podgląd
- Toggle trybów: Regułowy / AI / Hybrydowy
- Lista wypełnionych pól z kolorami:
  - 🟢 zielony = regułowe (pewne)
  - 🔵 niebieski = AI (do weryfikacji)
  - 🔴 czerwony = brak danych
- Statystyka: "Wypełniono X/Y pól"

### Krok 3 — Download
- Przycisk "Pobierz wypełniony dokument"
- Opcja "Pobierz raport" (JSON)

## Decyzje techniczne

| Decyzja | Wybór | Powód |
|---------|-------|-------|
| Podgląd dokumentu | Lista pól (nie render DOCX) | Prostsze, wystarczy na demo |
| Format wejściowy | Tylko DOCX | PDF edytowalne to stretch goal |
| Baza danych | Brak — JSON + /tmp | To demo, nie SaaS |
| Auth | Brak | Demo bez logowania |
| AI model | Claude Sonnet | Szybki, tani, structured output |
| Deploy | Docker na serwerze Dokodu | tender-demo.dokodu.it |

## Stack

**Backend:** Python 3.11+, FastAPI, python-docx, anthropic SDK, uvicorn
**Frontend:** Next.js 14, React, TypeScript, Tailwind CSS
**Deploy:** Docker Compose, nginx reverse proxy

## Scope MVP (do 09.04)

### Must have
- Upload DOCX
- Rule engine (tabele + wielokropki)
- AI engine (Claude)
- Tryb hybrydowy
- Podgląd wypełnionych pól z kolorami
- Download wypełnionego DOCX
- Profil firmy edytowalny
- Deploy na serwerze Dokodu

### Nice to have (po deadline)
- Obsługa PDF
- Batch upload (wiele dokumentów naraz)
- Historia dokumentów
- Porównanie side-by-side trybów

## Struktura projektu

```
tender-doc-filler/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── engines/
│   │   ├── rule_engine.py   # Regex + table matching
│   │   └── ai_engine.py     # Claude API
│   ├── models.py            # Pydantic schemas
│   ├── profile.py           # Zarządzanie profilem
│   └── requirements.txt
├── frontend/
│   ├── src/app/
│   │   └── page.tsx         # Single page app
│   ├── src/components/
│   │   ├── Upload.tsx
│   │   ├── FieldPreview.tsx
│   │   └── ProfileCard.tsx
│   ├── package.json
│   └── tailwind.config.ts
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
└── README.md
```

## Ryzyko

| Ryzyko | Mitigacja |
|--------|-----------|
| AI halucynuje wartości | Confidence scoring + kolor niebieski = "do weryfikacji" |
| Formatowanie DOCX się psuje | python-docx zachowuje style — testowane w POC |
| 5 dni to mało | Regułowy engine już działa (POC), frontend proste SPA |
| Brak API key Anthropic na serwerze | Skonfigurować przed deploy |
