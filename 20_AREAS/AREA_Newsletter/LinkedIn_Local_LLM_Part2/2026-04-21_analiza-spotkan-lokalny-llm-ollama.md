---
title: "Analiza spotkań lokalnym modelem AI — Ollama + Qwen / GPT-OSS"
description: "Postaw lokalny model AI (Ollama + Qwen 3) do analizy spotkań — wyciągnij decyzje, akcje i ryzyka. Bez wysyłania danych do ChatGPT. Krok po kroku."
date: 2026-04-21
slug: analiza-spotkan-lokalnym-modelem-ai-ollama
---

# Spotkanie zostawia po sobie 80 stron tekstu. Nikt tego nie czyta.

*Czyli: jak postawić sobie lokalnego analityka spotkań, który nigdy nie wysyła Twoich rozmów do OpenAI.*

---

Tydzień temu pokazałem Ci, jak zrobić transkrypcję spotkania bez chmury — Whisper, lokalnie, za darmo. Po publikacji dostałem 12 wiadomości z wariantem tego samego pytania:

*"OK, mam transkrypcję. Plik txt. Osiemdziesiąt stron. I co teraz?"*

Słuszne pytanie. Bo transkrypcja to półprodukt. Nikt nie wraca do 80 stron rozmowy żeby znaleźć "co właściwie ustaliliśmy z klientem". Ja na pewno nie wracam.

Naturalna myśl: wkleić to do ChatGPT, powiedzieć "podsumuj". I tu wpadasz dokładnie w ten sam dylemat, który rozwiązaliśmy tydzień temu nagrywając lokalnie. Bo ta transkrypcja — z budżetami klientów, warunkami umów, czasem nazwiskami i danymi — właśnie poleciała na serwery w USA.

Więc dziś druga część. Jak postawić sobie lokalny model AI, który zrobi tę samą robotę co ChatGPT na Twojej transkrypcji — tylko że nigdzie jej nie wyśle.

[OBRAZEK: 01_pipeline.png — Pipeline: transkrypcja → Ollama → model → prompt → notatki]

## Dlaczego nie ChatGPT API albo Claude API?

Bo wracamy do tego samego pytania co w pierwszym poście. Tylko że tym razem jeszcze gorzej — bo do API trafia nie nagranie (z którego trzeba coś jeszcze wyłuskać), tylko gotowy, czysty tekst rozmowy. Zero szumu. Idealnie strawne dane.

[OBRAZEK: 02_comparison.png — ChatGPT/Claude API vs Ollama]

Cztery do jednego dla Ollamy. Konfiguracja przegrywa, ale to nadal jest 15 minut, które robisz raz w życiu.

I uczciwie — jakość polskiego u GPT-4 czy Claude'a jest lepsza niż u lokalnych modeli. Ale "lepsza" tu znaczy: niuanse. Do strukturyzowania notatek ze spotkania (kto co powiedział, jaka decyzja, jakie zadanie) lokalny model 14B w polskim jest aż nadto dobry. Sprawdziłem na siedmiu spotkaniach. Różnicy nie widzę.

## Czym jest Ollama?

Najprościej: **Docker dla modeli językowych**.

Jedna komenda instaluje serwis, który chodzi w tle na Twoim komputerze. Druga komenda pobiera model. Trzecia — uruchamia rozmowę. Cały model siedzi na Twoim dysku, działa offline, nie ma żadnego konta, żadnego abonamentu, żadnego limitu zapytań.

Działa na Macu (Apple Silicon — M1, M2, M3, M4), na Windowsie, na Linuxie. Najlepiej na Macach z układem M-series, bo Apple zrobiło dobrą robotę z Metal Performance Shaders i modele lecą tam zaskakująco szybko.

## Krok 1: Instalacja Ollamy

Na Macu:

```
brew install ollama
ollama serve
```

Na Windowsie pobierasz instalator z ollama.com, klikasz next-next-finish.

Pierwsza komenda instaluje. Druga uruchamia serwis (zostaw to okno otwarte albo skonfiguruj jako usługę systemową — Mac sam to zrobi po pierwszym pobraniu modelu).

To wszystko. Ollama jest gotowa.

## Krok 2: Wybór modelu

Tu mamy realny dylemat. Modeli językowych jest dziś setki, a Ollama dokłada nowe co kilka tygodni. Stan na kwiecień 2026 — biblioteka mogła się znów zmienić w międzyczasie, ale mój sprawdzony zestaw wygląda tak.

Trzy realne opcje na MacBooku Pro:

[OBRAZEK: 03_models.png — Qwen 3 (8B) / Qwen 3.5 (9B) / Qwen 3 (32B)]

**Qwen 3 (8B)** to bezpieczny start. Działa na każdym Macu z M1 wzwyż, pobiera się około 5 GB, jest błyskawiczna. Wybrałem Qwena zamiast Llamy, bo seria Qwen historycznie radzi sobie lepiej z polskim w tej klasie wielkości. Do większości zastosowań — w pełni wystarczy.

```
ollama pull qwen3:8b
```

**Qwen 3.5 (9B)** to najnowsza odsłona — Alibaba wydała ją kilka tygodni temu. Multimodalna (rozumie też obrazy), polski lepszy o widoczny próg względem 8B, pobiera się około 6 GB. Mój wybór, jeśli masz 16 GB RAM. Sam testuję od niedawna — jak będziesz mieć inne doświadczenia, daj znać w komentarzu.

```
ollama pull qwen3.5:9b
```

**Qwen 3 (32B)** to maksimum, jeśli masz MacBooka Pro z 32 GB+ unified memory (M3 Pro / M4 Pro / Max). Pobiera się około 20 GB i odpowiada wolniej, ale jakość jest porównywalna z dużymi modelami komercyjnymi. Dla 95% zastosowań — overkill, ale jak masz sprzęt, czemu nie.

```
ollama pull qwen3:32b
```

Moja rekomendacja: **zacznij od Qwen 3 (8B)**. Jak zobaczysz że polski jest "prawie ale nie zawsze" — zrób upgrade do Qwen 3.5 (9B). Zmiana modelu to dosłownie zmiana jednego słowa w komendzie.

## Krok 3: Prompt do analizy spotkania

To jest część, w którą warto włożyć pięć minut myślenia. Bo to ona decyduje, czy dostaniesz przydatne notatki, czy bezsensowne podsumowanie.

Po sześciu iteracjach na własnych spotkaniach mam taki prompt:

[OBRAZEK: 04_prompt.png — Prompt do analizy transkrypcji w 4 sekcjach]

Cztery sekcje, w tej kolejności, bo każda kolejna potrzebuje kontekstu z poprzedniej:

1. **Decyzje** — co konkretnie ustalono. Bez "wydaje się że", bez "prawdopodobnie".
2. **Akcje** — kto, co, do kiedy. Format ujednolicony, łatwy do wrzucenia w taska.
3. **Ryzyka i obiekcje** — co zabrzmiało niewygodnie. To tu ukrywają się rzeczy, które zapamiętałeś jako "wszystko OK", a klient odebrał inaczej.
4. **TL;DR** — trzy-cztery zdania na sam koniec, bo dopiero teraz model "zrozumiał" co naprawdę było ważne.

Zasada twarda: *"jeśli czegoś nie ma w transkrypcji — napisz «brak danych»"*. Bez tego model dopowiada, halucynuje, wymyśla cytaty których nigdy nie było. Dla notatek ze spotkania to dyskwalifikujące.

## Krok 4: Puszczamy transkrypcję przez model

Najprościej w terminalu:

```
ollama run qwen3:8b < transkrypcja.txt
```

Wkleisz prompt na początku pliku transkrypcji albo zostawisz go w osobnym pliku i sklejasz dwa pliki przed wysłaniem. Ja używam jednolinijkowca:

```
cat prompt.txt transkrypcja.txt | ollama run qwen3:8b
```

Po kilkudziesięciu sekundach (dla 8B/9B) albo kilku minutach (dla 32B) dostajesz na wyjściu strukturyzowane notatki. W formacie, który już prosi się żeby je wkleić w Notion, Slacku albo CRMie.

Pierwsze pięć sekund jest najprzyjemniejsze. To moment, w którym do Ciebie dociera, że właśnie zrobiłeś analizę poufnej rozmowy bez wysyłania jej nikomu.

## Co dalej?

Masz Whispera (część 1) i Ollamę (dziś). Dwa lokalne klocki, które robią całą robotę.

Logiczny następny krok: spiąć je w jeden skrypt. Jedno polecenie — wskazujesz nagranie, dostajesz strukturyzowane notatki w pliku Markdown. Bez klikania, bez kopiowania między oknami, bez czekania.

To jest dokładnie to, co mam u siebie w użyciu. Postawię to w kolejnym wpisie — jeśli ktoś jest zainteresowany, dajcie znać w komentarzu, wtedy wiem, że ma sens to spisać.

## Jedno zastrzeżenie

Lokalny LLM nadal może się mylić. Mnie zdarzyło się, że Qwen 3 (8B) pomylił nazwiska dwóch osób z tej samej firmy — jeden mówił "ja zrobię X", model przypisał to drugiemu. Po przejściu na Qwen 3.5 (9B) problem przestał występować.

Wniosek: **traktuj output lokalnego modelu jak draft, nie jak źródło prawdy**. Przeczytaj zanim wyślesz dalej. Tak samo jak po notatkach z ChatGPT byś zrobił.

---

[OBRAZEK: 05_cta.png — CTA: Chcesz to mieć u siebie? Napisz do mnie]

**P.S.** Jeśli wolisz nie grzebać samemu w terminalu, ale chcesz mieć u siebie w firmie cały pipeline — od nagrania do notatek w CRMie, lokalnie, dla całego zespołu — napisz do mnie. Pomogę to postawić, włącznie z integracjami z tym, czego już używacie.

**P.P.S.** Jest też wygodniejszy wariant z interfejsem graficznym (Open WebUI, LM Studio) zamiast terminala. Działa świetnie, ale to temat na osobny wpis. Jeśli ktoś by chciał — dajcie znać w komentarzu.

**P.P.P.S.** Mała ciekawostka, której nie wcisnąłem w główny tekst. OpenAI wypuściło niedawno **GPT-OSS** — swoje pierwsze modele open-source, które możesz uruchomić u siebie przez Ollamę. Tak, od tych od ChatGPT.

```
ollama pull gpt-oss:20b
```

Wymaga ~32 GB RAM, polski przyzwoity (nie jest jego mocna strona — to model "rozumowania", nie języka). Ale samego faktu, że da się go uruchomić w domu bez płacenia OpenAI ani złotówki, nie da się odzobaczyć.
