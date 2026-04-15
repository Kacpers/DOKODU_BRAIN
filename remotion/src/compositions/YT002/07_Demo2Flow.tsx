import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate, spring, useVideoConfig } from "remotion";
import { theme } from "../../style/theme";

const Step: React.FC<{ num: string; title: string; sub: string; delay: number }> = ({ num, title, sub, delay }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const progress = spring({ frame: frame - delay, fps, config: { damping: 14, stiffness: 120 } });
  return (
    <div style={{
      flex: 1,
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      gap: 20,
      opacity: Math.min(1, progress * 2),
      transform: `translateY(${interpolate(progress, [0, 1], [40, 0])}px)`,
    }}>
      <div style={{
        width: 80,
        height: 80,
        borderRadius: "50%",
        background: theme.colors.green,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontFamily: theme.fonts.ui,
        fontSize: 40,
        fontWeight: 800,
        color: theme.colors.bg,
      }}>
        {num}
      </div>
      <div style={{ textAlign: "center" }}>
        <div style={{ fontFamily: theme.fonts.ui, fontSize: 36, fontWeight: 700, color: theme.colors.white }}>
          {title}
        </div>
        <div style={{ fontFamily: theme.fonts.ui, fontSize: 26, color: theme.colors.gray, marginTop: 8 }}>
          {sub}
        </div>
      </div>
    </div>
  );
};

export const Demo2Flow: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill style={{
      backgroundColor: theme.colors.bg,
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      gap: 60,
      padding: "0 100px",
    }}>
      <div style={{ fontFamily: theme.fonts.ui, fontSize: 48, fontWeight: 700, color: theme.colors.white }}>
        Code Review z Gemini CLI
      </div>

      <div style={{ display: "flex", alignItems: "center", width: "100%", gap: 0 }}>
        <Step num="1" title="Prompt" sub="opisujesz co sprawdzić" delay={15} />
        <div style={{
          fontSize: 48,
          color: theme.colors.green,
          opacity: interpolate(frame, [40, 55], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
        }}>→</div>
        <Step num="2" title="Agent czyta kod" sub="plik po pliku, sam decyduje" delay={50} />
        <div style={{
          fontSize: 48,
          color: theme.colors.green,
          opacity: interpolate(frame, [80, 95], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
        }}>→</div>
        <Step num="3" title="Lista znalezisk" sub="krytyczne / średnie / niskie" delay={85} />
      </div>

      <div style={{
        fontFamily: theme.fonts.mono,
        fontSize: 30,
        color: theme.colors.green,
        opacity: interpolate(frame, [110, 130], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
      }}>
        ✓ Bez manualnego code review. Przed każdym deployem.
      </div>
    </AbsoluteFill>
  );
};
