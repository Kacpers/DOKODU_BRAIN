---
type: course-index
status: living-document
owner: kacper
last_reviewed: 2026-03-27
tags: [kurs, n8n, indeks, produkcja, pipeline]
---

# Kurs n8n + AI (Kacper Sieradziński / Dokodu) — Indeks Materiałów

> Ten plik to Mission Control dla całego kursu. Sprawdzaj przed każdą sesją nagraniową — co jest gotowe, co blokuje, jaka kolejność.

---

## Szybki status

| Moduł | Tytuł | Czas | Pliki gotowe | Status nagrania |
|:---:|---|:---:|:---:|:---:|
| 00 | Filozofia Automatyzacji *(FREE)* | ~45 min | 5/5 | ❌ |
| 01 | Fundamenty n8n | ~3h | 4/5 | ❌ |
| 02 | API i Dane | ~2h 05min | 4/5 | ❌ |
| 03 | Skalowalność i Odporność | ~4h | 4/5 | ❌ |
| 04 | Architektura Modularna | ~3h | 4/5 | ❌ |
| 05 | AI Human-in-the-Loop | ~3h | 3/5 | ❌ |
| 06 | Autonomous Agents | ~4h | 2/5 | ❌ |
| 07 | RAG — Cyfrowy Mózg Firmy | ~3h | 5/5 | ❌ |
| BONUS A | Bezpieczeństwo i Compliance | ~1h 30min | 5/5 | ❌ |
| BONUS B | Sprzedaż i Delivery | ~2h | 3/5 | ❌ |
| **SUMA** | | **~26h materiału** | **39/50** | |

---

## Jak korzystać z materiałów

### Struktura każdego modułu (5 plików)

```
01_Agenda.md         — Plan nagrania (segmenty, czasy, wskazówki produkcyjne)
02_Prezentacja.md    — Slajdy (Markdown → eksportuj do Canva/PowerPoint)
03_Skrypt.md         — Pełny skrypt do mówienia (z promptami dla prowadzącego)
04_Cwiczenia.md      — Ćwiczenia praktyczne dla uczestników kursu
05_Workflow_Blueprint.md — Gotowe workflow do skopiowania (JSON / szablony)
```

### Workflow produkcyjny (kolejność na każdy moduł)

```
1. Przeczytaj 01_Agenda.md (10 min) — zrozum strukturę i timing
2. Przejrzyj 02_Prezentacja.md — sprawdź czy slajdy są gotowe
3. Przeczytaj 03_Skrypt.md na głos (rehearsal) — minimum dzień przed nagraniem
4. Przetestuj workflow z 05_Blueprint na działającym n8n — dzień przed nagraniem
5. Nagraj — w kolejności segmentów z Agendy
6. Oznacz status w tym README jako ✅ po zaakceptowaniu przez edytora
```

### Zasady nagrywania

- Nagraj w blokach max 2h — potem przerwa. Głos i koncentracja spadają.
- Każdy segment to osobny plik wideo — edytor skleja w całość.
- Miej działające n8n na ekranie — demo live, nie slajdy z screenshotami.
- Błąd podczas demo? Nie przerywaj nagrania — powiedz "zróbmy to jeszcze raz" i powtórz segment.
- Nagraj minimum 2 wersje INTRO każdego modułu — wybierzesz lepszą w edycji.

---

## Szczegółowy indeks modułów

---

### MODUŁ 00 — Filozofia Automatyzacji *(FREE / Lead Magnet)*

**Katalog:** `Modul_00_Filozofia/`
**Czas całkowity:** ~45 minut
**Format:** Solo Kacper, twarz + prezentacja
**Cel:** Przekonać widza że n8n to właściwy wybór i że warto kupić resztę kursu
**Publiczność docelowa:** Przedsiębiorcy i freelancerzy bez doświadczenia w automatyzacji

| # | Plik | Status | Uwagi |
|---|------|:------:|-------|
| 01 | `01_Agenda.md` | ✅ | Gotowe |
| 02 | `02_Prezentacja.md` | ✅ | Gotowe |
| 03 | `03_Skrypt.md` | ✅ | Gotowe |
| 04 | `04_Cwiczenia.md` | ✅ | Gotowe |
| 05 | `05_Workflow_Blueprint.md` | ✅ | Gotowe |

**Nagranie:** ❌ Nie nagrane
**Priorytet nagrania:** 1 (nagrywaj jako pierwsze — blokuje pre-launch)

**Kluczowe momenty do podkreślenia podczas nagrania:**
- Hook na start: "Za 45 minut będziesz wiedział co automatyzować PIERWSZY"
- RODO jako argument za n8n vs Zapier/Make (dane w Polsce)
- Demo live: prosty workflow w 5 minut (Webhook → Slack)

---

### MODUŁ 01 — Fundamenty n8n i Pierwsza Automatyzacja

**Katalog:** `Modul_01_Fundamenty/`
**Czas całkowity:** ~3 godziny
**Format:** 12 segmentów × 10–20 minut, przemienne teoria/DEMO
**Projekt tygodnia:** Lead Capture System
**Cel:** Uczestnik ma działający workflow i rozumie podstawowe koncepcje n8n

| # | Plik | Status | Uwagi |
|---|------|:------:|-------|
| 01 | `01_Agenda.md` | ✅ | Gotowe |
| 02 | `02_Prezentacja.md` | ✅ | Gotowe |
| 03 | `03_Skrypt.md` | ✅ | Gotowe |
| 04 | `04_Cwiczenia.md` | ✅ | Gotowe |
| 05 | `05_Workflow_Blueprint.md` | ❌ | Brakujący plik |

**Nagranie:** ❌ Nie nagrane
**Priorytet nagrania:** 2

**Uwaga produkcyjna:** Podziel na dwie sesje (Seg. 1–6 i Seg. 7–12). Miej przygotowane środowisko Docker + ngrok przed nagraniem.

---

### MODUŁ 02 — Język Sieci: API i Transformacje Danych

**Katalog:** `Modul_02_API_i_Dane/`
**Czas całkowity:** ~2h 05min
**Format:** 6 segmentów, każdy kończy się cliffhangerem
**Projekt tygodnia:** Multi-API Data Pipeline
**Cel:** Uczestnik rozumie HTTP, REST API, i potrafi transformować dane w Code Node

| # | Plik | Status | Uwagi |
|---|------|:------:|-------|
| 01 | `01_Agenda.md` | ✅ | Gotowe |
| 02 | `02_Prezentacja.md` | ✅ | Gotowe |
| 03 | `03_Skrypt.md` | ✅ | Gotowe |
| 04 | `04_Cwiczenia.md` | ✅ | Gotowe |
| 05 | `05_Workflow_Blueprint.md` | ❌ | Brakujący plik |

**Nagranie:** ❌ Nie nagrane
**Priorytet nagrania:** 3

---

### MODUŁ 03 — Skalowalność, Odporność i Disaster Prevention

**Katalog:** `Modul_03_Skalowalnosc/`
**Czas całkowity:** ~4 godziny (dwie sesje po 2h)
**Format:** Teoria + DEMO + "co gdy padnie" live scenarios
**Projekt tygodnia:** Production-Ready Error Handling System
**Cel:** Workflow które nie padają po cichu — error handling, retry, alerting

| # | Plik | Status | Uwagi |
|---|------|:------:|-------|
| 01 | `01_Agenda.md` | ✅ | Gotowe |
| 02 | `02_Prezentacja.md` | ✅ | Gotowe |
| 03 | `03_Skrypt.md` | ✅ | Gotowe |
| 04 | `04_Cwiczenia.md` | ✅ | Gotowe |
| 05 | `05_Workflow_Blueprint.md` | ❌ | Brakujący plik |

**Nagranie:** ❌ Nie nagrane
**Priorytet nagrania:** 4

**Uwaga produkcyjna:** Ten moduł wymaga DWÓCH sesji nagraniowych. Zaplanuj z marginesem. Moduł 4h jest najdłuższy w kursie.

---

### MODUŁ 04 — Architektura Modularna: Koniec z Chaosem

**Katalog:** `Modul_04_Architektura_Modularna/`
**Czas całkowity:** ~3 godziny
**Format:** Diagnoza + live refactoring istniejącego workflow
**Projekt tygodnia:** Refactor "spaghetti" workflow do architektury modularnej
**Cel:** Uczestnik wie jak budować workflow które można utrzymywać po roku

| # | Plik | Status | Uwagi |
|---|------|:------:|-------|
| 01 | `01_Agenda.md` | ✅ | Gotowe |
| 02 | `02_Prezentacja.md` | ✅ | Gotowe |
| 03 | `03_Skrypt.md` | ✅ | Gotowe |
| 04 | `04_Cwiczenia.md` | ✅ | Gotowe |
| 05 | `05_Workflow_Blueprint.md` | ❌ | Brakujący plik |

**Nagranie:** ❌ Nie nagrane
**Priorytet nagrania:** 5

---

### MODUŁ 05 — Asystenci AI z Barierami Kontroli (Human-in-the-Loop)

**Katalog:** `Modul_05_AI_Human_in_Loop/`
**Czas całkowity:** ~3 godziny
**Format:** Teoria AI + DEMO Slack Approval Bot krok po kroku
**Projekt tygodnia:** Slack Approval Bot z OpenAI
**Cel:** Uczestnik buduje agenta AI który pyta człowieka przed podjęciem decyzji

| # | Plik | Status | Uwagi |
|---|------|:------:|-------|
| 01 | `01_Agenda.md` | ✅ | Gotowe |
| 02 | `02_Prezentacja.md` | ✅ | Gotowe |
| 03 | `03_Skrypt.md` | ✅ | Gotowe |
| 04 | `04_Cwiczenia.md` | ❌ | Brakujący plik |
| 05 | `05_Workflow_Blueprint.md` | ❌ | Brakujący plik |

**Nagranie:** ❌ Nie nagrane
**Priorytet nagrania:** 6

---

### MODUŁ 06 — Autonomiczne Agenty AI — MASTERCLASS

**Katalog:** `Modul_06_Autonomous_Agents/`
**Czas całkowity:** ~4 godziny
**Format:** 9 segmentów — Deep Dive z pełnym agentem produkcyjnym
**Projekt tygodnia:** Autonomous Research & Report Agent
**Cel:** Uczestnik buduje agenta który samodzielnie realizuje zadania wieloetapowe

| # | Plik | Status | Uwagi |
|---|------|:------:|-------|
| 01 | `01_Agenda.md` | ✅ | Gotowe |
| 02 | `02_Prezentacja.md` | ✅ | Gotowe |
| 03 | `03_Skrypt.md` | ❌ | Brakujący plik |
| 04 | `04_Cwiczenia.md` | ❌ | Brakujący plik |
| 05 | `05_Workflow_Blueprint.md` | ❌ | Brakujący plik |

**Nagranie:** ❌ Nie nagrane
**Priorytet nagrania:** 7

**Uwaga:** Moduł 06 wymaga ukończenia wszystkich 5 plików przed nagraniem. Najdłuższy poza Mod. 03.

---

### MODUŁ 07 — Cyfrowy Mózg Firmy (RAG) i Eliminacja Halucynacji

**Katalog:** `Modul_07_RAG/`
**Czas całkowity:** ~3 godziny
**Format:** Teoria RAG + live budowa Company Knowledge Assistant
**Projekt tygodnia:** Firmowy Asystent Wiedzy (Google Drive → Qdrant → Slack)
**Cel:** Uczestnik buduje system RAG który cytuje źródła i nie halucynuje

| # | Plik | Status | Uwagi |
|---|------|:------:|-------|
| 01 | `01_Agenda.md` | ✅ | Gotowe |
| 02 | `02_Prezentacja.md` | ✅ | Gotowe |
| 03 | `03_Skrypt.md` | ✅ | Gotowe |
| 04 | `04_Cwiczenia.md` | ✅ | Gotowe |
| 05 | `05_Workflow_Blueprint.md` | ✅ | Gotowe |

**Nagranie:** ❌ Nie nagrane
**Priorytet nagrania:** 8

**Uwaga produkcyjna:** Wymaga działającego Qdrant (Docker) i połączenia z Google Drive. Przetestuj co najmniej 2 dni przed nagraniem.

---

### MODUŁ BONUS A — Bezpieczeństwo i Compliance (n8n + RODO + AI Act)

**Katalog:** `Modul_BONUS_Bezpieczenstwo/`
**Czas całkowity:** ~1h 30min
**Format:** Kacper (tech) + Alina (prawo) — nagranie wspólne, podział segmentów
**Cel:** Uczestnik wie jak budować i wdrażać n8n zgodnie z RODO i AI Act 2024
**Wyjątkowość:** Jedyny moduł w Polsce łączący n8n + RODO + AI Act praktycznie

| # | Plik | Status | Uwagi |
|---|------|:------:|-------|
| 01 | `01_Agenda.md` | ✅ | Gotowe |
| 02 | `02_Prezentacja.md` | ✅ | Gotowe |
| 03 | `03_Skrypt.md` | ✅ | Gotowe |
| 04 | `04_Cwiczenia.md` | ✅ | Gotowe |
| 05 | `05_Workflow_Blueprint.md` | ✅ | Gotowe — HMAC, pseudonimizacja, audit log, RTBF, checklist 10pkt |

**Nagranie:** ❌ Nie nagrane
**Priorytet nagrania:** 9 (BONUS — po core modułach)

**Uwaga produkcyjna:** Wymaga skoordynowania z Aliną. Nagrywajcie razem — podział: Kacper prowadzi demo tech, Alina komentuje aspekty prawne "na żywo". Nie nagrywajcie osobno i nie sklejajcie — traci naturalność.

---

### MODUŁ BONUS B — Sprzedaż i Delivery Projektów Automatyzacji

**Katalog:** `Modul_BONUS_Sprzedaz/`
**Czas całkowity:** ~2 godziny
**Format:** Solo Kacper, twarz + prezentacja + 1 live wycena
**Cel:** Uczestnik wie jak wycenić projekt, przeprowadzić discovery call i zbudować retainer
**Wyjątkowość:** Jedyny moduł o business side — "umiesz budować, teraz naucz się za to brać"

| # | Plik | Status | Uwagi |
|---|------|:------:|-------|
| 01 | `01_Agenda.md` | ✅ | Gotowe |
| 02 | `02_Prezentacja.md` | ✅ | Gotowe |
| 03 | `03_Skrypt.md` | ❌ | Brakujący plik |
| 04 | `04_Cwiczenia.md` | ❌ | Brakujący plik |
| 05 | `05_Workflow_Blueprint.md` | ✅ | Gotowe — wycena, discovery, handover, retainer |

**Nagranie:** ❌ Nie nagrane
**Priorytet nagrania:** 10 (BONUS — jako ostatnie)

---

## Kolejność nagrywania (rekomendowana)

> Logika: od najkrótszego do najdłuższego, wolne leady magnet pierwsze, bonusy na koniec.

| Kolejność | Moduł | Czas nagrania | Zablokowany przez |
|:---:|---|:---:|---|
| 1 | Mod. 00 — Filozofia *(FREE)* | 1 sesja (~1h) | Nic — nagrywaj jako pierwsze |
| 2 | Mod. 01 — Fundamenty | 2 sesje (~1.5h każda) | Gotowość środowiska Docker |
| 3 | Mod. 02 — API i Dane | 1 sesja (~2.5h) | Ukończenie Mod. 01 |
| 4 | Mod. 04 — Architektura | 2 sesje (~1.5h każda) | Ukończenie Mod. 02 |
| 5 | Mod. 03 — Skalowalność | 2 sesje (~2h każda) | Ukończenie Mod. 01, 02 |
| 6 | Mod. 05 — Human-in-Loop | 2 sesje (~1.5h każda) | Ukończenie Mod. 01–04 |
| 7 | Mod. 07 — RAG | 2 sesje (~1.5h każda) | Qdrant gotowy, Google Drive |
| 8 | Mod. 06 — Autonomous Agents | 2 sesje (~2h każda) | Ukończenie Mod. 05–07 |
| 9 | BONUS A — Bezpieczeństwo | 1 sesja (~2h) | Alina dostępna |
| 10 | BONUS B — Sprzedaż | 1 sesja (~2.5h) | Nic |

**Szacowany czas nagrań łącznie: ~26h materiału = 52h produkcji (x2 rule)**

---

## Brakujące pliki do stworzenia

> Poniższe pliki są potrzebne przed nagraniem odpowiednich modułów.

| Priorytet | Moduł | Brakujący plik | Blokuje nagranie |
|:---:|---|---|:---:|
| WYSOKI | Mod. 01 | `05_Workflow_Blueprint.md` | TAK |
| WYSOKI | Mod. 02 | `05_Workflow_Blueprint.md` | TAK |
| WYSOKI | Mod. 03 | `05_Workflow_Blueprint.md` | TAK |
| WYSOKI | Mod. 04 | `05_Workflow_Blueprint.md` | TAK |
| WYSOKI | Mod. 05 | `04_Cwiczenia.md` | TAK |
| WYSOKI | Mod. 05 | `05_Workflow_Blueprint.md` | TAK |
| WYSOKI | Mod. 06 | `03_Skrypt.md` | TAK |
| WYSOKI | Mod. 06 | `04_Cwiczenia.md` | TAK |
| WYSOKI | Mod. 06 | `05_Workflow_Blueprint.md` | TAK |
| WYSOKI | Bon. B | `03_Skrypt.md` | TAK |
| WYSOKI | Bon. B | `04_Cwiczenia.md` | TAK |

---

## Definicja "Plik gotowy" (✅)

Plik oznaczony jako ✅ oznacza:
- [ ] Zawiera kompletną treść (nie draft, nie placeholder)
- [ ] Przeczytany i zaakceptowany przez Kacpra
- [ ] Blueprint przetestowany na działającym n8n (dotyczy 05_Workflow_Blueprint.md)
- [ ] Skrypt przeczytany na głos co najmniej raz (dotyczy 03_Skrypt.md)

**Zmień status na ✅ dopiero po spełnieniu wszystkich powyższych punktów.**
