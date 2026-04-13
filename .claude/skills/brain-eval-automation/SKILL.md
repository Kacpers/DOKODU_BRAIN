---
name: brain-eval-automation
description: Ocenia request automatyzacji klienta — wartość, ryzyko, utrzymanie. 5 werdyktów: ZRÓB / UPROŚĆ / POC / OUTSOURCE / ODMÓW. Pomaga Kacprowi decydować co wdrażać. Trigger: "oceń automatyzację", "czy to warto automatyzować", "eval automation", "wycena wdrożenia", /brain-eval-automation
---

# brain-eval-automation — Automation Governance Architect

Ocena requestu automatyzacji klienta w 5 minut. Klient przychodzi z pomyslem "chce zautomatyzowac X" — ten skill daje Kacprowi obiektywna ocene: czy to warto robic, jak, i za ile.

## KIEDY UZYWAC

- Klient opisuje proces do automatyzacji (na discovery call lub emailem)
- Kacper sam widzi potencjal automatyzacji u klienta
- Przed pisaniem oferty — zeby wiedziec czy to realny projekt
- `/brain-eval-automation` — szybka ocena w 5 minut

## KIEDY NIE UZYWAC

- Juz masz oferte gotowa (uzyj `/brain-new-offer`)
- To wewnetrzna automatyzacja Dokodu (just do it)
- Potrzebujesz research firmy (uzyj `/brain-lead-research`)

---

## KROK 1: Zbierz opis procesu

Zapytaj: **"Opisz proces ktory klient chce zautomatyzowac — jak najdokladniej."**

Potrzebujesz tych danych (dopytaj o brakujace):

| Dane | Pytanie |
| :--- | :--- |
| Co to za proces? | Nazwa, opis, cel |
| Kto go wykonuje? | Ile osob, jakie role |
| Jak czesto? | Dziennie / tygodniowo / miesiecznie / ad-hoc |
| Ile czasu zajmuje recznie? | Per wykonanie + per miesiac |
| Jakie systemy sa zaangazowane? | Excel, ERP, email, CRM... |
| Czy sa wyjatki / edge cases? | Ile % to "standardowy" przebieg? |
| Jaki jest koszt bledu? | Finansowy, reputacyjny, prawny |

Nie wymagaj wszystkich danych naraz — zbierz co jest, dopytaj o krytyczne braki (czestotliwosc, czas, systemy).

---

## KROK 2: Ocena wielowymiarowa

Zaladuj cennik z `30_RESOURCES/RES_Sales_Playbook/Sales_Playbook.md` — potrzebujesz widelek cenowych do ROI.

Ocen kazdy wymiar 1-5:

```
═══ OCENA AUTOMATYZACJI ═══
Proces: [nazwa]
Klient: [firma]

WYMIAR                    │ SCORE │ KOMENTARZ
──────────────────────────┼───────┼─────────────────────
WARTOSC BIZNESOWA         │ X/5   │ [oszczednosc czasu/pieniedzy]
POWTARZALNOSC             │ X/5   │ [jak regularny i przewidywalny]
ZLOZONOSC TECHNICZNA      │ X/5   │ [ile systemow, ile logiki]
UTRZYMYWALNOSC            │ X/5   │ [czy klient utrzyma sam?]
RYZYKO                    │ X/5   │ [co sie stanie jak sie zepsuje]
──────────────────────────┼───────┼─────────────────────
LACZNY SCORE              │ XX/25 │

ROI SZACUNEK:
- Koszt reczny: [X PLN/mies.] (osoby × czas × stawka)
- Koszt wdrozenia: [X PLN] (z cennika Dokodu)
- Koszt utrzymania: [X PLN/mies.] (infrastruktura + retainer)
- Zwrot inwestycji: [X miesiecy]
```

### Scoring guide

**WARTOSC BIZNESOWA:**
- 5: >10 000 PLN/mies. oszczednosci lub eliminuje krytyczny blad
- 4: 5-10k PLN/mies.
- 3: 2-5k PLN/mies.
- 2: <2k PLN/mies.
- 1: Trudna do zmierzenia / "nice to have"

**POWTARZALNOSC:**
- 5: Dzienny, identyczny przebieg, zero wyjatkow
- 4: Dzienny/tygodniowy, <10% wyjatkow
- 3: Tygodniowy, 10-30% wyjatkow
- 2: Miesieczny lub duzo wyjatkow (30-50%)
- 1: Ad-hoc, kazde wykonanie inne

**ZLOZONOSC TECHNICZNA (odwrocona — nizszy = trudniejszy):**
- 5: 1-2 systemy, proste API, linear flow
- 4: 2-3 systemy, dobrze udokumentowane API
- 3: 3-5 systemow, wymaga custom logic
- 2: Wiele systemow, legacy, slabe API
- 1: Wymaga ML/AI, brak API, reverse engineering

**UTRZYMYWALNOSC:**
- 5: Klient ma IT team, proste do monitorowania
- 4: Klient ma 1 techniczna osobe, jasne alerty
- 3: Wymaga szkolenia, ale wykonalne
- 2: Wymaga specjalistycznej wiedzy
- 1: Tylko Dokodu moze utrzymac (lock-in risk)

**RYZYKO (odwrocone — nizszy = ryzykowniejszy):**
- 5: Blad = drobna niedogodnosc
- 4: Blad = strata czasu (<1 dzien naprawy recznej)
- 3: Blad = strata pieniedzy (ale reversible)
- 2: Blad = compliance issue / strata klienta
- 1: Blad = konsekwencje prawne / safety

---

## KROK 3: Werdykt (5 opcji)

Na podstawie lacznego score i wzorca wymiarow:

**ZROB (20-25 pkt)** — Wysoka wartosc, niska zlozonosc, dobra utrzymywalnosc.
Rekomendacja: "Robimy to. Proponuj [tier z cennika]."

**POC NAJPIERW (15-19 pkt, zlozonosc <=3)** — Wartosc jest, ale technicznie ryzykowne.
Rekomendacja: "Warto, ale najpierw platny Proof of Concept (15-25k PLN) na jednym procesie."

**UPROSCIJ NAJPIERW (15-19 pkt, powtarzalnosc <=3)** — Proces jest zbyt chaotyczny do automatyzacji.
Rekomendacja: "Najpierw warsztat (3-5k PLN) — standaryzacja procesu, potem automatyzacja."

**OUTSOURCE / GOTOWE NARZEDZIE (<15 pkt, zlozonosc 4-5)** — Za mala wartosc na custom wdrozenie, ale istnieje gotowe rozwiazanie.
Rekomendacja: "To nie wymaga custom automatyzacji — polecam [gotowe narzedzie]. Mozemy pomoc we wdrozeniu za [kwota]."

**ODMOW (<12 pkt lub ryzyko=1)** — Za mala wartosc, za duze ryzyko, za duzo wyjatkow.
Rekomendacja: "Nie rekomendujemy automatyzacji tego procesu. [Dlaczego]. Alternatywa: [X]."
WAZNE: Odmowa to tez wartosc — lepiej odmowic niz wdrozyc badziewie.

---

## KROK 4: Rekomendacja dla Kacpra

```
═══ WERDYKT: [ZROB/POC/UPROSCIJ/OUTSOURCE/ODMOW] ═══

REKOMENDACJA:
[2-3 zdania co dokladnie proponowac klientowi]

PROPOZYCJA SCOPE:
- Faza 1: [co]
- Faza 2: [co]
- Retainer: [tak/nie]

WIDELKI CENOWE: [X — Y PLN]

CZAS REALIZACJI: [X tygodni]

NASTEPNY KROK:
→ [konkretna akcja: "wyslij propozycje", "umow warsztat", "polec narzedzie", "odmow grzecznie"]
```

---

## KROK 5: Zapis

Zapytaj: **"Zapisac ocene do profilu klienta?"**

Jezeli tak:
- Jezeli klient ma katalog w `20_AREAS/AREA_Customers/<Klient>/` → dopisz do `<Klient>_Opportunities.md`
- Jezeli nie ma katalogu → zapisz do `00_INBOX.md` z tagiem `#eval-automation`

---

## ZASADY JAKOSCI

1. **Nigdy nie zazyzaj score** zeby wyjsc na "ZROB" — uczciwosc > revenue
2. **ROI musi byc obliczony na liczbach** — nie "duza oszczednosc" ale "8 400 PLN/mies."
3. **Zlozonosc oceniaj realistycznie** — legacy systemy bez API to zawsze <=2
4. **Utrzymywalnosc to klucz** — jezeli klient nie utrzyma, to nie wdrozenie a abonament
5. **Zasada Vesper** — jezeli scope wymaga weekendow Kacpra → automatycznie +100% lub POC
6. **Odmowa to wartosc** — Kacper zyskuje wiarygodnosc odmawiajac bezsensownych projektow
7. **Cennik z Sales Playbook** — zawsze sprawdz aktualne widelki w `30_RESOURCES/RES_Sales_Playbook/Sales_Playbook.md`: wdrozenie MVP min. 20k, kompleksowe min. 50k
