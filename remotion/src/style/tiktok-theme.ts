/**
 * TikTok Theme — Vertical Video (1080x1920)
 * Dokodu brand colors + TikTok-optimized subtitle styling
 */
export const tiktokTheme = {
  width: 1080,
  height: 1920,
  fps: 30,
  colors: {
    bg: "#000000",
    bgCard: "#1A1A1A",
    text: "#FFFFFF",
    accent: "#00D26A", // Dokodu green
    highlight: "#FFE135", // Yellow — active word highlight
    shadow: "#000000",
    gray: "#A0A0A0",
    red: "#FF4444",
  },
  fonts: {
    primary: "'Inter', sans-serif",
    mono: "'JetBrains Mono', monospace",
  },
  subtitles: {
    fontSize: 68,
    maxWordsPerLine: 4,
    yPosition: 0.55, // 55% from top — below face, above bottom UI
    outlineWidth: 4,
    shadowOffset: 3,
  },
} as const;
