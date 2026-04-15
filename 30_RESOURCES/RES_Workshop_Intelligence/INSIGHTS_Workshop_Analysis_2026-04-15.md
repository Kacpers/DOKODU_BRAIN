---
type: resource
status: active
owner: kacper
created: 2026-04-15
tags: [insights, strategia, youtube, social-media, micro-saas, szkolenia, workshop-intelligence]
source: analiza danych z ~200+ uczestników z ~10 grup warsztatowych
---

# Workshop Intelligence — Kluczowe wnioski (2026-04-15)

> Synteza danych z 10 warsztatów, ~200+ osób, kilkanaście firm i branż.
> Baza źródłowa: `30_RESOURCES/RES_Workshop_Intelligence/Workshop_*.md`

---

## 1. TEMATY NA YOUTUBE (potwierdzone bolączką)

| # | Temat | Ile grup zgłosiło | Hook / kontekst |
|---|-------|-------------------|-----------------|
| 1 | AI halucynuje przy liczbach — jak walidować wyniki | 8/10 | #1 bariera adopcji AI we wszystkich grupach |
| 2 | Podsumowanie spotkań bez nagrywania | 7/10 | CFO, PM, sales, managerowie — wszyscy tego chcą |
| 3 | Dlaczego AI prezentacje wyglądają jak plastik | 6/10 | Ogromna frustracja, zero dobrych rozwiązań na rynku |
| 4 | 1900 maili dziennie — jak AI pomaga zespołowi sales | 1 ale TWARDE DANE | 8 osób × 240 maili/dzień — policzalne ROI |
| 5 | Podłącz AI do PowerBI — czy to w ogóle możliwe? | 4/10 | Dosłowne pytanie z warsztatu |
| 6 | Promptowanie trwa dłużej niż zrobienie samemu — co robisz źle | 6/10 | CFO, Copilot users, managerowie — kontrintuicyjne |
| 7 | Agent AI pilnowacz — nie zapomnisz o żadnym deadlinie | 3/10 | Proste, pokazywalne, n8n demo |
| 8 | Dane firmowe w ChatGPT — co wolno, a co nie | 5/10 | Compliance bariera, Dokodu Tech+Legal positioning |

---

## 2. TEMATY NA SOCIAL MEDIA (posty z językiem klienta)

### Posty edukacyjne (LinkedIn)
- "Irytuje mnie że coś ustalimy, poprawię go, a po kilku pytaniach robi ten sam błąd" → wyjaśnienie okien kontekstowych
- "Korzystam głównie z Excela, więc AI nie jest jeszcze wiarygodnym źródłem" → jak AI + Excel naprawdę działa
- "Brak deterministyczności outputu — każdy kod muszę mocno walidować" → dlaczego AI nie jest deterministyczne
- "Im bardziej rozbudowany prompt, tym gorszy wynik" → kontrintuicyjne, engagement gwarantowany

### Posty sprzedażowe (LinkedIn)
- "40 osób × 6h dziennie kopiuje treści ogłoszeń do systemu publikacyjnego" → ile to kosztuje rocznie?
- "Mamy dane w HubSpot, Pipedrive, FOTCnet i Jirze" → ile czasu tracicie na szukanie jednej informacji?
- "Podsumowanie spotkania? 14 osób × 20-30 min dziennie" → policzalny koszt braku automatyzacji

### Cytaty do użycia (dosłowne, od uczestników)
- "Próbuję się nauczyć podstaw aby AI nie był tylko lepszą wyszukiwarką... i mam wrażenie że potrzeba dużo czasu"
- "Pisanie promptów zajmuje więcej czasu niż zrobienie danego zadania"
- "Finalnie wciąż robię sama" (o prezentacjach)
- "Nie mam zaufania do treści które zwraca mi chat"
- "Masy maili — nawet takich gdzie nie jestem potrzebna"
- "Wszyscy są przeciążeni pracą i część tematów spada na niski priorytet"

---

## 3. STARTUP / MICRO-SAAS — trzy luki

### A. PREZENTACJE KORPORACYJNE z danych + szablon firmowy ⭐ REKOMENDACJA #1
- **Zgłoszone:** 6/10 grup
- **Problem:** "Aktualizacja prezentacji KPI — dane z PowerBI i Excela, layout firmowy (powtarzalny template)"
- **Cytaty:** "Narzędzie jak Gamma — masz tu szablon i stwórz prezentację", "Przeniesienie flow spotkania na slajdy używając szablonów firmowych", "Prezentacja z firmowymi kolorami i designem"
- **Dlaczego luka:** Gamma = generyczna. Copilot PPT = słaby. Claude = nie ogarnia szablonów. NIKT nie robi tego dobrze.
- **Rynek:** Każda firma 200+ osób, każdy tydzień, każdy manager
- **MVP:** Upload szablonu PPTX + dane z Excela/CSV → gotowa prezentacja w brandingu
- **Monetyzacja:** SaaS per seat, enterprise pricing, custom templates

### B. MEETING → TASKS PIPELINE ⭐ REKOMENDACJA #2
- **Zgłoszone:** 7/10 grup
- **Problem:** "Podsumowanie spotkania → taski w Jirze → update Confluence → follow-up reminder"
- **Luka:** Fireflies/Otter robią TYLKO transkrypcję. Nikt nie robi full pipeline: transkrypcja → podsumowanie → taski z przypisanymi osobami → reminder
- **MVP:** n8n workflow jako SaaS: Meet/Teams → Whisper → AI → Jira/Asana API
- **Ryzyko:** Fireflies ma $100M+ i goni ten rynek

### C. "AGENT PILNOWACZ" — deadline & follow-up tracker
- **Zgłoszone:** 3/10 grup
- **Problem:** "Automat który pilnuje — upomina o dostarczenie kosztów, odpowiedź na maila, umowy"
- **Cytat:** "Agent pilnowacz — masz coś do zrobienia? nie zapomnisz, bo Ci nie pozwolę"
- **MVP:** Slack/Teams bot, proste do zbudowania w weekend
- **Ryzyko:** Mniejszy rynek, ale prostszy start

**Ranking:** A > B > C (największy ból × najmniej konkurencji)

---

## 4. ROZWÓJ DOKODU — co wynika z danych

### Szkolenia — design oparty na danych

**Format potwierdzony:** Hands-on > wykład (KAŻDA grupa ma to w zasadach warsztatu)

**Biggest barrier:** "Nie ufam AI" + "promptowanie trwa za długo"
→ Szkolenie MUSI zaczynać od quick wina (podsumuj dokument, przeanalizuj tabelę), nie od teorii promptów

**4 persony szkoleniowe:**

| Persona | Przykład | Poziom | Co im dać |
|---------|---------|--------|-----------|
| Początkujący | CFO, HR, księgowość | "Jedyną styczność mam z ChatGPT" | Quick win: podsumuj raport, napisz maila |
| Użytkownik chatbota | Managerowie, sales | Korzystają, ale frustracja | Prompty + baza wiedzy + customowe instrukcje |
| Power user | Analitycy, PM | PBI, SQL, chcą agentów | Agenci, n8n, API, multi-source analysis |
| Techniczny | DevOps, data eng | n8n, API, pipelines | Architektura, deterministyczność, walidacja |

**Dokodu Tech+Legal = UNIKALNA POZYCJA**
"Kiedy mogę wrzucić dokument firmowy do Chata?" — pada na KAŻDYM warsztacie. Nikt inny nie odpowiada z pozycji tech + legal jednocześnie. To jest Twój moat.

### Oferta wdrożeniowa — top 3 use case'y (potwierdzone danymi)

| # | Use case | Grup zgłaszających | Przykład wyceny |
|---|---------|-------------------|-----------------|
| 1 | Podsumowania spotkań → CRM/Jira | 7/10 | 15-25k PLN |
| 2 | Analiza raportów z wielu źródeł → insights | 8/10 | 20-40k PLN |
| 3 | Automatyzacja emaili sprzedażowych | dane: 1900 maili/dzień | 25-50k PLN |

### Pozycjonowanie vs konkurencja

- **AI Hero (Aleksander Piskorz):** Pozycja = edukacja i metodologia. 68 silników, frameworki, "transfer myślenia". Buduje skalowalny content edukacyjny.
- **Dokodu (Kacper):** Pozycja = wdrożenia + legal + konkretne workflow. NIE konkurujesz z AI Hero na edukację — konkurujesz na "zbudujemy to dla Ciebie i będzie compliance-ready."
- **Linia podziału:** AI Hero uczy MYŚLEĆ o AI. Dokodu BUDUJE AI w firmie.

---

## Pliki źródłowe

Wszystkie surowe dane w `30_RESOURCES/RES_Workshop_Intelligence/`:

| Plik | Grupa |
|------|-------|
| `Workshop_Managers_Pain_Points.md` | Managerowie (Tutore) |
| `Workshop_DataDriven_Company_Pain_Points.md` | Firma data-driven (PUCCINI/retail) |
| `Workshop_CFO_Leadership_Pain_Points.md` | Kadra kierownicza / CFO |
| `Workshop_Sales_Team_Pain_Points.md` | Zespół sales (eRecruiter/Pracuj) |
| `Workshop_FOTC_Internal_Pain_Points.md` | Firma IT/services |
| `Workshop_Analytics_BI_Sales_Ops.md` | Analytics / Sales Ops (DANE ILOŚCIOWE!) |
| `Workshop_Copilot_Users_SalesTeam.md` | Copilot users / sales+marketing |
| `Workshop_PM_UX_Management.md` | PM / UX / Management |
| `Workshop_University_Education.md` | Uczelnia wyższa |
| `Workshop_Participant_Prompts_Examples.md` | Realne prompty uczestników (materiał dydaktyczny) |
| `Presentation_ILoveMarketing_AgentsAI.md` | Planning board prezentacji I Love Marketing |
