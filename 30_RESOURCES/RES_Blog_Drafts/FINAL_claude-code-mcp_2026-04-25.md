# Claude Code MCP — co to jest i top 10 serwerów do podłączenia (2026)

MCP (Model Context Protocol) to standard od Anthropic, który zmienił pracę z agentami AI w 2025 roku. W tym przewodniku pokażę dokładnie **co to jest**, jak skonfigurować pierwszy MCP server w 5 minut, oraz **top 10 serwerów** które używam w agencji AI Dokodu — od Notion przez n8n po GitHub.

Jeśli zastanawiasz się **czym jest Claude Code w ogóle**, zacznij od pillara: [Claude Code — kompletny przewodnik 2026](/blog/claude-code).

---

## Co to jest MCP w prostych słowach?

**MCP (Model Context Protocol)** to standardowy sposób w jaki Claude (i inne modele) podłączają się do **zewnętrznych narzędzi**. Bez MCP agent AI to "rozmówca w boxie" — zna ogólną wiedzę z treningu, ale nie ma dostępu do Twoich danych ani narzędzi.

Z MCP podłączonym, Claude może:
- Czytać Twoje **bazy danych** (Postgres, MongoDB, Supabase)
- Sprawdzać **kalendarz** Google, mailbox Gmail
- Tworzyć/edytować strony w **Notion**, tickety w **Linear/Jira**
- Robić **commits** do GitHub, otwierać PR-y, sprawdzać CI
- Wywoływać **API** firmowe — Twoje, klientów, zewnętrzne
- Operować na **n8n workflow** (pełne CRUD)

W praktyce: zamiast pisać "skopiuj te dane z Notion do CRM", Claude **realnie robi to za Ciebie** w jednym kroku.

### Architektura MCP

```
┌─────────────┐     stdin/stdout     ┌──────────────────┐
│ Claude Code │ <─────────────────>  │   MCP Server     │
│   (klient)  │     JSON-RPC         │ (np. notion)     │
└─────────────┘                       └──────────────────┘
                                              │
                                              ▼
                                      ┌──────────────────┐
                                      │ Notion API       │
                                      │ (Twój workspace) │
                                      └──────────────────┘
```

**MCP server** to programik (najczęściej Node.js lub Python) który tłumaczy między formatem Claude'a (Tool Use API) a konkretnym serwisem (Notion, Slack, Postgres). Serwery uruchamiane są **lokalnie na Twojej maszynie** — Twoje dane nie idą przez Anthropic poza tym co Claude potrzebuje do odpowiedzi.

### MCP vs zwykłe API integration — co MCP daje ekstra?

| Cecha | Zwykłe API (custom) | MCP |
|-------|--------------------:|----:|
| Czas integracji | Godziny–dni | 2–5 minut |
| Spójny interfejs | Różnie | Standard |
| Auth handling | Custom per service | Wbudowane |
| Dyskoverable tools | Manual docs | Auto-discovery |
| Reusable across modeli | Nie (custom dla GPT, Claude...) | Tak (standard) |
| Marketplace gotowych | Brak | 100+ MCP servers |

**Bottom line:** MCP to "USB dla AI" — podłączasz tool, działa.

---

## Jak zainstalować pierwszy MCP server (5 minut)

Pokażę na przykładzie **filesystem MCP** — pozwala Claude'owi czytać i pisać pliki w określonym katalogu (poza projektem CWD).

### Krok 1: Stwórz konfigurację MCP

W katalogu projektu lub `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/twoj_user/dokumenty"
      ]
    }
  }
}
```

`command` mówi Claude'owi jak uruchomić server (`npx -y` pobiera i odpala paczkę npm).
`args` to argumenty — dla filesystem to **dozwolony katalog** (Claude ma access tylko do niego, nie do całego dysku).

### Krok 2: Restart Claude Code

```bash
# zamknij Claude Code (Ctrl+C lub /exit)
claude
```

Przy starcie zobaczysz log: `MCP server "filesystem" connected — 5 tools available`.

### Krok 3: Test

```
> Wylistuj pliki w katalogu dokumenty i pokaż 3 najnowsze .md
```

Claude wywołuje `list_directory` i `read_file` przez filesystem MCP — dostajesz wynik bez wychodzenia poza chat.

To **wszystko**. 5 minut od zera do działającego MCP. Każdy kolejny server ma identyczny pattern.

---

## Top 10 MCP servers, które używam w Dokodu

Lista uporządkowana wg ROI / częstotliwości użycia w agencji AI.

### 1. Filesystem — czytanie/pisanie poza projektem

**Po co:** Claude domyślnie widzi tylko bieżący katalog (cwd). Filesystem MCP pozwala dotknąć innych — np. `~/Dokumenty/notatki/`, `/var/log/`, dysku zewnętrznego.

**Konfig (jak wyżej).**

**Use case:** czytanie meeting notes z Drive, modyfikacja plików w innym projekcie bez restartu Claude'a.

### 2. GitHub — full repo control

**Po co:** browse repo, czytaj issues, otwieraj PR, commentuj inline na PR-ach, sprawdzaj CI status.

**Konfig:**
```json
{
  "github": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-github"],
    "env": {
      "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxxxxxxxxxxxxxxxxx"
    }
  }
}
```

Token wygenerujesz na github.com → Settings → Developer settings → Personal access tokens (potrzebne `repo`, `workflow`, `issues`).

**Use case w Dokodu:**
- "Otwórz issue na repo blog z opisem buga w SEO_Ideas_Bank"
- "Sprawdź status CI ostatniego commita na main"
- "Zaproponuj review komentarze na PR #142"

### 3. Notion — pełen workspace access

**Po co:** Notion to centrum wiedzy w Dokodu (CRM, projekty, baza wiedzy). MCP daje pełen CRUD na strony i bazy.

**Konfig:** OAuth flow przy pierwszym połączeniu, Claude prowadzi przez kroki.

**Use case:**
- "Znajdź wszystkie strony w Notion z tagiem 'klient' i podsumuj statusy"
- "Dodaj nowy lead do bazy CRM z danymi z tej rozmowy"
- "Stwórz stronę meeting notes z dzisiejszą datą"

### 4. n8n — pełne CRUD na workflow automation

**Po co:** Claude może czytać, modyfikować, deploy'ować workflow n8n bez wychodzenia z czatu.

**Konfig:** wymaga API key z Twojego n8n (n8n.dokodu.it → Settings → n8n API).

**Use case** (z mojej praktyki):
- "Zbuduj workflow który czyta maila z Gmail, klasyfikuje przez Claude API i zapisuje lead do Notion CRM"
- "Sprawdź ostatnie 10 wykonań workflow X — czy są błędy?"
- "Dodaj webhook trigger do workflow Y"

W Dokodu mam **askprzed-write** policy dla n8n MCP — Claude nigdy nie zapisuje zmian bez mojego OK. Dla produkcyjnego n8n to absolutnie konieczne.

### 5. Linear — tickety i sprint planning

**Po co:** alternatywa dla Jira, zwięzła w użyciu. MCP daje pełen zestaw operacji.

**Use case:**
- "Pokaż otwarte ticki w sprincie X z priorytetem high"
- "Stwórz ticket: bug logout flow nie działa w Safari"
- "Update progress na ticket ABC-123"

### 6. Slack — czytanie + writing wiadomości

**Po co:** Slack to gdzie żyją prawdziwe rozmowy. MCP umożliwia kontekst kanału + posting.

**Use case:**
- "Sprawdź ostatnie 50 wiadomości w #engineering — czy ktoś pyta o API X?"
- "Wyślij notyfikację na #releases o deploy v2.5.3"
- "Wyciągnij decyzje z thread'a o nowej architekturze"

### 7. Postgres MCP — direct DB access

**Po co:** zapytania SQL do produkcyjnej bazy bez pisania osobnych queries.

**Konfig (read-only zalecane):**
```json
{
  "postgres-readonly": {
    "command": "npx",
    "args": [
      "-y",
      "@modelcontextprotocol/server-postgres",
      "postgresql://readonly_user:pass@host:5432/db"
    ]
  }
}
```

**KRYTYCZNE:** zawsze używaj **read-only usera** dla agentowych MCP. Pełen access dla agenta = ryzyko nieprzemyślanego DROP TABLE.

**Use case:**
- "Ile rejestracji było w ostatnich 7 dniach z każdego kraju?"
- "Pokaż top 10 najbardziej aktywnych userów wg liczby logowań"

### 8. Google Drive / Calendar / Gmail

**Po co:** ekosystem Google produktywności, jeśli żyjesz w Workspace.

**Konfig:** Anthropic ma natywne connectors w panelu (Settings → Connectors).

**Use case w Dokodu:**
- "Sprawdź mój kalendarz na jutro i sugeruj agenda do meetingów"
- "Wyciągnij nieprzeczytane maile od klientów z ostatnich 2 dni"
- "Otwórz dokument Drive 'Strategia 2026' i podsumuj sekcję pricing"

### 9. Anthropic API (search, computer use)

**Po co:** Anthropic udostępnia własne tools — search w internecie z kontekstem (różny od Brave/Google search), plus "computer use" do screenshotów / klikania UI.

**Use case:**
- "Wyszukaj najnowsze publikacje o AI Act compliance dla SaaS"
- "Zrób screenshot strony X i pokaż gdzie jest błąd UI"

### 10. Custom MCP — Twój własny

Najlepsze MCP to Twoje własne, dostosowane do Twojego biznesu. W Dokodu mamy custom MCP do:
- Synchronizacji Stripe → Notion CRM
- Querowania własnej bazy Pracuj.pl scrape'ów
- Łączenia Mailerlite stats z naszym dashboardem

Jak napisać własny MCP server: [Claude Agent SDK](https://docs.anthropic.com/) ma starter template w 5 językach (Python, TypeScript, Go, Rust, Ruby). Czas: 30 minut–2h zależnie od complexity.

---

## Bezpieczeństwo MCP — co MUSISZ wiedzieć

### 1. Każdy MCP ma uprawnienia

MCP server podłączony z full GitHub access **widzi cały Twój workspace** — produkcyjne repo, sekrety, historię zmian. Pierwsza zasada: **zawsze używaj minimum uprawnień**.

Przykład: dla GitHub MCP nie dawaj `repo:full`, tylko `repo:read` + `pull_requests:write`. Reszta operacji — manualnie.

### 2. Lokalne uruchomienie ≠ lokalne dane

MCP server działa lokalnie, ale **dane idą przez API serwisu** (Notion, GitHub, Slack). To są zewnętrzne usługi z własnymi politykami prywatności. Nie używaj MCP na produkcyjnych instancjach z PII bez weryfikacji.

### 3. Settings.local.json — gdzie żyją tokeny

Tokeny do MCP servers są zapisane w `~/.claude/mcp.json` lub `~/.claude/settings.json`. **Te pliki MUSZĄ być w `.gitignore`** — nie commit'uj nigdy.

Memorka dla Twojego repo:
```
# .gitignore
.claude/settings.local.json
.claude/mcp.json
```

### 4. AI Act compliance — audit log

Dla branż regulowanych (banki, prawo, healthcare) — MCP wymaga audit log każdego użycia. Anthropic Premium plan ma to wbudowane. Jeśli budujesz własny MCP server, **zaloguj każde wywołanie** (timestamp, tool, args, result, user).

### 5. Read vs write — domyślnie read

Większość MCP servers ma flagę "read-only mode". Zacznij **zawsze od read** — Claude czyta Notion, sprawdza tickety, wyświetla dane. Włącz write tylko gdzie świadomie potrzebujesz (i wtedy zazwyczaj z dodatkowym confirmation prompt).

---

## Top 5 errorów MCP i jak je rozwiązać

### Error: "MCP server failed to start"

**Diagnoza:** sprawdzić logi przy starcie Claude — pokazuje konkretny błąd. Zazwyczaj:
- Brakujący token w `env`
- Server nie znaleziony w npm (literówka)
- Niepoprawny path (np. filesystem MCP z nieistniejącym katalogiem)

### Error: "Tool not found" gdy próbuję użyć

MCP nie connectuje się przy starcie. Sprawdź `claude /mcp` — wylistuje wszystkie connected/failed servers.

### Error: "401 Unauthorized" przy każdej operacji

Token wygasł (typowe dla GitHub PAT po 90 dniach). Wygeneruj nowy, podstaw w `mcp.json`, restart Claude.

### Error: Server zaczął zwracać "rate limit"

Niektóre API (np. GitHub free tier — 5k req/h) mają twarde limity. Dla intensywnego usage rozważ upgrade tier serwisu lub batch'owanie zapytań.

### Server timeout na dużych zapytaniach

MCP standard ma default 30s timeout. Dla wolnych operacji (np. duża query Postgres) — zmień w settings.json:
```json
{
  "mcp": {
    "requestTimeout": 120000
  }
}
```

---

## Marketplace MCP servers (gdzie szukać gotowych)

- **[Anthropic MCP Servers (oficjalne)](https://github.com/modelcontextprotocol/servers)** — referencje, wzorce, ~20 oficjalnych
- **[Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)** — community list, 200+ serwerów
- **[Smithery](https://smithery.ai)** — marketplace + CLI installer

W skali tygodniowej w Dokodu używam ~5–7 MCP servers. Każdy zaoszczędza **godzinę–dwie pracy tygodniowo**.

---

## Co czytać dalej

- **[Claude Code — kompletny przewodnik 2026](/blog/claude-code)** — pillar
- **[Claude Code — cennik 2026](/blog/claude-code/cennik)** — który plan dla Twojego use case
- **[Claude Code — instalacja krok po kroku](/blog/claude-code/instalacja)** — od zera do działającej instalacji
- **[n8n self-hosted z Dockerem](/blog/n8n/docker-instalacja-konfiguracja)** — jeśli chcesz uruchomić n8n MCP server
- **[Agent AI dla firm — jak wdrożyć](/blog/agent-ai-dla-firm)** — pillar dla zarządu

<AD:n8n-workshop>

---

## FAQ — Claude Code MCP

**Czy MCP działa tylko z Claude'em?**

Standard jest open. W teorii każdy model (GPT, Gemini, lokalny LLM) może implementować MCP client. W praktyce — Claude jest pierwszy i najlepiej obsługuje MCP. Pozostałe stopniowo dodają wsparcie.

**Czy mogę napisać własny MCP server?**

Tak, w ~30 min. Anthropic ma starter templates: TypeScript, Python, Go, Rust. Specyfikacja JSON-RPC nad stdin/stdout — bardzo prosta.

**Czy MCP server jest bezpieczny — co widzi Anthropic?**

Tylko to co Claude potrzebuje do odpowiedzi. Wynik z `read_file` przechodzi przez Claude → Anthropic API → odpowiedź wraca. Reszta danych w MCP serverze nie jest wysyłana nigdzie.

**Czy MCP server konsumuje moje tokeny?**

Tak — każda komenda do MCP zwiększa context (Claude widzi `tool_call` + result). Większe operacje (np. SELECT z 1000 wierszy) zajadają sporo tokenów. Pisz queries z LIMIT.

**Co jeśli MCP server zhanguje?**

Claude detektuje timeout, abortuje wywołanie, kontynuuje konwersację z error info. Dla critical operations używaj retry z exponential backoff w MCP server (większość gotowych ma to wbudowane).

**Czy MCP działa offline?**

Sam server tak (lokalny). Ale jeśli MCP łączy się z external API (GitHub, Notion), bez internetu API zwraca błąd. Wyjątek: filesystem, sqlite, postgres lokalny — działają offline.

**Premium plan i MCP — co ekstra?**

Premium ma audit log wszystkich MCP calls + SSO. Jakość/funkcjonalność MCP servers identyczna na każdym planie.

---

*Lista MCP servers oparta na własnym użyciu w agencji AI Dokodu. Stan kwiecień 2026 — ekosystem szybko się rozwija, sprawdzaj najnowsze release na [Anthropic MCP](https://github.com/modelcontextprotocol/servers).*
