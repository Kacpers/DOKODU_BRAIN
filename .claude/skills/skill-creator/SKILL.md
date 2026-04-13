---
name: skill-creator
description: Tworzy nowe skille dla Claude Code — prowadzi przez wywiad z użytkownikiem, pisze SKILL.md, definiuje test cases i iteruje do zadowalającej jakości. Uzyj gdy chcesz zautomatyzować nowy rodzaj pracy jako skill/komendę, zbudować własny workflow AI, lub gdy masz powtarzalne zadanie które chcesz skodyfikować. Trigger: "stwórz skill", "nowy skill", "zbuduj komendę", "skodyfikuj workflow", /skill-creator
---

# Skill Creator — Meta-skill do tworzenia nowych skillów

Jesteś ekspertem w tworzeniu skillów dla Claude Code. Prowadzisz użytkownika przez cały proces: od pomysłu do gotowego, przetestowanego skilla.

## Filozofia

Skille to skodyfikowana wiedza proceduralna — instrukcje "jak działać" w konkretnym kontekście. Dobry skill:
- Ma precyzyjne triggery (kiedy używać, kiedy NIE używać)
- Wyjaśnia "dlaczego" zamiast podawać sztywne reguły
- Jest zwarty (max ~500 linii SKILL.md), resztę ładuje z plików referencyjnych
- Generalizuje z przykładów zamiast overfitować do konkretnych przypadków

---

## FAZA 1: Wywiad — Capture Intent

Zanim cokolwiek napiszesz, przeprowadź wywiad. Zadaj te pytania:

1. **Co skill ma robić?** (konkretne zadanie, outcome)
2. **Kiedy ma się triggerować?** (słowa kluczowe, konteksty, komendy /slash)
3. **Kiedy NIE powinien się triggerować?** (edge cases, kiedy inny skill pasuje lepiej)
4. **Jaki jest oczekiwany output?** (plik, tekst, akcja, raport?)
5. **Jakie dane wejściowe dostaje?** (co user podaje, co Claude musi sam znaleźć)
6. **Czy są zależności?** (pliki, zewnętrzne systemy, inne skille)

Jeśli użytkownik podał dużo informacji z góry — potwierdź rozumienie, dopytaj tylko o brakujące kluczowe szczegóły.

---

## FAZA 2: Draft SKILL.md

Napisz SKILL.md w tej strukturze:

```markdown
---
name: <nazwa-skilla>
description: <opis triggera — napisany "trochę nachalnie", żeby Claude wiedział kiedy go użyć. Zawiera trigger words i /slash-command>
---

# <Nazwa Skilla> — <Krótki opis>

## Cel
Co skill robi i po co istnieje.

## Kiedy używać / Kiedy NIE używać
Precyzyjne triggery i wyjątki.

## Dane wejściowe
Co user podaje, co Claude musi znaleźć samodzielnie.

## Proces
Krok po kroku workflow. Wyjaśniaj "dlaczego" przy kluczowych decyzjach.

## Output
Format i lokalizacja deliverable.

## Zasady jakości
Co sprawdzić przed oddaniem wyniku.
```

**Zasady pisania SKILL.md:**
- Opis w frontmatter pisze się tak, żeby Claude rozpoznał go jako odpowiedni — bądź konkretny i "pushy" w triggerach
- Trzymaj poniżej 500 linii — dłuższą wiedzę przenieś do pliku `references/`
- Nie duplikuj instrukcji z CLAUDE.md projektu
- Używaj języka polskiego (zgodnie z konwencją DOKODU_BRAIN)

---

## FAZA 3: Walidacja z użytkownikiem

Po napisaniu draftu:
1. Pokaż gotowy SKILL.md
2. Zapytaj: *"Czy to odzwierciedla co chciałeś? Co brakuje lub jest nieprecyzyjne?"*
3. Zbierz feedback i popraw

Iteruj tak długo, aż użytkownik potwierdzi, że skill jest gotowy.

---

## FAZA 4: Zapis i rejestracja

Gdy skill jest zatwierdzony:

1. Utwórz katalog: `.claude/skills/<nazwa-skilla>/` (w repo DOKODU_BRAIN, NIE w ~/.claude/skills/)
2. Zapisz `SKILL.md` do tego katalogu
3. Jeśli skill wymaga plików referencyjnych — utwórz podkatalog `references/`
4. **Zaktualizuj CLAUDE.md** projektu — dodaj skill do tabeli dostępnych skillów (sekcja "Dostępne skille")
5. Potwierdź użytkownikowi lokalizację i jak triggerować skill

---

## FAZA 5: Test Cases (opcjonalnie)

Jeśli użytkownik chce przetestować skill przed wdrożeniem:

Przygotuj 2-3 realistyczne prompty testowe:
- Jeden "standardowy" przypadek użycia
- Jeden edge case (niekompletne dane, niejednoznaczny request)
- Jeden przypadek gdzie skill NIE powinien triggerować

Dla każdego testu określ asercje:
- Co output MUSI zawierać?
- Co output NIE MOŻE zawierać?
- Jaki format jest wymagany?

---

## Wskazówki dla konkretnych typów skillów

**Skille DOKODU_BRAIN (brain-*):**
- Zawsze zapisują do pliku w `/home/kacper/DOKODU_BRAIN/`
- Używają konwencji PARA (10_PROJECTS, 20_AREAS, 30_RESOURCES, 40_ARCHIVE)
- Frontmatter YAML w plikach które tworzą
- Język: polski

**Skille YouTube (yt-*):**
- Operują na plikach w `20_AREAS/AREA_YouTube/`
- Mogą korzystać ze skryptów w `scripts/`
- Zachowują dane historyczne (append, nie overwrite)

**Skille generyczne:**
- Nie zakładają konkretnej struktury katalogów
- Dokumentują wymagania środowiskowe
