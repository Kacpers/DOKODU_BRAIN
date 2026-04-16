import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import { loadFont } from "@remotion/google-fonts/Inter";
import { tiktokTheme as t } from "../../../../style/tiktok-theme";

const { fontFamily } = loadFont();

const EXIT_FRAMES = 10;
const DIVIDER_HEIGHT = 300;

interface VSCompareProps {
  left: { title: string; points: string[]; color?: string };
  right: { title: string; points: string[]; color?: string };
  vsText?: string;
}

export const VSCompare: React.FC<VSCompareProps> = ({
  left,
  right,
  vsText = "VS",
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const exitStart = durationInFrames - EXIT_FRAMES;

  // Left column: slides in from left
  const leftSpring = spring({
    frame,
    fps,
    config: { damping: 12 },
  });

  // Right column: slides in from right (delay 3 frames)
  const rightSpring = spring({
    frame: frame - 3,
    fps,
    config: { damping: 12 },
  });

  // VS badge: scale bounce (delay 10 frames)
  const vsSpring = spring({
    frame: frame - 10,
    fps,
    config: { damping: 8, stiffness: 200 },
  });

  // Divider line: height animation concurrent with columns
  const dividerSpring = spring({
    frame,
    fps,
    config: { damping: 12 },
  });

  // Exit animations
  const isExiting = frame >= exitStart;
  const exitProgress = interpolate(
    frame,
    [exitStart, durationInFrames],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  const leftTranslateX = isExiting
    ? interpolate(exitProgress, [0, 1], [0, -540])
    : interpolate(leftSpring, [0, 1], [-540, 0]);

  const rightTranslateX = isExiting
    ? interpolate(exitProgress, [0, 1], [0, 540])
    : interpolate(rightSpring, [0, 1], [540, 0]);

  const dividerCurrentHeight = interpolate(
    dividerSpring,
    [0, 1],
    [0, DIVIDER_HEIGHT]
  );

  const leftColor = left.color ?? t.colors.text;
  const rightColor = right.color ?? t.colors.accent;

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
          flexDirection: "row",
          alignItems: "center",
          justifyContent: "center",
          width: "100%",
          paddingLeft: 40,
          paddingRight: 40,
          position: "relative",
        }}
      >
        {/* Left column */}
        <div
          style={{
            width: "45%",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            transform: `translateX(${leftTranslateX}px)`,
          }}
        >
          <div
            style={{
              fontFamily,
              fontSize: 36,
              fontWeight: 700,
              color: leftColor,
              marginBottom: 24,
              textAlign: "center",
            }}
          >
            {left.title}
          </div>
          {left.points.map((point, i) => {
            const pointSpring = spring({
              frame: frame - (i * 8 + 5),
              fps,
              config: { damping: 14 },
            });
            const pointOpacity = Math.max(0, Math.min(1, pointSpring));
            return (
              <div
                key={i}
                style={{
                  display: "flex",
                  flexDirection: "row",
                  alignItems: "flex-start",
                  gap: 10,
                  marginBottom: 16,
                  opacity: pointOpacity,
                  width: "100%",
                }}
              >
                <div
                  style={{
                    width: 10,
                    height: 10,
                    borderRadius: 5,
                    backgroundColor: leftColor,
                    marginTop: 9,
                    flexShrink: 0,
                  }}
                />
                <span
                  style={{
                    fontFamily,
                    fontSize: 28,
                    color: t.colors.text,
                    lineHeight: 1.4,
                  }}
                >
                  {point}
                </span>
              </div>
            );
          })}
        </div>

        {/* Center: divider + VS badge */}
        <div
          style={{
            width: "10%",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            position: "relative",
          }}
        >
          {/* Vertical divider */}
          <div
            style={{
              width: 2,
              height: dividerCurrentHeight,
              backgroundColor: t.colors.accent,
              position: "absolute",
            }}
          />

          {/* VS badge */}
          <div
            style={{
              width: 60,
              height: 60,
              borderRadius: 30,
              backgroundColor: t.colors.accent,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              transform: `scale(${Math.max(0, vsSpring)})`,
              zIndex: 1,
            }}
          >
            <span
              style={{
                fontFamily,
                fontSize: 24,
                fontWeight: 900,
                color: t.colors.text,
              }}
            >
              {vsText}
            </span>
          </div>
        </div>

        {/* Right column */}
        <div
          style={{
            width: "45%",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            transform: `translateX(${rightTranslateX}px)`,
          }}
        >
          <div
            style={{
              fontFamily,
              fontSize: 36,
              fontWeight: 700,
              color: rightColor,
              marginBottom: 24,
              textAlign: "center",
            }}
          >
            {right.title}
          </div>
          {right.points.map((point, i) => {
            const pointSpring = spring({
              frame: frame - (i * 8 + 5),
              fps,
              config: { damping: 14 },
            });
            const pointOpacity = Math.max(0, Math.min(1, pointSpring));
            return (
              <div
                key={i}
                style={{
                  display: "flex",
                  flexDirection: "row",
                  alignItems: "flex-start",
                  gap: 10,
                  marginBottom: 16,
                  opacity: pointOpacity,
                  width: "100%",
                }}
              >
                <div
                  style={{
                    width: 10,
                    height: 10,
                    borderRadius: 5,
                    backgroundColor: rightColor,
                    marginTop: 9,
                    flexShrink: 0,
                  }}
                />
                <span
                  style={{
                    fontFamily,
                    fontSize: 28,
                    color: t.colors.text,
                    lineHeight: 1.4,
                  }}
                >
                  {point}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};
