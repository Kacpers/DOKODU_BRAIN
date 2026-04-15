---
name: tiktok-pipeline
description: Zarządza pipeline produkcji TikToków — scenariusze, post-production, napisy, upload. Pełny flow od pomysłu do gotowego klipu.
user_invocable: true
---

# TikTok Pipeline — Dokodu

Pipeline produkcji TikToków w 3 fazach:

## FLOW

```
SCENARIUSZE → NAGRANIE (Kacper) → POST-PRODUCTION → PUBLIKACJA
     ↓              ↓                    ↓               ↓
 Ideas Bank    Parrot Prompter    Whisper + FFmpeg    TikTok upload
 10 skryptów   batch session      napisy + cięcie     opis + hashtagi
```

## KOMENDY

### Faza 1: Pre-production (scenariusze)

Użytkownik mówi: "przygotuj tiktoki", "scenariusze tiktok", "batch tiktok"

1. Załaduj `30_RESOURCES/RES_YouTube/TikTok_Playbook.md` — ZAWSZE czytaj przed pisaniem
2. Załaduj `20_AREAS/AREA_YouTube/TikTok_Ideas_Bank.md`
3. Wybierz 10 pomysłów w statusie `POMYSŁ` (lub tyle ile user chce)
4. Dla każdego napisz PEŁNY scenariusz teleprompterowy wg struktury z Playbooka:
   ```
   [HOOK 0-0.5s] — Pattern interrupt, bold statement, BEZ "Cześć jestem Kacper"
   [PROBLEM 0.5-3s] — Nazwij ból w 1-2 zdaniach
   [KONTEKST 3-8s] — Dlaczego to ważne
   [WARTOŚĆ 8-45s] — Demo / rozwiązanie / insight (RDZEŃ scenariusza)
   [PUNCHLINE 45-55s] — Twist, zaskakujący wniosek
   [CTA 55-60s] — "Obserwuj po więcej" / pytanie prowokujące komentarze
   ```
5. TON: TikTok Voice z Playbooka — luźny, szybki, gadany, jak do kolegi
   - "Słuchaj...", "Patrzcie", "Serio teraz", "I teraz najlepsze..."
   - Krótkie zdania. Max 10 słów. Energia.
   - Liczby konkretne. "6 godzin", "200 maili", "30 dolarów"
6. Eksportuj do Dropboxa: `~/Dropbox/Apps/Parrot Teleprompter/TikTok_T-XXX_scenariusz.txt`
7. Zaktualizuj status w Ideas Bank: `POMYSŁ` → `SCENARIUSZ`
8. Powiedz Kacprowi: "10 scenariuszy czeka w Parrot Teleprompter, siadaj nagrywaj"

### Faza 2: Post-production (po nagraniu)

Użytkownik mówi: "obróbka tiktok", "zmontuj tiktoki", "przerób nagrania"

Uruchom skrypt pipeline:
```bash
# Pojedynczy klip:
python3 scripts/tiktok_pipeline.py process /ścieżka/do/klipu.mp4

# Cały batch:
python3 scripts/tiktok_pipeline.py batch /ścieżka/do/folderu/

# Tylko napisy:
python3 scripts/tiktok_pipeline.py subtitles /ścieżka/do/klipu.mp4

# Eksport do DaVinci Resolve (timeline FCPXML):
python3 scripts/tiktok_pipeline.py davinci /ścieżka/do/klipu.mp4
```

Pipeline automatycznie:
- Transkrybuje (Whisper, word-level timestamps, polski)
- Generuje napisy ASS (stylowane, polskie znaki, word-by-word highlight)
- Tnie pauzy >0.8s
- Wypala napisy (FFmpeg)
- Dodaje intro/CTA (Remotion render)
- Generuje FCPXML timeline (import w DaVinci: File > Import > Timeline)
- Generuje opis + hashtagi

Wyniki lądują w: `20_AREAS/AREA_YouTube/tiktok_publish/<clip_name>/`

### Faza 2b: DaVinci Resolve (opcjonalnie)

Użytkownik mówi: "eksport do davinci", "timeline davinci", "chcę sam zmontować"

```bash
python3 scripts/tiktok_pipeline.py davinci /ścieżka/do/klipu.mp4
```

Generuje:
- `.fcpxml` — timeline z auto-cięciem pauz (File > Import > Timeline w DaVinci)
- `.ass` — napisy do importu jako subtitle track
- `.txt` — surowa transkrypcja

Kacper otwiera w DaVinci, dopracowuje cięcia, eksportuje MP4.

### Faza 3: Publikacja

Użytkownik mówi: "wrzuć tiktoki", "publikuj"

1. Sprawdź folder `tiktok_publish/` — pokaż co jest gotowe
2. Dla każdego klipu pokaż: preview opisu, hashtagi, rozmiar pliku
3. Upload: (TODO — wymaga TikTok API setup)
   - Na razie: podaj instrukcję ręcznego uploadu przez apkę
   - Docelowo: automatyczny upload przez TikTok Content Posting API

## WAŻNE ZASADY

- **Napisy MUSZĄ mieć polskie znaki** — UTF-8, font Inter z pełnym supportem PL
- **Hook jest KLUCZOWY** — pierwsze 2 sekundy decydują o scroll-stop
- **Max 60s** dla TikToka, do 90s dla YT Shorts / Reels
- **Cross-post:** TikTok → YT Shorts → IG Reels → LinkedIn Video
- Format: 1080x1920 (vertical 9:16)
- **Ton:** konkretny, bez lania wody, lekko prowokacyjny

## PLIKI SYSTEMU

- `scripts/tiktok_pipeline.py` — główny skrypt pipeline
- `remotion/src/compositions/TikTok/` — Remotion compositions (Intro, CTA, TopicCard)
- `remotion/src/style/tiktok-theme.ts` — vertical theme (1080x1920)
- `20_AREAS/AREA_YouTube/TikTok_Ideas_Bank.md` — bank pomysłów
- `20_AREAS/AREA_YouTube/tiktok_publish/` — output folder

## WYMAGANIA

```bash
pip3 install faster-whisper
sudo apt-get install ffmpeg
cd remotion && npm install  # dla intro/CTA renders
```
