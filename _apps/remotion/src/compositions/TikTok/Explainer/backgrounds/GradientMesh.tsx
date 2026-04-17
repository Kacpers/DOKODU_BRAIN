import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";
import { tiktokTheme as t } from "../../../../style/tiktok-theme";

/**
 * GradientMesh — animated multi-point gradient.
 * Magenta in one corner, cyan in another, violet accent.
 * Positions shift slowly over time.
 */
export const GradientMesh: React.FC = () => {
  const frame = useCurrentFrame();

  // Animate gradient focal points
  const mag_x = 20 + Math.sin(frame * 0.005) * 15;
  const mag_y = 25 + Math.cos(frame * 0.004) * 20;
  const cyan_x = 80 + Math.cos(frame * 0.006) * 15;
  const cyan_y = 75 + Math.sin(frame * 0.005) * 15;
  const violet_x = 50 + Math.sin(frame * 0.007 + 1.5) * 20;
  const violet_y = 50 + Math.cos(frame * 0.008 + 0.5) * 25;

  const fadeIn = interpolate(frame, [0, 15], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: t.colors.bg,
        overflow: "hidden",
        opacity: fadeIn,
      }}
    >
      {/* Magenta radial */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background: `radial-gradient(ellipse at ${mag_x}% ${mag_y}%, ${t.colors.accent}30 0%, transparent 50%)`,
          pointerEvents: "none",
        }}
      />
      {/* Cyan radial */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background: `radial-gradient(ellipse at ${cyan_x}% ${cyan_y}%, ${t.colors.cyan}25 0%, transparent 50%)`,
          pointerEvents: "none",
        }}
      />
      {/* Violet radial */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background: `radial-gradient(ellipse at ${violet_x}% ${violet_y}%, ${t.colors.violet}1A 0%, transparent 45%)`,
          pointerEvents: "none",
        }}
      />
    </AbsoluteFill>
  );
};
