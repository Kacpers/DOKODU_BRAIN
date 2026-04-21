"""Render LinkedIn post images for Part 2 (Local LLM / Ollama).

Style matches Part 1 (LinkedIn_AI_w_Pracy): dark navy bg, hot-pink accent,
cyan/purple highlights, Inter font.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT_DIR = Path(__file__).parent

BASE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }
html, body {
  font-family: 'Inter', sans-serif;
  background: #0B0F1A;
  color: #E5E7EB;
  -webkit-font-smoothing: antialiased;
}
.bg {
  background:
    radial-gradient(ellipse at top right, rgba(236, 72, 153, 0.08), transparent 50%),
    radial-gradient(ellipse at bottom left, rgba(34, 211, 238, 0.05), transparent 50%),
    #0B0F1A;
  width: 100%;
  min-height: 100vh;
  padding: 60px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.title {
  font-size: 36px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 8px;
  background: linear-gradient(135deg, #22D3EE, #A78BFA);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.subtitle {
  font-size: 18px;
  color: #94A3B8;
  text-align: center;
  margin-bottom: 36px;
}
.muted { color: #64748B; }
.pink { color: #EC4899; }
.cyan { color: #22D3EE; }
.purple { color: #A78BFA; }
"""

# ============================================================
# IMAGE 1 — Pipeline (5 steps: transkrypcja → wynik)
# ============================================================
PIPELINE_HTML = """
<!DOCTYPE html><html><head><meta charset="utf-8"><style>""" + BASE_CSS + """
.row { display: flex; align-items: center; gap: 18px; }
.card {
  background: linear-gradient(160deg, #131A2A, #0F1422);
  border: 1px solid rgba(148, 163, 184, 0.12);
  border-radius: 18px;
  padding: 28px 22px;
  width: 200px;
  height: 180px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: center;
}
.card .step {
  font-size: 11px;
  letter-spacing: 2px;
  color: #64748B;
  font-weight: 600;
  margin-bottom: 12px;
}
.card .name {
  font-size: 20px;
  font-weight: 700;
  color: #F1F5F9;
  line-height: 1.2;
  margin-bottom: 10px;
}
.card .meta {
  font-size: 13px;
  color: #94A3B8;
  line-height: 1.3;
}
.card.accent {
  background: linear-gradient(160deg, #EC4899, #BE185D);
  border-color: rgba(236, 72, 153, 0.6);
  box-shadow: 0 0 60px rgba(236, 72, 153, 0.35);
}
.card.accent .step { color: rgba(255,255,255,0.7); }
.card.accent .name, .card.accent .meta { color: #fff; }
.card.cyan-card .name { color: #22D3EE; }
.card.purple-card .name { color: #A78BFA; }
.card.purple-card { border-color: rgba(167, 139, 250, 0.3); border-style: dashed; }
.arrow { color: #EC4899; font-size: 24px; font-weight: 800; }
</style></head><body><div class="bg">
<div class="row">
  <div class="card"><div class="step">WEJŚCIE</div><div class="name">Transkrypcja</div><div class="meta">.txt z części 1<br>(80 stron tekstu)</div></div>
  <div class="arrow">→</div>
  <div class="card"><div class="step">KROK 1</div><div class="name">Ollama</div><div class="meta">Lokalny silnik LLM<br>jedna komenda</div></div>
  <div class="arrow">→</div>
  <div class="card accent"><div class="step">KROK 2</div><div class="name">Qwen 3 / Qwen 3.5</div><div class="meta">Model uruchomiony<br>na Twoim Macu</div></div>
  <div class="arrow">→</div>
  <div class="card"><div class="step">KROK 3</div><div class="name">Prompt analityczny</div><div class="meta">Decyzje, akcje,<br>ryzyka, TL;DR</div></div>
  <div class="arrow">→</div>
  <div class="card cyan-card"><div class="step">WYNIK</div><div class="name">Notatki</div><div class="meta">Strukturyzowane<br>4 sekcje</div></div>
</div>
</div></body></html>
"""

# ============================================================
# IMAGE 2 — Comparison: ChatGPT/Claude API vs Ollama
# ============================================================
COMPARE_HTML = """
<!DOCTYPE html><html><head><meta charset="utf-8"><style>""" + BASE_CSS + """
.bg { padding-top: 48px; }
table {
  border-collapse: separate;
  border-spacing: 0;
  background: linear-gradient(160deg, #131A2A, #0F1422);
  border: 1px solid rgba(148, 163, 184, 0.12);
  border-radius: 20px;
  overflow: hidden;
  width: 1100px;
}
th, td {
  padding: 22px 28px;
  text-align: center;
  font-size: 18px;
  border-bottom: 1px solid rgba(148, 163, 184, 0.08);
}
tr:last-child td { border-bottom: none; }
th {
  font-size: 19px;
  font-weight: 700;
  background: rgba(15, 23, 42, 0.5);
}
th.col-api { color: #94A3B8; background: linear-gradient(180deg, #1E293B, #0F172A); }
th.col-ollama {
  color: #fff;
  background: linear-gradient(180deg, #EC4899, #BE185D);
}
td.row-label { text-align: left; font-weight: 600; color: #F1F5F9; width: 200px; }
td.api { color: #94A3B8; }
td.ollama { color: #FBCFE8; font-weight: 600; }
td.ollama strong { color: #FFFFFF; font-weight: 800; }
.bg.compare-bg { background:
  radial-gradient(ellipse at top, rgba(236, 72, 153, 0.10), transparent 50%),
  #0B0F1A; }
.note { color: #64748B; font-size: 15px; margin-top: 24px; text-align: center; }
.note strong { color: #EC4899; }
</style></head><body><div class="bg compare-bg">
<div class="title">ChatGPT API / Claude API vs Ollama lokalnie</div>
<div class="subtitle">Analiza transkrypcji spotkania — ten sam dylemat co przy nagraniu</div>
<table>
  <tr>
    <th></th>
    <th class="col-api">ChatGPT / Claude API</th>
    <th class="col-ollama">Ollama (lokalnie)</th>
  </tr>
  <tr>
    <td class="row-label">Koszt (1h spotkania)</td>
    <td class="api">~0.50–2 PLN</td>
    <td class="ollama"><strong>0 PLN</strong></td>
  </tr>
  <tr>
    <td class="row-label">Twoje dane</td>
    <td class="api">USA / Irlandia</td>
    <td class="ollama"><strong>Twój komputer</strong></td>
  </tr>
  <tr>
    <td class="row-label">Polski</td>
    <td class="api">bardzo dobry</td>
    <td class="ollama"><strong>dobry (Qwen 3.5)</strong></td>
  </tr>
  <tr>
    <td class="row-label">Limity tokenów</td>
    <td class="api">tak (rate limits)</td>
    <td class="ollama"><strong>brak</strong></td>
  </tr>
  <tr>
    <td class="row-label">Konfiguracja</td>
    <td class="api"><strong style="color:#EC4899">2 min</strong></td>
    <td class="ollama">15 min (raz)</td>
  </tr>
</table>
<div class="note">Wynik: <strong>4:1 dla Ollamy</strong>. Jakość polskiego — w 90% przypadków wystarczy. Dane zostają u Ciebie.</div>
</div></body></html>
"""

# ============================================================
# IMAGE 3 — Models × MacBook Pro
# ============================================================
MODELS_HTML = """
<!DOCTYPE html><html><head><meta charset="utf-8"><style>""" + BASE_CSS + """
.cards { display: flex; gap: 24px; }
.mcard {
  background: linear-gradient(160deg, #131A2A, #0F1422);
  border: 1px solid rgba(148, 163, 184, 0.12);
  border-radius: 20px;
  padding: 32px 28px;
  width: 320px;
  text-align: center;
}
.mcard .req { font-size: 12px; color: #64748B; letter-spacing: 1.5px; font-weight: 600; margin-bottom: 6px; }
.mcard .ram { font-size: 14px; color: #94A3B8; margin-bottom: 24px; }
.mcard .name { font-size: 38px; font-weight: 800; margin-bottom: 6px; }
.mcard .desc { font-size: 14px; color: #94A3B8; margin-bottom: 24px; }
.mcard .stat { font-size: 13px; color: #CBD5E1; margin: 4px 0; }
.mcard.accent {
  background: linear-gradient(160deg, #EC4899, #BE185D);
  box-shadow: 0 0 60px rgba(236, 72, 153, 0.3);
}
.mcard.accent .req, .mcard.accent .ram { color: rgba(255,255,255,0.7); }
.mcard.accent .name { color: #fff; }
.mcard.accent .desc, .mcard.accent .stat { color: #FCE7F3; }
.mcard .name.cyan { color: #22D3EE; }
.mcard .name.purple { color: #A78BFA; }
.foot { color: #64748B; font-size: 14px; margin-top: 30px; text-align: center; }
.foot code { background: #1E293B; padding: 3px 8px; border-radius: 4px; color: #22D3EE; font-family: 'JetBrains Mono', monospace; font-size: 12px; }
</style></head><body><div class="bg">
<div class="title">Który model uruchomić na MacBooku?</div>
<div class="subtitle">Trzy poziomy — od "działa wszędzie" do "maksimum"</div>
<div class="cards">
  <div class="mcard accent">
    <div class="req">BEZPIECZNY START</div>
    <div class="ram">≥ 8 GB RAM</div>
    <div class="name">Qwen 3</div>
    <div class="desc">8B parametrów</div>
    <div class="stat">~ 5 GB pobrania</div>
    <div class="stat">~ 30 sek / strona</div>
    <div class="stat">Działa na każdym M1+</div>
  </div>
  <div class="mcard">
    <div class="req">NAJLEPSZY POLSKI</div>
    <div class="ram">≥ 16 GB RAM</div>
    <div class="name cyan">Qwen 3.5</div>
    <div class="desc">9B, multimodal</div>
    <div class="stat">~ 6 GB pobrania</div>
    <div class="stat">~ 45 sek / strona</div>
    <div class="stat">Najnowszy z rodziny Qwen</div>
  </div>
  <div class="mcard">
    <div class="req">MAKSIMUM</div>
    <div class="ram">≥ 32 GB RAM</div>
    <div class="name purple">Qwen 3</div>
    <div class="desc">32B parametrów</div>
    <div class="stat">~ 20 GB pobrania</div>
    <div class="stat">~ 2 min / strona</div>
    <div class="stat">MBP Pro M3/M4 z 36 GB+</div>
  </div>
</div>
<div class="foot">Zmiana modelu = jedna komenda: <code>ollama pull qwen3.5:9b</code></div>
</div></body></html>
"""

# ============================================================
# IMAGE 4 — Prompt card (screenshotable)
# ============================================================
PROMPT_HTML = """
<!DOCTYPE html><html><head><meta charset="utf-8"><style>""" + BASE_CSS + """
.bg { padding: 48px; }
.wrap { width: 1100px; }
.label { font-size: 12px; letter-spacing: 2px; color: #EC4899; font-weight: 700; margin-bottom: 8px; }
.h1 { font-size: 32px; font-weight: 700; color: #F1F5F9; margin-bottom: 28px; }
.code {
  background: #131A2A;
  border: 1px solid rgba(236, 72, 153, 0.25);
  border-radius: 16px;
  padding: 32px 36px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 15px;
  line-height: 1.7;
  color: #E5E7EB;
  box-shadow: 0 0 40px rgba(236, 72, 153, 0.1);
}
.code .com { color: #64748B; }
.code .key { color: #22D3EE; font-weight: 600; }
.code .val { color: #FBCFE8; }
.foot { color: #64748B; font-size: 14px; margin-top: 20px; }
.foot strong { color: #EC4899; }
</style></head><body><div class="bg">
<div class="wrap">
  <div class="label">PROMPT DO ZAPISANIA</div>
  <div class="h1">Analiza transkrypcji spotkania → 4 sekcje</div>
  <div class="code">
<span class="com"># Wklej do Ollamy razem z transkrypcją</span><br><br>
Jesteś asystentem analizującym transkrypcje spotkań biznesowych.<br>
Przeanalizuj poniższą rozmowę i zwróć <span class="key">DOKŁADNIE</span> 4 sekcje:<br><br>
<span class="key">## 1. DECYZJE</span><br>
<span class="val">Co zostało ustalone? Lista punktów. Bez interpretacji.</span><br><br>
<span class="key">## 2. AKCJE</span><br>
<span class="val">Format: [KTO] — [CO] — [DO KIEDY]. Tylko konkrety.</span><br><br>
<span class="key">## 3. RYZYKA / OBIEKCJE</span><br>
<span class="val">Co zabrzmiało niewygodnie? Czego klient się obawia?</span><br><br>
<span class="key">## 4. TL;DR</span><br>
<span class="val">3–4 zdania. Tylko najważniejsze.</span><br><br>
<span class="com">Zasady: odpowiadaj po polsku. Nie wymyślaj cytatów.</span><br>
<span class="com">Jeśli czegoś nie ma w transkrypcji — napisz "brak danych".</span>
  </div>
  <div class="foot">Działa z każdym modelem. <strong>Skopiuj, wklej, zapisz</strong> jako swój standard.</div>
</div>
</div></body></html>
"""

# ============================================================
# IMAGE 5 — CTA card (recreated from Part 1 style)
# ============================================================
CTA_HTML = """
<!DOCTYPE html><html><head><meta charset="utf-8"><style>""" + BASE_CSS + """
.bg { padding: 56px; }
.card-cta {
  background: linear-gradient(160deg, #131A2A, #0F1422);
  border: 1px solid rgba(236, 72, 153, 0.25);
  border-radius: 22px;
  padding: 48px 56px;
  width: 1080px;
  box-shadow: 0 0 60px rgba(236, 72, 153, 0.08);
}
.label { font-size: 12px; letter-spacing: 2px; color: #EC4899; font-weight: 700; margin-bottom: 14px; }
.headline { font-size: 32px; font-weight: 700; color: #F1F5F9; line-height: 1.25; margin-bottom: 32px; }
.bullets { display: grid; grid-template-columns: 1fr 1fr; gap: 14px 28px; margin-bottom: 36px; }
.bullet { display: flex; align-items: center; gap: 12px; color: #CBD5E1; font-size: 15px; }
.bullet::before { content: '●'; color: #EC4899; font-size: 14px; }
.actions { display: flex; align-items: center; gap: 24px; }
.btn {
  background: linear-gradient(135deg, #EC4899, #BE185D);
  color: #fff;
  padding: 16px 28px;
  border-radius: 12px;
  font-weight: 700;
  font-size: 16px;
  display: inline-block;
  box-shadow: 0 8px 24px rgba(236, 72, 153, 0.35);
}
.sub { color: #94A3B8; font-size: 14px; }
</style></head><body><div class="bg">
<div class="card-cta">
  <div class="label">DLA TWOJEJ FIRMY</div>
  <div class="headline">Chcesz mieć analizę spotkań,<br>która nie wychodzi z Twojej firmy?</div>
  <div class="bullets">
    <div class="bullet">Whisper + Ollama lokalnie</div>
    <div class="bullet">Automatyczne podsumowania</div>
    <div class="bullet">Decyzje, akcje, ryzyka — w 4 sekcjach</div>
    <div class="bullet">Integracja z CRM / Slack / Notion</div>
    <div class="bullet">Zero abonamentów, zero chmury</div>
    <div class="bullet">Postawione i wdrożone u Ciebie</div>
  </div>
  <div class="actions">
    <div class="btn">Napisz do mnie</div>
    <div class="sub">Pomogę to postawić u Ciebie — od instalacji po integracje.</div>
  </div>
</div>
</div></body></html>
"""

# ============================================================
# IMAGE 0 — Cover (LinkedIn 1200x628 standard)
# ============================================================
COVER_HTML = """
<!DOCTYPE html><html><head><meta charset="utf-8"><style>""" + BASE_CSS + """
.bg {
  padding: 70px 80px;
  display: grid;
  grid-template-columns: 1.05fr 1fr;
  gap: 60px;
  align-items: center;
  background:
    radial-gradient(ellipse at top left, rgba(167, 139, 250, 0.10), transparent 55%),
    radial-gradient(ellipse at bottom right, rgba(236, 72, 153, 0.12), transparent 55%),
    #0B0F1A;
}
.left { display: flex; flex-direction: column; }
.badge {
  display: inline-block;
  background: linear-gradient(135deg, #EC4899, #BE185D);
  color: #fff;
  font-size: 12px;
  letter-spacing: 2px;
  font-weight: 700;
  padding: 8px 14px;
  border-radius: 8px;
  align-self: flex-start;
  margin-bottom: 28px;
}
.cover-h1 {
  font-size: 56px;
  font-weight: 800;
  line-height: 1.08;
  letter-spacing: -0.5px;
  margin-bottom: 24px;
}
.cover-h1 .l1 { color: #F1F5F9; display: block; }
.cover-h1 .l2 {
  background: linear-gradient(135deg, #22D3EE, #A78BFA);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: block;
}
.cover-sub { font-size: 18px; color: #94A3B8; line-height: 1.5; max-width: 460px; }
.author { margin-top: 48px; font-size: 14px; color: #64748B; }
.author strong { color: #CBD5E1; font-weight: 600; }
.steps { display: flex; flex-direction: column; gap: 12px; }
.step {
  display: flex;
  align-items: center;
  gap: 18px;
  background: linear-gradient(160deg, #131A2A, #0F1422);
  border: 1px solid rgba(148, 163, 184, 0.10);
  border-radius: 14px;
  padding: 16px 22px;
}
.step .num {
  width: 32px; height: 32px; border-radius: 8px;
  background: rgba(148, 163, 184, 0.10);
  color: #94A3B8;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 14px;
  flex-shrink: 0;
}
.step .lab { color: #CBD5E1; font-size: 16px; font-weight: 500; }
.step.hot {
  background: linear-gradient(135deg, #EC4899, #BE185D);
  border-color: rgba(236, 72, 153, 0.6);
  box-shadow: 0 0 50px rgba(236, 72, 153, 0.30);
}
.step.hot .num { background: rgba(255,255,255,0.20); color: #fff; }
.step.hot .lab { color: #fff; font-weight: 700; }
</style></head><body><div class="bg">
  <div class="left">
    <div class="badge">AI W PRACY · CZ. 2</div>
    <div class="cover-h1">
      <span class="l1">Analiza spotkań</span>
      <span class="l2">lokalnym modelem AI</span>
    </div>
    <div class="cover-sub">Ollama + Qwen 3&nbsp;/ Qwen 3.5. Decyzje, akcje, ryzyka<br>w&nbsp;4&nbsp;sekcjach. Bez ChatGPT, bez wysyłania transkrypcji w&nbsp;chmurę.</div>
    <div class="author"><strong>Kacper Sieradziński</strong> · dokodu.it</div>
  </div>
  <div class="steps">
    <div class="step"><div class="num">1</div><div class="lab">Transkrypcja (.txt z części 1)</div></div>
    <div class="step hot"><div class="num">2</div><div class="lab">Ollama — lokalny silnik LLM</div></div>
    <div class="step hot"><div class="num">3</div><div class="lab">Qwen 3 / Qwen 3.5</div></div>
    <div class="step"><div class="num">4</div><div class="lab">Prompt analityczny</div></div>
    <div class="step"><div class="num">5</div><div class="lab">Strukturyzowane notatki</div></div>
  </div>
</div></body></html>
"""

# ============================================================
# Render all
# ============================================================
SPECS = [
    ("00_cover.png", COVER_HTML, 1200, 628),
    ("01_pipeline.png", PIPELINE_HTML, 1500, 380),
    ("02_comparison.png", COMPARE_HTML, 1280, 880),
    ("03_models.png", MODELS_HTML, 1280, 700),
    ("04_prompt.png", PROMPT_HTML, 1280, 760),
    ("05_cta.png", CTA_HTML, 1280, 620),
]

def render():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for filename, html, w, h in SPECS:
            page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=2)
            page.set_content(html)
            page.wait_for_load_state("networkidle")
            out = OUT_DIR / filename
            page.screenshot(path=str(out), full_page=False, omit_background=False)
            print(f"OK  {filename}  ({w}x{h})")
            page.close()
        browser.close()

if __name__ == "__main__":
    render()
