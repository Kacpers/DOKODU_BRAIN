#!/usr/bin/env node
/**
 * Dokodu PPTX Generator
 * Generuje brandowane prezentacje PowerPoint z plików 02_Prezentacja.md
 *
 * Użycie:
 *   node generate_pptx.js                    # wszystkie moduły
 *   node generate_pptx.js Modul_01           # jeden moduł
 *
 * Output: MATERIALY_KURSU/<Modul>/Prezentacja_<Modul>.pptx
 */

const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

// ── Kolory Dokodu ─────────────────────────────────────────────
const C = {
  navy:    "0F2137",
  red:     "E63946",
  slate:   "5A6677",
  lightBg: "F8FAFC",
  white:   "FFFFFF",
  offWhite:"F0F4F8",
  darkBg:  "0A1628",
  muted:   "8096AA",
  border:  "E2E8F0",
  codeGb:  "1E2D40",
  codeFg:  "A8D8EA",
  accent2: "FF6A00",  // orange accent (jak na stronie kursu)
};

const BASE = path.join(__dirname, "../10_PROJECTS/PRJ_Kurs_n8n_Launch/MATERIALY_KURSU");

// ── Parser Markdown ───────────────────────────────────────────
function parsePresentation(mdText) {
  const slides = [];
  // Usuń frontmatter YAML
  const content = mdText.replace(/^---[\s\S]*?---\n/, "");
  // Podziel po separatorach ---
  const blocks = content.split(/\n---\n/);

  for (const block of blocks) {
    const trimmed = block.trim();
    if (!trimmed) continue;

    // Wyciągnij tytuł slajdu (## Slajd N: Tytuł lub # Tytuł)
    const titleMatch = trimmed.match(/^##\s+Slajd\s+\d+:\s+(.+)|^#\s+(.+)/m);
    if (!titleMatch) continue;

    const title = (titleMatch[1] || titleMatch[2]).trim();

    // Wyciągnij notatkę prowadzącego
    const noteMatch = trimmed.match(/>\s*🎙️\s*NOTATKA:\s*(.+)/s);
    const note = noteMatch ? noteMatch[1].trim().replace(/\n>/g, " ").trim() : "";

    // Usuń tytuł i notatkę — zostaje treść
    let bodyRaw = trimmed
      .replace(/^##\s+Slajd\s+\d+:\s+.+\n?/m, "")
      .replace(/^#\s+.+\n?/m, "")
      .replace(/>\s*🎙️\s*NOTATKA:[\s\S]*$/, "")
      .trim();

    // Wykryj typ slajdu
    const hasTable = bodyRaw.includes("|---|");
    const hasCode  = bodyRaw.includes("```");
    const hasBullets = bodyRaw.match(/^\s*[-*]\s+/m);

    // Parsuj zawartość
    const items = parseBody(bodyRaw);

    slides.push({ title, note, items, hasTable, hasCode, hasBullets, raw: bodyRaw });
  }

  return slides;
}

function parseBody(raw) {
  const lines = raw.split("\n");
  const items = [];
  let inCode = false;
  let codeLines = [];
  let inTable = false;
  let tableRows = [];

  for (const line of lines) {
    // Blok kodu
    if (line.startsWith("```")) {
      if (!inCode) {
        inCode = true;
        codeLines = [];
      } else {
        items.push({ type: "code", text: codeLines.join("\n") });
        inCode = false;
        codeLines = [];
      }
      continue;
    }
    if (inCode) { codeLines.push(line); continue; }

    // Tabela
    if (line.startsWith("|")) {
      if (!inTable) { inTable = true; tableRows = []; }
      if (!line.match(/^\|[-| :]+\|$/)) {
        const cells = line.split("|").slice(1, -1).map(c => c.trim());
        tableRows.push(cells);
      }
      continue;
    } else if (inTable) {
      items.push({ type: "table", rows: tableRows });
      inTable = false;
      tableRows = [];
    }

    // Bullet
    const bulletMatch = line.match(/^\s*([-*])\s+(.+)/);
    if (bulletMatch) {
      items.push({ type: "bullet", text: stripMd(bulletMatch[2]) });
      continue;
    }

    // Numeracja
    const numMatch = line.match(/^\s*\d+\.\s+(.+)/);
    if (numMatch) {
      items.push({ type: "numbered", text: stripMd(numMatch[1]) });
      continue;
    }

    // Nagłówek inline (bold linia)
    if (line.match(/^\*\*(.+)\*\*$/) && !line.includes(" ")) {
      items.push({ type: "heading", text: line.replace(/\*\*/g, "") });
      continue;
    }

    // Zwykły tekst
    if (line.trim()) {
      items.push({ type: "text", text: stripMd(line.trim()) });
    }
  }

  if (inTable && tableRows.length) items.push({ type: "table", rows: tableRows });
  if (inCode && codeLines.length) items.push({ type: "code", text: codeLines.join("\n") });

  return items;
}

function stripMd(text) {
  return text
    .replace(/\*\*(.+?)\*\*/g, "$1")
    .replace(/\*(.+?)\*/g, "$1")
    .replace(/`(.+?)`/g, "$1")
    .replace(/\[(.+?)\]\(.+?\)/g, "$1");
}

// ── Helpery slajdów ───────────────────────────────────────────
function makeShadow() {
  return { type: "outer", color: "000000", blur: 8, offset: 2, angle: 135, opacity: 0.12 };
}

function addTitleBand(slide, title, pres) {
  // Granatowy pasek górny
  slide.addShape(pres.ShapeType.rect, {
    x: 0, y: 0, w: 10, h: 0.75,
    fill: { color: C.navy }, line: { color: C.navy }
  });
  // Czerwona kreska akcentująca
  slide.addShape(pres.ShapeType.rect, {
    x: 0, y: 0.75, w: 10, h: 0.06,
    fill: { color: C.red }, line: { color: C.red }
  });
  // Tytuł slajdu
  slide.addText(title, {
    x: 0.4, y: 0.09, w: 8.5, h: 0.57,
    fontSize: 22, bold: true, color: C.white,
    fontFace: "Calibri", align: "left", valign: "middle", margin: 0
  });
  // Logo Dokodu
  slide.addText("dokodu", {
    x: 8.5, y: 0.09, w: 1.1, h: 0.57,
    fontSize: 13, bold: true, color: C.muted,
    fontFace: "Calibri", align: "right", valign: "middle", margin: 0
  });
}

function addSpeakerNote(slide, note) {
  if (note) slide.addNotes(note.replace(/"/g, "'"));
}

// ── Typy slajdów ──────────────────────────────────────────────
function buildTitleSlide(pres, title, subtitle, moduleLabel) {
  const slide = pres.addSlide();
  slide.background = { color: C.darkBg };

  // Pionowa kreska czerwona po lewej
  slide.addShape(pres.ShapeType.rect, {
    x: 0.5, y: 1.2, w: 0.08, h: 3.2,
    fill: { color: C.red }, line: { color: C.red }
  });

  // Label modułu
  if (moduleLabel) {
    slide.addText(moduleLabel.toUpperCase(), {
      x: 0.75, y: 1.2, w: 8, h: 0.4,
      fontSize: 11, bold: false, color: C.muted,
      fontFace: "Calibri", align: "left", charSpacing: 4
    });
  }

  // Tytuł główny
  slide.addText(title, {
    x: 0.75, y: 1.7, w: 8.5, h: 1.5,
    fontSize: 36, bold: true, color: C.white,
    fontFace: "Calibri", align: "left", valign: "top"
  });

  // Podtytuł
  if (subtitle) {
    slide.addText(subtitle, {
      x: 0.75, y: 3.3, w: 8, h: 0.6,
      fontSize: 16, bold: false, color: C.muted,
      fontFace: "Calibri", align: "left"
    });
  }

  // Logo
  slide.addText("dokodu.it", {
    x: 0.75, y: 4.6, w: 3, h: 0.4,
    fontSize: 12, bold: false, color: C.red,
    fontFace: "Calibri", align: "left"
  });

  return slide;
}

function buildBulletSlide(pres, slideData) {
  const slide = pres.addSlide();
  slide.background = { color: C.white };
  addTitleBand(slide, slideData.title, pres);

  const bullets = slideData.items.filter(i => i.type === "bullet" || i.type === "numbered" || i.type === "text");
  const headings = slideData.items.filter(i => i.type === "heading");

  let yPos = 0.95;

  // Sekcje z headingami
  if (headings.length > 0) {
    const groups = groupByHeadings(slideData.items);
    for (const group of groups) {
      if (group.heading) {
        slide.addShape(pres.ShapeType.rect, {
          x: 0.4, y: yPos, w: 9.2, h: 0.35,
          fill: { color: C.offWhite }, line: { color: C.border }
        });
        slide.addText(group.heading, {
          x: 0.55, y: yPos, w: 9, h: 0.35,
          fontSize: 13, bold: true, color: C.navy,
          fontFace: "Calibri", align: "left", valign: "middle", margin: 0
        });
        yPos += 0.42;
      }

      const bulletItems = group.items.map(i => ({
        text: i.text,
        options: { bullet: true, color: C.slate, fontSize: 13, fontFace: "Calibri", breakLine: true }
      }));
      if (bulletItems.length > 0 && bulletItems[bulletItems.length - 1]) {
        bulletItems[bulletItems.length - 1].options.breakLine = false;
      }
      if (bulletItems.length > 0) {
        slide.addText(bulletItems, {
          x: 0.5, y: yPos, w: 9, h: Math.min(bulletItems.length * 0.42, 4.0),
          fontFace: "Calibri", fontSize: 13, color: C.slate
        });
        yPos += bulletItems.length * 0.42 + 0.15;
      }
    }
  } else if (bullets.length > 0) {
    // Prosty layout bulletów
    const bulletItems = bullets.map((i, idx) => ({
      text: i.text,
      options: {
        bullet: (i.type === "bullet"),
        color: C.slate, fontSize: 14, fontFace: "Calibri",
        breakLine: idx < bullets.length - 1
      }
    }));
    slide.addText(bulletItems, {
      x: 0.5, y: 0.95, w: 9, h: 4.4,
      fontFace: "Calibri", fontSize: 14, color: C.slate, valign: "top"
    });
  } else {
    // Zwykły tekst
    const textItems = slideData.items.filter(i => i.type === "text");
    if (textItems.length > 0) {
      slide.addText(textItems.map((i, idx) => ({
        text: i.text,
        options: { breakLine: idx < textItems.length - 1, color: C.slate, fontSize: 14 }
      })), { x: 0.5, y: 0.95, w: 9, h: 4.4, fontFace: "Calibri", valign: "top" });
    }
  }

  addSpeakerNote(slide, slideData.note);
  return slide;
}

function buildTableSlide(pres, slideData) {
  const slide = pres.addSlide();
  slide.background = { color: C.white };
  addTitleBand(slide, slideData.title, pres);

  const tableItem = slideData.items.find(i => i.type === "table");
  if (tableItem && tableItem.rows.length > 0) {
    const rows = tableItem.rows;
    const colCount = rows[0].length;
    const colW = Array(colCount).fill(9.0 / colCount);

    const tableData = rows.map((row, ri) =>
      row.map(cell => ({
        text: stripMd(cell),
        options: {
          bold: ri === 0,
          color: ri === 0 ? C.white : C.slate,
          fill: { color: ri === 0 ? C.navy : (ri % 2 === 0 ? C.offWhite : C.white) },
          fontSize: 12,
          fontFace: "Calibri",
          align: "left",
          valign: "middle"
        }
      }))
    );

    slide.addTable(tableData, {
      x: 0.5, y: 0.95, w: 9.0,
      colW,
      border: { pt: 1, color: C.border },
      rowH: 0.42
    });
  }

  // Tekst poza tabelą
  const textItems = slideData.items.filter(i => i.type !== "table");
  if (textItems.length > 0) {
    const bullets = textItems.filter(i => i.type === "bullet").map((i, idx, arr) => ({
      text: i.text,
      options: { bullet: true, color: C.slate, fontSize: 12, breakLine: idx < arr.length - 1 }
    }));
    if (bullets.length > 0) {
      const tableH = (tableItem?.rows?.length || 3) * 0.42 + 0.2;
      slide.addText(bullets, {
        x: 0.5, y: 0.95 + tableH + 0.1, w: 9, h: 1.5,
        fontFace: "Calibri", fontSize: 12
      });
    }
  }

  addSpeakerNote(slide, slideData.note);
  return slide;
}

function buildCodeSlide(pres, slideData) {
  const slide = pres.addSlide();
  slide.background = { color: C.white };
  addTitleBand(slide, slideData.title, pres);

  const codeItem = slideData.items.find(i => i.type === "code");
  const textItems = slideData.items.filter(i => i.type === "text" || i.type === "bullet");

  // Tekst przed kodem
  if (textItems.length > 0) {
    const textRuns = textItems.map((i, idx, arr) => ({
      text: i.text,
      options: { color: C.slate, fontSize: 13, breakLine: idx < arr.length - 1 }
    }));
    slide.addText(textRuns, {
      x: 0.5, y: 0.92, w: 9, h: 0.5,
      fontFace: "Calibri", fontSize: 13
    });
  }

  // Blok kodu
  if (codeItem) {
    const codeY = textItems.length > 0 ? 1.5 : 0.92;
    const codeH = Math.min(3.6, 5.2 - codeY);

    // Tło kodu
    slide.addShape(pres.ShapeType.rect, {
      x: 0.4, y: codeY, w: 9.2, h: codeH,
      fill: { color: C.codeGb }, line: { color: C.navy }
    });

    // Treść kodu
    const codeText = codeItem.text;
    slide.addText(codeText, {
      x: 0.55, y: codeY + 0.1, w: 8.9, h: codeH - 0.2,
      fontSize: 10, fontFace: "Consolas", color: C.codeFg,
      align: "left", valign: "top"
    });
  }

  addSpeakerNote(slide, slideData.note);
  return slide;
}

function groupByHeadings(items) {
  const groups = [];
  let current = { heading: null, items: [] };
  for (const item of items) {
    if (item.type === "heading") {
      if (current.items.length > 0 || current.heading) groups.push(current);
      current = { heading: item.text, items: [] };
    } else {
      current.items.push(item);
    }
  }
  if (current.items.length > 0 || current.heading) groups.push(current);
  return groups;
}

function buildEndSlide(pres, moduleTitle) {
  const slide = pres.addSlide();
  slide.background = { color: C.darkBg };

  slide.addShape(pres.ShapeType.rect, {
    x: 0, y: 2.1, w: 10, h: 0.06,
    fill: { color: C.red }, line: { color: C.red }
  });

  slide.addText("Pytania?", {
    x: 1, y: 1.0, w: 8, h: 1.0,
    fontSize: 42, bold: true, color: C.white,
    fontFace: "Calibri", align: "center"
  });

  slide.addText(moduleTitle, {
    x: 1, y: 2.3, w: 8, h: 0.6,
    fontSize: 16, color: C.muted, fontFace: "Calibri", align: "center"
  });

  slide.addText("kacper@dokodu.it  ·  dokodu.it", {
    x: 1, y: 3.2, w: 8, h: 0.5,
    fontSize: 14, color: C.red, fontFace: "Calibri", align: "center"
  });

  slide.addText("© Dokodu 2026 — materiały objęte prawami autorskimi", {
    x: 1, y: 4.8, w: 8, h: 0.4,
    fontSize: 9, color: C.muted, fontFace: "Calibri", align: "center"
  });
}

// ── Generator główny ──────────────────────────────────────────
function generateForModule(modulePath, moduleName) {
  const mdPath = path.join(modulePath, "02_Prezentacja.md");
  if (!fs.existsSync(mdPath)) {
    console.log(`  ⚠️  Brak 02_Prezentacja.md w ${moduleName}`);
    return;
  }

  const mdText = fs.readFileSync(mdPath, "utf-8");
  const slides = parsePresentation(mdText);

  if (slides.length === 0) {
    console.log(`  ⚠️  Brak slajdów w ${moduleName}`);
    return;
  }

  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  pres.author = "Kacper Sieradzinski | Dokodu";
  pres.title = `Kurs n8n + AI — ${moduleName}`;

  // Slajd tytułowy z pierwszego slajdu
  const firstSlide = slides[0];
  const subtitle = slides[1]?.title || "";
  buildTitleSlide(pres, firstSlide.title, subtitle ? `Następnie: ${subtitle}` : "Kacper Sieradziński | Dokodu", moduleName.replace(/_/g, " "));

  // Pozostałe slajdy
  for (let i = 1; i < slides.length; i++) {
    const s = slides[i];
    if (s.hasTable) {
      buildTableSlide(pres, s);
    } else if (s.hasCode) {
      buildCodeSlide(pres, s);
    } else {
      buildBulletSlide(pres, s);
    }
  }

  // Slajd końcowy
  buildEndSlide(pres, moduleName.replace(/_/g, " "));

  const outFile = path.join(modulePath, `Prezentacja_${moduleName}.pptx`);
  pres.writeFile({ fileName: outFile }).then(() => {
    console.log(`  ✅ ${moduleName} → ${path.basename(outFile)} (${slides.length} slajdów)`);
  }).catch(err => {
    console.error(`  ❌ Błąd ${moduleName}: ${err.message}`);
  });
}

// ── Entry point ───────────────────────────────────────────────
const filter = process.argv[2];
const modules = fs.readdirSync(BASE)
  .filter(d => d.startsWith("Modul_") && fs.statSync(path.join(BASE, d)).isDirectory())
  .filter(d => !filter || d.includes(filter))
  .sort();

console.log(`\n🎨 Dokodu PPTX Generator`);
console.log(`📁 Base: ${BASE}`);
console.log(`🗂️  Modułów do przetworzenia: ${modules.length}\n`);

for (const mod of modules) {
  generateForModule(path.join(BASE, mod), mod);
}
