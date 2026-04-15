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

export const TikTokCTA: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const fadeIn = interpolate(frame, [0, 10], [0, 1], {
    extrapolateRight: "clamp",
  });
  const buttonSpring = spring({
    frame: frame - 10,
    fps,
    config: { damping: 10, stiffness: 100 },
  });
  const arrowBounce = Math.sin(frame * 0.15) * 8;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: t.colors.bg,
        justifyContent: "center",
        alignItems: "center",
        opacity: fadeIn,
      }}
    >
      {/* Arrow pointing down */}
      <div
        style={{
          fontSize: 48,
          color: t.colors.accent,
          marginBottom: 20,
          transform: `translateY(${arrowBounce}px)`,
        }}
      >
        ▼
      </div>

      {/* CTA Button */}
      <div
        style={{
          fontFamily,
          fontSize: 36,
          fontWeight: 700,
          color: t.colors.bg,
          backgroundColor: t.colors.accent,
          padding: "18px 48px",
          borderRadius: 50,
          transform: `scale(${interpolate(buttonSpring, [0, 1], [0.5, 1])})`,
          opacity: Math.max(0, buttonSpring),
        }}
      >
        Obserwuj po więcej
      </div>

      {/* Handle */}
      <div
        style={{
          fontFamily,
          fontSize: 24,
          color: t.colors.gray,
          marginTop: 20,
          opacity: Math.max(0, buttonSpring),
        }}
      >
        @kacpersieradzinski
      </div>
    </AbsoluteFill>
  );
};
