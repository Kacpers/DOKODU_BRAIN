---
type: customer-profile
status: active
owner: kacper
last_reviewed: 2026-03-23
tags: [klient, produkcja, bok, szkolenie, n8n, sap, sharepoint]
client_since: 2026-02-15
---

# KLIENT: Animex
> Klient szkoleniowy. Projekt aktywny: [[../../../10_PROJECTS/PRJ_Animex_Szkolenie/PRJ_Animex_Szkolenie|PRJ_Animex_Szkolenie]]

---

## PROFIL FIRMY

| Pole | Wartosc |
| :--- | :--- |
| **Pelna nazwa** | Animex _[uzupelnij]_ |
| **NIP** | _[uzupelnij]_ |
| **Branza** | Produkcja / Biuro Obsługi Klienta |
| **Wielkosc** | ~_[X]_ pracownikow, ~15 w BOK |
| **Lokalizacja** | _[uzupelnij]_ |
| **Glowny system (ERP)** | SAP _[potwierdzic wersje]_ |
| **Email** | Outlook (O365) |
| **AI wczesniej** | Brak / minimalne uzytakowanie |
| **Klientem od** | 2026-02-20 |
| **Zrodlo leada** | Przetarg |

---

## KONTAKTY

| Imie i Nazwisko | Stanowisko | Email | Telefon | Rola |
| :--- | :--- | :--- | :--- | :--- |
| **Kamil Kowalski** | Osoba kontaktowa (kontrakt §7) | Kamil.Kowalski@animex.pl | 668140030 | Kontakt operacyjny — właściwy kanał upsell |
| **Katarzyna Kasprzak** | Dyrektor Zarządzający ds. Finansów, Pełnomocnik | — | — | Podpisała umowę (strona Animex) |

**Preferowany kanal:** Email (Kamil Kowalski)
**Ważne:** Klient z przetargu — wszelki kontakt handlowy wyłącznie przez Kamila Kowalskiego, nie przez uczestników szkoleń.

---

## PERSONY — UCZESTNICY SZKOLEŃ (tylko kontekst wdrożeniowy)

> ⚠️ **RODO / Consent:** Uczestnicy wyrazili zgodę na kontakt wyłącznie w zakresie szkolenia. Animex pochodzi z przetargu — bezpośredni outreach do uczestników ws. sprzedaży jest prawnie ryzykowny i reputacyjnie nieodpowiedni. Wszelki upsell musi iść przez oficjalny kanał Animex (osoba kontaktowa / procurement).
>
> Poniższe dane służą jako **intel wdrożeniowy** — rozumienie potrzeb firmy, nie lista kontaktów do cold outreach.

### Zidentyfikowane obszary bólu (do wykorzystania w rozmowach z oficjalnym kontaktem Animex)

| Obszar | Ból zidentyfikowany | Potencjalne rozwiązanie |
| :--- | :--- | :--- |
| SAP HANA | Ręczne przełączanie danych SAP↔Excel | Orkiestracja SAP ↔ n8n |
| OCR / Computer Vision | Pipeline YOLO wymaga optymalizacji | CV pipeline + fine-tuning |
| SharePoint (dokumenty) | Dokumentacja firmowa niesearchowalna | GraphRAG na M365 |
| Migracje cloud (Entra ID) | Złożoność Copilot / Entra ID setup | Doradztwo M365 AI + Presidio |

### Bóle grupy deweloperów (.NET / Ruby)
- 48 GB VRAM to za mało na lokalne LLMy
- Zapychanie okna kontekstowego (brak GraphRAG)
- Niechęć do Pythona (preferują JS/TS)

**Ścieżka upsell:** Przez konsultacje już zaplanowane z Animexem → rozmowa z decydentem / osobą kontaktową z przetargu → oficjalna propozycja. Nie przez uczestników.

---

## KONTEKST BIZNESOWY

**Glowny problem:**
> Dzial BOK obsługuje ~200 zgłoszen miesiecznie recznie (Outlook + Excel). Brak kategoryzacji, brak priorytyzacji, duze opoznienia w odpowiedziach. Menedzer BOK traci ~15h/mies. na reczne raportowanie.

**Co probowali wczesniej:**
- Wewnetrzna reorganizacja procesow (bez narzedzi AI)

**Dlaczego wybrali Dokodu:**
- _[uzupelnij po rozmowie]_

**Kryteria sukcesu:**
- Pracownicy BOK wiedza jak uzywac agenta AI do kategoryzacji emaili
- Demo agenta ktory czyta maile z SAP robi WOW
- NPS po szkoleniu > 8/10

**Budzet:** 18 000 PLN (ten kontrakt) + potencjal na wdrozenie produkcyjne

---

## STOS TECHNOLOGICZNY

```
ERP:         SAP (wersja TBD)
Email:       Outlook O365
Komunikacja: Teams (TBD)
Pliki:       SharePoint (TBD)
```

---

## HISTORIA WSPOLPRACY

| Data | Zdarzenie | Wartosc | Status |
| :---: | :--- | ---: | :---: |
| 2026-02-20 | Podpisanie umowy szkoleniowej (5 grup + 6 konsultacji) | 40 000 PLN netto | Aktywne — brak zaliczki, płatność po realizacji całości (szkolenia + konsultacje) |
| 2026-03-05/06 | Szkolenie Grupa 1 | — | Zrealizowane |
| 2026-03-10/11 | Szkolenie Grupa 2 | — | Zrealizowane |
| 2026-03-12/13 | Szkolenie Grupa 3 | — | Zrealizowane |
| 2026-03-23/24 | Szkolenie Grupa 4 | — | W toku |
| 2026-03-25/26 | Szkolenie Grupa 5 | — | Planowane |
| _[po grupie 5]_ | Faktura końcowa | 40 000 PLN netto | Oczekuje |

**Łączna wartość:** 40 000 PLN netto
**Retainer:** Nie (potencjał po szkoleniu)
**Logo:** Prawo do użycia logo Animex na dokodu.it po pisemnym zatwierdzeniu pozytywnej realizacji (§11 ust. 2)

---

## POTENCJAL UPSELL

Po udanym szkoleniu:
- **Wdrozenie produkcyjne agenta BOK** — szacunek: 25 000 - 40 000 PLN
- **Retainer monitoring** — 3 000 PLN/mies.
- **Rozszerzenie: integracja z SAP** — TBD
- **Szkolenie dla IT** — osobny modul n8n

**Kluczowe pytania do zebrania podczas szkolenia:**
- [ ] Jakie inne procesy BOK sa bolesne?
- [ ] Kto jest "internal champion" dla AI?
- [ ] Jaki budzet maja na automatyzacje w 2026?
- [ ] Kto decyduje o zakupie narzedzi?

---

## LINKI
- Projekt: [[../../../10_PROJECTS/PRJ_Animex_Szkolenie/PRJ_Animex_Szkolenie]]
- Spotkania: [[Animex_Meetings]]
- Okazje: [[Animex_Opportunities]]
- Playbook branżowy: [[../../../30_RESOURCES/RES_Industry_Playbooks/Playbook_Produkcja]]
