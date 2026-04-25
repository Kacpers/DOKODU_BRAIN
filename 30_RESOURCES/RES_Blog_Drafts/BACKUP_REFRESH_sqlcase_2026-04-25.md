---
backup: sql/case-when-w-sql
id: cmls1wp9q0052w3hssa46q7zu
original_title: Instrukcja CASE WHEN w SQL
---

CASE WHEN to jedno z najczęściej używanych, a jednocześnie najbardziej niedocenianych narzędzi w SQL. Nie zmienia struktury danych, nie filtruje — ale potrafi zmienić sposób, w jaki myślisz o logice zapytań.

<AD:skumajbazy-newsletter>

Dzięki CASE możesz tworzyć kolumny warunkowe, etykietować dane, kategoryzować wyniki i porządkować raporty bez żadnych zewnętrznych if-ów w kodzie aplikacji. To wbudowany mechanizm warunkowy, który działa w SELECT, ORDER BY, GROUP BY i HAVING, pozwalając budować dynamiczne zachowania bez wychodzenia poza SQL.

W tym artykule poznasz składnię CASE WHEN, różnice między jego wariantami, przykłady praktyczne oraz sytuacje, w których lepiej użyć czegoś innego. Po tej lekturze Twoje zapytania będą nie tylko działały — będą **myśleć**.

# Instrukcja CASE WHEN w SQL


## Czym jest CASE WHEN
CASE to wyrażenie warunkowe, a nie osobna instrukcja sterująca. Zwraca jedną wartość w oparciu o warunki, dlatego świetnie nadaje się do tworzenia kolumn pochodnych, etykiet, przedziałów i sortowań. Instrukcja CASE WHEN w SQL występuje w dwóch wariantach: porównującym pojedynczą wartość (simple CASE) i warunkowym (searched CASE).

CASE WHEN w SQL działa w SELECT, WHERE, ORDER BY, GROUP BY i HAVING. Najczęściej używamy go jako CASE w SELECT do kategoryzacji i czyszczenia danych. Jeśli dopiero zaczynasz, przypomnij sobie składnię klauzul w materiale: [Podstawy SQL: SELECT, WHERE, JOIN, GROUP BY](/blog/sql/podstawy-sql-select-where-join-group-by).

<AD:mysql_ebook>

## Składnia podstawowa
Dwa warianty:

- Searched CASE (najczęstszy): warunki logiczne po WHEN.

```sql
SELECT
  CASE
    WHEN score >= 90 THEN 'A'
    WHEN score >= 75 THEN 'B'
    WHEN score >= 60 THEN 'C'
    ELSE 'F'
  END AS grade
FROM exams;
```

- Simple CASE: porównania do tej samej wartości wejściowej.

```sql
SELECT
  CASE status
    WHEN 'new'  THEN 'Nowe'
    WHEN 'paid' THEN 'Opłacone'
    ELSE 'Inne'
  END AS status_label
FROM orders;
```

ELSE jest opcjonalne. Gdy go brak i żaden warunek nie pasuje, wynik to NULL. Wszystkie gałęzie powinny zwracać kompatybilne typy.

## Przykłady użycia
CASE w SELECT do etykietowania i łączenia z agregacją:

```sql
SELECT
  CASE
    WHEN amount >= 1000 THEN 'duże'
    WHEN amount >= 200  THEN 'średnie'
    ELSE 'małe'
  END AS koszyk,
  COUNT(*) AS liczba
FROM payments
GROUP BY
  CASE
    WHEN amount >= 1000 THEN 'duże'
    WHEN amount >= 200  THEN 'średnie'
    ELSE 'małe'
  END
ORDER BY liczba DESC;
```

CASE w ORDER BY do niestandardowego sortowania:

```sql
SELECT id, status
FROM tickets
ORDER BY
  CASE status
    WHEN 'critical' THEN 1
    WHEN 'high'     THEN 2
    WHEN 'medium'   THEN 3
    WHEN 'low'      THEN 4
    ELSE 5
  END,
  created_at DESC;
```

Przy agregacjach warunkowych często wygodniej liczyć selektywnie w jednej kwerendzie niż robić kilka zapytań. Zobacz też: [Funkcje agregujące w SQL](/blog/sql/funkcje-agregujace-w-sql).

## Zagnieżdżone CASE
Zagnieżdżone CASE pozwala budować hierarchię decyzji. Dbaj o czytelność i kolejność warunków od najbardziej restrykcyjnych do najmniej.

```sql
SELECT
  CASE
    WHEN status = 'cancelled' THEN 'anulowane'
    WHEN status = 'paid' THEN
      CASE
        WHEN amount >= 1000 THEN 'paid_big'
        ELSE 'paid_regular'
      END
    WHEN status = 'pending' THEN 'oczekujące'
    ELSE 'inne'
  END AS kategoria
FROM invoices;
```

Jeśli zagnieżdżenia rosną, rozważ rozbicie logiki na CTE lub tabelę słownikową. To ułatwia testy i utrzymanie.

## CASE w praktyce
Typy zwracane przez gałęzie muszą być zgodne. Silnik wybierze typ docelowy i może wymusić konwersje. ELSE domyślnie daje NULL, co wpływa na agregacje i porównania.

Wydajność: CASE w predykacie na kolumnie często uniemożliwia użycie indeksu. Zamiast:
```sql
-- słabo: CASE w WHERE opakowuje kolumnę
SELECT * FROM sales
WHERE CASE WHEN region = 'EU' THEN amount ELSE 0 END > 100;
```
lepiej zapisać równoważnie z OR, aby pozostać sargowalnym:
```sql
SELECT * FROM sales
WHERE (region = 'EU' AND amount > 100)
   OR (region <> 'EU' AND 0 > 100); -- ta gałąź i tak odpada
```

Uważaj na błędy wykonania jak dzielenie przez zero. Owiń ryzykowną część w CASE:
```sql
SELECT
  CASE WHEN denominator = 0 THEN NULL ELSE numerator / denominator END AS ratio
FROM metrics;
```
CASE dobrze współpracuje z oknami (np. selektywne PARTITION BY lub warunkowe sumy w OVER). Jeśli używasz funkcji okienkowych, zajrzyj do: [Funkcje okienkowe w SQL: PostgreSQL i MySQL](/blog/sql/funkcje-okienkowe-sql-postgresql-i-mysql).

## Alternatywy dla CASE
Proste zamienniki:
- COALESCE do wartości domyślnych zamiast CASE WHEN x IS NULL.
- NULLIF do bezpiecznego dzielenia.
- DECODE (Oracle), IF (MySQL), IIF (SQL Server) jako skróty dialektowe.

Przykłady:
```sql
-- Domyślna wartość zamiast CASE
SELECT COALESCE(nickname, 'anon') AS name FROM users;

-- Uniknięcie dzielenia przez zero
SELECT numerator / NULLIF(denominator, 0) AS ratio FROM metrics;

-- MySQL
SELECT IF(score >= 60, 'pass', 'fail') AS result FROM exams;

-- SQL Server
SELECT IIF(active = 1, 'on', 'off') AS flag FROM devices;
```

Złożone mapowania lepiej trzymać w tabelach słownikowych i JOIN-ować. Alternatywnie użyj CTE, gdy logika jest wieloetapowa: [Podzapytania i CTE w SQL](/blog/sql/podzapytania-i-cte-w-sql).

## Podsumowanie
Instrukcja CASE WHEN w SQL to uniwersalne narzędzie do warunkowego wyliczania wartości. Działa w SELECT, ORDER BY, GROUP BY i HAVING, pozwalając etykietować, sortować i agregować w jednym przebiegu.

Wybieraj searched CASE do dowolnych warunków, a simple CASE do porównań jednej wartości. Dbaj o zgodność typów, unikaj owijania indeksowanych kolumn w WHERE, a większą logikę przenoś do CTE lub tabel referencyjnych. Dzięki temu CASE w SELECT pozostanie czytelny i szybki.

<AD:skumajbazy_course>