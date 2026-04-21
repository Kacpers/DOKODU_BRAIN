// Page templates part 3: Code Deep-Dive (LIGHT), Data (LIGHT), Image-Led (DARK), Back (LIGHT)

// 8. CODE DEEP-DIVE — LIGHT
const PageCodeDive = () => (
  <Page label="LISTING 4.1 · KOD" pageNum={112} variant="light">
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 20 }}>
      <div style={{ fontFamily: tokens.font.mono, fontSize: 11, color: tokens.color.orange, letterSpacing: '0.2em', fontWeight: 500 }}>
        § 4.1 · LISTING 4.1 · python
      </div>
      <div style={{ fontFamily: tokens.font.mono, fontSize: 10, color: tokens.color.inkMute }}>run · python 3.11+</div>
    </div>
    <h2 style={{ fontSize: 40, fontWeight: 700, letterSpacing: '-0.025em', lineHeight: 1, margin: '0 0 24px', color: tokens.color.navy }}>
      RAG w <span style={{ color: tokens.color.orange, fontStyle: 'italic', fontWeight: 400 }}>40 liniach</span> — pełny pipeline.
    </h2>

    <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 24, flex: 1 }}>
      <div style={{
        fontFamily: tokens.font.mono, fontSize: 12, lineHeight: 1.65,
        background: tokens.color.codeBg, border: `1px solid ${tokens.color.hairline}`,
        borderLeft: `3px solid ${tokens.color.orange}`, borderRadius: 2,
        padding: '20px 22px 20px 50px', color: tokens.color.codeText,
        position: 'relative', overflow: 'hidden',
      }}>
        <div style={{
          position: 'absolute', left: 0, top: 0, bottom: 0, width: 36,
          borderRight: `1px solid ${tokens.color.hairline}`, padding: '20px 0',
          color: tokens.color.inkMute, fontSize: 10, textAlign: 'right',
        }}>
          {Array.from({ length: 24 }).map((_, i) => (
            <div key={i} style={{ lineHeight: 1.65, paddingRight: 10 }}>{i + 1}</div>
          ))}
        </div>
        <div><span style={{ color: tokens.color.codeComment }}># rag_pipeline.py — minimalny retrieval-augmented generator</span></div>
        <div><span style={{ color: tokens.color.codeKeyword }}>from</span> openai <span style={{ color: tokens.color.codeKeyword }}>import</span> OpenAI</div>
        <div><span style={{ color: tokens.color.codeKeyword }}>from</span> qdrant_client <span style={{ color: tokens.color.codeKeyword }}>import</span> QdrantClient</div>
        <div><span style={{ color: tokens.color.codeKeyword }}>from</span> pathlib <span style={{ color: tokens.color.codeKeyword }}>import</span> Path</div>
        <div>&nbsp;</div>
        <div>client = OpenAI()</div>
        <div>qdrant = QdrantClient(<span style={{ color: tokens.color.codeString }}>"localhost"</span>, port=<span style={{ color: tokens.color.codeNumber }}>6333</span>)</div>
        <div>&nbsp;</div>
        <div><span style={{ color: tokens.color.codeKeyword }}>def</span> <span style={{ color: tokens.color.codeFn }}>embed</span>{'(text: '}<span style={{ color: tokens.color.codeNumber }}>str</span>{') -> '}<span style={{ color: tokens.color.codeNumber }}>list</span>{'['}<span style={{ color: tokens.color.codeNumber }}>float</span>{']:'}</div>
        <div style={{ paddingLeft: 20 }}>{'res = client.embeddings.create('}</div>
        <div style={{ paddingLeft: 40 }}>{'model='}<span style={{ color: tokens.color.codeString }}>"text-embedding-3-small"</span>,</div>
        <div style={{ paddingLeft: 40 }}>{'input=text,'}</div>
        <div style={{ paddingLeft: 20 }}>{')'}</div>
        <div style={{ paddingLeft: 20 }}><span style={{ color: tokens.color.codeKeyword }}>return</span>{' res.data['}<span style={{ color: tokens.color.codeNumber }}>0</span>{'].embedding'}</div>
        <div>&nbsp;</div>
        <div><span style={{ color: tokens.color.codeKeyword }}>def</span> <span style={{ color: tokens.color.codeFn }}>retrieve</span>{'(query, k='}<span style={{ color: tokens.color.codeNumber }}>4</span>{'):'}</div>
        <div style={{ paddingLeft: 20 }}>{'hits = qdrant.search('}<span style={{ color: tokens.color.codeString }}>"docs"</span>{', embed(query), limit=k)'}</div>
        <div style={{ paddingLeft: 20 }}><span style={{ color: tokens.color.codeKeyword }}>return</span>{' [h.payload['}<span style={{ color: tokens.color.codeString }}>"text"</span>{'] '}<span style={{ color: tokens.color.codeKeyword }}>for</span>{' h '}<span style={{ color: tokens.color.codeKeyword }}>in</span>{' hits]'}</div>
        <div>&nbsp;</div>
        <div><span style={{ color: tokens.color.codeKeyword }}>def</span> <span style={{ color: tokens.color.codeFn }}>answer</span>{'(question):'}</div>
        <div style={{ paddingLeft: 20 }}>{'ctx = '}<span style={{ color: tokens.color.codeString }}>{'"\\n---\\n"'}</span>{'.join(retrieve(question))'}</div>
        <div style={{ paddingLeft: 20 }}>{'prompt = f'}<span style={{ color: tokens.color.codeString }}>{'"Kontekst:\\n{ctx}\\n\\nPytanie: {question}"'}</span></div>
        <div style={{ paddingLeft: 20 }}>{'resp = client.chat.completions.create('}</div>
        <div style={{ paddingLeft: 40 }}>{'model='}<span style={{ color: tokens.color.codeString }}>"gpt-4o-mini"</span>,</div>
        <div style={{ paddingLeft: 40 }}>{'messages=[{'}<span style={{ color: tokens.color.codeString }}>"role"</span>{': '}<span style={{ color: tokens.color.codeString }}>"user"</span>{', '}<span style={{ color: tokens.color.codeString }}>"content"</span>{': prompt}],'}</div>
        <div style={{ paddingLeft: 20 }}>{')'}</div>
        <div style={{ paddingLeft: 20 }}><span style={{ color: tokens.color.codeKeyword }}>return</span>{' resp.choices['}<span style={{ color: tokens.color.codeNumber }}>0</span>{'].message.content'}</div>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 18 }}>
        {[
          { line: 'L.05–06', title: 'Dwaj klienci', body: 'OpenAI do LLM i embeddingów, Qdrant jako baza wektorowa. Oba self-hosted-friendly.' },
          { line: 'L.09–13', title: 'Embedding', body: 'Zamieniamy tekst na 1536-wymiarowy wektor. Model „small" kosztuje grosze.' },
          { line: 'L.16–18', title: 'Retrieval', body: 'Top-k najbliższych sąsiadów w przestrzeni wektorowej. k=4 zwykle wystarczy.' },
          { line: 'L.20–28', title: 'Generacja', body: 'Kontekst sklejony, model widzi go przed pytaniem. To cała „magia" RAG.' },
        ].map(c => (
          <div key={c.line} style={{ borderLeft: `3px solid ${tokens.color.orange}`, paddingLeft: 14 }}>
            <div style={{ fontFamily: tokens.font.mono, fontSize: 9.5, letterSpacing: '0.2em', color: tokens.color.orange, marginBottom: 4, fontWeight: 600 }}>
              → {c.line}
            </div>
            <div style={{ fontSize: 14, fontWeight: 600, letterSpacing: '-0.01em', marginBottom: 4, color: tokens.color.navy }}>{c.title}</div>
            <div style={{ fontSize: 12, lineHeight: 1.55, color: tokens.color.inkDim }}>{c.body}</div>
          </div>
        ))}
      </div>
    </div>
  </Page>
);

// 9. DATA + CHART — LIGHT
const PageData = () => {
  const rows = [
    ['Microsoft Copilot',  '2023-03', '28%', '4.1×', '6 tyg.'],
    ['Google Gemini',      '2023-12', '19%', '3.2×', '8 tyg.'],
    ['OpenAI ChatGPT Ent', '2023-08', '34%', '5.0×', '5 tyg.'],
    ['Anthropic Claude',   '2024-03', '22%', '3.8×', '7 tyg.'],
    ['Własne (open)',      '2024-06', '12%', '2.1×', '14 tyg.'],
  ];
  const bars = [28, 19, 34, 22, 12];
  const maxBar = 40;
  return (
    <Page label="FIG. 7.3 · DANE" pageNum={224} variant="light">
      <div style={{ marginBottom: 24 }}>
        <div style={{ fontFamily: tokens.font.mono, fontSize: 11, color: tokens.color.orange, letterSpacing: '0.2em', marginBottom: 8, fontWeight: 500 }}>
          TABLE 7.3 / BENCHMARK · N=140 FIRM
        </div>
        <h2 style={{ fontFamily: tokens.font.sans, fontSize: 44, fontWeight: 700, letterSpacing: '-0.03em', margin: '0 0 12px', lineHeight: 1, color: tokens.color.navy }}>
          Adopcja narzędzi AI <span style={{ color: tokens.color.orange, fontStyle: 'italic', fontWeight: 300 }}>w liczbach.</span>
        </h2>
        <p style={{ fontSize: 13.5, lineHeight: 1.55, color: tokens.color.inkDim, maxWidth: 720, margin: 0 }}>
          Wyniki ankiety przeprowadzonej na grupie 140 polskich firm MŚP — III kw. 2025.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: 28, flex: 1 }}>
        <div>
          <div style={{ fontFamily: tokens.font.mono, fontSize: 9.5, color: tokens.color.inkMute, letterSpacing: '0.15em', marginBottom: 8 }}>TABELA 7.3</div>
          <div style={{ border: `1px solid ${tokens.color.hairline}`, borderRadius: 2, background: tokens.color.paperElev }}>
            <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr 0.8fr 0.8fr 1fr', padding: '10px 14px',
              fontFamily: tokens.font.mono, fontSize: 9.5, color: tokens.color.inkMute, letterSpacing: '0.12em', fontWeight: 500,
              background: tokens.color.paperAlt, borderBottom: `1px solid ${tokens.color.hairline2}` }}>
              <span>NARZĘDZIE</span><span>GA</span><span>ADOPCJA</span><span>ROI</span><span>WDROŻENIE</span>
            </div>
            {rows.map((r, i) => (
              <div key={i} style={{ display: 'grid', gridTemplateColumns: '2fr 1fr 0.8fr 0.8fr 1fr',
                padding: '14px 14px', borderTop: i === 0 ? 'none' : `1px solid ${tokens.color.hairline}`,
                fontSize: 13, color: tokens.color.navy, alignItems: 'center',
                background: i === 2 ? `color-mix(in oklch, ${tokens.color.orange} 8%, transparent)` : 'transparent' }}>
                <span style={{ fontWeight: 500 }}>{r[0]}</span>
                <span style={{ fontFamily: tokens.font.mono, color: tokens.color.inkDim, fontSize: 11 }}>{r[1]}</span>
                <span style={{ fontFamily: tokens.font.mono, color: tokens.color.orange, fontWeight: 600 }}>{r[2]}</span>
                <span style={{ fontFamily: tokens.font.mono, color: tokens.color.navy }}>{r[3]}</span>
                <span style={{ fontFamily: tokens.font.mono, color: tokens.color.inkDim, fontSize: 11 }}>{r[4]}</span>
              </div>
            ))}
          </div>
          <div style={{ fontFamily: tokens.font.mono, fontSize: 9.5, color: tokens.color.inkMute, letterSpacing: '0.08em', marginTop: 10 }}>
            GA = general availability · ROI po 9 mies. · n=140
          </div>
        </div>

        <div>
          <div style={{ fontFamily: tokens.font.mono, fontSize: 9.5, color: tokens.color.inkMute, letterSpacing: '0.15em', marginBottom: 8 }}>WYKRES 7.3a — ADOPCJA (%)</div>
          <Card style={{ padding: 22 }}>
            <div style={{ display: 'flex', alignItems: 'flex-end', gap: 12, height: 260, borderBottom: `1px solid ${tokens.color.hairline2}` }}>
              {bars.map((b, i) => (
                <div key={i} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6, height: '100%', justifyContent: 'flex-end' }}>
                  <div style={{ fontFamily: tokens.font.mono, fontSize: 11, color: tokens.color.navy, fontWeight: 500 }}>{b}%</div>
                  <div style={{
                    width: '100%',
                    height: `${(b / maxBar) * 100}%`,
                    background: i === 2
                      ? `linear-gradient(to top, ${tokens.color.orangeDeep}, ${tokens.color.orange})`
                      : `linear-gradient(to top, ${tokens.color.navyMid}, oklch(0.55 0.06 250))`,
                  }} />
                </div>
              ))}
            </div>
            <div style={{ display: 'flex', gap: 12, marginTop: 8 }}>
              {['MS', 'GG', 'OAI', 'ANT', 'OSS'].map((l, i) => (
                <div key={i} style={{ flex: 1, fontFamily: tokens.font.mono, fontSize: 9, color: tokens.color.inkMute, letterSpacing: '0.14em', textAlign: 'center' }}>{l}</div>
              ))}
            </div>
          </Card>
          <div style={{ marginTop: 18, fontSize: 12.5, lineHeight: 1.55, color: tokens.color.inkDim }}>
            OpenAI ChatGPT Enterprise wyprzedza stawkę dzięki łatwości integracji — ale różnica w ROI jest mniejsza, niż sugerują nagłówki.
          </div>
        </div>
      </div>
    </Page>
  );
};

// 10. IMAGE-LED — keeps DARK per user request (hero / bleed)
const PageImageLed = () => (
  <Page label="ROZDZIAŁ 06 · OTWARCIE" pageNum={178} showChrome={false} bleed variant="dark">
    <div style={{ position: 'absolute', inset: 0,
      background: 'radial-gradient(ellipse at 30% 40%, oklch(0.30 0.14 50 / 0.65), oklch(0.10 0.06 250)), ' +
                  'repeating-linear-gradient(45deg, transparent 0 14px, rgba(255,255,255,0.03) 14px 15px)' }} />
    <div style={{ position: 'absolute', inset: 0,
      background: 'linear-gradient(180deg, rgba(11,17,32,0.2) 0%, transparent 30%, transparent 55%, rgba(11,17,32,0.9) 100%)' }} />

    <div style={{ position: 'absolute', top: 48, left: 72, display: 'flex', alignItems: 'center', gap: 12 }}>
      <div style={{ width: 8, height: 8, background: tokens.color.orange }} />
      <div style={{ fontFamily: tokens.font.mono, fontSize: 11, letterSpacing: '0.25em', color: tokens.color.text, textTransform: 'uppercase' }}>
        Rozdział 06 · Etyka w AI
      </div>
    </div>

    <div style={{ position: 'absolute', left: 72, right: 72, top: 520, display: 'flex', justifyContent: 'center' }}>
      <div style={{ maxWidth: 720, textAlign: 'center' }}>
        <div style={{ fontFamily: 'Georgia, serif', fontSize: 120, color: tokens.color.orange, lineHeight: 0.5, fontStyle: 'italic', marginBottom: 10 }}>"</div>
        <p style={{
          fontFamily: tokens.font.sans, fontSize: 48, fontWeight: 300,
          fontStyle: 'italic', lineHeight: 1.15, letterSpacing: '-0.02em',
          color: tokens.color.text, margin: 0,
        }}>
          Maszyna nie jest nieetyczna.<br/>
          Jest <span style={{ color: tokens.color.orange, fontStyle: 'normal', fontWeight: 500 }}>obojętna</span> — i to <br/>jest dużo gorsze.
        </p>
        <div style={{ fontFamily: tokens.font.mono, fontSize: 11, letterSpacing: '0.2em', color: tokens.color.textDim, marginTop: 30, textTransform: 'uppercase' }}>
          — Stuart Russell, UC Berkeley
        </div>
      </div>
    </div>

    <div style={{ position: 'absolute', bottom: 48, left: 72, right: 72,
      display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' }}>
      <div style={{ maxWidth: 420 }}>
        <div style={{ fontFamily: tokens.font.mono, fontSize: 10, letterSpacing: '0.2em', color: tokens.color.orange, marginBottom: 8, textTransform: 'uppercase' }}>
          Fot. — Open placeholder
        </div>
        <p style={{ fontSize: 12.5, lineHeight: 1.55, color: tokens.color.textDim, margin: 0 }}>
          Zastąp to zdjęciem lub grafiką konceptualną obrazującą temat rozdziału. Zalecany format: 1240×1754 px, tonacja chłodna, niska saturacja.
        </p>
      </div>
      <div style={{ fontFamily: tokens.font.mono, fontSize: 10, color: tokens.color.textMute, letterSpacing: '0.12em' }}>178</div>
    </div>
  </Page>
);

// 11. BACK / CLOSING — LIGHT (switched from dark)
const PageBack = () => (
  <Page label="KOLOFON · ZAMKNIĘCIE" pageNum={284} showChrome={false} bleed variant="paperAlt">
    <div style={{ position: 'absolute', top: 72, left: 72, right: 72,
      display: 'flex', justifyContent: 'space-between' }}>
      <div style={{ fontFamily: tokens.font.mono, fontSize: 11, color: tokens.color.orange, letterSpacing: '0.2em', fontWeight: 500 }}>FIN.</div>
      <div style={{ fontFamily: tokens.font.mono, fontSize: 11, color: tokens.color.inkMute, letterSpacing: '0.2em' }}>Dokodu · Vol. 01 / 01</div>
    </div>

    <div style={{ position: 'absolute', left: 72, right: 72, top: 280 }}>
      <h2 style={{ fontFamily: tokens.font.sans, fontSize: 96, fontWeight: 700, letterSpacing: '-0.035em', lineHeight: 0.92, margin: 0, color: tokens.color.navy }}>
        To nie jest<br/>
        <span style={{ color: 'transparent', WebkitTextStroke: `1.5px ${tokens.color.navy}`, fontWeight: 200 }}>koniec.</span><br/>
        <span style={{ color: tokens.color.orange, fontStyle: 'italic', fontWeight: 400 }}>Zaczynaj.</span>
      </h2>
    </div>

    <div style={{ position: 'absolute', left: 72, right: 72, bottom: 220,
      display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 28 }}>
      <div>
        <div style={{ fontFamily: tokens.font.mono, fontSize: 10, color: tokens.color.orange, letterSpacing: '0.2em', marginBottom: 10, fontWeight: 500 }}>NASTĘPNY KROK</div>
        <div style={{ fontSize: 15, lineHeight: 1.55, color: tokens.color.navy }}>
          Umów bezpłatną 30-minutową konsultację. Bez zobowiązań, bez slajdów.
        </div>
        <div style={{ fontFamily: tokens.font.mono, fontSize: 13, color: tokens.color.orange, marginTop: 14, borderTop: `1px solid ${tokens.color.orange}`, paddingTop: 10, fontWeight: 500 }}>
          → dokodu.it/konsultacje
        </div>
      </div>
      <div>
        <div style={{ fontFamily: tokens.font.mono, fontSize: 10, color: tokens.color.orange, letterSpacing: '0.2em', marginBottom: 10, fontWeight: 500 }}>KONTYNUUJ</div>
        <div style={{ fontSize: 15, lineHeight: 1.55, color: tokens.color.navy }}>
          Kolejny tom — „Agenci AI w praktyce" — ukaże się jesienią 2026.
        </div>
        <div style={{ fontFamily: tokens.font.mono, fontSize: 13, color: tokens.color.orange, marginTop: 14, borderTop: `1px solid ${tokens.color.orange}`, paddingTop: 10, fontWeight: 500 }}>
          → dokodu.it/blog
        </div>
      </div>
      <div>
        <div style={{ fontFamily: tokens.font.mono, fontSize: 10, color: tokens.color.orange, letterSpacing: '0.2em', marginBottom: 10, fontWeight: 500 }}>KOLOFON</div>
        <div style={{ fontFamily: tokens.font.mono, fontSize: 11, color: tokens.color.inkDim, lineHeight: 1.75 }}>
          Typo · Inter + JetBrains Mono<br/>
          Papier · 120 g, matowy<br/>
          Druk · Poligrafia Gdańsk<br/>
          © 2026 Dokodu sp. z o.o.<br/>
          KRS 0000925166
        </div>
      </div>
    </div>

    <div style={{ position: 'absolute', bottom: 60, left: 72, right: 72,
      display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end',
      borderTop: `1px solid ${tokens.color.hairline}`, paddingTop: 20,
      fontFamily: tokens.font.mono, fontSize: 10, color: tokens.color.inkMute, letterSpacing: '0.12em' }}>
      <span>biuro@dokodu.it · ul. Kosynierów 76/22, 84-230 Rumia</span>
      <span>284 / 284</span>
    </div>
  </Page>
);

Object.assign(window, { PageCodeDive, PageData, PageImageLed, PageBack });
