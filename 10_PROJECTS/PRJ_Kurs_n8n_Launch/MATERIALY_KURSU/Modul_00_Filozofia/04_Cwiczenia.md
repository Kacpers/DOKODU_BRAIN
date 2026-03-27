# Moduł 0: Ćwiczenie — Twoje pierwsze 15 minut z n8n

> **Cel ćwiczenia:** Uruchomić n8n lokalnie i zbudować pierwszy działający workflow: Webhook → wysyłka emaila przez Gmail.
>
> **Czas:** 15–25 minut (przy pierwszym razie, łącznie z czekaniem na Docker)
>
> **Trudność:** Beginner — zero wcześniejszego doświadczenia z automatyzacją

---

## Zanim zaczniesz — co potrzebujesz

- [ ] Komputer z systemem Windows 10/11, macOS 12+, lub Linux Ubuntu 20.04+
- [ ] Połączenie z internetem (pobieranie obrazu Docker ~200 MB)
- [ ] Konto Gmail (dowolne — możesz stworzyć testowe)
- [ ] 20–30 minut spokojnego czasu

**Nie potrzebujesz:**
- Wiedzy programistycznej
- Serwera
- Karty kredytowej
- Żadnych płatnych narzędzi

---

## CZĘŚĆ 1 — Instalacja Docker i uruchomienie n8n

### Krok 1: Zainstaluj Docker Desktop

> *(Jeśli masz już Docker — przejdź do Kroku 3)*

**Windows i macOS:**
1. Wejdź na [docker.com/products/docker-desktop](https://docker.com/products/docker-desktop)
2. Pobierz wersję dla swojego systemu
3. Uruchom instalator, kliknij Next/Install
4. Po instalacji uruchom Docker Desktop
5. Poczekaj na zielony znacznik w zasobniku systemowym ("Docker is running")

**Linux (Ubuntu):**
```bash
sudo apt-get update
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo usermod -aG docker $USER
# Wyloguj się i zaloguj ponownie żeby zmiany zadziałały
```

*Co powinieneś zobaczyć:* Po uruchomieniu Docker Desktop — ikona wieloryba w pasku zadań (Windows/Mac) lub komenda `docker --version` zwraca numer wersji (Linux).

---

### Krok 2: Weryfikacja Docker

Otwórz terminal (Windows: PowerShell lub CMD, macOS: Terminal, Linux: bash) i uruchom:

```bash
docker --version
```

*Co powinieneś zobaczyć:*
```
Docker version 24.x.x, build xxxxxxx
```

Jeśli widzisz błąd — sprawdź czy Docker Desktop jest uruchomiony (zielona ikona).

---

### Krok 3: Uruchom n8n

Wklej tę komendę do terminala i naciśnij Enter:

```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  docker.n8n.io/n8nio/n8n
```

**Co robi ta komenda (nie musisz zapamiętywać — ale warto wiedzieć):**
- `docker run` — uruchom kontener
- `--name n8n` — nazwij go "n8n"
- `-p 5678:5678` — wystaw port 5678 na localhost
- `-v ~/.n8n:/home/node/.n8n` — zapisuj dane w folderze `.n8n` na Twoim komputerze (persistent storage)
- `docker.n8n.io/n8nio/n8n` — oficjalny obraz n8n

*Co powinieneś zobaczyć (pierwsze uruchomienie — 1-3 minuty):*
```
Unable to find image 'docker.n8n.io/n8nio/n8n:latest' locally
latest: Pulling from n8nio/n8n
...
Editor is now accessible via:
http://localhost:5678
```

*Gdy zobaczysz "Editor is now accessible via: http://localhost:5678" — przejdź do następnego kroku.*

- [ ] n8n uruchomiony i dostępny na localhost:5678

---

### Krok 4: Pierwsze logowanie

1. Otwórz przeglądarkę (Chrome, Firefox, Edge — dowolna)
2. Wejdź na `http://localhost:5678`
3. Wypełnij formularz rejestracji:
   - Email: wpisz swój email (lub `test@test.pl` — do ćwiczeń nie ma znaczenia)
   - Hasło: min. 8 znaków, jakiekolwiek
4. Kliknij "Get started"
5. Przejdź przez krótki onboarding (możesz klikać "Skip" we wszystkich pytaniach)

*Co powinieneś zobaczyć:* Główny interfejs n8n — sidebar po lewej, pusty canvas w środku, przycisk "+ New Workflow" lub podobny.

- [ ] Zalogowany do n8n

---

## CZĘŚĆ 2 — Połącz konto Gmail

> **Dlaczego to robimy pierwsze?** Autoryzacja OAuth2 wymaga kilku kroków konfiguracji i lepiej zrobić to zanim zaczniesz budować workflow, żeby nie przerywać przepływu.

### Krok 5: Utwórz Google OAuth2 Credentials w n8n

1. W sidebarze po lewej znajdź **"Credentials"** (lub kliknij ikonę klucza)
2. Kliknij **"+ Add credential"**
3. Wyszukaj **"Gmail OAuth2"**
4. Kliknij na wynik

*Co powinieneś zobaczyć:* Formularz z polami "Client ID" i "Client Secret"

---

### Krok 6: Utwórz Google Cloud Project (jednorazowo)

> *(Brzmi skomplikowanie, ale zajmuje 5 minut i robi się raz)*

1. Wejdź na [console.cloud.google.com](https://console.cloud.google.com)
2. Zaloguj się swoim kontem Gmail
3. Na górze — kliknij **"Wybierz projekt"** → **"Nowy projekt"**
4. Nazwa projektu: `n8n-kurs` (cokolwiek)
5. Kliknij **"Utwórz"**

*Co powinieneś zobaczyć:* Nowy projekt wybrany w górnym menu.

---

### Krok 7: Włącz Gmail API

1. W Google Cloud Console — znajdź menu hamburger (≡) → **"APIs & Services"** → **"Library"**
2. Wyszukaj **"Gmail API"**
3. Kliknij na wynik → **"Enable"**

*Co powinieneś zobaczyć:* Status API zmienia się na "Enabled".

---

### Krok 8: Utwórz OAuth2 credentials w Google Cloud

1. Menu → **"APIs & Services"** → **"Credentials"**
2. Kliknij **"+ Create Credentials"** → **"OAuth client ID"**
3. Jeśli system pyta o "Configure Consent Screen":
   - User Type: External
   - App name: `n8n-test`
   - Support email: Twój email
   - Kliknij Save and Continue aż do końca (wszystkie pozostałe pola możesz pominąć)
4. Wróć do tworzenia OAuth client ID:
   - Application type: **Web application**
   - Name: `n8n-kurs`
   - Authorized redirect URIs: kliknij **"+ Add URI"** i wpisz:
     `http://localhost:5678/rest/oauth2-credential/callback`
5. Kliknij **"Create"**
6. Skopiuj **Client ID** i **Client Secret** z okna które się pojawi

---

### Krok 9: Wklej credentials do n8n

1. Wróć do n8n (zakładka z localhost:5678)
2. W formularzu Gmail OAuth2:
   - Client ID: wklej z Google Cloud
   - Client Secret: wklej z Google Cloud
3. Kliknij **"Sign in with Google"**
4. Zaloguj się na swoje konto Gmail
5. Kliknij **"Allow"** / **"Zezwól"**

*Co powinieneś zobaczyć:* Zielony znacznik "Connected" przy credentials.

- [ ] Gmail OAuth2 credentials połączone

---

## CZĘŚĆ 3 — Zbuduj workflow

### Krok 10: Utwórz nowy workflow

1. W sidebarze kliknij **"Workflows"**
2. Kliknij **"+ New Workflow"** lub przycisk "+" na canvasie
3. Kliknij na tytuł (domyślnie "My workflow") i zmień na: **"Hello Automation"**
4. Kliknij Save (Ctrl+S / Cmd+S)

- [ ] Nowy workflow "Hello Automation" utworzony

---

### Krok 11: Dodaj node Webhook (Trigger)

1. Kliknij **"+"** na pustym canvasie lub przycisk "Add first step"
2. Wyszukaj **"Webhook"**
3. Kliknij na wynik — node pojawi się na canvasie
4. Kliknij na node żeby otworzyć konfigurację:
   - HTTP Method: **POST**
   - Path: **hello-automation** (możesz wpisać cokolwiek)
5. Skopiuj **"Test URL"** — będzie Ci potrzebny w Kroku 14

*Co powinieneś zobaczyć:* Node "Webhook" na canvasie z ikonką wtyczki. W panelu po prawej — URL w stylu `http://localhost:5678/webhook-test/hello-automation`

- [ ] Node Webhook skonfigurowany i URL skopiowany

---

### Krok 12: Dodaj node Set (przetwarzanie danych)

1. Najedź na prawy brzeg node'a Webhook — pojawi się "+"
2. Kliknij **"+"** → wyszukaj **"Set"**
3. Kliknij wynik — node Set pojawi się połączony z Webhookiem
4. W konfiguracji Set node:
   - Kliknij **"Add value"**
   - Name: **`recipientName`**
   - Value: kliknij ikonę `{}` (expression) i wpisz: **`{{ $json.body.name }}`**
   - Kliknij **"Add value"** drugi raz
   - Name: **`recipientEmail`**
   - Value: **`{{ $json.body.email }}`**

*Co powinieneś zobaczyć:* Dwa pola w Set node z expressions w nawiasach klamrowych.

> **Tip:** Expressions `{{ }}` to sposób n8n na odwoływanie się do danych z poprzednich nodów. `$json.body.name` oznacza: "z danych JSON które przyszły, pole `body`, a w nim pole `name`".

- [ ] Node Set skonfigurowany z polami recipientName i recipientEmail

---

### Krok 13: Dodaj node Gmail (akcja wysyłki)

1. Kliknij **"+"** na wyjściu Set node
2. Wyszukaj **"Gmail"** → wybierz **"Gmail"** (nie "Gmail Trigger")
3. W konfiguracji:
   - Credential: wybierz credentials które stworzyłeś w Kroku 9
   - Resource: **Message**
   - Operation: **Send**
   - To: kliknij `{}` → wpisz **`{{ $json.recipientEmail }}`**
   - Subject: **`Cześć {{ $json.recipientName }}, witamy Cię!`**
   - Email Type: **Text**
   - Message: wpisz tekst (przykład poniżej):
     ```
     Hej {{ $json.recipientName }}!

     Dziękujemy za kontakt. Twoja automatyzacja działa!

     To jest pierwszy email wysłany przez Twój workflow w n8n.

     Pozdrawiam,
     Kacper z Dokodu
     ```

*Co powinieneś zobaczyć:* Trzy nody połączone strzałkami: Webhook → Set → Gmail

- [ ] Node Gmail skonfigurowany z expressions

---

### Krok 14: Przetestuj workflow

1. Kliknij na node **Webhook** → w panelu kliknij **"Listen for test event"**
2. n8n czeka na dane (piszze "Waiting for test event...")
3. Otwórz nowy terminal i uruchom:

**macOS / Linux:**
```bash
curl -X POST http://localhost:5678/webhook-test/hello-automation \
  -H "Content-Type: application/json" \
  -d '{"name": "Kacper", "email": "TWOJ_EMAIL@gmail.com"}'
```

**Windows (PowerShell):**
```powershell
Invoke-RestMethod -Uri "http://localhost:5678/webhook-test/hello-automation" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"name": "Kacper", "email": "TWOJ_EMAIL@gmail.com"}'
```

> **Ważne:** Zamień `TWOJ_EMAIL@gmail.com` na Twój prawdziwy email — bo za chwilę sprawdzisz skrzynkę!

4. W n8n powinieneś zobaczyć że Webhook odebrał dane (zielone "1 item")
5. Kliknij **"Test step"** albo **"Execute all"** żeby uruchomić resztę workflow

*Co powinieneś zobaczyć:* Zielone znaczniki przy każdym node. W Execution log — dane przepływają przez węzły.

6. Sprawdź swoją skrzynkę Gmail

- [ ] Email dotarł na skrzynkę

---

### Krok 15: Aktywuj workflow

1. Na górze canvasu — kliknij przełącznik **"Inactive"** → zmień na **"Active"**
2. Teraz workflow działa nie tylko w trybie testowym, ale na prawdziwym URL:
   - Test URL: `http://localhost:5678/webhook-test/hello-automation` (tylko gdy workflow jest w trybie "listen")
   - Production URL: `http://localhost:5678/webhook/hello-automation` (działa zawsze gdy workflow aktywny)

3. Przetestuj production URL:
```bash
curl -X POST http://localhost:5678/webhook/hello-automation \
  -H "Content-Type: application/json" \
  -d '{"name": "Anna", "email": "TWOJ_EMAIL@gmail.com"}'
```

- [ ] Workflow aktywny i działa na production URL

---

## Gratulacje — Twój pierwszy workflow działa!

Właśnie zbudowałeś coś co:
- Odbiera dane z zewnętrznego systemu przez HTTP
- Przetwarza i przekształca te dane
- Wysyła spersonalizowanego emaila

To jest fundament 80% workflow które budujesz dla klientów. Tylko skala i złożoność rosną.

---

## TROUBLESHOOTING — 5 najczęstszych błędów

### Błąd 1: "Cannot connect to Docker daemon" / Docker nie startuje

**Objawy:** Komenda `docker run` zwraca błąd o połączeniu.

**Przyczyna:** Docker Desktop nie jest uruchomiony.

**Rozwiązanie:**
1. Znajdź ikonę Docker Desktop w zasobniku systemowym (wieloryb)
2. Jeśli nie ma — uruchom Docker Desktop z menu Start/Applications
3. Poczekaj aż ikona stanie się zielona lub nieruchoma (nie animowana)
4. Spróbuj ponownie komendy `docker --version`

---

### Błąd 2: "Port 5678 already in use"

**Objawy:** n8n nie startuje, błąd o zajętym porcie.

**Przyczyna:** Inny program używa portu 5678, albo poprzednia instancja n8n nie zamknęła się poprawnie.

**Rozwiązanie:**

```bash
# Sprawdź co używa portu
# macOS/Linux:
lsof -i :5678

# Windows (PowerShell):
netstat -ano | findstr :5678

# Zabij poprzedni kontener n8n:
docker stop n8n
docker rm n8n

# Uruchom ponownie
```

Albo zmień port w komendzie uruchomienia: `-p 5679:5678` i wejdź na `localhost:5679`.

---

### Błąd 3: Gmail OAuth — "redirect_uri_mismatch"

**Objawy:** Podczas autoryzacji Google pokazuje błąd "redirect_uri_mismatch" lub "Error 400".

**Przyczyna:** URI w Google Cloud Console nie pasuje do URI n8n.

**Rozwiązanie:**
1. Wróć do Google Cloud Console → Credentials → Twój OAuth client
2. W "Authorized redirect URIs" upewnij się że jest DOKŁADNIE:
   `http://localhost:5678/rest/oauth2-credential/callback`
3. Bez spacji, bez ukośnika na końcu, http (nie https)
4. Kliknij Save i spróbuj ponownie w n8n

---

### Błąd 4: Expression `{{ $json.body.name }}` zwraca "undefined"

**Objawy:** Email wychodzi, ale zamiast imienia jest pusty tekst lub "undefined".

**Przyczyna:** Dane w JSON mają inną strukturę niż się spodziewasz.

**Rozwiązanie:**
1. Kliknij na node Webhook → zakładka "Output"
2. Sprawdź jak wygląda struktura danych które odebrał
3. Jeśli struktura to `{ "name": "Kacper" }` bez wrappera "body" — użyj `{{ $json.name }}`
4. Jeśli curl wysyłał `body.name` a struktura jest inna — sprawdź czy dodałeś `-H "Content-Type: application/json"` do komendy curl

**Jak sprawdzić strukturę danych:**
```
Kliknij node Webhook → Input/Output panel po prawej → zobaczysz dokładne drzewo danych
```

---

### Błąd 5: Workflow aktywny ale email nie przychodzi

**Objawy:** curl zwraca sukces, ale email nie dociera. Workflow execution nie widać.

**Przyczyna:** Używasz Test URL zamiast Production URL, albo workflow jest w trybie "Inactive".

**Rozwiązanie:**
1. Sprawdź czy workflow ma włączony przełącznik "Active" (zielony)
2. Test URL działa tylko gdy klikniesz "Listen for test event" — do normalnego działania używaj Production URL
3. Production URL: `http://localhost:5678/webhook/[twoja-sciezka]` (bez "-test")
4. Sprawdź Executions (sidebar) — jeśli workflow był wywołany, zobaczysz wpis (sukces lub błąd)

---

## Checkpoint — Co powinieneś mieć po ćwiczeniu

- [ ] Docker Desktop zainstalowany i działa
- [ ] n8n dostępny na `http://localhost:5678`
- [ ] Konto n8n utworzone (email + hasło)
- [ ] Gmail OAuth2 credentials skonfigurowane
- [ ] Workflow "Hello Automation" zbudowany (3 nody)
- [ ] Email testowy odebrany na skrzynce
- [ ] Workflow aktywowany i przetestowany na Production URL

---

## Co dalej?

Zrobiłeś podstawowy webhook → email. W Module 1 kursu budujemy to samo, ale:
- Z prawdziwym CRM (Notion, Airtable, lub Google Sheets jako CRM)
- Z logiką warunkową (IF node)
- Z obsługą błędów (Error workflow)
- Z formatowaniem HTML emaila

Jeśli chcesz poćwiczyć zanim przejdziesz dalej — spróbuj:

**Wyzwanie 1 (łatwe):** Dodaj pole "company" do danych testowych i użyj go w treści emaila.

**Wyzwanie 2 (średnie):** Przed wysłaniem emaila — zapisz dane do Google Sheets (node Google Sheets → Append Row).

**Wyzwanie 3 (trudniejsze):** Dodaj IF node między Set a Gmail: jeśli `name` zawiera słowo "Kacper" — wyślij inny email niż do pozostałych.
