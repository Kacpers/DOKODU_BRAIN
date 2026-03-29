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

<div class="cover-tag">MODUŁ 00 — FILOZOFIA</div>

# > Plik dla prowadzącego. Każdy slajd zawiera treść wizualną + notatkę co mówisz.


<p style="color:#E63946;font-weight:600">Kacper Sieradziński</p>
<p style="color:#8096AA;font-size:0.8rem;margin-top:0.2rem">dokodu.it</p>


---
---

# Tytuł — filozofia automatyzacji

## n8n + AI dla Agencji i Firm
## Moduł 0: Filozofia Automatyzacji

*(małe napisy)*
*Kacper Sieradziński | CEO Dokodu | FREE*

<!--
Ten slajd pojawia się tylko na chwilę — zanim w ogóle go pokażesz, zacznij od haka słownego. Slajd jest tłem, nie głównym przekazem. Możesz go wyświetlić zanim zaczniesz mówić, żeby dać chwilę na odczyt.
-->


---
---

# Hook — liczby mówią same za siebie

## 4 godziny tygodniowo
Tyle odzyskałem automatyzując jeden proces w Dokodu.

## 208 godzin rocznie
Czyli 26 dni roboczych. Cały miesiąc.

## Koszt ustawienia: 20 minut

<!--
Stój cicho przez 3 sekundy po pokazaniu tego slajdu. Daj im czas na policzenie. Potem mów: "Jeden workflow. Nie AI, nie magia. Prosty if-then w n8n. Zaraz Ci pokażę jak to działa."
-->


---
---

# Kim jestem (30 sekund, bez przesady)

## Kacper Sieradziński
CEO Dokodu — agencja AI automation


<v-clicks>

- ~50 000 subskrybentów YouTube (n8n, AI, automatyzacja)
- 15+ lat w branży tech
- Buduję workflow dla polskich firm: od startupu do korporacji
- Użytkownik n8n od wersji 0.x (pamiętam jak to wyglądało na początku)

</v-clicks>


<!--
Mów szybko. Ten slajd to tylko „dlaczego warto mnie słuchać" — nie autobiography. Końcowa linijka o wersji 0.x to ludzki element, pokazuje że jesteś z narzędziem od dawna. Przejdź do następnego slajdu w 30 sekund.
-->


---
---

# Co wyniesiesz z tego modułu

Po tych 45 minutach:

✅ Rozumiesz czym jest (i NIE jest) automatyzacja procesów
✅ Wiesz dlaczego n8n — twarde argumenty, nie marketing
✅ Znasz framework: trigger → akcja → warunek
✅ Masz n8n uruchomione na swoim komputerze lub w Cloud
✅ Budujesz swój pierwszy działający workflow

<!--
Przeczytaj każdy punkt głośno, zatrzymując się chwilę. To kontrakt z uczestnikiem. Mówisz: "Oto co dostajesz, oto moje zobowiązanie wobec Ciebie." Wytwarza oczekiwanie i trzyma ludzi do końca.
-->


---
---

# Definicja robocza — czym jest automatyzacja?

## Automatyzacja = software robi za Ciebie to, co robisz ręcznie i co można opisać krok po kroku

*Klucz: "można opisać krok po kroku"*

Przykład ręczny:

<v-clicks>

1. Sprawdzam skrzynkę co godzinę
2. Widzę nowy formularz
3. Kopiuję dane do arkusza
4. Wysyłam email powitalny
5. Dodaję do CRM

</v-clicks>


Przykład zautomatyzowany:
→ Formularz wypełniony → (n8n robi kroki 2-5 automatycznie w 3 sekundy)

<!--
Zatrzymaj się na "można opisać krok po kroku" — to jest granica automatyzacji. Jeśli czegoś nie możesz opisać jako algorytmu, nie zautomatyzujesz tego (jeszcze). Intuicja, kreatywność, negocjacje — na razie poza zasięgiem.
-->


---
---

# MIT #1 — "to tylko dla developerów"

## ❌ MIT: Automatyzacja wymaga programowania

## ✅ PRAWDA
- n8n ma 400+ integracji bez jednej linii kodu
- Większość workflow to drag & drop
- Kod (JavaScript/Python) jest opcją, nie wymogiem
- Jeśli umiesz Excel, umiesz n8n

*Disclaimer: im głębiej, tym przydaje się znajomość JSON i podstaw JS. Ale do 80% przypadków — zbędne.*

<!--
Dodaj: "W tym kursie będę czasem pisać kod — nie dlatego że musisz, ale dlatego że jest szybszy dla zaawansowanych przypadków. Każdy kod będę tłumaczyć linijka po linijce."
-->


---
---

# MIT #2 — "ai zastąpi potrzebę automatyzacji"

## ❌ MIT: Mam ChatGPT, po co mi n8n?

## ✅ PRAWDA
- AI = składnik. n8n = silnik który nim zarządza.
- ChatGPT nie wie kiedy przyszedł formularz
- ChatGPT nie zapisze danych do bazy danych
- ChatGPT nie wyśle emaila za Ciebie

**Analogia:** AI to silnik. n8n to cały samochód (skrzynia biegów, układ hamulcowy, GPS).

<!--
To jest ważne dla 2026 roku gdy wszyscy pytają "po co workflow skoro mam agenta AI?". Odpowiedź: agenty AI działają WEWNĄTRZ n8n. Moduł 6 kursu jest w całości o agentach. Wspomnij to tutaj — to jest teaser.
-->


---
---

# MIT #3 — "to zajmuje miesiące konfiguracji"

## ❌ MIT: Automatyzacja to projekt na kwartał

## ✅ PRAWDA
| Co budujesz | Czas ustawienia |
|-------------|----------------|
| Email powitalny po formularzu | 20 minut |
| Powiadomienie Slack z nowego leada | 15 minut |
| Raport tygodniowy ze spreadsheet | 45 minut |
| Pełny pipeline obsługi klienta | 2-3 dni |

*Pierwszy workflow: dziś. Pierwsza realna wartość: ten tydzień.*

<!--
Mów to z energią. "Zanim skończymy ten moduł — masz działający workflow." To nie obietnica — to dosłownie co się stanie jeśli przejdziesz ćwiczenie.
-->


---
---

# Co warto automatyzować — przykłady z polskich firm

## Procesy powtarzalne i opisywalne

🔔 **Powiadomienia** — nowy lead, nowa faktura, termin płatności
📧 **Emaile** — powitalne, przypomnienia, follow-upy
📊 **Raporty** — tygodniowe, miesięczne, na żądanie
🔄 **Synchronizacja danych** — między systemami (CRM, ERP, arkusze)
✅ **Onboarding** — klientów, pracowników, partnerów
🔍 **Monitoring** — strona działa? Czy serwer odpowiada?

<!--
Każdy punkt to historia. Powiedz "Mam klienta który..." dla 2-3 z nich. Konkret sprzedaje lepiej niż abstrakcja.
-->


---
---

# Czego NIE automatyzować

## Trzymaj człowieka tam gdzie człowiek ma wartość

❌ Decyzje strategiczne (komu dać rabat, którego klienta wziąć)
❌ Relacje (rozmowy sprzedażowe, negocjacje)
❌ Twórcze elementy (strategia, branding, narracja)
❌ Zarządzanie kryzysem (gdy coś się sypie — człowiek decyduje)
❌ Wszystko co wymaga empatii i kontekstu społecznego

*n8n może Ci przygotować dane do decyzji. Decyzja — Twoja.*

<!--
Ten slajd buduje zaufanie. Nie sprzedajesz automatyzacji jako panaceum — mówisz kiedy NIE stosować. To jest dojrzałe podejście które odróżnia ekspertów od guru.
-->


---
---

# n8n vs Zapier vs Make — porównanie ogólne

| | **n8n** | **Zapier** | **Make** |
|---|---------|----------|---------|
| Model | Self-hosted / Cloud | SaaS Cloud | SaaS Cloud |
| Kod źródłowy | Open Source (fair-code) | Zamknięty | Zamknięty |
| Dane klientów | Na Twoim serwerze | Serwery US | Serwery US/EU |
| RODO | ✅ Pełna kontrola | ⚠️ Umowa DPA | ⚠️ Umowa DPA |
| Vendor lock-in | Brak | Wysoki | Średni |
| Krzywa uczenia | Średnia | Niska | Średnia |
| Community | Rosnące | Duże | Średnie |

<!--
Nie atakuj Zapiera ani Make. Powiedz: "Zapier to świetne narzędzie dla pewnych scenariuszy. Ale jeśli pracujesz z danymi klientów, budujesz agencję lub dbasz o RODO — n8n wygrywa."
-->


---
---

# n8n vs Zapier vs Make — ceny (twarde liczby, 2026)

## Scenariusz: 10 000 operacji miesięcznie, 1 użytkownik

| Narzędzie | Plan | Koszt/mies. |
|-----------|------|------------|
| **n8n self-hosted** | VPS ~20 USD/mies. | ~80 PLN |
| **n8n Cloud** | Starter | $20 (~80 PLN) |
| **Zapier** | Professional | $49 (~200 PLN) |
| **Make** | Core | $9 (ale: operacje!) |

**Make pułapka:** 10 000 "operacji" Make ≠ 10 000 tasków. Multi-step scenarios mnożą operacje. Realne koszty często 3-5x wyższe niż szacowane.

*Różnica rok do roku przy 10k operacji: Zapier $588 vs n8n Cloud $240 = oszczędność $348/rok*

<!--
Pokaż kalkulator na żywo lub przygotuj screenshoty z aktualnych cenników (ceny zmieniają się — sprawdź przed nagraniem!). Liczby robią wrażenie.
-->


---
---

# RODO i dane klientów — to nie jest akademickie pytanie

## Gdzie lądują dane Twoich klientów gdy używasz Zapier?

Zapier Terms of Service (2024):
> *"Zapier processes data on servers located in the United States..."*

## Co to oznacza praktycznie
- Dane z formularzy → Zapier US servers
- Dane z CRM → Zapier US servers
- Imiona, emaile, numery telefonów → US servers

## n8n self-hosted
→ Dane zostają na Twoim serwerze. Koniec historii.

Kara RODO: do 4% obrotu globalnego lub 20 mln EUR

<!--
Nie strasz, ale informuj. Mów: "Większość firm to ignoruje. Większość firm też nie ma audytu RODO. Kiedy mają — wtedy zaczynają migrację do n8n. Lepiej zacząć od razu."
-->


---
transition: fade
layout: two-cols-header
---

# Vendor lock-in — historia przestrogą

<div class="col-header col-pos">Zapier zmienił cennik w 2022</div>

- Usunął "multi-step zaps" z darmowego planu
- Podniósł ceny Professional o ~50%
- Tysiące małych firm musiały migrować lub płacić

::right::

<div class="col-header col-neg">n8n open-source</div>

- Możesz pobrać cały kod
- Możesz hostować gdzie chcesz
- Możesz zmodyfikować do własnych potrzeb
- Nawet jeśli n8n Inc. zniknie — narzędzie dalej działa

<!--
Dodaj osobistą historię jeśli masz — migracja z innego narzędzia, ból który z tym związany. Osobiste doświadczenie > case study z internetu.
-->


---
transition: fade
---

# Diagram — framework trigger → akcja → warunek

<N8nBranch
  :source="{icon: 'mdi:lightning-bolt', label: 'TRIGGER', desc: 'co uruchamia workflow?'}"
  :branches="[
    {icon: 'mdi:cog', label: 'AKCJA', desc: 'co workflow robi?', result: 'email, zapis, API call', variant: 'action'},
  ]"
/>

<div style="margin-top:0.6rem;display:flex;gap:0.8rem;align-items:center;justify-content:center">
  <div style="background:#1E2D40;border-radius:8px;padding:0.6rem 1rem;border-top:2px solid #F97316;text-align:center">
    <div style="color:#F97316;font-weight:700;font-size:0.78rem">WARUNEK (IF)</div>
    <div style="color:#8096AA;font-size:0.68rem">czy spełniony X?</div>
  </div>
  <div style="display:flex;flex-direction:column;gap:0.4rem">
    <div style="background:#1E2D40;border-left:3px solid #22C55E;padding:0.35rem 0.7rem;border-radius:0 6px 6px 0">
      <span style="color:#22C55E;font-weight:700;font-size:0.72rem">TAK →</span>
      <span style="color:#A8D8EA;font-size:0.68rem"> Akcja A</span>
    </div>
    <div style="background:#1E2D40;border-left:3px solid #EF4444;padding:0.35rem 0.7rem;border-radius:0 6px 6px 0">
      <span style="color:#EF4444;font-weight:700;font-size:0.72rem">NIE →</span>
      <span style="color:#A8D8EA;font-size:0.68rem"> Akcja B</span>
    </div>
  </div>
</div>


<!--
Narysuj ten diagram ręcznie na tablicy lub pokaż animację w Canva. Fizyczny gest (rysowanie) lepiej zapada w pamięć niż statyczny slajd. Wróć do tego diagramu w demonstracji live.
-->


---
transition: fade
---

# Przykład procesu rozłożonego na trigger/akcja/warunek

<N8nFlow
  :nodes="[
    {icon: 'mdi:form-select', label: 'Formularz', desc: 'wypełniony na stronie', variant: 'trigger'},
    {icon: 'logos:google-sheets', label: 'Arkusz / CRM', desc: 'zapisz dane', variant: 'action'},
    {icon: 'logos:gmail', label: 'Email', desc: 'powitalny do klienta', variant: 'action'},
    {icon: 'mdi:source-branch', label: 'IF', desc: 'budżet > 10k?', variant: 'default'},
  ]"
  animated
/>

<div style="margin-top:0.6rem;display:flex;gap:0.8rem">
  <div style="background:#1E2D40;border-left:3px solid #22C55E;padding:0.5rem 0.8rem;border-radius:0 6px 6px 0;flex:1">
    <div style="color:#22C55E;font-weight:700;font-size:0.75rem">TAK → budżet > 10k</div>
    <div style="color:#A8D8EA;font-size:0.72rem;margin-top:2px">Slack do Kacpra + Calendly call</div>
  </div>
  <div style="background:#1E2D40;border-left:3px solid #F97316;padding:0.5rem 0.8rem;border-radius:0 6px 6px 0;flex:1">
    <div style="color:#F97316;font-weight:700;font-size:0.75rem">NIE → mały budżet</div>
    <div style="color:#A8D8EA;font-size:0.72rem;margin-top:2px">Nurturing sequence MailerLite</div>
  </div>
</div>


<!--
Pokaż że to dokładnie ten diagram który przed chwilą rysowali. Teoria staje się praktyką w ciągu 60 sekund. To jest eureka moment.
-->


---
transition: fade
---

# Setup — decision tree (kiedy co wybrać)

<N8nBranch
  :source="{icon: 'mdi:rocket-launch', label: 'Chcę zacząć z n8n', desc: 'wybierz ścieżkę'}"
  :branches="[
    {icon: 'mdi:laptop', label: 'Testuję lokalnie', result: 'Docker Desktop → port 5678', variant: 'action'},
    {icon: 'logos:docker-icon', label: 'Mam VPS (Linux)', result: 'Self-hosted n8n (Docker na VPS)', variant: 'trigger'},
    {icon: 'mdi:cloud-outline', label: 'Nie mam VPS / DevOps', result: 'n8n Cloud (trial → $20/mies.)', variant: 'output'},
  ]"
/>

<div style="margin-top:0.8rem;background:#1E2D40;border-radius:8px;padding:0.8rem 1rem;border-left:3px solid #F97316;font-size:0.8rem">
  <strong style="color:#F97316">Tip:</strong>
  <span style="color:#A8D8EA"> Freelancer testujący → Docker lokalnie. Projekt dla klienta → Cloud lub VPS.</span>
</div>


<!--
Przejdź przez każdą ścieżkę. Mów do różnych grup: "Jeśli jesteś freelancerem testującym — Docker lokalnie. Jeśli robisz to dla klienta — Cloud lub VPS." Różni uczestnicy, różne potrzeby.
-->


---
---

# Docker — instalacja w jednej komendzie

## Wymagania
- Docker Desktop (Mac/Windows) lub Docker Engine (Linux)
- Port 5678 wolny

## Komenda
```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  docker.n8n.io/n8nio/n8n
```

**Potem:** otwórz `http://localhost:5678` w przeglądarce

**Czas:** ~2 minuty (pierwsze pobranie obrazu: ~1-2 min, start: ~10 sek)

<!--
Pokaż terminal na żywo. Skopiuj komendę z notatek. Nie pisz z pamięci — pomyłka w live demo psuje zaufanie. Plik `04_Cwiczenia.md` zawiera pełną instrukcję krok po kroku dla uczestników.
-->


---
---

# Interfejs n8n — mapa terenu

*(Tutaj: screenshot interfejsu n8n z ponumerowanymi elementami)*

**1. Sidebar** — lista workflow, credentials, executions
**2. Canvas** — główna przestrzeń robocza (drag & drop)
**3. Node panel** — klikasz "+" żeby dodać nowy node
**4. Execution log** — co się wydarzyło, dane wejście/wyjście
**5. Run/Save** — uruchom i zapisz workflow

*Analogia:* Sidebar = szuflady biurka. Canvas = blat. Node panel = skrzynka narzędziowa.

<!--
Ten slajd to tylko orientacja — nie tłumacz każdej opcji menu. Mów: "Nie musisz teraz wszystkiego zapamiętać. Za chwilę zobaczysz to na żywo i samo wpadnie."
-->


---
transition: fade
---

# Demo — workflow hello automation

<N8nFlow
  :nodes="[
    {icon: 'mdi:webhook', label: 'Webhook', desc: 'odbierz HTTP POST', variant: 'trigger'},
    {icon: 'mdi:code-json', label: 'Parse JSON', desc: 'wyciągnij dane', variant: 'default'},
    {icon: 'logos:gmail', label: 'Gmail', desc: 'email powitalny', variant: 'output'},
  ]"
  animated
  caption="Wysyłasz HTTP request → osoba dostaje spersonalizowany email. Czas budowania: ~8 minut."
/>


<!--
Ten slajd jest przejściem do demo na żywo. Pokaż go, powiedz "To budujemy. Gotowy? Zaczynamy." — i przeskocz do n8n. Nie tłumacz za dużo przed demo. Demo tłumaczy samo.
-->


---
class: layout-takeaway
---

# Podsumowanie modułu 0

## Dzisiaj nauczyłeś się

✅ Automatyzacja = procesy opisywalne krok po kroku
✅ n8n: self-hosted, RODO-friendly, bez vendor lock-in, tańszy
✅ Framework: Trigger → Akcja → Warunek (dotyczy każdego workflow)
✅ Setup: Docker lokalnie lub n8n Cloud
✅ Zbudowałeś pierwszy workflow (webhook → email)

## To był Moduł 0. W pełnym kursie
→ API REST i webhooks (głęboko)
→ AI nodes: GPT, Claude, Whisper
→ Autonomous agents i RAG
→ Bezpieczeństwo i produkcyjne deployments

<!--
Mów z energią. To jest zamknięcie pętli otwartej na początku. "Obiecałem Ci 5 rzeczy — oto potwierdzenie że to dostarczyłem."
-->


---
---

# CTA — co dalej?

## Jeśli ten moduł był wartościowy

🔗 **Pełny kurs:** [link do strony zapisu]

## Co jest w kursie
- 7 modułów + 2 bonusy
- ~8 godzin materiału
- Projekty z prawdziwych klientów Dokodu
- Dostęp dożywotni + aktualizacje
- Społeczność (Discord)

## Dla kogo
✅ Właściciel firmy / agencji który chce automatyzować
✅ Freelancer który chce oferować automatyzacje
✅ Developer który chce szybko budować pipelines

<!--
Nie czytaj slajdu. Powiedz to swoimi słowami. Zakończ tak: "Do zobaczenia w Module 1 — tam zaczynamy od API i webhooków. Serio." I urwij. Bez długiego pożegnania.
-->


---
class: layout-exercise
---

# Ćwiczenia praktyczne

Czas na praktykę! Otwórz n8n i zrób ćwiczenia samodzielnie.


---
class: layout-exercise
---

# Zanim zaczniesz — co potrzebujesz


## Checkpointy

<v-clicks>

- Komputer z systemem Windows 10/11, macOS 12+, lub Linux Ubuntu 20.04+
- Połączenie z internetem (pobieranie obrazu Docker ~200 MB)
- Konto Gmail (dowolne — możesz stworzyć testowe)
- 20–30 minut spokojnego czasu

</v-clicks>



---
class: layout-exercise
---

# CZĘŚĆ 1 — instalacja Docker i uruchomienie n8n


## Checkpointy

<v-clicks>

- n8n uruchomiony i dostępny na localhost:5678
- Zalogowany do n8n

</v-clicks>



---
class: layout-exercise
---

# CZĘŚĆ 2 — połącz konto Gmail


## Checkpointy

<v-clicks>

- Gmail OAuth2 credentials połączone

</v-clicks>



---
class: layout-exercise
---

# CZĘŚĆ 3 — zbuduj workflow


## Checkpointy

<v-clicks>

- Nowy workflow "Hello Automation" utworzony
- Node Webhook skonfigurowany i URL skopiowany
- Node Set skonfigurowany z polami recipientName i recipientEmail
- Node Gmail skonfigurowany z expressions
- Email dotarł na skrzynkę
- Workflow aktywny i działa na production URL

</v-clicks>



---
class: layout-exercise
---

# Gratulacje — twój pierwszy workflow działa!




---
class: layout-exercise
---

# Checkpoint — co powinieneś mieć po ćwiczeniu


## Checkpointy

<v-clicks>

- Docker Desktop zainstalowany i działa
- n8n dostępny na `http://localhost:5678`
- Konto n8n utworzone (email + hasło)
- Gmail OAuth2 credentials skonfigurowane
- Workflow "Hello Automation" zbudowany (3 nody)
- Email testowy odebrany na skrzynce
- Workflow aktywowany i przetestowany na Production URL

</v-clicks>



---
class: layout-exercise
---

# Co dalej?


