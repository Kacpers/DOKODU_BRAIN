---
type: roadmap
status: active
owner: kacper
last_reviewed: 2026-03-06
tags: [roadmap, todo, strategia, rozwoj, planowanie]
---

# DOKODU — TODO & ROADMAP ROZWOJU
> Analiza oparta na: second brain (stan aktualny) + audit strony dokodu.it + benchmark agencji AI (Morningside AI, Liam Ottley, Brennan Dunn, Alex Hormozi model, Nathan Barry)
> Data: Marzec 2026 | Właściciel: Kacper Sieradziński

---

## LEGENDA PRIORYTETOW

- 🔴 KRYTYCZNE — blokuje wzrost, zrób teraz
- 🟡 WAZNE — zrób w ciagu miesiaca
- 🟢 STRATEGICZNE — Q2-Q3 2026
- 💡 INNOWACJA — moonshot, rozważ

---

## FAZA 0: NATYCHMIASTOWE (ten tydzien)
*Rzeczy, ktorych brak aktywnie kosztuje Cie pieniadze i klientow*

### Second Brain — uszczelnienie
- 🔴 Stworzyc `30_RESOURCES/RES_Templates/Schema_Faktura_v1.md` — JSON schema dla BP-003/PROMPT-001 (linki martwe)
- 🔴 Stworzyc `30_RESOURCES/RES_Templates/Logging_Standard.md` — standard logowania dla Code nodes (linki martwe)
- 🔴 Stworzyc `30_RESOURCES/RES_AI_Act_Notes/AI_Act_Notes.md` — notatki robocze z wytycznych EROD + UODO
- 🔴 Stworzyc `001_VISION.md` — 1 strona: kim jest Dokodu za 3 lata, ilu klientow, jaki przychod, jakie projekty, jaka reputacja. To kotwica dla wszystkich decyzji.
- 🟡 Dodac YAML frontmatter do wszystkich 20 plikow (type, status, tags, owner, last_reviewed)
- 🟡 Stworzyc `30_RESOURCES/RES_Market_Intelligence/Competitor_Landscape.md`

### Strona dokodu.it — krytyczne luki
- 🔴 **Brak case studies** — to jest zabojca konwersji. Bez 3 case studies z liczbami strona to ulotka, nie narzedzie sprzedazowe. Priorytet #1 na stronie.
- 🔴 **Brak testimonialów** — zero dowodu spolecznego. Nawet 3 cytaty z imienia i stanowiska = zmiana psychologiczna dla visitora
- 🔴 **Blog jest poza marką** — artykuly o Django, FastAPI, Docker, SQL nie buduja pozycji agencji AI dla biznesu. To przyciaga developerow, nie CEO i dyrektorow. Zmien strategie contentowa lub wydziel osobna sekcje.

---

## FAZA 1: FUNDAMENTY (Tydzien 1-4)
*Zbuduj to co boli najbardziej*

### A. Social Proof Machine (priorytet absolutny)

- 🔴 **Case Study #1: Corleonis** — po zakonczeniu projektu napisz case study: problem → rozwiazanie → wyniki (godziny zaoszczedzone, % dokumentow automatycznych, czas przetwarzania). Format: 800-1200 slow + 3 kluczowe liczby w nagłowku. Nie czekaj na "idealne dane" — minimum 30 dni po go-live.
- 🔴 **Case Study #2: Animex** — po szkoleniu zebrać ankiety + NPS + konkretne "aha moments". Napisac w stylu: "Jak Animex zredukował czas obsługi BOK o X% bez zatrudniania nowego pracownika"
- 🟡 **Testimonial Video** — po kazdym projekcie, przed ostatnia faktura, popros o 2-minutowe nagranie. Pytania: "Jaki był problem przed Dokodu? Co sie zmienilo? Co powiedziałbys komus, kto rozważa wspolprace?" Nie musisz motnowac — telefon wystarczy.
- 🟡 **"Licznik dowodow"** na stronie — "X firm przeszkolonych | Y godzin pracy zaoszczedzonych | Z wdrozen" (nawet szacunkowe na start). Liczby daja wiarygodnosc. Noah Kagan z AppSumo: "Social proof beats features every time."
- 🟡 **LinkedIn Recommendations** — po kazdym projekcie wyslij link do rekomendacji na LinkedIn. 10 rekomendacji na profilu Kacpra = darmowy social proof dla kazdego, kto googluje Dokodu.

### B. Content Pivot (blog i LinkedIn)

- 🔴 **Zmien strategie blogowa** — zamiast szerokiego tech contentu, pisz WYLACZNIE dla swojego ICP: CEO, COO, Dyrektor IT w firmach 50-500 prac. Tematy ktore konwertuja:
  - "Ile kosztuje Twoja firma kazda godzina straconą na ręczne procesy?" (kalkulator w artykule)
  - "AI Act 2026: co musisz wdrożyc przed sierpniem" (Twoja unikalna przewaga)
  - "Copilot vs ChatGPT Enterprise vs własne rozwiązanie — co wybrać dla firmy 100+ osób?"
  - "Case study: jak zautomatyzowalismy obieg dokumentow w firmie logistycznej" (Corleonis)
- 🟡 **LinkedIn jako glowny kanal** — nie blog, nie YouTube na start. LinkedIn dociera do decydentow B2B. Cel: 3 posty/tydzien przez 90 dni. Wzoruj sie na Liam Ottley (Morningside AI) — duzo konkretnych case studies, duzo liczb, zero teorii.
- 🟡 **Seria "AI w 60 sekund"** — krotkie posty/rolki z jednym konretnym trikiem AI dla biznesu. Niski koszt produkcji, wysoki zasieg. Po 20 epizodach — zebrac w e-book jako lead magnet.
- 🟢 **Newsletter "Dokodu Brief"** — tygodniowe 5 minut dla menadzera: 1 narzedzie AI, 1 case study z rynku, 1 update prawny (AI Act, RODO), 1 tip z n8n. Cel: 500 subskrybentow w 6 miesiecy. Model: Lenny's Newsletter (substack) ale dla polskiego B2B AI. Newsletter = lista wlasna = odpornnosc na algorytmy.

### C. Strona — quick wins

- 🟡 **Kalkulator ROI** — "Sprawdz, ile godzin miesiecznie mozemy odzyskac dla Twojej firmy". Proste 4-5 pytan (liczba pracownikow, sredni proces ręczny, ilosc godzin/tydz.), wynik w zlotowkach. Najlepszy lead magnet dla B2B. Doda po lewej stronie formularza konsultacji.
- 🟡 **FAQ sekcja** — "Ile kosztuje szkolenie?", "Jak dlugo trwa wdrozenie?", "Czy moje dane sa bezpieczne?", "Czy to dziala z naszym systemem ERP?", "Jaka jest gwarancja efektow?". Bez FAQ klient odpada zanim zadzwoni.
- 🟡 **Video na hero sekcji** — 90-sekundowe wideo Kacpra: "Oto co robimy i dla kogo". Nagranie telefonem w dobrym oswietleniu = wystarczy. Wideo na hero zwieksza konwersje o 20-30% (dane Wistia 2025).
- 🟡 **Pricing ballpark** — nawet "szkolenia zamkniete od 8 000 PLN" eliminuje nieodpowiednich leadow i kwalifikuje budzetowych. Nie musisz podawac dokladnych cen — daj widely. To buduje zaufanie, nie straszy.
- 🟢 **Calendly bezposrednio na stronie** — zamiast formularza → oczekiwania na email → odpowiedz → ustalanie terminu. Bezposredni booking = 60% wiecej umowionych konsultacji (dane Calendly 2025).

---

## FAZA 2: AUTOMATYZACJA SYSTEMU (Tydzien 2-6)
*Agencja automatyzacji, ktora nie automatyzuje siebie = utrata wiarygodnosci*

### Automatyzacja Second Brain (n8n)

- 🔴 **Workflow: "Brain Inbox Capture"**
  - Telegram Bot (@dokodu_brain_bot) lub dedykowany email → webhook → auto-dopisuje do `00_INBOX.md`
  - Capture z telefonu w 3 sekundy. Bez otwierania VS Code.
  - Dodatkowo: jezeli wiadomosc zawiera slowo "LEAD:" → auto-dopisuje do `CRM_Leady_B2B.md`

- 🟡 **Workflow: "Project Health Monitor"**
  - Trigger: codziennie 09:00
  - Sprawdza YAML `last_reviewed` w plikach projektow
  - Jezeli >7 dni bez update → Slack alert: "Corleonis nie byl aktualizowany 8 dni. Ostatni krok: [X]"
  - Jezeli >14 dni → Slack alert RED + email do Kacpra
  - Koszt wdrozenia: 2-3h. Efekt: nigdy wiecej "zapomnianych" projektow.

- 🟡 **Workflow: "Weekly Dashboard Updater"**
  - Trigger: piatek 07:30 (przed Weekly Review)
  - Pobiera: liczbe wykonan n8n (sukces/blad), nowe leady z formularza strony, kluczowe metryki
  - Aktualizuje sekcje KPI w `000_DASHBOARD.md`
  - Wyslij Slack summary: "Tydzien w liczbach: X leadow, Y projektow aktywnych, Z bledow n8n"

- 🟡 **Workflow: "Executive AI Shadow" (prawdziwy pipeline)**
  - Trigger: piatek 17:00 (po Weekly Review)
  - Wczytuje `000_DASHBOARD.md` + `00_INBOX.md` przez File Read
  - Wysyla do Claude API z PROMPT-040 z biblioteki
  - Output: Slack DM do Kacpra z analizą cross-domain + 1 trudne pytanie na weekend
  - To jest Twoj "CFO dla AI" dzialajacy automatycznie co tydzien.

- 🟢 **Workflow: "Lead Capture → CRM Auto"**
  - Formularz dokodu.it (webhook) → parsowanie danych → walidacja ICP
  - Automatyczny wpis do `CRM_Leady_B2B.md` + powiadomienie Slack #leady w ciagu <60 sekund
  - Auto-reply email do leada z linkiem do Calendly (personalizowany na podstawie kontekstu formularza)

- 🟢 **Workflow: "Skills → Content Correlator"**
  - Co tydzien analizuje nowe notatki w `005_SKILLS.md` i `00_INBOX.md`
  - Zlicza tagi (LangGraph, RAG, AI Act, etc.)
  - Jezeli tag pojawia sie >3x w miesiacu → Slack: "Duzo notatek o [X]. Rozwaz post LinkedIn lub nowy modul szkoleniowy."
  - Zamienia Twoja wiedze w pipeline contentowy automatycznie.

- 🟢 **Workflow: "Competitor Intelligence Monitor"**
  - Trigger: 1. dzien miesiaca
  - Scraping: strony konkurencji (cenniki, nowe usługi, case studies)
  - Claude API: "Co sie zmienilo w stosunku do poprzedniego miesiaca? Jakie sa implikacje dla Dokodu?"
  - Raport do Slacka #strategia

### Automatyzacja Biznesowa (usprawnij operacje)

- 🟡 **Auto-fakturowanie** — n8n + Fakturownia/iFirma API: po podpisaniu protokolu odbioru → automatyczna faktura + email do klienta + wpis w `AREA_Finanse`
- 🟡 **Onboarding Automation** — po podpisaniu umowy: n8n wysyla automatycznie caly "Onboarding Pack" (PDF welcome, link Calendly kickoff, Pre-kickoff checklist) bez recznej pracy Kacpra
- 🟢 **Retainer Reminder** — 5. dien miesiaca: automatyczny email do klientow retainerowych z faktura i krotkim update co dostaja w tym miesiacu

---

## FAZA 3: PRODUKTYZACJA (Miesiac 2-3)
*Zamien czas na produkty. Produkty skaluja sie, czas nie.*

Inspiracja: Brennan Dunn (Double Your Freelancing) — agencja → kursy → SaaS. Liam Ottley (Morningside AI) — agencja → YouTube → kursy → skalowanie. Nathan Barry (ConvertKit) — freelancer → kurs → SaaS.

### Produkty do stworzenia

- 🟡 **Kurs n8n — LAUNCH** (juz w backlogu, odblokuj blokady)
  - Blokada: skrypt VSL → sesja 2h solo, metoda Problem-Agitacja-Rozwiazanie
  - Blokada: platforma → decyzja do 2026-03-08 (Teachable jest najlatwiejszy do startu)
  - Nie czekaj na perfekcje — "done beats perfect". Liam Ottley launsowal pierwszy kurs nagrany w pokoju z IKEA półkami.

- 🟡 **"AI Act Compliance Kit"** — produkt cyfrowy, 997 PLN
  - Co zawiera: checklist audytu (PDF), szablon DPIA (Word/Notion), klasyfikator ryzyka (Excel), 60-minutowy kurs video + 30-minutowa konsultacja z Aliną
  - Target: compliance officers, prawnicy in-house, IT managerowie którzy dostali zadanie "sprawdz AI Act"
  - Lejek: artykul blogowy "AI Act w 10 punktach" → lead magnet PDF → pitch Kit
  - To jest Wasza unikalna oferta. Nikt inny w Polsce nie robi AI + legal w jednej agencji.

- 🟢 **"n8n Starter Pack" dla Agencji** — produkt cyfrowy, 299-499 PLN
  - Co zawiera: 8 gotowych blueprintow (juz masz!), biblioteka promptow (juz masz!), 2-godzinny kurs setup
  - Target: freelancerzy i male agencje ktore chca zaczac oferowac automatyzacje
  - To jest Twoj sposob na monetyzacje wiedzy bez sprzedawania czasu.

- 🟢 **Warsztaty Otwarte (grupowe)** — 699 PLN/os., max 12 osob, online
  - Tematy miesiecznie: "n8n dla Firm", "Copilot dla Managerow", "AI Act — co Twoja firma musi wiedziec"
  - Staly kalendarz = staly przychod. Nawet 8 osob × 699 PLN = 5 592 PLN za jeden dzien.
  - Platforma: Zoom + Notion/strona events

- 🟢 **"Diagnoza AI" jako produkt** — 500 PLN (teraz gratis)
  - Zamien bezplatna konsultacje w platny produkt diagnostyczny
  - Co dostaja: 45-minutowa sesja + 2-stronicowy raport z rekomendacjami + priorytetyzacja quick wins
  - Dlaczego platne: filtruje nieserio zainteresowanych, zwieksza perceived value, klient rozumie ze to praca
  - Model: Alex Hormozi — "darmowe = bezwartosciowe w glowie klienta". $100 audit = zaangazowanie.

### Productized Services (staly zakres, stala cena)

- 🟢 **"AI Act Ready" — pakiet** — 12 000 PLN (staly zakres)
  - Zakres: 2-dniowy audyt + raport + plan naprawczy + 1 miesiac support emailowy
  - Staly zakresu = mozna delegowac, skalowac, wyceniac bez dyskusji

- 🟢 **"n8n MVP" — pakiet** — 15 000 PLN (staly zakres)
  - Zakres: 1 workflow produkcyjny, max 3 integracje, dokumentacja, 30 dni wsparcia
  - Deadline: 3 tygodnie
  - Jezeli klient chce wiecej → aneks

- 🟢 **"Copilot Quick Start"** — 5 000 PLN (staly zakres)
  - Zakres: 1-dniowy warsztat dla max 15 osob + materialy + 2 tygodnie Q&A email
  - Latwy entry point, wysoka powtarzalnosc

---

## FAZA 4: WZROST I DYSTRYBUCJA (Miesiac 3-6)
*Zbuduj maszyne pozyskiwania klientow, ktora dziala bez Twojego czasu*

### Content Flywheel (Kolo zamachowe contentu)

Model: Matt Wolfe / Liam Ottley — content → social → lista → sprzedaz

```
Blog/LinkedIn post (darmowy)
    ↓
Lead magnet (PDF/kalkulator/kurs bezplatny)
    ↓
Lista email (Newsletter "Dokodu Brief")
    ↓
Nurturing (automatyczny — 7-emailowa sekwencja n8n)
    ↓
Oferta (kurs / diagnoza / szkolenie zamkniete)
    ↓
Klient
    ↓
Case study
    ↓
Nowy content (kolo sie zamyka)
```

- 🟢 **Lead Magnet #1: "AI Act Checklist 2026"** — PDF, 2 strony, bramka emailowa. Idealny dla Waszego pozycjonowania Tech+Legal. Cel: 200 emaili w pierwszym miesiacu.
- 🟢 **Lead Magnet #2: Kalkulator ROI "Ile tracisz bez automatyzacji?"** — interaktywny, na stronie. Uzytkownik wpisuje liczbe pracownikow i godziny → dostaje PLN rocznie + oferta diagnostyki.
- 🟢 **Lead Magnet #3: Modul 0 kursu n8n** — darmowy, 45-minutowy kurs video za email. To Twoj najsilniejszy magnes dla Persony C (freelancer/junior IT ktory chce oferowac automatyzacje).
- 🟢 **Email Sequence (n8n!)** — 7 emaili przez 14 dni po zapisaniu sie na liste:
  1. Powitanie + obiecany lead magnet
  2. Czym jest Dokodu (historia, nie pitch)
  3. Case study (Corleonis lub Animex — anonimizowane)
  4. Najczestszy blad przy wdrazaniu AI (edukacja)
  5. "Shadow AI" — artykul/post ktory rezonuje
  6. Pytanie: "Jaki jest Twoj glowny problem z AI w firmie?" (reply!)
  7. Miekki pitch: "Kiedy bedziesz gotowy, zaczynamy od bezplatnej diagnozy"

### Partnerstwa i Kanaly

- 🟢 **Microsoft Partner Program** — zostac oficjalnym partnerem Microsoft (AI + Copilot). Daje: badge na stronie, dostep do leadow Microsoft, materialy szkoleniowe. Klienci widza badge = zaufanie +30%. Wymaga: certyfikaty, liczba wdrozen.
- 🟢 **Google Partner Program** — analogicznie dla Gemini/Workspace. Badge "Google Partner" na stronie konwertuje.
- 🟢 **Program Partnerski z Prawnikami IT** — Alina ma siec. Prawnicy obsługujacy firmy tech dostaja zapytania "jak wdrozyc AI zgodnie z prawem" = idealny referral. Prowizja: 10-15% za polecenie.
- 🟢 **Program Partnerski z VAR-ami (Resellers M365)** — firmy sprzedajace licencje Copilot i nie wiedzace jak szkolyc = perfect fit dla Dokodu. Revenue share model.
- 🟢 **Wspolpraca z HR-tech firmami** — firmy IT rekrutacyjne (NoFluff Jobs, JustJoin) maja klientow HR ktory wdrazaja AI. Webinary wspolne = wzajemna ekspozycja.

### Community Building

- 🟢 **Discord/Slack "AI dla Firm Polska"** — darmowa spolecznosc dla managerow i IT pracujacych z AI. Dokodu jako moderator/expert = top-of-mind positioning. Model: Liam Ottley's AI Business Automation community.
- 🟢 **Webinary miesieczne (darmowe)** — "AI w [branza] — co dziala w 2026". Kazdy webinar = 50-200 nowych leadow. Nagranie = evergreen content. Leadow z webinarow nurturuj przez newsletter.
- 💡 **"Automatyzacja Live" na YouTube** — nagrywaj jak budujesz workflow na zywo dla anonimowego klienta. Zero edycji. Autentycznosc. Wes Roth/Matt Wolfe model. Budujesz autorytet i pipeline jednoczesnie.

---

## FAZA 5: SKALOWANIE (Q3-Q4 2026)
*Kiedy masz maszynę, czas ją skalować*

### Poszerzenie Oferty

- 🟢 **Industry Playbooks (x5 branż)** — po Corleonis (logistyka) i Animex (produkcja) budujesz playbooki: HR tech, finanse, e-commerce, budownictwo. Kazdy playbook to: gotowe pytania discovery, typowe bóle, znane systemy ERP, szacunkowe ROI, referencja do case study. Sprzedawalne produkty lub lead magnety premium.
- 🟢 **Rozszerzenie na sektor publiczny?** — AI Act jest najpilniejszy dla instytucji publicznych (szpitale, urzedy). High-value, ale dlugi cykl sprzedazy. Rozwazyc jako oddzielna linia przychodow.
- 💡 **White Label** — sprzedaj swoj know-how innym agencjom ktore chca oferowac AI compliance. Ty dostarczasz: metodologie, szablony, training. Oni robia sprzedaz. Revenue share. Model Brennan Dunn.
- 💡 **SaaS Tool — "AI Compliance Checker"** — automatyczny checker ktory analizuje opis systemu AI klienta i klasyfikuje ryzyko AI Act. Prosty form → AI → raport PDF. Cena: 99-299 PLN/raport lub SaaS. Unikalny na rynku polskim.

### Zatrudnienie / Skalowanie Zespołu

- 🟢 **Rekrutacja: AI Automation Consultant Junior** — kiedy MRR stabilnie >35k przez 3 miesiace. Profil: n8n + JavaScript + komunikatywnosc. Model B2B. Onboarding: 4-6 tygodni shadowingu.
- 🟢 **Outsourcing Content** — copywriter (jeden, zaufany) do artykulow blogowych pod SEO. Kacper dostarcza brief + kluczowe insights, copywriter pisze. Kacper edytuje. 4-6 artykulow/miesiac bez burnoutu.
- 💡 **Affiliate Program** — dla kursantow kursu n8n: polec klienta → dostaniesz 20% prowizji. Twoi studenci staja sie Twoimi handlowcami. Model ConvertKit (Nathan Barry).

### Zewnetrzna Ekspozycja

- 🟢 **Konferencja Infoshare (Gdansk, maj)** — wystapienie jako speaker. Temat: "AI Act w praktyce — co musi zmienic Twoja firma". To jest najlepszy kanal dla Twojego ICP. Zglos propozycje do marca.
- 🟢 **Podcast Guest Tour** — 5-10 polskich podcastow biznesowych/tech w Q2-Q3. Tematy: "AI dla firm", "automatyzacja procesow", "RODO a AI". Buduje autorytet i inbound.
- 🟢 **"Metodyka Dokodu" — White Paper** — 20-stronicowy dokument: jak wdrazamy AI w firmach, nasza filozofia, case studies, frameworki. Nie sprzedajacy — edukacyjny. Wysylasz do enterprise prospektow zamiast oferty. Konwersja rośnie gdy klient wie "jak myslisz".
- 💡 **Ksiazka** — Q4 2026 / Q1 2027. "AI w Twoim Biznesie — od Eksperymentu do Systemu". Self-published (Amazon KDP + wersja papierowa). Kazdy autor ksiazki biznesowej w Polsce to "ekspert z definicji". Moze nie zarobisz na niej duzo — ale kazda konsultacja zaczyna sie od "o, czytalam Twoja ksiazke".

---

## MOONSHOTS I WILD IDEAS
*Nie odrzucaj bo sa za duze — to najciekawsze rzeczy*

- 💡 **"AI Compliance SaaS"** — narzedzie online ktore firmy uzywaja samodzielnie do audytu AI Act. Dokodu jako tworca = recurring revenue bez sprzedawania czasu. Rynek: kazda firma w UE uzywajaca AI po 2026-08.
- 💡 **Program Certyfikacji "Certified AI Automation Specialist"** — Dokodu tworzy wlasny certyfikat. Firmy wysylaja pracownikow. Recurring cohorts. Model: Reforge (Brian Balfour) lub CXL Institute.
- 💡 **Fundusz AI dla MŚP** — wspolnie z inwestorem/funduszem: Dokodu wdraża AI w firmie w zamian za equity lub success fee od ROI. High risk, high reward. Rynek nieeksploatowany w Polsce.
- 💡 **"Second Brain as a Service"** — sprzedawaj ten system innym wlascicielom agencji. Nie jako szablon, jako wdrozenie. Pakiet: setup systemu + 2h onboarding + miesiac wsparcia = 3 000 PLN. Twoja pierwsza "productized operations service".
- 💡 **Podcast "AI w Polskim Biznesie"** — co 2 tygodnie, 30-minutowy wywiad z CEO/COO ktory wdrozyl AI. Ty jako host = top of mind, siec kontaktow, treści na kazdy kanal. Koszt: mikrofon (400 PLN) + czas.

---

## METRYKI SUKCESU (jak mierzyc postep)

| Metryka | Teraz (est.) | Cel Q2 2026 | Cel Q4 2026 |
| :--- | ---: | ---: | ---: |
| MRR (PLN) | ~15 000 | 35 000 | 75 000 |
| Klientow aktywnych | 2 | 5 | 10+ |
| Case studies opublikowanych | 0 | 3 | 7 |
| Lista emailowa | ~0 | 300 | 1 000 |
| Obserwujacy LinkedIn | ___ | +500 | +2 000 |
| Produkty cyfrowe (przychod) | 0 | 15 000 | 50 000 |
| NPS sredni | N/A | >8 | >9 |
| Czas CEO na operacjach | 80% | 60% | 40% |

---

## ZASADA HORMOZIE ZASTOSOWANA DO DOKODU

Alex Hormozi ("$100M Offers"): "Make your offer so good that people feel stupid saying no."

Twoja oferta powinna brzmiec tak:
> "W 30-minutowej diagnozie (darmowej) pokaze Ci DOKLADNIE ile PLN/miesiac tracisz na recznych procesach. Jezeli nie znajde przynajmniej 5x wartosci naszej usluge — nie bedziemy wspolpracowac. I tak nie bedziemy Ci nic sprzedawac — dostaniesz raport gratis."

To jest "Grand Slam Offer" dla agencji AI. Niemozliwy do odrzucenia. Bez ryzyka dla klienta.

---

## COTYGODNIOWY CHECK-IN (czy idzie dobrze?)

Zadaj sobie co piatek:
1. Czy opublikowalem przynajmniej 1 post LinkedIn?
2. Czy jest przynajmniej 1 nowy lead w CRM?
3. Czy aktualizowalem przynajmniej 1 projekt w systemie?
4. Czy zrobilem 1 krok w kierunku case study / testimonial?
5. Czy ten tydzien przybliżyl mnie do oferty, ktora "niemozliwa do odrzucenia"?

Jezeli 3+ TAK — jestes na dobrej drodze.

---

*Ten plik to zyjacy dokument. Aktualizuj go po kazdym miesiacu. Skreslaj co zrobione. Dodawaj co nowe. Nie pozwol mu sie zakurzyc.*
*Ostatnia aktualizacja: Marzec 2026 | Na podstawie: audit dokodu.it + second brain analysis + benchmark (Morningside AI, Hormozi, Nathan Barry, Liam Ottley, Brennan Dunn)*
