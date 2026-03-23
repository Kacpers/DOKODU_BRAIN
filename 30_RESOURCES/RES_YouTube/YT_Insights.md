---
type: resource
status: active
owner: kacper
last_reviewed: 2026-03-11
tags: [youtube, insights, analytics, wnioski]
---

# YT Insights — Baza Wiedzy o Kanale

Kumulatywna baza wniosków z analiz. Każda analiza `/yt-stats` dopisuje nowy wpis.
Im więcej wpisów, tym lepiej AI rozumie Twój kanał i może dawać celniejsze rekomendacje.

---

## Wzorce Tytułów (co działa)

- **Odwrócone oczekiwanie** — "nie kłamie", "zmienia wszystko", "nikt tego nie używa" → top 3 filmy kanału
- **Emocjonalny hook przed tematem** — "Własne AI, które nie kłamie? Zbuduj RAG" lepiej niż "Tutorial: RAG w n8n"
- **Pytania retoryczne** — "Dlaczego ChatGPT daje słabe odpowiedzi?" działa (1.9K na relatywnie nowym filmie)

---

## Wzorce Thumbnails

> Brak danych CTR z API — uzupełnij ręcznie po sprawdzeniu YouTube Studio.

---

## Wzorce Treści (co trzyma widza)

- **Format 14-16 min na lokalnym AI** → najwyższy engagement absolutny (7K wyśw., 250 likes, 26-27% retencji)
- **Shorty z bardzo konkretnym tipsem** → retencja 95% (0:41 film trzyma prawie do końca) — dobra jakość sygnału
- **n8n + konkretna funkcja** → dobra retencja procentowa (31% przy 27 min to solidny wynik)
- **Długość optimum: 14-20 min** — 29-30 min obniża zasięg na wejściu mimo dobrej retencji

---

## Co NIE Działa

- **Shorty viralne algorytmiczne** — 119K wyśw. przy avg 0:09 i like rate 0.07% = zero wartości biznesowej
- **Bardzo długie formaty (29-30 min)** — tracą zasięg mimo dobrej retencji procentowej
- **Przypadkowe nagrania** ("Odpowiedź głosowa", prywatne) — usunąć, szkodzą metrykom kanału

---

## Archiwum Analiz

---

### Analiza — 2026-03-11

**Okres:** 2026-02-11 → 2026-03-11 | Filmy: ostatnie 30

**Top 3 filmy (wyświetlenia + engagement):**
1. "Własne AI, które nie kłamie? Zbuduj system RAG" — 7.1K wyśw. | avg 3:55 (26% ret.) | 252 likes | like rate 3.5%
2. "Claude Code zmienia wszystko - n8n już nie będzie..." — 6.9K wyśw. | avg 3:55 (27% ret.) | 207 likes | like rate 3.0%
3. "Dlaczego nikt tego nie używa?! Python + MCP" — 2.5K wyśw. | avg 3:33 | 59 likes

**Bottom / problematyczne:**
1. 5x "Odpowiedź głosowa" — 0 wyśw., 0 likes → USUNĄĆ
2. "Julian Sieradzinski" — 7 wyśw. → USUNĄĆ
3. "Twoje dane nigdy nie opuszczą tego PC" (19:55) — tylko 758 wyśw. mimo dobrego tematu

**Kluczowe metryki:**
- Watch time: 1,607 godz. / 28 dni
- Net subskrybenci: +300 (27.3K total)
- Wyświetlenia/sub/miesiąc: **0.79** — poniżej normy (zdrowy kanał: 2-4x)

**Insighty:**
1. Long-form 14-16 min na lokalnym AI (RAG, Claude) = core kanału — replicate każdy tydzień
2. Emotionally charged tytuły z odwróconym oczekiwaniem → top 3 filmy mają je wszystkie
3. Algorytmiczne shorty (119K, 106K wyśw.) = fałszywe metryki, avg dur 0:09, like rate 0.07%

**Rekomendacje:**
- [ ] Usuń 6 przypadkowych filmów z YouTube Studio (Odpowiedź głosowa + Julian)
- [ ] Następny film: replikuj formułę RAG/Claude — 14-16 min, tytuł z napięciem
- [ ] Ogranicz długość do maks. 20 min — 29-30 min traci zasięg na wejściu

**Pytanie do przemyślenia:**
27.3K subs, 21.4K wyśw./miesiąc = <1 wyśw./sub. Czy Twoi subskrybenci to realni fani czy "martwe dusze" z algorytmicznych shortów z października? Jeśli drugie — jaką masz strategię na reaktywację?
