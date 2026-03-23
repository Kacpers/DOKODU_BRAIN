---
type: resource
status: active
owner: both
last_reviewed: 2026-03-06
tags: [onboarding, klienci, kickoff, komunikacja, odbiory, cr]
---

# CLIENT ONBOARDING — Dokodu Standard
> **Cel:** Pierwsze 30 dni z klientem decyduje, czy zostanie na 3 lata. Zrob to dobrze.
> **Zasada:** Klient kupil spokojny sen, nie projekt IT. Dawaj mu pewnosc na kazdym kroku.

---

## TYDZIEN 0: PRZYGOTOWANIE (przed kickoff)

### Wewnetrzne (Dokodu side)
- [ ] Brief projektu wewnetrzny — Kacper + Alina czyta umowe i rozumie zakres
- [ ] Folder projektu stworzony (Google Drive + Dokodu Brain → [[10_PROJECTS/]])
- [ ] Narzedzia: dostep do klienckich systemow zamowiony z wyprzedzeniem
- [ ] Slack/Teams: decyzja — osobny kanal u nas czy u klienta?
- [ ] Onboarding pack przygotowany (patrz nizej)

### Zewnetrzne (klient side)
Wyslij do klienta "Pre-Kickoff Checklist":
```
Czesc [Imie],

Cieszymy sie ze wspolpracy! Zeby kickoff byl efektywny, prosze o przygotowanie:

1. DOSTEPY (potrzebujemy przed kickoff):
   [ ] Email dostep do systemow, z ktorymi bedziemy pracowac
   [ ] VPN lub inne dostepy do sieci firmowej (jezeli wdrozenie on-premise)
   [ ] Kontakt do IT/Admina, ktory moze nadawac uprawnienia

2. DOKUMENTY:
   [ ] Opis obecnego procesu (nawet krotki email opisujacy "jak to dziala teraz")
   [ ] Przykladowe pliki/dokumenty (3-5 przykladow rzeczywistych — mozesz zanonimizowac)
   [ ] Lista systemow, z ktorymi mamy sie integrowac (z numerami wersji)

3. KONTAKTY:
   [ ] Kto jest "internal champion" — osoba po Waszej stronie, ktora dopilnuje projektu?
   [ ] Kto jest uzytkownikiem konczowym systemu (musimy z nim porozmawiac)
   [ ] Kto podpisuje odbiory (UAT approval)?

Majac to, zrobimy kickoff 2x szybciej.

Kacper
```

---

## KICKOFF CALL (45-60 min)

### Agenda (wyslij dzien wczesniej)
```
AGENDA KICKOFF — [Projekt] × Dokodu

1. Cel spotkania i agenda (2 min)
2. Powitanie i przedstawienie (5 min)
3. Potwierdzenie zakresu i celów (10 min)
   — "Upewnijmy sie, ze mamy te sama wizje sukcesu"
4. Model wspolpracy (10 min)
   — komunikacja (kanal, czestotliwosc)
   — dostepy i bezpieczenstwo
   — procedura zmian zakresu
5. Timeline — etapy i milestones (10 min)
6. Pytania i ustalenie pierwszego zadania (10 min)
7. Nastepne spotkanie: [data]
```

### Kluczowe ustalenia do zapisania po kickoff
- [ ] Zdefiniowany "Definition of Done" dla kazdego etapu
- [ ] Zaakceptowany harmonogram (daty milestones, kto co robi)
- [ ] Procedura raportowania (jak i kiedy)
- [ ] Procedura zmian (aneks → co wchodzi w budzet, co nie)
- [ ] Eskalacja: kto do kogo, gdy cos idzie nie tak

---

## TYDZIEN 1-2: DISCOVERY I DIAGNOZA

### Warsztaty mapowania procesu (1-2h z klientem)
**Cel:** Zrozumiec obecny stan ZANIM zaproponujesz rozwiazanie.

**Narzedzia:**
- Miro / FigJam: mapowanie procesu (Swimlane lub flowchart)
- Nagranie spotkania (za zgoda!) dla dokumentacji
- Kwestionariusz procesowy:

```
KWESTIONARIUSZ MAPOWANIA PROCESU (Dokodu)

1. Krok po kroku: jak wygladal proces WCZORAJ? (opisz jak Twojemu 12-letniemu dziecku)
2. Gdzie tracisz najwiecej czasu? (TOP 3 bole)
3. Jakie sa najczestsze bledy w tym procesie? (i ile kosztuja?)
4. Jakie systemy sa zaangazowane? (lista, wersje)
5. Ile osob uczestniczy? (role, nie imiona)
6. Jak czesto ten proces sie powtarza? (dzienny/tygodniowy/zdarzeniowy)
7. Jakie sa wyjatki od reguly? (edge cases — to czesto psuje automatyzacje)
8. Co bylo probowane wczesniej? (co zadzialalo, co nie i dlaczego?)
9. Jak wyglada sukces dla Ciebie? (konkretnie, mierzalnie)
10. Co sprawia, ze ten projekt moze sie nie powies? (szczerosc jest bezcenna)
```

---

## KOMUNIKACJA PRZEZ PROJEKT

### Standard komunikacji Dokodu
| Kanal | Do czego | Czas reakcji |
| :--- | :--- | :---: |
| Slack/Teams | Pytania operacyjne, szybkie decyzje | <4h (w godz. roboczych) |
| Email | Formalne ustalenia, dokumenty | <24h |
| Video call | Skomplikowane tematy, demo, retrospektywy | Wg harmonogramu |
| Telefon | TYLKO pilne/kryzysowe | Zawsze |

### Raportowanie statusu
**Format raportu tygodniowego (wyslij co piatek):**
```
STATUS UPDATE — [Projekt] — Tydzien [X]

STATUS OGOLNY: ZIELONY / ZOLTY / CZERWONY

CO ZOSTALO ZROBIONE W TEN TYDZIEN:
- [zadanie 1]
- [zadanie 2]

CO PLANUJEMY W NASTEPNYM TYGODNIU:
- [zadanie 1]
- [zadanie 2]

POTRZEBUJEMY OD KLIENTA:
- [akcja 1 — do [data]]

RYZYKA / PROBLEMY:
- [opis, wplyw, plan mitygacji]

MILESTONE STATUS:
- [Etap 1]: ZAKONCZONE / W TRAKCIE / PLANOWANE
- [Etap 2]: ...
```

---

## ODBIORY I MILESTONES

### Definition of Done (per etap — ustalane na kickoff)
Kazdy etap musi miec KONKRETNE kryteria odbioru, np.:
- "MVP workflow przetwarza 95% testowych dokumentow bez bledow w UAT"
- "Szkolenie zakonczone, wszyscy uczestnicy wypelnili ankiete satysfakcji (NPS>7)"

### Protokol odbioru
1. Dokodu: przygotuj "Release Notes" (co dostarczone, jak testowac)
2. Klient: 5-7 dni roboczych na testy UAT
3. Klient: zglosenie usterek (lista, priorytet)
4. Dokodu: naprawa usterek krytycznych (w ramach scope)
5. Klient: podpisanie protokolu odbioru etapu
6. Dokodu: wystawienie faktury za etap

### Zmiany zakresu (Change Request)
Jezeli klient chce czegos, co nie bylo w umowie:
1. Potwierdz na pismie (email): "Rozumiem, ze chcesz X. To wykracza poza obecny zakres."
2. Wycen zmiane: godziny × stawka + 20% bufora
3. Wyslij Change Request do podpisania (Alina przygotowuje wzor)
4. Po podpisaniu: implementuj

**NIGDY nie rob "bo klient poprosil" bez pisemnego CR. To droga do bezplatnej pracy.**

---

## 30 DAYS CHECK-IN (po miesiacu od go-live)

Spotkanie 30-minutowe z klientem:
1. Co dziala dobrze? (zbierz przykladowe "wygrane" — do case study!)
2. Co mozna poprawic?
3. Czy uzytkownicy adoptowali system? (jezeli nie — dlaczego?)
4. Czy sa nowe pomysly/potrzeby? (okazja do upsell naturalnego)
5. NPS: "Na skali 0-10, jak bardzo polecilbys Dokodu swojemu znajomemu?"

**Po spotkaniu:** Wyslij email podsumowujacy + propozycja retainera (jezeli nie maja).

---

## OFFBOARDING (zakonczenie projektu)

Nawet jezeli projekt sie konczy — relacja trwa.

- [ ] Final delivery: dokumentacja techniczna + uzytkownika
- [ ] Knowledge transfer: 2h sesja z IT klienta (jezeli wdrozenie)
- [ ] Referencje: popros o pisemna referencje lub nagranie wideo
- [ ] Case study: czy mozemy opublikowac? (NDA pozwala?)
- [ ] Testimonial na LinkedIn: wyslij link do profilu Kacpra
- [ ] Retainer pitch: "Jak bedziemy mogli wspierac Was dalej?"
- [ ] Urodziny firmy / rocznica projektu: wyslij pamiatke (relacja!)

---

## ONBOARDING PACK (wyslij klientowi w Dniu 1)

Zestaw dokumentow, ktore klient dostaje na start:
1. "Witamy w Dokodu" — 1-stronicowy dokument: kim jestesmy, jak pracujemy, czego oczekujemy
2. Harmonogram projektu (PDF lub Miro)
3. Kontakty: Kacper + Alina + ich role i kiedy kontaktowac
4. FAQ: najczestsze pytania na start projektu
5. Link do Slack/Teams workspace

*Onboarding pack = pierwsze wrazenie. Profesjonalizm zaczyna sie tu.*
