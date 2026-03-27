---
type: kurs-cwiczenia
modul: 04
tytul: "Architektura Modularna — Ćwiczenia Praktyczne"
czas_total: "~95 min + zadanie domowe"
poziom: średniozaawansowany
last_updated: 2026-03-27
---

# Moduł 4 — Ćwiczenia Praktyczne

> Ćwiczenia są ułożone od prostszego do trudniejszego. Zanim zaczniesz Ćwiczenie 2, upewnij się że rozumiesz mechanizm Execute Workflow z Ćwiczenia 1. Każde ćwiczenie zawiera kryteria sukcesu — użyj ich jako checklisty po ukończeniu.

---

## Ćwiczenie 1 — Refaktoryzacja Lead Capture System (25 min)

### Cel

Przerobić monolityczny workflow z Tygodnia 1 na architekturę master + subworkflows. Zrozumieć, jak rozbijanie logiki na mniejsze jednostki wpływa na czytelność i łatwość utrzymania.

### Kontekst

W Tygodniu 1 zbudowałeś Lead Capture System — formularz zbierał dane kontaktowe, workflow walidował email i zapisywał lead do Google Sheets. Prawdopodobnie wszystko siedzi w jednym workflow. Dziś to zmieniamy.

### Krok po kroku

**Faza 1 — Analiza (5 min)**

Otwórz swój Lead Capture workflow z Tygodnia 1. Zrób mentalną mapę: gdzie zaczyna się walidacja emaila? Gdzie kończy? Gdzie zaczyna się zapis do Sheets? Narysuj na kartce dwa prostokąty z etykietami "Walidacja emaila" i "Zapis do Sheets". To będą twoje subworkflows.

**Faza 2 — Subworkflow #1: Walidacja emaila (8 min)**

1. Utwórz nowy, pusty workflow. Nazwij go: `[SUB] Waliduj Email`
2. Jako trigger ustaw node: **When Called by Another Workflow**
3. Dodaj node **Code** (JavaScript) z logiką walidacji:
   ```javascript
   const email = $input.first().json.email;
   const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

   return [{
     json: {
       email: email,
       is_valid: isValid,
       error: isValid ? null : "Niepoprawny format emaila"
     }
   }];
   ```
4. Dodaj node **Return** — upewnij się, że zwraca pole `is_valid` i `error`
5. Zapisz i aktywuj subworkflow. Zanotuj jego Workflow ID

**Faza 3 — Subworkflow #2: Zapis do Sheets (7 min)**

1. Utwórz nowy workflow. Nazwij go: `[SUB] Zapisz Lead do Sheets`
2. Trigger: **When Called by Another Workflow**
3. Dodaj node **Google Sheets** (Update/Append) — przenieś tutaj konfigurację z oryginalnego workflow
4. Dodaj node **Code** — przygotuj potwierdzenie:
   ```javascript
   return [{
     json: {
       status: "saved",
       timestamp: new Date().toISOString(),
       message: "Lead zapisany pomyślnie"
     }
   }];
   ```
5. Dodaj node **Return**
6. Zapisz i aktywuj. Zanotuj Workflow ID

**Faza 4 — Master Workflow (5 min)**

1. Wróć do oryginalnego Lead Capture workflow (lub stwórz nowy)
2. Po triggerze (formularz / webhook) dodaj node **Execute Workflow** → wybierz `[SUB] Waliduj Email`
3. Dodaj node **If** — sprawdź czy `{{ $json.is_valid }}` to `true`
   - Ścieżka TRUE: node **Execute Workflow** → wybierz `[SUB] Zapisz Lead do Sheets`
   - Ścieżka FALSE: node **Respond to Webhook** z błędem `{{ $json.error }}`
4. Po zapisaniu: node **Respond to Webhook** z sukcesem
5. Usuń z master workflow wszystkie node'y, które przeniosłeś do subworkflows

### Kryteria sukcesu

- [ ] Master workflow ma maksymalnie 6-8 nodów (trigger, execute x2, if, respond x2)
- [ ] Obydwa subworkflows uruchamiają się poprawnie gdy wywołasz je ręcznie z testowymi danymi
- [ ] Testowy email `jan.kowalski@firma.pl` przechodzi walidację i ląduje w Sheets
- [ ] Testowy email `nievalid@` zwraca błąd bez zapisu do Sheets

### Refleksja (umieść w Sticky Note na canvasie master workflow)

Po ukończeniu ćwiczenia dodaj do master workflow **Sticky Note** (prawy przycisk myszy na canvasie → Add Sticky Note) i odpowiedz w kilku zdaniach:

- Czy workflow jest teraz czytelniejszy niż oryginał? Co konkretnie jest lepiej widoczne?
- Ile nodów miał oryginał, ile ma teraz master?
- Co byłoby łatwiejsze gdybyś musiał zmienić logikę walidacji emaila — w wersji monolitycznej czy modularnej? Dlaczego?

> Wskazówka: Nie ma złej odpowiedzi. Chodzi o to, żebyś zaczął myśleć o kompromisach architektonicznych — modularność ma swoje koszty (więcej plików, większa złożoność nawigacji), ale w projektach powyżej 15 nodów zdecydowanie się opłaca.

---

## Ćwiczenie 2 — Corporate Request Router (60 min)

### Cel

Zbudować od zera system routowania zgłoszeń z master workflow, Switch node i minimum 3 subworkflows. Każde zgłoszenie jest klasyfikowane, trafia do odpowiedniego działu i generuje potwierdzenie z numerem referencyjnym.

### Architektura systemu

```
[Webhook / Formularz]
        |
[Master Workflow]
        |
[Switch: Klasyfikacja]
   |        |        |        |
 [IT]     [HR]  [Finance]  [Other]
   |        |        |        |
        [Merge]
           |
  [Email: Potwierdzenie]
```

### Krok po kroku

**Faza 1 — Subworkflow IT Support (15 min)**

1. Nowy workflow: `[SUB] IT — Obsłuż Zgłoszenie`
2. Trigger: **When Called by Another Workflow**
3. Node **Code** — wygeneruj numer ticketu i przygotuj wpis:
   ```javascript
   const ticketNumber = "IT-" + Date.now().toString().slice(-6);
   const input = $input.first().json;

   return [{
     json: {
       ticket_number: ticketNumber,
       department: "IT",
       subject: input.subject || "Brak tematu",
       requester: input.email || "Brak emaila",
       status: "open",
       priority: input.priority || "normal",
       created_at: new Date().toISOString(),
       confirmation_message: `Twoje zgłoszenie IT zostało przyjęte. Numer ticketu: ${ticketNumber}. Czas reakcji: do 4 godzin roboczych.`
     }
   }];
   ```
4. (Opcjonalnie) Dodaj node **Google Sheets** — zapisz ticket do arkusza "IT Helpdesk"
5. Node **Return**
6. Zapisz i aktywuj. Zanotuj Workflow ID

**Faza 2 — Subworkflow HR (10 min)**

1. Nowy workflow: `[SUB] HR — Obsłuż Zgłoszenie`
2. Trigger: **When Called by Another Workflow**
3. Node **Code**:
   ```javascript
   const ticketNumber = "HR-" + Date.now().toString().slice(-6);
   const input = $input.first().json;

   return [{
     json: {
       ticket_number: ticketNumber,
       department: "HR",
       subject: input.subject || "Brak tematu",
       requester: input.email || "Brak emaila",
       status: "pending",
       created_at: new Date().toISOString(),
       confirmation_message: `Twoje zgłoszenie do HR zostało przyjęte. Numer referencyjny: ${ticketNumber}. Odpowiemy w ciągu 2 dni roboczych.`
     }
   }];
   ```
4. Node **Return**. Zapisz i aktywuj.

**Faza 3 — Subworkflow Finance (10 min)**

1. Nowy workflow: `[SUB] Finance — Obsłuż Zgłoszenie`
2. Analogicznie jak HR, zmień prefix na `FIN-` i treść potwierdzenia na stosowną dla działu finansowego (np. "Czas rozpatrzenia: do 5 dni roboczych")
3. Node **Return**. Zapisz i aktywuj.

**Faza 4 — Subworkflow Other / Kolejka Ręczna (5 min)**

1. Nowy workflow: `[SUB] Other — Kolejka Ręczna`
2. Node **Code**:
   ```javascript
   const ticketNumber = "OTH-" + Date.now().toString().slice(-6);
   const input = $input.first().json;

   return [{
     json: {
       ticket_number: ticketNumber,
       department: "Other",
       subject: input.subject || "Brak tematu",
       requester: input.email || "Brak emaila",
       status: "review_needed",
       created_at: new Date().toISOString(),
       confirmation_message: `Twoje zgłoszenie zostało przyjęte do weryfikacji. Numer: ${ticketNumber}. Skontaktujemy się w ciągu 24 godzin.`
     }
   }];
   ```
3. Node **Return**. Zapisz i aktywuj.

**Faza 5 — Master Workflow (20 min)**

1. Nowy workflow: `[MASTER] Corporate Request Router`
2. Node **Webhook** (lub **Form Trigger**) — pola: `email`, `subject`, `description`, `department`, `priority`
3. Node **Switch** — nazwa: `[SWITCH] Klasyfikuj Dział`
   - Wartość do sprawdzenia: `{{ $json.department }}`
   - Output 1: wartość = `IT` → etykieta: "IT Support"
   - Output 2: wartość = `HR` → etykieta: "Human Resources"
   - Output 3: wartość = `Finance` → etykieta: "Finanse"
   - Output 4 (Fallback / Default): etykieta: "Inne"
4. Podepnij każdy output Switch do odpowiedniego node'a **Execute Workflow**:
   - Output "IT" → Execute Workflow ID: `[SUB] IT — Obsłuż Zgłoszenie`
   - Output "HR" → Execute Workflow ID: `[SUB] HR — Obsłuż Zgłoszenie`
   - Output "Finance" → Execute Workflow ID: `[SUB] Finance — Obsłuż Zgłoszenie`
   - Output "Inne" → Execute Workflow ID: `[SUB] Other — Kolejka Ręczna`
5. Po każdym Execute Workflow podepnij node **Merge** (tryb: Merge by Position)
6. Po Merge: node **Gmail** (lub **Send Email**) — wyślij potwierdzenie:
   - Do: `{{ $json.requester }}`
   - Temat: `Potwierdzenie zgłoszenia {{ $json.ticket_number }}`
   - Treść: `{{ $json.confirmation_message }}`
7. Ostatni node: **Respond to Webhook** z `{ "status": "ok", "ticket": "{{ $json.ticket_number }}" }`

> Jeśli nie masz skonfigurowanego Gmail w n8n — zastąp node emailowy node'em **Set** który tylko zapisuje dane. Logika routowania jest ważniejsza niż integracja emailowa w tym ćwiczeniu.

### Testowanie

Przetestuj każdą ścieżkę osobno, wysyłając testowe dane z różnym polem `department`:

| Test | Pole `department` | Oczekiwany prefix ticketu |
|---|---|---|
| 1 | `IT` | `IT-XXXXXX` |
| 2 | `HR` | `HR-XXXXXX` |
| 3 | `Finance` | `FIN-XXXXXX` |
| 4 | `Marketing` (nieznany) | `OTH-XXXXXX` |

### Kryteria sukcesu

- [ ] Switch node poprawnie kieruje do 4 różnych ścieżek
- [ ] Każdy subworkflow zwraca unikalny numer ticketu z odpowiednim prefixem
- [ ] Master workflow wysyła (lub przygotowuje) email z potwierdzeniem
- [ ] Webhook odpowiada z `{ "status": "ok" }` niezależnie od ścieżki
- [ ] Wszystkie node'y w master workflow mają czytelne nazwy (nie "Execute Workflow", "Execute Workflow 1" itd.)

---

## Ćwiczenie 3 — Naming Convention Audit (10 min)

### Cel

Przeprowadzić szybki audit własnych workflow z poprzednich tygodni i zastosować konwencje nazewnictwa z Modułu 4.

### Konwencja nazewnictwa nodów (przypomnienie)

Format: **[Typ] Opis akcji**

| Typ | Kiedy używać | Przykład |
|---|---|---|
| `HTTP` | Zapytania do API | `HTTP Pobierz dane GUS` |
| `SET` | Transformacja danych | `SET Przygotuj payload emaila` |
| `IF` | Rozgałęzienie binarne | `IF Czy email jest poprawny?` |
| `SWITCH` | Routing wielokierunkowy | `SWITCH Klasyfikuj typ zgłoszenia` |
| `CODE` | Node JavaScript | `CODE Generuj numer ticketu` |
| `SHEETS` | Google Sheets | `SHEETS Zapisz lead` |
| `GMAIL` | Wysyłka emaila | `GMAIL Wyślij potwierdzenie` |
| `MERGE` | Łączenie ścieżek | `MERGE Zbierz wyniki subworkflows` |
| `SUB` | Execute Workflow | `SUB Waliduj email` |
| `LOG` | Logowanie / monitoring | `LOG Zapisz błąd do arkusza` |

### Krok po kroku

1. Otwórz każdy workflow z Tygodni 1–3 (Lead Capture, Email Automation, AI Agent lub cokolwiek zbudowałeś)
2. Kliknij dwukrotnie na każdy node i zmień jego nazwę zgodnie z konwencją powyżej
3. Zidentyfikuj logiczne sekcje w workflow (np. "Walidacja wejścia", "Przetwarzanie", "Powiadomienie") i dodaj Sticky Note opisujący każdą sekcję

**Jak dodać Sticky Note:**
- Prawy przycisk myszy na pustym miejscu canvasu → "Add Sticky Note"
- Zmień tło na żółte dla ważnych sekcji, niebieskie dla informacyjnych
- Rozmiar: taki, żeby obejmował node'y danej sekcji

### Kryteria sukcesu

- [ ] Żaden node nie ma domyślnej nazwy (np. "HTTP Request", "Set", "If", "Code")
- [ ] Co najmniej 2 Sticky Notes opisują sekcje logiczne workflow
- [ ] Podgląd workflow "na zimno" (jakbyś widział go pierwszy raz) — czy rozumiesz co robi bez otwierania nodów?

---

## Zadanie Domowe

### Część A — Subworkflow "Urgent" z alertem SMS

Rozszerz swój Request Router o nową ścieżkę dla pilnych zgłoszeń. Gdy pole `priority` = `urgent`, workflow powinien wysłać SMS alert zanim skieruje ticket do odpowiedniego działu.

**Krok po kroku:**

1. Utwórz nowy subworkflow: `[SUB] Alert — Wyślij SMS Urgent`
2. Wybierz jedną z opcji integracji SMS:
   - **Twilio** (rekomendowany) — darmowe konto trial daje 15 USD kredytu, wystarczy na setki SMSów testowych. Node "Twilio" dostępny w n8n.
   - **CallMeBot** (bezpłatny, tylko WhatsApp) — API URL: `https://api.callmebot.com/whatsapp.php?phone=TWÓJ_NUMER&text=TREŚĆ&apikey=TWÓJ_KLUCZ`
   - **Mock SMS** — node HTTP Request do `https://httpbin.org/post` z polem `sms_content` (symulacja bez prawdziwego SMSa)
3. Treść SMS: `URGENT: Nowe pilne zgłoszenie [ticket_number] od [requester]: [subject]`
4. W Master Workflow dodaj przed Switch node'em node **If** sprawdzający `{{ $json.priority == "urgent" }}`:
   - TRUE: najpierw `SUB Alert — Wyślij SMS Urgent`, potem normalny Switch routing
   - FALSE: bezpośrednio do Switch
5. Przetestuj wysyłając zgłoszenie z `priority = urgent` i `department = IT`

### Część B — Dokumentacja architektury (1 strona)

Napisz krótki dokument opisujący architekturę swojego Request Routera. Nie musi być długi — chodzi o ćwiczenie myślenia architektonicznego i komunikowania decyzji technicznych. Dokument powinien zawierać:

**Sekcja 1: Przegląd systemu (2-3 zdania)**
Co robi system? Jaki problem rozwiązuje? Kto jest użytkownikiem końcowym?

**Sekcja 2: Diagram komponentów**
Prosty ASCII diagram lub opis słowny: master workflow → jakie subworkflows → jakie integracje zewnętrzne (Sheets, Gmail, SMS itd.)

**Sekcja 3: Input/Output Contracts (tabela)**
Dla każdego subworkflow: co przyjmuje na wejściu, co zwraca na wyjściu

| Subworkflow | Input (pola) | Output (pola) |
|---|---|---|
| IT Support | email, subject, priority | ticket_number, department, confirmation_message |
| HR | email, subject | ticket_number, department, confirmation_message |
| Finance | email, subject | ticket_number, department, confirmation_message |
| Other | email, subject | ticket_number, department, confirmation_message |
| Alert SMS | ticket_number, requester, subject | sms_sent (bool), sms_status |

**Sekcja 4: Decyzje architektoniczne (2-3 punkty)**
Dlaczego wybrałeś taką strukturę? Jakie alternatywy rozważałeś? Co byś zmienił gdybyś miał więcej czasu?

**Sekcja 5: Jak rozbudować (opcjonalnie)**
Co jest następnym krokiem? Np. dodanie kolejki (integracja z Jira/Linear), dashboard statusu ticketów, automatyczne SLA monitorowanie.

> Wskazówka: Zapisz dokument jako Markdown lub Google Doc. W przyszłości taki dokument będzie punktem wejścia dla każdego nowego członka zespołu który będzie pracował z systemem.

---

## Podsumowanie modułu — checklista

Przed przejściem do Modułu 5 upewnij się, że:

- [ ] Rozumiesz różnicę między Execute Workflow synchronicznym a asynchronicznym
- [ ] Potrafisz zdefiniować "input contract" i "output contract" dla subworkflow
- [ ] Twoje workflow mają czytelne nazwy nodów i Sticky Notes
- [ ] Zbudowałeś przynajmniej jedną architekturę master + subworkflows

W Module 5 wrócimy do AI — ale tym razem zbudujemy system z **Human in the Loop**: AI podejmuje decyzję, człowiek ją zatwierdza lub odrzuca, workflow reaguje. Do zobaczenia!
