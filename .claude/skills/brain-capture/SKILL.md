---
name: brain-capture
description: Szybki capture — dodaje notatkę, pomysł, zadanie lub obserwację do INBOX w DOKODU_BRAIN. Najszybszy sposob na zapisanie mysli bez kategoryzowania. Uzyj gdy masz pomysl, cos do sprawdzenia, szybkie zadanie. Trigger slowa: "zanotuj", "capture", "zapamietaj", "dodaj do inboxa", "wrzuc do inboxa", /brain-capture, /capture
---

# Instrukcja: Szybki Capture do DOKODU_BRAIN INBOX

## Dzialanie

To jest najszybszy skill. Nie pyta o wiele — po prostu zapisuje.

## KROK 1: Otrzymaj tresc

Uzytkownik podaje notatke (moze byc nieustrukturyzowana, chaotyczna, krótka).
Przykłady:
- "zanotuj: sprawdzic nowy node AI Agent w n8n 1.78"
- "capture: pomysl na post - 'dlaczego Copilot jest uzywany jak wyszukiwarka'"
- "wrzuc do inboxa: zadzwonic do Marcina ws. webhokow"
- "zapamietaj: Corleonis wspominal o dziale handlowym — potencjal upsell"

## KROK 2: Kategoryzuj (automatycznie, bez pytania)

Na podstawie tresci dobierz prefix:
- `POMYSL:` — pomysl na produkt, content, usluge
- `LEAD:` — potencjalny klient lub okazja biznesowa
- `TODO:` — konkretne zadanie do zrobienia
- `SPRAWDZ:` — cos do weryfikacji lub zbadania
- `PYTANIE:` — pytanie do siebie lub kogoś
- `UPSELL:` — okazja upsell u istniejacego klienta
- Brak prefixu — ogolna notatka

## KROK 3: Dodaj do INBOX

Dopisz na górze sekcji "NOTATKI Z TELEFONU / MYSLI" w `/home/kacper/DOKODU_BRAIN/00_INBOX.md`:

```
- [ ] [PREFIX:] [tresc notatki] — [data dzisiaj]
```

## KROK 4: Potwierdz krotko

Odpowiedz jednym zdaniem: "Dodano do Inboxa: [tresc]"

Nie pytaj o nic wiecej. Nie proponuj kategoryzacji. Nie analizuj.
Cel: capture w <10 sekund.

## ZASADY

- Nie poprawiaj ortografii — zachowaj jak uzytkownik powiedział
- Nie rozwijaj — zapisz minimum, reszte dopiszesz pozniej
- Jezeli tresc zawiera slowo "LEAD" + imie firmy → rowniez zaproponuj `/brain-add-lead`
- Jezeli tresc zawiera "UPSELL" + klient → rowniez dodaj do [Klient]_Opportunities.md
