---
type: project
status: active
owner: kacper
last_reviewed: 2026-03-06
tags: [projekt, wdrozenie, corleonis, dokumenty, n8n, erp]
client: Corleonis
value_pln: 35000
retainer_pln: 3000
deadline: 2026-04-15
health: green
---

# PRJ: Corleonis — Wdrozenie Obiegu Dokumentow
> **Typ:** Wdrozenie produkcyjne (Automatyzacja + AI Agent)
> **Wartosc kontraktu:** 35 000 PLN netto + retainer 3 000 PLN/mies.
> **Status:** ZIELONY — Stabilne
> **Termin Fazy 1:** 2026-04-15
> **Kontakt klienta:** _______________ (Head of Logistics) | Tel: _______________
> **Kontakt Dokodu:** Kacper (Arch.) + Alina (DPIA/Legal)

---

## BRIEF PROJEKTU

**Problem klienta:**
Dzial logistyki Corleonis przetwarza ~500 dokumentow miesiecznie (faktury, WZ, CMR, listy przewozowe). Proces: email → reczne przepisanie do ERP → archiwizacja lokalna. Czas: ~3 minuty/dokument = ~25h/miesiac w straconej pracy.

**Rozwiazanie Dokodu:**
Automatyczny pipeline obiegowy:
1. Email/Skan wplywa na dedykowana skrzynke
2. n8n odbiera, uruchamia AI parser (Gemini 1.5 Pro)
3. Ekstrakcja strukturyzowanych danych (JSON) + walidacja NIP, kwot
4. Automatyczne wejscie do ERP (Comarch ERP XL via API)
5. Archiwizacja w S3-compatible storage
6. Powiadomienie na Slack/Teams z podsumowaniem

**ROI dla klienta:**
- Oszczednosc: ~25h/mies. × 65 PLN/h = 1 625 PLN/mies.
- Redukcja bledow: szacunkowo 80% mniej powielonych wpisow
- Payback period: ~22 miesiace

---

## ARCHITEKTURA TECHNICZNA

```
[Email Inbox]
    ↓ (IMAP/OAuth2)
[n8n: Trigger — Email Received]
    ↓
[n8n: Extract Attachments — PDF/Image]
    ↓
[n8n: HTTP Request → Gemini 1.5 Pro API]
    (System prompt: Parser dokumentow ksiegowych)
    ↓
[n8n: Code Node — Walidacja JSON]
    (Sprawdz NIP, kontrola sumy VAT, schema v1)
    ↓
[Decision: Czy walidacja przeszla?]
    ├── TAK → [n8n: HTTP → ERP API (Comarch)]
    │          [n8n: S3 Upload — archiwum]
    │          [n8n: Slack — OK notification]
    └── NIE → [n8n: Email → Manual Review Queue]
               [n8n: Slack — UWAGA: wymagana weryfikacja]
```

**Stack technologiczny:**
- n8n: Self-hosted (VPS, 4 vCPU, 8GB RAM)
- AI Model: Gemini 1.5 Pro (via Google AI Studio API)
- Sekrety: HashiCorp Vault (integracja z n8n)
- Storage: MinIO (S3-compatible, on-premise)
- Monitoring: n8n built-in logs + Grafana (opcja)
- ERP: Comarch ERP XL REST API

---

## FAZY I CHECKLIST

### FAZA 1: DISCOVERY I MAPOWANIE (ZAKONCZONE)
- [x] Mapowanie procesow w dziale logistyki (2h warsztatu)
- [x] Inwentaryzacja typow dokumentow (faktury, WZ, CMR, inne)
- [x] Analiza API Comarch ERP XL — dokumentacja odebrana
- [x] Ocena wolumenu (500 dok/mies.) i jakosci skanov

### FAZA 2: SETUP I DEVELOPMENT (W TRAKCIE)
- [x] VPS skonfigurowany, n8n zainstalowany
- [x] Vault wdrozony, sekrety API zaladowane
- [ ] **Workflow n8n — v1.0 gotowy** (cel: 2026-03-10)
  - [x] Trigger email (OAuth2 Outlook)
  - [x] Ekstrakcja PDF attachments
  - [ ] Integracja Gemini — dopracowanie promptu dla CMR
  - [ ] Code Node: walidacja JSON + kontrola NIP
  - [ ] ERP API connector — testowe wejscie
- [ ] DPIA (Data Protection Impact Assessment) — Alina przygotowuje

### FAZA 3: TESTY (2026-03-15 — 2026-04-01)
- [ ] **Unit tests:** kazdy node osobno (dane mockowane)
- [ ] **Idempotency check:** uruchomienie tego samego dokumentu 2x — czy duplikat w ERP?
- [ ] **Edge cases:** dokumenty nieczytelne, brak zalacznika, zly format
- [ ] **Performance test:** 50 dokumentow jednoczesnie — czy VPS daje rade?
- [ ] **Security audit:** czy PII wycieka poza siec klienta?
- [ ] **UAT (User Acceptance Testing)** z 3 pracownikami logistyki

### FAZA 4: GO-LIVE I STABILIZACJA (2026-04-01 — 2026-04-15)
- [ ] Migracja ze srodowiska testowego na produkcje
- [ ] Szkolenie 2h dla administratora systemu (klient-side)
- [ ] Dokumentacja techniczna (Confluence lub PDF)
- [ ] Konfiguracja alertow w n8n (blad workflow → SMS/Slack)
- [ ] Monitoring przez 2 tygodnie (SLA: odpowiedz <4h)

### FAZA 5: RETAINER (od 2026-05-01)
- [ ] Umowa retainer podpisana (3 000 PLN/mies.)
- [ ] Zakres retainera: monitoring, male zmiany, support, miesięczny report
- [ ] Review miesięczny: metryki, nowe typy dokumentow, optymalizacja

---

## COMPLIANCE & SECURITY

### RODO / DPIA
- [ ] DPIA sporządzona i zaakceptowana — Alina prowadzi ([[RODO_Checklist]])
- [ ] Klauzule powierzenia przetwarzania danych podpisane
- [ ] Czas retencji danych w archiwum zdefiniowany (klient: 5 lat)
- [ ] Procedura usuwania danych po retencji skonfigurowana w n8n

### Bezpieczenstwo technicze
- [ ] Vault: rotacja kluczy co 90 dni (automatyczny trigger w n8n)
- [ ] Network: VPS za VPN klienta (nie publiczne IP)
- [ ] Szyfrowanie at rest: MinIO z AES-256
- [ ] Szyfrowanie in transit: TLS 1.3 wszedzie
- [ ] Logi dostepu: zachowane 12 miesiecy
- [ ] Backup konfiguracji n8n: co tydzien na zewnetrzny storage

### AI Act Compliance
- [ ] Klasyfikacja systemu: niskie ryzyko (proces wewnetrzny, decyzja czlowieka)
- [ ] Human-in-the-loop: niejasne dokumenty → manual review queue (nie AI finalnie)
- [ ] Disclosure: klient poinformowany, ze AI analizuje dokumenty

---

## RYZYKA I MITYGACJE

| Ryzyko | Poziom | Status | Mitygacja |
| :--- | :---: | :---: | :--- |
| ERP API zmiana (Comarch update) | Sredni | Monitorowany | Versioning w URL, testy regresji |
| Jakos skanow ponizej 150 DPI | Wysoki | Aktywny | Preprocessing (deskew, enhance) w n8n |
| Gemini API: quota limit | Sredni | Monitorowany | Retry z exponential backoff |
| Vault niedostepny (VPS down) | Niski | Zarzadzany | Fallback: env zmienne (tylko dev!) |
| Pracownicy omijaja system | Sredni | Badany | Szkolenie + change management |

---

## METRYKI SUKCESU (mierzone po 30 dniach live)
- Proc. dokumentow przetworzonych automatycznie (cel: >85%)
- Proc. bledow walidacji (cel: <5%)
- Sredni czas przetworzenia dokumentu (cel: <90 sek.)
- NPS od pracownikow logistyki (cel: >7/10)
- Liczba incydentow bezpieczenstwa (cel: 0)

---

## LINKI I ZASOBY
- Umowa + aneksy: [Dysk — link]
- Dokumentacja API Comarch: [Link]
- DPIA draft: [Dysk Aliny — link]
- [[30_RESOURCES/RES_n8n_Blueprints/N8N_Blueprints]] — Blueprint #003: Document Parser
- [[30_RESOURCES/RES_Prompt_Library/300_BIBLIOTEKA_PROMPTOW]] — Prompt: Ekstrakcja danych z PDF
