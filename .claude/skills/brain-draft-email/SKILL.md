---
name: brain-draft-email
description: Pisze gotowy email do klienta Dokodu na podstawie profilu klienta i kontekstu projektu. Zna styl Kacpra — konkretny, ciepły, bez korporacyjnego bełkotu. Trigger: "napisz email do [klient]", "przygotuj wiadomość do", "zredaguj maila", /brain-draft-email
---

# brain-draft-email

## Cel

Generuje gotowego emaila do wysłania — nie szkielet, nie template z [WSTAW TU]. Gotowy tekst, który można skopiować i wysłać.

## KROK 1: Zbierz kontekst

Zapytaj (jeśli nie podane):
1. **Do kogo?** — nazwa klienta lub imię osoby
2. **W jakiej sprawie?** — 1 zdanie opisu celu emaila

Nie pytaj o nic więcej. Resztę wyciągnij z BRAIN.

## KROK 2: Załaduj dane z BRAIN

Wczytaj:
- `20_AREAS/AREA_Customers/[Klient]/[Klient]_Profile.md` — kontakt, kontekst, historia
- `20_AREAS/AREA_Customers/[Klient]/[Klient]_Meetings.md` — ostatnie ustalenia
- Aktywny projekt klienta z `10_PROJECTS/` jeśli istnieje

Wyciągnij: imię osoby kontaktowej, email, ostatnie ustalenia, aktualny status projektu.

## KROK 3: Napisz email

### Styl Kacpra (przestrzegaj ściśle):
- **Zwrot:** "Cześć [Imię]," — zawsze po imieniu, nigdy "Szanowny Pan"
- **Długość:** max 5-7 zdań. Jeden akapit jeśli możliwe.
- **Ton:** konkretny, ciepły, partnerski. Bez "Uprzejmie informuję", "W nawiązaniu do".
- **CTA:** jedno, konkretne zdanie na końcu — co chcesz żeby zrobił
- **Podpis:** Kacper + opcjonalnie "Kacper Sieradzński | Dokodu | kacper@dokodu.it | 508 106 046"

### Struktura:
```
Cześć [Imię],

[Kontekst w 1 zdaniu jeśli potrzebny]

[Sedno sprawy — konkretnie co chcesz / co proponujesz]

[CTA — jedno pytanie lub prośba]

Kacper
```

### Przykłady dobrego stylu:
✅ "Cześć Kamilu, chciałem umówić terminy 6 sesji konsultacyjnych z umowy. Czy masz wolne okienka w tygodniu 7-11 kwietnia? Możemy zrobić to w jednym bloku — 3h i mamy z głowy."

❌ "Szanowny Panie Kamilu, w nawiązaniu do zawartej umowy o świadczenie usług szkoleniowych, niniejszym zwracam się z uprzejmą prośbą o ustalenie terminów konsultacji..."

## KROK 4: Przedstaw gotowy email

Pokaż email w bloku kodu (łatwy do skopiowania).

Następnie zapytaj:
- "Wysłać przez Gmail MCP?" (jeśli adres znany)
- "Coś zmienić?"

## KROK 5: Wyślij (opcjonalnie)

Jeśli użytkownik chce wysłać przez Gmail MCP:
- Użyj `mcp__gmail__send_email` lub `mcp__gmail__draft_email`
- Potwierdź przed wysłaniem: "Wysyłam do [email] — potwierdzasz?"

## ZASADY

- Nigdy nie wymyślaj faktów których nie ma w BRAIN — opieraj się tylko na danych
- Jeśli brakuje emaila kontaktowego → podaj imię i zaznacz "uzupełnij adres"
- Jeden email = jedna sprawa. Nie pakuj dwóch tematów w jeden mail.
- Podpisuj zawsze jako Kacper, nie "Zespół Dokodu"
