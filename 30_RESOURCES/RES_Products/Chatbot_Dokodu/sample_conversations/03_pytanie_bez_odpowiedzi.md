---
type: sample-conversation
scenario: Pytanie spoza bazy wiedzy — bot uczciwie przyznaje
outcome: lead captured + analytics flag
duration: 2 min
messages: 6
---

# Przykład 3: Pytanie bez odpowiedzi → lead + sygnał do właściciela

**Kontekst:** Ta sama Parkowa Rezydencje. User pyta o coś, czego NIE MA w bazie wiedzy. Ważne — to jest **scenariusz sprzedażowy** dla właściciela bota. Bot uczciwie mówi „nie mam" + proponuje kontakt, a pytanie ląduje w dashboardzie w sekcji *„Pytania bez dobrej odpowiedzi"* — właściciel widzi czego brakuje.

---

**👤 Użytkownik (14:22)**
Czy na osiedlu będzie plac zabaw dla dzieci?

**🤖 Bot (14:22)**
Nie mam tej informacji w bazie wiedzy. Przekażę pytanie doradcy — odezwiemy się z konkretną odpowiedzią. Proszę zostawić kontakt.

**[Pojawia się pill-button: „Zostaw kontakt: umów wizytę"]**

*Sugestie: „Jaki standard wykończenia?" · „Które mieszkania są dostępne?"*

---

**👤 Użytkownik klika button**

**Formularz (bottom sheet):**
- Imię i nazwisko *: Piotr Nowak
- Telefon *: 501 234 567
- E-mail *: piotr.nowak@example.com
- Którym mieszkaniem jesteś zainteresowany?: „Nie konkretnym, pytam o część wspólną dla rodzin z dziećmi — plac zabaw, ścieżka rowerowa, strefa relaksu."

**[Wyślij zgłoszenie]**

---

**🤖 Bot (14:23)**
✓ Dziękujemy! Mamy już Państwa kontakt — odezwiemy się wkrótce.

---

## Co widzi właściciel w panelu admina

### 1. Konwersacja
**4 wiadomości · 1 min · Lead ✓ · Pytania bez bazy wiedzy: 1 ⚠**

W conversation detail — pod odpowiedzią bota pojawia się pomarańczowy znacznik:
> ⚠ Brak dopasowania w bazie wiedzy — rozważ wgranie dokumentu

### 2. Dashboard — sekcja *Pytania bez dobrej odpowiedzi*

| Pytanie | Liczba | Ostatnio |
| :--- | :---: | :---: |
| czy na osiedlu będzie plac zabaw dla dzieci? | ×1 | 20.04.2026 |
| jaka jest powierzchnia balkonu w b2.02? | ×3 | 19.04.2026 |
| czy dopuszczacie zwierzęta? | ×2 | 17.04.2026 |

### 3. Akcja właściciela
- Klika „Pokaż rozmowy z pytaniami bez odpowiedzi →"
- Widzi 6 rozmów w których padło podobne pytanie
- Wgrywa PDF *„Częsci_wspólne_i_tereny_zewnętrzne.pdf"* w `/admin/documents`
- Po 2 minutach (przetwarzanie + embedding) — kolejny user z tym samym pytaniem dostaje merytoryczną odpowiedź z cytowaniem dokumentu.

---

## Komentarz biznesowy

Ten scenariusz pokazuje **najcenniejszą funkcję dla sprzedaży właściciela**: chatbot nie tylko sprzedaje, ale też **uczy właściciela czego brakuje na jego stronie**.

- User nie dostał odpowiedzi, ale zostawił kontakt → **nie jest stracony**.
- Właściciel dostaje **listę braków w ofercie** — to dane których nie dałby mu ani Google Analytics, ani zwykły formularz.
- Każda „porażka" bota = **bezpośrednia rekomendacja co uzupełnić** = lepsze ROI z każdym kolejnym miesiącem.

Bot, który „nie wie", jest lepszy niż bot, który halucynuje. W panelu widać: *„w tym miesiącu 18 osób pytało o X — dopisz X do oferty"*.
