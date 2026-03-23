#!/usr/bin/env python3
"""
Dokodu Offer Generator
Przyjmuje plik JSON z danymi oferty, generuje PDF przez WeasyPrint.

Użycie:
  python3 generate.py <offer_data.json> [output.pdf]
  python3 generate.py --test
"""

import sys
import json
import os
import base64
from pathlib import Path
from datetime import datetime, timedelta

SCRIPT_DIR = Path(__file__).parent

# ── Wczytaj dane ──────────────────────────────────────────
if len(sys.argv) < 2:
    print("Użycie: python3 generate.py <offer_data.json> [output.pdf]")
    print("        python3 generate.py --test")
    sys.exit(1)

if sys.argv[1] == '--test':
    today = datetime.today()
    valid = today + timedelta(days=14)
    months_pl = ["stycznia","lutego","marca","kwietnia","maja","czerwca","lipca","sierpnia","września","października","listopada","grudnia"]
    fmt = lambda d: f"{d.day} {months_pl[d.month-1]} {d.year}"
    data = {
        "clientName":    "Firma Przykładowa S.A.",
        "clientSlug":    "FirmaPrzykladowa",
        "date":          fmt(today),
        "validUntil":    fmt(valid),
        "coverSubtitle": "Automatyzacja procesów operacyjnych działu obsługi klienta z wykorzystaniem AI.",
        "execSummary":   "Wasz dział BOK obsługuje miesięcznie ok. 2 000 zapytań, z czego 70% to powtarzalne pytania wymagające ręcznego wyszukiwania odpowiedzi. Proponujemy wdrożenie agenta AI zintegrowanego z Waszym CRM, który automatycznie odpowie na 65% zapytań — szacowana oszczędność: 3 etaty i 40 000 PLN miesięcznie.",
        "problemIntro":  "W trakcie discovery call zidentyfikowaliśmy trzy główne obszary generujące straty operacyjne:",
        "pains": [
            {"icon": "⏱", "title": "Czas odpowiedzi: 4–6 godzin", "desc": "Klienci czekają na prostą informację, którą agent AI udzieliłby w 3 sekundy."},
            {"icon": "🔁", "title": "70% zapytań jest powtarzalnych", "desc": "Konsultanci ręcznie piszą te same odpowiedzi każdego dnia."},
            {"icon": "📉", "title": "CSAT spada przez czas oczekiwania", "desc": "Niezadowolenie klientów rośnie proporcjonalnie do czasu odpowiedzi — ryzyko churn."},
        ],
        "approach": [
            {"title": "Analiza i mapowanie", "desc": "Audyt procesów BOK: kategorie zapytań, źródła danych, systemy (CRM, helpdesk)."},
            {"title": "Budowa agenta AI", "desc": "Wdrożenie agenta n8n zintegrowanego z Waszym CRM i bazą wiedzy."},
            {"title": "Testy i kalibracja", "desc": "Dwutygodniowy okres testów z Waszym teamem na realnych przypadkach."},
            {"title": "Wdrożenie i transfer wiedzy", "desc": "Go-live na produkcji i szkolenie Waszego zespołu."},
        ],
        "optionA": {
            "name": "Start AI",
            "deliverables": ["Agent FAQ — 50 najczęstszych zapytań", "Integracja z helpdeskiem", "Dashboard monitoring", "Szkolenie 2 administratorów", "1 miesiąc wsparcia"],
            "features": ["50 zautomatyzowanych odpowiedzi", "Integracja helpdesk", "Szkolenie zespołu", "1 mies. support"],
            "price": "24 900 PLN",
        },
        "optionB": {
            "name": "AI Full Stack",
            "deliverables": ["Wszystko z Opcji A", "Agent 200+ scenariuszy", "Integracja CRM + helpdesk + e-mail", "Smart routing do konsultantów", "Retainer 6 miesięcy", "Raport ROI co miesiąc"],
            "features": ["200+ scenariuszy", "CRM + helpdesk + e-mail", "Smart routing", "Retainer 6 mies.", "Raport ROI"],
            "price": "54 900 PLN",
        },
        "timeline": [
            {"week": "Tyg. 1–2", "label": "Analiza i mapowanie", "width": 30},
            {"week": "Tyg. 3–5", "label": "Budowa agenta AI", "width": 55},
            {"week": "Tyg. 6–7", "label": "Testy z teamem", "width": 42},
            {"week": "Tyg. 8",   "label": "Go-live", "width": 20},
            {"week": "Mies. 2–7","label": "Retainer (Opcja B)", "width": 80},
        ],
        "roiHeadline": "Zwrot inwestycji w ok. 2 miesiące",
        "roiDetail":   "Przy koszcie 3 etatów BOK (~40 000 PLN/mies.) oszczędność za rok to ok. 480 000 PLN.",
        "whyUs": [
            {"icon": "🏭", "title": "Znamy Waszą branżę", "desc": "Realizowaliśmy podobny projekt dla firmy produkcyjnej — efekty po 6 tygodniach."},
            {"icon": "⚖️", "title": "Tech + Legal w jednym", "desc": "Wdrożenie i compliance AI Act w jednym pakiecie. Alina (COO/Legal) dba o bezpieczeństwo."},
            {"icon": "🔓", "title": "Zero lock-in", "desc": "Cały kod i konfiguracja na Waszej infrastrukturze."},
            {"icon": "🇵🇱", "title": "Polski support", "desc": "Dostępni w języku polskim, w polskich godzinach pracy."},
        ],
        "ctaSteps": [
            "Odpiszcie z potwierdzeniem wybranej opcji (A lub B)",
            "Prześlę umowę w ciągu 24 godzin",
            "Kickoff call — zarezerwujemy termin od razu",
        ],
    }
    output_path = f"Oferta_Test_{datetime.today().strftime('%Y-%m')}.pdf"
else:
    with open(sys.argv[1]) as f:
        data = json.load(f)
    output_path = sys.argv[2] if len(sys.argv) > 2 else \
        f"Oferta_{data.get('clientSlug','Klient')}_{data.get('date','')[:7]}.pdf"

# ── Logo jako base64 ──────────────────────────────────────
logo_path = SCRIPT_DIR / "assets" / "logo_black.avif"
with open(logo_path, "rb") as f:
    logo_b64 = base64.b64encode(f.read()).decode()
logo_data_url = f"data:image/avif;base64,{logo_b64}"

# ── HTML builders ─────────────────────────────────────────
def pain_item(icon, title, desc):
    return f'<div class="pain-item"><span class="pain-title">{title}</span><span class="pain-desc">{desc}</span></div>'

def approach_step(num, title, desc):
    return (
        '<table width="100%" cellspacing="0" cellpadding="0" style="margin-bottom:12px;border-collapse:collapse;">'
        '<tr>'
        '<td width="42" style="vertical-align:top;padding-top:2px;">'
        f'<span style="display:inline-block;width:32px;height:32px;border-radius:16px;background:#0F2137;color:#fff;font-weight:800;font-size:11pt;text-align:center;line-height:32px;">{num}</span>'
        '</td>'
        '<td style="vertical-align:top;padding-top:4px;">'
        f'<span style="display:block;font-weight:700;font-size:11pt;color:#0F2137;margin-bottom:3px;">{title}</span>'
        f'<span style="display:block;font-size:10pt;color:#5A6677;">{desc}</span>'
        '</td>'
        '</tr></table>'
    )

def scope_card(featured, badge, name, deliverables):
    cls = "scope-card featured" if featured else "scope-card"
    items = "".join(f'<div class="scope-item">{d}</div>' for d in deliverables)
    return f'<div class="{cls}"><div class="scope-badge">{badge}</div><h3>{name}</h3>{items}</div>'

def scope_cols(a, b):
    return f'<div class="scope-col">{a}</div><div class="scope-col">{b}</div>'

def timeline_item(week, label, width):
    return (f'<div class="tl-row">'
            f'<div class="tl-week">{week}</div>'
            f'<div class="tl-bar-cell"><div class="tl-bar-bg"><div class="tl-bar-fill" style="width:{width}%"></div></div></div>'
            f'<div class="tl-label">{label}</div>'
            f'</div>')

def price_card(featured, option_label, name, amount, amount_sub, features):
    cls = "price-card featured" if featured else "price-card"
    items = "".join(f'<div class="price-feature">{f}</div>' for f in features)
    return (f'<div class="{cls}">'
            f'<span class="price-option-label">{option_label}</span>'
            f'<span class="price-name">{name}</span>'
            f'<span class="price-amount">{amount}</span>'
            f'<span class="price-vat">{amount_sub}</span>'
            f'<hr class="price-hr">{items}</div>')

def price_cols(a, b):
    return f'<div class="pricing-col">{a}</div><div class="pricing-col">{b}</div>'

def why_item(icon, title, desc):
    # icon_labels: map common icons to short text labels
    icon_map = {
        '🏭': 'BRANŻA', '⚖️': 'LEGAL', '🔓': 'OPEN', '🇵🇱': 'PL',
        '🎯': 'CEL', '💡': 'IDEA', '🚀': 'SPEED', '🔒': 'SEC',
    }
    label = icon_map.get(icon, icon[:2] if icon else '★')
    return (f'<div class="why-card">'
            f'<div style="display:inline-block;background:#0F2137;color:#ffffff;font-size:7pt;font-weight:800;letter-spacing:1px;padding:4px 8px;border-radius:6px;margin-bottom:10px;">{label}</div>'
            f'<span class="why-title">{title}</span>'
            f'<span class="why-desc">{desc}</span>'
            f'</div>')

def why_rows(items):
    html = ''
    for i in range(0, len(items), 2):
        pair = items[i:i+2]
        cells = "".join(f'<div class="why-col">{why_item(**p)}</div>' for p in pair)
        if len(pair) < 2:
            cells += '<div class="why-col"></div>'
        html += f'<div class="why-row">{cells}</div>'
    return html

def cta_step(num, text):
    return (f'<div class="cta-step">'
            f'<div class="cta-num-cell"><span class="cta-num">{num}</span></div>'
            f'<div class="cta-text-cell">{text}</div>'
            f'</div>')

# ── Buduj sekcje ──────────────────────────────────────────
pain_html     = "".join(pain_item(**p) for p in data["pains"])
approach_html = "".join(approach_step(i+1, s["title"], s["desc"]) for i,s in enumerate(data["approach"]))

card_a = scope_card(False, "Opcja A — MVP", data["optionA"]["name"], data["optionA"]["deliverables"])
card_b = scope_card(True, "Opcja B — Pełne rozwiązanie", data["optionB"]["name"], data["optionB"]["deliverables"])
scope_html    = scope_cols(card_a, card_b)

timeline_html = "".join(timeline_item(t["week"], t["label"], t["width"]) for t in data["timeline"])

pc_a = price_card(False, "Opcja A", data["optionA"]["name"], data["optionA"]["price"], "netto + 23% VAT", data["optionA"]["features"])
pc_b = price_card(True,  "Opcja B", data["optionB"]["name"], data["optionB"]["price"], "netto + 23% VAT", data["optionB"]["features"])
pricing_html  = price_cols(pc_a, pc_b)

why_html      = why_rows(data["whyUs"])
cta_html      = "".join(cta_step(i+1, s) for i,s in enumerate(data["ctaSteps"]))

# ── Wczytaj i podmień szablon ─────────────────────────────
template_path = SCRIPT_DIR / "template.html"
html = template_path.read_text(encoding="utf-8")

replacements = {
    "{{LOGO_PATH}}":      logo_data_url,
    "{{CLIENT_NAME}}":    data["clientName"],
    "{{DATE}}":           data["date"],
    "{{VALID_UNTIL}}":    data["validUntil"],
    "{{COVER_SUBTITLE}}": data["coverSubtitle"],
    "{{EXEC_SUMMARY}}":   data["execSummary"],
    "{{PROBLEM_INTRO}}":  data["problemIntro"],
    "{{PAIN_ITEMS}}":     pain_html,
    "{{APPROACH_STEPS}}": approach_html,
    "{{SCOPE_COLS}}":     scope_html,
    "{{TIMELINE_ITEMS}}": timeline_html,
    "{{PRICING_COLS}}":   pricing_html,
    "{{ROI_HEADLINE}}":   data["roiHeadline"],
    "{{ROI_DETAIL}}":     data["roiDetail"],
    "{{WHY_ROWS}}":       why_html,
    "{{CTA_STEPS}}":      cta_html,
}

for key, val in replacements.items():
    html = html.replace(key, val or "")

# ── Generuj PDF ───────────────────────────────────────────
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

font_config = FontConfiguration()
css = CSS(string='''
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=DM+Sans:wght@400;500;600&display=swap');
  @page { margin: 0; size: A4; }
''', font_config=font_config)

print(f"Generuję PDF: {output_path} ...")
HTML(string=html, base_url=str(SCRIPT_DIR)).write_pdf(
    output_path,
    stylesheets=[css],
    font_config=font_config,
    optimize_images=True,
)
print(f"✅ PDF wygenerowany: {output_path}")
