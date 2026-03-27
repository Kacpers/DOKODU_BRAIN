---
type: course-agenda
modul: 05
tytul: "Asystenci AI z Barierami Kontroli (Human-in-the-Loop)"
czas_total: "3h 00min"
projekt_tygodnia: "Slack Approval Bot"
status: draft
last_reviewed: 2026-03-27
---

# Modul 05 — Agenda nagrania (3h)

**Tytuł tygodnia:** Asystenci AI z Barierami Kontroli (Human-in-the-Loop)
**Projekt tygodnia:** Wirtualny Asystent na Slacku z Approval Flow

---

## SEGMENT 1: AI Agent Node w n8n — od zera do działającego agenta
**Czas: 0:00 – 0:35 (35 min)**

| Minuty | Zawartość | Format |
|--------|-----------|--------|
| 0:00–0:03 | **Hook + intro** — "AI bez kontroli to jak nowy pracownik z dostępem do wszystkiego" | Kamera na twarz |
| 0:03–0:08 | Przegląd tygodnia: co zbudujemy, czego się nauczymy | Slajd agendy |
| 0:08–0:20 | **AI Agent node** — anatomia, konfiguracja, system prompt, tools | Demo n8n |
| 0:20–0:28 | **Modele w n8n** — GPT-4o vs Claude 3.5 Sonnet vs Gemini 1.5 Pro: kiedy co | Slajd tabela |
| 0:28–0:35 | **Tools dla agenta** — HTTP Request, Code Node, Google Sheets jako narzędzia | Demo n8n |

---

## SEGMENT 2: Dlaczego pełna autonomia to ryzyko — i co z tym zrobić
**Czas: 0:35 – 1:10 (35 min)**

| Minuty | Zawartość | Format |
|--------|-----------|--------|
| 0:35–0:45 | **Demo: agent bez guardrails** — co może pójść nie tak (realne przykłady) | Demo n8n LIVE |
| 0:45–0:55 | **Human-in-the-Loop pattern** — AI robi 90%, człowiek decyduje 10% | Slajd diagram |
| 0:55–1:00 | **Zasada Minimalnych Uprawnień** dla AI agentów (Principle of Least Privilege) | Slajd |
| 1:00–1:05 | **Guardrails** — allow/deny lists, scope ograniczenia, rate limiting | Demo n8n |
| 1:05–1:10 | **Prompt injection** — czym jest, jak się przed nim bronić | Slajd + demo |

---

## PRZERWA: 5 minut
**Czas: 1:10 – 1:15**

---

## SEGMENT 3: Wait Node i Approval Flow — serce Human-in-the-Loop
**Czas: 1:15 – 1:55 (40 min)**

| Minuty | Zawartość | Format |
|--------|-----------|--------|
| 1:15–1:25 | **Wait node** — jak działa, webhook resume, timeout, expiry | Demo n8n |
| 1:25–1:35 | **Approval via Slack/Teams** — wysyłanie akcji do zatwierdzenia przez przyciski | Demo n8n + Slack |
| 1:35–1:45 | **Output validation** — sprawdź wynik AI zanim wykonasz akcję | Demo n8n |
| 1:45–1:55 | **Structured output** — wymuszenie JSON schema na odpowiedzi AI | Demo n8n |

---

## SEGMENT 4: Prompt Engineering dla n8n Agentów
**Czas: 1:55 – 2:25 (30 min)**

| Minuty | Zawartość | Format |
|--------|-----------|--------|
| 1:55–2:05 | **System prompt best practices** dla agentów n8n | Slajd + edytor |
| 2:05–2:15 | **Kontekst dynamiczny** — jak przekazywać dane z workflow do promptu | Demo n8n |
| 2:15–2:20 | **Błędy w promptach agentów** — top 5 najczęstszych | Slajd |
| 2:20–2:25 | **Prompt injection defense** — konkretne techniki | Demo n8n |

---

## SEGMENT 5: Budujemy Slack Approval Bot — projekt tygodnia LIVE
**Czas: 2:25 – 3:00 (35 min)**

| Minuty | Zawartość | Format |
|--------|-----------|--------|
| 2:25–2:30 | Przegląd architektury: 3 workflows, Slack App konfiguracja | Slajd diagram |
| 2:30–2:45 | **Live coding Workflow 1** — Slack Listener + AI Agent | Demo n8n LIVE |
| 2:45–2:55 | **Live coding Workflow 2+3** — Approval Sender + Approval Handler | Demo n8n LIVE |
| 2:55–3:00 | **Outro** — omówienie ćwiczeń, zadanie domowe, zapowiedź Tygodnia 6 | Kamera na twarz |

---

## Notatki dla reżysera / montażysty

- **Segmenty demo** nagrywać bez cięć — autentyczne pomyłki są OK, pokazują realne podejście do debugowania
- **Segment 2 (agent bez guardrails)** — przygotować oddzielne środowisko testowe żeby nie naruszać produkcji
- **Slajdy** po każdym demie — "co właśnie zobaczyłeś w 3 bulletach"
- **Lower thirds** przy każdym nowym pojęciu technicznym (Wait Node, Guardrail, etc.)
- **Timestamp chapters** do opisu na platformie kursowej zgodnie z agendą

---

## Materiały do przygotowania przed nagraniem

- [ ] n8n z zainstalowanym: HTTP Request, Code, Google Sheets, AI Agent nodes
- [ ] Konto OpenAI z kluczem API (GPT-4o) + konto Anthropic (Claude 3.5 Sonnet)
- [ ] Slack App z botscopes: `chat:write`, `commands`, `interactivity`, `channels:read`
- [ ] Ngrok lub publiczny URL do Slack webhooków podczas nagrania
- [ ] Konto Google z Google Sheet "Demo_Klienci" (10 wierszy testowych)
- [ ] Środowisko testowe (oddzielna instancja n8n) do demo "bez guardrails"
