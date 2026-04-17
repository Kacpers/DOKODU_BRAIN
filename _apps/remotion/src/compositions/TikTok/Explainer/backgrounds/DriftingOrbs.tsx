import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";
import { tiktokTheme as t } from "../../../../style/tiktok-theme";

/**
 * DriftingOrbs — 3 blurred color orbs drifting slowly across the screen.
 * Colors: magenta, cyan, violet from Dokodu palette.
 * Opacity ~20% to not overpower content.
 */
export const DriftingOrbs: React.FC = () => {
  const frame = useCurrentFrame();

  const orbs = [
    {
      color: t.colors.accent, // magenta
      size: 500,
      blur: 120,
      x: 50 + Math.sin(frame * 0.008) * 35,
      y: 30 + Math.cos(frame * 0.006) * 25,
      opacity: 0.18,
    },
    {
      color: t.colors.cyan,
      size: 400,
      blur: 100,
      x: 70 + Math.cos(frame * 0.01) * 30,
      y: 65 + Math.sin(frame * 0.007) * 20,
      opacity: 0.15,
    },
    {
      color: t.colors.violet,
      size: 350,
      blur: 90,
      x: 25 + Math.sin(frame * 0.012 + 2) * 25,
      y: 50 + Math.cos(frame * 0.009 + 1) * 30,
      opacity: 0.12,
    },
  ];

  // Fade in over first 15 frames
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
      {orbs.map((orb, i) => (
        <div
          key={i}
          style={{
            position: "absolute",
            left: `${orb.x}%`,
            top: `${orb.y}%`,
            width: orb.size,
            height: orb.size,
            borderRadius: "50%",
            background: `radial-gradient(circle, ${orb.color} 0%, transparent 70%)`,
            filter: `blur(${orb.blur}px)`,
            opacity: orb.opacity,
            transform: "translate(-50%, -50%)",
            pointerEvents: "none",
          }}
        />
      ))}
    </AbsoluteFill>
  );
};
