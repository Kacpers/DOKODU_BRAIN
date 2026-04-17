import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { tiktokTheme as t } from "../../../../style/tiktok-theme";

/**
 * ProgressBar — thin line at bottom showing video progress.
 * Helps retention: viewer sees "almost done" and watches to the end.
 * Positioned above TikTok UI (above safe zone bottom).
 */
export const ProgressBar: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const progress = frame / durationInFrames;

  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      {/* Track */}
      <div
        style={{
          position: "absolute",
          bottom: 310, // just above TikTok UI zone
          left: 40,
          right: 100,
          height: 3,
          backgroundColor: `${t.colors.text}15`, // very subtle track
          borderRadius: 2,
        }}
      >
        {/* Fill */}
        <div
          style={{
            width: `${progress * 100}%`,
            height: "100%",
            background: `linear-gradient(90deg, ${t.colors.accent}, ${t.colors.cyan})`,
            borderRadius: 2,
            boxShadow: `0 0 8px ${t.colors.accent}60`,
          }}
        />
      </div>
    </AbsoluteFill>
  );
};
