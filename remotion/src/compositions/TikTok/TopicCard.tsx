import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  interpolate,
  spring,
  useVideoConfig,
} from "remotion";
import { loadFont } from "@remotion/google-fonts/Inter";
import { loadFont as loadMono } from "@remotion/google-fonts/JetBrainsMono";
import { tiktokTheme as t } from "../../style/tiktok-theme";

const { fontFamily } = loadFont();
const { fontFamily: monoFamily } = loadMono();

/**
 * TopicCard — wyświetla tytuł/temat TikToka na początku
 * Używany jako overlay na pierwszych 2-3 sekundach
 * Props przez Remotion inputProps (topic, category)
 */
export const TopicCard: React.FC<{
  topic?: string;
  category?: string;
}> = ({ topic = "Temat TikToka", category = "AI Tips" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const slideIn = spring({ frame, fps, config: { damping: 14 } });
  const fadeOut = interpolate(frame, [60, 75], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        justifyContent: "flex-end",
        alignItems: "center",
        paddingBottom: 400,
        opacity: fadeOut,
      }}
    >
      {/* Category badge */}
      <div
        style={{
          fontFamily: monoFamily,
          fontSize: 20,
          color: t.colors.accent,
          backgroundColor: `${t.colors.accent}22`,
          padding: "8px 20px",
          borderRadius: 20,
          marginBottom: 16,
          transform: `translateY(${interpolate(slideIn, [0, 1], [40, 0])}px)`,
          opacity: slideIn,
          textTransform: "uppercase",
          letterSpacing: 2,
        }}
      >
        {category}
      </div>

      {/* Topic text */}
      <div
        style={{
          fontFamily,
          fontSize: 44,
          fontWeight: 800,
          color: t.colors.text,
          textAlign: "center",
          maxWidth: 900,
          lineHeight: 1.3,
          transform: `translateY(${interpolate(slideIn, [0, 1], [60, 0])}px)`,
          opacity: slideIn,
          textShadow: "0 4px 20px rgba(0,0,0,0.8)",
        }}
      >
        {topic}
      </div>
    </AbsoluteFill>
  );
};
