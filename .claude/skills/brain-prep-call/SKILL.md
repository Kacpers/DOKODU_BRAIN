---
name: brain-prep-call
description: Przygotowuje strategię na discovery call / spotkanie z klientem — ładuje profil, generuje pytania discovery, identyfikuje buying signals, planuje przebieg rozmowy. Trigger: "przygotuj się na call", "prep call", "przed spotkaniem", "strategia rozmowy", /brain-prep-call
---

# Call Prep Assistant — Dokodu Edition

Przygotowuje kompleksowa strategie przed spotkaniem z klientem. Laduje kontekst z BRAIN, analizuje sytuacje, generuje spersonalizowane pytania i plan rozmowy.

## KIEDY UZYWAC

- Przed discovery call z nowym leadem
- Przed spotkaniem statusowym z klientem
- Przed upsell rozmowa
- Przed QBR (Quarterly Business Review) z klientem po wdrozeniu

## KIEDY NIE UZYWAC

- Po spotkaniu — uzyj `/brain-meeting-notes`
- Do pisania oferty — uzyj `/brain-new-offer`
- Do dodania leada — uzyj `/brain-add-lead`
- Do researchu firmy — uzyj `/brain-lead-research`

## PROCES

### KROK 1: Wczytaj kontekst

Zapytaj: **"Z kim masz spotkanie? (firma + typ: discovery / status / upsell / QBR)"**

Nastepnie zaladuj z BRAIN:
- `/home/kacper/DOKODU_BRAIN/20_AREAS/AREA_Customers/<Klient>/<Klient>_Profile.md` (jezeli istnieje)
- `/home/kacper/DOKODU_BRAIN/20_AREAS/AREA_Customers/<Klient>/<Klient>_Meetings.md` (historia spotkan)
- `/home/kacper/DOKODU_BRAIN/20_AREAS/AREA_Customers/<Klient>/<Klient>_Opportunities.md` (pipeline)
- `/home/kacper/DOKODU_BRAIN/20_AREAS/AREA_Marketing_Sales/CRM_Leady_B2B.md` (status leada)
- `/home/kacper/DOKODU_BRAIN/30_RESOURCES/RES_Sales_Playbook/Sales_Playbook.md` (ICP, cennik, metodologia)

Jezeli katalog klienta nie istnieje:
1. Sprawdz CRM (`CRM_Leady_B2B.md`) — moze lead jest tam
2. Sprawdz pliki Lead_Qualification w `20_AREAS/AREA_Marketing_Sales/`
3. Jezeli brak danych — zapytaj Kacpra o podstawowe informacje (branza, wielkosc, kontekst)

### KROK 2: Analiza sytuacji

Wygeneruj analiza sytuacyjna:

```
═══ PREP: [Firma] — [Typ spotkania] ═══

PROFIL FIRMY:
- Branza: [X] | Wielkosc: [X prac.] | ICP fit: [✅/⚠️/❌ + dlaczego]
- Znane systemy: [Microsoft/Google/inne]
- Historia z Dokodu: [nowy lead / po discovery / po wdrozeniu]

ZNANE BOLE:
1. [bol z profilu/notatek]
2. [bol z ogloszen/researchu]

BUYING SIGNALS (sygnaly zakupowe):
- [✅/❌] Zatrudniaja na stanowiska tech/IT
- [✅/❌] Zmiana w C-suite (nowy CTO/COO)
- [✅/❌] Wspominali budzet/timeline
- [✅/❌] Sami sie odezwali (inbound)
- [✅/❌] Wzrost/ekspansja firmy
- [✅/❌] Problemy z compliance (AI Act, RODO)

POTENCJALNA OFERTA:
→ [Rekomendowany tier z cennika: warsztat / szkolenie / wdrozenie MVP / kompleksowe]
→ Widelki: [X — Y PLN]
```

### KROK 3: Pytania discovery (framework)

Wygeneruj 8-12 pytan spersonalizowanych pod firme i typ spotkania.

**Dla DISCOVERY — framework SPIN + Gap Selling:**

SYTUACJA (Situation):
- "Jak obecnie wyglada proces [X] u Was?"
- "Ile osob jest zaangazowanych?"
- "Jakich narzedzi uzywacie?"

PROBLEM:
- "Co Was najbardziej boli w [proces]?"
- "Ile czasu/pieniedzy to kosztuje miesiecznie?"
- "Jak czesto zdarzaja sie bledy?"

IMPLIKACJA:
- "Co sie stanie jesli tego nie zmienicie w ciagu 6 miesiecy?"
- "Jak to wplywa na [inne dzialy / klientow]?"

NEED-PAYOFF:
- "Gdybyscie mogli to zautomatyzowac — co by to zmienilo?"
- "Jaki wynik bylby dla Was sukcesem?"

BANT+ KWALIFIKACJA (wplataj naturalnie, nie pytaj wprost):
- Budget: "Macie zarezerwowany budzet na ten temat?"
- Authority: "Kto oprocz Pana/Pani bedzie decydowal?"
- Need: "Co jest teraz priorytetem #1?"
- Timeline: "Kiedy chcielibyscie miec to wdrozone?"
- Pain: "Co Was sklonilo zeby teraz sie tym zajac?"

**Dla STATUS:**
- "Co sie zmienilo od ostatniego spotkania?"
- "Jak team przyjmuje [wdrozone rozwiazanie]?"
- "Jaki feedback od uzytkownikow?"
- "Czy pojawialy sie jakies problemy techniczne?"

**Dla UPSELL:**
- "Jak dziala [poprzednie wdrozenie]?"
- "Jakie inne procesy Was bola?"
- "Czy pojawily sie nowe potrzeby?"
- "Jak oceniacie ROI z dotychczasowej wspolpracy?"

**Dla QBR:**
- "Jakie KPI sledzicie od wdrozenia?"
- "Czy ROI jest zgodny z oczekiwaniami?"
- "Jakie cele na nastepny kwartal?"
- "Co mozemy zrobic lepiej jako partner?"

### KROK 4: Strategia rozmowy

```
PLAN ROZMOWY (45 min):
═══════════════════════

0-5 min   │ Small talk + agenda
5-15 min  │ Pytania SYTUACJA + PROBLEM
15-25 min │ IMPLIKACJA + NEED-PAYOFF
25-35 min │ Nasze podejscie (bez ceny!)
35-40 min │ Nastepne kroki + timeline
40-45 min │ Pytania klienta

RED FLAGS do obserwowania:
⚠️ [specyficzne dla tej firmy/branzy]
⚠️ [np. "brak decydenta na callu", "mowia o budzecie ponizej minimum"]

GOLDEN PHRASES (do uzycia):
💡 "[fraza dopasowana do branzy klienta]"
💡 "[social proof: aktualny klient/projekt z BRAIN]"

NIE MOW:
🚫 Nie mow o cenie na discovery — to na propozycje
🚫 Nie mow "automatyzacja" — mow "odciazenie zespolu"
🚫 Nie mow "AI" zbyt wczesnie — mow "rozwiazanie"
```

Dla STATUS/UPSELL/QBR dostosuj plan czasowy odpowiednio.

### KROK 5: Output

Wyswietl wszystko w ustrukturyzowanym formacie. Na koncu zapytaj:

**"Chcesz cos doprecyzowac przed callem?"**

## ZASADY JAKOSCI

1. Pytania MUSZA byc spersonalizowane pod firme/branze — zero generycznych
2. Zawsze sprawdz historie w Meetings.md — nie pytaj o rzeczy ktore klient juz mowil
3. Social proof musi byc aktualny — sprawdz aktywne projekty w BRAIN
4. Rekomendacja oferty musi byc zgodna z cennikiem z Sales Playbook
5. Red flags musza byc specyficzne, nie generyczne
6. Przy QBR/upsell — przygotuj dane z wdrozenia (jezeli sa w BRAIN)
7. Zasada Vesper: jezeli scope wyglada na weekend-work — flaguj od razu
8. Nie generuj pytan na ktore juz znasz odpowiedz z profilu klienta
