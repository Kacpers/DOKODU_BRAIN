---
type: refresh_brief
status: BRIEF
target_url: /blog/n8n/docker-instalacja-konfiguracja
existing_words: 16282
existing_rank: 3
existing_keyword: n8n docker (590 vol)
new_target_keyword: n8n self-hosted (780 vol) + n8n docker (590 vol) — DUAL targeting
total_target_volume: 1370
priority: high
effort: 1 dzień
risk: low (nie zmieniamy URL — autorytet zostaje)
created: 2026-04-25
target_publish: 2026-05-02
research_pool: RESEARCH_n8n-self-hosted_content-pool_2026-04-25.md
---

# REFRESH BRIEF: `/blog/n8n/docker-instalacja-konfiguracja`

> Cel: rozszerzyć już rankujący artykuł (#3 na "n8n docker") tak żeby DODATKOWO celował w `n8n self-hosted` (780 vol). 1 artykuł, 2 frazy, 1 370 vol/mc total.

---

## Status istniejącego artykułu

- **URL:** https://dokodu.it/blog/n8n/docker-instalacja-konfiguracja
- **Aktualny H1:** "n8n i Docker – instalacja i konfiguracja krok po kroku"
- **Słów:** 16 282 (już duży pillar)
- **Ranking PL:** #3 na "n8n docker" (590 vol)
- **Istniejące H2:**
  1. Dlaczego warto uruchomić n8n w Dockerze?
  2. Szybki start: Uruchomienie n8n w Dockerze (dla początkujących)
  3. Utrwalanie danych i wydajność: zewnętrzna baza PostgreSQL
  4. Dodanie serwera proxy i HTTPS (Nginx + Certbot)
  5. Dodatkowe usługi towarzyszące
  6. Wskazówki i najlepsze praktyki

## Co konkretnie zmienić — patch list

### 1. Title + Meta (KRYTYCZNE — 5 min, największy efekt)

| Pole | OBECNIE | NOWY |
|------|---------|------|
| **H1** | n8n i Docker – instalacja i konfiguracja krok po kroku | **n8n self-hosted z Dockerem — kompletny tutorial 2026** |
| **SEO Title** | (sprawdź w meta) | **n8n self-hosted z Dockerem — tutorial 2026 \| Dokodu** |
| **Meta Description** | (sprawdź) | Pełny przewodnik n8n self-hosted z Dockerem — Postgres, Nginx/Caddy, SSL, backup. Krok po kroku w 30 minut. Z kodem KACPER10 -10%. |
| **Slug** | docker-instalacja-konfiguracja | **NIE ZMIENIAĆ** — zachowuje #3 ranking |

### 2. Dodać 2 nowe sekcje (~1 200 słów)

#### A. NOWA H2: "Caddy zamiast Nginx — szybsza alternatywa SSL" (~500 słów)
Wstawić **po** istniejącej sekcji 4 ("Dodanie serwera proxy i HTTPS — Nginx + Certbot").

Treść do skopiowania z `RESEARCH_n8n-self-hosted_content-pool_2026-04-25.md` → sekcja "H2: Krok 5 — Caddy + automatyczne SSL". Plus:
- Tabela porównawcza Nginx + Certbot **vs** Caddy (5 wierszy: linie configa, czas setup, auto-renewal, security headers, krzywa nauki)
- Code block: `Caddyfile` (3 linie!) + `docker-compose.yml` Caddy service
- "Dlaczego Caddy:" — auto-Let's Encrypt out of the box, zero cron, security headers domyślne

#### B. NOWA H2: "n8n self-hosted vs Cloud — kiedy się opłaca" (~400 słów)
Wstawić **po** sekcji 1 ("Dlaczego warto uruchomić n8n w Dockerze?").

Treść:
- Tabela 8-wierszowa Cloud vs Self-hosted (z research pool)
- 3 use cases dla self-hosted (compliance RODO/AI Act, > 10k wykonań/mc, on-prem ERP/CRM)
- 2 use cases dla Cloud (solo, < 1k wykonań/mc)
- Link wewn.: "Pełny breakdown cen → /blog/n8n/licencja-cennik"

#### C. NOWA H3: "AI Act compliance dla n8n self-hosted" (~300 słów)
Wstawić **w sekcji 6** ("Wskazówki i najlepsze praktyki") jako podsekcja.

Treść:
- `N8N_AUDIT_LOGS=true` + retention policy
- PII masking w logach (Code Node)
- Egress whitelisting (UFW + Cloudflare WAF)
- Link wewn.: "Pełny audit bezpieczeństwa → /blog/n8n/self-host-bezpieczenstwo"
- Link wewn.: "Webhook security → /blog/n8n/webhook-bezpieczenstwo-throttling"

### 3. Dodać Box afiliacyjny KACPER10 (3 miejsca)

#### Miejsce 1: w sekcji "Wybór hostingu" (jeśli nie ma — dodaj nową H3 do sekcji 2)
```markdown
### Wybór hostingu — co używam

Postawiłem n8n.dokodu.it na **Hostinger VPS** (KVM 2 = 4 GB RAM, 2 vCPU, 80 GB NVMe).
Wystarcza na kilka tysięcy wykonań dziennie + jest najtańszy w PL z dobrym supportem.

> 🔥 **Z kodem KACPER10 dostajesz -10% na Hostinger VPS** → [hostinger.com/kacper10](https://www.hostinger.com/kacper10)
>
> *Disclosure: To link afiliacyjny — używam Hostingera produkcyjnie i polecam z autopsji.
> Klikając wesprzesz Dokodu prowizją (a Ty masz -10%).*

**Alternatywy** (porównanie cen w PLN, 2026):
| Hosting | Plan | RAM | vCPU | Cena/mies. (PLN) |
|---------|------|-----|------|------------------|
| **Hostinger VPS KVM 2** | KVM 2 | 4 GB | 2 | ~30 zł (z KACPER10) |
| Hetzner Cloud CX22 | CX22 | 4 GB | 2 | ~20 zł (€4,35) |
| DigitalOcean | Basic | 4 GB | 2 | ~100 zł ($24) |
| OVH VPS Value | Value | 4 GB | 2 | ~50 zł |
```

#### Miejsce 2: na końcu artykułu (przed Tagami)
Box końcowy z research pool → sekcja "Box afiliacyjny" (kompletny markdown gotowy do wklejenia).

### 4. Atrybuty linków afiliacyjnych

Każdy `<a href="https://www.hostinger.com/kacper10">` MUSI mieć:
```html
<a href="https://www.hostinger.com/kacper10" rel="sponsored nofollow" target="_blank">
```

Sprawdź czy `blog_publish.py` to ogarnia automatycznie. Jeśli nie — dodaj manualnie.

### 5. Usunąć/odświeżyć przestarzałe fragmenty

Przed publikacją zrób grep w istniejącym artykule:
- Wersje n8n < 1.0 → zaktualizuj na current 1.x
- Linki do dokumentacji n8n → sprawdź że żyją (docs.n8n.io)
- Daty / "rok 2024" → zaktualizuj na 2026
- Screenshoty z UI → jeśli są stare, zrób nowe (n8n UI zmienił się w 2025)

### 6. Cross-linki — dodaj 4 backlinki TO refreshed article

W tych istniejących artykułach dodaj link do `/blog/n8n/docker-instalacja-konfiguracja`:

| Artykuł | Gdzie wstawić | Anchor |
|---------|---------------|--------|
| `/blog/n8n` (pillar) | sekcja "Jak zacząć z n8n" | "Pełny tutorial self-hosted n8n z Dockerem →" |
| `/blog/n8n/licencja-cennik` | sekcja self-hosted free | "Krok po kroku jak postawić self-hosted →" |
| `/blog/n8n/self-host-bezpieczenstwo` | intro | "Nie masz jeszcze n8n? Zacznij tu →" |
| `/blog/n8n/przyklady-workflow-automatyzacji` | sekcja "Skąd brać workflow" | "Przed importem postaw n8n self-hosted →" |

To wzmacnia topical authority refreshed pillara.

---

## Featured image

Sprawdź czy istniejący jest aktualny. Jeśli nie:
```bash
python3 scripts/generate_image.py \
  --prompt "Server room dark navy + orange Dokodu accent, n8n logo on glowing screen, abstract tech background, minimalist editorial style, 16:9, no text" \
  --variant pro \
  --output public/blog/n8n-self-hosted-docker-2026.webp
```

---

## Synergia YT

Z tego refreshu nagram odcinek YT (15 min, jeden take, OBS):
- Lokowanie Hostingera 2 500 PLN
- Reflink KACPER10 w opisie
- Link do refreshed artykułu jako "rozwinięcie tematu"

YT brief planowany osobno przez `/yt-plan-video` po publikacji refreshu.

---

## Procedura wdrożenia

1. **Backup obecnego artykułu** — zapisz HTML/MD do `/30_RESOURCES/RES_Blog_Drafts/BACKUP_n8n-docker_2026-04-25.html`
2. **Edytuj content** — wstaw 3 nowe sekcje + KACPER10 box (3 miejsca)
3. **Zmień title + meta** w CMS bloga
4. **Sprawdź internal links** — refreshed article powinien mieć 4-6 outgoing + 3-4 incoming
5. **Submit URL do Google Search Console** dla rein-indexing
6. **Czekaj 4-6 tygodni** na efekt SEO. Mierz w GSC: pozycja na "n8n self-hosted", "n8n docker", "n8n self hosted"

---

## Sukces refreshu — KPI

- **Pozycja "n8n docker":** zachować #3 lub awansować
- **Pozycja "n8n self-hosted":** wejść do top 20 w 6 tyg, top 10 w 12 tyg
- **Kliki KACPER10:** mierzalne przez Hostinger affiliate dashboard (cel: 5+ rejestracji/mies. = ~150 zł prowizji)
- **Lead-gen:** kliknięcia na CTA `/kontakt` z tego artykułu (cel: 3+ konsultacji/mies.)
