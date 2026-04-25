# Claude Code CLI — 15 komend i flag, które warto znać (2026)

Pomimo że Claude Code reklamuje się jako "agent autonomiczny", świadomość komend i flag CLI **drastycznie skraca pracę**. Przedstawię 15 najczęściej używanych komend, które oszczędzają mi godziny tygodniowo, plus konfigurację, którą trzymam w `~/.claude/settings.json`.

Pełny przegląd Claude Code w pillarze: [Claude Code — kompletny przewodnik 2026](/blog/claude-code).

---

## Podstawowe komendy startowe

### `claude`
Najprostsza komenda — startuje Claude Code w bieżącym katalogu (cwd). Otwiera interactive chat z dostępem do plików projektu.

```bash
cd ~/projekty/blog && claude
```

### `claude --version`
Sprawdza wersję CLI. Aktualizacje co 1-2 tygodnie — warto wiedzieć kiedy zaktualizować.

### `claude --help`
Pełna lista komend i flag. Pierwsza komenda do uruchomienia po świeżej instalacji.

### `claude logout`
Czyści zapisany token autoryzacji. Po tym kolejny `claude` poprosi o zalogowanie. Używaj gdy zmieniasz konto Anthropic lub chcesz zresetować problem z auth.

---

## Komendy chat-a (po starcie `claude`)

Wewnątrz interactive sesji masz dostęp do slashy:

### `/help`
Lista wszystkich slash commands dostępnych w aktualnym kontekście (pillar + custom skills + system).

### `/clear`
Czyści kontekst sesji. Używasz gdy zmieniasz temat — nowy task, świeży start, oszczędność tokenów.

### `/exit` (lub Ctrl+D)
Zamyka sesję. Token + memory są zapisane, kolejne `claude` startuje od nowa.

### `/mcp`
Wylistuje wszystkie aktywne MCP servers + ich tooli. Diagnoza gdy MCP nie działa.

### `/permissions`
Pokazuje aktualną listę allowed/denied actions. Odpowiednik `~/.claude/settings.json` w UI.

### `/model <nazwa>`
Przełącza model w trakcie sesji (`/model claude-opus-4-7` lub `/model claude-haiku-4-5`). Default zależy od planu.

### `/compact`
Kompresuje długą historię konwersacji do podsumowania. Używaj gdy konwersacja przekracza limit kontekstu.

---

## Custom slash commands (skills)

Każdy plik `.claude/skills/<nazwa>/SKILL.md` w projekcie staje się slash commandem `/<nazwa>`. W Dokodu mam:

- `/seo-plan-post`
- `/blog-draft`
- `/daily-briefing`
- `/yt-transcribe`
- `/brain-capture`
- ~30 innych

Wywołujesz: `/seo-plan-post n8n self-hosted` — Claude czyta SKILL.md, wykonuje workflow, zwraca wynik.

Pełen tutorial pisania custom skili: [Claude Code Skills — jak budować workflow](/blog/claude-code/skills).

---

## Najważniejsze flag CLI

### `claude --no-browser`
Autoryzacja bez otwierania przeglądarki. Pokazuje URL — kopiujesz, otwierasz na lokalnej maszynie, autoryzujesz, wklejasz token. **Niezbędne na Linux serwerach bez display** lub w WSL2 bez integracji.

### `claude --resume <session-id>`
Wraca do poprzedniej sesji. Sesje są zapisane w `~/.claude/sessions/`. Lista przez `claude --list-sessions`.

### `claude --print "<prompt>"`
**Non-interactive mode** — wywołuje Claude'a, dostaje odpowiedź, kończy. Idealne do automatyzacji (cron, CI):

```bash
claude --print "Sprawdź czy są błędy w kodzie i napisz raport" > raport.md
```

### `claude --dangerously-skip-permissions`
Wyłącza wszystkie pytania o pozwolenia. **Używaj OSTROŻNIE** — Claude może bez pytania uruchomić destrukcyjne komendy. Dobre dla CI gdzie chcesz pełną autonomię.

### `claude --add-dir <path>`
Dodaje extra katalog do kontekstu (poza cwd). Przydatne gdy projekt rozrzucony po wielu katalogach.

### `claude --no-tools`
Wyłącza wszystkie tooli — czysty chat bez file access, bash, MCP. Dla brainstorming bez ryzyka że Claude coś zrobi.

---

## Konfiguracja `~/.claude/settings.json` — co warto ustawić

Mój settings.json (uproszczony):

```json
{
  "defaultModel": "claude-opus-4-7",
  "permissions": {
    "allow": [
      "Bash(npm install:*)",
      "Bash(npm run *:*)",
      "Bash(git status:*)",
      "Bash(git diff:*)",
      "Bash(git log:*)",
      "Bash(git checkout *:*)",
      "Bash(pnpm *:*)",
      "Bash(python3 scripts/*:*)"
    ],
    "deny": [
      "Bash(rm -rf *:*)",
      "Bash(git push origin main:*)",
      "Bash(sudo *:*)",
      "Bash(curl * | bash:*)"
    ]
  },
  "hooks": [
    {
      "matcher": "Edit",
      "filePattern": "*.py",
      "command": "ruff format $FILE"
    }
  ],
  "memory": {
    "enabled": true,
    "directory": "~/.claude/memory"
  }
}
```

### Co ustawić jako default

- **`defaultModel`** — Opus dla complex tasków, Haiku dla high-volume. W Dokodu Opus dla wszystkiego (Max 5× plan absorbuje koszt).
- **`permissions.allow`** — komendy które chcesz bez pytania (Git status/diff/log to klasyk)
- **`permissions.deny`** — destruktywne (rm -rf, git push origin main, sudo)
- **`hooks`** — auto-formatowanie, lintowanie po Edit
- **`memory.enabled: true`** — auto-memory zapisuje user/feedback/project memories

---

## Power user combo — automatyzacja przez `--print` + cron

Najczęściej używana automatyzacja w Dokodu — codzienny commit'owalny raport stanu projektu:

```bash
#!/bin/bash
# scripts/daily-status.sh
cd ~/Projekty/dokodu-brain
claude --print "Sprawdź dziennik dziś — uruchamiałem jakieś deploye? Co zmieniłem? Zwróć raport markdown" > "daily-status-$(date +%F).md"
git add daily-status-*.md && git commit -m "chore: daily status $(date +%F)"
```

Cron (codziennie 18:00):
```cron
0 18 * * * /home/kacper/Projekty/dokodu-brain/scripts/daily-status.sh
```

Po tygodniu masz folder z 7 raportami — łatwiej widzisz pattern pracy.

---

## Najczęstsze błędy nowych userów CLI

### 1. Nie używanie `/clear`

Sesja trwa 4 godziny, kontekst zapchany 200k tokenów, każde nowe pytanie kosztuje. Po zmianie tematu — `/clear`.

### 2. Brak `CLAUDE.md`

Bez `CLAUDE.md` Claude pyta co projekt o każdą podstawową rzecz (jaki stack, jakie konwencje). **Pierwsze 30 minut po instalacji = napisz CLAUDE.md.**

### 3. Permissions na "allow all"

Niebezpieczne. Lepiej `allow` konkretne wzorce + `deny` destrukcyjne.

### 4. Nie używanie skills

99% userów Claude Code nie ma żadnego custom skilla. Tracą najpotężniejszą funkcję narzędzia.

### 5. Run `claude` z głównego `$HOME`

Claude czyta cwd jako "projekt". Z `$HOME` widzi wszystkie Twoje pliki — niepotrzebnie zwiększa kontekst i ryzyko.

---

## Co czytać dalej

- **[Claude Code — kompletny przewodnik 2026](/blog/claude-code)** — pillar
- **[Claude Code Skills — jak budować workflow](/blog/claude-code/skills)** — przy customowych komendach
- **[Claude Code — instalacja](/blog/claude-code/instalacja)** — od zera do działającego CLI
- **[Claude Code MCP — top 10 serwerów](/blog/claude-code/mcp)** — integracje zewnętrzne
- **[Claude Code — cennik 2026](/blog/claude-code/cennik)** — który plan dla CLI usage

<AD:kurs-n8n-waitlist>

---

## FAQ

**Czy `claude --print` zlicza się do limitu mojego planu?**

Tak. Każde wywołanie Anthropic API liczy się tak samo, niezależnie czy interactive czy non-interactive.

**Mogę uruchomić Claude w GitHub Actions?**

Tak — używasz `claude --print` w step CI. Token autoryzacji ustawiasz przez env var `ANTHROPIC_API_KEY`.

**Czy CLI ma autocomplete?**

Tak — instalacja generuje completion script. Dla zsh: `claude completion zsh > /usr/local/share/zsh/site-functions/_claude`. Tab-completion na slashy + flagi.

**Co jeśli Claude wykona `rm -rf` mimo `deny`?**

Permissions blokują **przed wykonaniem**. Jeśli komenda jest w `deny`, Claude pyta usera o override. Jeśli `--dangerously-skip-permissions` → **wszystko leci bez pytania**, więc używaj tylko w izolowanym środowisku (Docker, VM).

**Może mieć różne ustawienia per projekt?**

Tak. Każdy projekt może mieć własny `.claude/settings.json` (override globalnego `~/.claude/settings.json`).

---

*Komendy + flag-i z mojej praktyki w Dokodu, sprawdzone w wielu projektach. Stan kwiecień 2026.*
