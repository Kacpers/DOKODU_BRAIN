# TikTok Explainer Scenes — Design Spec

**Data:** 2026-04-16
**Status:** Approved

## Problem

Kanał TikTok Dokodu ma tylko jeden format — gadająca głowa. Potrzebujemy explainerów (tekst + animacje + muzyka, bez nagrywania) do przeplatania z talking head.

## Rozwiązanie

Biblioteka reużywalnych scen Remotion + JSON-driven pipeline. Claude pisze scenariusz (JSON), Remotion renderuje MP4, Kacper dodaje muzykę i publikuje.

## Sceny (6 kompozycji Remotion)

| Scena | Opis | Domyślny czas |
|---|---|---|
| KineticText | Animowane słowa kluczowe, emphasis na wybranym słowie | 3s |
| SlideCard | Karta z ikoną + nagłówek + bullets (stagger) | 5s |
| ScreenMockup | Animowany screenshot w ramce telefonu/monitora | 6s |
| StatCounter | Liczba odliczająca od 0 do targetu | 4s |
| VSCompare | Dwie kolumny side-by-side (X vs Y, przed/po) | 7s |
| CTACard | Logo Dokodu + CTA tekst | 3s |

## Przejścia (5 typów)

- `glitch` — RGB shift (2-3 klatki)
- `swipeUp` — następna scena od dołu
- `zoom` — zoom in → nowa scena
- `cut` — ostre cięcie
- `dissolve` — crossfade

## Format scenariusza (JSON)

```json
{
  "id": "T-033",
  "title": "ChatGPT vs Claude vs Gemini",
  "scenes": [
    { "type": "KineticText", "text": "Który AI wybrać?", "emphasis": "wybrać", "duration": 3 },
    { "type": "VSCompare", "left": { "title": "ChatGPT", "points": ["Obrazy", "Browsing"] }, "right": { "title": "Claude", "points": ["Dokumenty", "Kod"] }, "duration": 8 },
    { "type": "CTACard", "duration": 3 }
  ]
}
```

## Struktura plików

```
remotion/src/compositions/TikTok/Explainer/
  ├── ExplainerVideo.tsx       (root — czyta JSON, montuje Series)
  ├── scenes/
  │   ├── KineticText.tsx
  │   ├── SlideCard.tsx
  │   ├── ScreenMockup.tsx
  │   ├── StatCounter.tsx
  │   ├── VSCompare.tsx
  │   └── CTACard.tsx
  ├── transitions/
  │   └── Transitions.tsx
  └── Lookbook.tsx             (katalog demo)
```

## Pipeline

Nowa komenda w `tiktok_pipeline.py`:
- `explainer <json>` — renderuje explainera z JSON
- `lookbook` — renderuje katalog wszystkich scen
- `explainer-batch <folder>` — batch render

## Integracja ze skillem

Faza 1b w `/tiktok-pipeline`: generuje JSON scenariusza (zamiast tekstu telepromptera).
Ideas Bank: nowy format `Explainer`.

## Audio

Brak — MP4 renderowany bez audio. Kacper dodaje muzykę z platformy lub nagrany voiceover.

## Plan implementacji

1. Lookbook first — budowa scen + katalog wizualny do akceptacji
2. Feedback Kacpra — wybór animacji i przejść
3. Pipeline integration — komenda `explainer` w tiktok_pipeline.py
4. Skill update — faza 1b w `/tiktok-pipeline`
