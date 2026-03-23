---
type: area-index
status: active
owner: kacper
last_reviewed: 2026-03-06
tags: [klienci, crm, relacje, historia]
---

# AREA: Customers — Baza Klientow i Prospektow
> Kazdy klient ma swoj katalog. Kazdy katalog ma 3 pliki: Profil, Spotkania, Okazje.
> Uzywaj skilla `/brain-new-customer` do tworzenia nowego klienta.

---

## AKTYWNI KLIENCI

| Klient | Branza | Wartosc (PLN) | Status | Opiekun |
| :--- | :--- | ---: | :---: | :--- |
| [[Animex/Animex_Profile\|Animex]] | Produkcja / BOK | 18 000 | Szkolenie | Kacper |
| [[Corleonis/Corleonis_Profile\|Corleonis]] | Logistyka | 35 000 + 3k/mies | Wdrozenie | Kacper |

## PROSPEKCI (pipeline)

| Prospekt | Zrodlo | Etap | Wartosc est. | Link |
| :--- | :--- | :--- | ---: | :--- |
| _[dodaj z CRM]_ | | | | |

---

## STRUKTURA KATALOGU KLIENTA

```
[Nazwa_Klienta]/
├── [Nazwa]_Profile.md      ← KTO to jest. Dane, kontakty, stos IT, historia, ICP-fit.
├── [Nazwa]_Meetings.md     ← Chronologiczne notatki ze spotkan i rozmow.
└── [Nazwa]_Opportunities.md ← Historia projektow + potencjal upsell/renewal.
```

## SZYBKIE KOMENDY

- Nowy klient: `/brain-new-customer`
- Nowa notatka ze spotkania: `/brain-capture` (lub reczni do `_Meetings.md`)
- Status wszystkich: `/brain-status`
