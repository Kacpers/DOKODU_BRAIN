---
type: agenda
status: ready
owner: kacper
last_reviewed: 2026-03-25
tags: [django, python, szkolenie, agenda, flagship]
---

# Szkolenie: Django Professional — Aplikacje Webowe od Podstaw

**Format:** 4 dni × 8h intensywny kurs praktyczny
**Dla kogo:** Zespoły które chcą szybko i efektywnie wdrażać rozwiązania webowe wspierające procesy wewnętrzne
**Wynik:** Uczestnicy tworzą aplikacje wydajne, bezpieczne i łatwe w utrzymaniu (best practices)
**Cena:** od 14 000 PLN netto / grupa do 12 osób (szacunek)
**Status:** ✅ Pełna agenda, gotowe do sprzedaży

---

## Dzień 1: Fundamenty Django i praca z danymi

### Wprowadzenie do Django i konfiguracja środowiska
- Czym jest Django i dlaczego warto go używać w projektach wewnętrznych
- Instalacja i konfiguracja środowiska na Windows (bez uprawnień administratora)
- Konfiguracja Visual Studio Code do efektywnej pracy z Django
- Tworzenie pierwszego projektu i zrozumienie struktury

### Podstawy Django i wzorzec MVT
- Model-View-Template (MVT) — zrozumienie architektury Django
- Tworzenie i rejestracja aplikacji w projekcie
- Projektowanie pierwszych widoków i szablonów
- Konfiguracja URL-i i system routingu

### Praca z bazami danych
- Konfiguracja połączenia z SQL Server (wersja darmowa)
- Projektowanie modeli danych w Django
- Django ORM — CRUD: tworzenie, odczyt, aktualizacja, usuwanie
- Migracje bazy danych — zarządzanie schematem
- Relacje między modelami (one-to-many, many-to-many)

---

## Dzień 2: Formularze, autoryzacja i bezpieczeństwo

### Formularze Django i walidacja danych
- Tworzenie formularzy w Django
- Walidacja danych wejściowych
- Niestandardowe walidatory i czyszczenie danych
- Obsługa formularzy w widokach i szablonach

### System autoryzacji i autentykacji
- Wbudowany system użytkowników w Django
- Integracja z Windows Authentication (środowisko domenowe)
- Implementacja uwierzytelniania użytkowników domeny Windows
- Konfiguracja middleware do automatycznej identyfikacji użytkowników

### Zarządzanie uprawnieniami
- System uprawnień w Django
- Tworzenie grup użytkowników i przydzielanie uprawnień
- Ograniczanie dostępu do widoków i funkcjonalności
- Bezpieczne praktyki programistyczne — ochrona przed OWASP Top 10

---

## Dzień 3: Interfejsy użytkownika i REST API

### Zaawansowane szablony i interfejs użytkownika
- System szablonów Django — zaawansowane techniki
- Dziedziczenie szablonów i komponenty wielokrotnego użytku
- Obsługa statycznych plików (CSS, JavaScript)
- Integracja z bibliotekami frontendowymi

### Projektowanie i implementacja REST API
- Wprowadzenie do Django REST Framework
- Dobre praktyki projektowania REST API
- Serializacja danych i walidacja
- Uwierzytelnianie i uprawnienia w API
- Dokumentowanie API z Swagger/OpenAPI

### Testowanie aplikacji Django
- Pisanie testów jednostkowych
- Testowanie widoków, modeli i formularzy
- Testy integracyjne
- Mierzenie pokrycia testami i CI/CD

---

## Dzień 4: Skalowalność, konteneryzacja i wdrożenie

### Kolejkowanie zadań z Celery
- Wprowadzenie do Celery
- Konfiguracja Celery z Django
- Tworzenie i zarządzanie zadaniami asynchronicznymi
- Monitorowanie i debugowanie zadań

### Konteneryzacja z Docker
- Podstawy Dockera dla aplikacji Django
- Tworzenie Dockerfile i docker-compose.yml
- Zarządzanie zależnościami i zmiennymi środowiskowymi
- Multi-stage builds dla optymalizacji obrazów

### Deployment aplikacji Django
- Przygotowanie aplikacji do wdrożenia produkcyjnego
- Konfiguracja serwera VPS
- Wdrażanie aplikacji na serwer
- Zabezpieczanie aplikacji produkcyjnej
- Monitorowanie i utrzymanie aplikacji

---

## Informacje organizacyjne

**Wymagania wstępne:** Podstawy Pythona (poziom E-PYTH1/PYTH01 lub równoważny)
**Materiały:** Dostarczane przez Dokodu (PDF + kod przykładów)
**Środowisko:** Visual Studio Code, Python 3.11+, SQL Server (wersja Express — darmowa)
**Certyfikat:** Na życzenie
