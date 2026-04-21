---
n: "03"
title: "Tydzień 3–4: Wybór pierwszego use case'a"
abstract: "Matryca wartość × ryzyko. Dlaczego nie zaczynasz od kontaktu z klientem, tylko od procesu wewnętrznego."
reading_time: "16 min"
level: "Podstawowy"
sections: "3.1 – 3.4"
kicker: "Rozdział trzeci"
---

<!-- template: chapter -->
# Tydzień 3–4: Wybór pierwszego use case'a

**Abstrakt:** Mają Państwo arkusz z 80 pozycjami. Teraz musicie wybrać jedną. Od tej decyzji zależy, czy pilot wystartuje, czy ugrzęźnie w nieskończonych konsultacjach.

---

<!-- template: standard -->
## 3.1 Matryca wartość × ryzyko

Dokładamy do arkusza z rozdziału 2 dwie kolumny:

- **Wartość roczna (PLN)** = (czas/miesiąc × 12) × koszt godziny osoby × potencjał redukcji (0.3–0.8)
- **Ryzyko wdrożenia (1–5)** = kontakt z klientem? dane osobowe? wymaga zmian w systemach zewnętrznych?

Wybieracie Państwo kandydata z **górnej trzeciej części wartości** i **ryzykiem ≤ 2**. To zwykle 2–5 pozycji z 80. Pozostałe zostają na później.

---

<!-- template: data -->
## 3.2 Typowe kandydatury w polskim MŚP

Benchmark z 17 firm, które przeszły ten proces w 2025. Kolumna "procent firm" pokazuje, jak często dany use case trafia do top 3.

| Use case | Procent firm | Średnia wartość roczna | Średnie ryzyko |
|---|---|---|---|
| Raporty miesięczne z wielu źródeł | 71% | 180 000 PLN | 1 |
| Obsługa RFP / zapytań ofertowych | 53% | 240 000 PLN | 2 |
| Onboarding nowego pracownika | 47% | 95 000 PLN | 1 |
| Przegląd umów przed podpisaniem | 41% | 210 000 PLN | 2 |
| Odpowiedzi na powtarzające się pytania klientów | 35% | 160 000 PLN | 3 |
| Notatki ze spotkań i follow-up | 29% | 85 000 PLN | 1 |

Dla 70% firm pierwszy use case to wariant "konsolidacja danych / raport" — niewidzialny dla klientów, za to bardzo bolesny wewnętrznie. To jest właściwy punkt startu.

---

<!-- template: standard -->
## 3.3 Kryteria odrzucenia

Niezależnie od wartości — odrzucacie Państwo use case, jeśli spełnia chociaż jedno z poniższych:

- **Wymaga danych osobowych klientów w promptach** (RODO + AI Act → drugi pilot, nie pierwszy).
- **Efekt trafia bezpośrednio do klienta bez przeglądu człowieka** (halucynacja = reputacja).
- **Zależy od systemu, do którego mamy słabe API / brak API** (koszt integracji > koszt AI).
- **Właściciel procesu właśnie idzie na urlop macierzyński / do innej firmy / zmienia dział** (pilot bez ownera zawsze padnie).
- **Lider działu na pytanie "czy ruszamy?" odpowiada *"muszę przemyśleć"*** (brak gotowości operacyjnej).

---

<!-- template: standard -->
## 3.4 Decyzja i commitment

Wybór use case'a kończy się **60-minutowym spotkaniem zarządu**, na którym:

1. Pokazujecie Państwo top 3 kandydatów z arkusza.
2. Rekomendujecie jednego (ten, nie pozostałe).
3. Nadajecie mu właściciela (konkretne imię, nie rolę).
4. Ustalacie budżet (zwykle 40–120 tys. PLN na pilot 8-tygodniowy).
5. Ustalacie **jedną metrykę sukcesu** — tylko jedną, mierzalną, z konkretnym targetem.

Po tym spotkaniu wchodzicie w 5. tydzień — pilot. Następny rozdział opisuje, co dokładnie robić.

> [!info]
> Jedna metryka, nie trzy. *"Skrócenie czasu raportu miesięcznego z 8h do 2h"* działa. *"Poprawa jakości raportów, satysfakcji zespołu i terminowości"* nie. Cokolwiek, co ma spójnik "i", jest w rzeczywistości trzema projektami udającymi jeden.
