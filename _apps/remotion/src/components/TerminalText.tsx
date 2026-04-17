import React from "react";
import { useCurrentFrame, interpolate } from "remotion";
import { theme } from "../style/theme";

interface Props {
  text: string;
  startFrame?: number;
  color?: string;
  fontSize?: number;
  delay?: number; // frames before starting
}

export const TerminalText: React.FC<Props> = ({
  text,
  startFrame = 0,
  color = theme.colors.green,
  fontSize = 42,
  delay = 0,
}) => {
  const frame = useCurrentFrame();
  const actualFrame = frame - startFrame - delay;
  const charsPerFrame = 2;
  const charsToShow = Math.max(0, Math.floor(actualFrame * charsPerFrame));
  const visible = text.slice(0, charsToShow);
  const showCursor = actualFrame >= 0;

  return (
    <span style={{ fontFamily: theme.fonts.mono, fontSize, color }}>
      {visible}
      {showCursor && (
        <span
          style={{
            opacity: Math.floor(frame / 15) % 2 === 0 ? 1 : 0,
            color: theme.colors.greenNeon,
          }}
        >
          █
        </span>
      )}
    </span>
  );
};
