---
type: course-exercises
modul: 06
tytul: "Autonomiczne Agenty AI — MASTERCLASS"
liczba_cwiczen: 2
zadanie_domowe: true
status: draft
last_reviewed: 2026-03-27
---

# Moduł 06 — Ćwiczenia

---

## Ćwiczenie 1: Agent z dostępem do internetu
**Czas: ~30 minut | Poziom: podstawowy**

### Cel
Zbudujesz agenta AI, który potrafi samodzielnie przeszukać internet i zebrać konkretne informacje o firmie. Nauczysz się konfigurować AI Agent node z narzędziem SerpAPI oraz mierzyć koszt w tokenach na podstawie execution log.

### Wymagania
- n8n działające lokalnie lub w chmurze
- Klucz API SerpAPI (darmowe konto: 100 wyszukiwań/miesiąc)
- Klucz API OpenAI (model GPT-4o-mini wystarczy)
- Webhook Tester (np. Postman lub cURL)

---

### Krok 1: Skonfiguruj kredencjały SerpAPI (3 min)

W n8n przejdź do **Settings → Credentials → Add Credential → SerpAPI**.

Wejdź na [serpapi.com](https://serpapi.com), stwórz darmowe konto, skopiuj API Key.

Wklej klucz w n8n i kliknij **Save**. Zielony tick = gotowe.

---

### Krok 2: Zbuduj workflow (15 min)

Zbuduj workflow według schematu:

```
[Webhook Trigger]
  Method: POST
  Path: /agent-firma
      ↓
[AI Agent]
  Model: GPT-4o-mini
  Tools: SerpAPI
  System Prompt: (patrz niżej)
      ↓
[Webhook Respond]
  Response: {{ $json.output }}
```

**System Prompt dla AI Agent:**

```
Jesteś analitykiem biznesowym. Gdy dostaniesz nazwę firmy, wykonaj wyszukiwanie i odpowiedz w formacie JSON:

{
  "firma": "nazwa firmy",
  "co_robi": "1-2 zdania czym się zajmuje",
  "rok_zalozenia": "rok lub 'nieznany'",
  "produkty_ai": true/false,
  "produkty_ai_opis": "jeśli tak — co konkretnie, jeśli nie — 'brak'"
}

Używaj narzędzia SerpAPI do wyszukania aktualnych informacji.
Wyszukaj: "[nazwa firmy] company founded products AI"
Jeśli nie znajdziesz roku założenia — wpisz "nieznany".
Odpowiedz WYŁĄCZNIE JSONem, bez żadnego dodatkowego tekstu.
```

**Konfiguracja Webhook Trigger:**
- W polu **Response Mode** ustaw: `Using Respond to Webhook Node`
- Zapamiętaj URL webhooka — będziesz go używać do testów

---

### Krok 3: Przetestuj agenta (5 min)

Wyślij request przez cURL lub Postman:

```bash
curl -X POST https://twoj-n8n.com/webhook/agent-firma \
  -H "Content-Type: application/json" \
  -d '{"firma": "Figma"}'
```

Oczekiwana odpowiedź (format może się lekko różnić):

```json
{
  "firma": "Figma",
  "co_robi": "Narzędzie do projektowania interfejsów UI/UX działające w przeglądarce, umożliwiające współpracę w czasie rzeczywistym.",
  "rok_zalozenia": "2012",
  "produkty_ai": true,
  "produkty_ai_opis": "Figma AI — funkcje generowania komponentów, auto-layout suggestions, treści tekstowych"
}
```

Przetestuj z 3 różnymi firmami: jedną dużą (np. Figma, Notion), jedną polską (np. Allegro, CD Projekt), jedną mniej znaną ze swojej branży.

---

### Krok 4: Zmierz koszt w tokenach (5 min)

Po wykonaniu workflow kliknij na node **AI Agent** w execution log.

Znajdź sekcję **Tokens** lub **Usage** — zobaczysz:
- `prompt_tokens` — ile tokenów zużył prompt (kontekst + system prompt + wynik wyszukiwania)
- `completion_tokens` — ile tokenów zajęła odpowiedź agenta
- `total_tokens` — suma

**Przelicz koszt:**

Dla GPT-4o-mini (ceny orientacyjne, sprawdź aktualne na platform.openai.com):
- Input: ~$0.15 / 1M tokenów
- Output: ~$0.60 / 1M tokenów

Wzór: `koszt = (prompt_tokens / 1_000_000 * 0.15) + (completion_tokens / 1_000_000 * 0.60)`

Dla typowego requestu o firmę koszt powinien wynosić **poniżej $0.01**.

Zanotuj wyniki dla 3 firm. Czy złożoność firmy (duża vs mała vs polska) wpływa na liczbę tokenów?

---

### Czego nauczyłeś się w tym ćwiczeniu
- AI Agent w n8n to node który sam decyduje kiedy i ile razy wywołać narzędzie
- SerpAPI daje agentowi dostęp do aktualnych danych z sieci — bez limitów wiedzy z treningu modelu
- Koszt jednego zapytania agentowego to ułamki centa — skalowalność jest realna
- Execution log jest Twoim oknem na to co agent "myślał" — używaj go do debugowania

---

## Ćwiczenie 2: B2B Lead Analyst Lite — system multi-agentowy
**Czas: ~90 minut | Poziom: zaawansowany**

### Cel
Zbudujesz uproszczoną wersję systemu wieloagentowego do analizy leadów B2B. Dwa wyspecjalizowane subagenty (Research Agent i ICP Scoring Agent) będą współpracować pod nadzorem Supervisor Node, który zbierze ich wyniki i wygeneruje raport w formacie Markdown.

### Wymagania
- n8n działające lokalnie lub w chmurze
- Klucz API SerpAPI
- Klucz API OpenAI (GPT-4o lub GPT-4o-mini)
- Podstawowa znajomość swojego ICP (Ideal Customer Profile)

---

### Architektura systemu

```
[Webhook Trigger: POST /lead-analyst]
  Input: { "firma": "NazwaFirmy", "branża": "branża" }
      ↓
[SUBAGENT 1: Research Agent]
  Zbiera fakty o firmie z internetu
      ↓
[SUBAGENT 2: ICP Scoring Agent]
  Ocenia dopasowanie do ICP na podstawie wyników researchu
      ↓
[SUPERVISOR: Raport Generator]
  Łączy wyniki, generuje raport Markdown
      ↓
[Webhook Respond: raport]
```

---

### SUBAGENT 1: Research Agent (25 min)

Stwórz nowy workflow o nazwie `Sub_ResearchAgent` z **Execute Workflow Trigger**.

Zbuduj workflow:

```
[Execute Workflow Trigger]
  Input: firma, branża
      ↓
[AI Agent: Research]
  Model: GPT-4o-mini
  Tools: SerpAPI
      ↓
[Set: Ustandaryzuj output]
      ↓
[Execute Workflow Trigger: Respond]
```

**System Prompt dla Research Agent:**

```
Jesteś analitykiem biznesowym specjalizującym się w badaniu firm B2B.

Twoim zadaniem jest zebranie faktycznych informacji o firmie: {{ $json.firma }} z branży {{ $json.branża }}.

Wykonaj wyszukiwanie i uzupełnij poniższy JSON (nie wymyślaj danych — jeśli nie wiesz, wpisz null):

{
  "firma": "nazwa",
  "branża": "branża",
  "wielkosc": "startup/SME/enterprise (oszacuj na podstawie liczby pracowników)",
  "kraj": "kraj siedziby",
  "rok_zalozenia": rok lub null,
  "liczba_pracownikow": "przedział np. 50-200 lub null",
  "przychody_szacunek": "przedział w PLN/EUR/USD lub null",
  "produkty_glowne": ["produkt1", "produkt2"],
  "uzywane_technologie": ["technologia1", "technologia2"],
  "automatyzacja_ai": true/false,
  "opis_dzialalnosci": "2-3 zdania"
}

Odpowiedz WYŁĄCZNIE tym JSONem.
```

**Set Node "Ustandaryzuj output":**
- Field: `research_result`
- Value: `{{ JSON.parse($json.output) }}`

Aktywuj workflow (nie uruchamiaj ręcznie — będzie wywoływany przez supervisor).

---

### SUBAGENT 2: ICP Scoring Agent (25 min)

Stwórz nowy workflow `Sub_ICPScoring` z **Execute Workflow Trigger**.

**System Prompt dla ICP Scoring Agent:**

```
Jesteś ekspertem od kwalifikacji leadów B2B. Otrzymujesz dane o firmie i oceniasz jej dopasowanie do Ideal Customer Profile (ICP).

DANE FIRMY:
{{ $json.research_result }}

ICP (Idealny Klient):
- Wielkość: SME lub enterprise (10-500 pracowników)
- Branże: produkcja, logistyka, e-commerce, usługi B2B
- Pain points: powtarzalne procesy manualne, brak automatyzacji, duży wolumen dokumentów
- Budżet: >50 000 PLN/rok na narzędzia IT
- Sygnały zakupowe: zatrudnianie na stanowiska techniczne, ekspansja, cyfryzacja

Oceń firmę i odpowiedz w formacie JSON:

{
  "icp_score": liczba od 0 do 100,
  "kategoria": "hot/warm/cold",
  "pasujace_kryteria": ["kryterium1", "kryterium2"],
  "brakujace_kryteria": ["kryterium1"],
  "glowny_pain_point": "1 zdanie",
  "rekomendacja": "Skontaktuj się / Dodaj do nurturingu / Pomiń",
  "proponowany_produkt": "nazwa usługi Dokodu najlepiej pasującej do tego leadu",
  "uzasadnienie": "2-3 zdania dlaczego taka ocena"
}
```

Aktywuj workflow.

---

### SUPERVISOR: Raport Generator (25 min)

W głównym workflow (wywoływanym przez Webhook Trigger) zbuduj:

```
[Webhook Trigger: POST /lead-analyst]
      ↓
[Execute Workflow: Sub_ResearchAgent]
  Pass: firma, branża
      ↓
[Execute Workflow: Sub_ICPScoring]
  Pass: research_result z poprzedniego kroku
      ↓
[Code Node: "Generuj raport Markdown"]
      ↓
[Webhook Respond]
```

**Code Node — generowanie raportu:**

```javascript
const research = $('Execute Workflow').first().json.research_result || {};
const scoring = $('Execute Workflow1').first().json || {};

// Parsuj jeśli stringi
const r = typeof research === 'string' ? JSON.parse(research) : research;
const s = typeof scoring === 'string' ? JSON.parse(scoring) : scoring;

const score = s.icp_score || 0;
const emoji = score >= 70 ? '🟢' : score >= 40 ? '🟡' : '🔴';

const raport = `# Raport Analizy Leadu B2B
**Firma:** ${r.firma || 'N/A'}
**Data analizy:** ${new Date().toISOString().split('T')[0]}
**Analityk:** B2B Lead Analyst Lite v1.0

---

## 1. Profil Firmy

| Pole | Wartość |
|------|---------|
| Branża | ${r.branża || 'N/A'} |
| Wielkość | ${r.wielkosc || 'N/A'} |
| Kraj | ${r.kraj || 'N/A'} |
| Rok założenia | ${r.rok_zalozenia || 'N/A'} |
| Pracownicy | ${r.liczba_pracownikow || 'N/A'} |
| Przychody (szacunek) | ${r.przychody_szacunek || 'N/A'} |

**Opis:** ${r.opis_dzialalnosci || 'Brak danych'}

**Główne produkty/usługi:** ${(r.produkty_glowne || []).join(', ') || 'N/A'}

**Używane technologie:** ${(r.uzywane_technologie || []).join(', ') || 'N/A'}

**Automatyzacja / AI w firmie:** ${r.automatyzacja_ai ? 'TAK' : 'NIE'}

---

## 2. Ocena ICP

### Wynik: ${emoji} ${score}/100 — ${s.kategoria?.toUpperCase() || 'N/A'}

**Pasujące kryteria:**
${(s.pasujace_kryteria || []).map(k => `- ✅ ${k}`).join('\n') || '- brak'}

**Brakujące kryteria:**
${(s.brakujace_kryteria || []).map(k => `- ❌ ${k}`).join('\n') || '- brak'}

**Główny pain point:** ${s.glowny_pain_point || 'N/A'}

---

## 3. Rekomendacja

**Akcja:** **${s.rekomendacja || 'N/A'}**

**Proponowany produkt Dokodu:** ${s.proponowany_produkt || 'N/A'}

**Uzasadnienie:** ${s.uzasadnienie || 'N/A'}

---
*Raport wygenerowany automatycznie przez B2B Lead Analyst Lite — n8n + GPT-4o-mini*
`;

return [{ json: { raport, firma: r.firma, score, kategoria: s.kategoria } }];
```

---

### Test końcowy: zbadaj 3 firmy (15 min)

Wyślij 3 requesty z różnymi firmami i porównaj jakość raportów:

```bash
# Firma 1 — duży gracz e-commerce
curl -X POST https://twoj-n8n.com/webhook/lead-analyst \
  -H "Content-Type: application/json" \
  -d '{"firma": "Allegro", "branża": "e-commerce"}'

# Firma 2 — producent przemysłowy
curl -X POST https://twoj-n8n.com/webhook/lead-analyst \
  -H "Content-Type: application/json" \
  -d '{"firma": "Fakro", "branża": "produkcja"}'

# Firma 3 — mała firma usługowa z Twojej okolicy
curl -X POST https://twoj-n8n.com/webhook/lead-analyst \
  -H "Content-Type: application/json" \
  -d '{"firma": "Twój lokalny lead", "branża": "Twoja branża"}'
```

**Pytania do refleksji po teście:**
- Która firma dostała najwyższy ICP score? Czy zgadzasz się z oceną?
- Czy Research Agent wypełnił wszystkie pola? Gdzie były luki?
- Ile czasu zajęło wygenerowanie jednego raportu? Ile tokenów?
- Jak poprawiłbyś ICP scoring prompt żeby lepiej pasował do Twojej branży?

---

### Kryteria zaliczenia ćwiczenia
- [ ] Oba subworkflowy działają i zwracają poprawny JSON
- [ ] Supervisor łączy wyniki i generuje czytelny raport Markdown
- [ ] Testy przeszły dla 3 firm (raporty zapisane/wklejone na platformie)
- [ ] Przeanalizowałeś przynajmniej jeden raport i skomentowałeś jakość danych

---

## Zadanie domowe: Integracja z Google Sheets CRM
**Czas: ~60 minut | Poziom: zaawansowany**

### Zadanie
Rozbuduj główny workflow o automatyczne dodawanie wyników do arkusza Google Sheets pełniącego rolę uproszczonego CRM.

### Przygotuj arkusz

Stwórz nowy arkusz w Google Sheets o nazwie `CRM_Leady_AI`. Dodaj nagłówki w wierszu 1:

```
Data | Firma | Branża | ICP Score | Kategoria | Rekomendacja | Proponowany Produkt | Liczba Pracowników | Kraj | Automatyzacja AI
```

### Rozbuduj workflow

Za Code Node "Generuj raport Markdown" dodaj:

```
[Code Node: Generuj raport]
      ↓
[Google Sheets: Append Row]
  Spreadsheet: CRM_Leady_AI
  Sheet: Sheet1
  Columns Mapping:
    Data:                {{ new Date().toISOString().split('T')[0] }}
    Firma:               {{ $json.firma }}
    Branża:              {{ $('Webhook Trigger').item.json.body.branża }}
    ICP Score:           {{ $json.score }}
    Kategoria:           {{ $json.kategoria }}
    Rekomendacja:        {{ $('Execute Workflow1').item.json.rekomendacja }}
    Proponowany Produkt: {{ $('Execute Workflow1').item.json.proponowany_produkt }}
    Liczba Pracowników:  {{ $('Execute Workflow').item.json.research_result.liczba_pracownikow }}
    Kraj:                {{ $('Execute Workflow').item.json.research_result.kraj }}
    Automatyzacja AI:    {{ $('Execute Workflow').item.json.research_result.automatyzacja_ai }}
      ↓
[Webhook Respond: raport]
```

### Bonus: Kolorowanie wierszy

Dodaj za Sheets node kolejny node **Google Sheets: Update Row** z formatowaniem warunkowym:
- Score ≥ 70 → kolor tła: zielony (`#d9ead3`)
- Score 40–69 → żółty (`#fff2cc`)
- Score < 40 → czerwony (`#fce8e6`)

Użyj Google Sheets API (Sheets v4) przez node **HTTP Request** z metodą `batchUpdate`.

### Sukces zadania domowego

Zbadaj 5 firm. Arkusz CRM powinien mieć 5 wypełnionych wierszy z poprawnymi danymi, posortowanych według ICP Score. Zrób screenshot i wrzuć na platformę kursową.

---

## Materiały dodatkowe

- [n8n AI Agent documentation](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/) — pełna dokumentacja node'a
- [SerpAPI Playground](https://serpapi.com/playground) — testuj zapytania zanim użyjesz w n8n
- [ReAct Pattern — paper](https://arxiv.org/abs/2210.03629) — fundamenty działania agentów (Yao et al. 2022)
- [LangGraph Multi-Agent Concepts](https://langchain-ai.github.io/langgraph/concepts/multi_agent/) — teoria systemów wieloagentowych
- Moduł 05 (Human-in-the-Loop) — wróć jeśli chcesz dodać approval step przed wysłaniem raportu do CRM
