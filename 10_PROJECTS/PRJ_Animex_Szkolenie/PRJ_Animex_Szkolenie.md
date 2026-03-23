---
type: project
status: active
owner: kacper
last_reviewed: 2026-03-06
tags: [projekt, szkolenie, animex, bok, n8n]
client: Animex
value_pln: 18000
deadline: 2026-03-20
health: yellow
---

# PRJ: Animex — Szkolenie Automatyzacja BOK
> **Typ:** Szkolenie zamkniete (on-site/hybrid)
> **Wartosc kontraktu:** 18 000 PLN netto
> **Status:** ZOLTY — W trakcie
> **Termin dostarczenia:** 2026-03-20
> **Kontakt klienta:** _______________ | Tel: _______________
> **Kontakt Dokodu:** Kacper (Lead) + Alina (Legal/NDA)

---

## BRIEF PROJEKTU

**Problem klienta:**
Dzial BOK Animex obsługuje ~200 zgloszen miesiecznie recznie (Outlook + Excel). Brak kategoryzacji, priorytetyzacji, duze opoznienia. Menedzer BOK traci ~15h/miesiac na reciclowy raportowanie.

**Rozwiazanie Dokodu:**
Szkolenie 2-dniowe (8h + 8h) dla 15 osob. Zakres:
1. Dzien 1: Filozofia AI w BOK, demo agenta czytajacego maile, hands-on z n8n
2. Dzien 2: Budowa wlasnych przepływow, integracja z SAP (demo), Q&A

**Oczkiwane efekty dla klienta:**
- Redukcja czasu odpowiedzi na zgłoszenie o 40%
- Automatyczna kategoryzacja i priorytetyzacja emaili
- Raport tygodniowy generowany automatycznie (n8n + Google Sheets)

---

## FAZY I CHECKLIST

### FAZA 0: PRZYGOTOWANIE (do 2026-03-05)
- [x] Podpisanie umowy szkoleniowej
- [x] Otrzymanie zaliczki (50% = 9 000 PLN)
- [ ] **Ankieta diagnostyczna** — wyslac do uczestnikow (max 10 pytan)
  - Co uzywaja teraz do obslugi zgloszen?
  - Jaki jest ich poziom komputerowy (1-5)?
  - Jaki system pocztowy (Outlook? inne?)
- [ ] **NDA** podpisane przez wszystkich 15 uczestnikow
- [ ] Ustalenie daty szkolenia z koordynatorem HR Animex

### FAZA 1: CONTENT (do 2026-03-10)
- [ ] Prezentacja Dzien 1 (PPT/Keynote) — max 40 slajdow
- [ ] Prezentacja Dzien 2 — cwiczenia i warsztaty
- [ ] **Demo: Agent AI czytajacy maile z SAP** (kluczowe WOW!)
  - Techstack: n8n + Gmail API / Outlook API + GPT-4o
  - Output: JSON z kategorią, priorytetem, sugerowaną odpowiedzią
- [ ] Materialy handout dla uczestnikow (PDF, max 20 str.)
- [ ] Cwiczenia praktyczne (min. 3 scenariusze z ich branzy)

### FAZA 2: INFRASTRUKTURA TECHNICZNA (do 2026-03-15)
- [ ] Instancja n8n Self-hosted przygotowana dla 15 osob
  - [ ] Osobne konta uzytkownikow (nie admin!)
  - [ ] Testowe przeplywy wgrane
  - [ ] Backup konfiguracji
- [ ] Dostep do internetu w sali szkoleniowej potwierdzony
- [ ] Sprzet: projektor/TV HDMI, adaptery USB-C, powerbank
- [ ] Pendrive Emergency z offline JSON workflows

### FAZA 3: REALIZACJA (Dzien szkolenia)
- [ ] Rejestracja uczestnikow + lista obecnosci
- [ ] Check audio/video przed startem (15 min przed)
- [ ] Sesja 1: Teoria + Demo (90 min)
- [ ] Sesja 2: Hands-on (120 min) — Cwiczenie 1
- [ ] Lunch break (60 min) — nieformalne rozmowy = sales intelligence!
- [ ] Sesja 3: Hands-on (90 min) — Cwiczenie 2 i 3
- [ ] Q&A + feedback live (30 min)
- [ ] Zebranie ankiet satysfakcji (papier lub online)

### FAZA 4: FOLLOWUP (do 7 dni po szkoleniu)
- [ ] Wyslac materialy do uczestnikow (zip: PDFy + JSONy workflows)
- [ ] Wyslac fakture koncowa (50% pozostale = 9 000 PLN)
- [ ] NPS survey (3 pytania, Google Forms)
- [ ] **Oferta upsell:** Wdrozenie produkcyjne agenta AI w BOK — wycena w [[30_RESOURCES/RES_Sales_Playbook/Sales_Playbook]]
- [ ] Poprosic o referencje pisemne (do case study)

---

## RYZYKA I MITYGACJE

| Ryzyko | Prawdopodobienstwo | Mitygacja |
| :--- | :---: | :--- |
| Brak internetu w sali | Srednie | Offline JSONs na pendrive, demo nagrane wideo |
| Uczestnicy bez podstaw IT | Wysokie | Uproszczone cwiczenia dla grupy A, zaawansowane dla B |
| SAP API nie dziala podczas demo | Srednie | Mockowane dane JSON jako fallback |
| Ktos filmuje bez zgody | Niskie | NDA obejmuje zakaz nagrywania |
| Klient chce zmienic zakres w trakcie | Srednie | Zakres jasno opisany w umowie — zmiana = aneks |

---

## NOTATKI SPRZEDAZOWE (Sales Intelligence)
> Co zebrac podczas szkolenia — to zloto dla przyszlych projektow.

- Jakie inne procesy BOK sa bolesne? (lista problemow do upsell)
- Kto jest "internal champion" dla AI w firmie?
- Jaki budzet maja na automatyzacje w przyszlym roku?
- Czy jest IT, ktory moze wspomagac wdrozenie po szkoleniu?
- Kto decyduje o zakupie narzedzi? (CEO? IT Manager? COO?)

---

## LINKI I ZASOBY
- Umowa: [Dysk/SharePoint — link]
- Materialy szkoleniowe: [Dysk — link]
- Ankieta diagnostyczna: [Google Forms — link]
- [[30_RESOURCES/RES_n8n_Blueprints/N8N_Blueprints]] — przeplywy do demonstracji
- [[30_RESOURCES/RES_Prompt_Library/300_BIBLIOTEKA_PROMPTOW]] — prompty do agenta email

---

## HISTORIA ZMIAN
| Data | Zmiana | Kto |
| :--- | :--- | :--- |
| 2026-02-15 | Projekt zainicjowany, umowa podpisana | Kacper |
| | | |
