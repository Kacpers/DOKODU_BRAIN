---
type: resource
status: active
owner: kacper
created: 2026-04-15
tags: [prezentacja, i-love-marketing, agenci-ai, marketing, n8n, competitive-intel]
source: planning board prezentacji na I Love Marketing (dane zewnętrzne, kontekst AI Hero / FOTC)
---

# Planning Board — Prezentacja "I Love Marketing" (Agenci AI)

> Notatki z planowania prezentacji na konferencję I Love Marketing.
> Prelegent: kontekst AI Hero. Pora: 13:50-14:30. Duża sala.
> Format: 3 live-built agentów w 4 różnych toolach (AgentSpace, Copilot Studio, n8n, ???)

---

## Struktura prezentacji

### Wstęp
- Otwieracz: silna luka informacyjna, wartość, lekki uśmiech
- "Zbudujemy razem 3 agentów" + "Wyjdziesz z konkretnym planem"
- Canvas do wypełnienia (QR code) — 6 pól: Problem, Oczekiwany rezultat, Potencjalne rozwiązanie, Korzyści, Zagrożenia, Jak dalej rozwijać
- Live post na LinkedIn ze sceny — presja "jak sfailuję, LinkedIn się dowie"

### Kluczowe narracje
- "Money glitch" — gdzie jest 10x wartość? Musisz znaleźć 10x dla biznesu, inaczej nikt nie zauważy
- "Niewyjebywalny marketer" — AI zabiera części pracy, nie całą pracę
- "Narzędzia są wtórne" — MS, Google, ChatGPT — narzędzia się zmieniają, mechanizmy zostają
- "Oddasz nudną pracę" — ale NIE oddawaj fajnych zadań (zostaniesz asystentem AI)
- "Korzyści dzielić, straty agregować" — WNIOSEK

### 3 use case'y (live demo)
1. **Prasówka branżowa** — monitoring konkurencji + branży → pogrupowane sygnały na Slacka/Teams
2. **Content/Post** — na podstawie zebranych danych → draft posta → publikacja (z akceptacją)
3. **Toole marketingowe** — alerty/rekomendacje z Google Ads, Senuto + reguły firmowe

### Narzędzia
- **AgentSpace** (Google) — dane z systemów Google, MCP do GA i Google Ads
- **Copilot Studio** (Microsoft) — baza wiedzy, odpowiadanie na pytania
- **n8n** — orkiestracja, Apify, Firecrawl, Airtable jako baza
- **???** — OpenAI Agent Builder?

### Źródła danych
- Konkurencja: strona + social media (IG, LinkedIn per hashtag + konto)
- Branża: newslettery + blogi
- Toole marketingowe: Google Ads, Senuto
- Archiwalne treści + baza wiedzy
- Config w Airtable/Notion

### Kluczowe cytaty / pomysły
- "70-osobowa agencja marketingowa, 500h miesięcznie i 20k oszczędności" (test 2023)
- "Jeden klient odzyskał utopione 150k" (case study)
- Wykres rynku pracy: platforms.substack.com/p/the-many-fallacies-of-ai-wont-take
- "Korzystasz z samego chatbota? Jesteś w dupie w porównaniu z osobą z agentem"
- "Naparzasz jak małpa w kołowrotku"
- Licznik wyjebek (live counter na scenie)

### Zadania do zrobienia
- [ ] Przegląd dokumentacji agentowej: MS, Google, n8n w Marketing
- [ ] Request do OpenAI Azure Services
- [ ] Sprawdzić VertexAI + porządki GCP
- [ ] Rozkminić licencje Copilot Studio
- [ ] FOTC: dostęp do wersji plus
- [ ] Wywiady z grupą docelową
- [ ] Zbudowanie NotebookLM z materiałami
- [ ] Przygotować testowe dane per branża
- [ ] Przygotować żarty sytuacyjne
- [ ] Dograć z Matim scenariusz w n8n

---

## Zastosowanie w Dokodu

### Competitive intel
- AI Hero planuje prezentację z live-built agentami w n8n + AgentSpace + Copilot Studio
- Ich pitch: "Money glitch" + "Niewyjebywalny marketer" + live demo na scenie
- Porównanie toolowe: AgentSpace vs Copilot Studio vs n8n — Kacper może zrobić kontr-content

### Content inspiration
- Format "3 agentów na żywo" jest świetny do YT
- "Prasówka branżowa z AI" = artykuł na blog (ludzie tego szukają)
- "Monitoring konkurencji z n8n + Apify" = tutorial
