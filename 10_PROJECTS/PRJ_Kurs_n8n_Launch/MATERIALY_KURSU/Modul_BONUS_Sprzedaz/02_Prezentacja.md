---
type: course-presentation
module: BONUS_B
title: "Sprzedaż i Delivery Projektów Automatyzacji"
slides: 35
status: draft
last_reviewed: 2026-03-27
---

# Prezentacja — Moduł BONUS B: Sprzedaż i Delivery
## 35 slajdów

---

## Slajd 1: Tytuł modułu

**MODUŁ BONUS B**
# Sprzedaż i Delivery Projektów Automatyzacji

*Jak brać za automatyzacje tyle, ile są warte — i dostarczać je bez bólu*

> 🎙️ NOTATKA: Powitanie. "Gratulacje — jesteś w miejscu, gdzie większość kursów n8n się kończy. My dopiero zaczynamy to, co decyduje czy zarobisz pieniądze."

---

## Slajd 2: Problem, który rozwiązujemy

**Dlaczego świetni technicznie eksperci n8n zarabiają 8 000 PLN/miesiąc?**

- Nie umieją wycenić swojej pracy
- Biorą każdego klienta (nawet złego)
- Oddają projekt bez umowy
- Nie mają retainerów

**Wynik: projekt goni projekt, zero pasywnego przychodu**

> 🎙️ NOTATKA: "Znam kogoś (siebie z 2019 roku) kto przez 3 miesiące budował system za 5 000 PLN który był wart 40 000. Nie ze złośliwości klienta — bo nie umiałem tego wycenić."

---

## Slajd 3: Co zmieni się po tym module

**Po tych 2 godzinach będziesz umiał:**

- Wycenić projekt automatyzacji w 3 modelach
- Przeprowadzić Discovery Call jak doradca, nie technik
- Napisać ofertę która sprzedaje (nie lista technologii)
- Podpisać umowę która cię chroni
- Przekonać klienta do retainera

**Bonus: szablony do pobrania — wszystko gotowe do użycia jutro**

> 🎙️ NOTATKA: Krótkie, konkretne. Pokaż folder z szablonami — zbuduj anticipation.

---

## Slajd 4: Trzy modele wyceny

**Jak wyceniasz projekty automatyzacji?**

| Model | Kiedy | Ryzyko |
|---|---|---|
| **T&M** (czas + materiały) | Niejasny scope, R&D | Klient nie wie ile zapłaci |
| **Fixed Price** | Jasny scope, powtarzalne projekty | Scope creep zjada marżę |
| **Value-Based** | Znasz wartość biznesową | Wymaga dobrego discovery |

> 🎙️ NOTATKA: "T&M brzmi bezpiecznie dla ciebie — ale klienci tego nie lubią. Fixed price jest wygodny dla klienta — ale niebezpieczny dla ciebie. Value-based jest najtrudniejszy do sprzedania, ale najbardziej opłacalny."

---

## Slajd 5: T&M — kiedy tak, kiedy nie

**Time & Materials — dla projektów badawczych**

TAK gdy:
- Proof of concept / MVP automatyzacji
- Integracja z systemem legacy (nieznana głębokość)
- Klient chce płacić za iteracje

NIE gdy:
- Klient pyta "a ile to zajmie łącznie?"
- Projekt ma jasne wymagania
- Klient budżetuje z góry

**Zabezpieczenie T&M: tygodniowy raport godzin + cap budżetowy**

> 🎙️ NOTATKA: Pokaż przykład raportu godzinowego — prostego, w Notion lub arkuszu.

---

## Slajd 6: Fixed Price — jak się nie naciąć

**Fixed Price bez protekcji = prezent dla klienta**

**Musisz zdefiniować z góry:**
- Dokładne deliverables (lista, nie opis)
- Liczba rund poprawek (max 2)
- Co jest "poza scope" (procedura change request)
- Środowisko testowe vs produkcyjne

**Złota zasada: jeśli nie możesz tego napisać na liście — nie wyceniaj fixed**

> 🎙️ NOTATKA: "Kiedyś wziąłem fixed price projekt 'integracji CRM z systemem wysyłkowym'. Okazało się że system wysyłkowy ma API z 2012 roku, bez dokumentacji, z podstawową autoryzacją. +40 godzin ekstra, za które nikt nie zapłacił."

---

## Slajd 7: Value-Based Pricing — jak rozmawiać o pieniądzach

**Value-Based: sprzedajesz wynik, nie godziny**

**Formuła:**
```
Wartość dla klienta = oszczędność czasu × koszt godziny pracownika
                   + eliminacja błędów × koszt błędu
                   + przyspieszenie procesu × wartość szybszego wyniku
```

**Przykład:**
- Klient: 5 pracowników × 3h/dzień wprowadzania danych = 75h/tydzień
- Koszt: 75h × 60 PLN = 4 500 PLN/tydzień = **234 000 PLN/rok**
- Twój workflow: 20 000 PLN → ROI w 5 tygodni

> 🎙️ NOTATKA: "Kiedy klient widzi 234 000 PLN rocznie po lewej i 20 000 PLN po prawej — nie ma o czym rozmawiać. Problem polega na tym, że musisz to policzyć razem z klientem na discovery."

---

## Slajd 8: Kalkulator wyceny — Breakdown Tasks

**Jak szacować projekt? Rozbij na zadania.**

| Kategoria | Przykładowe zadania | Typowy czas |
|---|---|---|
| **Discovery & analiza** | Mapping procesów, wywiady | 4–8h |
| **Projektowanie** | Diagram flow, architektura | 2–6h |
| **Konfiguracja środowiska** | Docker, credentials, VPN | 1–4h |
| **Budowa workflow** | Każdy nietrywialny node | 1–3h |
| **Integracja API** | Jedna integracja | 2–6h |
| **Obsługa błędów** | Error handling, retry logic | +25% do budowy |
| **Testy** | Happy path + edge cases | +20% do budowy |
| **Dokumentacja** | Techniczna + użytkowa | +10% całości |
| **Handover & training** | Sesja z klientem | 2–4h |
| **Bufor niespodzianek** | Zawsze | **+30%** |

**Suma × stawka godzinowa = cena bazowa**

> 🎙️ NOTATKA: "Najczęstszy błąd: ludzie liczą tylko czas budowy i zapominają o wszystkim wokół. Discovery, dokumentacja, testy, setup środowiska — to często 50% projektu."

---

## Slajd 9: Przykładowe wyceny — 3 typy projektów

**Co ile kosztuje w realu?**

| Typ projektu | Zakres | Szacunek godzin | Cena PLN |
|---|---|---|---|
| **Prosty workflow** | Powiadomienia, sync danych, 1-2 integracje | 20–40h | 8 000–15 000 |
| **Złożony agent** | Multi-step, AI, decyzje, 4+ systemy | 80–180h | 30 000–80 000 |
| **System RAG** | Baza wiedzy, embeddingi, UI, maintenance | 50–120h | 20 000–50 000 |

*Założenie: stawka 250–450 PLN/h zależnie od złożoności i klienta*

> 🎙️ NOTATKA: "To są liczby z prawdziwych projektów, zanonimizowane. Proszę żebyś nie traktował dolnych widełek jako normy — to jest absolutne minimum dla klienta który jest super zorganizowany i ma czas. Większość projektów ląduje bliżej górnej granicy."

---

## Slajd 10: Bufor 30% — dlaczego to za mało

**Co zjada twój bufor:**

- API które nie działają jak w dokumentacji (zawsze)
- Klient który "miał coś powiedzieć wcześniej"
- Środowisko produkcyjne różni się od testowego
- "Czy możecie dodać jeszcze jedno małe..."
- Rotacja po stronie klienta (nowy koordynator)
- Urlopy, choroby, opóźnienia w dostarczeniu dostępów

**Realna zasada: 30% to minimum. Dla nowych klientów — 40–50%.**

> 🎙️ NOTATKA: Śmiech jest OK. "Tak, mówię poważnie. Mój bufor na nowych klientach to 50%. I nadal czasem ledwo wychodzę."

---

## Slajd 11: Discovery Call — po co to w ogóle

**Discovery Call to NIE jest zbieranie wymagań technicznych**

**Discovery Call to:**
- Zrozumienie bólu biznesowego
- Kwalifikacja: czy to dobry klient dla ciebie
- Zbudowanie zaufania
- Zebranie danych do value-based pricing

**Efekt dobrego discovery:**
- Wiesz co zbudować
- Wiesz ile to warte
- Wiesz czy chcesz z tym klientem pracować

> 🎙️ NOTATKA: "Większość konsultantów idzie na discovery żeby zbierać wymagania techniczne. To błąd. Idziesz żeby zrozumieć — po co to tak naprawdę?"

---

## Slajd 12: 10 pytań na Discovery Call (gotowe do wydruku)

**10 pytań które MUSISZ zadać:**

1. **Jaki konkretny problem chcecie rozwiązać?** *(nie: co chcecie zautomatyzować)*
2. **Co się dzieje jeśli ten problem nie zostanie rozwiązany?** *(skala bólu)*
3. **Jak ten proces wygląda dziś, krok po kroku?** *(mapping procesów)*
4. **Ile osób jest w to zaangażowanych i ile czasu poświęcają?** *(kalkulacja ROI)*
5. **Czy próbowaliście już to rozwiązać? Co nie zadziałało?** *(oczekiwania i historia)*
6. **Kto podjął decyzję o szukaniu rozwiązania i kto zatwierdza budżet?** *(authority)*
7. **Jaki macie budżet na ten projekt?** *(budget — zapytaj wprost)*
8. **Do kiedy chcecie to uruchomić i dlaczego właśnie ta data?** *(timeline + priorytet)*
9. **Jak wygląda wasza infrastruktura techniczna? Jakie systemy używacie?** *(complexity)*
10. **Co jest dla was definicją sukcesu tego projektu?** *(kryteria akceptacji)*

> 🎙️ NOTATKA: "Wydrukuj to i połóż przed sobą na każdym discovery callu. Pytanie 7 jest najtrudniejsze — większość ludzi je pomija. Nie pomijaj."

---

## Slajd 13: Pytanie #7 — jak rozmawiać o budżecie

**"Jaki macie budżet?" — dlaczego to kluczowe**

**Jeśli klient nie poda budżetu:**
> "Żeby zaproponować właściwe rozwiązanie, muszę wiedzieć z jakimi możliwościami pracuję. Czy mówimy o budżecie poniżej 10 000, między 10 a 50 tys., czy powyżej?"

**Jeśli budżet jest za mały:**
> "To co opisujesz wymaga X zł. Możemy omówić co wchodzi w mniejszy zakres, ale nie chcę obiecywać czegoś czego nie dostarczę."

**Dlaczego nie warto ukrywać cen:**
- Oszczędza czas obu stron
- Buduje wiarygodność
- Eliminuje złych klientów wcześnie

> 🎙️ NOTATKA: "Pytanie o budżet to nie jest bezczelność. To jest szacunek dla czasu klienta i twojego. Nauczyłem się tego po tym jak spędziłem 6 godzin na discovery dla klienta który miał budżet 3 000 PLN."

---

## Slajd 14: Red Flags — kiedy powiedzieć NIE

**7 sygnałów że ten projekt/klient będzie koszmarem:**

🚩 **"Zrób to szybko, potem rozliczymy"** — brak formalności to brak płatności

🚩 **Brak osoby decyzyjnej w rozmowie** — sprzedajesz komuś kto i tak nie zatwierdzi

🚩 **"To proste, to zajmie wam godzinę"** — klient nie rozumie zakresu pracy

🚩 **Poprzedni dostawca "zawiódł ich"** — możliwe że problem leży gdzie indziej

🚩 **Nie mają zdefiniowanego procesu** — automatyzujesz chaos (to nie działa)

🚩 **Negocjują cenę zanim zobaczyli ofertę** — będą negocjować na każdym etapie

🚩 **"Chcemy wszystko zrobić sami, tylko powiedzcie jak"** — nie potrzebują wykonawcy

> 🎙️ NOTATKA: "Każdy z tych flagów to projekt który zakończyłem albo z bólem i bez pełnej zapłaty, albo którego nie wziąłem i byłem z siebie dumny. Każdy."

---

## Slajd 15: BANT dla Automatyzacji

**Kwalifikacja leadu — 4 kryteria**

| Kryterium | Pytanie | Minimum |
|---|---|---|
| **Budget** | Czy mają środki na projekt? | Zadeklarowany lub widoczny |
| **Authority** | Czy rozmawiasz z decydentem? | Dostęp do osoby zatwierdzającej |
| **Need** | Czy ból jest realny i bolesny? | Problem kosztuje ich czas/pieniądze |
| **Timeline** | Czy jest presja czasowa? | Chcą wdrożyć w ciągu 3–6 miesięcy |

**Brakuje 2+ kryteriów? Nie wysyłaj oferty.**

> 🎙️ NOTATKA: "BANT to narzędzie ze sprzedaży enterprise — ale działa idealnie dla projektów automatyzacji. Jeśli klient nie ma budżetu, nie jest decydentem, nie ma realnego bólu albo 'może kiedyś' — to nie jest lead, to jest rozmowa."

---

## Slajd 16: Struktura oferty która sprzedaje

**Błąd który popełniają wszyscy:**

❌ Zła struktura:
> "Zbudujemy workflow n8n z integracją Airtable przez REST API, wdrożymy na Docker z obsługą webhooków..."

✅ Dobra struktura:
> "Wyeliminujemy 3 godziny dziennie pracy manualnej w dziale handlowym przez automatyczne przekazywanie leadów z formularza do CRM i powiadamianie handlowca SMS-em w ciągu 30 sekund."

**Zasada: najpierw wynik, potem jak to osiągniemy**

> 🎙️ NOTATKA: "Klient nie kupuje n8n. Klient kupuje 3 godziny dziennie swojego handlowca z powrotem. Pisz o tym."

---

## Slajd 17: Struktura oferty — 6 sekcji

**Oferta handlowa krok po kroku:**

1. **Rozumiemy twój problem** *(pokaż że słuchałeś na discovery)*
2. **Nasze rozwiązanie** *(wynik, nie technologia)*
3. **Co dostarczymy** *(deliverables: lista, daty, formaty)*
4. **Dlaczego to się opłaca** *(ROI kalkulator)*
5. **Inwestycja** *(Opcja A i B z cenami)*
6. **Następny krok** *(konkretne CTA: "Odezwij się do piątku")*

**Max 4–6 stron. Więcej = klient nie przeczyta.**

> 🎙️ NOTATKA: "Moje oferty mają 4 strony. Klient który potrzebuje 20-stronicowej oferty żeby podjąć decyzję — to nie jest gotowy klient."

---

## Slajd 18: Opcja A i B — psychologia wyboru

**Zawsze dwie opcje — nigdy jedna, rzadko trzy**

| | Opcja A | Opcja B |
|---|---|---|
| **Scope** | Podstawowy zakres | Rozszerzony zakres |
| **Wsparcie po** | Brak lub 30 dni | 6 miesięcy retainer |
| **Dokumentacja** | Standardowa | Rozszerzona + szkolenie |
| **Cena** | Np. 20 000 PLN | Np. 28 000 PLN |

**Dlaczego to działa:**
- Klient porównuje A z B, nie twoją ofertę z konkurencją
- B jest zazwyczaj lepszą inwestycją — klient to widzi
- Jeśli nie ma budżetu na B, ma "wyjście" przez A

> 🎙️ NOTATKA: "70% moich klientów wybiera Opcję B. Nie dlatego że jest droższa — dlatego że jest logicznie lepsza. Budujesz Opcję A jako bazę, ale tak żeby B była oczywistym wyborem dla kogoś kto myśli długoterminowo."

---

## Slajd 19: ROI — jak to liczyć z klientem

**Kalkulator ROI dla projektu automatyzacji:**

```
OSZCZĘDNOŚCI ROCZNE =
  (Czas zaoszczędzony tygodniowo w godzinach)
  × (Stawka godzinowa pracownika)
  × 52 tygodnie

DODATKOWE KORZYŚCI =
  Eliminacja błędów × koszt błędu
  + Szybszy czas reakcji × wartość szybszości
  + Skalowalność bez nowych etatów

ROI = (Oszczędności roczne / Koszt projektu) × 100%
Payback period = Koszt projektu / Oszczędności miesięczne
```

**Przykład: 25 000 PLN projekt, 5h/tydz oszczędności, 80 PLN/h pracownik**
→ Oszczędności roczne: 5 × 80 × 52 = 20 800 PLN
→ Payback: ~14,5 miesiąca

> 🎙️ NOTATKA: "Zawsze rób kalkulator ROI razem z klientem na discovery — nie wstawiaj liczb samemu. Kiedy klient sam policzy ile traci — sam uzasadnia ci cenę projektu."

---

## Slajd 20: Follow-up — strategia bez natrętności

**Co zrobić gdy klient nie odpowiada:**

| Dzień | Akcja |
|---|---|
| Dzień 0 | Wysłanie oferty + potwierdzenie telefoniczne |
| Dzień 3 | "Czy dotarła oferta? Mam pytanie wyjaśniające..." |
| Dzień 7 | Wartościowy follow-up: artykuł, case study branżowy |
| Dzień 14 | Ostatni kontakt: "Decyzja jeszcze otwarta czy zamknięta?" |

**Po 14 dniach bez odpowiedzi: move on**

**Co NIE działa:** "Tylko sprawdzam czy już zdecydowali..."

> 🎙️ NOTATKA: "Najlepszy follow-up jaki wysłałem to był newsletter z case study z branży klienta. Napisał do mnie sam następnego dnia. Daj wartość, nie pytaj o decyzję."

---

## Slajd 21: Umowa IT — co MUSI być

**5 klauzul bez których nie podpisuj umowy:**

1. **Definicja zakresu** (scope) — lista deliverables, nie opis ogólny
2. **Procedura change request** — co się dzieje gdy klient chce czegoś spoza scope
3. **Kryteria akceptacji** — konkretne, mierzalne (nie "działa poprawnie")
4. **Harmonogram płatności** — zaliczka min. 30%, milestone, płatność końcowa
5. **Własność intelektualna** — kto jest właścicielem workflow po oddaniu

> 🎙️ NOTATKA: "Miałem projekt gdzie klient po 3 miesiącach powiedział że workflow 'nie spełnia wymagań'. Nie mieliśmy zdefiniowanych kryteriów akceptacji. To był bardzo drogi błąd — i dla mnie, i dla klienta."

---

## Slajd 22: IP — kto jest właścicielem workflow?

**Kwestia własności jest bardziej skomplikowana niż myślisz:**

| Komponent | Domyślnie należy do |
|---|---|
| Workflow n8n (eksport JSON) | Klient (zamówił i zapłacił) |
| Twoje reużywalne komponenty/snippety | Ty (chyba że inaczej uzgodnione) |
| Integracje z API zewnętrznymi | API provider (licencja) |
| Modele AI (OpenAI, Anthropic) | Provider (warunki użytkowania) |
| Custom nodes które napisałeś | Negocjowane w umowie |

**Rekomendacja: licencja "right to use" dla klienta, ty zachowujesz know-how**

> 🎙️ NOTATKA: "Kluczowe: możesz budować podobne rozwiązania dla innych klientów. Nie sprzedajesz unikalnej wiedzy — sprzedajesz implementację. Klient dostaje prawo do używania, nie do tego żeby sprzedawać twoje rozwiązanie dalej."

---

## Slajd 23: RODO i DPA w projektach automatyzacji

**Kiedy musisz podpisać Data Processing Agreement:**

TAK — gdy twój workflow:
- Przetwarza dane osobowe klientów klienta (np. CRM → email)
- Pobiera dane z systemów HR
- Integruje formularze z danymi osób fizycznych
- Wysyła komunikację personalną

**Co DPA musi zawierać:**
- Cel przetwarzania danych
- Kategorie danych i podmiotów
- Czas przetwarzania
- Środki bezpieczeństwa
- Sub-procesorzy (np. OpenAI, n8n cloud)

> 🎙️ NOTATKA: "90% projektów automatyzacji B2B dotyka danych osobowych. Nie ignoruj tego — podpisanie DPA to 30 minut pracy prawnej, brak DPA to potencjalna odpowiedzialność z AI Act i RODO."

---

## Slajd 24: SLA po wdrożeniu — realny vs marketingowy

**SLA (Service Level Agreement) — co obiecywać, a czego nie:**

| Parametr | Bezpieczne | Ryzykowne |
|---|---|---|
| Czas reakcji na zgłoszenie | 24–48h w dni robocze | 2h (tylko jeśli masz monitoring) |
| Dostępność workflow | 99% (zależy od infrastruktury klienta) | 99.9% |
| Czas naprawy krytycznego błędu | 24–72h | "ASAP" (bez definicji) |
| Zakres SLA | Błędy w kodzie który napisałeś | Problemy z zewnętrznymi API |

**Złota zasada: SLA bez monitoringu to puste obietnice**

> 🎙️ NOTATKA: "Mam klienta który dzwoni o 22:00 bo workflow 'nie działa'. Okazało się że API Shopify miało przerwę. To nie mój błąd — ale bez jasnego SLA byłem traktowany jak winny. Teraz mam to w każdej umowie."

---

## Slajd 25: Deliverables — kompletna lista

**Co dostarczasz klientowi po projekcie:**

**Obowiązkowe:**
- [ ] Workflow n8n (eksport JSON + import guide)
- [ ] Dokumentacja techniczna (architektura, flow diagram, node-by-node)
- [ ] Dokumentacja użytkowa (co robi, jak uruchomić, jak zatrzymać)
- [ ] Lista credentials i jak je rotować
- [ ] Protokół testów (co testowałeś, wyniki)
- [ ] Protokół odbioru (podpisany przez obie strony)

**Opcjonalne (w wyższych pakietach):**
- [ ] Szkolenie użytkownika (nagranie lub na żywo)
- [ ] Runbook operacyjny (co robić gdy coś nie działa)
- [ ] Monitoring setup (alerty, dashboardy)

> 🎙️ NOTATKA: "Lista checkboxów to nie formalność — to twoja ochrona. Kiedy klient podpisze protokół odbioru potwierdzając że otrzymał wszystkie deliverables, trudniej mu powiedzieć że 'projekt nie jest skończony'."

---

## Slajd 26: Dokumentacja n8n — jak pisać

**Struktura dokumentu technicznego:**

```
1. Overview (1 akapit)
   - Co robi workflow, trigger, output

2. Prerequisites
   - Wymagane konta, klucze API, uprawnienia

3. Flow Diagram
   - Wizualny diagram (screenshot lub mermaid)

4. Node-by-Node opis
   - Dla każdego kluczowego node: co robi, konfiguracja, uwagi

5. Error Handling
   - Co się dzieje gdy coś pójdzie nie tak

6. Troubleshooting
   - Top 5 problemów i jak je rozwiązać

7. Maintenance
   - Co sprawdzać regularnie, jak rotować kredencjale
```

> 🎙️ NOTATKA: "Dobra dokumentacja to 2–3 godziny pracy. Zła dokumentacja to 10 telefonów od klienta w ciągu roku. Matematyka jest prosta."

---

## Slajd 27: Training klienta — co pokazać

**Sesja szkoleniowa: 2–4 godziny**

**Co pokazać:**
- Gdzie jest workflow w n8n (gdzie szukać, jak uruchomić manualnie)
- Jak sprawdzić logi i ostatnie executions
- Co robić gdy workflow "nie działa" (pierwsze kroki diagnostyki)
- Jak mnie skontaktować (i kiedy NIE kontaktować — bo to nie mój problem)
- Gdzie jest dokumentacja

**Czego NIE pokazywać na szkoleniu:**
- Jak modyfikować workflow (chyba że retainer tech — wtedy szkolenie developerskie)
- Wewnętrzna architektura (niepotrzebna złożoność)

> 🎙️ NOTATKA: "Nagrywaj szkolenia. Zawsze. Klient obejrzy to 5 razy w ciągu roku i uniknie 5 telefonów do ciebie."

---

## Slajd 28: Protokół odbioru — format

**Protokół odbioru kończy projekt (i otwiera płatność końcową)**

```
PROTOKÓŁ ODBIORU PROJEKTU

Projekt: [nazwa]
Klient: [firma]
Wykonawca: [twoja firma]
Data: [YYYY-MM-DD]

ZAKRES PROJEKTU:
✓ Workflow n8n: [nazwa]
✓ Integracje: [lista]
✓ Dokumentacja: dostarczona [data]
✓ Szkolenie: przeprowadzone [data]

TESTY AKCEPTACYJNE:
✓ Test 1: [opis] — PASS
✓ Test 2: [opis] — PASS

UWAGI KLIENTA:
[brak / lista]

Odbieram projekt jako kompletny i spełniający wymagania.

Podpis klienta: ___________  Data: ___________
Podpis wykonawcy: _________  Data: ___________
```

> 🎙️ NOTATKA: "Ten dokument to twoja tarcza. Klient który podpisał protokół odbioru nie może 6 miesięcy później powiedzieć że projekt nie był skończony."

---

## Slajd 29: Retainer — dlaczego klient powinien chcieć

**Co się może stać bez retainera:**

- API zewnętrzne zmienia strukturę → workflow przestaje działać
- Platforma SaaS aktualizuje się → endpoint przestał istnieć
- Klient chce dodać nową integrację → musisz wyceniać od zera
- Rotacja pracowników → nowa osoba nie wie jak obsługiwać workflow
- Problem produkcyjny → klient nie ma priorytetowego dostępu do ciebie

**Z retainerem: spokój, ciągłość, optymalizacja**

> 🎙️ NOTATKA: "Sprzedaż retainera to nie jest wciskanie klientowi kolejnego kosztu. To jest dawanie im peace of mind. Jeśli nie rozumiesz dlaczego mieliby tego chcieć — nie umiesz jeszcze sprzedawać."

---

## Slajd 30: Kiedy sprzedawać retainera

**Moment sprzedaży: tuż przed zakończeniem projektu**

**Dlaczego PRZED handoverem, nie po:**
- Klient jest zaangażowany emocjonalnie (projekt idzie dobrze)
- Widzi wartość w działającym systemie
- Jest "w trybie inwestycji" (właśnie zapłacił)
- Po zamknięciu projektu: "dziękujemy, wrócimy jak będziemy potrzebować"

**Jak to powiedzieć:**
> "Zanim zamkniemy projekt, chcę porozmawiać o tym co się dzieje po wdrożeniu. Mam klientów którzy biorą retainer i klientów którzy nie biorą — mogę opowiedzieć różnicę."

> 🎙️ NOTATKA: "To zdanie działa, bo nie sprzedajesz — informujesz. Klient pyta o różnicę i sam sobie sprzedaje retainera."

---

## Slajd 31: Struktura retainera — co wchodzi

**Trzy poziomy retainera:**

| | Tier A — Monitoring | Tier B — Wsparcie | Tier C — Rozwój |
|---|---|---|---|
| Monitoring działania | ✓ | ✓ | ✓ |
| Naprawy błędów (<2h) | — | ✓ | ✓ |
| Aktualizacje po zmianach API | — | ✓ | ✓ |
| Nowe mikro-workflows | — | — | ✓ (X godzin/m-c) |
| Quarterly review | — | ✓ | ✓ |
| SLA reakcja | 48h | 24h | 8h |

> 🎙️ NOTATKA: "Tier A to pasywny przychód. Tier B to gdzie większość klientów trafia. Tier C to faktycznie outsourcing automatyzacji na stałe — idealny dla firm które chcą rozwijać automation roadmap."

---

## Slajd 32: Pricing retainerów — formuła

**Jak wycenić retainera:**

```
Retainer miesięczny = Wartość projektu × 2–3%
Retainer roczny = Wartość projektu × 15–30%
```

**Przykłady:**
- Projekt 20 000 PLN → retainer 400–600 PLN/mies. (Tier A) / 800–1 200 PLN/mies. (Tier B)
- Projekt 50 000 PLN → retainer 1 000–1 500 PLN/mies. (Tier A) / 2 000–3 000 PLN/mies. (Tier B)

**Dlaczego ta formuła:**
- Klient widzi że retainer jest "proporcjonalny" do inwestycji
- Ty masz przewidywalny przychód
- Wartość projektu to proxy złożoności systemu

> 🎙️ NOTATKA: "10 klientów na Tier B retainerze przy średnim projekcie 30k = 10 × 900 PLN/mies = 9 000 PLN pasywnie. To pół etatu bez nowych projektów. Tak budujesz firmę."

---

## Slajd 33: Pasywny przychód z portfela klientów

**Model biznesowy agencji automatyzacji z retainerami:**

```
Projekty (aktywny przychód):
  2–3 projekty/kwartał × 20–50k = 120–300k PLN/rok

Retainery (pasywny przychód):
  10 klientów × 1 500 PLN/mies = 18 000 PLN/mies = 216k PLN/rok

Suma: 336–516k PLN/rok
```

**Kluczowa zasada: każdy projekt to potencjalny retainer**

> 🎙️ NOTATKA: "Kiedy to zrozumiałem — przestałem panikować przy braku nowych projektów. Retainery to fundament, projekty to wzrost."

---

## Slajd 34: Błędy które popełniłem — top 5

**Żebyś ty ich nie popełniał:**

1. **Brak zaliczki** — klient zrezygnował po 30 godzinach pracy
2. **Brak procedury change request** — projekt urósł 3x poza scope
3. **Zbyt niskie ceny przez pierwsze 2 lata** — referencje bez pieniędzy nie płacą rachunków
4. **Projekt bez Discovery** — zbudowałem coś czego nikt nie używał
5. **Brak protokołu odbioru** — klient "nie pamiętał" że odebrał projekt

> 🎙️ NOTATKA: Spokojnie, bez samodramatyzowania. "Każdy z tych błędów kosztował mnie realnie — czas, pieniądze lub stres. Opowiadam o tym żebyś nie musiał ich powtarzać na własnym budżecie."

---

## Slajd 35: Następny krok

**Masz teraz wszystko żeby sprzedawać automatyzacje profesjonalnie**

**Do pobrania w materiałach kursu:**
- Szablon wyceny (Markdown/arkusz)
- Szablon propozycji handlowej
- Lista 10 pytań Discovery Call
- Checklist handover projektu
- Kalkulator retainera

**Zadanie domowe:**
Przeprowadź mock Discovery Call z kimś ze społeczności kursu — jeden gra klienta, drugi konsultanta. 30 minut. Użyj listy 10 pytań.

**Pytania? Wpadnij na społeczność kursu.**

> 🎙️ NOTATKA: Entuzjastyczne zamknięcie. "Daj znać w społeczności jak poszedł twój pierwszy Discovery Call z tą metodologią. Czytam każdy komentarz."
