#!/usr/bin/env python3
"""
n8n Screenshot Tool — Modul_01_Fundamenty
==========================================
Otwiera n8n.dokodu.it w prawdziwej przeglądarce.
Ty logujesz się raz ręcznie, potem skrypt sam robi screenshoty.

Użycie:
  python3 scripts/n8n_screenshot.py

Screenshoty trafiają do:
  10_PROJECTS/PRJ_Kurs_n8n_Launch/SLIDEV/assets/screenshots/
"""

import os
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

N8N_URL = "https://n8n.dokodu.it"

OUT_DIR = Path(__file__).parent / "../10_PROJECTS/PRJ_Kurs_n8n_Launch/SLIDEV/assets/screenshots"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Lista slajdów do zescreenowania ──────────────────────────────
# Format: (nazwa_pliku, url_lub_path, selektor_do_czekania, opis)
# url_lub_path: pełny URL lub ścieżka względem N8N_URL
# selektor: element którego Playwright czeka przed zrobieniem screena
# crop: None = full page, (x,y,w,h) = przytnij do obszaru

SHOTS = [
    {
        "file": "01_canvas_pusty.png",
        "url": "/workflow/new",
        "wait_for": ".workflow-canvas, canvas, [data-test-id='workflow-canvas']",
        "clip": None,           # cały viewport
        "desc": "Pusty canvas — główny widok n8n",
        "viewport": (1400, 900),
    },
    {
        "file": "02_node_library.png",
        "url": "/workflow/new",
        "wait_for": ".node-creator, [data-test-id='node-creator-plus-button']",
        "clip": None,
        "desc": "Panel z biblioteką nodów (po kliknięciu +)",
        "action": "open_node_panel",   # specjalna akcja
        "viewport": (1400, 900),
    },
    {
        "file": "03_webhook_trigger.png",
        "url": "/workflow/new",
        "wait_for": ".workflow-canvas",
        "clip": None,
        "desc": "Webhook Trigger skonfigurowany",
        "viewport": (1400, 900),
    },
]


def wait_for_login(page):
    """Czeka aż użytkownik zaloguje się ręcznie."""
    print("\n" + "="*60)
    print("  ZALOGUJ SIĘ DO n8n w oknie przeglądarki")
    print("  Skrypt czeka automatycznie na wykrycie loginu...")
    print("="*60 + "\n")

    # Czekaj aż URL zmieni się z /signin na coś innego
    page.wait_for_url(lambda url: "/signin" not in url and "/login" not in url,
                      timeout=120_000)

    # Dodatkowe potwierdzenie — czekaj na element głównej nawigacji
    page.wait_for_selector("nav, .el-menu, [data-test-id='main-sidebar']",
                           timeout=30_000)
    print("✅ Wykryto zalogowanie!\n")


def do_screenshot(browser, shot: dict):
    """Robi jeden screenshot według specyfikacji."""
    page = browser.new_page()

    url = shot["url"]
    if not url.startswith("http"):
        url = N8N_URL + url

    print(f"  → {shot['desc']}")
    print(f"     URL: {url}")

    page.goto(url, wait_until="networkidle", timeout=30_000)

    # Czekaj na selector
    try:
        page.wait_for_selector(shot["wait_for"], timeout=15_000)
    except Exception:
        print(f"     ⚠️  Selektor '{shot['wait_for']}' nie pojawił się — robię screen anyway")

    # Specjalne akcje
    action = shot.get("action")
    if action == "open_node_panel":
        try:
            # Spróbuj kliknąć przycisk + aby otworzyć bibliotekę nodów
            page.click("[data-test-id='node-creator-plus-button'], .add-node-button, button[title*='Add']",
                       timeout=5_000)
            time.sleep(1)
        except Exception:
            print("     ⚠️  Nie udało się otworzyć panelu nodów — screen bez panelu")

    # Małe opóźnienie dla animacji
    time.sleep(0.8)

    # Screenshot
    out_path = OUT_DIR / shot["file"]
    clip = shot.get("clip")
    if clip:
        x, y, w, h = clip
        page.screenshot(path=str(out_path), clip={"x": x, "y": y, "width": w, "height": h})
    else:
        page.screenshot(path=str(out_path))

    print(f"     ✅ Zapisano: {out_path.name} ({out_path.stat().st_size // 1024} KB)\n")
    page.close()


def main():
    print("\n🎬 n8n Screenshot Tool — Modul_01_Fundamenty")
    print(f"   Target: {N8N_URL}")
    print(f"   Output: {OUT_DIR.resolve()}\n")

    with sync_playwright() as p:
        # Odpal widoczną przeglądarkę (headful) żebyś mógł się zalogować
        browser = p.chromium.launch(
            headless=False,
            args=["--start-maximized"],
            slow_mo=50,
        )
        context = browser.new_context(
            viewport={"width": 1400, "height": 900},
            no_viewport=False,
        )

        # Strona logowania
        login_page = context.new_page()
        login_page.goto(N8N_URL, timeout=30_000)

        # Czekaj na login
        wait_for_login(login_page)
        login_page.close()

        # Rób screenshoty jeden po drugim
        print(f"📸 Robię {len(SHOTS)} screenshotów...\n")
        for i, shot in enumerate(SHOTS, 1):
            print(f"[{i}/{len(SHOTS)}] {shot['file']}")
            try:
                do_screenshot(context, shot)
            except Exception as e:
                print(f"     ❌ Błąd: {e}\n")

        browser.close()

    print("\n✅ Gotowe! Screenshoty w:")
    print(f"   {OUT_DIR.resolve()}")
    print("\nNastępny krok: powiedz Claude'owi które screenshoty")
    print("chcesz wstawić na które slajdy.\n")


if __name__ == "__main__":
    main()
