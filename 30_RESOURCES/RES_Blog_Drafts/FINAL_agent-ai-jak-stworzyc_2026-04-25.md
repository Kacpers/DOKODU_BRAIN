# Jak stworzyć agenta AI — tutorial krok po kroku (od zera do działającego, 2026)

Pokażę dokładnie jak zbudować pierwszego agenta AI od zera — bez programowania, w n8n. Tutorial bazuje na realnym workflow, który stworzyłem dla agencji AI Dokodu — **klasyfikator i pre-qualifier leadów B2B** który działa produkcyjnie.

Jeśli zastanawiasz się **co to jest agent AI** — zacznij od: [Agent AI — co to jest i czym różni się od chatbota](/blog/agent-ai-co-to). Pełen przewodnik biznesowy: [Agent AI dla firm](/blog/agent-ai-dla-firm).

---

## Co zbudujemy — workflow

**Agent kwalifikacji leadów B2B:**

1. Lead wpada (formularz, mail, LinkedIn webhook)
2. Agent pobiera dane firmy leadu (Hunter.io, LinkedIn API)
3. Klasyfikuje (BANT score: Budżet, Authority, Need, Timeline)
4. Aktualizuje CRM (Notion / HubSpot)
5. Jeśli score ≥ 7: powiadamia handlowca na Slacku z gotowym podsumowaniem
6. Jeśli score < 7: wysyła automatycznego maila nurturingowego

**Czas wdrożenia:** 4-6 godzin.
**Koszt operacyjny:** ~50 zł/mies. (n8n VPS + Claude API).
**ROI:** 4-5 godzin tygodniowo na handlowca.

---

## Krok 1: Wybór stacka

**n8n self-hosted** — platforma automatyzacji wizualna, no-code/low-code.

Dlaczego n8n a nie Make/Zapier:
- Self-hosted (dane w Twojej infrastrukturze, RODO/AI Act compliance)
- Tańszy przy skali (>10k wykonań/mc)
- AI Agent node natywnie (od n8n 1.30+)
- 400+ integracji, custom code możliwy

**Setup:** [n8n self-hosted z Dockerem](/blog/n8n/docker-instalacja-konfiguracja). 30 minut od zera do produkcyjnej instancji.

**Model AI:** Claude Sonnet 4.6 lub 4.7 (rekomendacja dla B2B — najlepsze rozumowanie + długi kontekst). Alternatywa: GPT-4o, Gemini 2.5 Pro.

**Tools:** Hunter.io API (enrichment leadów), Slack webhook (notyfikacje), Notion API (CRM).

---

## Krok 2: Setup n8n + AI Agent node

W n8n stwórz nowy workflow. Dodaj **AI Agent** node:

1. Klik "+ Add node" → szukaj "AI Agent"
2. Wybierz **"AI Agent"** (LangChain integration, default)
3. Konfiguracja:
   - **Chat Model:** Claude (Anthropic) — wybierz Sonnet 4.6
   - **Memory:** Window Buffer Memory (10 ostatnich wiadomości)
   - **Tools:** dodamy później

W panelu credentials dodaj **Anthropic API key** (z console.anthropic.com → API Keys).

**System prompt agenta** (kluczowy element):

```
Jesteś asystentem kwalifikacji leadów B2B dla agencji AI specjalizującej 
się we wdrożeniach automatyzacji dla firm 50-500 osób.

Twoja rola:
1. Analizuj informacje o firmie leadu
2. Oceń BANT score (1-10):
   - Budget: czy mają budżet na wdrożenie 10-50k PLN?
   - Authority: czy osoba jest decision-makerem?
   - Need: czy mają problem który rozwiązujemy?
   - Timeline: czy szukają teraz, czy "kiedyś"?
3. Klasyfikuj jako: HOT (8-10), WARM (5-7), COLD (1-4)
4. Zwracaj structured JSON z polami: score, classification, reasoning, 
   recommended_action, key_signals

ICP firmy: 50-500 pracowników, branża logistyczna/produkcyjna/usługowa, 
problemy z manualnymi procesami, świadomość AI ale brak technicznego know-how.
```

---

## Krok 3: Trigger — webhook od formularza

Pierwszy node workflow: **Webhook trigger**.

1. Dodaj node "Webhook"
2. Method: POST
3. Path: `/lead-qualifier`
4. Response: "Immediately" (żeby formularz nie czekał na pełne wykonanie)

W n8n widzisz URL — np. `https://n8n.twojafirma.pl/webhook/lead-qualifier`. To URL, który podpinasz pod formularz na stronie / Zapier-a / cokolwiek dostarcza leady.

**Test:** w terminalu:
```bash
curl -X POST https://n8n.twojafirma.pl/webhook-test/lead-qualifier \
  -H "Content-Type: application/json" \
  -d '{"email":"jan@example.com","company":"Example Sp. z o.o.","message":"Zainteresowany wdrożeniem AI"}'
```

n8n pokazuje "execution received" — webhook działa.

---

## Krok 4: Enrichment — pobranie danych firmy

Agent musi wiedzieć więcej niż tylko nazwa firmy. Dodaj node "HTTP Request" do **Hunter.io domain search**:

```
Method: GET
URL: https://api.hunter.io/v2/domain-search
Query Parameters:
  domain: {{ $json.email.split('@')[1] }}
  api_key: YOUR_HUNTER_KEY
```

Wynik: dane firmy (size, industry, location), top employees, websites.

Drugi enrichment (opcjonalnie): **LinkedIn API** dla profil osoby kontaktowej. Albo prostsze: Apollo.io / Lusha.

---

## Krok 5: AI Agent klasyfikuje

Z output enrichment idzie do **AI Agent** node:

```
Input prompt:
Lead z formularza:
- Email: {{ $('Webhook').item.json.email }}
- Firma: {{ $('Webhook').item.json.company }}
- Wiadomość: {{ $('Webhook').item.json.message }}

Dane z Hunter.io:
- Wielkość firmy: {{ $('HTTP Request').item.json.data.organization }}
- Branża: {{ $('HTTP Request').item.json.data.industry }}
- Lokalizacja: {{ $('HTTP Request').item.json.data.country }}

Oceń BANT score i zwróć structured JSON.
```

Claude analizuje, zwraca JSON typu:

```json
{
  "score": 8,
  "classification": "HOT",
  "reasoning": "Firma 200 osób, branża logistyczna (ICP fit), email od dyrektora operacyjnego, konkretne pytanie o automatyzację magazynu",
  "recommended_action": "Umów discovery call w ciągu 24h",
  "key_signals": ["company size match", "decision maker", "specific pain point", "timeline urgent"]
}
```

---

## Krok 6: Routing — IF condition

Po AI Agent dodaj **IF node**:

```
Condition: {{ $json.score }} >= 7
```

- **TRUE branch** (HOT/WARM): notyfikacja na Slacka + zapis do Notion CRM
- **FALSE branch** (COLD): mail nurturingowy + zapis do "low priority" pipeline

---

## Krok 7: Notyfikacja na Slacka (HOT leady)

W TRUE branch dodaj **Slack node**:

```
Channel: #sales-hot-leads
Message:
🔥 NOWY HOT LEAD (Score: {{ $('AI Agent').item.json.score }}/10)

📧 {{ $('Webhook').item.json.email }}
🏢 {{ $('Webhook').item.json.company }}
📊 Wielkość: {{ $('HTTP Request').item.json.data.organization }}
🎯 Branża: {{ $('HTTP Request').item.json.data.industry }}

💬 "{{ $('Webhook').item.json.message }}"

🤖 Reasoning: {{ $('AI Agent').item.json.reasoning }}
✅ Action: {{ $('AI Agent').item.json.recommended_action }}
```

Plus **Notion node** żeby utworzyć rekord w bazie CRM:

```
Database: Leads (twoja baza Notion)
Properties:
  Name: {{ $('Webhook').item.json.email }}
  Company: {{ $('Webhook').item.json.company }}
  Score: {{ $('AI Agent').item.json.score }}
  Status: HOT
  Source: Web form
```

---

## Krok 8: Mail nurturingowy (COLD leady)

W FALSE branch dodaj **Send Email** node:

```
To: {{ $('Webhook').item.json.email }}
Subject: Twoje pytanie o automatyzację AI — krótka odpowiedź
Body:
Cześć,

Dzięki za zainteresowanie automatyzacją AI w Twojej firmie. 
Z naszych doświadczeń pierwszy krok to ZROZUMIENIE jakie procesy 
najbardziej Ci pochłaniają czas.

Załączam darmowy ebook "Agent AI dla firm — 30 minut do pierwszego ROI" 
[link]. Po przeczytaniu — daj znać czy ma sens umówić call.

Pozdrawiam,
Kacper Sieradzinski
CEO Dokodu
```

---

## Krok 9: Test end-to-end

W n8n kliknij "Execute Workflow", potem na webhook → Listen for Test Event.

Z drugiego okna terminala:
```bash
curl -X POST [URL webhooka] \
  -H "Content-Type: application/json" \
  -d '{"email":"jan@duzafirma.pl","company":"Duża Firma Logistyczna","message":"Szukamy automatyzacji magazynu"}'
```

Obserwuj jak workflow biegnie w UI n8n — powinieneś zobaczyć każdy node executing → AI Agent zwraca JSON → IF kieruje do Slacka.

Jeśli wszystko OK → "Activate" workflow. Od teraz każdy lead z webhooka jest obsługiwany.

---

## Krok 10: Production hardening

Przed real produkcją dodaj:

### 1. Error handling
- Każdy node: "On Error: Continue + zapisz do Slacka #errors"
- Retry policy: 3 retries z exponential backoff dla HTTP requests

### 2. Logging
- Po każdym AI Agent zapisuj prompt + response do osobnej tabeli (audit log dla AI Act)

### 3. Rate limiting
- Hunter.io ma limity (100 req/h free) — dodaj "Wait" node między enrichment a AI Agent

### 4. Cost monitoring
- Alert na Slacku gdy miesięczny koszt Anthropic API > X PLN
- W Anthropic console ustaw limit budżetu

### 5. Testing data set
- 20 prawdziwych leadów z przeszłości
- Uruchom workflow na nich, porównaj decyzje agenta z rzeczywistymi
- Cel: ≥ 90% zgodności

---

## Co zostało (do zrobienia po pierwszej iteracji)

- **Multi-agent setup:** osobny agent dla różnych branż (logistic vs SaaS vs e-commerce)
- **Memory długoterminowa:** vector DB (Qdrant, Pinecone) — agent pamięta interakcje z firmą historycznie
- **A/B testing maili nurturingowych:** różne warianty, mierzony open rate
- **Voice channel:** integracja z Twilio dla telefonicznych leadów

---

## Co czytać dalej

- **[Agent AI dla firm — kompletny przewodnik 2026](/blog/agent-ai-dla-firm)** — pillar dla zarządu (ROI, koszty, AI Act)
- **[Agent AI — co to jest](/blog/agent-ai-co-to)** — wyjaśnienie po ludzku
- **[n8n AI Agent — tutorial budowy w n8n](/blog/n8n/n8n-ai-agent-tutorial)** — głębszy dive w specyficznie n8n
- **[n8n self-hosted z Dockerem](/blog/n8n/docker-instalacja-konfiguracja)** — infrastruktura
- **[Claude Code — kompletny przewodnik](/blog/claude-code)** — narzędzie do generowania workflow

<AD:n8n-workshop>

---

## FAQ

**Czy potrzebuję programisty żeby zbudować agenta?**

Nie dla prostych przypadków. n8n + AI Agent node = no-code. Złożone wdrożenia (custom integracje, multi-agent) wymagają wsparcia technicznego.

**Ile czasu zajmuje pierwsze działające wdrożenie?**

4-6 godzin dla agenta z tego tutorialu. 1-2 dni dla bardziej złożonego (multi-source enrichment, custom logika scoringu, integracje ERP).

**Co z RODO?**

Self-hosted n8n = dane zostają w Twojej infrastrukturze. API Anthropic / OpenAI dostają tylko dane potrzebne do decyzji (pseudonimizowane jeśli wrażliwe). Audit log obowiązkowy dla AI Act.

**Czy mogę użyć GPT zamiast Claude?**

Tak — n8n AI Agent obsługuje OpenAI GPT-4o, GPT-4 Turbo, Gemini, Mistral, lokalne modele (Ollama). Dla B2B preferuję Claude (lepsze rozumowanie), dla volume zazwyczaj GPT.

**Co jeśli chcę zacząć od czegoś prostszego?**

Najprostszy agent: workflow który czyta jeden mail i klasyfikuje (lead/spam). 30 minut od zera. Potem dosypujesz funkcje.

**Mogę zatrudnić Was do wdrożenia?**

Tak — Dokodu wdraża agentów AI dla firm 50-500 osób. Audyt procesów → POC → produkcja. [Umów konsultację](/kontakt).

---

*Tutorial bazuje na realnym workflow Dokodu, działającym produkcyjnie. Stan kwiecień 2026 — n8n 1.45+, Anthropic API, Notion CRM. Powstał z użyciem Claude Code.*
