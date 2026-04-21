---
n: "06"
title: "Tydzień 9–10: Rollout i trening zespołu"
abstract: "Najtrudniejsza część wdrożenia to nie technologia — to ludzie. 6 zasad, które działają."
reading_time: "18 min"
level: "Średniozaawansowany"
sections: "6.1 – 6.4"
kicker: "Rozdział szósty"
---

<!-- template: chapter -->
# Tydzień 9–10: Rollout i trening zespołu

**Abstrakt:** Po pilocie mają Państwo działający workflow. Teraz 5–20 osób ma zacząć go używać. To moment, w którym 40% wdrożeń się wywraca — nie z winy technologii.

---

<!-- template: standard -->
## 6.1 Dwa poziomy rolloutu

**Rollout poziom 1 — wewnątrz działu właściciela procesu.** To się dzieje automatycznie pod koniec pilota. Zespół właściciela już widział wyniki, czasem sam pomagał. Żadnej akcji nie trzeba, oprócz formalnego ogłoszenia: *"Od poniedziałku raport robimy tą drogą"*.

**Rollout poziom 2 — do innych działów, które korzystają z wyniku.** To jest trudne. Zarząd dostaje raport, ale nie robi z nim tego, co przed AI. Dział HR dostaje nowe dane o zatrudnieniu, ale nie wie, czy może im ufać. To miejsce, gdzie wypada co drugi pilot.

Rozdzielajcie Państwo te dwa poziomy świadomie. Poziom 1 kończycie w tygodniu 9, poziom 2 rozpoczynacie dopiero w tygodniu 10 — po tygodniu obserwacji.

---

<!-- template: cheat -->
## 6.2 Cheat sheet: 6 zasad rolloutu do innych działów

1. **Nazywaj AI "nowym procesem", nie "AI"** → *"Od poniedziałku raporty przychodzą nowym kanałem"* działa. *"Wdrożyliśmy AI do raportów"* uruchamia połowę działu do dyskusji o zagrożeniach. Nazwa "AI" jest marketingowa dla dostawcy, nie dla użytkownika.

2. **Pokaż porównanie strona-w-stronę** → W pierwszym tygodniu wysyłacie Państwo dwa raporty: stary i nowy. Użytkownicy sami zobaczą, że są identyczne. To szybciej niż jakiekolwiek zapewnienia.

3. **Jedno szkolenie 30 min, nie tydzień workshopów** → Jeśli rollout wymaga 3-dniowego szkolenia, pilot był za szeroki. Cofnijcie Państwo do rozdziału 3 i zwężcie zakres.

4. **Jeden kanał na feedback, jedna osoba go czyta** → Slack, e-mail, formularz — nieważne. Ważne, że jeden. I jedna osoba (zwykle właściciel procesu) odpowiada na każdą uwagę w 24h.

5. **Nie mów o oszczędnościach w komunikacji do zespołu** → *"Dzięki temu zespół X będzie mógł zająć się Y"* działa. *"Oszczędzimy 40% czasu"* generuje pytanie "to kogo zwalniacie". Zarząd słyszy ROI, zespół słyszy groźbę.

6. **Plan "wycofania" jako wypisane w komunikacji** → *"Jeśli przez 2 tygodnie będzie gorzej niż wcześniej, wracamy do starego procesu"*. Brzmi defensywnie — jest emocjonalnie kluczowe. Zdejmuje presję, że "to musi zadziałać". Paradoksalnie, zmniejsza szansę wycofania.

---

<!-- template: standard -->
## 6.3 Co zrobić, gdy zespół mówi "nie ufam temu"

Zwykły błąd: dowody. *"Zobaczcie — 94% akceptacji, zero halucynacji, testowaliśmy 6 tygodni"*. To nie działa, bo nieufność nie jest racjonalna, jest emocjonalna.

Co działa zamiast tego: **możliwość ingerencji**. Dodajcie Państwo na tym etapie krok, w którym użytkownik może **odrzucić output i wrócić do starego procesu dla tej konkretnej sprawy**. Jeden klik, bez pytań. Pierwszy miesiąc ten klik będzie użyty 20% razy. W drugim 8%. W trzecim 2%. Po tym można go usunąć.

Opór zespołu to nie jest bug, którego trzeba się pozbyć — to jest sygnał, że chcą kontroli. Dacie im kontrolę → przestaną jej używać. Odmówicie → będą walczyć z pilotem aż do jego śmierci.

---

<!-- template: standard -->
## 6.4 Dokumentacja minimalna

Do końca tygodnia 10 musi powstać dokument "operational handbook" — około 4–8 stron A4, napisany przez właściciela procesu (nie przez developera). Struktura:

1. Co robi ten workflow (jedno zdanie).
2. Kiedy jest uruchamiany (zdarzenie / harmonogram).
3. Co robić, gdy się nie uruchomi (kontakt + plan B).
4. Jak wygląda "normalny" output (2–3 przykłady).
5. Jak zgłosić błąd (jeden kanał).
6. Kto jest właścicielem procesu (imię + kontakt).

Żadnej dokumentacji technicznej. Kod się zmieni — workflow operacyjny zostanie. To jest dokument dla **kolejnego właściciela procesu za rok**, nie dla developera.
