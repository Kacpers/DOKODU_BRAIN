# Specyfikacja Funkcjonalna — Załącznik nr 1

**Projekt:** Aplikacja SaaS do fakturowania dla Administratiekantoor Gibula  
**Wersja:** 1.0  
**Data:** 4 kwietnia 2026  
**Wykonawca:** DOKODU Sp. z o.o., ul. Kosynierów 76/22, 84-230 Rumia, NIP: 5882473305  
**Zamawiający:** Administratiekantoor Gibula, Holandia  
**Kwota netto:** 66 000 PLN  

---

## 1. Opis ogólny systemu

System jest aplikacją webową typu SaaS przeznaczoną dla przedsiębiorców prowadzących działalność gospodarczą w Holandii. Umożliwia wystawianie faktur, prowadzenie uproszczonej ewidencji kosztów, godzin pracy i kilometrów oraz generowanie raportów finansowych.

Architektura systemu od początku zakłada model wielodostępowy (multi-tenant), umożliwiający w przyszłości podłączenie kolejnych biur rachunkowych bez konieczności przebudowy systemu.

Język interfejsu: polski.  
Język generowanych dokumentów (faktur): holenderski.  
Waluta: wyłącznie EUR (€).

---

## 2. System ról i uprawnień

System przewiduje trzy poziomy dostępu:

### 2.1. Administrator
- Pełny dostęp do wszystkich funkcji systemu
- Zarządzanie kontami księgowych i użytkowników
- Konfiguracja globalna systemu (stawki, szablony, ustawienia)
- Wgląd w dane wszystkich użytkowników i księgowych

### 2.2. Księgowy
- Zarządzanie przypisanymi do siebie klientami (użytkownikami)
- Wgląd w faktury, koszty i raporty swoich klientów
- Możliwość wykonania eksportu kwartalnego dla swoich klientów
- Dostęp do funkcji "Magicznego Przycisku" (automatyczne księgowanie)
- Przydzielona pula kont użytkowników do podpięcia

### 2.3. Użytkownik (przedsiębiorca)
- Wystawianie faktur, pro-form, ofert i korekt
- Prowadzenie ewidencji kosztów, godzin i kilometrów
- Dostęp do własnych raportów i dashboardu
- Użytkownik podpięty pod biuro rachunkowe nie ponosi opłaty abonamentowej
- Użytkownik niezależny opłaca abonament samodzielnie

---

## 3. Moduł fakturowania

### 3.1. Typy dokumentów
System obsługuje następujące typy dokumentów:
- Faktura (Factuur)
- Pro-forma
- Oferta — dokument o strukturze identycznej z fakturą, oznaczony jako oferta, z możliwością przekształcenia jednym kliknięciem w fakturę końcową
- Korekta (Creditnota) — patrz punkt 3.5

### 3.2. Stawki BTW
Dostępne stawki podatku dla każdej pozycji na dokumencie:
- 21%
- 9%
- 0%
- BTW verlegd (reverse charge)
- BTW vrijgesteld (zwolniony z BTW)
- BTW marge regel (procedura marży)

### 3.3. Numeracja dokumentów
- Domyślny format: NN-RRRR (np. 01-2026, 02-2026)
- Każda kolejna faktura otrzymuje automatycznie kolejny numer
- Użytkownik ma możliwość ręcznej edycji numeracji

### 3.4. Personalizacja
- Możliwość wgrania własnego logo firmy przez użytkownika
- Logo wyświetlane na wszystkich generowanych dokumentach

### 3.5. Faktury korygujące (Creditnota)
- Korekta jest powiązana z fakturą oryginalną (referencja do numeru)
- System automatycznie pobiera dane z faktury źródłowej
- Użytkownik wskazuje które pozycje koryguje i podaje nowe wartości
- System przelicza różnicę automatycznie
- Korekta otrzymuje własny numer z osobnej serii numeracji
- Korekta wpływa na raporty i dashboard (pomniejsza przychód)

### 3.6. Kod QR do przelewu (EPC QR)
Na podglądzie i wydruku faktury generowany jest kod QR w standardzie EPC (European Payments Council). Po zeskanowaniu kodem w aplikacji bankowej odbiorcy automatycznie wypełniają się dane przelewu (IBAN wystawcy, kwota, tytuł). Nie wymaga integracji z bramką płatniczą.

### 3.7. Eksport UBL/XML
System umożliwia eksport wystawionych faktur do formatu UBL/XML.

---

## 4. Moduł ewidencji

### 4.1. Ewidencja kosztów
Prosty formularz dodawania kosztów zawierający:
- Kwota
- Opis
- Kategoria (do wyboru z listy)
- Data

Koszty zliczają się do głównego raportu na dashboardzie.

### 4.2. Ewidencja godzin pracy (godzinówka)
Uproszczona tabela ewidencji:
- Data
- Liczba godzin
- Opis

Możliwość pobrania/eksportu ewidencji.

### 4.3. Ewidencja kilometrów (kilometrówka)
Uproszczona tabela ewidencji:
- Data
- Liczba kilometrów
- Opis

Możliwość pobrania/eksportu ewidencji.

---

## 5. Dashboard i raporty

### 5.1. Panel główny (Dashboard)
Karty podsumowujące z kluczowymi metrykami:
- Suma przychodów ze wszystkich faktur
- Suma dodanych kosztów
- Wynik: kwota do opodatkowania (przychód minus koszty)

### 5.2. Rozliczenie kwartalne
- Generowanie raportu kwartalnego per użytkownik
- Eksport do pliku Excel w formacie kompatybilnym z programem Exact Online
- Raport zawiera zestawienie faktur i kosztów za dany kwartał
- Funkcja dostępna dla ról Księgowy i Administrator

### 5.3. Instrukcje video
Przestrzeń na kafelki z linkami do filmów instruktażowych (YouTube). Treść filmów przygotowuje Zamawiający.

---

## 6. Miękka windykacja

### 6.1. Lista faktur ze statusami
Widok listy wystawionych faktur z oznaczeniem statusu:
- Opłacona
- Oczekuje na płatność
- Po terminie płatności

### 6.2. Akcje windykacyjne
Przy każdej niezapłaconej fakturze dostępne przyciski akcji w trzech krokach eskalacji:
1. Przypomnienie o płatności — uprzejma wiadomość email z przypomnieniem o zbliżającym się lub minionym terminie płatności
2. Drugie przypomnienie — stanowcza wiadomość z informacją o zaległości
3. Oficjalne wezwanie do zapłaty — formalne wezwanie z terminem ostatecznym

Każdy krok generuje email na podstawie wbudowanego szablonu. Treść szablonów w języku holenderskim.

---

## 7. Integracja z księgowością ("Magiczny Przycisk")

Wyróżniony przycisk umożliwiający automatyczne przesłanie danych księgowych do systemu Zamawiającego. Mechanizm oparty na istniejącej integracji opracowanej wcześniej przez Wykonawcę (aplikacja łącząca faktury z kontami bankowymi).

Dodatkowo system generuje eksport Excel kompatybilny z importem do programu Exact Online (główny program księgowy Zamawiającego). Kompatybilność eksportu z pozostałymi programami księgowymi (AFAS, Twinfield, Moneybird, e-Boekhouden.nl, SnelStart, Yuki) zostanie dodana w miarę potrzeb na późniejszym etapie.

---

## 8. System abonamentowy i płatności

### 8.1. Rejestracja i weryfikacja
- Każdy użytkownik zakłada własne konto z loginem
- Weryfikacja firmy w rejestrze KvK (Kamer van Koophandel) w celu potwierdzenia tożsamości przedsiębiorcy
- Wymagane dane firmy przy rejestracji: nazwa firmy, numer KvK, BTW-nummer (numer identyfikacji podatkowej NL), adres, IBAN (numer konta bankowego), BIC banku (opcjonalnie). IBAN i nazwa firmy są niezbędne do generowania kodu EPC QR na fakturach. BTW-nummer jest wymagany na holenderskich fakturach oraz w eksporcie UBL/XML

### 8.2. Płatności abonamentowe
- Integracja z bramką płatniczą Mollie
- Jeden pakiet abonamentowy, płatny automatycznie co miesiąc
- W przypadku braku płatności — automatyczna blokada dostępu do systemu
- Użytkownicy podpięci pod biuro rachunkowe są zwolnieni z opłaty abonamentowej

### 8.3. Program poleceń
Użytkownik posiadający abonament może polecić nowego klienta za pomocą indywidualnego linku polecającego. Za każde skuteczne polecenie (polecony klient aktywuje abonament) polecający otrzymuje jednorazową zniżkę na kolejny miesiąc abonamentu. Wysokość zniżki oraz pozostałe warunki programu konfiguruje Administrator w panelu systemu.

---

## 9. Wymagania techniczne

- Aplikacja webowa (przeglądarkowa), responsywna
- Technologia: Next.js, React, Tailwind CSS
- Bezpieczny panel logowania z autoryzacją
- Architektura multi-tenant
- Przygotowanie pod przyszłą wielojęzyczność interfejsu (holenderski, angielski, ukraiński, rumuński, bułgarski)

---

## 10. Rozszerzenia opcjonalne (poza zakresem V1.0)

Poniższe funkcjonalności nie wchodzą w zakres niniejszej umowy. Mogą zostać zrealizowane jako Etap 2, na podstawie osobnej wyceny i zamówienia po odbiorze Wersji 1.0.

### 10.1. OCR faktur zakupowych
Automatyczne odczytywanie danych z faktur zakupowych wgrywanych jako pliki PNG lub PDF. System rozpoznaje dane z dokumentu (kwota, data, kontrahent, stawka BTW) i automatycznie dodaje je do ewidencji kosztów.

Orientacyjna wycena: 3 000 – 4 000 PLN netto.

### 10.2. Integracja z siecią Peppol
Wysyłka i odbiór e-faktur przez sieć Peppol.

### 10.3. Pełna gospodarka magazynowa
Stany magazynowe, przyjęcia, wydania — powiązane z fakturami.

### 10.4. Zaawansowana ewidencja godzin i kilometrów
GPS, projekty, stawki per klient.

### 10.5. Integracja z bramkami płatniczymi dla odbiorców faktur
Umożliwienie klientom końcowym opłacenia faktury jednym kliknięciem.

### 10.6. Dodatkowe języki interfejsu
Holenderski, angielski, ukraiński, rumuński, bułgarski.

---

## 11. Wyłączenia

Niniejsza specyfikacja nie obejmuje:
- Obsługi paragonów/bonów fiskalnych
- Integracji z systemem Peppol (poza eksportem UBL/XML)
- Pełnej gospodarki magazynowej
- Funkcji GPS w ewidencji kilometrów
- Obsługi walut innych niż EUR
- Hostingu i utrzymania serwerów (do ustalenia osobno)

---

## 12. Wysyłka dokumentów

System umożliwia wysyłkę dokumentów drogą emailową bezpośrednio z aplikacji:
- Wysyłka faktur, pro-form, ofert i korekt do odbiorcy
- Wysyłka przypomnień o płatności
- Wysyłka oficjalnych wezwań do zapłaty

Emaile wysyłane są z adresu systemowego (np. noreply@fakturowanie.gibula.nl) z danymi wystawcy w treści wiadomości. Odbiorca odpowiada na adres email wystawcy podany w ustawieniach konta (pole reply-to).

---

## 13. Warunki odbioru

System uznaje się za dostarczony po spełnieniu wszystkich punktów opisanych w rozdziałach 1–12 niniejszej specyfikacji.

Procedura odbioru:
1. Wykonawca prezentuje gotowy system Zamawiającemu
2. Zamawiający ma 14 dni kalendarzowych na zgłoszenie uwag od daty prezentacji
3. W cenę wchodzą 2 rundy poprawek zgłoszonych w ramach odbioru
4. Poprawki dotyczą wyłącznie niezgodności z niniejszą specyfikacją, nie nowych funkcjonalności
5. Brak zgłoszenia uwag w terminie 14 dni oznacza akceptację systemu
