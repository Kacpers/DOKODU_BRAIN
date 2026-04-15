import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  interpolate,
  spring,
  useVideoConfig,
} from "remotion";
import { loadFont } from "@remotion/google-fonts/Inter";
import { tiktokTheme as t } from "../../style/tiktok-theme";

const { fontFamily } = loadFont();

export const TikTokIntro: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const nameSpring = spring({ frame, fps, config: { damping: 12 } });
  const handleSpring = spring({
    frame: frame - 8,
    fps,
    config: { damping: 15 },
  });
  const fadeOut = interpolate(frame, [35, 45], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: t.colors.bg,
        justifyContent: "center",
        alignItems: "center",
        opacity: fadeOut,
      }}
    >
      {/* Accent line */}
      <div
        style={{
          width: interpolate(nameSpring, [0, 1], [0, 200]),
          height: 3,
          backgroundColor: t.colors.accent,
          marginBottom: 24,
        }}
      />

      {/* Name */}
      <div
        style={{
          fontFamily,
          fontSize: 52,
          fontWeight: 700,
          color: t.colors.text,
          transform: `translateY(${interpolate(nameSpring, [0, 1], [30, 0])}px)`,
          opacity: nameSpring,
          letterSpacing: 2,
        }}
      >
        KACPER SIERADZIŃSKI
      </div>

      {/* Handle */}
      <div
        style={{
          fontFamily,
          fontSize: 28,
          color: t.colors.accent,
          marginTop: 12,
          transform: `translateY(${interpolate(handleSpring, [0, 1], [20, 0])}px)`,
          opacity: Math.max(0, handleSpring),
        }}
      >
        @kacpersieradzinski
      </div>
    </AbsoluteFill>
  );
};
