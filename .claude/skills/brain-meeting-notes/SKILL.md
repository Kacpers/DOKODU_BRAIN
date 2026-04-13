---
name: brain-meeting-notes
description: Przetwarza surowe notatki lub transkrypcje ze spotkania i zapisuje je w ustrukturyzowanym formacie do pliku Meetings klienta w DOKODU_BRAIN. Wydobywa kluczowe ustalenia, cytaty, akcje i sales intelligence. Inspirowany meeting-insights-analyzer z awesome-claude-skills. Trigger: "zapisz spotkanie", "dodaj notatke ze spotkania", "przetworz spotkanie", /brain-meeting-notes
---

# Meeting Notes Processor — Dokodu Edition

Adaptacja meeting-insights-analyzer dla Dokodu. Zamiast analizy komunikacji — zapisuje operacyjna wiedze ze spotkania do systemu.

## KIEDY UZYWAC

- Zaraz po rozmowie z klientem (telefonicznej, Teams, on-site)
- Po discovery callu
- Po kickoffie
- Po rozmowie statusowej
- Po nieformlanej rozmowie (networking, konferencja)

**Najlepiej: zaraz po spotkaniu. Pamiec ginie szybko.**

## JAK UZYWAC

Wklej surowe notatki lub transkrypcje:
```
Mialem spotkanie z Corleonis dzisiaj. Opowiedz co ustalilismy:
- Head of Logistics mowil ze chce wdrozyc do konca marca
- IT Admin pytal o bezpieczenstwo Vault
- Wspominali ze dzial handlowy tez ma problemy z dokumentami
- NPS po rozmowie: pozytywny
Nastepny krok: wyslac dokumentacje Vault do IT Admina
```

Lub wklej transkrypcje (Otter, Teams, Google Meet):
```
[TRANSKRYPCJA]
...pelna tresc...
```

## PROCES

### 1. Identyfikacja klienta

Zapytaj (jezeli nie podano): "Ktory klient? Jaki byl typ spotkania?"
Sprawdz czy katalog klienta istnieje w `/home/kacper/DOKODU_BRAIN/20_AREAS/AREA_Customers/`.

### 2. Ekstrakcja ze surowych notatek

Z podanego tekstu wyodrebnij:

**Kluczowe ustalenia** — fakty, decyzje, potwierdzenia
**Cytaty dosłowne** — co klient powiedzial (bezcenne dla propozycji i case study)
**Akcje** — kto co robi i do kiedy
**Sales Intelligence** — sygnaly, bole, potencjal upsell, ryzyka relacyjne
**Sentiment** — ogolny nastroj spotkania (pozytywny / neutralny / negatywny / napiety)

### 3. Sformatuj notatke

Uzyteczny format do wpisania do `[Klient]_Meetings.md`:

```markdown
## YYYY-MM-DD — [TEMAT SPOTKANIA]

**Uczestnicy:** [lista]
**Typ:** [discovery | kickoff | status | upsell | support]
**Sentiment:** [pozytywny/neutralny/negatywny]

**Kluczowe ustalenia:**
1. [ustalenie 1]
2. [ustalenie 2]

**Cytaty klienta:**
> "[dokladny cytat]"
> "[dokladny cytat]"

**Akcje:**
| Kto | Akcja | Deadline |
| :--- | :--- | :---: |
| Kacper | | |
| [Klient] | | |

**Nastepne spotkanie:** [data lub "TBD"]

**Sales Intelligence:**
- [obserwacja 1 — potencjal / ryzyko / sygnaly]
- [obserwacja 2]
```

### 4. Zapisz do pliku

Dodaj notatke na GORZE (nie na dole) pliku `[Klient]_Meetings.md`.
Najnowsze spotkanie zawsze na gorze.

### 5. Akcje do Inboxu / CRM

Jezeli sa akcje Kacpra z deadlinem → zaproponuj dodanie do `00_INBOX.md`.
Jezeli jest potencjal upsell → zaproponuj dodanie do `[Klient]_Opportunities.md`.

### 6. Aktualizuj profil klienta

Jezeli na spotkaniu pojawily sie nowe informacje (budzet, kontakty, problemy) → zaproponuj aktualizacje `[Klient]_Profile.md`.

## WYNIKI

Po przetworzeniu wyswietl:
- Sformatowana notatka (do wklejenia lub auto-zapis)
- Lista akcji Kacpra (TOP 3)
- Sales Intelligence summary (1-3 punkty)
- Nastepny krok z tym klientem

## CRM SYNC

Po zapisaniu notatki do Meetings.md, zsynchronizuj spotkanie do CRM:
```bash
python ~/DOKODU_BRAIN/scripts/crm_sync.py push-meeting "<nazwa_klienta>"
```
To utworzy Activity (type: MEETING) w CRM powiazana z firma.

## ZASADY

- Cytaty klienta ZAWSZE dosłownie — nie parafrazuj
- Sales Intelligence to PRYWATNA sekcja — nie dla klienta
- Jezeli brak deadlinu dla akcji — wstaw "PILNIE" lub zapytaj
- Sentiment napiety/negatywny → dodaj do alertow w Inboxie
