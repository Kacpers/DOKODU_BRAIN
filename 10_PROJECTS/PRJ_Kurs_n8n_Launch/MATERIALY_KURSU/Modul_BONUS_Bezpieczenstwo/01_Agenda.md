---
type: course-material
modul: BONUS_A
status: ready
owner: kacper
last_reviewed: 2026-03-27
tags: [kurs, n8n, bezpieczenstwo, rodo, ai-act, compliance, agenda]
---

# Moduł BONUS A: Bezpieczeństwo i Compliance — Agenda nagrania

> **Czas całkowity:** ~90 minut
> **Format:** Kacper (tech) + Alina (prawo) — nagranie wspólne, podział segmentów
> **Wyjątkowość:** Nikt w Polsce nie łączy n8n + RODO + AI Act w jednym module praktycznym

---

## PLAN NAGRANIA — TIMELINE

### SEGMENT 1 — INTRO I HOOK (0:00–5:00) | 5 minut
**Prowadzący:** Kacper + Alina razem

- Hook Kacpra: historia incydentu (webhook bez zabezpieczeń → wyciek danych)
- Alina: "To nie jest straszak — to mapa do bezpiecznego deploymentu"
- Zapowiedź: co konkretnie pokażemy (lista 6 obszarów)
- Dlaczego TERAZ jest krytyczne: AI Act wchodzi w życie 08.2026 (za 5 miesięcy!)

---

### SEGMENT 2 — CREDENTIAL VAULT (5:00–20:00) | 15 minut
**Prowadzący:** Kacper

**5:00–10:00 | n8n built-in vault — kiedy wystarczy**
- Co to jest n8n Credentials i jak to działa pod spodem
- Encryption key (`N8N_ENCRYPTION_KEY`) — gdzie go ustawić i dlaczego nie może być "changeme"
- Środowisko DEV vs PROD — różne zestawy credentials
- Demonstracja: credential w environment variable vs hardcoded w workflow

**10:00–15:00 | HashiCorp Vault — kiedy jest niezbędny**
- Scenariusz: klient enterprise, wiele środowisk, rotacja kluczy
- Architektura: n8n → Vault Agent → sekret
- Dynamiczne sekrety: klucz API generowany na czas jednej sesji (!)
- Demonstracja: HTTP Request do Vault API z n8n

**15:00–20:00 | Least Privilege Principle w praktyce**
- Zasada: każdy workflow ma dostęp TYLKO do tego, czego potrzebuje
- Przykład złej konfiguracji: jeden klucz OpenAI do wszystkiego
- Rotacja kluczy: harmonogram + workflow n8n do automatycznej rotacji
- Checklist: audyt credentials przed przejściem na produkcję

---

### SEGMENT 3 — RODO W AUTOMATYZACJACH (20:00–50:00) | 30 minut
**Prowadzący:** Alina (prawo) + Kacper (implementacja techniczna)

**20:00–27:00 | Jakie dane osobowe przepływają przez Twój workflow [ALINA]**
- Data Flow Audit: jak narysować mapę przepływu danych
- Dane osobowe w n8n: e-mail, IP, imię/nazwisko, cookies, NIP osoby fizycznej
- Pułapka: "dane anonimowe" które anonimowe nie są (IP + timestamp = identyfikacja)
- Zgody i podstawy prawne dla automatycznego przetwarzania (Art. 6 RODO)
- Kiedy potrzebujesz zgody, a kiedy wystarczy uzasadniony interes

**27:00–35:00 | Pseudonimizacja i anonimizacja w Code Node [KACPER + demo]**
- Różnica: pseudonimizacja (odwracalna) vs anonimizacja (nieodwracalna)
- Implementacja SHA-256 hash dla e-maila w n8n Code Node
- Microsoft Presidio jako tarcza PII przed wysyłką do LLM API
- Demonstracja: workflow z Presidio w architekturze Dokodu

**35:00–42:00 | Prawo do usunięcia danych — automatyzacja [ALINA + KACPER]**
- Co mówi RODO (Art. 17 — prawo do bycia zapomnianym)
- Typowe pułapki: dane w logach, backupach, systemach zewnętrznych
- Workflow n8n: wniosek RTBF → wyszukanie we wszystkich systemach → usunięcie → potwierdzenie
- Czas na odpowiedź: 30 dni (RODO) — jak to monitorować automatycznie

**42:00–50:00 | RODO Checklist dla workflow n8n [slajd + omówienie]**
- Przegląd kompletnej checklisty (slajd)
- Najczęstsze błędy które widzimy w audytach klientów
- Umowa powierzenia przetwarzania: kiedy wymagana z dostawcami API

---

### SEGMENT 4 — AI ACT 2024/1689 (50:00–65:00) | 15 minut
**Prowadzący:** Alina + Kacper

**50:00–57:00 | Klasyfikacja ryzyka — gdzie jesteś [ALINA]**
- 4 kategorie ryzyka: unacceptable, high, limited, minimal
- High-risk w praktyce agencji automatyzacji: HR screening, credit scoring, rekrutacja
- Timeline: 08.2026 — pełne stosowanie dla high-risk. 5 miesięcy zostało!
- Które automatyzacje Dokodu buduje → które są potencjalnie high-risk

**57:00–62:00 | Transparency requirement — chatboty i AI agents [ALINA + KACPER]**
- Art. 50 AI Act: użytkownik MUSI wiedzieć że rozmawia z AI
- Implementacja w n8n: pierwsza wiadomość chatbota z informacją
- Deep-fake i syntetyczny content: obowiązek oznaczenia
- Demonstracja: system prompt z wymaganym disclosure

**62:00–65:00 | Audit trail dla systemów AI [KACPER]**
- Dlaczego AI potrzebuje szczególnego loggingu (decyzje muszą być wyjaśnialne)
- Co logować dla compliance: input, model version, output, timestamp, user ID (pseudonimy)
- Retencja logów AI: minimum 12 miesięcy dla high-risk systemów

---

### SEGMENT 5 — BEZPIECZEŃSTWO SIECI (65:00–78:00) | 13 minut
**Prowadzący:** Kacper

**65:00–69:00 | n8n za reverse proxy**
- Nginx/Caddy: konfiguracja headers, rate limiting, TLS termination
- Przykładowy nginx.conf dla n8n (gotowy template)
- NIGDY n8n nie powinien być dostępny bezpośrednio na porcie 5678 w produkcji

**69:00–74:00 | Webhook security — HMAC signature verification**
- Problem: publiczny webhook = każdy może go wywołać
- HMAC: jak działa (diagram)
- Implementacja w n8n Code Node: weryfikacja podpisu HMAC-SHA256
- IP whitelisting jako dodatkowa warstwa (Nginx + n8n)

**74:00–78:00 | Rate limiting**
- Na poziomie Nginx: limit_req_zone
- Na poziomie n8n: Workflow Executions per minute
- Alertowanie gdy przekroczony próg

---

### SEGMENT 6 — LOGOWANIE I AUDIT TRAIL (78:00–87:00) | 9 minut
**Prowadzący:** Kacper

- Co logować vs czego nie logować (dylemat RODO vs bezpieczeństwo)
- Dokodu Logging Standard v1.0 — format JSON, pola obowiązkowe
- Centralizacja logów: Grafana Loki (self-hosted, free) vs ELK Stack
- Server-side tracking zamiast client-side: dlaczego i jak

---

### SEGMENT 7 — PODSUMOWANIE I NASTĘPNE KROKI (87:00–90:00) | 3 minuty
**Prowadzący:** Kacper + Alina

- Recap: 6 obszarów bezpieczeństwa = Twoja tarcza
- Ćwiczenia do modułu (zapowiedź 04_Cwiczenia.md)
- Alina: "Compliance to nie koszt — to przewaga gdy klient pyta"
- Link do Security Checklist PDF (materiał do pobrania)

---

## MATERIAŁY DO PRZYGOTOWANIA

| Materiał | Prowadzący | Status |
| :--- | :--- | :---: |
| Slajdy (02_Prezentacja.md) | Kacper | Do przygotowania |
| Skrypt nagrania (03_Skrypt.md) | Kacper + Alina | Do przygotowania |
| Ćwiczenia (04_Cwiczenia.md) | Kacper | Do przygotowania |
| Workflow Blueprint (05_Workflow_Blueprint.md) | Kacper | Do przygotowania |
| nginx.conf template | Kacper | Do przygotowania |
| Security Checklist PDF | Alina + Kacper | Do przygotowania |

---

## UWAGI TECHNICZNE DO NAGRANIA

- Nagraj demo Presidio na osobnym ekranie (demo-n8n.dokodu.it)
- Przygotuj "złośliwy" webhook request bez podpisu do pokazania problemu
- Alina nagrywa swoje segmenty osobno jeśli nie możemy się spotkać — montaż na zmianę
- Screen ratio: 16:9, n8n UI powiększony do 125% dla czytelności
