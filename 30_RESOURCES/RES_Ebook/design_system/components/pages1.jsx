// Page templates part 1: Cover (DARK), TOC (LIGHT), Chapter break (DARK)

const LOREM = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.";
const LOREM_LONG = LOREM + " Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Curabitur pretium tincidunt lacus. Nulla gravida orci a odio. Nullam varius, turpis et commodo pharetra, est eros bibendum elit, nec luctus magna felis sollicitudin mauris.";

// 1. COVER — keeps DARK treatment per user request
const PageCover = () => (
  <Page label="COVER" variant="dark" showChrome={false} bleed>
    <div style={{ position: 'absolute', inset: 0, background:
      'radial-gradient(ellipse at 25% 15%, oklch(0.45 0.14 40 / 0.55), transparent 58%),' +
      'radial-gradient(ellipse at 80% 85%, oklch(0.35 0.1 250 / 0.5), transparent 55%),' +
      'radial-gradient(ellipse at 55% 55%, oklch(0.40 0.18 45 / 0.25), transparent 60%)' }} />
    <GenerativeGrid opacity={0.32} density={50} />

    <div style={{ position: 'absolute', top: 48, left: 72, right: 72,
      display: 'flex', justifyContent: 'space-between',
      fontFamily: tokens.font.mono, fontSize: 11, letterSpacing: '0.2em',
      color: tokens.color.textDim, textTransform: 'uppercase' }}>
      <span>Dokodu · Vol. 01</span>
      <span>2026 · Ed. PL</span>
    </div>

    <div style={{ position: 'absolute', left: 40, top: '50%',
      transform: 'translateY(-50%) rotate(-90deg)', transformOrigin: 'left center',
      fontFamily: tokens.font.mono, fontSize: 10, letterSpacing: '0.4em',
      color: tokens.color.orange, textTransform: 'uppercase' }}>
      A Practical Field Guide — 284 pages
    </div>

    <div style={{ position: 'absolute', left: 72, right: 72, top: 380, display: 'flex', flexDirection: 'column', gap: 40 }}>
      <div style={{ fontFamily: tokens.font.mono, fontSize: 13, letterSpacing: '0.24em', color: tokens.color.orange, textTransform: 'uppercase' }}>
        01 / Compendium
      </div>
      <h1 style={{
        fontFamily: tokens.font.sans, fontWeight: 700,
        fontSize: 132, lineHeight: 0.92, letterSpacing: '-0.035em',
        color: tokens.color.text, margin: 0,
      }}>
        Sztuczna<br/>
        <span style={{
          color: tokens.color.orange,
          fontStyle: 'italic', fontWeight: 500,
        }}>inteligencja</span><br/>
        <span style={{ opacity: 0.45, fontWeight: 300 }}>w praktyce.</span>
      </h1>
      <div style={{ display: 'flex', gap: 10 }}>
        <Tag tone="orange" dark>LLM</Tag>
        <Tag tone="orange" dark>Etyka</Tag>
        <Tag tone="orange" dark>Wdrożenia</Tag>
      </div>
    </div>

    <div style={{ position: 'absolute', left: 72, right: 72, bottom: 56,
      display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' }}>
      <div>
        <div style={{ fontFamily: tokens.font.mono, fontSize: 10, letterSpacing: '0.2em',
          color: tokens.color.textMute, textTransform: 'uppercase', marginBottom: 10 }}>Wydane przez</div>
        <div style={{ fontFamily: tokens.font.sans, fontSize: 22, fontWeight: 500, letterSpacing: '-0.01em' }}>
          dokodu.it
        </div>
      </div>
      <div style={{ textAlign: 'right', fontFamily: tokens.font.mono, fontSize: 10,
        color: tokens.color.textMute, letterSpacing: '0.12em' }}>
        ISBN 978-83-0000-000-0<br/>
        EAN · PL · PDF · EPUB
      </div>
    </div>

    <Corner pos="tl" /><Corner pos="tr" /><Corner pos="bl" /><Corner pos="br" />
  </Page>
);

const Corner = ({ pos }) => {
  const s = 18, o = 28;
  const c = tokens.color.orange;
  const styles = {
    tl: { top: o, left: o, borderTop: `1px solid ${c}`, borderLeft: `1px solid ${c}` },
    tr: { top: o, right: o, borderTop: `1px solid ${c}`, borderRight: `1px solid ${c}` },
    bl: { bottom: o, left: o, borderBottom: `1px solid ${c}`, borderLeft: `1px solid ${c}` },
    br: { bottom: o, right: o, borderBottom: `1px solid ${c}`, borderRight: `1px solid ${c}` },
  };
  return <div style={{ position: 'absolute', width: s, height: s, ...styles[pos] }} />;
};

// 2. TABLE OF CONTENTS — LIGHT
const PageTOC = () => {
  const chapters = [
    { n: '01', title: 'Wstęp do LLM', abs: 'Jak modele językowe widzą świat. Tokeny, wektory, uwaga.', page: 12, parts: 4 },
    { n: '02', title: 'Architektury sieci neuronowych', abs: 'Transformer, konwolucja, dyfuzja — wizualnie.', page: 38, parts: 6 },
    { n: '03', title: 'Prompt engineering', abs: 'Nie rozmawiasz z AI. Programujesz ją językiem.', page: 72, parts: 5 },
    { n: '04', title: 'RAG i bazy wektorowe', abs: 'Retrieval, embeddingi, chunking dokumentów.', page: 106, parts: 4 },
    { n: '05', title: 'Agenci AI w biznesie', abs: 'Autonomia, narzędzia, pętle decyzyjne.', page: 138, parts: 5 },
    { n: '06', title: 'Etyka w AI', abs: 'Bias, hallucinations, AI Act — po ludzku.', page: 176, parts: 4 },
    { n: '07', title: 'Wdrożenia i ROI', abs: 'Case studies z polskich firm.', page: 212, parts: 3 },
    { n: '08', title: 'Cheat Sheets', abs: 'Gotowe karty referencyjne do druku.', page: 248, parts: 6 },
  ];
  return (
    <Page label="SPIS TREŚCI · 002" pageNum={2} variant="light">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 40 }}>
        <div>
          <div style={{ fontFamily: tokens.font.mono, fontSize: 11, letterSpacing: '0.2em', color: tokens.color.orange, textTransform: 'uppercase' }}>Indeks</div>
          <h2 style={{ fontFamily: tokens.font.sans, fontSize: 88, fontWeight: 700, letterSpacing: '-0.035em', lineHeight: 0.95, margin: '12px 0 0', color: tokens.color.navy }}>
            Spis<br/>
            <span style={{ color: tokens.color.inkMute, fontWeight: 300 }}>treści</span>
          </h2>
        </div>
        <div style={{ fontFamily: tokens.font.mono, fontSize: 11, color: tokens.color.inkMute, textAlign: 'right', lineHeight: 1.6 }}>
          08 rozdziałów<br/>
          37 sekcji<br/>
          12 cheat-sheetów<br/>
          284 stron
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0 32px', flex: 1, alignContent: 'start' }}>
        {chapters.map((c, i) => (
          <div key={c.n} style={{
            gridColumn: i % 3 === 1 ? 'span 2' : 'span 1',
            borderTop: `1px solid ${tokens.color.hairline}`,
            padding: '20px 0 22px',
            display: 'flex', gap: 20, alignItems: 'flex-start',
          }}>
            <div style={{ fontFamily: tokens.font.mono, fontSize: 13, color: tokens.color.orange, letterSpacing: '0.1em', minWidth: 36, fontWeight: 500 }}>
              {c.n}
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', gap: 12 }}>
                <h3 style={{ fontSize: 22, fontWeight: 600, letterSpacing: '-0.015em', margin: 0, color: tokens.color.navy }}>{c.title}</h3>
                <div style={{ fontFamily: tokens.font.mono, fontSize: 12, color: tokens.color.inkDim }}>p.{c.page}</div>
              </div>
              <p style={{ fontSize: 13, lineHeight: 1.55, color: tokens.color.inkDim, margin: '8px 0 0', maxWidth: 360 }}>
                {c.abs}
              </p>
              <div style={{ display: 'flex', gap: 4, marginTop: 12 }}>
                {Array.from({ length: c.parts }).map((_, k) => (
                  <div key={k} style={{ flex: 1, height: 2, background: k === 0 ? tokens.color.orange : tokens.color.hairline2 }} />
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </Page>
  );
};

// 3. CHAPTER BREAK — keeps DARK
const PageChapterBreak = ({ n = '03', title = 'Prompt\nengineering', abstract = "Model nie zgaduje intencji. Intencja musi być wpisana w strukturę zapytania. W tym rozdziale pokażemy, jak projektować prompty jak interfejsy.", kicker = 'Rozdział trzeci' }) => (
  <Page label={`ROZDZIAŁ ${n}`} pageNum={72} showChrome={false} bleed variant="dark">
    <div style={{ position: 'absolute', inset: 0,
      background: `radial-gradient(circle at 25% 70%, oklch(0.38 0.15 45 / 0.55), transparent 55%),` +
                  `radial-gradient(circle at 85% 25%, oklch(0.30 0.10 250 / 0.5), transparent 60%),` +
                  tokens.color.bg }} />
    <GenerativeGrid opacity={0.18} density={60} />

    <div style={{
      position: 'absolute', right: -40, top: 140,
      fontFamily: tokens.font.sans, fontWeight: 200,
      fontSize: 820, lineHeight: 0.8,
      color: 'transparent',
      WebkitTextStroke: `1px ${tokens.color.orange}`,
      letterSpacing: '-0.05em',
      opacity: 0.7,
    }}>
      {n}
    </div>

    <div style={{ position: 'absolute', top: 72, left: 72, display: 'flex', alignItems: 'center', gap: 16 }}>
      <div style={{ width: 40, height: 1, background: tokens.color.orange }} />
      <div style={{ fontFamily: tokens.font.mono, fontSize: 12, letterSpacing: '0.25em', color: tokens.color.orange, textTransform: 'uppercase' }}>
        {kicker} / {n} of 08
      </div>
    </div>

    <div style={{ position: 'absolute', left: 72, bottom: 260, maxWidth: 760 }}>
      <h1 style={{
        fontFamily: tokens.font.sans, fontSize: 128, fontWeight: 700,
        letterSpacing: '-0.035em', lineHeight: 0.92, margin: 0,
        whiteSpace: 'pre-wrap',
      }}>
        {title.split('\n').map((line, i) => (
          <span key={i} style={{ display: 'block', color: i === 0 ? tokens.color.text : 'transparent',
            WebkitTextStroke: i === 0 ? 'none' : `1.5px ${tokens.color.text}`,
            fontWeight: i === 0 ? 700 : 200 }}>
            {line}
          </span>
        ))}
      </h1>
    </div>

    <div style={{ position: 'absolute', left: 72, bottom: 120, maxWidth: 520 }}>
      <div style={{ fontFamily: tokens.font.mono, fontSize: 10, letterSpacing: '0.2em', color: tokens.color.textMute, marginBottom: 12, textTransform: 'uppercase' }}>
        — Abstrakt
      </div>
      <p style={{ fontSize: 18, lineHeight: 1.5, color: tokens.color.textDim, margin: 0, fontWeight: 300 }}>
        {abstract}
      </p>
    </div>

    <div style={{ position: 'absolute', right: 72, bottom: 120, width: 220, fontFamily: tokens.font.mono, fontSize: 10, color: tokens.color.textMute, letterSpacing: '0.08em' }}>
      <div style={{ borderTop: `1px solid ${tokens.color.hairlineDark}`, paddingTop: 12, marginBottom: 16 }}>
        <div style={{ color: tokens.color.orange, marginBottom: 4 }}>CZAS CZYTANIA</div>
        <div style={{ color: tokens.color.text, fontSize: 14 }}>~ 42 min</div>
      </div>
      <div style={{ borderTop: `1px solid ${tokens.color.hairlineDark}`, paddingTop: 12, marginBottom: 16 }}>
        <div style={{ color: tokens.color.orange, marginBottom: 4 }}>POZIOM</div>
        <div style={{ color: tokens.color.text, fontSize: 14 }}>Średniozaawansowany</div>
      </div>
      <div style={{ borderTop: `1px solid ${tokens.color.hairlineDark}`, paddingTop: 12 }}>
        <div style={{ color: tokens.color.orange, marginBottom: 4 }}>SEKCJE</div>
        <div style={{ color: tokens.color.text, fontSize: 14 }}>3.1 – 3.5</div>
      </div>
    </div>

    <div style={{ position: 'absolute', bottom: 48, left: 72, right: 72,
      display: 'flex', justifyContent: 'space-between',
      fontFamily: tokens.font.mono, fontSize: 10, color: tokens.color.textMute, letterSpacing: '0.12em' }}>
      <span>dokodu.it / ai-compendium</span>
      <span>072</span>
    </div>
  </Page>
);

Object.assign(window, { PageCover, PageTOC, PageChapterBreak, LOREM, LOREM_LONG, Corner });
