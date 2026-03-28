#!/usr/bin/env python3
"""
Konwerter 02_Prezentacja.md → Slidev slides.md

Użycie:
  python3 convert_to_slidev.py Modul_01_Fundamenty
  python3 convert_to_slidev.py --all    # wszystkie moduły
"""

import re
import sys
import os
import shutil

BASE = os.path.join(os.path.dirname(__file__), "../10_PROJECTS/PRJ_Kurs_n8n_Launch/MATERIALY_KURSU")
OUT_DIR = os.path.join(os.path.dirname(__file__), "../10_PROJECTS/PRJ_Kurs_n8n_Launch/SLIDEV")

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


def convert_module(folder_name):
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

            lines.append('')
            lines.append('---')
            if is_comp:
                fm, content = build_two_col(title, h1, b1, h2, b2)
                lines.append(fm)
                lines.append('---')
                lines.append('')
                lines.append(content)
            else:
                lines.append('---')
                lines.append('')
                lines.append(f'# {title}')
                lines.append('')
                if is_mermaid_override:
                    lines.append(body)
                else:
                    lines.append(add_vclicks(body))

        # Speaker notes
        if note:
            lines.append('')
            lines.append('<!--')
            lines.append(note)
            lines.append('-->')

        lines.append('')

    out_md = os.path.join(out_path, 'slides.md')
    with open(out_md, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"  ✅ {folder_name} → {out_md} ({len(slides)} slajdów)")
    return out_path


def main():
    args = sys.argv[1:]

    if '--all' in args:
        modules = sorted([d for d in os.listdir(BASE) if os.path.isdir(os.path.join(BASE, d))])
    elif args:
        modules = args
    else:
        modules = ['Modul_01_Fundamenty']

    print(f"🎨 Konwerter MD → Slidev")
    print(f"📁 Output: {OUT_DIR}")
    print()

    for m in modules:
        convert_module(m)

    print()
    if len(modules) == 1:
        out = os.path.join(OUT_DIR, modules[0])
        print(f"Podgląd dev:    cd {out} && slidev slides.md")
        print(f"Build statyczny: cd {out} && slidev build slides.md --out dist")


if __name__ == '__main__':
    main()
