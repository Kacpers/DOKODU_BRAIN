import React from "react";
import {
  AbsoluteFill,
  Img,
  useCurrentFrame,
  interpolate,
  staticFile,
} from "remotion";

/**
 * LogoWatermark — Dokodu logo (PNG) in top-left safe zone.
 * Uses the real logo from dokodu.it, not text.
 */
export const LogoWatermark: React.FC = () => {
  const frame = useCurrentFrame();

  const fadeIn = interpolate(frame, [10, 30], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div
        style={{
          position: "absolute",
          top: 55,
          left: 36,
          opacity: fadeIn * 0.7,
        }}
      >
        <Img
          src={staticFile("dokodu_logo.png")}
          style={{
            height: 24,
            width: "auto",
          }}
        />
      </div>
    </AbsoluteFill>
  );
};
