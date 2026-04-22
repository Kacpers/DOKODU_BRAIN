# Broken Internal Links — dokodu.it
Wygenerowano: 2026-04-22 08:35

Łącznie unikalnych broken targets: **35**
- 🚫 Prawdziwe 404: **12** (trzeba naprawić lub usunąć linki)
- 🟢 Actually 200 OK: **23** (slug w DB out of sync, samo się naprawi po sync-full)
- ↪️ Redirecty 3xx: **0** (działają, ale update linków byłby lepszy)
- ⚠️ Errors: **0**

---

## 🚫 Prawdziwe 404 — DO NAPRAWY

Linki w treści postów wskazujące na nieistniejące URLe. **3 opcje:**
1. **Usunąć link** z treści linkujących postów (jeśli content był kiedyś, teraz nie ma)
2. **Opublikować target** (jeśli to draft który był planowany)
3. **Podmienić na inny post** (jeśli content przeniesiony/rebranded)

| Target | Refs | Z tych postów |
|--------|------|---------------|
| `/blog/wykorzystanie-generative-ai-w-automatycznym-generowaniu-kodu` | 2 | `automatyzacja-codziennych-zadan-jak-odzyskalem-czas-dla-siebie`, `generative-ai-w-grach-i-symulacjach` |
| `/blog/google-meet-transkrypcja` | 1 | `google-workspace/gemini-co-to-jest` |
| `/blog/google-docs-gemini` | 1 | `google-workspace/gemini-co-to-jest` |
| `/blog/gmail-gemini-ai-asystent` | 1 | `google-workspace/gemini-co-to-jest` |
| `/blog/agenci-ai/stable-diffusion-flux-lora-comfyui-rtx` | 1 | `agenci-ai` |
| `/blog/agenci-ai/rag-chatbot-n8n-qdrant` | 1 | `agenci-ai` |
| `/blog/agenci-ai/python-mcp-server-fast-mcp` | 1 | `agenci-ai` |
| `/blog/agenci-ai/mcp-n8n-claude-code-automatyzacja` | 1 | `agenci-ai` |
| `/blog/agenci-ai/lokalny-rag-rtx-5080-colqwen-lancedb` | 1 | `agenci-ai` |
| `/blog/agenci-ai/lokalny-asystent-ai-qwen3-cursor-docker` | 1 | `agenci-ai` |
| `/blog/agenci-ai/gemini-imagen-edycja-zdjec-n8n` | 1 | `agenci-ai` |
| `/blog/agenci-ai/agent-ai-wlasne-dane-n8n-gemini` | 1 | `agenci-ai` |

## 🟢 Actually OK (200) — Slug Mismatch w DB

Target URL zwraca 200 — czyli strona istnieje. Nasz `blog_articles` DB nie ma tego sluga
(prawdopodobnie inna struktura folderów). Najbliższy sync-full powinien to wyłapać.

| Target | Refs |
|--------|------|
| `/blog/tekstowe-modele-generatywne-gpt-i-inne` | 6 |
| `/blog/testowanie-jednostkowe-w-pythonie-wprowadzenie-do-unittest` | 4 |
| `/blog/integracja-generatorow-z-asynchronicznym-programowaniem-w-pythonie` | 4 |
| `/blog/regresja-liniowa-wprowadzenie` | 3 |
| `/blog/n8n-pierwsze-kroki-automatyzacja-bez-kodowania` | 3 |
| `/blog/docker-swarm-orkiestracja-kontenerow-na-wielu-hostach` | 3 |
| `/blog/docker-compose-ulatwienie-zarzadzania-wieloma-kontenerami` | 3 |
| `/blog/wprowadzenie-do-programowania-funkcyjnego-w-pythonie` | 2 |
| `/blog/tworzenie-aplikacji-webowych-w-pythonie-flask-czy-fastapi` | 2 |
| `/blog/sztuczna-inteligencja-jak-zaczac` | 2 |
| `/blog/sql-dla-poczatkujacych-roznice-mysql-postgresql-sqlite` | 2 |
| `/blog/rozpoznawanie-i-generowanie-mowy-z-ai` | 2 |
| `/blog/programowanie-obiektowe-w-pythonie-klasy-i-obiekty` | 2 |
| `/blog/porownanie-generatorow-z-innymi-wzorcami-projektowymi-w-pythonie` | 2 |
| `/blog/dockerfile-tworzenie-wlasnych-obrazow-dockera` | 2 |
| `/blog/dekoratory-w-pythonie-jak-i-kiedy-ich-uzywac` | 2 |
| `/blog/debugowanie-kontenerow-docker-najlepsze-narzedzia` | 2 |
| `/blog/bezpieczenstwo-w-dockerze-best-practices` | 2 |
| `/blog/zarzadzanie-kontenerami-skalowanie-i-monitoring` | 1 |
| `/blog/zaawansowane-techniki-w-dockerze-multi-stage-builds` | 1 |
| `/blog/praca-z-woluminami-w-dockerze-przechowywanie-danych` | 1 |
| `/blog/instalacja-dockera-na-roznych-systemach-operacyjnych` | 1 |
| `/blog/generative-ai-w-nauce-symulacje-i-modelowanie` | 1 |

---
*Broken Links Report | 2026-04-22 08:35*