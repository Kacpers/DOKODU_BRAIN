import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate, spring, useVideoConfig } from "remotion";
import { theme } from "../../style/theme";

export const EndScreen: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const logoProgress = spring({ frame, fps, config: { damping: 16, stiffness: 100 } });
  const cardProgress = spring({ frame: frame - 20, fps, config: { damping: 14, stiffness: 120 } });

  return (
    <AbsoluteFill style={{
      backgroundColor: theme.colors.bg,
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      gap: 60,
    }}>
      {/* Channel name */}
      <div style={{
        fontFamily: theme.fonts.mono,
        fontSize: 32,
        fontWeight: 600,
        color: theme.colors.green,
        opacity: Math.min(1, logoProgress * 2),
        transform: `scale(${interpolate(logoProgress, [0, 1], [0.9, 1])})`,
        letterSpacing: 4,
        textTransform: "uppercase",
      }}>
        Kacper Sieradzinski
      </div>

      {/* Poprzedni film placeholder */}
      <div style={{
        width: 640,
        height: 360,
        background: theme.colors.bgCard,
        border: `2px solid ${theme.colors.grayDark}`,
        borderRadius: 20,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        gap: 16,
        opacity: Math.min(1, cardProgress * 2),
        transform: `translateY(${interpolate(cardProgress, [0, 1], [30, 0])}px)`,
      }}>
        <div style={{ fontSize: 48 }}>▶️</div>
        <div style={{ fontFamily: theme.fonts.ui, fontSize: 26, color: theme.colors.white, fontWeight: 600, textAlign: "center", padding: "0 40px" }}>
          Gemini CLI vs Claude Code
        </div>
        <div style={{ fontFamily: theme.fonts.ui, fontSize: 20, color: theme.colors.gray }}>
          wyniki mnie zaskoczyły →
        </div>
      </div>

      {/* Subscribe nudge */}
      <div style={{
        fontFamily: theme.fonts.mono,
        fontSize: 28,
        color: theme.colors.green,
        opacity: interpolate(frame, [60, 80], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
      }}>
        Subskrybuj — nowe filmy co tydzień
      </div>
    </AbsoluteFill>
  );
};
