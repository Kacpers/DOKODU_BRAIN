import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";
import { TitleCard } from "../../components/TitleCard";
import { theme } from "../../style/theme";

export const TitleCardComp: React.FC = () => {
  const frame = useCurrentFrame();
  // Subtle scan line effect
  const scanY = (frame * 8) % theme.height;

  return (
    <AbsoluteFill style={{
      backgroundColor: theme.colors.bg,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      overflow: "hidden",
    }}>
      {/* Subtle grid background */}
      <div style={{
        position: "absolute",
        inset: 0,
        backgroundImage: `
          linear-gradient(${theme.colors.green}08 1px, transparent 1px),
          linear-gradient(90deg, ${theme.colors.green}08 1px, transparent 1px)
        `,
        backgroundSize: "80px 80px",
      }} />

      {/* Green glow top */}
      <div style={{
        position: "absolute",
        top: -200,
        left: "50%",
        transform: "translateX(-50%)",
        width: 800,
        height: 400,
        background: `radial-gradient(circle, ${theme.colors.green}30 0%, transparent 70%)`,
      }} />

      <TitleCard
        title="GEMINI CLI OD ZERA"
        subtitle="> AI agent w terminalu"
        accentColor={theme.colors.green}
      />
    </AbsoluteFill>
  );
};
