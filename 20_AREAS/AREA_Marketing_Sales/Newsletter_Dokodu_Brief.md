---
type: resource
status: active
owner: kacper
last_reviewed: 2026-03-06
tags: [newsletter, email-marketing, lista, content]
related: [[Content_Calendar]], [[100_MARKETING_ADS]]
---

# NEWSLETTER "DOKODU BRIEF" — Strategia i Szablony
> Cel: Lista wlasna jako najcenniejszy aktyw marketingowy. Newsletter = relacja z czytelnikiem, nie spam.
> Rytm: co tydzien, piatek 10:00
> Platform: MailerLite (lub EmailOctopus — sprawdzic cennik dla >1000 subskrybentow)

---

## POZYCJONOWANIE NEWSLETTERA

**Nazwa:** Dokodu Brief
**Podtytul:** "5 minut o AI dla Twojej firmy — co warto wiedziec w tym tygodniu"
**Dla kogo:** Managerowie i CEO ktory chca byc na biezaco z AI, ale nie maja czasu sledzic wszystkiego
**Ton:** Konkretny, bez bullshit, z odrobina humoru. Jak email od znajomego-eksperta, nie od korporacji.
**Format:** 4 sekcje, max 500 slow, czyta sie w 5 minut

---

## FORMAT (szablon tygodniowy)

```
Temat: [KONKRETNY HOOK — nie "Newsletter #X"] | Dokodu Brief

---

Czesc [Imie] (personalizacja w MailerLite),

[INTRO — 2 zdania, co dzisiaj]

---

🔧 NARZEDZIE TYGODNIA

[Nazwa narzedzia]
[1 zdanie: co to jest]
[2-3 zdania: dlaczego warto, dla kogo, konkretny use case]
[Link]

---

⚖️ UPDATE PRAWNY

[Temat: AI Act / RODO / cokolwiek aktualnego]
[3-4 zdania: co sie stalo, co to oznacza dla firmy, co zrobic]
[Jezeli nic nowego → maly tip lub przypomnienie o nadchodzacym deadlinie]

---

⚡ TIP Z N8N / AUTOMATYZACJI

[Jeden konkretny tip — screenshot, przyklad, mini tutorial]
[Cel: zeby czytelnik mogl cos wdrozyc w 30 minut]

---

💬 MOJA OPINIA

[1 akapit — osobista obserwacja z tygodnia, kontrowersyjna teza, cos co mnie zaskoczylo]
[Bez bullshit, bez cudzych mysli — to musi byc moja perspektywa]

---

Do nastepnego tygodnia,
Kacper

P.S. [Jedno zdanie — CTA, ciekawostka, albo pytanie do czytelnika]

---
[Stopka: link do wypisania, adres firmy, link do archiwum]
```

---

## PRZYKLADOWE WYDANIA (do weryfikacji)

### Wydanie #001 — Launch (planowany marzec 2026)

**Temat emaila:** "AI Act za 5 miesięcy — czy Twoja firma jest gotowa?"

**Intro:**
Dzisiaj startuję z Dokodu Brief — tygodniowe 5 minut które (mam nadzieję) bedzie warte Twojego czasu. Bez spamu, bez "transformacji cyfrowej", bez ogolnikow. Tylko konkret.

**Narzedzie tygodnia: n8n 1.78 — AI Agent node**
n8n wypuscilo nowy node AI Agent (beta). Pozwala zbudowac agenta ktory samodzielnie korzysta z narzedzi (przeszukuje dokumenty, wysyla maile, sprawdza ERP) — bez kodowania. Testowałem przez tydzien — pierwsze wrażenia: obiecujace dla prostych agentow, jeszcze nie dla skomplikowanych procesow. Polecam przetestowac jesli masz juz n8n.

**Update prawny: AI Act — 5 miesięcy do pelnego stosowania**
2 sierpnia 2026 — pelne stosowanie AI Act dla systemow wysokiego ryzyka. Jezeli Twoja firma uzywa AI w HR (screening CV, ocena pracownikow) lub infrastrukturze — masz 5 miesiecy na dostosowanie sie. Kara za niezgodnosc: do 15 mln EUR lub 3% globalnego obrotu. Nie straszę — ale warto sprawdzic, co macie. [Link do checklisty AI Act — lead magnet]

**Tip z n8n: Jak zapobiec duplikatom w workflowie**
Dodaj node "Check Duplicate" z MD5 hash dokumentu przed przetwarzaniem. Jezeli hash juz istnieje w Airtable/bazie — pomiń. Uratowalo mnie to od podwojnych faktur w ERP klienta. [Kod do przeklejenia]

**Moja opinia:**
Widzę coraz wiecej firm ktore "wdrozenie AI" rozumieja jako wklejenie ChatGPT do Teams. To nie jest wdrozenie — to eksperyment bez infrastruktury, bez compliance, bez mierzenia efektow. Technologia nie jest problemem. Problem to brak procesu wokol niej. Na tym skupiamy sie w Dokodu.

---

## SEKWENCJA POWITALNA (7 emaili — onboarding nowych subskrybentow)

### Email 1 (natychmiast po zapisie): Powitanie + obiecany lead magnet
```
Temat: Twoja AI Act Checklist jest gotowa (+ kilka slow ode mnie)

Czesc [Imie],

Dzieki za zapis na Dokodu Brief.

Tutaj Twoja checklist: [LINK]

Kim jestesmy? Krotko: agencja ktora laczy wdrozenia AI z compliance prawnym.
Robimy to czego wiekszosc agencji nie robi — sprawdzamy nie tylko czy technologia dziala,
ale czy jest zgodna z prawem. CEO + Kacper (tech), COO + Alina (legal).

Co tydzien, w piatek, dostaniesz od nas krotki brief o AI dla Twojej firmy.

Jezeli masz konkretny problem do omowienia — po prostu odpisz na ten email.
Czytam kazda wiadomosc.

Kacper
```

### Email 2 (dzien 2): Historia Dokodu
```
Temat: Dlaczego zalozylismy Dokodu (i co nas zaskoczylo)

[Historia — dlaczego nie ma sensu wdrazac AI bez compliance, co nas nauczyli pierwsi klienci]
```

### Email 3 (dzien 4): Case study (anonimizowane)
```
Temat: Co sie stalo gdy firma logistyczna sprobowala "zautomatyzowac" dokumenty sama

[Historia Corleonis-like — bledy, lekcje, wyniki]
```

### Email 4 (dzien 7): Najczestszy blad
```
Temat: Blad ktory widzę u 80% firm wdrazajacych AI

[Konretny, bolesny insight + rozwiazanie + CTA do diagnozy]
```

### Email 5 (dzien 10): Edukacja (AI Act)
```
Temat: 3 rzeczy o AI Act ktore Twoj prawnik pewnie jeszcze nie wie

[Konkretna, uzyteczna wiedza o AI Act dla nie-prawnikow]
```

### Email 6 (dzien 14): Narzedzie
```
Temat: Najuzyteczniejszy workflow n8n jaki zbudowalem w tym kwartale

[Konkretny blueprint — co robi, dla kogo, jak zrobic]
```

### Email 7 (dzien 21): Miekki pitch
```
Temat: Kiedy bedziesz gotowy — oto jak zaczynamy

[Opis procesu wspolpracy z Dokodu + CTA do bezplatnej diagnozy]
[Bez presji, z poszanowaniem ze moga jeszcze nie byc gotowi]
```

---

## METRYKI (cel i monitoring)

| Metryka | Cel | Aktualnie |
| :--- | ---: | ---: |
| Liczba subskrybentow | 300 (Q2) / 1000 (Q4) | ___ |
| Open Rate | >35% | ___% |
| Click Rate | >5% | ___% |
| Wskaznik wypisow | <1%/mies. | ___% |
| Leady z newslettera (mies.) | 2 | ___ |

**Benchmark branżowy:** Open Rate B2B tech: 28-35%. Jesli jestesmy powyzej 35% — tresci sa wartosciowe. Ponizej 25% — audyt tematow i linii tematow.

---

## WZROST LISTY (jak zdobywac subskrybentow)

1. **Lead magnety** — "AI Act Checklist" + "Kalkulator ROI" = bramka emailowa
2. **LinkedIn CTA** — kazdy post z linkiem do zapisu ("Daje co tydzien konkretny tip, link w bio")
3. **Webinary** — obowiazkowy zapis na liste przy rejestracji na webinar
4. **Klienci** — po kazdym projekcie: "Czy moge dodac Cie do naszego tygodniowego briefu?"
5. **Stopka emaila** — link do zapisu w kazdym wyslanym emailu Kacpra i Aliny
