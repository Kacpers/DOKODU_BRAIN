---
type: lead_magnet
status: draft
format: pdf_source
owner: kacper
created: 2026-03-29
tags: [ai-act, compliance, lead-magnet, pdf, bramkowany-content]
---

<!-- STRONA 1: OKLADKA -->

# AI Act Checklist 2026

## Czy Twoja firma jest gotowa?

### 12 kroków do zgodności z Rozporządzeniem UE 2024/1689

---

**Dokodu.it** — Wdrożenia AI z wbudowaną zgodnością prawną

Kacper Sieradzinski (CEO / Tech) + Alina Sieradzinska (COO / Legal)

*Wersja: Marzec 2026*

---

<!-- STRONA 2: DLACZEGO TO WAZNE -->

## Dlaczego nie możesz tego ignorować

Rozporządzenie AI Act (UE 2024/1689) to pierwszy na świecie kompleksowy akt prawny regulujący sztuczną inteligencję. Obowiązuje wszystkie firmy działające na rynku UE — niezależnie od tego, czy AI tworzą, wdrażają czy tylko z niej korzystają. **Kary sięgają 35 milionów EUR lub 7% globalnego rocznego obrotu** — biorą pod uwagę kwotę wyższą.

Przepisy wchodzą w życie etapami. Zakazy dotyczące systemów niedopuszczalnego ryzyka obowiązują od lutego 2025. **Najważniejszy milestone — pełne wymogi dla systemów wysokiego ryzyka — wchodzi 2 sierpnia 2026.** To za kilka miesięcy.

Według naszych obserwacji większość polskich firm średniej wielkości nie rozpoczęła jeszcze przygotowań. Jeśli korzystasz z Copilota, ChatGPT Enterprise, własnych chatbotów lub automatyzacji AI — ta checklista jest dla Ciebie.

---

<!-- STRONA 3-6: CHECKLISTA 12 KROKOW -->

## Checklista: 12 kroków do zgodności z AI Act

---

### 1. Inwentaryzacja systemów AI w firmie

- [ ] **Zrób pełną listę wszystkich narzędzi AI, z których korzysta Twoja firma.**

Przejdź przez każdy dział i spisz wszystkie systemy wykorzystujące sztuczną inteligencję — od ChatGPT i Copilota, przez wewnętrzne chatboty, po automatyzacje w CRM, HR czy księgowości. Uwzględnij też narzędzia, z których pracownicy korzystają na własną rękę (shadow AI). Bez tej listy nie możesz przejść do żadnego kolejnego kroku.

**Deadline:** Natychmiast — to fundament całego procesu
**Odpowiada:** CTO / IT Manager + przedstawiciele każdego działu

---

### 2. Klasyfikacja ryzyka każdego systemu

- [ ] **Przypisz każdemu systemowi AI kategorię ryzyka: zakazane, wysokie, ograniczone lub minimalne.**

AI Act dzieli systemy na 4 kategorie. Systemy zakazane (np. social scoring, manipulacja podświadoma) musisz natychmiast wyłączyć. Systemy wysokiego ryzyka (HR, rekrutacja, scoring kredytowy, infrastruktura krytyczna) podlegają najsurowszym wymogom. Chatboty i generatory treści to ryzyko ograniczone. Filtry spamu czy rekomendacje to ryzyko minimalne. Większość firm ma systemy z kilku kategorii jednocześnie.

**Deadline:** Do końca Q2 2026
**Odpowiada:** CTO + Dział Prawny

---

### 3. Dokumentacja techniczna systemów wysokiego ryzyka

- [ ] **Przygotuj pełną dokumentację techniczną dla każdego systemu zakwalifikowanego jako wysokie ryzyko.**

Jeśli Twój system AI wpływa na decyzje dotyczące ludzi (rekrutacja, ocena pracowników, scoring), musisz udokumentować: jak działa, na jakich danych był trenowany, jakie ma ograniczenia i jak testujesz jego dokładność. Dokumentacja musi być aktualna i dostępna dla organów nadzoru na żądanie.

**Deadline:** Do 2 sierpnia 2026
**Odpowiada:** CTO / Zespół AI + Dział Prawny

---

### 4. Transparentność — informowanie użytkowników o AI

- [ ] **Upewnij się, że każdy użytkownik wie, kiedy wchodzi w interakcję z AI.**

Każdy chatbot musi jasno informować: "Rozmawiasz z asystentem AI, nie z człowiekiem." Treści generowane przez AI (teksty, obrazy, wideo) muszą być odpowiednio oznaczone. Deep-faki wymagają wyraźnego oznaczenia. Użytkownik musi mieć możliwość przejścia do kontaktu z człowiekiem na żądanie.

**Deadline:** Obowiązuje już teraz (od sierpnia 2025 dla generatywnej AI)
**Odpowiada:** Product Manager / UX + Marketing

---

### 5. Human oversight — nadzór człowieka nad AI

- [ ] **Wyznacz konkretne osoby odpowiedzialne za nadzór nad każdym systemem AI.**

Dla systemów wysokiego ryzyka musisz wdrożyć mechanizm "human-in-the-loop" — człowiek musi mieć możliwość interwencji, nadpisania decyzji AI lub wyłączenia systemu. To nie może być fikcja — osoba nadzorująca musi rozumieć system, mieć uprawnienia do działania i regularnie przeglądać wyniki AI.

**Deadline:** Do 2 sierpnia 2026
**Odpowiada:** Kierownik działu korzystającego z AI + CTO

---

### 6. Zarządzanie danymi treningowymi

- [ ] **Sprawdź jakość, reprezentatywność i legalność danych używanych przez Twoje systemy AI.**

Jeśli trenujesz lub fine-tunujesz modele AI na własnych danych, musisz zapewnić, że dane są kompletne, wolne od stronniczości (bias) i legalnie pozyskane. Dotyczy to też sytuacji, gdy dostawca AI trenuje model na Twoich danych — sprawdź ustawienia API i DPA. Dane treningowe zawierające dane osobowe wymagają dodatkowej podstawy prawnej.

**Deadline:** Do 2 sierpnia 2026 (dla systemów wysokiego ryzyka)
**Odpowiada:** Data Engineer / CTO + DPO

---

### 7. Cyberbezpieczeństwo systemów AI

- [ ] **Zabezpiecz systemy AI przed atakami, manipulacją i wyciekiem danych.**

Systemy AI są podatne na specyficzne ataki: prompt injection, data poisoning, model extraction. Musisz zadbać o: szyfrowanie danych (AES-256 w spoczynku, TLS 1.3 w transmisji), kontrolę dostępu (zasada minimalnych uprawnień), logi aktywności (min. 12 miesięcy) i przechowywanie kluczy API w sejfie (Vault), nie w kodzie.

**Deadline:** Natychmiast — to podstawa bezpieczeństwa
**Odpowiada:** CISO / IT Security + CTO

---

### 8. Generative AI i Foundation Models — obowiązki wobec dostawców

- [ ] **Sprawdź, czy Twoi dostawcy AI (OpenAI, Google, Microsoft, Anthropic) spełniają wymogi AI Act.**

Jeśli korzystasz z modeli foundation (GPT, Gemini, Claude, Llama) — ich dostawcy mają własne obowiązki: dokumentacja techniczna, polityka praw autorskich, oznaczanie treści generowanych przez AI. Ty jako deployer musisz zweryfikować, że dostawca je spełnia. Sprawdź aktualne DPA (Data Processing Agreement) i warunki użytkowania. Preferuj modele hostowane w UE (Azure West Europe, Google europe-west1).

**Deadline:** Obowiązki dostawców GPAI od maja 2025; Twoja weryfikacja — bieżąca
**Odpowiada:** CTO + Dział Zakupów / Procurement

---

### 9. RODO x AI Act — przetwarzanie danych osobowych

- [ ] **Przeprowadź DPIA (ocenę skutków) dla każdego systemu AI przetwarzającego dane osobowe.**

AI Act nie zastępuje RODO — nakłada się na niego. Jeśli Twój system AI przetwarza dane osobowe (emaile, imiona, numery telefonów, dane HR), potrzebujesz: podstawy prawnej przetwarzania, DPIA dla systemów podejmujących zautomatyzowane decyzje, anonimizacji danych przed wysłaniem do zewnętrznych API oraz zdefiniowanego czasu retencji danych.

**Deadline:** Natychmiast — RODO już obowiązuje; DPIA dla AI to wymóg bieżący
**Odpowiada:** DPO (Inspektor Ochrony Danych) + CTO

---

### 10. Rejestracja w unijnej bazie systemów AI

- [ ] **Zarejestruj systemy wysokiego ryzyka w EU AI Database przed ich uruchomieniem.**

Od sierpnia 2026 każdy system AI zakwalifikowany jako wysokie ryzyko musi zostać zarejestrowany w ogólnounijnej bazie danych prowadzonej przez Komisję Europejską. Rejestracja wymaga podania informacji o systemie, jego przeznaczeniu, dostawcy i osobie odpowiedzialnej. Bez rejestracji nie możesz legalnie uruchomić takiego systemu na rynku UE.

**Deadline:** Do 2 sierpnia 2026 (przed uruchomieniem systemu)
**Odpowiada:** Dział Prawny + CTO

---

### 11. Odpowiedzialność i ubezpieczenie

- [ ] **Określ, kto ponosi odpowiedzialność za decyzje AI i rozważ ubezpieczenie OC.**

Jeśli system AI popełni błąd — kto odpowiada? Ty jako firma wdrażająca, dostawca modelu, czy integrator? Ustal to w umowach z dostawcami i klientami. Dla systemów wysokiego ryzyka rozważ dedykowane ubezpieczenie od odpowiedzialności cywilnej za szkody spowodowane przez AI. Sprawdź, czy Twoje obecne polisy OC pokrywają scenariusze związane z AI.

**Deadline:** Do Q3 2026
**Odpowiada:** Zarząd + Dział Prawny + Broker ubezpieczeniowy

---

### 12. Szkolenia zespołu z AI literacy

- [ ] **Przeszkol wszystkich pracowników korzystających z AI — od zarządu po operacje.**

Art. 4 AI Act wymaga, żeby każda osoba pracująca z systemami AI miała odpowiedni poziom wiedzy (AI literacy). To nie jest opcja — to obowiązek prawny. Szkolenia powinny obejmować: podstawy działania AI, ograniczenia i ryzyka, zasady bezpiecznego korzystania, procedury eskalacji problemów i podstawy AI Act istotne dla danego stanowiska.

**Deadline:** Bieżąco — obowiązek od wejścia w życie AI Act (sierpień 2024)
**Odpowiada:** HR / L&D + CTO + Zarząd

---

<!-- STRONA 7: CTA -->

## Nie musisz tego robić sam

Ta checklista to punkt wyjścia. Ale sama lista nie wystarczy — potrzebujesz kogoś, kto zrozumie zarówno technologię, jak i prawo.

**Dokodu to jedyna agencja AI w Polsce, która łączy inżynierię wdrożeń z audytem prawnym w jednym zespole.** Kacper odpowiada za technologię, Alina za compliance. Dzięki temu zgodność z regulacjami budujemy w architekturze systemu od pierwszego dnia — nie doklejamy jej po fakcie.

---

### AI Act Ready Audit

Dwudniowy audyt Twoich systemów AI zakończony raportem i planem naprawczym.

**Co dostajesz:**
- Pełną inwentaryzację i klasyfikację ryzyka Twoich systemów AI
- Raport zgodności z AI Act i RODO
- Konkretny plan naprawczy z priorytetami i terminami
- Rekomendacje techniczne (architektura, bezpieczeństwo, logi)

**Cena:** 8 000 - 15 000 PLN netto (zależnie od liczby systemów)
**Czas realizacji:** 2 dni audyt + 5 dni roboczych na raport

---

### Skontaktuj się

**Kacper Sieradzinski** — CEO / Tech Lead
- Email: kacper@dokodu.it
- Telefon: 508 106 046
- Web: [dokodu.it/automatyzacja-ai](https://dokodu.it/automatyzacja-ai)

---

*Dokodu.it — Zero-Trust AI: Compliance by Design*

*Ten dokument ma charakter informacyjny i nie stanowi porady prawnej. Aby uzyskać indywidualną ocenę zgodności, skontaktuj się z nami.*
