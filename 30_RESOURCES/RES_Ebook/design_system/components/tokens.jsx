// Design tokens — LIGHT mode, dokodu.it-inspired (warm cream paper, deep navy ink, orange accent)
const tokens = {
  color: {
    // paper / surfaces (LIGHT)
    paper:       '#FAF7F0',   // warm cream body bg
    paperAlt:    '#F2ECDF',   // slightly deeper band
    paperElev:   '#FFFFFF',   // elevated card surface
    surfaceTint: '#EFE8D6',   // call-out tint
    hairline:    'rgba(20,25,45,0.10)',
    hairline2:   'rgba(20,25,45,0.18)',

    // ink (text on light)
    ink:         '#141B2D',   // deep navy body text
    inkDim:      '#3A4560',
    inkMute:     '#7A8299',

    // dark variants (kept for cover / chapter / image-led)
    bg:          '#0B1120',
    bgElev:      '#111A30',
    surface:     '#16213A',
    hairlineDark:'rgba(255,255,255,0.10)',
    text:        '#F5F1E6',
    textDim:     '#B8BFD1',
    textMute:    '#7C8499',

    // accents — warm dokodu palette
    orange:      'oklch(0.70 0.17 50)',    // primary brand accent (warm)
    orangeDeep:  'oklch(0.58 0.18 45)',
    navy:        '#141B2D',
    navyMid:     'oklch(0.35 0.08 255)',
    blueInk:     'oklch(0.45 0.12 250)',   // for subtle link/emphasis on light

    // code
    codeBg:       '#F2ECDF',
    codeBgDark:   '#0B1020',
    codeText:     '#2A3045',
    codeKeyword:  'oklch(0.45 0.18 310)',  // deep magenta
    codeString:   'oklch(0.48 0.12 145)',  // deep green
    codeNumber:   'oklch(0.55 0.16 45)',   // orange
    codeFn:       'oklch(0.50 0.14 250)',  // deep blue
    codeComment:  '#9A9280',
  },
  font: {
    sans:  "'Inter', system-ui, -apple-system, Helvetica, sans-serif",
    mono:  "'JetBrains Mono', 'Fira Code', ui-monospace, monospace",
  },
  page: {
    w: 1240, h: 1754,
    margin: 72,
    cols: 12,
    gutter: 24,
  },
};

// Page shell — defaults to LIGHT paper; pass variant="dark" for cover/chapter/image-led
const Page = ({ children, variant = 'light', label, pageNum, showChrome = true, bleed = false }) => {
  const isDark = variant === 'dark' || variant === 'darkElev';
  const bg = variant === 'dark'      ? tokens.color.bg
           : variant === 'darkElev'  ? tokens.color.bgElev
           : variant === 'paperAlt'  ? tokens.color.paperAlt
           : variant === 'paperElev' ? tokens.color.paperElev
           :                           tokens.color.paper;
  const fg = isDark ? tokens.color.text : tokens.color.ink;
  return (
    <div
      data-screen-label={label}
      style={{
        width: tokens.page.w, height: tokens.page.h,
        background: bg, color: fg,
        position: 'relative', overflow: 'hidden',
        fontFamily: tokens.font.sans,
        boxShadow: '0 40px 100px rgba(12,18,40,0.25), 0 0 0 1px rgba(20,25,45,0.06)',
        borderRadius: 2,
      }}
    >
      <div style={{
        position: 'absolute',
        inset: bleed ? 0 : tokens.page.margin,
        display: 'flex', flexDirection: 'column',
      }}>
        {children}
      </div>
      {showChrome && <PageChrome dark={isDark} pageNum={pageNum} label={label} />}
    </div>
  );
};

const PageChrome = ({ dark, pageNum, label }) => {
  const c = dark ? tokens.color.textMute : tokens.color.inkMute;
  return (
    <>
      <div style={{
        position: 'absolute', top: 32, left: tokens.page.margin, right: tokens.page.margin,
        display: 'flex', justifyContent: 'space-between',
        fontFamily: tokens.font.mono, fontSize: 10, letterSpacing: '0.14em',
        textTransform: 'uppercase', color: c,
      }}>
        <span>Dokodu · AI Compendium</span>
        <span>{label || '—'}</span>
      </div>
      <div style={{
        position: 'absolute', bottom: 32, left: tokens.page.margin, right: tokens.page.margin,
        display: 'flex', justifyContent: 'space-between',
        fontFamily: tokens.font.mono, fontSize: 10, letterSpacing: '0.14em', color: c,
      }}>
        <span>dokodu.it</span>
        <span>{pageNum ? String(pageNum).padStart(3, '0') : ''}</span>
      </div>
    </>
  );
};

// Placeholder w wersji light + dark
const ImgPlaceholder = ({ w = '100%', h = 300, label = 'IMAGE', note, tone = 'orange', dark = false, style = {} }) => {
  const colMap = {
    orange: { stripe: dark ? 'rgba(255,170,90,0.10)' : 'rgba(200,110,40,0.08)', stroke: tokens.color.orange },
    navy:   { stripe: dark ? 'rgba(120,160,255,0.08)' : 'rgba(20,27,45,0.06)',  stroke: dark ? 'rgba(200,210,240,0.35)' : tokens.color.navyMid },
    neutral:{ stripe: dark ? 'rgba(255,255,255,0.05)' : 'rgba(20,27,45,0.05)',  stroke: dark ? 'rgba(255,255,255,0.2)' : 'rgba(20,27,45,0.22)' },
  };
  const { stripe, stroke } = colMap[tone] || colMap.neutral;
  const labelColor = dark ? tokens.color.textDim : tokens.color.inkMute;
  return (
    <div style={{
      width: w, height: h,
      background: `repeating-linear-gradient(45deg, transparent 0 12px, ${stripe} 12px 13px)`,
      border: `1px dashed ${stroke}`,
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      flexDirection: 'column', gap: 6,
      fontFamily: tokens.font.mono, fontSize: 11, letterSpacing: '0.12em',
      color: labelColor, textTransform: 'uppercase',
      ...style,
    }}>
      <div style={{ opacity: 0.9 }}>[ {label} ]</div>
      {note && <div style={{ fontSize: 9, opacity: 0.7, textTransform: 'none', letterSpacing: '0.04em', maxWidth: '70%', textAlign: 'center' }}>{note}</div>}
    </div>
  );
};

const Tag = ({ children, tone = 'orange', dark = false }) => {
  const c = tone === 'orange' ? tokens.color.orange
          : tone === 'navy'   ? (dark ? '#BFC8DA' : tokens.color.navy)
          : tokens.color.blueInk;
  const bg = dark ? `${c} / 0.08` : `${c} / 0.06`;
  return (
    <span style={{
      display: 'inline-flex', alignItems: 'center', gap: 6,
      padding: '4px 10px', borderRadius: 2,
      border: `1px solid ${c}`, color: c,
      fontFamily: tokens.font.mono, fontSize: 10, letterSpacing: '0.14em',
      textTransform: 'uppercase',
      background: dark ? `color-mix(in oklch, ${c} 12%, transparent)` : `color-mix(in oklch, ${c} 8%, transparent)`,
    }}>
      <span style={{ width: 5, height: 5, background: c, borderRadius: '50%' }} />
      {children}
    </span>
  );
};

const Card = ({ children, dark = false, style = {} }) => (
  <div style={{
    background: dark ? 'rgba(255,255,255,0.03)' : tokens.color.paperElev,
    backdropFilter: dark ? 'blur(20px)' : 'none',
    border: `1px solid ${dark ? 'rgba(255,255,255,0.1)' : tokens.color.hairline}`,
    borderRadius: 4,
    padding: 24,
    ...style,
  }}>
    {children}
  </div>
);
const GlassCard = Card; // backcompat

// Generative grid for dark hero pages
const GenerativeGrid = ({ opacity = 0.5, density = 40, color = 'white' }) => {
  const dots = [];
  for (let i = 0; i < density; i++) {
    for (let j = 0; j < density; j++) {
      const jitter = Math.sin(i * 7.3 + j * 3.1) * 0.5 + 0.5;
      const size = jitter > 0.7 ? 2 : 1;
      dots.push(
        <circle key={`${i}-${j}`}
          cx={(i + 0.5) * (100 / density)}
          cy={(j + 0.5) * (100 / density)}
          r={size * 0.15}
          fill={color}
          opacity={jitter * 0.6}
        />
      );
    }
  }
  return (
    <svg viewBox="0 0 100 100" preserveAspectRatio="none"
      style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', opacity }}>
      {dots}
    </svg>
  );
};

Object.assign(window, { tokens, Page, PageChrome, ImgPlaceholder, Tag, Card, GlassCard, GenerativeGrid });
