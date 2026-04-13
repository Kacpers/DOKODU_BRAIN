---
name: yt-blueprint
description: Pełny pipeline od tematu do briefu produkcyjnego — research YouTube, analiza mocnych stron konkurencji, competitive synthesis i gotowy plan odcinka. Trigger: "zrób blueprint", "research i plan", "przygotuj film od A do Z", "pełny plan odcinka", /yt-blueprint
---

# Instrukcja: YouTube Blueprint — Od Researchu do Planu Produkcji

## Cel skilla

Zamiast planować film "na wyczucie" — najpierw zbadaj co już istnieje, zrozum DLACZEGO to działa, a dopiero potem zaplanuj film który to przebija. Jeden pipeline od tematu do gotowego briefu.

---

## KROK 1: Pobierz temat i wczytaj kontekst kanału

Jeśli użytkownik nie podał tematu — zapytaj w jednej wiadomości:
- **Temat odcinka** — o czym chcesz nagrać?
- **Cel** — edukacja / lead gen / brand?
- **Czy masz już roboczy tytuł lub kąt?** (opcja)

Wczytaj kontekst kanału:
- `/home/kacper/DOKODU_BRAIN/20_AREAS/AREA_YouTube/AREA_YouTube.md` — pillary, ICP
- `/home/kacper/DOKODU_BRAIN/30_RESOURCES/RES_YouTube/YT_Insights.md` — co działa NA TYM kanale
- `/home/kacper/DOKODU_BRAIN/20_AREAS/AREA_YouTube/YT_Videos.md` — ostatnie filmy (unikaj powtórzeń)

---

## KROK 2: Research YouTube — znajdź konkurencję

Uruchom research dla tematu. Jeśli temat ma wymiar PL i EN — uruchom oba:

```bash
cd /home/kacper/DOKODU_BRAIN/scripts && python3 youtube_research.py "[TEMAT]" --lang pl --max 10 --save 2>/dev/null
python3 youtube_research.py "[TEMAT]" --lang en --max 15 --save 2>/dev/null
```

Jeśli tylko globalny:
```bash
cd /home/kacper/DOKODU_BRAIN/scripts && python3 youtube_research.py "[TEMAT]" --max 20 --save 2>/dev/null
```

Wczytaj wygenerowany plik research z `30_RESOURCES/RES_YouTube/` jeśli nie masz wyników w output.

---

## KROK 3: Analiza top 5 filmów — mocne strony i luki

Wybierz **top 5 filmów** (wg wyświetleń, preferuj nowsze niż 12 miesięcy). Dla każdego wykonaj WebFetch strony YouTube żeby pobrać opis i dodatkowe dane:

```
https://www.youtube.com/watch?v=[VIDEO_ID]
```

Dla każdego z top 5 filmów wypełnij kartę analizy:

```
### Film [N]: "[TYTUŁ]" — [KANAŁ] — [Xk wyśw.]

**Formuła tytułu:**
[Jaka technika: odwrócone oczekiwanie / liczba / pytanie / obietnica / "quit" / "zmienia wszystko"?]
[Jakie słowa kluczowe na początku?]

**Format i engagement:**
- Długość: [X min] → [long-form / medium / short]
- Engagement rate: [likes/views %] → [wysoki >3% / średni / niski]
- Czy thumbnail wzmacnia tytuł, czy duplikuje?

**Hook / framing (z opisu lub tytułu):**
[Jaki problem/obietnica jest w pierwszym zdaniu opisu?]
[Jak widz wie "co z tego mam"?]

**Co robi dobrze (top 2-3 rzeczy):**
1.
2.
3.

**Czego NIE robi / luki:**
1. [Brak kąta B2B / brak PL / za dużo teorii / brak konkretnych liczb / etc.]
2.
```

---

## KROK 4: Competitive Intelligence Synthesis

Na podstawie analizy top 5 wygeneruj syntezę:

```
## Competitive Intelligence — "[TEMAT]"

### Rynek
- Saturacja globalna: [wysoka/średnia/niska] — [uzasadnienie]
- Saturacja PL: [wysoka/średnia/niska / blue ocean]
- Dominujące kanały: [lista z % udziałem wyświetleń]

### Wzorce które działają (zaadoptuj)
1. **[Nazwa wzorca]** — [co konkretnie robią + przykład z top filmów]
2. **[Nazwa wzorca]** — [...]
3. **[Nazwa wzorca]** — [...]

### Luki do zagospodarowania
1. **[Luka]** — żaden z top filmów nie robi X. Kacper może to zająć bo [uzasadnienie]
2. **[Luka]** — [...]
3. **[Luka]** — [...]

### Jak Kacper to przebija (jego przewagi)
1. **Kąt B2B Polska** — [jak konkretnie zastosować do tego tematu]
2. **n8n / automatyzacja praktyczna** — [co może pokazać czego inni nie pokażą]
3. **Autorytet eksperta** — [case studies, liczby, realne wdrożenia]

### Rekomendowany kąt dla Kacpra
[Jeden konkretny kąt: co, dla kogo, czym różny od konkurencji]

### Ocena opłacalności
🟢 Nagraj teraz / 🟡 Rozważ / 🔴 Pomiń — [uzasadnienie]
```

---

## KROK 5: Pełny Brief Produkcyjny

Na podstawie competitive intelligence wygeneruj pełny brief:

### A. SEO Tytuły (3 warianty)
- Maks 60 znaków
- Keyword na początku jeśli możliwe
- Wariant 1: z odwróconym oczekiwaniem / napięciem (formuła top filmów Kacpra)
- Wariant 2: z liczbą lub konkretną obietnicą
- Wariant 3: z pytaniem lub "dlaczego"
- Benchmark: bazuj na formułach które DZIAŁAJĄ w researchu + YT_Insights.md

### B. Hook — pierwsze 30 sekund (skrypt dosłowny)
```
[Zaskakujące stwierdzenie lub problem — 1 zdanie. Inspirowane mocnym hookiem z top filmów, ale lepsze]
[Dlaczego to ważne dla widza — realia polskiej firmy / B2B — 1 zdanie]
[Co konkretnie pokaże ten film — 1 zdanie, bez "dzień dobry, jestem Kacper"]
[Mini-CTA: "Zostań do końca bo pokażę też X" — X musi być zaskakujące]
```
Zasada: hook powinien być LEPSZY niż hook najlepszego konkurencyjnego filmu.

### C. Struktura odcinka
Każda sekcja z szacowanym czasem. Optymalnie 14-16 min (wg YT_Insights.md).
Zaznacz które sekcje odpowiadają na "luki" zidentyfikowane w competitive intel.

### D. Opis YouTube (SEO)
- Akapit 1 (157 znaków): najważniejsze słowa kluczowe + hook tekstowy
- Akapit 2-3: co widz się nauczy, czym różni się od innych filmów na ten temat
- Linki: bezpłatna konsultacja Dokodu, polecane filmy
- Hashtagi (3-5)
- Chapters (szkielet)

### E. Tagi (15-20)
Mix: broad + specific + long-tail. Bazuj na słowach kluczowych z researchu.

### F. Brief Thumbnail
```
Emocja/wyraz twarzy Kacpra: [konkretna — nie "zainteresowany", tylko "WTF" / "dumny" / "zaskoczony"]
Tekst na thumbnail: [MAX 3 słowa, kontrast do tytułu — nie powtarzaj tytułu]
Kolor tła: [konkretny hex — sprawdź poprzedni odcinek i użyj inny]
Elementy graficzne: [loga, screenshoty, VS, strzałki — konkretnie]
Kontrast w feedzie: [jak się wyróżnić względem thumbnails z researchu]
```

### G. CTA w filmie
- Główne CTA (jedno, konkretne — gdzie i co): moment w filmie + treść
- Pytanie do komentarzy (konkretne, prowokujące odpowiedź)

---

## KROK 6: Zapisz wyniki

### 6A. Research file
Zapisz competitive intel do:
`/home/kacper/DOKODU_BRAIN/30_RESOURCES/RES_YouTube/YT_Research_[slug-tematu].md`

Format pliku:
```markdown
# Research: "[TEMAT]"
Wygenerowano: [DATA] | Filmy: [N]

[Tabela top filmów z researchu]

[Analiza top 5 — karty z KROK 3]

[Competitive Intelligence Synthesis z KROK 4]
```

### 6B. Brief w YT_Videos.md
Dodaj nowy wpis w sekcji "W Produkcji":
`/home/kacper/DOKODU_BRAIN/20_AREAS/AREA_YouTube/YT_Videos.md`

```markdown
### YT-[NR] — [TYTUŁ ROBOCZY]
**Status:** SCENARIUSZ
**Deadline nagrania:** [tydzień od dziś]
**Cel:** [edukacja/lead gen/brand]
**Pillar:** [Tutorial n8n / Case study / AI Act / Behind scenes]
**Research:** [link do pliku research]

[Pełny brief z KROK 5]
```

Numer ID: sprawdź ostatni numer w YT_Videos.md i dodaj +1.

---

## KROK 7: Zaproponuj następny krok

Po wygenerowaniu briefu zaproponuj:
- "Chcesz żebym napisał pełny scenariusz do telepromptera?"
- "Chcesz zoptymalizować thumbnail brief bardziej szczegółowo?"
- "Chcesz zbadać pokrewny temat blueprintem?"

---

## ZASADY

- **Competitive first, plan second** — nie planuj niczego przed analizą top 5 filmów
- **Konkretne > ogólne** — każda rekomendacja musi mieć uzasadnienie w danych z researchu
- **Hook dosłowny i po polsku** — Kacper czyta z promptera, nie interpretuje
- **Thumbnail: konkretne kolory (hex), nie "żywe kolory"**
- **Długość 14-16 min** — wg YT_Insights.md to optimum dla tego kanału
- **Nie rekomenduj tematu 🟢 jeśli top 3 mają >500K wyśw. i są nowsze niż 3 miesiące** — chyba że Kacper ma wyraźną lukę
- **B2B Polska jest zawsze luką** — globalny content rzadko trafia w realia polskich firm 50-500 os.
- Jeśli research file dla tego tematu już istnieje w `RES_YouTube/` — wczytaj go zamiast uruchamiać ponownie
