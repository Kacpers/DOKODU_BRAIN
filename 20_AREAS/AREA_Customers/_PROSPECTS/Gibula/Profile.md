---
type: prospect
status: discovery
owner: kacper
created: 2026-03-30
wartosc_est: 62 000–66 000 PLN netto
tags: [prospect, holandia, faktury, webapp, custom-dev]
---

# Administratiekantoor Gibula

## Dane kontaktowe
- **Kontakt:** Jakub Gibula (właściciel), Grzegorz Gibula
- **Email:** adm.kantoor.gibula@gmail.com
- **Telefon:** +31 616 951 592, +31 651 103 061
- **Godziny:** Pn-Czw 9:00-17:30, Pt 9:00-16:00, Sob nieczynne

## O firmie
- Holenderskie biuro rachunkowe (administratiekantoor)
- Obsługuje klientów prowadzących firmy w Holandii
- Już korzysta z aplikacji do łączenia faktur z kontami bankowymi (reconciliation — zrobione przez Dokodu)

## Projekt: System fakturowy (webapp)
- **Cel:** Platforma webowa gdzie klienci Gibuli mogą wystawiać faktury
- **Spec:** `Program_factuur_spec.xlsx` w tym katalogu
- **Wybrany wariant:** MINIMUM + ROZSZERZONA (połączenie) + bramka płatności
- **Wycena wysłana:** 25-30k (min) / **62-66k (rozszerzona + płatności)** / 70-85k (pełna) PLN netto
- **Reakcja klienta:** Pozytywna, błyskawiczna odpowiedź, chce się spotkać
- **Uwagi programu reconciliation:** Działa, w maju mogą pojawić się dodatkowe uwagi gdy cały zespół zacznie z niego pracować

### Odpowiedzi Jakuba na pytania (email 31.03.2026)

**Model biznesowy:**
- Na początek **tylko klienci Gibuli + oni sami**, później wejście na rynek dla innych przedsiębiorców i księgowych
- **Abonament miesięczny** — automatyczna płatność z konta klienta (jeden pakiet na start)
- Docelowo **500+ klientów**
- **Bonusy za polecenie** — klient poleca przez swój link → dostaje zniżkę na abonament za księgowość

**Faktury i dokumenty:**
- Typy: **Factuur, pro-forma, creditnota** (paragon/bon NIE)
- BTW: **21%, 9%, 0%, BTW verlegd, BTW vrijgesteld, BTW marge regel**
- Waluta: **tylko EUR**
- Szablony: klient musi mieć możliwość dodania **logo**
- Numeracja: domyślnie 01-2026, kolejne numery, z możliwością ręcznej zmiany

**Integracje:**
- Peppol: na start **eksport UBL/XML** (nie pełna integracja)
- "Połączenie z księgowym": **jednym przyciskiem auto-księgowanie** z danego kwartału do ich programu (ten sam, do którego Kacper zrobił reconciliation!)
- Integracja z innym oprogramowaniem: **tak, na późniejszym etapie** (programy księgowe popularne w NL)
- Płatności: **kod QR na fakturze** do szybkiej płatności

**Funkcje dodatkowe:**
- Magazyn: **na późniejszym etapie**
- Godzinówka/kilometrówka: **proste**, bez GPS
- **Przypomnienia o płatności + oficjalne wezwania do zapłaty**
- Raporty: **obrót ze wszystkich faktur + koszty → kwota do opodatkowania**
- Instrukcje video: linki do YouTube — tak

**Języki:**
- Interfejs: **polski na start**, później holenderski, angielski, ukraiński, rumuński, bułgarski
- Język na fakturze: **holenderski**, później angielski

**Użytkownicy:**
- Każdy klient **jedno konto** z loginem
- Weryfikacja przez **Holenderską Izbę Handlową (KVK)** — zabezpieczenie przed oszustwami

### Wizja Jakuba (cytat kluczowy)
> "Chcemy uprościć życie naszym klientom żeby nie musieli wysyłać do nas swoich wystawionych faktur tylko same koszty, a dwa sobie ułatwić tym że za pomocą jednego przycisku automatycznie wszystkie wystawione faktury księgują u nas w programie. Na etapie jak to będzie dobrze działało chcemy wyjść z tym produktem dla przedsiębiorców oraz księgowych."

## Następne kroki
- [ ] **Sobota 04.04, 9:30** — Call z Jakubem (WhatsApp) — potwierdzić zakres, omówić bramkę płatności (Stripe vs Mollie), ustalić finalną cenę
- [ ] Po callu: precyzyjna wycena + umowa
- [ ] Reconciliation: czekamy na feedback zespołu (maj)

## Historia korespondencji

### Email #1 — Jakub → Kacper (30.03.2026, 09:59)
**Temat:** NOWY PROJEKT DO WYCENY
Przesłał spec (Program_factuur_spec.xlsx) — opis systemu fakturowego.

### Email #2 — Kacper → Jakub (30.03.2026, 12:11)
20 pytań technicznych + wstępna wycena w 3 wariantach (25-30k / 50-60k / 70-85k). Propozycja podejścia etapowego.

### Email #3 — Jakub → Kacper (30.03.2026, 12:17)
Entuzjastyczna odpowiedź, propozycja calla na sobotę 04.04 9:30. Brak uwag do reconciliation na teraz.

### Email #4 — Jakub → Kacper (31.03.2026, 13:08)
**Pełne odpowiedzi na 20 pytań.** Wybrał połączenie wersji minimum + rozszerzonej. Kluczowe: auto-księgowanie jednym przyciskiem, 500+ klientów docelowo, abonament, KVK verification, QR na fakturze. Wizja: zacząć dla siebie → wyjść na rynek NL.

### Email #5 — Jakub → Kacper (01.04.2026)
Potwierdzenie calla sob 9:30. Dodatkowe uwagi:
- Oferty = faktury z opisem "OFERTA", oferta → faktura jednym kliknięciem
- Chce bramkę płatności już w v1.0 (nie v2) — pełna automatyzacja, blokada dostępu przy braku wpłaty
- Lista programów księgowych NL: Exact Online, AFAS, Twinfield, Moneybird, e-Boekhouden.nl, SnelStart, Yuki — wszystkie obsługują import z Excela

### Email #6 — Kacper → Jakub (01.04.2026)
Potwierdzenie calla sob 9:30 (WhatsApp). Odpowiedzi:
1. Moduł ofertowy w v1.0 — oferta → faktura jednym kliknięciem
2. Bramka płatności dodana do v1.0 — sugestia Stripe lub Mollie (iDEAL), Gibula zakłada własne konto, prowizja ~1-2%
3. Zaktualizowana wycena: **62 000 – 66 000 PLN netto** (było 50-60k)
4. Uniwersalny generator Excel dla programów NL (Exact, AFAS, Yuki itd.)

### Email (osobny wątek) — Jakub → Kacper (30.03.2026, 15:15)
**Temat:** Re: PYTANIA DO UMOWY (wątek reconciliation)
Bug report: w zakładce "Do sprawdzenia" przyciski "Brak faktury"/"Brak dopasowania" nie da się cofnąć. Kacper naprawił tego samego dnia (30.03 10:59).
