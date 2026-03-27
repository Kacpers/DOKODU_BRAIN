---
type: course-script
module: BONUS_B
title: "Sprzedaż i Delivery Projektów Automatyzacji — Skrypt nagrania"
duration: "~2h 00min"
status: draft
last_reviewed: 2026-03-27
---

# Skrypt nagrania — Moduł BONUS B
## Sprzedaż i Delivery Projektów Automatyzacji

---

## SEGMENT 1: HOOK I WSTĘP (00:00 – 05:00)

[SLAJD 1 — Tytuł modułu]

Umiesz budować automatyzacje. Ale czy umiesz za to wziąć 30 000 złotych?

Bo to jest właśnie problem, który widzę u większości osób które uczą się n8n. Uczą się techniki — i to dobrze. Ale technologia to jest może 20% sukcesu w tym biznesie. Pozostałe 80% to sprzedaż, komunikacja z klientem i delivery. I właśnie tym zajmiemy się przez te dwie godziny.

Zanim przejdziemy dalej — kilka słów o tym dlaczego możesz mi w ogóle wierzyć. Nie dlatego że mam ładny kurs. Dlatego że popełniłem dosłownie każdy błąd który zaraz ci pokażę. Zbudowałem system za 5 000 złotych, który był wart 40 000. Wziąłem projekt bez zaliczki i klient zrezygnował po 30 godzinach mojej pracy. Podpisałem umowę bez zakresu i projekt urósł trzy razy. Wrócimy do każdego z tych przypadków szczegółowo.

[SLAJD 2 — Problem]

Gratulacje. Jesteś w miejscu, gdzie większość kursów n8n się kończy. My dopiero zaczynamy to, co decyduje czy zarobisz pieniądze.

[SLAJD 3 — Co zmieni się po tym module]

Po tych dwóch godzinach będziesz umiał wycenić projekt w trzech modelach — i wiedzieć który wybrać. Przeprowadzić Discovery Call jak doradca, nie jak technik. Napisać ofertę która sprzedaje, a nie listę technologii. Podpisać umowę która cię chroni. I przekonać klienta do retainera — bo to jest właśnie fundament stabilnego przychodu.

Na koniec pokażę ci też szablony — gotowe do użycia od jutra.

Zaczynamy.

---

## SEGMENT 2: WYCENA PROJEKTÓW AUTOMATYZACJI (05:00 – 30:00)

### 2.1 Trzy modele wyceny (05:00 – 13:00)

[SLAJD 4 — Trzy modele wyceny]

Są trzy modele wyceny w projektach automatyzacji. Nie ma jednego dobrego. Jest właściwy dla sytuacji.

Pierwszy to T&M — Time and Materials. Płacisz za czas. Drugi to Fixed Price — stała cena za zdefiniowany zakres. Trzeci to Value-Based Pricing — wyceniasz na podstawie wartości którą tworzysz dla klienta, nie godzin które spędzasz.

Zacznijmy od T&M, bo to jest to co większość osób zaczyna robić intuicyjnie.

[SLAJD 5 — T&M]

T&M brzmi bezpiecznie dla ciebie — ale klienci tego nie lubią. I mają rację. Klient dostaje workflow który działa — ale nie wie ile to go kosztuje do końca. To buduje niepewność i tarcie.

T&M ma sens kiedy robimy proof of concept. Kiedy integrujemy się z systemem legacy i nie wiadomo jak głęboka jest królicza nora. Kiedy klient chce płacić za iteracje, bo sam nie wie dokładnie czego chce.

T&M nie ma sensu kiedy zakres jest jasny. Kiedy klient budżetuje z góry i chce znać finalną kwotę. Kiedy to jest standardowy projekt który już robiłeś.

Zabezpieczenie dla T&M: tygodniowy raport godzin plus budżetowy cap. Coś w stylu: "pracujemy w modelu T&M do 80 godzin — po przekroczeniu wracamy do rozmowy." Dzięki temu klient nie dostaje niespodzianki, a ty nie ryzykujesz pracy bez limitu.

[SLAJD 6 — Fixed Price]

Fixed Price jest wygodny dla klienta — i niebezpieczny dla ciebie, jeśli nie wiesz co robisz.

Kiedyś wziąłem projekt fixed price: "integracja CRM z systemem wysyłkowym." Brzmiało prosto. Okazało się że system wysyłkowy ma API z 2012 roku, bez dokumentacji, z podstawową autoryzacją przez HTTP. Spędziłem 40 dodatkowych godzin na reverse engineeringu. Za które nikt nie zapłacił — bo fixed price.

Żeby Fixed Price zadziałał, musisz zdefiniować z góry: dokładne deliverables jako listę, maksymalną liczbę rund poprawek, co jest poza scope i jak działa change request, oraz różnicę między środowiskiem testowym a produkcyjnym.

Złota zasada: jeśli nie możesz opisać zakresu jako listy punktów — nie wyceniaj fixed.

[SLAJD 7 — Value-Based Pricing]

A teraz najtrudniejszy model — i najbardziej opłacalny. Value-Based Pricing.

Tutaj sprzedajesz wynik, nie godziny. I to całkowicie zmienia dynamikę.

Formuła wygląda tak: bierzesz oszczędność czasu, mnożysz przez koszt godziny pracownika klienta, dodajesz eliminację błędów i ich koszt, dodajesz wartość przyspieszenia procesów. I dostajesz wartość biznesową twojego rozwiązania.

Konkretny przykład. Klient ma pięciu pracowników którzy spędzają trzy godziny dziennie na ręcznym wprowadzaniu danych. To jest 75 godzin tygodniowo. Przy koszcie 60 złotych za godzinę — to jest 4 500 złotych tygodniowo. Rocznie 234 000 złotych zmarnowanych na pracę manualną.

Twój workflow kosztuje 20 000 złotych i daje zwrot w pięć tygodni.

Kiedy klient widzi 234 000 złotych po lewej stronie i 20 000 po prawej — nie ma o czym rozmawiać. Problem polega na tym że musisz to policzyć razem z klientem na Discovery Callu. Jeśli wyliczysz to sam i prześlesz — klient nie wierzy. Jeśli wy to liczycie razem — klient sam uzasadnia twoją cenę.

---

### 2.2 Jak szacować godziny — WBS (13:00 – 23:00)

[SLAJD 8 — Kalkulator wyceny, Breakdown Tasks]

Teraz porozmawiajmy o tym jak konkretnie szacować projekt. Metoda nazywa się WBS — Work Breakdown Structure. Rozbijasz projekt na wszystkie kategorie pracy i szacujesz każdą osobno.

[DEMO: pokaż szablon tabeli WBS]

Pokażę ci teraz jak to wygląda na żywo. Mam tutaj tabelę — to będzie jeden z szablonów do pobrania po module.

Kategorie są następujące: Discovery i analiza to 4 do 8 godzin. Projektowanie architektury i diagramu flow — 2 do 6 godzin. Konfiguracja środowiska, Docker, credentials, VPN — od godziny do czterech. Budowa każdego nietrywialnego node'a — 1 do 3 godzin. Każda integracja API — 2 do 6 godzin. Obsługa błędów i retry logic — dolicz 25% do całości budowy. Testy — 20% do całości budowy. Dokumentacja techniczna i użytkowa — 10% całości projektu. Handover i szkolenie klienta — 2 do 4 godzin. I bufor na niespodzianki — zawsze minimum 30%.

Najczęstszy błąd który widzę: ludzie liczą tylko czas budowy. Zapominają o discovery, dokumentacji, testach, setupie środowiska. A to jest często 50% projektu.

Suma wszystkich godzin razy twoja stawka — to jest cena bazowa przed buforem.

---

### 2.3 Przykładowe wyceny i psychologia cen (23:00 – 30:00)

[SLAJD 9 — Przykładowe wyceny]

Dajmy teraz konkretne liczby. Bo przez lata widziałem jak ludzie się boją podawać ceny — i to jest jeden z głównych powodów dla których zarabiają za mało.

Prosty workflow: powiadomienia, sync danych, jedna lub dwie integracje. 20 do 40 godzin pracy. Cena: 8 000 do 15 000 złotych. Przy stawce 250 do 400 złotych za godzinę.

Złożony agent z logiką decyzyjną, AI, czterema lub więcej systemami: 80 do 180 godzin. Cena: 30 000 do 80 000 złotych.

System RAG z bazą wiedzy, embeddingami i interfejsem: 50 do 120 godzin. 20 000 do 50 000 złotych.

[SLAJD 10 — Bufor 30%]

Te liczby są z prawdziwych projektów, zanonimizowane. Proszę żebyś nie traktował dolnych widełek jako normy. To jest absolutne minimum dla klienta który jest super zorganizowany, ma czas, dostarcza dostępy w jeden dzień i nie zmienia wymagań. Taki klient istnieje — ale jest rzadszy niż myślisz. Większość projektów ląduje bliżej górnej granicy.

I teraz o bufforze. Mówiłem że minimum 30%. Pozwól że powiem ci co zjada twój bufor: API które nie działają jak w dokumentacji — zawsze tak jest. Klient który "miał coś powiedzieć wcześniej". Środowisko produkcyjne które różni się od testowego. Rotacja po stronie klienta — nowy koordynator, który nie wie o co chodzi. Urlopy, choroby, opóźnienia w dostarczeniu dostępów.

Mój bufor na nowych klientach to 50%. I nadal czasem ledwo wychodzę.

Na koniec — psychologia ceny. Dlaczego 28 000 złotych jest gorsze niż 30 000? Bo 28 000 wygląda jak "zrobiłem rabat ale nadal drogo". 30 000 wygląda jak świadoma, profesjonalna wycena. Okrągłe liczby budują poczucie że wiesz co robisz. I zwykle masz rację.

---

## SEGMENT 3: CASE STUDY — BŁĘDY KTÓRYCH POPEŁNIŁEM (30:00 – 40:00)

[SLAJD 34 — Błędy które popełniłem]

Teraz czas na szczerość. Opowiem wam o projekcie który poszedł źle. Serio źle.

[CASE STUDY: Projekt "integracja bez discovery"]

Był rok 2022. Dostałem zapytanie od firmy e-commerce — chcieli zautomatyzować obsługę zamówień. Dostałem briefing przez email: dwa akapity. Nie zrobiłem Discovery Callu bo "brzmiało prosto". Nie miałem w ogóle procesu discovery w tamtym czasie.

Zbudowałem workflow. Zajęło mi dwa tygodnie. Byłem z siebie dumny. Wysłałem do klienta z prośbą o testy.

Cisza przez trzy dni. Potem telefon. Klient mówi: "Ale my chcieliśmy coś innego. My mieliśmy na myśli integrację z naszym wewnętrznym systemem magazynowym, nie z WooCommerce."

Nie wiedziałem że mają wewnętrzny system magazynowy. Bo nie zapytałem. Bo nie zrobiłem discovery.

Projekt kosztował klienta 15 000 złotych. Żeby zrobić to co naprawdę chcieli — potrzebowałem kolejnych trzech tygodni i nowego workflow od zera. Klient nie chciał więcej płacić. Miał rację — obiecałem mu rozwiązanie problemu, nie konkretny workflow.

Co z tego wyciągnąłem? Trzy lekcje, które zmieniły jak prowadzę projekty.

Pierwsza: discovery to nie jest opcja. To jest obowiązek — wobec klienta i wobec siebie. Bez 45 minut rozmowy żadna wycena nie ma sensu.

Druga: "rozwiązanie problemu" i "konkretna technologia" to nie to samo. Klient kupuje wynik. Jeśli twój workflow nie daje mu tego wyniku — nie ma znaczenia że technicznie działa.

Trzecia: brak discovery to nie tylko ryzyko dla ciebie. To ryzyko dla klienta. On traci czas i pieniądze na coś co nie rozwiązuje jego problemu.

Opowiem wam za chwilę jak wygląda mój Discovery Call dzisiaj. Ale najpierw jeszcze jeden błąd — bo warto o tym mówić.

Projekt bez zaliczki. Klient był polecony przez znajomego — więc uznałem że mogę zaufać bez standardowych formalności. Zacząłem pracę. Po 30 godzinach klient powiedział że "projekt idzie w innym kierunku niż planowali" i przepraszają. Miło. 30 godzin pracy — zero złotych.

Od tego dnia każdy projekt startuje od zaliczki. Minimum 30%, przelewem przed pierwszym spotkaniem projektowym. Nie z powodu braku zaufania — z powodu szacunku do własnej pracy.

---

## SEGMENT 4: DISCOVERY CALL FRAMEWORK (40:00 – 60:00)

### 4.1 Struktura Discovery Callu (40:00 – 45:00)

[SLAJD 11 — Discovery Call]

Discovery Call to nie jest zbieranie wymagań technicznych. To jest jedno z najczęstszych nieporozumień które widzę.

Większość konsultantów idzie na discovery żeby zapytać: jakie API, jaki CRM, jakie dane. To błąd. Idziesz na discovery żeby zrozumieć: po co to właściwie jest? Co się naprawdę stanie jeśli ten problem zostanie rozwiązany? Albo nie zostanie?

Dobry Discovery Call ma trzy efekty. Wiesz co zbudować. Wiesz ile to warte — masz dane do value-based pricing. I wiesz czy chcesz z tym klientem pracować. Ten trzeci punkt jest równie ważny co poprzednie dwa.

Czas: 45 do 60 minut. Nie więcej. Jeśli nie udało ci się zebrać potrzebnych informacji w godzinę — albo scope jest zbyt niejasny, albo klient nie jest gotowy do projektu.

Jak się przygotować: przejrzyj stronę firmy, profil LinkedIn osoby z którą rozmawiasz, podstawowe informacje o branży. Pięć minut researchu zmienia ton rozmowy — pokazujesz że traktujesz klienta poważnie.

---

### 4.2 10 pytań które musisz zadać (45:00 – 55:00)

[SLAJD 12 — 10 pytań na Discovery Call]

[DEMO: pokaż wydrukowaną listę pytań]

Teraz 10 pytań. Wydrukuj tę listę i połóż przed sobą na każdym discovery callu. Bez wyjątków.

Pytanie pierwsze: jaki konkretny problem chcecie rozwiązać? Nie: co chcecie zautomatyzować. Chcesz usłyszeć problem, nie rozwiązanie które klient już sobie wymyślił. Bo często to co mówi że chce — to nie jest to czego potrzebuje.

Pytanie drugie: co się dzieje jeśli ten problem nie zostanie rozwiązany? To jest pytanie o skalę bólu. Klient który odpowiada "no cóż, jakoś damy radę" — to jest klient bez pilności. Klient który odpowiada "mamy deadline w przyszłym miesiącu i grozi nam kara umowna" — to jest klient który podejmie decyzję.

Pytanie trzecie: jak ten proces wygląda dziś, krok po kroku? Tu chcesz dosłownie prześledzić każdy krok. Kto robi co. Jakie systemy. Gdzie są ręczne kroki. To jest baza do budowania workflow.

Pytanie czwarte: ile osób jest w to zaangażowanych i ile czasu poświęcają? To jest twój kalkulator ROI. 3 osoby po 2 godziny dziennie to 6 godzin dziennie — pomnóż przez stawkę i masz wartość biznesową.

Pytanie piąte: czy próbowaliście już to rozwiązać? Co nie zadziałało? To jest bardzo ważne pytanie. Jeśli próbowali i się nie udało — chcesz wiedzieć dlaczego. Bo może problem leży gdzie indziej niż myślisz. Albo masz okazję pokazać że twoje podejście jest inne.

Pytanie szóste: kto podjął decyzję o szukaniu rozwiązania i kto zatwierdza budżet? Musisz wiedzieć czy rozmawiasz z decydentem. Jeśli rozmawiasz z kimś kto będzie "raportował do zarządu" — cały twój discovery może pójść na marne jeśli zarząd ma inne priorytety.

[SLAJD 13 — Pytanie o budżet]

Pytanie siódme: jaki macie budżet na ten projekt? To jest najtrudniejsze pytanie. Większość ludzi je pomija. Nie pomijaj.

Jeśli klient nie chce podać liczby, powiedz tak: "Żeby zaproponować właściwe rozwiązanie, muszę wiedzieć z jakimi możliwościami pracuję. Czy mówimy o budżecie poniżej 10 000, między 10 a 50 tysiącami, czy powyżej?"

Podałeś widełki — klient wybierze przedział. To jest neutralne. Nie mówisz że coś kosztuje X, pytasz gdzie jesteś. Mam klienta który miał 3 000 złotych budżetu. Dowiedziałem się o tym po 6 godzinach discovery. To był mój błąd — nie jego.

Pytanie ósme: do kiedy chcecie to uruchomić i dlaczego właśnie ta data? Dlaczego ta data — to jest kluczowe. "Chcemy do końca kwartału" bez powodu to sygnał że deadline jest miękki. "Mamy targi branżowe 15 marca i chcemy pokazać system klientom" to jest twarda motywacja.

Pytanie dziewiąte: jak wygląda wasza infrastruktura techniczna? Jakie systemy używacie? Tu zaczynasz zbierać dane techniczne. Ale dopiero na dziewiątym pytaniu — po tym jak zrozumiałeś problem i wartość biznesową.

Pytanie dziesiąte: co jest dla was definicją sukcesu tego projektu? To pytanie usuwa nieporozumienia zanim się pojawią. "Workflow działa" to za mało. "Mamy zero manualnych kroków w procesie i czas obsługi zamówienia spadł o 80%" — to jest definicja sukcesu z której możesz zbudować kryteria akceptacji.

---

### 4.3 Red Flags — kiedy powiedzieć NIE (55:00 – 60:00)

[SLAJD 14 — Red Flags]

Teraz najtrudniejsza część. Kiedy powiedzieć NIE.

Wiem że to jest trudne. Szczególnie na początku kiedy każdy projekt wygląda jak szansa. Ale wziąłem kilka projektów mimo oczywistych red flagów — i każdy z nich kosztował mnie więcej niż był wart.

Pierwsza flaga: "zrób to szybko, potem rozliczymy." Brak formalności to brak płatności. Nie dlatego że klient jest nieuczciwy — dlatego że priorytety się zmieniają, ludzie odchodzą, projekty się kończą.

Druga flaga: brak osoby decyzyjnej w rozmowie. Jeśli na discovery callu siedzisz z kimś kto mówi "muszę to jeszcze skonsultować z szefem" i szef nigdy nie pojawi się w rozmowie — nie wiesz czy ktoś naprawdę chce ten projekt.

Trzecia flaga: "to proste, to zajmie wam godzinę." Klient który mówi ci ile coś zajmie — nie rozumie zakresu pracy. I nie będzie rozumiał twojej wyceny.

Czwarta flaga: poprzedni dostawca ich "zawiódł." Możliwe. Ale równie możliwe że problem leży po stronie klienta — nierealistyczne oczekiwania, brak decyzji, ciągłe zmiany zakresu. Zawsze pytaj co konkretnie nie zadziałało.

Piąta flaga: nie mają zdefiniowanego procesu. Automatyzujesz chaos — to nie działa. Możesz zautomatyzować tylko to co jest stabilne i powtarzalne. Jeśli klient sam nie wie jak jego proces wygląda — najpierw musi go zdefiniować.

Szósta flaga: negocjują cenę zanim zobaczyli ofertę. "A ile mniej więcej..." po dwóch minutach rozmowy. Taki klient będzie negocjował na każdym etapie. I nigdy nie będzie zadowolony z ceny.

Siódma flaga: "chcemy wszystko zrobić sami, tylko powiedzcie jak." Nie potrzebują wykonawcy — potrzebują konsultanta. To jest inny produkt. Możesz ich obsłużyć — ale nie jako projekt implementacyjny.

Każdy z tych flagów to projekt który zakończyłem albo z bólem i bez pełnej zapłaty, albo którego nie wziąłem i byłem z siebie dumny. Każdy. Serio.

[SLAJD 15 — BANT]

Używam też frameworku BANT do kwalifikacji. Budget — czy mają środki. Authority — czy rozmawiasz z decydentem. Need — czy ból jest realny. Timeline — czy jest presja. Brakuje dwóch lub więcej — nie wysyłaj oferty.

---

## SEGMENT 5: PROPOZYCJA HANDLOWA (60:00 – 80:00)

### 5.1 Struktura oferty (60:00 – 68:00)

[SLAJD 16 — Struktura oferty]

Dobra. Zrobiłeś discovery. Klient jest zakwalifikowany. Czas na ofertę.

Pokażę ci najpierw co NIE działa, a potem co działa.

Zła oferta wygląda tak: "Zbudujemy workflow n8n z integracją Airtable przez REST API, wdrożymy na Docker z obsługą webhooków, implementujemy retry logic i error handling..." Klient widzi technologię. Nie kupuje technologii. Kupuje wynik.

Dobra oferta wygląda tak: "Wyeliminujemy trzy godziny dziennie pracy manualnej w dziale handlowym przez automatyczne przekazywanie leadów z formularza do CRM i powiadamianie handlowca SMS-em w ciągu trzydziestu sekund."

Klient kupuje trzy godziny swojego handlowca z powrotem. Pisz o tym.

[SLAJD 17 — 6 sekcji oferty]

Struktura dobrej oferty to sześć sekcji.

Pierwsza: "rozumiemy twój problem." Streść w kilku zdaniach co zrozumiałeś z discovery. Klient czyta to i myśli: "tak, dokładnie o to chodzi." Zaufanie rośnie.

Druga: "nasze rozwiązanie." Opisz wynik. Nie technologię.

Trzecia: "co dostarczymy." Lista deliverables z datami. Konkretna, bez niedomówień.

Czwarta: "dlaczego to się opłaca." ROI kalkulator — liczby które policzyliście razem na discovery.

Piąta: "inwestycja." Opcja A i Opcja B. Za chwilę wyjaśnię dlaczego zawsze dwie opcje.

Szósta: "następny krok." Konkretne CTA. "Odezwij się do piątku" albo "Zarezerwuj spotkanie pod tym linkiem." Nie "daj znać jeśli masz pytania."

Moje oferty mają 4 strony. Klient który potrzebuje 20-stronicowej oferty żeby podjąć decyzję — to nie jest gotowy klient.

---

### 5.2 Dwie opcje — psychologia wyboru (68:00 – 76:00)

[SLAJD 18 — Opcja A i B]

Zawsze dwie opcje. Nigdy jedna, rzadko trzy.

Dlaczego? Bo jedna opcja to decyzja "tak albo nie." Klient porównuje twoją ofertę z nicnierobieniem albo z konkurencją. Dwie opcje zmieniają pytanie na "którą?" Klient porównuje A z B — nie ciebie z kimś innym.

Jak konstruować opcje: Opcja A to podstawowy zakres który w pełni rozwiązuje problem. Opcja B to Opcja A plus rozszerzenia — zazwyczaj wsparcie po wdrożeniu, bardziej rozbudowana dokumentacja, szkolenie. Cena B jest o 30 do 40% wyższa niż A.

Ważne: Opcja B ma być logicznie lepsza dla kogoś kto myśli długoterminowo. Nie droższa dla kaprysu — naprawdę lepsza.

70% moich klientów wybiera Opcję B. Nie dlatego że jest droższa. Dlatego że kiedy porównają zakres i cenę — B jest oczywistym wyborem jeśli ktoś serio podchodzi do inwestycji.

Opcja C? Dodajesz tylko kiedy jest trzecia, wyraźnie inna propozycja wartości — na przykład "monitoring przez rok" jako osobny produkt. Nie dodawaj C żeby mieć "premium." Trzy opcje często paraliżują decyzję.

---

### 5.3 ROI i follow-up (76:00 – 80:00)

[SLAJD 19 — ROI kalkulator]

[DEMO: pokaż szablon kalkulatora ROI]

Kalkulator ROI. Zawsze rób go razem z klientem na discovery — nie wstawiaj liczb samemu. Kiedy klient sam policzy ile traci — sam uzasadnia twoją cenę.

Formuła jest prosta. Czas zaoszczędzony tygodniowo w godzinach, razy stawka godzinowa pracownika, razy 52 tygodnie. To są oszczędności roczne. Podziel wartość projektu przez oszczędności miesięczne — masz payback period.

Przykład: projekt 25 000 złotych, 5 godzin tygodniowo oszczędności, 80 złotych za godzinę pracownika. Oszczędności roczne: 20 800 złotych. Payback: nieco ponad rok. ROI po dwóch latach: 166%.

[SLAJD 20 — Follow-up]

Follow-up. Co robić kiedy klient milczy.

Dzień zero: wysyłasz ofertę i potwierdzasz telefonicznie że dotarła. Dzień trzeci: krótki kontakt — "czy dotarła oferta? Mam jedno pytanie wyjaśniające." To nie jest natrętność — to jest troska o to żeby klient miał wszystko czego potrzebuje. Dzień siódmy: wartościowy follow-up. Artykuł, case study z branży klienta, coś co da mu wartość niezależnie od decyzji. Dzień czternasty: "czy decyzja jest jeszcze otwarta czy zamknięta? Pytam bo planuje harmonogram na kolejny kwartał."

Po 14 dniach bez odpowiedzi: move on. Nie torturuj ani siebie, ani klienta.

Najlepszy follow-up jaki wysłałem to był newsletter z case study z branży klienta. Napisał do mnie sam następnego dnia. Daj wartość, nie pytaj o decyzję.

---

## SEGMENT 6: UMOWA IT (80:00 – 95:00)

### 6.1 Co musi być w umowie (80:00 – 88:00)

[SLAJD 21 — Umowa IT]

Teraz umowa. Nie jestem prawnikiem i nie będę ci mówić żebyś nie brał prawnika — powinieneś. Ale powiem ci co musi być w każdej umowie na projekt automatyzacji, żebyś miał o czym rozmawiać z prawnikiem i z klientem.

Pięć elementów bez których nie podpisujesz.

Jeden: definicja zakresu. Nie ogólny opis — lista deliverables. "Workflow n8n integrujący Pipedrive z WooCommerce, obsługujący nowe zamówienia, aktualizujący status klienta w CRM, wyzwalający email powitalny przez Mailchimp." To jest zakres. Nie "automatyzacja procesu sprzedaży."

Dwa: procedura change request. Co się dzieje kiedy klient chce czegoś poza scope? Musi być jasna procedura. Klient zgłasza zmianę pisemnie. Ty szacujesz koszt i czas w ciągu 48 godzin. Klient zatwierdza lub rezygnuje. Bez tego "a czy moglibyście jeszcze dodać jedno małe..." wysadzi twój budżet.

Trzy: kryteria akceptacji. Konkretne, mierzalne. "Workflow przetwarza zamówienie w ciągu 30 sekund od złożenia, dane klienta pojawiają się w CRM bez ręcznej interwencji, w przypadku błędu generowany jest alert na wskazany email." To są kryteria. Nie "działa poprawnie."

Miałem projekt gdzie klient po trzech miesiącach powiedział że workflow "nie spełnia wymagań." Nie mieliśmy zdefiniowanych kryteriów akceptacji. To był bardzo drogi błąd — dla obu stron.

Cztery: harmonogram płatności. Zaliczka minimum 30% przed startem prac. Milestone payment po deliverables połowy zakresu. Płatność końcowa przy protokole odbioru. Nigdy całość po zakończeniu.

Pięć: własność intelektualna. O tym za chwilę osobno.

[SLAJD 22 — IP i własność workflow]

Kwestia własności jest bardziej skomplikowana niż myślisz.

Workflow n8n jako eksport JSON: po zapłacie należy do klienta. Twoje reużywalne komponenty i snippety które napisałeś wcześniej: twoje — chyba że inaczej uzgodnione. Custom nodes które napisałeś specjalnie dla projektu: negocjowane w umowie.

Rekomendacja: klient dostaje "right to use" — prawo do używania rozwiązania. Ty zachowujesz know-how i możliwość budowania podobnych rozwiązań dla innych klientów. Klient nie może sprzedawać twojego rozwiązania dalej. To jest uczciwy podział.

---

### 6.2 RODO, DPA i SLA (88:00 – 95:00)

[SLAJD 23 — RODO i DPA]

90% projektów automatyzacji B2B dotyka danych osobowych. Nie ignoruj RODO.

Kiedy musisz podpisać Data Processing Agreement? Kiedy twój workflow przetwarza dane klientów klienta — na przykład integracja CRM z email marketingiem. Kiedy pobierasz dane z systemów HR. Kiedy integrujesz formularze z danymi osób fizycznych.

DPA musi zawierać cel przetwarzania danych, kategorie danych i podmiotów, czas przetwarzania, środki bezpieczeństwa i listę sub-procesorów — na przykład OpenAI, n8n cloud, AWS jeśli tam hostujesz.

Podpisanie DPA to 30 minut pracy prawnej. Brak DPA to potencjalna odpowiedzialność z RODO i AI Act.

[SLAJD 24 — SLA]

SLA — Service Level Agreement. Co obiecywać po wdrożeniu.

Czas reakcji na zgłoszenie: 24 do 48 godzin w dni robocze. Nie 2 godziny — chyba że masz monitoring i dedykowany dyżur. Dostępność workflow: 99% — ale tylko w zakresie tego co kontrolujesz. Nie obiecuj 99.9% na infrastrukturze klienta. Czas naprawy krytycznego błędu: 24 do 72 godziny.

I kluczowe: zakres SLA obejmuje tylko błędy w kodzie który napisałeś. Problemy z zewnętrznymi API — Shopify, OpenAI, cokolwiek — nie są twoją odpowiedzialnością. Musi to być w umowie czarno na białym.

Mam klienta który dzwonił o 22:00 bo workflow "nie działał." Okazało się że API Shopify miało przerwę serwisową. To nie był mój błąd — ale bez jasnego SLA byłem traktowany jak winny. Teraz mam to w każdej umowie.

---

## SEGMENT 7: DOKUMENTACJA I HANDOVER (95:00 – 110:00)

### 7.1 Deliverables — co dostarczasz klientowi (95:00 – 100:00)

[SLAJD 25 — Deliverables]

Co dostarczasz klientowi na końcu projektu? Mam standardową listę — i ty powinieneś mieć swoją.

Obowiązkowe elementy to: workflow n8n jako eksport JSON z instrukcją importu. Dokumentacja techniczna — architektura, diagram flow, opis node po nodzie. Dokumentacja użytkowa — co robi workflow, jak go uruchomić, jak zatrzymać, co zrobić w razie problemu. Lista credentials i instrukcja rotacji kluczy API. Protokół testów — co testowałeś i jakie były wyniki. Protokół odbioru — podpisany przez obie strony.

To są elementy które są w każdym projekcie bez wyjątku.

Opcjonalnie, w wyższych pakietach: nagranie szkolenia dla użytkownika, runbook operacyjny i setup monitoringu z alertami.

Dlaczego dokumentacja to inwestycja, nie koszt? Bo każda godzina spędzona na dokumentacji to pięć telefonów mniej w ciągu roku. I to jest baza do sprzedania retainera — pokazujesz klientowi że zależy ci na tym żeby ich system działał długoterminowo.

---

### 7.2 Jak pisać dokumentację dla n8n (100:00 – 105:00)

[SLAJD 26 — Dokumentacja n8n]

[DEMO: pokaż przykład dokumentu technicznego]

Struktura dokumentu technicznego — pokażę wam przykład z prawdziwego projektu (zanonimizowany).

Sekcja pierwsza: overview. Jeden akapit. Co robi workflow, co go triggeruje, co jest outputem.

Sekcja druga: prerequisites. Jakie konta, klucze API, uprawnienia są potrzebne. Ten rozdział chroni cię przed "ale jak my mamy to uruchomić na nowym serwerze?"

Sekcja trzecia: diagram flow. Screenshot workflow w n8n albo diagram Mermaid. Klient widzi całość na jednym obrazku.

Sekcja czwarta: node po nodzie. Dla każdego kluczowego node: co robi, jak jest skonfigurowany, na co uważać. Nie musisz opisywać trywialnych nodeów — Set, Function z jedną linią — ale wszystkie integracje, logika decyzyjna, obsługa błędów — opisane.

Sekcja piąta: error handling. Co się dzieje kiedy coś idzie nie tak. Gdzie są alerty, jak wyglądają, co zrobić.

Sekcja szósta: troubleshooting. Pięć najczęstszych problemów i jak je rozwiązać. To jest gold dla klienta — zmniejsza liczność ticketów o 80%.

Sekcja siódma: maintenance. Co sprawdzać regularnie, jak rotować credentials.

Dobra dokumentacja to 2 do 3 godzin pracy. Zła dokumentacja to 10 telefonów od klienta w ciągu roku. Matematyka jest prosta.

---

### 7.3 Training i protokół odbioru (105:00 – 110:00)

[SLAJD 27 — Training klienta]

Szkolenie klienta: 2 do 4 godzin.

Co pokazujesz: gdzie jest workflow w n8n, jak go uruchomić manualnie jeśli trzeba, jak sprawdzić logi i executions, co robić kiedy coś "nie działa" (pierwsze kroki diagnostyki), jak się ze mną skontaktować i kiedy — bo "workflow nie działa" o 22:00 w sobotę to nie emergency jeśli SLA mówi 48h w dni robocze.

Czego NIE pokazujesz: jak modyfikować workflow — chyba że to retainer z development tier. Wewnętrzna architektura — niepotrzebna złożoność.

I najważniejsza rada: nagrywaj szkolenia. Zawsze. Klient obejrzy to pięć razy w ciągu roku zamiast dzwonić do ciebie.

[SLAJD 28 — Protokół odbioru]

[DEMO: pokaż szablon protokołu odbioru]

Protokół odbioru to dokument który formalnie zamyka projekt. I otwiera ostatnią płatność.

Zawiera nazwę projektu i stron, listę deliverables z potwierdzeniem dostarczenia, wyniki testów akceptacyjnych, uwagi klienta jeśli są, i podpisy obu stron z datą.

Kiedy klient podpisze protokół odbioru — projekt jest zamknięty. Klient nie może pół roku później powiedzieć że projekt "nie był skończony." To jest twoja tarcza.

Praktyczna rada: nigdy nie wysyłaj faktury końcowej bez podpisanego protokołu odbioru. Nigdy.

---

## SEGMENT 8: MODEL RETAINEROWY (110:00 – 120:00)

### 8.1 Jak sprzedać retainera (110:00 – 115:00)

[SLAJD 29 — Retainer]

Teraz czas na pasywny przychód. Retainer.

Powiem ci najpierw dlaczego klient powinien chcieć retainer — bo to jest podstawa. Jeśli sam w to nie wierzysz, nie sprzedasz.

Bez retainera: API zewnętrzne zmienia strukturę i workflow przestaje działać. Platforma SaaS aktualizuje się i endpoint znika. Klient chce nową integrację i musi startować od zera z wyceną. Rotacja pracowników — nowa osoba nie wie jak obsługiwać workflow. Problem produkcyjny — klient nie ma priorytetowego dostępu do ciebie.

Z retainerem: masz kogoś kto śledzi zmiany, reaguje szybko, zna system od środka, i ma roadmapę automatyzacji.

Sprzedaż retainera to nie jest wciskanie klientowi kolejnego kosztu. To jest dawanie mu peace of mind i ciągłości.

[SLAJD 30 — Kiedy sprzedawać retainera]

Moment sprzedaży: tuż przed zakończeniem projektu. Nie po. Nie przy pierwszym spotkaniu.

Dlaczego przed handoverem: klient jest emocjonalnie zaangażowany — projekt idzie dobrze, widzi działający system, jest "w trybie inwestycji." Po zamknięciu projektu dostaniesz "dziękujemy, wrócimy jak będziemy potrzebować." I nie wrócą przez rok.

Jak to powiedzieć: "Zanim zamkniemy projekt, chcę porozmawiać o tym co się dzieje po wdrożeniu. Mam klientów którzy biorą retainer i klientów którzy nie biorą — mogę opowiedzieć różnicę."

To zdanie działa dlatego że nie sprzedajesz — informujesz. Klient pyta o różnicę i sam sobie sprzedaje retainera.

---

### 8.2 Struktura i pricing retainera (115:00 – 120:00)

[SLAJD 31 — Trzy tiery retainera]

Mam trzy poziomy.

Tier A to Monitoring — sprawdzam że workflow działa, reaguję na alerty. SLA 48 godzin. Bez aktywnych zmian.

Tier B to Wsparcie — monitoring plus naprawa błędów do dwóch godzin, aktualizacje po zmianach API, quarterly review stanu systemu. SLA 24 godziny.

Tier C to Rozwój — wszystko z B plus pula godzin miesięcznie na nowe workflow i integracje. SLA 8 godzin. Factycznie outsourcing automatyzacji na stałe.

Większość klientów trafia na Tier B. Tier C to firmy które chcą budować automation roadmap na stałe — idealny klient.

[SLAJD 32 — Pricing retainerów]

Formuła cenowa jest prosta.

Retainer miesięczny to 2 do 3% wartości projektu. Retainer roczny to 15 do 30%.

Przykład: projekt 20 000 złotych. Retainer Tier A: 400 do 600 złotych miesięcznie. Tier B: 800 do 1 200 złotych miesięcznie.

Projekt 50 000 złotych: Tier A 1 000 do 1 500, Tier B 2 000 do 3 000 złotych miesięcznie.

Dlaczego ta formuła: klient widzi że retainer jest proporcjonalny do inwestycji. Nie czuje się że to jest oderwana liczba — ona ma logikę. Ty masz przewidywalny przychód który rośnie z każdym projektem.

[SLAJD 33 — Model biznesowy]

Policzymy razem. 10 klientów na Tier B retainerze przy średnim projekcie 30 000 złotych to 10 razy 900 złotych miesięcznie. To jest 9 000 złotych pasywnie. Pół etatu bez nowych projektów.

Kiedy to zrozumiałem — przestałem panikować przy braku nowych leadów. Retainery to fundament. Projekty to wzrost.

---

## SEGMENT 9: PODSUMOWANIE I WEZWANIE DO DZIAŁANIA (120:00 – 125:00)

[SLAJD 35 — Następny krok]

Dobra. Dwie godziny za nami.

Podsumujmy sześć kroków do profesjonalnego projektu automatyzacji.

Jeden: Discovery Call — 45 minut, 10 pytań, kwalifikacja BANT. Dwa: wycena w odpowiednim modelu z WBS i buforem minimum 30%. Trzy: oferta dwuopcyjna z ROI i konkretnym CTA. Cztery: umowa z zakresem, change request, kryteriami akceptacji i IP. Pięć: delivery z dokumentacją, szkoleniem i protokołem odbioru. Sześć: retainer sprzedany przed handoverem.

Teraz zadanie domowe. Przeprowadź mock Discovery Call z kimś ze społeczności kursu. Jeden gra klienta — wymyśl firmę e-commerce albo produkcyjną. Drugi gra konsultanta. 30 minut. Użyj listy 10 pytań.

Po callu zamieńcie się rolami. Zobaczysz jak inaczej brzmi twój własny proces kiedy sam siedzisz po drugiej stronie.

Szablony do pobrania znajdziesz w materiałach modułu: szablon wyceny, szablon propozycji handlowej, lista 10 pytań do wydrukowania, checklist handover projektu i kalkulator retainera.

Na koniec chcę powiedzieć jedną rzecz. Przez te dwie godziny dałem ci narzędzia, frameworki, szablony. Ale żaden z nich nie zadziała dopóki nie zadzwonisz do pierwszego klienta.

Teraz masz narzędzia. Jedyne co zostało — zadzwonić do pierwszego klienta.

Powodzenia. I daj znać w społeczności jak poszedł twój pierwszy Discovery Call z tą metodologią. Czytam każdy komentarz.

---

## NOTATKI PRODUKCYJNE

| Element | Rekomendacja |
|---|---|
| Tempo mówienia | Wolniejsze niż normalnie — techniczne treści, daj czas na zapamiętanie |
| Pauzy | Przed każdym "zapiszcie sobie..." — 2 sekundy ciszy |
| Demo segmenty | Miej otwarte: szablon WBS, kalkulator ROI, protokół odbioru, dokument techniczny |
| Ton | Szczery, bez korporacyjnego bullshitu — mówisz z własnego doświadczenia |
| Case studies | Opowiadaj spokojnie, bez samodramatyzowania — błędy to lekcje, nie wstyd |
| Lista 10 pytań | Wydrukuj jako rekwizyt wizualny — trzymaj w rękach kiedy omawiasz |
| Segmenty demo | Zatrzymaj nagranie, przejdź na screen share, wróć do kamery po demo |
| CTA w trakcie | "Zatrzymaj i odpowiedz na to pytanie sam sobie..." — używaj 2-3 razy (segment 2, 3 i 4) |
| Długość | ~125 minut — zostaw margines na naturalne rozwinięcia w nagraniu |
