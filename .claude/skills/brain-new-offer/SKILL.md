---
name: brain-new-offer
description: Tworzy ofertę handlową dla klienta Dokodu — zbiera dane z profilu klienta, dopytuje o szczegóły discovery call, dobiera usługi z cennika i generuje gotową propozycję w Markdown zapisaną w katalogu klienta. Używaj gdy klient jest po discovery call i trzeba wysłać propozycję, gdy piszesz ofertę, proposal lub wycenę dla konkretnej firmy. Trigger: "przygotuj ofertę", "napisz ofertę", "stwórz proposal", "wyceń projekt", "oferta dla klienta", /brain-new-offer
---

# brain-new-offer — Generator Oferty Handlowej Dokodu

## Cel

Wygenerować gotową, profesjonalną propozycję handlową w ciągu jednej rozmowy. Oferta musi sprzedawać WYNIK (spokojny sen CEO), nie usługę. Musi być wysłana max 48h po discovery call.

## Kiedy używać / Kiedy NIE używać

**Używaj gdy:**
- Klient jest po discovery call i czeka na propozycję
- Piszesz ofertę upsell dla istniejącego klienta
- Potrzebujesz szybkiego szkicu propozycji do negocjacji

**NIE używaj gdy:**
- Nie było discovery call (użyj najpierw `/brain-lead-research`)
- Klient nie jest jeszcze zakwalifikowany (użyj `/brain-add-lead` + BANT)
- Chcesz tylko zaktualizować status w CRM (edytuj plik bezpośrednio)

---

## KROK 1: Wczytaj kontekst klienta

1. Zapytaj: **"Dla kogo piszemy ofertę?"** (nazwa firmy)
2. Załaduj profil klienta z `20_AREAS/AREA_Customers/<Klient>/<Klient>_Profile.md`
3. Załaduj notatki ze spotkań: `<Klient>_Meetings.md` — szukaj ostatniego discovery call
4. Załaduj pipeline: `<Klient>_Opportunities.md`

Jeśli klient nie ma katalogu → zasugeruj najpierw `/brain-new-customer`.

---

## KROK 2: Zbierz brakujące dane

Na podstawie wczytanego kontekstu zidentyfikuj luki i zadaj TYLKO pytania o brakujące dane. Maksymalnie 5 pytań naraz.

**Kluczowe dane do oferty:**

| Pole | Źródło | Pytanie jeśli brak |
| :--- | :--- | :--- |
| Problem klienta (jego słowami) | Meetings.md | "Jak klient opisał swój główny problem?" |
| Oczekiwany wynik / KPI | Meetings.md | "Co będzie dla klienta sukcesem? (czas, pieniądze, błędy?)" |
| Zakres (co wdrażamy) | Meetings.md | "Jakie procesy/systemy wchodzą w zakres?" |
| Typ usługi | Profile.md | "Co proponujemy: szkolenie, wdrożenie MVP, kompleksowe, retainer?" |
| Opcja A (baseline) | — | "Co minimum chcemy zaoferować?" |
| Opcja B (premium) | — | "Co pełne rozwiązanie by obejmowało?" |
| Deadline klienta | Meetings.md | "Kiedy klient chce zacząć / kiedy ma deadline?" |
| Dlaczego Dokodu (nie konkurencja) | — | "Co wyróżniło nas w rozmowie?" |

Załaduj cennik z pliku referencyjnego → `references/cennik.md` żeby wstępnie zaproponować widełki.

---

## KROK 3: Zaproponuj wycenę (2 opcje)

Na podstawie zebranych danych zaproponuj:

**Opcja A — MVP/Podstawowe:**
- Minimalny zakres rozwiązujący core problem
- Szybszy czas dostawy
- Niższa cena (z cennika: dolna granica widełek)

**Opcja B — Kompleksowe:**
- Pełny zakres + retainer / wsparcie po wdrożeniu
- Wyższy ROI długoterminowo
- Wyższa cena (górna granica lub package deal)

Zasada wyceny wdrożeń: `(godziny × 1.3) × stawka + infrastruktura + 20% marża`, zaokrąglij do "przyjaznych" kwot (np. 24 900 zamiast 25 100).

Pokaż kalkulację Kacprowi i poczekaj na potwierdzenie/korektę przed generowaniem dokumentu.

---

## KROK 4: Generuj propozycję

Po zatwierdzeniu wyceny — wygeneruj dokument wg struktury poniżej.

**Format pliku:** `<Klient>_Oferta_<YYYY-MM>.md`
**Lokalizacja:** `20_AREAS/AREA_Customers/<Klient>/`

---

### SZABLON PROPOZYCJI

```markdown
---
type: oferta
klient: <Nazwa>
data: <YYYY-MM-DD>
status: szkic | wysłana | zaakceptowana | odrzucona
wartosc_A: <PLN>
wartosc_B: <PLN>
owner: kacper
---

# Propozycja Współpracy: [Nazwa Klienta]
**Dokodu × [Nazwa Klienta] | [Miesiąc Rok]**

---

## Streszczenie (Executive Summary)

> [2-3 zdania: ich problem ich słowami + nasze rozwiązanie + konkretny wynik.
> Przykład: "W Waszym dziale operacyjnym X osób spędza Y godzin tygodniowo na Z.
> Proponujemy wdrożenie automatyzacji, która zredukuje ten czas o ~60% w ciągu 6 tygodni.
> Przy obecnych kosztach oznacza to oszczędność ok. NNN PLN miesięcznie."]

---

## Rozumiemy Wasz Problem

[Opisz problem z perspektywy klienta — używaj ich języka z discovery call.
Pokaż, że słuchałeś. Nie używaj żargonu technicznego.]

**Obecna sytuacja:**
- [Konkretny ból #1]
- [Konkretny ból #2]
- [Konsekwencje: czas / pieniądze / ryzyko]

---

## Nasze Podejście

[Opisz metodologię — NIE listę narzędzi. Klient kupuje podejście i pewność, nie n8n.]

**Jak pracujemy:**
1. [Faza 1: np. Analiza i mapowanie procesów — co robimy i po co]
2. [Faza 2: np. Budowa MVP — co dostarczamy]
3. [Faza 3: np. Testy i wdrożenie produkcyjne]
4. [Opcjonalnie: Wsparcie i optymalizacja]

---

## Co Dostarczamy (Zakres)

**Opcja A — [Nazwa, np. "Start AI"]:**
- [ ] [Deliverable 1]
- [ ] [Deliverable 2]
- [ ] [Deliverable 3]

**Opcja B — [Nazwa, np. "AI Full Stack"]:**
- Wszystko z Opcji A, plus:
- [ ] [Dodatkowy deliverable 1]
- [ ] [Dodatkowy deliverable 2]
- [ ] Retainer [X] miesięcy po wdrożeniu

---

## Harmonogram

**Opcja A — [X] tygodni:**

```
Tydzień 1-2  │ Analiza i mapowanie
Tydzień 3-4  │ Budowa MVP
Tydzień 5    │ Testy z teamem klienta
Tydzień 6    │ Go-live i przekazanie
```

**Opcja B — [X] tygodni + retainer:**

```
Tydzień 1-2  │ Analiza i architektura
Tydzień 3-6  │ Budowa pełnego rozwiązania
Tydzień 7-8  │ Integracje i testy
Tydzień 9    │ Go-live
Miesięcznie  │ Monitoring i optymalizacja (retainer)
```

---

## Inwestycja

| | Opcja A | Opcja B |
| :--- | ---: | ---: |
| **[Zakres A]** | [X PLN] | — |
| **[Zakres B]** | — | [Y PLN] |
| **Retainer (opcjonalnie)** | — | [Z PLN/mies.] |
| **Łącznie** | **[X PLN] netto** | **[Y PLN] netto** |

*Ceny netto + 23% VAT. Płatność: 50% zaliczka, 50% po go-live.*

> **Dlaczego warto:** Przy [aktualnym koszcie procesu = X PLN/mies.], inwestycja zwraca się w [Y miesięcy].

---

## Dlaczego Dokodu

- **[Argument 1 specyficzny dla tego klienta]** — np. "Mamy za sobą podobny projekt w branży logistycznej (Corleonis)"
- **Tech + Legal w jednym zespole** — wdrożenie i compliance AI Act od razu
- **Bez lock-in** — wszystko na Twojej infrastrukturze, Twoje dane, Twój kod

---

## Następny Krok

**Jeśli chcesz ruszyć z Opcją [A/B]:**

1. Odpowiedz na tego maila z potwierdzeniem
2. Prześlę umowę w ciągu 24h
3. Kickoff call ustawiamy na [data propozycja]

**Masz pytania?** Zadzwoń: [numer Kacpra] lub odpisz bezpośrednio.

---
*Dokodu Sp. z o.o. | kacper@dokodu.pl | dokodu.pl*
*Oferta ważna 14 dni od daty wystawienia.*
```

---

## KROK 5: Generuj PDF i zapisz

**Generator PDF** — gotowy w systemie:

```bash
cd /home/kacper/DOKODU_BRAIN/30_RESOURCES/RES_Templates/offer-generator
python3 generate.py <offer_data.json> <output.pdf>
```

Schemat JSON do wypełnienia: patrz sekcja `getTestData()` w `generate.py`.

Plik wynikowy zapisz do katalogu klienta:
`20_AREAS/AREA_Customers/<Klient>/Oferta_<Klient>_<YYYY-MM>.pdf`

Następnie:

1. Zaktualizuj `CRM_Leady_B2B.md` — zmień etap na **"Propozycja"**, wpisz wartość (Opcja A i B)
3. Zaktualizuj `<Klient>_Opportunities.md` — dodaj/zaktualizuj aktywną okazję
4. Przypomnij Kacprowi: *"Wyślij propozycję max 48h po discovery call. Follow-up po 5 dniach bez odpowiedzi (PROMPT-020 variant B)."*

---

## Zasady jakości

Przed oddaniem sprawdź:
- [ ] Problem jest opisany słowami klienta, nie naszym żargonem
- [ ] Obie opcje cenowe są obecne i logicznie uzasadnione
- [ ] Jest konkretny ROI / zwrot inwestycji (liczby)
- [ ] Następny krok jest jednoznaczny (co klient ma zrobić)
- [ ] Cena jest nazwana "Inwestycją", nie "Kosztem"
- [ ] Frontmatter YAML jest wypełniony
