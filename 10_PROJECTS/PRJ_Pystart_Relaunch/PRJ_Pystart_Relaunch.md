---
type: project
status: active
owner: kacper
created: 2026-03-30
deadline: 2026-04-28
health: 🟡
tags: [pystart, relaunch, kurs, python, ai]
---

# Projekt: PyStart Relaunch z AI

> **Cel:** Przekształcić PyStart z "kolejny kurs Pythona" w "jedyny kurs Python + AI w Polsce"
> **Revenue target:** PyStart Classic 499 + PyStart+AI 899 + Bundle 999 PLN

---

## Stan obecny
- ✅ 10 modułów, 40h+, 386 lekcji — gotowe
- ✅ LP poprawiona (headline, gwarancja, bio, obietnice zarobków)
- ✅ Transkrypcje wszystkich modułów w BRAIN
- ✅ Mapa treści + mapowanie AI → `Pystart_Mapa_Tresci.md`
- ✅ Analiza konkurencji → `Pystart_Konkurencja.md`
- ❌ Moduły AI — do nagrania
- ❌ Testimoniale — do zebrania
- ❌ Nowa struktura cenowa — do wdrożenia na stronie

---

## Zadania

### FAZA 1: Social proof (ten tydzień, do 4.04)

- [ ] **Wrzucić prośbę o testimoniale na Discord PyStart**
  Tekst gotowy w `PRJ_Sprzedaz_Kursy_Q2_2026.md`
  Cel: 5 tekstowych + 3 video (30s telefonem)
  Incentive: darmowy SkumajBazy za testimonial video

- [ ] **Zebrać screenshoty z Discorda**
  Pozytywne wiadomości od kursantów, "udało się", "dostałem pracę"
  Min. 10 screenshotów

- [ ] **Znaleźć case study "Z X do Y"**
  Kursant który zmienił karierę / dostał podwyżkę / zaczął freelancing
  Napisać 3-5 zdań historii

### FAZA 2: Moduły AI (7-25 kwietnia)

- [ ] **BONUS 1: Python + AI asystent kodowania (~3-4h nagrania)**
  - Kodowanie z Copilot / Claude Code od lekcji 1
  - Prompt engineering dla programistów
  - Debugging z AI vs debugger (nawiązanie do M4)
  - Ćwiczenie: 5 zadań z kursu — sam vs z AI
  - Refaktoryzacja z AI (nawiązanie do M6)

- [ ] **BONUS 2: API OpenAI/Anthropic z Pythona (~4-5h nagrania)**
  - Co to LLM (bez matmy, z analogiami)
  - Pierwszy request do API (5 linijek, nawiązanie do M7 requests)
  - Chatbot konsolowy (while True + input + API, nawiązanie do M4+M5)
  - Structured outputs — JSON mode (nawiązanie do M7 JSON)
  - Projekt: Asystent CV (czyta PDF → AI analizuje, nawiązanie do M7+M8)
  - Koszty API — kalkulator tokenów

- [ ] **BONUS 3: Automatyzacja z Pythonem i AI (~3-4h nagrania)**
  - Web scraping: requests + BeautifulSoup (nawiązanie do M7)
  - Excel/CSV + AI: openpyxl + LLM (nawiązanie do M8 CSV)
  - Automatyczny email: smtplib (nawiązanie do M5 funkcje)
  - Projekt: Bot cenowy — scraping → DB → alert → AI (nawiązanie do M3+M8)
  - Python ↔ n8n webhook (preview kursu n8n = natural upsell)

### FAZA 3: Pricing i strona (21-28 kwietnia)

- [ ] **Nowa struktura cenowa na stronie**
  - PyStart Classic: 499 PLN (obecny kurs, obniżka z 699)
  - PyStart + AI: 899 PLN (Classic + 3 moduły bonus AI)
  - Bundle PyStart+AI + SkumajBazy: 999 PLN
  - ~~Przekreślona cena~~: 1 298 PLN

- [ ] **Aktualizacja LP z testimonialami**
  Prawdziwe opinie zamiast generycznych (Marta K., Tomasz W., Anna M.)

- [ ] **Lead magnet: "Python + AI w 15 min"**
  Darmowa mini-lekcja wideo (10-15 min)
  Student pisze pierwszy skrypt z AI
  Zbiera email → nurture sequence

### FAZA 4: Kampania (28 kwietnia — 5 maja, Majówka)

- [ ] **Emaile relaunch** (w PRJ_Sprzedaz_Kursy_Q2_2026.md)
- [ ] **Film YT: "Dodałem AI do kursu Pythona"**
- [ ] **Post LinkedIn z testimonialami**
- [ ] **Evergreen funnel: lead magnet → nurture → oferta**

---

## Harmonogram nagrań modułów AI

| Tydzień | Co | Czas | Priorytet |
|:--|:--|:--|:--|
| 7-11.04 | BONUS 1: Python + AI asystent | ~4h | 🔴 (wymagany do relaunch) |
| 14-18.04 | BONUS 2: API OpenAI/Anthropic | ~5h | 🔴 |
| 21-25.04 | BONUS 3: Automatyzacja + AI | ~4h | 🟡 (może być po launch) |

---

## Pliki projektu

- `Pystart_Mapa_Tresci.md` — pełna mapa 10 modułów + mapowanie AI
- `Pystart_Konkurencja.md` — benchmark vs 3 konkurentów
- `PRJ_Sprzedaz_Kursy_Q2_2026.md` — master plan sprzedaży (wspólny z n8n)
- `30_RESOURCES/RES_Kursy_Transkrypcje/pystart/` — transkrypcje źródłowe
