import React from "react";
import { useCurrentFrame, interpolate, spring, useVideoConfig } from "remotion";
import { theme } from "../style/theme";

interface Props {
  label: string;
  color?: string;
  bgColor?: string;
  startFrame?: number;
}

export const Badge: React.FC<Props> = ({
  label,
  color = theme.colors.bg,
  bgColor = theme.colors.green,
  startFrame = 0,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const progress = spring({
    frame: frame - startFrame,
    fps,
    config: { damping: 12, stiffness: 180 },
  });
  return (
    <div style={{
      display: "inline-flex",
      alignItems: "center",
      background: bgColor,
      color,
      padding: "12px 28px",
      borderRadius: 999,
      fontFamily: theme.fonts.ui,
      fontWeight: 700,
      fontSize: 30,
      opacity: Math.min(1, progress * 2),
      transform: `scale(${interpolate(progress, [0, 1], [0.5, 1])})`,
    }}>
      {label}
    </div>
  );
};
