---
type: customer-profile
status: active
owner: kacper
last_reviewed: 2026-03-24
tags: [klient, ksiegowosc, finanse, python, ai, holandia]
client_since: 2026-02-25
nip: "NL868538711B01"
---

# KLIENT: GRAVIS GROUP BV

---

## PROFIL FIRMY

| Pole | Wartosc |
| :--- | :--- |
| **Pelna nazwa** | Gravis Group BV |
| **NIP** | NL868538711B01 |
| **KvK (odpowiednik KRS)** | 98539035 |
| **Branza** | Ksiegowosc / Finanse |
| **Lokalizacja** | Den Haag, Holandia (Paul van Osaijenstraat 6, 2548MZ) |
| **Glowny system** | Excel (.xlsm) — INKOOPBOEK / VERKOOPBOEK / BANKBOEK |
| **Bank** | ING (wyciagi PDF — format angielski i holenderski) |
| **Klientem od** | 2026-02-25 |
| **Zrodlo leada** | — |

---

## KONTAKTY

| Imie i Nazwisko | Stanowisko | Email | Rola |
| :--- | :--- | :--- | :--- |
| Grzegorz Gibula | — | — | Kontakt techniczny / opiekun projektu |
| Jakub | — | — | Uzytkownik systemu (podpisuje maile jako Jakub) |

**Uwaga:** Maile przychodzą od Grzegorza Gibuli, ale podpisywane są imieniem "Jakub" — prawdopodobnie dwie osoby lub jedna podpisuje się imieniem.

**Preferowany kanal komunikacji:** Email

---

## KONTEKST BIZNESOWY

**Glowny problem:**
> Reczne parowanie transakcji z wyciagów bankowych ING z zapisami w ksiedze Excel (INKOOPBOEK/VERKOOPBOEK). Klient obsluguje wielu podklientow (ADAMCZYK, MARCOL, DYLEWSKI, HUNADY, KOBYLECKI, LESICKI i in.) — kazdy ma osobny plik PDF i Excel.

**Rozwiazanie Dokodu:**
Aplikacja webowa (Python/FastAPI + React) do automatycznego reconciliation:
- Import PDF (wyciag ING) + Excel (.xlsm)
- Kaskadowe dopasowanie: regex → reguly statyczne → mappings → kwota+data → VAT → AI
- Interfejs do recenzji i recznego dopasowania
- Raport Excel z wynikami

**Kryteria sukcesu:**
- >85% transakcji obsluzonych automatycznie lub z propozycja kandydata
- 0 false positive (blednych autopowiazan)
- Dziala dla obu formatow ING (angielski i holenderski)

---

## STOS TECHNOLOGICZNY

```
Backend:    Python 3.10 + FastAPI + pdfplumber + openpyxl + rapidfuzz
AI:         OpenAI GPT-4o-mini (Pass 3 — analizy niejednoznaczne)
Frontend:   React + TypeScript (Vite) + TailwindCSS
Hosting:    Serwer klienta (kod instalowany przez Dokodu)
Dane:       PDF (ING) + Excel .xlsm (Arkusz1)
```

---

## HISTORIA WSPOLPRACY

| Data | Zdarzenie | Wartosc | Status |
| :---: | :--- | ---: | :---: |
| 2026-02-25 | Umowa o dzielo nr 1/2026 — System reconciliation | 12 000 PLN netto | Aktywne |
| 2026-02-25 | Zaliczka 30% | 3 600 PLN | Do odebrania |

**Lacna wartosc wspolpracy:** 12 000 PLN netto
**Retainer aktywny:** Nie

---

## RELACJA I SALES INTELLIGENCE

**Poziom zaufania (1-5):** 3
**Kluczowe obserwacje:**
- Klient aktywnie testuje system i przesyla szczegolowe uwagi (dobry znak — zaangazowany)
- Pyta o dodatkowe funkcje (export z adnotacjami) — potencjal na Change Request
- Komunikacja mailowa na per Pan, odpowiedzi konkretne i merytoryczne

**Potencjal upsell:**
- Export wyciagu z adnotacjami BOEKSTUK (zgloszone 2026-03-24 — Change Request)
- Retainer wsparcia po odbiorze (gwarancja 6 mies. jest, ale placi za dodatkowe prace)
- Rozszerzenie na wieksza liczbe klientow / inne banki

---

## LINKI

- Projekt: [[../../../10_PROJECTS/PRJ_GravisGroup_Faktury/PRJ_GravisGroup_Faktury]]
- Umowa: Umowa o dzielo nr 1/2026 z dn. 25.02.2026
- Spotkania: [[GravisGroup_Meetings]]
