---
name: seo-dataforseo
description: Cotygodniowy research SEO przez DataForSEO API — pobiera keyword suggestions dla seedów dokodu.it, sprawdza co już rankujemy w top 30 PL, identyfikuje gapy commercial/informational i generuje raport tygodniowy. Trigger: "weekly seo dataforseo", "co napisać dataforseo", "raport seo z dataforseo", "tygodniowy keyword research", /seo-dataforseo
---

# Instrukcja: SEO DataForSEO Weekly

Cel: raz w tygodniu (piątek razem z `/seo-weekly`) pobrać świeże dane z DataForSEO Labs API, znaleźć nowe gapy do napisania i monitorować ruch pozycji dokodu.it w SERP PL. Budżet: ~$0.15-0.30 / tydzień (~5 PLN/mies.).

## Architektura

- **Klient API:** `scripts/dataforseo_fetch.py` (Python stdlib, brak zależności)
- **Auth:** `~/.config/dokodu/dataforseo_credentials` (chmod 600)
- **Konfiguracja seedów:** `~/.config/dokodu/dataforseo_seeds.txt` (1 fraza/linia)
- **Log kosztów:** `~/.config/dokodu/dataforseo_budget.json` (każdy płatny call)
- **Raporty MD:** `20_AREAS/AREA_Blog_SEO/dataforseo/weekly/YYYY-WW.md`
- **Surowe JSON-y:** `20_AREAS/AREA_Blog_SEO/dataforseo/weekly/YYYY-WW-raw.json`

## Cadence

**Piątek rano** — odpalaj razem z `/seo-weekly` przed weekly review.
Jeden run = ~$0.15. Tygodniowy budżet $5/mies. zostawia bufor 30× na ad-hoc queries.

Kacper może też odpalać manualnie kiedy potrzebuje (np. przed pisaniem nowego artykułu — zobaczy aktualne volume i gapy).

## KROK 1: Sprawdź balance

```bash
cd ~/Projects/dokodu/brain-public && python3 scripts/dataforseo_fetch.py check
```

Pokazuje saldo USD i kumulatywny wydatek z lokalnego loga. Jeśli balance < $1 → zatrzymaj i powiedz Kacprowi że trzeba doładować.

## KROK 2: Odpal weekly research

```bash
cd ~/Projects/dokodu/brain-public && python3 scripts/dataforseo_fetch.py weekly
```

Co robi:
1. Czyta seedy z `~/.config/dokodu/dataforseo_seeds.txt` (default: n8n, automatyzacja ai, cursor, claude code, agent ai)
2. Estymuje koszt PRZED odpaleniem — jeśli >$0.50, wymaga `--confirm`
3. Per seed: keyword suggestions (limit 200 kw, intent + volume + CPC)
4. Ranked keywords dokodu.it (top 30 SERP PL, limit 500)
5. Generuje raport MD + raw JSON snapshot
6. **Diff vs poprzedni tydzień** — nowe pozycje, awanse, spadki

Output:
- `20_AREAS/AREA_Blog_SEO/dataforseo/weekly/YYYY-WW.md` ← czytelny raport
- `20_AREAS/AREA_Blog_SEO/dataforseo/weekly/YYYY-WW-raw.json` ← do diffów

## KROK 3: Czytaj raport i wybierz akcje

Raport MD ma 4 sekcje:

1. **Top 30 GAPS** — frazy z volume ≥30, intent informational/commercial/transactional, dokodu.it NIE rankuje w top 30
2. **Top 15 COMMERCIAL/TRANSACTIONAL GAPS** — najbardziej lead-gen-friendly (firmy szukające wdrożenia)
3. **Top 20 RANKED dokodu.it** — co już mamy + URL
4. **Diff vs poprzedni tydzień** — nowe / wypadły / awans / spadek

**Rekomendacje dla Kacpra (zaproponuj 3 konkretne akcje):**

a) **Najlepszy nowy temat na artykuł** — top 1 gap z największym volume i komercyjnym intentem. Zaproponuj komendę:
```bash
/seo-plan-post [keyword]
```

b) **Optymalizacja istniejącego** — jeśli któraś rankująca fraza SPADŁA w diffie, zaproponuj refresh artykułu pod nią.

c) **Quick win** — fraza z LOW competition + commercial intent, niskie volume (50-300) ale szybko do napisania.

## KROK 4: Aktualizuj SEO_Ideas_Bank (opcjonalnie)

Jeśli któreś gapy nie są w `SEO_Ideas_Bank.md`, zapytaj Kacpra czy dodać. Komenda:

```bash
python3 scripts/seo_ideas.py add "[tytuł artykułu]" \
  --keyword "[fraza główna]" \
  --pillar "[n8n Automatyzacja|AI w firmie|Cursor AI|Python|SQL]" \
  --priority "[high|medium|low]" \
  --notes "[volume X, CPC Y, comp Z, dataforseo W17]"
```

## KROK 5: Loguj koszt

Skrypt automatycznie loguje każdy call. Sprawdź podsumowanie:

```bash
python3 scripts/dataforseo_fetch.py budget
```

Pokazuje total spent, breakdown by endpoint, last 10 calls. Jeśli tygodniowy koszt przekracza $0.50 → ostrzeż Kacpra (oszczędność > kompletność).

## Subkomendy ad-hoc (nie tylko weekly)

Gdy Kacper pyta o konkretny temat poza weekly schedule:

- **`suggestions <seed1> <seed2>`** — keyword suggestions dla podanych seedów (long-tail PL z volume + intent)
- **`ideas <seed1> <seed2>`** — semantyczna pula (UWAGA: testowo daje śmieci typu "X praca", używaj tylko jak suggestions zwróci za mało)
- **`ranked <domain>`** — keywords po których konkretna domena rankuje (np. konkurencja: `make.com`, `n8n.io`)

Każda taka komenda dodaje koszt do logu. Powiedz Kacprowi szacowaną cenę przed odpaleniem.

## Limity i pułapki

- **Endpoint `keyword_ideas` daje śmieci** — algorytm dryfuje semantycznie do popularnych fraz (np. "X praca"). Trzymaj się `keyword_suggestions` chyba że konkretnie potrzebujesz semantyki.
- **`automatyzacja ai`** zwraca tylko ~5 fraz — DataForSEO ma słabe pokrycie tej dokładnej frazy. Lepiej rozbić na "automatyzacja procesów ai", "ai dla firm" itp.
- **Ranked endpoint** filtruje top 30 — jeśli dokodu.it ma więcej fraz w top 100, zwiększ limit lub usuń filtr.
- **Cost prediction** w skrypcie zakłada cennik z 04.2026. Jeśli DataForSEO zmieni pricing — sprawdź realny koszt w logu.

## Co zrobić jeśli skrypt padnie

1. **HTTP 401** — credentials wygasły. Wygeneruj nowy password w app.dataforseo.com → API Access → zaktualizuj `~/.config/dokodu/dataforseo_credentials`.
2. **HTTP 403 z status_code 40104** — konto wymaga weryfikacji KYC. Wejdź do panelu i uzupełnij dane firmowe.
3. **Empty results** — seed za wąski (małe volume w PL). Poszerz frazę albo użyj angielskiego ekwiwalentu.
4. **Balance == 0** — doładuj konto w panelu DataForSEO.

## Integracja z innymi skillami

- **`/seo-weekly`** (piątek) — Claude w przeglądzie powinien sprawdzić ostatni raport DataForSEO i wpleść top gapy w sekcję "Plan na następny tydzień"
- **`/seo-plan-post`** — przed pisaniem briefu, sprawdź volume + competition z najnowszego DataForSEO snapshotu (zamiast tylko zgadywać z Trends)
- **`/seo-research`** — uzupełnia DataForSEO o web research (top 5 SERP, PAA, content gaps); używaj obu razem dla high-priority tematów
