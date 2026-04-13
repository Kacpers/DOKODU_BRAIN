---
name: brain-new-prompt
description: Dodaje nowy prompt do Biblioteki Promptow Dokodu (300_BIBLIOTEKA_PROMPTOW.md). Standaryzuje format, nadaje ID, kategoryzuje. Uzyj gdy odkryjesz lub napiszesz prompt ktory chcesz zachowac i wielokrotnie uzywac. Trigger: "dodaj prompt", "zapisz prompt", "nowy prompt do biblioteki", /brain-new-prompt
---

# Instrukcja: Dodawanie Nowego Prompta do Biblioteki

## KROK 1: Zbierz informacje o prompcie

Zapytaj o:
1. **Nazwa** (krótka, opisowa — np. "Klasyfikacja emaili BOK")
2. **Model** (Claude Sonnet / GPT-4o / Gemini 1.5 Pro / inne)
3. **Kategoria** — wybierz:
   - Ekstrakcja Danych
   - Analiza i Code Review
   - Sales i Marketing
   - Legal i Compliance
   - Asystent Biznesowy
   - Szkolenia i Content
   - Inne (podaj jaka)
4. **Tresc prompta** (System Prompt i/lub User Prompt)
5. **Kiedy uzywac** (kontekst, trigger)
6. **Przykładowe wyjscie** (opcjonalne)
7. **Uwagi** (edge cases, ograniczenia)

## KROK 2: Nadaj ID

Sprawdz ostatni ID w `/home/kacper/DOKODU_BRAIN/30_RESOURCES/RES_Prompt_Library/300_BIBLIOTEKA_PROMPTOW.md`.
Nadaj nastepny: PROMPT-[NR] (np. jezeli ostatni to 050, nowy to 051).

## KROK 3: Sformatuj wpis

Uzyj szablonu:

```markdown
### PROMPT-[ID]: [Nazwa]
**Model:** [model]
**Uzycie:** [gdzie/kiedy uzywac]
**Wersja:** 1.0
**Data dodania:** [dzisiaj]

\`\`\`
SYSTEM:
[tresc system prompta]

USER:
[tresc user prompta z placeholderami [WKLEJ X]]
\`\`\`

**Uwagi:**
- [uwaga 1]
- [uwaga 2]

---
```

## KROK 4: Dodaj do biblioteki

Wstaw wpis w odpowiedniej sekcji kategorialnej w pliku `300_BIBLIOTEKA_PROMPTOW.md`.
Dodaj tez do CHANGELOG na koncu pliku:
```
| v1.X | [data] | Dodano: PROMPT-[ID] ([Nazwa]) |
```

## KROK 5: Zaktualizuj indeks kategorii

Na poczatku pliku jest spis kategorii — sprawdz czy nowy prompt pasuje do istniejącej, jezeli nie — dodaj nowa sekcje.

## KROK 6: Potwierdz

"Prompt PROMPT-[ID] '[Nazwa]' dodany do kategorii [Kategoria]. ID: PROMPT-[ID]."

## ZASADY

- Jezeli prompt byl uzywany >3 razy — zapisz go KONIECZNIE
- Jezeli prompt zawiodl — opisz w Uwagach dlaczego i jak uniknac
- Model musi byc konkretny — nie "AI", tylko "Claude Sonnet 4.6" lub "GPT-4o"
- Placeholder w prompcie zawsze w formacie: `[WKLEJ TRESC]`
