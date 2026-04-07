# AUTOMATYZACJA PROCESÓW DLA FIRM
# UMOWA O DZIEŁO NA WYKONANIE SYSTEMU

zawarta w dniu 07.04.2026 r. w Rumi, pomiędzy:

**1) Zamawiającym**
GRAVIS GROUP BV z siedzibą w DEN HAAG, adres: PAUL VAN OSAIJENSTRAAT 6, 2548MZ DEN HAAG. NIP: NL868538711B01 REGON/KRS: 98539035 (KvK)
reprezentowanym przez: Grzegorz Gibula
zwanym dalej "Zamawiającym",

a

**2) Wykonawcą**
DOKODU SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ z siedzibą w Rumii, adres: ul. Kosynierów 76, 84-230 Rumia, wpisaną do rejestru przedsiębiorców Krajowego Rejestru Sądowego prowadzonego przez Sąd Rejonowy w Gdańsku, VIII Wydział Gospodarczy Krajowego Rejestru Sądowego, pod numerem KRS: 0000925166, posiadającą NIP: 5882473305 oraz REGON: 520149113, o kapitale zakładowym 5.000,00 zł (pięć tysięcy złotych), reprezentowaną przez:
Kacper Jan Sieradziński - Prezes Zarządu
zwanym dalej „Wykonawcą".

Zamawiający i Wykonawca zwani są dalej łącznie „Stronami", a każdy z osobna „Stroną".

---

## § 1. Definicje

Na potrzeby Umowy poniższe pojęcia mają następujące znaczenie:

1. „System" – aplikacja webowa typu SaaS do fakturowania, ewidencji i raportowania finansowego, przeznaczona dla przedsiębiorców prowadzących działalność gospodarczą w Holandii, o funkcjach opisanych w Umowie i Specyfikacji.
2. „Dzieło" – System wraz z elementami określonymi w Specyfikacji (Załącznik nr 1).
3. „Użytkownik" – osoba korzystająca z Systemu w jednej z ról: Administrator, Księgowy lub Użytkownik (przedsiębiorca), zgodnie ze Specyfikacją.
4. „Testy Wykonawcy" – testy funkcjonalne wykonywane przez Wykonawcę na danych testowych, obejmujące weryfikację zgodności Systemu ze Specyfikacją.
5. „Testy Akceptacyjne" – testy wykonywane przez Zamawiającego na środowisku udostępnionym przez Wykonawcę, na danych testowych i/lub danych rzeczywistych Zamawiającego.
6. „Komponenty Zewnętrzne" – oprogramowanie lub usługi podmiotów trzecich wykorzystywane w Systemie, w tym w szczególności: biblioteki JavaScript/React, framework Next.js, bramka płatnicza Mollie, usługa KvK API, system Exact Online, usługi email oraz inne elementy objęte odrębnymi licencjami/regulaminami.
7. „Lista Uwagi/Błędów" – jedno zbiorcze zestawienie zgłaszanych niezgodności w ramach Testów Akceptacyjnych, sporządzone jako jeden plik.

---

## § 2. Przedmiot Umowy

1. Zamawiający zamawia, a Wykonawca zobowiązuje się do wykonania Dzieła w postaci Systemu, zgodnie z Umową oraz Specyfikacją stanowiącą Załącznik nr 1.
2. System zostanie wykonany jako aplikacja webowa typu SaaS umożliwiająca:
   - wystawianie faktur, pro-form, ofert i korekt w standardzie holenderskim (BTW, numeracja NN-RRRR, kod QR EPC, eksport UBL/XML),
   - prowadzenie uproszczonej ewidencji kosztów, godzin pracy i kilometrów,
   - generowanie raportów finansowych i rozliczeń kwartalnych z eksportem kompatybilnym z Exact Online,
   - miękką windykację należności (3-stopniowa eskalacja przypomnień email),
   - integrację z systemem księgowym Zamawiającego („Magiczny Przycisk"),
   - zarządzanie użytkownikami w architekturze multi-tenant (Administrator, Księgowy, Użytkownik),
   - obsługę płatności abonamentowych przez Mollie z programem poleceń.
3. Szczegółowy opis funkcjonalności, interfejsów, raportowania i wymagań niefunkcjonalnych zawiera Załącznik nr 1.
4. Strony potwierdzają, że System będzie wytwarzany przy wykorzystaniu technologii Next.js, React, Tailwind CSS oraz mechanizmów integracji z usługami zewnętrznymi. Wykorzystanie Komponentów Zewnętrznych nie oznacza udzielenia Zamawiającemu licencji przez Wykonawcę; zasady korzystania z Komponentów Zewnętrznych mogą wynikać z licencji/regulaminów ich producentów.

---

## § 3. Środowisko, dane, formaty i ograniczenia

1. Strony potwierdzają, że Wykonawca nie uzyska dostępu do bazy danych Zamawiającego ani do środowiska produkcyjnego Zamawiającego, chyba że Strony uzgodnią inaczej na piśmie (w tym e-mail).
2. Testy Akceptacyjne przeprowadza Zamawiający na środowisku udostępnionym przez Wykonawcę. Jeżeli Zamawiający nie zgłosi uwag w terminach określonych w § 7, Strony uznają Dzieło za wykonane zgodnie z Umową.
3. Wykonawca nie odpowiada za jakość, kompletność oraz spójność danych wprowadzanych przez użytkowników Systemu (w tym danych kontrahentów, faktur, kosztów) ani za błędy wynikające z nieprawidłowego użytkowania Systemu.
4. Wykonawca nie odpowiada za działanie usług zewnętrznych, z którymi System się integruje (Mollie, KvK API, Exact Online, usługi email), w tym za ich dostępność, zmiany API lub ograniczenia nałożone przez dostawców tych usług.
5. Wsparcie dodatkowych integracji z programami księgowymi, dodatkowych języków interfejsu oraz funkcjonalności nieopisanych w Specyfikacji nie jest objęte Umową, chyba że Strony uzgodnią to jako prace dodatkowe.
6. System obsługuje wyłącznie walutę EUR (€) oraz stawki BTW obowiązujące w Holandii. Obsługa innych walut, jurysdykcji podatkowych lub systemów fiskalnych nie jest objęta Umową.
7. Zamawiający odpowiada za dostarczenie treści szablonów emailowych (przypomnienia, wezwania do zapłaty) w języku holenderskim oraz treści filmów instruktażowych. Wykonawca zapewnia infrastrukturę techniczną do ich osadzenia w Systemie.
8. Zamawiający odpowiada za bezpieczeństwo, kopie zapasowe, aktualizacje oraz prawidłową konfigurację własnego środowiska (w tym serwerów, baz danych, uprawnień i sieci), na którym uruchamiany będzie System, chyba że Strony uzgodnią inaczej.

---

## § 5. Współpraca Stron i materiały

1. Zamawiający zobowiązuje się dostarczyć Wykonawcy informacje niezbędne do realizacji Dzieła (w tym wymagania dotyczące szablonów faktur, danych testowych, konfiguracji Exact Online) w terminie 7 dni od dnia zawarcia Umowy, chyba że Strony ustalą inaczej.
2. Wszelkie uzgodnienia robocze, w tym przekazywanie materiałów, odbywa się w formie e-mail na adresy wskazane w § 15.
3. Prace wykraczające poza Specyfikację (prace dodatkowe / zmiany zakresu) wymagają aneksu lub pisemnego potwierdzenia Stron (w tym e-mail) z opisem zakresu, wpływu na termin oraz wynagrodzenie.

---

## § 5a. Obowiązki Zamawiającego

1. Zamawiający zobowiązuje się do współdziałania przy wykonaniu Umowy, w szczególności do:
   a) terminowego przekazania informacji, materiałów i danych testowych niezbędnych do realizacji Dzieła,
   b) wyznaczenia osoby kontaktowej upoważnionej do podejmowania bieżących decyzji oraz przekazywania wyjaśnień merytorycznych,
   c) przeprowadzenia Testów Akceptacyjnych w terminach określonych w Umowie,
   d) zgłaszania uwag w sposób umożliwiający ich weryfikację (zgodnie z § 7),
   e) zapewnienia środowiska produkcyjnego po swojej stronie (jeżeli wdrożenie odbywa się u Zamawiającego), w tym dostępu administracyjnego lub wsparcia IT w zakresie uruchomienia.
2. Zamawiający oświadcza, że posiada prawa/zgody do udostępnienia danych testowych oraz że dane te są zgodne z prawem, a ich przekazanie Wykonawcy nie narusza praw osób trzecich.
3. Brak współdziałania Zamawiającego, opóźnienia w dostarczeniu materiałów, brak wykonania Testów Akceptacyjnych lub nieprzekazanie informacji niezbędnych do realizacji Dzieła skutkują odpowiednim przesunięciem terminów.

---

## § 5b. Zmiany zakresu (Change Request) i „zamrożenie" Specyfikacji

1. Specyfikacja (Załącznik nr 1) obowiązuje w brzmieniu uzgodnionym na dzień zawarcia Umowy.
2. Każda zmiana zakresu, w tym w szczególności: dodawanie nowych typów dokumentów, zmiana integracji z programami księgowymi, dodanie języków interfejsu, nowe funkcjonalności płatnicze, integracja z siecią Peppol, OCR faktur zakupowych, wymaga zgłoszenia zmiany („Change Request") i akceptacji Stron w formie e-mail, wraz z określeniem wpływu na termin i wynagrodzenie.
3. Do czasu akceptacji Change Request Wykonawca realizuje Umowę zgodnie z aktualną Specyfikacją; zmiany niezaakceptowane nie stanowią wady Dzieła.

---

## § 6. Terminy i etapy

1. Wykonawca wykona Dzieło w następujących etapach:
   a) Etap 1 – implementacja i konfiguracja Systemu zgodnie ze Specyfikacją;
   b) Etap 2 – Testy Wykonawcy oraz przekazanie wersji do Testów Akceptacyjnych;
   c) Etap 3 – usunięcie zasadnie zgłoszonych niezgodności (o ile dotyczą zgodności ze Specyfikacją) i finalne przekazanie Dzieła.
2. Szczegółowy harmonogram (daty kamieni milowych) Strony określą w korespondencji e-mail. Brak przekazania materiałów przez Zamawiającego lub opóźnienia w Testach Akceptacyjnych skutkują odpowiednim przesunięciem terminów.

---

## § 7. Testy i odbiór Dzieła

1. Po zakończeniu Etapu 2 Wykonawca udostępni Zamawiającemu Dzieło do Testów Akceptacyjnych (np. poprzez środowisko testowe online) oraz przekaże instrukcje obsługi.
2. Testy Akceptacyjne trwają 14 dni roboczych od dnia udostępnienia Dzieła do testów, chyba że Zamawiający zakończy Testy Akceptacyjne wcześniej i złoży oświadczenie o odbiorze Dzieła (w tym e-mail).
3. Jeżeli w toku Testów Akceptacyjnych Zamawiający stwierdzi niezgodność Dzieła ze Specyfikacją, zgłosi je Wykonawcy w formie pisemnej (e-mail) w jednym zbiorczym zestawieniu („Lista Uwagi/Błędów"), w postaci jednego pliku (np. XLSX/DOC/PDF), zawierającego co najmniej: opis błędu, kroki odtworzenia oraz oczekiwany rezultat. Zgłoszenia rozproszone lub bez wymaganych danych nie wstrzymują biegu terminu Testów Akceptacyjnych, o ile uniemożliwiają weryfikację.
4. Wykonawca usunie zasadnie zgłoszone niezgodności w terminie 7 dni roboczych od otrzymania kompletnej „Listy Uwagi/Błędów", po czym udostępni poprawioną wersję do ponownych Testów Akceptacyjnych trwających 7 dni roboczych.
5. Niezgłoszenie uwag w terminie, o którym mowa w ust. 2, oznacza odbiór Dzieła bez zastrzeżeń (milczący odbiór).
6. Z odbioru Strony sporządzają Protokół Odbioru (Załącznik nr 2). Dopuszcza się podpisanie protokołu elektronicznie lub potwierdzenie odbioru w e-mailu.
7. Za wadę Dzieła uznaje się wyłącznie niezgodność funkcjonalności ze Specyfikacją (Załącznik nr 1). Nie stanowi wady w szczególności: niedostępność usług zewnętrznych (Mollie, KvK API, Exact Online), zmiany API po stronie dostawców zewnętrznych, ani problemy wynikające z nieprawidłowego użytkowania Systemu przez Użytkowników.
8. Kryteria odbioru: odbiór Dzieła następuje na podstawie spełnienia funkcjonalności opisanych w Umowie i Specyfikacji. System uznaje się za zgodny ze Specyfikacją, jeżeli wszystkie moduły opisane w rozdziałach 1–12 Specyfikacji działają zgodnie z opisem.
9. Jeżeli Zamawiający nie przekaże „Listy Uwagi/Błędów" w terminie określonym w ust. 2 lub nie przeprowadzi testów mimo udostępnienia Dzieła, zastosowanie ma ust. 5 (milczący odbiór).
10. Strony dopuszczają odbiór częściowy Dzieła (odbiór etapów) w zakresie funkcjonalności określonych w harmonogramie lub uzgodnionych e-mailem. Odbiór częściowy potwierdzony jest protokołem lub e-mailem.

---

## § 8. Wynagrodzenie

1. Strony ustalają ryczałtowe wynagrodzenie za wykonanie Dzieła w kwocie **15 428,28 EUR netto** (słownie: piętnaście tysięcy czterysta dwadzieścia osiem EUR 28/100) plus należny podatek VAT, o ile ma zastosowanie („Wynagrodzenie").
2. Wynagrodzenie zostanie zapłacone w następujących transzach:
   a) zaliczka: 30% Wynagrodzenia, tj. **4 628,48 EUR**, w terminie 7 dni od dnia zawarcia Umowy,
   b) pozostała część: 70% Wynagrodzenia, tj. **10 799,80 EUR**, w terminie 14 dni od dnia odbioru Dzieła (zgodnie z § 7).
3. Wynagrodzenie obejmuje przeniesienie autorskich praw majątkowych na zasadach § 10.
4. Prace dodatkowe wymagają odrębnego wynagrodzenia, zgodnie z § 5 ust. 3 i § 5b.

---

## § 9. Gwarancja

1. Wykonawca udziela Zamawiającemu gwarancji na okres 6 (sześciu) miesięcy od dnia odbioru Dzieła, ograniczonej do usuwania wad polegających na niezgodności Systemu ze Specyfikacją (Załącznik nr 1).
2. Gwarancja nie obejmuje w szczególności:
   a) zmian po stronie Zamawiającego (środowisko, konfiguracje, integracje),
   b) zmian w Komponentach Zewnętrznych (Mollie, KvK API, Exact Online, usługi email),
   c) przerw/limitów/uszkodzeń wynikających z usług podmiotów trzecich, chyba że wada wynika bezpośrednio z błędu implementacji po stronie Wykonawcy.
3. Zgłoszenia gwarancyjne Zamawiający składa e-mailem, z podaniem co najmniej: opisu błędu, kroków odtworzenia oraz zrzutów ekranu, o ile dostępne.
4. Wykonawca usuwa wady gwarancyjne w terminie nie dłuższym niż 5 dni roboczych od otrzymania kompletnego zgłoszenia, chyba że wada wymaga współdziałania Zamawiającego.
5. Za usterkę krytyczną uznaje się brak możliwości logowania do Systemu, brak możliwości wystawienia faktury lub brak możliwości eksportu danych mimo spełnienia warunków Specyfikacji. Pozostałe usterki traktowane są jako niekrytyczne.

---

## § 10. Prawa autorskie – przeniesienie (bez licencji) + ograniczenia obrotu

1. Wykonawca przenosi na Zamawiającego całość autorskich praw majątkowych do Dzieła (w tym kodu źródłowego, dokumentacji i materiałów towarzyszących), bez ograniczeń terytorialnych i czasowych, na czas trwania ochrony, na polach eksploatacji wskazanych w ust. 3, z chwilą zapłaty całego Wynagrodzenia.
2. Strony potwierdzają, że Umowa nie ustanawia licencji – następuje przeniesienie praw. Do czasu zapłaty całego Wynagrodzenia Zamawiający może korzystać z Dzieła wyłącznie w celu przeprowadzenia Testów Akceptacyjnych oraz uruchomienia produkcyjnego po odbiorze.
3. Przeniesienie praw obejmuje w szczególności następujące pola eksploatacji (dla utworów i programów komputerowych):
   a) utrwalanie i zwielokrotnianie dowolną techniką, w tym cyfrową, na wszelkich nośnikach;
   b) wprowadzanie do pamięci komputera, baz danych, środowisk chmurowych oraz sieci teleinformatycznych (Internet, intranet);
   c) publiczne udostępnianie w taki sposób, aby każdy mógł mieć dostęp w miejscu i czasie przez siebie wybranym;
   d) modyfikacja, adaptacja, tłumaczenie, łączenie z innym oprogramowaniem, tworzenie wersji pochodnych (prawa zależne) oraz zezwalanie osobom trzecim na wykonywanie praw zależnych – wyłącznie na potrzeby Zamawiającego zgodnie z ust. 12–14.
4. Wykonawca wyraża zgodę na wykonywanie przez Zamawiającego praw zależnych oraz na dokonywanie zmian bez nadzoru autorskiego Wykonawcy.
5. Wykonawca oświadcza, że Dzieło będzie wolne od wad prawnych i nie będzie naruszać praw osób trzecich.
6. Wykonawca zobowiązuje się, że nie będzie wykorzystywał, udostępniał ani zbywał Dzieła (w tym kodu, konfiguracji, UI oraz dokumentacji) na rzecz osób trzecich. Postanowienie to nie ogranicza prawa Wykonawcy do korzystania z ogólnej wiedzy, doświadczenia i know-how nabytego przy realizacji Umowy, pod warunkiem niewykorzystywania elementów identyfikowalnych Dzieła i Informacji Poufnych Zamawiającego.
7. Przeniesienie praw obejmuje w szczególności: kod źródłowy, kod wynikowy, konfiguracje, dokumentację techniczną i użytkową oraz materiały projektowe.
8. Strony potwierdzają, że przeniesienie praw autorskich nie obejmuje praw do Komponentów Zewnętrznych (w tym bibliotek, usług zewnętrznych), które pozostają na licencjach/regulaminach ich twórców; Wykonawca przenosi prawa wyłącznie do elementów wytworzonych przez niego w ramach Dzieła.
9. Wykonawca wyda Zamawiającemu kod źródłowy instalując go na serwerze klienta, po przekazaniu danych logowania, najpóźniej w dniu odbioru Dzieła lub niezwłocznie po zapłacie Wynagrodzenia (zgodnie z ust. 1).
10. Zamawiający nabywa prawo do modyfikacji, rozwoju i łączenia Dzieła z innymi systemami oraz zlecania osobom trzecim prac rozwojowych – z zastrzeżeniem ust. 12–14.
11. Strony potwierdzają, że nie dochodzi do udzielenia licencji na Dzieło – przeniesienie praw jest jedyną podstawą korzystania z Dzieła przez Zamawiającego po zapłacie Wynagrodzenia.
12. Pomimo przeniesienia praw autorskich Zamawiający zobowiązuje się wykorzystywać Dzieło wyłącznie na własne potrzeby wewnętrzne i nie jest uprawniony do odpłatnego lub nieodpłatnego zbywania, odsprzedaży, udostępniania, publikowania i rozpowszechniania Dzieła osobom trzecim, w całości ani w części, bez uprzedniej pisemnej zgody Wykonawcy.
13. Zakaz z ust. 12 obejmuje w szczególności: przekazywanie kodu źródłowego, repozytorium, konfiguracji lub dokumentacji.
14. Zamawiający może zlecać prace rozwojowe podwykonawcom wyłącznie na własną rzecz, pod warunkiem zobowiązania ich do poufności i niewykorzystywania Dzieła poza realizacją usług na rzecz Zamawiającego.
15. Naruszenie postanowień ust. 12–14 skutkuje obowiązkiem zapłaty kar umownych zgodnie z § 14a.

---

## § 11. Poufność

1. Strony zobowiązują się do zachowania w poufności wszelkich informacji technicznych, organizacyjnych i biznesowych uzyskanych w związku z wykonywaniem Umowy („Informacje Poufne").
2. Obowiązek poufności obowiązuje w czasie trwania Umowy oraz przez 3 lata po jej zakończeniu.
3. Strony mogą ujawnić Informacje Poufne wyłącznie osobom zaangażowanym w realizację Umowy, w zakresie niezbędnym, przy zapewnieniu co najmniej takiego samego poziomu ochrony.

---

## § 12. Dane i bezpieczeństwo

1. Zamawiający oświadcza, że posiada podstawy prawne do udostępnienia danych testowych. Wykonawca przetwarza dane wyłącznie w zakresie niezbędnym do realizacji Umowy.
2. System przetwarza dane wprowadzane przez Użytkowników (dane kontrahentów, faktury, koszty, godziny, kilometry). Odpowiedzialność za prawidłowość i kompletność tych danych ponoszą Użytkownicy.
3. Wykonawca nie ponosi odpowiedzialności za przerwy, limity lub zmiany po stronie dostawców usług zewnętrznych (Mollie, KvK API, Exact Online), o ile System spełnia Specyfikację.

---

## § 12a. Ochrona danych osobowych (RODO)

1. Strony ustalają, że w związku z realizacją Umowy oraz funkcjonowaniem Systemu może dojść do przetwarzania danych osobowych Użytkowników oraz ich kontrahentów.
2. Zamawiający oświadcza, że jest administratorem danych osobowych przetwarzanych w Systemie i posiada podstawę prawną do ich przetwarzania.
3. Wykonawca przetwarza dane osobowe wyłącznie w celu wykonania Umowy, w zakresie niezbędnym, z zachowaniem zasad minimalizacji.
4. Strony potwierdzają, że Wykonawca nie uzyskuje dostępu do bazy danych Zamawiającego ani do środowiska produkcyjnego, o ile Strony nie postanowią inaczej na piśmie.
5. Jeżeli dojdzie do powierzenia przetwarzania danych osobowych w rozumieniu art. 28 RODO, Strony zawrą odrębną umowę powierzenia (DPA). Do czasu zawarcia DPA Wykonawca może przetwarzać dane wyłącznie w zakresie Testów Wykonawcy na danych testowych lub danych zanonimizowanych/pseudonimizowanych przekazanych przez Zamawiającego.
6. Wykonawca stosuje odpowiednie środki techniczne i organizacyjne: kontrolę dostępu, szyfrowanie transmisji, minimalizację dostępu personelu, ograniczenie kopiowania danych oraz bezpieczne usuwanie danych po zakończeniu prac.
7. Po zakończeniu realizacji Umowy (najpóźniej w terminie 14 dni od odbioru Dzieła) Wykonawca usunie lub zwróci Zamawiającemu dane testowe oraz ich kopie, chyba że obowiązek dłuższego przechowywania wynika z przepisów prawa.

---

## § 13. Odpowiedzialność i wyłączenia

1. Wykonawca odpowiada za niewykonanie lub nienależyte wykonanie Umowy na zasadach ogólnych, z uwzględnieniem ograniczeń wynikających z § 3, § 7 ust. 7 oraz § 12.
2. System ma charakter narzędzia wspomagającego fakturowanie i ewidencję. Wykonawca nie ponosi odpowiedzialności za decyzje księgowe, podatkowe lub biznesowe podjęte na podstawie danych w Systemie, w szczególności za prawidłowość rozliczeń podatkowych Użytkowników.
3. Strony ustalają limit odpowiedzialności Wykonawcy do wysokości Wynagrodzenia, z wyłączeniem szkody wyrządzonej umyślnie.

---

## § 14a. Kary umowne

1. Kary umowne należne Wykonawcy od Zamawiającego:
   a) za naruszenie zakazu z § 10 ust. 12–13 – 10 000 PLN za każde naruszenie,
   b) za przekazanie osobom trzecim kodu/repozytorium/konfiguracji/dokumentacji bez zgody – 10 000 PLN za każde naruszenie,
   c) za opóźnienie w zapłacie przekraczające 14 dni – 0,2% Wynagrodzenia brutto za każdy dzień opóźnienia, max 10% Wynagrodzenia brutto.
2. Kary umowne należne Zamawiającemu od Wykonawcy:
   a) za zwłokę w wykonaniu Dzieła z przyczyn po stronie Wykonawcy – 0,2% Wynagrodzenia netto za każdy dzień roboczy zwłoki, max 10% Wynagrodzenia netto,
   b) za zwłokę w usunięciu wad gwarancyjnych z przyczyn po stronie Wykonawcy – 0,1% Wynagrodzenia netto za każdy dzień roboczy zwłoki, max 5% Wynagrodzenia netto.
3. Kary nie przysługują, jeżeli opóźnienie lub niewykonanie wynika z: braku współdziałania Zamawiającego, przyczyn po stronie podmiotów trzecich (dostawcy usług zewnętrznych) lub siły wyższej.
4. Zapłata kary następuje w terminie 7 dni od wezwania.
5. Strony mogą dochodzić odszkodowania uzupełniającego, jeżeli szkoda przekracza wysokość kary.

---

## § 14b. Odstąpienie od Umowy

1. Zamawiający może odstąpić od Umowy wyłącznie w przypadku rażącego naruszenia Umowy przez Wykonawcę, w szczególności gdy Wykonawca mimo pisemnego wezwania nie rozpocznie realizacji Dzieła lub przerwie pracę na okres dłuższy niż 14 dni roboczych bez uzasadnienia.
2. Wykonawca może odstąpić od Umowy ze skutkiem natychmiastowym, gdy Zamawiający:
   a) opóźnia się z zapłatą zaliczki lub części Wynagrodzenia o więcej niż 7 dni mimo wezwania, lub
   b) nie współdziała (brak danych, brak testów, brak odpowiedzi/wyjaśnień) przez ponad 14 dni roboczych mimo wezwania, lub
   c) uniemożliwia wykonanie Dzieła.
3. Odstąpienie następuje w formie pisemnej lub dokumentowej (e-mail) z podaniem przyczyny.
4. W razie odstąpienia z przyczyn leżących po stronie Zamawiającego, Zamawiający płaci za prace wykonane do dnia odstąpienia – nie mniej niż kwota zaliczki – oraz zwraca uzasadnione koszty poniesione przez Wykonawcę (w tym koszty Komponentów Zewnętrznych), o ile poniesiono je na potrzeby Umowy.
5. W razie odstąpienia z przyczyn leżących po stronie Wykonawcy, Wykonawca zwróci niewykorzystaną część zapłaconego wynagrodzenia w terminie 14 dni.
6. Brak współdziałania Zamawiającego wstrzymuje bieg terminów realizacji Dzieła oraz terminów usuwania niezgodności; terminy ulegają przedłużeniu o czas opóźnienia Zamawiającego.
7. Odstąpienie nie narusza prawa do kar umownych i odszkodowania.

---

## § 15. Postanowienia końcowe

1. Strony dopuszczają składanie oświadczeń woli i uzgodnień w formie elektronicznej (e-mail), o ile Umowa nie stanowi inaczej.
2. Dane do kontaktu:
   a) Zamawiający: ……………………………………… (e-mail) / ……………………………………… (osoba kontaktowa)
   b) Wykonawca: kacper@dokodu.it / Kacper Sieradziński
3. Zmiany Umowy wymagają formy pisemnej pod rygorem nieważności, z zastrzeżeniem postanowień dopuszczających e-mail dla uzgodnień operacyjnych.
4. W sprawach nieuregulowanych Umową zastosowanie mają przepisy Kodeksu cywilnego oraz ustawy o prawie autorskim i prawach pokrewnych.
5. Spory wynikłe z Umowy Strony będą starały się rozwiązać polubownie, a w razie braku porozumienia – przez sąd właściwy miejscowo dla siedziby Wykonawcy.
6. Załączniki stanowią integralną część Umowy:
   - Załącznik nr 1 – Specyfikacja Funkcjonalna V1.0 (opis funkcjonalności i wymagania)
   - Załącznik nr 2 – Wzór Protokołu Odbioru

---

Grzegorz Gibula

…………………………………… ……………………………………
Zamawiający                    Wykonawca

---

## ZAŁĄCZNIK NR 2 – WZÓR PROTOKOŁU ODBIORU DZIEŁA

do Umowy o Dzieło na Wykonanie Systemu z dnia 07.04.2026 r.

### 1. STRONY PROTOKOŁU

Protokół sporządzono w dniu ……………………… w …………………………… pomiędzy:

1. **Zamawiającym:**
   GRAVIS GROUP BV z siedzibą w DEN HAAG
   Reprezentowanym przez: Grzegorz Gibula

2. **Wykonawcą:**
   DOKODU SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ z siedzibą w Rumii
   Reprezentowaną przez: Kacper Jan Sieradziński - Prezes Zarządu

### 2. PRZEDMIOT ODBIORU

Przedmiotem odbioru jest Dzieło – System (aplikacja webowa typu SaaS do fakturowania, ewidencji i raportowania finansowego), wykonany zgodnie z Umową oraz Specyfikacją stanowiącą Załącznik nr 1 do Umowy.

### 3. PRZEBIEG I WYNIKI TESTÓW AKCEPTACYJNYCH

1. Wykonawca udostępnił Dzieło do Testów Akceptacyjnych (Etap 2) w dniu: ………………………
2. Testy Akceptacyjne trwały zgodnie z § 7 ust. 2 Umowy i zakończyły się w dniu: ………………………
3. Lista Uwagi/Błędów:
   - ☐ Nie stwierdzono niezgodności Dzieła ze Specyfikacją (Załącznik nr 1).
   - ☐ Stwierdzono niezgodności, które zostały zgłoszone w dniu: ……………………… i usunięte przez Wykonawcę. Poprawiona wersja udostępniona w dniu: ………………………

### 4. KRYTERIA ODBIORU

Strony potwierdzają, że Dzieło spełnia funkcjonalności określone w Umowie (§ 2) i Specyfikacji (Załącznik nr 1), w tym wszystkie moduły opisane w rozdziałach 1–12 Specyfikacji.

### 5. OŚWIADCZENIE O ODBIORZE DZIEŁA

- ☐ Zamawiający odbiera Dzieło bez zastrzeżeń.
- ☐ Zamawiający odbiera Dzieło z następującymi zastrzeżeniami:
  ………………………………………………………………………………………………

Data odbioru Dzieła: ………………………

### 6. PODPISY STRON

Zamawiający                    Wykonawca
…………………………                 …………………………

(Zgodnie z § 7 ust. 6, dopuszcza się podpisanie protokołu elektronicznie lub potwierdzenie odbioru w e-mailu.)
