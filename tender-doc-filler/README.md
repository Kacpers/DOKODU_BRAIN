# TenderScope Document Filler — MVP Demo

Automatyczne uzupełnianie danych wykonawcy w dokumentach przetargowych (DOCX).

## Quick Start (dev)

Backend:

    cd tender-doc-filler && pip install -r backend/requirements.txt
    uvicorn backend.main:app --reload --port 8000

Frontend:

    cd tender-doc-filler/frontend && npm install && npm run dev

## Docker

    docker build -t tender-filler .
    docker run -p 80:80 -e ANTHROPIC_API_KEY=sk-... tender-filler

## Tryby

- **Regułowy** — regex + table matching, szybki, 100% pewny na znanych polach
- **AI** — Claude Sonnet rozpoznaje pola z treści dokumentu
- **Hybrydowy** — reguły first, AI fallback dla nieznalezionych pól
