---
type: resource
status: active
owner: alina
last_reviewed: 2026-03-06
tags: [legal, ai-act, compliance, EU, wytyczne]
related: [[AI_Act_Tracker]], [[RODO_Checklist]]
---

# AI ACT — NOTATKI ROBOCZE
> Zyjacy dokument. Tu trafiaja surowe notatki z lektury, konsultacji, webinarow.
> Nie jest to finalny dokument prawny — to baza do pracy Aliny i Kacpra.
> Zrodla: EUR-Lex, European AI Office, UODO, LexLegali, EROD wytyczne.

---

## STRUKTURA ROZPORZĄDZENIA (mapa orientacyjna)

```
Rozporzadzenie EU 2024/1689 (AI Act)
│
├── Art. 1-4:    Zakres, definicje (co to jest "system AI"?)
├── Art. 5:      Zakazy (unacceptable risk) — obowiazuje od 02.2025
├── Art. 6-51:   Systemy wysokiego ryzyka (high-risk)
│   ├── Art. 6:  Klasyfikacja
│   ├── Art. 9:  Zarzadzanie ryzykiem
│   ├── Art. 10: Dane i zarzadzanie danymi
│   ├── Art. 11: Dokumentacja techniczna
│   ├── Art. 13: Przejrzystosc
│   ├── Art. 14: Nadzor ludzki
│   └── Art. 15: Dokladnosc i solidnosc
├── Art. 50:     Obowiazki przejrzystosci (chatboty, deepfakes)
├── Art. 52-56:  GPAI (modele ogolnego przeznaczenia — GPT, Claude, Gemini)
├── Art. 57-68:  Zarzadzanie i egzekwowanie
├── Art. 71:     Kary (do 35 mln EUR lub 7% globalnego obrotu)
└── Aneks I-IX:  Techniczne, listy sektorow wysokiego ryzyka, etc.
```

---

## DEFINICJE KLUCZOWE (Art. 3)

**"System AI"** (def. minimalistyczna po poprawkach):
> Maszynowy system zaprojektowany do dzialania z rozna autonomia, ktory na podstawie danych wejsciowych — dla zbioru celow okreslonych przez czlowieka — generuje wyjscia takie jak prognozy, rekomendacje, decyzje lub tresci, ktore moga wplywac na srodowiska fizyczne lub wirtualne.

**Praktyczna implikacja dla Dokodu:**
- Prosty workflow n8n bez modelu AI = NIE jest systemem AI wg definicji → brak wymogów AI Act
- Workflow n8n z GPT-4o/Claude/Gemini = JEST systemem AI → klasyfikacja wymagana
- Chatbot regexowy = NIE jest systemem AI
- Chatbot LLM-based = JEST systemem AI → obowiazek przejrzystosci (Art. 50)

---

## ART. 5 — ZAKAZY (od 02.2025)

Czego NIE mozna wdrazac (i czego Dokodu nigdy nie zrobi):

| Zakaz | Przyklad |
| :--- | :--- |
| Social scoring przez władze publiczne | Ocenianie obywateli na podstawie zachowania |
| Biometryczna identyfikacja RT w miejscach publicznych | Kamery z rozpoznawaniem twarzy w czasie rzeczywistym |
| Manipulacja podswiadoma | AI ktore wpływa na decyzje bez swiadomosci uzytkownika |
| Eksploatacja podatnosci (wiek, niepelnosprawnosc) | Targetowanie reklam do uzaleznionej mlodziezy |
| Przewidywanie przestepstw na podstawie samego profilowania | "Predictive policing" bez faktycznych dowodow |

**Nota praktyczna:** Klasyczne use cases Dokodu (parser faktur, agent BOK, kalkulator ROI, chatbot support) NIE wchodza w te zakazy.

---

## ART. 6 + ANEKS III — HIGH-RISK AI (od 08.2026)

Sektory wysokiego ryzyka (Aneks III) — zaznaczone te, gdzie Dokodu moze pracowac:

| Sektor | Przyklady | Ryzyko dla Dokodu? |
| :--- | :--- | :---: |
| Infrastruktura krytyczna | Energia, woda, transport | Niskie |
| Edukacja | Ocenianie, rekrutacja do szkol | Srednie (HRtech) |
| **Zatrudnienie i HR** | **Screening CV, monitoring pracownikow** | **UWAGA — TAK** |
| Uslugi publiczne | Ocena zdolnosci kredytowej, swiadczenia | Niskie |
| Prawo | Analiza dowodow, decyzje sadowe | Niskie |
| Bezpieczenstwo osob | Maszyny, pojazdy autonomiczne | Srednie (produkcja) |
| Migracja | Ocena ryzyka azylantow | Niskie |
| Wymiar sprawiedliwosci | Analiza ryzyka recydywy | Niskie |

**KLUCZOWE dla projektow HR-tech:**
Jezeli klient wdraза AI do screeningu CV lub oceny pracownikow → AUTOMATYCZNIE high-risk → pelne wymogi art. 9-15 + rejestracja EU AI Database.

---

## ART. 50 — PRZEJRZYSTOSC (CHATBOTY)

Obowiazuje dla KAZDEGO chatbota/agenta AI ktory wchodzi w interakcje z uzytkownikiem.

**Wymogi:**
1. Uzytkownik MUSI byc poinformowany ze rozmawia z AI (nie czlowiekiem)
2. Jezeli system generuje audio/video/obraz/tekst syntetyczny → oznaczenie jako "AI-generated"
3. Deepfakes muszą byc wyraznie oznaczone
4. Wyjatki: systemy oczywiscie artystyczne, satyryczne, z wyraźną ludzką kontrola

**Implementacja techniczna w Dokodu:**
```
Standardowy komunikat poczatkowy chatbota:
"Jestem asystentem AI firmy [KLIENT]. Moge pomoc Ci z [ZAKRES].
Pamietaj, ze jestem programem komputerowym — w pilnych lub skomplikowanych
sprawach mozesz poprosic o kontakt z czlowiekiem wpisujac 'Chce rozmawiac z konsultantem'."
```

---

## ART. 52-56 — GPAI (GENERAL PURPOSE AI)

Dotyczy dostawcow modeli (OpenAI, Anthropic, Google, Mistral) — NIE bezposrednio uzytkownikow.

**Ale Dokodu musi wiedziec:**
- Dostawcy GPAI musza udostepniac dokumentacje techniczna developerom (nam)
- Musimy uwzglednic ograniczenia modelu w dokumentacji dla klienta
- Modele GPAI "systemowego ryzyka" (ponad 10^25 FLOPs treningowych) maja dodatkowe wymogi → oznacza to GPT-4, Claude 3+, Gemini Ultra

---

## KARY I EGZEKWOWANIE (Art. 71)

| Naruszenie | Maksymalna kara |
| :--- | ---: |
| Naruszenie zakazow (Art. 5) | 35 000 000 EUR lub 7% globalnego obrotu |
| Naruszenie wymogów high-risk | 15 000 000 EUR lub 3% globalnego obrotu |
| Nieprawdziwe informacje dla organow | 7 500 000 EUR lub 1,5% globalnego obrotu |

**Dla MŚP:** Kary sa proporcjonalne do wielokosci firmy — ale ryzyko reputacyjne jest takie samo.

---

## WYTYCZNE EROD I INTERPRETACJE

### Pytania bez ostatecznej odpowiedzi (monitorowac)
- Jak dokladnie klasyfikowac "asystenta AI" ktory tylko podpowiada (nie decyduje)?
- Kiedy "human-in-the-loop" jest wystarczajacy dla high-risk?
- Czy integracja AI w istniejace oprogramowanie tworzy nowy "system AI"?
- Jak liczyc progi GPAI dla modeli fine-tunowanych?

### Orzecznictwa i decyzje (uzupelniaj na biezaco)
- [data] [organ] [temat] — [link/notatka]
-

---

## NOTATKI Z KONSULTACJI

### Konsultacja z Marcinem (LexLegali) — [data do uzupelnienia]
- Temat: webhoki i odpowiedzialnosc za przetwarzanie danych
- Kluczowy wniosek: webhok jako kanał transmisji = odpowiedzialnosc lezy po stronie nadawcy danych
- Implikacja dla Dokodu: Corleonis odpowiada za dane ktore wysyla do n8n; Dokodu odpowiada za przetwarzanie
- Akcja: zaktualizowac klauzule umowne → Alina

### Webinar European AI Office — [data do uzupelnienia]
- Temat: implementacja Art. 13 (przejrzystosc)
- Kluczowy wniosek:
- Akcja:

---

## LINKI I ZRODLA

- Pelny tekst AI Act (PL): https://eur-lex.europa.eu/legal-content/PL/TXT/?uri=CELEX:32024R1689
- European AI Office: https://digital-strategy.ec.europa.eu/en/policies/ai-office
- UODO — wytyczne AI: https://uodo.gov.pl (szukaj: sztuczna inteligencja)
- EROD (EDPB) Wytyczne AI: https://www.edpb.europa.eu (Opinion 28/2024)
- AI Act Explorer (nieoficjalny, wygodny): https://artificialintelligenceact.eu

---

*Uzupelniaj na biezaco. Oznacz [NOWE] przy swiezych notatkach. Archiwizuj stare interpretacje gdy sa juz potwierdzone.*
