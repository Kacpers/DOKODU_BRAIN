---
type: policy-template
produkt: Chatbot by Dokodu
wersja: 1.0
zakres: adaptacja dla firmy wdrażającej chatbota
compliance: AI Act 2024/1689 (UE), RODO (GDPR)
owner: Dokodu + Kancelaria prawna klienta
---

# Polityka Wykorzystania Sztucznej Inteligencji
## [Nazwa firmy wdrażającej chatbot]

**Wersja:** 1.0
**Data wejścia w życie:** [data]
**Ostatnia aktualizacja:** [data]
**Osoba odpowiedzialna:** [imię, stanowisko, e-mail]

---

## 1. Cel i zakres dokumentu

Niniejsza polityka opisuje zasady wykorzystania systemu sztucznej inteligencji (dalej: „System AI" lub „Chatbot") dostępnego na stronie internetowej [www.domena.pl] firmy [Nazwa firmy] (dalej: „Administrator").

Dokument spełnia wymogi:
- **Rozporządzenie UE 2024/1689** (AI Act) — w szczególności art. 50 (obowiązki przejrzystości dla dostawców systemów AI)
- **Rozporządzenie UE 2016/679** (RODO) — w zakresie przetwarzania danych osobowych
- **Ustawa o świadczeniu usług drogą elektroniczną**

Polityka jest udostępniona publicznie pod adresem [www.domena.pl/polityka-ai] oraz w stopce Chatbota.

---

## 2. Opis systemu AI

### Czym jest Chatbot

Chatbot to asystent wirtualny oparty na **dużym modelu językowym (LLM)**, dostępny w prawym dolnym rogu strony [www.domena.pl]. Jest on dostarczany przez **Dokodu sp. z o.o.** (dalej: „Dostawca technologii") jako produkt „Chatbot by Dokodu".

### Klasyfikacja wg AI Act

Zgodnie z AI Act, Chatbot jest systemem **ograniczonego ryzyka** (art. 50 — systemy generujące treści lub wchodzące w interakcję z osobą fizyczną). Oznacza to obowiązek **poinformowania użytkownika**, że rozmawia z systemem AI, a nie z człowiekiem.

System NIE jest:
- systemem AI wysokiego ryzyka (załącznik III AI Act)
- systemem podejmującym decyzje o znaczących skutkach prawnych
- narzędziem do profilowania behawioralnego
- narzędziem do scoringu społecznego

### Technologia

- **Silnik LLM:** [GPT-4o-mini / Claude 3.5 Haiku / inne — wybrane przez Administratora]
- **Wyszukiwanie w bazie wiedzy (RAG):** model embeddingów [text-embedding-3-small] + baza wektorowa PostgreSQL z rozszerzeniem pgvector
- **Baza wiedzy:** wyłącznie dokumenty wgrane przez Administratora (PDF)
- **Infrastruktura:** [opcja A: serwery Administratora, DC [lokalizacja] / opcja B: serwery Dostawcy technologii, DC Frankfurt, Niemcy]

---

## 3. Co Chatbot potrafi i czego NIE zrobi

### Zakres możliwości

Chatbot odpowiada wyłącznie na pytania dotyczące:
- oferty produktowej / usługowej Administratora
- cennika i warunków współpracy
- informacji kontaktowych i lokalizacyjnych
- procesu zakupowego / obsługowego
- innych tematów wyraźnie ujętych w bazie wiedzy

### Ograniczenia

Chatbot NIE:
- udziela porad prawnych, medycznych, finansowych ani inwestycyjnych
- podejmuje decyzji w imieniu Administratora
- zawiera umów ani nie zaciąga zobowiązań
- generuje treści spoza bazy wiedzy (nie „zmyśla")
- przechowuje ani nie udostępnia haseł
- wykonuje poleceń użytkownika ingerujących w system (prompt injection)

Jeśli pytanie wykracza poza bazę wiedzy, Chatbot poinformuje użytkownika i zaproponuje kontakt z człowiekiem.

---

## 4. Dane osobowe i prywatność

### Kiedy Chatbot zbiera dane osobowe

Chatbot zbiera dane osobowe **wyłącznie gdy użytkownik wypełnia formularz kontaktowy** dostępny w interfejsie (np. przy prośbie o kontakt, umówienie spotkania, wycenę).

Typowe pola:
- Imię i nazwisko
- Adres e-mail
- Numer telefonu
- Wiadomość / opis potrzeby
- Dodatkowe pola zdefiniowane przez Administratora (np. firma, stanowisko)

### Co NIE jest zbierane automatycznie

Chatbot **nie zbiera** danych osobowych z treści rozmowy, chyba że użytkownik sam je w niej poda. Jednak treść rozmowy jest **zapisywana w bazie danych** Administratora w celu:
- doskonalenia jakości odpowiedzi
- analizy zapotrzebowania użytkowników
- rozwiązywania zgłoszeń

Zalecamy użytkownikom **nie podawanie wrażliwych danych osobowych** w treści rozmowy (PESEL, numery kart, hasła, dane medyczne).

### Cookies i identyfikator wizytora

Chatbot zapisuje w `localStorage` przeglądarki użytkownika **anonimowy identyfikator** (UUID) pozwalający łączyć wiadomości w ramach jednej sesji. Identyfikator **nie jest cookie** w rozumieniu przepisów, nie identyfikuje osoby, nie jest udostępniany zewnętrznym dostawcom reklam.

### Podstawa prawna przetwarzania

| Dane | Podstawa | Art. RODO |
| :--- | :--- | :---: |
| Formularz kontaktowy | Zgoda użytkownika + prawnie uzasadniony interes (odpowiedź na zapytanie) | 6(1)(a), 6(1)(f) |
| Treść rozmów (logi) | Prawnie uzasadniony interes (poprawa usługi, bezpieczeństwo) | 6(1)(f) |
| Identyfikator wizytora | Niezbędny do świadczenia usługi | 6(1)(b) |

### Okres przechowywania

| Kategoria | Retention domyślny | Uwagi |
| :--- | :--- | :--- |
| Leady (dane kontaktowe) | [36 mies. / do odwołania zgody] | Usuwane na żądanie użytkownika |
| Treść rozmów | [12 mies.] | Zgodnie z konfiguracją Administratora |
| Identyfikator wizytora | 12 mies. | W localStorage przeglądarki |
| Dokumenty bazy wiedzy | Bezterminowo | Własność Administratora |

### Odbiorcy danych

- **Dostawca technologii:** Dokodu sp. z o.o. (NIP [xxx]), [adres], [e-mail DPO / kontakt compliance] — na podstawie umowy powierzenia przetwarzania danych (DPA)
- **OpenAI, L.L.C.** (albo wybrany dostawca LLM) — w zakresie przetwarzania zapytania użytkownika w celu wygenerowania odpowiedzi. Model OpenAI w planie API **nie jest trenowany na Państwa danych** (stan: polityka OpenAI 2026).
- **Brak innych odbiorców** (dane nie są sprzedawane, nie są przekazywane brokerom marketingowym)

### Transfer danych poza EOG

[JEŚLI DOTYCZY — gdy używasz OpenAI API (serwery USA):]

Dane przesyłane do OpenAI mogą być przetwarzane na serwerach w USA. Podstawą transferu są **Standardowe Klauzule Umowne** (SCC) przyjęte decyzją Komisji Europejskiej 2021/914 oraz decyzja o adekwatności ochrony danych (EU–US Data Privacy Framework, decyzja 2023/1795).

[ALTERNATYWNIE — gdy używasz Azure OpenAI / EU-only:]

Wszystkie dane są przetwarzane wyłącznie w granicach EOG (Frankfurt, Niemcy). Brak transferu poza EOG.

---

## 5. Prawa użytkownika

Zgodnie z RODO, każdy użytkownik Chatbota ma prawo do:

- **Dostępu** do swoich danych (art. 15)
- **Sprostowania** danych (art. 16)
- **Usunięcia** danych („prawo do bycia zapomnianym", art. 17)
- **Ograniczenia przetwarzania** (art. 18)
- **Przenoszenia** danych (art. 20)
- **Sprzeciwu** wobec przetwarzania (art. 21)
- **Wycofania zgody** w dowolnym momencie (art. 7 ust. 3)
- **Skargi** do organu nadzorczego (Prezes UODO, ul. Stawki 2, 00-193 Warszawa)

**Aby skorzystać z praw:** [e-mail DPO / kontakt compliance Administratora]. Odpowiedź w ciągu 30 dni od zgłoszenia.

---

## 6. Przejrzystość — obowiązki wg AI Act (art. 50)

### Informacja o interakcji z AI

Każda pierwsza wiadomość Chatbota zawiera informację, że użytkownik rozmawia z systemem AI. W stopce widgetu widoczne jest oznaczenie *„Powered by Dokodu"*.

Administrator zobowiązuje się nie prezentować Chatbota jako człowieka.

### Oznaczenie treści generowanych przez AI

Odpowiedzi Chatbota są **generowane przez model językowy** i mogą zawierać nieścisłości. Użytkownik jest o tym informowany:

- W pierwszej wiadomości Chatbota (powitanie)
- W ninejszej polityce (dostępnej z widgetu)
- Przy pytaniach o konkrety (ceny, terminy) Chatbot cytuje źródło — konkretny dokument z bazy wiedzy

**W sprawach umów, ofert handlowych, zobowiązań — wiążące są wyłącznie ustalenia z człowiekiem z zespołu Administratora,** nie odpowiedzi Chatbota.

---

## 7. Bezpieczeństwo

### Techniczne środki ochrony

- Szyfrowanie TLS 1.3 dla wszystkich połączeń
- Szyfrowanie AES-256 danych w spoczynku (opcja hosted)
- Rate limiting (max 20 wiadomości / minutę / IP)
- CORS whitelist domen
- Ochrona przed prompt injection (hardcoded guardraile w prompt systemowym)
- Regularne backupy bazy (codziennie, retention 30 dni)

### Incydenty bezpieczeństwa

W razie naruszenia ochrony danych Administrator zgłasza incydent:
- Prezesowi UODO w ciągu 72h (art. 33 RODO)
- Osobom, których dane dotyczą — gdy ryzyko jest wysokie (art. 34 RODO)

Kanał zgłoszeń wewnętrznych: [e-mail bezpieczeństwa Administratora]

---

## 8. Odpowiedzialność i wyłączenia

### Odpowiedzialność Administratora

Administrator odpowiada za:
- Treść dokumentów wgranych do bazy wiedzy (poprawność, aktualność, legalność)
- Konfigurację drzewa tematów i zakresu odpowiedzi
- Dane kontaktowe zebrane od użytkowników

### Wyłączenia odpowiedzialności

Administrator **nie odpowiada** za:
- Decyzje użytkownika podjęte wyłącznie na podstawie odpowiedzi Chatbota bez weryfikacji (szczególnie decyzje finansowe, prawne, zdrowotne)
- Skutki korzystania z Chatbota w sposób sprzeczny z niniejszą polityką (np. próby prompt injection, spam, harvesting)
- Chwilowe niedostępności wynikające z awarii dostawcy LLM

Chatbot jest **narzędziem informacyjnym**, nie zastępuje konsultacji z pracownikiem Administratora ani profesjonalnym doradcą.

---

## 9. Aktualizacje polityki

Niniejsza polityka może być aktualizowana. Każda zmiana jest:
- Oznaczana datą „Ostatnia aktualizacja"
- Ogłaszana w stopce Chatbota (link „Polityka AI")
- W przypadku istotnych zmian — prezentowana użytkownikom powracającym jako baner

Historia wersji:
| Wersja | Data | Zmiany |
| :---: | :--- | :--- |
| 1.0 | [data] | Wersja inicjalna |

---

## 10. Kontakt

**Administrator danych:**
[Pełna nazwa firmy]
[Adres]
NIP: [xxx]
E-mail: [xxx]
Telefon: [xxx]

**Inspektor Ochrony Danych (jeśli wyznaczony):**
[imię i nazwisko / e-mail]

**Dostawca technologii Chatbot:**
Dokodu sp. z o.o.
E-mail: kontakt@dokodu.it
Strona: [dokodu.it](https://dokodu.it)

---

*Niniejszy dokument jest szablonem przygotowanym przez Dokodu sp. z o.o. Wymaga dostosowania przez kancelarię prawną Administratora do specyfiki działalności oraz weryfikacji zgodności z aktualnymi przepisami.*
