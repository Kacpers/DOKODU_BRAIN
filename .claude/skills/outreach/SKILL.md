---
name: outreach
description: Prowadzi prospecting LinkedIn krok po kroku — identyfikuje buying signals, pokazuje następną firmę, generuje spersonalizowane DM/email, śledzi status w CRM. Użyj gdy Kacper mówi "outreach", "prospecting", "leady linkedin", "kontaktujemy firmy", "wysyłamy DM" lub `/outreach`.
---

# Outreach — Prospecting LinkedIn krok po kroku

## Cel

Prowadzenie Kacpra przez proces kontaktowania firm B2B na LinkedIn. Claude przygotowuje research, wiadomości i śledzi status — Kacper tylko szuka osoby na LinkedIn i klika "wyślij".

## Kiedy używać

- `/outreach` — rozpocznij sesję prospectingową
- `/outreach status` — pokaż pipeline i co wymaga follow-upu
- `/outreach [nazwa firmy]` — przejdź do konkretnej firmy
- "kontaktujemy firmy", "leady", "prospecting", "wyślij DM"

## Kiedy NIE używać

- Gdy Kacper chce dodać nowego leada manualnie → `/brain-add-lead`
- Gdy Kacper chce zbadać firmę bez kontaktu → `/brain-lead-research`
- Gdy rozmowa już trwa i trzeba napisać email → `/brain-draft-email`

## Dane wejściowe

Skill automatycznie wczytuje:
1. `20_AREAS/AREA_Marketing_Sales/Lead_Qualification_Full_*.md` — zakwalifikowane firmy (Score A/B/C/X)
2. `20_AREAS/AREA_Marketing_Sales/Outreach_Kit_*.md` — gotowe researche i szablony (jeśli istnieje)
3. `20_AREAS/AREA_Marketing_Sales/Outreach_Tracker.md` — status kontaktów (jeśli istnieje)
4. `20_AREAS/AREA_Marketing_Sales/CRM_Leady_B2B.md` — aktywny pipeline
5. `30_RESOURCES/RES_Sales_Playbook/Sales_Playbook.md` — oferta i ceny Dokodu

## Proces

### KROK 1: Załaduj stan

Przeczytaj Outreach_Tracker.md (jeśli istnieje). Pokaż podsumowanie:

```
OUTREACH STATUS
═══════════════
Firmy Score A: X (Y skontaktowanych, Z oczekujących)
Firmy Score B: X
Do follow-upu DZIŚ: [lista]
Następna firma do kontaktu: [nazwa]
```

Jeśli Outreach_Tracker.md nie istnieje — stwórz go na podstawie Lead_Qualification_Full.

### KROK 1.5: Identyfikacja buying signals

Przed kontaktem sprawdź sygnały zakupowe firmy. Im więcej sygnałów → wyższy priorytet kontaktu.

**Sygnały z danych (automatyczne):**
- 🔍 **Rekrutacja tech/IT** — firma zatrudnia na stanowiska techniczne (z Lead_Qualification)
- 📈 **Wzrost firmy** — nowe lokalizacje, przejęcia, funding (sprawdź web)
- 🔄 **Zmiana w C-suite** — nowy CTO/COO/CDO = nowe priorytety
- ⚠️ **Compliance pressure** — branża regulowana (AI Act, RODO, KSeF)

**Sygnały z kontekstu (sprawdź ręcznie):**
- 💬 **Aktywność LinkedIn** — decision maker publikuje o AI/automatyzacji
- 🏆 **Konkurencja wdraża** — ich competitor ogłosił AI transformation
- 📢 **Publiczne ogłoszenie** — firma wspomniała o digitalizacji w mediach
- 🔥 **Pain event** — wyciek danych, duży błąd, utrata klienta

**Scoring:**
- 3+ sygnały → 🔴 KONTAKTUJ NATYCHMIAST (priorytet nad kolejką Score A)
- 2 sygnały → 🟡 Kontaktuj w standardowej kolejce
- 0-1 sygnał → 🟢 Standardowa kolejka

Wyświetl przy każdej firmie w KROK 2:
```
BUYING SIGNALS: [X/8]
✅ Rekrutacja tech (stanowisko: [X])
✅ Compliance pressure (branża: [X])
❌ Brak widocznej zmiany C-suite
...
```

### KROK 2: Wybierz firmę

Pokaż następną firmę Score A która nie została jeszcze skontaktowana. Wyświetl:

```
═══ NASTĘPNA FIRMA ═══
[Nazwa firmy]
Stanowisko: [tytuł z ogłoszenia]
Branża: [branża]
Rekomendowana oferta: [SZ/W/A/D]
Buying signals: [X/8] — [🔴/🟡/🟢]

RESEARCH:
- Czym się zajmują: [1 zdanie]
- Prawdopodobny ból: [1-2 zdania]
- Procesy do automatyzacji: [2-3 bullet points]

KOGO SZUKAĆ NA LINKEDIN:
→ Wejdź na linkedin.com/search → wpisz "[Firma]" → People
→ Filtruj po Title: "[Tytuł 1]" lub "[Tytuł 2]" lub "[Tytuł 3]"
→ Szukasz kogoś kto wygląda jak szef osoby z ogłoszenia

Znalazłeś kogoś? Podaj imię, nazwisko i stanowisko.
```

**Jeśli research nie istnieje w Outreach_Kit** — wygeneruj go na miejscu na podstawie:
- Nazwa firmy + stanowisko z ogłoszenia + branża
- Wiedza o typowych procesach w tej branży
- ICP Dokodu i oferta z Sales Playbook

### KROK 3: User podaje osobę

Gdy Kacper poda imię, nazwisko i stanowisko, wygeneruj:

**A) Notatkę do zaproszenia LinkedIn (max 300 znaków)**
- Spersonalizowana pod firmę i stanowisko
- Ton: profesjonalny ale ludzki, nie sprzedażowy
- Wspomina ogłoszenie jako sygnał
- Kończy na "chętnie dodam do sieci"

**B) DM po akceptacji (do wysłania 2-3 dni po zaproszeniu)**
- Nawiązanie do ogłoszenia i bólu firmy
- 1 social proof (Animex 40 os., Corleonis wdrożenie, lub inny aktualny)
- Propozycja 30-min rozmowy bez zobowiązań
- Podpis: Kacper | dokodu.it

**C) Cold email jako backup**
- Subject line: 2-4 słowa, lowercase, BEZ imienia odbiorcy (-12% reply!), bez sales speak — wzór patrz `references/subject-lines.md`
- Body: 5-7 zdań max
- CTA: 30-min rozmowa
- Podpis z linkiem do dokodu.it/automatyzacja-ai

Pokaż wszystkie 3 w blokach ```code``` gotowych do skopiowania.

### KROK 4: Zaktualizuj tracker

Po wygenerowaniu wiadomości, zaktualizuj `Outreach_Tracker.md`:

```markdown
| Firma | Osoba | Stanowisko | Data zaproszenia | Status | Następny krok | Data follow-up |
```

Statusy: `zaproszenie_wysłane` → `zaakceptowane` → `dm_wysłany` → `odpowiedział` → `call_umówiony` → `propozycja` → `wygrana/przegrana`

### KROK 5: Następna firma lub follow-up

Zapytaj:
- "Następna firma?" → wróć do KROKU 2
- "Ktoś zaakceptował?" → pokaż listę oczekujących, generuj DM follow-up
- "Koniec na dziś" → pokaż podsumowanie sesji

## Tryb `/outreach status`

Pokaż tabelę ze wszystkimi kontaktami i ich statusem. Podświetl wg cadence (patrz `references/follow-up-cadence.md`):

| Sygnał | Akcja |
| :--- | :--- |
| Zaproszenia bez akceptacji >5 dni | Rozważ cold email z innym angle |
| Akceptacje bez DM | Wyślij DM dziś (Day 0 sequence) |
| DM bez odpowiedzi 3 dni | Touch 1 — nowa wartość/insight |
| DM bez odpowiedzi 7-8 dni | Touch 2 — social proof / mini-case |
| DM bez odpowiedzi 14 dni | Touch 3 — resource (ebook, post bloga) |
| DM bez odpowiedzi 21-28 dni | Touch 4 — **breakup email** (1-2-3 format), potem STOP |

**Reguła brzegowa:** Jeśli wysłałeś breakup mail — nie kontaktuj się ponownie z tej osoby. Honor zobowiązania.

## Follow-up content rules

Każdy follow-up musi spełniać:
- [ ] Wnosi NOWĄ wartość (nie "bumping this up")
- [ ] Inny angle niż poprzedni touch
- [ ] Brak phrases-killerów ("just checking in", "wracam do mojej wiadomości")
- [ ] CTA dopasowane do seniority (CEO = ultra-low effort, manager = konkret)

Pełna kadencja + przykłady polskich breakup maili → `references/follow-up-cadence.md`

## Tryb `/outreach [firma]`

Przejdź bezpośrednio do konkretnej firmy — pokaż research i status, generuj wiadomość.

## Output

- Wiadomości: wyświetlane w czacie w blokach code (do skopiowania)
- Tracker: `20_AREAS/AREA_Marketing_Sales/Outreach_Tracker.md`
- CRM: aktualizacja `CRM_Leady_B2B.md` gdy lead przejdzie do etapu `call_umówiony`

## CRM Sync

Po kazdej interakcji outreach, zaloguj aktywnosc w CRM:
```bash
python ~/DOKODU_BRAIN/scripts/crm_sync.py push-activity "<firma>" linkedin_message "<temat>"
```

## Zasady jakości

1. **Nigdy nie wysyłaj wiadomości automatycznie** — zawsze pokazuj do skopiowania
2. **Personalizuj pod firmę i branżę** — żadnych generycznych "pomagamy firmom wdrażać AI"
3. **Notatka LinkedIn max 300 znaków** — limit platformy
4. **Social proof musi być aktualny** — sprawdź w BRAIN jakie projekty Kacper aktualnie realizuje
5. **Ton: ekspert, nie sprzedawca** — LinkedIn DM to budowanie relacji, nie pitch
6. **Compliance z RODO** — nie zbieraj/przechowuj prywatnych danych kontaktowych (email prywatny, telefon) bez zgody
7. **Max 5-8 firm per sesję** — jakość > ilość
8. **Buying signals zmieniają kolejność** — firma Score B z 3+ sygnałami > firma Score A z 0 sygnałów
