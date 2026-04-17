import React from "react";
import { AbsoluteFill } from "remotion";

/**
 * SafeZone — constrains children to the area not covered by TikTok/IG UI.
 *
 * TikTok UI overlaps:
 *  - Top: ~150px (status bar + account name)
 *  - Bottom: ~300px (description, buttons, music ticker)
 *  - Right: ~80px (like/comment/share buttons)
 *
 * This component adds padding so content stays visible.
 */
export const SafeZone: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  return (
    <AbsoluteFill
      style={{
        paddingTop: 160,
        paddingBottom: 320,
        paddingLeft: 40,
        paddingRight: 100, // right side has like/comment buttons
      }}
    >
      {children}
    </AbsoluteFill>
  );
};
