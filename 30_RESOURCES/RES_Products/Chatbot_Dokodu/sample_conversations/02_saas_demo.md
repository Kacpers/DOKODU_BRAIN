---
type: sample-conversation
scenario: SaaS B2B — CTO porównuje narzędzia compliance
outcome: lead captured
duration: 6 min
messages: 14
---

# Przykład 2: SaaS B2B — CTO pyta o bezpieczeństwo + umawia demo

**Kontekst:** FlowOps — SaaS do zarządzania procesami DevOps. W bazie wiedzy: cennik, integracje, SOC 2 attestation, RODO statement, roadmap, case studies. Drzewo tematów: Funkcje → Integracje / Bezpieczeństwo, Cennik, Wsparcie, Umów demo.

---

**👤 Użytkownik (09:14)**
Z jakimi narzędziami się integrujecie?

**🤖 Bot (09:14)**
Natywnie: GitLab, GitHub, Jira, Slack, Datadog. Przez Zapier i webhooki — 3000+ aplikacji. Custom API dostępne w planie Enterprise.

*Sugestie: „Mamy Bitbucket — jak to zrobić?" · „Mamy on-premise GitLab" · „Chcę zobaczyć listę wszystkich webhooków"*

---

**👤 Użytkownik (09:15)**
Mamy on-premise GitLab z self-hosted runnerami.

**🤖 Bot (09:15)**
On-premise GitLab jest wspierane od planu Team wzwyż. Łączymy przez dedykowany agent deployed w Państwa VPC. Self-hosted runnery działają bez zmian.

*Sugestie: „Jak wygląda agent i co robi?" · „SOC 2 — jest?" · „Gdzie trzymacie dane?"*

---

**👤 Użytkownik (09:16)**
SOC 2 mam priorytet. Gdzie przechowujecie dane?

**🤖 Bot (09:16)**
SOC 2 Type II mamy od 2024 r. Dane w regionie EU (Frankfurt, AWS), opcja dedicated instance w innym regionie dostępna dla Enterprise. Szyfrowanie AES-256 at rest, TLS 1.3 in transit.

*Sugestie: „Jaki SLA dla Enterprise?" · „Kiedy kolejny audyt?" · „Data residency — Polska?"*

---

**👤 Użytkownik (09:18)**
Cennik Enterprise?

**🤖 Bot (09:18)**
Enterprise wyceniamy indywidualnie — zaczyna się od 2 500 €/mies. przy 50 seats. Zawiera dedykowaną instancję, SSO, SLA 99,9%, custom DPA i dedicated CSM.

*Sugestie: „Chcę zobaczyć demo" · „Jak długo trwa wdrożenie?" · „Czy można na trial?"*

---

**👤 Użytkownik (09:19)**
Chcę zobaczyć demo, ale potrzebuję kogoś od compliance na calu.

**🤖 Bot (09:19)**
Jasne — na demo z Enterprise prospectami zawsze przychodzi nasz Security Lead. Umówmy spotkanie.

**[Pojawia się pill-button: „Zostaw kontakt: umów demo"]**

---

**Formularz (bottom sheet):**
- Imię i nazwisko *: Marek Piotrowski
- Służbowy e-mail *: m.piotrowski@kompania-x.pl
- Firma *: Kompania X
- Wielkość zespołu: 80 osób w R&D
- Co chcesz zobaczyć na demo?: „Demo plus 20 min z Security Lead. Mamy on-prem GitLab, interesuje nas dedicated agent + DPA."

**[Wyślij zgłoszenie]**

---

**🤖 Bot (09:21)**
✓ Dziękujemy! Mamy już Państwa kontakt — odezwiemy się wkrótce.

---

## Co wylądowało w panelu admina

**Konwersacja:** 10 wiadomości · 7 min · **Lead ✓** · Temat dominujący: *Bezpieczeństwo*

**Lead:**
- Marek Piotrowski, m.piotrowski@kompania-x.pl, Kompania X
- Topic: `demo-lead`
- Team size: 80 osób w R&D
- Note: „Demo plus 20 min z Security Lead. Mamy on-prem GitLab, interesuje nas dedicated agent + DPA."

**Sources:**
- `SOC_2_attestation_2024.pdf` (94%)
- `Security_whitepaper.pdf` (89%)
- `Pricing_enterprise.pdf` (91%)
- `Integrations_catalog.pdf` (83%)

---

## Komentarz biznesowy

- User B2B, techniczny — od razu pyta o konkrety (integracje, compliance).
- Bot prowadzi rozmowę aż do momentu gdy pytanie przekracza to, co ma w bazie („chcę zobaczyć demo z Security Leadem" — to leadgen signal).
- Pre-kwalifikacja: w lead form odchwycone custom pole „team size" i „what do you want on demo" — sales zespół ma pełen brief zanim oddzwoni.
- Marker `[LEAD:demo-lead]` + matchujące pole z drzewa = pełny kontekst w CRM.
