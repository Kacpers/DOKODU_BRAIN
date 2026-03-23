---
type: resource
status: active
owner: kacper
last_reviewed: 2026-03-06
tags: [n8n, schema, faktury, ekstrakcja, json]
related: [[300_BIBLIOTEKA_PROMPTOW]], [[N8N_Blueprints]]
---

# SCHEMA: Faktura v1
> Uzywany w: PROMPT-001 (Ekstrakcja danych PDF), BP-003 (Document Parser)
> Wersja: 1.0 | Jezyk: JSON Schema (Draft-07)
> Walidowany przez: Code Node w n8n

---

## JSON SCHEMA (pelna definicja)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://dokodu.it/schemas/faktura-v1.json",
  "title": "Faktura",
  "description": "Schema dla faktury VAT zgodnej z polskim prawem podatkowym",
  "type": "object",
  "required": [
    "numer_faktury",
    "data_wystawienia",
    "sprzedawca",
    "nabywca",
    "pozycje",
    "suma_brutto",
    "waluta"
  ],
  "properties": {
    "numer_faktury": {
      "type": "string",
      "description": "Numer faktury wg numeracji sprzedawcy",
      "examples": ["FV/2026/03/001", "2026/03/FV/001"]
    },
    "data_wystawienia": {
      "type": "string",
      "format": "date",
      "description": "Data wystawienia faktury (YYYY-MM-DD)"
    },
    "data_sprzedazy": {
      "type": ["string", "null"],
      "format": "date",
      "description": "Data dokonania lub zakończenia dostawy/usługi (jesli inna od wystawienia)"
    },
    "data_platnosci": {
      "type": ["string", "null"],
      "format": "date",
      "description": "Termin platnosci"
    },
    "sprzedawca": {
      "type": "object",
      "required": ["nazwa", "nip"],
      "properties": {
        "nazwa": { "type": "string" },
        "nip": {
          "type": "string",
          "pattern": "^[0-9]{10}$",
          "description": "NIP bez kresek, 10 cyfr"
        },
        "adres": { "type": ["string", "null"] },
        "nip_valid": {
          "type": "boolean",
          "description": "Wynik walidacji sumy kontrolnej NIP"
        }
      }
    },
    "nabywca": {
      "type": "object",
      "required": ["nazwa"],
      "properties": {
        "nazwa": { "type": "string" },
        "nip": {
          "type": ["string", "null"],
          "pattern": "^[0-9]{10}$"
        },
        "adres": { "type": ["string", "null"] },
        "nip_valid": { "type": ["boolean", "null"] }
      }
    },
    "pozycje": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["opis", "wartosc_netto", "stawka_vat", "wartosc_brutto"],
        "properties": {
          "lp": { "type": ["integer", "null"] },
          "opis": { "type": "string" },
          "ilosc": { "type": ["number", "null"] },
          "jm": {
            "type": ["string", "null"],
            "description": "Jednostka miary (szt., kg, h, etc.)"
          },
          "cena_netto": { "type": ["number", "null"] },
          "stawka_vat": {
            "type": "string",
            "enum": ["23%", "8%", "5%", "0%", "ZW", "NP", "__NIECZYTELNE__"],
            "description": "Stawka VAT. ZW = zwolniony, NP = nie podlega"
          },
          "wartosc_netto": { "type": "number" },
          "wartosc_vat": { "type": ["number", "null"] },
          "wartosc_brutto": { "type": "number" },
          "pkwiu": {
            "type": ["string", "null"],
            "description": "Kod PKWiU jesli podany"
          }
        }
      }
    },
    "podsumowanie_vat": {
      "type": ["array", "null"],
      "description": "Podsumowanie per stawka VAT",
      "items": {
        "type": "object",
        "properties": {
          "stawka": { "type": "string" },
          "podstawa": { "type": "number" },
          "kwota_vat": { "type": "number" },
          "brutto": { "type": "number" }
        }
      }
    },
    "suma_netto": { "type": ["number", "null"] },
    "suma_vat": { "type": ["number", "null"] },
    "suma_brutto": { "type": "number" },
    "waluta": {
      "type": "string",
      "default": "PLN",
      "examples": ["PLN", "EUR", "USD"]
    },
    "kurs_waluty": {
      "type": ["object", "null"],
      "description": "Kurs jezeli faktura nie jest w PLN",
      "properties": {
        "kurs": { "type": "number" },
        "data_kursu": { "type": "string", "format": "date" },
        "tabela_nbp": { "type": ["string", "null"] }
      }
    },
    "metoda_platnosci": {
      "type": ["string", "null"],
      "examples": ["przelew", "gotowka", "karta"]
    },
    "numer_konta": {
      "type": ["string", "null"],
      "description": "Numer rachunku bankowego sprzedawcy"
    },
    "uwagi": { "type": ["string", "null"] },
    "typ_dokumentu": {
      "type": "string",
      "enum": ["FAKTURA_VAT", "FAKTURA_KORYGUJACA", "FAKTURA_ZALICZKOWA", "FAKTURA_KONCOWA", "INNE"],
      "default": "FAKTURA_VAT"
    },
    "faktura_korygowana": {
      "type": ["string", "null"],
      "description": "Numer faktury korygowanej (jezeli to korekta)"
    },
    "_meta": {
      "type": "object",
      "description": "Metadane ekstrakcji — nie jest czescia faktury",
      "properties": {
        "confidence": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "description": "Pewnosc modelu AI (0-1)"
        },
        "parser_version": { "type": "string" },
        "extracted_at": { "type": "string", "format": "date-time" },
        "source_filename": { "type": "string" },
        "warnings": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Lista ostrzezen parsera (nieczytelne pola, niespojnosci)"
        },
        "validation_errors": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Lista bledow walidacji (NIP, sumy)"
        }
      }
    }
  }
}
```

---

## WALIDATOR NIP (JavaScript — n8n Code Node)

```javascript
/**
 * Walidacja sumy kontrolnej NIP (Numer Identyfikacji Podatkowej)
 * Algorytm: waga [6,5,7,2,3,4,5,6,7], reszta z dzielenia przez 11
 */
function validateNIP(nip) {
  if (!nip) return null;

  // Usun znaki niebedace cyframi
  const cleanNip = String(nip).replace(/[^0-9]/g, '');

  // Sprawdz dlugosc
  if (cleanNip.length !== 10) return false;

  // Wagi
  const weights = [6, 5, 7, 2, 3, 4, 5, 6, 7];

  // Oblicz sume kontrolna
  const sum = weights.reduce((acc, weight, idx) => {
    return acc + (weight * parseInt(cleanNip[idx]));
  }, 0);

  const checkDigit = sum % 11;

  // Cyfra kontrolna nie moze byc 10
  if (checkDigit === 10) return false;

  return checkDigit === parseInt(cleanNip[9]);
}

// Uzycie w Code Node:
const invoice = $input.item.json;

if (invoice.sprzedawca?.nip) {
  invoice.sprzedawca.nip_valid = validateNIP(invoice.sprzedawca.nip);
}
if (invoice.nabywca?.nip) {
  invoice.nabywca.nip_valid = validateNIP(invoice.nabywca.nip);
}

// Walidacja sum
const obliczoneBrutto = invoice.pozycje?.reduce((sum, p) => sum + (p.wartosc_brutto || 0), 0);
const roznicaBrutto = Math.abs((obliczoneBrutto || 0) - (invoice.suma_brutto || 0));

if (roznicaBrutto > 0.05) { // tolerancja 5 groszy na bledy zaokraglen
  invoice._meta = invoice._meta || {};
  invoice._meta.warnings = invoice._meta.warnings || [];
  invoice._meta.warnings.push(
    `Niespójnosc sum: obliczone ${obliczoneBrutto?.toFixed(2)}, na fakturze ${invoice.suma_brutto}`
  );
}

return invoice;
```

---

## PRZYKLADOWE WYJSCIE (valid invoice)

```json
{
  "numer_faktury": "FV/2026/03/042",
  "data_wystawienia": "2026-03-06",
  "data_platnosci": "2026-03-20",
  "sprzedawca": {
    "nazwa": "Przykladowa Sp. z o.o.",
    "nip": "5882473305",
    "adres": "ul. Przykladowa 1, 84-230 Rumia",
    "nip_valid": true
  },
  "nabywca": {
    "nazwa": "Klient Sp. z o.o.",
    "nip": "1234567890",
    "adres": "ul. Klienta 5, 80-001 Gdansk",
    "nip_valid": false
  },
  "pozycje": [
    {
      "lp": 1,
      "opis": "Szkolenie AI dla zespolu (1 dzien)",
      "ilosc": 1,
      "jm": "usł.",
      "cena_netto": 10000.00,
      "stawka_vat": "23%",
      "wartosc_netto": 10000.00,
      "wartosc_vat": 2300.00,
      "wartosc_brutto": 12300.00
    }
  ],
  "suma_netto": 10000.00,
  "suma_vat": 2300.00,
  "suma_brutto": 12300.00,
  "waluta": "PLN",
  "metoda_platnosci": "przelew",
  "typ_dokumentu": "FAKTURA_VAT",
  "_meta": {
    "confidence": 0.97,
    "parser_version": "1.0",
    "extracted_at": "2026-03-06T10:30:00Z",
    "source_filename": "faktura_042.pdf",
    "warnings": [],
    "validation_errors": []
  }
}
```

---

## CHANGELOG

| Wersja | Data | Zmiana |
| :--- | :---: | :--- |
| v1.0 | 2026-03 | Inicjalizacja schema dla projektu Corleonis |
