---
type: project-doc
status: active
owner: kacper
last_reviewed: 2026-03-18
tags: [kurs, n8n, marketing, launch]
---

# Kurs n8n + AI — Mapa Zasobów i Plan Marketingowy

## 1. Istniejące zasoby (inwentaryzacja)

### Strony

| URL | Co robi | Stan | Uwagi |
|-----|---------|------|-------|
| `/blog/n8n` | SEO content hub, 30 min lektura | ✅ działa | Dobry ruch organiczny, 4 CTA, YT playlist |
| `/kursy/n8n` | Waitlista + opis kursu | ⚠️ działa, ale | Data "czerwiec 2025" — NIEAKTUALNA. Wymaga aktualizacji |
| `/lp.dokodu.it/transformacja/` | Lead magnet — e-book "automatyzacja biznesowa" | ✅ działa | Ogólny, nie n8n-specyficzny. Leady idą do innej grupy niż waitlista |
| `/ebooki/n8n-automatyzacja` | E-book n8n | ❌ 404 | Blog post kieruje tu — ZEPSUTY funnel |

### Email / Lista

| Zasób | Stan | Uwagi |
|-------|------|-------|
| Waitlista kursu n8n | ✅ | MailerLite group `113044950` — zbiera od miesięcy |
| Ogólna lista | ✅ | ~15 359 subskrybentów |
| Lista z transformacja LP | ✅ | Osobna grupa — inny segment |

### Treści

| Zasób | Stan | Uwagi |
|-------|------|-------|
| Blog `/blog/n8n` | ✅ | Rozbudowany, dobry SEO, linkuje do sub-artykułów |
| Blog sub-artykuły | ✅ | node-code, integracja-z-ai, docker, licencja, webhook, workflow, make-vs-n8n |
| YT playlist n8n | ✅ | Kilka filmów — "kompleksowy przewodnik" |
| E-book "automatyzacja" | ⚠️ | Istnieje (zbiera leady), ale strona e-booka n8n 404 |
| Discord community | ✅ | 25 000+ osób |

### Produkt

| Element | Szczegóły |
|---------|-----------|
| Format | 7 tygodni, sesja + warsztat + projekt wdrożeniowy |
| Prowadzący | Kacper (technical) + Alina (RODO/AI Act/compliance) |
| Cena pre-sale | < 1 500 PLN netto |
| Cena regularna | 2 490 PLN netto |
| Differentiator | Jedyny PL kurs n8n z kątem compliance + Tech+Legal |

---

## 2. Krytyczne błędy funnelu (napraw ASAP)

### 🔴 PRIORYTET 1 — E-book 404
Blog post `/blog/n8n` → CTA "Pobierz darmowy e-book" → `/ebooki/n8n-automatyzacja` → **404**
- Każdy zainteresowany widz wychodzi z błędem
- Strata leadów z najlepszego organicznego ruchu

**Fix:** Albo stwórz stronę e-booka, albo zmień CTA w blogu na kierowanie do waitlisty kursu

### 🔴 PRIORYTET 2 — Nieaktualna data
`/kursy/n8n` mówi "cena wzrośnie od czerwca 2025" — jest marzec 2026
- Niszczy zaufanie przy pierwszej wizycie
- Sugeruje że projekt jest porzucony

**Fix:** Zmień na datę launch albo usuń konkretną datę → "cena wzrośnie przy starcie przedsprzedaży"

### 🟡 PRIORYTET 3 — Rozjechany funnel
LP `transformacja` zbiera leady na "automatyzację biznesową" → inna lista niż waitlista kursu
Leady nie wiedzą o kursie n8n, kurs nie wykorzystuje tych leadów

**Fix:** Dodaj do sekwencji "transformacja" maila o kursie n8n (po 3-5 dniach od zapisu)

---

## 3. Mapa funnelu (jak powinno być)

```
ŚWIADOMOŚĆ
    ↓
YouTube (n8n playlist) ←→ Blog /blog/n8n ←→ Organic SEO
    ↓                           ↓
CTA: Waitlista kursu       CTA: E-book (lead magnet)
    ↓                           ↓
/kursy/n8n              /lp.dokodu.it/transformacja/
    ↓                           ↓
MailerLite              Sekwencja welcome
group 113044950              ↓ (mail 3)
    ↓                    Wzmianka o kursie n8n
    ↓←←←←←←←←←←←←←←←←←←←←←↓
WARM-UP SEQUENCE (waitlista)
    ↓
LAUNCH — przedsprzedaż
    ↓
ZAKUP
    ↓
Ankieta → Testimoniale → Kolejna edycja
```

---

## 4. Plan marketingowy — fazy

### FAZA 0: Naprawa fundamentów (1-2 tygodnie)
- [ ] Fix 404 e-book lub zmień CTA w blogu → waitlista
- [ ] Aktualizacja daty na `/kursy/n8n`
- [ ] Sprawdź ile osób jest na waitliście (MailerLite group 113044950)
- [ ] Dodaj cross-sell do sekwencji "transformacja" LP

### FAZA 1: Budowanie grupy (ongoing, przed launchem)
**YouTube:**
- [ ] Film o kursie n8n (YT-003 rework) — "Jak zbudowałem kurs który uczy n8n + compliance w 7 tygodni"
- [ ] Film: case study z klientem który wdrożył n8n (internal champion angle)
- [ ] Na końcu każdego odcinka n8n → CTA do waitlisty

**Newsletter (warm-up sequence dla waitlisty):**
- [ ] Mail 1 (po zapisie): "Jesteś na liście — oto co cię czeka" + preview programu
- [ ] Mail 2 (tydzień po): "Dlaczego n8n + compliance to jedyne co ma sens dla polskiej firmy" (Alina)
- [ ] Mail 3 (co 2 tygodnie): case study / tip z n8n — utrzymanie zaangażowania
- [ ] Mail 4 (na miesiąc przed launch): "wkrótce ogłaszamy datę"

**Blog SEO (content gap):**
- [ ] "Kurs n8n — czy warto w 2026?" (commercial intent)
- [ ] "n8n vs Zapier — koszty dla polskiej firmy" (porównanie)
- [ ] "n8n i RODO — co musisz wiedzieć przed wdrożeniem" (Alina jako autor)

**LinkedIn:**
- [ ] Post Kacpra 1x/tydzień z n8n tipem lub case study
- [ ] Post Aliny o compliance + AI automatyzacja

### FAZA 2: Pre-launch (4-6 tygodni przed)
- [ ] Webinar "n8n od zera — live demo" (historycznie 52% OR!)
- [ ] Ogłoszenie daty startu przedsprzedaży do waitlisty
- [ ] "Okno wczesnego dostępu" — pierwsze 48h cena niższa
- [ ] Sekwencja 5 maili przed otwarciem koszyka

### FAZA 3: Launch (przedsprzedaż, 5-7 dni)
- [ ] Dzień 1: "Koszyk otwarty" — do waitlisty
- [ ] Dzień 2: FAQ + odpowiedzi na obiekcje
- [ ] Dzień 4: "Połowa miejsc zajęta" (lub social proof — pierwsze zapisy)
- [ ] Dzień 6: "Ostatnie 24h ceny pre-sale"
- [ ] Dzień 7: "Dziś kończymy" (2 maile: rano + wieczór)

### FAZA 4: Po launch — social proof machine
- [ ] Ankieta po tygodniu 1 i po ukończeniu
- [ ] Zbieranie testimoniali (publishConsent) → strona kursu
- [ ] Case study z uczestnika → post na LinkedIn + blog
- [ ] Rekrutacja na drugą edycję z testimonialami

---

## 5. Differentiatory do komunikacji

### Główny wyróżnik (USP)
> "Jedyny polski kurs n8n który uczy nie tylko jak budować automatyzacje — ale jak robić to zgodnie z RODO i AI Act."

### Supporting points:
- Kacper: 15+ lat, self-hosted n8n, realne wdrożenia dla firm
- Alina: RODO/AI Act specialist — nie ma tego nigdzie indziej w PL
- 7 tygodni struktury zamiast chaotycznych tutoriali
- Projekt wdrożeniowy = coś działa po kursie, nie tylko certyfikat
- Self-hosted = 0 zł miesięcznego abonamentu

### Buyer personas:
1. **Manager IT / Ops** — chce zautomatyzować procesy, ma budżet, musi uzasadnić compliance
2. **Freelancer/konsultant** — chce oferować automatyzację klientom jako usługę
3. **Właściciel firmy 20-100 os.** — widział YouTube, chce wdrożyć sam lub z teamem

---

## 6. Treści do stworzenia (backlog)

| Zasób | Typ | Priorytet | Notatki |
|-------|-----|-----------|---------|
| Fix 404 / CTA w blogu | Tech | 🔴 Teraz | |
| Aktualizacja daty waitlista | Tech | 🔴 Teraz | |
| Warm-up sequence (4 maile) | Newsletter | 🔴 Przed launchem | Dla group 113044950 |
| Film YT o kursie | YouTube | 🟡 Faza 1 | Nie clickbait — value-first |
| Blog "czy warto n8n 2026" | SEO | 🟡 Faza 1 | Commercial intent |
| Blog "n8n i RODO" (Alina) | SEO | 🟡 Faza 1 | Unique differentiator |
| Webinar live demo | Event | 🟡 Pre-launch | Najwyższy OR historycznie |
| Sekwencja launch (5 maili) | Newsletter | 🟡 Faza 2 | |
| Strona sprzedażowa (nie waitlista) | LP | 🟡 Pre-launch | Testimoniale + cena + FAQ |

---

*Ostatnia aktualizacja: 2026-03-18*
*Następny krok: sprawdź ile osób na waitliście (group 113044950 w MailerLite) + fix 404*
