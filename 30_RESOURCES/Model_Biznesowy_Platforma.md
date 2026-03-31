---
type: resource
created: 2026-03-30
tags: [platforma, model-biznesowy, feed, kursy, subskrypcja, monetyzacja]
---

# Model Biznesowy Platformy Dokodu — Ustalenia 2026-03-30

## Kontekst

Rozmowa o tym jak ułożyć monetyzację platformy (feed + kursy + subskrypcje). Decyzje podjęte wspólnie z Kacprem.

---

## Kluczowe Decyzje

### 1. Subskrypcja — UKRYTA na teraz
- Brak regularnego contentu w feedzie — nie uzasadnia recurring payment
- Kod zostaje, ale UI subskrypcji ukrywamy
- Wróci gdy: regularny content + większa baza kursantów

### 2. Kursy — jednorazowy zakup (CORE model)
Trzy kursy: **Pystart**, **Skumajbazy**, **n8n** (planowany)
- Jednorazowa opłata
- 365 dni dostępu
- Po wygaśnięciu: blokada lekcji + postów kursu → możliwość odnowienia
- Mini-kursy / tanie produkty na przyszłość (entry point do większych)

### 3. Feed — dwa tiery

| Tier | Kto | Co widzi |
|------|-----|----------|
| **Darmowy** | Każdy z kontem (np. z YouTube) | Posty publiczne: prompty, pliki z YT, materiały do pobrania, podgląd kursów. **BEZ wideo Vimeo** (oszczędność transferu) |
| **Kursant** | Kupił kurs | Posty publiczne + posty tagowane do jego kursu/kursów |

- Feed tagowany per kurs
- Kursant Pystart widzi: publiczne + Pystart
- Kursant Pystart + Skumajbazy widzi: publiczne + oba
- Po wygaśnięciu 365 dni → wraca do darmowego (traci posty kursu)

### 4. Funnel klienta

```
YouTube/Social → Darmowe konto → Widzi wartość (prompty, pliki, samplerki)
                                        ↓
                              Kupuje kurs (jednorazowo, 365 dni)
                                        ↓
                              Lekcje + feed kursu + upselling kolejnych
                                        ↓
                              Wygasa → odnawia LUB wraca do darmowego
```

### 5. Mini-kursy (PRZYSZŁOŚĆ)
- Małe, tanie kursy jako entry point
- Promocje / bundle z większymi kursami
- Szczegóły do ustalenia — Kacper myśli nad konceptem

---

## Co wymaga implementacji w kodzie

- Tagowanie postów w feedzie per kurs (relacja Post ↔ Course)
- Filtrowanie feedu wg kupionych kursów
- Ukrycie wideo Vimeo dla darmowych kont
- Ukrycie UI subskrypcji
- Flow odnowienia dostępu (wygasł → kup ponownie → odblokuj)
- Upselling w feedzie dla zalogowanych

---

*Pełna specyfikacja techniczna: `STRONA/Dokodu_nextjs/docs/BUSINESS_MODEL_2026-03-30.md`*
