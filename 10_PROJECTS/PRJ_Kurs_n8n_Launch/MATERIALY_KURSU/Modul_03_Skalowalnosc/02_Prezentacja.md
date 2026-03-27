---
type: kurs-prezentacja
modul: 03
slajdow: 38
status: draft
last_reviewed: 2026-03-27
---

# Tydzień 3: Skalowalność, Odporność i Disaster Prevention
## Prezentacja — 38 slajdów

---

## Slajd 1: Tytuł
**Tydzień 3: Skalowalność, Odporność i Disaster Prevention**
*n8n + AI dla Agencji i Firm — Kacper Sieradzinski*

> 🎙️ NOTATKA: "Witajcie w trzecim tygodniu kursu. Jeśli doszliście do tego miejsca — gratulacje, macie już działające workflow. Teraz nauczę was jak je utwardzić tak, żeby działały w produkcji bez patrzenia na nie przez tygodnie."

---

## Slajd 2: Problem (emocjonalny hook)
**Twój workflow działa pięknie w piątek.**
**W poniedziałek rano klient dzwoni z pretensjami.**

- API zewnętrzne zwróciło błąd o 3 w nocy
- Webhook dostał to samo zamówienie dwa razy → 2 faktury
- 1000 rekordów → n8n się zawiesiło po 200
- Nikt nie wiedział, że coś padło przez 8 godzin

> 🎙️ NOTATKA: "Każda z tych sytuacji to coś, co widziałem u klientów Dokodu. To nie są edge cases. To norma na produkcji. Dzisiaj nauczymy się jak temu zapobiegać — i jak reagować gdy już się stanie."

---

## Slajd 3: Analogia — Budowanie Mostu
**Inżynierowie mostów nie zakładają, że most będzie stał.**
**Zakładają, że coś się stanie — i projektują na to.**

- Nadmiarowe liny (redundancja)
- Dylatacje termiczne (elastyczność)
- Inspekcje co 6 miesięcy (monitoring)
- Plany ewakuacyjne (disaster recovery)

**Twoje workflow to most. Zaprojektuj je tak samo.**

> 🎙️ NOTATKA: "Ta analogia zmienia sposób myślenia. Zamiast pytać 'czy mój workflow padnie?' — pytaj 'kiedy padnie i co się wtedy stanie?'. To jest disaster recovery mindset."

---

## Slajd 4: Plan na dziś (roadmap)
**Czego się nauczysz w Tygodniu 3:**

1. Batching — przetwarzaj tysiące rekordów bez crashu
2. Idempotency — workflow bezpieczne do wielokrotnego uruchomienia
3. Error Trigger — globalny handler błędów
4. Retry + Backoff — automatyczne ponowne próby
5. Wait Node — pauzy i scheduled retries
6. Monitoring — wiesz że coś padło, zanim klient zadzwoni
7. Logging — pełna historia wykonań
8. Testing — testuj bez produkcyjnych danych
9. **Projekt:** Armored Invoicing System

> 🎙️ NOTATKA: "Dużo materiału. Ale każdy element zbudujemy razem, krok po kroku. Na końcu złożysz to w jeden system fakturowania, który będzie produkcyjnie odporny."

---

## Slajd 5: Batching — Dlaczego to ważne
**Co się dzieje gdy workflow nie ma batching:**

- 1000 rekordów → n8n ładuje wszystko do pamięci RAM
- Przy 500 rekordach: timeout (domyślnie 1h w n8n)
- Przy 1000 rekordach: crash procesu lub timeout API
- Efekt: żadne dane nie zostają przetworzone

**Z batchingiem:**
- Przetwarzaj 50 rekordów → zapisz → przetwarzaj kolejne 50
- Jeśli błąd w batchu 7 → batch 1-6 już zapisane
- Możesz wznawiać od miejsca awarii

> 🎙️ NOTATKA: "Kluczowe słowo to 'checkpoint'. Batching to nie tylko kwestia pamięci — to kwestia możliwości wznowienia po błędzie."

---

## Slajd 6: SplitInBatches — Anatomia Node'a
**Parametry SplitInBatches:**

| Parametr | Wartość | Opis |
|----------|---------|------|
| Batch Size | 50–200 | Ile rekordów na raz |
| Options → Reset | true/false | Resetuj przy każdym uruchomieniu |

**Jak działa pętla:**
```
Input: 1000 rekordów
↓
SplitInBatches (size: 100)
↓
[Batch 1: 0-99] → procesuj → [Batch 2: 100-199] → ...
↓
Po ostatnim batchu: context.$batchIndex === last
```

> 🎙️ NOTATKA: "Pokażę to zaraz w demie. Ważne: SplitInBatches tworzy pętlę wewnątrz workflow — nie musisz robić osobnego workflow per rekord."

---

## Slajd 7: Optimal Batch Size — Tabela
**Jak dobrać rozmiar batcha:**

| Scenariusz | Rekomendowany rozmiar | Dlaczego |
|------------|----------------------|----------|
| Proste transformacje danych | 200–500 | Szybko, mało API calls |
| HTTP Request do zewnętrznego API | 20–50 | Rate limiting API |
| Generowanie AI (GPT, Claude) | 5–10 | Koszt + timeout modelu |
| Zapis do bazy danych | 100–200 | Bulk insert efektywny |
| Email wysyłka | 10–20 | Anti-spam limits |

> 🎙️ NOTATKA: "Nie ma jednej magicznej liczby. Testuj. Zacznij od 50 i sprawdź logi n8n — czas wykonania, error rate."

---

## Slajd 8: DIAGRAM — Co się dzieje bez vs z Batchingiem
```
BEZ BATCHING:
[1000 rekordów] → [Jeden wielki node] → 💥 TIMEOUT / CRASH
                                          ↓
                                    Zero rekordów przetworzone

Z BATCHINGIEM:
[1000 rekordów] → [Batch 1: 1-100] → ✅ zapisane
                → [Batch 2: 101-200] → ✅ zapisane
                → [Batch 3: 201-300] → ❌ BŁĄD
                                        ↓
                              Tylko batch 3 do powtórzenia
                              Batch 1-2 bezpieczne
```

> 🎙️ NOTATKA: "To jest fundamentalna różnica. Z batchingiem błąd to problem lokalny, nie katastrofa globalna."

---

## Slajd 9: Idempotency — Co to jest
**Idempotency = operacja którą można wykonać wiele razy z tym samym efektem**

Przykłady idempotentnych operacji:
- Ustaw pole X na wartość Y (zawsze ten sam efekt)
- Wstaw rekord JEŚLI NIE ISTNIEJE (duplicate safe)

Przykłady nieindempotentnych operacji:
- Dodaj 10 PLN do salda (za każdym razem inny efekt)
- Wystaw fakturę (2 wywołania = 2 faktury)
- Wyślij email (2 wywołania = 2 emaile)

**Dlaczego webhook może przyjść 2 razy:**
- Shopify/WooCommerce ma retry przy braku odpowiedzi 200
- Twoje n8n odpowie 200, ale potem crashnie w środku
- Shopify nie wie, że n8n coś zrobił — wyśle ponownie

> 🎙️ NOTATKA: "To jest pułapka na którą wpada 95% ludzi. Twoje API klienta nie jest głupie — ono zakłada że możesz nie odpowiedzieć i ponawia próbę. I ma rację."

---

## Slajd 10: DIAGRAM — Idempotency Flow
```
Webhook przychodzy z order_id: ORD-12345
              ↓
  ┌──────────────────────────────┐
  │  SPRAWDŹ czy ORD-12345       │
  │  istnieje w tabeli "processed" │
  └──────────────────────────────┘
         ↓               ↓
      NIE ISTNIEJE    JUŻ ISTNIEJE
         ↓               ↓
    WYKONAJ          POMIŃ (zwróć 200)
    operację         bez działania
         ↓
    OZNACZ jako
    przetworzone
    (zapisz ORD-12345)
         ↓
    Zwróć 200 OK
```

> 🎙️ NOTATKA: "Trzy kroki: Sprawdź. Wykonaj. Oznacz. W tej kolejności zawsze. Jeśli crashniesz między Wykonaj a Oznacz — następna próba ponowi operację. Więc operacja musi być idempotentna z natury LUB musisz to jakoś obsłużyć."

---

## Slajd 11: Idempotency — Klucze deduplication
**Jak wybrać klucz deduplication:**

| Źródło | Klucz | Przykład |
|--------|-------|---------|
| WooCommerce | order_id | "wc_12345" |
| Shopify | order.id | "shopify_4291847" |
| Email webhook | message_id | "msg_abc123" |
| Form submission | submission_id + timestamp | "form_2026-03-27T10:00:00Z" |
| Własny system | UUID v4 generowany po stronie klienta | "550e8400-e29b..." |

**Gdzie przechowywać processed keys:**
- Google Sheets (proste, wolne przy >10K rekordów)
- Airtable (wygodne, API limits)
- Redis (najszybsze, wymaga serwera)
- Postgres/MySQL (production grade)

> 🎙️ NOTATKA: "Na start Google Sheets wystarczy. Przy dużym ruchu przejdź na Redis — n8n ma natywny node Redis."

---

## Slajd 12: Error Trigger — Architektura
**Jak działa globalny error handler w n8n:**

```
Workflow A (normalny) ──────────────────→ ✅ sukces
                         \
                          └─[BŁĄD]──→ Error Trigger Workflow
                                            ↓
                                     1. Log do Sheets
                                     2. Alert Slack
                                     3. Ticket w systemie
                                     (opcjonalnie: retry)

Workflow B (normalny) ──────────────────→ ✅ sukces
                         \
                          └─[BŁĄD]──→ Error Trigger Workflow (ten sam!)
```

**Jeden Error Workflow obsługuje WSZYSTKIE twoje workflow.**

> 🎙️ NOTATKA: "To jest mega wygodne. Zamiast budować error handling w każdym workflow osobno — masz jeden centralny punkt. Jak CRM dla błędów."

---

## Slajd 13: Error Trigger — Co wiesz o błędzie
**Dane dostępne w Error Trigger node:**

```javascript
// $json zawiera:
{
  "execution": {
    "id": "1234",
    "url": "https://twoj-n8n.com/workflow/5/executions/1234",
    "error": {
      "message": "Connection timeout",
      "stack": "Error: ..."
    },
    "mode": "trigger",        // jak było uruchomione
    "retryOf": null           // jeśli to retry
  },
  "workflow": {
    "id": "5",
    "name": "Armored Invoicing"
  }
}
```

> 🎙️ NOTATKA: "Masz URL do konkretnego wykonania! Możesz go kliknąć z Slacka i od razu zobaczyć co się stało. Bezcenne przy debuggowaniu."

---

## Slajd 14: Error Trigger — Konfiguracja krok po kroku
**Jak skonfigurować globalny Error Handler:**

1. Stwórz nowy workflow: "🚨 Global Error Handler"
2. Dodaj node: **Error Trigger** (jako trigger)
3. Dodaj logikę:
   - `Set` node — sformatuj wiadomość alertu
   - `Slack` node — wyślij do kanału #n8n-alerts
   - `Google Sheets` node — dopisz do error log
4. Wejdź w **Settings** każdego workflow produkcyjnego
5. W polu **"Error Workflow"** wybierz "🚨 Global Error Handler"

> 🎙️ NOTATKA: "Krok 4 i 5 jest często pomijany. Pamiętajcie: Error Workflow musi być explicite podpięty w ustawieniach każdego workflow. To nie jest automatyczne dla wszystkich."

---

## Slajd 15: Retry Logic — Kiedy co robić
**Tabela decyzyjna: Retry vs Fail Fast vs Dead Letter Queue**

| Sytuacja | Strategia | Dlaczego |
|----------|-----------|---------|
| API timeout (503, 504) | Retry z backoffem | Tymczasowy problem serwera |
| Rate limit (429) | Retry z dłuższym czekaniem | Poczekaj i spróbuj znów |
| Błąd autentykacji (401, 403) | Fail fast | Retry nic nie zmieni |
| Zły format danych (400) | Fail fast + alert | Bug w danych źródłowych |
| Błąd sieciowy (ECONNRESET) | Retry 3x | Chwilowa niestabilność |
| Baza danych niedostępna | Dead Letter Queue | Długa awaria, przetwórz później |
| Błąd logiki biznesowej | Fail fast + manual review | Wymaga człowieka |

> 🎙️ NOTATKA: "Zasada kciuka: jeśli retry jest bezsensowny — nie rób retry. Retry przy błędzie 401 to tylko marnowanie zasobów."

---

## Slajd 16: Exponential Backoff — Teoria
**Dlaczego nie retry co sekundę:**

Problem: 10 serwisów retryuje co sekundę po awarii → 10x więcej ruchu → serwer nie wstaje

**Exponential Backoff z Jitter:**
```
Próba 1: czekaj 1s + losowe 0-1s
Próba 2: czekaj 2s + losowe 0-2s
Próba 3: czekaj 4s + losowe 0-4s
Próba 4: czekaj 8s + losowe 0-8s
MAX: 32s (cap)
```

**Jitter** = losowy składnik, żeby serwisy nie retryowały jednocześnie

> 🎙️ NOTATKA: "AWS, Google, Stripe — wszyscy używają exponential backoff z jitter. To jest przemysłowy standard, nie rocket science."

---

## Slajd 17: Retry w n8n — Dwa Podejścia
**Podejście 1: Natywny retry w node settings**
- Prawy klik na node → "Settings" → "Retry on fail"
- Prosto, ale brak kontroli nad backoffem
- Dobre dla szybkich, prostych przypadków

**Podejście 2: Custom retry loop**
```
[HTTP Request] ──→ [IF: sukces?] ──Yes──→ [dalej]
      ↑                  │
      │                 No
      │                  ↓
      │           [Set: retryCount++]
      │                  ↓
      │           [IF: retryCount < 3] ──No──→ [Error Handler]
      │                  │
      │                 Yes
      │                  ↓
      └────────── [Wait: 2^retryCount sekundy]
```

> 🎙️ NOTATKA: "Custom loop daje pełną kontrolę. Możesz zmieniać strategię backoffu, logować każdą próbę, reagować różnie na różne kody HTTP."

---

## Slajd 18: Wait Node — Typy
**Wait node w n8n — trzy tryby:**

| Tryb | Kiedy używać | Przykład |
|------|-------------|---------|
| **Fixed amount** | Poczekaj X sekund/minut | Poczekaj 30s przed retry |
| **At specified time** | Poczekaj do konkretnej daty/godziny | Wyślij o 9:00 rano |
| **Until webhook call** | Poczekaj na zewnętrzne zdarzenie | Czekaj na zatwierdzenie przez człowieka |

**Uwaga na timeout:** n8n domyślnie kończy wykonanie po 1h. Dla długich Wait — sprawdź ustawienia `executions.timeout` w config.

> 🎙️ NOTATKA: "Wait node to klucz do 'human in the loop'. Workflow może czekać godzinami na zatwierdzenie i wznowić się automatycznie po kliknięciu linku."

---

## Slajd 19: Monitoring — Disaster Recovery Mindset
**Zmień pytanie:**
~~"Czy moje workflow padnie?"~~
**"Kiedy padnie i skąd będę wiedział?"**

**Trzy poziomy alertów:**

| Poziom | Przykład | Kanał |
|--------|---------|-------|
| 🔴 Krytyczny | Faktura nie wystawiona | Slack + SMS |
| 🟡 Ostrzeżenie | API wolniejsze niż zwykle | Slack |
| 🔵 Info | Dzienny raport | Email |

**Zasada:** Dowiesz się o problemie przed klientem, nie po jego telefonie.

> 🎙️ NOTATKA: "To jest definicja dojrzałości operacyjnej. Nie budzić się od telefonu klienta — budzić się od własnego alertu."

---

## Slajd 20: Monitoring — Co Monitorować
**Kluczowe metryki dla workflow produkcyjnych:**

- **Success Rate:** % wykonań zakończonych sukcesem (cel: >99%)
- **Error Rate:** liczba błędów / dzień / workflow
- **Execution Time:** czas wykonania (jeśli nagle rośnie — coś jest nie tak)
- **Queue Depth:** ile executions czeka (jeśli rośnie — bottleneck)
- **Last Successful Run:** kiedy ostatnio sukces (idealny dla cron-workflow)

**Gdzie to zbierać:**
- n8n API: `GET /executions` z filterami
- External DB (Postgres, Airtable)
- Gotowe narzędzia: Grafana + n8n, Datadog, UptimeRobot

> 🎙️ NOTATKA: "Na start wystarczy Google Sheets i cron job co noc. Nie musisz od razu Grafany."

---

## Slajd 21: Logging Standard — Struktura Logu
**Każde wykonanie powinno logować:**

```json
{
  "timestamp": "2026-03-27T10:15:33Z",
  "workflow_name": "Armored Invoicing",
  "execution_id": "n8n_exec_1234",
  "status": "success",            // success | error | partial
  "order_id": "ORD-12345",        // klucz biznesowy
  "duration_ms": 3420,
  "error_message": null,
  "error_node": null,
  "retry_count": 0,
  "environment": "production"     // staging | production
}
```

> 🎙️ NOTATKA: "Ten format to standard Dokodu. Każdy log musi mieć klucz biznesowy — tu order_id. Bez tego nie możesz odpowiedzieć na pytanie 'co się stało z zamówieniem klienta X?'"

---

## Slajd 22: Logging — Sub-workflow Pattern
**Nie duplikuj kodu logowania — stwórz sub-workflow:**

```
Workflow A → [Execute Workflow: Log Entry] → kontynuuj
Workflow B → [Execute Workflow: Log Entry] → kontynuuj
Workflow C → [Execute Workflow: Log Entry] → kontynuuj

[Log Entry Sub-workflow]:
  Input → Validate → Format → Write to Sheets/DB → Return
```

**Zalety:**
- Jeden punkt zmiany (dodasz Postgres jutro — zmienisz w jednym miejscu)
- Consistent format we wszystkich workflow
- Łatwe testowanie

> 🎙️ NOTATKA: "To jest DRY principle w n8n — Don't Repeat Yourself. Logowanie to infrastruktura, nie feature."

---

## Slajd 23: Testing — Środowisko Staging vs Produkcja
**Problem:** Nie możesz testować na produkcji.

**Rozwiązanie: Oddzielne środowiska w n8n**

| Aspekt | Staging | Produkcja |
|--------|---------|-----------|
| URL | n8n-staging.twojadomena.com | n8n.twojadomena.com |
| Credentials | Testowe API keys | Prawdziwe API keys |
| Webhooks | Oddzielne URL | Oddzielne URL |
| Dane | Syntetyczne/testowe | Realne dane klientów |
| Error alerts | Do #n8n-staging w Slack | Do #n8n-alerts |

**Minimum viable staging:** Osobny folder workflow + testowe credentials w tym samym n8n

> 🎙️ NOTATKA: "Na początku nie musisz mieć osobnego serwera. Wystarczy osobne credentials i naming convention: 'DEV_' prefix na workflow testowych."

---

## Slajd 24: Testing — Techniki Testowania w n8n
**4 techniki testowania workflow:**

1. **Manual Trigger + Static JSON** — symuluj webhook bez prawdziwego ruchu
2. **Pinned Data** — przypnij przykładowe dane do node'a (prawy klik → "Pin Data")
3. **Test webhook** — n8n ma tryb "Test" dla webhook triggerów
4. **Partial execution** — uruchom od wybranego node'a (Ctrl+klik)

**Scenariusze do przetestowania:**
- Happy path: wszystko działa
- API timeout: serwer nie odpowiada
- Bad data: null, puste stringi, nieprawidłowy format
- Duplicate: ten sam payload 2x
- Large volume: 1000 rekordów

> 🎙️ NOTATKA: "Pinned Data to mój ulubiony feature. Możesz 'zamrozić' dane z jednego uruchomienia i testować resztę workflow wielokrotnie bez wywoływania API."

---

## Slajd 25: Projekt — Armored Invoicing System
**Co zbudujesz:**

```
[Webhook: Nowe Zamówienie]
         ↓
[Idempotency Check: czy już przetworzono?]
         ↓
[Pobierz dane: klient + zamówienie]
         ↓
[Generuj Fakturę: API iFaktury/Fakturownia]  ←── 3x retry + backoff
         ↓
[Wyślij Email do Klienta]
         ↓
[Zaktualizuj CRM/Sheets]
         ↓
[Oznacz jako Przetworzone: idempotency]
         ↓
[Log: zapis do error/success log]
```

**+ Error Handler Workflow** (globalny)
**+ Batch Mode** dla importu historycznych zamówień

> 🎙️ NOTATKA: "To jest workflow klasy produkcyjnej. Nie skrypt który działa na demo — system który możesz wdrożyć u klienta i spać spokojnie."

---

## Slajd 26: Armored Invoicing — Moduły
**Architektura modułowa systemu:**

| Moduł | Opis | Typ |
|-------|------|-----|
| Main Invoicing Workflow | Główna logika | Webhook trigger |
| Error Handler | Globalny handler błędów | Error trigger |
| Log Entry | Sub-workflow logowania | Execute Workflow |
| Idempotency Check | Sprawdź/oznacz przetworzone | Execute Workflow |
| Invoice Generator | Wrapper na API fakturowe | Execute Workflow |
| Batch Processor | Tryb wsadowy dla >100 zamówień | Schedule trigger |

> 🎙️ NOTATKA: "Modułowość to temat Tygodnia 4, ale tu już ją stosujemy. Każdy sub-workflow możesz testować osobno i wielokrotnie używać."

---

## Slajd 27: Error Handling Matrix
**Co się dzieje przy każdym typie błędu:**

| Błąd | Akcja natychmiastowa | Po 3 próbach | Alert |
|------|---------------------|-------------|-------|
| API fakturowe timeout | Retry backoff | Slack + Ticket | 🔴 Krytyczny |
| Email SMTP fail | Retry 2x | Log + manual | 🟡 Ostrzeżenie |
| CRM niedostępne | Retry 3x | Pomiń, log | 🔵 Info |
| Zły format danych | Fail fast | Log szczegóły | 🟡 Ostrzeżenie |
| Duplikat zamówienia | Pomiń (idempotency) | — | 🔵 Info |
| Autentykacja fail | Fail fast | Alert natychmiast | 🔴 Krytyczny |

> 🎙️ NOTATKA: "Ta macierz to dokument dla klienta. Kiedy wdrażasz system — dajesz im tę tabelę i mówią 'rozumiem co się dzieje'. To buduje zaufanie."

---

## Slajd 28: 5 Zasad Armored Workflow
**Checklista przed wdrożeniem produkcyjnym:**

1. **Idempotency** — workflow bezpieczny na wielokrotne uruchomienie
2. **Error Handler** — podpięty Error Workflow z alertem
3. **Retry Logic** — automatyczne ponowne próby dla tymczasowych błędów
4. **Logging** — każde wykonanie pozostawia ślad
5. **Monitoring Alert** — wiesz o problemie przed klientem

Jeśli brakuje któregoś z tych 5 — workflow nie jest gotowy na produkcję.

> 🎙️ NOTATKA: "Zapamiętajcie tę listę. Przed każdym wdrożeniem u klienta przejdź przez te 5 punktów. Jeśli coś brakuje — nie wdrażaj."

---

## Slajd 29: Przypadek Użycia — Agencja E-commerce
**Przykład z życia: Agencja obsługująca sklep 200 zamówień/dzień**

**Przed:**
- Ręczne wystawianie faktur: 2h/dzień
- 3x w miesiącu duplikat faktury (ręczna korekta)
- Klient dzwonił bo nie dostał faktury → 30 min debugowania

**Po wdrożeniu Armored Invoicing:**
- 0h/dzień na faktury
- 0 duplikatów (idempotency)
- Alert na Slack zanim klient zadzwoni
- ROI: 40h/miesiąc zaoszczędzone = ~4000 PLN wartości

> 🎙️ NOTATKA: "To jest szablon case study który możecie pokazać swoim klientom. Zamień liczby na ich specyfikę i masz gotowy argument sprzedażowy."

---

## Slajd 30: Code — Idempotency Check (JS)
**Kod do sprawdzenia duplikatu:**

```javascript
// W Function node lub Code node
const orderId = $input.item.json.order_id;
const processedOrders = $('Google Sheets').all();

const alreadyProcessed = processedOrders.some(
  row => row.json.order_id === orderId
);

if (alreadyProcessed) {
  // Zwróć specjalny flag zamiast rzucać błąd
  return [{ json: { skip: true, order_id: orderId, reason: 'duplicate' } }];
}

return [{ json: { skip: false, order_id: orderId } }];
```

> 🎙️ NOTATKA: "Zwracamy skip:true zamiast rzucać błąd. Duplikat to nie błąd — to oczekiwana sytuacja. W następnym IF node filtrujemy po skip."

---

## Slajd 31: Code — Exponential Backoff (JS)
**Kod do obliczenia czasu czekania:**

```javascript
// W Code node przed Wait node
const retryCount = $input.item.json.retryCount || 0;
const baseDelay = 1000; // 1 sekunda
const maxDelay = 32000; // max 32 sekundy

// Exponential: 1s, 2s, 4s, 8s, 16s, 32s
const exponential = Math.pow(2, retryCount) * baseDelay;

// Jitter: losowe 0-25% dodatkowego czasu
const jitter = Math.random() * exponential * 0.25;

const waitMs = Math.min(exponential + jitter, maxDelay);

return [{
  json: {
    ...($input.item.json),
    retryCount: retryCount + 1,
    waitSeconds: Math.round(waitMs / 1000)
  }
}];
```

> 🎙️ NOTATKA: "Ten kod kopiujcie 1:1. Jest przetestowany w produkcji u kilku klientów Dokodu. Jitter zapobiega 'thundering herd' — sytuacji gdy wszystkie retry uderzają jednocześnie."

---

## Slajd 32: Monitoring — Dzienny Raport (template)
**Szablon raportu emailowego:**

```
🔄 n8n Daily Report — 2026-03-27

📊 Statystyki:
- Executions: 847
- ✅ Sukces: 834 (98.5%)
- ❌ Błędy: 13 (1.5%)
- ⏱️ Avg execution time: 2.3s

🚨 Top błędy:
1. "Armored Invoicing" — API timeout (8x)
2. "CRM Sync" — Auth error (3x)
3. "Email Notifier" — SMTP limit (2x)

📈 Trend: sukces rate wzrósł o 0.3% vs wczoraj

[Link do n8n dashboard]
```

> 🎙️ NOTATKA: "Ten raport wysyłacie sobie i klientowi. Klient widzi że macie system pod kontrolą. To jest feature, nie obowiązek."

---

## Slajd 33: Staging vs Produkcja — Naming Convention
**Prosta konwencja bez osobnego serwera:**

| Typ | Prefix | Przykład |
|-----|--------|---------|
| Workflow produkcyjny | brak | "Armored Invoicing" |
| Workflow staging/dev | [DEV] | "[DEV] Armored Invoicing" |
| Sub-workflow | brak + jasna nazwa | "Sub: Log Entry" |
| Error handler | 🚨 | "🚨 Global Error Handler" |
| Cron/monitoring | 📊 | "📊 Daily Report" |

**Credentials:** Dwa zestawy — "Fakturownia PROD" i "Fakturownia TEST"

> 🎙️ NOTATKA: "Prosty system ale ratuje życie. Nigdy nie uruchomisz przypadkowo [DEV] workflow na produkcji bo natychmiast widzisz prefix."

---

## Slajd 34: Anti-patterns — Czego Nie Robić
**Top 5 błędów które widzę u klientów:**

1. ❌ **Catch-all error handler bez logowania** — wiesz że był błąd, nie wiesz jaki
2. ❌ **Retry bez limitu** — nieskończona pętla blokuje kolejkę
3. ❌ **Batch size 1000** — traktuj to jak brak batchingu
4. ❌ **Idempotency key w RAM** — restarty n8n kasują pamięć
5. ❌ **Alerts na email który nikt nie czyta** — alert na Slack do kanału z people

> 🎙️ NOTATKA: "Każdy z tych błędów widziałem co najmniej 3 razy u różnych klientów. Nie musisz ich popełniać — uczcie się na cudzych błędach."

---

## Slajd 35: Checklist — Przed Wdrożeniem
**Production Readiness Checklist:**

- [ ] Idempotency check zaimplementowany
- [ ] Error Workflow podpięty w Settings
- [ ] Retry logic z limitem prób (max 3-5)
- [ ] Logging sub-workflow wywołany na sukces i błąd
- [ ] Alert Slack skonfigurowany (test: wyślij ręcznie)
- [ ] Staging przetestowany (happy path + error path)
- [ ] Batch size dobrany do typu operacji
- [ ] Timeout n8n sprawdzony vs oczekiwany czas wykonania
- [ ] Credentials oznaczone PROD vs TEST
- [ ] Dzienny raport skonfigurowany

> 🎙️ NOTATKA: "Skopiujcie tę checklistę. Używajcie przed każdym wdrożeniem. Klienci pytają 'czy to jest bezpieczne?' — wy macie checklistę z podpisami."

---

## Slajd 36: Zadanie Domowe
**Tydzień 3 — Zadanie:**

**Część obowiązkowa (Armored Invoicing):**
- Zbuduj workflow z idempotency check (Google Sheets jako lock table)
- Podłącz globalny Error Handler z alertem Slack
- Dodaj retry 3x dla API fakturowego (możesz używać mock HTTP endpoint)

**Część dodatkowa (+bonus):**
- Dodaj dzienny raport email z liczbą sukcesów/błędów
- Przetestuj duplikat webhooka — czy system go poprawnie odrzuca?
- Uruchom batch mode dla 50 testowych rekordów

**Termin:** Wrzuć do Community przed następną lekcją

> 🎙️ NOTATKA: "Część obowiązkowa zajmie ~60-90 minut. Część dodatkowa — kolejne 30 minut. Razem 2 godziny pracy i macie system klasy produkcyjnej."

---

## Slajd 37: Zasoby i Linki
**Materiały dodatkowe:**

- **n8n docs:** Error Workflow configuration → docs.n8n.io/error-handling
- **AWS whitepaper:** Exponential Backoff and Jitter (darmowy)
- **Blueprint:** Armored Invoicing — plik `05_Workflow_Blueprint.md` w materiałach kursu
- **Template:** Logging Standard Dokodu — `Logging_Standard.md`
- **Community n8n:** forum.n8n.io (template do pobrania: "Error Handler Starter")

> 🎙️ NOTATKA: "Wszystkie linki są w materiałach kursu. Nie musicie teraz nic zapisywać."

---

## Slajd 38: Tydzień 4 — Zapowiedź
**Następny tydzień: Architektura Modularna**

- Sub-workflows jako biblioteka wielokrotnego użytku
- Jak organizować duże projekty automatyzacyjne
- Execute Workflow node — synchroniczne vs asynchroniczne
- Wersjonowanie workflow
- **Projekt:** Modular CRM Automation (Pipedrive/HubSpot + 5 sub-workflow)

**Wymaganie wstępne:** Ukończony Armored Invoicing z Tygodnia 3

> 🎙️ NOTATKA: "Tydzień 4 to poziom zaawansowany — ale po tym co zrobiliście dzisiaj, będziecie gotowi. Do zobaczenia za tydzień."
