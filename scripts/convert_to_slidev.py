#!/usr/bin/env python3
"""
Konwerter 02_Prezentacja.md → Slidev slides.md

Użycie:
  python3 convert_to_slidev.py Modul_01_Fundamenty
  python3 convert_to_slidev.py --all    # wszystkie moduły
  python3 convert_to_slidev.py Modul_01_Fundamenty --with-exercises
"""

import re
import sys
import os
import shutil

BASE = os.path.join(os.path.dirname(__file__), "../10_PROJECTS/PRJ_Kurs_n8n_Launch/MATERIALY_KURSU")
OUT_DIR = os.path.join(os.path.dirname(__file__), "../10_PROJECTS/PRJ_Kurs_n8n_Launch/SLIDEV")
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "../10_PROJECTS/PRJ_Kurs_n8n_Launch/SLIDEV/assets")

# ── Screenshot mapping: folder → {oryginalny tytuł slajdu → plik} ──
# Klucze to oryginalne tytuły slajdów (pre-normalizacja), wartości to ścieżki
# względem ASSETS_DIR. Screenshoty generowane przez n8n_screenshot.py.
SCREENSHOT_MAPPING = {
    'Modul_01_Fundamenty': {
        'Interfejs n8n — Mapa': 'screenshots/01_canvas_pusty.png',
        'Anatomia Node\'a — Szczegółowo': 'screenshots/02_node_library.png',
        'Webhook Trigger — Detale': 'screenshots/03_webhook_trigger.png',
    },
}

GLOBAL_FRONTMATTER = '''\
---
theme: default
titleTemplate: "%s | Dokodu"
highlighter: shiki
lineNumbers: false
drawings:
  persist: false
transition: slide-left
mdc: true
fonts:
  sans: Inter
  mono: Fira Code
css: style.css
---
'''

# ── Mermaid config injected after frontmatter ──────────────────
MERMAID_CONFIG = '''
<script setup>
import { useMermaid } from '@slidev/client'
</script>
'''

_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(_SCRIPTS_DIR, 'slidev_theme.css'), encoding='utf-8') as _f:
    CUSTOM_CSS = _f.read()


# ── Mermaid theme ──────────────────────────────────────────────
MERMAID_INIT = '''%%{init: {
  'theme': 'base',
  'themeVariables': {
    'primaryColor': '#0F2137',
    'primaryTextColor': '#ffffff',
    'primaryBorderColor': '#E63946',
    'lineColor': '#E63946',
    'secondaryColor': '#F8FAFC',
    'tertiaryColor': '#F1F5F9',
    'fontFamily': 'Inter'
  }
}}%%
'''

# ── ASCII art → Mermaid heuristics ─────────────────────────────
ASCII_DIAGRAM_CHARS = set('┌┐└┘│─┼╔╗╚╝║═├┤┬┴╠╣╦╩╬')

def is_ascii_diagram(code_text):
    """True jeśli blok kodu jest rysunkiem ASCII (nie prawdziwym kodem)"""
    diagram_chars = sum(1 for c in code_text if c in ASCII_DIAGRAM_CHARS)
    total = len(code_text.replace('\n','').replace(' ',''))
    if total == 0:
        return False
    ratio = diagram_chars / total
    # Min 3% box-drawing chars AND ma strzałki/kształty
    has_arrows = bool(re.search(r'[→←↑↓▶▼◀▲►◄]|──►|─►|→|<─', code_text))
    return ratio > 0.03 or (diagram_chars > 8 and has_arrows)

def ascii_to_mermaid(code_text, title=""):
    """
    Próbuje skonwertować prosty ASCII diagram do Mermaid.
    Zwraca (True, mermaid_code) lub (False, None) jeśli zbyt złożone.
    """
    lines = [l for l in code_text.strip().split('\n') if l.strip()]

    # Heurystyka: jeśli mamy wyraźne "strzałki między węzłami" na osobnych liniach
    # Format: TEXT → TEXT lub TEXT → TEXT → TEXT
    simple_flow = []
    for line in lines:
        clean = re.sub(r'[┌┐└┘│─┼╔╗╚╝║═├┤┬┴]', '', line).strip()
        clean = re.sub(r'\s+', ' ', clean)
        if '→' in clean or '──▶' in clean or '─►' in clean:
            simple_flow.append(clean)

    if len(simple_flow) >= 2:
        # Buduj flowchart z prostych linii ze strzałkami
        nodes = {}
        edges = []
        node_counter = [0]

        def get_node(label):
            label = label.strip().strip('[](){}')
            if not label:
                return None
            if label not in nodes:
                node_counter[0] += 1
                nodes[label] = f"N{node_counter[0]}"
            return nodes[label]

        for line in simple_flow:
            parts = re.split(r'\s*(?:→|──▶|─►)\s*', line)
            parts = [p.strip() for p in parts if p.strip()]
            for i in range(len(parts)-1):
                a = get_node(parts[i])
                b = get_node(parts[i+1])
                if a and b:
                    edges.append((a, parts[i], b, parts[i+1]))

        if edges:
            mermaid_lines = [MERMAID_INIT.strip(), 'flowchart LR']
            for a, alabel, b, blabel in edges:
                alabel_clean = alabel.replace('"', "'")[:40]
                blabel_clean = blabel.replace('"', "'")[:40]
                mermaid_lines.append(f'    {a}["{alabel_clean}"] --> {b}["{blabel_clean}"]')
            mermaid_lines.append('    classDef default fill:#0F2137,stroke:#E63946,color:#fff')
            return True, '\n'.join(mermaid_lines)

    return False, None


# ── Detekcja typów slajdów ─────────────────────────────────────
TAKEAWAY_PATTERNS = re.compile(
    r'^(Takeaway|Podsumowanie|Kluczowe wnioski|Zapamiętaj)', re.IGNORECASE
)

EXERCISE_PATTERNS = re.compile(
    r'(Ćwiczenie|Zadanie|Praktyka|Twój ruch|Hands-on)', re.IGNORECASE
)


def detect_slide_class(title):
    """Zwraca klasę CSS slajdu na podstawie tytułu, lub None."""
    if TAKEAWAY_PATTERNS.search(title):
        return 'layout-takeaway'
    if EXERCISE_PATTERNS.search(title):
        return 'layout-exercise'
    return None


# ── Parser ćwiczeń z 04_Cwiczenia.md ──────────────────────────
def parse_exercises(exercises_path):
    """
    Parsuje 04_Cwiczenia.md i zwraca listę slajdów exercise.
    Każde ## Ćwiczenie... / Zadanie Domowe staje się osobnym slajdem.
    """
    if not os.path.exists(exercises_path):
        return []

    with open(exercises_path, encoding='utf-8') as f:
        text = f.read()

    # Usuń frontmatter YAML
    text = re.sub(r'^---[\s\S]*?---\n', '', text)

    # Podziel na sekcje ## (Ćwiczenie, Zadanie Domowe)
    sections = re.split(r'(?=^## )', text, flags=re.MULTILINE)
    slides = []

    for section in sections:
        section = section.strip()
        if not section:
            continue

        m = re.match(r'^##\s+(.+)', section)
        if not m:
            continue

        title = m.group(1).strip()

        # Pomiń sekcje Troubleshooting — nie są ćwiczeniami
        if re.search(r'Troubleshooting', title, re.IGNORECASE):
            continue

        body_lines = []
        raw_body = section[m.end():].strip()

        # Wyciągnij metadata (Czas, Poziom, Czego się uczysz, Cel)
        time_m = re.search(r'\*\*Czas:\*\*\s*(.+)', raw_body)
        level_m = re.search(r'\*\*Poziom:\*\*\s*(.+)', raw_body)
        goal_m = re.search(r'\*\*Cel:\*\*\s*(.+)', raw_body)
        learns_m = re.search(r'\*\*Czego się uczysz:\*\*\s*(.+)', raw_body)

        if time_m:
            body_lines.append(f'**Czas:** {time_m.group(1).strip()}')
        if level_m:
            body_lines.append(f'**Poziom:** {level_m.group(1).strip()}')
        if learns_m:
            body_lines.append(f'**Czego się uczysz:** {learns_m.group(1).strip()}')
        if goal_m:
            body_lines.append('')
            body_lines.append(goal_m.group(1).strip())

        # Wyciągnij kroki (### Krok N) jako bullet pointy
        steps = re.findall(r'###\s+Krok\s+\d+\s*[—–-]\s*(.+)', raw_body)
        if steps:
            body_lines.append('')
            body_lines.append('## Kroki')
            for step in steps:
                body_lines.append(f'- {step.strip()}')

        # Wyciągnij checkpointy jeśli są
        checkpoints = re.findall(r'- \[[ x]\]\s+(.+)', raw_body)
        if checkpoints:
            body_lines.append('')
            body_lines.append('## Checkpointy')
            for cp in checkpoints:
                body_lines.append(f'- {cp.strip()}')

        body = '\n'.join(body_lines)
        slides.append({'title': title, 'body': body, 'note': ''})

    return slides


# ── Parser Markdown ────────────────────────────────────────────
def parse_slides(md_text):
    content = re.sub(r'^---[\s\S]*?---\n', '', md_text)
    blocks = content.split('\n---\n')
    slides = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        m = re.search(r'^##\s+Slajd\s+\d+:\s+(.+)|^#\s+(.+)', block, re.MULTILINE)
        if not m:
            continue
        title = (m.group(1) or m.group(2)).strip()

        note_m = re.search(r'>\s*🎙️\s*NOTATKA:\s*(.+)', block, re.DOTALL)
        note = ''
        if note_m:
            note = re.sub(r'\s+', ' ', note_m.group(1).strip().replace('\n>', ' '))

        body = block
        body = re.sub(r'^##\s+Slajd\s+\d+:\s+.+\n?', '', body, flags=re.MULTILINE)
        body = re.sub(r'^#\s+.+\n?', '', body, flags=re.MULTILINE)
        body = re.sub(r'>\s*🎙️\s*NOTATKA:[\s\S]*$', '', body)
        body = body.strip()
        slides.append({'title': title, 'body': body, 'note': note})
    return slides


def process_body(body):
    """Konwertuje **Section:** standalone linie → ## Section: (dla pill stylingu)"""
    lines = body.split('\n')
    result = []
    for line in lines:
        stripped = line.strip()
        # Standalone **bold text** lub **bold text:** → ## header
        if re.match(r'^\*\*[^*\n]+\*\*:?\s*$', stripped):
            text = re.sub(r'^\*\*([^*]+)\*\*:?\s*$', r'\1', stripped).rstrip(':')
            result.append(f'## {text}')
        else:
            result.append(line)
    return '\n'.join(result)


def process_code_blocks(body):
    """ASCII diagram code blocks → mermaid lub diagram-block div"""
    parts = re.split(r'(```[^\n]*\n[\s\S]*?```)', body)
    result = []
    for part in parts:
        if part.startswith('```'):
            # Wyciągnij język i treść
            m = re.match(r'```([^\n]*)\n([\s\S]*?)```', part)
            if not m:
                result.append(part)
                continue
            lang = m.group(1).strip().lower()
            code = m.group(2)

            # Czy to ASCII diagram (nie prawdziwy kod)?
            skip_langs = {'python', 'javascript', 'js', 'yaml', 'json',
                          'bash', 'sh', 'sql', 'typescript', 'ts', 'html', 'css'}
            if lang not in skip_langs and is_ascii_diagram(code):
                ok, mermaid_code = ascii_to_mermaid(code)
                if ok:
                    result.append(f'```mermaid\n{mermaid_code}\n```')
                else:
                    # Zostaw jako code block ale z klasą diagram
                    result.append(f'<div class="diagram-block">\n\n```\n{code}```\n\n</div>')
            else:
                result.append(part)
        else:
            result.append(part)
    return ''.join(result)


def detect_comparison(body):
    """
    True jeśli slajd ma dokładnie 2 sekcje ## Header + lista pod każdą.
    Zwraca (True, header1, items1, header2, items2) lub (False,...)
    """
    # Po process_body mamy już ## headery
    sections = re.split(r'^(##\s+.+)$', body, flags=re.MULTILINE)
    # sections = [pre, h1, body1, h2, body2, ...]
    if len(sections) < 5:
        return False, None, None, None, None

    # Zbierz sekcje nagłówek + treść
    pairs = []
    for i in range(1, len(sections)-1, 2):
        header = sections[i].strip()
        content = sections[i+1].strip() if i+1 < len(sections) else ''
        pairs.append((header, content))

    if len(pairs) != 2:
        return False, None, None, None, None

    # Obie sekcje muszą mieć listy
    for _, content in pairs:
        if not re.search(r'^\s*[-*]\s+', content, re.MULTILINE):
            return False, None, None, None, None

    return True, pairs[0][0], pairs[0][1], pairs[1][0], pairs[1][1]


def add_vclicks(body):
    """
    Wraps list blocks in <v-clicks> ONLY for slides z pojedynczą sekcją.
    Slajdy z 2+ nagłówkami ## pokazują wszystko naraz (bez animacji)
    — inaczej nagłówki sekcji wiszą w powietrzu przed pojawiem się list.
    """
    section_count = len(re.findall(r'^##\s+', body, re.MULTILINE))
    if section_count >= 2:
        # Multi-sekcja: pokaż wszystko od razu, bez animacji
        return body

    lines = body.split('\n')
    result = []
    in_list = False
    in_code = False
    list_buf = []

    def flush():
        if list_buf:
            result.extend(['', '<v-clicks>', ''])
            result.extend(list_buf)
            result.extend(['', '</v-clicks>', ''])
            list_buf.clear()

    for line in lines:
        if line.strip().startswith('```'):
            if in_list:
                flush()
                in_list = False
            in_code = not in_code
            result.append(line)
            continue
        if in_code:
            result.append(line)
            continue

        is_item = bool(re.match(r'^\s*[-*]\s+', line)) or bool(re.match(r'^\s*\d+\.\s+', line))
        if is_item:
            in_list = True
            list_buf.append(line)
        else:
            if in_list:
                flush()
                in_list = False
            result.append(line)

    if in_list:
        flush()

    return '\n'.join(result)


# ── Mermaid overrides: slajdy z diagramami ASCII → ładne flowcharty ──
MERMAID_THEME = '''%%{init: {'theme': 'base', 'themeVariables': {
  'primaryColor': '#1E2D40', 'primaryTextColor': '#A8D8EA',
  'primaryBorderColor': '#E63946', 'lineColor': '#E63946',
  'secondaryColor': '#0F2137', 'tertiaryColor': '#0A1628',
  'fontFamily': 'Inter', 'fontSize': '13px'
}}}%%
'''

def get_mermaid_overrides(folder_name):
    """
    Wizualne overrides dla kluczowych slajdów diagramowych.
    Używa Vue komponentów N8nFlow / N8nBranch z ikonami Iconify
    zamiast statycznych bloków kodu ASCII.
    """
    if folder_name == 'Modul_01_Fundamenty':
        return {

# ── Slajd 6: Interfejs n8n — Mapa ────────────────────────────
'Interfejs n8n — Mapa': '''\
<div style="background:#0A1628;border-radius:10px;overflow:hidden;border:1px solid rgba(255,255,255,0.08);box-shadow:0 8px 32px rgba(0,0,0,0.4);font-family:Inter,sans-serif;position:relative">

  <!-- Dot grid -->
  <div style="position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,0.04) 1px,transparent 1px);background-size:20px 20px;pointer-events:none"></div>

  <!-- Top bar -->
  <div style="position:relative;background:#0F2137;border-bottom:2px solid #E63946;padding:0.5rem 1rem;display:flex;align-items:center;gap:1.5rem">
    <div style="display:flex;align-items:center;gap:0.4rem">
      <div style="background:#E63946;color:#fff;font-weight:900;font-size:0.65rem;width:18px;height:18px;border-radius:3px;display:flex;align-items:center;justify-content:center">n</div>
      <span style="color:#fff;font-size:0.72rem;font-weight:700">n8n</span>
    </div>
    <div style="display:flex;gap:1rem">
      <span style="color:#A8D8EA;font-size:0.68rem;font-weight:600;border-bottom:2px solid #E63946;padding-bottom:2px">Workflows</span>
      <span style="color:#64748B;font-size:0.68rem">Credentials</span>
      <span style="color:#64748B;font-size:0.68rem">Executions</span>
      <span style="color:#64748B;font-size:0.68rem">Settings</span>
    </div>
    <div style="margin-left:auto;display:flex;gap:0.5rem">
      <span style="background:#1E2D40;color:#8096AA;font-size:0.6rem;padding:0.2rem 0.55rem;border-radius:4px;border:1px solid rgba(255,255,255,0.08)">Save</span>
      <span style="background:#1E2D40;color:#8096AA;font-size:0.6rem;padding:0.2rem 0.55rem;border-radius:4px;border:1px solid rgba(255,255,255,0.08)">Test</span>
      <span style="background:#22C55E;color:#fff;font-size:0.6rem;padding:0.2rem 0.55rem;border-radius:4px;font-weight:700">Activate</span>
    </div>
  </div>

  <!-- Main area -->
  <div style="position:relative;display:flex;gap:0;min-height:160px">

    <!-- Left panel — node library -->
    <div style="width:140px;flex-shrink:0;background:#0F2137;border-right:1px solid rgba(255,255,255,0.07);padding:0.6rem 0.7rem">
      <div style="color:#E63946;font-size:0.6rem;font-weight:700;letter-spacing:0.08em;margin-bottom:0.5rem">BIBLIOTEKA NODÓW</div>
      <div style="display:flex;flex-direction:column;gap:0.3rem">
        <div style="background:#1E2D40;border-radius:4px;padding:0.25rem 0.5rem;font-size:0.62rem;color:#A8D8EA;border-left:2px solid #F97316">⚡ Triggery</div>
        <div style="background:#1E2D40;border-radius:4px;padding:0.25rem 0.5rem;font-size:0.62rem;color:#A8D8EA;border-left:2px solid #3B82F6">⚙ Akcje</div>
        <div style="background:#1E2D40;border-radius:4px;padding:0.25rem 0.5rem;font-size:0.62rem;color:#A8D8EA;border-left:2px solid #8B5CF6">🔀 Logika</div>
        <div style="background:#1E2D40;border-radius:4px;padding:0.25rem 0.5rem;font-size:0.62rem;color:#A8D8EA;border-left:2px solid #64748B">🔗 HTTP / Code</div>
      </div>
    </div>

    <!-- Canvas -->
    <div style="flex:1;padding:1rem 1.2rem;display:flex;align-items:center;gap:0.6rem">
      <div style="background:#1E2D40;border-radius:6px;border:1px solid rgba(255,255,255,0.08);border-top:2px solid #F97316;padding:0.4rem 0.7rem;text-align:center;min-width:72px">
        <div style="font-size:0.6rem;color:#F97316;font-weight:700">WEBHOOK</div>
        <div style="font-size:0.55rem;color:#64748B;margin-top:2px">Trigger</div>
      </div>
      <svg width="28" height="8" viewBox="0 0 28 8"><line x1="0" y1="4" x2="20" y2="4" stroke="#E63946" stroke-width="1.5" stroke-dasharray="3 2"/><polygon points="20,1 28,4 20,7" fill="#E63946"/></svg>
      <div style="background:#1E2D40;border-radius:6px;border:1px solid rgba(255,255,255,0.08);border-top:2px solid #3B82F6;padding:0.4rem 0.7rem;text-align:center;min-width:72px">
        <div style="font-size:0.6rem;color:#3B82F6;font-weight:700">IF NODE</div>
        <div style="font-size:0.55rem;color:#64748B;margin-top:2px">Logika</div>
      </div>
      <svg width="28" height="8" viewBox="0 0 28 8"><line x1="0" y1="4" x2="20" y2="4" stroke="#E63946" stroke-width="1.5" stroke-dasharray="3 2"/><polygon points="20,1 28,4 20,7" fill="#E63946"/></svg>
      <div style="background:#1E2D40;border-radius:6px;border:1px solid rgba(255,255,255,0.08);border-top:2px solid #22C55E;padding:0.4rem 0.7rem;text-align:center;min-width:72px">
        <div style="font-size:0.6rem;color:#22C55E;font-weight:700">GMAIL</div>
        <div style="font-size:0.55rem;color:#64748B;margin-top:2px">Wyślij</div>
      </div>
      <div style="margin-left:auto;background:#0F2137;border-radius:6px;padding:0.5rem 0.8rem;font-size:0.6rem;color:#64748B;border:1px dashed rgba(255,255,255,0.1);text-align:center">
        <div style="color:#A8D8EA;font-weight:600;margin-bottom:2px">CANVAS</div>
        <div>przeciągnij nody</div>
        <div>z biblioteki →</div>
      </div>
    </div>
  </div>

  <!-- Bottom bar -->
  <div style="position:relative;background:#0F2137;border-top:1px solid rgba(255,255,255,0.07);padding:0.4rem 1rem;display:flex;align-items:center;gap:1.5rem">
    <span style="color:#22C55E;font-size:0.62rem;font-weight:600">✓ Executions: 14 total</span>
    <span style="color:#64748B;font-size:0.6rem">Last: 2 min ago</span>
    <div style="margin-left:auto;display:flex;gap:1rem">
      <span style="color:#8096AA;font-size:0.6rem">← Execution log</span>
      <span style="color:#8096AA;font-size:0.6rem">Settings →</span>
    </div>
  </div>
</div>
''',

# ── Slajd 9: Triggery ─────────────────────────────────────────
'Triggery — Kiedy Workflow Startuje': '''\
<N8nBranch
  :source="{icon: 'mdi:lightning-bolt', label: 'TRIGGER', desc: 'zawsze 1 na workflow'}"
  :branches="[
    {icon: 'mdi:cursor-default-click', label: 'MANUAL', desc: 'Klikasz Test btn', result: 'Testowanie', variant: 'action'},
    {icon: 'mdi:clock-time-four-outline', label: 'SCHEDULE', desc: 'Co 5 min / Każdy pn', result: 'Cykliczne zadania', variant: 'default'},
    {icon: 'mdi:webhook', label: 'WEBHOOK', desc: 'HTTP POST z zewnątrz', result: 'Reaktywne odpowiedzi', variant: 'trigger'},
  ]"
/>

<div style="margin-top:0.8rem;font-size:0.78rem;color:#64748B">
Są też triggery aplikacyjne — np. <strong>nowy email w Gmail</strong>, <strong>nowa karta Trello</strong>. Ale te trzy to fundament.
</div>
''',

# ── Slajd 15: IF Node ──────────────────────────────────────────
'IF Node — Logika Warunkowa': '''\
**Typy warunków:** String (contains, equals, regex) · Number (>, <, =) · Boolean · Date

<N8nFlow
  :nodes="[
    {icon: 'mdi:database-arrow-right', label: 'INPUT', desc: 'dane z poprzedniego node', variant: 'default'},
    {icon: 'mdi:source-branch', label: 'IF Node', desc: 'warunek spełniony?', variant: 'trigger'},
    {icon: 'mdi:check-circle', label: 'TRUE', desc: 'dalsze działanie', variant: 'output'},
  ]"
/>

<div style="margin-top:0.6rem;display:flex;gap:0.8rem;align-items:center">
  <div style="background:#1E2D40;border-left:3px solid #EF4444;padding:0.4rem 0.8rem;border-radius:0 6px 6px 0;font-size:0.78rem;color:#A8D8EA">
    <strong style="color:#EF4444">FALSE branch</strong> → obsługa błędu / odrzucenie
  </div>
  <div style="font-size:0.72rem;color:#64748B">💡 Zawsze podłącz OBIE gałęzie!</div>
</div>
''',

# ── Slajd 16: Switch ───────────────────────────────────────────
'Switch Node — Wielokrotne Rozgałęzienie': '''\
**Użycie:** gdy masz więcej niż 2 ścieżki. Zawsze dodaj **Default** case.

<N8nBranch
  :source="{icon: 'mdi:source-branch', label: 'Switch Node', desc: 'wartość: typ_leadu'}"
  :branches="[
    {icon: 'mdi:account-plus', label: 'lead', result: 'zapisz lead', variant: 'action'},
    {icon: 'mdi:account-check', label: 'klient', result: 'aktualizuj CRM', variant: 'action'},
    {icon: 'mdi:cancel', label: 'spam', result: 'ignoruj', variant: 'default'},
    {icon: 'mdi:email-alert', label: 'Default', result: 'email do admina', variant: 'trigger'},
  ]"
/>
''',

# ── Slajd 26: Lead Capture Architecture ───────────────────────
'Lead Capture System — Architektura': '''\
<N8nFlow
  :nodes="[
    {icon: 'mdi:form-select', label: 'FORMULARZ', desc: 'landing page', variant: 'default'},
    {icon: 'mdi:webhook', label: 'Webhook', desc: 'Trigger', variant: 'trigger'},
    {icon: 'mdi:check-decagram', label: 'Walidacja', desc: 'email + pola', variant: 'default'},
    {icon: 'logos:google-sheets', label: 'Sheets', desc: 'Append Row', variant: 'action'},
    {icon: 'logos:gmail', label: 'Gmail', desc: 'Email powitalny', variant: 'action'},
    {icon: 'logos:slack-icon', label: 'Slack', desc: '#leady notify', variant: 'output'},
  ]"
  caption="Każdy krok ma odpowiedź HTTP — klient nie widzi błędów, admin dostaje alerty"
/>
''',

# ── Slajd 22: Error Handling Flow ─────────────────────────────
'Flow Error Handling — Diagram': '''\
<N8nFlow
  :nodes="[
    {icon: 'mdi:webhook', label: 'Webhook', variant: 'trigger'},
    {icon: 'mdi:check-circle', label: 'Walidacja', variant: 'default'},
    {icon: 'logos:google-sheets', label: 'Sheets', variant: 'action'},
    {icon: 'logos:gmail', label: 'Gmail', variant: 'action'},
    {icon: 'mdi:source-branch', label: 'IF: error?', variant: 'default'},
  ]"
/>

<div style="margin-top:0.8rem;background:#1E2D40;border-radius:8px;padding:0.8rem 1rem;border-left:3px solid #EF4444;font-size:0.8rem">
  <strong style="color:#EF4444">Error Workflow (oddzielny)</strong>
  <span style="color:#8096AA"> → Error Trigger → </span>
  <span style="color:#A8D8EA">Gmail do admina + Slack #alerty</span>
</div>
''',

        }

    if folder_name == 'Modul_02_API_i_Dane':
        return {

# ── Slajd 13: Vibe Coding Flow ──────────────────────────────────
'Vibe Coding — Flow AI + n8n': '''\
<N8nFlow
  :nodes="[
    {icon: 'mdi:text-box-outline', label: 'OPISZ PROBLEM', desc: 'co chcesz osiągnąć', variant: 'default'},
    {icon: 'mdi:robot-outline', label: 'ZAPYTAJ AI', desc: 'wejście + wyjście + kontekst', variant: 'action'},
    {icon: 'mdi:play-circle-outline', label: 'WKLEJ I TESTUJ', desc: 'Code Node → Test Step', variant: 'output'},
    {icon: 'mdi:refresh', label: 'ITERUJ', desc: 'wklej błąd → popraw', variant: 'error'},
  ]"
  caption="Vibe Coding: AI jako junior developer — opisujesz, AI pisze, ty testujesz i iterujesz"
/>
''',

# ── Slajd 16: Item Lists ─────────────────────────────────────────
'Item Lists — Split, Aggregate, Merge': '''\
<N8nBranch
  :source="{icon: 'mdi:database', label: 'DANE', desc: '1 item z tablicą'}"
  :branches="[
    {icon: 'mdi:arrow-split-vertical', label: 'Split Out', result: '1 → wiele itemów', variant: 'action'},
    {icon: 'mdi:arrow-collapse-vertical', label: 'Aggregate', result: 'wiele → 1 item', variant: 'output'},
  ]"
/>

<div style="margin-top:0.8rem;background:#1E2D40;border-radius:8px;padding:0.8rem 1rem;border-left:3px solid #3B82F6;font-size:0.8rem">
  <strong style="color:#3B82F6">Pattern:</strong>
  <span style="color:#A8D8EA"> Split → przetwórz każdy element → Aggregate → wyślij batch</span>
</div>
''',

# ── Slajd 19: Data Enrichment Architektura ────────────────────────
'Architektura Projektu — Data Enrichment': '''\
<N8nFlow
  :nodes="[
    {icon: 'mdi:webhook', label: 'Webhook', desc: 'POST {nip}', variant: 'trigger'},
    {icon: 'mdi:text-search', label: 'Normalize NIP', desc: 'Code Node', variant: 'default'},
    {icon: 'mdi:cached', label: 'Cache Check', desc: 'Sheets Lookup', variant: 'action'},
    {icon: 'mdi:api', label: 'GUS API', desc: 'HTTP Request', variant: 'action'},
    {icon: 'mdi:code-braces', label: 'Parse XML→JSON', desc: 'Code Node', variant: 'default'},
    {icon: 'logos:google-sheets', label: 'Save', desc: 'Sheets Append', variant: 'output'},
  ]"
  caption="Cache sprawdza czy NIP już był — jeśli tak, zwraca dane z Sheets bez odpytywania GUS"
/>
''',

        }

    if folder_name == 'Modul_03_Skalowalnosc':
        return {

# ── Slajd 8: Batching diagram ────────────────────────────────────
'DIAGRAM — Co się dzieje bez vs z Batchingiem': '''\
<N8nBranch
  :source="{icon: 'mdi:database-outline', label: '1000 rekordów', desc: 'do przetworzenia'}"
  :branches="[
    {icon: 'mdi:alert-circle', label: 'BEZ batching', result: 'Timeout / Crash → 0 zapisane', variant: 'error'},
    {icon: 'mdi:checkbox-multiple-marked', label: 'Z batchingiem', result: 'Batch 1-6 ✅ — Batch 7 ❌ retry', variant: 'output'},
  ]"
/>

<div style="margin-top:0.8rem;background:#1E2D40;border-radius:8px;padding:0.8rem 1rem;border-left:3px solid #22C55E;font-size:0.8rem">
  <strong style="color:#22C55E">Checkpoint:</strong>
  <span style="color:#A8D8EA"> Z batchingiem błąd to problem lokalny, nie katastrofa globalna</span>
</div>
''',

# ── Slajd 10: Idempotency Flow ───────────────────────────────────
'DIAGRAM — Idempotency Flow': '''\
<N8nFlow
  :nodes="[
    {icon: 'mdi:webhook', label: 'Webhook', desc: 'order_id: ORD-12345', variant: 'trigger'},
    {icon: 'mdi:magnify', label: 'Sprawdź', desc: 'czy już przetworzone?', variant: 'default'},
    {icon: 'mdi:source-branch', label: 'IF', desc: 'istnieje?', variant: 'default'},
  ]"
/>

<div style="margin-top:0.6rem;display:flex;gap:0.8rem">
  <div style="background:#1E2D40;border-left:3px solid #22C55E;padding:0.5rem 0.8rem;border-radius:0 6px 6px 0;flex:1">
    <div style="color:#22C55E;font-weight:700;font-size:0.75rem">NIE ISTNIEJE</div>
    <div style="color:#A8D8EA;font-size:0.72rem;margin-top:2px">Wykonaj → Oznacz → Zwróć 200</div>
  </div>
  <div style="background:#1E2D40;border-left:3px solid #F97316;padding:0.5rem 0.8rem;border-radius:0 6px 6px 0;flex:1">
    <div style="color:#F97316;font-weight:700;font-size:0.75rem">JUŻ ISTNIEJE</div>
    <div style="color:#A8D8EA;font-size:0.72rem;margin-top:2px">Pomiń → Zwróć 200 (bez działania)</div>
  </div>
</div>
''',

# ── Slajd 12: Error Trigger Architektura ─────────────────────────
'Error Trigger — Architektura': '''\
<N8nBranch
  :source="{icon: 'mdi:alert-octagon', label: 'Error Trigger', desc: 'jeden globalny handler'}"
  :branches="[
    {icon: 'logos:google-sheets', label: 'Log do Sheets', result: 'pełna historia błędów', variant: 'action'},
    {icon: 'logos:slack-icon', label: 'Alert Slack', result: '#n8n-alerts', variant: 'output'},
    {icon: 'mdi:ticket-outline', label: 'Ticket', result: 'Jira / Asana', variant: 'action'},
  ]"
/>

<div style="margin-top:0.8rem;background:#1E2D40;border-radius:8px;padding:0.8rem 1rem;border-left:3px solid #E63946;font-size:0.8rem">
  <strong style="color:#E63946">Zasada:</strong>
  <span style="color:#A8D8EA"> Jeden Error Workflow obsługuje WSZYSTKIE workflow produkcyjne</span>
</div>
''',

        }

    if folder_name == 'Modul_04_Architektura_Modularna':
        return {

# ── Slajd 5: Modularna architektura (PO) ─────────────────────────
'Problem — Spaghetti Workflow (PO)': '''\
<N8nFlow
  :nodes="[
    {icon: 'mdi:webhook', label: 'Webhook', desc: 'trigger', variant: 'trigger'},
    {icon: 'mdi:robot-outline', label: 'AI Classifier', desc: 'GPT-4o-mini', variant: 'action'},
    {icon: 'mdi:source-branch', label: 'Switch', desc: 'route by category', variant: 'default'},
  ]"
/>

<N8nBranch
  :source="{icon: 'mdi:source-branch', label: 'Switch', desc: 'kategoria zgłoszenia'}"
  :branches="[
    {icon: 'mdi:monitor', label: 'IT Support', result: 'Execute: WF_IT', variant: 'action'},
    {icon: 'mdi:account-group', label: 'HR', result: 'Execute: WF_HR', variant: 'action'},
    {icon: 'mdi:currency-usd', label: 'Finance', result: 'Execute: WF_FIN', variant: 'action'},
    {icon: 'mdi:handshake', label: 'Sales', result: 'Execute: WF_SAL', variant: 'output'},
    {icon: 'mdi:help-circle', label: 'Other', result: 'Human Review', variant: 'default'},
  ]"
/>
''',

# ── Slajd 9: Master-Subworkflow ──────────────────────────────────
'Architektura Master-Subworkflow': '''\
<N8nFlow
  :nodes="[
    {icon: 'mdi:webhook', label: 'Trigger', desc: 'wejście', variant: 'trigger'},
    {icon: 'mdi:text-search', label: 'Parse', desc: 'normalizuj', variant: 'default'},
    {icon: 'mdi:robot-outline', label: 'Classify', desc: 'AI kategoryzacja', variant: 'action'},
    {icon: 'mdi:source-branch', label: 'Switch', desc: 'routing', variant: 'default'},
    {icon: 'mdi:call-merge', label: 'Merge', desc: 'zbierz wyniki', variant: 'action'},
    {icon: 'mdi:email-check', label: 'Confirm', desc: 'email z ticket_id', variant: 'output'},
  ]"
  caption="Master orchestruje — subworkflows wykonują. Komunikacja przez JSON in/out."
/>
''',

# ── Slajd 21: Projekt tygodnia ───────────────────────────────────
'Projekt tygodnia — Architektura': '''\
<N8nFlow
  :nodes="[
    {icon: 'mdi:email-outline', label: 'Email / Form', desc: 'Webhook trigger', variant: 'trigger'},
    {icon: 'mdi:text-search', label: 'Parse', desc: 'normalize input', variant: 'default'},
    {icon: 'mdi:robot-outline', label: 'AI Classify', desc: 'GPT-4o-mini', variant: 'action'},
    {icon: 'mdi:source-branch', label: 'Switch', desc: 'route by category', variant: 'default'},
  ]"
/>

<N8nBranch
  :source="{icon: 'mdi:source-branch', label: 'Switch', desc: '5 kategorii'}"
  :branches="[
    {icon: 'mdi:monitor', label: 'IT', result: 'Jira Ticket + Email IT', variant: 'action'},
    {icon: 'mdi:account-group', label: 'HR', result: 'Sheets + Email HR', variant: 'action'},
    {icon: 'mdi:currency-usd', label: 'Finance', result: 'Sheets + Email CFO', variant: 'action'},
    {icon: 'mdi:handshake', label: 'Sales', result: 'CRM + Slack', variant: 'output'},
    {icon: 'mdi:help-circle', label: 'Other', result: 'Human Review Queue', variant: 'default'},
  ]"
/>
''',

        }

    if folder_name == 'Modul_05_AI_Human_in_Loop':
        return {

# ── Slajd 4: AI Agent Node ───────────────────────────────────────
'AI Agent Node — czym jest?': '''\
<N8nFlow
  :nodes="[
    {icon: 'mdi:message-text', label: 'INPUT', desc: 'polecenie użytkownika', variant: 'default'},
    {icon: 'mdi:brain', label: 'LLM', desc: 'rozumie cel', variant: 'action'},
    {icon: 'mdi:wrench', label: 'TOOL', desc: 'wykonuje akcję', variant: 'trigger'},
    {icon: 'mdi:brain', label: 'LLM', desc: 'cel osiągnięty?', variant: 'action'},
    {icon: 'mdi:check-circle', label: 'OUTPUT', desc: 'wynik końcowy', variant: 'output'},
  ]"
  caption="ReAct pattern: LLM → wybierz tool → wykonaj → sprawdź → powtórz lub zakończ"
/>
''',

# ── Slajd 11: Human-in-the-Loop Flow ─────────────────────────────
'Diagram — Human-in-the-Loop Flow': '''\
<N8nFlow
  :nodes="[
    {icon: 'mdi:webhook', label: 'Trigger', desc: 'polecenie', variant: 'trigger'},
    {icon: 'mdi:robot-outline', label: 'AI Agent', desc: 'interpretuje + drafts', variant: 'action'},
    {icon: 'mdi:shield-check', label: 'Validation', desc: 'JSON Schema check', variant: 'default'},
    {icon: 'logos:slack-icon', label: 'Slack', desc: 'wyślij do managera', variant: 'action'},
    {icon: 'mdi:timer-sand', label: 'WAIT', desc: 'czekaj na approval', variant: 'default'},
  ]"
/>

<div style="margin-top:0.6rem;display:flex;gap:0.6rem">
  <div style="background:#1E2D40;border-left:3px solid #22C55E;padding:0.4rem 0.7rem;border-radius:0 6px 6px 0;flex:1">
    <div style="color:#22C55E;font-weight:700;font-size:0.72rem">✅ Zatwierdź</div>
    <div style="color:#A8D8EA;font-size:0.68rem">Wykonaj + Zaloguj</div>
  </div>
  <div style="background:#1E2D40;border-left:3px solid #EF4444;padding:0.4rem 0.7rem;border-radius:0 6px 6px 0;flex:1">
    <div style="color:#EF4444;font-weight:700;font-size:0.72rem">❌ Anuluj</div>
    <div style="color:#A8D8EA;font-size:0.68rem">Zaloguj anulowanie</div>
  </div>
  <div style="background:#1E2D40;border-left:3px solid #F97316;padding:0.4rem 0.7rem;border-radius:0 6px 6px 0;flex:1">
    <div style="color:#F97316;font-weight:700;font-size:0.72rem">✏️ Edytuj</div>
    <div style="color:#A8D8EA;font-size:0.68rem">Modal → Nowa wersja</div>
  </div>
</div>
''',

# ── Slajd 23: Slack Approval Bot Architektura ────────────────────
'Architektura Slack Approval Bot — 3 Workflows': '''\
<N8nFlow
  :nodes="[
    {icon: 'logos:slack-icon', label: 'Slack Trigger', desc: 'wiadomość', variant: 'trigger'},
    {icon: 'mdi:robot-outline', label: 'AI Agent', desc: 'GPT-4o + 3 tools', variant: 'action'},
    {icon: 'mdi:shield-check', label: 'Validate', desc: 'Code Node', variant: 'default'},
    {icon: 'logos:slack-icon', label: 'Slack Buttons', desc: '✅ ❌ ✏️', variant: 'output'},
    {icon: 'mdi:timer-sand', label: 'WAIT', desc: 'timeout 24h', variant: 'default'},
  ]"
  caption="WF1: Listener → WF2: Approval Handler → WF3: Timeout Handler"
/>
''',

        }

    if folder_name == 'Modul_06_Autonomous_Agents':
        return {

# ── Slajd 3: Projekt — Supervisor + Workers ──────────────────────
'Co zbudujesz w tym tygodniu': '''\
<N8nBranch
  :source="{icon: 'mdi:shield-crown', label: 'Supervisor Agent', desc: 'GPT-4o — dekompozycja + synteza'}"
  :branches="[
    {icon: 'mdi:magnify', label: 'Research', result: 'web + KRS + scraping', variant: 'action'},
    {icon: 'mdi:target', label: 'ICP Fit', result: 'score + reasoning', variant: 'output'},
    {icon: 'mdi:handshake', label: 'Sales Strategy', result: 'pitch + pytania', variant: 'trigger'},
  ]"
/>

<div style="margin-top:0.8rem;background:#1E2D40;border-radius:8px;padding:0.8rem 1rem;border-left:3px solid #22C55E;font-size:0.8rem">
  <strong style="color:#22C55E">Output:</strong>
  <span style="color:#A8D8EA"> Raport PDF/MD — profil firmy + ICP score + pitch sprzedażowy</span>
  <span style="color:#64748B"> (~0,80 PLN per analiza)</span>
</div>
''',

# ── Slajd 20: Multi-Agent Architecture ───────────────────────────
'Multi-Agent Architecture — Diagram': '''\
<N8nBranch
  :source="{icon: 'mdi:shield-crown', label: 'SUPERVISOR', desc: 'GPT-4o, temp: 0.1'}"
  :branches="[
    {icon: 'mdi:magnify', label: 'Worker 1: Research', result: 'GPT-4o — fakty', variant: 'action'},
    {icon: 'mdi:target', label: 'Worker 2: ICP Fit', result: 'Claude 3.5 — analiza', variant: 'output'},
    {icon: 'mdi:chart-line', label: 'Worker 3: Sales', result: 'Claude 3.5 — strategia', variant: 'trigger'},
  ]"
/>

<div style="margin-top:0.8rem;background:#1E2D40;border-radius:8px;padding:0.8rem 1rem;border-left:3px solid #8B5CF6;font-size:0.8rem">
  <strong style="color:#8B5CF6">Supervisor zbiera wyniki</strong>
  <span style="color:#A8D8EA"> → synteza w finalny raport. Różne modele dla różnych workerów.</span>
</div>
''',

# ── Slajd 32: B2B Lead Analyst Architektura ──────────────────────
'Projekt — B2B Lead Analyst Overview': '''\
<N8nFlow
  :nodes="[
    {icon: 'logos:gmail', label: 'Gmail / CRM', desc: 'trigger', variant: 'trigger'},
    {icon: 'mdi:text-search', label: 'Extract', desc: 'nazwa, NIP, URL', variant: 'default'},
    {icon: 'mdi:shield-crown', label: 'Supervisor', desc: 'GPT-4o', variant: 'action'},
  ]"
/>

<N8nBranch
  :source="{icon: 'mdi:shield-crown', label: 'Supervisor', desc: 'deleguje zadania'}"
  :branches="[
    {icon: 'mdi:magnify', label: 'Research', result: 'web + KRS', variant: 'action'},
    {icon: 'mdi:target', label: 'ICP Fit', result: 'score 1-10', variant: 'output'},
    {icon: 'mdi:chart-line', label: 'Sales', result: 'pitch + questions', variant: 'trigger'},
  ]"
/>

<div style="margin-top:0.6rem;display:flex;gap:0.5rem;justify-content:center">
  <div style="background:#1E2D40;border-top:2px solid #22C55E;padding:0.3rem 0.7rem;border-radius:6px;font-size:0.68rem;color:#A8D8EA;text-align:center">
    <div style="color:#22C55E;font-weight:700">Gmail draft</div>
  </div>
  <div style="background:#1E2D40;border-top:2px solid #3B82F6;padding:0.3rem 0.7rem;border-radius:6px;font-size:0.68rem;color:#A8D8EA;text-align:center">
    <div style="color:#3B82F6;font-weight:700">HubSpot contact</div>
  </div>
  <div style="background:#1E2D40;border-top:2px solid #F97316;padding:0.3rem 0.7rem;border-radius:6px;font-size:0.68rem;color:#A8D8EA;text-align:center">
    <div style="color:#F97316;font-weight:700">Slack alert</div>
  </div>
</div>
''',

        }

    if folder_name == 'Modul_07_RAG':
        return {

# ── Slajd 6: RAG Pipeline ────────────────────────────────────────
'RAG Pipeline — pełny diagram': '''\
<div style="display:flex;gap:1.2rem;align-items:flex-start">
  <div style="flex:1">
    <div style="color:#F97316;font-weight:700;font-size:0.78rem;margin-bottom:0.5rem">INGEST (jednorazowo)</div>
    <N8nFlow
      :nodes="[
        {icon: 'mdi:file-document', label: 'Dokumenty', variant: 'default'},
        {icon: 'mdi:content-cut', label: 'Chunking', desc: '500 tokenów', variant: 'action'},
        {icon: 'mdi:vector-point', label: 'Embeddings', desc: 'ada-002', variant: 'action'},
        {icon: 'mdi:database', label: 'Qdrant', desc: 'Vector DB', variant: 'output'},
      ]"
    />
  </div>
  <div style="flex:1">
    <div style="color:#3B82F6;font-weight:700;font-size:0.78rem;margin-bottom:0.5rem">QUERY (każde pytanie)</div>
    <N8nFlow
      :nodes="[
        {icon: 'mdi:help-circle', label: 'Pytanie', variant: 'trigger'},
        {icon: 'mdi:magnify', label: 'Search', desc: 'Top-K chunks', variant: 'action'},
        {icon: 'mdi:brain', label: 'LLM', desc: 'prompt + chunks', variant: 'action'},
        {icon: 'mdi:message-text', label: 'Odpowiedź', desc: 'z cytatami!', variant: 'output'},
      ]"
    />
  </div>
</div>
''',

# ── Slajd 18: Ingestion Workflow ──────────────────────────────────
'Ingestion Workflow #1 — architektura': '''\
<N8nFlow
  :nodes="[
    {icon: 'logos:google-drive', label: 'Drive Trigger', desc: 'nowy plik', variant: 'trigger'},
    {icon: 'mdi:download', label: 'Download', desc: 'pobierz plik', variant: 'default'},
    {icon: 'mdi:file-document-outline', label: 'Extract Text', desc: 'PDF/DOCX → text', variant: 'action'},
    {icon: 'mdi:content-cut', label: 'Chunker', desc: '500 tok, 50 overlap', variant: 'action'},
    {icon: 'mdi:vector-point', label: 'Embeddings', desc: 'text-embedding-3-small', variant: 'action'},
    {icon: 'mdi:database-plus', label: 'Qdrant Insert', desc: '+ metadane', variant: 'output'},
  ]"
  caption="Automatyczny pipeline: nowy plik na Drive → chunki + embeddingi → baza wektorowa"
/>
''',

# ── Slajd 21: Query Workflow ─────────────────────────────────────
'Query Workflow #2 — architektura': '''\
<N8nFlow
  :nodes="[
    {icon: 'logos:slack-icon', label: 'Slack / Webhook', desc: 'pytanie', variant: 'trigger'},
    {icon: 'mdi:vector-point', label: 'Embed pytanie', desc: 'text-emb-3-small', variant: 'default'},
    {icon: 'mdi:database-search', label: 'Qdrant Retrieve', desc: 'top 5, score > 0.75', variant: 'action'},
    {icon: 'mdi:sort-ascending', label: 'Reranker', desc: 'opcjonalny', variant: 'default'},
    {icon: 'mdi:brain', label: 'AI Agent', desc: 'TYLKO z fragmentów', variant: 'action'},
    {icon: 'logos:slack-icon', label: 'Odpowiedź', desc: 'z cytatami + źródło', variant: 'output'},
  ]"
  caption="Guardrail: score < 0.65 → 'Nie znalazłem tej informacji' (bez halucynacji)"
/>
''',

        }

    if folder_name == 'Modul_00_Filozofia':
        return {

# ── Slajd 15: Framework trigger → akcja → warunek ───────────────
'Diagram — framework trigger → akcja → warunek': '''\
<N8nBranch
  :source="{icon: 'mdi:lightning-bolt', label: 'TRIGGER', desc: 'co uruchamia workflow?'}"
  :branches="[
    {icon: 'mdi:cog', label: 'AKCJA', desc: 'co workflow robi?', result: 'email, zapis, API call', variant: 'action'},
  ]"
/>

<div style="margin-top:0.6rem;display:flex;gap:0.8rem;align-items:center;justify-content:center">
  <div style="background:#1E2D40;border-radius:8px;padding:0.6rem 1rem;border-top:2px solid #F97316;text-align:center">
    <div style="color:#F97316;font-weight:700;font-size:0.78rem">WARUNEK (IF)</div>
    <div style="color:#8096AA;font-size:0.68rem">czy spełniony X?</div>
  </div>
  <div style="display:flex;flex-direction:column;gap:0.4rem">
    <div style="background:#1E2D40;border-left:3px solid #22C55E;padding:0.35rem 0.7rem;border-radius:0 6px 6px 0">
      <span style="color:#22C55E;font-weight:700;font-size:0.72rem">TAK →</span>
      <span style="color:#A8D8EA;font-size:0.68rem"> Akcja A</span>
    </div>
    <div style="background:#1E2D40;border-left:3px solid #EF4444;padding:0.35rem 0.7rem;border-radius:0 6px 6px 0">
      <span style="color:#EF4444;font-weight:700;font-size:0.72rem">NIE →</span>
      <span style="color:#A8D8EA;font-size:0.68rem"> Akcja B</span>
    </div>
  </div>
</div>
''',

# ── Slajd 16: Przykład procesu — obsługa leada ──────────────────
'Przykład procesu rozłożonego na trigger/akcja/warunek': '''\
<N8nFlow
  :nodes="[
    {icon: 'mdi:form-select', label: 'Formularz', desc: 'wypełniony na stronie', variant: 'trigger'},
    {icon: 'logos:google-sheets', label: 'Arkusz / CRM', desc: 'zapisz dane', variant: 'action'},
    {icon: 'logos:gmail', label: 'Email', desc: 'powitalny do klienta', variant: 'action'},
    {icon: 'mdi:source-branch', label: 'IF', desc: 'budżet > 10k?', variant: 'default'},
  ]"
  animated
/>

<div style="margin-top:0.6rem;display:flex;gap:0.8rem">
  <div style="background:#1E2D40;border-left:3px solid #22C55E;padding:0.5rem 0.8rem;border-radius:0 6px 6px 0;flex:1">
    <div style="color:#22C55E;font-weight:700;font-size:0.75rem">TAK → budżet > 10k</div>
    <div style="color:#A8D8EA;font-size:0.72rem;margin-top:2px">Slack do Kacpra + Calendly call</div>
  </div>
  <div style="background:#1E2D40;border-left:3px solid #F97316;padding:0.5rem 0.8rem;border-radius:0 6px 6px 0;flex:1">
    <div style="color:#F97316;font-weight:700;font-size:0.75rem">NIE → mały budżet</div>
    <div style="color:#A8D8EA;font-size:0.72rem;margin-top:2px">Nurturing sequence MailerLite</div>
  </div>
</div>
''',

# ── Slajd 17: Setup decision tree ────────────────────────────────
'Setup — decision tree (kiedy co wybrać)': '''\
<N8nBranch
  :source="{icon: 'mdi:rocket-launch', label: 'Chcę zacząć z n8n', desc: 'wybierz ścieżkę'}"
  :branches="[
    {icon: 'mdi:laptop', label: 'Testuję lokalnie', result: 'Docker Desktop → port 5678', variant: 'action'},
    {icon: 'logos:docker-icon', label: 'Mam VPS (Linux)', result: 'Self-hosted n8n (Docker na VPS)', variant: 'trigger'},
    {icon: 'mdi:cloud-outline', label: 'Nie mam VPS / DevOps', result: 'n8n Cloud (trial → $20/mies.)', variant: 'output'},
  ]"
/>

<div style="margin-top:0.8rem;background:#1E2D40;border-radius:8px;padding:0.8rem 1rem;border-left:3px solid #F97316;font-size:0.8rem">
  <strong style="color:#F97316">Tip:</strong>
  <span style="color:#A8D8EA"> Freelancer testujący → Docker lokalnie. Projekt dla klienta → Cloud lub VPS.</span>
</div>
''',

# ── Slajd 20: Demo workflow ──────────────────────────────────────
'Demo — workflow hello automation': '''\
<N8nFlow
  :nodes="[
    {icon: 'mdi:webhook', label: 'Webhook', desc: 'odbierz HTTP POST', variant: 'trigger'},
    {icon: 'mdi:code-json', label: 'Parse JSON', desc: 'wyciągnij dane', variant: 'default'},
    {icon: 'logos:gmail', label: 'Gmail', desc: 'email powitalny', variant: 'output'},
  ]"
  animated
  caption="Wysyłasz HTTP request → osoba dostaje spersonalizowany email. Czas budowania: ~8 minut."
/>
''',

        }

    if folder_name == 'Modul_BONUS_Bezpieczenstwo':
        return {

# ── Slajd 6: Least Privilege ────────────────────────────────────
'Least privilege — zasada minimalnych uprawnień': '''\
<N8nBranch
  :source="{icon: 'mdi:key-variant', label: 'OpenAI API Key', desc: 'jeden klucz do wszystkiego'}"
  :branches="[
    {icon: 'mdi:email-outline', label: 'Workflow A', result: 'email summary — ma dostęp do billing!', variant: 'error'},
    {icon: 'mdi:account-search', label: 'Workflow B', result: 'HR screening — dostęp do wszystkiego!', variant: 'error'},
    {icon: 'mdi:robot', label: 'Workflow C', result: 'chatbot — bez rate limit!', variant: 'error'},
  ]"
/>

<div style="margin-top:0.5rem;color:#22C55E;font-weight:700;font-size:0.78rem;text-align:center">↓ DOBRZE: osobny Project API Key per workflow ↓</div>

<N8nBranch
  :source="{icon: 'mdi:shield-check', label: 'OpenAI Projects', desc: 'izolacja per workflow'}"
  :branches="[
    {icon: 'mdi:email-outline', label: 'Key A', result: 'tylko gpt-4o-mini, bez fine-tuning', variant: 'output'},
    {icon: 'mdi:account-search', label: 'Key B', result: 'osobny projekt, osobny monitoring', variant: 'output'},
    {icon: 'mdi:robot', label: 'Key C', result: 'rate limit 100 req/min', variant: 'output'},
  ]"
/>
''',

# ── Slajd 12: RTBF Workflow ─────────────────────────────────────
'Prawo do usunięcia danych — automatyzacja wniosku': '''\
<N8nFlow
  :nodes="[
    {icon: 'mdi:webhook', label: 'Webhook', desc: 'wniosek RTBF', variant: 'trigger'},
    {icon: 'mdi:account-check', label: 'Weryfikacja', desc: 'token email', variant: 'default'},
    {icon: 'mdi:magnify', label: 'Szukaj PII', desc: 'we WSZYSTKICH systemach', variant: 'action'},
    {icon: 'mdi:delete-outline', label: 'Usuń / Pseudonim.', desc: 'usunięcie danych', variant: 'error'},
    {icon: 'mdi:file-document-check', label: 'Audit Log', desc: 'data_deleted event', variant: 'output'},
  ]"
  animated
  caption="RODO: 30 dni na realizację wniosku. Wyjątek: faktury — 5 lat (prawo podatkowe)."
/>
''',

# ── Slajd 13: AI Act mapa ryzyka ────────────────────────────────
'AI act — mapa ryzyka (2024/1689)': '''\
<div style="display:flex;flex-direction:column;gap:0.5rem">
  <div style="background:linear-gradient(90deg,#7F1D1D,#991B1B);border-radius:8px;padding:0.5rem 1rem;border-left:4px solid #EF4444">
    <div style="color:#FCA5A5;font-weight:700;font-size:0.78rem">UNACCEPTABLE — ZAKAZANE od 02.2025</div>
    <div style="color:#FDA4AF;font-size:0.68rem;margin-top:2px">Social scoring · Biometryka real-time · Manipulacyjne AI</div>
  </div>
  <div style="background:linear-gradient(90deg,#78350F,#92400E);border-radius:8px;padding:0.5rem 1rem;border-left:4px solid #F97316">
    <div style="color:#FED7AA;font-weight:700;font-size:0.78rem">HIGH RISK — pełne wymagania od 08.2026</div>
    <div style="color:#FDBA74;font-size:0.68rem;margin-top:2px">HR screening CV · Scoring kredytowy · Ocena pracowników · Infrastruktura krytyczna</div>
  </div>
  <div style="background:linear-gradient(90deg,#1E3A5F,#1E40AF);border-radius:8px;padding:0.5rem 1rem;border-left:4px solid #3B82F6">
    <div style="color:#93C5FD;font-weight:700;font-size:0.78rem">LIMITED RISK — obowiązki transparency TERAZ</div>
    <div style="color:#BFDBFE;font-size:0.68rem;margin-top:2px">Chatboty: informuj że to AI · Deep-fake: oznaczenie · AI-generated content</div>
  </div>
  <div style="background:linear-gradient(90deg,#14532D,#166534);border-radius:8px;padding:0.5rem 1rem;border-left:4px solid #22C55E">
    <div style="color:#86EFAC;font-weight:700;font-size:0.78rem">MINIMAL RISK — bez specjalnych wymogów</div>
    <div style="color:#BBF7D0;font-size:0.68rem;margin-top:2px">Filtry antyspam · Rekomendacje · Gry</div>
  </div>
</div>

<div style="margin-top:0.6rem;background:#1E2D40;border-radius:8px;padding:0.6rem 1rem;border-left:3px solid #F97316;font-size:0.78rem">
  <strong style="color:#F97316">08.2026 = 5 miesięcy.</strong>
  <span style="color:#A8D8EA"> Sprawdź czy Twoje automatyzacje nie wpadają w HIGH RISK.</span>
</div>
''',

# ── Slajd 16: Bezpieczeństwo sieci — architektura ───────────────
'Bezpieczeństwo sieci — architektura': '''\
<N8nFlow
  :nodes="[
    {icon: 'mdi:web', label: 'INTERNET', desc: 'ruch przychodzący', variant: 'default'},
    {icon: 'mdi:shield-outline', label: 'Cloudflare', desc: 'DDoS + WAF', variant: 'action'},
    {icon: 'mdi:server', label: 'Nginx / Caddy', desc: 'reverse proxy + TLS + rate limit', variant: 'action'},
    {icon: 'logos:docker-icon', label: 'Docker network', desc: 'izolacja internal', variant: 'default'},
    {icon: 'mdi:hexagon-outline', label: 'n8n :5678', desc: 'NIGDY na zewnątrz!', variant: 'error'},
    {icon: 'mdi:database-lock', label: 'PostgreSQL', desc: 'tylko sieć wewnętrzna', variant: 'output'},
  ]"
  animated
  caption="n8n nigdy nie powinien być dostępny na surowym porcie 5678 w internecie"
/>
''',

# ── Slajd 19: HMAC Signature Verification ────────────────────────
'Webhook security — HMAC signature verification': '''\
<div style="display:flex;gap:1rem;align-items:flex-start">
  <div style="flex:1">
    <div style="color:#F97316;font-weight:700;font-size:0.78rem;margin-bottom:0.4rem">NADAWCA (GitHub, Stripe...)</div>
    <N8nFlow
      :nodes="[
        {icon: 'mdi:file-document', label: 'Body', desc: 'raw bytes', variant: 'default'},
        {icon: 'mdi:lock', label: 'HMAC-SHA256', desc: 'secret_key + body', variant: 'action'},
        {icon: 'mdi:send', label: 'Wyślij', desc: 'X-Signature header', variant: 'trigger'},
      ]"
    />
  </div>
  <div style="flex:1">
    <div style="color:#3B82F6;font-weight:700;font-size:0.78rem;margin-bottom:0.4rem">ODBIORCA (n8n webhook)</div>
    <N8nFlow
      :nodes="[
        {icon: 'mdi:download', label: 'Odbierz', desc: 'request + header', variant: 'trigger'},
        {icon: 'mdi:lock', label: 'HMAC-SHA256', desc: 'ten sam secret_key', variant: 'action'},
        {icon: 'mdi:check-decagram', label: 'Porównaj', desc: 'expected == received?', variant: 'output'},
      ]"
    />
  </div>
</div>

<div style="margin-top:0.6rem;display:flex;gap:0.6rem">
  <div style="background:#1E2D40;border-left:3px solid #22C55E;padding:0.4rem 0.7rem;border-radius:0 6px 6px 0;flex:1">
    <span style="color:#22C55E;font-weight:700;font-size:0.72rem">✅ Podpis OK</span>
    <span style="color:#A8D8EA;font-size:0.68rem"> → request autentyczny → przetwórz</span>
  </div>
  <div style="background:#1E2D40;border-left:3px solid #EF4444;padding:0.4rem 0.7rem;border-radius:0 6px 6px 0;flex:1">
    <span style="color:#EF4444;font-weight:700;font-size:0.72rem">❌ Podpis zły</span>
    <span style="color:#A8D8EA;font-size:0.68rem"> → sfałszowany → odrzuć z 401</span>
  </div>
</div>
''',

# ── Slajd 25: Microsoft Presidio ─────────────────────────────────
'Microsoft presidio — tarcza PII': '''\
<N8nFlow
  :nodes="[
    {icon: 'mdi:account-details', label: 'Surowe dane', desc: 'email, PESEL, imię', variant: 'error'},
    {icon: 'mdi:magnify-scan', label: 'Presidio Analyzer', desc: 'identyfikuje PII', variant: 'action'},
    {icon: 'mdi:shield-lock', label: 'Presidio Anonymizer', desc: 'zamienia na tokeny', variant: 'action'},
    {icon: 'mdi:robot-outline', label: 'OpenAI API', desc: 'dane bez PII!', variant: 'output'},
    {icon: 'mdi:account-convert', label: 'De-anonymizacja', desc: 'przywróć (opcjonalnie)', variant: 'default'},
  ]"
  animated
  caption="Zero-Trust AI Architecture: dane klientów nigdy nie trafiają do LLM w surowej formie"
/>
''',

# ── Slajd 26: 6 warstw bezpieczeństwa ───────────────────────────
'Podsumowanie — twoja tarcza bezpieczeństwa': '''\
<div style="display:flex;flex-direction:column;gap:0.35rem">
  <div style="background:#1E2D40;border-radius:6px;padding:0.4rem 0.8rem;border-left:3px solid #F97316;display:flex;align-items:center;gap:0.6rem">
    <span style="color:#F97316;font-weight:700;font-size:0.72rem;min-width:24px">1</span>
    <div><span style="color:#A8D8EA;font-weight:600;font-size:0.72rem">Credential Vault</span> <span style="color:#64748B;font-size:0.65rem">— N8N_ENCRYPTION_KEY + Least Privilege</span></div>
  </div>
  <div style="background:#1E2D40;border-radius:6px;padding:0.4rem 0.8rem;border-left:3px solid #3B82F6;display:flex;align-items:center;gap:0.6rem">
    <span style="color:#3B82F6;font-weight:700;font-size:0.72rem;min-width:24px">2</span>
    <div><span style="color:#A8D8EA;font-weight:600;font-size:0.72rem">RODO Compliance</span> <span style="color:#64748B;font-size:0.65rem">— Data Flow Audit + Pseudonimizacja + RTBF</span></div>
  </div>
  <div style="background:#1E2D40;border-radius:6px;padding:0.4rem 0.8rem;border-left:3px solid #8B5CF6;display:flex;align-items:center;gap:0.6rem">
    <span style="color:#8B5CF6;font-weight:700;font-size:0.72rem;min-width:24px">3</span>
    <div><span style="color:#A8D8EA;font-weight:600;font-size:0.72rem">AI Act Compliance</span> <span style="color:#64748B;font-size:0.65rem">— Klasyfikacja ryzyka + Transparency</span></div>
  </div>
  <div style="background:#1E2D40;border-radius:6px;padding:0.4rem 0.8rem;border-left:3px solid #22C55E;display:flex;align-items:center;gap:0.6rem">
    <span style="color:#22C55E;font-weight:700;font-size:0.72rem;min-width:24px">4</span>
    <div><span style="color:#A8D8EA;font-weight:600;font-size:0.72rem">Bezpieczeństwo sieci</span> <span style="color:#64748B;font-size:0.65rem">— Nginx + HMAC webhooks + IP whitelist</span></div>
  </div>
  <div style="background:#1E2D40;border-radius:6px;padding:0.4rem 0.8rem;border-left:3px solid #E63946;display:flex;align-items:center;gap:0.6rem">
    <span style="color:#E63946;font-weight:700;font-size:0.72rem;min-width:24px">5</span>
    <div><span style="color:#A8D8EA;font-weight:600;font-size:0.72rem">Logowanie bez PII</span> <span style="color:#64748B;font-size:0.65rem">— Dokodu Logging Standard + Loki</span></div>
  </div>
  <div style="background:#1E2D40;border-radius:6px;padding:0.4rem 0.8rem;border-left:3px solid #EC4899;display:flex;align-items:center;gap:0.6rem">
    <span style="color:#EC4899;font-weight:700;font-size:0.72rem;min-width:24px">6</span>
    <div><span style="color:#A8D8EA;font-weight:600;font-size:0.72rem">PII Redaction przed AI</span> <span style="color:#64748B;font-size:0.65rem">— Microsoft Presidio w architekturze</span></div>
  </div>
</div>
''',

        }

    if folder_name == 'Modul_BONUS_Sprzedaz':
        return {

# ── Slajd 7: Value-Based Pricing ─────────────────────────────────
'Value-Based pricing — jak rozmawiać o pieniądzach': '''\
<N8nFlow
  :nodes="[
    {icon: 'mdi:clock-outline', label: 'Czas pracownika', desc: '5 osób × 3h/dzień', variant: 'default'},
    {icon: 'mdi:calculator', label: 'Koszt roczny', desc: '75h/tydz × 60 PLN × 52', variant: 'error'},
    {icon: 'mdi:arrow-right-bold', label: '234 000 PLN/rok', desc: 'wartość problemu', variant: 'error'},
  ]"
/>

<div style="margin-top:0.5rem;display:flex;gap:0.8rem;align-items:center;justify-content:center">
  <div style="background:#1E2D40;border-radius:8px;padding:0.6rem 1rem;border-top:2px solid #22C55E;text-align:center">
    <div style="color:#22C55E;font-weight:700;font-size:1rem">20 000 PLN</div>
    <div style="color:#8096AA;font-size:0.68rem">Twój workflow</div>
  </div>
  <div style="color:#F97316;font-size:1.2rem;font-weight:700">→</div>
  <div style="background:#1E2D40;border-radius:8px;padding:0.6rem 1rem;border-top:2px solid #F97316;text-align:center">
    <div style="color:#F97316;font-weight:700;font-size:1rem">ROI w 5 tygodni</div>
    <div style="color:#8096AA;font-size:0.68rem">klient sam uzasadnia cenę</div>
  </div>
</div>
''',

# ── Slajd 15: BANT kwalifikacja ──────────────────────────────────
'BANT dla automatyzacji': '''\
<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem">
  <div style="background:#1E2D40;border-radius:8px;padding:0.6rem 0.8rem;border-left:3px solid #22C55E">
    <div style="color:#22C55E;font-weight:700;font-size:0.82rem">B — Budget</div>
    <div style="color:#A8D8EA;font-size:0.7rem;margin-top:2px">Czy mają środki na projekt?</div>
    <div style="color:#64748B;font-size:0.62rem;margin-top:2px">Min: zadeklarowany lub widoczny</div>
  </div>
  <div style="background:#1E2D40;border-radius:8px;padding:0.6rem 0.8rem;border-left:3px solid #3B82F6">
    <div style="color:#3B82F6;font-weight:700;font-size:0.82rem">A — Authority</div>
    <div style="color:#A8D8EA;font-size:0.7rem;margin-top:2px">Czy rozmawiasz z decydentem?</div>
    <div style="color:#64748B;font-size:0.62rem;margin-top:2px">Min: dostęp do osoby zatwierdzającej</div>
  </div>
  <div style="background:#1E2D40;border-radius:8px;padding:0.6rem 0.8rem;border-left:3px solid #F97316">
    <div style="color:#F97316;font-weight:700;font-size:0.82rem">N — Need</div>
    <div style="color:#A8D8EA;font-size:0.7rem;margin-top:2px">Czy ból jest realny i bolesny?</div>
    <div style="color:#64748B;font-size:0.62rem;margin-top:2px">Min: problem kosztuje czas/pieniądze</div>
  </div>
  <div style="background:#1E2D40;border-radius:8px;padding:0.6rem 0.8rem;border-left:3px solid #8B5CF6">
    <div style="color:#8B5CF6;font-weight:700;font-size:0.82rem">T — Timeline</div>
    <div style="color:#A8D8EA;font-size:0.7rem;margin-top:2px">Czy jest presja czasowa?</div>
    <div style="color:#64748B;font-size:0.62rem;margin-top:2px">Min: wdrożenie w 3-6 miesięcy</div>
  </div>
</div>

<div style="margin-top:0.6rem;background:#1E2D40;border-radius:8px;padding:0.6rem 1rem;border-left:3px solid #EF4444;font-size:0.78rem">
  <strong style="color:#EF4444">Brakuje 2+ kryteriów?</strong>
  <span style="color:#A8D8EA"> Nie wysyłaj oferty. To nie jest lead — to jest rozmowa.</span>
</div>
''',

# ── Slajd 31: Struktura retainera ────────────────────────────────
'Struktura retainera — co wchodzi': '''\
<N8nBranch
  :source="{icon: 'mdi:handshake', label: 'RETAINER', desc: 'pasywny przychód po projekcie'}"
  :branches="[
    {icon: 'mdi:eye-outline', label: 'Tier A: Monitoring', result: 'monitoring + SLA 48h', variant: 'default'},
    {icon: 'mdi:wrench', label: 'Tier B: Wsparcie', result: '+ naprawy + aktualizacje + SLA 24h', variant: 'action'},
    {icon: 'mdi:rocket-launch', label: 'Tier C: Rozwój', result: '+ nowe workflows + SLA 8h', variant: 'output'},
  ]"
/>

<div style="margin-top:0.8rem;background:#1E2D40;border-radius:8px;padding:0.8rem 1rem;border-left:3px solid #22C55E;font-size:0.8rem">
  <strong style="color:#22C55E">Formuła:</strong>
  <span style="color:#A8D8EA"> retainer = wartość projektu x 2-3% / mies. Projekt 30k → ~900 PLN/mies. (Tier B)</span>
</div>
''',

# ── Slajd 33: Model biznesowy z retainerami ──────────────────────
'Pasywny przychód z portfela klientów': '''\
<div style="display:flex;gap:1rem;align-items:stretch">
  <div style="flex:1;background:#1E2D40;border-radius:8px;padding:0.8rem 1rem;border-top:3px solid #3B82F6">
    <div style="color:#3B82F6;font-weight:700;font-size:0.82rem;margin-bottom:0.4rem">Projekty (aktywny przychód)</div>
    <div style="color:#A8D8EA;font-size:0.72rem">2-3 projekty/kwartał x 20-50k</div>
    <div style="color:#3B82F6;font-weight:700;font-size:1rem;margin-top:0.4rem">120-300k PLN/rok</div>
  </div>
  <div style="display:flex;align-items:center;color:#F97316;font-size:1.5rem;font-weight:700">+</div>
  <div style="flex:1;background:#1E2D40;border-radius:8px;padding:0.8rem 1rem;border-top:3px solid #22C55E">
    <div style="color:#22C55E;font-weight:700;font-size:0.82rem;margin-bottom:0.4rem">Retainery (pasywny przychód)</div>
    <div style="color:#A8D8EA;font-size:0.72rem">10 klientów x 1 500 PLN/mies.</div>
    <div style="color:#22C55E;font-weight:700;font-size:1rem;margin-top:0.4rem">216k PLN/rok</div>
  </div>
</div>

<div style="margin-top:0.6rem;background:linear-gradient(90deg,#1E2D40,#0F2137);border-radius:8px;padding:0.6rem 1rem;border-top:2px solid #F97316;text-align:center">
  <span style="color:#F97316;font-weight:700;font-size:1.1rem">Suma: 336-516k PLN/rok</span>
  <div style="color:#8096AA;font-size:0.68rem;margin-top:2px">Retainery to fundament, projekty to wzrost.</div>
</div>
''',

        }

    return {}


def build_two_col(title, h1, body1, h2, body2):
    """
    Zwraca (slide_frontmatter, slide_content) dla layout: two-cols.
    Używa Slidev built-in two-cols layout z ::right:: separatorem.
    """
    label1 = h1.replace('## ', '').strip()
    label2 = h2.replace('## ', '').strip()

    neg_keywords = ['nie', 'without', 'before', 'problem', 'stara', 'brak']
    pos_keywords = ['jest', 'with', 'after', 'solution', 'nowa', 'wynik', 'teraz']

    cls1 = 'col-neg' if any(k in label1.lower() for k in neg_keywords) else 'col-pos'
    cls2 = 'col-pos' if any(k in label2.lower() for k in pos_keywords) else 'col-neg'
    if cls1 == cls2:
        cls1, cls2 = 'col-neg', 'col-pos'

    items1 = re.findall(r'^\s*[-*]\s+(.+)', body1, re.MULTILINE)
    items2 = re.findall(r'^\s*[-*]\s+(.+)', body2, re.MULTILINE)

    left_items = '\n'.join(f'- {i}' for i in items1)
    right_items = '\n'.join(f'- {i}' for i in items2)

    frontmatter = 'layout: two-cols-header'
    content = f'''# {title}

<div class="col-header {cls1}">{label1}</div>

{left_items}

::right::

<div class="col-header {cls2}">{label2}</div>

{right_items}'''
    return frontmatter, content


def normalize_title(title):
    """Konwertuje Title Case → sentence case. Zachowuje akronimy i nazwy własne."""
    PROTECTED = {
        'n8n', 'AI', 'API', 'HTTP', 'HTTPS', 'CSS', 'JS', 'URL', 'SQL',
        'JSON', 'YAML', 'CRM', 'MVP', 'ROI', 'KPI', 'CEO', 'B2B', 'SaaS',
        'Docker', 'JavaScript', 'TypeScript', 'Python', 'Google', 'Gmail',
        'Slack', 'Trello', 'GitHub', 'Webhook', 'PostgreSQL', 'MongoDB',
        'Redis', 'Linux', 'Windows', 'Mac', 'WSL', 'SSH', 'Dokodu',
        'Airtable', 'Notion', 'Zapier', 'Make', 'Node', 'ActiveCampaign',
        'NIE', 'JEST',
    }
    words = title.split()
    result = []
    for i, word in enumerate(words):
        stripped = word.strip('—–-:.,!?()')
        if i == 0:
            result.append(word)
        elif stripped in PROTECTED:
            result.append(word)
        elif stripped.upper() == stripped and len(stripped) > 1 and stripped.isalpha():
            result.append(word)  # Akronim (AI, API…)
        else:
            result.append(word.lower())
    return ' '.join(result)


def build_screenshot_html(screenshot_file):
    """
    Generuje HTML blok ze screenshotem w stylu okna przeglądarki.
    screenshot_file: nazwa pliku (np. '01_canvas_pusty.png') — serwowany z public/screenshots/
    """
    return f'''\
<div style="margin-top:0.8rem">
  <div style="background:#2D3748;border-radius:8px 8px 0 0;padding:6px 12px;display:flex;align-items:center;gap:6px">
    <div style="width:10px;height:10px;border-radius:50%;background:#EF4444"></div>
    <div style="width:10px;height:10px;border-radius:50%;background:#F59E0B"></div>
    <div style="width:10px;height:10px;border-radius:50%;background:#22C55E"></div>
    <span style="margin-left:8px;font-size:0.6rem;color:#94A3B8">n8n.dokodu.it</span>
  </div>
  <img src="/screenshots/{screenshot_file}" style="max-height:280px;width:100%;object-fit:contain;border-radius:0 0 8px 8px;box-shadow:0 4px 24px rgba(0,0,0,0.35);display:block" />
</div>'''


def get_screenshot_for_slide(folder_name, orig_title):
    """
    Zwraca (html, found) dla slajdu. Sprawdza SCREENSHOT_MAPPING i fizyczną obecność pliku.
    """
    mapping = SCREENSHOT_MAPPING.get(folder_name, {})
    rel_path = mapping.get(orig_title)
    if not rel_path:
        return '', False

    screenshot_file = os.path.basename(rel_path)
    abs_path = os.path.join(ASSETS_DIR, rel_path)

    if os.path.exists(abs_path):
        return build_screenshot_html(screenshot_file), True
    else:
        return f'<!-- TODO: screenshot {screenshot_file} -->', True


def build_module_label(folder_name):
    parts = folder_name.replace('Modul_', '').split('_', 1)
    if len(parts) == 2:
        num, name = parts
        return f"MODUŁ {num} — {name.upper().replace('_', ' ')}"
    return folder_name.upper()


def extract_clean_title(first_slide_body):
    """Wyciąga główny tytuł z body pierwszego slajdu (bez 'X slajdów')"""
    lines = [l.strip() for l in first_slide_body.split('\n') if l.strip()]
    for line in lines:
        clean = re.sub(r'\*+', '', line).strip()
        # Pomiń linie z "slajdów", "Prezentacja", "Tydzień X:"
        if re.search(r'\d+\s*slajd|Prezentacja|^Tydzień\s+\d+:', clean):
            continue
        if clean and len(clean) > 5:
            # Wyczyść prefix "Tydzień X:"
            clean = re.sub(r'^Tydzień\s+\d+:\s*', '', clean)
            return clean
    # Fallback: pierwsze pole z folder_name
    return lines[0].replace('**', '').replace('*', '') if lines else "Kurs n8n"


def convert_module(folder_name, with_exercises=False):
    src = os.path.join(BASE, folder_name, '02_Prezentacja.md')
    if not os.path.exists(src):
        print(f"  ❌ Brak pliku: {src}")
        return

    with open(src, encoding='utf-8') as f:
        md_text = f.read()

    slides = parse_slides(md_text)
    if not slides:
        print(f"  ❌ Brak slajdów w: {src}")
        return

    module_label = build_module_label(folder_name)
    clean_title = extract_clean_title(slides[0]['body'] if slides else '')

    out_path = os.path.join(OUT_DIR, folder_name)
    os.makedirs(out_path, exist_ok=True)

    # Kopiuj współdzielone komponenty Vue
    shared_components = os.path.join(_SCRIPTS_DIR, 'slidev_components')
    if os.path.isdir(shared_components):
        shutil.copytree(shared_components, os.path.join(out_path, 'components'), dirs_exist_ok=True)

    # Zapisz CSS
    with open(os.path.join(out_path, 'style.css'), 'w', encoding='utf-8') as f:
        f.write(CUSTOM_CSS)

    # Mermaid dark theme setup
    setup_dir = os.path.join(out_path, 'setup')
    os.makedirs(setup_dir, exist_ok=True)
    with open(os.path.join(setup_dir, 'mermaid.ts'), 'w', encoding='utf-8') as f:
        f.write('''\
import { defineMermaidSetup } from \'@slidev/types\'

export default defineMermaidSetup(() => ({
  theme: \'base\',
  themeVariables: {
    primaryColor: \'#1E2D40\',
    primaryTextColor: \'#A8D8EA\',
    primaryBorderColor: \'#E63946\',
    lineColor: \'#E63946\',
    secondaryColor: \'#0F2137\',
    tertiaryColor: \'#0A1628\',
    edgeLabelBackground: \'#0F2137\',
    fontFamily: \'Inter, sans-serif\',
    fontSize: \'14px\',
    actorBkg: \'#0F2137\',
    actorBorder: \'#E63946\',
    actorTextColor: \'#ffffff\',
    signalColor: \'#A8D8EA\',
    signalTextColor: \'#A8D8EA\',
    noteBkgColor: \'#1E2D40\',
    noteTextColor: \'#A8D8EA\',
  }
}))
''')

    lines = []
    mermaid_overrides = get_mermaid_overrides(folder_name)

    # Frontmatter
    lines.append(GLOBAL_FRONTMATTER.strip())
    lines.append('')

    for i, slide in enumerate(slides):
        title = slide['title']
        body = slide['body']
        note = slide['note']

        # Pomiń slajdy-placeholdery (tytuł modułu z szablonu)
        if re.match(r'^Tytu[łl]\s+Modu[łl]u$', title, re.IGNORECASE):
            continue

        # Normalizuj tytuł do sentence case
        title = normalize_title(title)

        # Mermaid override zastępuje body — nie przetwarzaj dalej przez process_*
        is_mermaid_override = title in mermaid_overrides
        if not is_mermaid_override:
            # Sprawdź też oryginalny (nienormalizowany) klucz
            orig_title = slide['title']
            is_mermaid_override = orig_title in mermaid_overrides
            if is_mermaid_override:
                body = mermaid_overrides[orig_title]
        else:
            body = mermaid_overrides[title]

        if i == 0:
            # ── COVER SLIDE ──────────────────────────────────────
            body_lines = [l.strip() for l in body.split('\n') if l.strip()]
            main = clean_title
            subtitle = ''
            author = 'Kacper Sieradziński'
            for bl in body_lines:
                clean_bl = re.sub(r'\*+', '', bl).strip()
                if re.search(r'Tydzień\s+\d+', clean_bl):
                    subtitle = clean_bl
                elif 'Sieradziński' in bl:
                    author = re.sub(r'\*+', '', bl).replace('| Dokodu', '').strip()

            lines.append('')
            lines.append('---')
            lines.append('transition: fade')
            lines.append('layout: cover')
            lines.append('---')
            lines.append('')
            # Logo Dokodu
            lines.append('<img src="/dokodu_logo.png" style="height:28px;margin-bottom:1.8rem;opacity:0.92" alt="Dokodu" />')
            lines.append('')
            lines.append(f'<div class="cover-tag">{module_label}</div>')
            lines.append('')
            lines.append(f'# {main}')
            lines.append('')
            if subtitle:
                lines.append(f'<p style="color:#8096AA;font-size:1rem">{subtitle}</p>')
            lines.append('')
            lines.append(f'<p style="color:#E63946;font-weight:600">{author}</p>')
            lines.append('<p style="color:#8096AA;font-size:0.8rem;margin-top:0.2rem">dokodu.it</p>')

        else:
            # ── CONTENT SLIDES ────────────────────────────────────
            if not is_mermaid_override:
                body = process_body(body)
                body = process_code_blocks(body)

            # Wykryj slajd porównawczy (dwie sekcje z listami)
            is_comp = False
            if not is_mermaid_override:
                is_comp, h1, b1, h2, b2 = detect_comparison(body)

            # Screenshot do wstawienia pod treścią (jeśli zmapowany)
            screenshot_html, has_screenshot = get_screenshot_for_slide(folder_name, slide['title'])

            # Wykryj specjalny typ slajdu (takeaway / exercise)
            slide_class = detect_slide_class(title)

            lines.append('')
            lines.append('---')
            if is_comp:
                lines.append('transition: fade')
                fm, content = build_two_col(title, h1, b1, h2, b2)
                lines.append(fm)
                lines.append('---')
                lines.append('')
                lines.append(content)
            elif is_mermaid_override:
                lines.append('transition: fade')
                lines.append('---')
                lines.append('')
                lines.append(f'# {title}')
                lines.append('')
                lines.append(body)
            else:
                if slide_class:
                    lines.append(f'class: {slide_class}')
                lines.append('---')
                lines.append('')
                lines.append(f'# {title}')
                lines.append('')
                lines.append(add_vclicks(body))

            # Wstaw screenshot pod treścią slajdu
            if has_screenshot:
                lines.append('')
                lines.append(screenshot_html)

        # Speaker notes
        if note:
            lines.append('')
            lines.append('<!--')
            lines.append(note)
            lines.append('-->')

        lines.append('')

    # ── Ćwiczenia z 04_Cwiczenia.md (opcjonalnie) ────────────────
    exercises_count = 0
    if with_exercises:
        exercises_path = os.path.join(BASE, folder_name, '04_Cwiczenia.md')
        exercise_slides = parse_exercises(exercises_path)
        if exercise_slides:
            # Slajd-separator "Ćwiczenia"
            lines.append('')
            lines.append('---')
            lines.append('class: layout-exercise')
            lines.append('---')
            lines.append('')
            lines.append('# Ćwiczenia praktyczne')
            lines.append('')
            lines.append('Czas na praktykę! Otwórz n8n i zrób ćwiczenia samodzielnie.')
            lines.append('')

            for ex_slide in exercise_slides:
                ex_title = normalize_title(ex_slide['title'])
                ex_body = process_body(ex_slide['body'])

                lines.append('')
                lines.append('---')
                lines.append('class: layout-exercise')
                lines.append('---')
                lines.append('')
                lines.append(f'# {ex_title}')
                lines.append('')
                lines.append(add_vclicks(ex_body))
                lines.append('')

            exercises_count = len(exercise_slides)
            print(f"  📝 Dodano {exercises_count} slajd(ów) ćwiczeń z 04_Cwiczenia.md")
        else:
            print(f"  ⚠️  Brak pliku 04_Cwiczenia.md lub pusty — pomijam ćwiczenia")

    out_md = os.path.join(out_path, 'slides.md')
    with open(out_md, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    # Kopiuj screenshoty do public/screenshots/ (Slidev serwuje z public/)
    screenshots_src = os.path.join(ASSETS_DIR, 'screenshots')
    if os.path.isdir(screenshots_src) and folder_name in SCREENSHOT_MAPPING:
        public_screenshots = os.path.join(out_path, 'public', 'screenshots')
        os.makedirs(public_screenshots, exist_ok=True)
        copied = 0
        for rel_path in SCREENSHOT_MAPPING[folder_name].values():
            src_file = os.path.join(ASSETS_DIR, rel_path)
            if os.path.exists(src_file):
                shutil.copy2(src_file, os.path.join(public_screenshots, os.path.basename(rel_path)))
                copied += 1
        if copied:
            print(f"  📸 Skopiowano {copied} screenshot(ów) → public/screenshots/")

    total = len(slides) + exercises_count
    print(f"  ✅ {folder_name} → {out_md} ({total} slajdów)")
    return out_path


def main():
    args = sys.argv[1:]

    with_exercises = '--with-exercises' in args
    args = [a for a in args if a != '--with-exercises']

    if '--all' in args:
        args = [a for a in args if a != '--all']
        modules = sorted([d for d in os.listdir(BASE) if os.path.isdir(os.path.join(BASE, d))])
    elif args:
        modules = args
    else:
        modules = ['Modul_01_Fundamenty']

    print(f"🎨 Konwerter MD → Slidev")
    print(f"📁 Output: {OUT_DIR}")
    if with_exercises:
        print(f"📝 Ćwiczenia: włączone (--with-exercises)")
    print()

    for m in modules:
        convert_module(m, with_exercises=with_exercises)

    print()
    if len(modules) == 1:
        out = os.path.join(OUT_DIR, modules[0])
        print(f"Podgląd dev:    cd {out} && slidev slides.md")
        print(f"Build statyczny: cd {out} && slidev build slides.md --out dist")


if __name__ == '__main__':
    main()
