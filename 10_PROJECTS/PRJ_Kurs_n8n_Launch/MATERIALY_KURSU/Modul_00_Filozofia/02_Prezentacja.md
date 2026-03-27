# Moduł 0: Filozofia Automatyzacji — Prezentacja (Slajd po slajdzie)

> **Plik dla prowadzącego.** Każdy slajd zawiera treść wizualną + notatkę co mówisz.
> Narzędzie: Canva / PowerPoint / Keynote — do wyboru. Kolory: granatowy (#1a1a2e) + akcent pomarańczowy (#f97316) + biały tekst.

---

## Slajd 1: Tytuł — Filozofia Automatyzacji

**n8n + AI dla Agencji i Firm**
**Moduł 0: Filozofia Automatyzacji**

*(małe napisy)*
*Kacper Sieradziński | CEO Dokodu | FREE*

> 🎙️ NOTATKA: Ten slajd pojawia się tylko na chwilę — zanim w ogóle go pokażesz, zacznij od haka słownego. Slajd jest tłem, nie głównym przekazem. Możesz go wyświetlić zanim zaczniesz mówić, żeby dać chwilę na odczyt.

---

## Slajd 2: Hook — Liczby mówią same za siebie

**4 godziny tygodniowo**
Tyle odzyskałem automatyzując jeden proces w Dokodu.

**208 godzin rocznie**
Czyli 26 dni roboczych. Cały miesiąc.

**Koszt ustawienia: 20 minut**

> 🎙️ NOTATKA: Stój cicho przez 3 sekundy po pokazaniu tego slajdu. Daj im czas na policzenie. Potem mów: "Jeden workflow. Nie AI, nie magia. Prosty if-then w n8n. Zaraz Ci pokażę jak to działa."

---

## Slajd 3: Kim jestem (30 sekund, bez przesady)

**Kacper Sieradziński**
CEO Dokodu — agencja AI automation

- ~50 000 subskrybentów YouTube (n8n, AI, automatyzacja)
- 15+ lat w branży tech
- Buduję workflow dla polskich firm: od startupu do korporacji
- Użytkownik n8n od wersji 0.x (pamiętam jak to wyglądało na początku)

> 🎙️ NOTATKA: Mów szybko. Ten slajd to tylko „dlaczego warto mnie słuchać" — nie autobiography. Końcowa linijka o wersji 0.x to ludzki element, pokazuje że jesteś z narzędziem od dawna. Przejdź do następnego slajdu w 30 sekund.

---

## Slajd 4: Co wyniesiesz z tego modułu

Po tych 45 minutach:

✅ Rozumiesz czym jest (i NIE jest) automatyzacja procesów
✅ Wiesz dlaczego n8n — twarde argumenty, nie marketing
✅ Znasz framework: trigger → akcja → warunek
✅ Masz n8n uruchomione na swoim komputerze lub w Cloud
✅ Budujesz swój pierwszy działający workflow

> 🎙️ NOTATKA: Przeczytaj każdy punkt głośno, zatrzymując się chwilę. To kontrakt z uczestnikiem. Mówisz: "Oto co dostajesz, oto moje zobowiązanie wobec Ciebie." Wytwarza oczekiwanie i trzyma ludzi do końca.

---

## Slajd 5: Definicja robocza — Czym jest automatyzacja?

**Automatyzacja = software robi za Ciebie to, co robisz ręcznie i co można opisać krok po kroku**

*Klucz: "można opisać krok po kroku"*

Przykład ręczny:
1. Sprawdzam skrzynkę co godzinę
2. Widzę nowy formularz
3. Kopiuję dane do arkusza
4. Wysyłam email powitalny
5. Dodaję do CRM

Przykład zautomatyzowany:
→ Formularz wypełniony → (n8n robi kroki 2-5 automatycznie w 3 sekundy)

> 🎙️ NOTATKA: Zatrzymaj się na "można opisać krok po kroku" — to jest granica automatyzacji. Jeśli czegoś nie możesz opisać jako algorytmu, nie zautomatyzujesz tego (jeszcze). Intuicja, kreatywność, negocjacje — na razie poza zasięgiem.

---

## Slajd 6: MIT #1 — "To tylko dla developerów"

**❌ MIT: Automatyzacja wymaga programowania**

**✅ PRAWDA:**
- n8n ma 400+ integracji bez jednej linii kodu
- Większość workflow to drag & drop
- Kod (JavaScript/Python) jest opcją, nie wymogiem
- Jeśli umiesz Excel, umiesz n8n

*Disclaimer: im głębiej, tym przydaje się znajomość JSON i podstaw JS. Ale do 80% przypadków — zbędne.*

> 🎙️ NOTATKA: Dodaj: "W tym kursie będę czasem pisać kod — nie dlatego że musisz, ale dlatego że jest szybszy dla zaawansowanych przypadków. Każdy kod będę tłumaczyć linijka po linijce."

---

## Slajd 7: MIT #2 — "AI zastąpi potrzebę automatyzacji"

**❌ MIT: Mam ChatGPT, po co mi n8n?**

**✅ PRAWDA:**
- AI = składnik. n8n = silnik który nim zarządza.
- ChatGPT nie wie kiedy przyszedł formularz
- ChatGPT nie zapisze danych do bazy danych
- ChatGPT nie wyśle emaila za Ciebie

**Analogia:** AI to silnik. n8n to cały samochód (skrzynia biegów, układ hamulcowy, GPS).

> 🎙️ NOTATKA: To jest ważne dla 2026 roku gdy wszyscy pytają "po co workflow skoro mam agenta AI?". Odpowiedź: agenty AI działają WEWNĄTRZ n8n. Moduł 6 kursu jest w całości o agentach. Wspomnij to tutaj — to jest teaser.

---

## Slajd 8: MIT #3 — "To zajmuje miesiące konfiguracji"

**❌ MIT: Automatyzacja to projekt na kwartał**

**✅ PRAWDA:**
| Co budujesz | Czas ustawienia |
|-------------|----------------|
| Email powitalny po formularzu | 20 minut |
| Powiadomienie Slack z nowego leada | 15 minut |
| Raport tygodniowy ze spreadsheet | 45 minut |
| Pełny pipeline obsługi klienta | 2-3 dni |

*Pierwszy workflow: dziś. Pierwsza realna wartość: ten tydzień.*

> 🎙️ NOTATKA: Mów to z energią. "Zanim skończymy ten moduł — masz działający workflow." To nie obietnica — to dosłownie co się stanie jeśli przejdziesz ćwiczenie.

---

## Slajd 9: Co warto automatyzować — przykłady z polskich firm

**Procesy powtarzalne i opisywalne:**

🔔 **Powiadomienia** — nowy lead, nowa faktura, termin płatności
📧 **Emaile** — powitalne, przypomnienia, follow-upy
📊 **Raporty** — tygodniowe, miesięczne, na żądanie
🔄 **Synchronizacja danych** — między systemami (CRM, ERP, arkusze)
✅ **Onboarding** — klientów, pracowników, partnerów
🔍 **Monitoring** — strona działa? Czy serwer odpowiada?

> 🎙️ NOTATKA: Każdy punkt to historia. Powiedz "Mam klienta który..." dla 2-3 z nich. Konkret sprzedaje lepiej niż abstrakcja.

---

## Slajd 10: Czego NIE automatyzować

**Trzymaj człowieka tam gdzie człowiek ma wartość:**

❌ Decyzje strategiczne (komu dać rabat, którego klienta wziąć)
❌ Relacje (rozmowy sprzedażowe, negocjacje)
❌ Twórcze elementy (strategia, branding, narracja)
❌ Zarządzanie kryzysem (gdy coś się sypie — człowiek decyduje)
❌ Wszystko co wymaga empatii i kontekstu społecznego

*n8n może Ci przygotować dane do decyzji. Decyzja — Twoja.*

> 🎙️ NOTATKA: Ten slajd buduje zaufanie. Nie sprzedajesz automatyzacji jako panaceum — mówisz kiedy NIE stosować. To jest dojrzałe podejście które odróżnia ekspertów od guru.

---

## Slajd 11: n8n vs Zapier vs Make — Porównanie ogólne

| | **n8n** | **Zapier** | **Make** |
|---|---------|----------|---------|
| Model | Self-hosted / Cloud | SaaS Cloud | SaaS Cloud |
| Kod źródłowy | Open Source (fair-code) | Zamknięty | Zamknięty |
| Dane klientów | Na Twoim serwerze | Serwery US | Serwery US/EU |
| RODO | ✅ Pełna kontrola | ⚠️ Umowa DPA | ⚠️ Umowa DPA |
| Vendor lock-in | Brak | Wysoki | Średni |
| Krzywa uczenia | Średnia | Niska | Średnia |
| Community | Rosnące | Duże | Średnie |

> 🎙️ NOTATKA: Nie atakuj Zapiera ani Make. Powiedz: "Zapier to świetne narzędzie dla pewnych scenariuszy. Ale jeśli pracujesz z danymi klientów, budujesz agencję lub dbasz o RODO — n8n wygrywa."

---

## Slajd 12: n8n vs Zapier vs Make — Ceny (twarde liczby, 2026)

**Scenariusz: 10 000 operacji miesięcznie, 1 użytkownik**

| Narzędzie | Plan | Koszt/mies. |
|-----------|------|------------|
| **n8n self-hosted** | VPS ~20 USD/mies. | ~80 PLN |
| **n8n Cloud** | Starter | $20 (~80 PLN) |
| **Zapier** | Professional | $49 (~200 PLN) |
| **Make** | Core | $9 (ale: operacje!) |

**Make pułapka:** 10 000 "operacji" Make ≠ 10 000 tasków. Multi-step scenarios mnożą operacje. Realne koszty często 3-5x wyższe niż szacowane.

*Różnica rok do roku przy 10k operacji: Zapier $588 vs n8n Cloud $240 = oszczędność $348/rok*

> 🎙️ NOTATKA: Pokaż kalkulator na żywo lub przygotuj screenshoty z aktualnych cenników (ceny zmieniają się — sprawdź przed nagraniem!). Liczby robią wrażenie.

---

## Slajd 13: RODO i dane klientów — to nie jest akademickie pytanie

**Gdzie lądują dane Twoich klientów gdy używasz Zapier?**

Zapier Terms of Service (2024):
> *"Zapier processes data on servers located in the United States..."*

**Co to oznacza praktycznie:**
- Dane z formularzy → Zapier US servers
- Dane z CRM → Zapier US servers
- Imiona, emaile, numery telefonów → US servers

**n8n self-hosted:**
→ Dane zostają na Twoim serwerze. Koniec historii.

Kara RODO: do 4% obrotu globalnego lub 20 mln EUR

> 🎙️ NOTATKA: Nie strasz, ale informuj. Mów: "Większość firm to ignoruje. Większość firm też nie ma audytu RODO. Kiedy mają — wtedy zaczynają migrację do n8n. Lepiej zacząć od razu."

---

## Slajd 14: Vendor lock-in — historia przestrogą

**Zapier zmienił cennik w 2022**

- Usunął "multi-step zaps" z darmowego planu
- Podniósł ceny Professional o ~50%
- Tysiące małych firm musiały migrować lub płacić

**n8n open-source:**
- Możesz pobrać cały kod
- Możesz hostować gdzie chcesz
- Możesz zmodyfikować do własnych potrzeb
- Nawet jeśli n8n Inc. zniknie — narzędzie dalej działa

*Twoje workflow = Twój majątek. Nie czyiś SaaS.*

> 🎙️ NOTATKA: Dodaj osobistą historię jeśli masz — migracja z innego narzędzia, ból który z tym związany. Osobiste doświadczenie > case study z internetu.

---

## Slajd 15: Diagram — Framework trigger → akcja → warunek

```
         TRIGGER
    (Co uruchamia workflow?)
           │
           ▼
         AKCJA
    (Co workflow robi?)
           │
           ▼
       WARUNEK (IF)
    (Czy spełniony X?)
      /         \
    TAK          NIE
     │            │
  AKCJA A      AKCJA B
```

**Trigger:** Nowy email, formularz, harmonogram, webhook, zmiana w bazie
**Akcja:** Wyślij email, zapisz dane, wywołaj API, wyślij powiadomienie
**Warunek:** Jeśli wartość X jest większa/mniejsza/równa Y

> 🎙️ NOTATKA: Narysuj ten diagram ręcznie na tablicy lub pokaż animację w Canva. Fizyczny gest (rysowanie) lepiej zapada w pamięć niż statyczny slajd. Wróć do tego diagramu w demonstracji live.

---

## Slajd 16: Przykład procesu rozłożonego na trigger/akcja/warunek

**Proces: Obsługa nowego leada z formularza**

**TRIGGER:** Formularz na stronie wypełniony
  ↓
**AKCJA 1:** Zapisz dane do arkusza Google / CRM
  ↓
**AKCJA 2:** Wyślij email powitalny do klienta
  ↓
**WARUNEK:** Czy budżet > 10 000 PLN?
  ├── TAK → Powiadom Kacpra na Slack + zaplanuj call w Calendly
  └── NIE  → Wyślij do nurturing sequence w MailerLite

**W n8n:** każdy krok = jeden node. Strzałka = połączenie.

> 🎙️ NOTATKA: Pokaż że to dokładnie ten diagram który przed chwilą rysowali. Teoria staje się praktyką w ciągu 60 sekund. To jest eureka moment.

---

## Slajd 17: Setup — Decision tree (kiedy co wybrać)

```
Chcę zacząć z n8n
         │
    ┌────┴────┐
    │Testuję  │ Mam klienta/
    │lokalnie │ prawdziwe dane
    └────┬────┘      │
         │     ┌─────┴─────┐
    Docker     │ Mam VPS   │ Nie mam VPS
    lokalnie   │ (Linux)   │ / DevOps
    port 5678  └─────┬─────┘     │
                     │      n8n Cloud
               Self-hosted      (trial darmowy,
               n8n (Docker      potem $20/mies.)
               na VPS)
```

> 🎙️ NOTATKA: Przejdź przez każdą ścieżkę. Mów do różnych grup: "Jeśli jesteś freelancerem testującym — Docker lokalnie. Jeśli robisz to dla klienta — Cloud lub VPS." Różni uczestnicy, różne potrzeby.

---

## Slajd 18: Docker — instalacja w jednej komendzie

**Wymagania:**
- Docker Desktop (Mac/Windows) lub Docker Engine (Linux)
- Port 5678 wolny

**Komenda:**
```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  docker.n8n.io/n8nio/n8n
```

**Potem:** otwórz `http://localhost:5678` w przeglądarce

**Czas:** ~2 minuty (pierwsze pobranie obrazu: ~1-2 min, start: ~10 sek)

> 🎙️ NOTATKA: Pokaż terminal na żywo. Skopiuj komendę z notatek. Nie pisz z pamięci — pomyłka w live demo psuje zaufanie. Plik `04_Cwiczenia.md` zawiera pełną instrukcję krok po kroku dla uczestników.

---

## Slajd 19: Interfejs n8n — mapa terenu

*(Tutaj: screenshot interfejsu n8n z ponumerowanymi elementami)*

**1. Sidebar** — lista workflow, credentials, executions
**2. Canvas** — główna przestrzeń robocza (drag & drop)
**3. Node panel** — klikasz "+" żeby dodać nowy node
**4. Execution log** — co się wydarzyło, dane wejście/wyjście
**5. Run/Save** — uruchom i zapisz workflow

*Analogia:* Sidebar = szuflady biurka. Canvas = blat. Node panel = skrzynka narzędziowa.

> 🎙️ NOTATKA: Ten slajd to tylko orientacja — nie tłumacz każdej opcji menu. Mów: "Nie musisz teraz wszystkiego zapamiętać. Za chwilę zobaczysz to na żywo i samo wpadnie."

---

## Slajd 20: Demo — Workflow Hello Automation

**Co budujemy:**
`Webhook → Parse JSON → Gmail (email powitalny)`

**Co pokazuje:**
- Jak odebrać dane z zewnątrz (webhook)
- Jak przetworzyć dane (Set node / Expressions)
- Jak wysłać email przez integrację (Gmail OAuth2)

**Wynik:** Wysyłasz HTTP request → osoba dostaje spersonalizowany email

*Czas budowania na żywo: ~8 minut (z komentarzem)*

> 🎙️ NOTATKA: Ten slajd jest przejściem do demo na żywo. Pokaż go, powiedz "To budujemy. Gotowy? Zaczynamy." — i przeskocz do n8n. Nie tłumacz za dużo przed demo. Demo tłumaczy samo.

---

## Slajd 21: Podsumowanie Modułu 0

**Dzisiaj nauczyłeś się:**

✅ Automatyzacja = procesy opisywalne krok po kroku
✅ n8n: self-hosted, RODO-friendly, bez vendor lock-in, tańszy
✅ Framework: Trigger → Akcja → Warunek (dotyczy każdego workflow)
✅ Setup: Docker lokalnie lub n8n Cloud
✅ Zbudowałeś pierwszy workflow (webhook → email)

**To był Moduł 0. W pełnym kursie:**
→ API REST i webhooks (głęboko)
→ AI nodes: GPT, Claude, Whisper
→ Autonomous agents i RAG
→ Bezpieczeństwo i produkcyjne deployments

> 🎙️ NOTATKA: Mów z energią. To jest zamknięcie pętli otwartej na początku. "Obiecałem Ci 5 rzeczy — oto potwierdzenie że to dostarczyłem."

---

## Slajd 22: CTA — Co dalej?

**Jeśli ten moduł był wartościowy:**

🔗 **Pełny kurs:** [link do strony zapisu]

**Co jest w kursie:**
- 7 modułów + 2 bonusy
- ~8 godzin materiału
- Projekty z prawdziwych klientów Dokodu
- Dostęp dożywotni + aktualizacje
- Społeczność (Discord)

**Dla kogo:**
✅ Właściciel firmy / agencji który chce automatyzować
✅ Freelancer który chce oferować automatyzacje
✅ Developer który chce szybko budować pipelines

> 🎙️ NOTATKA: Nie czytaj slajdu. Powiedz to swoimi słowami. Zakończ tak: "Do zobaczenia w Module 1 — tam zaczynamy od API i webhooków. Serio." I urwij. Bez długiego pożegnania.
