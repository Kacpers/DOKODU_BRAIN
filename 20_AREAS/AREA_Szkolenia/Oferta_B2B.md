---
type: reference
status: active
owner: kacper
last_reviewed: 2026-04-22
tags: [szkolenia, b2b, strategia, oferta, sciezki]
---

> ⚠️ Korekta 2026-04-22: ceny flagshipów wyrównane do nowego cennika warsztatów Dokodu (baseline 6 999 PLN/dzień/do 15 os).
> Strona dokodu.it nie publikuje żadnych cen publicznie (wszędzie „wycena indywidualna"), więc aktualizacja nie powoduje rozjazdu z publikiem.
> Szczegóły: `30_RESOURCES/RES_Sales_Playbook/Dokodu_Oferta_Dane.md`

# Oferta B2B — Mapa Szkoleń Zamkniętych

> Jak ścieżki, flagship i katalog współgrają ze sobą.
> To jest dokument strategiczny — co komu pokazujemy i kiedy.

---

## Trzy warstwy oferty

```
┌─────────────────────────────────────────────────────────────┐
│  WARSTWA 1 — ŚCIEŻKI  (dokodu.it/sciezki/*)                │
│  Dla kogo: Nie wiem co AI może dla mnie zrobić              │
│  CTA: Umów bezpłatny audyt (konsultacja)                    │
│  Cena: Brak — wycena po diagnozie                           │
│  Gdzie: /sciezki/microsoft, /google, /openai                │
└──────────────────────────┬──────────────────────────────────┘
                           │ prowadzi do
┌──────────────────────────▼──────────────────────────────────┐
│  WARSTWA 2 — FLAGSHIP  (dokodu.it/dla-firm/szkolenia-*)     │
│  Dla kogo: Wiem czego chcę, chcę zobaczyć co kupuję         │
│  CTA: Zamów to szkolenie / Zapytaj o wycenę                 │
│  Cena: Widoczna (od X PLN)                                  │
│  Gdzie: /dla-firm/szkolenia-zamkniete (sekcja programów)    │
└──────────────────────────┬──────────────────────────────────┘
                           │ back-office
┌──────────────────────────▼──────────────────────────────────┐
│  WARSTWA 3 — KATALOG  (back-office, nie na stronie)         │
│  Dla kogo: Klient po konsultacji prosi o pełną ofertę       │
│  CTA: Pobierz katalog PDF (lead gen, email gate)            │
│  Gdzie: Katalog_Szkolen.md + PDF do wygenerowania           │
└─────────────────────────────────────────────────────────────┘
```

---

## Ścieżki — logika i moduły

Każda ścieżka to ten sam schemat:
`Prompting basics → Narzędzia codzienne → Automatyzacje/Agenci → Solutions Day (warsztat)`

| Ścieżka | Dla kogo | Ekosystem | Moduły |
|---------|----------|-----------|--------|
| `/sciezki/microsoft` | Firmy na M365 | Copilot, Teams, SharePoint | Prompting → Office Mastery → Copilot Studio → Solutions Day |
| `/sciezki/google` | Firmy na Google Workspace | Gemini, Docs, Sheets, Gmail | Prompting → AI tools → GEMs → n8n automation → Solutions Day |
| `/sciezki/openai` | Firmy bez konkretnego ekosystemu / własne rozwiązania | ChatGPT, Custom GPTs, n8n | Prompting → Custom GPTs → n8n automation → Solutions Day |

**Kiedy kierować na którą ścieżkę:**
- Używają Outlooka/Teams/SharePoint → Microsoft
- Używają Gmaila/Google Drive/Meet → Google
- Używają ChatGPT lub "nie mamy nic z AI" → OpenAI
- Mają SAP/ERP + chcą automatyzacji → OpenAI lub Microsoft + n8n (moduł głęboki)

**Brakuje ścieżki:** "Programiści / Tech Team" — tam trafia zapotrzebowanie na Python, Django, FastAPI, Claude Code. Dziś nie ma tego w ścieżkach, trafia na `/dla-firm/szkolenia-zamkniete` do sekcji deweloperskiej.

---

## Flagship Programs — co jest gotowe do sprzedaży

Kryterium: pełna agenda + doświadczenie z realizacji + można wycenić bez konsultacji.

### 🏆 FLAGSHIP #1: Automatyzacja z n8n + AI Agenci + M365
**URL docelowy:** `/dla-firm/szkolenia-zamkniete` (sekcja już istnieje)
- **Format:** 2 dni × 8h, on-site lub zdalnie
- **Dla kogo:** Działy BOK, Operations, IT, Administracja
- **Technologie:** n8n, Microsoft 365 (Outlook/Teams/SharePoint), GPT-4o/Azure OpenAI, SAP (opcja)
- **Wynik:** Uczestnicy wychodzą z działającymi automatyzacjami
- **Cena:** od 13 999 PLN netto / grupa do 15 os. (= Enterprise 2-dniowe z nowego cennika, rabat 15% vs 2× Standard)
- **Status:** ✅ Zrealizowane 5x (Animex, 75 uczestników, ocena 4.8/5)
- **Historyczna cena:** 8 000 PLN (Animex et al., 2025-2026Q1) — nowa oferta od 2026-04-22
- **Agenda:** Pełna — plik `10_PROJECTS/PRJ_Animex_Szkolenie/`
- **Social proof:** 4.8/5 ogólna, 4.9/5 trener, cytaty z ankiet

### 🏆 FLAGSHIP #2: Django Professional — Aplikacje Webowe od Podstaw
**URL docelowy:** Do stworzenia — `/dla-firm/szkolenia-zamkniete/django` lub sekcja na B2B page
- **Format:** 4 dni × 8h, on-site lub zdalnie
- **Dla kogo:** Programiści wewnętrzni, zespoły które chcą budować własne narzędzia webowe
- **Technologie:** Django, Python, SQL Server, Docker, REST API, Celery
- **Wynik:** Uczestnicy budują i wdrażają własną aplikację webową
- **Cena:** od 23 999 PLN netto / grupa do 12 os. (4 dni × 6 999 × rabat 15% ≈ 23 800, zaokr.)
- **Status:** ✅ Pełna agenda dostępna (wklejona przez Kacpra 25.03.2026)
- **Historyczny szacunek:** 14 000 PLN — zaktualizowane 2026-04-22
- **Agenda:** W `AREA_Szkolenia/Agendas/Django_4dni.md`

### 🏆 FLAGSHIP #3: Microsoft Copilot Specialist dla Firmy
**URL docelowy:** `/sciezki/microsoft` (już istnieje) + opcja "zamów szkolenie zamknięte"
- **Format:** 1 dzień × 8h (lub 2 × 4h "pół na pół")
- **Dla kogo:** Każdy pracownik biurowy na M365
- **Wynik:** Zespół odzyskuje 30–60 min dziennie per osoba
- **Cena:** od 6 999 PLN netto / grupa do 15 os. (= Standard z nowego cennika)
- **Status:** ✅ Moduły gotowe w ścieżce, realizowane wielokrotnie
- **Historyczny szacunek:** 4 000 PLN — zaktualizowane 2026-04-22
- **Uwaga:** Nie ma dedykowanej strony produktowej — CTA "Umów audyt" prowadzi do konsultacji

### 🟡 KANDIDAT #4: Google Gemini Specialist dla Firmy
- Analogiczny do Microsoft — moduły gotowe, brakuje strony produktowej
- **Status:** 🟡 Gotowe do produktyzacji

### 🟡 KANDIDAT #5: Python dla analityków / raportujących
- Ogromny popyt, wiele zrealizowanych edycji przez Altkom
- **Status:** 🟡 Trzeba wybrać konkretny poziom (podstawy vs. analiza danych)

---

## Co brakuje żeby zamknąć sprzedaż B2B

1. **Flagship #2 (Django) — strona produktowa** — mam pełną agendę, brakuje strony
2. **Flagships #1-3 — sekcja na `/dla-firm/szkolenia-zamkniete`** — dziś strona jest generyczna
3. **Katalog PDF** — do stworzenia gdy będzie potrzeba (lead gen / po konsultacji)
4. **Ścieżka dla programistów** — `/sciezki/tech` lub sekcja na B2B page — brakuje kompletnie

---

## Mapa: skąd klient trafia → gdzie ląduje

| Skąd | Intencja | Gdzie ląduje | Co widzi |
|------|----------|--------------|----------|
| Google "szkolenie n8n dla firm" | Chce kupić konkretnie | `/dla-firm/szkolenia-zamkniete` | Flagship #1 z agendą i ceną |
| Google "szkolenie copilot dla firmy" | Chce kupić konkretnie | `/sciezki/microsoft` | Moduły + "Umów audyt" (brak ceny) ← **gap** |
| Google "szkolenie AI dla pracowników" | Nie wie czego chce | `/sciezki/*` lub `/dla-firm` | Ścieżka + diagnoza |
| Referral / networking | Zna Kacpra | Bezpośredni kontakt | Katalog PDF lub rozmowa |
| Animex → kolejne firmy | Rekomendacja | Strona + Flagship #1 | Social proof działa |

---

## Priorytety do zrobienia

- [ ] Napisać agendę Django do `AREA_Szkolenia/Agendas/Django_4dni.md` (mam treść z 25.03)
- [ ] Dodać sekcję Flagship Programs do `/dla-firm/szkolenia-zamkniete` (3 karty)
- [ ] Dodać CTA "Zamów jako szkolenie zamknięte" na `/sciezki/microsoft` i `/sciezki/google`
- [ ] Rozważyć ścieżkę `/sciezki/tech` dla programistów
- [ ] PDF katalogu — gdy pojawi się potrzeba (nie priorytet teraz)
