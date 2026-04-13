---
name: brain-add-lead
description: Dodaje nowy lead do CRM i opcjonalnie tworzy profil prospekta w AREA_Customers. Uzyj gdy masz nowy kontakt B2B, bylas na konferencji, ktos wypelnil formularz, lub dostales polecenie. Trigger slowa: "nowy lead", "dodaj lead", "dodaj kontakt", "dodalem kontakt", /brain-add-lead
---

# Instrukcja: Dodawanie Nowego Leadu do DOKODU_BRAIN

## KROK 1: Zbierz podstawowe dane

Zapytaj o (mozna podac wszystko na raz):
1. **Firma** i **imie/nazwisko kontaktu**
2. **Stanowisko**
3. **Email / LinkedIn / Telefon**
4. **Skad pochodzi lead?** (LinkedIn / Konferencja / Polecenie od [kogo] / Inbound strona / inne)
5. **Co powiedział / jaki problem wspominal?** (1-2 zdania)
6. **Szacunkowy budzet** (jesli znany)
7. **Pilnosc** (chce dzialac od razu / planuje / "kiedys")
8. **Czy spelnia ICP?** (firma 50-500 prac., branza operacyjna, budzet >10k PLN)

## KROK 2: Kwalifikacja BANT+

Na podstawie zebranych informacji oceń:
- **Budget**: znany / nieznany / powyzej 10k PLN
- **Authority**: czy kontakt moze podpisac umowe?
- **Need**: czy ma realny, nazwany problem?
- **Timeline**: kiedy chce dzialac?
- **Fit ICP**: tak / nie / czesciowo

Wynik: **KWALIFIKOWANY** / **DO DALSZEGO BADANIA** / **NIEKWALIFIKOWANY**

## KROK 3: Dodaj do CRM

Dodaj wpis do tabeli PIPELINE AKTYWNY w `/home/kacper/DOKODU_BRAIN/20_AREAS/AREA_Marketing_Sales/CRM_Leady_B2B.md`:

```
| [NR] | [Firma] | [Imie Nazwisko] | [Zrodlo] | [Etap] | [Wartosc est.] | [Nastepny krok] | [Deadline] |
```

Etap poczatkowy zazwyczaj: **Nowy** lub **Kontakt** (jezeli juz byl kontakt)

## KROK 4: Nastepny krok

Na podstawie kwalifikacji zaproponuj:
- **KWALIFIKOWANY**: "Wyslij wiadomosc na LinkedIn / email z zaproszeniem do discovery call. Uzyj szablonu T-001 z Templates.md. Cel: umow discovery call w ciagu 5 dni."
- **DO DALSZEGO BADANIA**: "Dodaj do nurturingu. Wyslij 1 wartosciowy artykul za 3 dni. Wróc do rozmowy za 2 tygodnie."
- **NIEKWALIFIKOWANY**: "Nie inwestuj czasu. Dodaj do listy niskopriorytetowej i wyslij 1 newsletter."

## KROK 5: Opcjonalnie — prospekt w AREA_Customers

Jezeli lead jest KWALIFIKOWANY i jest szansa na kontrakt > 15k PLN:
Zaproponuj: "Czy stworzyc tez profil prospekta w `_PROSPECTS/`? Wtedy bedziesz miec pelna historię gdy zostanie klientem."

Jezeli tak → stworz `/home/kacper/DOKODU_BRAIN/20_AREAS/AREA_Customers/_PROSPECTS/[Firma].md` z podstawowymi danymi.

## KROK 6: Inbox update

Dodaj do `/home/kacper/DOKODU_BRAIN/00_INBOX.md`:
```
- [ ] LEAD: [Firma / Imie] — [nastepny krok] do [data]
```

## KROK 7: CRM Sync

Po dodaniu do CRM_Leady_B2B.md, dodaj firme rowniez do CRM PostgreSQL:
```bash
python ~/DOKODU_BRAIN/scripts/crm_sync.py push-lead "<nazwa_firmy>"
```

## ZASADY

- Kazdy lead, z ktorym rozmawiasz → CRM. Bez wyjatkow. Nawet "za malo informacji".
- Nie kwalifikuj za szybko. "Nie wiem" to nie "nie" — dopytaj.
- Data w kolumnie Deadline = kiedy MUSISZ wykonac nastepny krok, nie kiedy podpisujesz umowe.
