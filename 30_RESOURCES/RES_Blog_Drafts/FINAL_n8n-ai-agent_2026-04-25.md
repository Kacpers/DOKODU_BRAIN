# n8n AI Agent — jak zbudować agenta AI w n8n (tutorial 2026)

n8n od wersji 1.30+ ma natywny **AI Agent node** — dzięki temu zbudujesz agenta AI w 30 minut bez kodowania. Pokażę dokładnie jak skonfigurować pierwszy AI Agent w n8n, jakie mam ustawienia w produkcji w Dokodu i jak unikać pułapek, które kosztują pieniądze.

Pełny przewodnik biznesowy o agentach AI: [Agent AI dla firm](/blog/agent-ai-dla-firm). Tutorial budowy generic agenta: [Jak stworzyć agenta AI](/blog/agent-ai-jak-stworzyc).

---

## Co to jest AI Agent node w n8n?

**AI Agent node** to wbudowana integracja LangChain w n8n, która łączy:
- **Chat Model** (Claude, GPT, Gemini, Ollama) jako "mózg"
- **Memory** (Window Buffer / Vector / Postgres-based) — pamięć
- **Tools** — narzędzia, które agent może wywoływać (Hunter, Slack, Postgres, custom)

Wszystko skonfigurowane wizualnie — żadnej linijki kodu w przypadku 80% użytków.

---

## Krok 1: n8n self-hosted z AI Agent (5 min)

Jeśli nie masz jeszcze n8n self-hosted, zacznij od: [n8n self-hosted z Dockerem](/blog/n8n/docker-instalacja-konfiguracja). 30 min od zera do produkcyjnej instancji.

> 🔥 **Potrzebujesz hostingu pod n8n?**
>
> Polecam [Hostinger VPS](https://www.hostinger.com/kacper10) — z kodem **KACPER10** masz -10% (~30 zł/mies. za 4 GB RAM). Używam tego do n8n.dokodu.it produkcyjnie.
>
> *Disclosure: link afiliacyjny — używam Hostingera sam.*

W n8n self-hosted od wersji 1.30+ AI Agent node jest dostępny natywnie. Sprawdź wersję w panelu n8n (Settings → About).

---

## Krok 2: Stwórz pierwszy workflow z AI Agent

W n8n: **+ Add node → AI → AI Agent**.

Pojawia się node z 3 polami:
- **Chat Model** (wymagane)
- **Memory** (opcjonalne, domyślnie brak)
- **Tools** (opcjonalne, domyślnie brak)

### Chat Model: Claude Sonnet 4.6

1. Klik na pole "Chat Model" → "+ Add Chat Model"
2. Wybierz "Anthropic Chat Model"
3. W panelu konfiguracji:
   - **Credential**: dodaj Anthropic API key (z console.anthropic.com)
   - **Model**: `claude-sonnet-4-6` (lub `claude-opus-4-7` dla maksymalnej jakości)
   - **Temperature**: 0.7 (default — kreatywność vs determinizm)
   - **Max tokens**: 4096

**Dlaczego Sonnet 4.6 a nie Opus 4.7:**
Sonnet 4.6 jest 5× tańszy od Opus 4.7, dla większości B2B taska wystarczy. Opus rezerwuję dla najważniejszych decyzji (np. analiza danych finansowych, długie raporty).

**Dlaczego Claude a nie GPT:**
Claude lepiej radzi sobie z długim kontekstem (1M tokens vs 128k GPT-4o), strukturalnymi outputami (JSON), i decyzjami biznesowymi B2B. Na benchmarkach Claude wygrywa w "agent reasoning" o 20-30%.

---

## Krok 3: System prompt — najważniejszy element

W AI Agent node, w polu **"Prompt - System Message"**, wpisz instrukcję dla agenta.

**Przykład — klasyfikator leadów B2B:**

```
Jesteś asystentem AI agencji Dokodu specjalizującej się we wdrożeniach 
automatyzacji i agentów AI dla firm MŚP w Polsce.

ICP klienta:
- Firma 50-500 pracowników
- Branże: logistyka, produkcja, e-commerce, usługi profesjonalne
- Lokalizacja: Polska
- Świadomość AI: średnia, brak własnego zespołu ML
- Budżet na wdrożenie: 10-50k PLN

Twoja rola:
1. Analizuj informacje o leadzie (firma, osoba, message)
2. Oceń BANT score (1-10):
   - Budget: czy budżet wskazuje na 10-50k PLN range?
   - Authority: decision maker (CTO/CEO/dyrektor) czy zwykły pracownik?
   - Need: konkretny problem czy ogólne zainteresowanie?
   - Timeline: "teraz" / "w tym kwartale" / "kiedyś"?
3. Klasyfikuj: HOT (8-10), WARM (5-7), COLD (1-4)
4. Zwracaj JSON: {"score": int, "classification": str, "reasoning": str, 
   "recommended_action": str, "key_signals": [str]}

WAŻNE:
- Score zawsze 1-10 (integer)
- Reasoning po polsku, max 200 znaków
- Recommended action: konkretny krok ("Umów call w 24h", "Wyślij ebook", 
  "Zignoruj — spam")
- Bądź sceptyczny przy ogólnikach typu "chcę AI"
```

Dobry system prompt = **80% sukcesu agenta**.

---

## Krok 4: Memory — pamięć rozmowy

Bez memory agent jest "stateless" — każde wywołanie zaczyna od zera.

W AI Agent node, dodaj **"Memory" → "Window Buffer Memory"**:

- **Memory Buffer Window**: 10 (ostatnie 10 wymian — wystarczające dla większości zastosowań)
- **Session ID**: `{{ $('Webhook').item.json.session_id }}` (lub email leadu, lub jakikolwiek unique identifier)

**Window Buffer** trzyma ostatnie N wiadomości — proste, działa.

Dla bardziej zaawansowanych: **Postgres Memory** (persistent przez lata) lub **Vector Store Memory** (semantyczne wyszukiwanie historycznego kontekstu).

---

## Krok 5: Tools — co agent może zrobić

Tools to **narzędzia, które agent autonomicznie wywołuje** podczas reasoning'u.

W AI Agent node, dodaj **"Tools"** — masz do wyboru:

### A. Built-in tooli (najczęściej używane)
- **Calculator** — operacje matematyczne (np. ROI calculations)
- **Code Tool** — Python lub JS execution dla customowej logiki
- **HTTP Request Tool** — woła zewnętrzne API
- **Workflow Tool** — wywołuje inny workflow n8n jako sub-routine

### B. Integration tools
- **Notion Tool** — query/update Notion database
- **Slack Tool** — wysyła wiadomości
- **Google Sheets Tool** — operations na arkuszach
- **Postgres Tool** — query bazę danych
- **Vector Store Tool** — semantic search

### C. Custom tool (najpotężniejsze)

Możesz stworzyć **custom tool** który robi cokolwiek przez n8n workflow:

1. Dodaj "Workflow Tool"
2. Wybierz workflow który będzie wykonany (np. "Lead Enrichment Sub-workflow")
3. Opisz co tool robi: "Wzbogaca dane firmy o liczbę pracowników, branżę, lokalizację"
4. Agent autonomicznie zdecyduje kiedy go wywołać

**Pro tip:** opis tool-a dla agenta jest **kluczowy** — dobry opis = agent wie kiedy użyć.

---

## Krok 6: Trigger + workflow connection

AI Agent node potrzebuje **input message**. Najczęstsze triggery:

### Webhook trigger (formularz / API)
```
Trigger: Webhook → AI Agent (input: $json.message) → IF (score >=7) → 
  TRUE: Slack notify + Notion CRM
  FALSE: Email nurturing
```

### Schedule trigger (codzienne raporty)
```
Trigger: Schedule (codziennie 8:00) → Database query (nowe leady z 24h) → 
  Loop: AI Agent klasyfikuje każdy → Aggregate → Send report
```

### Email trigger (klasyfikacja maili)
```
Trigger: Gmail (nowe maile) → AI Agent (input: $json.body) → 
  Switch: lead/support/spam/internal → Routing
```

---

## Krok 7: Production — co jeszcze MUSISZ mieć

### 1. Error handling

Każdy node powinien mieć "On Error: Continue + Notify Slack #errors". Inaczej zepsute wykonanie zatrzymuje pipeline.

### 2. Audit log (AI Act compliance)

Po każdym AI Agent execution zapisz do osobnej tabeli (Postgres / Notion):
- Timestamp
- Input prompt
- Output (full JSON)
- Tools wywołane
- Cost (tokens used × price)

Dla high-risk decyzji (HR, finance, medical) — **wymóg AI Act**, nie opcja.

### 3. Rate limiting

Anthropic ma limity API (zależnie od planu). Dla intensywnego usage:
- "Wait" node między iteracjami pętli
- Queue mode w n8n (Redis-based)
- Worker nodes do skalowania

### 4. Cost monitoring

Każde wywołanie AI Agent zużywa tokens. W intensywnym workflow (1000+ leadów dziennie):
- Alert Slack przy miesięcznym koszcie > X PLN
- Anthropic console: ustaw budget limit
- Switch na Haiku 4.5 (10× tańszy) dla wysokoskalowych zadań

### 5. Backup + recovery

n8n workflow JSON commitowany do Git. Każda zmiana w produkcji = osobny commit. Łatwe rollback.

---

## Najczęstsze błędy w n8n AI Agent

### 1. Brak system prompt → agent improwizuje

Bez konkretnego system prompt agent traktuje każdy request jako pytanie generyczne. Output = "wycieczka" zamiast structured response.

**Fix:** zawsze definiuj rolę, zadanie, format output.

### 2. Memory bez session_id → wszyscy mieszają się

Default memory używa global session, więc lead A widzi rozmowę z leadem B w pamięci. Bezpieczeństwo + jakość = problem.

**Fix:** zawsze ustaw `Session ID` na coś unique (email, lead ID, user ID).

### 3. Tools bez opisu → agent nie wie kiedy ich użyć

Tool "HTTP Request" bez opisu = agent zgaduje. Albo nigdy nie używa, albo wszędzie wstawia.

**Fix:** każdy tool ma 1-2 zdaniowy opis: "Używaj kiedy potrzebujesz X z serwisu Y".

### 4. Brak structured output

Agent zwraca text. Twój workflow potem musi parsować. Często bug.

**Fix:** w system prompt: "Zwracaj zawsze JSON z polami X, Y, Z". Plus walidacja schema po AI Agent (Set node z validation).

### 5. Overuse of Opus

Opus 4.7 jest 5× droższy od Sonnet 4.6. Dla większości tasków Sonnet wystarczy. Opus = top decyzje, długie konteksty, krytyczne raporty.

**Fix:** default Sonnet, switch na Opus tylko per-need.

---

## Co czytać dalej

- **[Agent AI dla firm — pillar](/blog/agent-ai-dla-firm)** — kompletny przewodnik biznesowy
- **[Agent AI — co to jest](/blog/agent-ai-co-to)** — definicja, vs chatbot, vs RPA
- **[Jak stworzyć agenta AI — tutorial](/blog/agent-ai-jak-stworzyc)** — generic tutorial
- **[n8n self-hosted z Dockerem](/blog/n8n/docker-instalacja-konfiguracja)** — infrastruktura
- **[n8n Templates 2026](/blog/n8n/przyklady-workflow-automatyzacji)** — gotowe workflow do skopiowania
- **[Claude Code MCP](/blog/claude-code/mcp)** — alternatywa: agent w terminalu zamiast n8n

<AD:n8n-workshop>

---

## FAQ — n8n AI Agent

**Jaki jest minimalny plan n8n żeby używać AI Agent?**

n8n self-hosted (free, open source). Cloud: dowolny plan obsługuje AI Agent.

**Czy AI Agent node zlicza się do limitu wykonań w n8n Cloud?**

Tak — każda execution AI Agent to jedna n8n execution + tokens API.

**Mogę używać lokalnego LLM (Ollama)?**

Tak — n8n AI Agent obsługuje Ollama. Konfiguracja: "Chat Model" → "Ollama" → URL lokalnego serwera. Jakość modeli lokalnych (Llama 3, Mistral) jest gorsza od Claude/GPT, ale 0 PLN za API.

**Czy AI Agent może wywołać inny AI Agent (multi-agent)?**

Tak — przez Workflow Tool. Agent A wywołuje workflow B który ma własnego AI Agent. Klasyczny multi-agent setup.

**Najlepszy model dla wysokiego volume?**

Claude Haiku 4.5 — 10× tańszy od Opus, 5× szybszy, jakość wystarcza dla 80% zadań klasyfikacyjnych.

**Co jeśli n8n AI Agent zwraca śmieciowy output?**

Najczęściej winien jest system prompt (zbyt ogólny / niejasny / bez schemat output). Drugi problem: za niska temperature (0 = deterministyczne ale sztywne) lub za wysoka (1.5 = chaos).

---

*Tutorial bazuje na produkcyjnym workflow w Dokodu (klasyfikator leadów B2B). n8n 1.45+, AI Agent node z LangChain integration, Claude Sonnet 4.6.*
