---
name: yt-repurpose
description: Przetwarza transkrypcję nagrania YouTube w blog post + post LinkedIn. Jeden film → artykuł na blogu + post LinkedIn gotowy do wklejenia. Trigger: "zrób blog post z filmu", "repurposing", "przeróbka na bloga", "artykuł z nagrania", /yt-repurpose
---

# Instrukcja: YT Repurpose

## Działanie

Bierze transkrypcję nagrania (wygenerowaną przez `/yt-transcribe`) i przetwarza ją w:
1. Kompletny draft artykułu na blog dokodu.it (przez `/blog-draft`)
2. Gotowy post LinkedIn do wklejenia

## KROK 1: Sprawdź czy jest transkrypcja

Przeczytaj: `movies/YT-XXX/publish/transkrypcja.txt`

Jeśli brak — powiedz: "Najpierw uruchom `/yt-transcribe YT-XXX --file nagranie.mp4`"

## KROK 2: Przeczytaj metadata

Przeczytaj: `movies/YT-XXX/metadata.md`
- Tytuł, tagi, opis YouTube — to jest kontekst SEO
- Sekcje scenariusza — to jest struktura artykułu

## KROK 3: Zbuduj brief SEO z transkrypcji

Na podstawie transkrypcji i metadata zbuduj brief:

```
Główna fraza kluczowa: [wyciągnij z tytułu/tagów]
Typ contentu: how-to / tutorial
Docelowy czytelnik: developer lub manager IT w polskiej firmie

Struktura (na podstawie sekcji scenariusza):
- H2 dla każdej głównej sekcji ze scenariusza
- Treść H2 uzupełniona transkrypcją z tej sekcji
- Przykłady kodu/komend przepisane z transkrypcji
```

## KROK 4: Napisz draft artykułu

Napisz kompletny artykuł który:
- **NIE jest transkrypcją** — to jest artykuł, nie przepisanie tego co powiedziano
- Zachowuje wszystkie konkretne przykłady, komendy, kod z nagrania
- Dodaje linki (których nie ma w filmie bo to wideo)
- Ma SEO intro, nagłówki H2/H3, listy gdzie pasuje
- Długość: 1500-2500 słów

Wyślij jako draft przez API bloga:
```bash
cd /home/kacper/DOKODU_BRAIN/scripts && python3 blog_publish.py create \
  --title "[SEO Title]" \
  --slug "[slug]" \
  --status draft
```

## KROK 5: Zaktualizuj post LinkedIn

Przeczytaj `movies/YT-XXX/publish/linkedin_post.txt` i uzupełnij placeholdery:
- 3 główne punkty wartości z artykułu
- Zapis do pliku

Pokaż gotowy post użytkownikowi do skopiowania.

## KROK 6: Zaproponuj następny krok

- "Draft artykułu jest na blogu — chcesz go przejrzeć i opublikować? (`/blog-publish`)"
- "Post LinkedIn gotowy w `publish/linkedin_post.txt` — skopiuj i wklej"

## ZASADY

- Artykuł musi być wartościowy sam w sobie — ktoś kto nie oglądał filmu powinien z niego skorzystać
- Zachowaj wszystkie komendy, ścieżki, kod — to jest największa wartość tutoriali technicznych
- Nie przepisuj 1:1 — artykuł ma inną strukturę niż mówiony scenariusz
- CTA na końcu artykułu: link do filmu YT + link do kursu n8n (jeśli relevant) lub konsultacji
- Slug artykułu: bez polskich znaków, myślniki, max 6 słów
