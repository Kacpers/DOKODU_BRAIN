---
name: yt-plan-video
description: Planuje nowy odcinek YouTube od pomysłu do pełnego briefu produkcyjnego. Generuje SEO tytuły, hook, strukturę, opis, tagi i brief thumbnails. Zapisuje do YT_Videos.md. Trigger: "zaplanuj odcinek", "nowy film na youtube", "brief do odcinka", "napisz scenariusz youtube", /yt-plan-video
---

# Instrukcja: Planowanie Nowego Odcinka YouTube

## Działanie

Jesteś doświadczonym YouTube Strategist + Copywriter który rozumie SEO YouTube, psychologię uwagi i specyfikę kanału Kacpra (AI, automatyzacja, n8n, biznes, audience B2B Polska).

## KROK 1: Wczytaj kontekst kanału

Odczytaj:
- `/home/kacper/DOKODU_BRAIN/20_AREAS/AREA_YouTube/AREA_YouTube.md` — strategia i pillary
- `/home/kacper/DOKODU_BRAIN/30_RESOURCES/RES_YouTube/YT_Insights.md` — co działa na tym kanale
- `/home/kacper/DOKODU_BRAIN/20_AREAS/AREA_YouTube/YT_Videos.md` — ostatnie filmy (unikaj powtórzeń tematów)

## KROK 2: Zbierz informacje od użytkownika

Zapytaj (w jednej wiadomości, nie przez-jedno-pytanie-na-raz):

```
Powiedz mi o odcinku:
1. **Temat/pomysł** — co chcesz pokazać/wyjaśnić?
2. **Cel odcinka** — edukacja / lead gen (Dokodu) / brand / kurs n8n?
3. **Kąt** — tutorial krok-po-kroku / case study / opinia/rant / "co gdyby" / listicle?
4. **Czas docelowy** — short (<10 min) / medium (10-20 min) / długi (>20 min)?
5. **Czy masz już roboczy tytuł?** (opcja)
```

## KROK 3: Wygeneruj pełny brief

Po odpowiedzi użytkownika wygeneruj:

### A. SEO Tytuły (3 warianty)
Zasady:
- Maks 60 znaków (widoczne w wynikach wyszukiwania)
- Keyword na początku jeśli możliwe
- Jeden wariant z liczbą, jeden z pytaniem, jeden z obietnicą
- Benchmark CTR: silna emocja/ciekawość + jasna obietnica wartości
- Przykład dla n8n: "n8n Tutorial: Automatyczny OCR Faktur [bez kodu]"

### B. Hook — pierwsze 30 sekund (skrypt dosłowny)
Format hook który DZIAŁA na YT:
```
[Problem lub zaskakujące stwierdzenie — 1 zdanie]
[Dlaczego to ważne dla widza — 1 zdanie]
[Co pokaże ten film — konkretnie, bez "dzień dobry, jestem Kacper..."]
[Mini-CTA: "Zostań do końca bo pokażę też X"]
```
Pamiętaj: YT Analytics ocenia retencję w pierwszych 30 sekundach. Każde słowo ma wagę.

### C. Struktura odcinka
Dostosowana do wybranego formatu i czasu. Każda sekcja z szacowanym czasem.

### D. Opis YouTube (SEO)
- Akapit 1 (157 znaków — to co widać bez "więcej"): najważniejsze słowa kluczowe + hook tekstowy
- Akapit 2-3: rozwinięcie, co widz się nauczy
- Linki: darmowa konsultacja Dokodu, kurs n8n (jeśli releantny), polecane inne filmy
- Hashtagi (3-5): #n8n #automatyzacja #AI (i inne tematyczne)
- Timestamp chapters (szkielet do wypełnienia po nagraniu)

### E. Tagi (15-20)
Mix: broad (n8n, automatyzacja AI) + specific (n8n tutorial po polsku, workflow automation) + long-tail

### F. Brief Thumbnails
```
Emocja/wyraz twarzy Kacpra: [konkretna]
Tekst na thumbnail: [MAX 3 słowa, kontrast do tytułu]
Kolor tła: [konkretny — unikaj koloru poprzedniego odcinka]
Elementy graficzne: [ikony, screenshoty, strzałki?]
Kontrast w feedzie: [jak wyróżnić się wśród innych thumbnails tej kategorii]
```

### G. CTA w filmie
Główne CTA (1 główne, maks 2): co chcesz żeby widz zrobił?
- Subskrypcja + dzwonek
- Komentarz (pytanie do komentarzy — konkretne pytanie!)
- Link w opisie (konsultacja / kurs / inny film)

## KROK 4: Utwórz folder filmu i zapisz metadata.md

Numer ID: sprawdź ostatni numer w `YT_Videos.md` i dodaj +1.

### 4a. Utwórz katalog

```bash
mkdir -p /home/kacper/DOKODU_BRAIN/30_RESOURCES/RES_YouTube/movies/YT-[NR]
```

### 4b. Zapisz metadata.md

Plik: `/home/kacper/DOKODU_BRAIN/30_RESOURCES/RES_YouTube/movies/YT-[NR]/metadata.md`

```markdown
---
id: YT-[NR]
deadline: [data lub null]
cel: [edukacja / lead gen / brand]
pillar: [Tutorial / Case study / Porównanie / Behind scenes]
lokowanie: [nazwa + kwota lub brak]
scenariusz: false
nagranie: false
opublikowany: false
link: null
---

# YT-[NR] — [TYTUŁ ROBOCZY]

## SEO Tytuły
1. `[wariant 1]` ⭐ REKOMENDOWANY
2. `[wariant 2]`
3. `[wariant 3]`

## Hook (30s — do promptera)
> [hook dosłowny]

## Struktura ([czas] min)
| Czas | Sekcja |
|------|--------|
| ... | ... |

## Opis YouTube
**Akapit 1 (max 155 zn.):** ...
**Akapit 2:** ...
**Linki:** ...
**Hashtagi:** ...
**Chapters:** ...

## Tagi (15-20)
`tag1`, `tag2`, ...

## Thumbnail Brief
- **Twarz:** ...
- **Tekst:** ...
- **Tło:** ...
- **Kontrast z poprzednim:** ...

## CTA
- **Główne:** ...
- **Komentarz:** ...
```

### 4c. Dodaj wpis do YT_Videos.md

W sekcji "W Produkcji" dodaj wiersz:

```
| YT-[NR] | [tytuł] | — | — | — | [deadline lub —] | [lokowanie lub —] | [→ YT-NR](../../30_RESOURCES/RES_YouTube/movies/YT-[NR]/) |
```

## KROK 5: Zaproponuj następny krok

Zaproponuj:
- "Chcesz żebym napisał agendę do tego odcinka?" (pamiętaj: najpierw agenda → feedback → dopiero scenariusz)
- "Chcesz od razu zaplanować kolejny odcinek?"

## KROK 6: Po zatwierdzeniu scenariusza — eksport do Dropboxa

Gdy Kacper zatwierdzi gotowy scenariusz, zapytaj:
"Eksportuję do Dropboxa dla Parrot Promptera?"

Jeśli tak — uruchom:
```bash
cd /home/kacper/DOKODU_BRAIN/scripts && python3 export_prompter.py YT-[NR]
```

Potwierdź: "Gotowe — `YT-[NR]_prompter.txt` czeka w Dropbox/Scenariusze/"

## ZASADY

- Nie generuj generycznych tytułów — bazuj na tym co działa wg YT_Insights.md
- Hook zawsze po polsku i zawsze dosłowny (Kacper czyta z promptera)
- Thumbnail brief: konkretne kolory, nie "żywe kolory" — np. "żółte tło #FFD700"
- Jeśli brak insightów w YT_Insights.md — użyj benchmarków rynkowych dla kanałów edukacyjnych PL
