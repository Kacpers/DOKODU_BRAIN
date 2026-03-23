---
type: area
status: active
owner: alina
last_reviewed: 2026-03-06
tags: [finanse, cashflow, fakturowanie, kpi, budzet]
---

# AREA: Finanse — Dokodu sp. z o.o.
> **NIP:** 5882473305 | **KRS:** 0000925166 | **Kapital zakladowy:** 5 000 PLN
> **Prowadzaca operacyjnie:** Alina (COO) + ksiegowy zewnetrzny
> **Kacper przegladat:** Co miesiac (w 1. tygodniu nastepnego miesiaca)

---

## PRZEGIAD FINANSOWY (Marzec 2026)

### Przychody

| Zrodlo | Wartosc (PLN netto) | Status fakturowani | Uwagi |
| :--- | ---: | :---: | :--- |
| Animex — zaliczka (50%) | 9 000 | Wystawiona | PRJ_Animex |
| Corleonis — etap 1 | 17 500 | Wystawiona | PRJ_Corleonis |
| Corleonis — retainer | 3 000 | Cykliczna | Co miesiac |
| Kurs n8n — przychod | 0 | — | Launch w marcu |
| **RAZEM przychod** | **29 500** | | |

### Koszty stale (miesiac)

| Pozycja | Koszt (PLN netto) | Czestotliwosc | Optymalizacja? |
| :--- | ---: | :---: | :--- |
| Hosting VPS (n8n Prod + inne) | ~400 | Miesiac | Sprawdzic Oracle Free Tier |
| OpenAI API | ~300 | Miesiac | Monitoruj uzycie |
| Google Workspace | ~200 | Miesiac | — |
| Marketing (ads) | 8 500 | Miesiac | Zob. [[100_MARKETING_ADS]] |
| Ksiegowosc zewnetrzna | 500 | Miesiac | — |
| Platforma kursu | 400 | Miesiac | — |
| Software (Notion, Mailerlite, etc.) | ~300 | Miesiac | Audyt subskrypcji! |
| **RAZEM koszty** | **~10 600** | | |

### Wynik operacyjny szacunkowy
| | PLN |
| :--- | ---: |
| Przychod | 29 500 |
| Koszty | -10 600 |
| **Wynik brutto** | **18 900** |
| ZUS + podatek (est.) | ~5 000 |
| **Do dyspozycji** | **~13 900** |

---

## FAKTUROWANIE — STANDARD DOKODU

### Warunki platnosci
- Projekty szkoleniowe: 50% zaliczka przed realizacja + 50% po
- Wdrozenia: 30% na start + 40% po MVP + 30% po go-live
- Retainery: platnosc z gory do 5. dnia miesiaca
- Faktury: 14 dni platnosc (krotsze dla nowych klientow)

### Narzedzie: fakturowanie
- Aktualne: [Fakturownia / iFirma / inne]
- Automatyzacja fakturowania: n8n + [narzedzie] — rozwazyc

### Numeracja faktur
```
FV/[ROK]/[MIESIAC]/[NUMER]
Przyklad: FV/2026/03/001
```

---

## CASHFLOW — SYGNALY ALARMOWE

Reaguj natychmiast gdy:
- [ ] Saldo konta spada ponizej 15 000 PLN
- [ ] Faktura przeterminowana >14 dni bez kontaktu od klienta
- [ ] Klient opoznia platnosc o >30 dni (wezwanie do zaplaty)
- [ ] Koszt pojedynczej subskrypcji przekracza 1 000 PLN/mies. bez rewizji ROI

### Procedura windykacji (etapy)
1. Dzien +1 od terminu: Uprzejmy reminder (email + SMS)
2. Dzien +7: Formalne wezwanie do zaplaty (email + pisemnie)
3. Dzien +14: Kontakt telefoniczny + ustalenie planu
4. Dzien +30: Nota odsetkowa + rozwazyc odsprzedaz wierzytelnosci lub sad
5. Alina prowadzi sprawy >30 dni

---

## PLANOWANIE FINANSOWE

### Cele przychodowe 2026

| Kwartal | Cel (PLN netto) | Plan |
| :--- | ---: | :--- |
| Q1 (styczen-marzec) | 80 000 | Animex + Corleonis + pocz. retainera |
| Q2 (kwiecien-czerwiec) | 120 000 | Kurs n8n + nowe wdrozenia |
| Q3 (lipiec-wrzesien) | 150 000 | Skalowanie + mozliwy nowy pracownik |
| Q4 (pazdziernik-grudzien) | 180 000 | Kursy + wdrozenia + partnerstwa |
| **RAZEM 2026** | **530 000** | |

### Inwersja ryzyka (co moze zniszczyc plan)
- Strata 2 duzych klientow = -100 000 PLN
- Brak sukcesu kursu n8n = -120 000 PLN pipeline
- Zmiana przepisow AI Act blokujaca konkretna usluge
- Kluczowy dostawca (OpenAI, n8n) zmienia cennik drastycznie

---

## AUDYT SUBSKRYPCJI (co kwartal)

| Narzedzie | Koszt/mies. | Uzycie | Zachowac? |
| :--- | ---: | :---: | :---: |
| OpenAI API | zmienny | Wysoki | TAK |
| Google Workspace | ~200 | Wysoki | TAK |
| Notion | ~100 | — | ROZWAZYC |
| Mailerlite | ~100 | Sredni | TAK |
| Taplio (LinkedIn) | ~150 | Niski | SPRAWDZIC |
| Hotjar | ~200 | Niski | ROZWAZYC |
| [dodac...] | | | |

**Zasada:** Jezeli narzedzia nie dotykasz przez 30 dni — anuluj.

---

*Przegladaj co miesiac. Aktualizuj przychody po kazdej wystawionej fakturze.*
