import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  interpolate,
  spring,
  useVideoConfig,
} from "remotion";
import { loadFont } from "@remotion/google-fonts/PlusJakartaSans";
import { tiktokTheme as t } from "../../../../style/tiktok-theme";

const { fontFamily } = loadFont();

export interface CTACardProps {
  text?: string;
  handle?: string;
  showLogo?: boolean;
}

export const CTACard: React.FC<CTACardProps> = ({
  text = "Obserwuj po więcej",
  handle = "@kacpersieradzinski",
  showLogo = true,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Animated gradient: shift radial gradient position using sin/cos of frame
  const gradientX = 50 + Math.sin(frame * 0.02) * 30;
  const gradientY = 50 + Math.cos(frame * 0.015) * 25;

  // Accent line drops from above with spring bounce
  const lineSpring = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 120 },
  });
  const lineTranslateY = interpolate(lineSpring, [0, 1], [-100, 0]);

  // "DOKODU" text: fade in with spring, delay 8 frames
  const logoSpring = spring({
    frame: frame - 8,
    fps,
    config: { damping: 14 },
  });
  const logoOpacity = Math.max(0, Math.min(1, logoSpring));

  // CTA text: fade in + scale 0.9→1.0, delay 15 frames
  const ctaSpring = spring({
    frame: frame - 15,
    fps,
    config: { damping: 14 },
  });
  const ctaOpacity = Math.max(0, Math.min(1, ctaSpring));
  const ctaScale = interpolate(ctaSpring, [0, 1], [0.9, 1.0]);

  // Handle: fades in, delay 20 frames
  const handleOpacity = interpolate(frame, [20, 35], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Arrow bouncing down: sin-wave translateY, amplitude 8px
  const arrowBounce = Math.sin(frame * 0.15) * 8;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: t.colors.bg,
        background: `radial-gradient(circle at ${gradientX}% ${gradientY}%, #1a0a1e 0%, ${t.colors.bg} 60%)`,
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
      }}
    >
      {/* Accent line */}
      <div
        style={{
          width: 200,
          height: 3,
          backgroundColor: t.colors.accent,
          marginBottom: 28,
          transform: `translateY(${lineTranslateY}px)`,
          opacity: Math.max(0, Math.min(1, lineSpring)),
        }}
      />

      {/* DOKODU logo text */}
      {showLogo && (
        <div
          style={{
            fontFamily,
            fontWeight: 700,
            fontSize: 48,
            color: t.colors.text,
            textTransform: "uppercase",
            letterSpacing: 4,
            marginBottom: 48,
            opacity: logoOpacity,
            transform: `translateY(${interpolate(logoSpring, [0, 1], [10, 0])}px)`,
          }}
        >
          DOKODU
        </div>
      )}

      {/* Arrow bouncing down */}
      <div
        style={{
          fontSize: 36,
          color: t.colors.accent,
          marginBottom: 20,
          transform: `translateY(${arrowBounce}px)`,
          opacity: ctaOpacity,
        }}
      >
        ▼
      </div>

      {/* CTA text */}
      <div
        style={{
          fontFamily,
          fontSize: 36,
          fontWeight: 600,
          color: t.colors.accent,
          textAlign: "center",
          opacity: ctaOpacity,
          transform: `scale(${ctaScale})`,
          marginBottom: 20,
        }}
      >
        {text}
      </div>

      {/* Handle */}
      <div
        style={{
          fontFamily,
          fontSize: 24,
          fontWeight: 400,
          color: t.colors.gray,
          opacity: handleOpacity,
        }}
      >
        {handle}
      </div>
    </AbsoluteFill>
  );
};
