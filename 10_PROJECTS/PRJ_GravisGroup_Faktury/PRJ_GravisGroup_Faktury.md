---
type: project
status: active
owner: kacper
last_reviewed: 2026-03-24
tags: [projekt, python, ai, reconciliation, ksiegowosc, holandia, ing]
client: GravisGroup
value_pln: 12000
retainer_pln: 0
deadline: TBD (harmonogram do ustalenia emailem wg §6)
health: green
---

# PRJ: Gravis Group — System Reconciliation Faktur

> **Typ:** Umowa o dzielo — System IT (aplikacja webowa)
> **Wartosc kontraktu:** 12 000 PLN netto (Umowa nr 1/2026, dn. 25.02.2026)
> **Platnosci:** 30% zaliczka (3 600 PLN) + 70% po odbiorze (8 400 PLN)
> **Status:** ZIELONY — W fazie testow akceptacyjnych
> **Gwarancja:** 6 miesiecy od odbioru (wady = niezgodnosc ze Specyfikacja)
> **Kontakt klienta:** Grzegorz Gibula / Jakub
> **Kontakt Dokodu:** Kacper (Arch. + Dev)

---

## BRIEF PROJEKTU

**Problem klienta:**
Biuro ksiegowe obslugujace klientow holenderskich (BV) recznie paruje transakcje z wyciagów bankowych ING (PDF) z zapisami w ksiedze Excel (.xlsm — INKOOPBOEK / VERKOOPBOEK). Przy wielu klientach i setkach transakcji miesiecznie — praca czasochlonna i podatna na bledy.

**Rozwiazanie Dokodu:**
Aplikacja webowa do automatycznego reconciliation:
1. Upload PDF (wyciag ING) + Excel (.xlsm)
2. Kaskadowy algorytm dopasowania (Waterfall: regex → reguly → mappings → kwota/data → VAT → AI)
3. Interfejs do weryfikacji i recznego uzupelnienia
4. Raport Excel z wynikami

**Repo:** `/home/kacper/DOKODU/FAKTURY_KOSZTY`
**Stack:** Python 3.10 + FastAPI + pdfplumber + openpyxl + rapidfuzz + OpenAI GPT-4o-mini + React/TypeScript (Vite)

---

## ARCHITEKTURA SYSTEMU

```
[PDF wyciag ING] + [Excel .xlsm]
        ↓
[FastAPI: /api/upload]
        ↓
[Parser PDF] → [Parser Excel (Arkusz1)]
        ↓
[run_waterfall() — dla kazdej transakcji]
  Pass 0:   Regex numeru faktury → EXACT
  Pass 0.5: 93 reguly statyczne → STATIC_RULE
  Pass 1:   Mappings vendor (242 wpisow) + kwota ±0.005 EUR + okno daty → EXACT
  Pass 1.5: Dopasowanie VAT (21% / 9%) + fuzzy ≥70% → EXACT
  Pass 2:   Kandydaci (kwota ±1 EUR / VAT / fuzzy ≥80%) → SUGGESTED
  Pass 3:   AI (GPT-4o-mini) ≥85% pewnosci → EXACT lub SUGGESTED
  Brak:     UNMATCHED
        ↓
[React Dashboard — tabela z akcjami]
  - EXACT / MANUAL: dopasowane, mozliwosc cofniecia
  - SUGGESTED: Wybierz pozycje / Brak faktury / Brak dopasowania / Odrzuc
  - UNMATCHED: Brak faktury / Brak dopasowania
  - BRAK_FAKTURY: przekreslone na czerwono (zostaje w Do sprawdzenia)
  - BRAK_DOPASOWANIA: niebieskie (zostaje w Do sprawdzenia)
        ↓
[/api/download-report] → Excel z wynikami
```

---

## STATUSY WYNIKOW

| Status | Znaczenie |
| :--- | :--- |
| EXACT | Automatyczne dopasowanie (kwota + data) |
| STATIC_RULE | Regula statyczna (np. Shell → Autokosten) |
| PRIVATE | Przelew wewnetrzny / prywatny / Spaarrekening |
| BANK_FEE | Oplata bankowa |
| SUGGESTED | Propozycje do weryfikacji przez uzytkownika |
| MANUAL | Reczne dopasowanie przez uzytkownika |
| UNMATCHED | Brak kandydatow — wymaga akcji |
| BRAK_FAKTURY | Platnosc bez faktury — sygnalizacja (czerwone) |
| BRAK_DOPASOWANIA | Reczne oznaczenie braku — sygnalizacja (niebieskie) |
| NEW_ENTRY | Odrzucone propozycje |

---

## WYNIKI TESTOW (2026-02-26, bez AI, 10 klientow)

| Klient | TXs | EXACT | Auto |
|--------|-----|-------|------|
| GULBIERZ | 75 | 21 | 42 |
| DYLEWSKI | 96 | 33 | 70 |
| BEDNARSKI | 115 | 32 | 56 |
| HUNADY | 63 | 23 | 31 |
| MARCINIAK | 87 | 33 | 38 |
| NALAZEK | 140 | 73 | 92 |
| OZOROWSKI | 86 | 28 | 68 |
| PIERZGALSKI | 69 | 31 | 34 |
| CHORAZAK | 118 | 70 | 78 |
| KUCIK | 41 | 19 | 26 |
| **RAZEM** | **890** | **363** | **535 (60,1%)** |

False positives: 0

---

## FAZY I CHECKLIST

### FAZA 1: DEVELOPMENT (ZAKONCZONA)
- [x] Parser PDF (angielski + holenderski format ING)
- [x] Parser Excel (.xlsm — Arkusz1, sekcje INKOOP/VERKOOP/BANK)
- [x] Algorytm kaskadowy (Waterfall) — wszystkie etapy
- [x] 93 reguly statyczne (STATIC_RULES)
- [x] Mappings vendor (242 par z learn_from_connected.py)
- [x] Interfejs React — tabela, filtry, statusy, ConflictResolver
- [x] Raport Excel (download)
- [x] Autentykacja (login/haslo)
- [x] Async processing + progress bar
- [x] Wykluczenie Zakelijke Oranje Spaarrekening z dopasowania

### FAZA 2: TESTY AKCEPTACYJNE (W TRAKCIE — marzec 2026)
- [x] Testy na danych TESTY_1603, TESTY_1903, TESTY_2303 itp.
- [x] Poprawki po uwagach 19.03 (merge zakladek, fix telecom, Brak faktury)
- [x] Poprawki po uwagach 23.03 (BRAK_FAKTURY, BRAK_DOPASOWANIA, Spaarrekening, tolerancja kwot)
- [ ] Finalna Lista Uwagi/Bledow (jedno zbiorcze zestawienie wg §7 ust. 3)
- [ ] Protokol Odbioru (Zalacznik nr 2)

### FAZA 3: ODBIÓR I ROZLICZENIE
- [ ] Podpisanie Protokolu Odbioru
- [ ] Faktura za pozostale 70% (8 400 PLN netto)
- [ ] Instalacja na serwerze klienta
- [ ] Przekazanie kodu zrodlowego

---

## CHANGE REQUESTY (poza umowa)

| Data | Opis | Status | Wycena |
| :---: | :--- | :---: | ---: |
| 2026-03-24 | Export wyciagu z adnotacjami BOEKSTUK (2 warianty: Excel lub PDF) | Oczekuje na decyzje klienta | TBD |

---

## KLUCZOWE USTALENIA TECHNICZNE

- **Tolerancja kwot:** 0.005 EUR (od 2026-03-24) — tylko dokladne dopasowania auto-match
- **Okno dat:** -10 do +30 dni (przychody) / -10 do +90 dni (koszty)
- **Spaarrekening:** wykluczone z dopasowania (PRIVATE z nota)
- **Boekstuk:** krotki (<5 znakow) nie triggeruje regex — unika false positive na "1","2"
- **Format PDF holenderski:** DD-MM-YYYY, Incasso, Online bankieren
- **Format PDF angielski:** DD/MM/YYYY, SEPA direct debit, Online Banking

---

## WARUNKI UMOWY (KLUCZOWE)

- **Wartosc:** 12 000 PLN netto (§8)
- **Zaliczka:** 30% = 3 600 PLN w ciagu 7 dni od podpisania (§8 ust. 2a)
- **Reszta:** 70% = 8 400 PLN w ciagu 14 dni od odbioru (§8 ust. 2b)
- **Testy akceptacyjne:** 14 dni roboczych od udostepnienia (§7 ust. 2)
- **Poprawki:** 7 dni roboczych od Lista Uwagi/Bledow (§7 ust. 4)
- **Milczacy odbior:** brak uwag w terminie = odbiór bez zastrzezen (§7 ust. 5)
- **Gwarancja:** 6 miesiecy — tylko niezgodnosc ze Specyfikacja (§9)
- **Prace dodatkowe:** wymagaja aneksu lub e-mail z opisem zakresu i wycena (§5b)
- **Kary za opoznienie Dokodu:** 0,2% Wynagrodzenia/dzien, max 10% (§14a)

---

## RYZYKA

| Ryzyko | Poziom | Mitygacja |
| :--- | :---: | :--- |
| Klient zgloszi uwagi poza Lista Uwagi/Bledow (rozproszone maile) | Sredni | Przypomniec o §7 ust. 3 — jedno zbiorcze zestawienie |
| Nowe formaty PDF/Excel po odbiorze | Niski | §4 ust. 6f — nowy bank to Change Request |
| Zbyt maly procent dopasowania na danych produkcyjnych | Sredni | Wyniki testow 60% (bez AI) / umowny prog 85% lacznie z propozycjami |
| Klient nie zaplacil zaliczki | Nieaktywny | Zaliczka 3 600 PLN wpłynęła ✅ |

---

## LINKI

- Repo: `/home/kacper/DOKODU/FAKTURY_KOSZTY`
- Profil klienta: [[../../20_AREAS/AREA_Customers/GravisGroup/GravisGroup_Profile]]
- Umowa: Umowa o dzielo nr 1/2026, dn. 25.02.2026 (Gravis Group BV)
