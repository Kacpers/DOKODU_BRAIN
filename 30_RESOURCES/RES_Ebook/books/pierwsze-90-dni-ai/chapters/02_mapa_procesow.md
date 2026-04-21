---
n: "02"
title: "Tydzień 1–2: Mapa procesów"
abstract: "Jak zinwentaryzować to, co robią ludzie — zanim zautomatyzujesz. Bez tego każde wdrożenie jest hazardem."
reading_time: "22 min"
level: "Podstawowy"
sections: "2.1 – 2.5"
kicker: "Rozdział drugi"
---

<!-- template: chapter -->
# Tydzień 1–2: Mapa procesów

**Abstrakt:** Przed pierwszym modelem, przed pierwszym narzędziem, przed pierwszym spotkaniem z dostawcą — mapa procesów. Dwa tygodnie pracy, które decydują o całym wdrożeniu.

---

<!-- template: standard -->
## 2.1 Co to znaczy "mapa procesów"

Mapa procesów to lista **wszystkiego, co ludzie w firmie robią powtarzalnie co najmniej raz w tygodniu**, z trzema informacjami przy każdym wpisie: kto to robi, ile to zajmuje, i ile razy w miesiącu. Nic więcej na tym etapie.

To nie jest BPMN. To nie jest Value Stream Mapping. To nie jest wielki workshop z post-itami. To jest arkusz w Excelu (albo Google Sheets, albo Notion) z trzema kolumnami i około 40–120 wierszami.

Dlaczego tak prosto? Bo celem nie jest udokumentować proces — celem jest **znaleźć kandydatów do automatyzacji**. Formalna mapa procesów kosztuje 50–150 tys. PLN i zajmuje 3 miesiące. My robimy to w dwóch tygodniach, bo nie próbujemy opisać wszystkiego — tylko znaleźć 5–10 miejsc, gdzie AI daje realną wartość.

---

<!-- template: standard -->
## 2.2 Kto i jak

**Właściciel mapy:** jedna osoba z zarządu lub senior manager z pełnomocnictwem do rozmawiania z każdym działem. Nie HR, nie IT — operacje albo COO. Ten sam człowiek, który będzie potem właścicielem pilota.

**Metoda:** 30-minutowe rozmowy z **liderami każdego działu**. Nie z całymi zespołami — z liderami. Jedno pytanie otwierające: *"Na co Państwa ludzie marnują najwięcej czasu w ciągu miesiąca?"* Potem dopytki.

**Efekt po rozmowie:** 5–15 pozycji w arkuszu. Po 8 rozmowach mają Państwo 40–120 pozycji. Wystarczy.

> **‡** Definicja: **Lider działu** — osoba odpowiedzialna za wyniki zespołu 3–15 osób. W małej firmie często sam właściciel, w średniej — head of ops, head of sales, CFO. Nie delegują tego zadania dalej.

---

<!-- template: info -->
## 2.3 Wzór arkusza

Poniżej struktura, której używamy u klientów. Kopiujecie Państwo, wypełniacie przez 2 tygodnie, zostawiacie — wraca do niej dopiero w rozdziale 3.

![Przykładowe 8 pozycji w arkuszu procesów, z kolumną bólu zaznaczoną kolorem](assets/process_map_preview.svg)

**Kolumny (w tej kolejności):**

1. **ID** — numer 001, 002, 003. Do łatwego odwoływania się.
2. **Dział** — jednowyrazowo (Sprzedaż, Operacje, HR, Finanse, Produkcja).
3. **Proces** — jedno zdanie, bez żargonu. *"Przygotowuje raport miesięczny dla zarządu"*, nie *"Cross-funkcyjna konsolidacja KPI"*.
4. **Kto robi** — rola, nie imię. *"Analityk finansowy"*, nie *"Kasia"*.
5. **Czas / wykonanie** — w minutach. *"45 min"*.
6. **Częstotliwość / miesiąc** — liczba całkowita. *"4"*, *"20"*, *"120"*.
7. **Czas / miesiąc** — kolumny 5 × 6. Excel policzy.
8. **Bolączka 1–5** — subiektywna ocena lidera: jak bardzo ten proces "boli". 1 = nikt nie narzeka, 5 = wszyscy go nienawidzą.

To wszystko. Żadnego "ownera procesu", "SLA", "inputów i outputów". Osiem kolumn, 80 wierszy, dwa tygodnie.

---

<!-- template: cheat -->
## 2.4 Cheat sheet: 6 zasad rozmów z liderami

Po kilkudziesięciu tego typu rozmowach wyciągnęliśmy 6 zasad, które skracają spotkanie do 30 minut i dają użyteczny output.

1. **Najpierw pytanie otwierające, nie kwestionariusz** → *"Na co marnujecie najwięcej czasu?"* otwiera głowy. Excel pokazuje się dopiero w 15. minucie.

2. **Pytajcie o miesiąc, nie o dzień** → Dzień jest chaotyczny i pełen wyjątków. W miesiącu widać wzorce. *"Co robicie regularnie co miesiąc?"* daje lepszy sygnał niż *"Jak wygląda typowy dzień?"*.

3. **Pytaj o powtarzalność, nie o technologię** → Jeśli lider mówi *"używamy Excela do raportów"*, nie pytaj o Excel. Pytaj, **co wchodzi w raport i skąd to ściągają**. Technologia jest po naszej stronie stołu.

4. **Zapisuj dosłownie jedno zdanie opisu** → Dłuższe opisy oznaczają, że lider sam jeszcze nie wie, co to za proces. Wtedy warto zrobić follow-up, ale nie rozszerzać pól w arkuszu.

5. **Oceniaj bolączkę na żywo** → Pytaj wprost: *"Gdybyś mógł to jutro usunąć z życia Kasi, to ile by się ucieszyła?"*. Odpowiedź 4 lub 5 = kandydat do automatyzacji. 1 lub 2 = zostaw.

6. **Kończcie rozmowę z konkretną listą, nie z "przemyślę"** → Na koniec 30 minut musicie Państwo wyjść z 5–15 pozycjami. Jeśli nie macie — rozmowa była zbyt ogólna, umówcie drugi termin.

---

<!-- template: standard -->
## 2.5 Co teraz nie robić

Po dwóch tygodniach mają Państwo arkusz. **Nie eliminujcie jeszcze kandydatów.** Nie rankingujcie. Nie pokazujcie dostawcom AI. Nie liczcie ROI.

To jest rozdział 3. Teraz po prostu zamknijcie dokument i idźcie do następnej pracy. W następnym tygodniu wrócicie Państwo z chłodną głową, dodacie dwie kolumny ("wartość roczna", "ryzyko wdrożenia") i zobaczycie wyraźnie 3–5 kandydatów, którzy wyróżniają się od reszty.

Jedna drobna uwaga: w międzyczasie lider, z którym Państwo rozmawiali, prawdopodobnie przyśle dwa–trzy pomysły, które przyszły mu do głowy po rozmowie. Dopiszcie do arkusza. To są często najlepsze kandydatury, bo wymagały aktywnego myślenia.

> [!warning]
> **Nie pokazujcie Państwo arkusza dostawcom AI na tym etapie.** Oni zobaczą w nim wszystko, co da się zautomatyzować, i będą proponować pakiet na 1.8 mln PLN. W rozdziale 3 odfiltrujecie Państwo 95% pozycji. Wtedy rozmowa z dostawcą ma sens.
