---
name: yt-research
description: Bada temat na YouTube — szuka popularnych filmów, analizuje wzorce tytułów, kanały, długości, identyfikuje luki i rekomenduje kąty dla Kacpra. Łączy wyniki z danymi kanału i competitive intel. Trigger: "zbadaj temat", "zrób research", "co jest na yt o", "jakie filmy są o", /yt-research
---

# Instrukcja: YouTube Topic Research

## Działanie

Pełny research tematu: co już istnieje na YT, co działa, czego brakuje, jaki kąt wybrać dla kanału Kacpra.

## KROK 1: Uruchom research

Zapytaj użytkownika o temat jeśli nie podał. Następnie:

```bash
cd /home/kacper/DOKODU_BRAIN/scripts && python3 youtube_research.py "[TEMAT]" --max 20 --save 2>/dev/null
```

Dla polskiego contentu dodaj `--lang pl`, dla przeglądu globalnego zostaw bez flagi.

Jeśli temat ma polski i angielski wymiar (np. "Claude Code") — uruchom OBA:
```bash
python3 youtube_research.py "[TEMAT]" --lang pl --max 10 --save 2>/dev/null
python3 youtube_research.py "[TEMAT]" --lang en --max 10 --save 2>/dev/null
```

## KROK 2: Wczytaj kontekst kanału

Odczytaj:
- `/home/kacper/DOKODU_BRAIN/30_RESOURCES/RES_YouTube/YT_Insights.md` — co działa NA TYM kanale
- `/home/kacper/DOKODU_BRAIN/20_AREAS/AREA_YouTube/AREA_YouTube.md` — pillary i ICP

## KROK 3: Analiza — 5 pytań

**1. Saturacja rynku**
- Ile filmów istnieje na ten temat? Jaka jest średnia wyświetleń?
- Czy temat jest zdominowany przez wielkich graczy (Fireship, Anthropic, NetworkChuck)?
- Czy PL rynek jest nasycony, czy to wciąż "blue ocean"?

**2. Luki tematyczne**
- Jakich kątów/podtematów NIE ma w top wynikach?
- Co jest pokryte słabo (mało filmów lub niskie wyśw.)?
- Co robi Kacper wyjątkowo dobrze, czego nie ma w wynikach? (np. n8n + Claude Code, B2B Polska, RODO)

**3. Wzorce które działają**
- Który format wybija: shorts vs long-form?
- Które tytuły mają najlepszy stosunek wyświetleń do daty publikacji?
- Jaki hook/framing pojawia się w top filmach?

**4. Kąt dla Kacpra**
- Co on może zrobić INACZEJ lub LEPIEJ niż istniejące filmy?
- Jak dopasować temat do jego ICP (polskie firmy B2B, automatyzacja)?
- Czy pasuje do pillaru: Tutorial n8n / Local AI / Automatyzacja B2B / AI Act?

**5. Timing**
- Czy temat jest evergreen czy trending?
- Ile ma lat najstarszy film w wynikach? Czy to wciąż aktualne?
- Czy warto nagrywać teraz, czy lepiej poczekać na rozwój tematu?

## KROK 4: Wygeneruj raport analizy

```
### Research: "[TEMAT]" — [DATA]

**SATURACJA RYNKU:**
- Globalna: [wysoka/średnia/niska] — [uzasadnienie]
- PL: [wysoka/średnia/niska / brak danych]

**TOP 3 ISTNIEJĄCE FILMY (warte obejrzenia przed nagraniem):**
1. "[tytuł]" — [kanał] — [Xk wyśw.] — [co robią dobrze]
2.
3.

**LUKI — czego NIE MA na rynku:**
1. [Konkretna luka z uzasadnieniem]
2.
3.

**REKOMENDOWANY KĄT DLA KACPRA:**
[Jeden konkretny kąt który: (a) nie jest zajęty, (b) pasuje do jego expertise, (c) trafi w ICP]

**3 PROPOZYCJE TYTUŁÓW:**
1. [Tytuł z napięciem/odwróceniem — jak top filmy Kacpra]
2. [Tytuł z liczbą lub pytaniem]
3. [Tytuł evergreen/tutorial]

**FORMAT:**
- Długość: [X-Y min] — [uzasadnienie z danych]
- Short czy long-form? [rekomendacja]

**OCENA OPŁACALNOŚCI:**
🟢 Nagraj teraz / 🟡 Rozważ / 🔴 Pomiń — [1-2 zdania dlaczego]
```

## KROK 5: Zaproponuj następny krok

- "Chcesz żebym przeszedł od razu do `/yt-plan-video` z tym kątem?"
- "Chcesz zbadać pokrewny temat? (np. osobno 'Gemini CLI tutorial' i 'Claude Code tutorial')"

## ZASADY

- Nie rekomenduj tematu jeśli top 3 filmy mają >500K wyśw. i są nowsze niż 3 miesiące — rynek nasycony
- Zawsze sprawdź czy PL rynek jest nasycony oddzielnie od globalnego
- Kąt B2B Polska jest zawsze luką — globalny content rzadko trafia w realia polskich firm
- Jeśli temat ma <5 filmów w wynikach — albo bardzo niszowy, albo świetna okazja (oceń kontekstem)
- Raporty zapisuj do `30_RESOURCES/RES_YouTube/YT_Research_[slug].md`
