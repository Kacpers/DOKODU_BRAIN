import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate, spring, useVideoConfig } from "remotion";
import { theme } from "../../style/theme";

const Node: React.FC<{ icon: string; label: string; delay: number }> = ({ icon, label, delay }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const progress = spring({ frame: frame - delay, fps, config: { damping: 14, stiffness: 120 } });
  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      gap: 20,
      opacity: Math.min(1, progress * 2),
      transform: `translateY(${interpolate(progress, [0, 1], [40, 0])}px)`,
    }}>
      <div style={{
        width: 140,
        height: 140,
        borderRadius: 28,
        background: theme.colors.bgCard,
        border: `2px solid ${theme.colors.green}50`,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontSize: 64,
      }}>
        {icon}
      </div>
      <div style={{ fontFamily: theme.fonts.ui, fontSize: 32, color: theme.colors.white, fontWeight: 600 }}>
        {label}
      </div>
    </div>
  );
};

const Arrow: React.FC<{ delay: number; label?: string }> = ({ delay, label }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [delay, delay + 15], [0, 1], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 8, opacity }}>
      <div style={{ fontFamily: theme.fonts.mono, fontSize: 24, color: theme.colors.green }}>{label}</div>
      <div style={{ color: theme.colors.green, fontSize: 48 }}>→</div>
    </div>
  );
};

export const ReactLoop: React.FC = () => {
  const frame = useCurrentFrame();
  const subtitleOpacity = interpolate(frame, [80, 100], [0, 1], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{
      backgroundColor: theme.colors.bg,
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      gap: 60,
    }}>
      <div style={{ fontFamily: theme.fonts.ui, fontSize: 48, color: theme.colors.white, fontWeight: 700 }}>
        Jak działa Gemini CLI?
      </div>

      <div style={{ display: "flex", alignItems: "center", gap: 40 }}>
        <Node icon="💻" label="Terminal" delay={10} />
        <Arrow delay={30} label="prompt" />
        <Node icon="✨" label="Gemini" delay={40} />
        <Arrow delay={60} label="wynik" />
        <Node icon="🖥️" label="Serwer / Pliki" delay={70} />
      </div>

      <div style={{
        fontFamily: theme.fonts.mono,
        fontSize: 34,
        color: theme.colors.green,
        opacity: subtitleOpacity,
        letterSpacing: 1,
      }}>
        ReAct loop — myśl → działaj → obserwuj → myśl → ...
      </div>
    </AbsoluteFill>
  );
};
