import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";
import { TerminalText } from "../../components/TerminalText";
import { theme } from "../../style/theme";

export const Opener: React.FC = () => {
  const frame = useCurrentFrame();
  const bgOpacity = interpolate(frame, [120, 150], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{
      backgroundColor: theme.colors.bg,
      display: "flex",
      flexDirection: "column",
      justifyContent: "center",
      padding: "0 140px",
      gap: 32,
      opacity: bgOpacity,
    }}>
      {/* Prompt line */}
      <div style={{ fontFamily: theme.fonts.mono, fontSize: 38, color: theme.colors.gray }}>
        root@dokodu:~#
      </div>

      {/* SSH command */}
      <TerminalText
        text="ssh deploy@vps.hostinger.com"
        startFrame={0}
        color={theme.colors.white}
        fontSize={44}
      />

      {/* Connected response */}
      {frame > 30 && (
        <div style={{
          fontFamily: theme.fonts.mono,
          fontSize: 36,
          color: theme.colors.green,
          opacity: interpolate(frame, [30, 45], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          }),
        }}>
          ✓ Połączono z serwerem
        </div>
      )}

      {/* gemini command */}
      {frame > 55 && (
        <>
          <div style={{ fontFamily: theme.fonts.mono, fontSize: 38, color: theme.colors.gray, marginTop: 24 }}>
            root@vps-hostinger:~#
          </div>
          <TerminalText
            text="gemini"
            startFrame={55}
            color={theme.colors.greenNeon}
            fontSize={52}
          />
        </>
      )}
    </AbsoluteFill>
  );
};
