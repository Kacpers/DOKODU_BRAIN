import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  interpolate,
  spring,
  useVideoConfig,
} from "remotion";
import { loadFont } from "@remotion/google-fonts/Inter";
import { tiktokTheme as t } from "../../../../style/tiktok-theme";

const { fontFamily } = loadFont();

export interface StatCounterProps {
  value: number;
  from?: number;
  label: string;
  suffix?: string;
  prefix?: string;
}

export const StatCounter: React.FC<StatCounterProps> = ({
  value,
  from = 0,
  label,
  suffix,
  prefix,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Count up over 70% of total frames with easeOut
  const countDuration = Math.floor(durationInFrames * 0.7);
  const currentValue = Math.round(
    interpolate(frame, [0, countDuration], [from, value], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: (t) => 1 - Math.pow(1 - t, 3), // easeOut cubic
    })
  );

  // Label fades in after number reaches 30% of count duration
  const labelFadeStart = Math.floor(countDuration * 0.3);
  const labelOpacity = interpolate(
    frame,
    [labelFadeStart, labelFadeStart + 15],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  // Scale pulse when reaching target value
  const pulseFrame = frame - countDuration;
  const pulseSpring = spring({
    frame: pulseFrame,
    fps,
    config: { damping: 8, stiffness: 300 },
  });
  // Pulse: 1.0 → 1.1 → 1.0
  const pulseScale =
    pulseFrame >= 0 && pulseFrame < 20
      ? 1 + interpolate(pulseSpring, [0, 1], [0, 0.1]) * (1 - pulseSpring)
      : 1;

  // Exit: smash zoom out — scale 1→2.5 + opacity 1→0 in last 10 frames
  const exitStart = durationInFrames - 10;
  const exitScale = interpolate(frame, [exitStart, durationInFrames], [1, 2.5], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const exitOpacity = interpolate(frame, [exitStart, durationInFrames], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const isExiting = frame >= exitStart;
  const finalScale = isExiting ? exitScale : pulseScale;
  const finalOpacity = isExiting ? exitOpacity : 1;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: t.colors.bg,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          transform: `scale(${finalScale})`,
          opacity: finalOpacity,
        }}
      >
        {/* Number row: prefix + number + suffix */}
        <div
          style={{
            display: "flex",
            alignItems: "baseline",
            gap: 4,
          }}
        >
          {prefix && (
            <span
              style={{
                fontFamily,
                fontWeight: 900,
                fontSize: 120,
                color: t.colors.accent,
                lineHeight: 1,
              }}
            >
              {prefix}
            </span>
          )}
          <span
            style={{
              fontFamily,
              fontWeight: 900,
              fontSize: 160,
              color: t.colors.accent,
              lineHeight: 1,
              letterSpacing: -4,
            }}
          >
            {currentValue}
          </span>
          {suffix && (
            <span
              style={{
                fontFamily,
                fontWeight: 900,
                fontSize: 120,
                color: t.colors.accent,
                lineHeight: 1,
              }}
            >
              {suffix}
            </span>
          )}
        </div>

        {/* Label */}
        <div
          style={{
            fontFamily,
            fontWeight: 400,
            fontSize: 40,
            color: t.colors.gray,
            marginTop: 16,
            opacity: labelOpacity,
            textAlign: "center",
          }}
        >
          {label}
        </div>
      </div>
    </AbsoluteFill>
  );
};
