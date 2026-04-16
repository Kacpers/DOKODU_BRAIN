/**
 * TikTok Theme — Vertical Video (1080x1920)
 * Dokodu brand colors (from dokodu.it tailwind config)
 * Fonts: Plus Jakarta Sans (display), DM Sans (body)
 */
export const tiktokTheme = {
  width: 1080,
  height: 1920,
  fps: 30,
  colors: {
    bg: "#0A0D14",          // bg-950 (deepest navy)
    bgCard: "#12192A",      // bg-800 (card background)
    bgCardLight: "#1A2B42", // navy-light (lighter card/hover)
    text: "#E8EFFA",        // txt-100 (primary text)
    textSecondary: "#C9D7EE", // txt-200 (secondary text)
    accent: "#E91E63",      // magenta (primary CTA)
    accentLight: "#F06292", // magenta-light
    cyan: "#22D3EE",        // acc-cyan (secondary accent)
    violet: "#8B5CF6",      // acc-violet
    teal: "#14B8A6",        // acc-teal
    highlight: "#22D3EE",   // cyan — active word highlight
    shadow: "#000000",
    gray: "#6E7A95",        // muted-400
    red: "#EF4444",         // err
    green: "#10B981",       // ok
  },
  gradients: {
    main: "linear-gradient(135deg, #22D3EE 0%, #8B5CF6 50%, #F472B6 100%)",
    teal: "linear-gradient(135deg, #14B8A6 0%, #22D3EE 60%, #8B5CF6 100%)",
  },
  glows: {
    cyan: "0 0 30px rgba(34,211,238,.35)",
    violet: "0 0 30px rgba(139,92,246,.3)",
    magenta: "0 0 30px rgba(233,30,99,.4)",
  },
  fonts: {
    display: "'Plus Jakarta Sans', sans-serif",
    body: "'DM Sans', sans-serif",
    mono: "'JetBrains Mono', monospace",
    // Keep Inter as legacy/fallback
    primary: "'Plus Jakarta Sans', sans-serif",
  },
  subtitles: {
    fontSize: 68,
    maxWordsPerLine: 4,
    yPosition: 0.55, // 55% from top — below face, above bottom UI
    outlineWidth: 4,
    shadowOffset: 3,
  },
} as const;
