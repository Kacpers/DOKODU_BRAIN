---
n: "05"
title: "Wywiad: jak NovaLogistics odzyskał 4h tygodniowo"
abstract: "6 tygodni, 240 osób, 38% mniej czasu na raporty. Rozmowa z CFO Magdaleną Wiśniewską."
reading_time: "14 min"
level: "Podstawowy"
sections: "5.1 – 5.3"
kicker: "Wywiad · Case 05 / 12"
meta:
  company: "NovaLogistics sp. z o.o."
  industry: "Logistyka"
  team_size: 240
  interviewee:
    name: "Magdalena Wiśniewska"
    role: "CFO"
  rollout_weeks: 6
  tools: "M365 Copilot + n8n + własny pipeline raportujący"
---

<!-- template: chapter -->
# Wywiad: jak NovaLogistics odzyskał 4h tygodniowo

**Abstrakt:** Magdalena Wiśniewska, CFO NovaLogistics (240 osób, logistyka kontraktowa), prowadziła pilot z Dokodu w I kw. 2026. Pierwotnie 8 tygodni — skończyli w 6. Co zrobili inaczej?

---

<!-- template: case -->
## 5.1 Wywiad

> "Największą zmianą nie była technologia, tylko **nawyk**."
> — Magdalena Wiśniewska

---

**DK — Dokodu:** Jak wyglądał pierwszy dzień po uruchomieniu agenta?

**MW:** Nudno. Dosłownie — nikt nie zauważył. Raport poszedł rano do zarządu, tak jak zwykle w pierwszy poniedziałek miesiąca. Nikt nie pytał, skąd się wziął. To był pierwszy moment, kiedy zrozumiałam, że się udało.

**DK:** Dlaczego cisza oznacza sukces?

**MW:** Bo raport miesięczny od zawsze był okazją do interwencji. Jak nie pasowały liczby, ktoś pisał do mnie: *"Kasia, sprawdź jeszcze segment X".* Kiedy to robił AI i ja miałam go tylko zaakceptować — liczby były spójne, bo nikt nie rozciągał deadline'u o 3 dni żeby "doprecyzować wykresy". Zarząd dostał raport punktualnie, bez drobnych niezgodności, bez dosyłania korekt. Nie chwaliłam się, że to AI. I nie musiałam.

**DK:** Które procesy zostały zautomatyzowane najpierw?

**MW:** Tylko konsolidacja raportu miesięcznego. Świadomie jeden. Kacper na pierwszym spotkaniu powiedział: *"Jeśli chcecie dziesięć rzeczy, wybierzcie jedną"*. Denerwowało mnie to wtedy — wiedziałam, że mamy takich miejsc ze dwadzieścia. Ale w szóstym tygodniu zrozumiałam, dlaczego. Nie mieliśmy czasu i energii na więcej, a ta jedna sprawa pochłonęła nam trzy osoby przez dwa miesiące.

**DK:** Dlaczego zdążyliście w 6 tygodni zamiast 8?

**MW:** Dwa powody. Pierwszy — właścicielem procesu była osoba, która siedziała nad raportem od trzech lat, więc widziała dokładnie, gdzie są bóle. Drugi — zarząd zaakceptował, że pierwszy miesiąc raport będzie *brzydszy* niż wcześniej. To odebrało presję na perfekcję w tygodniu czwartym. Zwalniało to nam ręce na testowanie.

---

## 5.2 Metryki

| Metryka | Przed | Po | Zmiana |
|---|---|---|---|
| Czas przygotowania raportu miesięcznego | 8 h | 1.5 h | −81% |
| Liczba korekt po pierwszej wersji | 4.2 średnio | 0.6 średnio | −86% |
| Ludzie zaangażowani | 3 | 1 | −67% |
| Opóźnienia vs deadline zarządu | 1.5 dnia | 0 dni | — |

Czas odzyskany przez zespół: **około 4h tygodniowo**, wyłącznie w kontekście tego procesu. Co zrobiliśmy z odzyskanym czasem? Nie zwolniliśmy nikogo. Analitycy przesunęli się w stronę analiz ad hoc dla działu operacyjnego, co dało kolejne 60 tys. PLN oszczędności w następnym kwartale — ale to już inny case study.

---

<!-- template: image -->
## 5.3 Pull-quote

> "Wdrożyliśmy AI i zwolniliśmy… **Excela**."
> — Magdalena Wiśniewska, CFO NovaLogistics

*Fotografia: open placeholder — rekomendowane zdjęcie zespołu finansów NovaLogistics w biurze, tonacja chłodna, low-sat. Format 1240×1754 px, full bleed.*

---

<!-- template: standard -->
## 5.4 Lessons learned (z perspektywy Dokodu)

Co było inne w NovaLogistics względem typowego pilota:

1. **Właściciel procesu = osoba robiąca go od 3 lat.** W większości firm właścicielem jest nowy manager, który "ma ogarnąć". Tam to była osoba z najgłębszym kontekstem. Skróciło to tydzień 7 o 5 dni.

2. **Zarząd świadomie obniżył wymagania na miesiąc 1.** To jest najczęściej pomijany krok. Jeśli zarząd wymaga "jakości jak zwykle od dnia pierwszego", pilot padnie.

3. **Zespół nie dowiedział się, że to AI.** Brzmi kontrowersyjnie, ale było świadome. Przed pilotem zarząd komunikował: *"Pracujemy nad sprawniejszym raportowaniem"*. Dopiero po miesiącu 2. pokazaliśmy, jak to działa. Efekt: zero oporu, bo nie było z czym walczyć.

Trzeci punkt nie pasuje do każdej firmy. Omawiamy go szczegółowo w rozdziale 6, w kontekście rolloutu.
