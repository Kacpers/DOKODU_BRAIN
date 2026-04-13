---
name: brain-archive-project
description: Archiwizuje zakonczony projekt — przeprowadza retrospekywe, przenosi do 40_ARCHIVE, aktualizuje profil klienta i wydobywa wiedze do blueprintow/playbooks. Uzyj gdy projekt jest oficjalnie zamkniety (podpisany odbior, faktura wyplacona). Trigger: "archiwizuj projekt", "zamknij projekt", "projekt zakonczony", /brain-archive-project
---

# Instrukcja: Archiwizacja Zakonczonego Projektu

Archiwizacja to nie tylko przeniesienie pliku. To ekstrakcja wiedzy dla przyszlych projektow.

## KROK 1: Potwierdzenie

Zapytaj:
1. **Ktory projekt archiwizujemy?** (nazwa)
2. **Czy faktura koncowa jest wyplacona?** (jezeli nie — STOP, nie archiwizuj)
3. **Jaki byl wynik NPS?** (jezeli zbierany)
4. **Czy mozemy opublikowac case study?** (tak / nie / za zgoda klienta)

## KROK 2: Retrospektywa (wypelnij wspolnie z uzytkownikiem)

Zadaj pytania:
1. Co poszlo dobrze? (3 rzeczy)
2. Co poszlo zle lub moglo byc lepiej?
3. Co zrobimy inaczej w nastepnym projekcie?
4. Co nalezy zaktualizowac w Blueprintach lub Playbooku branżowym?
5. Czy byl potencjal upsell — czy go wykorzystalismy?

## KROK 3: Stworz folder archiwum

Sciezka: `/home/kacper/DOKODU_BRAIN/40_ARCHIVE/PRJ_[Nazwa]_[Rok]/`

Skopiuj (nie przenosisz) do archiwum:
- Plik projektu z `10_PROJECTS/`
- Plik retrospektywy (stworz nowy na podstawie odpowiedzi z Kroku 2, uzyj szablonu T-020 z Templates.md)

Dopisz na gorze oryginalnego pliku projektu:
```yaml
status: archived
archived_date: [dzisiaj]
archived_to: 40_ARCHIVE/PRJ_[Nazwa]_[Rok]/
```

## KROK 4: Zaktualizuj profil klienta

W `/home/kacper/DOKODU_BRAIN/20_AREAS/AREA_Customers/[Klient]/[Klient]_Profile.md`:
- Dodaj projekt do tabeli HISTORIA WSPOLPRACY ze statusem "Zamkniete"
- Zaktualizuj "Lacna wartosc wspolpracy"
- Uzupelnij sekcje POTENCJAL UPSELL na podstawie wiedzy z projektu

W `[Klient]_Opportunities.md`:
- Przenies projekt z "Aktywna wspolpraca" do "Historia"
- Dodaj nowe okazje upsell odkryte podczas projektu

## KROK 5: Ekstrakcja wiedzy (najwazniejszy krok)

Na podstawie retrospektywy zaproponuj:

**Blueprinty n8n:**
- Czy powstal workflow, ktory mozna uogolnic i dodac do `N8N_Blueprints.md`?
- Jezeli tak — zaproponuj dodanie jako BP-[NR]

**Playbook branżowy:**
- Czy zdobylismy wiedze branżowa ktora nalezy zaktualizowac w Playbooku?
- Jezeli tak — zaproponuj konkretne uzupelnienie

**Biblioteka promptow:**
- Czy uzyto nowych promptow ktore nie sa w bibliotece?
- Jezeli tak — zaproponuj `/brain-new-prompt`

**Case Study:**
- Jezeli klient zgodzil sie — sformatuj dane do case study:
  - Problem (ich slowami)
  - Rozwiazanie (nasza architektura)
  - Wyniki (liczby: godziny, procenty, PLN)
  - Cytat klienta (jesli mamy)

## KROK 6: Zaktualizuj Dashboard

Usun projekt z tabeli STATUS PROJEKTOW w `000_DASHBOARD.md`.

## KROK 7: Potwierdz

Wyswietl liste wszystkich zmodyfikowanych plikow.

## ZASADY

- NIE archiwizuj jezeli faktura nie jest wyplacona
- NIE usuwaj oryginalnego pliku — tylko oznacz jako archived
- Archiwum jest read-only — jezeli chcesz cos poprawic, rob to w kopii
- Retencja archiwum: 5 lat dla klientow, 2 lata dla projektow wewnetrznych
