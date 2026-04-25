# Claude Code — instalacja krok po kroku (macOS, Linux, Windows) — 2026

Ten przewodnik prowadzi Cię od zera do działającego Claude Code w terminalu w mniej niż 10 minut. Pokażę dokładne komendy dla **macOS**, **Linux** i **Windows (WSL2)** plus rozwiązania najczęstszych błędów, na które natknąłem się ja sam i developerzy w Dokodu.

Jeśli zastanawiasz się **czym właściwie jest Claude Code**, zacznij od pełnego przewodnika: [Claude Code — kompletny przewodnik 2026](/blog/claude-code).

---

## Wymagania systemowe (zanim cokolwiek instalujesz)

Sprawdź czy spełniasz minimum:

- **macOS 13.0 Ventura albo nowszy** (Sonoma/Sequoia idealne) lub **Linux** (Ubuntu 22.04+, Debian 12+, Fedora 39+, większość modernych dystrybucji) lub **Windows 10/11 z zainstalowanym WSL2**
- **Node.js 18 lub nowszy** — Claude Code instaluje się przez npm
- **Konto Anthropic** — założenie darmowe na [console.anthropic.com](https://console.anthropic.com), plan płatny (od $20/mc Pro) potrzebny dopiero do faktycznego użycia
- **Co najmniej 2 GB wolnej pamięci RAM** — dla większych projektów (>100 MB codebase) lepiej 4–8 GB

**Pamiętaj:** sam Claude Code ma minimalne wymagania. Co go obciąża to **kontekst projektu** który wczytuje. Dla projektu w 100k linii kodu RAM-u mocno się kurczy.

---

## Sprawdź Node.js (5 sekund)

W terminalu:

```bash
node --version
```

Wynik typu `v18.x.x`, `v20.x.x` lub `v22.x.x` = OK. Jeśli `command not found` lub wersja niższa niż 18 — zainstaluj/zaktualizuj Node.

### Jak zainstalować/zaktualizować Node.js

**macOS (Homebrew):**
```bash
brew install node
```

**Linux (przez nvm — rekomendacja):**
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
# zamknij i otwórz terminal
nvm install 22
nvm use 22
```

**Windows (WSL2):**
W WSL2 użyj tej samej komendy nvm co w Linuxie. Nie instaluj Node natywnie w PowerShell — większość AI developer tools radzi sobie znacznie lepiej w środowisku Unix.

---

## Instalacja Claude Code

Jedna komenda, ten sam syntax dla wszystkich systemów:

```bash
npm install -g @anthropic-ai/claude-code
```

Co się dzieje:
- npm pobiera oficjalny pakiet z npmjs.com
- Instaluje binarkę `claude` w globalnym katalogu npm
- Dodaje do `$PATH` automatycznie (jeśli npm jest poprawnie skonfigurowany)

Test instalacji:

```bash
claude --version
```

Jeśli widzisz numer wersji typu `1.x.x` — gotowe. Jeśli `command not found` → patrz "Najczęstsze błędy" poniżej.

---

## Pierwsze uruchomienie + autoryzacja

W terminalu, w katalogu projektu:

```bash
cd ~/projekty/twoj-projekt
claude
```

Co się dzieje przy pierwszym razie:

1. CLI wykrywa brak tokena auth
2. Otwiera przeglądarkę z URL na `auth.anthropic.com`
3. Logujesz się do swojego konta Anthropic
4. Klikasz "Authorize"
5. Token wraca do CLI, zostaje zapisany lokalnie w `~/.claude/auth.json` (lub podobnym, zależnie od OS)
6. CLI pokazuje "Welcome to Claude Code"

Token żyje miesiącami — kolejne uruchomienia `claude` startują natychmiast bez logowania.

### Pierwsza komenda (test że wszystko działa)

W oknie czatu Claude wpisz:

```
Pokaż mi strukturę tego projektu i wyjaśnij co tu jest
```

Claude wykonuje `ls -la`, czyta kluczowe pliki (`package.json`, `README.md`, `Cargo.toml`, etc.), buduje obraz projektu i zwraca opis. Jeśli to widzisz — jesteś w grze.

---

## Konfiguracja projektu — `CLAUDE.md`

To **najważniejszy plik** który dorzucisz. `CLAUDE.md` w katalogu głównym projektu jest czytany przy każdym otwarciu — Claude wie kontekst, konwencje i Twoje zasady bez powtarzania ich co sesję.

Stwórz plik `CLAUDE.md`:

```markdown
# CLAUDE.md

## O projekcie
Aplikacja [Twoja firma] — system do [krótki opis]. 
Stack: TypeScript, Next.js 15, PostgreSQL, Prisma, Tailwind.
Architektura: monorepo z apps/ i packages/.

## Konwencje kodu
- Używamy TypeScript strict
- ESLint + Prettier (config w root)
- Testy w Jest, target 80% coverage na utility libs
- Komentarze tylko gdy biznesowy why nie jest oczywisty

## Branching i PR
- Feature branch z `feat/nazwa-feature`
- Squash merge tylko
- Każdy PR musi mieć test (chyba że to docs)

## Co powinno być oczywiste
- Sekrety w `.env.local` (gitignored), produkcyjne w Vercel env vars
- Build: `pnpm build`, test: `pnpm test`, deploy: GitHub Actions

## Zasady
- NIE commit'uj do main bezpośrednio (brak permisji)
- Przy refactorach: backupuj przed (`git stash` lub branch)
- Krytyczne ścieżki w API mają testy integracyjne (nie tylko unit)
```

Kacper z Dokodu ma w `CLAUDE.md` projektu blog'a m.in. zasadę "każdy post musi mieć featured image, mermaid, 4-6 linków wewnętrznych" — Claude czyta to przy każdym pisaniu artykułu i nie pyta więcej.

---

## Najczęstsze błędy instalacji i jak je rozwiązać

### "command not found: claude" po `npm install -g`

Twój globalny npm path nie jest w `$PATH`. Sprawdź:

```bash
npm config get prefix
# typowo: /usr/local lub /opt/homebrew (macOS) lub /home/user/.npm-global (Linux)

echo $PATH | tr ':' '\n' | grep -i npm
```

Jeśli wynik pusty — dodaj do `.zshrc` (macOS) lub `.bashrc` (Linux):

```bash
export PATH="$(npm config get prefix)/bin:$PATH"
```

Restart terminala i `claude --version` powinno działać.

### "EACCES: permission denied" przy npm install -g

Twój system nie pozwala instalować globalnie bez `sudo`. Dwa rozwiązania (drugie znacznie lepsze):

**Złe (działa, ale pułapka):**
```bash
sudo npm install -g @anthropic-ai/claude-code
```

**Dobre (zmień konfigurację):**
```bash
# Zmień npm prefix na user-owned katalog
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.zshrc  # lub ~/.bashrc
source ~/.zshrc
npm install -g @anthropic-ai/claude-code
```

To koniec problemów z permission errors w przyszłości dla wszystkich pakietów npm.

### "401 Unauthorized" w aplikacji po zalogowaniu

Token się rozjechał. Wyczyść i autoryzuj ponownie:

```bash
rm ~/.claude/auth.json
claude
# otworzy ponownie autoryzację w przeglądarce
```

### Browser nie otwiera się przy autoryzacji (Linux serwer / WSL bez display)

```bash
claude --no-browser
# wypisze URL — skopiuj, otwórz na lokalnej maszynie, zalogowuj
```

Po zalogowaniu CLI poprosi o token — wklejasz i działa.

### Windows PowerShell: "Cannot run script because running scripts is disabled"

PowerShell domyślnie blokuje zewnętrzne skrypty. W PowerShell jako admin:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Restart PowerShell, `claude` zadziała. **Lepsze rozwiązanie:** zainstaluj WSL2 i pracuj w Ubuntu — Claude Code działa znacznie lepiej w środowisku Linuxowym.

### Bardzo wolne uruchomienie / "Loading project..."

Projekt ma za dużo plików, które Claude próbuje zindeksować. Stwórz `.claudeignore` (analogiczny do `.gitignore`):

```
node_modules/
.next/
dist/
build/
*.log
.git/
public/uploads/
data/snapshots/
```

Restart Claude Code — startuje pod sekundę.

---

## Aktualizacja Claude Code

Anthropic wypuszcza nowe wersje co 1-2 tygodnie. Sprawdź czy masz aktualną:

```bash
claude --version
npm view @anthropic-ai/claude-code version
```

Jeśli się różnią — update:

```bash
npm install -g @anthropic-ai/claude-code@latest
```

Major version (np. `1.x` → `2.x`) może wymagać regeneracji `~/.claude/settings.json` — Claude poprosi przy pierwszym uruchomieniu.

---

## Konfiguracja zaawansowana (opcjonalnie)

Po pierwszej działającej instalacji, te 3 rzeczy warto skonfigurować od razu:

### 1. Permissions (kontrola co Claude może)

Plik `~/.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(npm install:*)",
      "Bash(npm run *:*)",
      "Bash(git status:*)",
      "Bash(git diff:*)",
      "Bash(git log:*)"
    ],
    "deny": [
      "Bash(rm -rf *:*)",
      "Bash(git push origin main:*)",
      "Bash(sudo *:*)"
    ]
  }
}
```

Claude pyta o zgodę przy każdej akcji która nie pasuje do `allow`. Akcje z `deny` są blokowane całkowicie.

### 2. Model preference

Domyślnie używa Opus 4.6 lub 4.7 (zależnie od planu). Jeśli chcesz wymusić tańszy:

```json
{
  "defaultModel": "claude-haiku-4-5"
}
```

Haiku 4.5 jest 5–10× tańszy niż Opus, kosztem trochę gorszego rozumienia kontekstu. Dla większości codziennych tasków wystarczy.

### 3. MCP servers (zewnętrzne narzędzia)

Edytuj `~/.claude/mcp.json` lub `.claude/mcp.json` w projekcie:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/twoj_user/projekty"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxxxxxxx"
      }
    }
  }
}
```

Po restarcie Claude Code masz dostęp do GitHub API + filesystem przez MCP. Pełna lista 50+ MCP serwerów: [Claude Code MCP — co to i jak skonfigurować](/blog/claude-code/mcp).

---

## Podsumowanie — checklist po instalacji

- [x] Node.js 18+ zainstalowany
- [x] `npm install -g @anthropic-ai/claude-code` przeszło bez błędu
- [x] `claude --version` zwraca numer
- [x] Pierwszy `claude` w terminalu autoryzował się przez przeglądarkę
- [x] `CLAUDE.md` w głównym katalogu projektu z opisem stacka i konwencji
- [x] (Opcjonalnie) `~/.claude/settings.json` z `permissions`
- [x] (Opcjonalnie) `.claudeignore` jeśli projekt ma >5 GB / >50k plików
- [x] (Opcjonalnie) MCP servers dla narzędzi zewnętrznych

W praktyce: 5–10 minut od `npm install -g` do pierwszej działającej komendy. Kolejny krok: poznaj **5 funkcji game-changer** w pełnym przewodniku [Claude Code — kompletny przewodnik 2026](/blog/claude-code).

---

## Co czytać dalej

- **[Claude Code — kompletny przewodnik 2026](/blog/claude-code)** — pillar z porównaniem Claude Code vs Cursor vs Copilot, cennikiem, 5 funkcji game-changer i 5 use case'ów z agencji AI
- **[Claude Code — cennik 2026 (Pro/Max/Premium)](/blog/claude-code/cennik)** — szczegółowy breakdown planów, kalkulator ROI dla developera w PL
- **[Claude Code MCP — top 10 serwerów i jak je skonfigurować](/blog/claude-code/mcp)** — Notion, Slack, GitHub, Linear, n8n, Postgres
- **[n8n self-hosted z Dockerem — tutorial 2026](/blog/n8n/docker-instalacja-konfiguracja)** — jeśli chcesz zintegrować Claude Code z workflow automation

<AD:kurs-n8n-waitlist>

---

## FAQ

**Czy mogę zainstalować Claude Code bez konta Anthropic?**

Nie. CLI bez tokena nie startuje — autoryzacja jest wymagana przy pierwszym uruchomieniu. Konto Anthropic darmowe, plan płatny od $20/mc.

**Czy Claude Code działa offline?**

Sam CLI startuje bez internetu, ale każde zapytanie idzie do API Anthropic. Bez połączenia z internetem dostaniesz timeout. Workaround: Ollama + lokalny model jako fallback (jakość spada).

**Ile zajmuje sama instalacja na dysku?**

CLI sam ~50 MB. Dependencies + cache npm: dodatkowe ~200 MB. Razem do 300 MB. Pojedynczy projekt z dużym kontekstem może chwilowo cache'ować dodatkowe 100–500 MB.

**Mogę używać Claude Code w VS Code zamiast terminala?**

Tak. Anthropic ma oficjalne extension `Claude Code` w VS Code Marketplace (od grudnia 2025). Po instalacji w sidebarze masz panel Claude — wszystkie funkcje CLI plus wizualny diff. Konfiguracja `CLAUDE.md` i `permissions` współdzielona z CLI.

**Czy mogę mieć dwa różne projekty z różnymi `CLAUDE.md`?**

Tak. `CLAUDE.md` jest **per katalog projektu**. Claude czyta ten z bieżącego katalogu (cwd) przy starcie. Plus może być globalny `~/.claude/CLAUDE.md` — wspólny dla wszystkich projektów.

**Co jeśli zgubiłem token i nie mam dostępu do email?**

Wpisz `claude logout` (czyści lokalny token), potem `claude` ponownie — autoryzacja od zera. Jeśli nie pamiętasz emaila konta Anthropic — skontaktuj się z [support Anthropic](https://support.anthropic.com).

---

*Artykuł napisany przez Kacpra Sieradzińskiego, CEO Dokodu. Tutorial bazowany na własnej instalacji Claude Code w marcu 2026 + setupie w 30+ projektach klientów. Powstał przy użyciu Claude Code (Opus 4.7).*
