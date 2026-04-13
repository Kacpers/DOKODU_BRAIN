---
name: seo-plan-post
description: Planuje nowy post na blog dokodu.it od słowa kluczowego do pełnego briefu produkcyjnego. Generuje SEO tytuł, slug, meta description, strukturę H2/H3, intro hook, CTA i brief do pisania. Zapisuje do SEO_Ideas_Bank. Trigger: "zaplanuj post", "brief seo", "napisz brief bloga", "plan artykułu", /seo-plan-post
---

# Instrukcja: SEO Plan Post

Cel: z podanego tematu/frazy wygenerować kompletny brief produkcyjny gotowy do pisania posta na dokodu.it/blog/.

## KROK 0: Zbierz dane wejściowe

Potrzebujesz od użytkownika (zapytaj jeśli nie podał):
1. Temat / główna fraza kluczowa
2. Typ contentu (how-to / porównanie / case study / pillar / lista)
3. Docelowy czytelnik (np. "manager IT w firmie 200 osób")

## KROK 1: Sprawdź GSC pod kątem frazy

```bash
python3 /home/kacper/DOKODU_BRAIN/scripts/gsc_fetch.py --from-db --mode queries --json
```

Sprawdź czy fraza lub powiązane frazy już generują impressions/kliknięcia na dokodu.it.
Jeśli tak → mamy punkt startowy i wiemy z jakiej pozycji startujemy.

## KROK 1b: Sprawdź Link Graph — sugestie linków wewnętrznych

```bash
python3 /home/kacper/DOKODU_BRAIN/scripts/link_graph.py --suggest "[główna fraza tematu]"
```

To pokaże istniejące artykuły które warto podlinkować z nowego artykułu.
Wyniki użyj do wypełnienia sekcji **Linki Wewnętrzne** w briefie.

Sprawdź też sieroty (artykuły bez linków przychodzących):
```bash
python3 /home/kacper/DOKODU_BRAIN/scripts/link_graph.py --orphans
```
Jeśli nowy artykuł może linkować do sieroty z naturalnym pretekstem → uwzględnij to.

## KROK 2: Web Research (szybki)

Użyj WebSearch aby sprawdzić:
- Top 3 wyniki Google PL dla głównej frazy → jakie formaty, długości, nagłówki?
- Czy istnieje "People Also Ask" → dodatkowe pytania do H2/H3

## KROK 3: Wygeneruj pełny brief

Wygeneruj brief w tym formacie:

---

## BRIEF: [Tytuł roboczy]

**Data:** [data]
**Autor:** Kacper Sieradzinski

### SEO Meta
| Element | Wartość |
|---------|---------|
| **SEO Title** | [tytuł max 60 znaków, z frazą kluczową na początku] |
| **Slug** | /blog/[slug-po-polsku-z-myślnikami] |
| **Meta Description** | [opis 120-155 znaków, z frazą kluczową, z CTA] |
| **Główna fraza** | [keyword] |
| **Frazy poboczne** | [keyword2], [keyword3] |
| **Search Intent** | informational / commercial |
| **Szacowana długość** | [800-1200 / 1500-2500 / 2500+] słów |

### Dla Kogo
[1 zdanie — konkretna persona: np. "Manager IT w polskiej firmie 100-500 os. rozważający wdrożenie M365 Copilot"]

### Hook (pierwsze 2 zdania artykułu)
[Napisz przykładowy hook — angażujący, z konkretną obietnicą wartości]

### Struktura

**H1:** [tytuł artykułu — taki sam lub podobny do SEO Title]

**Intro:** (150-200 słów)
- Problem / pain point czytelnika
- Co artykuł rozwiąże
- Social proof lub liczba (np. "X firm w Polsce już wdrożyło...")

**H2: [Nagłówek 1]** (~300 słów)
- [punkt 1]
- [punkt 2]
- [punkt 3]

  **H3: [Podnagłówek]** (jeśli potrzebny)

**H2: [Nagłówek 2]** (~300 słów)
...

**H2: Podsumowanie / Wnioski** (~150 słów)
- 3-5 bullet points z kluczowymi takeaways

**CTA (Call to Action):**
[Konkretny CTA pasujący do contentu — np. "Umów bezpłatną konsultację wdrożenia M365 Copilot" / "Pobierz checklistę" / "Zobacz kurs n8n"]
- Link docelowy: [URL na dokodu.it]

### Linki Wewnętrzne
| Anchor Text | URL na dokodu.it | Kontekst |
|-------------|-----------------|---------|
| [anchor] | [/url] | [gdzie umieścić] |

### Linki Zewnętrzne (autorytety)
- [Microsoft Learn / oficjalna doku / research]

### Multimedia
- [Screenshoty / GIF / tabela / checklist — co warto dodać]

### Uwagi dla Autora
- [specyficzne wskazówki, tone of voice, czego unikać]

---

## KROK 4: Dodaj do Ideas Bank

Uruchom:
```bash
python3 /home/kacper/DOKODU_BRAIN/scripts/seo_ideas.py add "[SEO Title]" \
  --keyword "[główna fraza]" \
  --slug "[slug]" \
  --intent [informational/commercial] \
  --pillar "[pillar]" \
  --priority [high/medium/low] \
  --source seo-plan-post \
  --status BRIEF
```

Podaj komendę użytkownikowi do skopiowania i uruchomienia.

## KROK 4b: Zaktualizuj Link Graph

Po wygenerowaniu briefu dodaj nowy artykuł do grafu linków (status: brief):
```bash
python3 /home/kacper/DOKODU_BRAIN/scripts/link_graph.py --add-article \
  --slug "[slug]" \
  --title "[SEO Title]" \
  --keyword "[główna fraza]" \
  --pillar "[pillar]" \
  --url "/blog/[slug]" \
  --status brief
```

Dla każdego sugerowanego linku wewnętrznego z Kroku 1b — dodaj go do grafu:
```bash
python3 /home/kacper/DOKODU_BRAIN/scripts/link_graph.py --add-link \
  --from-slug "[slug-nowego]" \
  --to-slug "[slug-istniejacego]" \
  --anchor "[tekst anchor]"
```

## KROK 5: Zaproponuj następny krok

- "Czy mam teraz napisać draft artykułu na podstawie tego briefu?"
- "Czy chcesz zaktualizować meta title/slug po napisaniu?"

## ZASADY BRIEFU

- SEO Title: zawiera główną frazę kluczową blisko początku, max 60 znaków
- Slug: tylko małe litery, myślniki zamiast spacji, bez polskich znaków, max 6 słów
- Meta description: ZAWSZE z CTA, między 120-155 znaków
- H2: powinny zawierać frazy poboczne lub pytania z People Also Ask
- Linki wewnętrzne: minimum 2-3, zawsze do istniejących stron na dokodu.it
- CTA: dopasowany do funnel stage (informational → lead magnet lub kurs; commercial → konsultacja/usługa)
- Nie używaj fraz potocznych — ton ekspercki ale przystępny
