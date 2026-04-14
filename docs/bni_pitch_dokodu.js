const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const path = require("path");
const fs = require("fs");
const {
  FaShieldAlt, FaUmbrella,
  FaGraduationCap, FaBolt, FaLaptopCode,
  FaIndustry, FaCheckCircle, FaHandshake,
  FaPhone, FaEnvelope, FaGlobe, FaUserTie,
  FaClock, FaMoneyBillWave, FaRobot,
  FaChartLine, FaBalanceScale, FaUsers
} = require("react-icons/fa");

// --- Icon helper ---
function renderIconSvg(IconComponent, color = "#000000", size = 256) {
  return ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color, size: String(size) })
  );
}
async function iconToBase64Png(IconComponent, color, size = 256) {
  const svg = renderIconSvg(IconComponent, color, size);
  const pngBuffer = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + pngBuffer.toString("base64");
}

// --- Logo ---
const logoWhiteBase64 = "image/png;base64," + fs.readFileSync(
  path.join(__dirname, "../10_PROJECTS/PRJ_Kurs_n8n_Launch/SLIDEV/Modul_01_Fundamenty/public/dokodu_logo.png")
).toString("base64");

// We need a dark logo for light slides — invert the white one
let logoDarkBase64;

async function prepareDarkLogo() {
  const logoBuffer = fs.readFileSync(
    path.join(__dirname, "../10_PROJECTS/PRJ_Kurs_n8n_Launch/SLIDEV/Modul_01_Fundamenty/public/dokodu_logo.png")
  );
  // Negate (invert) colors while preserving alpha
  const darkBuffer = await sharp(logoBuffer).negate({ alpha: false }).png().toBuffer();
  logoDarkBase64 = "image/png;base64," + darkBuffer.toString("base64");
}

// --- DOKODU BRAND COLORS ---
const C = {
  navy:       "0F2137",
  midNavy:    "162D4A",
  blue:       "0056D2",
  lightBlue:  "EBF2FF",   // very light blue for cards on white
  blueBg:     "F0F5FF",   // blue-tinted background
  red:        "FF3D3D",
  white:      "FFFFFF",
  offWhite:   "F8FAFC",
  lightGray:  "E2E8F0",
  gray:       "94A3B8",
  darkGray:   "5A6677",
  textDark:   "1E293B",
  green:      "10B981",
  teal:       "0891B2",
  amber:      "D97706",
  graphite:   "1E293B",
};

const FONT = "Poppins";
const makeCardShadow = () => ({ type: "outer", blur: 6, offset: 2, angle: 135, color: "000000", opacity: 0.1 });

// --- Logo on light slides (navy header strip) ---
function addLogoBar(slide) {
  slide.addShape(slide._slideLayout ? undefined : pres_ref.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.5, fill: { color: C.navy }
  });
  slide.addImage({ data: logoWhiteBase64, x: 0.4, y: 0.13, w: 1.0, h: 0.16 });
}

let pres_ref; // reference for shapes

async function buildPresentation() {
  const pres = new pptxgen();
  pres_ref = pres;
  pres.layout = "LAYOUT_16x9";
  pres.author = "Dokodu sp. z o.o.";
  pres.title = "Dokodu — AI ma pracować na Twój biznes. Bezpiecznie.";

  await prepareDarkLogo();

  // ============================================================
  // SLIDE 1: TITLE (Hook) — DARK
  // ============================================================
  {
    const slide = pres.addSlide();
    slide.background = { color: C.navy };

    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.blue }
    });

    // Logo centered
    slide.addImage({
      data: logoWhiteBase64,
      x: 3.5, y: 0.5, w: 3.0, h: 0.49
    });

    slide.addText([
      { text: "AI ma pracować na Twój biznes.", options: { bold: true, color: C.white, fontSize: 40, breakLine: true } },
      { text: "Bezpiecznie.", options: { bold: true, color: C.blue, fontSize: 40 } }
    ], { x: 0.8, y: 1.5, w: 8.4, h: 1.8, fontFace: FONT, margin: 0 });

    slide.addText("Transformacja Cyfrowa pod Parasolem Prawa", {
      x: 0.8, y: 3.3, w: 8.4, h: 0.5,
      fontSize: 18, fontFace: FONT, color: C.gray, margin: 0
    });

    slide.addText("Tech + Legal pod jednym dachem", {
      x: 0.8, y: 3.75, w: 8.4, h: 0.4,
      fontSize: 14, fontFace: FONT, color: C.blue, bold: true, margin: 0
    });

    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.8, y: 4.35, w: 3.5, h: 0.03, fill: { color: C.blue, transparency: 50 }
    });

    const userIcon = await iconToBase64Png(FaUserTie, "#0056D2", 256);
    slide.addImage({ data: userIcon, x: 0.8, y: 4.55, w: 0.3, h: 0.3 });
    slide.addText([
      { text: "Alina Sieradzińska", options: { bold: true, color: C.white, fontSize: 14, breakLine: true } },
      { text: "COO & Legal · Dokodu sp. z o.o.", options: { color: C.gray, fontSize: 11 } }
    ], { x: 1.2, y: 4.5, w: 5, h: 0.65, fontFace: FONT, margin: 0 });

    const shieldIcon = await iconToBase64Png(FaShieldAlt, "#0056D2", 256);
    slide.addImage({ data: shieldIcon, x: 8.0, y: 4.0, w: 1.2, h: 1.2, transparency: 80 });
  }

  // ============================================================
  // SLIDE 2: 3 PROBLEMS — LIGHT
  // ============================================================
  {
    const slide = pres.addSlide();
    slide.background = { color: C.offWhite };

    // Navy header bar with logo
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 0.5, fill: { color: C.navy }
    });
    slide.addImage({ data: logoWhiteBase64, x: 0.4, y: 0.13, w: 1.0, h: 0.16 });

    slide.addText([
      { text: "Brzmi znajomo? ", options: { bold: true, color: C.textDark, fontSize: 30 } },
      { text: "Boisz się wdrażać AI?", options: { bold: true, color: C.red, fontSize: 30 } }
    ], { x: 0.8, y: 0.65, w: 8.4, h: 0.6, fontFace: FONT, margin: 0 });

    const problems = [
      {
        icon: FaClock, label: "MARNOTRAWSTWO",
        title: "40h miesięcznie w błoto",
        desc: "Twój zespół ręcznie parsuje e-maile, kopiuje dane między systemami i robi follow-upy, które mógłby robić automat."
      },
      {
        icon: FaBalanceScale, label: "PARALIŻ PRAWNY",
        title: "AI Act i RODO straszą zarząd",
        desc: "Kary do 35 mln EUR paraliżują decyzje. Zarząd wstrzymuje wdrożenia, bo nikt nie wie co jest zgodne z prawem."
      },
      {
        icon: FaRobot, label: "ZMARNOWANA ADOPCJA",
        title: "Copilot/Gemini = \"drogi Google\"",
        desc: "Kupiliście licencje, ale ludzie boją się halucynacji i wycieku danych. Brak strategii = brak efektów."
      }
    ];

    const cardW = 2.7, cardH = 3.2, gap = 0.3, startX = 0.8, cardY = 1.5;

    for (let i = 0; i < problems.length; i++) {
      const p = problems[i];
      const x = startX + i * (cardW + gap);

      slide.addShape(pres.shapes.RECTANGLE, {
        x, y: cardY, w: cardW, h: cardH,
        fill: { color: C.white }, shadow: makeCardShadow()
      });

      // Red top accent
      slide.addShape(pres.shapes.RECTANGLE, {
        x, y: cardY, w: cardW, h: 0.05, fill: { color: C.red }
      });

      slide.addText(p.label, {
        x: x + 0.25, y: cardY + 0.2, w: cardW - 0.5, h: 0.3,
        fontSize: 9, fontFace: FONT, color: C.red,
        bold: true, charSpacing: 2, margin: 0
      });

      const iconData = await iconToBase64Png(p.icon, "#FF3D3D", 256);
      slide.addImage({ data: iconData, x: x + 0.25, y: cardY + 0.6, w: 0.4, h: 0.4 });

      slide.addText(p.title, {
        x: x + 0.25, y: cardY + 1.15, w: cardW - 0.5, h: 0.55,
        fontSize: 14, fontFace: FONT, color: C.textDark,
        bold: true, margin: 0
      });

      slide.addText(p.desc, {
        x: x + 0.25, y: cardY + 1.7, w: cardW - 0.5, h: 1.3,
        fontSize: 10.5, fontFace: FONT, color: C.darkGray,
        lineSpacingMultiple: 1.35, margin: 0
      });
    }
  }

  // ============================================================
  // SLIDE 3: USP — Tech + Legal — LIGHT
  // ============================================================
  {
    const slide = pres.addSlide();
    slide.background = { color: C.offWhite };

    // Navy header
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 0.5, fill: { color: C.navy }
    });
    slide.addImage({ data: logoWhiteBase64, x: 0.4, y: 0.13, w: 1.0, h: 0.16 });

    // Blue umbrella bar
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.8, y: 0.7, w: 8.4, h: 0.8, fill: { color: C.blue }
    });

    const umbrellaIcon = await iconToBase64Png(FaUmbrella, "#FFFFFF", 256);
    slide.addImage({ data: umbrellaIcon, x: 1.1, y: 0.82, w: 0.4, h: 0.4 });

    slide.addText("Jedyny na rynku duet: Architekt IT + Ekspert Prawny", {
      x: 1.65, y: 0.7, w: 7.2, h: 0.8,
      fontSize: 18, fontFace: FONT, color: C.white,
      bold: true, valign: "middle", margin: 0
    });

    const bullets = [
      { icon: FaUsers, text: "Dokodu to duet CEO/Tech (Kacper) i COO/Legal (Alina) pracujący ramię w ramię." },
      { icon: FaCheckCircle, text: "Wdrażamy tylko takie rozwiązania, pod którymi sami byśmy się podpisali — technicznie i prawnie." },
      { icon: FaShieldAlt, text: "Każde szkolenie, automatyzacja i system dedykowany przechodzi audyt na zgodność z RODO i AI Act od pierwszego dnia." }
    ];

    const bulletStartY = 1.8;
    for (let i = 0; i < bullets.length; i++) {
      const b = bullets[i];
      const y = bulletStartY + i * 1.0;

      slide.addShape(pres.shapes.RECTANGLE, {
        x: 0.8, y, w: 8.4, h: 0.85,
        fill: { color: C.white }, shadow: makeCardShadow()
      });

      slide.addShape(pres.shapes.RECTANGLE, {
        x: 0.8, y, w: 0.06, h: 0.85, fill: { color: C.blue }
      });

      const iconData = await iconToBase64Png(b.icon, "#0056D2", 256);
      slide.addImage({ data: iconData, x: 1.15, y: y + 0.22, w: 0.35, h: 0.35 });

      slide.addText(b.text, {
        x: 1.7, y, w: 7.2, h: 0.85,
        fontSize: 13, fontFace: FONT, color: C.textDark,
        valign: "middle", lineSpacingMultiple: 1.3, margin: 0
      });
    }

    // Bottom badge
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 2.5, y: 4.9, w: 5, h: 0.45, fill: { color: C.blue }
    });
    slide.addText("GWARANCJA COMPLIANCE OD PIERWSZEGO DNIA", {
      x: 2.5, y: 4.9, w: 5, h: 0.45,
      fontSize: 12, fontFace: FONT, color: C.white,
      bold: true, align: "center", valign: "middle", charSpacing: 2, margin: 0
    });
  }

  // ============================================================
  // SLIDE 4: ZŁOTY TRÓJKĄT — LIGHT
  // ============================================================
  {
    const slide = pres.addSlide();
    slide.background = { color: C.offWhite };

    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 0.5, fill: { color: C.navy }
    });
    slide.addImage({ data: logoWhiteBase64, x: 0.4, y: 0.13, w: 1.0, h: 0.16 });

    slide.addText("Złoty Trójkąt Transformacji", {
      x: 0.8, y: 0.65, w: 8.4, h: 0.55,
      fontSize: 28, fontFace: FONT, color: C.textDark, bold: true, margin: 0
    });

    const pillars = [
      {
        icon: FaGraduationCap, color: C.blue,
        title: "Szkolenia AI\n& Edukacja",
        desc: "Zmieniamy \"drogi Google\" w realne narzędzie pracy biurowej. Copilot, Gemini, warsztaty praktyczne.",
        result: "Zyskaj przewagę operacyjną"
      },
      {
        icon: FaBolt, color: C.teal,
        title: "Automatyzacja\nProcesów n8n",
        desc: "Silniki integracji CRM, e-mail, ERP działające 24/7. Koniec ręcznych raportów i kopiowania danych.",
        result: "Odzyskaj 40h miesięcznie"
      },
      {
        icon: FaLaptopCode, color: C.amber,
        title: "Systemy\nDedykowane",
        desc: "Customowe aplikacje na Twoim serwerze. Pełna skalowalność, własność kodu, zero abonamentu.",
        result: "100% Twoja własność"
      }
    ];

    const colW = 2.7, colH = 3.4, colGap = 0.3, colStartX = 0.8, colY = 1.4;

    for (let i = 0; i < pillars.length; i++) {
      const p = pillars[i];
      const x = colStartX + i * (colW + colGap);

      slide.addShape(pres.shapes.RECTANGLE, {
        x, y: colY, w: colW, h: colH,
        fill: { color: C.white }, shadow: makeCardShadow()
      });

      slide.addShape(pres.shapes.RECTANGLE, {
        x, y: colY, w: colW, h: 0.06, fill: { color: p.color }
      });

      slide.addShape(pres.shapes.OVAL, {
        x: x + 0.25, y: colY + 0.25, w: 0.55, h: 0.55, fill: { color: p.color }
      });
      const iconData = await iconToBase64Png(p.icon, "#FFFFFF", 256);
      slide.addImage({ data: iconData, x: x + 0.35, y: colY + 0.35, w: 0.35, h: 0.35 });

      slide.addText(p.title, {
        x: x + 0.25, y: colY + 0.95, w: colW - 0.5, h: 0.65,
        fontSize: 15, fontFace: FONT, color: C.textDark,
        bold: true, lineSpacingMultiple: 1.1, margin: 0
      });

      slide.addText(p.desc, {
        x: x + 0.25, y: colY + 1.6, w: colW - 0.5, h: 0.95,
        fontSize: 10.5, fontFace: FONT, color: C.darkGray,
        lineSpacingMultiple: 1.35, margin: 0
      });

      slide.addShape(pres.shapes.RECTANGLE, {
        x: x + 0.25, y: colY + 2.75, w: colW - 0.5, h: 0.4,
        fill: { color: p.color }
      });
      slide.addText(p.result, {
        x: x + 0.25, y: colY + 2.75, w: colW - 0.5, h: 0.4,
        fontSize: 10, fontFace: FONT, color: C.white,
        bold: true, align: "center", valign: "middle", margin: 0
      });
    }

    const shieldSmall = await iconToBase64Png(FaShieldAlt, "#0056D2", 256);
    slide.addImage({ data: shieldSmall, x: 0.8, y: 5.1, w: 0.2, h: 0.2 });
    slide.addText("Każdy filar objęty Parasolem Prawnym: RODO + AI Act", {
      x: 1.1, y: 5.05, w: 6, h: 0.3,
      fontSize: 11, fontFace: FONT, color: C.blue, bold: true, margin: 0
    });
  }

  // ============================================================
  // SLIDE 5: ANIMEX — LIGHT
  // ============================================================
  {
    const slide = pres.addSlide();
    slide.background = { color: C.offWhite };

    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 0.5, fill: { color: C.navy }
    });
    slide.addImage({ data: logoWhiteBase64, x: 0.4, y: 0.13, w: 1.0, h: 0.16 });

    // Case study badge
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.8, y: 0.7, w: 2.0, h: 0.35, fill: { color: C.blue }
    });
    slide.addText("CASE STUDY", {
      x: 0.8, y: 0.7, w: 2.0, h: 0.35,
      fontSize: 10, fontFace: FONT, color: C.white,
      bold: true, align: "center", valign: "middle", charSpacing: 3, margin: 0
    });

    slide.addText([
      { text: "Przeszkoliliśmy zespół ", options: { color: C.textDark, fontSize: 28, bold: true } },
      { text: "ANIMEX", options: { color: C.blue, fontSize: 28, bold: true } },
      { text: " z n8n.", options: { color: C.textDark, fontSize: 28, bold: true } }
    ], { x: 0.8, y: 1.2, w: 8.4, h: 0.7, fontFace: FONT, margin: 0 });

    slide.addText("Szkolenie AI Fundamenty dla Enterprise", {
      x: 0.8, y: 1.9, w: 8.4, h: 0.35,
      fontSize: 13, fontFace: FONT, color: C.darkGray, margin: 0
    });

    const points = [
      { icon: FaIndustry, text: "Największy producent mięsa w Polsce (Enterprise) wybrał Dokodu do wdrożenia kultury n8n." },
      { icon: FaBolt, text: "Przekształciliśmy ręczne, czasochłonne raporty w zautomatyzowane, bezpieczne workflowy." },
      { icon: FaChartLine, text: "Zespół biurowy zyskał realne narzędzie do oszczędzania setek godzin rocznie." }
    ];

    const pointStartY = 2.5;
    for (let i = 0; i < points.length; i++) {
      const p = points[i];
      const y = pointStartY + i * 0.85;

      slide.addShape(pres.shapes.RECTANGLE, {
        x: 0.8, y, w: 8.4, h: 0.7,
        fill: { color: C.white }, shadow: makeCardShadow()
      });

      slide.addShape(pres.shapes.RECTANGLE, {
        x: 0.8, y, w: 0.06, h: 0.7, fill: { color: C.blue }
      });

      const iconData = await iconToBase64Png(p.icon, "#0056D2", 256);
      slide.addImage({ data: iconData, x: 1.15, y: y + 0.17, w: 0.32, h: 0.32 });

      slide.addText(p.text, {
        x: 1.65, y, w: 7.3, h: 0.7,
        fontSize: 12.5, fontFace: FONT, color: C.textDark,
        valign: "middle", lineSpacingMultiple: 1.3, margin: 0
      });
    }

    // Bottom impact
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.8, y: 4.9, w: 8.4, h: 0.45, fill: { color: C.lightBlue }
    });
    slide.addText("Moc Dokodu w pigułce: Technologia + Prawo + Realne Efekty", {
      x: 0.8, y: 4.9, w: 8.4, h: 0.45,
      fontSize: 12, fontFace: FONT, color: C.blue,
      bold: true, align: "center", valign: "middle", margin: 0
    });
  }

  // ============================================================
  // SLIDE 6: SOCIAL PROOF — LIGHT
  // ============================================================
  {
    const slide = pres.addSlide();
    slide.background = { color: C.offWhite };

    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 0.5, fill: { color: C.navy }
    });
    slide.addImage({ data: logoWhiteBase64, x: 0.4, y: 0.13, w: 1.0, h: 0.16 });

    slide.addText("Oszczędzamy czas i pieniądze naszych klientów", {
      x: 0.8, y: 0.65, w: 8.4, h: 0.55,
      fontSize: 22, fontFace: FONT, color: C.textDark, bold: true, margin: 0
    });

    // Stats
    const stats = [
      { num: "140+", label: "firm nam\nzaufało", color: C.blue },
      { num: "40h", label: "miesięcznie\nodzyskanego czasu", color: C.teal },
      { num: "80%", label: "procesów\nzautomatyzowanych", color: C.green }
    ];

    const statW = 2.7, statGap = 0.3, statStartX = 0.8, statY = 1.4;

    for (let i = 0; i < stats.length; i++) {
      const s = stats[i];
      const x = statStartX + i * (statW + statGap);

      slide.addShape(pres.shapes.RECTANGLE, {
        x, y: statY, w: statW, h: 1.15,
        fill: { color: C.white }, shadow: makeCardShadow()
      });

      slide.addText(s.num, {
        x, y: statY + 0.05, w: statW, h: 0.65,
        fontSize: 40, fontFace: FONT, color: s.color,
        bold: true, align: "center", margin: 0
      });

      slide.addText(s.label, {
        x, y: statY + 0.65, w: statW, h: 0.45,
        fontSize: 10, fontFace: FONT, color: C.darkGray,
        align: "center", lineSpacingMultiple: 1.2, margin: 0
      });
    }

    // Divider
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.8, y: 2.8, w: 8.4, h: 0.01, fill: { color: C.lightGray }
    });

    slide.addText("Co mówią klienci:", {
      x: 0.8, y: 2.95, w: 8.4, h: 0.35,
      fontSize: 13, fontFace: FONT, color: C.textDark, bold: true, margin: 0
    });

    const quotes = [
      { text: "~4 500 zł miesięcznie oszczędności na samej obsłudze faktur.", source: "CEO, Software House", icon: FaMoneyBillWave },
      { text: "4 godziny tygodniowo odzyskane dla PM-ów. Zero błędów.", source: "Dyrektor operacyjna, E-commerce", icon: FaClock },
      { text: "~50 godzin oszczędności miesięcznie na tworzeniu raportów.", source: "Prezes, Firma konsultingowa", icon: FaChartLine }
    ];

    const qW = 2.7, qGap = 0.3, qStartX = 0.8, qY = 3.4;

    for (let i = 0; i < quotes.length; i++) {
      const q = quotes[i];
      const x = qStartX + i * (qW + qGap);

      slide.addShape(pres.shapes.RECTANGLE, {
        x, y: qY, w: qW, h: 1.7,
        fill: { color: C.white }, shadow: makeCardShadow()
      });

      slide.addShape(pres.shapes.RECTANGLE, {
        x, y: qY, w: 0.05, h: 1.7, fill: { color: C.blue }
      });

      const iconData = await iconToBase64Png(q.icon, "#0056D2", 256);
      slide.addImage({ data: iconData, x: x + 0.2, y: qY + 0.2, w: 0.28, h: 0.28 });

      slide.addText("\"" + q.text + "\"", {
        x: x + 0.2, y: qY + 0.55, w: qW - 0.4, h: 0.8,
        fontSize: 10.5, fontFace: FONT, color: C.textDark,
        italic: true, lineSpacingMultiple: 1.3, margin: 0
      });

      slide.addText("— " + q.source, {
        x: x + 0.2, y: qY + 1.35, w: qW - 0.4, h: 0.25,
        fontSize: 9, fontFace: FONT, color: C.darkGray, margin: 0
      });
    }
  }

  // ============================================================
  // SLIDE 7: KOGO POLECAĆ — LIGHT
  // ============================================================
  {
    const slide = pres.addSlide();
    slide.background = { color: C.offWhite };

    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 0.5, fill: { color: C.navy }
    });
    slide.addImage({ data: logoWhiteBase64, x: 0.4, y: 0.13, w: 1.0, h: 0.16 });

    const handshakeIcon = await iconToBase64Png(FaHandshake, "#0056D2", 256);
    slide.addImage({ data: handshakeIcon, x: 0.8, y: 0.7, w: 0.45, h: 0.45 });

    slide.addText("Kogo możesz nam polecić?", {
      x: 1.4, y: 0.7, w: 7, h: 0.5,
      fontSize: 28, fontFace: FONT, color: C.textDark, bold: true, margin: 0
    });

    // Left: profiles
    slide.addText("PROFIL FIRMY", {
      x: 0.8, y: 1.45, w: 4.5, h: 0.3,
      fontSize: 10, fontFace: FONT, color: C.blue,
      bold: true, charSpacing: 2, margin: 0
    });

    const checkIcon = await iconToBase64Png(FaCheckCircle, "#0056D2", 256);
    const profiles = [
      "Firmy 50–500 pracowników",
      "Zespoły tonące w Excelu i ręcznej pracy",
      "Zarządy, które boją się kar AI Act",
      "Firmy, które kupiły Copilota / Gemini\ni nie widzą efektów",
      "Każdy, kto mówi: \"chcemy AI,\nale nie wiemy od czego zacząć\""
    ];

    let profileY = 1.85;
    for (let i = 0; i < profiles.length; i++) {
      const lines = profiles[i].split("\n").length;
      const h = lines > 1 ? 0.55 : 0.38;
      slide.addImage({ data: checkIcon, x: 0.8, y: profileY + 0.05, w: 0.24, h: 0.24 });
      slide.addText(profiles[i], {
        x: 1.15, y: profileY, w: 4.2, h,
        fontSize: 12, fontFace: FONT, color: C.textDark,
        lineSpacingMultiple: 1.2, margin: 0
      });
      profileY += h + 0.1;
    }

    // Right: industries card
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 5.8, y: 1.45, w: 3.6, h: 3.5,
      fill: { color: C.white }, shadow: makeCardShadow()
    });

    slide.addShape(pres.shapes.RECTANGLE, {
      x: 5.8, y: 1.45, w: 3.6, h: 0.05, fill: { color: C.blue }
    });

    slide.addText("BRANŻE", {
      x: 6.1, y: 1.65, w: 3, h: 0.3,
      fontSize: 10, fontFace: FONT, color: C.blue,
      bold: true, charSpacing: 2, margin: 0
    });

    const industries = [
      "Produkcja i logistyka",
      "E-commerce i retail",
      "Kancelarie prawne",
      "Software house'y",
      "Firmy konsultingowe",
      "Finanse i księgowość"
    ];

    slide.addText(
      industries.map((ind, idx) => ({
        text: ind,
        options: {
          bullet: { code: "2022" }, color: C.textDark, fontSize: 12,
          breakLine: idx < industries.length - 1, paraSpaceAfter: 8
        }
      })),
      { x: 6.1, y: 2.0, w: 3.0, h: 2.8, fontFace: FONT, margin: 0 }
    );
  }

  // ============================================================
  // SLIDE 8: CTA — LIGHT with red accent
  // ============================================================
  {
    const slide = pres.addSlide();
    slide.background = { color: C.offWhite };

    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 0.5, fill: { color: C.navy }
    });
    slide.addImage({ data: logoWhiteBase64, x: 0.4, y: 0.13, w: 1.0, h: 0.16 });

    // Dark logo centered bigger
    slide.addImage({
      data: logoDarkBase64,
      x: 3.5, y: 0.7, w: 3.0, h: 0.49
    });

    slide.addText("Umów bezpłatną diagnozę AI", {
      x: 0.8, y: 1.4, w: 8.4, h: 0.7,
      fontSize: 34, fontFace: FONT, color: C.textDark, bold: true, margin: 0
    });

    slide.addText("w Twojej firmie.", {
      x: 0.8, y: 2.0, w: 8.4, h: 0.5,
      fontSize: 34, fontFace: FONT, color: C.blue, bold: true, margin: 0
    });

    slide.addText("30 minut, które pokażą gdzie Twoja firma traci czas\ni pieniądze — i co z tym zrobić. Zgodnie z prawem.", {
      x: 0.8, y: 2.7, w: 8.4, h: 0.6,
      fontSize: 13, fontFace: FONT, color: C.darkGray,
      lineSpacingMultiple: 1.4, margin: 0
    });

    // RED CTA button
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.8, y: 3.5, w: 3.5, h: 0.55, fill: { color: C.red }
    });
    slide.addText("POROZMAWIAJMY  →", {
      x: 0.8, y: 3.5, w: 3.5, h: 0.55,
      fontSize: 15, fontFace: FONT, color: C.white,
      bold: true, align: "center", valign: "middle", margin: 0
    });

    // Contact
    const phoneIcon = await iconToBase64Png(FaPhone, "#0056D2", 256);
    const emailIcon = await iconToBase64Png(FaEnvelope, "#0056D2", 256);
    const globeIcon = await iconToBase64Png(FaGlobe, "#0056D2", 256);

    const contactY = 4.3;

    slide.addImage({ data: phoneIcon, x: 0.8, y: contactY + 0.05, w: 0.22, h: 0.22 });
    slide.addText("+48 508 106 046", {
      x: 1.1, y: contactY, w: 3, h: 0.3,
      fontSize: 12, fontFace: FONT, color: C.textDark, margin: 0
    });

    slide.addImage({ data: emailIcon, x: 0.8, y: contactY + 0.4, w: 0.22, h: 0.22 });
    slide.addText("biuro@dokodu.it", {
      x: 1.1, y: contactY + 0.35, w: 3, h: 0.3,
      fontSize: 12, fontFace: FONT, color: C.textDark, margin: 0
    });

    slide.addImage({ data: globeIcon, x: 0.8, y: contactY + 0.75, w: 0.22, h: 0.22 });
    slide.addText("dokodu.it", {
      x: 1.1, y: contactY + 0.7, w: 3, h: 0.3,
      fontSize: 12, fontFace: FONT, color: C.textDark, margin: 0
    });

    // Team card
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 5.8, y: 3.5, w: 3.6, h: 1.6,
      fill: { color: C.white }, shadow: makeCardShadow()
    });

    slide.addShape(pres.shapes.RECTANGLE, {
      x: 5.8, y: 3.5, w: 3.6, h: 0.05, fill: { color: C.blue }
    });

    const userIcon = await iconToBase64Png(FaUserTie, "#0056D2", 256);
    slide.addImage({ data: userIcon, x: 6.1, y: 3.7, w: 0.3, h: 0.3 });
    slide.addText([
      { text: "Alina Sieradzińska", options: { bold: true, color: C.textDark, fontSize: 13, breakLine: true } },
      { text: "COO & Legal · RODO · AI Act", options: { color: C.darkGray, fontSize: 10 } }
    ], { x: 6.5, y: 3.65, w: 2.7, h: 0.5, fontFace: FONT, margin: 0 });

    slide.addImage({ data: userIcon, x: 6.1, y: 4.25, w: 0.3, h: 0.3 });
    slide.addText([
      { text: "Kacper Sieradziński", options: { bold: true, color: C.textDark, fontSize: 13, breakLine: true } },
      { text: "CEO & Architekt AI", options: { color: C.darkGray, fontSize: 10 } }
    ], { x: 6.5, y: 4.2, w: 2.7, h: 0.5, fontFace: FONT, margin: 0 });

    // Tagline bottom
    slide.addText("Tech + Legal w Twojej firmie.", {
      x: 0.8, y: 5.2, w: 8.4, h: 0.3,
      fontSize: 11, fontFace: FONT, color: C.darkGray, italic: true, margin: 0
    });
  }

  // ============================================================
  const outputPath = "/home/kacper/DOKODU_BRAIN/docs/Dokodu_BNI_Pitch.pptx";
  await pres.writeFile({ fileName: outputPath });
  console.log("OK: " + outputPath);
}

buildPresentation().catch(err => {
  console.error("Error:", err);
  process.exit(1);
});
