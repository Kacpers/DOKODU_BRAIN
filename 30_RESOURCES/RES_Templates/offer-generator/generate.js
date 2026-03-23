#!/usr/bin/env node
/**
 * Dokodu Offer Generator
 * Przyjmuje plik JSON z danymi oferty, generuje PDF.
 *
 * Użycie:
 *   node generate.js <offer_data.json> [output.pdf]
 *
 * Lub z danymi wbudowanymi (tryb testowy):
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

const logoPath = path.join(__dirname, 'assets', 'logo_black.avif');
const logoDataUrl = `data:image/avif;base64,${fs.readFileSync(logoPath).toString('base64')}`;

// Helpery do generowania bloków HTML
function painItem(icon, title, desc) {
  return `<div class="pain-item"><div class="icon">${icon}</div><div class="text"><strong>${title}</strong>${desc}</div></div>`;
}

function approachStep(num, title, desc) {
  return `<div class="step"><div class="step-number">${num}</div><div class="step-body"><strong>${title}</strong><span>${desc}</span></div></div>`;
}

function deliverableItem(text) {
  return `<li>${text}</li>`;
}

function scopeCard(featured, badge, title, deliverables) {
  const cls = featured ? 'option-card featured' : 'option-card';
  const items = deliverables.map(deliverableItem).join('');
  return `<div class="${cls}"><div class="badge">${badge}</div><h3>${title}</h3><ul class="deliverable-list">${items}</ul></div>`;
}

function timelineItem(week, label, widthPct) {
  return `<div class="timeline-item"><div class="timeline-week">${week}</div><div class="timeline-bar-wrap"><div class="timeline-bar" style="width:${widthPct}%"></div><div class="timeline-label">${label}</div></div></div>`;
}

function priceCard(featured, optionLabel, name, amount, amountSub, features) {
  const cls = featured ? 'price-card featured' : 'price-card';
  const items = features.map(f => `<div class="price-feature">${f}</div>`).join('');
  return `<div class="${cls}"><div class="option-label">${optionLabel}</div><div class="price-name">${name}</div><div class="amount">${amount}</div><div class="amount-sub">${amountSub}</div><hr>${items}</div>`;
}

function whyItem(icon, title, desc) {
  return `<div class="why-item"><div class="why-icon">${icon}</div><strong>${title}</strong><span>${desc}</span></div>`;
}

function ctaStep(num, text) {
  return `<div class="cta-step"><div class="num">${num}</div><div class="text">${text}</div></div>`;
}

// ── Buduj sekcje z danych ─────────────────────────────────
const painHtml = (data.pains || []).map(p => painItem(p.icon, p.title, p.desc)).join('');
const approachHtml = (data.approach || []).map((s,i) => approachStep(i+1, s.title, s.desc)).join('');

const scopeHtml = [
  scopeCard(false, 'Opcja A — MVP', data.optionA.name, data.optionA.deliverables),
  scopeCard(true,  'Opcja B — Pełne rozwiązanie', data.optionB.name, data.optionB.deliverables),
].join('');

const timelineHtml = (data.timeline || []).map(t => timelineItem(t.week, t.label, t.width)).join('');

const pricingHtml = [
  priceCard(false, 'Opcja A', data.optionA.name, data.optionA.price, 'netto + 23% VAT', data.optionA.features),
  priceCard(true,  'Opcja B', data.optionB.name, data.optionB.price, 'netto + 23% VAT', data.optionB.features),
].join('');

const whyHtml = (data.whyUs || []).map(w => whyItem(w.icon, w.title, w.desc)).join('');
const ctaHtml = (data.ctaSteps || []).map((s,i) => ctaStep(i+1, s)).join('');

// ── Podmień placeholdery ──────────────────────────────────
const replacements = {
  '{{LOGO_PATH}}':      logoDataUrl,
  '{{CLIENT_NAME}}':    data.clientName,
  '{{DATE}}':           data.date,
  '{{VALID_UNTIL}}':    data.validUntil,
  '{{COVER_SUBTITLE}}': data.coverSubtitle,
  '{{EXEC_SUMMARY}}':   data.execSummary,
  '{{PROBLEM_INTRO}}':  data.problemIntro,
  '{{PAIN_ITEMS}}':     painHtml,
  '{{APPROACH_STEPS}}': approachHtml,
  '{{SCOPE_CARDS}}':    scopeHtml,
  '{{TIMELINE_ITEMS}}': timelineHtml,
  '{{PRICING_CARDS}}':  pricingHtml,
  '{{ROI_HEADLINE}}':   data.roiHeadline,
  '{{ROI_DETAIL}}':     data.roiDetail,
  '{{WHY_ITEMS}}':      whyHtml,
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
    clientName:    'Firma Przykładowa S.A.',
    clientSlug:    'FirmaPrzykladowa',
    date:          fmt(today),
    validUntil:    fmt(valid),
    coverSubtitle: 'Automatyzacja procesów operacyjnych działu obsługi klienta z wykorzystaniem AI.',
    execSummary:   'Wasz dział BOK obsługuje miesięcznie ok. 2 000 zapytań, z czego 70% to powtarzalne pytania wymagające ręcznego wyszukiwania odpowiedzi. Proponujemy wdrożenie agenta AI zintegrowanego z Waszym systemem CRM, który automatycznie odpowie na 65% zapytań bez udziału człowieka — szacowana oszczędność: 3 etaty i 40 000 PLN miesięcznie.',
    problemIntro:  'W trakcie discovery call zidentyfikowaliśmy trzy główne obszary generujące straty operacyjne:',
    pains: [
      { icon: '⏱️', title: 'Czas odpowiedzi: 4–6 godzin', desc: 'Klienci czekają na prostą informację, którą agent AI udzieliłby w 3 sekundy.' },
      { icon: '🔁', title: '70% zapytań jest powtarzalnych', desc: 'Konsultanci ręcznie piszą te same odpowiedzi każdego dnia, zamiast zająć się złożonymi sprawami.' },
      { icon: '📉', title: 'CSAT spada przez czas oczekiwania', desc: 'Niezadowolenie klientów rośnie proporcjonalnie do czasu odpowiedzi — bezpośrednie ryzyko churn.' },
    ],
    approach: [
      { title: 'Analiza i mapowanie',         desc: 'Audyt Waszych procesów BOK: kategorie zapytań, źródła danych, systemy (CRM, helpdesk). Definiujemy zakres automatyzacji.' },
      { title: 'Budowa agenta AI',             desc: 'Wdrożenie agenta w n8n zintegrowanego z Waszym CRM i bazą wiedzy. Agent rozumie kontekst i odpowiada po polsku.' },
      { title: 'Testy i kalibracja',           desc: 'Dwutygodniowy okres testów z Waszym teamem. Uczymy agenta na realnych przypadkach z Waszej historii.' },
      { title: 'Wdrożenie i transfer wiedzy',  desc: 'Go-live na produkcji. Szkolenie Waszego zespołu z obsługi i monitorowania systemu.' },
    ],
    optionA: {
      name:        'Start AI',
      deliverables: ['Agent FAQ — 50 najczęstszych zapytań', 'Integracja z Waszym helpdeskiem', 'Dashboard monitoring w n8n', 'Szkolenie dla 2 administratorów', '1 miesiąc wsparcia po wdrożeniu'],
      features:    ['50 zautomatyzowanych odpowiedzi', 'Integracja helpdesk', 'Szkolenie zespołu', '1 mies. support'],
      price:       '24 900 PLN',
    },
    optionB: {
      name:        'AI Full Stack',
      deliverables: ['Wszystko z Opcji A', 'Agent obsługujący 200+ scenariuszy', 'Integracja CRM + helpdesk + e-mail', 'Eskalacja do człowieka (smart routing)', 'Miesięczny raport efektywności', 'Retainer 6 miesięcy (monitoring + optymalizacja)'],
      features:    ['200+ scenariuszy automatyzacji', 'CRM + helpdesk + e-mail', 'Smart routing do konsultantów', 'Retainer 6 mies. w cenie', 'Raport ROI co miesiąc'],
      price:       '54 900 PLN',
    },
    timeline: [
      { week: 'Tyg. 1–2',  label: 'Analiza i mapowanie procesów',    width: 30 },
      { week: 'Tyg. 3–5',  label: 'Budowa agenta AI',                 width: 55 },
      { week: 'Tyg. 6–7',  label: 'Testy z teamem klienta',           width: 42 },
      { week: 'Tyg. 8',    label: 'Go-live i przekazanie',            width: 20 },
      { week: 'Mies. 2–7', label: 'Retainer — monitoring (Opcja B)', width: 80 },
    ],
    roiHeadline: 'Zwrot inwestycji w ok. 2 miesiące',
    roiDetail:   'Przy obecnym koszcie 3 etatów BOK (~40 000 PLN/mies.) oszczędność za rok to ok. 480 000 PLN. Opcja A zwraca się w ~3 tygodnie.',
    whyUs: [
      { icon: '🏭', title: 'Znamy Waszą branżę',   desc: 'Zrealizowaliśmy podobny projekt dla firmy w branży produkcyjnej — efekty po 6 tygodniach.' },
      { icon: '⚖️', title: 'Tech + Legal w jednym', desc: 'Wdrożenie i compliance AI Act w jednym pakiecie. Alina (COO/Legal) dba o bezpieczeństwo prawne.' },
      { icon: '🔓', title: 'Zero lock-in',          desc: 'Cały kod i konfiguracja na Waszej infrastrukturze. Możecie to obsługiwać sami po przekazaniu.' },
      { icon: '🇵🇱', title: 'Polski support',       desc: 'Dostępni w języku polskim, w polskich godzinach pracy. Bez czekania na odpowiedź z innej strefy.' },
    ],
    ctaSteps: [
      'Odpiszcie na maila z potwierdzeniem wybranej opcji (A lub B)',
      'Prześlę umowę w ciągu 24 godzin',
      'Kickoff call — zarezerwujemy termin już teraz',
    ],
  };
}
