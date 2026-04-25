---
type: tracker
status: active
owner: kacper
created: 2026-04-25
tags: [tiktok, shorts, batch, automatyzacja, wdrażanie, scenariusze]
---

# Batch nagraniowy 2026-04-25 — Wdrażanie Automatyzacji

> Pakiet 10 rolek talking-head do batch recording session (~50-70 min).
> Mix angle: fundamenty (2) + błędy (3) + quick wins (2) + insider/kontrowersja (3).
> Wszystkie zgodne z TOV TikTok (TikTok_Playbook.md) i ŻELAZNĄ ZASADĄ — nie strasz AI, pokaż że Kacper wie jak to zrobić dobrze.
> Cross-post: TikTok → YT Shorts → IG Reels → LinkedIn Video.

**Wersja v2 (2026-04-25):** wydłużone do 75-90s, dodane konkretne case'y z warsztatów, liczby, nazwane narzędzia (n8n, Pipedrive, Comarch, Aleo, Azure AD, M365 admin), struktury API (status 422, OAuth refresh, JSON), kwoty w PLN i USD.

---

## Notatki produkcyjne (przed nagraniem)

- **Format:** 1080x1920, 30 fps, talking-head, eye-level
- **Długość docelowa:** 75-90s (TikTok wciąż OK, YT Shorts ≤90s)
- **Tło:** czyste — białe biurko / monitor z kodem
- **Koszulka:** zmień co 3-4 klipy (T-050/051/052 → zmiana → T-053/054/055 → zmiana → T-056/057/058 → zmiana → T-059)
- **Między klipami:** 5s pauza + klaśnięcie (markery do cięcia)
- **Teleprompter:** Parrot (Dropbox sync) — wgraj scenariusze poniżej
- **Speed:** szybciej niż normalnie — TikTok pace, ale daj oddech przy liczbach (na nich zatrzymuj się 0.3s)
- **Patrz w obiektyw, nie w ekran**
- **Pauzy emfatyczne:** przed punchline, po hookach typu "powiem Wam dlaczego"

---

## T-050 — "Zanim wdrożysz automatyzację, zrób te 3 rzeczy"

**Angle:** A (fundamenty) | **Hook:** H4 + H2 | **Rola:** TRAILER serii | **~80s**

### Scenariusz

**[0-4s HOOK]**
Zanim wydasz dziesięć tysięcy na automatyzację, zrób te trzy rzeczy. Bo inaczej te pieniądze pójdą w błoto.

**[4-13s PROBLEM]**
Przeszkoliłem prawie dwieście firm. Widziałem to dziesiątki razy. Firma kupuje n8n, Make albo licencję Copilota. Wdraża na hurra. Pół roku później — jeden nieużywany dashboard i frustracja zarządu.

**[13-65s WARTOŚĆ — 3 konkretne kroki]**
**Pierwsze: spisz proces — ale konkretnie.** Nie "obsługujemy zamówienia". Tylko: kto, co, kiedy, w jakim systemie, na jaki output. Dla każdego kroku. Ja zaczynam zawsze od godziny warsztatu na Miro — i osiemdziesiąt procent projektu jest jasne zanim ktokolwiek dotknie n8n. Jak nie umiesz tego napisać na kartce — żaden workflow tego nie zautomatyzuje.

**Drugie: znajdź właściciela z imienia i nazwiska.** Nie "IT się tym zajmie". Nie "wszyscy". Konkretna osoba, która dostaje za to KPI i godziny w kalendarzu na utrzymanie. Bez tego — pierwsza zmiana tokenu w Google API i automatyzacja leży miesiąc.

**Trzecie: policz baseline w godzinach i złotówkach.** Cztery godziny księgowej tygodniowo razy stawka razy pięćdziesiąt dwa tygodnie. Konkretna kwota. Bez tego nigdy nie udowodnisz że wdrożenie się zwróciło — i drugi projekt zarząd Ci już nie zaaprobuje.

**[65-73s PUNCHLINE]**
Większość firm wybiera narzędzie zanim spisała pierwszy proces. To jak budowa domu zaczynając od wyboru mebli.

**[73-80s CTA]**
Obserwuj — kolejne dziewięć odcinków rozwija każdy z tych punktów na konkretnych przypadkach z warsztatów.

**Hashtagi:** #automatyzacja #ai #wdrażanieAI #n8n #firma

---

## T-051 — "Zaczynasz automatyzację od narzędzia? Już przegrałeś"

**Angle:** A (fundamenty) | **Hook:** H1 (przestań robić X) | **~80s**

### Scenariusz

**[0-4s HOOK]**
Zaczynasz automatyzację od wyboru narzędzia? Słuchaj — już przegrałeś. I to spektakularnie.

**[4-12s PROBLEM]**
n8n versus Make. ChatGPT versus Claude. Power Automate versus Zapier. Widzę firmy które trzy miesiące porównują licencje, nim w ogóle zdecydują CO chcą zautomatyzować.

**[12-65s WARTOŚĆ]**
Przykład z warsztatu w marcu. Firma logistyczna, sto pięćdziesiąt osób. Zarząd zdecydował że "robimy AI". Wybrali Microsoft Copilota. Wszystkim. Trzydzieści dolarów per użytkownik. Cztery i pół tysiąca dolarów miesięcznie.

Pytam: który proces to ma rozwiązać? Cisza. Rozglądają się. Odpowiedź: "no... wszystkie".

A wystarczyło zacząć od pytania: gdzie tracimy najwięcej godzin tygodniowo? W tej firmie odpowiedź to było awizowanie kierowców i przygotowywanie dokumentów odprawy celnej. Ani Copilot ani ChatGPT tego nie ogarnia. Tam potrzebny był konkretny agent na n8n integrowany z ich TMS-em.

Cztery i pół tysiąca dolarów miesięcznie wydane na narzędzie które ich problemu nie rozwiązuje.

**[65-73s PUNCHLINE]**
Narzędzie wybiera się POD proces. Nie odwrotnie. Bo narzędzie zmieni się za rok. Proces zostanie z firmą przez najbliższą dekadę.

**[73-80s CTA]**
Macie u siebie podobne wpadki? Komentarz, ciekawe ile osób się odnajdzie.

**Hashtagi:** #automatyzacja #procesy #wdrażanieAI #firma #management

---

## T-052 — "Twoja firma wdraża n8n od złej strony" (zmęczony n8n)

**Angle:** B (błędy) | **Hook:** H7 (powiem dlaczego nie działa) | **~85s**

### Scenariusz

**[0-4s HOOK]**
Twoja firma wdraża n8n od złej strony. Powiem Wam dokładnie dlaczego — i jak to naprawić.

**[4-13s PROBLEM]**
Każdy widzi w internecie że n8n robi cuda. Drag and drop, czterysta plus integracji, no-code rewolucja. Marketingowiec klika dwie godziny i ma agenta. I tak to się zaczyna.

**[13-70s WARTOŚĆ]**
A teraz co dzieje się trzy miesiące później. Realny przykład.

Klient wdrożył sobie sam workflow do pobierania zamówień z Allegro i wpisywania ich do Subiekta. Działało. Aż przestało.

Allegro zmieniło format API. Workflow zwraca błąd 422. Marketingowiec który to budował patrzy w logi n8n — JSON, headery, payloady. Nic z tego nie rozumie. IT też nie wie co ten workflow w ogóle robił.

Dwa tygodnie firma fakturuje ręcznie. Bo n8n to NIE jest no-code. To low-code.

Realnie potrzebujesz w firmie kogoś kto rozumie cztery rzeczy: REST API, autoryzacja OAuth versus klucze, format JSON i error handling. Bez tego — każde wdrożenie ma datę ważności.

Rozwiązanie? Buduj z partnerem który zostawia dokumentację i monitoring. Albo zatrudnij juniora dewelopera dwa-trzy dni w tygodniu na utrzymanie. To i tak taniej niż dwa tygodnie ręcznego fakturowania.

**[70-78s PUNCHLINE]**
n8n to nie różdżka z Hogwartu. To narzędzie inżynierskie z ładnym interfejsem.

**[78-85s CTA]**
Jak u Was wygląda utrzymanie automatyzacji — komentarz.

**Hashtagi:** #n8n #automatyzacja #lowcode #wdrożenia #it

---

## T-053 — "Najgłupszy błąd przy AI — robi go prawie każdy"

**Angle:** B (błędy) | **Hook:** H13 (sam ten błąd popełniałem) | **~85s**

### Scenariusz

**[0-4s HOOK]**
Najgłupszy błąd przy wdrażaniu AI w firmie. Sam go popełniałem rok i kosztowało mnie to klientów.

**[4-13s PROBLEM]**
Robi to prawie każda firma między pięćdziesiąt a pięćset osób. Zarząd czyta artykuł o ChatGPT. Decyzja: kupujemy Copilota. Wszystkim. Bo "trzeba być w temacie AI".

**[13-70s WARTOŚĆ]**
Liczby z prawdziwego klienta. Sto dwadzieścia osób. Trzydzieści dolarów per user. Trzy tysiące sześćset dolarów miesięcznie. Czterdzieści trzy tysiące dolarów rocznie.

Po dwóch miesiącach uruchomiłem im audyt użycia. Z M365 admin center wyciągnąłem dane. Wynik?

Aktywnych użytkowników: jedenaście osób. Reszta otworzyła Copilota raz, kliknęła, zamknęła.

Dlaczego? Bo nikt im nie pokazał konkretnego use case'u w ICH dziale. Księgowa nie wie czy może tam wkleić numer NIP. Handlowiec nie wie czy to widzi maile klientów. Project manager nie ma pomysłu jak to wpiąć w Asanę.

Co działa zamiast tego: pilot z pięcioma osobami z jednego działu, dwa konkretne use case'y, dwa tygodnie, mierzysz oszczędność godzin. Dopiero wtedy decyzja o skalowaniu — i to ze szkoleniem które startuje w PRACY tych osób, nie z teorii promptów.

**[70-78s PUNCHLINE]**
Większość firm KUPUJE AI w wielkim stylu. Mało która faktycznie je WDRAŻA. To dwie różne dyscypliny.

**[78-85s CTA]**
Macie Copilota i nie używacie? Komentarz — dziękuję za szczerość.

**Hashtagi:** #ai #copilot #wdrażanieAI #firma #produktywność

---

## T-054 — "Twoja automatyzacja umrze za 6 miesięcy"

**Angle:** B (błędy) | **Hook:** H4 (zanim zrobisz X) | **~85s**

### Scenariusz

**[0-4s HOOK]**
Twoja automatyzacja umrze za sześć miesięcy. Powiem Ci dokładnie dlaczego — i jak temu zapobiec.

**[4-13s PROBLEM]**
Standardowy scenariusz. Buduje ją zewnętrzny developer freelancer. Albo pasjonat z marketingu który robi to po godzinach. Wdrożone, działa, fajerwerki na Slacku.

**[13-70s WARTOŚĆ]**
Sześć miesięcy później. Freelancer ma już innych klientów, nie odbiera. Pasjonat dostał awans, nie ma czasu. Workflow zaczyna pikać błędami.

Realny case z lutego. Klient miał automatyzację która generowała oferty handlowe z Pipedrive. Działała półtora roku. Aż HubSpot kupił Pipedrive i zmienili strukturę API. Workflow padł.

Otworzyłem ich projekt n8n. Trzydzieści osiem nodów. Zero komentarzy. Zero dokumentacji. Trzy ukryte sub-workflowy. Zajęło mi sześć godzin żeby zrozumieć co to w ogóle ma robić — to znaczy SZEŚĆ GODZIN klienta na moim koszcie.

Co MUSI mieć każda automatyzacja w firmie: README w repo z opisem co robi i kogo pingować jak padnie. Komentarze przy każdym nietrywialnym kroku. Logging błędów do Slacka albo Sentry — nie ślepe nody. I druga osoba która rozumie chociaż dwadzieścia procent — backup biologiczny.

**[70-78s PUNCHLINE]**
Bus factor jeden to nie automatyzacja. To bomba zegarowa z kalendarzem na sześć miesięcy.

**[78-85s CTA]**
Macie automatyzacje od których wszystko wisi i zna je jeden człowiek? Dajcie znać.

**Hashtagi:** #automatyzacja #busfactor #it #wdrożenia #dokumentacja

---

## T-055 — "3 procesy które MUSISZ zautomatyzować jako pierwsze"

**Angle:** C (quick wins) | **Hook:** H2 (X rzeczy których nie wiesz) | **~85s**

### Scenariusz

**[0-4s HOOK]**
Trzy procesy które MUSISZ zautomatyzować jako pierwsze w firmie. Kolejność też ma znaczenie. Zapisuj.

**[4-12s PROBLEM]**
Bo jak zaczniesz od czegoś egzotycznego — utopisz tydzień bez efektu i zarząd Ci nie da budżetu na drugi projekt.

**[12-72s WARTOŚĆ]**
**Pierwszy: kwalifikacja leadów przychodzących.** Ktoś wypełnia formularz na stronie. Agent w n8n: pobiera dane firmy z Aleo albo Bisnode, sprawdza zatrudnienie, branżę, kondycję finansową, ocenia fit z waszym ICP, dodaje do CRM z gotową notatką dla handlowca. Pięć minut research handlowca per lead znika. Przy stu leadach miesięcznie — osiem godzin odzyskane.

**Drugi: opisywanie faktur kosztowych.** Wpada PDF na maila. Agent: wyciąga dane przez OCR, kategoryzuje koszt według planu kont, dopisuje do Comarchu albo iFirmy. Godzina księgowej dziennie znika. Przy minimalnej krajowej księgowej — to siedemset złotych miesięcznie czystej oszczędności.

**Trzeci: raport tygodniowy do zarządu.** Agent zbiera dane z Pipedrive, Slacka, kalendarza i Google Analytics. Generuje trzy slajdy z highlightami i tabelą KPI. Trzy godziny menedżera w piątek znikają.

Wszystkie trzy zaczniesz w jednym sprincie. Wszystkie trzy mają natychmiastowe ROI mierzalne w godzinach.

**[72-80s PUNCHLINE]**
Cztery godziny dziennie odzyskane w każdej firmie powyżej dwudziestu osób. To nie jest hipoteza. To matematyka.

**[80-85s CTA]**
Który byście odpalili u siebie pierwszy?

**Hashtagi:** #automatyzacja #ai #produktywność #crm #firma

---

## T-056 — "Najszybsze ROI z automatyzacji nie jest tym co myślisz"

**Angle:** C (quick wins) | **Hook:** H8 + twist | **~85s**

### Scenariusz

**[0-4s HOOK]**
Najszybsze ROI z automatyzacji nie jest tam gdzie patrzysz. Dosłownie wszyscy szukają nie tam.

**[4-12s PROBLEM]**
Wszyscy patrzą na sprzedaż, marketing, obsługę klienta. Bo te procesy widać. Bo o nich się mówi na konferencjach.

**[12-72s WARTOŚĆ]**
A najszybszy zwrot? Wewnątrz. W rzeczach których nikt nie pokazuje na slajdach.

Trzy realne wdrożenia z ostatniego półrocza:

**Onboarding nowego pracownika.** Ręczne tworzenie kont w Microsoft 365, Slack, Asana, Confluence, GitHub plus dostępy w VPN. Trzy godziny działu IT per osoba. Firma rekrutująca dwadzieścia osób miesięcznie? Sześćdziesiąt godzin IT zżartych. Po automatyzacji w Azure AD plus n8n — piętnaście minut per osoba.

**Powtarzalne pytania pracowników do HR.** "Ile mam urlopu?". "Jak złożyć wniosek o sprzęt?". "Kiedy wypłata?". Agent na bazie firmowego intranetu odpowiada instantowo. HR oszczędza półtorej godziny dziennie na samym odpisywaniu.

**Raport miesięczny do banku albo na zarząd.** Manager kopiuje dane z trzech systemów do PowerPointa. Cztery godziny w ostatni piątek miesiąca. Agent generuje go w minutę.

Nikt o tym nie mówi bo to nudne. Ale ROI mierzalny od pierwszego tygodnia.

**[72-80s PUNCHLINE]**
Sprzedaż jest sexy. Procesy wewnętrzne są pieniędzmi. Wybieraj pieniądze.

**[80-85s CTA]**
Co u Was kradnie najwięcej godzin tygodniowo — komentarz, polecę gdzie szukać quick winów.

**Hashtagi:** #automatyzacja #roi #firma #produktywność #procesy

---

## T-057 — "Przeszkoliłem 200 firm. Większość ma TEN sam problem."

**Angle:** D (insider) | **Hook:** H9 + H14 | **~85s**

### Scenariusz

**[0-4s HOOK]**
Przeszkoliłem prawie dwieście firm z AI. Dziewięćdziesiąt procent z nich ma dokładnie ten sam problem.

**[4-13s PROBLEM]**
I to nie jest brak narzędzi. Nie brak budżetu. Nawet nie brak ludzi do wdrażania. Mają wszystko.

**[13-72s WARTOŚĆ]**
Chodzi o to że nikt w firmie nie wie czyje to jest.

AI? Pytam na warsztacie: kto u Was odpowiada za wdrożenia AI? IT mówi że to projekty biznesowe, nie ich. Marketing że to nie ich kompetencja. Operacje że nie mają budżetu. Zarząd że "to wszystkich".

A "wszystkich" znaczy "nikogo". I dlatego po warsztacie nic się nie dzieje. Mimo że osiem godzin szkolenia kosztowało firmę kilkanaście tysięcy złotych.

Każda firma która rzeczywiście wdrożyła AI po naszej współpracy — i mówię o realnych case'ach, nie o slajdach — miała to samo.

**Jedna konkretna osoba.** Imię, nazwisko, mail. Z formalną rolą. AI Lead, AI Champion, Head of Automation — nazwa drugorzędna. Dostaje konkretne KPI: na przykład trzy wdrożenia kwartalnie. Dostaje czas w kalendarzu — dwadzieścia procent etatu minimum. Dostaje budżet — choćby skromny, sto tysięcy rocznie.

To jest ten jeden warunek. Reszta jest do zrobienia.

**[72-80s PUNCHLINE]**
Firmy nie potrzebują ChatGPT. Potrzebują człowieka który za AI bierze odpowiedzialność.

**[80-85s CTA]**
Macie u siebie tę jedną osobę? Komentarz tak / nie — ciekawi mnie statystyka.

**Hashtagi:** #ai #wdrażanieAI #firma #management #aichampion

---

## T-058 — "3 rzeczy których sprzedawca AI Ci NIE powie"

**Angle:** D (insider) | **Hook:** H9 (nikt Ci nie powie) | **~85s**

### Scenariusz

**[0-4s HOOK]**
Trzy rzeczy których sprzedawca AI w życiu Ci nie powie. Słuchaj uważnie — to ratuje budżety.

**[4-12s PROBLEM]**
Bo na każdy dolar który wydasz mniej myśląc, on dostaje większą prowizję. To nie jest osobiste — to jest model biznesowy.

**[12-72s WARTOŚĆ]**
**Pierwsze: cena per user to maksymalnie czterdzieści procent realnego kosztu.** Reszta to: integracja z waszymi systemami — kilkadziesiąt tysięcy. Konfiguracja Single Sign-On — kolejne kilkanaście. Szkolenie zespołu — dwa, trzy dni stawek konsultantów. Utrzymanie i support pierwszej linii. Realny TCO przez trzy lata to dwa do trzech razy ich oferta z PDF-a.

**Drugie: halucynacje są w KAŻDYM modelu.** Nawet w GPT-5. Nawet w Claude Opus. Bez procesu weryfikacji człowieka — wkładasz firmie minę. Klient prawnicza, sprawdzała umowy AI bez review prawnika. Trzy umowy podpisane z błędnymi paragrafami. Strata sześciocyfrowa.

**Trzecie: lock-in danych.** Prompty, fine-tuned modele, embeddingi, baza wiedzy — wszystko w ich infrastrukturze. Zmiana dostawcy za dwa lata? Trzy do sześciu miesięcy migracji plus kilkadziesiąt godzin pracy zespołu. Często firmy się poddają i płacą podwyżki.

Pytaj o to przed podpisaniem umowy. Zapisuj odpowiedzi. Wracaj do nich za rok.

**[72-80s PUNCHLINE]**
AI to nie magia. To narzędzie z konkretnymi kosztami, ryzykami i polityką dostawcy. Reszta to marketing.

**[80-85s CTA]**
Jakie ukryte koszty Wam się objawiły po wdrożeniu? Komentarz.

**Hashtagi:** #ai #wdrażanieAI #copilot #saas #lockin

---

## T-059 — "Jeśli nie masz TEGO w firmie — n8n Ci nie pomoże"

**Angle:** D (kontrowersja, drugi take na n8n) | **Hook:** H7 | **~85s**

### Scenariusz

**[0-4s HOOK]**
Jeśli nie masz tego jednego w firmie — n8n Ci nie pomoże. Choćbyś zapłacił za pakiet enterprise.

**[4-13s PROBLEM]**
Wszyscy mówią o n8n jak o magicznej różdżce. Drag, drop, automatyzacja gotowa, marketing pisze że "no-code dla każdego". Półprawda.

**[13-72s WARTOŚĆ]**
Realnie n8n to potężne narzędzie inżynierskie. Tylko wymaga jednej kompetencji w firmie — kogoś kto rozumie cztery rzeczy:

**REST API i HTTP** — co znaczy GET, POST, PUT, DELETE. Co zwraca status 401, 403, 422. Bo każda integracja to gadanie z czyimś API.

**OAuth versus klucze API.** Jak refreshować token. Co zrobić gdy Google rotuje credentials. Bo tutaj pada osiemdziesiąt procent automatyzacji.

**JSON i transformacje danych.** Function node, expressions, jq. Bo dane między systemami nigdy nie pasują jeden do jednego.

**Error handling.** Try-catch w n8n. Webhook do Slacka jak coś padnie. Bo workflow który pada cicho jest gorszy niż brak workflow.

Marketingowiec tego nie ogarnie. Księgowa też nie. Potrzebujesz programisty na pół etatu, tech-savvy konsultanta z umową albo zewnętrznego partnera z SLA.

Bez tej osoby — zostań przy Zapierze. Tańsze, prostsze, mniej możliwości ale i mniej rozczarowań.

**[72-80s PUNCHLINE]**
n8n to nie no-code dla każdego. To low-code dla ludzi którzy wiedzą co robią z API.

**[80-85s CTA]**
Macie kogoś od n8n in-house czy outsourcujecie? Komentarz.

**Hashtagi:** #n8n #automatyzacja #it #lowcode #wdrożenia

---

## Sugerowany harmonogram publikacji (10 dni)

| Dzień | Klip | Optymalna godzina |
|---|---|---|
| Pon 27.04 | T-050 (TRAILER) | 18:00 |
| Wt 28.04 | T-055 (3 procesy) | 16:00 |
| Śr 29.04 | T-053 (Copilot dla wszystkich) | 17:00 |
| Czw 30.04 | T-052 (n8n złą stroną) | 18:00 |
| Pt 01.05 | T-057 (200 firm) | 12:00 |
| Sob 02.05 | T-051 (od narzędzia przegrałeś) | 10:00 |
| Nd 03.05 | T-056 (najszybsze ROI) | 20:00 |
| Pon 04.05 | T-054 (umrze za 6 miesięcy) | 18:00 |
| Wt 05.05 | T-058 (sprzedawcy AI) | 16:00 |
| Śr 06.05 | T-059 (n8n bez kogoś od API) | 17:00 |

---

## Po nagraniu — checklist

- [ ] Wszystkie klipy w 1080x1920, 30fps
- [ ] Napisy auto-generowane z polskimi znakami (ą, ę, ś, ź, ż, ó, ł, ń, ć)
- [ ] Cross-post bez watermarku TikToka (do IG/YT Shorts/LinkedIn)
- [ ] Aktualizacja statusów w `TikTok_Ideas_Bank.md` (POMYSŁ → NAGRANY → OPUBLIKOWANY)
- [ ] Po pierwszym tygodniu — szybki review metryk (watch-through, saves, shares)
