---
type: area
status: active
owner: alina
last_reviewed: 2026-03-06
tags: [legal, rodo, gdpr, dpia, checklist, prywatnosc]
---

# RODO / GDPR — CHECKLIST WDROZENIOWA
> **Zasada Dokodu:** Compliance budujemy w architekturze, nie klepimy w dokumentach po fakcie.
> **Prowadzaca:** Alina Sieradzinska (COO/Legal)

---

## KIEDY RODO JEST ISTOTNE W PROJEKCIE DOKODU

Jezeli projekt spełnia ktorykolwiek z ponizszych kryteriow → RODO jest istotne:

- [ ] System przetwarza jakiekolwiek dane osobowe (email, IP, imie, NIP osoby fiz.)
- [ ] AI analizuje dokumenty zawierajace dane pracownikow lub klientow
- [ ] Chatbot zbiera dane od uzytkownikow
- [ ] Tracking reklamowy / analytics jest wlaczony w scope
- [ ] Dane sa wyslane do zewnetrznych API (OpenAI, Google, Meta itp.)

---

## CHECKLIST: PRZED STARTEM PROJEKTU

### Podstawy prawne (Art. 6 RODO)
- [ ] Zidentyfikowana podstawa prawna przetwarzania:
  - [ ] Zgoda (Art. 6(1)(a)) — wymagana forma pisemna/cyfrowa
  - [ ] Wykonanie umowy (Art. 6(1)(b)) — najczesciej dla danych klientow
  - [ ] Uzasadniony interes (Art. 6(1)(f)) — wymaga testu balansu
  - [ ] Obowiazek prawny (Art. 6(1)(c)) — dla wymogow podatkowych itp.

### Minimalizacja danych
- [ ] Czy przetwarzamy TYLKO dane niezbedne do celu?
- [ ] Czy mozna zastapic dane osobowe danymi anonimowymi lub pseudonimizowanymi?
- [ ] Czas retencji danych zdefiniowany i skonfigurowany technicznie

### Bezpieczenstwo
- [ ] Szyfrowanie danych w spoczynku (at rest): AES-256 min.
- [ ] Szyfrowanie danych w transmisji (in transit): TLS 1.3
- [ ] Sekrety / klucze API przechowywane w Vault (nie w kodzie!)
- [ ] Dostep do danych: zasada minimalnych uprawnien (least privilege)
- [ ] Logi dostepow zachowane (min. 12 miesiecy)

### Umowy
- [ ] Umowa powierzenia przetwarzania danych (Art. 28) podpisana z klientem
- [ ] Umowy z podwykonawcami (OpenAI, Google, hosting) sprawdzone
- [ ] DPA (Data Processing Agreement) z dostawcami AI cloud
  - OpenAI Enterprise: DPA dostepna — czy klient to akceptuje?
  - Google AI Studio: sprawdzic aktualne warunki
  - Anthropic API: sprawdzic DPA

---

## CHECKLIST: DPIA (Data Protection Impact Assessment)

**Kiedy DPIA jest WYMAGANA (Art. 35):**
- [ ] Profilowanie na duzа skale
- [ ] Przetwarzanie szczegolnych kategorii danych (zdrowie, wyznanie, biometria)
- [ ] Systematyczne monitorowanie obszarow publicznych
- [ ] AI podejmujaca decyzje z istotnymi skutkami dla osob

**Struktura DPIA (wg wytycznych UODO):**
1. Opis przetwarzania (co, jak, po co, kto)
2. Ocena niezbednosci i proporcjonalnosci
3. Identyfikacja ryzyk (dla praw i wolnosci osob)
4. Srodki ograniczajace ryzyko
5. Wniosek: czy ryzyko jest akceptowalne?

**Wzor DPIA:** [[30_RESOURCES/RES_Templates/Templates]] → DPIA Template

---

## DANE OSOBOWE W N8N — STANDARDY TECHNICZNE

### Zasady dla wszystkich workflowow n8n Dokodu
1. **Dane wrażliwe NIE trafiają do logów n8n** (wyłacz "Save Execution Data" dla wezłow z PII)
2. **API keys / sekrety** → zawsze przez Credentials Manager lub Vault
3. **Dane zewnetrzne (OpenAI, Google):** sprawdz, czy API nie trenuje sie na Twoich danych
   - OpenAI API (nie ChatGPT.com): domyslnie NIE trenuje sie na danych przez API
   - Google AI Studio: sprawdzic aktualne ustawienia (toggleable)
4. **Anonimizacja przed AI:** jezeli mozliwe, usun/zamien PII przed wyslaniem do LLM
   - Przyklad: zamiast "Jan Kowalski, PESEL 85010112345" → "Klient_A, ID: anonymized"
5. **Retencja:** Configure automatic deletion po zdefiniowanym czasie (n8n execution history)

### Wzorzec anonimizacji w Code Node n8n
```javascript
// Usuwanie PII przed wyslaniem do AI
const anonymize = (text) => {
  return text
    .replace(/\b\d{11}\b/g, '[PESEL]')          // PESEL
    .replace(/\b\d{10}\b/g, '[NIP]')             // NIP (10 cyfr)
    .replace(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g, '[EMAIL]')
    .replace(/\b\d{3}[\s-]?\d{3}[\s-]?\d{3}\b/g, '[TEL]');
};

const cleanText = anonymize($input.item.json.email_body);
return { anonymized_text: cleanText };
```

---

## PRAWA PODMIOTOW DANYCH — SLA Dokodu

Jezeli klient (lub ich klient) zglosza zadanie → musimy moc wykonac:

| Prawo | Art. | Termin realizacji | Jak technicznie? |
| :--- | :---: | :---: | :--- |
| Dostep do danych | 15 | 1 miesiac | Export z bazy / n8n history |
| Sprostowanie | 16 | 1 miesiac | Update w systemie |
| Usuniecie ("prawo do bycia zapomnianym") | 17 | 1 miesiac | Delete script (n8n workflow!) |
| Ograniczenie przetwarzania | 18 | 1 miesiac | Flaga w systemie |
| Przenoszenie danych | 20 | 1 miesiac | Export JSON/CSV |
| Sprzeciw | 21 | Natychmiast | Stop processing workflow |

**Rekomendacja:** Dla kazdego wdrozenia zbuduj "RODO Workflow" w n8n — automatyczna obsluga zadan.

---

## TRANSFER DANYCH POZA UE

Jezeli uzywasz US-based API (OpenAI, Anthropic, AWS, itp.):
- [ ] Standard Contractual Clauses (SCC) sprawdzone / podpisane
- [ ] Transfer Impact Assessment (TIA) jesli dane wrazliwe
- [ ] Alternatywa: modele EU-hosted (Mistral AI, europejskie data centers Google/MS)

**Praktyczna zasada Dokodu:**
- OpenAI API przez Azure (region West Europe) = bezpieczniejszy wybor
- Google Vertex AI (region europe-west1) = GDPR compliant
- Anthropic Claude API = sprawdz aktualne DPA na ich stronie

---

## INCYDENT BEZPIECZENSTWA — PROCEDURA

Jezeli wykryjesz lub podejrzewasz naruszenie:

1. **Zatrzymaj** przetwarzanie danych (wylaczyc workflow w n8n)
2. **Udokumentuj:** co, kiedy, kto, zakres, potencjalny wplyw
3. **Powiadom Aline (COO)** w ciagu 1 godziny
4. **Ocena:** czy naruszenie dotyczy praw osob fizycznych?
5. **UODO:** jezeli ryzyko dla osob — zgloszenie w ciagu **72 godzin**
6. **Klienci:** jezeli ich dane zostaly naruszone — informacja bez zbednej zwloki

**Kontakt UODO:** uodo.gov.pl | tel. 22 531 03 00

---

*Plik prowadzony przez Aline. Kacper konsultuje kwestie techniczne. Przeglad kwartalny.*
