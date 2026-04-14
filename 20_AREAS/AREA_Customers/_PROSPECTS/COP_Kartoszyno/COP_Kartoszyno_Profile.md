---
type: prospect
name: COP Kartoszyno
industry: Noclegi pracownicze / hospitality
contact_person: Wojciech Lubowiedzki
phone: (do uzupełnienia)
email: (do uzupełnienia)
source: (do uzupełnienia)
stage: Oferta wysłana
score: 8/10
---

# COP Kartoszyno — Profil Prospekta

## O firmie
- Obiekt noclegowy w Kartoszynie (okolice elektrowni jądrowej Lubiatowo-Kopalino)
- ~400–500 łóżek, 3 budynki (A, B, C), 8 modułów na budynek
- Obsługuje firmy budowlane / energetyczne (Budimex, PGE, Energa, etc.)
- Strona: kartoszyno.pl

## Obecna sytuacja
- Zarządza rezerwacjami w **zeszycie papierowym**
- Brak widoku obłożenia, brak historii, brak analityki
- Rozlicza za pokój (nie za gościa) — problem z pustymi łóżkami
- Usterki zgłaszane ustnie — giną, brak śledzenia
- Rozliczenia ręczne — koniec miesiąca = mozolne liczenie faktur

## Co chce
- System do zarządzania pokojami i rezerwacjami
- Widok "z lotu ptaka" kto gdzie mieszka (Gantt)
- Rozliczenie miesięczne do faktur (firma po firmie, pokój po pokoju)
- Zgłaszanie usterek ze zdjęciami/filmami
- 3 role: zarząd, recepcja, koordynator firmy
- Mobile-first (tablety, telefony)
- Deadline: czerwiec 2026

## Struktura fizyczna
- 3 budynki (A, B, C), każdy po 8 modułów (4 parter, 4 piętro)
- Moduł ma wejście z zewnątrz, 4–8 lokali
- Lokal = "mieszkanie" ze wspólną łazienką i kuchnią, 1–3 pokoje
- Pokój = najmniejsza jednostka, 2–4 łóżka, zamykany na klucz
- Firmy mogą się mieszać w modułach/lokalach, ale NIE w pokojach
- Oznaczenia: B.1.6 = Budynek B, Moduł 1, Lokal 6

## Model cenowy
- Cena za łóżko ustalana per firma (negocjowana)
- Specjaliści energetyczni płacą więcej, Azjaci mniej
- Firma płaci za pełną pojemność pokoju, nie za liczbę gości
- Okres rozliczeniowy = miesiąc kalendarzowy

## Sales intelligence
- Rozmawia z kilkoma firmami — prawdopodobnie wybierze tańszą
- Nie podał budżetu
- Rozmiar obiektu (400–500 łóżek) sugeruje poważny biznes
- Bliskość elektrowni jądrowej = stały napływ kontrahentów na lata

## Status systemu (2026-04-09)
- **System zbudowany i wdrożony na serwerze testowym**
- URL: https://dev.dokodu.it/wynajem/login
- Konta testowe: zarzad / recepcja / koordynator @kartoszyno.pl (hasło: admin123)
- Repo: git@github.com:Kacpers/kartoszyno.git
- Stack: Next.js 16, Prisma 7, SQLite, Tailwind CSS 4, Docker

## Funkcjonalności systemu
### Pakiet podstawowy (Opcja A)
- Panel główny z usterkami i rozliczeniem
- Oś czasu — widok Gantta
- Zarządzanie rezerwacjami + CSV export
- Tetris Engine — inteligentna alokacja pokoi
- Zarządzanie pokojami (hierarchia Budynek→Moduł→Lokal→Pokój, kolory statusów)
- CRM kontrahentów
- Protokoły zdawczo-odbiorcze (zdjęcia, podpis cyfrowy)
- Rozliczenie miesięczne do faktur (nawigacja po miesiącach)
- Wersja mobilna (tablet + telefon, dolna nawigacja)
- System usterek ze zdjęciami

### Pakiet premium (Opcja B) — powyższe plus:
- System usterek z filmami
- Portal Koordynatora firmy (własny login, moje pokoje, zgłoś usterkę)
- 3 role z uprawnieniami (Zarząd / Recepcja / Koordynator)

## Oferta
- Opcja A: **9 999 PLN** netto (system podstawowy)
- Opcja B: **12 900 PLN** netto (system premium)
- Plik v1: Oferta_COP_Kartoszyno_2026-04.docx (stara, 8 modułów, 2 role)
- Plik v2: Oferta_COP_Kartoszyno_2026-04_v2.docx (aktualna, pełny system, nowe screeny)
- Go-live: ~2 tygodnie od podpisania umowy (w ofercie 4 tyg.)

## Nowe wymagania (feedback 2026-04-14)
Uwagi od Wojciecha Lubowiedzki po testowaniu prototypu:

1. **Rejestr lokatorów w pokojach** — koordynatorzy firm wynajmujących muszą mieć obowiązek wpisywania nazwisk lokatorów przypisanych do konkretnych pokoi
2. **Usuwanie lokatorów po wyjeździe** — gdy lokator wyjeżdża, koordynator musi móc usunąć jego nazwisko z systemu
3. **Wyszukiwanie lokatorów po nazwisku** — policja i straż graniczna regularnie dzwonią pytając o konkretne osoby. System musi umożliwiać szybkie wyszukanie nazwiska i zwrócenie informacji: z jakiej firmy jest lokator i gdzie mieszka (budynek/moduł/lokal/pokój)

> _"Bardzo często do nas dzwoni policja lub straż graniczna i pytają się o informację o dane nazwisko czy jest. Taki system by nam pomagał w wyszukiwaniu danego nazwiska i przekazywaniu informacji z jakiej firmy jest i gdzie mieszka."_ — Wojciech Lubowiedzki

## Historia kontaktu
- **2026-04-09** — Wysłany mail do Pana Wojciecha z ofertą PDF, linkiem do sandboxa (dev.dokodu.it/wynajem) i opisem 3 perspektyw (Zarząd/Recepcja/Koordynator). Zaznaczono że makieta jest poglądowa, docelowe rozwiązanie po warsztacie. Szacowany czas wdrożenia: 4 tygodnie od umowy. Czekamy na feedback.
- **2026-04-14** — Feedback od Wojciecha po testach prototypu: rejestr lokatorów (nazwiska w pokojach), wyszukiwanie po nazwisku (policja/SG). Renegocjacja zamknięta na 10k netto. Status: WYGRANA → implementacja.
