---
name: brain-new-customer
description: Tworzy nowy profil klienta w DOKODU_BRAIN/20_AREAS/AREA_Customers/. Uzyj gdy pojawia sie nowy klient (podpisana umowa) lub gdy chcesz dodac prospekta do bazy. Tworzy automatycznie katalog klienta z plikami Profile, Meetings i Opportunities. Trigger slowa: "nowy klient", "dodaj klienta", "stworz profil klienta", /brain-new-customer
---

# Instrukcja: Tworzenie Nowego Klienta w DOKODU_BRAIN

Gdy uzytkownik uzywa tego skilla, wykonaj nastepujace kroki:

## KROK 1: Zbierz informacje

Zapytaj uzytkownika o:
1. **Nazwa firmy** (pelna nazwa prawna)
2. **Typ**: klient (podpisana umowa) czy prospekt (pipeline)?
3. **Branza** (logistyka / produkcja / finanse / HR / inne)
4. **Wielkosc** (liczba pracownikow orientacyjnie)
5. **Glowny kontakt** (imie, nazwisko, stanowisko, email)
6. **Glowny problem / potrzeba** (1-2 zdania)
7. **Wartosc kontraktu lub szacunkowa** (PLN)
8. **Zrodlo leada** (LinkedIn / Polecenie / Konferencja / Inbound)

Jezeli brakuje danych — uzupelnij `[do uzupelnienia]` i kontynuuj.

## KROK 2: Stworz strukture katalogow

```
/home/kacper/DOKODU_BRAIN/20_AREAS/AREA_Customers/[NazwaFirmy]/
├── [NazwaFirmy]_Profile.md
├── [NazwaFirmy]_Meetings.md
└── [NazwaFirmy]_Opportunities.md
```

Jezeli to prospekt — stworz w `_PROSPECTS/[NazwaFirmy].md` (pojedynczy plik zamiast katalogu).

## KROK 3: Wypelnij pliki

**Profile.md** — na podstawie szablonu `_TEMPLATE_Customer_Profile.md`:
- Wypelnij wszystkie pola zebrane w kroku 1
- Ustaw `status: active` (klient) lub `status: prospect` (prospekt)
- Ustaw `client_since` na dzisiejsza date
- Dodaj link do projektu jezeli juz istnieje

**Meetings.md** — pusty log z dzisiejsza data pierwszego kontaktu (jezeli znana)

**Opportunities.md** — wpisz aktywna wspolprace (jezeli klient) lub otwarty pipeline (jezeli prospekt)

## KROK 4: Zaktualizuj README obszaru

Dodaj klienta do tabeli w `/home/kacper/DOKODU_BRAIN/20_AREAS/AREA_Customers/README.md`

## KROK 5: Potwierdz uzytkownikowi

Wyswietl:
- Sciezki stworzonych plikow
- Liste pól które wymagają uzupelnienia ([do uzupelnienia])
- Nastepny krok (np. "Stworz projekt: /brain-new-project")

## ZASADY

- Nazwy katalogow i plikow: PascalCase, bez spacji, bez polskich znakow
- Jezeli klient ma juz folder — NIE nadpisuj, poinformuj uzytkownika
- Zawsze uzyj dzisiejszej daty jako `last_reviewed`
- Tag klienta to lowercase nazwa firmy (np. `corleonis`, `animex`)
