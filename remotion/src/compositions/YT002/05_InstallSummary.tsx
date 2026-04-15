import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate, spring, useVideoConfig } from "remotion";
import { Badge } from "../../components/Badge";
import { theme } from "../../style/theme";

const CodeLine: React.FC<{ code: string; delay: number; dim?: boolean }> = ({ code, delay, dim }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const progress = spring({ frame: frame - delay, fps, config: { damping: 16, stiffness: 140 } });
  return (
    <div style={{
      fontFamily: theme.fonts.mono,
      fontSize: 38,
      color: dim ? theme.colors.gray : theme.colors.green,
      opacity: Math.min(1, progress * 2),
      transform: `translateX(${interpolate(progress, [0, 1], [-20, 0])}px)`,
    }}>
      <span style={{ color: theme.colors.gray, marginRight: 16 }}>$</span>{code}
    </div>
  );
};

export const InstallSummary: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill style={{
      backgroundColor: theme.colors.bg,
      display: "flex",
      flexDirection: "column",
      justifyContent: "center",
      padding: "0 160px",
      gap: 40,
    }}>
      <div style={{ display: "flex", alignItems: "center", gap: 20, marginBottom: 16 }}>
        <div style={{ fontFamily: theme.fonts.ui, fontSize: 52, fontWeight: 700, color: theme.colors.white }}>
          Instalacja
        </div>
        <Badge label="2 minuty" startFrame={5} />
        <Badge label="Node.js 18+" bgColor={theme.colors.geminiBlue} color={theme.colors.white} startFrame={15} />
      </div>

      <CodeLine code="node --version" delay={20} dim />
      <CodeLine code="npm install -g @google/gemini-cli" delay={40} />

      <div style={{
        fontFamily: theme.fonts.ui,
        fontSize: 28,
        color: theme.colors.gray,
        opacity: interpolate(frame, [65, 80], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
        marginTop: 8,
        paddingLeft: 4,
      }}>
        lub bez instalacji:
      </div>

      <CodeLine code="npx @google/gemini-cli" delay={70} dim />

      <div style={{
        fontFamily: theme.fonts.mono,
        fontSize: 30,
        color: theme.colors.green,
        opacity: interpolate(frame, [95, 110], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
        marginTop: 16,
      }}>
        ✓ Gotowe — wpisz: gemini
      </div>
    </AbsoluteFill>
  );
};
