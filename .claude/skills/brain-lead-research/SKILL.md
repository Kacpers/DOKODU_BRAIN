---
name: brain-lead-research
description: Bada i kwalifikuje potencjalnych klientow dla Dokodu. Na podstawie branzy, firmy lub osoby — sprawdza fit z ICP, szacuje potencjal, sugeruje personalizowany outreach. Bazuje na ICP Dokodu (firmy 50-500 prac., problemy z AI/automatyzacja). Inspirowany lead-research-assistant z awesome-claude-skills. Trigger: "zbadaj lead", "sprawdz firme", "research klienta", /brain-lead-research
---

# Lead Research Assistant — Dokodu Edition

Adapatacja lead-research-assistant dla kontekstu Dokodu sp. z o.o. — agencja AI automation Tech+Legal.

## DOKODU ICP (zawsze uwzgledniaj przy kwalifikacji)

**Firma:**
- Polska firma, 50-500 pracownikow
- Branza: logistyka, produkcja, finanse B2B, HR tech, uslugi B2B
- Uzywaja juz AI (Copilot, ChatGPT) ale nie widza efektow LUB maja procesy reczne ktore chca automatyzowac
- Maja budzet >10 000 PLN na wdrozenie
- Maja "internal champion" (ktos w firmie chce zmiany)

**Kontakt (decision maker):**
- CEO, COO, Dyrektor Operacyjny, IT Manager decyzyjny
- Jezykami mowia: "oszczednosc czasu", "redukcja bledow", "compliance", "ROI"

## KIEDY UZYWAC

- Przed cold outreach — sprawdz czy firma spelnia ICP
- Po poleceniu lub spotkaniu na konferencji — zbadaj kontekst
- Przy przygotowaniu do discovery call — co wiemy o firmie?
- Przy poszukiwaniu nowych leadow w konkretnej branzy

## JAK UZYWAC

**Wariant A — Znana firma:**
```
Zbadaj firme [Nazwa] pod katem wspolpracy z Dokodu. Sprawdz: branze, wielkosc, stos IT, czy uzywaja AI.
```

**Wariant B — Szukaj leadow:**
```
Znajdz 5-10 firm w branzy [logistyka/produkcja/finanse] z Polski, 50-500 prac., ktore moga miec problem z [automatyzacja dokumentow/wdrozeniem AI].
```

**Wariant C — Przygotowanie do discovery call:**
```
Mam discovery call z [Firma] za 2 godziny. Przygotuj mi: kontekst firmy, mozliwe bole, pytania do zadania, nasz pitch.
```

## PROCES

### 1. Analiza firmy (WebSearch + WebFetch)
Zbierz:
- Branza i glowna dzialalnosc
- Wielkosc (pracownicy, przychody jesli dostepne)
- Lokalizacja (Polska — tak / nie)
- Strona www — czy maja blog o AI/automatyzacji? (sygnał zainteresowania)
- LinkedIn — kto jest CEO/COO/IT Manager? Ile maja obserwujacych? Co postuja?
- Czy sa wzmianki o Copilot/ChatGPT/AI w mediach lub job ofertach?
- Job offers — czy rekrutuja na "AI", "automatyzacja", "RPA"? (sygnał budzetu i potrzeby)
- Newsroom — finansowanie, ekspansja, problemy (kontekst do pitcha)

### 2. ICP Fit Score

Ocen na skali 1-5 kazde kryterium:

| Kryterium | Ocena | Komentarz |
| :--- | :---: | :--- |
| Wielkosc (50-500 prac.) | /5 | |
| Branza (operacyjna) | /5 | |
| Problem z AI widoczny | /5 | |
| Budzet potencjalny | /5 | |
| Decision maker dostepny | /5 | |
| **SUMA** | /25 | |

Score:
- 20-25: Idealny lead — priorytet
- 15-19: Dobry lead — warto podjac
- 10-14: Sredni — nurturing
- <10: Nie inwestuj czasu

### 3. Personalizacja outreach

Na podstawie researchu przygotuj:

**Hook (pierwsze zdanie)** — konkretny do tej firmy:
> "Widzialem/am ze [Firma] rekrutuje na stanowisko [X] — to czesto oznacza ze [proces] jest reczny i bolesny. Czy tak jest u Was?"

**Problem hipoteza** — co prawdopodobnie ich boli:
> "Firmy w [branza] z [X] pracownikami zazwyczaj mają problem z [konkretny proces]."

**Dowod** — nasze referencje z podobnej branzy:
> Corleonis (logistyka) / Animex (produkcja)

**CTA** — jedno, proste:
> "15-minutowa rozmowa — sprawdzimy czy mamy cos dla Was."

### 4. Zapis

Jezeli lead jest KWALIFIKOWANY (score >15):
- Zaproponuj dodanie do CRM: `/brain-add-lead`
- Jezeli duzy potencjal: zaproponuj stworznie prospekta: `/brain-new-customer`

## FORMAT RAPORTU

```
LEAD RESEARCH: [Nazwa Firmy]
Data: [dzisiaj]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROFIL FIRMY
  Branza:       [branza]
  Wielkosc:     [X] pracownikow
  Lokalizacja:  [miasto, Polska: tak/nie]
  Strona:       [URL]
  LinkedIn CEO: [imie, link]

ICP FIT SCORE: [X]/25 — [Idealny/Dobry/Sredni/Slaby]

MOZLIWY PROBLEM (hipoteza):
  [opis bolu na podstawie researchu]

SYGNALY ZAINTERESOWANIA AI:
  + [sygnał 1]
  + [sygnał 2]
  - [brak sygnalu]

PERSONALIZOWANY HOOK:
  "[tresc pierwszego zdania]"

REKOMENDACJA:
  [Priorytetowy outreach / Nurturing / Pomiń]

NASTEPNY KROK:
  [konketna akcja]
```
