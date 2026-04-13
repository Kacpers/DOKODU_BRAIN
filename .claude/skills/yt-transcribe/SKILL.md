---
name: yt-transcribe
description: Transkrybuje nagranie YouTube przez Whisper i generuje napisy SRT, chapters template, surowy tekst (baza do blog posta) i gotowy post LinkedIn. Trigger: "transkrybuj film", "zrób napisy", "transkrypcja nagrania", /yt-transcribe
---

# Instrukcja: YT Transcribe

## Działanie

Uruchamia Whisper lokalnie na pliku nagrania i generuje 4 pliki w `movies/YT-XXX/publish/`:

| Plik | Do czego |
|------|----------|
| `transkrypcja.txt` | Surowy tekst — baza do blog posta (repurposing) |
| `napisy.srt` | Napisy do DaVinci Resolve lub YouTube Studio |
| `chapters_template.md` | Template chapters z sekcjami ze scenariusza |
| `linkedin_post.txt` | Gotowy post do wklejenia na LinkedIn |

## KROK 1: Ustal co transkrybować

Zapytaj jeśli nie podano:
- ID filmu (np. YT-002)
- Ścieżka do pliku nagrania (mp4, mov, wav, mp3)

## KROK 2: Sprawdź wymagania

```bash
python3 -c "import whisper; print('OK')" 2>/dev/null || echo "brak"
which ffmpeg 2>/dev/null || echo "brak ffmpeg"
```

Jeśli brak whisper:
```bash
pip3 install openai-whisper
```

Jeśli brak ffmpeg — powiedz użytkownikowi:
```bash
sudo apt-get install -y ffmpeg
```

## KROK 3: Uruchom transkrypcję

```bash
cd /home/kacper/DOKODU_BRAIN/scripts && python3 whisper_transcribe.py YT-XXX \
  --file /ścieżka/do/nagrania.mp4 \
  --model medium
```

Model `medium` jest domyślny i najlepszy dla polskiego. Jeśli plik jest długi (>30 min) i zależy Ci na szybkości, użyj `small`.

## KROK 4: Pokaż wynik

Po zakończeniu powiedz:
- Ile segmentów wygenerował Whisper
- Gdzie są pliki (`movies/YT-XXX/publish/`)
- Zaproponuj następny krok: "Chcesz żebym teraz wygenerował draft blog posta z transkrypcji? (`/yt-repurpose`)"

## KROK 5: Repurposing (opcjonalny)

Jeśli użytkownik chce blog post z transkrypcji — uruchom `/yt-repurpose YT-XXX`.

## ZASADY

- Model `medium` dla polskiego — nie używaj `tiny` ani `base` bo jakość PL jest słaba
- Whisper działa lokalnie, offline — żadne dane nie wychodzą na zewnątrz
- Transkrypcja 15-minutowego filmu na CPU trwa ~5-10 minut (model medium)
- Jeśli GPU jest dostępne — Whisper używa go automatycznie (10x szybciej)
- Pliki SRT są kompatybilne z DaVinci Resolve, Premiere, YouTube Studio
