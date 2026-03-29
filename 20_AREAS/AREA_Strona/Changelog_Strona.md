---
type: changelog
owner: kacper + claude
last_updated: 2026-03-29
tags: [strona, dokodu.it, changelog, web]
---

# Changelog — dokodu.it (Next.js)

Logi zmian wprowadzanych na stronie przez Claude Code. Przy analizie danych (GA/GSC) zawsze sprawdź najpierw czy dana strona/sekcja nie była niedawno zmieniana.

Format: `YYYY-MM-DD | ścieżka/plik | opis zmiany`

---

## 2026-03-29

### SEO meta title & description — `/blog/wdrozenie-ai-w-firmie`

**Źródło:** GSC analysis — frazy "automatyzacje dla firm" (#11.0, 132 imp.) i "automatyzacja ai" (#11.2, 208 imp.)
**Metoda:** blog API (`--meta-title` + `--excerpt`), revalidacja ISR automatyczna
**Brief:** `20_AREAS/AREA_Blog_SEO/Brief_Automatyzacja_Dla_Firm_2026-03-29.md`

- meta title: "Automatyzacja AI w firmie - jak wdrożyć sztuczną inteligencję" → **"Automatyzacja AI dla Firm — Jak Zacząć w 2026?"** (47 zn., fraza "Automatyzacja AI" na początku)
- meta description: "Kompletny przewodnik po wdrożeniu AI w firmie..." → **"Automatyzacja AI w firmie: które procesy wdrożyć pierwsze, ile to kosztuje i jak wybrać partnera. Sprawdź praktyczny przewodnik dla CEO i dyrektorów."** (152 zn., CTA + fraza docelowa)
- **Uwaga:** treść artykułu nie zmieniona, tylko meta tagi. Cel: pozycja #11 → top 5–7 dla "automatyzacja ai dla firm". Efekt widoczny po 14–21 dniach w GSC.

---

### SEO meta title & description — 2 strony blogowe

**Źródło:** GSC analysis (SEO_Meta_Fixes_2026-03-29.md) — niski CTR przy dobrych pozycjach
**Metoda:** blog API (`--meta-title` + `--excerpt`), revalidacja ISR automatyczna

- `/blog/n8n` — meta title: "N8n - co to jest? Przewodnik od zera do eksperta" → "n8n: Automatyzacja bez kodu — kompletny przewodnik"; meta desc zaktualizowany (cel: CTR z 2.4% → ~5%)
- `/blog/python/podstawy/list-comprehension` — meta title: "List Comprehension Python – skróć kod 3x [przykłady i ćwiczenia]" → "Python List Comprehension — składnia, przykłady, pułapki"; meta desc zaktualizowany (cel: CTR z 0.2% → ~1.8%)
- **Uwaga:** treść artykułów nie zmieniona, tylko meta tagi. Efekt widoczny po 14-21 dniach w GSC.

---

## 2026-03-26

### `/blog/n8n` — dodanie sekcji CTA do szkolenia zamkniętego

**Źródło:** GA/GSC: 1191 sesji/miesiąc, 78.3% bounce, brak konwersji B2B
**Metoda:** blog API (contentMarkdown update), revalidacja ISR automatyczna

- Dodana sekcja "Chcesz wdrożyć n8n w swoim zespole?" na końcu artykułu
- Link do `/dla-firm/szkolenia-zamkniete` z opisem programu i social proof (4.8/5, 75 uczestników)
- Kontakt bezpośredni: kacper@dokodu.it · 508 106 046
- **Uwaga:** dane GA/GSC dla tej strony po tej dacie mogą pokazywać zmianę bounce rate / konwersji

---

### `/dla-firm/szkolenia-zamkniete` — duży rewrite B2B landing

**Pliki:** `src/app/dla-firm/szkolenia-zamkniete/page.tsx`, `src/components/features/Trainings/TrainingContactForm.tsx`

- **Stworzony** `TrainingContactForm.tsx` — formularz kontaktowy z dropdownem programów, zapisuje lead do `/api/lead` (source: discovery_form), context = "Szkolenie: X | Firma: Y"
- **Hero** — podmieniony subtitle z n8n-specyficznego na ogólny (szkolenia zamknięte dla firm)
- **Flagship cards** — dodane 3 karty (n8n+AI 8k, Copilot 4k, Django 14k), potem rozszerzone do 5 (+ Prompt Engineering 3.5k, Python dla analityków 7k)
- **Sekcja "2 dni intensywnej praktyki"** — przemianowana na "Przykładowy program — n8n + AI Agenci" dla kontekstu
- **Cennik** — zmieniony z karty "Szkolenie 2-dniowe" na tabelę 5 programów z cenami
- **Final CTA** — zastąpiony formularzem kontaktowym (`id="kontakt"`)
- **Wszystkie CTA** — przepięte z `/umow-spotkanie` na `#kontakt` (scroll do formularza)
- **Przyciski na kartach** — zawsze widoczne (usunięta animacja opacity-0/group-hover, zostawiony hover shadow+translate na karcie)

### `/szkolenia` (public store)

**Plik:** `src/app/szkolenia/page.tsx`

- Usunięta sekcja `B2BSection` — sklep publiczny nie jest priorytetem (solo trener)

### DOKODU_BRAIN — dokumenty szkoleniowe

- **Stworzony** `20_AREAS/AREA_Szkolenia/Katalog_Szkolen.md` — master katalog 30+ szkoleń wg 3 osi (AI Biurowe, AI Engineering, SQL/Dane)
- **Stworzony** `20_AREAS/AREA_Szkolenia/Oferta_B2B.md` — mapa strategiczna 3-warstwowa (Ścieżki → Flagship → Katalog)
- **Stworzony** `20_AREAS/AREA_Szkolenia/Agendas/n8n_AI_Agenci_2dni.md` — pełna agenda 2-dniowa (z umowy Animex)
- **Stworzony** `20_AREAS/AREA_Szkolenia/Agendas/Django_4dni.md` — pełna agenda 4-dniowa Django

---

## Szablon wpisu

```
## YYYY-MM-DD

### `/ścieżka/strony` — opis

**Pliki:** `src/...`

- zmiana 1
- zmiana 2
```

---

> **Zasada:** przed oceną strony w danych GA/GSC sprawdź czy nie była zmieniana w ostatnich 14 dniach — dane mogą nie odzwierciedlać jeszcze nowej wersji.
