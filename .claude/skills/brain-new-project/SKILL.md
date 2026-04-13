---
name: brain-new-project
description: Tworzy nowy plik projektu w DOKODU_BRAIN/10_PROJECTS/ na podstawie szablonu. Uzyj gdy zaczyna sie nowy projekt dla klienta lub wewnetrzny. Automatycznie wypelnia YAML frontmatter, brief, fazy i checklist. Trigger slowa: "nowy projekt", "stworz projekt", "zacznij projekt", /brain-new-project
---

# Instrukcja: Tworzenie Nowego Projektu w DOKODU_BRAIN

## KROK 1: Zbierz informacje

Zapytaj o:
1. **Nazwa projektu** (krotka, np. "MedCorp_Wdrozenie" lub "Kurs_Python_Launch")
2. **Typ projektu**: szkolenie / wdrozenie / produkt-cyfrowy / wewnetrzny
3. **Klient** (nazwa firmy lub "internal")
4. **Wartosc kontraktu** (PLN netto)
5. **Deadline** (data YYYY-MM-DD)
6. **Krotki opis problemu klienta** (1-2 zdania)
7. **Nasze rozwiazanie** (1-2 zdania)
8. **Health na start** (green / yellow / red — zazwyczaj green)

## KROK 2: Stworz katalog i plik

Sciezka: `/home/kacper/DOKODU_BRAIN/10_PROJECTS/PRJ_[NazwaProjektu]/PRJ_[NazwaProjektu].md`

## KROK 3: Wypelnij szablon projektu

Uzyj tej struktury (dostosuj typ projektu):

```markdown
---
type: project
status: active
owner: kacper
last_reviewed: [dzisiaj]
tags: [projekt, [typ], [klient-lowercase]]
client: [klient]
value_pln: [wartosc]
deadline: [YYYY-MM-DD]
health: green
---

# PRJ: [Nazwa] — [Klient]
> Brief projektu, wartosc, status, kontakt klienta

## BRIEF PROJEKTU
**Problem klienta:** [opis]
**Rozwiazanie Dokodu:** [opis]
**Oczekiwane efekty:** [lista]

## FAZY I CHECKLIST
### FAZA 0: PRZYGOTOWANIE
- [ ] Podpisanie umowy
- [ ] Zaliczka odebrana
- [ ] Kickoff call zaplanowany

### FAZA 1: [dostosuj do typu]
- [ ]
- [ ]

### FAZA OSTATNIA: FOLLOWUP
- [ ] Faktura koncowa wystawiona
- [ ] NPS survey wyslany
- [ ] Case study rozwazyc
- [ ] Oferta upsell wyslana

## RYZYKA
| Ryzyko | Prawdop. | Mitygacja |
| :--- | :---: | :--- |
| | | |

## METRYKI SUKCESU
-

## LINKI
- Klient: [[../../20_AREAS/AREA_Customers/[Klient]/[Klient]_Profile]]
- Playbook: [[../../30_RESOURCES/RES_Industry_Playbooks/Playbook_[Branza]]]
```

## KROK 4: Zaktualizuj Dashboard

Dodaj projekt do tabeli STATUS PROJEKTOW w `/home/kacper/DOKODU_BRAIN/000_DASHBOARD.md`

## KROK 5: Zaktualizuj Customers

Dodaj projekt do `[Klient]_Opportunities.md` jako "Aktywna wspolpraca"

## KROK 6: Potwierdz

Wyswietl sciezki stworzonych i zaktualizowanych plikow.

## ZASADY

- Prefiks katalog/plik zawsze: `PRJ_`
- NazwaProjektu: PascalCase bez spacji i polskich znakow
- Health: green (nowy, na torze), yellow (ryzyko), red (blokada)
- Jezeli projekt dla istniejacego klienta — sprawdz czy folder klienta istnieje w AREA_Customers
