---
name: newsletter-check
description: Ocenia newsletter przed wysłaniem — analizuje subject line, CTA, strukturę, cel emaila. Porównuje z historycznymi kampaniami Kacpra. Daje ocenę 1-10 i konkretne poprawki. Zapisuje draft do BRAIN. Trigger: "sprawdź newsletter", "oceń maila", "przejrzyj newsletter", "zanim wyślę", /newsletter-check
---

# Instrukcja: Newsletter Check (Pre-send Review)

## Cel

Kacper wkleja treść newslettera PRZED wysłaniem. Ty analizujesz, oceniasz i sugerujesz poprawki. Zapisujesz do BRAIN. Po wysłaniu i sync — stats się uzupełniają automatycznie.

## KROK 1: Zbierz dane wejściowe

Jeśli Kacper nie podał — zapytaj o:
1. **Subject line** (temat maila)
2. **Treść** (cały tekst emaila)
3. **Cel tego maila** (sprzedaż / feedback / wartość / event / reminder) — jeśli nie podał, zgadnij z treści

## KROK 2: Załaduj historię dla kontekstu

Przeczytaj kilka plików z:
`/home/kacper/DOKODU_BRAIN/20_AREAS/AREA_Newsletter/Newsletters/`

Szukaj wzorców subject line które dawały wysokie OR (open_rate > 42%) i niskie OR (< 30%).
Przeczytaj 5-10 plików posortowanych datą (najnowsze).

## KROK 3: Analiza emaila

Oceń każde kryterium w skali 1–5:

### A) Subject Line (waga: 40% końcowej oceny)
- **Długość**: optimum 30–50 znaków — zbyt długi (>60) ucina się na mobile
- **Curiosity gap**: czy buduje ciekawość bez clickbaitu?
- **Konkretność**: liczba / imię / sytuacja > abstrakcja
- **Wzorzec historyczny**: porównaj z top subject lines Kacpra (te z OR > 42%)
  - Wzorce które działają u Kacpra: osobiste ("Przełom w moim studiu"), pytania ("Ile pomysłów dziś zapomniałeś?"), intryga ("Programista 2.0")
  - Wzorce które nie działają: sprzedażowe ("🛑 STOP -30%"), nagłówkowe ("Ostatnie godziny")

### B) Jeden cel (waga: 25%)
- Czy email ma JEDNO jasne zadanie? (feedback LUB sprzedaż LUB wartość — nie wszystko naraz)
- Ile CTA jest w emailu? (optimum: 1, max: 2)
- Czy PS nie sabotuje głównego CTA?

### C) CTA (waga: 20%)
- Czy jest jasny, konkretny przycisk/link z instrukcją działania?
- Czy benefit jest oczywisty? ("kup teraz" < "wejdź i sprawdź co zyskujesz")
- Czy urgency jest uzasadnione czy sztuczne?

### D) Ton i relacja (waga: 15%)
- Czy pisze do człowieka czy do listy?
- Czy jest "Ty" focused (co Ty zyskasz) czy "Ja" focused (co ja zrobiłem)?
- Zgodny z TOV Kacpra: bezpośredni, ciepły, konkretny, anty-hype

## KROK 4: Wynik i raport

Wyświetl w tym formacie:

---

## Newsletter Check — [Subject Line]

**Ocena: X/10** | Cel: [typ] | Data sprawdzenia: [data]

### Subject Line: X/5
[Ocena + co działa, co nie + alternatywy]

**3 alternatywne subject liny:**
1. `[propozycja 1]` — [dlaczego lepsza]
2. `[propozycja 2]`
3. `[propozycja 3]`

### Jeden cel: X/5
[Czy email ma jeden cel? Co go rozbija?]

### CTA: X/5
[Ocena CTA, co zmienić]

### Ton: X/5
[Ocena tonu, co zmienić]

### 🔴 Krytyczne błędy (napraw przed wysłaniem)
- [błąd 1]
- [błąd 2]

### 🟡 Do poprawy (jeśli jest czas)
- [sugestia 1]

### ✅ Co działa dobrze
- [mocna strona 1]

### Prognoza Open Rate
Na podstawie historii Kacpra i subject line:
**Prognozowany OR: ~X%** (Jego avg: 37.7%, benchmark: 25-35%)

---

## KROK 5: Zaproponuj poprawioną wersję

Jeśli ocena < 7/10 — napisz poprawioną wersję emaila lub przynajmniej kluczowych fragmentów.

Jeśli Kacper potwierdzi że chce poprawioną wersję — napisz ją w całości.

## KROK 6: Wypchnij do MailerLite jako DRAFT

Po zapisaniu do BRAIN — zapytaj: **"Do których grup wysłać?"**

Pokaż skróconą listę popularnych grup (z `Newsletter_Last_Sync.md` lub pamięci):
- `111679368` — Dostał "o mnie" (4 491 os.)
- `111682076` — Klienci (1 297 os.)
- Można podać kilka ID po przecinku

Gdy Kacper poda grupy — uruchom:
```bash
python3 /home/kacper/DOKODU_BRAIN/scripts/mailerlite_create.py \
  --subject "SUBJECT_LINE" \
  --body "TREŚĆ_MAILA" \
  --groups "ID1,ID2"
```

Skrypt zapisze kampanię jako **DRAFT** (nie wysyła automatycznie).
Podaj Kacperowi link do podglądu w MailerLite admin.

Jeśli Kacper chce wysłać od razu — uruchom z `--send` (skrypt poprosi o potwierdzenie "WYSLIJ").

## KROK 8: Zapisz do BRAIN

Zapisz plik:
`/home/kacper/DOKODU_BRAIN/20_AREAS/AREA_Newsletter/Reviews/[YYYY-MM-DD]_[slug-subject].md`

Format pliku:

```markdown
---
date_reviewed: [DATA]
date_sent: null
subject: [SUBJECT LINE]
goal: [cel emaila]
score: [X/10]
subject_score: X/5
cta_score: X/5
goal_score: X/5
tone_score: X/5
predicted_or: X%
actual_or: null
actual_ctr: null
campaign_id: null
status: draft
---

# Review: [Subject Line]

## Treść emaila (oryginał)

[PEŁNA TREŚĆ]

## Ocena

[Pełny raport z KROKU 4]

## Poprawiona wersja (jeśli była)

[POPRAWIONA TREŚĆ lub "brak"]
```

Po wysłaniu i `/mailerlite-sync` — Kacper aktualizuje `date_sent`, `actual_or`, `actual_ctr`, `campaign_id` i `status: sent`.

## ZASADY

- Jeden email = jeden cel. Jeśli email ma 2+ cele → powiedz to wprost i zaproponuj split na 2 emaile
- Subject line to 40% sukcesu. Zawsze dawaj 3 alternatywy
- Nie pochwalaj słabego emaila żeby nie zrazić — Kacper chce szczerości, nie komplementów
- Prognoza OR: bazuj na wzorcach z historii (pliki w Newsletters/) — osobiste tematy ~45-47%, sprzedażowe ~35-37%, promo z emoji ~2-35%
- TOV Kacpra: bezpośredni, ciepły, autentyczny, praktyczny. Nie korporacyjny, nie clickbaitowy
- Kacper BĘDZIE wysyłał wszystkie maile z Tobą — to jest stały workflow, traktuj go poważnie
