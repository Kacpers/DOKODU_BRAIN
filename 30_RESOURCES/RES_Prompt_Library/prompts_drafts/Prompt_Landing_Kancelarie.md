---
type: prompt_draft
purpose: Generowanie copy na landing page /dla-firm/kancelarie/ dla dokodu.it
status: draft
created: 2026-04-17
target_llm: Claude Sonnet/Opus 4.x lub GPT-5 lub Gemini 2.5 Pro
---

# Prompt: Landing Page dla Kancelarii Prawnych — dokodu.it

> Wklej poniższy tekst (wszystko pomiędzy `==PROMPT START==` a `==PROMPT END==`) jako pojedynczy prompt do Claude/ChatGPT/Gemini. Output — gotowy markdown copy do wklejenia w Next.js page.

---

==PROMPT START==

# Rola

Jesteś senior copywriterem B2B specjalizującym się w technologii dla branży prawniczej. Piszesz w języku polskim, dla kancelarii prawnych w Polsce. Nie piszesz jak marketer ani jak copywriter-generalista. Piszesz jak praktyk, który sam wdrażał AI w firmach i rozumie różnicę między teorią a codzienną pracą kancelarii.

# Zadanie

Napisz kompletne copy landing page'a **dokodu.it/dla-firm/kancelarie/** — dedykowanej strony dla kancelarii prawnych poszukujących wdrożenia AI i automatyzacji. Output w markdown, gotowy do wklejenia w komponenty Next.js/React.

# Kontekst — firma Dokodu

**Dokodu** to polska agencja AI z Gdyni, specjalizująca się w integracji AI w firmach 50–500 pracowników. Pozycjonujemy się jako **"Enterprise AI Integration Boutique"** z warstwą prawną zintegrowaną od dnia pierwszego.

**Dwójka założycieli jest kluczowa dla tego landing:**

1. **Kacper Sieradziński** — CEO, programista i praktyk wdrożeń AI. Wdrażał rozwiązania AI dla firm produkcyjnych, logistycznych, agencji. Buduje systemy w n8n, Python, LLM-API.

2. **Alina Sieradzińska** — COO, **radca prawny z certyfikatem ISO 42001 (Lead Auditor AI Management Systems)**, IT/AI Legal Expert. Specjalizuje się w AI Act, RODO w IT, prawie własności intelektualnej przy AI, compliance AI w firmach.

To duet **Tech + Legal** — różnicuje Dokodu od typowych agencji AI (które nie rozumieją prawa) i typowych kancelarii (które nie rozumieją technologii).

# Filozofia Dokodu (to MUSI być w landing)

- **Human in the Loop** — człowiek zatwierdza kluczowe akcje, AI wspiera, nie zastępuje. To fundament bezpieczeństwa — szczególnie krytyczny dla zawodów zaufania publicznego jak prawo.
- **AI Act ready od dnia pierwszego** — każde wdrożenie projektowane z uwzględnieniem AI Act (Rozp. UE 2024/1689), który w pełni wchodzi w życie 2 sierpnia 2026 dla systemów wysokiego ryzyka.
- **Tajemnica zawodowa i RODO jako ramy, nie jako ograniczenia** — wdrożenia projektowane tak, żeby dane klientów kancelarii nie wychodziły do publicznych LLM (ChatGPT, Gemini) bez kontroli.
- **Zero-Trust AI** — zakładamy, że model może się pomylić. Projektujemy proces z punktami kontrolnymi.

# Target odbiorcy (persona)

**Decydent:** partner zarządzający kancelarii prawnej 5–50 prawników, 45–60 lat, świadomy że "coś trzeba zrobić z AI", ale:
- boi się ryzyka prawnego (tajemnica zawodowa, RODO, AI Act)
- widział złe wdrożenia AI u znajomych
- nie wierzy agencjom IT bo "nie rozumieją prawa"
- ma zespół prawników którzy w 70% spędzają czas na **powtarzalnych zadaniach** (kwerenda, pisma standardowe, review umów, odpowiedzi klientom)
- nie ma czasu na naukę nowych narzędzi

Ten decydent **szanuje konkret, nie hype**. Jeden fałszywy ruch ("rewolucja", "AI zmieni prawo") — zamyka zakładkę.

# Realne pain points branży prawniczej w Polsce (użyj w copy)

1. **Kwerenda orzeczeń i doktryny** — prawnicy spędzają 8–15h/tydzień na wyszukiwaniu w LEX, Lexis, systemie informacji prawnej. 60–70% tej pracy to powtarzalne wzorce.
2. **Pisma standardowe** — pozwy, odpowiedzi na pozwy, wezwania do zapłaty, pełnomocnictwa. Pisane ręcznie od zera, mimo że 80% struktury się powtarza.
3. **Review umów** — analiza umów handlowych, najmu, NDA. Powtarzalne klauzule i ryzyka, które doświadczony prawnik widzi od razu — ale młodszy musi przeczytać każde słowo.
4. **Obsługa klienta** — maile "jaki jest status mojej sprawy?", wnioski o kopie dokumentów, fakturowanie. Zajmują 2–4h dziennie wspólnie w kancelarii.
5. **Compliance własnej kancelarii** — kancelaria sama musi spełniać RODO, AI Act (gdy korzysta z AI), zachować tajemnicę zawodową. A tu w 2026 wchodzi AI Act i większość kancelarii nie ma własnej polityki AI.
6. **Research tematyczny** — nowe orzecznictwo SN, ETPCz, TSUE w wybranym obszarze. Gdyby ktoś to codziennie śledził...

# Konkretne use cases do wykorzystania (wybierz 3–5 najmocniejszych)

- **Asystent do kwerendy orzeczeń** — pytasz "sprawy o mobbing w adm. publicznej, 2023–2025, oddalone", dostajesz listę z sygnaturami + streszczenia
- **Generator pism procesowych** — szablon + dane sprawy → draft pisma w 15 min zamiast 2h
- **Asystent do review umów** — czerwone flagi w umowie, klauzule abuzywne, niestandardowe ryzyka
- **Obsługa maili klientów** — asystent odpowiada na pytania o status, wysyła statusy, przygotowuje drafty
- **Compliance checklist dla kancelarii** — audyt wewnętrzny pod AI Act + RODO (we współpracy z Aliną)
- **Monitoring orzecznictwa** — co rano newsletter: "3 nowe wyroki SN w obszarze X"

Każdy use case pokazuj **operacyjnie** (ile czasu oszczędza, jak wygląda w praktyce) — nie marketingowo.

# Tone of Voice (KRYTYCZNE, przestrzegaj co do joty)

**Używaj słów:**
proces, ręczna robota, przeklejanie danych, koszt, czas, efekt, kontrola, system, wdrożenie, gotowy, działa, schemat, model, odciążyć, odzyskać czas, poukładać, uruchomić, u siebie

**NIGDY nie używaj:**
rewolucja, game changer, sekret, przełomowe rozwiązanie, niesamowite, genialne, petarda, sztos, kompleksowe podejście, metodologia 360, innowacyjna synergia, end-to-end enablement, "jedyny program w Polsce", "unikalny na rynku", "AI zmieni prawo", "era AI"

**O AI Act / RODO / bezpieczeństwie mów chłodno, rzeczowo, BEZ STRASZENIA.** Fakt: "AI Act wchodzi 2.08.2026 dla high-risk. Kancelaria używająca AI to podlega określonym wymogom. Pomagamy je spełnić." Nie: "AI Act może zrujnować Twoją kancelarię".

**Buduj autorytet przez:**
- Doświadczenie z praktyki (konkretne liczby z wdrożeń)
- Obserwacje operacyjne (czas, koszt, efekt)
- Pokazanie co testowałeś i dlaczego NIE zadziałało
- Spokojny, rzeczowy ton

**Składnia:**
- Zdania krótkie i średnie. Strona czynna.
- Jeden akapit = jedna funkcja
- Rytm jak naturalne mówienie do inteligentnej osoby
- Żadnych ozdobników. Jeśli zdanie nie pcha tekstu — wyrzuć.

# Forma do odbiorcy

Pisz w formie "**Państwo**" (nie Wy, nie Ty). To B2B, decydent to partner kancelarii. Zero korporacyjnego bełkotu, ale zero spoufalania się.

# Struktura outputu (wygeneruj dokładnie w tej kolejności)

## 1. Hero Section
- **H1** (max 10 słów) — mocna teza, problem+stawka albo obietnica efektu. NIE hype, NIE pytanie retoryczne.
- **Podnagłówek** (1–2 zdania, max 30 słów) — uszczegółowienie + co dokładnie robicie
- **Primary CTA:** "Umów konsultację z Aliną i Kacprem" (15 min, bez opłat)
- **Secondary CTA:** "Zobacz jak wygląda wdrożenie" (link do sekcji niżej)

## 2. Sekcja "Co Państwa kancelaria robi ręcznie każdego tygodnia"
Lista 4–5 konkretnych pain points z realnym czasem (np. "12h tygodniowo"). Każdy bullet = 1 zdanie obserwacji + 1 zdanie "co to kosztuje". Bez marketingu, tylko fakty operacyjne.

## 3. Sekcja "Jak wygląda kancelaria, która wdrożyła AI świadomie"
3–4 krótkie paragrafy. Obraz dnia pracy PO wdrożeniu. Konkret: "Prawnik otwiera mail, widzi 3 propozycje odpowiedzi, wybiera jedną, edytuje w 30 sekund, wysyła." NIE: "Kancelaria działa efektywniej dzięki AI."

## 4. Sekcja "Co konkretnie wdrażamy"
3–5 use case'ów z listy wyżej. Każdy ze strukturą:
- **Nazwa** (konkretna, np. "Asystent do kwerendy orzeczeń")
- **Problem** (1 zdanie)
- **Jak działa** (2–3 zdania operacyjnie — NIE "wykorzystuje zaawansowane AI", ale "wtyczka do LEX + model LLM na Państwa bazie pism")
- **Efekt** (konkret — "z 8h na 1,5h tygodniowo per prawnik")

## 5. Sekcja "Dlaczego Dokodu, a nie agencja IT"
Krótkie paragrafy (bez bulletów). Wyjaśnij że:
- Alina jest radcą prawnym z ISO 42001 — rozumie tajemnicę zawodową i AI Act
- Kacper jest technologiem z realnymi wdrożeniami
- Większość agencji AI nie rozumie prawa, większość kancelarii nie rozumie technologii — Dokodu robi oba
- Wszystkie wdrożenia projektowane z Human in the Loop (człowiek kontroluje kluczowe akcje)
- Zero-Trust AI — zakładamy że model się pomyli, projekt chroni przed tym

## 6. Sekcja "AI Act dla kancelarii — krótko"
2–3 paragrafy faktograficzne:
- Co to AI Act (1 zdanie)
- Kiedy wchodzi (2 sierpnia 2026 high-risk, pełna implementacja do 2027)
- Co to oznacza dla kancelarii (używających AI + doradzających klientom ws. AI)
- Jak Państwu pomagamy (audyt, dokumentacja, polityka AI wewnętrzna)

Na końcu: "Przygotowaliśmy **AI Act Checklist dla polskich kancelarii** — [pobierz bezpłatnie]" (placeholder link).

## 7. Sekcja "Jak wygląda współpraca"
4 kroki:
1. **Konsultacja 15 min** (bezpłatna) — rozmowa z Aliną i Kacprem, mapa gdzie AI Państwu pomoże
2. **Audyt 1–2 dni** — analiza procesów w Państwa kancelarii, konkretne rekomendacje
3. **Wdrożenie** — zwykle 4–8 tygodni, zaczynamy od 1–2 procesów
4. **Utrzymanie + compliance** — aktualizacje, reakcja na zmiany w AI Act

## 8. FAQ
5–6 pytań + odpowiedzi 2–4 zdania. Proponowane pytania:
- "Czy dane naszych klientów trafią do ChatGPT?"
- "Ile to kosztuje?"
- "Ile trwa wdrożenie?"
- "Czy to zgodne z tajemnicą zawodową?"
- "Co jeśli AI się pomyli?"
- "Czy potrzebujemy własnego IT żeby to utrzymać?"

## 9. Finalne CTA
Mocne, krótkie. Zaproszenie do konsultacji. 2–3 zdania max.

# Ograniczenia i zasady

- **Długość łącznie:** 1200–1800 słów (nie dłużej — decydent nie przeczyta)
- **Żadnych emoji** (ton poważny, B2B)
- **Żadnych "od X do Y" cen w copy** — ceny dajemy w konsultacji, na stronie tylko CTA
- **Konkretne liczby** tam gdzie to możliwe (8h/tydzień, 30 min, 2 sierpnia 2026, ISO 42001)
- **Zero wzmianek o konkurencji po nazwie** (np. "lepsze niż Kancelaria X")
- **Output: czysty markdown** z nagłówkami `##`, `###`, bulletami gdzie pasuje, bez komentarzy poza treścią

# Dane wspierające (możesz wpleść gdzie naturalne, NIE na siłę)

- Stanford AI Index 2026: ponad 88% firm deklaruje wdrożenie AI, ale **poniżej 5% ma AI działające w produkcji poza pilotami**. Rozdźwięk między "mówimy że używamy" a "faktycznie działa" jest ogromny.
- AI Act 2024/1689: pełna implementacja 2 sierpnia 2026 dla systemów wysokiego ryzyka. Kancelarie korzystające z AI dla klientów mogą podlegać szczególnym obowiązkom.
- Badanie BIS (Bank for International Settlements, 2025): firmy, które inwestują 1% budżetu operacyjnego w szkolenia AI, osiągają 5,9 pkt proc. wyższą produktywność niż te, które wdrażają AI bez szkoleń.

Użyj maksymalnie **1–2 z tych statystyk**, nie wszystkie. Żadnych "według badań", "eksperci twierdzą" — zawsze konkretne źródło.

# Format wyjścia

```markdown
# [H1]

**[Podnagłówek]**

[CTA block]

---

## Co Państwa kancelaria robi ręcznie każdego tygodnia

[treść]

---

## Jak wygląda kancelaria, która wdrożyła AI świadomie

[treść]

---

... (i tak dalej, każda sekcja oddzielona ---)
```

Nie dodawaj komentarzy typu "Oto gotowe copy:" ani "Mam nadzieję, że się podoba". **Od razu zacznij od `# [H1]` i skończ na ostatniej sekcji CTA.**

==PROMPT END==

---

## Instrukcja użycia

1. Otwórz Claude (claude.ai) lub ChatGPT albo Gemini
2. Skopiuj WSZYSTKO pomiędzy `==PROMPT START==` a `==PROMPT END==`
3. Wklej jako pojedynczą wiadomość
4. Output to gotowy markdown → skopiuj do `/src/app/dla-firm/kancelarie/page.tsx` i zamień na komponenty
5. Zanim wrzucisz na stronę: **Alina musi przeczytać i zatwierdzić** cały rozdział AI Act + FAQ — to jej obszar odpowiedzialności

## Iteracje (jeśli output słaby)

Jeśli output jest za marketingowy albo za ogólny — wróć do chata i napisz:
- "Przepisz sekcję 4 (Co konkretnie wdrażamy). Każdy use case ma być **bardziej operacyjny** — jak konkretnie prawnik używa tego w dniu pracy, nie jakie to AI."
- "Usuń wszystkie zdania które zaczynają się od 'Dzięki AI' albo 'W erze sztucznej inteligencji'."
- "Skróć całość o 30%. Za długie."

## Co zrobić PO wygenerowaniu

1. Alina review AI Act + tajemnica zawodowa sections
2. Przepisanie H1 ręcznie jeśli nie trafia (LLM czasem jest za ostrożny w nagłówkach)
3. Dodanie real case study — gdy LexLegali zamknie, wrzuć jako proof
4. SEO meta tags (title, description) — osobny prompt lub ręcznie
