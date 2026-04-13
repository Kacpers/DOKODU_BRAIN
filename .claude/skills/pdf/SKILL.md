---
name: pdf
description: Czyta i analizuje pliki PDF — umowy, oferty, faktury, dokumenty. Dla umów automatycznie wyciąga kluczowe klauzule (strony, zakres, płatność, terminy, kary, prawa do logo/referencji). Trigger: podana ścieżka do .pdf, "przeanalizuj umowę", "przeczytaj PDF", "wyciągnij z umowy", /pdf
---

# PDF Skill

## Kiedy używać

- Użytkownik podaje ścieżkę do pliku .pdf
- Mówi "przeanalizuj umowę", "sprawdź kontrakt", "co jest w tym PDF"
- Pyta o konkretną klauzulę dokumentu

## KROK 1: Odczytaj plik

Użyj narzędzia Read z podaną ścieżką. Read obsługuje PDF bezpośrednio.

Jeśli plik ma >10 stron — czytaj po 10 stron naraz (pages: "1-10", "11-20" itd.).

## KROK 2: Rozpoznaj typ dokumentu

- **Umowa** → przejdź do ekstrakcji klauzul kontraktowych
- **Oferta/cennik** → wyciągnij: zakres usług, ceny, warunki
- **Faktura** → wyciągnij: kwota, termin płatności, dane stron
- **Inny** → podsumuj kluczowe informacje

## KROK 3a: Ekstrakcja dla UMÓW

Wyciągnij i przedstaw w ustrukturyzowanej formie:

### Strony umowy
- Zleceniodawca: nazwa, NIP, adres, osoba podpisująca
- Zleceniobiorca: nazwa, NIP, adres, osoba podpisująca
- Data zawarcia

### Przedmiot i zakres
- Co dokładnie jest przedmiotem umowy
- Szczegółowy zakres (załączniki)
- Terminy realizacji poszczególnych etapów

### Wynagrodzenie i płatności
- Kwota netto + VAT
- Struktura płatności (zaliczka / etapy / po realizacji)
- Termin płatności (dni od faktury)
- Adres do faktur
- Warunki wystawienia faktury ("po zrealizowaniu usług"?)

### Kluczowe obowiązki
- Obowiązki Zleceniobiorcy (Dokodu)
- Obowiązki Zleceniodawcy (klienta)

### Prawa i ograniczenia
- Logo / referencje — czy i na jakich warunkach
- Poufność / NDA
- Zakaz cesji wierzytelności

### Kary umowne i odpowiedzialność
- Kary za odstąpienie (obie strony)
- Terminy i warunki

### Dodatkowe ustalenia
- Konsultacje / godziny dodatkowe (cena/h)
- Możliwość aneksowania
- Prawo właściwe, sąd właściwy

## KROK 3b: Dla INNYCH dokumentów

Podsumuj w punktach: co to jest, kto jest stroną, kluczowe liczby i terminy, co wymaga działania.

## KROK 4: Zapisz do BRAIN (opcjonalnie)

Zapytaj użytkownika: "Czy zapisać wyciąg do profilu klienta [Klient] lub projektu [Projekt]?"

Jeśli tak → dopisz sekcję "## Umowa — wyciąg kluczowych klauzul" do odpowiedniego pliku w AREA_Customers lub 10_PROJECTS.

## ZASADY

- Cytuj bezpośrednio z dokumentu gdy to ważne (np. dokładne brzmienie klauzuli płatniczej)
- Oznaczaj ⚠️ rzeczy wymagające uwagi lub niestandardowe klauzule
- Jeśli czegoś nie ma w dokumencie — napisz wprost "brak w umowie"
- Nie interpretuj prawnie — opisuj co jest napisane, nie co to znaczy prawnie
