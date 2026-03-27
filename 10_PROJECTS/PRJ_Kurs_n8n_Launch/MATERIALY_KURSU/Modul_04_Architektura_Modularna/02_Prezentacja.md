---
type: kurs-prezentacja
modul: 04
tytul: "Architektura Modularna — Koniec z Chaosem"
liczba_slajdow: 32
last_updated: 2026-03-27
---

# Moduł 4: Prezentacja — 32 slajdy

---

## Slajd 1: Tytuł modułu

**Architektura Modularna**
**Koniec z Chaosem Workflow**

Moduł 4 z 8 — n8n + AI dla Agencji i Firm

> 🎙️ NOTATKA: Zaczynamy od pytania do widza — "Czy zdarzyło ci się otworzyć workflow, który sam zbudowałeś miesiąc temu i nie rozumieć, co on robi?" Poczekaj 2 sekundy. Prawie każdy tak ma. To właśnie rozwiązujemy dziś.

---

## Slajd 2: Co zbudujesz dziś

**Corporate Request Router — Firmowy Router Zgłoszeń**

- Trigger: email lub formularz z typem zgłoszenia
- AI klasyfikuje: IT / HR / Finance / Sales / Other
- Każda kategoria = osobny subworkflow
- Master zwraca potwierdzenie z numerem ticketu

**Czas budowy:** ~60 minut (po tym module)

> 🎙️ NOTATKA: Pokaż finalny efekt — screenshot lub krótkie demo gotowego routera. "Na koniec tego modułu zbudujesz dokładnie to. Zaczynamy."

---

## Slajd 3: Agenda modułu

1. Problem spaghetti workflow (10 min)
2. Filozofia architektury modularnej (15 min)
3. Execute Workflow node — demo (20 min)
4. Switch node i routing (15 min)
5. Konwencje i organizacja (30 min)
6. Projekt tygodnia — budujemy razem (55 min)
7. Ćwiczenia i zadanie domowe (25 min)

> 🎙️ NOTATKA: Przejdź przez agendę szybko, 15 sekund. Ludzie lubią wiedzieć gdzie są w materiale.

---

## Slajd 4: Problem — Spaghetti Workflow (PRZED)

```
[Webhook] → [HTTP] → [IF] → [Set] → [HTTP] → [Email] → [IF] → [Sheets]
               ↓                        ↓                   ↓
            [Set2]               [Slack]→[IF]→[HTTP]    [Email2]
               ↓                        ↓
            [Code]                   [Set3]
```

**Objawy spaghetti:**
- Niemożliwość zrozumienia bez autora
- Debug = Russian roulette (gdzie jest błąd?)
- Copy-paste tej samej logiki w 3 miejscach
- Zmiana jednej rzeczy psuje dwie inne

> 🎙️ NOTATKA: Pokaż prawdziwy screenshot z n8n — monolityczny workflow 25+ nodów z połączeniami przechodzącymi przez ekran. "Znacie to. Ja też tak budowałem. To normalne — dopóki nie wiesz, że jest lepszy sposób."

---

## Slajd 5: Problem — Spaghetti Workflow (PO)

```
[Webhook] → [AI Classifier] → [Switch]
                                  ├─ IT Support  → [Execute: WF_IT]   → [Merge]
                                  ├─ HR          → [Execute: WF_HR]   → [Merge]
                                  ├─ Finance     → [Execute: WF_FIN]  → [Merge]
                                  ├─ Sales       → [Execute: WF_SAL]  → [Merge]
                                  └─ Other       → [Execute: WF_OTH]  → [Merge]
                                                                           ↓
                                                                    [Send Confirmation]
```

**Efekty modularyzacji:**
- Każdy workflow ma jedną odpowiedzialność
- Debugujesz subworkflow w izolacji
- Zmieniasz logikę HR bez dotykania IT
- Nowy współpracownik rozumie w 5 minut

> 🎙️ NOTATKA: Daj chwilę na porównanie obu slajdów. "Przed i po. Obie architektury robią to samo. Ale tylko jedna jest utrzymywalna."

---

## Slajd 6: Cztery prawdziwe problemy monolitu

**1. Niemożliwość ponownego użycia**
→ Masz logikę "wyślij email potwierdzający" w 5 workflow. Zmiana formatu = 5 edycji.

**2. Piekło debugowania**
→ Błąd w Node 23 z 40. Który Node 23? Który output?

**3. Brak izolacji zmian**
→ Poprawiasz routing sprzedażowy, przez przypadek psujesz routing HR.

**4. Niemożliwość testowania**
→ Nie możesz uruchomić tylko "części" workflow. Musisz odpalić całość z prawdziwymi danymi.

> 🎙️ NOTATKA: Dla każdego problemu — 1-2 zdania przykładu z życia agencji. "Miałem klienta, który miał 15 wariantów tego samego emaila w różnych workflow..."

---

## Slajd 7: Heurystyka — kiedy modularyzować?

**Modularyzuj jeśli:**
- Workflow ma więcej niż 15 nodów
- Ta sama logika pojawia się w 2+ miejscach
- Zmiana jednej ścieżki nie powinna wpływać na inne
- Chcesz testować poszczególne kroki oddzielnie
- Pracujesz w zespole

**Zostaw inline jeśli:**
- Prosta sekwencja < 10 nodów
- Jednorazowy skrypt / eksperyment
- Brak powtarzalnej logiki
- Solo projekt, bardzo krótki lifecycle

> 🎙️ NOTATKA: "To nie jest dogmat. Architektura to narzędzie, nie religia. Stosuj tam, gdzie ma sens."

---

## Slajd 8: Analogia — Orkiestra i Dyrygent

**Master Workflow = Dyrygent**
- Zna partyturę (wie co i kiedy)
- Daje sygnał każdemu muzykowi
- Zbiera wyniki w spójną całość
- Sam nie gra na żadnym instrumencie

**Subworkflow = Muzyk**
- Specjalizuje się w jednym instrumencie
- Wykonuje zadanie na sygnał dyrygenta
- Zgłasza że skończył (return)
- Nie wie, co robi reszta orkiestry

> 🎙️ NOTATKA: "Dyrygent nie gra na skrzypcach — on koordynuje. Master workflow nie wysyła emaili — on wywołuje subworkflow, który to robi. To kluczowa różnica."

---

## Slajd 9: Architektura Master-Subworkflow

```
MASTER WORKFLOW
┌─────────────────────────────────┐
│  Trigger → Parse → Classify     │
│               ↓                 │
│           [Switch]              │
│         ↙    ↓    ↓    ↘       │
│  [Exec] [Exec] [Exec] [Exec]   │
│    ↓      ↓      ↓      ↓      │
│         [Merge Results]         │
│               ↓                 │
│        [Send Confirmation]      │
└─────────────────────────────────┘
         ↕ dane in/out ↕
SUBWORKFLOWS
┌──────────┐ ┌──────────┐ ┌──────────┐
│ WF: IT   │ │ WF: HR   │ │ WF: FIN  │
│ Support  │ │          │ │          │
└──────────┘ └──────────┘ └──────────┘
```

**Zasada komunikacji:**
- Master → Sub: JSON z danymi zgłoszenia
- Sub → Master: JSON z wynikiem (ticket_id, status, message)

> 🎙️ NOTATKA: Narysuj to też na tablicy lub w draw.io. Wizualizacja jest kluczowa dla zrozumienia przepływu danych.

---

## Slajd 10: Execute Workflow Node — Anatomy

**Lokalizacja:** Action in app → n8n → Execute Workflow

**Kluczowe parametry:**
| Parametr | Opis | Przykład |
|---|---|---|
| Workflow | ID lub nazwa | `WF_IT_Support` |
| Mode | synchronous / async | synchronous (czekamy na wynik) |
| Input Data | JSON do przekazania | `{{ $json }}` |
| Wait for finish | true/false | true (chcemy return) |

**Kiedy async?**
- Długie operacje (>30s)
- Fire-and-forget (nie czekamy na wynik)
- Równoległe wykonanie wielu subworkflowów

> 🎙️ NOTATKA: Przejdź do n8n i pokaż na żywo jak wygląda node w UI. "Zamiast slajdu — zobaczmy to w akcji."

---

## Slajd 11: Subworkflow Trigger — "When Called"

**Trigger do użycia:** `When Called by Another Workflow`

**Co definiujemy:**
```json
{
  "inputFields": [
    {"name": "request_id", "type": "string", "required": true},
    {"name": "requester_email", "type": "string", "required": true},
    {"name": "description", "type": "string", "required": true},
    {"name": "priority", "type": "string", "required": false}
  ]
}
```

**Dlaczego definiować pola?**
- Dokumentacja dla przyszłego siebie
- Walidacja w n8n UI
- Jasny kontrakt = mniej błędów

> 🎙️ NOTATKA: "To jest 'interfejs' twojego subworkflow. Jak signature funkcji w programowaniu. Kto wywołuje, wie czego potrzebuje dostarczyć."

---

## Slajd 12: Return Node — Zwracanie Wyniku

**Return Data node** (ostatni w subworkflow):

```json
{
  "success": true,
  "ticket_id": "IT-2847",
  "message": "Zgłoszenie IT przekazane do zespołu. Odpowiedź w ciągu 4h.",
  "assigned_to": "it-support@firma.pl",
  "sla_hours": 4
}
```

**Zasady dobrego return:**
- Zawsze `success: true/false`
- Zawsze `message` czytelny dla end-usera
- `ticket_id` jeśli system to tworzy
- Nie zwracaj więcej niż potrzeba

> 🎙️ NOTATKA: "Master bierze ten JSON i używa go do wysyłki potwierdzenia użytkownikowi. Im lepszy return contract, tym prostszy master."

---

## Slajd 13: Switch Node — Intelligent Routing

**Switch vs IF:**
| | Switch | IF |
|---|---|---|
| Liczba ścieżek | 2–10+ | 2 (true/false) |
| Czytelność | Wysoka | Spada przy zagnieżdżeniu |
| Use case | Klasyfikacja | Prosty warunek binarny |

**Konfiguracja Switch:**
- Mode: Rules
- Wartość do sprawdzenia: `{{ $json.category }}`
- Case 1: `IT_Support` → output 1
- Case 2: `HR` → output 2
- Default: output 5 (Other)

> 🎙️ NOTATKA: "Zawsze ustaw Default. Nigdy nie zakładaj, że AI/logika nie może zwrócić nieoczekiwanej wartości. Default ratuje życie o 3 w nocy."

---

## Slajd 14: n8n Variables — Shared Configuration

**Problem bez Variables:**
```
URL serwisu hardcoded w 12 workflow
Zmiana URL = 12 edycji ręcznie
```

**Rozwiązanie: n8n Variables**
```
Ustawienia → Variables → Nowa zmienna
Nazwa: JIRA_BASE_URL
Wartość: https://firma.atlassian.net
```

**Użycie:**
```
{{ $vars.JIRA_BASE_URL }}/rest/api/2/issue
```

**Dobre kandydatury na Variables:**
- Base URL zewnętrznych systemów
- Adresy email zespołów (it@, hr@, fin@)
- SLA w godzinach per kategoria
- Flagi feature (np. `SEND_SMS: true`)

> 🎙️ NOTATKA: "Variables to centralne miejsce konfiguracji. Jak plik .env w programowaniu. Zmieniasz w jednym miejscu, działa wszędzie."

---

## Slajd 15: Naming Conventions — Workflow

**Format nazwy workflow:**
```
[ENV]_[OBSZAR]_[FUNKCJA]_v[X]
```

**Przykłady:**
```
PROD_Sales_Lead_Capture_v3
PROD_IT_Request_Handler_v1
PROD_HR_Onboarding_Notify_v2
DEV_Finance_Invoice_Process_v1
TEST_Master_Request_Router_v1
```

**Reguły:**
- ENV zawsze na początku: PROD / DEV / TEST
- OBSZAR: krótki, bez spacji
- FUNKCJA: czasownik + rzeczownik
- Wersja: tylko major zmiany logiki

> 🎙️ NOTATKA: "Kiedy masz 50 workflow i szukasz 'tego co obsługuje faktury', naming convention ratuje ci 10 minut za każdym razem."

---

## Slajd 16: Naming Conventions — Nody

**Zasada:** Każdy node musi mieć czytelną nazwę. Domyślna jest złem.

**Złe nazwy:**
```
HTTP Request, HTTP Request1, HTTP Request2
Set, Set1, Set2
IF, IF1
```

**Dobre nazwy:**
```
POST Ticket to Jira
GET Employee Data from HR System
IF: Priority is Urgent
Set: Prepare Confirmation Email Body
```

**Konwencja:**
```
[CZASOWNIK]: [CO + GDZIE/PO CO]
```

> 🎙️ NOTATKA: "Pokaż przed i po w n8n UI. Różnica w czytelności jest natychmiastowa. To 2 sekundy pracy, które oszczędzają minuty debugowania."

---

## Slajd 17: Folder Structure w n8n

**Rekomendowana struktura:**
```
📁 00_MASTER_WORKFLOWS/
   └─ PROD_Master_Request_Router_v2
   └─ PROD_Master_Lead_Processor_v1

📁 01_IT_Support/
   └─ PROD_IT_Request_Handler_v1
   └─ PROD_IT_Escalation_Alert_v1

📁 02_HR/
   └─ PROD_HR_Request_Handler_v1
   └─ PROD_HR_Onboarding_Welcome_v2

📁 03_Finance/
   └─ PROD_FIN_Request_Handler_v1

📁 04_Sales/
   └─ PROD_SAL_Request_Handler_v1
   └─ PROD_SAL_Lead_Notify_v3

📁 99_ARCHIVE/
   └─ [stare workflow - dezaktywowane]

📁 DEV/
   └─ [workflow w budowie]
```

> 🎙️ NOTATKA: "Foldery w n8n są pod Settings → Folders. Jeśli tego nie masz w swojej wersji — używaj prefixów w nazwach. Efekt ten sam."

---

## Slajd 18: Wersjonowanie w n8n

**Opcja 1: Tagi**
- Dodaj tag `v1`, `v2`, `stable`, `deprecated`
- Szybkie filtrowanie w UI

**Opcja 2: Historia zmian**
- n8n przechowuje historię wersji workflow
- Wróć do poprzedniej wersji: Workflow → ... → History
- Ogranicz do: pamiętaj o limicie historii w self-hosted

**Opcja 3: Export JSON (backup)**
```bash
# Eksport przez CLI n8n
n8n export:workflow --all --output=/backups/
# lub przez API
GET /api/v1/workflows/{id}
```

**Opcja 4: Git (advanced)**
- Export JSON → commit do repo
- CI/CD: automatyczny deploy workflow na staging/prod

> 🎙️ NOTATKA: "Minimum viable versioning: eksport JSON do folderu Dropbox/Drive co tydzień. Zaawansowani: Git. Absolutne minimum: tagi 'stable'."

---

## Slajd 19: Tabela decyzyjna — Subworkflow vs Inline

| Kryterium | Subworkflow | Inline Logic |
|---|---|---|
| Logika reużywalna w 2+ workflow | ✅ TAK | ❌ |
| Logika używana tylko raz | ❌ | ✅ TAK |
| Chcesz testować w izolacji | ✅ TAK | ❌ |
| < 5 nodów | ❌ | ✅ TAK |
| Różni właściciele (np. IT vs HR) | ✅ TAK | ❌ |
| Prosta sekwencja bez rozgałęzień | ❌ | ✅ TAK |
| Zmiana w jednym miejscu = zmiana wszędzie | ✅ TAK | ❌ |
| Prototyp / eksperyment | ❌ | ✅ TAK |

> 🎙️ NOTATKA: "Wydrukuj tę tabelę i przyklej przy monitorze. Naprawdę. Przez pierwsze miesiące będziesz do niej wracał."

---

## Slajd 20: Input/Output Contract — Standard

**Każdy subworkflow ma udokumentowany kontrakt:**

```markdown
## WF_IT_Support — Kontrakt

### INPUT (wymagane)
- request_id: string — unikalny ID zgłoszenia
- requester_email: string — email zgłaszającego
- description: string — treść zgłoszenia
- priority: string — "low" | "medium" | "high" | "urgent"

### OUTPUT (zawsze zwracane)
- success: boolean
- ticket_id: string — np. "IT-2847"
- message: string — komunikat dla użytkownika
- assigned_to: string — email osoby obsługującej
- sla_hours: number — czas odpowiedzi w godzinach

### BŁĘDY
- success: false, error: "JIRA_UNAVAILABLE"
- success: false, error: "INVALID_EMAIL"
```

> 🎙️ NOTATKA: "Kontrakt to umowa między master a subworkflow. Jak swagger API. Zapisuj go w sticky note bezpośrednio w workflow albo w osobnym dokumencie."

---

## Slajd 21: Projekt tygodnia — Architektura

```
CORPORATE REQUEST ROUTER
════════════════════════════════════════

[Email / Form Webhook]
         ↓
[Parse & Normalize Input]
         ↓
[AI: Classify Category]
   (GPT-4o-mini, structured output)
         ↓
[Switch: Route by Category]
    │
    ├── IT_Support  → [Execute: WF_IT_Support]
    │                      ↓
    │                 Jira Ticket + Email IT
    │
    ├── HR          → [Execute: WF_HR]
    │                      ↓
    │                 Google Sheets + Email HR Manager
    │
    ├── Finance     → [Execute: WF_Finance]
    │                      ↓
    │                 Google Sheets + Email CFO
    │
    ├── Sales       → [Execute: WF_Sales]
    │                      ↓
    │                 CRM Lead + Slack Handlowiec
    │
    └── Other       → [Execute: WF_Other]
                           ↓
                      Human Review Queue
         ↓
[Merge Results from all branches]
         ↓
[Send Confirmation Email to Requester]
(ticket_id, category, SLA, next steps)
```

> 🎙️ NOTATKA: "Mamy 6 workflow: 1 master + 5 subworkflowów. Każdy można budować niezależnie. Zaczynamy od subworkflowów, potem łączymy w master."

---

## Slajd 22: AI Classifier — Konfiguracja

**Node:** OpenAI (GPT-4o-mini) lub Anthropic

**Prompt systemowy:**
```
Jesteś klasyfikatorem zgłoszeń firmowych.
Przeanalizuj zgłoszenie i przypisz kategorię.

Kategorie:
- IT_Support: problemy techniczne, sprzęt, software, dostępy
- HR: urlopy, umowy, onboarding, benefity, rekrutacja
- Finance: faktury, rozliczenia, budżety, zwroty kosztów
- Sales: zapytania sprzedażowe, oferty, leady
- Other: wszystko poza powyższymi

Odpowiedz TYLKO nazwą kategorii. Bez wyjaśnień.
```

**Structured Output:**
```json
{"category": "IT_Support"}
```

> 🎙️ NOTATKA: "GPT-4o-mini jest wystarczający do prostej klasyfikacji. Tani (~$0.001 za klasyfikację), szybki. Nie przesadzaj z modelem do prostych zadań."

---

## Slajd 23: IT Support Subworkflow — Detale

**Wejście:** `request_id`, `requester_email`, `description`, `priority`

**Kroki:**
1. `Set: Prepare Jira Payload`
   - Mapowanie priority → Jira priority
   - Budowanie summary z description
2. `POST: Create Jira Issue`
   - Endpoint: `{{ $vars.JIRA_BASE_URL }}/rest/api/2/issue`
   - Authentication: API Token
3. `Send Email to IT Team`
   - To: `{{ $vars.IT_TEAM_EMAIL }}`
   - Subject: `[{{ $json.priority }}] Nowe zgłoszenie #{{ $json.ticket_id }}`
4. `Return: Confirmation`
   - success, ticket_id, message, sla_hours

**Czas realizacji:** < 3 sekundy

> 🎙️ NOTATKA: "Każdy subworkflow buduj i testuj oddzielnie. Dopiero gdy działa samodzielnie, wpisujesz go do mastera."

---

## Slajd 24: HR Subworkflow — Detale

**Wejście:** `request_id`, `requester_email`, `description`, `priority`

**Kroki:**
1. `Append Row to HR Requests Sheet`
   - Google Sheets: zakładka "Zgłoszenia HR"
   - Kolumny: ID, Data, Email, Opis, Status, Priorytet
2. `Send Email to HR Manager`
   - To: `{{ $vars.HR_MANAGER_EMAIL }}`
   - Treść: nowe zgłoszenie, link do arkusza
3. `Return: Confirmation`
   - success, ticket_id (row ID), message, sla_hours: 8

**Różnica vs IT:** Brak integracji z ticketingiem — HR używa Sheets.
To normalne. Każdy subworkflow dostosowuje się do narzędzi danego działu.

> 🎙️ NOTATKA: "Piękno modularności: IT używa Jira, HR używa Sheets, Sales używa CRM. Master nie wie i nie musi wiedzieć. Każdy subworkflow działa na własnych narzędziach."

---

## Slajd 25: Other — Human Review Queue

**Filozofia:** Nie każde zgłoszenie da się zautomatyzować.

**Subworkflow "Other":**
1. `Append to Review Queue` (Google Sheets)
2. `Send Alert to Admin`
   - Email + Slack do osoby dyżurnej
   - "Nowe zgłoszenie wymagające ręcznej klasyfikacji"
3. `Return: Confirmation`
   - success: true (odebraliśmy!)
   - message: "Twoje zgłoszenie trafi do naszego zespołu w ciągu 24h"
   - sla_hours: 24

**Kluczowa zasada:**
Nawet "Other" daje potwierdzenie użytkownikowi.
Nigdy nie znikaj po odbiorze zgłoszenia.

> 🎙️ NOTATKA: "'Other' to też ścieżka sukcesu. Użytkownik dostaje potwierdzenie, admin dostaje alert. Nic nie wypada w próżnię."

---

## Slajd 26: Merge i Confirmation Email

**Po Execute Workflow dla każdej gałęzi:**

```
[Merge] — tryb: Merge by Key
  Klucz: request_id
  Zbiera wyniki ze wszystkich gałęzi
```

**Potwierdzenie dla użytkownika:**
```
Temat: Twoje zgłoszenie #{{ $json.ticket_id }} zostało zarejestrowane

Drogi/a {{ $json.requester_name }},

Twoje zgłoszenie zostało odebrane i przypisane.

📋 Numer referencyjny: {{ $json.ticket_id }}
📂 Kategoria: {{ $json.category }}
👤 Przypisano do: {{ $json.assigned_to }}
⏱️ Przewidywany czas odpowiedzi: {{ $json.sla_hours }}h

{{ $json.message }}

—
System Zgłoszeń Firmowych
```

> 🎙️ NOTATKA: "Zawsze wysyłaj potwierdzenie. To jedna z tych rzeczy, które odróżniają profesjonalną automatyzację od skryptu. Użytkownik wie, że jego zgłoszenie nie przepadło."

---

## Slajd 27: Testowanie Modularnej Architektury

**Strategia testowania:**

**Krok 1: Testuj subworkflows w izolacji**
- Stwórz test workflow z hardcoded JSON input
- Wywołaj każdy subworkflow bezpośrednio
- Weryfikuj output JSON

**Krok 2: Testuj Switch node**
- 5 testowych inputów (po jednym na kategorię)
- Weryfikuj, że każda trafia na właściwą ścieżkę

**Krok 3: Test end-to-end**
- Wyślij email testowy z każdą kategorią
- Sprawdź: ticket w Jira, row w Sheets, email wysłany
- Sprawdź: email potwierdzający z właściwym ticket_id

**Testy regresji:** Po każdej zmianie — test #1 i #3 zawsze.

> 🎙️ NOTATKA: "Modularność to nie tylko czytelność — to możliwość testowania. Testuj subworkflow w izolacji jak unit testy. To właśnie jest przewaga architektury."

---

## Slajd 28: Checklista przed deployem workflow

**Przed aktywacją workflow na produkcji:**

- [ ] Wszystkie nody mają czytelne nazwy
- [ ] Workflow ma nazwę według konwencji
- [ ] Jest folder i tagi (środowisko + wersja)
- [ ] Każda ścieżka IF/Switch ma Default
- [ ] Error handling: co się stanie gdy API nie odpowie?
- [ ] Zmienne środowiskowe w n8n Variables, nie hardcoded
- [ ] Przetestowałem każdą ścieżkę ręcznie
- [ ] Return contract jest udokumentowany
- [ ] Wykonałem eksport JSON (backup)
- [ ] Ktoś inny rozumie co robi ten workflow (opcjonalne, ale zalecane)

> 🎙️ NOTATKA: "Wydrukuj tę checklistę. Naprawdę. Pierwszym razem gdy ją pominiesz i deployment pójdzie źle o 23:00, zapamiętasz."

---

## Slajd 29: Anty-wzorce do unikania

**1. "Master który robi wszystko"**
Zamiast delegować do subworkflowów — robi całą logikę sam.
→ To nie jest master, to monolith przemianowany.

**2. "Zagnieżdżone wywołania"**
Master → Sub1 → Sub2 → Sub3
→ Debugowanie staje się koszmarnym trackowaniem.
→ Maksymalnie 2 poziomy głębokości.

**3. "Brak return contract"**
Subworkflow nie zwraca nic / zwraca wszystko.
→ Master nie wie co dostał.
→ Zawsze definiuj kontrakt.

**4. "Tight coupling przez ID"**
Master hardcoduje ID subworkflow zamiast używać nazw.
→ Zmiana workflow = naprawa mastera.
→ Używaj n8n Variables do przechowywania ID.

> 🎙️ NOTATKA: "Widziałem każdy z tych anty-wzorców w produkcji. Łącznie z własnym."

---

## Slajd 30: Ćwiczenie 1 — Refaktoryzacja Lead Capture

**Zadanie (20 min):**

Weź workflow Lead Capture z Tygodnia 1 i podziel go na:
- `PROD_Lead_Capture_Master` (orchestrator)
- `PROD_Lead_Enrich_Data` (subworkflow: weryfikacja + enrichment)
- `PROD_Lead_Save_CRM` (subworkflow: zapis do CRM)
- `PROD_Lead_Notify_Sales` (subworkflow: powiadomienie zespołu)

**Punkty kontrolne:**
1. Każdy subworkflow uruchamia się samodzielnie z testowym JSON
2. Master wywołuje je sekwencyjnie i zbiera wyniki
3. Kontrakt wejście/wyjście udokumentowany w sticky note

> 🎙️ NOTATKA: "To ćwiczenie celowo używa workflow który już znacie. Refaktoryzacja istniejącego kodu jest trudniejsza niż budowanie od zera. I bardziej realistyczna."

---

## Slajd 31: Zadanie domowe — Kategoria "Urgent"

**Rozbuduj Request Router o kategorię "Urgent":**

- Trigger: email z subject zawierającym "[URGENT]" lub priorytet "urgent"
- Subworkflow `WF_Urgent`:
  1. Zapis do Sheets (wspólna kolejka)
  2. Email do CFO + CEO
  3. SMS przez Twilio do managera dyżurnego
  4. Zwróć ticket_id z prefixem "URG-"

**Wskazówki:**
- Twilio w n8n: szukaj node "Twilio" w panel nodów
- Credentials: Twilio Account SID + Auth Token
- SMS: endpoint SMS z `$vars.DUTY_MANAGER_PHONE`
- Switch: dodaj case "Urgent" przed "Other"

**Termin:** Przed Modułem 5

> 🎙️ NOTATKA: "Twilio ma darmowy trial — nie musisz płacić żeby to przetestować. To realistyczna funkcja którą wiele firm naprawdę potrzebuje."

---

## Slajd 32: Podsumowanie — 5 Zasad Architektury Modularnej

**1. Jeden workflow = jedna odpowiedzialność**
Master orchestruje. Subworkflow wykonuje.

**2. Definiuj kontrakty, nie zakładaj**
Input/output każdego subworkflow musi być udokumentowany.

**3. Variables zamiast hardcoding**
Konfiguracja w jednym miejscu. Używana wszędzie.

**4. Testuj w izolacji, deployuj razem**
Subworkflow testowane solo. System testowany end-to-end.

**5. Naming convention od dnia zero**
Konwencja narzucona od początku. Chaos narasta bez niej.

---

**Moduł 5 → AI + Human in the Loop**
Kiedy AI musi poprosić człowieka o decyzję.

> 🎙️ NOTATKA: "Przejdź przez 5 zasad wolno. Zostaw je na ekranie przez 10 sekund. To najważniejszy slajd w całym module. Kto te zasady wdroży, zaoszczędzi sobie tygodnie pracy w ciągu roku."
