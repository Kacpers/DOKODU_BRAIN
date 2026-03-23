---
type: customer-profile
status: active
owner: kacper
last_reviewed: 2026-03-06
tags: [klient, logistyka, wdrozenie, n8n, erp, retainer]
client_since: 2026-01-10
---

# KLIENT: Corleonis
> Klient wdrozeniowy (Faza 2/4) + retainer od maja 2026.
> Projekt: [[../../../10_PROJECTS/PRJ_Corleonis_Wdrozenie/PRJ_Corleonis_Wdrozenie|PRJ_Corleonis_Wdrozenie]]

---

## PROFIL FIRMY

| Pole | Wartosc |
| :--- | :--- |
| **Pelna nazwa** | Corleonis _[uzupelnij]_ |
| **NIP** | _[uzupelnij]_ |
| **Branza** | Logistyka / Spedycja |
| **Wielkosc** | ~150 pracownikow, 15 w logistyce |
| **Lokalizacja** | _[uzupelnij]_ |
| **Glowny system (ERP)** | Comarch ERP XL |
| **Email** | Outlook (O365) |
| **Storage** | MinIO (S3-compatible, on-premise) |
| **AI wczesniej** | Brak |
| **Klientem od** | 2026-01-10 |
| **Zrodlo leada** | LinkedIn |

---

## KONTAKTY

| Imie i Nazwisko | Stanowisko | Email | Telefon | Rola |
| :--- | :--- | :--- | :--- | :--- |
| _[uzupelnij]_ | Head of Logistics | _[email]_ | _[tel]_ | Decision Maker + Champion |
| _[uzupelnij]_ | IT Administrator | _[email]_ | _[tel]_ | Techniczny kontakt |
| _[uzupelnij]_ | CFO / Ksiegowosc | _[email]_ | _[tel]_ | Stakeholder (wplywa na budzet) |

**Preferowany kanal:** Email (formalny) + Slack (operacyjny — czy maja?)
**Najlepszy czas kontaktu:** Ranki (8-10), unikac piatek popołudnia

---

## KONTEKST BIZNESOWY

**Glowny problem:**
> Dzial logistyki przetwarza ~500 dokumentow miesiecznie (faktury, WZ, CMR, listy przewozowe) recznie. Email → reczne przepisanie do Comarch ERP XL → archiwizacja lokalna. Czas: ~3 minuty/dokument = ~25h/mies. straconej pracy.

**Obliczony ROI:**
- Oszczędnosc: ~25h × 65 PLN/h = 1 625 PLN/mies.
- Redukcja bledow: szacunkowo 80% mniej powielonych wpisow
- Payback period: ~22 miesiace (przy cenie projektu 35k)

**Dlaczego wybrali Dokodu:**
- Doswiadczenie z Comarch ERP XL
- Kompleksowe podejscie Tech + Legal (RODO, DPIA)
- Self-hosted n8n = dane zostaja w ich infrastrukturze

**Kryteria sukcesu:**
- >85% dokumentow przetworzonych automatycznie
- Czas przetwarzania <90 sek.
- 0 incydentow bezpieczenstwa
- NPS pracownikow logistyki > 7/10

**Budzet:** 35 000 PLN (projekt) + 3 000 PLN/mies. retainer

---

## STOS TECHNOLOGICZNY

```
ERP:         Comarch ERP XL (REST API — dostepne)
Email:       Outlook O365 (OAuth2)
Storage:     MinIO (S3-compatible, on-premise)
Secrets:     HashiCorp Vault (wdrozony przez Dokodu)
VPS:         [provider] — 4 vCPU, 8GB RAM
n8n:         Self-hosted (Dokodu deployed)
AI Model:    Gemini 1.5 Pro (Google AI Studio API)
```

**Integracje zrealizowane:**
- Outlook → n8n (IMAP OAuth2) ✅
- Gemini API → n8n (HTTP Request) — testowane
- Comarch ERP XL → n8n (REST API) — w trakcie
- MinIO → n8n (S3 Upload) — testowane

---

## HISTORIA WSPOLPRACY

| Data | Zdarzenie | Wartosc | Status |
| :---: | :--- | ---: | :---: |
| 2026-01-10 | Discovery call | — | Zamkniete |
| 2026-01-20 | Propozycja wyslana | — | Zamkniete |
| 2026-02-01 | Umowa podpisana | 35 000 PLN | Zamkniete |
| 2026-02-01 | Zaliczka 30% | 10 500 PLN | Oplacona |
| 2026-02-15 | Faza 1: Discovery zakonczona | — | Zamkniete |
| 2026-03 | Faza 2: Development (aktywna) | — | Aktywne |
| 2026-04-01 | Planowane: Start testow UAT | — | Planowane |
| 2026-04-15 | Planowane: Go-live | — | Planowane |
| 2026-04-15 | Platnosc etap 2 (40%) | 14 000 PLN | Oczekuje |
| 2026-05-01 | Platnosc etap 3 (30%) | 10 500 PLN | Oczekuje |
| 2026-05-01 | Retainer start | 3 000 PLN/mies. | Planowane |

**Lacna wartosc (rok 1):** 35 000 + 24 000 = **59 000 PLN**

---

## RELACJA I NOTES

**Poziom zaufania:** 4/5 — dobra relacja, Head of Logistics jest bardzo zaangazowany
**Kluczowe obserwacje:**
- Head of Logistics jest "internal champion" — przekonany do AI, wspiera projekt wewnatrz
- IT Administrator jest ostrozny — lubi dokumentacje i bezpieczenstwo
- CFO obserwuje ROI — dostarczyc liczby po 30 dniach live

**Ryzyka relacyjne:**
- Jezeli Head of Logistics odejdzie z firmy → projekt w niebezpieczenstwie
- CFO moze zakwestionowac retainer jezeli ROI nie bedzie widoczny

---

## POTENCJAL UPSELL

| Okazja | Wartosc est. | Kiedy | Trigger |
| :--- | ---: | :--- | :--- |
| Rozszerzenie na nowe typy dokumentow | 8 000 - 15 000 PLN | Q3 2026 | Sukces fazy 1 |
| Agent AI dla dzialu handlowego | 20 000 - 35 000 PLN | Q4 2026 | NPS > 8 |
| Szkolenie AI dla calego zespolu | 12 000 - 18 000 PLN | Q3 2026 | Po go-live |
| Audit AI Act (Corleonis) | 8 000 - 12 000 PLN | Q2 2026 | Zblizy sie deadline sierpien |

---

## LINKI
- Projekt: [[../../../10_PROJECTS/PRJ_Corleonis_Wdrozenie/PRJ_Corleonis_Wdrozenie]]
- Spotkania: [[Corleonis_Meetings]]
- Okazje: [[Corleonis_Opportunities]]
- Playbook branżowy: [[../../../30_RESOURCES/RES_Industry_Playbooks/Playbook_Logistyka]]
- DPIA: [Dysk Aliny — link]
