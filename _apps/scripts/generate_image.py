#!/usr/bin/env python3
"""
DOKODU BRAIN — Image generation via Google Gemini (Nano Banana)

Generuje featured/inline images do blog postów przez Gemini API.
Domyślnie używa Nano Banana Pro (Gemini 3 Pro Image) — najwyższa jakość.
Dla inline/tańszych obrazów: flaga --flash (Gemini 3.1 Flash Image, ~50% taniej).

Setup (jednorazowo):
    pip install google-genai Pillow
    # opcjonalnie dla AVIF:
    pip install pillow-avif-plugin

    # API key (Google AI Studio → https://aistudio.google.com/apikey):
    mkdir -p ~/.config/dokodu
    echo "AIzaSy..." > ~/.config/dokodu/google_ai_key
    chmod 600 ~/.config/dokodu/google_ai_key

Użycie:
    # Featured image dla blog posta (domyślnie 1920x1080, Pro model):
    python3 generate_image.py \\
        "Modern minimalist infographic, 3 horizontal layers..." \\
        --output /path/to/website-nextjs/public/images/posts/n8n-cennik-2026.png

    # Inline image, taniej (Flash model, 1024x1024):
    python3 generate_image.py "Prompt here..." \\
        --output /path/to/image.png \\
        --flash \\
        --size 1024x1024

    # Wygeneruj + automatycznie konwertuj do webp i avif:
    python3 generate_image.py "Prompt..." \\
        --output /path/to/image.png \\
        --all-formats

Koszty (stan 2026-04):
    Nano Banana Pro (domyślny)  — $0.134 / img @ 1K (~0.54 PLN)
    Nano Banana 2 Flash (--flash) — $0.067 / img @ 1K (~0.27 PLN)
"""

from __future__ import annotations

import argparse
import io
import os
import sys
from pathlib import Path

CONFIG_KEY_PATH = Path.home() / ".config" / "dokodu" / "google_ai_key"

# Model IDs — update gdy Google zmienia nazwy endpoint-ów
MODEL_PRO = "gemini-3-pro-image-preview"      # Nano Banana Pro
MODEL_FLASH = "gemini-3.1-flash-image-preview"  # Nano Banana 2 Flash

DEFAULT_SIZE = "1920x1080"  # 16:9 hero / featured image
DEFAULT_OUTPUT_FORMATS = ("png",)  # dodatkowe via --all-formats


def load_api_key() -> str:
    """Czyta API key z pliku lub env — kolejność: env > plik konfiguracyjny."""
    for env_var in ("GOOGLE_AI_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY"):
        if os.environ.get(env_var):
            return os.environ[env_var]

    if CONFIG_KEY_PATH.exists():
        return CONFIG_KEY_PATH.read_text().strip()

    sys.exit(
        f"❌ Brak API key. Ustaw GOOGLE_AI_KEY (env) lub zapisz klucz do:\n"
        f"   {CONFIG_KEY_PATH}\n"
        f"   (odbierz klucz z https://aistudio.google.com/apikey)"
    )


def parse_size(size_str: str) -> tuple[int, int]:
    try:
        w, h = size_str.lower().split("x")
        return int(w), int(h)
    except (ValueError, AttributeError):
        sys.exit(f"❌ Nieprawidłowy format --size: '{size_str}'. Oczekiwany: 1920x1080")


def generate_with_gemini(prompt: str, model: str, api_key: str) -> bytes:
    """Woła Gemini image gen API i zwraca surowe bajty PNG."""
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        sys.exit(
            "❌ Brak paczki google-genai. Zainstaluj:\n"
            "   pip install google-genai"
        )

    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model=model,
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
            ),
        )
    except Exception as e:
        sys.exit(f"❌ Błąd API Gemini: {e}")

    # Response zawiera parts — szukamy inline_data z image/png
    for candidate in response.candidates or []:
        for part in candidate.content.parts or []:
            if getattr(part, "inline_data", None) and part.inline_data.data:
                return part.inline_data.data

    sys.exit("❌ Gemini nie zwrócił obrazu. Sprawdź prompt / limity konta.")


def save_formats(
    raw_png: bytes,
    output_path: Path,
    target_size: tuple[int, int],
    formats: tuple[str, ...],
) -> list[Path]:
    """Zapisuje obraz w wybranych formatach. Resize do target_size jeśli != output modelu."""
    try:
        from PIL import Image
    except ImportError:
        sys.exit("❌ Brak Pillow. Zainstaluj: pip install Pillow")

    img = Image.open(io.BytesIO(raw_png))

    # Resize jeśli rozmiar z modelu różni się od oczekiwanego
    if img.size != target_size:
        img = img.resize(target_size, Image.Resampling.LANCZOS)

    # Konwersja do RGB (AVIF i WebP lepiej obsługują RGB niż P/RGBA)
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGB")

    saved = []
    output_path = output_path.with_suffix("")  # strip obecnego suffixu

    for fmt in formats:
        target = output_path.with_suffix(f".{fmt}")
        save_kwargs: dict = {}

        if fmt == "png":
            save_kwargs = {"format": "PNG", "optimize": True}
        elif fmt == "webp":
            save_kwargs = {"format": "WEBP", "quality": 90, "method": 6}
        elif fmt == "avif":
            try:
                import pillow_avif  # noqa: F401 — rejestruje handler AVIF w PIL
            except ImportError:
                print(f"⚠️  Pomijam .avif — brak pillow-avif-plugin (pip install pillow-avif-plugin)")
                continue
            save_kwargs = {"format": "AVIF", "quality": 80}
        else:
            print(f"⚠️  Nieobsługiwany format: {fmt}")
            continue

        img.save(target, **save_kwargs)
        saved.append(target)
        print(f"✅ {target} ({target.stat().st_size // 1024} KB)")

    return saved


def main():
    parser = argparse.ArgumentParser(
        description="Generuj featured/inline image przez Nano Banana (Gemini).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("prompt", help="Prompt do modelu (szczegółowy, w angielskim)")
    parser.add_argument("--output", "-o", required=True, type=Path,
                        help="Ścieżka docelowa (bez rozszerzenia lub z .png)")
    parser.add_argument("--size", default=DEFAULT_SIZE,
                        help=f"Rozmiar WxH (domyślnie {DEFAULT_SIZE})")
    parser.add_argument("--flash", action="store_true",
                        help="Użyj Nano Banana 2 Flash zamiast Pro (taniej, niższa jakość)")
    parser.add_argument("--all-formats", action="store_true",
                        help="Zapisz też .webp i .avif (jeśli plugin dostępny)")
    parser.add_argument("--model", default=None,
                        help=f"Nadpisz ID modelu (domyślnie: {MODEL_PRO} lub {MODEL_FLASH} przy --flash)")

    args = parser.parse_args()

    model = args.model or (MODEL_FLASH if args.flash else MODEL_PRO)
    target_size = parse_size(args.size)
    formats = ("png", "webp", "avif") if args.all_formats else DEFAULT_OUTPUT_FORMATS

    # Katalog docelowy
    args.output.parent.mkdir(parents=True, exist_ok=True)

    print(f"🎨 Model: {model}")
    print(f"📐 Rozmiar docelowy: {target_size[0]}x{target_size[1]}")
    print(f"💾 Formaty: {', '.join(formats)}")
    print(f"📝 Prompt: {args.prompt[:80]}{'...' if len(args.prompt) > 80 else ''}")
    print()

    api_key = load_api_key()
    print("⏳ Generuję obraz...")
    raw_png = generate_with_gemini(args.prompt, model, api_key)

    saved = save_formats(raw_png, args.output, target_size, formats)

    print()
    print(f"✨ Gotowe. Zapisano {len(saved)} plik(ów).")

    # Szacunkowy koszt (informacyjny — rzeczywisty rozliczany przez Google)
    cost_usd = 0.067 if args.flash else 0.134
    cost_pln = cost_usd * 4.0  # przybliżony kurs
    print(f"💰 Szacunkowy koszt: ${cost_usd:.3f} (~{cost_pln:.2f} PLN)")


if __name__ == "__main__":
    main()
