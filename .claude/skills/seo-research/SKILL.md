---
name: seo-research
description: Bada temat pod kątem SEO dla dokodu.it/blog/ — analizuje zapytania w GSC, szuka powiązanych fraz, intencje wyszukiwań, konkurencję i rekomenduje kąt artykułu. Łączy dane GSC z web researchem. Trigger: "zbadaj temat seo", "zrób keyword research", "jakie frazy dla", "researchu seo", /seo-research
---

# Instrukcja: SEO Research

Cel: dla podanego tematu/frazy zbudować pełny obraz keyword landscape i zarekomendować najlepszy kąt artykułu dla dokodu.it.

## KROK 1: Pobierz powiązane frazy z GSC

```bash
cd /home/kacper/DOKODU_BRAIN/scripts && python3 gsc_fetch.py --from-db --mode queries --json
```

Z wyjścia JSON przefiltruj zapytania powiązane z tematem podanym przez użytkownika.
Wypisz: zapytanie | kliknięcia | impressions | CTR | pozycja

## KROK 2: Web Research — konkurencja i wolumeny

Użyj WebSearch żeby zbadać:

1. **Top 5 wyników Google PL** dla głównego słowa kluczowego
   - Jakie strony dominują?
   - Jakie typy contentu (pillar, lista, how-to, case study)?
   - Jakie nagłówki H1 używają?

2. **Powiązane frazy** — wyszukaj "[temat] site:Google PL" i sprawdź "Люди также ищут" (People Also Ask)
   - Minimum 5 powiązanych fraz z szacowanym intendem

3. **Competitor content gaps** — czego NIE ma w top wynikach (co Dokodu może zrobić lepiej)?

## KROK 3: Klasyfikacja Intencji

Dla każdej zebranej frazy przypisz intent:
- `informational` — użytkownik chce wiedzieć (jak działa X, co to jest X)
- `commercial` — użytkownik rozważa zakup/wdrożenie (najlepszy X, X vs Y, X cena)
- `transactional` — użytkownik chce kupić/zamówić (kup X, zamów X)
- `navigational` — użytkownik szuka konkretnej marki

## KROK 4: Rekomendacja Kąta

Podaj JEDNĄ rekomendację: jaki artykuł napisać, żeby wygrać z konkurencją:

```
REKOMENDOWANY ARTYKUŁ:
- Tytuł SEO: [tytuł z główną frazą]
- Główna fraza: [keyword] (est. X/mies.)
- Frazy poboczne: [keyword2], [keyword3]
- Intent: [informational/commercial]
- Format: [pillar page / how-to / porównanie / case study / lista]
- Kąt wyróżniający: [czego nie ma konkurencja a co Dokodu może dać — np. PL perspektywa, case study z polskiej firmy, cennik PLN]
- Powiązane strony do linkowania wewnętrznego: [URL1], [URL2]
```

## KROK 5: Zaproponuj dodanie do Ideas Bank

Podaj gotową komendę (nie uruchamiaj):
```bash
python3 /home/kacper/DOKODU_BRAIN/scripts/seo_ideas.py add "[tytuł]" \
  --keyword "[główna fraza]" \
  --secondary "[fraza2], [fraza3]" \
  --intent [informational/commercial] \
  --pillar "[pillar]" \
  --priority high \
  --source seo-research \
  --notes "[kąt wyróżniający]"
```

## ZASADY

- Skupiaj się na polskich wynikach (lang:pl) — to jest target Dokodu
- Zawsze szukaj fraz z commercial intent → wyższy ROI dla Dokodu
- Minimum 1 fraza "long tail" (4+ słowa) — łatwiej wygrać pozycję
- Jeśli fraza ma <20 impressions w GSC i brak danych webowych → niska priorytet
- Zawsze link do `/seo-plan-post` jako następny krok
