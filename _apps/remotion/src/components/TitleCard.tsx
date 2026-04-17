import React from "react";
import { useCurrentFrame, interpolate, spring, useVideoConfig } from "remotion";
import { theme } from "../style/theme";

interface Props {
  title: string;
  subtitle?: string;
  accentColor?: string;
}

export const TitleCard: React.FC<Props> = ({
  title,
  subtitle,
  accentColor = theme.colors.green,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({ frame, fps, config: { damping: 18, stiffness: 100 } });
  const opacity = interpolate(frame, [0, 15], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      gap: 24,
    }}>
      <div
        style={{
          fontFamily: theme.fonts.ui,
          fontSize: 96,
          fontWeight: 800,
          color: theme.colors.white,
          letterSpacing: -2,
          textAlign: "center",
          opacity,
          transform: `scale(${interpolate(progress, [0, 1], [0.85, 1])})`,
        }}
      >
        {title}
      </div>
      {subtitle && (
        <div style={{
          fontFamily: theme.fonts.mono,
          fontSize: 36,
          color: accentColor,
          opacity: interpolate(frame, [20, 35], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          }),
        }}>
          {subtitle}
        </div>
      )}
    </div>
  );
};
