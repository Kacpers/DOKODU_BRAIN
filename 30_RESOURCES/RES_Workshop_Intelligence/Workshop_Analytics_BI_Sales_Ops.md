---
type: resource
status: active
owner: kacper
created: 2026-04-15
tags: [szkolenia, pain-points, analytics, bi, powerbi, salesforce, sales-intel, workshop-data]
source: warsztat z zespołem analitycznym / sales ops (dane zewnętrzne, kontekst PowerBI, SalesForce, HR)
---

# Workshop Intelligence — Analytics / BI / Sales Ops (dane surowe)

> Grupa analityków, sales ops, marketing ops. Kontekst: PowerBI, SalesForce, Excel, dane reklamowe.
> Kluczowy motyw: analiza raportów, prezentacje, podsumowania spotkań, cykliczne raporty.

---

## Procesy do usprawnienia (z danymi ilościowymi!)

### Spotkania & podsumowania
- Podsumowania spotkań i rozdzielanie zadań (wielokrotnie powtarzane)
- Wyciąganie najważniejszych punktów z dyskusji i koncepcji
- Planowanie spotkań z agendą wg dostępności zaproszonych
- Przeniesienie flow spotkania na slajdy z szablonami firmowymi

### Analiza danych i raporty
- Codziennie mail z tabelą za 14 dni + 1 dzień — analiza odchyleń + trend + alert anomalii
- Zderzenie zaplanowanych celów z realizacją w nakładających się kontekstach biznesowych
- Analiza raportów Excel na danych firmowych
- Analiza kilku raportów z różnymi danymi → konkretne wnioski
- Analiza danych z wykresów → komentarze objaśniające → raport na rynek
- Streszczenie wniosków sprzedażowych z kwartalnych ankiet
- Modele predykcyjne do danych przyszłościowych
- Łączenie kropek z PowerBI dla poprawy efektywności rekrutacji klientów
- "Czy na naszym poziomie da się podłączyć agenta AI do raportów z PowerBI?"
- Cykliczne insighty z raportów sprzedaży (PBI)
- Wsparcie AI w analizie pricingu — proaktywność, nie tylko analiza wsteczna
- Możliwość korzystania z lokalnych modeli do analizy danych wrażliwych
- Budowanie lokalnych narzędzi do analizy raportów (brak możliwości udostępniania danych wewnętrznych)

### Prezentacje (POWTARZAJĄCY SIĘ BÓL)
- Szybkie tworzenie prezentacji warsztatowych i podsumowujących
- "Narzędzie jak Gamma — masz tu szablon i stwórz prezentację"
- Wsparcie w tworzeniu cyklicznych prezentacji — automatyczne aktualizowanie slajdów z PBI
- Streszczenia i prezentacje oparte na PBI — bez eksportów i pracy na Excelu

### Content & research
- Streszczenia rozmów, podcastów, nagrań YT — recykling treści contentowych
- Research danych o rynku pracy z zagranicy
- Audyty i badanie rynku, konkurencji
- Cykliczne podsumowania działań konkurencji pod kątem sprzedażowym
- Partner sparingowy odnośnie strategii social media — formaty, lejek

### Zarządzanie
- Analiza potencjału ludzi i identyfikacja obszarów do rozwoju
- Podsumowanie ocen/raportów 270 — wskazanie obszarów do rozwoju
- Agenci do przypominajek "zrób, wypełnij, zadbaj"
- "Agent pilnowacz — masz coś do zrobienia? nie zapomnisz, bo Ci nie pozwolę"
- Deep research agent do danych finansowych

---

## Macierz wartość/łatwość (DANE ILOŚCIOWE!)

| Proces | Częstotliwość | Czas | Osób | Kategoria |
|--------|-------------|------|------|-----------|
| Ofertowanie | — | 30-60 min | 14 | BIG BET |
| Ogłoszenia rekrutacyjne (kopiowanie do systemu) | codziennie | 6h/dzień | 40 | BIG BET / WiP |
| Analiza danych reklamowych + PBI + koszty | 1x/mies. | 1h | 2 | BIG BET |
| Przygotowanie do spotkania z klientem | codziennie | 20-30 min | 14 | BIG BET |
| Analiza danych reklamowych (wieloźródłowa) | co 2 dni | — | 5 | BIG BET |
| Prezentacje na warsztaty | 1x/mies. | 2-8h | 6 | BIG BET |
| Analizy z rekomendacjami zmian w ogłoszeniach | codziennie | 60 min | 6 | BIG BET |
| Przygotowanie oferty (rabaty, historia, konkurencja) | codziennie | — | 6 | BIG BET |
| Analizy danych w SF + wiadomości do zespołu | co tydzień | — | 12 | BIG BET |
| Kontrola komentarzy od klientów [RS] | 1x/dzień | 1h | 3 | QUICK WIN |
| Coaching maili [RS] | 1x/dzień | 1h | 50 | QUICK WIN |
| Analiza konkurencji | 2-3x/tydzień | 30 min | 6 | QUICK WIN |
| Szukanie leadów | 2-3x/tydzień | 60 min | 8 | QUICK WIN |
| Podsumowanie dla klienta | 6x/mies. | 30-45 min | 8 | QUICK WIN |
| Planowanie sprzedaży | 2x/mies. + codziennie | 15min-1h | 60 | QUICK WIN |
| Kontrola jakości maili [RS] | 1x/dzień | 1h | 8 | QUICK WIN |
| Podsumowania dla klientów | kilka razy/tydzień | 2h | 6 | QUICK WIN |
| Podsumowanie spotkania z klientem | codziennie | 20-30 min | 14 | QUICK WIN |
| Raportowanie w SF | codziennie | 10-15 min | 14 | QUICK WIN |
| Statystyki zespołowe [RS] | 1x/tydzień | 2h | 8 | QUICK WIN |
| Bieżąca analiza wyników | 2x/tydzień | 30 min | 5 | QUICK WIN |
| Analiza social media | 1x/mies. | 2h | 2 | FILL-IN |
| Przygotowywanie ofert sprzedażowych | codziennie | 1h | 6 | FILL-IN |
| Notatki po spotkaniach | codziennie | 10 min | 6 | FILL-IN |
| Uzupełnianie wyników w Excelu | 1x/dzień | 5 min | 8 | FILL-IN |
| Podsumowania kwartalne strategii [RS] | 1x/kwartał | 8h | 10 | FILL-IN |

---

## Zastosowanie w Dokodu

### Sprzedaż
- "40 osób × 6h dziennie na kopiowanie ogłoszeń do systemu" — to jest automatyzacja warta setki tysięcy
- "50 osób × coaching maili codziennie" — AI review maili to ogromna skala
- "14 osób × 20-30 min na przygotowanie do spotkania" — AI pre-meeting brief

### Wdrożenie
- PBI + AI agent = cykliczne insighty bez ręcznej analizy
- SF automation: uzupełnianie, coaching, kontrola jakości
- n8n: aggregacja danych z wielu źródeł → raport

### Content
- "Podłączenie AI do PowerBI" — temat na artykuł/film!
- "Lokalne modele do danych wrażliwych" — enterprise use case
