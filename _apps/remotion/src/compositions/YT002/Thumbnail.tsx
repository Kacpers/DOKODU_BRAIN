import React from "react";
import { AbsoluteFill } from "remotion";
import { theme } from "../../style/theme";

/**
 * YT-002 Thumbnail Base Layer — 1280×720
 *
 * Eksport: npx remotion still YT002-Thumbnail out/YT002_thumbnail_base.png --frame=0
 *
 * Lewa ~45%: gradient fade (tu wklejasz zdjęcie twarzy w Canvie/Photoshopie)
 * Prawa ~55%: tekst + grafika
 */
export const Thumbnail: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: theme.colors.bg,
        width: 1280,
        height: 720,
        overflow: "hidden",
      }}
    >
      {/* === TŁO: siatka terminala === */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage: `
            linear-gradient(${theme.colors.green}10 1px, transparent 1px),
            linear-gradient(90deg, ${theme.colors.green}10 1px, transparent 1px)
          `,
          backgroundSize: "60px 60px",
        }}
      />

      {/* === GLOW: zielona poświata po prawej === */}
      <div
        style={{
          position: "absolute",
          right: -100,
          top: "50%",
          transform: "translateY(-50%)",
          width: 700,
          height: 700,
          background: `radial-gradient(circle, ${theme.colors.green}35 0%, ${theme.colors.green}10 40%, transparent 70%)`,
          pointerEvents: "none",
        }}
      />

      {/* === GRADIENT: lewa strona ciemna (miejsce na twarz) === */}
      <div
        style={{
          position: "absolute",
          left: 0,
          top: 0,
          width: 620,
          height: 720,
          background: `linear-gradient(to right, ${theme.colors.bg} 30%, transparent 100%)`,
          zIndex: 2,
        }}
      />

      {/* === PLACEHOLDER INFO: tylko w podglądzie === */}
      <div
        style={{
          position: "absolute",
          left: 0,
          top: 0,
          width: 560,
          height: 720,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          zIndex: 3,
          flexDirection: "column",
          gap: 12,
          opacity: 0.25,
        }}
      >
        <div style={{ fontSize: 64 }}>👤</div>
        <div
          style={{
            fontFamily: theme.fonts.ui,
            fontSize: 22,
            color: theme.colors.gray,
            textAlign: "center",
          }}
        >
          TWOJA TWARZ
          <br />
          tu w Canvie
        </div>
      </div>

      {/* === PRAWA STRONA: tekst + branding === */}
      <div
        style={{
          position: "absolute",
          right: 40,
          top: 0,
          bottom: 0,
          width: 660,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          gap: 28,
          zIndex: 4,
        }}
      >
        {/* Terminal badge */}
        <div
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 12,
            background: `${theme.colors.green}18`,
            border: `1px solid ${theme.colors.green}50`,
            borderRadius: 8,
            padding: "8px 20px",
            width: "fit-content",
          }}
        >
          <span
            style={{
              fontFamily: theme.fonts.mono,
              fontSize: 22,
              color: theme.colors.green,
            }}
          >
            &gt;_
          </span>
          <span
            style={{
              fontFamily: theme.fonts.mono,
              fontSize: 20,
              color: theme.colors.green,
              letterSpacing: 2,
            }}
          >
            GEMINI CLI
          </span>
        </div>

        {/* Główny tekst */}
        <div
          style={{
            fontFamily: theme.fonts.ui,
            fontSize: 86,
            fontWeight: 900,
            color: theme.colors.white,
            lineHeight: 1.0,
            letterSpacing: -2,
            textShadow: `0 0 40px ${theme.colors.green}50`,
          }}
        >
          AI AGENT
          <br />
          <span style={{ color: theme.colors.green, whiteSpace: "nowrap" }}>W TERMINALU</span>
        </div>

        {/* Subtext */}
        <div
          style={{
            fontFamily: theme.fonts.mono,
            fontSize: 26,
            color: theme.colors.gray,
            letterSpacing: 1,
          }}
        >
          instalacja + demo na żywo
        </div>
      </div>

    </AbsoluteFill>
  );
};
