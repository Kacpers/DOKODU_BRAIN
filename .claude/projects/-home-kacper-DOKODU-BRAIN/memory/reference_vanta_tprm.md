---
name: Vanta i Third Party Risk Management
description: Wiedza o TPRM/Vanta — aktywuj gdy klient pyta o compliance dostawców, zarządzanie ryzykiem vendorów, SOC 2, ISO 27001
type: reference
---

## Czym jest TPRM (Third Party Risk Management)

Proces zarządzania ryzykiem dostawców zewnętrznych — klasyfikacja vendorów wg poziomu ryzyka, zbieranie certyfikatów (SOC 2, ISO 27001, PCI DSS), cykliczne audyty.

## Vanta jako narzędzie

- Automatyzuje compliance — po wrzuceniu dokumentów dostawcy (certyfikaty, raporty audytowe) nadaje poziom ryzyka
- AI analizuje PDFy i raporty audytowe, skraca czas weryfikacji
- Portal dla dostawców do przesyłania dowodów bezpieczeństwa
- Automatyczne alerty o wygasających certyfikatach
- Gotowe szablony kwestionariuszy (SIG Lite, SOC 2)
- Ograniczenia: nie obsługuje niektórych typów plików, może błędnie sklasyfikować dostawcę

## Jak to się ma do Dokodu

- **Dokodu NIE wdraża Vanty** — to nie nasza usługa
- **"Zgodnie z prawem" w Dokodu = AI Act + RODO**, nie TPRM
- Vanta jest po drugiej stronie stołu — narzędzie dla firm sprawdzających swoich dostawców (w tym potencjalnie nas)
- **Kiedy aktywować:** gdy klient 200+ osób mówi o problemach z zarządzaniem dostawcami, compliance vendorów, audytach — wspomnieć o Vancie jako rekomendacja (consulting, nie wdrożenie)
- **Styk z Dokodu:** jeśli klient chce automatycznie wyciągać dane z certyfikatów PDF i wrzucać do systemu — to jest n8n + AI workflow, który umiemy budować

## Źródło

Opis od Piotra (klient Dokodu), kwiecień 2026. Kroki wdrożenia: inwentaryzacja vendorów → matryca krytyczności → kwestionariusze → portal współpracy → workflow akceptacji → monitoring ciągły.
