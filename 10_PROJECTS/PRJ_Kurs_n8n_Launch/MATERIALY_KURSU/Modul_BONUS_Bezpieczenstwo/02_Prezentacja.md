---
type: course-material
modul: BONUS_A
status: ready
owner: kacper
last_reviewed: 2026-03-27
tags: [kurs, n8n, bezpieczenstwo, prezentacja, slajdy]
---

# Moduł BONUS A — Prezentacja (27 slajdów)

> **Styl:** Ciemne tło (dark mode), akcenty pomarańczowe Dokodu, font: Inter
> **Narzędzie:** Canva / Google Slides — szablon Dokodu
> **Rozdzielczość:** 1920×1080

---

## Slajd 1: TYTUŁ MODUŁU

**Bezpieczeństwo i Compliance w n8n**
*Jeden niezabezpieczony webhook = wyciek danych 10 000 klientów*

Moduł BONUS A | ~90 minut
Kacper Sieradzński + Alina Sieradzińska

> 🎙️ NOTATKA: Otwieramy mocno — nie suchą teorią, ale konkretnym incydentem. Chwila ciszy po slajdzie przed przejściem dalej.

---

## Slajd 2: DLACZEGO TEN MODUŁ JEST INNY

**Nikt w Polsce tego nie robi**

- Inne kursy n8n: tylko "jak działa" — zero bezpieczeństwa
- My: Tech (Kacper) + Legal (Alina) = pełny obraz
- AI Act wchodzi w pełni 08.2026 — masz 5 miesięcy
- Po tym module: wiesz co zrobić zanim klient zapyta o compliance

> 🎙️ NOTATKA: Kacper mówi to z energią — to jest przewaga konkurencyjna kursu. Podkreśl "5 miesięcy" — jest konkretna data.

---

## Slajd 3: CO OMÓWIMY — MAPA MODUŁU

**6 obszarów bezpieczeństwa:**

1. Credential Vault — gdzie trzymasz sekrety
2. RODO w automatyzacjach — dane osobowe w workflow
3. AI Act — które automatyzacje są high-risk
4. Bezpieczeństwo sieci — webhook, proxy, rate limiting
5. Logowanie i audit trail — co zapisywać
6. Server-side tracking — dlaczego to ważne

> 🎙️ NOTATKA: Pokaż tę mapę i wróć do niej na początku każdego segmentu — uczący wiedzą gdzie są.

---

## Slajd 4: CREDENTIAL VAULT — ARCHITEKTURA WYBORU

**n8n built-in vault** | HashiCorp Vault
---|---
Startup, 1-2 środowiska | Enterprise, wiele środowisk
Szyfrowanie AES (klucz w env) | Dynamiczne sekrety, rotacja
Wystarczy do ~10 integracji | Wymagany przy audytach ISO 27001
Łatwa konfiguracja | Wymaga dedykowanego serwera

**Reguła Dokodu:** n8n Credentials + silny `N8N_ENCRYPTION_KEY` = OK dla 90% projektów.
Vault → gdy klient pyta o certyfikaty bezpieczeństwa.

> 🎙️ NOTATKA: Pokaż tabelę, powiedz że pokażemy demo obu podejść. Nie strasz Vaultem na starcie.

---

## Slajd 5: N8N ENCRYPTION KEY — KRYTYCZNA KONFIGURACJA

```bash
# .env — NEVER commit to git!
N8N_ENCRYPTION_KEY=tu-wygeneruj-losowy-string-64-znaki

# Generowanie bezpiecznego klucza:
openssl rand -hex 32
```

**Złe praktyki (realne z audytów):**
- `N8N_ENCRYPTION_KEY=changeme` — widziane na produkcji!
- Klucz w repozytorium git (historia nie kłamie)
- Ten sam klucz na dev i prod

**Dobre praktyki:**
- Klucz w `.env` → `.env` w `.gitignore`
- Różne klucze per środowisko
- Backup klucza w bezpiecznym miejscu (1Password / Bitwarden)

> 🎙️ NOTATKA: Kacper — pokaż realny przykład z terminala jak wygenerować klucz. "changeme na produkcji" — mówisz to z lekkim niedowierzaniem, bo naprawdę to widziałeś.

---

## Slajd 6: LEAST PRIVILEGE — ZASADA MINIMALNYCH UPRAWNIEŃ

**Jeden klucz API do wszystkiego = jedna awaria do katastrofy**

```
ZLE:
OpenAI API Key: sk-... (jeden klucz, wszystkie workflowy)
  ↓
Workflow A (email summary) — ma dostęp do billing API
Workflow B (HR screening) — ma dostęp do wszystkiego
Workflow C (chatbot) — ma dostęp do wszystkiego

DOBRZE:
OpenAI Project API Key dla Workflow A: tylko model gpt-4o-mini, bez fine-tuning
OpenAI Project API Key dla Workflow B: osobny projekt, osobny monitoring
OpenAI Project API Key dla Workflow C: rate limit 100 req/min
```

> 🎙️ NOTATKA: Diagram "złe vs dobre" — narysuj strzałki. Powiedz o OpenAI Projects jako narzędziu do izolacji kluczy.

---

## Slajd 7: RODO W N8N — CO TO JEST DANA OSOBOWA

**Dane osobowe w workflow n8n — częstsze niż myślisz:**

| Co widzisz | Czy to dana osobowa? |
|---|---|
| jan.kowalski@firma.pl | TAK — bezpośrednia |
| 192.168.1.45 (IP) | TAK — gdy można powiązać z osobą |
| "Kowalski zamówił X" | TAK — imię + działanie |
| ID klienta #12345 | MOŻE — jeśli można przypisać do osoby |
| Wartość zamówienia: 5000 PLN | NIE — samo w sobie |
| Timestamp + IP + User-Agent | TAK — profilowanie |

**Pułapka:** "anonimizowałem dane" — ale zostawiłem timestamp + IP + kategoria produktu = wciąż identyfikowalny.

> 🎙️ NOTATKA: Alina mówi ten slajd. Tabela jest konkretna — uczący często nie wiedzą że IP to dana osobowa. Zatrzymaj się przy pułapce na dole.

---

## Slajd 8: PODSTAWY PRAWNE PRZETWARZANIA (Art. 6 RODO)

**Które podstawy prawne stosujesz w automatyzacjach?**

| Podstawa | Kiedy stosować | Przykład w n8n |
|---|---|---|
| **Zgoda** (6a) | Marketing, newsletter | Lead form → CRM workflow |
| **Umowa** (6b) | Obsługa klienta | Invoice parser, order processing |
| **Uzasadniony interes** (6f) | B2B, fraud detection | Email classifier dla supportu |
| **Obowiązek prawny** (6c) | Księgowość, podatki | Archiwizacja faktur 5 lat |

**Uwaga:** Uzasadniony interes wymaga "testu balansu" — nie stosuj go automatycznie.

> 🎙️ NOTATKA: Alina tłumaczy tabele. Podkreśl że "zgoda" jest najsłabszą podstawą — można ją wycofać. Uzasadniony interes jest mocniejszy ale wymaga dokumentacji.

---

## Slajd 9: PSEUDONIMIZACJA VS ANONIMIZACJA

```
PSEUDONIMIZACJA (odwracalna):
jan.kowalski@firma.pl → sha256("jan.kowalski@firma.pl") = "a3f2b1..."
Klucz mapowania: { "a3f2b1..." : "jan.kowalski@firma.pl" }
→ Można odwrócić mając klucz mapowania
→ RODO nadal stosuje się do pseudonimizowanych danych!

ANONIMIZACJA (nieodwracalna):
jan.kowalski@firma.pl → "[EMAIL_REDACTED]"
Lub: 192.168.1.45 → "192.168.x.x" (obcięcie ostatniego oktetu)
→ Nie można odwrócić
→ RODO nie stosuje się (brak możliwości identyfikacji)
```

**Reguła:** Pseudonimizacja redukuje ryzyko przy naruszeniu. Anonimizacja wyklucza cię z zakresu RODO dla tych danych.

> 🎙️ NOTATKA: Kacper — pokaż kod SHA-256 w n8n. Alina dodaje komentarz prawny: "pseudonimizacja nie = anonimizacja, RODO nadal obowiązuje".

---

## Slajd 10: PSEUDONIMIZACJA W CODE NODE — KOD GOTOWY

```javascript
// Pseudonimizacja e-maila (SHA-256)
const crypto = require('crypto');

const pseudonymize = (value, salt = process.env.PSEUDONYM_SALT) => {
  if (!value) return null;
  return crypto
    .createHash('sha256')
    .update(salt + value.toLowerCase().trim())
    .digest('hex')
    .substring(0, 16); // skróć do 16 znaków — wystarczy
};

// Użycie:
const items = $input.all();
return items.map(item => ({
  json: {
    ...item.json,
    email: pseudonymize(item.json.email),     // "a3f2b1c4d5e6f7g8"
    phone: pseudonymize(item.json.phone),     // pseudonimy
    name: '[REDACTED]',                        // anonimizacja imienia
    order_value: item.json.order_value,        // nie jest PII — zostaw
    order_id: item.json.order_id,              // wewnętrzny ID — OK
  }
}));
```

> 🎙️ NOTATKA: Kacper pokazuje ten kod w n8n. Ważne: PSEUDONYM_SALT musi być w zmiennych środowiskowych — nie hardcoded. Zatrzymaj się przy "skróć do 16 znaków" — wyjaśnij że pełny SHA-256 = 64 znaki, to za dużo dla DB.

---

## Slajd 11: RODO CHECKLIST DLA WORKFLOW N8N

**Przed deploymentem produkcyjnym — sprawdź każdy punkt:**

**Dane**
- [ ] Zidentyfikowane wszystkie pola z PII (email, IP, imię, PESEL, telefon)
- [ ] Zdefiniowana podstawa prawna (Art. 6 RODO) — zapisana w dokumentacji
- [ ] Dane minimalne: czy zbierasz TYLKO to co potrzebujesz?
- [ ] Czas retencji zdefiniowany i skonfigurowany technicznie

**Techniczne**
- [ ] PII nie trafia do logów n8n (wyłącz "Save Execution Data" dla wrażliwych węzłów)
- [ ] Pseudonimizacja/anonimizacja przed wysyłką do zewnętrznych API (OpenAI, Google)
- [ ] Szyfrowanie in-transit: TLS 1.3 na wszystkich połączeniach
- [ ] Sekrety w Vault / env variables — nie w workflow JSON

**Umowy**
- [ ] Umowa powierzenia przetwarzania (Art. 28) z klientem
- [ ] DPA podpisane z dostawcami API (OpenAI, Google Cloud, Anthropic)

**Prawo do usunięcia**
- [ ] Workflow do obsługi wniosków RTBF (Right to be Forgotten)
- [ ] Zidentyfikowane wszystkie systemy gdzie dane są przechowywane (n8n, CRM, Google Sheets, baza)
- [ ] Termin odpowiedzi: 30 dni — monitoring aktywny

> 🎙️ NOTATKA: Ten slajd to materiał do pobrania — PDF dla uczestników. Przejdź przez każdy punkt powoli. Alina komentuje sekcję "Umowy" — to najczęściej pomijane.

---

## Slajd 12: PRAWO DO USUNIĘCIA DANYCH — AUTOMATYZACJA WNIOSKU

```
WORKFLOW: RTBF (Right to be Forgotten) Handler

[Webhook: wniosek RTBF]
    → [Weryfikacja tożsamości: token email]
    → [Wyszukanie we WSZYSTKICH systemach]:
        ├── CRM (HubSpot / Pipedrive)
        ├── Google Sheets (dane leadów)
        ├── Baza n8n (execution history)
        └── Newsletter (MailerLite / ActiveCampaign)
    → [Usunięcie lub pseudonimizacja]
    → [Log do audytu: "data_deleted" event]
    → [Email potwierdzający do osoby]
    → [Zapis do rejestru RTBF (Art. 30 RODO)]
```

**Termin:** 30 dni od złożenia wniosku (RODO)
**Uwaga:** Niektórych danych nie możesz usunąć — faktury przechowujesz 5 lat (prawo podatkowe). Masz obowiązek poinformować osobę o tym wyjątku.

> 🎙️ NOTATKA: Kacper rysuje diagram na żywo w n8n lub pokazuje gotowy blueprint. Alina komentuje "5 lat faktur" — wyjątek który zawsze ludzi zaskakuje.

---

## Slajd 13: AI ACT — MAPA RYZYKA (2024/1689)

**4 poziomy ryzyka — gdzie jesteś?**

```
UNACCEPTABLE (ZAKAZANE od 02.2025)
├── Social scoring
├── Biometryka real-time w przestrzeni publicznej
└── Manipulacyjne AI

HIGH RISK (pełne wymagania od 08.2026)
├── HR: screening CV, ocena pracowników        ← UWAGA dla agencji!
├── Edukacja: ocenianie uczniów
├── Kredyty: scoring zdolności kredytowej
└── Infrastruktura krytyczna

LIMITED RISK (obowiązki transparency — TERAZ)
├── Chatboty: muszą poinformować że to AI      ← Większość projektów!
├── Deep-fake: obowiązek oznaczenia
└── AI-generated content: oznaczenie

MINIMAL RISK (bez specjalnych wymogów)
└── Filtry antyspam, rekomendacje, gry
```

> 🎙️ NOTATKA: Alina prowadzi ten slajd. Podkreśl "08.2026 = 5 miesięcy". Zapytaj uczestników: "kto wdraża coś do HR? Sprawdź czy to high-risk."

---

## Slajd 14: AI ACT — KTÓRE AUTOMATYZACJE SĄ HIGH-RISK?

**Sprawdź swoje projekty:**

| Typ automatyzacji | Klasyfikacja AI Act | Co to oznacza |
|---|---|---|
| Chatbot obsługi klienta | Limited risk | Disclosure w pierwszej wiadomości |
| Email classifier (support) | Minimal risk | Nic specjalnego |
| CV screening / ranking kandydatów | **HIGH RISK** | Pełna dokumentacja, rejestracja EU AI DB |
| Scoring kredytowy / zdolność płatnicza | **HIGH RISK** | Wymagany human-in-the-loop |
| Predykcja churnu klientów | Zależy od kontekstu | Konsultacja z prawnikiem |
| Invoice parser (OCR + AI) | Minimal risk | Nic specjalnego |
| AI-generated marketing content | Limited risk | Oznaczenie "wygenerowane przez AI" |
| Monitoring pracowników przez AI | **HIGH RISK** | Pełna dokumentacja |

**Reguła kciuka:** Jeśli AI podejmuje decyzje które istotnie wpływają na ludzi (praca, kredyt, zdrowie) → prawdopodobnie HIGH RISK.

> 🎙️ NOTATKA: Alina + Kacper wspólnie. Kacper dopowiada o konkretnych workflow n8n które mogą wpaść w high-risk. Podkreślcie: "Nie wiemy wszystkiego — w razie wątpliwości: prawnik."

---

## Slajd 15: AI ACT — TRANSPARENCY REQUIREMENT (Art. 50)

**Chatboty i AI agenci: obowiązek TERAZ (od 08.2025)**

```javascript
// System prompt z wymaganym disclosure:
const SYSTEM_PROMPT = `
Jesteś asystentem AI firmy [NAZWA].
WAŻNE: Informuj użytkownika na początku każdej rozmowy:
"Witaj! Jestem asystentem AI, nie człowiekiem.
Mogę pomóc w [zakres]. W każdej chwili możesz
poprosić o kontakt z konsultantem."

Nigdy nie zaprzeczaj że jesteś AI, nawet jeśli użytkownik pyta.
`;
```

**Co jest wymagane:**
- Wyraźna informacja na POCZĄTKU interakcji (nie w regulaminie)
- Możliwość przejścia do człowieka na żądanie
- Nie udawaj człowieka nawet pod presją

**Kara za brak:** do 15 mln EUR lub 3% globalnego obrotu

> 🎙️ NOTATKA: Alina mówi o karach. Kacper pokazuje implementację w n8n chatbocie. "15 milionów euro" — to nie abstrakcja, to kwota.

---

## Slajd 16: BEZPIECZEŃSTWO SIECI — ARCHITEKTURA

```
INTERNET
    ↓
[Cloudflare / CDN] — DDoS protection, WAF
    ↓
[Nginx / Caddy] — Reverse proxy, TLS termination, rate limiting
    ↓
[Docker network: internal] — izolacja
    ↓
[n8n container: port 5678] — NIGDY bezpośrednio na zewnątrz
    ↓
[PostgreSQL container] — tylko wewnętrzna sieć
```

**Reguła:** n8n nigdy nie powinien być dostępny na surowym porcie 5678 w internecie.

> 🎙️ NOTATKA: Kacper rysuje diagram lub pokazuje gotowy. Podkreśl: "jeśli teraz otwierasz przeglądarkę na IP:5678 — to problem."

---

## Slajd 17: NGINX KONFIGURACJA DLA N8N

```nginx
# /etc/nginx/sites-available/n8n
server {
    listen 443 ssl http2;
    server_name n8n.twojafirma.pl;

    ssl_certificate     /etc/letsencrypt/live/.../fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/.../privkey.pem;
    ssl_protocols TLSv1.3;  # Tylko TLS 1.3!

    # Rate limiting — max 10 req/s per IP
    limit_req zone=n8n_limit burst=20 nodelay;

    # Security headers
    add_header X-Frame-Options "DENY";
    add_header X-Content-Type-Options "nosniff";
    add_header Strict-Transport-Security "max-age=31536000";

    location / {
        proxy_pass http://localhost:5678;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

# Rate limiting zone (w sekcji http {})
limit_req_zone $binary_remote_addr zone=n8n_limit:10m rate=10r/s;
```

> 🎙️ NOTATKA: Kacper pokazuje ten plik i tłumaczy każdą linię. Zatrzymaj się przy `ssl_protocols TLSv1.3` — wyjaśnij czemu tylko 1.3. Przy headers — wyjaśnij X-Frame-Options (clickjacking).

---

## Slajd 18: WEBHOOK SECURITY — PROBLEM

**Publiczny webhook bez zabezpieczenia:**

```
Twój webhook URL (publiczny):
https://n8n.firma.pl/webhook/abc123-xyz

Każdy kto zna URL może wywołać:
curl -X POST https://n8n.firma.pl/webhook/abc123-xyz \
  -H "Content-Type: application/json" \
  -d '{"action": "delete_all_leads"}'

↓
Workflow się uruchomi!
↓
Możliwe skutki:
- Spam do CRM (fałszywe leady)
- Uruchomienie kosztownych AI calls (kradną Twoje API credits)
- Wstrzyknięcie złośliwych danych do systemu
```

> 🎙️ NOTATKA: Kacper demonstruje atak na demo środowisku. Uczniowie muszą zobaczyć że to działa. Dopiero potem pokaż zabezpieczenie.

---

## Slajd 19: WEBHOOK SECURITY — HMAC SIGNATURE VERIFICATION

**Jak działa HMAC (diagram):**

```
NADAWCA (np. GitHub, Stripe, Twój system):
1. Weź body requestu (raw bytes)
2. Oblicz: HMAC-SHA256(secret_key, body) = "abc123xyz"
3. Dodaj nagłówek: X-Signature: sha256=abc123xyz
4. Wyślij request

ODBIORCA (n8n webhook):
1. Odbierz request
2. Weź ten sam secret_key (znasz go tylko Ty i nadawca)
3. Oblicz: HMAC-SHA256(secret_key, received_body) = "abc123xyz"
4. Porównaj: oczekiwany == otrzymany?
   ✅ TAK → request jest autentyczny → przetworz
   ❌ NIE → ktoś sfałszował request → odrzuć z 401
```

**Klucz:** Atakujący nie zna `secret_key` → nie może sfałszować podpisu.

> 🎙️ NOTATKA: Narysuj ten diagram powoli. To jeden z ważniejszych konceptów w module. Potem przejdź do kodu.

---

## Slajd 20: HMAC VERIFICATION — KOD W N8N CODE NODE

```javascript
// Webhook HMAC Verification — Dokodu Standard
const crypto = require('crypto');

// Pobierz dane z requestu
const payload = $input.first().json;
const headers = $input.first().json.headers || {};
const rawBody = JSON.stringify(payload.body || payload);

// Pobierz podpis z nagłówka (np. GitHub style: "sha256=abc123")
const receivedSignature = headers['x-hub-signature-256'] ||
                          headers['x-signature'] || '';

// Pobierz sekret z env variable (NIE hardcode!)
const secret = process.env.WEBHOOK_SECRET;
if (!secret) throw new Error('WEBHOOK_SECRET not configured');

// Oblicz oczekiwany podpis
const expectedSignature = 'sha256=' + crypto
  .createHmac('sha256', secret)
  .update(rawBody)
  .digest('hex');

// Porównaj (timing-safe comparison!)
const isValid = crypto.timingSafeEqual(
  Buffer.from(receivedSignature),
  Buffer.from(expectedSignature)
);

if (!isValid) {
  // Log próbę i odrzuć
  console.log(JSON.stringify({
    level: 'WARN',
    event: 'webhook.signature.invalid',
    message: 'Odrzucony request — nieprawidłowy podpis HMAC',
    timestamp: new Date().toISOString()
  }));
  throw new Error('Invalid signature — request rejected');
}

// Podpis prawidłowy — kontynuuj
return [{ json: { verified: true, ...payload } }];
```

> 🎙️ NOTATKA: Kacper kopiuje ten kod do n8n live. Wyjaśnij `timingSafeEqual` — dlaczego zwykłe `===` jest podatne na timing attacks.

---

## Slajd 21: IP WHITELISTING — DODATKOWA WARSTWA

**Kiedy stosować IP whitelisting:**
- Webhook od zewnętrznego systemu z fałym IP (Stripe: znane zakresy IP)
- Wewnętrzne webhook między serwerami
- Admin webhooks (nigdy nie powinny być publiczne)

```nginx
# Nginx: IP whitelist dla /webhook/admin/
location /webhook/admin/ {
    allow 192.168.1.0/24;     # Twoja sieć wewnętrzna
    allow 185.143.172.0/24;   # Znane IP partnera
    deny all;                  # Reszta blokowana

    proxy_pass http://localhost:5678;
}
```

```javascript
// Alternatywnie — sprawdzenie IP w n8n Code Node
const allowedIPs = ['185.143.172.1', '10.0.0.0/8'];
const clientIP = $input.first().json.headers['x-real-ip'];

if (!allowedIPs.includes(clientIP)) {
  throw new Error(`IP ${clientIP} not whitelisted`);
}
```

> 🎙️ NOTATKA: Kacper pokazuje konfigurację. Powiedz że IP whitelisting to bonus, nie substytut HMAC — atakujący mogą spoofować IP.

---

## Slajd 22: CO LOGOWAĆ — DYLEMAT RODO VS BEZPIECZEŃSTWO

**Napięcie:**

```
BEZPIECZEŃSTWO mówi: "Loguj wszystko — potrzebujesz historii do forensics"
RODO mówi: "Minimalizuj dane — nie zbieraj więcej niż potrzebujesz"

ROZWIĄZANIE: Loguj zdarzenia, nie dane osobowe
```

| Co logować | Co NIE logować |
|---|---|
| Timestamp, event type, workflow ID | Email użytkownika |
| Status (sukces/błąd) | Treść wiadomości |
| Pseudonim ID (hash) | Hasła, tokeny, API keys |
| Czas trwania operacji | Dane biometryczne |
| IP (uwaga: to PII!) | Pełne body requestu |

**IP w logach:** Jeśli logujesz IP — masz do czynienia z danymi osobowymi. Zastosuj czas retencji.

> 🎙️ NOTATKA: Kacper i Alina razem. To ważny punkt — uczący często logują za dużo. "Dobry log opisuje zdarzenie, nie człowieka."

---

## Slajd 23: DOKODU LOGGING STANDARD — FORMAT

```javascript
// Każdy log w tym formacie — kopiuj bez modyfikacji
{
  "level": "INFO",                          // INFO | WARN | ERROR
  "timestamp": "2026-03-27T10:30:00.123Z", // ISO 8601, UTC
  "workflow_name": "CLIENT_Usecase_v1",
  "execution_id": $execution.id,
  "event": "lead.captured",                // encja.akcja.status
  "message": "Nowy lead z formularza web", // czytelny opis
  "data": {
    "source": "landing_page_webinar",
    "lead_id": "lead_abc123",              // pseudonim, nie email!
    "score": 85
  },
  "duration_ms": 245
}
```

**Centralizacja logów:**
- Self-hosted: Grafana Loki (bezpłatny, kompatybilny z Prometheus)
- SaaS: Papertrail, Logtail (prostsze, płatne)
- Minimum: Google Sheets (dla małych projektów)

> 🎙️ NOTATKA: Kacper pokazuje ten format. Wspomnij że pełny standard jest w materiałach do pobrania (Logging_Standard.md).

---

## Slajd 24: SERVER-SIDE TRACKING — DLACZEGO I JAK

**Problem z client-side tracking (GA4, Facebook Pixel):**
- Blokowany przez ad-blockery (30-60% użytkowników w B2B!)
- Wymaga zgody cookies (RODO — baner cookies)
- Dane trafiają bezpośrednio do Google / Meta

**Server-side tracking:**
```
Użytkownik klika "Kup" na stronie
    ↓
Twój serwer: rejestruje zdarzenie (purchase)
    ↓
n8n webhook: odbiera event
    ↓
Przetwarzasz, anonimi zujesz IP
    ↓
Wysyłasz do GA4 Measurement Protocol (server → Google)
    ↓
Wynik: 100% event capture, RODO-compliant
```

**Korzyści:** Pełne dane, mniejsza zależność od cookies, lepsza jakość ML w GA4.

> 🎙️ NOTATKA: Kacper. To temat techniczny — pokaż diagram i powiedz że jest blueprint w materiałach kursu. Nie zanurzaj się za głęboko — osobny moduł mógłby być z tego.

---

## Slajd 25: MICROSOFT PRESIDIO — TARCZA PII

**Problem:** Wysyłasz do OpenAI dane klientów → dane trafiają poza EU (bez DPA = naruszenie RODO)

**Rozwiązanie — Presidio w architekturze:**

```
[n8n: surowe dane klienta]
    ↓
[Presidio Analyzer — identyfikuje PII]
    ├── Email: jan@firma.pl → <EMAIL>
    ├── PESEL: 90010112345 → <PESEL>
    ├── Imię: "Jan Kowalski" → <PERSON>
    └── NIP: 1234567890 → <NIP>
    ↓
[Presidio Anonymizer — zamienia na tokeny]
    ↓
[OpenAI API: dane bez PII]
    ↓
[n8n: wynik + de-anonymizacja (jeśli potrzebna)]
```

**Instalacja:** Docker container, REST API, integracja przez HTTP Request w n8n

> 🎙️ NOTATKA: Kacper. Presidio to element Zero-Trust AI Architecture Dokodu. Pokaż diagram. Powiedz że gotowy blueprint jest w materiałach.

---

## Slajd 26: PODSUMOWANIE — TWOJA TARCZA BEZPIECZEŃSTWA

**6 warstw = kompletna ochrona:**

```
WARSTWA 1: Credential Vault
└── N8N_ENCRYPTION_KEY + Least Privilege

WARSTWA 2: RODO Compliance
└── Data Flow Audit + Pseudonimizacja + RTBF Workflow

WARSTWA 3: AI Act Compliance
└── Klasyfikacja ryzyka + Transparency disclosure

WARSTWA 4: Bezpieczeństwo sieci
└── Nginx + HMAC webhooks + IP whitelist

WARSTWA 5: Logowanie bez PII
└── Dokodu Logging Standard + Loki/ELK

WARSTWA 6: PII Redaction przed AI
└── Microsoft Presidio w architekturze
```

> 🎙️ NOTATKA: Kacper + Alina razem. "Każda warstwa samodzielnie nie wystarczy. Wszystkie razem = bezpieczna automatyzacja którą możesz pokazać klientowi enterprise."

---

## Slajd 27: NASTĘPNE KROKI — CO ROBISZ PO TYM MODULE

**Dziś (30 minut):**
- [ ] Sprawdź swój `N8N_ENCRYPTION_KEY` — czy jest silny?
- [ ] Narysuj Data Flow Diagram jednego swojego workflow
- [ ] Sprawdź czy n8n jest za reverse proxy (nie na porcie 5678)

**Ten tydzień:**
- [ ] Przeprowadź RODO Audit swojego największego workflow (Ćwiczenie 1)
- [ ] Dodaj HMAC do przynajmniej jednego webhooka produkcyjnego (Ćwiczenie 2)

**Ten miesiąc:**
- [ ] Zidentyfikuj czy masz jakiekolwiek HIGH RISK automatyzacje (AI Act)
- [ ] Wdróż Presidio jeśli wysyłasz dane klientów do zewnętrznych LLM

**Termin nie do zignorowania:** AI Act pełne stosowanie — 2 sierpnia 2026

> 🎙️ NOTATKA: Alina kończy moduł. "Compliance to inwestycja — klienci enterprise o to pytają. Agencja która to ma = agencja która wygrywa przetargi."
