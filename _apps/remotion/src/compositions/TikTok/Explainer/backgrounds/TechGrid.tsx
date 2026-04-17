import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";
import { tiktokTheme as t } from "../../../../style/tiktok-theme";

/**
 * TechGrid — subtle dot grid with slow parallax drift.
 * Tech/AI aesthetic in Dokodu palette.
 */
export const TechGrid: React.FC = () => {
  const frame = useCurrentFrame();

  // Slow drift
  const offsetX = Math.sin(frame * 0.003) * 15;
  const offsetY = frame * 0.15; // slow upward scroll

  // Grid dots
  const dotSpacing = 60;
  const cols = Math.ceil(1080 / dotSpacing) + 2;
  const rows = Math.ceil(1920 / dotSpacing) + 2;

  const fadeIn = interpolate(frame, [0, 15], [0, 1], {
    extrapolateRight: "clamp",
  });

  // Generate dots
  const dots: React.ReactNode[] = [];
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const x = c * dotSpacing + offsetX;
      const y = (r * dotSpacing - (offsetY % dotSpacing));

      // Vary dot opacity based on distance from center
      const cx = 540; // center x
      const cy = 960; // center y
      const dist = Math.sqrt((x - cx) ** 2 + (y - cy) ** 2);
      const maxDist = 1100;
      const distOpacity = Math.max(0, 1 - dist / maxDist);

      // Alternate dot colors between cyan and violet at low opacity
      const isCyan = (r + c) % 3 === 0;
      const color = isCyan ? t.colors.cyan : t.colors.violet;

      dots.push(
        <circle
          key={`${r}-${c}`}
          cx={x}
          cy={y}
          r={1.5}
          fill={color}
          opacity={distOpacity * 0.12}
        />
      );
    }
  }

  // Occasional connecting lines between nearby dots (sparse)
  const lines: React.ReactNode[] = [];
  for (let r = 0; r < rows - 1; r += 3) {
    for (let c = 0; c < cols - 1; c += 4) {
      const x1 = c * dotSpacing + offsetX;
      const y1 = (r * dotSpacing - (offsetY % dotSpacing));
      const x2 = (c + 1) * dotSpacing + offsetX;
      const y2 = (r + 1) * dotSpacing - (offsetY % dotSpacing);

      const cx = 540;
      const cy = 960;
      const dist = Math.sqrt(((x1 + x2) / 2 - cx) ** 2 + ((y1 + y2) / 2 - cy) ** 2);
      const distOpacity = Math.max(0, 1 - dist / 900);

      lines.push(
        <line
          key={`l-${r}-${c}`}
          x1={x1}
          y1={y1}
          x2={x2}
          y2={y2}
          stroke={t.colors.cyan}
          strokeWidth={0.5}
          opacity={distOpacity * 0.06}
        />
      );
    }
  }

  return (
    <AbsoluteFill
      style={{
        backgroundColor: t.colors.bg,
        overflow: "hidden",
        opacity: fadeIn,
      }}
    >
      <svg
        width={1080}
        height={1920}
        style={{ position: "absolute", inset: 0 }}
      >
        {lines}
        {dots}
      </svg>
    </AbsoluteFill>
  );
};
