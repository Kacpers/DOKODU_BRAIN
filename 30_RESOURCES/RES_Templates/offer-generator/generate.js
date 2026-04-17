#!/usr/bin/env node
/**
 * Dokodu Offer Generator v2
 * Przyjmuje plik JSON z danymi oferty, generuje PDF.
 *
 * Użycie:
 *   node generate.js <offer_data.json> [output.pdf]
 *   node generate.js --test
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// ── Wczytaj dane ──────────────────────────────────────────
const args = process.argv.slice(2);
let data;

if (args[0] === '--test') {
  data = getTestData();
} else if (args[0]) {
  data = JSON.parse(fs.readFileSync(args[0], 'utf8'));
} else {
  console.error('Użycie: node generate.js <offer_data.json> [output.pdf]');
  console.error('        node generate.js --test');
  process.exit(1);
}

const outputPath = args[1] || path.join(
  process.cwd(),
  `Oferta_${data.clientSlug || 'Klient'}_${data.date || new Date().toISOString().slice(0,7)}.pdf`
);

// ── Zbuduj HTML ───────────────────────────────────────────
const templatePath = path.join(__dirname, 'template.html');
let html = fs.readFileSync(templatePath, 'utf8');

const logoBlackPath = path.join(__dirname, 'assets', 'logo_black.avif');
const logoBlackDataUrl = `data:image/avif;base64,${fs.readFileSync(logoBlackPath).toString('base64')}`;

// Logo white for cover (if exists, else use black with filter)
const logoWhitePath = path.join(__dirname, 'assets', 'logo_white.avif');
let logoWhiteDataUrl = logoBlackDataUrl;
if (fs.existsSync(logoWhitePath)) {
  logoWhiteDataUrl = `data:image/avif;base64,${fs.readFileSync(logoWhitePath).toString('base64')}`;
}

// ── Helpery HTML (matchują klasy w template.html) ─────────

function painItem(title, desc) {
  return `<div class="pain-item"><span class="pain-title">${title}</span><span class="pain-desc">${desc}</span></div>`;
}

function approachStep(num, title, desc) {
  return `<div class="step"><div class="step-num-cell"><span class="step-num">${num}</span></div><div class="step-body-cell"><span class="step-title">${title}</span><span class="step-desc">${desc}</span></div></div>`;
}

function scopeCol(featured, badge, title, deliverables) {
  const cardCls = featured ? 'scope-card featured' : 'scope-card';
  const items = deliverables.map(d => `<div class="scope-item">${d}</div>`).join('');
  return `<div class="scope-col"><div class="${cardCls}"><span class="scope-badge">${badge}</span><h3>${title}</h3>${items}</div></div>`;
}

function timelineItem(week, label, widthPct) {
  return `<div class="tl-row"><span class="tl-week">${week}</span><div class="tl-bar-cell"><div class="tl-bar-bg"><div class="tl-bar-fill" style="width:${widthPct}%"></div></div></div><span class="tl-label">${label}</span></div>`;
}

function priceCol(featured, optionLabel, name, amount, amountSub, features) {
  const cls = featured ? 'price-card featured' : 'price-card';
  const items = features.map(f => `<div class="price-feature">${f}</div>`).join('');
  return `<div class="pricing-col"><div class="${cls}"><span class="price-option-label">${optionLabel}</span><span class="price-name">${name}</span><span class="price-amount">${amount}</span><span class="price-vat">${amountSub}</span><hr class="price-hr">${items}</div></div>`;
}

function whyCard(num, title, desc) {
  return `<div class="why-col"><div class="why-card"><div class="why-icon-box">${num}</div><span class="why-title">${title}</span><span class="why-desc">${desc}</span></div></div>`;
}

function agendaTable(title, rows) {
  const rowsHtml = rows.map(r => {
    if (r.break) return `<tr class="agenda-break"><td colspan="3">${r.label || 'Przerwa'}</td></tr>`;
    return `<tr><td class="agenda-time">${hs(r.time)}</td><td class="agenda-block">${hs(r.block)}</td><td class="agenda-desc">${hs(r.desc)}</td></tr>`;
  }).join('');
  const titleHtml = title ? `<h3>${title}</h3>` : '';
  return `${titleHtml}<table class="agenda-table"><thead><tr><th>Czas</th><th>Blok</th><th>Co robimy</th></tr></thead><tbody>${rowsHtml}</tbody></table>`;
}

// ── Twarde spacje (polskie typografia) ────────────────────
// Zamienia "z ", "w ", "i ", "o ", "u ", "a " na wersje z &nbsp;
// żeby krótkie przyimki nie zostawały na końcu linii
function hardSpaces(text) {
  if (!text) return text;
  return text
    .replace(/(\s)(z|w|i|o|u|a|Z|W|I|O|U|A)\s/g, '$1$2\u00A0')
    .replace(/^(z|w|i|o|u|a|Z|W|I|O|U|A)\s/g, '$1\u00A0');
}

function ctaStep(num, text) {
  return `<div class="cta-step"><div class="cta-num-cell"><span class="cta-num">${num}</span></div><div class="cta-text-cell">${text}</div></div>`;
}

// ── Buduj sekcje z danych (z twardymi spacjami) ──────────
const hs = hardSpaces; // alias

const painHtml = (data.pains || []).map(p => painItem(hs(p.title), hs(p.desc))).join('');
const approachHtml = (data.approach || []).map((s,i) => approachStep(i+1, hs(s.title), hs(s.desc))).join('');

const scopeColsHtml = [
  scopeCol(false, data.optionA.badge || 'Szkolenie 1', hs(data.optionA.name), data.optionA.deliverables.map(hs)),
  scopeCol(true,  data.optionB.badge || 'Szkolenie 2', hs(data.optionB.name), data.optionB.deliverables.map(hs)),
].join('');

const timelineHtml = (data.timeline || []).map(t => timelineItem(t.week, hs(t.label), t.width)).join('');

let pricingColsHtml;
if (data.pricingTable && Array.isArray(data.pricingTable)) {
  const rows = data.pricingTable.map(r => {
    if (r.isNote) {
      return `<tr><td colspan="5" style="background:#F8FAFC;font-style:italic;color:var(--muted);padding:10px 12px;">${hs(r.note)}</td></tr>`;
    }
    return `<tr>
      <td>
        <div class="pc-item">${hs(r.item)}</div>
        ${r.meta ? `<div class="pc-meta">${hs(r.meta)}</div>` : ''}
      </td>
      <td class="pc-market">${hs(r.marketPrice)}</td>
      <td class="pc-vector">${hs(r.vectorPrice)}</td>
      <td class="pc-discount">${hs(r.discount || '')}</td>
    </tr>`;
  }).join('');
  const footNote = data.pricingFootnote ? `<tfoot><tr><td colspan="4">${hs(data.pricingFootnote)}</td></tr></tfoot>` : '';
  pricingColsHtml = `<table class="pricing-comparison">
    <thead>
      <tr>
        <th>Pozycja</th>
        <th style="text-align:right;">Cena standardowa</th>
        <th style="text-align:right;">Cena dla ${data.clientName}</th>
        <th style="text-align:center;">Rabat</th>
      </tr>
    </thead>
    <tbody>${rows}</tbody>
    ${footNote}
  </table>`;
} else {
  pricingColsHtml = [
    priceCol(false, data.optionA.badge || 'Szkolenie 1', hs(data.optionA.name), data.optionA.price, 'netto + 23% VAT', data.optionA.features.map(hs)),
    priceCol(true,  data.optionB.badge || 'Szkolenie 2', hs(data.optionB.name), data.optionB.price, 'netto + 23% VAT', data.optionB.features.map(hs)),
  ].join('');
}

// Why rows — 2x2 grid with numbered icons
const whyItems = data.whyUs || [];
let whyRowsHtml = '';
for (let i = 0; i < whyItems.length; i += 2) {
  whyRowsHtml += '<div class="why-row">';
  whyRowsHtml += whyCard(i+1, hs(whyItems[i].title), hs(whyItems[i].desc));
  if (whyItems[i+1]) {
    whyRowsHtml += whyCard(i+2, hs(whyItems[i+1].title), hs(whyItems[i+1].desc));
  }
  whyRowsHtml += '</div>';
}

const ctaHtml = (data.ctaSteps || []).map((s,i) => ctaStep(i+1, hs(s))).join('');

// Agenda pages (optional — each agenda gets its own page)
let agendaPageHtml = '';
if (data.agendas && data.agendas.length > 0) {
  agendaPageHtml = data.agendas.map((a, idx) => `
<div class="page">
  <div class="page-header">
    <div class="logo-cell"><img src="${logoBlackDataUrl}" alt="Dokodu"></div>
    <div class="client-cell">${data.clientName} — Propozycja ${data.date}</div>
  </div>
  <span class="section-label">Agenda${data.agendas.length > 1 ? ` (${idx+1}/${data.agendas.length})` : ''}</span>
  <h2>${hs(a.title)}</h2>
  ${agendaTable('', a.rows)}
  <div class="page-footer">
    <span class="footer-left">Dokodu Sp. z o.o. | kacper@dokodu.it | dokodu.it</span>
    <span class="footer-right">${4 + idx}</span>
  </div>
</div>`).join('');
}

// ── Podmień placeholdery ──────────────────────────────────
const coverTitle = data.coverTitle || `Automatyzacja AI<br>dla <span class="cover-title-highlight">${data.clientName}</span>`;

const replacements = {
  '{{LOGO_COVER}}':     logoWhiteDataUrl,
  '{{LOGO_PATH}}':      logoBlackDataUrl,
  '{{CLIENT_NAME}}':    data.clientName,
  '{{DATE}}':           data.date,
  '{{VALID_UNTIL}}':    data.validUntil,
  '{{COVER_TITLE}}':    coverTitle,
  '{{COVER_SUBTITLE}}': hs(data.coverSubtitle),
  '{{EXEC_SUMMARY}}':   hs(data.execSummary),
  '{{PROBLEM_INTRO}}':  hs(data.problemIntro),
  '{{PAIN_ITEMS}}':     painHtml,
  '{{APPROACH_STEPS}}': approachHtml,
  '{{SCOPE_COLS}}':     scopeColsHtml,
  '{{AGENDA_PAGE}}':    agendaPageHtml,
  '{{TIMELINE_ITEMS}}': timelineHtml,
  '{{PRICING_COLS}}':   pricingColsHtml,
  '{{PRICING_HEADLINE}}': hs(data.pricingHeadline || 'Dwie opcje dopasowane do Państwa potrzeb'),
  '{{ROI_HEADLINE}}':   data.roiHeadline,
  '{{ROI_DETAIL}}':     data.roiDetail,
  '{{WHY_ROWS}}':       whyRowsHtml,
  '{{CTA_STEPS}}':      ctaHtml,
};

for (const [key, val] of Object.entries(replacements)) {
  html = html.replaceAll(key, val || '');
}

// ── Generuj PDF ───────────────────────────────────────────
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  await page.setContent(html, { waitUntil: 'networkidle' });

  await page.pdf({
    path: outputPath,
    format: 'A4',
    printBackground: true,
    margin: { top: '0', bottom: '0', left: '0', right: '0' },
  });

  await browser.close();
  console.log(`✅ PDF wygenerowany: ${outputPath}`);
})();

// ── Dane testowe ──────────────────────────────────────────
function getTestData() {
  const today = new Date();
  const valid = new Date(today); valid.setDate(valid.getDate() + 14);
  const fmt = d => d.toLocaleDateString('pl-PL', { day: 'numeric', month: 'long', year: 'numeric' });

  return {
    clientName:    'SayFlu',
    clientSlug:    'SayFlu',
    date:          fmt(today),
    validUntil:    fmt(valid),
    coverTitle:    `Szkolenia AI<br>dla <span class="cover-title-highlight">SayFlu</span>`,
    coverSubtitle: 'Promptowanie i automatyzacja dla zespolu agencji kreatywnej.',
    execSummary:   'Testowy executive summary.',
    problemIntro:  'Testowy wstep do problemu:',
    pains: [
      { title: 'Raporty kampanii', desc: 'Kazda kampania = raport.' },
      { title: 'Przeciazony email', desc: 'Watki uciekaja, brak priorytetyzacji.' },
    ],
    approach: [
      { title: 'Szkolenie AI (5h)', desc: 'Prompt engineering, GEMs, maile.' },
      { title: 'Szkolenie n8n (7h)', desc: 'Automatyzacja workflow.' },
    ],
    optionA: {
      badge: 'Szkolenie 1',
      name: 'AI & Promptowanie',
      deliverables: ['5h warsztatu', 'Prompt engineering', 'Google GEMs'],
      features: ['5 godzin', 'Do 10 osob', 'Certyfikat'],
      price: '4 900 PLN',
    },
    optionB: {
      badge: 'Szkolenie 2',
      name: 'Automatyzacja n8n',
      deliverables: ['7h warsztatu', 'n8n od zera', '2-3 workflow'],
      features: ['7 godzin', 'Do 10 osob', 'Nagranie'],
      price: '5 900 PLN',
    },
    timeline: [
      { week: 'Krok 1', label: 'Ankieta', width: 15 },
      { week: 'Szkolenie 1', label: 'AI (5h)', width: 40 },
      { week: 'Szkolenie 2', label: 'n8n (7h)', width: 65 },
    ],
    roiHeadline: 'Pakiet: 9 400 PLN netto',
    roiDetail:   'Oszczednosc 1 400 PLN.',
    whyUs: [
      { title: 'Praktyk', desc: 'Live demo, nie PowerPoint.' },
      { title: 'Znamy agencje', desc: 'Szkolilismy Animex.' },
      { title: 'Szyte na miare', desc: 'Dedykowane pod Was.' },
      { title: 'Po polsku', desc: 'Polski jezyk, polska faktura.' },
    ],
    ctaSteps: [
      'Omowcie oferte wewnetrznie',
      'Wybierzcie szkolenie i termin',
      'Wysle ankiete i agende',
    ],
  };
}
