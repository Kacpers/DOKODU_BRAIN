---
type: area
status: active
owner: kacper
last_reviewed: 2026-03-06
tags: [crm, leady, sprzedaz, pipeline, b2b, discovery]
---

# CRM — LEADY B2B DOKODU
> **Zasada:** Kazdy lead, z ktorym rozmawiasz, trafia tu. Bez wyjatkow.
> **Stage'y pipeline:** Nowy → Kontakt → Discovery → Propozycja → Negocjacje → WYGRANA / PRZEGRANA / Odlozona

---

## PIPELINE AKTYWNY

<!-- SYNC:PIPELINE -->
| # | Firma | Kontakt | Zrodlo | Etap | Wartosc (PLN) | Nastepny krok | Deadline |
| :- | :--- | :--- | :--- | :--- | ---: | :--- | :---: |
| 1 | Animex | Kamil Kowalski | Ref. | WYGRANA | 40 000 | Faktura wystawiona, certyfikaty do wysłania ASAP. Sesje konsultacyjne czekają na security review n8n. | 2026-04-08 |
| 2 | Corleonis | [imie] | LinkedIn | Odłożona | 35 000 | WSTRZYMANE — klient poprosił o pauzę. Nie kontaktować do odwołania. | — |
| 3 | TenderScope | Borys Kowalik | Inbound (dokodu.it) | Kontakt | ~20 000 | Czekamy na odpowiedzi techniczne → wycena | 2026-04-03 |
| 4 | Adm. Gibula | Jakub Gibula | Istniejący klient | WYGRANA | 66 000 | Faktura za reconciliation OPŁACONA. Następny krok: faktura zaliczkowa po podpisaniu umowy. | 2026-04-15 |
| 5 | Cichy-Zasada (dealer VW/Audi/Porsche) | Rafał Nawrocki | Inbound (dokodu.it) | Odłożona | — | Chcą tylko licencję n8n, brak projektu wdrożeniowego | — |
| 6 | SayFlu | Krystian | LinkedIn DM | Propozycja | do wyceny | Info przekazane na Messengerze (znajomy Kacpra). Czekamy na akceptację i dalsze info od Krystiana. | — |
| 7 | LexLegali | Marcin Chrostek / Danuta Zawada-Miernik | Kontakt Kacpra | Propozycja | 35 000 | Spotkanie 20 lub 21.04 — Alina potwierdza datę. Oferta Automotive-Legal 32k+3k wysłana. | 2026-04-21 |
| 8 | COP Kartoszyno (Kwatery Pracownicze) | — | Inbound | WYGRANA | 10 000 | Renegocjacja 10.04 — stanęło na 10k netto. Robimy. | — |
<!-- /SYNC:PIPELINE -->

**Pipeline Value (otwarty):** ___ PLN
**Weighted Pipeline (×proc. konwersji):** ___ PLN

---

## PROTOKOL KWALIFIKACJI LEADU (BANT+)

Zanim powiesz "tak" do discovery call, sprawdz:

| Kryterium | Pytanie kwalifikacyjne | Minimum |
| :--- | :--- | :--- |
| **B**udget | "Czy maja budzet na wdrozenie AI >10k PLN?" | TAK |
| **A**uthority | "Czy moj kontakt moze podpisac umowe, czy potrzebuje zgodny?" | CEO/CFO/Dyrektor |
| **N**eed | "Czy maja realny, bolesny problem, ktory automatyzacja rozwiaze?" | Tak, nazwany |
| **T**imeline | "Czy planuja dzialac w ciagu 3 miesiecy?" | <6 mies. |
| **+Fit** | "Czy firma jest w naszym ICP (50-500 prac., branza operacyjna)?" | TAK |

**Jezeli odpowiedz na 3+ jest NIE → lead jest niekwalifikowany. Wrzuc do nurturingu.**

---

## DISCOVERY CALL FRAMEWORK (45-60 min)

### Otwarcie (5 min)
- Przedstaw sie krotko (Dokodu = agencja tech + legal, nie kurs)
- Ustal agenda i cel rozmowy: "Na koncu tej rozmowy chce wiedziec, czy mozemy Wam pomoc. Wy tez bedziecie wiedziec, czy jestesmy dobrym partnerem."

### Diagnoza (20-25 min) — suchaj 80%, mow 20%
1. "Jak wygladaja u Was procesy, ktore Cie bola najbardziej? Opowiedz mi o typowym dniu w zespole."
2. "Co probowaliscie do tej pory? Co zadzialalo, co nie?"
3. "Co sie dzieje, jezeli tego NIE rozwiazecie w ciagu 6 miesiecy?"
4. "Kto jeszcze jest zaangazowany w te decyzje w Waszej firmie?"
5. "Jak wyglada Wasz budzet na digitalizacje/AI na ten rok?"

### Prezentacja (10 min) — powiazana z bólem
- NIE prezentuj deck Dokodu generycznie
- Mow TYLKO o tym, co rozwiaze ich problem
- Uzyj 1-2 analogii do ich branzy

### Nastepny krok (5 min)
- ZAWSZE konczac na konkretnym dzialaniu: "Wyslam Wam propozycje do [data]. Mozemy sie spotkac [dzien] o [godz.] zeby omowic?"
- Jezeli sa niezdecydowani: "Co byloby potrzebne, zebyscie mogli podjac decyzje?"

---

## SZABLONY KOMUNIKACJI

### Email: Po Discovery Call
```
Temat: Podsumowanie rozmowy + proponowane nastepne kroki | Dokodu × [Firma]

Czesc [Imie],

Dziekuje za rozmowe. Pare kluczowych rzeczy, ktore zanotowalam:

Problem: [1 zdanie o ich bólu]
Cel: [co chca osiagnac]
Termin: [kiedy chca dzialac]

Zgodnie z ustaleniami, do [data] wysle Wam wstepna propozycje/wycene.

Gdyby cos sie zmienilo lub pojawily sie pytania — jestem dostepny.

Kacper
```

### Email: Follow-up (brak odpowiedzi po 5 dniach)
```
Temat: Szybkie pytanie — [Firma] × Dokodu

[Imie], wyslalem propozycje [data] — chcialem sie upewnic, ze dotarla i nie wpadla w spam.

Czy mieles/mielas chwile na przeglad?

(Rozumiem, ze to piekny miesiac — jesli potrzebujesz wiecej czasu, po prostu daj znac.)

Kacper
```

### Email: Przebudzenie (lead "przegrzany" — brak kontaktu >30 dni)
```
Temat: Cos co Cie moze zainteresowac | [Firma]

[Imie], rozmawialismy [data] o [temat].

Od tamtej pory zrealizowalismy projekt dla [branzy podobnej — anonimizowane], gdzie [efekt liczbowy].

Pomyslalem, ze to moze byc interesujace dla Ciebie. Chcesz 15-minutowa rozmowe?

Kacper
```

---

## BAZA LEADOW (Odlozeni / Nurturing)

| Firma | Kontakt | Powod odlozenia | Kiedy wrocic |
| :--- | :--- | :--- | :---: |
| | | | |

**Nurturing content:** Co miesiac wyslac 1 wartosciowy email (case study, narzedzie, tip). NIE sprzedajacy. Budujacy zaufanie.

---

## NOTATKI O LEADACH

### TenderScope sp. z o.o.
```
**Firma:** TenderScope sp. z o.o.
**Branza:** GovTech / Przetargi publiczne
**Wielkosc:** Startup (inkubowany w HugeTECH Revolution)
**Kontakt:** Borys Kowalik | CEO/Founder | boryskowalik@gmail.com | 574 555 940
**Adres:** ul. Stanisława Moniuszki 11, 35-015 Rzeszów
**Zrodlo leadu:** Inbound — formularz biuro@dokodu.it
**Data pierwszego kontaktu:** 2026-03-30
**Problem klienta:** Moduł półautomatycznego uzupełniania danych wykonawcy w dokumentach przetargowych (DOCX + edytowalne PDF). Python, python-docx, pypdf. Integracja z ich istniejącą aplikacją.
**Budzet orientacyjny:** Dofinansowanie UE (FEPW 2021-2027, "HugeTECH Revolution") — budżet przydzielony z góry
**Decydent:** Borys Kowalik (prawdopodobnie jedyny decydent — startup)
**Timeline klienta:** 28 dni roboczych od zlecenia. Wycenę potrzebują ASAP.
**Historia rozmow:**
- [2026-03-30 17:05]: Borys wysłał zapytanie ofertowe na biuro@dokodu.it — formalny RFQ z opisem przedmiotu zamówienia (2 zadania: mapowanie danych + integracja z aplikacją). Załącznik: "Formularz szacowania wartości zamówienia.docx"
- [2026-03-31 ~12:00]: Alina rozmawiała telefonicznie z Borysem
- [2026-03-31 12:48]: Alina wysłała email z 10 pytaniami technicznymi (typy dokumentów, API, mapowanie pól, kryteria odbioru). Obiecała ofertę do 03.04.
**Status:** Kontakt — czekamy na odpowiedzi techniczne
**Nastepny krok:** Po odpowiedziach Borysa → przygotować wycenę + wypełnić formularz szacowania
```

### Cichy-Zasada sp.j.
```
**Firma:** Cichy-Zasada sp.j.
**Branza:** Automotive / Dealerzy samochodów (VW, Seat, Cupra, Audi, Porsche)
**Wielkosc:** Średnia (dealer group, własny dział IT)
**Kontakt:** Rafał Nawrocki | rafal.nawrocki@cichy-zasada.pl | +48 882 375 188
**Zrodlo leadu:** Inbound — formularz dokodu.it (1.04.2026 06:31)
**Data pierwszego kontaktu:** 2026-04-01
**Problem klienta:** Chcą wdrożyć n8n Business. Obawy o KSEF-compliance faktur od n8n (firma zagraniczna). Szukają pośrednika w zakupie licencji + wsparcia merytorycznego przy wdrożeniu. Mają własne serwery i dział IT.
**Budzet orientacyjny:** ~25 000 PLN (wdrożenie + szkolenie), licencja n8n Business osobno (~$660/mies.)
**Decydent:** Rafał Nawrocki (do potwierdzenia — może być IT Manager, nie decydent budżetowy)
**Timeline klienta:** Aktywnie szukają rozwiązania — szybki timeline
**Historia rozmow:**
- [2026-04-01 06:31]: Rafał wysłał zapytanie przez formularz dokodu.it — pytania o licencję n8n, wsparcie wdrożeniowe, koszty
- [2026-04-01 ~09:00]: Kacper wysłał maila do n8n (formularz n8n.io) z pytaniem o reseller/partner program
**Status:** Kontakt — czekamy na odpowiedź n8n ws. modelu licencyjnego
**Nastepny krok:** Po odpowiedzi n8n → oddzwonić do Rafała z propozycją (wdrożenie + szkolenie + opcja licencji)
```

### SayFlu (agencja)
```
**Firma:** SayFlu
**Branza:** Agencja (product placement, marketing — ta sama co Nvidia PP)
**Wielkosc:** ~15 osób (zespół wewnętrzny)
**Kontakt:** Krystian | LinkedIn DM
**Zrodlo leadu:** LinkedIn — Krystian napisał bezpośrednio
**Data pierwszego kontaktu:** 2026-04-04
**Problem klienta:** Chce przeszkolić zespół z Gemini w Google Workspace — przyspieszenie pracy
**Budzet orientacyjny:** Do wyceny
**Decydent:** Do potwierdzenia (Krystian pyta o cenę — może być decydent lub delegowany)
**Timeline klienta:** Aktywnie szuka — szybkie zapytanie
**Oferta:** [Oferta_Szkolenie_Gemini.md](../AREA_Customers/_PROSPECTS/SayFlu/Oferta_Szkolenie_Gemini.md)
**Historia rozmow:**
- [2026-04-04]: Krystian pyta na LI o cenę i zakres szkolenia. Kacper dopytuje. Ustalone: Gemini w Google, 14-15 osób, zespół wewnętrzny. Kacper obiecał przygotować ofertę.
- [2026-04-08]: Oferta wysłana. Krystian: "pewnie w piątek lub weekend będę przeglądał". Chce spotkanie w przyszłym tygodniu, będzie miał pytania. Umówili się że Kacper odezwie się w poniedziałek 14.04.
**Status:** Propozycja — oferta wysłana, czeka na przegląd
**Nastepny krok:** Pn 14.04 — odezwij się, umów spotkanie na tydzień 14-18.04
```

### [Nazwa Firmy] — szablon notatki
```
**Firma:**
**Branza:**
**Wielkosc:** ___ pracownikow
**Kontakt:** Imie Nazwisko | stanowisko | email | tel
**Zrodlo leadu:**
**Data pierwszego kontaktu:**
**Problem klienta:**
**Budzet orientacyjny:** PLN
**Decydent:**
**Timeline klienta:**
**Historia rozmow:**
- [data]: [co omawiano]
**Status:** [Etap pipeline]
**Nastepny krok:**
```

---

## METRYKI SPRZEDAZOWE (Miesiec)

| Metryka | Cel | Aktualne |
| :--- | ---: | ---: |
| Nowe leady | 12 | ___ |
| Discovery calls | 6 | ___ |
| Wyslane propozycje | 3 | ___ |
| Wygrane kontrakty | 1-2 | ___ |
| Wskaznik konwersji | 25% | ___% |
| Srednia wartosc kontraktu | 25 000 PLN | ___ PLN |

---

*Aktualizuj po kazdej rozmowie sprzedazowej. Nie tydzien pozniej. Teraz.*
