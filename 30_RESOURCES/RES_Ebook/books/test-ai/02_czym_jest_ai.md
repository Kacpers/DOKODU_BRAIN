---
chapter: 2
title: Czym jest AI
subtitle: Od buzzwordu do narzędzia pracy
reading_time: 8 min
---

## Definicja, która ma sens

Zapomnij o filmowych wizjach robotów. Sztuczna inteligencja w biznesie to oprogramowanie, które uczy się z danych i podejmuje decyzje — lub pomaga je podejmować.

:::quote
AI to nie magia — to statystyka na sterydach. Im lepsze dane, tym lepsze wyniki.
--- Kacper Sieradziński
:::

## Jak działa AI w praktyce?

:::process
Dane wejściowe | Dokumenty, emaile, formularze, bazy danych
Przetwarzanie | Model AI analizuje, klasyfikuje, wyciąga informacje
Decyzja | Rekomendacja, klasyfikacja lub automatyczna akcja
Wynik | Raport, odpowiedź, zaktualizowany rekord w CRM
:::

## Historia w pigułce

:::timeline
2020 | GPT-3 | Początek ery generatywnej — pierwsza wersja zdolna do sensownego pisania
2022 | ChatGPT | Demokratyzacja AI — 100M użytkowników w 2 miesiące
2023 | GPT-4 | Enterprise-grade — multimodal, reasoning, tool use
2024 | Agenci AI | Autonomiczne systemy podejmujące decyzje i wykonujące zadania
2026 | AI natywne firmy | Firmy projektowane wokół AI od pierwszego dnia
:::

## Spróbuj sam

:::exercise
Otwórz ChatGPT lub Claude i wpisz następujący prompt:

"Przeanalizuj ten tekst i wyciągnij 3 kluczowe informacje: [wklej dowolny artykuł]"

Zwróć uwagę na:
1. Jakość wyciągniętych informacji
2. Czy AI poprawnie zidentyfikowało najważniejsze punkty
3. Ile czasu zaoszczędziłeś vs manualna analiza
:::

## Prosty przykład kodu

:::code python
from anthropic import Anthropic

client = Anthropic()
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Czym jest AI?"}]
)
print(response.content[0].text)
:::

## Czy AI jest dla mojej firmy?

:::decision
Czy masz powtarzalne procesy, które zajmują >2h tygodniowo?
TAK | AI może je zautomatyzować — zacznij od rozdziału 3
NIE | Skup się na identyfikacji procesów — użyj checklisty z rozdziału 3
:::

:::summary
AI to oprogramowanie uczące się z danych, nie magia z filmów
W praktyce: dane → model → decyzja → wynik
Historia AI przyspieszyła dramatycznie od 2020
Nawet prosty prompt może zaoszczędzić godziny pracy
:::
