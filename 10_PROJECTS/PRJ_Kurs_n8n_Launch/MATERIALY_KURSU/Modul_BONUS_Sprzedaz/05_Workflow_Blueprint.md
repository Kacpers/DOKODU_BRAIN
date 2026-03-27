---
type: course-material
modul: BONUS_B
status: ready
owner: kacper
last_reviewed: 2026-03-27
tags: [kurs, n8n, sprzedaz, wycena, discovery-call, retainer, handover, szablony-biznesowe]
---

# Moduł BONUS B — Szablony Biznesowe: Sprzedaż i Delivery Projektów Automatyzacji

> **Cel:** Gotowe do użycia szablony, kalkulatory i checklisty — skopiuj, uzupełnij, wyślij.
> **Zawiera:** Szablon wyceny, 10 pytań Discovery Call, checklist handover, kalkulator retainera.
> **Uwaga:** Ten moduł nie zawiera workflow n8n — to materiały biznesowe, nie techniczne.

---

## SZABLON 1 — WYCENA PROJEKTU AUTOMATYZACJI

> Kopiuj tabelę do Notion / Google Docs / emaila. Uzupełnij godziny i stawkę, resztę liczy się sama.

### Instrukcja użycia

1. Wypełnij kolumny "Godziny est." dla każdego zakresu
2. Wpisz stawkę godzinową (rekomendowana: 200–350 PLN/h)
3. Dodaj 30% bufor na niespodzianki (zawsze)
4. Opcjonalnie: podnieś o 20–40% jeśli klient nie zna swoich procesów (ryzyko scope creep)

### Tabela wyceny — szablon standardowy

| # | Faza / Task | Godziny est. | Stawka (PLN/h) | Wartość (PLN) | Uwagi |
|---|-------------|:------------:|:--------------:|:-------------:|-------|
| **1** | **Discovery i analiza procesów** | | | | |
| 1.1 | Warsztaty mapowania procesu (online) | 3h | 350 | 1 050 | 2×1,5h z klientem |
| 1.2 | Dokumentacja AS-IS i TO-BE | 2h | 350 | 700 | |
| 1.3 | Specyfikacja techniczna + akceptacja | 2h | 350 | 700 | Klient akceptuje przed budową |
| **2** | **Projektowanie workflow** | | | | |
| 2.1 | Diagram workflow (Miro/Draw.io) | 1h | 300 | 300 | |
| 2.2 | Dobór integracji i API | 1h | 300 | 300 | Research dostępnych connectorów |
| 2.3 | Architektura błędów i wyjątków | 1h | 300 | 300 | Error handling plan |
| **3** | **Budowa** | | | | |
| 3.1 | Konfiguracja triggerów i webhooków | 2h | 250 | 500 | |
| 3.2 | Integracje zewnętrzne (API/webhook) | 4h | 250 | 1 000 | Per integracja; estymuj osobno |
| 3.3 | Logika warunkowa (Switch/IF) | 2h | 250 | 500 | |
| 3.4 | Transformacje danych (Code Nodes) | 3h | 250 | 750 | |
| 3.5 | Obsługa błędów i retry | 2h | 250 | 500 | Min. 30% czasu budowy |
| 3.6 | Audit log i monitoring | 1h | 250 | 250 | Zawsze — nie skracaj |
| **4** | **Testy** | | | | |
| 4.1 | Testy jednostkowe węzłów | 2h | 250 | 500 | Każdy node z danymi testowymi |
| 4.2 | Testy integracyjne end-to-end | 2h | 250 | 500 | Real data, sandbox environment |
| 4.3 | UAT z klientem (User Acceptance Test) | 3h | 250 | 750 | Klient testuje, Ty asystujesz |
| **5** | **Dokumentacja** | | | | |
| 5.1 | Dokumentacja techniczna (Markdown/Notion) | 2h | 200 | 400 | Opis węzłów, zmiennych, logiki |
| 5.2 | Instrukcja obsługi dla użytkownika | 1h | 200 | 200 | "Co zrobić gdy..." |
| 5.3 | Video walkthrough (opcjonalne) | 1h | 200 | 200 | Nagraj Loom przez workflow |
| **6** | **Wdrożenie i handover** | | | | |
| 6.1 | Deployment na środowisko produkcyjne | 1h | 300 | 300 | |
| 6.2 | Szkolenie użytkownika końcowego | 2h | 300 | 600 | Online, nagrywane |
| 6.3 | Protokół odbioru i podpis | 0.5h | 300 | 150 | |
| | | | | | |
| | **SUMA BAZOWA** | **36.5h** | | **10 450 PLN** | |
| | **Bufor 30% (niespodzianki)** | +11h | | +3 135 PLN | Zawsze dodawaj |
| | **SUMA Z BUFOREM** | **47.5h** | | **13 585 PLN** | |
| | **Zaokrąglenie / cena finalna** | | | **14 000 PLN** | Okrągłe liczby lepiej wyglądają |

### Warianty wyceny według złożoności projektu

| Typ projektu | Przykład | Zakres godzin | Widełki ceny (PLN) |
|---|---|:---:|:---:|
| Prosty workflow | Powiadomienia email/Slack, sync danych między 2 systemami | 15–25h | 5 000–10 000 |
| Średni workflow | Multi-step z logiką warunkową, 3–5 integracji | 30–50h | 12 000–20 000 |
| Złożony system | Agent AI z pamięcią, RAG, approval flow | 60–100h | 25 000–45 000 |
| Enterprise | Wiele workflowów, integracje ERP/CRM, dokumentacja enterprise | 100–200h | 45 000–90 000 |

> **Zasada Kacpra:** Jeśli szacujesz mniej niż 20h — sprawdź dwa razy. Prawie zawsze jest więcej. Jeśli klient mówi "to tylko mała automatyzacja" — podwój estymację.

---

## SZABLON 2 — 10 PYTAŃ DISCOVERY CALL

> Cel discovery call: zrozumieć **problem biznesowy**, nie zbierać wymagania techniczne.
> Czas: 45–60 minut. Zadawaj pytania w tej kolejności — logika prowadzi klienta od ogółu do szczegółu.

---

### Pytanie 1: Jaki konkretny proces chcesz zautomatyzować?

**Jak zadać:** "Zanim przejdziemy do technologii — opiszcie mi ten proces krok po kroku, tak jak robicie to dzisiaj."

**DLACZEGO:** Klienci często mówią "chcemy automatyzację sprzedaży" nie wiedząc co to znaczy. To pytanie wyciąga konkret. Słuchaj czy mówią o kroKach (to dobry znak) czy o efektach ("żeby było szybciej" — to za mało).

**Sygnały alarmowe:** Jeśli klient nie potrafi opisać procesu krok po kroku — projekt nie jest gotowy. Zaproponuj najpierw warsztaty mapowania procesów (płatne).

---

### Pytanie 2: Ile razy dziennie/tygodniowo ten proces się powtarza?

**Jak zadać:** "Żeby zrozumieć skalę — jak często ten proces jest wykonywany? Przez kogo i ile to trwa za każdym razem?"

**DLACZEGO:** To podstawa kalkulacji ROI. Bez tej liczby nie możesz pokazać wartości. Wzór: `(czas na wykonanie × liczba powtórzeń × stawka godzinowa pracownika) × 12 miesięcy = roczna oszczędność`. Jeśli automatyzacja za 20 000 PLN zwraca się w 3 miesiące — to oczywista decyzja.

**Przykład:** 30 min/dzień × 250 dni roboczych × 80 PLN/h = 10 000 PLN/rok oszczędności tylko na czasie.

---

### Pytanie 3: Co się dzieje gdy ten proces zawodzi lub jest opóźniony?

**Jak zadać:** "Co się zdarzyło ostatnio gdy coś poszło nie tak? Jaki był koszt tej sytuacji dla firmy?"

**DLACZEGO:** Ból jest lepszym motywatorem niż zysk. Jeśli klient może przywołać konkretną historię o stracie (klient odszedł, faktura spóźniona, błąd w danych) — automatyzacja przestaje być "nice to have" i staje się "must have". Zapamiętaj tę historię — użyjesz jej w ofercie.

---

### Pytanie 4: Jakie systemy są zaangażowane w ten proces?

**Jak zadać:** "Jakich narzędzi używacie na każdym kroku? CRM, ERP, arkusze, email, komunikatory — wymieńcie wszystko."

**DLACZEGO:** To jest Twoja mapa techniczna. Każdy system to potencjalna integracja — sprawdź czy ma API, webhooks, n8n connector. Systemy legacy bez API (stare ERP, lokalne bazy Access) = czerwona flaga i wzrost ceny o 50–100%.

**Lista do sprawdzenia:** CRM (HubSpot/Salesforce/Pipedrive?), ERP (SAP/Comarch/Enova?), email (Gmail/Outlook?), komunikatory (Slack/Teams?), arkusze (Google Sheets/Excel?), własne systemy.

---

### Pytanie 5: Kto jest właścicielem tego procesu i kto go wykonuje?

**Jak zadać:** "Kto decyduje jak ten proces wygląda? A kto fizycznie go wykonuje na co dzień? To ta sama osoba?"

**DLACZEGO:** To pytanie o władzę i sabotaż. Jeśli właściciel procesu (manager) zleca automatyzację bez wiedzy wykonawców (pracownicy) — projekt może być bojkotowany. "Zmiana procesu to zmiana pracy" — ludzie się boją. Zidentyfikuj ambasadora projektu w zespole od razu.

---

### Pytanie 6: Jaki jest Wasz budżet na ten projekt?

**Jak zadać:** "Żebyśmy mogli zaproponować rozwiązanie które faktycznie pasuje do Waszych możliwości — jaki budżet macie zarezerwowany? Mamy projekty od 8 000 do 80 000 PLN."

**DLACZEGO:** Bez wiedzy o budżecie strzasz w ciemno. Podaj widełki (nie pytaj "ile możecie zapłacić" — to amatorskie). Jeśli budżet jest 5 000 PLN a projekt wymaga 30 000 PLN — lepiej wiedzieć teraz niż po tygodniu pracy nad ofertą.

**Technika:** Jeśli klient odmawia podania budżetu, spytaj: "Czy mówimy raczej o dziesiątkach tysięcy złotych czy setkach tysięcy?" — to łatwiej powiedzieć.

---

### Pytanie 7: Kiedy potrzebujecie tego działającego?

**Jak zadać:** "Czy jest jakiś konkretny deadline albo wydarzenie do którego to musi działać? Co się stanie jeśli nie będzie gotowe na czas?"

**DLACZEGO:** Timeline ujawnia prawdziwą pilność. "Do końca kwartału" z presją zarządu = kupuje szybko. "Kiedyś w tym roku" = długi cykl decyzyjny, duże ryzyko że projekt padnie. Deadline zewnętrzny (audyt, zmiana prawa, launcha produktu) = najsilniejsza motywacja.

**Uwaga:** Jeśli klient chce wszystko "na wczoraj" bez konkretnego powodu — to znak nieplanowania. Zastrzeż sobie prawo do premium za ekspresowe wykonanie.

---

### Pytanie 8: Czy próbowaliście to już automatyzować wcześniej? Co się stało?

**Jak zadać:** "Mam wrażenie że to nie jest pierwsza próba rozwiązania tego problemu. Czy coś wcześniej próbowaliście? Co nie zadziałało?"

**DLACZEGO:** To jedno z najważniejszych pytań. Wcześniejsze niepowodzenie mówi Ci: (1) co technicznie nie zadziałało, (2) kto był wtedy winny w oczach klienta (zewnętrzny dostawca czy własny zespół?), (3) jakie są ukryte lęki klienta. Jeśli poprzedni wykonawca zawiedli — klient będzie bardziej wymagający wobec Ciebie. Wbuduj to w umowę.

---

### Pytanie 9: Kto po stronie klienta będzie zarządzał tym systemem na co dzień?

**Jak zadać:** "Kiedy wdrożymy automatyzację i wyjdziemy — kto będzie Waszym wewnętrznym ekspertem od tego systemu? Czy ta osoba ma doświadczenie techniczne?"

**DLACZEGO:** To pytanie o długoterminowe ryzyko projektu i sprzedaż retainera. Jeśli nikt nie ma kompetencji technicznych — system jest kruchy. Zaproponuj szkolenie (płatne) i retainer (miesięczne wsparcie). Jeśli jest techniczna osoba wewnątrz — zaangażuj ją w projekt od początku, zredukujesz opór i ryzyko.

---

### Pytanie 10: Jak będziecie mierzyć sukces tego projektu za 6 miesięcy?

**Jak zadać:** "Wyobraźmy sobie że mamy spotkanie za 6 miesięcy. Po czym poznacie że projekt był sukcesem? Co się będzie działo inaczej niż teraz?"

**DLACZEGO:** To zamknięcie discovery. Po pierwsze — wymusza konkretne KPI (czas oszczędzony, liczba błędów, koszt operacyjny). Po drugie — staje się Twoim kryterium akceptacji w umowie. Po trzecie — jeśli klient nie potrafi odpowiedzieć, projekt nie ma zdefiniowanego celu. Doprecyzujcie razem przed podpisaniem umowy.

**Przykładowe KPI:** "Czas przetwarzania zamówienia z 2h do 15 minut", "Zero ręcznych transferów danych między systemem A i B", "Raport sprzedażowy gotowy co poniedziałek o 8:00 bez pracy człowieka".

---

### Podsumowanie Discovery Call — szablon notatki

```
Data: ___________
Klient: ___________
Uczestnicy: ___________

PROCES DO AUTOMATYZACJI:
- Opis procesu krok po kroku:
- Częstotliwość: ___ razy/dzień/tydzień
- Czas wykonania obecnie: ___ minut/godzin
- Wykonawca procesu: ___________

SYSTEMY ZAANGAŻOWANE:
□ CRM: ___________
□ ERP: ___________
□ Email: ___________
□ Inne: ___________

BIZNES:
- Koszt niedziałającego procesu: ___________
- Budżet klienta: ___________
- Deadline: ___________
- Próby wcześniejsze: ___________

KRYTERIA SUKCESU (za 6 miesięcy):
1. ___________
2. ___________

WŁAŚCICIEL PROCESU: ___________
TECHNICZNA OSOBA KLIENTA: ___________

RED FLAGS:
□ Brak opisu procesu krok po kroku
□ Brak budżetu / "zobaczymy"
□ Brak technicznych zasobów po stronie klienta
□ "To proste, tylko kilka dni pracy"
□ Wcześniejsze nieudane wdrożenia bez wyciągniętych wniosków
□ Decyzję podejmuje ktoś nieobecny na rozmowie
□ Timeline "na wczoraj" bez konkretnego powodu

NEXT STEP: ___________ (data + akcja)
```

---

## SZABLON 3 — CHECKLIST HANDOVER PROJEKTU

> Co dostarczasz klientowi na zakończenie projektu. Każda pozycja musi być potwierdzona przed podpisaniem protokołu odbioru.

### Deliverables techniczne

- [ ] **Eksport workflow n8n (JSON)** — plik z pełnym workflow gotowy do importu
  - Ścieżka w repozytorium/Notion: ___________
  - Wersja n8n na której testowano: ___________

- [ ] **Zmienne środowiskowe** — lista wszystkich wymaganych zmiennych `.env` z opisem (bez wartości!)
  - Klient otrzymuje: nazwy zmiennych, co zawierają, gdzie je ustawić
  - Klient NIE otrzymuje: wartości sekretów (ustawia sam po wdrożeniu)

- [ ] **Diagram workflow** (Miro / Draw.io / PNG)
  - Każdy węzeł opisany: co robi, jakie dane przyjmuje, jakie zwraca
  - Ścieżki błędów zaznaczone

- [ ] **Instrukcja instalacji** (krok po kroku)
  - [ ] Wymagania systemowe (Docker, Node, RAM, dysk)
  - [ ] Krok 1: Import workflow
  - [ ] Krok 2: Ustawienie zmiennych środowiskowych
  - [ ] Krok 3: Konfiguracja kredencjałów w n8n
  - [ ] Krok 4: Test end-to-end
  - [ ] Krok 5: Aktywacja workflow produkcyjnego

### Dokumentacja techniczna

- [ ] **Dokumentacja node-by-node** — opis każdego ważnego węzła
  - Dla każdego Code Node: co robi kod, jakie parametry, przykład wejścia/wyjścia
  - Dla każdej integracji zewnętrznej: API endpoint, metoda, wymagane uprawnienia

- [ ] **Obsługa błędów i troubleshooting**
  - Lista typowych błędów (Top 5) z krokami naprawy
  - Jak sprawdzić execution log w n8n
  - Kiedy i jak eskalować do Dokodu (jeśli jest retainer)

- [ ] **Audit log** — opis co jest logowane i gdzie (Google Sheets / zewnętrzna baza)

### Dokumentacja użytkownika

- [ ] **Instrukcja obsługi** (dla osoby nie-technicznej)
  - Jak uruchomić workflow ręcznie (jeśli potrzebne)
  - Jak sprawdzić czy workflow działa
  - Co zrobić gdy "coś nie działa" — prosty decision tree

- [ ] **Video walkthrough** (Loom, max 15 minut)
  - [ ] Przegląd całego workflow w n8n
  - [ ] Demo działania z prawdziwymi danymi
  - [ ] Najczęstsze scenariusze użycia
  - Link do nagrania: ___________

### Szkolenie

- [ ] **Szkolenie użytkownika końcowego** — ___h online (nagrywane)
  - Data szkolenia: ___________
  - Uczestnicy: ___________
  - Nagranie dostępne dla klienta: tak / nie

- [ ] **Szkolenie administratora systemu** (opcjonalne, jeśli jest techniczna osoba)
  - Co obejmuje: konfiguracja, monitoring, drobne modyfikacje
  - Data: ___________

### Protokół odbioru

- [ ] **Test end-to-end przeprowadzony wspólnie z klientem**
  - Scenariusz 1 (happy path): PASS / FAIL
  - Scenariusz 2 (błędne dane): PASS / FAIL
  - Scenariusz 3 (integracja zewnętrzna niedostępna): PASS / FAIL

- [ ] **Protokół odbioru podpisany** przez obie strony
  - Zawiera: listę deliverables, wyniki testów, datę odbioru, podpisy
  - Podpisanie = zamknięcie projektu, uruchomienie ostatniej płatności

- [ ] **Przekazanie dostępów** — zmiana wszystkich haseł i tokenów API
  - Klient przejął: credentials do n8n, klucze API, dostęp do Sheets/Notion z dokumentacją
  - Dokodu usunął: dostęp do produkcyjnych systemów klienta (zostaje dostęp serwisowy tylko jeśli jest retainer)

### Propozycja retainera (tuż przed podpisaniem protokołu!)

- [ ] **Propozycja retainera złożona przed podpisaniem protokołu odbioru**
  - Wartość miesięczna: ___________ PLN
  - Co zawiera: ___________
  - Klient odpowiedział: TAK / NIE / Zastanowię się (follow-up: ___________)

---

## SZABLON 4 — KALKULATOR RETAINERA

> Formuła: Retainer miesięczny = (Wartość projektu × współczynnik) / 12 miesięcy

### Formuła podstawowa

```
Retainer miesięczny = Wartość_projektu × R / 12

Gdzie R (współczynnik roczny) zależy od tieru:
- Tier A (Monitoring): R = 15% (min. 400 PLN/mies.)
- Tier B (Wsparcie aktywne): R = 20% (min. 700 PLN/mies.)
- Tier C (Rozwój): R = 30% (min. 1 200 PLN/mies.)
```

### Przykłady kalkulacji

| Wartość projektu | Tier A (15%) | Tier B (20%) | Tier C (30%) |
|:---:|:---:|:---:|:---:|
| 10 000 PLN | 125 PLN → **min. 400 PLN** | 167 PLN → **min. 700 PLN** | 250 PLN → **min. 1 200 PLN** |
| 20 000 PLN | 250 PLN → **min. 400 PLN** | 333 PLN → **min. 700 PLN** | 500 PLN → **min. 1 200 PLN** |
| 30 000 PLN | **375 PLN → min. 400 PLN** | **500 PLN → min. 700 PLN** | **750 PLN → min. 1 200 PLN** |
| 50 000 PLN | **625 PLN/mies.** | **833 PLN/mies.** | **1 250 PLN/mies.** |
| 80 000 PLN | **1 000 PLN/mies.** | **1 333 PLN/mies.** | **2 000 PLN/mies.** |

> **Uwaga:** Minimum zawsze obowiązuje. Projekt za 10 000 PLN na Tier A kosztuje 400 PLN/mies., nie 125 PLN — inaczej nie opłaca się Dokodu obsługiwać.

### Co wchodzi w każdy tier?

#### Tier A — Monitoring (15% rocznie)
- Monitoring dostępności workflow (alert gdy zatrzymany)
- Przegląd execution logów raz w miesiącu
- Powiadomienie o problemach do 24h (dni robocze)
- Aktualizacje środowiska (n8n, Docker) raz na kwartał
- **Nie wchodzi:** nowe funkcje, modyfikacje workflow, priorytetowy support

#### Tier B — Wsparcie Aktywne (20% rocznie)
- Wszystko z Tier A
- Czas reakcji do 4h w dni robocze
- 2h pracy miesięcznie wliczone (drobne poprawki, konfiguracje)
- Monthly review call (30 minut) — przegląd metryk workflow
- Priorytetowa obsługa zgłoszeń
- **Nie wchodzi:** nowe integracje, większe modyfikacje architektury

#### Tier C — Rozwój (30% rocznie)
- Wszystko z Tier B
- 8h pracy miesięcznie wliczone (nowe funkcje, integracje, optymalizacje)
- Quarterly business review (1h) — przegląd ROI automatyzacji
- Proaktywne rekomendacje nowych automatyzacji
- Priorytet w kolejce projektów nowych

### Skrypt sprzedaży retainera

> Moment: tuż przed podpisaniem protokołu odbioru (klient jest zadowolony, projekt działa)

"Mamy jeszcze jedną kwestię przed podpisaniem protokołu. Ten workflow będzie teraz pracował dla Was codziennie — integracje zewnętrzne się zmieniają, API aktualizują, n8n wydaje nowe wersje. Żebyście mieli gwarancję że to działa za rok tak samo jak dziś, przygotowałem propozycję serwisu.

Za [KWOTA] miesięcznie macie [CO ZAWIERA TIER]. To [PROCENT] miesięcznych kosztów projektu — a projekt oszczędza Wam [WYLICZONE ROI] miesięcznie. Podpisujemy razem z protokołem — jedna prosta umowa na 12 miesięcy."

---

### Obiekcje i odpowiedzi

| Obiekcja klienta | Odpowiedź |
|---|---|
| "To za drogo, sami to ogarniemy" | "Rozumiem. Pamiętajcie że gdy API Stripe zmieni autoryzację albo Google wycofa token, workflow stanie. Wtedy naprawa jest pilna i droższa. Mamy też opcję Tier A za X PLN — to tylko monitoring i alerty." |
| "Zadzwonimy gdy coś padnie" | "Oczywiście, to zawsze możliwe. Stawka reakcji poza retainerem to [STAWKA AWARYJNA] PLN/h z czasem reakcji do 48h. W retainerze to [CZAS REAKCJI] i 2h wliczone miesięcznie." |
| "Dajcie nam czas do przemyślenia" | "Oczywiście. Oferta retainera jest ważna 14 dni — potem muszę sprawdzić dostępność. Na kiedy mogę się spodziewać odpowiedzi?" |
| "A co jeśli nie będziemy potrzebować tych godzin?" | "Tier A to monitoring bez godzin — płacicie tylko za spokój że ktoś patrzy. Tier B i C — niezużyte godziny nie przechodzą na kolejny miesiąc, ale w praktyce zawsze się coś pojawia do ulepszenia." |
