---
type: kurs-skrypt
modul: 04
tytul: "Architektura Modularna — Koniec z Chaosem"
dlugosc_szacowana: "~3h nagrania"
liczba_slow: ~2100
last_updated: 2026-03-27
---

# Moduł 4 — Skrypt Nagrania

> Legenda: **[SLAJD N]** = zmiana slajdu | **[DEMO]** = przejdź do n8n | **[PAUZA]** = chwila ciszy dla efektu

---

## SEGMENT 1: Diagnoza problemu (35 min)

---

### Intro (2 min)

Cześć, witam was w Module 4 — Architektura Modularna. Dzisiaj zrobimy rzecz, która zmienia sposób myślenia o n8n na zawsze. Zbudujemy system, który wygląda profesjonalnie, daje się utrzymywać i nie sprawia, że po miesiącu patrzysz na własny workflow jak na obcy język.

**[SLAJD 2]**

Na końcu tego modułu zbudujesz Corporate Request Router — firmowy system routowania zgłoszeń. Email przychodzi, AI klasyfikuje, każda kategoria jedzie do odpowiedniego działu, zgłaszający dostaje potwierdzenie z numerem ticketu. Brzmi prosto? Jest proste — jeśli masz odpowiednią architekturę. Zobaczysz, jak to działa.

**[SLAJD 3]**

Agenda na dziś: zaczynamy od diagnozy problemu — co jest złego w tym, jak większość ludzi buduje workflow. Potem narzędzia: Execute Workflow, Switch, Variables. Następnie konwencje — jak utrzymywać porządek gdy masz 50 workflow. I na końcu — budujemy razem. Zaczynamy.

---

### Problem spaghetti workflow (10 min)

**[SLAJD 4]**

Mam dla was pytanie. Czy zdarzyło ci się otworzyć workflow, który sam zbudowałeś dwa miesiące temu — i nie wiedzieć co on robi? **[PAUZA 3 sekundy]**

Jeśli odpowiedź brzmi "tak" — jesteś w właściwym miejscu. Jeśli brzmi "nie" — albo dopiero zaczynasz albo nie budujesz wystarczająco dużo.

To co widzicie na slajdzie to klasyczny "spaghetti workflow". Trzydzieści kilka nodów. Połączenia krzyżujące się na pół ekranu. Kilka IF zagnieżdżonych w sobie. Nazwa nodeów: "HTTP Request", "HTTP Request1", "Set", "Set1".

Byłem u klienta, który miał workflow do przetwarzania faktur. Zbudowany przez zewnętrznego freelancera. Trzydzieści osiem nodów. Nikt w firmie nie rozumiał co on robi. Freelancer był niedostępny. Faktura z błędnym formatem zatrzymała cały system. Firma przez 3 dni procesowała faktury ręcznie.

To jest cena spaghetti.

**[SLAJD 5]**

A teraz ten sam system — ale zbudowany modularnie. Widzicie różnicę? Jeden master workflow z jasną sekwencją. Pięć wywołań do subworkflowów. Każde wywołanie ma czytelną nazwę. Całość czyta się jak diagram biznesowy, nie jak labirynt.

Obie wersje robią to samo. Ale tylko jedna da się utrzymywać.

**[SLAJD 6]**

Dlaczego monolity są złe? Cztery powody. Pierwszy: niemożliwość ponownego użycia. Jeśli masz logikę "wyślij email potwierdzający" — ile razy ją skopiowałeś? Dwa razy? Trzy? Teraz zmień format tego emaila. Ile edycji? Każda kopia to osobne miejsce do aktualizacji i osobne miejsce do błędu.

Drugi: piekło debugowania. Błąd w Node 23 z 40. Który Node 23? Który output? Które dane? W monolicie musisz prześledzić cały przepływ od początku.

Trzeci: brak izolacji zmian. Poprawiasz logikę sprzedażową — przez przypadek psujesz routing HR. Zdarzyło się? Mnie się zdarzyło.

Czwarty: niemożliwość testowania. Nie możesz uruchomić tylko "kawałka" workflow. Musisz odpalić całość z prawdziwymi danymi albo przygotować skomplikowany mock. Modularność to zmienia całkowicie.

---

### Filozofia architektury modularnej (15 min)

**[SLAJD 7]**

Zanim przejdziemy do narzędzi — heurystyka. Kiedy modularyzować, kiedy nie? Prosta odpowiedź: gdy workflow ma więcej niż 15 nodów, gdy ta sama logika pojawia się w 2 miejscach, gdy chcesz testować kawałki oddzielnie. Zostaw inline gdy to prosty skrypt poniżej 10 nodów, jednorazowy eksperyment, coś co istnieje tydzień.

Architektura to narzędzie, nie religia. Nie modularyzuj dla samego modularyzowania.

**[SLAJD 8]**

Moja ulubiona analogia na wytłumaczenie master-subworkflow: orkiestra i dyrygent.

Dyrygent zna partyturę. Wie, że po intro wchodzą skrzypce, potem w takcie 32 dołącza sekcja dęta. Ale — i to jest kluczowe — dyrygent sam nie gra na żadnym instrumencie. On koordynuje.

Muzyk jest ekspertem w swoim instrumencie. Skrzypek gra skrzypce. Kiedy dyrygent daje znak — skrzypek gra. Kiedy nie ma znaku — czeka. Nie wie i nie musi wiedzieć co robi sekcja dęta.

Tak działa master-subworkflow. Master wie co i kiedy wywołać. Sam nie wysyła emaili, nie tworzy ticketów, nie zapisuje do bazy. On wywołuje subworkflowy, które to robią. Subworkflow są ekspertami w swojej dziedzinie.

**[SLAJD 9]**

Diagram komunikacji. Master → subworkflow: JSON z danymi wejściowymi. Subworkflow → master: JSON z wynikiem. Nic więcej. To jest cały protokół komunikacji.

Ten diagram powinien zostać w waszej głowie. Za każdym razem gdy budujecie cokolwiek skomplikowanego w n8n — zadajcie sobie pytanie: "Który node to dyrygent, a które to muzycy?"

---

## SEGMENT 2: Narzędzia architektury (50 min)

---

### Execute Workflow node (20 min)

**[DEMO — przejście do n8n]**

Dobra, teraz do konkretów. Otwieram n8n. Tworzę nowy workflow. Szukam node'a — "Execute Workflow".

Mamy go. Klikam. Widzę kilka parametrów. Omówimy je po kolei.

Pierwszy: Workflow. Tu wpisujemy ID lub wybieramy z listy. Rekomendacja: wybierajcie z listy. ID się zmienia gdy importujesz workflow, nazwa pozostaje.

Drugi: Mode. Synchronous lub asynchronous. Synchronous: master czeka aż subworkflow skończy i dostaje wynik. Asynchronous: master odpala subworkflow i idzie dalej, nie czeka. Kiedy async? Gdy masz długą operację, która trwa ponad 30 sekund. Albo fire-and-forget — uruchamiasz i nie potrzebujesz wyniku. Dla naszego routera używamy synchronous — master musi dostać ticket_id żeby wysłać potwierdzenie.

Trzeci: Input Data. Co przekazujesz do subworkflow. Tutaj dajesz `{{ $json }}` jeśli chcesz przekazać cały aktualny obiekt. Albo budujesz własny JSON: `{{ { "request_id": $json.id, "email": $json.email } }}`.

**[SLAJD 10]**

Pokażę teraz prosty test. Tworzę minimalistyczny subworkflow — tylko trigger "When Called by Another Workflow" i Return Data z `{ "pong": true }`. Zapisuję. Wracam do mastera. Execute Workflow node → wybieram ten subworkflow → Input: `{ "ping": true }` → uruchamiam.

I widzę: subworkflow zwrócił `{ "pong": true }`. Dane przeszły tam i z powrotem.

To jest fundament. Cała reszta to budowanie na tym fundamencie.

---

### Subworkflows jako funkcje (15 min)

**[SLAJD 11]**

Przejdźmy do subworkflowów. Kluczowa decyzja przy designie: co przyjmuje subworkflow i co zwraca?

Trigger "When Called by Another Workflow" ma opcję zdefiniowania pól wejściowych. Zawsze to rób. Zdefiniuj `request_id`, `requester_email`, `description`, `priority`. Ustaw required: true dla tych, bez których subworkflow nie może działać.

Dlaczego to ważne? Po pierwsze — dokumentacja. Każdy kto otwiera subworkflow od razu widzi: "aha, potrzebuję tych czterech pól". Po drugie — walidacja. n8n UI pokaże błąd jeśli master nie przekaże wymaganego pola. Po trzecie — to jest kontrakt. Umowa między master a sub. Jak function signature w JavaScript.

**[SLAJD 12]**

Return Data node — ostatni node w subworkflow. Zawsze umieszczaj go na końcu każdej ścieżki, nie tylko na końcu głównego przepływu.

Co zwracać? Zawsze `success: true/false`. To jest sygnał dla mastera: "udało się" albo "nie". Zawsze `message` — czytelny tekst dla end-usera. Master wklei ten tekst do emaila potwierdzającego. Opcjonalnie: `ticket_id`, `assigned_to`, `sla_hours` — wszystko co przydatne.

Nie zwracaj całego JSON z API. Przefiltruj do tego, co potrzebuje master. Czysty output = prosty master.

---

### Switch node i routing (15 min)

**[DEMO — Switch node w n8n]**

**[SLAJD 13]**

Switch node. To jest serce routera.

Tworzę Switch node. Mode: Rules. Wartość do sprawdzenia: `{{ $json.category }}`.

Dodaję case: wartość równa `IT_Support` → output 1. Następny case: `HR` → output 2. `Finance` → output 3. `Sales` → output 4. I — kluczowe — Default → output 5.

Zawsze ustawiajcie Default. Zawsze. AI nie jest doskonała. Użytkownik może wpisać coś nieoczekiwanego. Default to siatka bezpieczeństwa. Bez Default — zgłoszenie znika w próżni i nikt nie wie.

Switch vs IF: Switch używaj gdy masz 3+ ścieżki. IF dla prostego tak/nie. Zagnieżdżone IF to twój wróg — każde zagnieżdżenie to kolejny poziom trudności debugowania.

---

## SEGMENT 3: Organizacja i konwencje (30 min)

---

### Naming conventions (10 min)

**[SLAJD 15]**

Czas na konwencje. Wiem, że to brzmi nudno. Ale naming convention to jedna z tych rzeczy, które po sześciu miesiącach użytkowania albo ci dziękujesz albo przeklinasz siebie z przeszłości.

Format nazwy workflow: `[ENV]_[OBSZAR]_[FUNKCJA]_v[X]`.

ENV zawsze na początku: PROD dla produkcji, DEV dla prac w toku, TEST dla testów. Dlaczego na początku? Bo w liście workflow sortujecie alfabetycznie — wszystkie produkcyjne razem, wszystkie deweloperskie razem.

OBSZAR: krótki identyfikator biznesowy. Sales, IT, HR, Finance. Bez polskich znaków — unikasz problemów z URL i API.

FUNKCJA: czasownik + rzeczownik. Lead_Capture, Request_Handler, Invoice_Process. Nie: "Nowy workflow" ani "Test 3".

Wersja: tylko major zmiany logiki. Nie inkrementuj przy każdej drobnej poprawce.

**[SLAJD 16]**

Nody. Każdy node — czytelna nazwa. Domyślne nazwy jak "HTTP Request1" są złem.

Konwencja: `[CZASOWNIK]: [CO + GDZIE/PO CO]`. "POST: Create Issue in Jira". "GET: Employee Data from HR System". "IF: Priority is Urgent". "Set: Prepare Confirmation Email".

Zmiana nazwy noda zajmuje 2 sekundy. Oszczędza minuty przy debugowaniu. Proste.

---

### Folder structure i wersjonowanie (20 min)

**[SLAJD 17]**

Foldery w n8n. Jeśli masz wersję n8n z folderami — używaj ich. Rekomendowana struktura: `00_MASTER_WORKFLOWS` na orchestratorów, foldery per obszar biznesowy, `DEV` na prace w toku, `99_ARCHIVE` na dezaktywowane.

Jeśli nie masz folderów — prefixy w nazwach działają tak samo. `PROD_Sales_` automatycznie grupuje wszystkie workflow sprzedażowe.

**[SLAJD 18]**

Wersjonowanie. Minimum viable: tagi. Tagnij "stable" gdy workflow przechodzi na produkcję. Tagnij "deprecated" gdy przestajesz używać ale nie chcesz usuwać. Historia zmian w n8n — jest, ale nie polegaj tylko na niej. Ekspot JSON do folderu na Dropbox co tydzień to proste ubezpieczenie.

Zaawansowani: Git. Export JSON + commit. Masz pełną historię, możesz porównywać wersje, możesz cofać zmiany. To temat na osobny materiał.

**[SLAJD 14]**

n8n Variables. Mam dla was pytanie: ile razy wpisałeś URL zewnętrznego API bezpośrednio w nod? I ile razy potem musiałeś go zmienić w 5 miejscach?

Variables rozwiązują ten problem. Ustawienia → Variables → Nowa zmienna. Nazwa: `JIRA_BASE_URL`. Wartość: `https://firma.atlassian.net`. Użycie w workflow: `{{ $vars.JIRA_BASE_URL }}`.

Zmiana URL? Zmiana w jednym miejscu. Wszystkie workflow zaktualizowane automatycznie. Dobre kandydatury na Variables: base URL systemów, adresy email zespołów, SLA per kategoria, numery telefonów dla alertów.

---

## SEGMENT 4: Budowa Corporate Request Router (55 min)

---

**[SLAJD 21]**

Dobra — budujemy. Diagram mamy przed oczami. Strategia: zacznij od subworkflowów, potem master. Dlaczego? Bo subworkflow możesz testować samodzielnie bez mastera. Gdy przychodzisz do budowy mastera, wszystkie "klocki" już działają. Łączysz działające komponenty.

---

### Konfiguracja Variables (5 min)

Zanim cokolwiek zbuduję — ustawiam Variables:
- `JIRA_BASE_URL`: URL twojego Jira
- `IT_TEAM_EMAIL`: email działu IT
- `HR_MANAGER_EMAIL`: email HR managera
- `FINANCE_CFO_EMAIL`: email CFO
- `SALES_TEAM_SLACK_CHANNEL`: kanał Slack sprzedaży
- `SLA_IT_HOURS`: 4
- `SLA_HR_HOURS`: 8
- `SLA_FINANCE_HOURS`: 24
- `SLA_SALES_HOURS`: 2

Wszystko w Variables. Nic hardcoded w workflowach.

---

### IT Support Subworkflow (10 min)

**[DEMO — budowa subworkflow w n8n]**

Nowy workflow: `PROD_IT_Request_Handler_v1`.

Trigger: "When Called by Another Workflow". Definiuję pola: `request_id`, `requester_email`, `description`, `priority`.

Node 2: `Set: Map Priority to Jira Format`
Mapuję: "urgent" → "Highest", "high" → "High", "medium" → "Medium", "low" → "Low".

Node 3: `POST: Create Issue in Jira`
HTTP Request → POST → `{{ $vars.JIRA_BASE_URL }}/rest/api/2/issue`
Body:
```json
{
  "fields": {
    "project": { "key": "IT" },
    "summary": "Zgłoszenie od {{ $json.requester_email }}",
    "description": "{{ $json.description }}",
    "issuetype": { "name": "Task" },
    "priority": { "name": "{{ $json.jira_priority }}" }
  }
}
```

Node 4: `Send Email to IT Team`
Gmail / SMTP → To: `{{ $vars.IT_TEAM_EMAIL }}`

Node 5: `Return: Success Confirmation`
```json
{
  "success": true,
  "ticket_id": "{{ $json.key }}",
  "message": "Zgłoszenie IT zarejestrowane. Odpowiedź w ciągu {{ $vars.SLA_IT_HOURS }}h.",
  "assigned_to": "{{ $vars.IT_TEAM_EMAIL }}",
  "sla_hours": "{{ $vars.SLA_IT_HOURS }}"
}
```

Teraz testuję ten subworkflow samodzielnie z testowym JSON. Działa? Zapisuję. Przechodzimy dalej.

---

### HR Subworkflow (8 min)

`PROD_HR_Request_Handler_v1`

Struktura analogiczna do IT, ale zamiast Jira — Google Sheets.

Node: `Append Row to HR Requests Sheet`
Google Sheets → Append Row
Kolumny: Timestamp, Request ID, Email, Description, Priority, Status=NEW

Node: `Send Email to HR Manager`

Node: `Return: Success`
```json
{
  "success": true,
  "ticket_id": "HR-{{ $now.format('YYYYMMDDHHmm') }}",
  "message": "Zgłoszenie HR przyjęte. Odpowiedź w ciągu {{ $vars.SLA_HR_HOURS }}h.",
  "assigned_to": "{{ $vars.HR_MANAGER_EMAIL }}",
  "sla_hours": "{{ $vars.SLA_HR_HOURS }}"
}
```

Zauważ: HR nie ma systemu ticketowego jak Jira. Generujemy ticket_id z timestamp. To rozwiązanie praktyczne i wystarczające.

---

### Finance i Sales (5 min szkic)

Finance: analogicznie do HR — Google Sheets + email do CFO.

Sales: Google Sheets albo CRM (HubSpot, Pipedrive) + Slack do handlowca. Node Slack: `Post Message` → kanał `{{ $vars.SALES_TEAM_SLACK_CHANNEL }}`.

Każdy subworkflow — ta sama struktura Return. `success`, `ticket_id`, `message`, `assigned_to`, `sla_hours`. Ta spójność to celowy design.

---

### Other — Human Review Queue (5 min)

`PROD_Other_Human_Review_v1`

Ten subworkflow jest najważniejszy z punktu widzenia UX. Użytkownik wysłał zgłoszenie, które nie pasuje do żadnej kategorii. Co się stanie?

Zła wersja: nic. Zgłoszenie znika. Użytkownik dzwoni do recepcji w panice.

Dobra wersja: automatyczne potwierdzenie + alert do admina.

```json
{
  "success": true,
  "ticket_id": "OTH-{{ $now.format('YYYYMMDDHHmm') }}",
  "message": "Twoje zgłoszenie wymaga ręcznego przeglądu. Skontaktujemy się w ciągu 24h.",
  "assigned_to": "admin@firma.pl",
  "sla_hours": 24
}
```

Always return success: true dla "Other". Odebraliśmy zgłoszenie — to sukces. Fakt, że wymaga ręcznej obsługi, to detal implementacyjny, nie błąd.

---

### Master Workflow (15 min)

**[DEMO — budowa master workflow]**

`PROD_Master_Request_Router_v1`

Node 1: `Webhook Trigger`
Path: `/request-router`
Method: POST

Node 2: `Set: Normalize Input`
Standaryzuj pola: `request_id` (generuj UUID jeśli brak), `requester_email`, `description`, `priority` (default: "medium").

Node 3: `AI: Classify Request Category`
OpenAI node → GPT-4o-mini
System prompt: [jak na Slajdzie 22]
Output: sparsowany JSON z polem `category`

Node 4: `Switch: Route by Category`
Cases: IT_Support, HR, Finance, Sales, Other

Dla każdej gałęzi:
Node 5a: `Execute: WF_IT_Request_Handler`
Workflow: PROD_IT_Request_Handler_v1
Input: `{{ { "request_id": $json.request_id, "requester_email": $json.requester_email, "description": $json.description, "priority": $json.priority } }}`
Mode: synchronous, Wait for finish: true

Node 6: `Merge: Collect Results`
Tryb: Merge by Key, Klucz: request_id

Node 7: `Send Email: Confirmation to Requester`
To: `{{ $json.requester_email }}`
Subject: `Zgłoszenie #{{ $json.ticket_id }} zarejestrowane`
Body: [jak na Slajdzie 26]

Test end-to-end: wyślę 5 requestów — jeden per kategoria. Weryfikuję każdą ścieżkę.

---

## SEGMENT 5: Ćwiczenia i podsumowanie (25 min)

---

### Ćwiczenia (10 min)

**[SLAJD 30]**

Ćwiczenie 1 — refaktoryzacja. Macie workflow Lead Capture z Tygodnia 1. Zadanie: podzielcie go na 4 workflow. Master + trzy subworkflowy: enrichment danych, zapis do CRM, powiadomienie sprzedaży. Czas: 20 minut. Jeśli skończycie wcześniej — dodajcie kontrakty wejście/wyjście w sticky note do każdego subworkflow.

**[SLAJD 31]**

Zadanie domowe — kategoria "Urgent". To jest realistyczne zadanie, które wiele firm naprawdę potrzebuje. Zgłoszenia oznaczone [URGENT] wymagają specjalnej ścieżki: email do zarządu i SMS do managera dyżurnego.

Twilio w n8n to 3 kliknięcia po skonfigurowaniu credentials. Nie bójcie się. Twilio ma darmowy trial. Numer telefonu testowy dostajecie od razu.

---

### Podsumowanie (10 min)

**[SLAJD 28]**

Zanim skończymy — checklista deployu. Przejdę przez nią raz na głos. Każdy punkt to realna lekcja z prawdziwych wdrożeń:

Czytelne nazwy nodów? Tak. Nazwa workflow według konwencji? Tak. Folder i tagi? Tak. Default w każdym Switch? TAK — to jest najczęstszy pominięty punkt. Error handling? Tak. Variables zamiast hardcoded wartości? Tak. Testy każdej ścieżki? Tak. Return contract udokumentowany? Tak. Eksport JSON backup? Tak.

Wydrukuj tę checklistę. Naprawdę. Pierwszym razem gdy ją pominiesz i deployment pójdzie źle o 23:00, zapamiętasz.

**[SLAJD 32]**

Pięć zasad na wynos:

Pierwsza: jeden workflow, jedna odpowiedzialność. Master orchestruje, sub wykonuje. Master nie wysyła emaili. Sub nie wie o innych subworkflowach.

Druga: definiuj kontrakty, nie zakładaj. Input/output każdego subworkflow jest udokumentowany. Jak swagger API.

Trzecia: Variables zamiast hardcoding. Konfiguracja w jednym miejscu.

Czwarta: testuj w izolacji, deployuj razem. Subworkflow testowany solo. System testowany end-to-end.

Piąta: naming convention od dnia zero. Konwencja narzucona od początku. Chaos narasta bez niej.

To są zasady, które stosuję w każdym projekcie. Teraz wy je macie.

---

W Module 5 wchodzimy w AI + Human in the Loop — kiedy AI musi poprosić człowieka o decyzję przed kontynuacją. To temat, który otwiera zupełnie nową klasę automatyzacji.

Do zobaczenia. Zadanie domowe — Twilio nie ugryzie. Powodzenia.

---

## Notatki do nagrania

- Czas Segment 1: 35 min — nie śpiesz się z analogią orkiestry, to buduje zrozumienie
- Czas Segment 2: 50 min — demo jest sercem, nie spiesz się
- Czas Segment 4: 55 min — buduj na żywo, nawet jeśli coś się psuje — to realistyczne
- Styl: konkretny, bez lania wody, dużo "tak właśnie robimy w praktyce"
- Unikaj: "jak wiecie", "oczywiście", "jak wspomniałem"
- Dodaj: "U klienta X widziałem..." — każda anegdota z życia wzmacnia przekaz
