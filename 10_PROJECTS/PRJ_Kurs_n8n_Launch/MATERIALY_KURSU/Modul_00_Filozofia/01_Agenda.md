# Moduł 0: Filozofia Automatyzacji — Plan Nagrania

> **Status:** Draft v1.0 | **Łączny czas:** ~45 minut | **Format:** FREE lead magnet
> **Cel modułu:** Przekonać uczestnika że (1) automatyzacja procesów to nie magia, (2) n8n to najlepszy wybór dla firmy w Polsce, (3) Kacper wie co robi i warto zapłacić za resztę kursu.

---

## Przegląd struktury

| # | Segment | Czas | Główny cel |
|---|---------|------|------------|
| 0 | Intro + hook | 3 min | Złapać uwagę, zbudować zaufanie |
| 1 | Czym jest (i nie jest) automatyzacja | 8 min | Obalić mity, ustawić oczekiwania |
| 2 | Dlaczego n8n, a nie Zapier/Make | 10 min | Uzasadnić wybór narzędzia, RODO |
| 3 | Myślenie procesami | 8 min | Nauczyć frameworku trigger→akcja→warunek |
| 4 | Setup środowiska | 8 min | Docker vs Cloud — kiedy co |
| 5 | Pierwsze 15 minut w interfejsie | 6 min | Oswoić interfejs, zredukować lęk |
| 6 | Outro + CTA | 2 min | Sprzedać resztę kursu |
| | **RAZEM** | **~45 min** | |

---

## Segment 0 — Intro i hook (3 minuty)

**Cel:** Zatrzymać uczestnika, zanim zdąży kliknąć "następny film".

**Co pokazujesz:**
- Slajd tytułowy z licznikiem: "Zaoszczędziłem 4 godziny tygodniowo tym jednym workflow"
- Krótki screen recording: workflow n8n działający — coś przychodzi, coś się dzieje, email wyjeżdża

**Timing szczegółowy:**
- 0:00–0:30 — Hook: konkretna liczba, konkretny problem
- 0:30–1:30 — Kim jesteś, dlaczego warto Cię słuchać (bez przesady, 60 sekund max)
- 1:30–3:00 — Co się wydarzy w tym module i co uczestnik wyniesie

**Notatki dla prowadzącego:**
Nie mów "zapraszam do oglądania". Zacznij od problemu. Idealny opener: stoisz przed ekranem i mówisz "Wyobraź sobie, że ktoś wypełnia formularz na Twojej stronie i zanim zdążysz otworzyć skrzynkę, on już dostał powitalny email, jego dane trafiły do CRM i Ty masz powiadomienie na telefonie. Tyle zajęło mi to na ustawieniu: 20 minut."

---

## Segment 1 — Czym jest (i NIE jest) automatyzacja (8 minut)

**Cel:** Wyrównać poziom wiedzy uczestników, obalić 3 największe mity.

**Co pokazujesz:**
- Slajdy z definicją i mitami
- Diagram: ręczny proces vs zautomatyzowany (przed/po)
- Przykłady z życia agencji/firmy (konkretne, nie abstrakcyjne)

**Timing szczegółowy:**
- 0:00–1:30 — Definicja robocza: "automatyzacja = software robi za Ciebie to, co robisz ręcznie i co można opisać krok po kroku"
- 1:30–4:00 — 3 mity do obalenia:
  - MIT #1: "To tylko dla developerów" (fałsz, n8n ma nody no-code)
  - MIT #2: "AI zastąpi automatyzację" (fałsz, AI to składnik, nie zamiennik)
  - MIT #3: "To zajmuje miesiące" (fałsz, pierwsze workflow w 20 minut)
- 4:00–6:00 — Przykłady: co można automatyzować w typowej polskiej firmie/agencji
- 6:00–8:00 — Czego NIE automatyzować (decyzje strategiczne, relacje, twórcze elementy)

**Notatki dla prowadzącego:**
W przykładach używaj polskich realiów: faktury w Wiadomości, leady z formularzy Webflow, powiadomienia na WhatsApp Business. Unikaj przykładów z Salesforce czy HubSpot — większość firm tu używa prostszych narzędzi.

---

## Segment 2 — Dlaczego n8n, a nie Zapier/Make (10 minut)

**Cel:** Uzasadnić wybór narzędzia. To jest najważniejszy segment dla decyzji zakupowej uczestnika.

**Co pokazujesz:**
- Tabela porównawcza: n8n vs Zapier vs Make (ceny, limity, RODO, vendor lock-in)
- Kalkulator kosztów: realna firma, 10 000 operacji miesięcznie — ile płaci za każde narzędzie
- Slajd: "Co się dzieje z Twoimi danymi w Zapier/Make"
- Slajd: n8n self-hosted = dane zostają u Ciebie

**Timing szczegółowy:**
- 0:00–3:00 — Porównanie cenowe. Twarde liczby.
- 3:00–6:00 — Kwestia danych i RODO: gdzie lądują dane Twoich klientów przy Zapier vs n8n self-hosted
- 6:00–8:00 — Vendor lock-in: co się dzieje gdy Zapier zmienia cennik (historia z 2022 r.)
- 8:00–10:00 — Kiedy n8n Cloud ma sens vs self-hosted. Uczciwa ocena.

**Notatki dla prowadzącego:**
Mów wprost: "Używam n8n od X lat i wiem, gdzie boli." Jeśli jest coś, w czym Zapier jest lepszy (onboarding, ekosystem integracji) — powiedz to. Uczciwa analiza buduje zaufanie bardziej niż jednostronna pochwała.

---

## Segment 3 — Jak myśleć procesami (8 minut)

**Cel:** Nauczyć uczestnika frameworku, który stosuje się do każdego workflow. To wiedza na całe życie.

**Co pokazujesz:**
- Diagram: trigger → akcja → warunek (ASCII na slajdzie, potem żywy przykład w n8n)
- 3 przykłady z codziennego życia biznesowego rozłożone na trigger/akcja/warunek
- Ćwiczenie na żywo: uczestnik ma 2 minuty żeby rozłożyć swój własny proces

**Timing szczegółowy:**
- 0:00–2:00 — Framework: Trigger (co go uruchamia?), Akcja (co robi?), Warunek (kiedy robi inaczej?)
- 2:00–5:00 — Przykład 1: formularz kontaktowy → zapis do CRM + email → jeśli budżet > 10k, powiadom Kacpra
- 5:00–6:30 — Przykład 2: nowa faktura w systemie → sprawdź status płatności → jeśli przeterminowana, wyślij reminder
- 6:30–8:00 — Zadanie dla uczestnika: "Zatrzymaj film, weź kartkę, rozpisz jeden swój ręczny proces na trigger/akcja/warunek"

**Notatki dla prowadzącego:**
Ten segment to mięso intelektualne modułu. Nie spiesz się. Diagram powinien być prosty — trzy słowa, strzałki. Potem pokaż jak ten diagram staje się dosłownie canvas w n8n (node = krok, strzałka = połączenie).

---

## Segment 4 — Setup środowiska (8 minut)

**Cel:** Uczestnik wie jak uruchomić n8n w 5 minut i rozumie kiedy wybrać Docker vs Cloud.

**Co pokazujesz:**
- Terminal: jedna komenda Docker i n8n działa lokalnie
- Porównanie: Docker lokalnie vs n8n Cloud vs self-hosted VPS
- Decision tree: kiedy co wybrać
- Screen recording: pierwsze logowanie, interfejs

**Timing szczegółowy:**
- 0:00–1:30 — Decision tree: Testujesz → Docker lokalnie. Klient produkcja, nie masz DevOps → n8n Cloud. Masz VPS i znasz Docker → self-hosted.
- 1:30–4:30 — Docker lokalnie: jedna komenda, port 5678, pierwsze logowanie (screen recording)
- 4:30–6:30 — n8n Cloud: rejestracja, darmowy trial, czym się różni interfejsowo
- 6:30–8:00 — Uwaga na temat bezpieczeństwa: nie wystawiaj n8n bez hasła na publiczne IP

**Notatki dla prowadzącego:**
Pokaż terminal naprawdę. Nie udawaj. Jeśli coś zajmuje 30 sekund na pobranie obrazu Docker — powiedz "teraz czekamy chwilę" i przyspiesz nagranie. Autentyczność > perfekcja.

---

## Segment 5 — Pierwsze 15 minut w interfejsie (6 minut)

**Cel:** Zredukować "page fright" przed pustym canvas. Uczestnik wie gdzie kliknąć.

**Co pokazujesz:**
- Screen recording: tworzysz workflow webhook → parsowanie JSON → Gmail od zera
- Komentarz na żywo: "To jest canvas, tu dodajesz nody, tu je łączysz"
- Pierwsze uruchomienie: curl webhook, zobaczenie danych w executions

**Timing szczegółowy:**
- 0:00–1:00 — Orientacja: lewa kolumna (workflows), środek (canvas), prawy panel (node config)
- 1:00–3:30 — Tworzysz workflow krok po kroku (szybki przegląd — pełne ćwiczenie jest w materiałach)
- 3:30–5:30 — Pierwsze wykonanie: dane wchodzą, email wychodzi
- 5:30–6:00 — "Właśnie stworzyłeś swój pierwszy workflow. To był Twój pierwszy krok."

**Notatki dla prowadzącego:**
Nie wchodź w szczegóły konfiguracji każdego noda — to jest w Ćwiczeniu 04. Tu chodzi o poczucie "o, to nie jest takie straszne." Klip powinien być dynamiczny, bez przerw.

---

## Segment 6 — Outro i CTA (2 minuty)

**Cel:** Sprzedać resztę kursu bez bycia nachalnym.

**Co pokazujesz:**
- Slajd: co jest w pełnym kursie (moduły 1-7 + bonusy)
- Slajd: dla kogo jest kurs (agencja, firma, freelancer)
- Link do zapisów

**Timing szczegółowy:**
- 0:00–1:00 — Podsumowanie: "Wiesz już X, Y, Z. To był 1% kursu."
- 1:00–2:00 — "W pełnym kursie budujesz [lista 3 konkretnych rzeczy]. Jeśli Ci się spodobało — link poniżej."

**Notatki dla prowadzącego:**
Nie mów "Kup teraz!". Mów "Jeśli to było wartościowe, reszta kursu idzie 10x głębiej." Pozwól materiałowi sprzedać siebie.

---

## Checklisty do nagrania

### Przed nagraniem
- [ ] n8n uruchomiony lokalnie (Docker) lub Cloud
- [ ] Konto Gmail połączone z n8n (OAuth2 skonfigurowany)
- [ ] Workflow "Hello Automation" zaimportowany i przetestowany
- [ ] Slajdy otwarte w trybie prezentacji
- [ ] Terminal z komendą Docker gotowy (nie wpisany jeszcze)
- [ ] Mikrofon przetestowany, tło czyste

### Po nagraniu
- [ ] Skrócić intro do max 3 minut w edycji
- [ ] Dodać callout graficzny przy tabeli porównawczej (segment 2)
- [ ] Timestamps do opisu YouTube/platformy kursowej
- [ ] Plik z ćwiczeniami (04_Cwiczenia.md) podlinkowany pod filmem
