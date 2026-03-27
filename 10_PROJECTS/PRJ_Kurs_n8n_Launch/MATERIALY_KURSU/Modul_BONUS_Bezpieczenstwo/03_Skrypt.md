---
type: course-material
modul: BONUS_Bezpieczenstwo
format: skrypt-nagrania
prowadzacy: [Kacper Sieradziński, Alina Sieradzińska]
segmentów: 7
szacowany-czas: 90 minut
created: 2026-03-27
tags: [kurs, n8n, bezpieczenstwo, RODO, AI-Act, skrypt, nagranie]
---

# Moduł BONUS: Bezpieczeństwo i Compliance — Skrypt nagrania

> **Legenda:**
> `[KACPER: tekst]` — mówi Kacper Sieradziński (technikalia, CEO)
> `[ALINA: tekst]` — mówi Alina Sieradzińska (prawo, AI Act, GDPR, COO)
> `[DEMO: opis]` — przełącz na ekran n8n / terminal
> `[SLAJD N]` — zmiana slajdu w prezentacji
> `[RAZEM]` — oboje na ekranie, dialog
> Czas całkowity: **~90 minut**
> Ton: konkretny, bez ściemniania. Kacper: techniczny, z przykładami z terenu. Alina: pewna, prawniczo precyzyjna, ale zrozumiała dla programistów.

---

## SEGMENT 1 — HOOK I INTRO (0:00–8:00)

[SLAJD 1]

[KACPER:]
Jeden niezabezpieczony webhook i masz wyciek danych 10 000 klientów.

To nie jest tytuł clickbaitowy. To jest dokładnie to, co stało się znajomemu który do mnie zadzwonił dwa lata temu. Zbudował automatyzację dla e-commerce: formularz na stronie, webhook do n8n, dane wprost do CRM i do systemu mailingowego. Działało świetnie. Przez cztery miesiące.

A potem ktoś znalazł URL webhooka — wyindeksowany przez Google'a z cache strony stagingowej — i zaczął go masowo wywoływać. Dziesiątki tysięcy requestów. Fałszywe dane klientów wpadają do CRM. System wysyła do każdego spersonalizowany email powitalny. Konto w platformie mailingowej zablokowane za spam. A w logach CRM — 10 000 rekordów śmieci których nie da się szybko odróżnić od prawdziwych klientów.

Dwa tygodnie czyszczenia bazy. Kara finansowa za opóźnione przetwarzanie zgłoszeń klientów. I umowa z klientem wypowiedziana z powodu „zaniedbania standardów bezpieczeństwa".

Jeden endpoint. Bez HMAC. Bez rate limitingu. Bez niczego.

Ten moduł jest po to, żebyś nigdy nie odbierał takiego telefonu.

[SLAJD 2]

[ALINA:]
I ja dodam wymiar prawny, zanim Kacper przejdzie do kodu.

Pracuję z firmami wdrażającymi automatyzacje od kilku lat i widzę zawsze ten sam schemat: najpierw budujemy, potem pytamy o compliance. Albo — co gorsza — pytamy dopiero kiedy dostajemy pismo z UODO lub od prawnika po drugiej stronie umowy.

Compliance nie jest opresją. To jest mapa. Mapa która mówi: zrób to i to — i możesz spać spokojnie. Dzisiaj razem z Kacprem dajemy ci tę mapę — technikalia i prawo w jednym miejscu.

W ciągu 90 minut omówimy sześć obszarów, a na koniec dostaniesz checklistę do pobrania. Zacznijmy.

[SLAJD 3 — Roadmapa modułu]

[KACPER:]
Plan na dzisiaj. Segment pierwszy — Credential Vault: gdzie trzymasz sekrety i jak je zabezpieczasz w n8n i opcjonalnie HashiCorp Vault. Segment drugi — Alina opowie o RODO w automatyzacjach: podstawy prawne, jakie dane możesz przetwarzać i kiedy potrzebujesz zgody. Segment trzeci — Webhook Security: live demo ataku na niezabezpieczony endpoint i implementacja HMAC signature verification. Segment czwarty — AI Act 2024: które automatyzacje są high-risk i co to oznacza praktycznie. Segment piąty — Logowanie i audit trail: co logować, a czego NIE logować, bo RODO. Segment szósty — Right to be forgotten: jak zautomatyzować prawo do usunięcia danych. I na końcu — zanonimizowane case studies incydentów.

Zaczynamy.

---

## SEGMENT 2 — CREDENTIAL VAULT (8:00–28:00)

[SLAJD 4 — Credential Vault]

[KACPER:]
Pierwsze pytanie które zadaję przy każdym audycie klienta: gdzie trzymasz klucze API?

Najczęstsze odpowiedzi które słyszę. „W workflow, hardcoded w polu." Najgorsze co można zrobić — klucz widoczny w historii każdego execution, eksportuje się razem z workflowem, pojawi się w backupie. „W .env na serwerze." Dobra odpowiedź. „W Credentials w n8n." Bardzo dobra odpowiedź — ale tylko jeśli ustawiłeś N8N_ENCRYPTION_KEY.

Dlatego zacznijmy od fundamentu.

[SLAJD 5 — N8N_ENCRYPTION_KEY]

[DEMO: pokaż docker-compose.yml w edytorze, sekcja environment]

N8N_ENCRYPTION_KEY to klucz którym n8n szyfruje wszystkie dane uwierzytelniające w bazie danych algorytmem AES-256. Jeśli go nie ustawisz, n8n wygeneruje losowy i zapisze w systemie — i masz dwa problemy. Przy migracji na nowy serwer wszystkie credentials stają się nieczytelne. Jeśli ktoś ukradnie bazę danych bez silnego, unikalnego klucza, ma szansę na bruteforce.

Generowanie klucza — jedno polecenie w terminalu:

```bash
openssl rand -hex 32
```

Wynik — 64-znakowy ciąg losowych znaków — wklejasz do pliku `.env`:

```
N8N_ENCRYPTION_KEY=twoj_wygenerowany_klucz_tutaj
```

Ten plik dodajesz do `.gitignore`. Robisz backup klucza w menedżerze haseł — 1Password, Bitwarden, Vault, cokolwiek. To jest dosłownie dziesięć minut roboty, która chroni wszystkie przyszłe credentials.

[SLAJD 6 — n8n Credentials vs HashiCorp Vault]

Teraz pytanie które często pada: kiedy n8n Credentials wystarczy, a kiedy potrzebujesz HashiCorp Vault?

n8n Credentials z silnym kluczem szyfrowania jest wystarczające dla zdecydowanej większości projektów agencyjnych i MŚP. Masz jedno środowisko produkcyjne, kilkanaście integracji, nie przechodzisz audytów ISO 27001. n8n — tak.

HashiCorp Vault rozważasz gdy: masz klienta enterprise który pyta o rotację kluczy i audyt dostępu. Vault ma dynamiczne sekrety — klucz API generowany na żądanie, ważny przez jedną godzinę, automatycznie wygasa. Atakujący który go przechwyci ma okno jednej godziny. To fundamentalna różnica w modelu bezpieczeństwa.

[DEMO: pokaż integrację n8n z Vault — HTTP Request do Vault API, endpoint secrets/data/]

```javascript
// Code Node — pobieranie sekretu z Vault
const vaultToken = $env.VAULT_TOKEN;
const secretPath = 'secret/data/openai-key';

const response = await $http.get(
  `${$env.VAULT_ADDR}/v1/${secretPath}`,
  { headers: { 'X-Vault-Token': vaultToken } }
);

return [{ json: { apiKey: response.data.data.key } }];
```

Ale Vault wymaga osobnego serwera, konfiguracji, i kogoś kto go utrzymuje. Dla małych projektów — over-engineering. Zacznij od n8n Credentials i migruj jeśli to kiedykolwiek stanie się wymaganiem.

[SLAJD 7 — Least Privilege]

Zasada Least Privilege — najmniejsze uprawnienia. Jeden klucz API do wszystkich workflow to błąd. Nie dlatego że ktoś go ukradnie. Dlatego że jeden workflow z bugiem który wywołuje API w pętli daje ci rachunek za kilka tysięcy złotych za jedną noc.

OpenAI Projects — możesz stworzyć osobny projekt per klient, osobny klucz API per projekt, osobny limit budżetowy. Zero dodatkowego kosztu. Możesz dezaktywować jeden klucz bez wpływu na resztę. Możesz śledzić koszty per klient.

Dla Google Cloud: Service Account per projekt, IAM role z minimalnym zakresem uprawnień. Dla Stripe: Restricted Keys — tylko operacje które dany workflow rzeczywiście potrzebuje.

[SLAJD 8 — checklist Credential Vault]

Checklist zanim przejdziemy dalej. N8N_ENCRYPTION_KEY ustawiony i w backupie — checkmark. Wszystkie klucze w Credentials, nie hardcoded — checkmark. Oddzielne klucze per projekt lub klient — checkmark. .env w .gitignore — checkmark.

---

## SEGMENT 3 — RODO W AUTOMATYZACJACH (28:00–50:00)

[SLAJD 9 — RODO intro]

[ALINA:]
Zanim powiem co robić z danymi osobowymi, muszę powiedzieć co to jest — bo naprawdę wiele osób budujących automatyzacje nie wie gdzie kończy się anonimowy log, a zaczyna przetwarzanie danych osobowych.

Dane osobowe to wszelkie informacje dotyczące zidentyfikowanej lub możliwej do zidentyfikowania osoby fizycznej. Kluczowe słowo: „możliwej do zidentyfikowania". Nie musisz znać imienia i nazwiska żeby mieć dane osobowe.

Adres email — dane osobowe. Numer IP — dane osobowe, bo w połączeniu z czasem i dostawcą internetowym można zidentyfikować konkretną osobę. Imię plus firma — dane osobowe. Numer telefonu — dane osobowe.

Ale najgroźniejsza sytuacja to kombinacja. Sam timestamp — nie jest daną osobową. Sam User-Agent przeglądarki — nie jest daną osobową. Ale timestamp plus IP plus User-Agent plus akcja na stronie — możesz zidentyfikować konkretną osobę. I te połączone dane to już dane osobowe w rozumieniu RODO.

To ma bezpośrednie przełożenie na każdy workflow który budujecie.

[SLAJD 10 — Data Flow Audit]

[KACPER:]
Dlatego zanim zaczniesz budować jakąkolwiek automatyzację która dotyka danych użytkowników, rób Data Flow Audit. Ja robię to na kartce papieru — pięć minut przed wejściem w n8n.

Rysujesz prostokąty dla każdego systemu przez który przechodzą dane: formularz, n8n, CRM, AI, arkusz, newsletter. I rysujesz strzałki dla każdego rodzaju danych. Email idzie tu i tu. IP idzie tu. Imię idzie tu.

Potem przy każdej strzałce trzy pytania: czy ten system musi mieć ten konkretny typ danych? Czy istnieje umowa powierzenia przetwarzania z tym dostawcą? Jak długo te dane tam siedzą zanim zostaną usunięte?

[DEMO: pokaż przykładowy diagram na slajdzie — Lead Capture z mapą przepływu danych]

Ta mapa zajmuje 20 minut. Może uchronić cię od miesięcy problemów z klientem i od kontroli UODO.

[SLAJD 11 — Art. 6 RODO — Podstawy prawne]

[ALINA:]
Podstawy prawne przetwarzania. Art. 6 RODO. Każdy kto buduje automatyzacje przetwarzające dane osobowe musi to znać.

Masz cztery główne podstawy.

Zgoda — użytkownik aktywnie wyraził zgodę na konkretny cel przetwarzania. To jest najsłabsza podstawa z perspektywy administratora, bo można ją wycofać w każdej chwili. Jeśli ktoś wycofa zgodę — musisz natychmiast zaprzestać przetwarzania we wszystkich systemach.

Wykonanie umowy — przetwarzasz dane bo musisz, żeby zrealizować usługę dla tej osoby. Klient składa zamówienie — przetwarzasz jego adres bo musisz dostarczyć paczkę. Solidna podstawa, osobna zgoda nie jest wymagana.

Uzasadniony interes — tu trzeba uważać. Możesz przetwarzać dane jeśli masz uzasadniony interes, ale ten interes nie może być nadrzędny nad prawami i wolnościami osoby. Trzeba przeprowadzić test balansu i udokumentować go. Przy kontaktach B2B między firmami — często dobra podstawa.

Obowiązek prawny — przechowujesz faktury pięć lat bo prawo podatkowe tego wymaga. Nie potrzebujesz zgody.

Dlaczego to ważne dla n8n? Bo musi ci się zgadzać podstawa prawna dla każdego celu przetwarzania osobno. Email marketingowy wymaga zgody. Obsługa zamówienia — nie. Analiza zachowań przez AI do retargetingu — wymaga zgody lub wykazania uzasadnionego interesu z testem balansu.

[SLAJD 12 — Pseudonimizacja vs Anonimizacja]

[KACPER:]
Techniki ochrony danych w pipeline n8n. Pseudonimizacja i anonimizacja — różnica jest kluczowa i ma konsekwencje prawne.

Pseudonimizacja to zamiana danych osobowych na pseudonim — coś z czego można odtworzyć oryginalne dane mając klucz. Najprostszy przykład: SHA-256 hash adresu email.

```javascript
// Code Node — pseudonimizacja emaila
const crypto = require('crypto');

const email = $input.first().json.email;
const pseudonym = crypto.createHash('sha256')
  .update(email + $env.PSEUDONYMIZATION_SALT)
  .digest('hex');

return [{
  json: {
    ...$input.first().json,
    email: undefined,        // usuń oryginał
    email_hash: pseudonym    // zachowaj pseudonim
  }
}];
```

Hash wygląda jak losowy ciąg. Ale jeśli masz oryginalny email i salt — możesz obliczyć ten sam hash i odnaleźć rekord. Odwracalne z kluczem.

RODO nadal stosuje się do pseudonimizowanych danych. Możesz te dane przetwarzać, ale podlegają przepisom.

Anonimizacja to permanentne usunięcie możliwości identyfikacji. Zamiana email na `[EMAIL USUNIĘTY]`. Nieodwracalne. Do zanonimizowanych danych RODO nie stosuje się.

Kiedy pseudonimizacja, a kiedy anonimizacja? Pseudonimizuj gdy musisz śledzić zachowania użytkownika w czasie — na przykład ścieżkę zakupową — bez przechowywania jego emaila w logach. Anonimizuj gdy dane służą tylko do statystyk i agregatów — nie musisz wiedzieć kto to był.

[SLAJD 13 — Zgody w automatyzacjach]

[ALINA:]
Zgody. Kilka zasad które musisz wdrożyć jeśli budujesz formularz zbierający dane i uruchamiający automatyzacje.

Po pierwsze, granularność. Jedna duża checkbox „akceptuję regulamin i politykę prywatności i zgadzam się na marketing" — nieważna. Zgoda na każdy cel musi być osobna, dobrowolna i jednoznaczna. Jedna checkbox do przeczytania regulaminu, osobna do marketingu emailowego, osobna do profilowania. Trzy checkboxy, nie jedna.

Po drugie, dokumentacja zgody. W momencie gdy użytkownik wyraża zgodę — n8n powinien zapisać timestamp, wersję treści zgody, źródło, i ID użytkownika. Bez tego nie możesz udowodnić w kontroli że zgoda była. Blueprint tego jest w materiałach kursu.

Po trzecie, mechanizm wycofania. Każdy email musi mieć link do wypisania. Każdy dashboard klienta musi mieć możliwość edycji zgód. I — kluczowe — wycofanie zgody musi być łatwie jak jej wyrażenie. Jeśli zapisałeś się klikając jeden przycisk, wypisanie też musi być jednym przyciskiem.

---

## SEGMENT 4 — WEBHOOK SECURITY (50:00–64:00)

[SLAJD 14 — Webhook Security intro]

[KACPER:]
Wracamy do webhooka z początku. Jak go zabezpieczyć żeby nikt go nie nadużył?

Trzy warstwy: Reverse proxy, HMAC signature verification, opcjonalnie IP whitelisting.

[SLAJD 15 — Warstwa 1: Reverse proxy]

Warstwa pierwsza — reverse proxy. n8n domyślnie nasłuchuje na porcie 5678. Jeśli otworzysz ten port bezpośrednio na internet, każdy na świecie może próbować dostać się do panelu n8n. To nie jest teoria — boty skanujące otwarte porty trafiają na taki serwer w ciągu godzin.

Nginx lub Caddy stoi przed n8n. TLS termination — HTTPS obsługuje proxy, n8n ma czysty HTTP wewnętrznie. Rate limiting — maksymalnie dziesięć requestów na sekundę per IP. Security headers: X-Frame-Options, HSTS, Content-Security-Policy.

[DEMO: pokaż gotowy nginx.conf dla n8n]

```nginx
server {
    listen 443 ssl;
    server_name n8n.twojadomena.pl;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=webhook:10m rate=10r/s;
    limit_req zone=webhook burst=20 nodelay;

    location /webhook/ {
        proxy_pass http://localhost:5678;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;

        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
    }

    # Panel n8n — tylko dla zaufanych IP
    location / {
        allow 85.203.45.0/24;  # Twoje biuro
        deny all;
        proxy_pass http://localhost:5678;
    }
}
```

To jest kompletny, gotowy do użycia config. Skopiuj, zmień server_name i dozwolone IP. Dziesięć minut roboty.

[SLAJD 16 — HMAC Signature Verification]

Warstwa druga — HMAC. I to jest najważniejsza z trzech warstw.

HMAC to Hash-based Message Authentication Code. Mechanizm który pozwala weryfikować że request pochodzi od kogo mówi że pochodzi, i że nie był zmodyfikowany w drodze.

[SLAJD 17 — Diagram jak działa HMAC]

Jak to działa. Ty i nadawca requestu macie wspólny sekret — ciąg znaków który tylko Wy znacie. Nadawca przed wysłaniem oblicza podpis: HMAC-SHA256(sekret, body requestu). Dodaje go do nagłówka requestu, na przykład `X-Signature`. Ty po otrzymaniu requestu obliczasz ten sam hash z tym samym sekretem. Jeśli wyniki się zgadzają — request jest autentyczny i nienaruszony.

Atakujący który przechwytuje requesty może zobaczyć URL, może zobaczyć body, może zobaczyć nagłówki. Ale nie zna sekretu — więc nie może obliczyć prawidłowego podpisu. Nie może sfałszować requestu.

[DEMO: Live demo — attack on unprotected webhook]

Najpierw pokażę ci jak wygląda atak na niezabezpieczony webhook. Mam prosty workflow — Webhook Trigger, zapisuje dane do zmiennej. Endpoint jest publiczny.

[DEMO: wyślij w pętli 50 requestów curl z losowymi danymi]

```bash
for i in {1..50}; do
  curl -s -X POST https://n8n.demo/webhook/lead \
    -H "Content-Type: application/json" \
    -d "{\"email\": \"spam$i@fake.com\", \"name\": \"Bot $i\"}" &
done
```

Pięćdziesiąt fałszywych leadów w sekundę. W realnym scenariuszu to dziesiątki tysięcy requestów dziennie.

Teraz z HMAC — ten sam endpoint, ale z weryfikacją podpisu.

[DEMO: Code Node z implementacją HMAC]

```javascript
// Code Node — HMAC Signature Verification
const crypto = require('crypto');

// Pobierz podpis z nagłówka
const signature = $input.first().headers['x-signature'];
const body = JSON.stringify($input.first().body);
const secret = $env.WEBHOOK_SECRET;

if (!signature) {
  throw new Error('Brak podpisu X-Signature');
}

// Oblicz oczekiwany podpis
const expected = 'sha256=' + crypto
  .createHmac('sha256', secret)
  .update(body)
  .digest('hex');

// WAŻNE: używaj timingSafeEqual, nie ===
// Zwykłe porównanie jest podatne na timing attack
const sigBuffer = Buffer.from(signature);
const expBuffer = Buffer.from(expected);

if (sigBuffer.length !== expBuffer.length ||
    !crypto.timingSafeEqual(sigBuffer, expBuffer)) {
  throw new Error('Nieprawidłowy podpis — request odrzucony');
}

// Podpis prawidłowy — kontynuuj przetwarzanie
return $input.all();
```

[SLAJD 18 — Timing Attack wyjaśnienie]

Ważna techniczna uwaga o `timingSafeEqual`. Dlaczego nie zwykłe `===`?

Zwykłe porównanie stringów zatrzymuje się przy pierwszym niezgodnym znaku. Jeśli pierwsza litera się nie zgadza — odpowiedź wraca natychmiast. Jeśli pierwsze dwadzieścia znaków się zgadza, a dwudziesty pierwszy nie — odpowiedź wraca trochę później.

Atakujący może mierzyć czas odpowiedzi w mikrosekundach i dedukcyjnie odgadywać kolejne znaki podpisu. To jest timing attack. `timingSafeEqual` zawsze porównuje dokładnie tyle samo czasu — niezależnie od tego w którym miejscu jest niezgodność.

To nie jest akademicka ciekawostka. To jest realna klasa ataków z CVE-ami i udokumentowanymi przypadkami w produkcji.

[DEMO: pokaz że request bez podpisu dostaje 401]

Z HMAC — te same pięćdziesiąt requestów bez podpisu dostaje 401 Unauthorized. Żaden nie przechodzi do workflow.

[SLAJD 19 — IP Whitelisting jako bonus]

Warstwa trzecia — IP whitelisting. Jako uzupełnienie, nie substytut HMAC.

Stripe publikuje listę swoich adresów IP. GitHub webhooks ma swoją listę. Jeśli znasz IP nadawcy — możesz dodać regułę w Nginx:

```nginx
location /webhook/stripe {
    allow 185.143.172.0/24;
    deny all;
    proxy_pass http://localhost:5678;
}
```

Pamiętaj: IP można spoofować w pewnych scenariuszach, sieci VPN zmieniają IP. HMAC + IP = bardzo silna ochrona, bo atakujący musiałby jednocześnie mieć prawidłowe IP i znać sekret HMAC.

---

## SEGMENT 5 — AI ACT 2024 (64:00–76:00)

[SLAJD 20 — AI Act intro]

[ALINA:]
AI Act. Rozporządzenie Parlamentu Europejskiego i Rady 2024/1689. Największa regulacja AI na świecie. Wchodzi w pełni w życie 2 sierpnia 2026 roku. To jest pięć miesięcy od dzisiaj.

Zacznę od dobrej wiadomości: większość automatyzacji które budujecie to albo ograniczone ryzyko, albo minimalne ryzyko. Nie jesteście w strefie wysokiego ryzyka, chyba że świadomie budujecie systemy do oceniania ludzi w kontekstach wrażliwych.

Zła wiadomość: jeśli budujesz automatyzacje do HR, rekrutacji, scoringu klientów, lub monitorowania pracowników — możesz być w high-risk bez wiedzy o tym.

[SLAJD 21 — Cztery kategorie ryzyka]

Cztery kategorie ryzyka. Omówię je od najgorszej.

Niedopuszczalne — systemy zakazane od 2 lutego 2025. Social scoring, biometryczna identyfikacja w czasie rzeczywistym w przestrzeni publicznej, systemy manipulacji podprogowej, systemy oceniające cechy osobowości na podstawie wyglądu. Dokodu tych systemów nie wdraża i nie pomaga wdrażać. Kara do 35 milionów euro lub 7% globalnych przychodów.

Wysokie ryzyko — pełne wymagania od 2 sierpnia 2026. W naszym kontekście automatyzacji to przede wszystkim: automatyczny screening CV i ranking kandydatów do pracy, scoring zdolności kredytowej, systemy edukacyjne do oceniania uczniów i studentów, monitorowanie pracowników w czasie rzeczywistym z oceną ich zachowań. Jeśli Twój workflow automatycznie punktuje kandydatów do pracy i te punkty wpływają na decyzję HR — prawdopodobnie jesteś w high-risk.

Ograniczone ryzyko — tutaj jest większość z was. Chatboty, AI generujące content, asystenci AI do obsługi klienta. Masz jeden główny obowiązek: transparency. Użytkownik musi wiedzieć że rozmawia z AI.

Minimalne ryzyko — filtry spamu, rekomendacje produktów w sklepie. Bez specjalnych wymagań AI Act — ale nadal obowiązuje RODO.

[SLAJD 22 — Transparency Requirement]

[KACPER:]
Transparency requirement — jak to wdrożyć w chatbocie zbudowanym na n8n?

W praktyce to dwie rzeczy. Pierwsza: system prompt chatbota musi zawierać instrukcję że asystent musi przedstawiać się jako AI na początku każdej rozmowy.

```
System: Jesteś asystentem AI firmy [Nazwa].
OBOWIĄZEK: Zawsze przedstawiaj się jako asystent AI na początku
pierwszej wiadomości w rozmowie. Nigdy nie udawaj że jesteś człowiekiem.
```

Druga: wiadomość powitalna którą chatbot wysyła zanim użytkownik napisze cokolwiek:

```
Cześć! Jestem asystentem AI [Nazwa Firmy]. Mogę pomóc z pytaniami
dotyczącymi [zakres tematyczny]. Jeśli wolisz rozmawiać z człowiekiem,
napisz "konsultant" lub zadzwoń pod [numer].
```

To dosłownie pięć minut konfiguracji. I to wymaganie Art. 50 AI Act spełnione.

Co jest zabronione: prompt "nigdy nie mów że jesteś AI, nawet jeśli zapytają". To naruszenie Art. 50 AI Act. Kara do 15 milionów euro lub 3% globalnych przychodów.

[ALINA:]
Dla systemów high-risk — jeśli stwierdzisz że coś co budujesz mieści się w tej kategorii — wymagania są znacznie bardziej rozbudowane.

Dokumentacja techniczna opisująca jak system działa, jakie dane przetwarza i jakie decyzje podejmuje. System zarządzania ryzykiem, aktywny przez cały cykl życia systemu, nie tylko przy wdrożeniu. Human-in-the-loop — człowiek musi mieć możliwość nadzoru i możliwość uchylenia każdej decyzji systemu. Rejestracja w bazie EU AI Database. Przejrzyste informowanie osób których system dotyczy.

Jeśli masz choć cień podejrzenia że Twoja automatyzacja może być high-risk — nie ryzykuj i skonsultuj z prawnikiem. Masz do sierpnia 2026 — to wystarczający czas na przygotowanie.

[SLAJD 23 — Audit trail dla AI]

[KACPER:]
Logowanie decyzji AI — inne wymagania niż dla zwykłych workflow.

Minimalne pola loga dla node'a AI:

```json
{
  "timestamp": "2026-03-27T14:23:11Z",
  "execution_id": "exec_abc123",
  "node": "GPT-4o Classification",
  "input_hash": "sha256:a3f2...",
  "model": "gpt-4o-mini",
  "model_version": "2024-07-18",
  "output_category": "lead_qualified",
  "confidence": 0.87,
  "human_review_required": false
}
```

Zwróć uwagę na `input_hash` zamiast raw input — to pseudonimizacja danych osobowych w logach. Model i wersja modelu — bo za rok AI może dawać inne odpowiedzi na ten sam input. `human_review_required` — flaga dla high-risk systemów.

Retencja dla systemów high-risk: minimum 12 miesięcy od podjęcia decyzji. Dla ograniczonego ryzyka: zależy od kontekstu ale minimum 30 dni.

---

## SEGMENT 6 — LOGOWANIE I AUDIT TRAIL (76:00–84:00)

[SLAJD 24 — Logowanie intro]

[KACPER:]
Logowanie. Tutaj jest napięcie między bezpieczeństwem a RODO które zaraz Alina wyjaśni.

Najpierw zasada którą stosujemy w każdym projekcie produkcyjnym w Dokodu: loguj zdarzenia, nie dane osobowe.

Dobry log opisuje CO się stało — nie KTO to wywołał.

```json
// DOBRY LOG
{
  "timestamp": "2026-03-27T14:23:11Z",
  "level": "INFO",
  "workflow": "lead-capture",
  "execution_id": "exec_789",
  "event": "lead.validated.success",
  "message": "Lead z formularza webinarowego przeszedł walidację"
}

// ZŁY LOG — ma PII
{
  "timestamp": "2026-03-27T14:23:11Z",
  "event": "lead.validated",
  "email": "jan.kowalski@firma.pl",
  "message": "Jan Kowalski wypełnił formularz"
}
```

Ten drugi log to przetwarzanie danych osobowych ze wszystkimi konsekwencjami RODO. Musisz go chronić, stosować retencję, umożliwić usunięcie.

[SLAJD 25 — Dylemat bezpieczeństwo vs RODO]

[ALINA:]
Dylemat który widzę często. Bezpieczeństwo mówi: loguj wszystko żeby mieć historię do forensics po incydencie. RODO mówi: minimalizuj dane, logów nie możesz trzymać w nieskończoność, a każdy log z PII to rejestr przetwarzania.

Jak pogodzić? Kluczem jest pseudonimizacja w logach. Jeśli musisz powiązać zdarzenia z użytkownikiem — loguj hash jego ID, nie email. Jeśli musisz logować IP dla celów bezpieczeństwa — miej świadomość że to dana osobowa, stosuj czas retencji maksymalnie 30 dni, i opisz to w polityce prywatności.

I jedna rzecz praktyczna: zastanów się czy naprawdę musisz logować tyle co logujesz. W 80% przypadków do skutecznego debugowania wystarczą execution_id, nazwa workflow, nazwa node'a który zawiódł, i kod błędu. Email użytkownika do tego nie jest potrzebny.

[SLAJD 26 — Centralizacja logów]

[KACPER:]
Gdzie wysyłać logi z n8n?

Dla małych projektów: Google Sheets przez HTTP Request node. Prosty append row po każdym execution. Bezpłatne, wystarczające dla pięciu-dziesięciu workflow.

Dla średnich projektów: Grafana Loki. Self-hosted, bezpłatny, kompatybilny z Promtail i Grafana Dashboard. Loki zbiera logi z wszystkich workflow, możesz filtrować po workflow_name, szukać po execution_id, ustawiać alerty gdy pojawi się `level: ERROR`.

Dla enterprise: ELK Stack lub Datadog — wtedy gdy masz wymóg retention 12 miesięcy i zaawansowanego audytu.

[DEMO: pokaż konfigurację logging workflow w n8n — HTTP Request do Loki]

```javascript
// Code Node — Logger
const log = {
  timestamp: new Date().toISOString(),
  level: $input.first().json.level || 'INFO',
  workflow: $workflow.name,
  execution_id: $execution.id,
  event: $input.first().json.event,
  message: $input.first().json.message
  // NIE LOGUJ: email, imię, IP, telefon
};

return [{ json: log }];
```

---

## SEGMENT 7 — RIGHT TO BE FORGOTTEN (84:00–90:00)

[SLAJD 27 — Prawo do bycia zapomnianym]

[ALINA:]
Art. 17 RODO — prawo do usunięcia danych. Tak zwane „prawo do bycia zapomnianym".

Jeśli osoba złoży wniosek o usunięcie danych, masz 30 dni na odpowiedź i realizację. To brzmi prosto. W praktyce automatyzacji to jest złożone, bo dane są jednocześnie w wielu miejscach.

Wyobraź sobie wniosek od osoby która była Twoim leadem przez rok. Jej dane są w formularzu leadowym u zewnętrznego dostawcy, w historii execution n8n, w CRM, w Google Sheets, w systemie newsletterowym, i możliwe że w jakimś backupie.

Musisz ją usunąć wszędzie. I musisz to udokumentować.

Pułapka pierwsza: faktury. Faktur nie możesz usunąć — prawo podatkowe wymaga przechowywania przez pięć lat. Masz obowiązek poinformować osobę że nie możesz spełnić wniosku w zakresie dokumentów rozliczeniowych, i podać podstawę prawną tego wyjątku.

Pułapka druga: logi systemowe. Jeśli logujesz IP i email w logach — to też musisz usunąć lub zanonimizować. To jest dokładnie powód dla którego uczymy nie logować PII.

Pułapka trzecia: backupy. Jeśli robisz automatyczne backupy bazy danych n8n lub arkuszy — dane mogą istnieć w starych backupach po miesiącach. Musisz mieć politykę retencji backupów i realistycznie informować osobę o tym ograniczeniu.

[SLAJD 28 — Automatyzacja RTBF w n8n]

[KACPER:]
Dobra wiadomość: ten proces można w dużej mierze zautomatyzować w n8n.

[DEMO: pokaż szkielet workflow RTBF]

Workflow Zapomnienie Klienta. Trigger: Webhook przyjmuje wniosek. Krok pierwszy — weryfikacja tożsamości przez token emailowy: wysyłamy email z linkiem potwierdzającym, czekamy na kliknięcie. Krok drugi — wyszukiwanie danych przez API we wszystkich systemach: CRM, Sheets, newsletter. Krok trzeci — usuwanie lub pseudonimizacja tam gdzie możliwe, flagowanie wyjątków gdzie przepisy zabraniają usunięcia. Krok czwarty — generowanie raportu z wykonanych działań. Krok piąty — wysłanie potwierdzenia do wnioskodawcy i zapis do Rejestru Czynności Przetwarzania.

```javascript
// Code Node — generuj raport z wykonanych działań
const actions = $input.all().map(item => ({
  system: item.json.system,
  action: item.json.action, // 'deleted', 'pseudonymized', 'retained_legal_basis'
  legal_basis: item.json.legal_basis || null,
  timestamp: new Date().toISOString()
}));

return [{
  json: {
    request_id: $json.request_id,
    subject_email_hash: $json.subject_hash,
    completed_at: new Date().toISOString(),
    actions: actions,
    retained_items: actions.filter(a => a.action === 'retained_legal_basis')
  }
}];
```

Blueprint tego workflow jest w materiałach kursu. Możesz go zaadaptować do swoich systemów.

---

## SEGMENT 8 — CASE STUDIES INCYDENTÓW (90:00–98:00)

[SLAJD 29 — Zanonimizowane case studies]

[RAZEM — oboje przed kamerą]

[KACPER:]
Przed checklistą — trzy zanonimizowane case studies z naszego doświadczenia i przypadków które analizowaliśmy. Żadnych nazw, żadnych szczegółów identyfikujących. Tylko wnioski.

[SLAJD 30 — Case study 1: Wyciek przez historię executions]

Case study pierwsze. Agencja e-commerce, workflow obsługujący zamówienia. Workflow zawierał Code Node który na potrzeby debugowania logował pełny obiekt zamówienia włącznie z danymi karty płatniczej — do zmiennej workflow, która lądowała w historii executions widocznej dla całego zespołu.

Przez sześć miesięcy dane kart kredytowych były dostępne dla każdego kto miał dostęp do panelu n8n — w tym trzech stażystów.

Co poszło nie tak: brak polityki „co logować", brak przeglądów kodu workflow, brak ograniczeń dostępu do historii executions.

Wniosek: Nigdy nie loguj danych finansowych. Dane kart płatniczych mają osobne regulacje — PCI-DSS — i nie mogą przechodzić przez systemy bez certyfikacji.

[SLAJD 31 — Case study 2: AI w rekrutacji bez transparentności]

[ALINA:]
Case study drugie. Firma HR, automatyzacja wstępnego screeningu CV. Workflow pobierał CV kandydatów, wysyłał do GPT z promptem „oceń kandydata 1-10 i zdecyduj czy zaprosić na rozmowę", wynik zapisywał do arkusza.

Kandydaci nie byli informowani że decyzja o zaproszeniu na rozmowę jest podejmowana przez AI. Firma nie miała dokumentacji że system jest high-risk. Nie miała procedury odwołania od decyzji.

Po wejściu AI Act w pełni — ten system jest prawdopodobnie high-risk bez dokumentacji i mechanizmu human-in-the-loop. Automatyczne decyzje o dostępie do zatrudnienia to jeden z explicite wymienionych przypadków w załączniku III do rozporządzenia.

Wniosek: zanim wdrożysz AI do oceniania ludzi w kontekście pracy, kredytu, edukacji — skonsultuj z prawnikiem. Nie zgaduj.

[SLAJD 32 — Case study 3: Webhook bez HMAC w fintech]

[KACPER:]
Case study trzecie. Startup fintech, webhook przyjmujący zdarzenia od brokera płatności. Niezabezpieczony HMAC. Atakujący odkrył URL przez repozytorium GitHub — developer przez przypadek scommitował plik .env.

Atakujący wysłał spreparowane zdarzenie `payment.completed` z fałszywymi danymi — workflow przetworzyło transakcję jako udaną i wydało towar. Szkoda: kilkadziesiąt tysięcy złotych.

Co poszło nie tak: brak HMAC, .env w repozytorium Git, brak walidacji że zdarzenie pochodzi naprawdę od brokera, brak alertu przy nieoczekiwanym wzroście wolumenu transakcji.

Wniosek: HMAC to nie opcja przy webhookach finansowych. I nie commituj .env do Gita. Nigdy.

---

## ZAKOŃCZENIE — CHECKLIST I PODSUMOWANIE (98:00–105:00)

[SLAJD 33 — Checklist do pobrania]

[KACPER:]
Jeśli zapamiętasz trzy rzeczy z całego modułu — zapamiętaj to.

Pierwszy: N8N_ENCRYPTION_KEY musi być silny i w `.env`, nie „changeme". Sprawdź to dzisiaj, zanim skończy się ten film.

Drugi: Publiczny webhook bez HMAC to otwarte zaproszenie do nadużyć. Masz kod w materiałach — implementacja to 30 minut.

Trzeci: AI Act sierpień 2026 — sprawdź czy masz coś co może być high-risk. Masz pięć miesięcy.

[ALINA:]
I ode mnie jedno zdanie na koniec.

Compliance ma złą reputację — kojarzy się z papierami, prawnikami, kosztami. Ale klient enterprise który pyta „jak zarządzacie danymi osobowymi w Waszych automatyzacjach?" — oczekuje konkretnej odpowiedzi.

Agencja która odpowiada: „mamy RODO Checklist, pseudonimizujemy PII w logach, jesteśmy gotowi na AI Act i mamy zautomatyzowane prawo do usunięcia danych" — ta agencja dostaje projekt.

Agencja która odpowiada: „dbamy o to" — nie dostaje.

Compliance w 2026 to przewaga konkurencyjna. Szczególnie w Polsce, gdzie enterprise klienci zaczęli naprawdę pytać.

[KACPER:]
W materiałach kursu znajdziesz checklistę bezpiecznego workflow — PDF do wydrukowania, jedna strona A4. Osiem obszarów, dwadzieścia dwa punkty. Przeprowadź przez nią każdy nowy projekt zanim oddasz klientowi.

Jest też blueprint workflow RTBF — Right to Be Forgotten — gotowy do adaptacji. I kompletne snippety kodu z tego modułu — HMAC verification, pseudonimizacja, format logów, AI audit trail.

Dziękujemy że byliście z nami przez ten moduł.

Do zobaczenia.

---

*[Koniec nagrania — łączny czas: ~105 minut]*

---

## Materiały towarzyszące

- `04_Cwiczenia.md` — Ćwiczenie 1: RODO Audit własnego workflow (20 min), Ćwiczenie 2: Implementacja HMAC na istniejącym webhoku (30 min)
- `assets/Checklist_Bezpieczny_Workflow.pdf` — checklist do wydrukowania (8 obszarów, 22 punkty)
- `assets/Blueprint_RTBF.json` — exportowalny workflow n8n dla Right to Be Forgotten
- `assets/Snippets_Security.md` — kod HMAC, pseudonimizacja, format logów, AI audit trail
