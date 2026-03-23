---
type: resource
status: active
owner: both
last_reviewed: 2026-03-06
tags: [szablony, emaile, dokumenty, propozycja, nps, cr, dpia]
---

# SZABLONY DOKODU — Reusable Templates
> Gotowe do uzycia. Kopiuj → wypelnij pola w [NAWIASACH] → wyslij/uzyj.

---

## SZABLONY KOMUNIKACJI

### T-001: Email po Discovery Call
```
Temat: Podsumowanie rozmowy [DATA] + nastepne kroki | [FIRMA] × Dokodu

Czesc [IMIE],

Dziekuje za rozmowe. Bardzo pomocna — szczegolnie Twoj komentarz o [KONKRETNA_RZECZ].

Jak to rozumiem, Wasza glowna potrzeba to:
→ [PROBLEM_1_ZDANIE — uzyj ich slow!]

Obiecalem wyslan propozycje do [DATA]. Zrobie to.

Gdyby pojawily sie pytania przed tym czasem — jestem dostepny pod tym mailem lub telefonicznie.

Kacper Sieradzinski
CEO | Dokodu sp. z o.o.
📱 [tel] | 🌐 dokodu.it
```

---

### T-002: Propozycja — Executive Summary (fragment)
```
# PROPOZYCJA WSPOLPRACY
## [NAZWA PROJEKTU] — [KLIENT] × Dokodu

---

### Rozumiemy Wasz problem

[KLIENT] zmaga sie z [PROBLEM_ICH_SLOWAMI]. Skutek: [KONSEKWENCJA_LICZBOWA_LUB_OPISOWA].

Proba wewnetrznego rozwiazania przez [POPRZEDNIE_PODEJSCIE] nie dala oczekiwanych efektow,
poniewaz [DLACZEGO_NIE_ZADZIAŁALO].

### Nasze podejscie

Zamiast kolejnego narzedzia, proponujemy [KROTKI_OPIS_ROZWIAZANIA].

Efekt, ktorego sie spodziewamy: [CEL_1], [CEL_2], [CEL_3].

Zrobilismy to juz dla [PODOBNA_FIRMA_LUB_BRANZA] — [WYNIK_LICZBOWY].

### Investycja

| Opcja | Zakres | Cena | Timeline |
| :--- | :--- | ---: | :---: |
| A — MVP | [zakres A] | [CENA_A] PLN netto | [X] tygodni |
| B — Kompleksowe | [zakres B] | [CENA_B] PLN netto | [X] tygodni |

### Nastepny krok

Jezeli chcesz ruszyc z Opcja [A/B] — wyslij nam potwierdzenie do [DATA].
Przygotujemy umowe i harmonogram w ciagu 48h.

W razie pytan — zadzwon lub napisz.
```

---

### T-003: Status Update Tygodniowy
```
Temat: Status Update — [PROJEKT] — Tydzien [NR] | [DATA_PONIEDZIALEK]-[DATA_PIATEK]

Czesc [IMIE],

Szybki update z tego tygodnia.

STATUS: [ZIELONY / ZOLTY — opis / CZERWONY — opis blokady]

ZROBIONE W TEN TYDZIEN:
✅ [zadanie 1]
✅ [zadanie 2]
⚠️ [zadanie 3 — w trakcie, bez opoznien]

PLAN NA NASTEPNY TYDZIEN:
📌 [zadanie 1]
📌 [zadanie 2]

POTRZEBUJEMY OD WAS (do [DATA]):
→ [KONKRETNA AKCJA / DECYZJA]
(bez tego moze nas to opoznic o [X] dni)

Pytania? Odpisz lub zadzwon.

Kacper
```

---

### T-004: NPS Survey (po projekcie)
```
Temat: Krotkie pytanie (1 minuta) | [PROJEKT] — Dokodu

Czesc [IMIE],

Projekt dobiegł konca — czas na szczere podsumowanie z Twojej strony.

3 szybkie pytania:

1. Na skali 0-10, jak bardzo poleciłbyś/polecilabys Dokodu znajomemu?
   [0 — zdecydowanie nie] [10 — zdecydowanie tak]

2. Co zrobiliśmy najlepiej? (1-2 zdania)

3. Co mogliśmy zrobic lepiej? (1-2 zdania — szczerosc jest bezcenna)

[LINK DO FORMULARZA lub odpowiedz bezposrednio na tego maila]

Dziekuje za czas i wspolprace.

Kacper
```

---

### T-005: Wezwanie do Zaplaty (pierwsza wiadomosc)
```
Temat: Faktura [NR_FAKTURY] — uprzejme przypomnienie

Czesc [IMIE],

Chciałem jedynie przypomnicc, ze faktura [NR_FAKTURY] na kwote [KWOTA] PLN
miala termin platnosci [DATA_TERMIN].

Jezeli platnosc juz zostala zrealizowana — prosze zignoruj tę wiadomosc.

Jezeli pojawil sie jakis problem z platnoscia lub masz pytania — chętnie pomoge.

Z powazaniem,
Kacper Sieradzinski | Dokodu sp. z o.o.
NIP: 5882473305
```

---

## SZABLONY DOKUMENTOW

### T-010: Notatka z projektu (Project Note)
```markdown
# Notatka: [TEMAT]
**Projekt:** [PROJEKT]
**Data:** [YYYY-MM-DD]
**Autor:** [Kacper / Alina]
**Uczestnicy:** [lista]

## Kluczowe ustalenia
-

## Decyzje podjete
-

## Akcje (kto / co / do kiedy)
| Kto | Akcja | Deadline |
| :--- | :--- | :---: |
| | | |

## Pytania otwarte
-
```

---

### T-011: DPIA Template (szkic — Alina finalizuje)
```markdown
# DPIA — [NAZWA SYSTEMU / PROJEKTU]
**Klient:** [NAZWA]
**Data:** [YYYY-MM-DD]
**Prowadzacy:** Alina Sieradzinska (COO/Legal, Dokodu)
**Status:** SZKIC — wymaga weryfikacji prawnika

---

## 1. OPIS PRZETWARZANIA

**Cel przetwarzania:**
[Opis celu — po co zbieramy/przetwarzamy dane]

**Kategorie danych osobowych:**
- [np. imie i nazwisko, email, NIP, IP]

**Kategorie podmiotow danych:**
- [np. pracownicy klienta, klienci klienta]

**Podstawa prawna (Art. 6 RODO):**
- [wskazac konkretny punkt]

**Odbiorcy danych:**
- Wewnetrzni: [lista]
- Zewnetrzni (podmioty przetwarzajace): [lista, w tym dostawcy AI]

**Transfer poza UE:**
- Tak / Nie — [jesli tak: podstawa transferu, kraj]

**Czas retencji:**
- [opis]

---

## 2. OCENA NIEZBEDNOSCI I PROPORCJONALNOSCI
[Czy nie mozna osiagnac celu z mniejsza iloscia danych?]

---

## 3. MAPA RYZYK

| Ryzyko | Prawdopodob. | Skutek | Ryzyko laczne | Mitygacja |
| :--- | :---: | :---: | :---: | :--- |
| Nieuprawniony dostep do danych | Srednie | Wysokie | Wysokie | Szyfrowanie, Vault, MFA |
| Wyciek do dostawcy AI | Niskie | Wysokie | Srednie | Anonimizacja przed AI |
| Utrata danych | Niskie | Srednie | Niskie | Backup, replikacja |
| | | | | |

---

## 4. SRODKI TECHNICZNE I ORGANIZACYJNE
- Szyfrowanie: AES-256 at rest, TLS 1.3 in transit
- Kontrola dostepu: role-based, least privilege
- Logi: 12 miesiecy, immutable
- Anonimizacja PII przed wyslaniem do AI
- Regularne testy bezpieczenstwa

---

## 5. WNIOSEK
Ryzyko rezydualne po wdrozeniu srodkow: [NISKIE / SREDNIE / WYSOKIE]
Rekomendacja: [Mozna wdrozyc / Wymaga dodatkowych srodkow / Wstrzymac]
```

---

### T-012: Change Request (Zmiana Zakresu)
```markdown
# CHANGE REQUEST #[NR]
**Projekt:** [NAZWA]
**Data:** [YYYY-MM-DD]
**Zglaszajacy:** [Kacper / Klient]

## Opis zmiany
[Co konkretnie chce sie zmienic / dodac / usunac]

## Uzasadnienie
[Dlaczego ta zmiana jest potrzebna]

## Wplyw na zakres
[Co nowego wchodzi, co ewentualnie wypada]

## Wplyw na harmonogram
Szacunkowe opoznienie: [X dni / brak wplywu]

## Wplyw na budzet
Dodatkowy koszt: [X PLN netto] (szacunek: [X]h × [stawka] PLN/h)

---

## AKCEPTACJA

| Strona | Imie i Nazwisko | Data | Podpis |
| :--- | :--- | :---: | :---: |
| Dokodu | Kacper Sieradzinski | | |
| Klient | [Imie Nazwisko] | | |
```

---

## SZABLONY WEWNETRZNE

### T-020: Retrospektywa Projektu (po zakonczeniu)
```markdown
# RETROSPEKTYWA: [PROJEKT]
**Data zakonczenia:** [DATA]
**Prowadzacy:** Kacper + Alina (30 min)

## CO POSZLO DOBRZE
-

## CO POSZLO ZLE LUB MOGLO BYC LEPIEJ
-

## CO ZROBIMY INACZEJ W NASTEPNYM PROJEKCIE
-

## WNIOSKI DO BLUEPRINTOW (co dodac / zaktualizowac?)
-

## WNIOSKI DO SALES PLAYBOOK
-

## POTENCJAL UPSELL / KOLEJNY PROJEKT
-

## NPS KLIENTA
Score: [X/10]
Komentarz: [cytat]
```
