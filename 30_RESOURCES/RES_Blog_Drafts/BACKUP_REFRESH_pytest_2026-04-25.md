---
backup: python/testowanie/testowanie-z-pytest
id: cmls1wozk003qw3hss3qxusu8
original_title: Testowanie z pytest – prostsze i szybsze testy w Pythonie
---

Jeśli już znasz podstawy testowania w Pythonie z modułem `unittest`, czas przejść na wyższy poziom. **pytest** to najpopularniejszy framework do testowania w Pythonie, który oferuje prostszą składnię, automatyczne wykrywanie testów, potężne fixture'y i wiele innych funkcji, które sprawiają, że pisanie testów jest szybsze i przyjemniejsze. W tym artykule poznasz, dlaczego pytest stał się standardem w branży i jak wykorzystać jego możliwości w swoich projektach.

## Dlaczego pytest zamiast unittest?

Chociaż `unittest` jest wbudowany w Pythonie i działa dobrze, pytest oferuje kilka kluczowych zalet, które czynią go lepszym wyborem dla większości projektów:

- **Prostsza składnia** – nie musisz tworzyć klas, wystarczy funkcja z nazwą zaczynającą się od `test_`
- **Automatyczne wykrywanie testów** – pytest sam znajdzie wszystkie testy w projekcie
- **Lepsze komunikaty błędów** – czytelniejsze raporty o niepowodzeniach testów
- **Fixture'y** – zaawansowany system zarządzania zasobami testowymi
- **Parametryzacja** – łatwe testowanie wielu scenariuszy jedną funkcją
- **Markery** – kategoryzacja i selektywne uruchamianie testów
- **Pluginy** – ogromny ekosystem rozszerzeń

Jeśli dopiero zaczynasz przygodę z testowaniem, sprawdź najpierw [wprowadzenie do unittest](/blog/python/testowanie/testowanie-jednostkowe-w-pythonie-wprowadzenie-do-unittest), aby zrozumieć podstawowe koncepcje.

## Instalacja pytest

Instalacja pytest jest bardzo prosta. Wystarczy użyć pip:

```bash
pip install pytest
```

Aby sprawdzić, czy instalacja się powiodła:

```bash
pytest --version
```

Dla projektów produkcyjnych warto również zainstalować `pytest-cov` do mierzenia pokrycia kodu:

```bash
pip install pytest-cov
```

## Podstawy pisania testów w pytest

### Prosty test jako funkcja

W przeciwieństwie do `unittest`, w pytest nie musisz tworzyć klas. Wystarczy zwykła funkcja:

```python
# test_calculator.py - przykładowe testy jednostkowe
def test_dodawanie():
    assert 2 + 2 == 4

def test_odejmowanie():
    assert 5 - 3 == 2

def test_mnozenie():
    assert 3 * 4 == 12

def test_dzielenie():
    assert 10 / 2 == 5
```

To wszystko! Uruchom testy za pomocą:

```bash
pytest test_calculator.py
```

lub po prostu:

```bash
pytest
```

pytest automatycznie znajdzie wszystkie pliki zaczynające się od `test_` lub kończące się na `_test.py` oraz funkcje zaczynające się od `test_`.

### Asercje w pytest

W pytest używamy standardowej instrukcji `assert`. Jeśli asercja się nie powiedzie, pytest automatycznie pokaże szczegółowe informacje o błędzie:

```python
def test_string_porownanie():
    assert "hello" == "world"# To się nie powiedzie z czytelnym komunikatem
```

Uruchomienie tego testu pokaże:

```bash
AssertionError: assert 'hello' == 'world'
- hello
+ world
```

### Testowanie funkcji – praktyczny przykład

Załóżmy, że mamy funkcję obliczającą średnią ocen:

```python
# calculator.py
def srednia_ocen(oceny):
    if not oceny:
        raise ValueError("Lista ocen nie może być pusta")
    return sum(oceny) / len(oceny)
```

Test w pytest może wyglądać tak:

```python
# tests/test_calculator.py - przykładowe testy funkcji srednia_ocen
import pytest
from calculator import srednia_ocen

def test_srednia_ocen_podstawowa():
    assert srednia_ocen([5, 4, 3, 5]) == 4.25

def test_srednia_ocen_jedna_ocena():
    assert srednia_ocen([5]) == 5.0

def test_srednia_ocen_pusta_lista():
    with pytest.raises(ValueError):
        srednia_ocen([])
```

### Testowanie wyjątków

W pytest do sprawdzania, czy funkcja rzuca wyjątek, używamy `pytest.raises()`:

```python
import pytest

def test_dzielenie_przez_zero():
    with pytest.raises(ZeroDivisionError):
        wynik = 10 / 0

def test_wyjatek_z_komunikatem():
    with pytest.raises(ValueError, match="nie może być pusta"):
        srednia_ocen([])
```

Parametr `match` pozwala sprawdzić, czy komunikat błędu zawiera określony tekst.

## Fixture'y – potężny mechanizm pytest

Fixture'y to jedna z najpotężniejszych funkcji pytest. Pozwalają na tworzenie danych testowych i zasobów, które są automatycznie udostępniane testom. Fixture'y eliminują powtarzający się kod i zapewniają spójność między testami.

### Podstawowy fixture

```python
import pytest

@pytest.fixture
def przykladowe_oceny():
    return [5, 4, 3, 5, 4]

def test_srednia_z_fixture(przykladowe_oceny):
    assert srednia_ocen(przykladowe_oceny) == 4.2
```

Fixture automatycznie wykonuje się przed testem i jego wynik jest przekazywany jako parametr.

### Fixture'y ze scope

Fixture'y mogą mieć różne zakresy żywotności:

```python
@pytest.fixture(scope="function")# Domyślny – wykonuje się dla każdego testu
def tymczasowe_dane():
    return {"temp": "data"}

@pytest.fixture(scope="class")# Wykonuje się raz na klasę
def wspolne_dane_dla_klasy():
    return {"shared": "data"}

@pytest.fixture(scope="module")# Wykonuje się raz na moduł
def wspolne_dane_dla_modulu():
    return {"module": "data"}

@pytest.fixture(scope="session")# Wykonuje się raz na całą sesję testów
def baza_danych():
    # Kosztowne połączenie z bazą danych
    db = connect_to_database()
    yield db# yield zamiast return pozwala na cleanup
    db.close()
```

### Fixture'y z cleanup (tearDown)

Używając `yield` zamiast `return`, możemy dodać kod wykonujący się po teście:

```python
@pytest.fixture
def plik_tymczasowy(tmp_path):
    plik = tmp_path / "test.txt"
    plik.write_text("test")
    yield plik

    # Tu można dodać cleanup, np. usunięcie pliku
    # W tym przypadku pytest automatycznie usunie tmp_path
```

### Fixture'y zależne od innych fixture'ów

Fixture'y mogą używać innych fixture'ów:

```python
@pytest.fixture
def uzytkownik():
    return {"id": 1, "name": "Jan"}

@pytest.fixture
def autoryzowany_uzytkownik(uzytkownik):
    uzytkownik["token"] = "abc123"
    return uzytkownik

def test_dostep_z_autoryzacją(autoryzowany_uzytkownik):
    assert autoryzowany_uzytkownik["token"] == "abc123"
```

### Wbudowane fixture'y pytest

pytest oferuje wiele przydatnych wbudowanych fixture'ów:

- `tmp_path` / `tmp_path_factory` – ścieżki do tymczasowych katalogów
- `tmpdir` / `tmpdir_factory` – tymczasowe katalogi (starsza wersja)
- `monkeypatch` – tymczasowa modyfikacja obiektów
- `capsys` – przechwytywanie stdout/stderr
- `caplog` – przechwytywanie logów

Przykład użycia `monkeypatch`:

```python
def test_environment_variable(monkeypatch):
    monkeypatch.setenv("TEST_VAR", "test_value")
    import os
    assert os.getenv("TEST_VAR") == "test_value"
```

## Parametryzacja testów

Parametryzacja pozwala uruchomić ten sam test z różnymi danymi wejściowymi. To eliminuje duplikację kodu:

```python
@pytest.mark.parametrize("a, b, expected", [
(2, 2, 4),
(3, 5, 8),
(0, 0, 0),
(-1, 1, 0),
])
def test_dodawanie(a, b, expected):
    assert a + b == expected
```

pytest uruchomi ten test 4 razy, raz dla każdej krotki danych.

### Parametryzacja z nazwami testów

Możesz nadać nazwy poszczególnym przypadkom testowym:

```python
@pytest.mark.parametrize("a, b, expected", [
(2, 2, 4),
(3, 5, 8),
(0, 0, 0),
], ids=["dodatnie", "mieszane", "zera"])
def test_dodawanie(a, b, expected):
    assert a + b == expected
```

### Zagnieżdżona parametryzacja

Można parametryzować na różnych poziomach:

```python
@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", [3, 4])
def test_mnozenie(x, y):
    assert isinstance(x * y, int)
    # Uruchomi się 4 razy: (1,3), (1,4), (2,3), (2,4)
```

## Markery – kategoryzacja testów

Markery pozwalają oznaczać testy i selektywnie je uruchamiać:

```python
@pytest.mark.slow
def test_dlugo_trwajacy_test():
    # Test, który trwa długo
    time.sleep(5)
    assert True

@pytest.mark.integration
def test_integracja_z_baza():
    # Test integracyjny
    pass

@pytest.mark.skip(reason="Nie jest jeszcze zaimplementowane")
def test_nowa_funkcjonalnosc():
    pass

@pytest.mark.skipif(sys.platform == "win32", reason="Działa tylko na Linux/Mac")
def test_unix_only():
    pass

@pytest.mark.xfail(reason="Znany bug, naprawimy później")
def test_znany_bug():
    assert False
```

Uruchamianie testów z markerami:

```bash
pytest -m slow# Uruchom tylko testy oznaczone jako slow
pytest -m "not slow"# Uruchom wszystkie oprócz slow
pytest -m integration # Tylko testy integracyjne
```

Aby używać niestandardowych markerów, dodaj do `pytest.ini`:

```ini
[pytest]
markers =
slow: oznacza testy, które trwają długo
integration: testy integracyjne
api: testy API
```

## Testowanie klas i obiektów

Chociaż pytest preferuje funkcje, możesz też testować klasy:

```python
class TestCalculator:
def test_dodawanie(self):
    assert 2 + 2 == 4

def test_odejmowanie(self):
    assert 5 - 3 == 2

@pytest.fixture
def calculator(self):
    return Calculator()

def test_z_fixture(self, calculator):
    assert calculator.add(2, 3) == 5
```

## Testowanie z mockowaniem

Chociaż pytest nie ma wbudowanego mockowania, świetnie współpracuje z `unittest.mock`:

```python
from unittest.mock import Mock, patch

def test_z_mockiem():
    mock_api = Mock()
    mock_api.get.return_value = {"status": "ok"}

    wynik = mock_api.get()
    assert wynik["status"] == "ok"
    mock_api.get.assert_called_once()

@patch('requests.get')
def test_patch_dekorator(mock_get):
    mock_get.return_value.json.return_value = {"data": "test"}
    # Twój kod używający requests.get
    pass
```

Więcej o mockowaniu dowiesz się w artykule o [mockowaniu i fixture'ach](/blog/python/testowanie/mockowanie-i-fixture-w-testach-python).

## Konfiguracja pytest

Plik `pytest.ini` pozwala skonfigurować pytest dla całego projektu:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
-v
--strict-markers
--tb=short
markers =
slow: oznacza testy, które trwają długo
integration: testy integracyjne
```

Lub w `setup.cfg`:

```ini
[tool:pytest]
testpaths = tests
addopts = -v --strict-markers
```

## Wskazówki i najlepsze praktyki

### 1. Organizacja plików testowych

Dobra struktura projektu testowego:

```
projekt/
├── src/
│ └── calculator.py
└── tests/
├── __init__.py
├── test_calculator.py
├── conftest.py# Wspólne fixture'y
└── integration/
└── test_api.py
```

### 2. conftest.py dla wspólnych fixture'ów

Plik `conftest.py` może znajdować się w każdym katalogu i jego fixture'y są dostępne dla wszystkich testów w tym katalogu i podkatalogach:

```python
# tests/conftest.py
import pytest

@pytest.fixture
def domyslne_dane():
    return {"default": "data"}
```

### 3. Unikanie zależności między testami

Każdy test powinien być niezależny i móc być uruchomiony w dowolnej kolejności. Nie polegaj na stanie globalnym lub poprzednich testach.

### 4. Testy powinny być szybkie

Jeśli test jest wolny, oznaczenie go markerem `@pytest.mark.slow` pozwala uruchamiać go tylko gdy potrzeba.

### 5. Używaj czytelnych nazw

Nazwa testu powinna jasno komunikować, co testuje:

```python
# Dobrze
def test_srednia_ocen_zwraca_zero_dla_pustej_listy():
    pass

# Źle
def test1():
    pass
```

### 6. AAA Pattern (Arrange-Act-Assert)

Organizuj test w trzy sekcje:

```python
def test_srednia_ocen():
    # Arrange - przygotowanie danych
    oceny = [5, 4, 3]

    # Act - wykonanie akcji
    wynik = srednia_ocen(oceny)

    # Assert - weryfikacja wyniku
    assert wynik == 4.0
```

## Pytest vs unittest – kiedy użyć którego?

- **Użyj pytest**, jeśli chcesz:
- Prostszej składni
- Zaawansowanych fixture'ów
- Dużego ekosystemu pluginów
- Lepszej integracji z CI/CD

- **Użyj unittest**, jeśli:
- Musisz używać wbudowanych modułów Pythona
- Współpracujesz z kodem bazującym na unittest
- Pracujesz w środowisku, gdzie pytest nie jest dostępny

Większość projektów używa pytest jako standardu.

## Integracja z innymi narzędziami

pytest świetnie integruje się z:

- **coverage.py** – mierzenie pokrycia kodu:
```bash
pytest --cov=src --cov-report=html
```
Więcej o coverage w artykule [Coverage i mierzenie jakości testów](/blog/python/testowanie/coverage-i-jak-mierzyc-jakosc-kodu).

- **CI/CD** – pytest jest standardem w GitHub Actions, GitLab CI i Jenkins. Przeczytaj więcej o [automatyzacji testów w GitHub Actions](/blog/python/testowanie/testowanie-i-ci-cd-github-actions).

- **IDE** – VS Code, PyCharm i inne IDE mają doskonałe wsparcie dla pytest.

## Podsumowanie

pytest to potężne narzędzie, które znacznie upraszcza i przyspiesza pisanie testów w Pythonie. Kluczowe korzyści to:

- ✅ Prostsza składnia niż unittest
- ✅ Automatyczne wykrywanie testów
- ✅ Fixture'y do zarządzania zasobami
- ✅ Parametryzacja dla testowania wielu scenariuszy
- ✅ Markery do kategoryzacji testów
- ✅ Ogromny ekosystem pluginów

Jeśli jeszcze nie używasz pytest, czas zacząć! Zacznij od prostych testów funkcjonalnych, a następnie poznaj fixture'y i parametryzację. Te narzędzia szybko staną się niezastąpione w Twoim codziennym workflow.

## Co dalej?

Teraz, gdy znasz podstawy pytest, możesz przejść do bardziej zaawansowanych tematów:

- [Testy integracyjne API w FastAPI i Django](/blog/python/testowanie/integracyjne-testy-api-fastapi-django) – naucz się testować całe aplikacje webowe
- [Mockowanie i fixture'y w testach Python](/blog/python/testowanie/mockowanie-i-fixture-w-testach-python) – zaawansowane techniki izolacji testów
- [Coverage i mierzenie jakości testów](/blog/python/testowanie/coverage-i-jak-mierzyc-jakosc-kodu) – sprawdź, ile kodu rzeczywiście testujesz

Pamiętaj, że testy to inwestycja w przyszłość projektu – im lepsze testy, tym łatwiej rozwijać i utrzymywać kod!