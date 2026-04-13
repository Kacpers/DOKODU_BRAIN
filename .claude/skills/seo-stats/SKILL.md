---
name: seo-stats
description: Analizuje dane z Google Search Console i wyciąga actionable insights SEO dla dokodu.it. Identyfikuje quick wins, content gaps, frazy z niskim CTR i strony do optymalizacji. Zapisuje wnioski do SEO_Insights.md. Trigger: "zanalizuj seo", "insighty z gsc", "co działa na blogu", "stats seo", "okazje seo", /seo-stats
---

# Instrukcja: SEO Stats & Insights

## Działanie

Pobiera ostatnie dane GSC z bazy lokalnej i przeprowadza głęboką analizę pod kątem okazji content marketingowych dla dokodu.it.

## KROK 1: Pobierz dane

```bash
cd /home/kacper/DOKODU_BRAIN/scripts && python3 gsc_fetch.py --from-db --mode opportunities
```

Jeśli baza jest pusta (błąd "Baza jest pusta") → uruchom najpierw `/seo-sync` i wróć.

Wczytaj też plik z ostatnim synciem:
`DOKODU_BRAIN/20_AREAS/AREA_Blog_SEO/SEO_Last_Sync.md`

## KROK 2: Analiza — 5 obszarów

Przeprowadź analizę i zaraportuj każdy z tych obszarów:

### 2A. Quick Wins (pozycje 4-15, wysokie impressions)
- Lista top 10 fraz które są "prawie" w top 3
- Dla każdej: jaka strona je przyciąga? co można poprawić (tytuł H1, treść, linki)?
- Priorytetyzuj te z najwyższymi impressions i kliknięciami

### 2B. Niski CTR przy dobrej pozycji (top 10, CTR < 3%)
- Te frazy Google pokazuje, ale nikt nie klika
- Problem prawdopodobnie: słaby meta title lub meta description
- Dla każdej podaj konkretną propozycję nowego tytułu/opisu

### 2C. Content Gaps (impressions bez kliknięć)
- Strony widoczne w Google ale bez ruchu → złe intencje lub zbyt słabe
- Zidentyfikuj czy to problem treści czy technikaliów (kanibalizacja, thin content)

### 2D. Top Performers — co warto rozbudować
- Top 5 stron z największym ruchem
- Dla każdej: czy są powiązane satelity? czy warto dodać CTA na usługi Dokodu?

### 2E. Nowe Tematy — frazy bez dedykowanej strony
- Zapytania z kliknięciami ale niską pozycją → brak dobrej strony docelowej
- To są pomysły na NOWE posty/pillar pages

## KROK 3: Wygeneruj Quick Wins Actions

Zbuduj listę max 5 konkretnych akcji, np.:
1. "Post /automatyzacja-maili ma pozycję 7 dla frazy X → dodaj sekcję o Y, podmień H1"
2. "Fraza 'n8n tutorial pl' — 500 impressions, brak strony — napisz post"

## KROK 4: Zaproponuj pomysły do Ideas Bank

Dla każdego zidentyfikowanego content gap zaproponuj dodanie pomysłu:
```bash
python3 /home/kacper/DOKODU_BRAIN/scripts/seo_ideas.py add "[tytuł]" \
  --keyword "[fraza]" --pillar "[pillar]" --priority high --source gsc-sync
```

Podaj gotowe komendy do skopiowania — nie uruchamiaj ich sam.

## KROK 5: Zapisz wnioski do SEO_Insights.md

Dopisz nowy wpis na początku pliku `DOKODU_BRAIN/20_AREAS/AREA_Blog_SEO/SEO_Insights.md`:

Format wpisu:
```markdown
## Insights — [data]

**Okres danych:** [start] → [end]

### Quick Wins
- [fraza] (poz. X, Y impressions) → [akcja]

### Content Gaps
- [fraza] → napisać: [tytuł posta]

### Zmiany w porównaniu do poprzedniego okresu
- [obserwacja]

---
```

## ZASADY

- Zawsze myśl z perspektywy ICP Dokodu: firmy 50-500 pracowników, problemy z AI/automatyzacja
- Priorytetyzuj frazy commercial intent (wdrożenie, cena, jak wybrać) nad strictly informational
- Nie sugeruj fraz z <10 impressions — za mały sygnał
- Jeśli dane są sprzed >14 dni — zasugeruj `/seo-sync` dla świeższych danych
