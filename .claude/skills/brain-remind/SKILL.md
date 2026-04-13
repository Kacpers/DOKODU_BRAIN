---
name: brain-remind
description: Dodaje przypomnienie z datą — jednocześnie do REMINDERS.md i do Google Calendar (przez MCP). Trigger: "przypomnij mi", "dodaj przypomnienie", "ustaw reminder", "zaplanuj", /brain-remind
---

# brain-remind

## Cel

Jeden skill = dwa miejsca: REMINDERS.md (dla cronowego injectu do INBOX) + Google Calendar event (natychmiastowe przypomnienie na telefonie).

## KROK 1: Zbierz dane

Jeśli nie podane, zapytaj tylko o:
1. **Co?** — treść przypomnienia
2. **Kiedy?** — data (i opcjonalnie godzina)

Nie pytaj o nic więcej.

## KROK 2: Zapisz do REMINDERS.md

Dopisz do sekcji "## Aktywne" w `/home/kacper/DOKODU_BRAIN/REMINDERS.md`:

```
- YYYY-MM-DD | BIZNES | [treść przypomnienia]
```

Dobierz kategorię automatycznie:
- `BIZNES` — klient, faktura, umowa, projekt
- `SEO` — blog, GSC, optymalizacja
- `YT` — YouTube, nagranie, publikacja
- `TECH` — serwer, kod, deployment
- `INNE` — wszystko inne

## KROK 3: Utwórz event w Google Calendar

Użyj `mcp__claude_ai_Google_Calendar__gcal_create_event` z parametrami:
- **title:** treść przypomnienia (zwięźle)
- **start:** podana data, godzina 9:00 jeśli nie podano
- **end:** start + 30 minut
- **description:** pełny kontekst jeśli dostępny
- **calendar:** primary (domyślny)

## KROK 4: Potwierdź

Odpowiedz jednym zdaniem:
"Reminder ustawiony na [data]: [treść] — dodano do REMINDERS.md i Google Calendar."

## ZASADY

- Jeśli użytkownik podaje względną datę ("w piątek", "za tydzień") → przelicz na bezwzględną na podstawie dzisiejszej daty
- Jeśli godzina nie podana → ustaw 9:00
- Nie pytaj o potwierdzenie przed zapisem — działaj od razu
- Dla przypomnień związanych z klientem → dodaj nazwę klienta w tytule Calendar eventu
