import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate, spring, useVideoConfig } from "remotion";
import { theme } from "../../style/theme";

const Column: React.FC<{
  label: string;
  time: string;
  color: string;
  delay: number;
  dimmed?: boolean;
}> = ({ label, time, color, delay, dimmed }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const progress = spring({ frame: frame - delay, fps, config: { damping: 14, stiffness: 100 } });

  return (
    <div style={{
      flex: 1,
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      gap: 24,
      opacity: dimmed ? 0.4 : Math.min(1, progress * 2),
      transform: `translateY(${interpolate(progress, [0, 1], [50, 0])}px)`,
    }}>
      <div style={{
        fontFamily: theme.fonts.ui,
        fontSize: 38,
        color: theme.colors.gray,
        fontWeight: 500,
      }}>
        {label}
      </div>
      <div style={{
        fontFamily: theme.fonts.ui,
        fontSize: 120,
        fontWeight: 800,
        color,
        lineHeight: 1,
      }}>
        {time}
      </div>
    </div>
  );
};

export const TimeComparison: React.FC = () => {
  const frame = useCurrentFrame();
  const dividerOpacity = interpolate(frame, [30, 50], [0, 1], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{
      backgroundColor: theme.colors.bg,
      display: "flex",
      flexDirection: "column",
    }}>
      <div style={{
        fontFamily: theme.fonts.ui,
        fontSize: 44,
        fontWeight: 700,
        color: theme.colors.white,
        textAlign: "center",
        padding: "60px 0 20px",
      }}>
        Konfiguracja infrastruktury
      </div>

      <div style={{ flex: 1, display: "flex", alignItems: "center" }}>
        <Column label="Ręcznie" time="~60 min" color={theme.colors.gray} delay={10} dimmed={frame > 60} />

        <div style={{
          width: 2,
          height: 300,
          background: theme.colors.grayDark,
          opacity: dividerOpacity,
        }} />

        <Column label="Gemini CLI" time="~15 min" color={theme.colors.green} delay={50} />
      </div>

      <div style={{
        fontFamily: theme.fonts.mono,
        fontSize: 32,
        color: theme.colors.green,
        textAlign: "center",
        padding: "20px 0 60px",
        opacity: interpolate(frame, [80, 100], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
      }}>
        4× szybciej
      </div>
    </AbsoluteFill>
  );
};
