---
type: analiza
status: active
owner: kacper
created: 2026-03-30
tags: [pystart, kurs, python, mapa-tresci, ai-integration]
---

# PyStart — Mapa Treści Kursu + Okazje AI

> Źródło: analiza transkrypcji z `30_RESOURCES/RES_Kursy_Transkrypcje/pystart/`

---

## Przegląd modułów

| Moduł | Temat | Kluczowe koncepty | Projekt/ćwiczenie | Biblioteki |
|:--|:--|:--|:--|:--|
| 1 | Pierwszy krok | Zmienne, typy, if/elif/else, operatory | Kalkulator, walidacja | PyCharm, venv |
| 2 | Kolekcje i pętle | Stringi, tuple, range, pętla for, slicing | Praca z tekstem, iteracja | enumerate, sorted |
| 3 | Listy, słowniki | Listy (mutowalne), słowniki, random | Papier/Kamień/Nożyce, Dinner Generator | random |
| 4 | Pętle i debug | While, match/case, debugger, breakpointy | Walidacja PESEL-u | time, debugger |
| 5 | Funkcje | def/return, scope, argumenty domyślne, rekurencja | Silnia, Fibonacci | — |
| 6 | Projekt i testy | Moduły, pakiety, pytest/TDD, setup.py, pip | Własny pakiet, testy | pytest, pip |
| 7 | Biblioteka std | JSON, pliki I/O, Tkinter GUI, REST API | Gra "Zgadnij liczbę", API pogoda | json, tkinter, requests |
| 8 | Bazy i system | SQLite, os/pathlib, argparse, Pillow, subprocess | CRUD na bazie, narzędzie CLI | sqlite3, argparse, Pillow |
| 9 | OOP | Klasy, dziedziczenie, enkapsulacja, wyjątki, try/except | Student, hierarchia Animal | — |
| 10 | Projekt końcowy | MVC, planowanie, asocjacje DB, Big O | Aplikacja CRUD z DB + CLI/GUI | sqlite3, argparse |

---

## Szczegóły modułów

### Moduł 1: Pierwszy krok do programowania
**Sekcje:** Informacje organizacyjne → Czas zadbać o środowisko → Python → Nauka programowania → Wszyscy do kodu → Praca domowa

**Czego uczy:**
- Środowisko: PyCharm, venv, instalacja Pythona
- Pierwszy program: print(), input(), f-stringi
- Zmienne: int, float, str, bool ("wszystko jest obiektem")
- Operatory: +, -, *, /, //, %, **
- if/elif/else, operatory logiczne (AND, OR), short-circuit evaluation
- Konwencje: snake_case, komentarze

**🤖 Gdzie wchodzi AI:**
- Debugowanie logiki warunkowej — "dlaczego ten if nie działa?"
- Wyjaśnianie typów — "czemu int + str daje błąd?"

---

### Moduł 2: Kolekcje i pętle
**Sekcje:** Rozwiązanie PD z M1 → Stringi → Tuple → Range → For → Praca domowa

**Czego uczy:**
- Stringi: indeksowanie (od 0), slicing [start:end:step], metody (.upper, .split, .join, .find, .replace)
- Tuple: niemutowalne, indeksowanie, enumerate(), rozpakowanie
- Range: range(stop), range(start, stop, step)
- Pętla for: iteracja, enumerate(), reversed(), sorted()
- Funkcje: len(), min(), max(), sum()

**🤖 Gdzie wchodzi AI:**
- Interaktywny sandbox do slicingu — "co zwróci text[2::3]?"
- Optymalizacja pętli — kiedy enumerate() zamiast ręcznego licznika

---

### Moduł 3: Listy, słowniki, losowość
**Sekcje:** Rozwiązanie PD z M2 → Listy → Słowniki → Połączenie list i słowników → Pseudolosowość → Mini-projekt → Praca domowa

**Czego uczy:**
- Listy (mutowalne): append, insert, remove, pop, sort vs sorted
- Słowniki: klucze (niemutowalne), .get(), .items(), .keys(), .values(), del
- Zagnieżdżone struktury: lista słowników (baza w pamięci)
- random: choice(), randint(), shuffle(), seed()

**🤖 Gdzie wchodzi AI:**
- Wizualizacja zagnieżdżonych struktur — "jak dostać się do list[2]['name']?"
- Generowanie testowych danych do ćwiczeń

---

### Moduł 4: Zaawansowane pętle i debugowanie
**Sekcje:** Rozwiązanie PD z M3 → While → Match Case → Zbiory → Debugowanie → Mini-projekt PESEL → Praca domowa

**Czego uczy:**
- While: warunek, while True, break, time.sleep()
- Match/case (Python 3.10+)
- Zbiory (sets)
- **Debugger**: breakpointy, Step Into/Over/Out, Evaluate Expression, obserwacja zmiennych

**🤖 Gdzie wchodzi AI:**
- Claude Code jako "debugger coach" — pokazuje krok po kroku co się dzieje
- "Dlaczego pętla się nie kończy?" — analiza warunku

---

### Moduł 5: Funkcje
**Sekcje:** Rozwiązanie PD z M4 → Wstęp do funkcji → Argumenty → Dokumentowanie → Rekurencja → Praca domowa

**Czego uczy:**
- def/return, scope (lokalne vs globalne)
- Argumenty domyślne, nadpisywanie
- Zwracanie wielu wartości (tuple)
- Rekurencja: warunek bazowy, stos wywołań, silnia, Fibonacci
- Dokumentowanie: docstringi

**🤖 Gdzie wchodzi AI:**
- Wizualizacja stosu rekurencji
- "Czy ta funkcja powinna być podzielona na mniejsze?"
- Generowanie docstringów

---

### Moduł 6: Projektowanie i dystrybucja
**Sekcje:** Rozwiązanie PD z M5 → Args i kwargs → Projekt/moduły/pakiety → Pytest & TDD → Zależności → Dystrybucja → Praca domowa

**Czego uczy:**
- *args, **kwargs
- Moduły (.py), pakiety (__init__.py), importy
- **Pytest & TDD**: Arrange-Act-Assert, pisanie testów przed kodem
- requirements.txt, pip, venv
- setup.py, dystrybucja na PyPI

**🤖 Gdzie wchodzi AI:**
- **Generowanie testów** — "napisz testy dla tej funkcji"
- Sugestia struktury projektu
- Analiza pokrycia testami

---

### Moduł 7: Biblioteka standardowa
**Sekcje:** Rozwiązanie PD z M6 → JSON → Pliki → Data → Tkinter → Praca domowa

**Czego uczy:**
- JSON: dumps/loads (stringi), dump/load (pliki)
- Pliki: open(), tryby r/w/a, context manager (with), readline/readlines
- Datetime
- **Tkinter**: okna, przyciski, pola tekstowe, event handling
- REST API: requests, parsowanie JSON z API

**🤖 Gdzie wchodzi AI:**
- "Narysuj mi tę aplikację w Tkinter" → generowanie kodu GUI
- Debugowanie skomplikowanych struktur JSON
- Pomoc z dokumentacją API

---

### Moduł 8: Bazy danych i system plików
**Sekcje:** Rozwiązanie PD z M7 → SQLite → System plików → CSV → Wykresy → Obrazy → Subprocess → Argparse → Praca domowa

**Czego uczy:**
- **SQLite**: connect, cursor, CREATE/INSERT/SELECT/UPDATE/DELETE, commit
- os/pathlib: walk, listdir, Path, suffix, is_file/is_dir
- CSV: czytanie/pisanie
- Matplotlib: wykresy
- Pillow: resize, crop, rotate
- Subprocess: uruchamianie komend systemowych
- **Argparse**: ArgumentParser, add_argument, parse_args

**🤖 Gdzie wchodzi AI:**
- **"Chcę pobrać dane gdzie..." → generator SQL**
- Automatyczna konwersja os.path na pathlib
- Generowanie kodu argparse dla CLI

---

### Moduł 9: Programowanie obiektowe
**Sekcje:** Rozwiązanie PD z M8 → Obiektowość → Dziedziczenie → Enkapsulacja → Metody specjalne → Wyjątki → Łączenie obiektów (Kompozycja) → Praca domowa

**Czego uczy:**
- Klasy: class, __init__, self
- Dziedziczenie: class Child(Parent), super(), override, polimorfizm
- Enkapsulacja: _private, __very_private, property
- Metody specjalne: __str__, __repr__, __len__, __eq__
- **Wyjątki**: try/except/else/finally, raise, własne wyjątki
- Kompozycja vs dziedziczenie

**🤖 Gdzie wchodzi AI:**
- Diagramy UML hierarchii klas
- "Jak to zmienić na klasy?" — refaktoryzacja proceduralnego kodu
- Code review klasy — "co tu poprawić?"

---

### Moduł 10: Projekt integrujący
**Sekcje:** Rozwiązanie PD z M9 → Zanim usiądziesz do kodu → MVC → Więcej o bazach danych → Projekt → Zakończenie

**Czego uczy:**
- Planowanie: analiza wymagań, use cases, podział na zadania
- **MVC**: Model (DB) → View (UI) → Controller (logika)
- Asocjacje: 1:1, 1:n, n:m, klucze obce
- Projekt końcowy: CRUD z DB + CLI/GUI + obsługa błędów + statystyki

**🤖 Gdzie wchodzi AI:**
- "Zaproponuj architekturę dla mojego projektu"
- Generator schematów baz danych
- Code review projektu końcowego
- Automatyczna dokumentacja

---

## Mapowanie: Moduły AI ← Obecna treść

### BONUS 1: "Python + AI asystent kodowania" (~3-4h)

| Lekcja bonus | Nawiązuje do modułu | Co rozszerza |
|:--|:--|:--|
| Kodowanie z Copilot/Claude Code | M1-M5 (wszystkie ćwiczenia) | Zamiast pisać od zera → pisz Z AI |
| Prompt engineering dla programistów | M4 (debugowanie) | "Jak opisać problem żeby AI go rozwiązał" |
| Debugging z AI | M4 (breakpointy, debugger) | Claude Code jako debugger coach |
| Ćwiczenie: 5 zadań — sam vs z AI | M2-M5 (prace domowe) | Porównanie podejść, kiedy AI pomaga a kiedy przeszkadza |
| Refaktoryzacja z AI | M6 (moduły, pakiety) | "Podziel ten kod na moduły" z pomocą AI |

### BONUS 2: "API OpenAI/Anthropic z Pythona" (~4-5h)

| Lekcja bonus | Nawiązuje do modułu | Co rozszerza |
|:--|:--|:--|
| Co to LLM (bez matmy) | M1 (wstęp) | Kontekst: dlaczego Python + AI |
| Pierwszy request do API | M7 (requests, JSON, REST API) | requests + OpenAI API zamiast API pogody |
| Chatbot konsolowy | M5 (funkcje) + M4 (while True) | Pętla while + input + API = chatbot |
| Structured outputs (JSON mode) | M7 (JSON) | json.loads() na odpowiedzi AI |
| Projekt: Asystent CV | M7 (pliki) + M8 (argparse) | Czyta PDF → AI analizuje → output |
| Koszty API | M1 (operatory, obliczenia) | Kalkulator kosztów tokenów |

### BONUS 3: "Automatyzacja z Pythonem i AI" (~3-4h)

| Lekcja bonus | Nawiązuje do modułu | Co rozszerza |
|:--|:--|:--|
| Web scraping (requests + BS4) | M7 (requests, JSON) | Zamiast API → scraping stron |
| Excel/CSV + AI | M8 (CSV, pliki) | openpyxl + LLM do analizy danych |
| Automatyczny email | M7 (pliki) + M5 (funkcje) | smtplib — wysyłka raportu |
| Projekt: Bot cenowy | M3 (słowniki) + M8 (SQLite) | Scraping → DB → alert → AI analiza |
| Python ↔ n8n (webhook) | M7 (requests, API) | requests.post() do n8n webhook → preview kursu n8n |
