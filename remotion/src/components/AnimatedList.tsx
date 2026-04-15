import React from "react";
import { useCurrentFrame, interpolate, spring, useVideoConfig } from "remotion";
import { theme } from "../style/theme";

interface ListItem {
  icon?: string;
  text: string;
  subtext?: string;
}

interface Props {
  items: ListItem[];
  startFrame?: number;
  itemDelay?: number; // frames between items
  color?: string;
}

export const AnimatedList: React.FC<Props> = ({
  items,
  startFrame = 0,
  itemDelay = 20,
  color = theme.colors.white,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>
      {items.map((item, i) => {
        const itemStart = startFrame + i * itemDelay;
        const progress = spring({
          frame: frame - itemStart,
          fps,
          config: { damping: 14, stiffness: 120, mass: 0.8 },
        });
        const opacity = interpolate(frame, [itemStart, itemStart + 10], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });
        return (
          <div
            key={i}
            style={{
              opacity,
              transform: `translateX(${interpolate(progress, [0, 1], [-40, 0])}px)`,
              display: "flex",
              alignItems: "center",
              gap: 20,
            }}
          >
            {item.icon && (
              <span style={{ fontSize: 36, width: 44 }}>{item.icon}</span>
            )}
            <div>
              <div style={{
                fontFamily: theme.fonts.ui,
                fontSize: 38,
                color,
                fontWeight: 600,
              }}>
                {item.text}
              </div>
              {item.subtext && (
                <div style={{
                  fontFamily: theme.fonts.ui,
                  fontSize: 26,
                  color: theme.colors.gray,
                  marginTop: 4,
                }}>
                  {item.subtext}
                </div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};
