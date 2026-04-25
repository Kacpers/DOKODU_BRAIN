---
backup: python/podstawy/list-comprehension
id: cmls1wosu002kw3hs5xz2wnt7
original_title: List Comprehension w Pythonie - Praktyczne przykłady
---

List comprehension to jedna z najbardziej eleganckich i efektywnych technik w Pythonie, pozwalająca na tworzenie list w sposób zwięzły i czytelny. Poświęcając kilka minut na przeczytanie artykułu, dowiesz się, jak wykorzystać jej zalety, a także porównasz ją z tradycyjnymi metodami iteracji, co pozwoli Ci zdecydować, która metoda lepiej pasuje do Twojego stylu programowania.

## Co to jest list comprehension?

List comprehension to technika w Pythonie, która umożliwia tworzenie nowych list poprzez przekazywanie istniejących sekwencji danych przez jedną formułę. Zamiast pisać wiele linijek kodu z wykorzystaniem pętli `for`, list comprehension umożliwia zdefiniowanie listy w jednej linijce. Pozwala to na czytelniejsze i bardziej eleganckie rozwiązanie, zwłaszcza gdy przetwarzamy duże zbiory danych.

### Składnia list comprehension

Składnia wygląda następująco:

```python
[expression for item in iterable if condition]
```

- **expression** - operacja wykonywana na każdym elemencie.
- **for item in iterable** - iterowanie przez zbiór danych.
- **if condition** - opcjonalny warunek do filtrowania elementów.

## Praktyczne przykłady użycia list comprehension

### Przykład 1: Podnoszenie do kwadratu

Zamieńmy listę liczb na listę ich kwadratów.

#### Tradycyjna metoda z pętlą for

```python
numbers = [1, 2, 3, 4, 5]
squared_numbers = []

for number in numbers:
    squared_numbers.append(number ** 2)
```

#### Rozwiązanie z list comprehension

```python
squared_numbers = [number ** 2 for number in numbers]
```

### Przykład 2: Filtrowanie danych

Załóżmy, że chcemy wybrać tylko parzyste liczby z listy.

#### Tradycyjna metoda z pętlą for i warunkiem

```python
numbers = [1, 2, 3, 4, 5, 6]
even_numbers = []

for number in numbers:
    if number % 2 == 0:
        even_numbers.append(number)
```

#### Rozwiązanie z list comprehension i filtrowaniem

```python
even_numbers = [number for number in numbers if number % 2 == 0]
```

## Zalety list comprehension

1. **Zwięzłość**: Redukcja liczby linii kodu.
2. **Czytelność**: Zrozumiałe nawet dla początkujących, pod warunkiem znajomości składni.
3. **Wydajność**: Często szybsze wykonanie dzięki optymalizacji wewnętrznej Pythona.

## Porównanie z tradycyjnymi metodami iteracji

Choć list comprehension jest bardziej kompaktowy i często szybszy, tradycyjne metody iteracji mogą być bardziej przejrzyste w przypadku skomplikowanych operacji. Gdy kod wymaga rozbudowanej logiki i wielu operacji, klasyczne pętle są bardziej zrozumiałe dla osób, które jeszcze nie opanowały list comprehension.

## Podsumowanie

List comprehension to potężne narzędzie, które może znacznie uprościć operacje na listach w Pythonie. Jest doskonałym rozwiązaniem, gdy potrzebujesz stworzyć nowe listy w oparciu o istniejące w prosty i szybki sposób. Zachęcamy do eksperymentowania z tą techniką, co pozwoli Ci na znalezienie najlepszych zastosowań w Twoich projektach.