// Page templates part 2: Standard text (LIGHT), Case study (LIGHT), Infographic (LIGHT), Cheat sheet (LIGHT)

// 4. STANDARD TEXT PAGE — LIGHT, 2 col + sidenotes
const PageStandard = () => (
  <Page label="ROZDZIAŁ 03 · 3.2" pageNum={78} variant="light">
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 24 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
        <div style={{ fontFamily: tokens.font.mono, fontSize: 11, color: tokens.color.orange, letterSpacing: '0.18em', fontWeight: 500 }}>§ 3.2</div>
        <div style={{ fontFamily: tokens.font.mono, fontSize: 11, color: tokens.color.inkMute, letterSpacing: '0.12em' }}>PROMPT ENGINEERING / STRUKTURA ZAPYTANIA</div>
      </div>
      <div style={{ fontFamily: tokens.font.mono, fontSize: 10, color: tokens.color.inkMute }}>03 · 04 · 05</div>
    </div>

    <h2 style={{ fontSize: 44, fontWeight: 700, letterSpacing: '-0.025em', lineHeight: 1.05, margin: '0 0 8px', maxWidth: 780, color: tokens.color.navy }}>
      Dlaczego kontekst jest<br/>
      <span style={{ color: tokens.color.orange, fontWeight: 400, fontStyle: 'italic' }}>ważniejszy</span> niż instrukcja.
    </h2>
    <div style={{ fontFamily: tokens.font.mono, fontSize: 11, color: tokens.color.inkMute, letterSpacing: '0.12em', marginBottom: 32 }}>
      Rafał Kowalczyk · 8 min czytania · opublikowano 2026-03
    </div>

    <div style={{ display: 'grid', gridTemplateColumns: '3fr 3fr 2fr', gap: 32, flex: 1 }}>
      <div style={{ fontSize: 13.5, lineHeight: 1.7, color: tokens.color.inkDim }}>
        <p style={{ margin: '0 0 14px' }}>
          <span style={{ float: 'left', fontFamily: tokens.font.sans, fontSize: 72, fontWeight: 700, lineHeight: 0.8, marginRight: 10, marginTop: 6, color: tokens.color.orange }}>M</span>
          odel językowy nie „wie" nic o Twoim projekcie, dopóki tego nie powiesz. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
        </p>
        <p style={{ margin: '0 0 14px' }}>{LOREM}</p>
        <p style={{ margin: '0 0 14px' }}>
          Ut enim ad minim veniam, quis nostrud <em style={{ color: tokens.color.navy, fontStyle: 'normal', borderBottom: `1px dotted ${tokens.color.orange}` }}>exercitation ullamco laboris</em> nisi ut aliquip ex ea commodo consequat.
        </p>
        <p style={{ margin: 0 }}>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.</p>
      </div>

      <div style={{ fontSize: 13.5, lineHeight: 1.7, color: tokens.color.inkDim }}>
        <p style={{ margin: '0 0 14px' }}>Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
        <h4 style={{ fontSize: 16, fontWeight: 600, color: tokens.color.navy, margin: '20px 0 10px', letterSpacing: '-0.01em' }}>
          Cztery warstwy kontekstu
        </h4>
        <p style={{ margin: '0 0 14px' }}>{LOREM}</p>
        <div style={{
          fontFamily: tokens.font.mono, fontSize: 11, lineHeight: 1.55,
          background: tokens.color.codeBg, border: `1px solid ${tokens.color.hairline}`,
          padding: '14px 16px', borderRadius: 2,
          color: tokens.color.codeText, marginBottom: 14,
          borderLeft: `3px solid ${tokens.color.orange}`,
        }}>
          <div style={{ color: tokens.color.codeComment, marginBottom: 6, fontSize: 9, letterSpacing: '0.1em' }}># prompt.py</div>
          <div><span style={{ color: tokens.color.codeKeyword }}>def</span> <span style={{ color: tokens.color.codeFn }}>build_prompt</span>(ctx, task):</div>
          <div style={{ paddingLeft: 16 }}><span style={{ color: tokens.color.codeKeyword }}>return</span> f<span style={{ color: tokens.color.codeString }}>"{'{ctx.role}'}\n{'{task}'}"</span></div>
        </div>
        <p style={{ margin: 0 }}>Curabitur pretium tincidunt lacus. Nulla gravida orci a odio bibendum elit.</p>
      </div>

      <div style={{ borderLeft: `1px solid ${tokens.color.hairline}`, paddingLeft: 20, fontFamily: tokens.font.mono, fontSize: 10.5, lineHeight: 1.7, color: tokens.color.inkMute }}>
        <div style={{ marginBottom: 28 }}>
          <div style={{ color: tokens.color.orange, fontSize: 9, letterSpacing: '0.2em', marginBottom: 6, fontWeight: 500 }}>† PRZYPIS 01</div>
          <div>Termin „prompt engineering" został spopularyzowany w 2022 przez OpenAI, ale korzenie sięgają badań nad few-shot learning z 2020.</div>
        </div>
        <div style={{ marginBottom: 28 }}>
          <div style={{ color: tokens.color.orange, fontSize: 9, letterSpacing: '0.2em', marginBottom: 6, fontWeight: 500 }}>‡ DEFINICJA</div>
          <div style={{ color: tokens.color.ink, fontFamily: tokens.font.sans, fontSize: 12, lineHeight: 1.55 }}>
            <b>Kontekst</b> — wszystko, co model widzi w oknie uwagi przed wygenerowaniem odpowiedzi.
          </div>
        </div>
        <ImgPlaceholder h={140} label="DIAGRAM 3.2a" note="szkic uwagi wielogłowicowej" tone="orange" style={{ marginBottom: 20 }} />
        <div style={{ color: tokens.color.inkDim, fontSize: 10 }}>Fig. 3.2a — Porównanie okien uwagi przy różnych długościach kontekstu.</div>
      </div>
    </div>
  </Page>
);

// 5. CASE STUDY — LIGHT with tinted surface
const PageCaseStudy = () => (
  <Page label="CASE STUDY · 07.2" pageNum={218} variant="paperAlt">
    <div style={{
      marginBottom: 32, padding: '0 0 28px',
      borderBottom: `1px solid ${tokens.color.hairline2}`,
      display: 'grid', gridTemplateColumns: '180px 1fr 200px', gap: 28, alignItems: 'end',
    }}>
      <ImgPlaceholder w={180} h={180} label="PORTRET" note="zdjęcie rozmówcy" tone="orange" />
      <div>
        <div style={{ fontFamily: tokens.font.mono, fontSize: 11, color: tokens.color.orange, letterSpacing: '0.2em', marginBottom: 10, fontWeight: 500 }}>
          WYWIAD · CASE 07 / 12
        </div>
        <h2 style={{ fontFamily: tokens.font.sans, fontSize: 52, fontWeight: 700, letterSpacing: '-0.03em', lineHeight: 1, margin: '0 0 14px', color: tokens.color.navy }}>
          „Wdrożyliśmy AI<br/>i zwolniliśmy… <span style={{ color: tokens.color.orange, fontStyle: 'italic', fontWeight: 400 }}>Excela.</span>"
        </h2>
        <div style={{ fontFamily: tokens.font.sans, fontSize: 14, color: tokens.color.inkDim }}>
          <b style={{ color: tokens.color.navy }}>Magdalena Wiśniewska</b>, CFO · <span style={{ color: tokens.color.inkMute }}>NovaLogistics sp. z o.o.</span>
        </div>
      </div>
      <div style={{ fontFamily: tokens.font.mono, fontSize: 10, color: tokens.color.inkMute, letterSpacing: '0.08em', lineHeight: 1.7 }}>
        <div style={{ color: tokens.color.orange, marginBottom: 6, fontWeight: 500 }}>METADANE</div>
        Branża · Logistyka<br/>
        Zespół · 240 osób<br/>
        Czas wdrożenia · 6 tyg.<br/>
        Narzędzia · M365 Copilot
      </div>
    </div>

    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 28, flex: 1 }}>
      <div style={{ gridColumn: 'span 2', fontSize: 13.5, lineHeight: 1.7, color: tokens.color.inkDim }}>
        <div style={{ marginBottom: 20 }}>
          <div style={{ fontFamily: tokens.font.mono, fontSize: 10, color: tokens.color.orange, letterSpacing: '0.2em', marginBottom: 6, fontWeight: 600 }}>DK — DOKODU</div>
          <p style={{ margin: 0, color: tokens.color.navy, fontWeight: 500 }}>Jak wyglądał pierwszy dzień po uruchomieniu agenta?</p>
        </div>
        <div style={{ marginBottom: 22 }}>
          <div style={{ fontFamily: tokens.font.mono, fontSize: 10, color: tokens.color.inkMute, letterSpacing: '0.2em', marginBottom: 6 }}>MW</div>
          <p style={{ margin: 0 }}>{LOREM}</p>
        </div>
        <div style={{ marginBottom: 20 }}>
          <div style={{ fontFamily: tokens.font.mono, fontSize: 10, color: tokens.color.orange, letterSpacing: '0.2em', marginBottom: 6, fontWeight: 600 }}>DK</div>
          <p style={{ margin: 0, color: tokens.color.navy, fontWeight: 500 }}>Które procesy zostały zautomatyzowane najpierw?</p>
        </div>
        <div>
          <div style={{ fontFamily: tokens.font.mono, fontSize: 10, color: tokens.color.inkMute, letterSpacing: '0.2em', marginBottom: 6 }}>MW</div>
          <p style={{ margin: 0 }}>Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. {LOREM}</p>
        </div>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
        <div style={{ position: 'relative', padding: '8px 0 8px 28px', borderLeft: `4px solid ${tokens.color.orange}` }}>
          <div style={{ position: 'absolute', left: 14, top: -18, fontSize: 90, fontFamily: 'Georgia, serif', color: tokens.color.orange, lineHeight: 0.8, fontStyle: 'italic' }}>"</div>
          <p style={{ fontFamily: tokens.font.sans, fontSize: 22, fontWeight: 400, fontStyle: 'italic', lineHeight: 1.25, letterSpacing: '-0.015em', color: tokens.color.navy, margin: 0 }}>
            Największą zmianą nie była technologia, tylko <span style={{ color: tokens.color.orange, fontStyle: 'normal' }}>nawyk</span>.
          </p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
          {[
            ['–38%', 'czasu na raporty'],
            ['+4.2h', 'tygodniowo / osoba'],
            ['6 tyg.', 'okres wdrożenia'],
            ['ROI 4.7×', 'po 9 miesiącach'],
          ].map(([big, lbl]) => (
            <Card key={lbl} style={{ padding: '14px 16px' }}>
              <div style={{ fontFamily: tokens.font.sans, fontSize: 28, fontWeight: 600, letterSpacing: '-0.02em', color: tokens.color.orange }}>{big}</div>
              <div style={{ fontFamily: tokens.font.mono, fontSize: 9, letterSpacing: '0.14em', color: tokens.color.inkMute, textTransform: 'uppercase', marginTop: 2 }}>{lbl}</div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  </Page>
);

// 6. INFOGRAPHIC — LIGHT
const PageInfographic = () => (
  <Page label="FIG. 2.4 · ARCHITEKTURA" pageNum={56} variant="light">
    <div style={{ marginBottom: 24 }}>
      <div style={{ fontFamily: tokens.font.mono, fontSize: 11, color: tokens.color.orange, letterSpacing: '0.2em', marginBottom: 8, fontWeight: 500 }}>
        FIGURE 2.4 / ROZDZIAŁ 02
      </div>
      <h2 style={{ fontFamily: tokens.font.sans, fontSize: 48, fontWeight: 700, letterSpacing: '-0.03em', margin: '0 0 12px', lineHeight: 1, color: tokens.color.navy }}>
        Architektura modelu <span style={{ color: tokens.color.orange, fontWeight: 300, fontStyle: 'italic' }}>Transformer</span>
      </h2>
      <p style={{ fontSize: 14, lineHeight: 1.55, color: tokens.color.inkDim, maxWidth: 780, margin: 0 }}>
        Uproszczona reprezentacja przepływu tokenów przez bloki uwagi. Kolor odpowiada wadze gradientu — im intensywniejszy, tym silniejszy sygnał podczas trenowania.
      </p>
    </div>

    <div style={{ flex: 1, display: 'grid', gridTemplateColumns: '1fr 260px', gap: 28 }}>
      <Card style={{ padding: 32, position: 'relative', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <NeuralDiagram />
      </Card>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
        <div>
          <div style={{ fontFamily: tokens.font.mono, fontSize: 10, letterSpacing: '0.2em', color: tokens.color.inkMute, marginBottom: 12, fontWeight: 500 }}>LEGENDA</div>
          {[
            ['Input Embed', tokens.color.orange,     'Token → wektor 768D'],
            ['Attention',   tokens.color.navyMid,    'Multi-head self-attention'],
            ['Feed Forward','oklch(0.45 0.14 310)',  'Warstwa gęsta 3072'],
            ['Output Head', 'oklch(0.48 0.12 145)',  'Softmax · logits'],
          ].map(([lbl, col, desc]) => (
            <div key={lbl} style={{ display: 'flex', gap: 10, alignItems: 'flex-start', padding: '10px 0', borderTop: `1px solid ${tokens.color.hairline}` }}>
              <div style={{ width: 10, height: 10, background: col, marginTop: 4 }} />
              <div>
                <div style={{ fontSize: 12, fontWeight: 600, color: tokens.color.navy }}>{lbl}</div>
                <div style={{ fontFamily: tokens.font.mono, fontSize: 9.5, color: tokens.color.inkMute, letterSpacing: '0.04em', marginTop: 2 }}>{desc}</div>
              </div>
            </div>
          ))}
        </div>

        <div style={{ marginTop: 8 }}>
          <div style={{ fontFamily: tokens.font.mono, fontSize: 10, letterSpacing: '0.2em', color: tokens.color.inkMute, marginBottom: 10, fontWeight: 500 }}>WYMIARY MODELU</div>
          <div style={{ fontFamily: tokens.font.mono, fontSize: 11 }}>
            {[
              ['Parametry', '7.2 B'],
              ['Ctx window', '32 k tok'],
              ['Heads', '32 × 12'],
              ['Warstwy', '32'],
              ['d_model', '4096'],
            ].map(([k, v]) => (
              <div key={k} style={{ display: 'flex', justifyContent: 'space-between', padding: '7px 0', borderTop: `1px solid ${tokens.color.hairline}`, color: tokens.color.inkDim }}>
                <span>{k}</span><span style={{ color: tokens.color.navy, fontWeight: 500 }}>{v}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>

    <div style={{ marginTop: 20, fontFamily: tokens.font.mono, fontSize: 10, color: tokens.color.inkMute, letterSpacing: '0.08em' }}>
      ŹRÓDŁO · opracowanie własne na podstawie Vaswani et al., 2017 · arXiv:1706.03762
    </div>
  </Page>
);

const NeuralDiagram = () => {
  const layers = [
    { x: 60,  n: 5, color: tokens.color.orange,      lbl: 'INPUT' },
    { x: 210, n: 8, color: tokens.color.navyMid,     lbl: 'ATTN'  },
    { x: 360, n: 8, color: 'oklch(0.45 0.14 310)',   lbl: 'FFN'   },
    { x: 510, n: 8, color: tokens.color.navyMid,     lbl: 'ATTN'  },
    { x: 660, n: 8, color: 'oklch(0.45 0.14 310)',   lbl: 'FFN'   },
    { x: 810, n: 5, color: 'oklch(0.48 0.12 145)',   lbl: 'OUT'   },
  ];
  const H = 440, W = 900;
  const nodes = layers.map(l => {
    const step = 340 / (l.n + 1);
    return { ...l, ys: Array.from({ length: l.n }, (_, i) => 50 + step * (i + 1)) };
  });
  const lines = [];
  for (let i = 0; i < nodes.length - 1; i++) {
    const a = nodes[i], b = nodes[i + 1];
    a.ys.forEach((ay, ai) => b.ys.forEach((by, bi) => {
      const w = ((ai * 7 + bi * 11) % 10) / 10;
      lines.push({ x1: a.x, y1: ay, x2: b.x, y2: by, opacity: 0.10 + w * 0.45, stroke: w > 0.7 ? tokens.color.orange : 'rgba(20,27,45,0.35)' });
    }));
  }
  return (
    <svg viewBox={`0 0 ${W} ${H}`} style={{ width: '100%', height: 440 }}>
      {lines.map((l, i) => <line key={i} {...l} strokeWidth={0.7} />)}
      {nodes.map(l => l.ys.map((y, i) => (
        <g key={`${l.x}-${i}`}>
          <circle cx={l.x} cy={y} r={11} fill={l.color} opacity={0.18} />
          <circle cx={l.x} cy={y} r={6} fill={l.color} />
        </g>
      )))}
      {nodes.map(l => (
        <text key={l.x + 'l'} x={l.x} y={H - 16} textAnchor="middle"
          style={{ fontFamily: tokens.font.mono, fontSize: 10, fill: tokens.color.inkMute, letterSpacing: '0.18em' }}>
          {l.lbl}
        </text>
      ))}
    </svg>
  );
};

// 7. CHEAT SHEET — LIGHT
const PageCheatSheet = () => {
  const cards = [
    { n: '01', title: 'Bądź konkretny', code: 'Napisz 3 akapity o X, styl formalny, 200 słów.', hint: 'Precyzja > uprzejmość.' },
    { n: '02', title: 'Daj przykłady', code: 'Przykład: wejście → wyjście.\nTeraz zrób to samo dla: ...', hint: 'Few-shot działa.' },
    { n: '03', title: 'Nadaj rolę', code: 'Jesteś senior DevOps z 10-letnim stażem.', hint: 'Persona kadruje styl.' },
    { n: '04', title: 'Zażądaj formatu', code: 'Odpowiedz w JSON:\n{ "title": ..., "steps": [...] }', hint: 'Schemat = kontrola.' },
    { n: '05', title: 'Krok po kroku', code: 'Myśl krok po kroku. Najpierw plan, potem wykonanie.', hint: 'Chain-of-thought.' },
    { n: '06', title: 'Iteruj', code: '(popraw) Zbyt długie. Skróć do 3 zdań.', hint: 'Dialog, nie monolog.' },
  ];
  return (
    <Page label="CHEAT SHEET · 3.X" pageNum={98} variant="paperAlt">
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 300px', gap: 28, marginBottom: 28 }}>
        <div>
          <div style={{ fontFamily: tokens.font.mono, fontSize: 11, color: tokens.color.orange, letterSpacing: '0.2em', marginBottom: 8, fontWeight: 500 }}>
            CHEAT SHEET · QUICK REF
          </div>
          <h2 style={{ fontFamily: tokens.font.sans, fontSize: 52, fontWeight: 700, letterSpacing: '-0.03em', lineHeight: 0.98, margin: '0 0 12px', color: tokens.color.navy }}>
            6 zasad <span style={{ color: tokens.color.orange, fontStyle: 'italic', fontWeight: 400 }}>dobrego</span><br/>
            promptu.
          </h2>
          <p style={{ fontSize: 14, lineHeight: 1.55, color: tokens.color.inkDim, maxWidth: 560, margin: 0 }}>
            Wydrukuj, przyklej obok monitora. Każda karta zawiera szablon, przykład i jedną rzecz do zapamiętania.
          </p>
        </div>
        <Card style={{ padding: 20 }}>
          <div style={{ fontFamily: tokens.font.mono, fontSize: 10, color: tokens.color.inkMute, letterSpacing: '0.18em', marginBottom: 8 }}>LEVEL</div>
          <div style={{ display: 'flex', gap: 4, marginBottom: 18 }}>
            {[1,2,3,4,5].map(i => <div key={i} style={{ flex: 1, height: 4, background: i <= 2 ? tokens.color.orange : tokens.color.hairline2 }} />)}
          </div>
          <div style={{ fontFamily: tokens.font.mono, fontSize: 10, color: tokens.color.inkMute, letterSpacing: '0.18em', marginBottom: 8 }}>DLA KOGO</div>
          <div style={{ fontSize: 13, color: tokens.color.navy, lineHeight: 1.5 }}>Manager / Analityk / Każdy, kto pisze.</div>
        </Card>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, flex: 1 }}>
        {cards.map(c => (
          <div key={c.n} style={{
            background: tokens.color.paperElev,
            border: `1px solid ${tokens.color.hairline}`,
            borderTop: `3px solid ${tokens.color.orange}`,
            padding: '20px 20px 18px',
            display: 'flex', flexDirection: 'column',
            borderRadius: 2,
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 14 }}>
              <div style={{ fontFamily: tokens.font.mono, fontSize: 22, color: tokens.color.orange, fontWeight: 500, letterSpacing: '-0.02em' }}>{c.n}</div>
              <div style={{ width: 10, height: 10, border: `1px solid ${tokens.color.orange}`, transform: 'rotate(45deg)' }} />
            </div>
            <h4 style={{ fontSize: 20, fontWeight: 600, letterSpacing: '-0.015em', margin: '0 0 14px', lineHeight: 1.1, color: tokens.color.navy }}>{c.title}</h4>
            <div style={{
              fontFamily: tokens.font.mono, fontSize: 11, lineHeight: 1.5,
              background: tokens.color.codeBg, border: `1px solid ${tokens.color.hairline}`,
              padding: '10px 12px', borderRadius: 2, color: tokens.color.codeText,
              whiteSpace: 'pre-wrap', flex: 1, marginBottom: 12,
            }}>{c.code}</div>
            <div style={{ fontFamily: tokens.font.mono, fontSize: 9.5, color: tokens.color.orange, letterSpacing: '0.15em', textTransform: 'uppercase', fontWeight: 500 }}>
              → {c.hint}
            </div>
          </div>
        ))}
      </div>
    </Page>
  );
};

Object.assign(window, { PageStandard, PageCaseStudy, PageInfographic, PageCheatSheet, NeuralDiagram });
