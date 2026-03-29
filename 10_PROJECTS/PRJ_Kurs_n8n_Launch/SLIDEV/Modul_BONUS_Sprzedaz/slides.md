---
theme: default
titleTemplate: "%s | Dokodu"
highlighter: shiki
lineNumbers: false
drawings:
  persist: false
transition: slide-left
mdc: true
fonts:
  sans: Inter
  mono: Fira Code
css: style.css
---


---
transition: fade
layout: cover
---

<img src="/dokodu_logo.png" style="height:28px;margin-bottom:1.8rem;opacity:0.92" alt="Dokodu" />

<div class="cover-tag">MODUŁ BONUS — SPRZEDAZ</div>

# ## 35 slajdów


<p style="color:#E63946;font-weight:600">Kacper Sieradziński</p>
<p style="color:#8096AA;font-size:0.8rem;margin-top:0.2rem">dokodu.it</p>


---
---

# Problem, który rozwiązujemy

## Dlaczego świetni technicznie eksperci n8n zarabiają 8 000 PLN/miesiąc?

- Nie umieją wycenić swojej pracy
- Biorą każdego klienta (nawet złego)
- Oddają projekt bez umowy
- Nie mają retainerów

## Wynik: projekt goni projekt, zero pasywnego przychodu

<!--
"Znam kogoś (siebie z 2019 roku) kto przez 3 miesiące budował system za 5 000 PLN który był wart 40 000. Nie ze złośliwości klienta — bo nie umiałem tego wycenić."
-->


---
---

# Co zmieni się po tym module

## Po tych 2 godzinach będziesz umiał

- Wycenić projekt automatyzacji w 3 modelach
- Przeprowadzić Discovery Call jak doradca, nie technik
- Napisać ofertę która sprzedaje (nie lista technologii)
- Podpisać umowę która cię chroni
- Przekonać klienta do retainera

## Bonus: szablony do pobrania — wszystko gotowe do użycia jutro

<!--
Krótkie, konkretne. Pokaż folder z szablonami — zbuduj anticipation.
-->


---
---

# Trzy modele wyceny

## Jak wyceniasz projekty automatyzacji?

| Model | Kiedy | Ryzyko |
|---|---|---|
| **T&M** (czas + materiały) | Niejasny scope, R&D | Klient nie wie ile zapłaci |
| **Fixed Price** | Jasny scope, powtarzalne projekty | Scope creep zjada marżę |
| **Value-Based** | Znasz wartość biznesową | Wymaga dobrego discovery |

<!--
"T&M brzmi bezpiecznie dla ciebie — ale klienci tego nie lubią. Fixed price jest wygodny dla klienta — ale niebezpieczny dla ciebie. Value-based jest najtrudniejszy do sprzedania, ale najbardziej opłacalny."
-->


---
---

# T&M — kiedy tak, kiedy nie

## Time & Materials — dla projektów badawczych

TAK gdy:
- Proof of concept / MVP automatyzacji
- Integracja z systemem legacy (nieznana głębokość)
- Klient chce płacić za iteracje

NIE gdy:
- Klient pyta "a ile to zajmie łącznie?"
- Projekt ma jasne wymagania
- Klient budżetuje z góry

## Zabezpieczenie T&M: tygodniowy raport godzin + cap budżetowy

<!--
Pokaż przykład raportu godzinowego — prostego, w Notion lub arkuszu.
-->


---
---

# Fixed price — jak się nie naciąć

## Fixed Price bez protekcji = prezent dla klienta

## Musisz zdefiniować z góry
- Dokładne deliverables (lista, nie opis)
- Liczba rund poprawek (max 2)
- Co jest "poza scope" (procedura change request)
- Środowisko testowe vs produkcyjne

## Złota zasada: jeśli nie możesz tego napisać na liście — nie wyceniaj fixed

<!--
"Kiedyś wziąłem fixed price projekt 'integracji CRM z systemem wysyłkowym'. Okazało się że system wysyłkowy ma API z 2012 roku, bez dokumentacji, z podstawową autoryzacją. +40 godzin ekstra, za które nikt nie zapłacił."
-->


---
transition: fade
---

# Value-Based pricing — jak rozmawiać o pieniądzach

<N8nFlow
  :nodes="[
    {icon: 'mdi:clock-outline', label: 'Czas pracownika', desc: '5 osób × 3h/dzień', variant: 'default'},
    {icon: 'mdi:calculator', label: 'Koszt roczny', desc: '75h/tydz × 60 PLN × 52', variant: 'error'},
    {icon: 'mdi:arrow-right-bold', label: '234 000 PLN/rok', desc: 'wartość problemu', variant: 'error'},
  ]"
/>

<div style="margin-top:0.5rem;display:flex;gap:0.8rem;align-items:center;justify-content:center">
  <div style="background:#1E2D40;border-radius:8px;padding:0.6rem 1rem;border-top:2px solid #22C55E;text-align:center">
    <div style="color:#22C55E;font-weight:700;font-size:1rem">20 000 PLN</div>
    <div style="color:#8096AA;font-size:0.68rem">Twój workflow</div>
  </div>
  <div style="color:#F97316;font-size:1.2rem;font-weight:700">→</div>
  <div style="background:#1E2D40;border-radius:8px;padding:0.6rem 1rem;border-top:2px solid #F97316;text-align:center">
    <div style="color:#F97316;font-weight:700;font-size:1rem">ROI w 5 tygodni</div>
    <div style="color:#8096AA;font-size:0.68rem">klient sam uzasadnia cenę</div>
  </div>
</div>


<!--
"Kiedy klient widzi 234 000 PLN rocznie po lewej i 20 000 PLN po prawej — nie ma o czym rozmawiać. Problem polega na tym, że musisz to policzyć razem z klientem na discovery."
-->


---
---

# Kalkulator wyceny — breakdown tasks

## Jak szacować projekt? Rozbij na zadania.

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

## Suma × stawka godzinowa = cena bazowa

<!--
"Najczęstszy błąd: ludzie liczą tylko czas budowy i zapominają o wszystkim wokół. Discovery, dokumentacja, testy, setup środowiska — to często 50% projektu."
-->


---
---

# Przykładowe wyceny — 3 typy projektów

## Co ile kosztuje w realu?

| Typ projektu | Zakres | Szacunek godzin | Cena PLN |
|---|---|---|---|
| **Prosty workflow** | Powiadomienia, sync danych, 1-2 integracje | 20–40h | 8 000–15 000 |
| **Złożony agent** | Multi-step, AI, decyzje, 4+ systemy | 80–180h | 30 000–80 000 |
| **System RAG** | Baza wiedzy, embeddingi, UI, maintenance | 50–120h | 20 000–50 000 |

*Założenie: stawka 250–450 PLN/h zależnie od złożoności i klienta*

<!--
"To są liczby z prawdziwych projektów, zanonimizowane. Proszę żebyś nie traktował dolnych widełek jako normy — to jest absolutne minimum dla klienta który jest super zorganizowany i ma czas. Większość projektów ląduje bliżej górnej granicy."
-->


---
---

# Bufor 30% — dlaczego to za mało

## Co zjada twój bufor

- API które nie działają jak w dokumentacji (zawsze)
- Klient który "miał coś powiedzieć wcześniej"
- Środowisko produkcyjne różni się od testowego
- "Czy możecie dodać jeszcze jedno małe..."
- Rotacja po stronie klienta (nowy koordynator)
- Urlopy, choroby, opóźnienia w dostarczeniu dostępów

## Realna zasada: 30% to minimum. Dla nowych klientów — 40–50%.

<!--
Śmiech jest OK. "Tak, mówię poważnie. Mój bufor na nowych klientach to 50%. I nadal czasem ledwo wychodzę."
-->


---
---

# Discovery call — po co to w ogóle

## Discovery Call to NIE jest zbieranie wymagań technicznych

## Discovery Call to
- Zrozumienie bólu biznesowego
- Kwalifikacja: czy to dobry klient dla ciebie
- Zbudowanie zaufania
- Zebranie danych do value-based pricing

## Efekt dobrego discovery
- Wiesz co zbudować
- Wiesz ile to warte
- Wiesz czy chcesz z tym klientem pracować

<!--
"Większość konsultantów idzie na discovery żeby zbierać wymagania techniczne. To błąd. Idziesz żeby zrozumieć — po co to tak naprawdę?"
-->


---
---

# 10 pytań na discovery call (gotowe do wydruku)

## 10 pytań które MUSISZ zadać


<v-clicks>

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

</v-clicks>


<!--
"Wydrukuj to i połóż przed sobą na każdym discovery callu. Pytanie 7 jest najtrudniejsze — większość ludzi je pomija. Nie pomijaj."
-->


---
---

# Pytanie #7 — jak rozmawiać o budżecie

## "Jaki macie budżet?" — dlaczego to kluczowe

## Jeśli klient nie poda budżetu
> "Żeby zaproponować właściwe rozwiązanie, muszę wiedzieć z jakimi możliwościami pracuję. Czy mówimy o budżecie poniżej 10 000, między 10 a 50 tys., czy powyżej?"

## Jeśli budżet jest za mały
> "To co opisujesz wymaga X zł. Możemy omówić co wchodzi w mniejszy zakres, ale nie chcę obiecywać czegoś czego nie dostarczę."

## Dlaczego nie warto ukrywać cen
- Oszczędza czas obu stron
- Buduje wiarygodność
- Eliminuje złych klientów wcześnie

<!--
"Pytanie o budżet to nie jest bezczelność. To jest szacunek dla czasu klienta i twojego. Nauczyłem się tego po tym jak spędziłem 6 godzin na discovery dla klienta który miał budżet 3 000 PLN."
-->


---
---

# Red flags — kiedy powiedzieć NIE

## 7 sygnałów że ten projekt/klient będzie koszmarem

🚩 **"Zrób to szybko, potem rozliczymy"** — brak formalności to brak płatności

🚩 **Brak osoby decyzyjnej w rozmowie** — sprzedajesz komuś kto i tak nie zatwierdzi

🚩 **"To proste, to zajmie wam godzinę"** — klient nie rozumie zakresu pracy

🚩 **Poprzedni dostawca "zawiódł ich"** — możliwe że problem leży gdzie indziej

🚩 **Nie mają zdefiniowanego procesu** — automatyzujesz chaos (to nie działa)

🚩 **Negocjują cenę zanim zobaczyli ofertę** — będą negocjować na każdym etapie

🚩 **"Chcemy wszystko zrobić sami, tylko powiedzcie jak"** — nie potrzebują wykonawcy

<!--
"Każdy z tych flagów to projekt który zakończyłem albo z bólem i bez pełnej zapłaty, albo którego nie wziąłem i byłem z siebie dumny. Każdy."
-->


---
transition: fade
---

# BANT dla automatyzacji

<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem">
  <div style="background:#1E2D40;border-radius:8px;padding:0.6rem 0.8rem;border-left:3px solid #22C55E">
    <div style="color:#22C55E;font-weight:700;font-size:0.82rem">B — Budget</div>
    <div style="color:#A8D8EA;font-size:0.7rem;margin-top:2px">Czy mają środki na projekt?</div>
    <div style="color:#64748B;font-size:0.62rem;margin-top:2px">Min: zadeklarowany lub widoczny</div>
  </div>
  <div style="background:#1E2D40;border-radius:8px;padding:0.6rem 0.8rem;border-left:3px solid #3B82F6">
    <div style="color:#3B82F6;font-weight:700;font-size:0.82rem">A — Authority</div>
    <div style="color:#A8D8EA;font-size:0.7rem;margin-top:2px">Czy rozmawiasz z decydentem?</div>
    <div style="color:#64748B;font-size:0.62rem;margin-top:2px">Min: dostęp do osoby zatwierdzającej</div>
  </div>
  <div style="background:#1E2D40;border-radius:8px;padding:0.6rem 0.8rem;border-left:3px solid #F97316">
    <div style="color:#F97316;font-weight:700;font-size:0.82rem">N — Need</div>
    <div style="color:#A8D8EA;font-size:0.7rem;margin-top:2px">Czy ból jest realny i bolesny?</div>
    <div style="color:#64748B;font-size:0.62rem;margin-top:2px">Min: problem kosztuje czas/pieniądze</div>
  </div>
  <div style="background:#1E2D40;border-radius:8px;padding:0.6rem 0.8rem;border-left:3px solid #8B5CF6">
    <div style="color:#8B5CF6;font-weight:700;font-size:0.82rem">T — Timeline</div>
    <div style="color:#A8D8EA;font-size:0.7rem;margin-top:2px">Czy jest presja czasowa?</div>
    <div style="color:#64748B;font-size:0.62rem;margin-top:2px">Min: wdrożenie w 3-6 miesięcy</div>
  </div>
</div>

<div style="margin-top:0.6rem;background:#1E2D40;border-radius:8px;padding:0.6rem 1rem;border-left:3px solid #EF4444;font-size:0.78rem">
  <strong style="color:#EF4444">Brakuje 2+ kryteriów?</strong>
  <span style="color:#A8D8EA"> Nie wysyłaj oferty. To nie jest lead — to jest rozmowa.</span>
</div>


<!--
"BANT to narzędzie ze sprzedaży enterprise — ale działa idealnie dla projektów automatyzacji. Jeśli klient nie ma budżetu, nie jest decydentem, nie ma realnego bólu albo 'może kiedyś' — to nie jest lead, to jest rozmowa."
-->


---
---

# Struktura oferty która sprzedaje

## Błąd który popełniają wszyscy

❌ Zła struktura:
> "Zbudujemy workflow n8n z integracją Airtable przez REST API, wdrożymy na Docker z obsługą webhooków..."

✅ Dobra struktura:
> "Wyeliminujemy 3 godziny dziennie pracy manualnej w dziale handlowym przez automatyczne przekazywanie leadów z formularza do CRM i powiadamianie handlowca SMS-em w ciągu 30 sekund."

## Zasada: najpierw wynik, potem jak to osiągniemy

<!--
"Klient nie kupuje n8n. Klient kupuje 3 godziny dziennie swojego handlowca z powrotem. Pisz o tym."
-->


---
---

# Struktura oferty — 6 sekcji

## Oferta handlowa krok po kroku

1. **Rozumiemy twój problem** *(pokaż że słuchałeś na discovery)*
2. **Nasze rozwiązanie** *(wynik, nie technologia)*
3. **Co dostarczymy** *(deliverables: lista, daty, formaty)*
4. **Dlaczego to się opłaca** *(ROI kalkulator)*
5. **Inwestycja** *(Opcja A i B z cenami)*
6. **Następny krok** *(konkretne CTA: "Odezwij się do piątku")*

## Max 4–6 stron. Więcej = klient nie przeczyta.

<!--
"Moje oferty mają 4 strony. Klient który potrzebuje 20-stronicowej oferty żeby podjąć decyzję — to nie jest gotowy klient."
-->


---
---

# Opcja a i b — psychologia wyboru

## Zawsze dwie opcje — nigdy jedna, rzadko trzy

| | Opcja A | Opcja B |
|---|---|---|
| **Scope** | Podstawowy zakres | Rozszerzony zakres |
| **Wsparcie po** | Brak lub 30 dni | 6 miesięcy retainer |
| **Dokumentacja** | Standardowa | Rozszerzona + szkolenie |
| **Cena** | Np. 20 000 PLN | Np. 28 000 PLN |

## Dlaczego to działa
- Klient porównuje A z B, nie twoją ofertę z konkurencją
- B jest zazwyczaj lepszą inwestycją — klient to widzi
- Jeśli nie ma budżetu na B, ma "wyjście" przez A

<!--
"70% moich klientów wybiera Opcję B. Nie dlatego że jest droższa — dlatego że jest logicznie lepsza. Budujesz Opcję A jako bazę, ale tak żeby B była oczywistym wyborem dla kogoś kto myśli długoterminowo."
-->


---
---

# ROI — jak to liczyć z klientem

## Kalkulator ROI dla projektu automatyzacji

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

## Przykład: 25 000 PLN projekt, 5h/tydz oszczędności, 80 PLN/h pracownik
→ Oszczędności roczne: 5 × 80 × 52 = 20 800 PLN
→ Payback: ~14,5 miesiąca

<!--
"Zawsze rób kalkulator ROI razem z klientem na discovery — nie wstawiaj liczb samemu. Kiedy klient sam policzy ile traci — sam uzasadnia ci cenę projektu."
-->


---
---

# Follow-up — strategia bez natrętności

## Co zrobić gdy klient nie odpowiada

| Dzień | Akcja |
|---|---|
| Dzień 0 | Wysłanie oferty + potwierdzenie telefoniczne |
| Dzień 3 | "Czy dotarła oferta? Mam pytanie wyjaśniające..." |
| Dzień 7 | Wartościowy follow-up: artykuł, case study branżowy |
| Dzień 14 | Ostatni kontakt: "Decyzja jeszcze otwarta czy zamknięta?" |

## Po 14 dniach bez odpowiedzi: move on

**Co NIE działa:** "Tylko sprawdzam czy już zdecydowali..."

<!--
"Najlepszy follow-up jaki wysłałem to był newsletter z case study z branży klienta. Napisał do mnie sam następnego dnia. Daj wartość, nie pytaj o decyzję."
-->


---
---

# Umowa IT — co MUSI być

## 5 klauzul bez których nie podpisuj umowy


<v-clicks>

1. **Definicja zakresu** (scope) — lista deliverables, nie opis ogólny
2. **Procedura change request** — co się dzieje gdy klient chce czegoś spoza scope
3. **Kryteria akceptacji** — konkretne, mierzalne (nie "działa poprawnie")
4. **Harmonogram płatności** — zaliczka min. 30%, milestone, płatność końcowa
5. **Własność intelektualna** — kto jest właścicielem workflow po oddaniu

</v-clicks>


<!--
"Miałem projekt gdzie klient po 3 miesiącach powiedział że workflow 'nie spełnia wymagań'. Nie mieliśmy zdefiniowanych kryteriów akceptacji. To był bardzo drogi błąd — i dla mnie, i dla klienta."
-->


---
---

# IP — kto jest właścicielem workflow?

## Kwestia własności jest bardziej skomplikowana niż myślisz

| Komponent | Domyślnie należy do |
|---|---|
| Workflow n8n (eksport JSON) | Klient (zamówił i zapłacił) |
| Twoje reużywalne komponenty/snippety | Ty (chyba że inaczej uzgodnione) |
| Integracje z API zewnętrznymi | API provider (licencja) |
| Modele AI (OpenAI, Anthropic) | Provider (warunki użytkowania) |
| Custom nodes które napisałeś | Negocjowane w umowie |

## Rekomendacja: licencja "right to use" dla klienta, ty zachowujesz know-how

<!--
"Kluczowe: możesz budować podobne rozwiązania dla innych klientów. Nie sprzedajesz unikalnej wiedzy — sprzedajesz implementację. Klient dostaje prawo do używania, nie do tego żeby sprzedawać twoje rozwiązanie dalej."
-->


---
transition: fade
layout: two-cols-header
---

# RODO i DPA w projektach automatyzacji

<div class="col-header col-pos">Kiedy musisz podpisać Data Processing Agreement</div>

- Przetwarza dane osobowe klientów klienta (np. CRM → email)
- Pobiera dane z systemów HR
- Integruje formularze z danymi osób fizycznych
- Wysyła komunikację personalną

::right::

<div class="col-header col-neg">Co DPA musi zawierać</div>

- Cel przetwarzania danych
- Kategorie danych i podmiotów
- Czas przetwarzania
- Środki bezpieczeństwa
- Sub-procesorzy (np. OpenAI, n8n cloud)

<!--
"90% projektów automatyzacji B2B dotyka danych osobowych. Nie ignoruj tego — podpisanie DPA to 30 minut pracy prawnej, brak DPA to potencjalna odpowiedzialność z AI Act i RODO."
-->


---
---

# SLA po wdrożeniu — realny vs marketingowy

## SLA (Service Level Agreement) — co obiecywać, a czego nie

| Parametr | Bezpieczne | Ryzykowne |
|---|---|---|
| Czas reakcji na zgłoszenie | 24–48h w dni robocze | 2h (tylko jeśli masz monitoring) |
| Dostępność workflow | 99% (zależy od infrastruktury klienta) | 99.9% |
| Czas naprawy krytycznego błędu | 24–72h | "ASAP" (bez definicji) |
| Zakres SLA | Błędy w kodzie który napisałeś | Problemy z zewnętrznymi API |

## Złota zasada: SLA bez monitoringu to puste obietnice

<!--
"Mam klienta który dzwoni o 22:00 bo workflow 'nie działa'. Okazało się że API Shopify miało przerwę. To nie mój błąd — ale bez jasnego SLA byłem traktowany jak winny. Teraz mam to w każdej umowie."
-->


---
---

# Deliverables — kompletna lista

## Co dostarczasz klientowi po projekcie

## Obowiązkowe
- [ ] Workflow n8n (eksport JSON + import guide)
- [ ] Dokumentacja techniczna (architektura, flow diagram, node-by-node)
- [ ] Dokumentacja użytkowa (co robi, jak uruchomić, jak zatrzymać)
- [ ] Lista credentials i jak je rotować
- [ ] Protokół testów (co testowałeś, wyniki)
- [ ] Protokół odbioru (podpisany przez obie strony)

## Opcjonalne (w wyższych pakietach)
- [ ] Szkolenie użytkownika (nagranie lub na żywo)
- [ ] Runbook operacyjny (co robić gdy coś nie działa)
- [ ] Monitoring setup (alerty, dashboardy)

<!--
"Lista checkboxów to nie formalność — to twoja ochrona. Kiedy klient podpisze protokół odbioru potwierdzając że otrzymał wszystkie deliverables, trudniej mu powiedzieć że 'projekt nie jest skończony'."
-->


---
---

# Dokumentacja n8n — jak pisać

## Struktura dokumentu technicznego

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

<!--
"Dobra dokumentacja to 2–3 godziny pracy. Zła dokumentacja to 10 telefonów od klienta w ciągu roku. Matematyka jest prosta."
-->


---
---

# Training klienta — co pokazać

## Sesja szkoleniowa: 2–4 godziny

## Co pokazać
- Gdzie jest workflow w n8n (gdzie szukać, jak uruchomić manualnie)
- Jak sprawdzić logi i ostatnie executions
- Co robić gdy workflow "nie działa" (pierwsze kroki diagnostyki)
- Jak mnie skontaktować (i kiedy NIE kontaktować — bo to nie mój problem)
- Gdzie jest dokumentacja

## Czego NIE pokazywać na szkoleniu
- Jak modyfikować workflow (chyba że retainer tech — wtedy szkolenie developerskie)
- Wewnętrzna architektura (niepotrzebna złożoność)

<!--
"Nagrywaj szkolenia. Zawsze. Klient obejrzy to 5 razy w ciągu roku i uniknie 5 telefonów do ciebie."
-->


---
---

# Protokół odbioru — format

## Protokół odbioru kończy projekt (i otwiera płatność końcową)

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

<!--
"Ten dokument to twoja tarcza. Klient który podpisał protokół odbioru nie może 6 miesięcy później powiedzieć że projekt nie był skończony."
-->


---
---

# Retainer — dlaczego klient powinien chcieć

## Co się może stać bez retainera

- API zewnętrzne zmienia strukturę → workflow przestaje działać
- Platforma SaaS aktualizuje się → endpoint przestał istnieć
- Klient chce dodać nową integrację → musisz wyceniać od zera
- Rotacja pracowników → nowa osoba nie wie jak obsługiwać workflow
- Problem produkcyjny → klient nie ma priorytetowego dostępu do ciebie

## Z retainerem: spokój, ciągłość, optymalizacja

<!--
"Sprzedaż retainera to nie jest wciskanie klientowi kolejnego kosztu. To jest dawanie im peace of mind. Jeśli nie rozumiesz dlaczego mieliby tego chcieć — nie umiesz jeszcze sprzedawać."
-->


---
---

# Kiedy sprzedawać retainera

## Moment sprzedaży: tuż przed zakończeniem projektu

## Dlaczego PRZED handoverem, nie po
- Klient jest zaangażowany emocjonalnie (projekt idzie dobrze)
- Widzi wartość w działającym systemie
- Jest "w trybie inwestycji" (właśnie zapłacił)
- Po zamknięciu projektu: "dziękujemy, wrócimy jak będziemy potrzebować"

## Jak to powiedzieć
> "Zanim zamkniemy projekt, chcę porozmawiać o tym co się dzieje po wdrożeniu. Mam klientów którzy biorą retainer i klientów którzy nie biorą — mogę opowiedzieć różnicę."

<!--
"To zdanie działa, bo nie sprzedajesz — informujesz. Klient pyta o różnicę i sam sobie sprzedaje retainera."
-->


---
transition: fade
---

# Struktura retainera — co wchodzi

<N8nBranch
  :source="{icon: 'mdi:handshake', label: 'RETAINER', desc: 'pasywny przychód po projekcie'}"
  :branches="[
    {icon: 'mdi:eye-outline', label: 'Tier A: Monitoring', result: 'monitoring + SLA 48h', variant: 'default'},
    {icon: 'mdi:wrench', label: 'Tier B: Wsparcie', result: '+ naprawy + aktualizacje + SLA 24h', variant: 'action'},
    {icon: 'mdi:rocket-launch', label: 'Tier C: Rozwój', result: '+ nowe workflows + SLA 8h', variant: 'output'},
  ]"
/>

<div style="margin-top:0.8rem;background:#1E2D40;border-radius:8px;padding:0.8rem 1rem;border-left:3px solid #22C55E;font-size:0.8rem">
  <strong style="color:#22C55E">Formuła:</strong>
  <span style="color:#A8D8EA"> retainer = wartość projektu x 2-3% / mies. Projekt 30k → ~900 PLN/mies. (Tier B)</span>
</div>


<!--
"Tier A to pasywny przychód. Tier B to gdzie większość klientów trafia. Tier C to faktycznie outsourcing automatyzacji na stałe — idealny dla firm które chcą rozwijać automation roadmap."
-->


---
---

# Pricing retainerów — formuła

## Jak wycenić retainera

```
Retainer miesięczny = Wartość projektu × 2–3%
Retainer roczny = Wartość projektu × 15–30%
```

## Przykłady
- Projekt 20 000 PLN → retainer 400–600 PLN/mies. (Tier A) / 800–1 200 PLN/mies. (Tier B)
- Projekt 50 000 PLN → retainer 1 000–1 500 PLN/mies. (Tier A) / 2 000–3 000 PLN/mies. (Tier B)

## Dlaczego ta formuła
- Klient widzi że retainer jest "proporcjonalny" do inwestycji
- Ty masz przewidywalny przychód
- Wartość projektu to proxy złożoności systemu

<!--
"10 klientów na Tier B retainerze przy średnim projekcie 30k = 10 × 900 PLN/mies = 9 000 PLN pasywnie. To pół etatu bez nowych projektów. Tak budujesz firmę."
-->


---
transition: fade
---

# Pasywny przychód z portfela klientów

<div style="display:flex;gap:1rem;align-items:stretch">
  <div style="flex:1;background:#1E2D40;border-radius:8px;padding:0.8rem 1rem;border-top:3px solid #3B82F6">
    <div style="color:#3B82F6;font-weight:700;font-size:0.82rem;margin-bottom:0.4rem">Projekty (aktywny przychód)</div>
    <div style="color:#A8D8EA;font-size:0.72rem">2-3 projekty/kwartał x 20-50k</div>
    <div style="color:#3B82F6;font-weight:700;font-size:1rem;margin-top:0.4rem">120-300k PLN/rok</div>
  </div>
  <div style="display:flex;align-items:center;color:#F97316;font-size:1.5rem;font-weight:700">+</div>
  <div style="flex:1;background:#1E2D40;border-radius:8px;padding:0.8rem 1rem;border-top:3px solid #22C55E">
    <div style="color:#22C55E;font-weight:700;font-size:0.82rem;margin-bottom:0.4rem">Retainery (pasywny przychód)</div>
    <div style="color:#A8D8EA;font-size:0.72rem">10 klientów x 1 500 PLN/mies.</div>
    <div style="color:#22C55E;font-weight:700;font-size:1rem;margin-top:0.4rem">216k PLN/rok</div>
  </div>
</div>

<div style="margin-top:0.6rem;background:linear-gradient(90deg,#1E2D40,#0F2137);border-radius:8px;padding:0.6rem 1rem;border-top:2px solid #F97316;text-align:center">
  <span style="color:#F97316;font-weight:700;font-size:1.1rem">Suma: 336-516k PLN/rok</span>
  <div style="color:#8096AA;font-size:0.68rem;margin-top:2px">Retainery to fundament, projekty to wzrost.</div>
</div>


<!--
"Kiedy to zrozumiałem — przestałem panikować przy braku nowych projektów. Retainery to fundament, projekty to wzrost."
-->


---
---

# Błędy które popełniłem — top 5

## Żebyś ty ich nie popełniał


<v-clicks>

1. **Brak zaliczki** — klient zrezygnował po 30 godzinach pracy
2. **Brak procedury change request** — projekt urósł 3x poza scope
3. **Zbyt niskie ceny przez pierwsze 2 lata** — referencje bez pieniędzy nie płacą rachunków
4. **Projekt bez Discovery** — zbudowałem coś czego nikt nie używał
5. **Brak protokołu odbioru** — klient "nie pamiętał" że odebrał projekt

</v-clicks>


<!--
Spokojnie, bez samodramatyzowania. "Każdy z tych błędów kosztował mnie realnie — czas, pieniądze lub stres. Opowiadam o tym żebyś nie musiał ich powtarzać na własnym budżecie."
-->


---
---

# Następny krok

## Masz teraz wszystko żeby sprzedawać automatyzacje profesjonalnie

## Do pobrania w materiałach kursu
- Szablon wyceny (Markdown/arkusz)
- Szablon propozycji handlowej
- Lista 10 pytań Discovery Call
- Checklist handover projektu
- Kalkulator retainera

## Zadanie domowe
Przeprowadź mock Discovery Call z kimś ze społeczności kursu — jeden gra klienta, drugi konsultanta. 30 minut. Użyj listy 10 pytań.

## Pytania? Wpadnij na społeczność kursu.

<!--
Entuzjastyczne zamknięcie. "Daj znać w społeczności jak poszedł twój pierwszy Discovery Call z tą metodologią. Czytam każdy komentarz."
-->


---
class: layout-exercise
---

# Ćwiczenia praktyczne

Czas na praktykę! Otwórz n8n i zrób ćwiczenia samodzielnie.


---
class: layout-exercise
---

# ĆWICZENIE 1 — WYCENA PROJEKTÓW AUTOMATYZACJI (20 minut)




---
class: layout-exercise
---

# ĆWICZENIE 2 — PROPOZYCJA HANDLOWA (30 minut)


Zautomatyzować przyjmowanie zamówień + wystawianie faktur. Budżet: "coś rozsądnego, nie chcemy milionowego ERP".

## Checkpointy

<v-clicks>

- Problem opisany słowami klienta (nie Twoim żargonem)
- Opcja A vs B mają wyraźną różnicę wartości (nie tylko cenową)
- ROI wyliczone na konkretnych liczbach
- Żadne zdanie nie zaczyna się od "My" lub "Nasza firma"
- Propozycja ma max 2 strony A4 (lub odpowiednik w Markdown)
- Jest jeden wyraźny "następny krok"

</v-clicks>



---
class: layout-exercise
---

# ĆWICZENIE 3 — MOCK DISCOVERY CALL (25 minut)




---
class: layout-exercise
---

# ZADANIE DOMOWE — PRAWDZIWA PROPOZYCJA




---
class: layout-exercise
---

# MATERIAŁY DODATKOWE


