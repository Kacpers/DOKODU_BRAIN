---
type: resource
status: draft
owner: kacper
last_reviewed: 2026-03-06
tags: [playbook, produkcja, manufacturing, branża, discovery]
related: [[PRJ_Animex_Szkolenie]], [[Sales_Playbook]]
---

# PLAYBOOK BRANŻOWY: Produkcja / Manufacturing
> Zbudowany na podstawie: projekt Animex + research branżowy.
> Status DRAFT — uzupelnic po zakonczeniu projektu Animex i kolejnych projektach produkcyjnych.

---

## PROFIL BRANZY

**Kim jest typowy klient z produkcji:**
- Producent z Pol DP lub europejski, 50-500 pracownikow
- Produkcja seryjna lub jednostkowa: FMCG, czesci maszynowe, elektronika, tekstylia
- Systemy: ERP (SAP, Comarch, EPICOR), MES, SCADA, QMS
- Bol: kontrola jakosci reczna, komunikacja miedzy halą a biurem, reklamacje, raporty produkcyjne
- Klienci: firmy handlowe, retail, inne producenci (B2B)

**Typowy decision maker:**
- Dyrektor Produkcji / Operations Manager / CEO (w firmach <100 prac.)
- Skupiony na: OEE (Overall Equipment Effectiveness), waste reduction, on-time delivery
- Jezyk: "przestoj", "defekty", "normy", "ISO 9001", "Kaizen"

---

## KLUCZOWE BOLE BRANZY (top 5)

### 1. Reczna kontrola jakosci i raportowanie defektow
**Opis:** Operatorzy zapisuja defekty w papierowych kartach lub Excelu. Dane trafiaja do managera z opoznieniem 24-48h.
**Skala bolu:** Bledy wykrywane pozno = drogie poprawki + ryzyko dostarczenia wadliwego produktu
**Nasza odpowiedz:** Formularz mobilny (n8n + Google Forms/Typeform) → automatyczny alert jakosci → raport shiftowy auto-generowany
**ROI przykladowy:** Wczesne wykrycie defektu oszczedza 5-15% kosztu produkcji danej partii

### 2. Komunikacja hala - biuro (przerwy w informacji)
**Opis:** Zamowienie zmienia sie w biurze ale informacja nie dociera do hali na czas. Lub odwrotnie — awaria maszyny nieraportowana do supply chain.
**Skala bolu:** Nieplanowane przestoje, bledne zamowienia surowcow
**Nasza odpowiedz:** Webhook trigger z systemu produkcyjnego → n8n → Slack/Teams do wlasciwych osob

### 3. Raporty produkcyjne (shiftowe, dzienne, tygodniowe)
**Opis:** Majster/supervisor spdza 1-2h dziennie na tworzeniu raportow. Czesto sa niekompletne lub niezgodne z ERP.
**Skala bolu:** Czas managera + bledy danych + opozniony wglad dla CEO
**Nasza odpowiedz:** BP-005 (Report Generator) — dane z ERP + MES → AI synteza → auto-email o 06:00

### 4. Obsługa reklamacji (BOK powiązany z produkcja)
**Opis:** Klient zgłasza reklamacje, biuro nie wie co produkcja, produkcja nie wie co wyslano. Brak traceability.
**Skala bolu:** Dlugi czas rozpatrzenia reklamacji, utrata klientow
**Nasza odpowiedz:** Agent BOK (jak w Animex) + integracja z ERP → automatyczna karta reklamacji z historia produkcji

### 5. Planowanie i harmonogramowanie (co reczne)
**Opis:** Planner produkcji uzgadnia harmonogram przez telefon i Excel. Zmiany nie sa komunikowane szybko.
**Skala bolu:** Suboptymalne uzycie maszyn, niezadowoleni klienci czekajacy na termin
**Nasza odpowiedz:** (zaawansowane) Agent AI analizujacy zamowienia + kapacytet → propozycja harmonogramu. Wymaga doswiadczenia z MES/ERP klienta.

---

## SYSTEMY KTORE BEDA W PROJEKCIE

| System | Typ | Popularnosc w PL | n8n Connector |
| :--- | :--- | :---: | :---: |
| SAP S/4HANA / SAP ERP | ERP | Wysoka (duze firmy) | HTTP REST / RFC |
| Comarch ERP XL | ERP | Wysoka (SMB) | REST API |
| EPICOR | ERP | Srednia | REST API |
| Infor LN | ERP/MES | Niska | REST API |
| Microsoft BC | ERP | Srednia | REST API |
| Outlook / Teams | Komunikacja | Bardzo wysoka | n8n wbudowany |
| Google Workspace | Komunikacja | Srednia | n8n wbudowany |
| Jira / Confluence | Zarzadzanie | Srednia (inz.) | n8n wbudowany |

**Najczestszy stack u klienta SMB produkcja:** Comarch/SAP + Outlook + Excel (duzo Excela!) + papier

---

## PYTANIA DISCOVERY (specyficzne dla produkcji)

1. "Ile zmian produkcyjnych dziennie? Kto tworzy raport po kazdej zmianie i ile mu to zajmuje?"
2. "Jak szybko informacja o defekcie trafia do managera? Co sie dzieje jezeli za wolno?"
3. "Jak wygladaja reklamacje klientow — od zgloszenia do odpowiedzi — ile trwa?"
4. "Czy posiadaja system MES? Czy ERP ma modul produkcyjny?"
5. "Jak komunikujesz zmiany harmonogramu z hala? Telefon? Tablica?"
6. "Czy macie problemy z traceability — mozecie powiedziec z ktorej partii pochodzi reklamowany produkt?"
7. "Jaka jest Wasza OEE (Overall Equipment Effectiveness)? Czy to mierzycie?"
8. "Ile czasu zajmuje przygotowanie dokumentacji dla ISO 9001 / innych certyfikacji?"
9. "Czy macie inicjatywy Lean / Kaizen? Co sie sprawdza, co nie?"
10. "Co by sie stalo gdybyscie mogli wiedziec o problemie 2h wczesniej niz teraz?"

---

## SPECYFIKA AI ACT DLA PRODUKCJI

**UWAGA — Bezpieczenstwo osob (Aneks III pkt 7):**
Systemy AI uzyway do: sterowania maszynami bezposrednio, predyktywnego utrzymania ruchu wplywajacego na bezpieczenstwo = HIGH-RISK.

**Co NIE jest high-risk w produkcji:**
- Raportowanie i dashboardy (tylko prezentuja dane, nie steruja)
- Agent BOK (obsługa zapytan, nie maszyn)
- Automatyzacja komunikacji (Slack alerty)
- Parser dokumentow zamowien

**Co MOZE byc high-risk (sprawdz z Alina):**
- System predykcji awarii maszyn ktory automatycznie wylacza maszyne
- AI ktora decyduje o dopuszczeniu produktu do sprzedazy (bez human-in-the-loop)
- Monitoring pracownikow przez kamery z AI

---

## CASE STUDY: Animex (anonimizowane)
*(Uzupelnic po zakonczeniu szkolenia)*

**Branza:** Produkcja / BOK (Biuro Obslugi Klienta)
**Wielkosc:** ___ pracownikow, ___ osob w BOK
**Problem:** Reczna obsługa ~200 zgłoszen/mies., brak kategoryzacji, duze opoznienia
**Rozwiazanie:** Szkolenie 2-dniowe + demo agenta AI klasyfikujacego maile
**Wyniki (NPS + feedback):**
- NPS: ___/10
- Najczesciej wspominany "aha moment": ___
- Co wdrozyli po szkoleniu: ___
- Upsell potential: ___

---

## LINKI
- [[PRJ_Animex_Szkolenie]] — aktywny projekt
- [[N8N_Blueprints]] → BP-002 (Email Classification), BP-005 (Report Generator)
- [[300_BIBLIOTEKA_PROMPTOW]] → PROMPT-002 (Email BOK)
