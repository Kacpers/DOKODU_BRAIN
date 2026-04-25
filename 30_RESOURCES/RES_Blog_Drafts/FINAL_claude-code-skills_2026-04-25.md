# Claude Code Skills — jak budować własne workflow AI (2026)

Skills to **najsilniejsza funkcja Claude Code, którą najmniej developerów używa**. Pozwala kodyfikować powtarzalne workflow w plikach markdownowych — Claude czyta je, wykonuje, nie musisz powtarzać kontekstu. W tym artykule pokażę dokładnie czym są Skills, jak napisać pierwszy w 10 minut i jakie skille mam w Dokodu (z konkretnymi nazwami i triggerami).

Pełen kontekst Claude Code — w pillarze: [Claude Code — kompletny przewodnik 2026](/blog/claude-code).

---

## Co to jest Claude Code Skill?

**Skill** to katalog z plikiem `SKILL.md` zawierającym instrukcję workflow. Claude czyta ten plik, wykonuje krok po kroku, używa dostępnych narzędzi (filesystem, MCP, Bash). Wywołujesz przez slash command — `/<nazwa-skilla>`.

W praktyce skill wygląda tak:

```
.claude/skills/seo-plan-post/
└── SKILL.md
```

I plik `SKILL.md`:

```markdown
---
name: seo-plan-post
description: Planuje artykuł SEO dla dokodu.it od keyword do briefu. Trigger: "zaplanuj post", /seo-plan-post
---

# Instrukcja: SEO Plan Post

## KROK 1: Zbierz dane wejściowe
[Claude pyta usera o keyword, intent, persona]

## KROK 2: Sprawdź GSC
```bash
python3 scripts/gsc_fetch.py --query [keyword]
```

## KROK 3: Web research
WebSearch top 3 wyniki Google PL...

## KROK 4: Generuj brief
[Strukturalny brief — meta, H2, hook, CTA, linki wewnętrzne]
```

Wywołanie:
```
> /seo-plan-post n8n self-hosted
```

Claude czyta `SKILL.md`, wykonuje 4 kroki, zwraca brief. Bez powtarzania "zrób research SEO + brief" co tydzień.

---

## Dlaczego Skills zmieniają zasady gry

### 1. Wiedza zostaje w repo

Twoje najlepsze prompty żyją w plikach commitowalnych do Git. Następny developer (lub Ty za 3 miesiące) odpala ten sam workflow bez przypominania sobie "jak to było".

### 2. Reusability across projektów

Skill `code-reviewer` napisany raz działa we wszystkich Twoich projektach. Importujesz przez kopiowanie katalogu `.claude/skills/code-reviewer/`.

### 3. Złożoność workflow bez kompliki promptów

Bez skilla: wpisujesz 200-słowny prompt z 7 krokami za każdym razem.
Ze skillem: wpisujesz `/cleanup-branches`. Claude wie reszty.

### 4. Versioning + team alignment

Skill jest pod Git — widać kto, kiedy, dlaczego zmienił workflow. Cały zespół ma ten sam standard pracy.

### 5. Współpraca z Hooks i MCP

Skills mogą wywoływać MCP servers, używać Bash, czytać pliki przez filesystem. Pełna automatyzacja bez kodu.

---

## Pierwsza Skill w 10 minut — `cleanup-branches`

Pokażę krok po kroku jak napisać skill, który czyści mergeowane branche.

### Krok 1: Stwórz katalog

```bash
mkdir -p .claude/skills/cleanup-branches
```

### Krok 2: Stwórz `SKILL.md`

```markdown
---
name: cleanup-branches
description: Usuwa lokalnie zmergeowane feature branche (zostawia main/master). Pokazuje listę przed usunięciem, prosi o potwierdzenie. Trigger: "wyczyść branche", "cleanup branches", /cleanup-branches
---

# Instrukcja: Cleanup Branches

## KROK 1: Sprawdź obecny branch

Wykonaj `git branch --show-current`. Jeśli nie jest to `main` lub `master` — zatrzymaj i poproś użytkownika o przejście na main:
```bash
git checkout main && git pull
```

## KROK 2: Pobierz listę zmergeowanych branch'y

```bash
git branch --merged main | grep -v "^\*" | grep -vE "(main|master|develop)"
```

## KROK 3: Pokaż listę użytkownikowi

Wypisz każdy branch w formie:
- `feat/old-stuff` (last commit: 2 weeks ago)

Zapytaj: "Usunąć te X branch-y? (tak/nie)"

## KROK 4: Po potwierdzeniu — usuń

```bash
git branch -d <branch-name>
```

Dla każdego z listy. Loguj wynik.

## KROK 5: Sprawdź czy są też zdalne do usunięcia

```bash
git remote prune origin
```

Wyświetl ile zostało wyczyszczone.
```

### Krok 3: Test

W terminalu (z otwartym Claude Code w tym repo):
```
> /cleanup-branches
```

Claude czyta SKILL.md, wykonuje 5 kroków, czyści branche.

---

## 10 Skills, które używam w Dokodu

Pokażę realną listę z mojego repo dokodu-brain — niektóre proste, niektóre złożone.

### 1. `/seo-plan-post` (planowanie SEO)
Od keyword do pełnego briefu produkcyjnego (meta, struktura H2, hook, CTA, linki wewnętrzne). 5 kroków, ~150 linii instrukcji. **Najczęściej używany skill — 3-5× w tygodniu.**

### 2. `/blog-draft` (pisanie + publish draft)
Bazuje na briefie z `/seo-plan-post`, generuje content markdown w TOV Dokodu, wgrywa jako draft do CMS przez API. Średni czas: 8-12 minut.

### 3. `/daily-briefing` (codzienny radar)
Skanuje rano: Reddit (16 subreddit-ów), HackerNews, GSC, Gmail unread, Calendar. Zwraca temat na film YouTube + 2-3 pomysły shorts + blog idea + lead signals.

### 4. `/seo-stats` (analiza GSC)
Pobiera dane z Google Search Console (28 dni), analizuje quick wins, content gaps, niski CTR. Zapisuje raport do `SEO_Insights.md`.

### 5. `/yt-transcribe` (Whisper na nagraniu YT)
Bierze plik MP4, odpala Whisper, generuje napisy SRT, opis YouTube + tagi, post LinkedIn. Pełen pipeline od nagrania do publish-ready content.

### 6. `/brain-capture` (szybki dump)
Najprostszy skill — dodaje notatkę/pomysł do `00_INBOX.md` z timestampem. Zero overhead.

### 7. `/brain-prep-call` (przygotowanie do meeting)
Ładuje profil klienta z `AREA_Customers/`, generuje pytania discovery, identifikuje buying signals, planuje przebieg rozmowy.

### 8. `/code-reviewer` (subagent code review)
Po większym zadaniu wywołuję — sprawdza kod przeciwko CLAUDE.md, security, test coverage, potencjalne bugi.

### 9. `/deploy` (deploy aplikacji)
Robi `git push do main`, czeka na GitHub Actions, sprawdza health check po deployu, raportuje status.

### 10. `/n8n-build-workflow` (custom MCP + skill combo)
Najbardziej złożony — kombinuje skill z MCP n8n. Bierze prozaiczny opis ("workflow który czyta maila i klasyfikuje"), buduje JSON workflow, validuje, wgrywa do n8n.

---

## Skills vs Hooks vs MCP — kiedy co

| Funkcja | Co robi | Kiedy używać |
|---------|---------|--------------|
| **Skill** | Wieloetapowy workflow uruchamiany przez `/<nazwa>` | Powtarzalne zadania ("zaplanuj post", "deploy") |
| **Hook** | Auto-trigger przy zdarzeniu (Edit, Write, Stop) | Auto-formatowanie, walidacje, notyfikacje |
| **MCP** | Podłączenie zewnętrznego API jako narzędzia | Integracje (Notion, GitHub, n8n, DB) |

W praktyce — **skills + MCP to combo killer**. Twój skill `/build-workflow` używa MCP `n8n` żeby wgrać workflow + MCP `notion` żeby zapisać dokumentację. Wszystko orkiestrowane jednym slashem.

---

## Anatomia dobrego skilla

### 1. Frontmatter z `name` + `description`

`description` ma trigger words ("zaplanuj post", "/skill-name") — Claude rozpoznaje że ma uruchomić ten skill bazując na opisie.

### 2. Krótki nagłówek z celem

Dwa zdania na początku: **co skill robi i kiedy się aplikuje**.

### 3. Kroki numerowane (KROK 1, KROK 2...)

Claude wykonuje sekwencyjnie, nie improwizuje. Każdy krok = jedna konkretna akcja.

### 4. Bash commands w blokach kodu

Bez ambiguity — Claude wie dokładnie jaką komendę odpalić.

### 5. Zakończenie z konkretnym output

Ostatni krok zawsze: "Wypisz wynik w formacie X" lub "Zapytaj usera czy potwierdza Y". Bez tego Claude może dryfować.

### 6. Granice — co skill **NIE** robi

Sekcja "Out of scope" — np. dla `/seo-plan-post`: "NIE pisze samego artykułu — tylko brief. Pisanie = `/blog-draft`".

---

## Najczęstsze błędy przy pisaniu skilli

### 1. Za długie / za krótkie

Optymalna długość: **80–250 linii**. Krótszy = za mało kontekstu. Dłuższy = Claude gubi się.

### 2. Brak placeholdera dla user input

Skill `/seo-plan-post` bez kroku "zapytaj o keyword" — Claude próbuje zgadnąć temat. Zawsze włącz **interaktywne kroki**.

### 3. Hardcoded paths

Zamiast `/Users/kacper/projekty/blog` używaj `$HOME/projekty/blog` lub względnych ścieżek. Inaczej skill nie działa na innym setupie.

### 4. Brak error handling

Co Claude ma zrobić jak `git push` faluje? Pisz: "Jeśli krok X faluje — zatrzymaj się i powiedz userowi co się stało."

### 5. Powtarzanie tego co Claude już wie

Skille typu "Czytaj plik X, parse JSON, wypisz Y" są zbędne — Claude to robi natywnie. Skille rób na **złożone, multi-step workflow**.

---

## Skills marketplace — gdzie znaleźć gotowe

- **Anthropic Cookbook** — oficjalne examples skilli na GitHub
- **awesome-claude-skills** — community list, ~50 skilli
- **Twoje repo** — najlepsze skille piszesz Ty pod swój workflow

W Dokodu mamy ~30 customowych skilli + kilka adoptowanych z awesome-claude-skills (np. `meeting-insights-analyzer`, `lead-research-assistant`).

---

## Co czytać dalej

- **[Claude Code — kompletny przewodnik 2026](/blog/claude-code)** — pillar (czym jest, vs Cursor, MCP)
- **[Claude Code — instalacja krok po kroku](/blog/claude-code/instalacja)** — od zera do działającego CLI
- **[Claude Code — cennik 2026](/blog/claude-code/cennik)** — który plan dla intensywnego usage
- **[Claude Code MCP — top 10 serwerów](/blog/claude-code/mcp)** — bo skille często używają MCP
- **[Agent AI dla firm](/blog/agent-ai-dla-firm)** — pillar dla zarządu

<AD:kurs-n8n-waitlist>

---

## FAQ — Claude Code Skills

**Czy skille działają w VS Code extension?**

Tak. Identyczny syntax `.claude/skills/<nazwa>/SKILL.md`. Slash command `/<nazwa>` działa w panelu Claude w VS Code.

**Czy mogę mieć global skille (poza projektem)?**

Tak — `~/.claude/skills/` jest globalny dla wszystkich projektów. Per-project: `.claude/skills/` w katalogu projektu.

**Czy skill może wywoływać inny skill?**

Tak — w SKILL.md możesz napisać "Wykonaj `/inny-skill`". Claude obsługuje to natywnie.

**Skill plus subagent — czym się różni?**

Skill to instrukcja dla głównej rozmowy. Subagent to **odrębna sesja** odpalana z dedykowanym kontekstem (np. `code-reviewer`). Skill = continuous, subagent = isolated.

**Czy skill może zapisywać dane między sesjami?**

Tak — używaj plików (np. `~/.claude/state/skill-name.json`) lub MCP servers ze state (np. SQLite, Postgres). Skill sam nie ma persistent state, ale może użyć tooli.

---

*Lista skilli z Dokodu — żywa, aktualizowana co tydzień. Pełne źródła w [repo brain-public](https://github.com/Kacpers/DOKODU_BRAIN). Tutorial powstał z użyciem Claude Code (Opus 4.7).*
