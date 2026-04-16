import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  interpolate,
  spring,
  useVideoConfig,
} from "remotion";
import { loadFont } from "@remotion/google-fonts/PlusJakartaSans";
import { loadFont as loadBody } from "@remotion/google-fonts/DMSans";
import { tiktokTheme as t } from "../../../../style/tiktok-theme";

const { fontFamily } = loadFont();
const { fontFamily: bodyFont } = loadBody();

export interface SlideCardProps {
  title: string;
  icon?: string;
  bullets: string[];
  accentColor?: string;
}

export const SlideCard: React.FC<SlideCardProps> = ({
  title,
  icon,
  bullets,
  accentColor = t.colors.accent,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Card slides up from bottom
  const cardSpring = spring({
    frame,
    fps,
    config: { damping: 14 },
  });

  // Icon bounce-in, delayed 5 frames from card
  const iconSpring = spring({
    frame: frame - 5,
    fps,
    config: { damping: 10, stiffness: 200 },
  });

  // Title fade + translateY, delayed 8 frames
  const titleSpring = spring({
    frame: frame - 8,
    fps,
    config: { damping: 14 },
  });

  // Exit: card slides down in last 10 frames
  const exitStart = durationInFrames - 10;
  const exitProgress = interpolate(frame, [exitStart, durationInFrames], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const exitTranslateY = interpolate(exitProgress, [0, 1], [0, 1200]);

  const cardTranslateY = interpolate(cardSpring, [0, 1], [400, 0]) + exitTranslateY;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: t.colors.bg,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      {/* Card */}
      <div
        style={{
          width: "80%",
          backgroundColor: t.colors.bgCard,
          borderRadius: 24,
          padding: "48px 44px",
          transform: `translateY(${cardTranslateY}px)`,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          boxShadow: `0 20px 60px rgba(0,0,0,0.6)`,
        }}
      >
        {/* Icon */}
        {icon && (
          <div
            style={{
              fontSize: 64,
              marginBottom: 24,
              transform: `scale(${Math.max(0, iconSpring)})`,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            {icon}
          </div>
        )}

        {/* Title */}
        <div
          style={{
            fontFamily,
            fontWeight: 700,
            fontSize: 44,
            color: t.colors.text,
            textAlign: "center",
            lineHeight: 1.25,
            marginBottom: 36,
            transform: `translateY(${interpolate(titleSpring, [0, 1], [20, 0])}px)`,
            opacity: Math.max(0, titleSpring),
          }}
        >
          {title}
        </div>

        {/* Bullets */}
        <div
          style={{
            width: "100%",
            display: "flex",
            flexDirection: "column",
            gap: 20,
          }}
        >
          {bullets.map((bullet, i) => {
            const bulletSpring = spring({
              frame: frame - (8 + i * 8),
              fps,
              config: { damping: 14 },
            });

            return (
              <div
                key={i}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 16,
                  transform: `translateX(${interpolate(bulletSpring, [0, 1], [60, 0])}px)`,
                  opacity: Math.max(0, bulletSpring),
                }}
              >
                {/* Accent dot */}
                <div
                  style={{
                    width: 10,
                    height: 10,
                    borderRadius: "50%",
                    backgroundColor: accentColor,
                    flexShrink: 0,
                  }}
                />
                {/* Bullet text */}
                <div
                  style={{
                    fontFamily: bodyFont,
                    fontWeight: 400,
                    fontSize: 34,
                    color: t.colors.text,
                    lineHeight: 1.3,
                  }}
                >
                  {bullet}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};
