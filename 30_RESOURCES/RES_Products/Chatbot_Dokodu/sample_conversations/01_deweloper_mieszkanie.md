---
type: sample-conversation
scenario: Deweloper nieruchomości — zainteresowany mieszkaniem 3-pok.
outcome: lead captured
duration: 4 min
messages: 12
---

# Przykład 1: Deweloper nieruchomości — zapytanie o mieszkanie

**Kontekst:** Parkowa Rezydencje — deweloper z Trójmiasta. W bazie wiedzy bota: karty lokali, cennik, harmonogram płatności, opis inwestycji, FAQ. Drzewo tematów: Inwestycja → Lokalizacja / Standard, Mieszkania → Karta lokalu / Miejsca postojowe, Finansowanie → Kredyt / Harmonogram, Umów wizytę.

---

**👤 Użytkownik (17:42)**
Cześć! Szukam 3-pokojowego mieszkania z balkonem. Macie coś wolnego?

**🤖 Bot (17:42)**
Tak — w budynku B mamy 4 trzypokojowe z balkonem, 62–74 m², 620–780 tys. zł. Termin oddania III kwartał 2026.

*Sugestie: „Chcę kartę lokalu na maila" · „Jak dojechać na osiedle?" · „Ile wynosi zadatek?"*

---

**👤 Użytkownik (17:43)**
A który ma najlepszy widok?

**🤖 Bot (17:43)**
Mieszkania B3.04 i B4.04 — oba wychodzą na park miejski od południa. B4.04 to ostatnie piętro z tarasem 8 m². Cena 780 tys. zł.

*Sugestie: „Wyślij kartę B4.04" · „Jak wygląda standard wykończenia?" · „Chcę zobaczyć na żywo"*

---

**👤 Użytkownik (17:44)**
Standard wykończenia?

**🤖 Bot (17:44)**
Stan deweloperski: okna PCV trzyszybowe, ogrzewanie podłogowe gazowe, tynki gipsowe, wylewki. Wykończenie pod klucz w opcji — cena od dewelopera 850 zł/m².

*Sugestie: „Czy da się sprawdzić zdolność kredytową?" · „Jaki jest harmonogram wpłat?"*

---

**👤 Użytkownik (17:45)**
Chcę zobaczyć B4.04 na żywo, kiedy można?

**🤖 Bot (17:45)**
Świetnie — umówię wizytę z naszym doradcą. Otwarte wizyty wt/czw 14:00–18:00, w sob 10:00–14:00. Zostawmy kontakt, oddzwonimy dziś.

**[Pojawia się pill-button: „Zostaw kontakt: umów wizytę"]**

---

**👤 Użytkownik klika button → otwiera się bottom sheet**

**Formularz:**
- Imię i nazwisko *: Anna Kowalska
- Telefon *: 600 123 456
- E-mail *: anna.kowalska@example.com
- Którym mieszkaniem jesteś zainteresowany?: B4.04 — wizyta najlepiej sobota 25.04 ok. 11:00

**[Wyślij zgłoszenie]**

---

**🤖 Bot (17:46)**
✓ Dziękujemy! Mamy już Państwa kontakt — odezwiemy się wkrótce.

---

## Co wylądowało w panelu admina

**Konwersacja:** 8 wiadomości · 4 min · **Lead ✓** · Temat dominujący: *Mieszkania*

**Lead:**
- Anna Kowalska, 600 123 456, anna.kowalska@example.com
- Topic: `wizyta-lead`
- Interest: „B4.04 — wizyta najlepiej sobota 25.04 ok. 11:00"

**Sources w odpowiedziach bota (widoczne pod każdą odpowiedzią):**
- `Karty_lokali_budynek_B.pdf` (92% match)
- `Cennik_mieszkań_2026_Q2.pdf` (87% match)
- `Standard_wykończenia.pdf` (78% match)

---

## Komentarz biznesowy

- Klasyczny funnel: pytanie ogólne → konkretny lokal → standard → wizyta.
- Bot odpowiada krótko (1–2 zdania), nie zasypuje tekstem.
- Widzi w bazie wiedzy konkretne numery mieszkań i ceny — nie zmyśla.
- Lead form pojawił się jako CTA, nie wyskakujący formularz — user mógł przeczytać wcześniejsze wiadomości.
- W panelu admin jasne: *„kto, którym mieszkaniem, kiedy"*. Doradca dzwoni z pełnym kontekstem.
