---
name: blog-publish
description: Zarządza publikacją postów na dokodu.it/blog/ — publikuje drafty, aktualizuje posty, listuje zawartość bloga. Integruje się z ideas bank. Trigger: "opublikuj post", "opublikuj draft", "opublikuj artykuł", "lista postów na blogu", "sprawdź bloga", /blog-publish
---

# Instrukcja: Blog Publish

Zarządzanie postami na dokodu.it przez API.

## Typowe operacje

### Sprawdź status bloga (lista postów)

```bash
# Wszystkie drafty
python3 /home/kacper/DOKODU_BRAIN/scripts/blog_publish.py list --status draft

# Wszystkie opublikowane
python3 /home/kacper/DOKODU_BRAIN/scripts/blog_publish.py list --status published

# Wszystkie (limit 50)
python3 /home/kacper/DOKODU_BRAIN/scripts/blog_publish.py list --limit 50
```

### Sprawdź konkretny post

```bash
# Po slugu
python3 /home/kacper/DOKODU_BRAIN/scripts/blog_publish.py get --slug <slug>

# Po ID
python3 /home/kacper/DOKODU_BRAIN/scripts/blog_publish.py get --id <id>
```

### Opublikuj draft

```bash
# Zwykła publikacja
python3 /home/kacper/DOKODU_BRAIN/scripts/blog_publish.py publish --id <blog_post_id>

# Publikacja + aktualizacja ideas bank
python3 /home/kacper/DOKODU_BRAIN/scripts/blog_publish.py publish \
  --id <blog_post_id> \
  --idea-id <seo_idea_id>
```

### Zaktualizuj istniejący post

```bash
# Zmień tylko treść
python3 /home/kacper/DOKODU_BRAIN/scripts/blog_publish.py update \
  --id <id> --content-file /tmp/updated_post.md

# Zmień meta i status
python3 /home/kacper/DOKODU_BRAIN/scripts/blog_publish.py update \
  --id <id> \
  --status published \
  --idea-id <seo_idea_id>
```

## Workflow: Draft → Publikacja

```
1. /blog-draft         → pisze artykuł + tworzy draft (status=draft)
2. Ręczna review       → przeglądasz na dokodu.it (zalogowany)
3. /blog-publish       → publikujesz (status=published)
```

## Konfiguracja API Key

Jeśli pojawi się błąd "BRAK KLUCZA API":
```bash
# Ustaw klucz (znajdziesz go w .env bloga jako EXTERNAL_API_KEY)
echo "twoj_klucz_api" > ~/.config/dokodu/blog_api_key
chmod 600 ~/.config/dokodu/blog_api_key
```

Lub jako zmienna środowiskowa:
```bash
export EXTERNAL_API_KEY=twoj_klucz_api
```

## ZASADY

- Nigdy nie publikuj bez pytania użytkownika — zawsze twórz draft najpierw
- Przed publikacją przypomnij użytkownikowi o review
- Po publikacji podaj pełny URL: `https://dokodu.it/blog/<slug>`
- Jeśli `--idea-id` podany → automatycznie zaktualizuj status w ideas bank na OPUBLIKOWANY
