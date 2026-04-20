---
type: draft-contract
model: white-label
produkt: Chatbot by Dokodu
status: DRAFT — do weryfikacji przez Alinę
wersja: 0.1
data: 2026-04-20
---

# Umowa o Współpracy Handlowej (White-Label)
## Dokodu Sp. z o.o. × [Nazwa Partnera]

**UWAGA:** Ten dokument jest szkicem roboczym przygotowanym przez Kacpra. Zanim wyślesz Partnerowi, **Alina musi to przejrzeć** — zwłaszcza klauzule o IP, anti-circumvention, odpowiedzialności za wady i compliance.

---

## 1. Strony

**Dostawca (Licencjodawca):**
Dokodu Sp. z o.o.
[adres, NIP, REGON, KRS]
reprezentowana przez: Kacper Sieradziński

**Partner (Dystrybutor):**
[Nazwa firmy]
[adres, NIP, REGON, KRS]
reprezentowana przez: [osoba]

---

## 2. Definicje

- **Produkt** — oprogramowanie „Chatbot by Dokodu" w wersji aktualnej, obejmujące widget, panel administratora, silnik RAG, drzewo tematów i integracje zgodnie z dokumentacją techniczną stanowiącą **Załącznik nr 1**.
- **Klient Końcowy** — osoba prawna, z którą Partner zawarł umowę o świadczenie usługi chatbota w oparciu o Produkt.
- **White-Label** — model sprzedaży, w którym Partner prezentuje Produkt pod własną marką, a Dostawca pozostaje niewidoczny dla Klienta Końcowego.
- **Cennik Hurtowy** — stawki pobierane przez Dostawcę od Partnera za wdrożenie i utrzymanie Produktu (Załącznik nr 2).
- **Cena Detaliczna** — cena ustalona przez Partnera w relacji z Klientem Końcowym. Partner ma pełną swobodę jej ustalania.

---

## 3. Przedmiot umowy

3.1. Dostawca udziela Partnerowi **niewyłącznej licencji** na sprzedaż Produktu Klientom Końcowym w modelu White-Label na terenie: **Polska**.

3.2. Partner zobowiązuje się do samodzielnej sprzedaży, marketingu i obsługi Klienta Końcowego. Dostawca odpowiada wyłącznie za techniczne dostarczenie Produktu.

3.3. Partner może używać własnej nazwy handlowej, logo i materiałów sprzedażowych. **Nie może natomiast prezentować się jako twórca oprogramowania ani ukrywać faktu, że Produkt bazuje na technologii trzeciej strony w dokumentach, które z mocy prawa wymagają wskazania podmiotu przetwarzającego dane** (DPA, RODO).

---

## 4. Cennik hurtowy (co Partner płaci Dostawcy)

| Pozycja | Cena hurtowa (netto) |
| :--- | ---: |
| Wdrożenie **Chatbot Starter** (jednorazowo) | **19 900 PLN** |
| Wdrożenie **Chatbot Pro** (jednorazowo) | **39 900 PLN** |
| Retainer Starter Care (miesięcznie) | **890 PLN** |
| Retainer Pro Care (miesięcznie) | **1 990 PLN** |
| Godzina dodatkowej pracy Dostawcy (rozszerzenia) | **350 PLN** |

**Partner zatrzymuje całą różnicę między Ceną Detaliczną a Cennikiem Hurtowym.** Dla orientacji: jeśli Partner sprzeda Chatbot Starter za 50 000 PLN, jego marża wynosi 30 100 PLN netto (61%).

**Anti-creep:** stawki hurtowe obowiązują przez 12 miesięcy od daty podpisania umowy. Po tym okresie mogą być waloryzowane o wskaźnik inflacji GUS (nie więcej niż 8%/rok) z 30-dniowym wyprzedzeniem.

---

## 5. Fakturowanie i płatności

5.1. **Cykl B2B:** Klient Końcowy płaci Partnerowi → Partner fakturuje Dostawcę → Partner ma 14 dni od wpłaty Klienta Końcowego na uregulowanie faktury Dostawcy.

5.2. **Alternatywnie (do wyboru przy podpisie):** Dostawca fakturuje Partnera po podpisaniu umowy z Klientem Końcowym (50% zaliczka, 50% po go-live), niezależnie od tego kiedy Partner otrzymuje płatność od Klienta.

5.3. Opóźnienie płatności > 14 dni uprawnia Dostawcę do wstrzymania dostarczania Produktu dla nowych Klientów Końcowych Partnera do czasu uregulowania zaległości.

---

## 6. Zakres obowiązków

### Po stronie Dostawcy:

- Dostarczenie gotowej do wdrożenia wersji Produktu
- Konfiguracja serwera (gdy Klient Końcowy hostuje u Dostawcy)
- Import dokumentów i konfiguracja drzewa tematów
- Podstawowy branding zgodnie z wytycznymi Partnera
- Dokumentacja produktowa i polityka AI w wersji white-label (bez brandingu Dostawcy)
- Wsparcie L2 dla Partnera (bugi, awarie, incydenty bezpieczeństwa) — **SLA: alert < 4h, naprawa < 24h w dniach roboczych**
- Aktualizacje Produktu (nowe funkcje, poprawki bezpieczeństwa) bez dodatkowych opłat

### Po stronie Partnera:

- Pozyskanie Klienta Końcowego i sprzedaż
- Kontraktowanie (umowa z Klientem Końcowym, DPA, polityka AI)
- Wsparcie L1 dla Klienta Końcowego (pierwsza linia, pytania użytkowe, zmiany konfiguracyjne w panelu)
- Rozliczenia finansowe z Klientem Końcowym
- Pokrycie kosztów infrastruktury Klienta Końcowego, jeśli nie są rozliczane bezpośrednio przez Klienta (VPS, OpenAI API)
- Przekazanie Dostawcy zgłoszeń L2 w uzgodnionym formacie

---

## 7. Ochrona relacji biznesowej (anti-circumvention)

7.1. **Zakaz pomijania Partnera:** Dostawca zobowiązuje się nie kontaktować bezpośrednio z Klientami Końcowymi Partnera w sprawach sprzedażowych i nie zawierać z nimi umów bez pośrednictwa Partnera przez okres trwania umowy **oraz 24 miesiące** po jej rozwiązaniu.

7.2. **Zakaz pomijania Dostawcy:** Partner zobowiązuje się nie próbować rekonstruować, dekompilować ani reimplementować Produktu w okresie obowiązywania umowy i przez 24 miesiące po jej rozwiązaniu. Klient Końcowy, który po zakończeniu współpracy z Partnerem chce kontynuować usługę u Dostawcy, może to zrobić — ale wyłącznie po wcześniejszym oficjalnym wypowiedzeniu umowy z Partnerem, z zachowaniem okresu wypowiedzenia.

7.3. **Klauzula solidarna:** Jeśli Klient Końcowy trafia do Dostawcy z naruszeniem pkt. 7.1 lub 7.2, strona naruszająca płaci drugiej **karę umowną w wysokości 100% rocznej wartości kontraktu** z tym klientem.

---

## 8. Prawo własności intelektualnej

8.1. Kod źródłowy Produktu pozostaje własnością Dostawcy. Partner otrzymuje licencję niewyłączną na sprzedaż i używanie.

8.2. Branding, materiały marketingowe i dokumenty sprzedażowe tworzone przez Partnera na bazie white-label'a są własnością Partnera.

8.3. Dane Klientów Końcowych (dokumenty, konwersacje, leady) są własnością Klienta Końcowego. Ani Dostawca, ani Partner nie mogą ich wykorzystywać w innych celach niż świadczenie usługi.

8.4. Dostawca zachowuje prawo do wykorzystania **anonimowych metryk zbiorczych** (np. średnia liczba rozmów na instalację, średnia konwersja) do rozwoju Produktu — bez identyfikacji Partnera ani Klientów Końcowych.

---

## 9. Odpowiedzialność i wady

9.1. Dostawca odpowiada za wady Produktu zgodnie z SLA (pkt 6). W razie niedotrzymania SLA, Partner ma prawo do **obniżenia retainera o 10% za każdy przypadek naruszenia**, nie więcej niż 50% miesięcznie.

9.2. Dostawca nie odpowiada za:
- Treść dokumentów wgranych przez Klienta Końcowego
- Decyzje Klienta Końcowego podjęte na bazie rozmowy z botem
- Koszty OpenAI API ponoszone przez Klienta Końcowego lub Partnera
- Awarie wynikające z wadliwej konfiguracji po stronie Klienta Końcowego lub Partnera

9.3. **Limit odpowiedzialności Dostawcy:** odpowiedzialność całkowita Dostawcy względem Partnera ograniczona jest do wysokości kwoty zapłaconej Dostawcy w ciągu ostatnich 12 miesięcy z tytułu konkretnego zdarzenia, nie więcej niż 100 000 PLN netto.

---

## 10. RODO i ochrona danych

10.1. W relacji Klient Końcowy–Partner–Dostawca zachodzi podwójne powierzenie przetwarzania danych (Podpowierzenie, art. 28 ust. 4 RODO).

10.2. Partner zobowiązany jest zawrzeć z Klientem Końcowym umowę DPA w formie załącznika do umowy głównej.

10.3. Dostawca udostępni Partnerowi wzór DPA w wersji white-label (bez logo Dostawcy) — **Załącznik nr 3**.

10.4. Strony zobowiązują się wzajemnie informować o każdym incydencie bezpieczeństwa dotyczącym danych osobowych w ciągu **24 godzin** od jego wykrycia.

---

## 11. Czas trwania i wypowiedzenie

11.1. Umowa zawarta na czas nieokreślony, wchodzi w życie z dniem podpisania.

11.2. Każda ze stron może wypowiedzieć umowę z **60-dniowym okresem wypowiedzenia**, składanym na piśmie.

11.3. W przypadku rażącego naruszenia umowy (nieopłacone faktury > 60 dni, naruszenie pkt 7, ujawnienie danych Klienta Końcowego) — **14 dni** wypowiedzenia.

11.4. Po wypowiedzeniu Dostawca zobowiązuje się zapewnić migrację Klientów Końcowych Partnera do alternatywnego providera lub self-hostingu przez okres **90 dni** od zakończenia umowy, za dodatkowym wynagrodzeniem wg stawki godzinowej z pkt 4.

---

## 12. Poufność

12.1. Wszelkie informacje handlowe, techniczne, cennikowe, listy klientów i know-how są poufne przez okres obowiązywania umowy i **5 lat** po jej rozwiązaniu.

12.2. Zobowiązanie dotyczy obu stron, ich pracowników, podwykonawców i osób, z którymi strony zawierają umowy cywilnoprawne.

---

## 13. Postanowienia końcowe

13.1. Wszelkie zmiany umowy wymagają formy pisemnej pod rygorem nieważności.

13.2. Spory rozstrzyga sąd właściwy dla siedziby Dostawcy.

13.3. W sprawach nieuregulowanych stosuje się Kodeks Cywilny.

13.4. Załączniki stanowiące integralną część umowy:
- Załącznik nr 1 — Dokumentacja techniczna Produktu
- Załącznik nr 2 — Cennik Hurtowy (obowiązujący)
- Załącznik nr 3 — Wzór DPA white-label
- Załącznik nr 4 — Wzór polityki AI white-label

---

**Podpisy:**

Za Dostawcę: _________________________ (data, podpis)
Kacper Sieradziński, Prezes Zarządu, Dokodu Sp. z o.o.

Za Partnera: _________________________ (data, podpis)
[imię, funkcja, firma]

---

## Notatki dla Kacpra (nie do wysyłki Partnerowi)

**Co sprawdzić z Aliną zanim wyślesz:**

1. **Pkt 4 — ceny hurtowe.** Czy 19.9k / 39.9k za wdrożenie hurtowo dla Partnera to ok, czy dać Partnerowi dodatkowy discount (np. 17k / 35k) żeby jego marża była większa przy sprzedaży za 50k/100k?
2. **Pkt 5.2 — model fakturowania.** Rekomenduję opcję: Dostawca fakturuje Partnera po podpisie umowy z Klientem, **niezależnie** od tego kiedy Partner dostanie pieniądze. To Ty nie bierzesz ryzyka płynności Partnera.
3. **Pkt 7.3 — kara umowna.** Alina może chcieć dopracować wysokość (może 50% zamiast 100%, zależy od apetytu na negocjacje).
4. **Pkt 9.3 — limit odpowiedzialności.** 100k to sporo. Można zejść do 50k albo „wartość rocznego retainera x 3".
5. **Pkt 11.4 — migracja po rozwiązaniu.** Warto dodać stawkę minimalną za migrację (np. 5 000 PLN za pierwszą instancję + godzinowo za kolejne).
6. **Exclusivity.** Umowa jest **niewyłączna** — możesz mieć wielu Partnerów. Jeśli ten Partner zażąda wyłączności na Polskę, zażądaj w zamian: minimum 10 kontraktów / rok albo opłatę 60 000 PLN/rok za wyłączność.
7. **Marketing:** ustalcie kto pokrywa co (własny landing Partnera, eventy, reklamy). Nic w umowie — ustalenie osobne.

**Nie używaj TEJ umowy jako ostatecznej — to draft do rozmowy z Aliną.** Zwłaszcza klauzule IP, odpowiedzialności i anti-circumvention muszą być sprawdzone pod polskie prawo.
