---
last_updated: 2026-03-29
period: 2026-03-01 → 2026-03-28 (28 dni)
total_sessions: 7030
total_users: 5074
avg_bounce: 53.2%
---

# GA Insights — dokodu.it

## Kluczowe metryki (ostatnie 28 dni)

| Metryka | Wartość | Ocena |
|---------|---------|-------|
| Sesje | **7 030** | — |
| Unikalni użytkownicy | **5 074** | — |
| Odsłony | **7 383** | — |
| Średni bounce rate | **53.2%** | ✅ Dobry (norma bloga: 60-70%) |

---

## Top 5 Insights

### 1. 🔴 list-comprehension — 200 sesji, bounce 94.5%, czas 14 sekund
To najgorszy stosunek ruchu do zaangażowania w całym serwisie. Historycznie 1 643 sesje ze średnio 25s — user trafia na stronę i natychmiast wychodzi. Prawdopodobna przyczyna: tytuł lub opis w Google sugeruje szybkie rozwiązanie/cheatsheet, a artykuł tego nie dostarcza. **Priorytet: przebudowa lub dodanie sekcji "szybki cheatsheet" na górze.**

### 2. 🔴 /blog/n8n — flagship z problemem bounce 78.5%
Największa strona serwisu (1 204 sesje w marcu, ~10 931 historycznie) ma bounce 78.5%. To wprawdzie "hub" z listą artykułów, ale 1m12s czasu sugeruje że ludzie czytają, ale nie klikają dalej. **Brakuje wyraźnych CTA i sekcji "od czego zacząć".**

### 3. 🟡 Microsoft Teams — 96 sesji = kursanci (nie B2B)
`statics.teams.cdn.office.net` — najprawdopodobniej kursanci klikają linki do ankiet poszkoleniowych przez Teams (liczba sesji zgadza się z liczbą uczestników kursu). Potwierdzają to dane DB: `/ankieta/ANIME-*` i `/admin/surveys/` mają 0% bounce i długi czas sesji. **Nie traktować jako sygnał B2B — to ruch wewnętrzny ze szkoleń.**

### 4. 🟢 /kursy/n8n — wzorzec angażowania (bounce 37.3%, 3m15s)
Strona kursu n8n angażuje lepiej niż jakikolwiek artykuł blogowy. 110 sesji z bounce zaledwie 37.3% i ponad 3 minuty na stronie. Podobnie `/szkolenia/n8n-automatyzacja` (6% bounce, 3m41s, 92 sesje). **Format strony kursowej działa — warto przenieść ten styl na "hub" /blog/n8n.**

### 5. 🟡 YouTube → strona = 345 sesji/miesiąc
Kanał YouTube generuje realny ruch (345 sesji, ~5% całego ruchu). To więcej niż chatgpt.com (20) + perplexity.ai (11) razem wzięte. Kanał działa jako top-of-funnel. Warto śledzić które konkretne filmy generują najwięcej wejść.

---

## Ścieżki B2B — Status

| Ścieżka | Sesje (marzec) | Sesje (historycznie) | Główne źródło |
|---------|---------------|----------------------|---------------|
| `/sciezki/openai` | 4 | 40 | organic + chatgptpolsku.app |
| `/sciezki/google` | 6 | 29 | organic |
| `/sciezki/microsoft` | 2 | 1 | direct |

**Ocena:** Ruch niski, ale każda sesja na /sciezki/* to potencjalny lead wart 10–50k PLN. Niepokojące: `/sciezki/microsoft` historycznie zaledwie 1 sesja — ta ścieżka jest słabo widoczna lub słabo wypozycjonowana. Brak zdarzeń `ad_click` w GA — albo pixel nie działa, albo CTA nie są tagowane.

---

## Strony do naprawy (bounce >80%, duży ruch)

| Strona | Bounce | Czas | Sesje | Problem |
|--------|--------|------|-------|---------|
| `/blog/python/podstawy/list-comprehension` | 94.5% | **14s** | 200 | Nie spełnia intencji — brakuje cheatsheet |
| `/blog/python/testowanie/testowanie-jednostkowe-python` | 88.4% | **23s** | 43 | Treść zbyt akademicka, brak praktycznych przykładów |
| `/blog/python/automatyzacja/tkinter-gui` | 82.5% | **10s** | 40 | Prawdopodobnie outdated — Tkinter to niszowy temat |
| `/blog/cursor-cursor-pro-programowanie-ai` | 88.0% | 44s | 50 | Silna konkurencja, treść nie wyróżnia się |
| `/blog/sql/jak-uczyc-sie-sql` | 77.4% | **28s** | 53 | Ogólny tytuł, brak konkretnego planu nauki |

---

## Strony wzorcowe (do powielenia)

| Strona | Bounce | Czas | Sesje | Dlaczego działa |
|--------|--------|------|-------|-----------------|
| `/szkolenia/n8n-automatyzacja` | **6%** | 3m41s | 92 | Jasny CTA, konkretna oferta |
| `/checkout` | **12%** | 7m50s | 51 | Użytkownicy kupują (!) |
| `/blog/docker/debugowanie-kontenerow-docker` | **4%** | 2m3s | 44 | Praktyczny, z narzędziami |
| `/kursy/n8n` | **37%** | 3m15s | 110 | Format kursu angażuje |
| `/blog/n8n/przyklady-workflow-automatyzacji` | 54.7% | **2m43s** | 86 | Przykłady = engagement |

---

## Rekomendacje

1. **PILNE: Przebuduj `/blog/python/podstawy/list-comprehension`** — dodaj "szybki cheatsheet" na górze strony, potem rozwinięcie. 200 sesji miesięcznie z 14s to zmarnowany ruch.

2. **Przeprojektuj `/blog/n8n` hub** — wzoruj na `/kursy/n8n`. Dodaj: sekcja "od czego zacząć", featured artykuły, CTA do kursu.

3. **B2B post targetowany pod Teams** — napisz artykuł w stylu "Jak wdrożyć AI w dziale X" skierowany do menedżerów. Teams referral = korporacje czytają Dokodu — trzeba to wykorzystać.

4. **Sprawdź tagowanie CTA na ścieżkach B2B** — brak zdarzeń `ad_click` może oznaczać brak śledzenia. Jeśli CTA klika ktoś z Teams → to jest lead, który teraz jest niewidoczny.

5. **Exploit: chatgptpolsku.app referral** — to nieoczekiwane źródło prowadzi bezpośrednio na /sciezki/openai i /sciezki/google. Warto sprawdzić skąd dokładnie i czy można tam umieścić więcej treści.

---

*DOKODU BRAIN GA4 Insights | 2026-03-29*
