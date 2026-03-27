---
type: course-material
modul: BONUS_B
status: ready
owner: kacper
last_reviewed: 2026-03-27
tags: [kurs, n8n, sprzedaz, cwiczenia, wycena, discovery-call, propozycja-handlowa]
---

# Moduł BONUS B — Ćwiczenia praktyczne

> **Format:** Ćwiczenia grupowe (2–3 osoby) + samodzielna wycena
> **Wymagania wstępne:** Obejrzany materiał wideo + prezentacja z Modułu BONUS B
> **Łączny czas:** ~75 minut (ćwiczenia) + zadanie domowe

---

## ĆWICZENIE 1 — WYCENA PROJEKTÓW AUTOMATYZACJI (20 minut)

### Cel
Nauczyć się szacować zakres i cenę projektu automatyzacji na podstawie briefu klienta — zanim przeprowadzisz discovery call. To umiejętność, która odróżnia doświadczonego implementera od juniora: senior potrafi zrobić przybliżoną wycenę z opisu problemu i zweryfikować ją na rozmowie.

### Jak korzystać z szablonu wyceny

Dla każdego projektu wypełnij poniższy szablon, a następnie zsumuj. Stawka godzinowa do ćwiczenia: **250 PLN/h netto** (dostosuj do własnej stawki po kursie).

```
SZABLON WYCENY — PROJEKT: ___________________________

FAZA 1 — Discovery & Design
  Analiza wymagań + wywiad z klientem:    ___h × 250 = _____ PLN
  Projekt architektury workflow:          ___h × 250 = _____ PLN

FAZA 2 — Implementacja
  Budowa głównego workflow:               ___h × 250 = _____ PLN
  Integracje zewnętrzne (per API):        ___h × 250 = _____ PLN
  Error handling + testy:                 ___h × 250 = _____ PLN

FAZA 3 — Wdrożenie & Dokumentacja
  Konfiguracja środowiska produkcyjnego:  ___h × 250 = _____ PLN
  Dokumentacja + szkolenie klienta:       ___h × 250 = _____ PLN

BUFOR NA NIEPRZEWIDZIANE (15%):                        _____ PLN
─────────────────────────────────────────────────────
RAZEM NETTO:                                           _____ PLN

UZASADNIENIE (kluczowa część!):
Największe ryzyko cenowe w tym projekcie: ________________________
Czego nie wiem i co musiałbym doprecyzować na discovery call: ____
```

### Projekty do wyceny

**PROJEKT A — FAQ Bot (email)**

> Klient prowadzi sklep internetowy ze sprzętem sportowym. Otrzymuje ok. 80 emaili dziennie z pytaniami, z czego 60% to powtarzające się pytania (czas dostawy, zwroty, dostępność). Chce automatycznej odpowiedzi na najczęstsze pytania. Linia eskalacji do człowieka gdy bot nie jest pewny odpowiedzi. Integracja z Gmail. Baza FAQ w Google Docs.

Wypełnij szablon. Odpowiedz na pytanie: co budzi Twoje największe wątpliwości przy tej wycenie?

---

**PROJEKT B — Multi-Agent Lead Scoring + CRM**

> Firma B2B (software house, 30 osób) zbiera leady przez formularz na stronie i z LinkedIn. Chce automatycznej kwalifikacji: sprawdzenie firmy leada (Clearbit lub podobne), scoring BANT (budget, authority, need, timeline), automatyczne tagowanie w HubSpot i przypisanie do odpowiedniego handlowca. Gdy score > 70 — wysłanie spersonalizowanego emaila powitalnego przez GPT-4o. Integracje: HubSpot, LinkedIn Sales Navigator, Clearbit, Gmail.

Wypełnij szablon. Co jest tutaj "scope creep trap" — gdzie projekt może urosnąć nieoczekiwanie?

---

**PROJEKT C — RAG Knowledge Base (1 000 dokumentów)**

> Firma prawnicza (15 prawników) chce wewnętrznego chatbota do przeszukiwania 1 000+ dokumentów: umów, orzeczeń, wewnętrznych procedur. Format: PDF, Word, niektóre skany (OCR wymagany). Interface: prosty chat w przeglądarce lub Teams. Wymagania bezpieczeństwa: dane nie mogą opuszczać UE, zero wysyłania dokumentów do OpenAI.

Wypełnij szablon. Jakie decyzje techniczne (model embedding, vector store, hosting) wpłyną na cenę i jak?

---

### Dyskusja grupowa (5 minut na koniec)

Po wypełnieniu szablonów — porównaj wyceny z osobą obok:
- Kto wycenił wyżej i dlaczego?
- Które założenia były inne?
- Gdzie jest największa rozbieżność i co ją powoduje?

Nie ma jednej poprawnej odpowiedzi. Chodzi o to żebyś potrafił **uzasadnić** każdą pozycję.

---

## ĆWICZENIE 2 — PROPOZYCJA HANDLOWA (30 minut)

### Cel
Napisać propozycję handlową dla fikcyjnego klienta korzystając ze struktury z kursu. Nacisk na część ROI i prezentację dwóch opcji cenowych — bo to decyduje czy klient powie "tak" czy "muszę to przemyśleć".

### Brief klienta — MANUFAKTURA GRZYBOWSKA SP. Z O.O.

> **Branża:** Produkcja artykułów spożywczych (przetwory, dżemy, grzyby suszone)
> **Wielkość:** 45 pracowników, obrót ~8M PLN rocznie
> **Osoba kontaktowa:** Karolina Wiśniewska, Dyrektor Operacyjna
> **Problem:** Zamówienia od hurtowników spływają przez email, WhatsApp i telefon. Ręczne przepisywanie do Excela, 2 osoby zajmują się tylko tym, błędy, opóźnienia. Fakturowanie ręczne w SubiektGT.
> **Cel:** Zautomatyzować przyjmowanie zamówień + wystawianie faktur. Budżet: "coś rozsądnego, nie chcemy milionowego ERP".
> **Gotowość:** Podpisana umowa NDA, gotowi na start w ciągu 2 tygodni.

### Struktura propozycji (użyj tej kolejności)

```
1. PROBLEM (1 paragraf)
   Nazwij ból klienta własnymi słowami — pokaż że rozumiesz ich sytuację.
   Nie pisz ogólnie "automatyzacja jest ważna". Pisz konkretnie.

2. NASZE PODEJŚCIE (2–3 zdania)
   Jak zamierzasz to rozwiązać? Na wysokim poziomie — bez żargonu technicznego.
   Klient musi to zrozumieć w 20 sekund.

3. ZAKRES — OPCJA A (Podstawowa)
   Lista 4–6 konkretnych deliverables.
   Przykład: "Workflow odbierający email z zamówieniem → parsowanie danych → zapis w arkuszu"
   NIE: "Implementacja systemu automatyzacji". TAK: "Bot emailowy obsługujący do 200 zamówień/miesiąc"

4. ZAKRES — OPCJA B (Rozszerzona)
   Opcja A + co jeszcze? Zwykle: dodatkowa integracja, rozszerzone raportowanie, szkolenie.

5. ROI — SZACOWANY ZWROT
   Konkretne liczby. Wypełnij poniższy mini-kalkulator:

   ┌─────────────────────────────────────────────────────────────┐
   │ OBECNY KOSZT PROCESU (miesięcznie)                          │
   │ Czas na ręczne przepisywanie:    ___ h × ___ PLN/h = ___ PLN│
   │ Koszt błędów (korekty faktur):   ___ PLN                    │
   │ Suma obecnego kosztu:            ___ PLN/miesiąc            │
   │                                                             │
   │ PO AUTOMATYZACJI                                            │
   │ Czas obsługi po wdrożeniu:       ___ h × ___ PLN/h = ___ PLN│
   │ Oszczędność miesięczna:          ___ PLN                    │
   │                                                             │
   │ ZWROT Z INWESTYCJI                                          │
   │ Cena projektu (Opcja A):         ___ PLN                    │
   │ Payback period:                  ___ miesięcy               │
   └─────────────────────────────────────────────────────────────┘

6. CENA
   Opcja A: ___ PLN netto (jednorazowo) + ___ PLN/miesiąc support
   Opcja B: ___ PLN netto (jednorazowo) + ___ PLN/miesiąc support

   Termin ważności oferty: 14 dni
   Płatność: 50% przed startem, 50% po odbiorze

7. NASTĘPNY KROK
   Jedno konkretne zdanie. Przykład:
   "Jeśli oferta jest OK — proszę o odpowiedź do piątku,
   wtedy zarezerwuję termin kick-off na przyszły wtorek."
```

### Zasady dobrej propozycji — lista kontrolna

Zanim oddasz do peer review, sprawdź:

- [ ] Problem opisany słowami klienta (nie Twoim żargonem)
- [ ] Opcja A vs B mają wyraźną różnicę wartości (nie tylko cenową)
- [ ] ROI wyliczone na konkretnych liczbach
- [ ] Żadne zdanie nie zaczyna się od "My" lub "Nasza firma"
- [ ] Propozycja ma max 2 strony A4 (lub odpowiednik w Markdown)
- [ ] Jest jeden wyraźny "następny krok"

### Peer Review (10 minut z pary)

Zamień propozycję z osobą obok. Oceniaj według skali 1–5 w każdym wymiarze:

| Wymiar | Ocena (1–5) | Komentarz |
|---|---|---|
| Czy problem jest dobrze zdefiniowany? | | |
| Czy zakres jest konkretny i mierzalny? | | |
| Czy ROI jest wiarygodne? | | |
| Czy dwie opcje są wyraźnie różne? | | |
| Czy chciałbyś/chciałabyś podpisać tę umowę? | | |

Najcenniejszy feedback: "To zdanie mnie zgubiło" + "Tego brakowało żebym powiedział/powiedziała tak".

---

## ĆWICZENIE 3 — MOCK DISCOVERY CALL (25 minut)

### Cel
Przeprowadzić 15-minutowy Discovery Call z partnerem i na koniec ocenić: czy masz wystarczająco dużo informacji żeby napisać propozycję? To ćwiczenie boli — i właśnie dlatego warto je zrobić na kursie, nie przy prawdziwym kliencie.

### Podział ról

**Osoba A — SPRZEDAWCA (prowadzi rozmowę)**
Twoim celem jest zebrać informacje niezbędne do wyceny. Masz 10 pytań z listy poniżej — ale nie musisz zadać wszystkich. Słuchaj, doprecyzowuj, nie przerywaj.

**Osoba B — KLIENT**
Grasz Prezesa/Dyrektora Operacyjnego firmy e-commerce:
- Firma: 50 pracowników, sklep z elektroniką, 500 zamówień dziennie
- Problem główny: obsługa zwrotów jest ręczna — 3 osoby przetwarzają zwroty przez 5h dziennie
- Dodatkowy kontekst (ujawnij tylko gdy zapytany): integracja z BaseLinker, magazyn w Poznaniu, używają Allegro i własnego sklepu Shopify
- Budżet: "nie mamy konkretnego budżetu, zależy co zaproponujesz" (klasyczny klient)
- Timeline: "chcielibyśmy to mieć przed wakacjami" (czerwiec)
- Blokada której nie ujawniaj sam/sama: dwa lata temu mieli złe doświadczenia z inną agencją IT która wdrożyła coś co nie działało

### Lista 10 pytań dla Sprzedawcy

Wybierz 6–8 spośród tych pytań — nie musisz zadać wszystkich, nie w tej kolejności:

1. "Proszę opisać jak wygląda teraz proces zwrotu — od momentu gdy klient klika 'chcę zwrócić' do momentu gdy pieniądze wracają na jego konto. Każdy krok."
2. "Ile zgłoszeń zwrotów macie tygodniowo? W jakich kanałach — email, formularz, telefon?"
3. "Które systemy są zaangażowane w ten proces dziś? (magazyn, sklep, BookKeeping, kurier?)"
4. "Co jest największym bólem w obecnym procesie — co powoduje najwięcej błędów lub opóźnień?"
5. "Czy próbowaliście to wcześniej automatyzować lub usprawniać? Co się stało?"
6. "Kto w firmie używa tego procesu — tylko Wasz zespół, czy klienci też mają jakiś panel?"
7. "Co byłoby dla Was miarą sukcesu — po czym poznamy że wdrożenie się powiodło?"
8. "Jaki macie horyzont czasowy? Czy jest jakiś termin który jest 'must have'?"
9. "Kto po Waszej stronie podejmuje decyzję o zakupie tego projektu?"
10. "Czy macie już wyobrażenie budżetu, czy chcecie najpierw usłyszeć co jest możliwe?"

### Przebieg ćwiczenia

```
Minuty 0–2:    Sprzedawca otwiera rozmowę (small talk, agenda)
Minuty 2–13:   Discovery — pytania i odpowiedzi
Minuty 13–15:  Sprzedawca podsumowuje: "Rozumiem że macie X, Y, Z. Czy dobrze?"
               + ustala następny krok
Minuty 15–20:  Debrief (oboje razem)
Minuty 20–25:  Zamiana ról (opcjonalnie — jeśli starczy czasu)
```

### Debrief — pytania po rozmowie

**Dla Sprzedawcy:**

| Pytanie | Twoja odpowiedź |
|---|---|
| Czy wiesz na czym polega problem technicznie? | TAK / NIE / CZĘŚCIOWO |
| Czy wiesz jakie systemy trzeba zintegrować? | TAK / NIE / CZĘŚCIOWO |
| Czy wiesz jaki jest budżet (choć orientacyjnie)? | TAK / NIE / CZĘŚCIOWO |
| Czy wiesz kto decyduje o zakupie? | TAK / NIE / CZĘŚCIOWO |
| Czy wiesz jaki jest deadline? | TAK / NIE / CZĘŚCIOWO |
| Czy odkryłeś/odkryłaś blokadę (złe doświadczenia)? | TAK / NIE |
| **Czy mógłbyś/mogłabyś napisać ofertę na podstawie tej rozmowy?** | TAK / NIE / POTRZEBUJĘ WIĘCEJ |

**Dla Klienta (feedback dla Sprzedawcy):**

- Które pytanie było najlepsze i dlaczego?
- Które pytanie Cię zaskoczyło lub poczułeś/poczułaś się niepotrzebnie przesłuchiwany/a?
- Czy Sprzedawca odkrył historię złego wdrożenia — i jeśli tak, to jak?
- Czy na koniec wiedziałeś/wiedziałaś co jest następnym krokiem?

### Co zrobić z "nie wiem żeby napisać ofertę"

Jeśli po rozmowie masz za mało danych — to normalne przy pierwszym Discovery Call. Plan na przyszłość:

```
Brakuje mi informacji o: ________________________________
Jak to zdobędę przed napisaniem oferty:
  □ Wyślę email z 2–3 pytaniami uzupełniającymi
  □ Umówię follow-up call (max 20 min, konkretna agenda)
  □ Poproszę o dostęp demo do systemu/demo API
  □ Poproszę o próbkę danych (anonimizowaną)
```

Pamiętaj: lepiej opóźnić ofertę o 2 dni i napisać ją dobrze, niż wysłać ją w ciągu godziny i przepraszać za złą wycenę przez 3 miesiące.

---

## ZADANIE DOMOWE — PRAWDZIWA PROPOZYCJA

### Cel
Napisać propozycję dla prawdziwego potencjalnego klienta, potencjalnego projektu który masz w głowie, lub "fikcyjnego klienta z Twojej branży" jeśli nie masz jeszcze żadnego leada.

### Wymagania

1. Użyj struktury z Ćwiczenia 2 (wszystkie 7 punktów)
2. ROI musi być wyliczone na liczbach — nie "oszczędzisz czas" ale "oszczędzisz 14h/miesiąc × 80 PLN/h = 1 120 PLN/miesiąc"
3. Dwie opcje cenowe (Podstawowa / Rozszerzona)
4. Maksymalnie 2 strony A4

### Opcjonalnie — prześlij na forum kursu

Jeśli chcesz feedback od Kacpra lub Aliny — prześlij propozycję (możesz zanonimizować nazwę klienta) na forum. Komentujemy wszystkie w ciągu tygodnia.

---

## MATERIAŁY DODATKOWE

- `05_Szablony_Handlowe.md` — gotowe szablony: propozycja, follow-up email, umowa NDA
- `30_RESOURCES/RES_Sales_Playbook/Sales_Playbook.md` — ICP Dokodu, cennik, lista obiekcji
- Kalkulator wyceny projektów automatyzacji (Google Sheets): link w zasobach kursu
- Rekomendowana lektura: "Fanatical Prospecting" (Jeb Blount) — rozdział o Discovery Calls
