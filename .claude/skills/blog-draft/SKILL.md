---
name: blog-draft
description: Pisze kompletny draft artykułu na blog dokodu.it na podstawie briefu SEO i wysyła go jako draft przez API. Łączy seo-plan-post + pisanie treści + publikację draftu w jednym pipeline. Trigger: "napisz draft", "napisz artykuł", "stwórz post", "wygeneruj artykuł", "napisz posta na bloga", /blog-draft
---

# Instrukcja: Blog Draft

Cel: napisać gotowy do review artykuł blogowy i zapisać go jako draft na dokodu.it.

## KROK 0: Zbierz dane wejściowe

Potrzebujesz (zapytaj jeśli nie podano):
1. Temat / główna fraza kluczowa
2. ID pomysłu z ideas bank (opcjonalne, ale przyspiesza)
3. Typ artykułu (how-to / porównanie / case study / pillar / lista)

Jeśli podano ID ideas bank — odczytaj metadane:
```bash
python3 /home/kacper/DOKODU_BRAIN/scripts/seo_ideas.py show <ID>
```

## KROK 1: Utwórz brief (jeśli nie istnieje)

Użyj `/seo-plan-post` mentalnie lub przeczytaj brief z ideas bank (notatki) i zbuduj strukturę:
- SEO Title, Slug, Meta Description
- Struktura H2/H3
- Kto jest czytelnikiem, jaki jest pain point

## KROK 2: Napisz artykuł

Napisz kompletny artykuł w Markdown, zgodnie z zasadami:

### Styl pisania (Dokodu voice)
- **Ton:** ekspercki, ale przystępny — piszesz do managera IT lub właściciela firmy 50-500 os.
- **Język:** polski, bez kalki z angielskiego, bez żargonu technicznego tam gdzie można prościej
- **Struktura:** jasne H2/H3, krótkie akapity (max 3-4 zdania), bullet lists gdzie pasuje
- **Długość:** 1200-2500 słów dla artykułów how-to/informational; 800-1200 dla porównań
- **Nie używaj:** słów "innowacyjny", "rewolucyjny", "przełomowy", "transformacja cyfrowa" — to puste słowa
- **Używaj:** konkretnych liczb, przykładów z polskiego rynku, scenariuszy z życia firmy

### Obowiązkowe elementy
1. **Intro (150-200 słów):** pain point → obietnica → proof
2. **Każdy H2:** zaczyna się od sedna, nie od wprowadzenia
3. **Linki wewnętrzne:** minimum 2-3 do stron na dokodu.it (kursy, szkolenia, wdrożenia)
4. **CTA na końcu:** konkretny (nie "skontaktuj się z nami" — ale "umów bezpłatną 30-min. konsultację")
5. **Meta/Excerpt:** 120-155 znaków, z główną frazą i CTA

### Format Markdown
```markdown
# [Tytuł H1 — taki sam lub podobny do SEO Title]

[Intro — pain point + obietnica + proof]

## [Nagłówek H2]

[Treść]

### [Podnagłówek H3 jeśli potrzebny]

## [Nagłówek H2]

...

## Podsumowanie

[3-5 kluczowych wniosków w bullet points]

**[CTA — konkretne wezwanie do działania z linkiem]**
```

## KROK 3: Sprawdź czy slug istnieje (unikaj duplikatów)

```bash
python3 /home/kacper/DOKODU_BRAIN/scripts/blog_publish.py get --slug <slug>
```

## KROK 4a: Utwórz draft (nowy post)

Zapisz treść do pliku tymczasowego i wyślij:
```bash
# Zapisz treść do pliku
cat > /tmp/blog_draft.md << 'EOF'
[TREŚĆ ARTYKUŁU]
EOF

# Utwórz draft
python3 /home/kacper/DOKODU_BRAIN/scripts/blog_publish.py create \
  --title "[SEO Title]" \
  --slug "[slug-bez-polskich-znaków]" \
  --content-file /tmp/blog_draft.md \
  --excerpt "[meta description 120-155 znaków]" \
  --meta-title "[SEO Title jeśli różny od title]" \
  --category "[Pillar: M365 Copilot / n8n Automatyzacja / etc.]" \
  --tags "[główna fraza],[tag2],[tag3]" \
  --author "Kacper"
```

Jeśli tworzysz z ideas bank (zalecane):
```bash
python3 /home/kacper/DOKODU_BRAIN/scripts/blog_publish.py create \
  --from-idea <ID> \
  --content-file /tmp/blog_draft.md
```

## KROK 4b: Zaktualizuj istniejący post

Jeśli slug już istnieje (post był wcześniej tworzony):
```bash
python3 /home/kacper/DOKODU_BRAIN/scripts/blog_publish.py update \
  --id <blog_post_id> \
  --content-file /tmp/blog_draft.md
```

## KROK 5: Potwierdź i zaraportuj

Po udanym wykonaniu powiedz użytkownikowi:
- Tytuł artykułu
- Slug / URL preview: `https://dokodu.it/blog/<slug>`
- Status: draft (nie jest jeszcze widoczny publicznie)
- Liczba słów (szacunkowo)
- ID posta (do późniejszej publikacji)

## KROK 6: Zaproponuj następny krok

```
"Draft jest na blogu jako 'draft' — widoczny tylko po zalogowaniu.
 Kiedy będziesz gotowy do publikacji, powiedz mi lub użyj:
 /blog-publish --id <ID>"
```

Opcjonalnie zaproponuj:
- "Czy chcesz żebym zoptymalizował meta description?"
- "Czy dodać schemat Article (JSON-LD) do tego posta?" → `/seo schema`

## KROK 2b: SEO Checklist — weryfikacja PRZED opublikowaniem

Przed wywołaniem `blog_publish.py create/update` sprawdź każdy punkt:

### Struktura i SEO on-page
- [ ] **H1** zawiera główną frazę kluczową (najlepiej na początku zdania)
- [ ] **Meta title** ≤ 60 znaków, fraza kluczowa blisko początku
- [ ] **Excerpt/meta description** 120–155 znaków, zawiera frazę + CTA
- [ ] **Slug** tylko małe litery + myślniki, bez polskich znaków, max 6 słów
- [ ] Artykuł ma min. **3 sekcje H2**, każda zaczyna się od sedna (nie od "W tej sekcji...")
- [ ] Żaden H2 nie jest pustym nagłówkiem bez treści

### Treść
- [ ] **Intro** (150–200 słów): pain point → obietnica → proof (liczba/statystyka)
- [ ] Artykuł zawiera **konkretne liczby, przykłady lub tabelę** (nie tylko ogólniki)
- [ ] Nie użyto zakazanych słów: "innowacyjny", "rewolucyjny", "przełomowy", "transformacja cyfrowa"
- [ ] Jest **sekcja FAQ** (min. 3 pytania) — format OBOWIĄZKOWY: `### Pytanie` + akapit odpowiedzi (nie używaj H4, nie używaj **bold** jako pytanie)
- [ ] Jest **podsumowanie** z bullet points (3–5 wniosków)
- [ ] Na końcu jest **konkretny CTA** z linkiem (nie "skontaktuj się" ale "umów bezpłatną 30-min. konsultację")

### Linki
- [ ] Min. **3 linki wewnętrzne** do realnych stron dokodu.it (sprawdź że URL istnieje)
- [ ] Żaden link wewnętrzny nie prowadzi do nieistniejącej strony — każdy link sprawdź pod kątem czy artykuł/strona istnieje na blogu lub jest zaplanowana w klastrze
- [ ] Linki wewnętrzne mają **opisowe anchor texty** (nie "kliknij tutaj")

### Reklamy
- [ ] Są **min. 2 tagi `<AD:...>`** w artykule
- [ ] Tagi `<AD:...>` są rozmieszczone naturalnie (po dużej sekcji, nie na samym początku lub końcu)
- [ ] Standardowy zestaw: `<AD:kurs-n8n-waitlist>` (środek artykułu) + `<AD:n8n-workshop>` lub `<AD:ai-automation-offer>` (koniec)

### Rok i aktualność
- [ ] Artykuł używa roku **2026** (nie 2025)
- [ ] Dane statystyczne mają źródło (Gartner, McKinsey, itp.) lub są opisane jako szacunkowe

### Finalna weryfikacja
- [ ] Sprawdź slug: `python3 blog_publish.py get --slug <slug>` — jeśli 404 to tworzysz nowy, jeśli 200 to aktualizujesz
- [ ] Plik .md zapisany lokalnie do `RES_Blog_Drafts/DRAFT_<slug>.md`
- [ ] Po opublikowaniu zaktualizuj link_graph: `python3 link_graph.py --add-article` + `--add-link` dla kluczowych linków

---

## ZASADY

- Zawsze najpierw sprawdź czy slug istnieje (KROK 3) — unikaj 409
- Nie publikuj automatycznie — zawsze twórz draft i daj użytkownikowi do review
- Jeśli brak API key → powiedz: "Ustaw klucz API w `~/.config/dokodu/blog_api_key` (szczegóły: scripts/GSC_SETUP.md)"
- Linki wewnętrzne muszą być do realnych stron na dokodu.it — nie linkuj do artykułów które nie istnieją
- Nie wymyślaj case studies — opisuj ogólne scenariusze, chyba że użytkownik poda dane

## FAQ — WAŻNE: standard formatu

FAQ w artykule MUSI być zapisane jako:
```markdown
## FAQ — najczęstsze pytania o [temat]

### Czy agent AI zastąpi moich pracowników?

Nie w sensie dosłownym...

### Ile kosztuje wdrożenie agenta AI?

Koszt startowy...
```

**Dlaczego?** `blog_publish.py publish` automatycznie wyciąga FAQ do tabeli `Faq` w bazie danych i usuwa sekcję z `contentMarkdown`. Dzięki temu FAQ renderuje się przez komponent `FAQLazy` z pełnym **JSON-LD schema** (SEO) i nie pojawia się zduplikowane w treści artykułu.

- NIE używaj `#### Pytanie` (H4) — parser tego nie obsługuje
- NIE używaj `**Pytanie**` jako nagłówka — parser obsługuje, ale `###` jest preferowany
- Format `### Pytanie` → akapit odpowiedzi jest jedynym oficjalnym formatem
