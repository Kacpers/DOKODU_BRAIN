---
type: oferta
klient: Korollo
data: 2026-03-27
status: szkic
wartosc_A: 8900
wartosc_B: 22900
owner: kacper
---

# Propozycja Współpracy: Korollo
**Dokodu × Korollo | Marzec 2026**

---

## Streszczenie

Wasz sklep generuje setki zamówień miesięcznie — ale żeby sprawdzić które produkty rotują, jakie promocje działają, czy tendencja sprzedaży w danej kategorii rośnie czy spada, trzeba grzebać w raportach albo eksportować Excele. Proponujemy jedno rozwiązanie: zadajesz pytanie po polsku i w kilka sekund dostajesz odpowiedź — bezpośrednio w narzędziu, którego już używasz (Copilot, ChatGPT lub Teams). Wdrożenie w 3 tygodnie, bez dotykania danych klientów.

---

## Rozumiemy Wasz Problem

Planowanie sprzedaży z 1–3-miesięcznym wyprzedzeniem to nie luksus — to konieczność. Ale żeby dobrze planować, trzeba wiedzieć co sprzedaje się teraz, co zwalnia, i kiedy stan konkretnego produktu zaczyna niebezpiecznie topnieć.

**Obecna sytuacja:**
- Żeby odpowiedzieć na pytanie "co sprzedaje się najlepiej w tym miesiącu?" — trzeba wejść w raporty, wyfiltrować, wyeksportować
- Alerty o niskich stanach są manualne albo ich nie ma — ryzyko, że produkt zniknie z oferty zanim zdążysz zamówić
- Analiza tendencji kategorii (np. kamienie naturalne vs syntetyczne) wymaga czasu którego nie ma
- Kiedy pojawia się nowa nowość, nie wiadomo szybko czy "iść w to" czy cofnąć zamówienie

**Konsekwencje:**
- Decyzje zakupowe oparte na intuicji, nie na liczbach
- Produkty schodzą zanim dotrze następna dostawa (1–3 miesiące lead time)
- Nowości "przelatują" bo team nie ma czasu ich śledzić

---

## Nasze Podejście

Budujemy AI Asystenta Sprzedaży podpiętego pod Wasz sklep Magento 2. Asystent czyta dane zamówień i stanów magazynowych w czasie rzeczywistym — bez dostępu do danych osobowych klientów. Następnie udostępniamy go przez interfejs, którego Wasz team już używa: Microsoft Copilot, ChatGPT lub prosty chat na Teams/przeglądarce.

**Jak pracujemy:**
1. **Tydzień 1 — Analiza i podłączenie** — mapujemy strukturę danych w Magento 2, konfigurujemy bezpieczny konektor przez API, wykluczamy dane klientów na poziomie połączenia
2. **Tydzień 2 — Budowa Asystenta** — trenujemy zapytania na Waszych danych, ustawiamy alerty, testujemy dokładność odpowiedzi
3. **Tydzień 3 — Wdrożenie i przekazanie** — uruchamiamy na środowisku produkcyjnym, szkolenie dla zespołu (1–2h), przekazujemy kod i dokumentację

**Zasada prywatności:** dane klientów (imiona, adresy, emaile) są odfiltrowane na poziomie konektora — Asystent widzi tylko dane produktowe i agregaty sprzedaży. Pełna zgodność z RODO.

---

## Co Dostarczamy

**AI Asystent Sprzedaży — zakres:**
- [ ] Konektor Magento 2 API → bezpieczny pipeline danych (bez PII klientów)
- [ ] Natural language queries po polsku: "top 100 produktów z ostatniego miesiąca", "średnia wartość koszyka z tego tygodnia", "tendencja sprzedaży w kategorii kamienie", "wszystkie zamówienia powyżej X PLN z ostatnich 7 dni"
- [ ] Alerty stanów magazynowych: konfigurowalny próg (np. -40% stanu początkowego → powiadomienie)
- [ ] Analiza historyczna: "czy 50 sztuk na stanie to dużo czy mało dla tego produktu?"
- [ ] Dostęp przez Microsoft Copilot Studio, Custom GPT lub interfejs webowy (do ustalenia na kickoffie)
- [ ] Szkolenie zespołu (1–2h online)
- [ ] Dokumentacja + przekazanie kodu (bez vendor lock-in)

**Czego NIE obejmuje ten zakres:**
- Integracja z Ship Town / ERP
- Konfigurator produktów na stronie
- Bot na stronie dla klientów zewnętrznych
- Masowe dodawanie produktów

*(Powyższe możemy wycenić oddzielnie po pilotażu — gdy AI Asystent już działa i widzisz wartość)*

---

## Harmonogram

```
Tydzień 1  │ Kickoff + analiza API Magento + konfiguracja konektora
Tydzień 2  │ Budowa Asystenta + testowanie zapytań na danych produkcyjnych
Tydzień 3  │ Wdrożenie + szkolenie zespołu + przekazanie dokumentacji
```

**Start:** tydzień od podpisania umowy i wpłaty zaliczki

---

## Inwestycja

| | Opcja A — AI Asystent Sprzedaży |
| :--- | ---: |
| Wdrożenie (konektor + asystent + szkolenie) | 8 900 PLN |
| **Łącznie** | **8 900 PLN netto** |

*Cena netto + 23% VAT. Płatność: 50% zaliczka przed startem, 50% po go-live.*
*Oferta ważna 14 dni od daty wystawienia.*

> **Zwrot z inwestycji:** jeśli Asystent oszczędza każdemu z 3 osób w teamie 2h tygodniowo na szukaniu danych w raportach — to przy koszcie pracy 50 PLN/h = **1 200 PLN miesięcznie**. Inwestycja zwraca się w ~7 miesięcy. W praktyce zwrot przychodzi szybciej — jedna dobra decyzja zakupowa (właściwy produkt zamówiony w odpowiednim momencie) może być warta wielokrotność tej kwoty.

---

## Dlaczego Dokodu

- **Znamy e-commerce na Magento** — integracje sklepów to nasz chleb powszedni
- **Dane zostają u Was** — wszystko działa na Waszej infrastrukturze, żadnych zewnętrznych baz danych, żadnych SaaS z miesięcznym abonamentem
- **RODO wbudowane, nie przyklejone** — Alina Sieradzińska (COO, ekspert prawny AI Act i GDPR) nadzoruje każde wdrożenie pod kątem zgodności
- **Bez vendor lock-in** — dostajecie kod, dokumentację i pełną własność rozwiązania
- **140+ firm, 4.9/5** — mamy doświadczenie w wdrożeniach dla firm tej wielkości

---

## Następny Krok

Jeśli chcecie ruszyć z AI Asystentem Sprzedaży:

1. Odpiszcie na tego maila z potwierdzeniem
2. Prześlę umowę w ciągu 24h
3. Kickoff call ustawiamy na Wasz termin — potrzebujemy ~1h z osobą mającą dostęp do Magento Admin

**Pytania?** Zadzwoń: +48 508 106 046 lub odpisz bezpośrednio.

---
*Dokodu | kacper@dokodu.it | dokodu.it | ul. Kosynierów 76/22, 84-230 Rumia*
*Oferta ważna 14 dni od daty wystawienia: 2026-03-27*
