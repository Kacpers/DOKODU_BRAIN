---
type: resource
status: active
owner: kacper
last_reviewed: 2026-03-06
tags: [playbook, logistyka, branża, discovery, wdrozenia]
related: [[PRJ_Corleonis_Wdrozenie]], [[Sales_Playbook]]
---

# PLAYBOOK BRANŻOWY: Logistyka / Transport / Spedycja
> Zbudowany na podstawie: projekt Corleonis + research branżowy.
> Uzupelniaj po kazdym projekcie w tej branzy. To jest aktyw Dokodu.

---

## PROFIL BRANZY

**Kim jest typowy klient z logistyki:**
- Firma spedycyjna lub operator logistyczny, 50-500 pracownikow
- Obsługuje transport drogowy (FTL/LTL), magazynowanie, cross-docking
- Systemy: TMS (Transport Management System), WMS, ERP (Comarch, SAP, Navision/BC)
- Papierologia: dziennie setki dokumentow — CMR, WZ, faktury, listy przewozowe, POD
- Klienci: firmy produkcyjne, e-commerce, retail

**Typowy decision maker:**
- Dyrektor Operacyjny / Logistics Manager / COO
- Czesto technofob ktory potrzebuje "to po prostu dzialalo"
- Boi sie: przestojow, bledow w dokumentach, kar od klientow za bledy

---

## KLUCZOWE BOLE BRANZY (top 5)

### 1. Reczne przetwarzanie dokumentow transportowych
**Opis:** CMR, WZ, faktury spedycyjne sa skanowane i reczne przepisywane do ERP/TMS.
**Skala bolu:** 3-5 osob × 2-4h/dzien = 6-20h/dzien straconej pracy
**Nasza odpowiedz:** BP-003 (Document Parser) + Gemini Vision → automatyczne wejscie do ERP
**ROI przykladowy:** 20h × 65 PLN/h × 22 dni = 28 600 PLN/mies. zaoszczone

### 2. Brak widocznosci w czasie rzeczywistym (real-time tracking)
**Opis:** Dyspozytor dzwoni do kierowcow zeby sprawdzic status dostawy. Klienci denerwuja sie brakiem informacji.
**Skala bolu:** 50-100 telefonow dziennie × 5 min = 4-8h/dzien dyspozyturze
**Nasza odpowiedz:** n8n + GPS API dostawcy + automatyczne powiadomienia email/SMS do klientow
**ROI przykladowy:** Eliminacja 80% telefonow statusowych = ~5h/dzien × 65 PLN = 7 150 PLN/mies.

### 3. Bledy w fakturowaniu i rozliczeniach z przewoznikami
**Opis:** Roznice miedzy zleceniem a faktura przewoznika — reczne sprawdzanie, spory, opoznione platnosci
**Skala bolu:** 10-30% faktur ma rozbieznosci, kazda wymaga 20-60 min analizy
**Nasza odpowiedz:** AI agent porownujacy zlecenie vs faktura, automatyczne oznaczanie roznic, Slack alert

### 4. Kompletacja dokumentow do archiwum
**Opis:** POD (Proof of Delivery), CMR, listy przewozowe — wymogi archiwizacji 5 lat, kontrole UKS
**Skala bolu:** Braki dokumentow = problemy z VAT, roszczenia od klientow
**Nasza odpowiedz:** Automatyczna archiwizacja w MinIO/S3 + indeksowanie + search po numerze CMR/WZ

### 5. Raportowanie dla klientow (KPI dostawy)
**Opis:** Kluczowi klienci wymagaja miesięcznych raportow: on-time delivery %, uszkodzenia, reklamacje
**Skala bolu:** 2-5h/mies. per klient × 10 klientow = 20-50h/mies.
**Nasza odpowiedz:** BP-005 (Weekly Report Generator) — dane z TMS/ERP → AI synteza → auto-email

---

## SYSTEMY KTORE BEDA W PROJEKCIE

| System | Typ | Popularnosc w PL | n8n Connector |
| :--- | :--- | :---: | :---: |
| Comarch ERP XL | ERP | Wysoka | HTTP REST API |
| SAP S/4HANA | ERP | Srednia (enterprise) | HTTP REST / RFC |
| Microsoft BC (Navision) | ERP | Srednia | REST API |
| Transics TX-Sky | TMS | Srednia | API (zapytac o klucz) |
| TimoCom | TMS/Gielda | Wysoka | API (beta) |
| Outlook / O365 | Email | Wysoka | n8n wbudowany |
| SharePoint | DMS | Srednia | n8n wbudowany |
| Fakturownia | Fakturowanie | Srednia | REST API |

**Najczestszy stack u klienta mid-market:** Comarch ERP XL + Outlook + Excel + SharePoint

---

## PYTANIA DISCOVERY (specyficzne dla logistyki)

Poza standardowymi pytaniami z [[CRM_Leady_B2B]], zapytaj:

1. "Ile dokumentow transportowych przetwarza Wasz dzial dziennie/miesiecznie? (CMR, WZ, faktury)"
2. "Kto dzisiaj wprowadza dane z dokumentow do systemu i ile mu to zajmuje?"
3. "Czy zdarzaja sie pomylki przy przepisywaniu? Jakie sa konsekwencje?"
4. "Jakiego systemu TMS/ERP uzywaja? Czy ma dostepne API?"
5. "Czy klienci wymagaja raportow KPI? Jak je teraz tworzycie?"
6. "Czy macie problemy z archiwizacja dokumentow (POD, CMR) — szczegolnie na potrzeby VAT?"
7. "Co sie dzieje gdy dokument jest nieczytelny lub brakuje zalacznika?"
8. "Czy mają EDI (Electronic Data Interchange) z klientami/dostawcami?"
9. "Jaki jest Wasz SLA na przetworzenie dokumentu (ile godzin od odebrania do wejscia do systemu)?"
10. "Czy byl jakis audyt UKS lub kontrola celna ktora ujawnila braki dokumentacji?"

---

## TYPOWE ROZWIAZANIA DOKODU DLA LOGISTYKI

### Pakiet Podstawowy (15 000 - 25 000 PLN)
- Automatyczny parser dokumentow (CMR, WZ, faktury) → ERP
- Email trigger (zalaczniki) + AI ekstrakcja + walidacja + ERP API
- Archiwum z wyszukiwarka
- SLA: 6 tygodni

### Pakiet Rozszerzony (35 000 - 60 000 PLN)
- Wszystko z podstawowego +
- Automatyczne powiadomienia statusowe dla klientow (tracking)
- Raportowanie KPI per klient (auto-email miesięczny)
- Reconciliacja faktur przewoznikow
- SLA: 10-14 tygodni

### Retainer (3 000 - 5 000 PLN/mies.)
- Monitoring workflowow
- Nowe typy dokumentow w zakresie
- Support i optymalizacja

---

## RYZYKA SPECYFICZNE DLA BRANZY

| Ryzyko | Dlaczego wazne | Jak mitygowac |
| :--- | :--- | :--- |
| Jakosc skanow dokumentow | Kierowcy fotografuja telefonem — slabe oswietlenie, obroty | Preprocessing (deskew, enhance) przed AI |
| Dokumenty w jezyku obcym | CMR po angielsku/niemiecku/ukrainsku | Gemini 1.5 Pro obsługuje multilingualnie |
| Dane osobowe kierowcow w dokumentach | RODO — imiona, numery praw jazdy | Anonimizacja lub brak zapisu tych pol |
| Legacy ERP bez API | Stary Comarch/SAP bez REST | Alternatywa: Excel/CSV import lub desktop scraping (ryzykowne) |
| Seasonality (szczyt Q4) | W sezonie brak czasu na wdrozenie | Planuj projekty Q1-Q3 |
| Niechec kierowcow do nowych procesow | "Zawsze tak robilimy" | Change management + szkolenie + prosta UX |

---

## CASE STUDY: Corleonis (anonimizowane)
*(Uzupelnic po zakonczeniu projektu)*

**Branza:** Logistyka / spedycja krajowa i miedzynarodowa
**Wielkosc:** ~150 pracownikow, dzial logistyki 15 osob
**Problem:** Reczne przetwarzanie ~500 dokumentow/mies. — 25h/mies. straconej pracy
**Rozwiazanie:** n8n + Gemini Vision + Comarch ERP XL API + MinIO archiwum
**Wyniki (po 30 dniach live):**
- ___% dokumentow przetworzonych automatycznie (cel: >85%)
- Sredni czas przetwarzania: ___ sek (cel: <90 sek)
- Oszczędność: ___h/mies. = ___PLN/mies.
- NPS: ___/10
**Kluczowe wyzwanie:** ___
**Lekcja na przyszlosc:** ___

---

## LINKI
- [[PRJ_Corleonis_Wdrozenie]] — aktywny projekt
- [[N8N_Blueprints]] → BP-003 Document Parser
- [[300_BIBLIOTEKA_PROMPTOW]] → PROMPT-001, PROMPT-003
- [[RODO_Checklist]] — dane osobowe kierowcow w dokumentach
