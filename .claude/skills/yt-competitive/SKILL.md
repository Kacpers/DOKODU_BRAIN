---
name: yt-competitive
description: Pobiera najnowsze filmy z kanałów konkurencji (PL) i trendsetterów (US), identyfikuje tematy do adaptacji dla kanału Kacpra. Bez zużywania API quota — używa RSS. Trigger: "co nowego u konkurencji", "trendy youtube", "co powinienem nagrać", "co wybija w US", /yt-competitive
---

# Instrukcja: Competitive Intelligence YouTube

## Działanie

Śledzi 9 kanałów (4 PL + 5 US), identyfikuje tematy które warto zaadaptować dla polskiej widowni.

## KROK 1: Fetch RSS (bez API)

```bash
cd /home/kacper/DOKODU_BRAIN/scripts && python3 youtube_rss.py --days 14 --save 2>/dev/null
```

## KROK 2: Odczytaj raport i dane z BRAIN

Odczytaj:
- `/home/kacper/DOKODU_BRAIN/30_RESOURCES/RES_YouTube/YT_Competitive.md` — świeży raport
- `/home/kacper/DOKODU_BRAIN/30_RESOURCES/RES_YouTube/YT_Insights.md` — co działa na kanale Kacpra
- `/home/kacper/DOKODU_BRAIN/20_AREAS/AREA_YouTube/AREA_YouTube.md` — pillary i ICP

## KROK 3: Analiza

**Polska konkurencja — pytania:**
- Który film ma >5K wyśw. w ostatnich 14 dniach? → to temat który rynek PL chłonie teraz
- Czy jest temat który nagrało 2+ kanałów PL? → prawdopodobnie trending w niszy
- Czy Kacper ma już film na ten temat? (sprawdź YT_Insights.md i YT_Videos.md)

**US trendsetting — pytania:**
- Filmy z >30K wyśw. w ostatnich 14 dniach → tematy które mają potencjał wiralowy
- Filmy z 10-30K wyśw. → solidne tematy, niższe ryzyko, dobre do adaptacji
- Co z US jeszcze NIE dotarło na PL rynek? → największa okazja

**Adaptacja US → PL (filtr):**
- Czy temat jest zrozumiały dla polskiego B2B (50-500 pracowników)?
- Czy Kacper ma expertise w tym temacie?
- Czy pasuje do pillaru: Tutorial n8n / Local AI / Case study / AI Act?

## KROK 4: Wygeneruj raport

Format:

```
### Competitive Intel — [DATA]

**🔥 NAGRAĆ TERAZ (trending PL):**
- [Temat] — [X kanałów PL nagrało, max wyśw: Xk] — [dlaczego Kacper może zrobić to lepiej/inaczej]

**🇺🇸 ADAPTOWAĆ Z US (potencjał >10K wyśw. na PL):**
- [Tytuł US] ([Xk wyśw.]) → PL adaptacja: "[Proponowany tytuł PL]"
  Dlaczego zadziała: [1 zdanie]

**⏳ OBSERWOWAĆ (za wcześnie lub zbyt niszowe):**
- [Temat] — [powód]

**❌ POMINĄĆ:**
- [Temat] — [dlaczego nie pasuje do kanału/ICP]
```

## KROK 5: Zaproponuj

Po raporcie zaproponuj:
- "Chcesz żebym od razu zrobił `/yt-plan-video` dla najlepszego tematu?"
- "Chcesz oznaczyć filmy do adaptacji w bazie? (zapisuję flagę adapt_flag=1)"

## ZASADY

- Nie rekomenduj tematów które NIE pasują do pillaru Dokodu (AI Act / n8n / local AI / automatyzacja B2B)
- Fireship i Matthew Berman mają bardzo techniczny content — filtruj pod kątem dostępności dla polskiego B2B
- Jeśli konkurent PL opublikował ten sam temat <7 dni temu → "za późno, pomiń lub zrób z innym kątem"
- Zawsze proponuj konkretny polski tytuł, nie tylko temat
