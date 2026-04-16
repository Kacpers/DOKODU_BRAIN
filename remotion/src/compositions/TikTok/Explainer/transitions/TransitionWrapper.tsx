import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";

interface TransitionWrapperProps {
  type: "glitch" | "swipeUp" | "zoom" | "cut" | "dissolve";
  children: React.ReactNode;
}

const ENTER_FRAMES = 15;
const EXIT_FRAMES = 10;

export const TransitionWrapper: React.FC<TransitionWrapperProps> = ({
  type,
  children,
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames, fps } = useVideoConfig();

  const exitStart = durationInFrames - EXIT_FRAMES;
  const isExiting = frame >= exitStart;
  const exitFrame = frame - exitStart;

  if (type === "glitch") {
    // Snap to clean after 4 frames
    if (frame >= 4 && !isExiting) {
      return <AbsoluteFill>{children}</AbsoluteFill>;
    }

    if (isExiting) {
      const opacity = interpolate(exitFrame, [0, EXIT_FRAMES], [1, 0], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      });
      return <AbsoluteFill style={{ opacity }}>{children}</AbsoluteFill>;
    }

    // Glitch enter: 3 overlapping copies with RGB offsets
    const offsets = [-4, 0, 4];
    const tints = [
      "rgba(255,0,0,0.2)",
      "rgba(0,255,0,0.2)",
      "rgba(0,0,255,0.2)",
    ];
    const progress = frame / 4; // 0→1 over first 4 frames

    return (
      <AbsoluteFill>
        {offsets.map((offset, i) => (
          <AbsoluteFill
            key={i}
            style={{
              transform: `translateX(${offset * (1 - progress)}px)`,
              mixBlendMode: i === 0 ? "normal" : "screen",
            }}
          >
            {children}
            <AbsoluteFill
              style={{
                backgroundColor: tints[i],
                pointerEvents: "none",
                opacity: 1 - progress,
              }}
            />
          </AbsoluteFill>
        ))}
      </AbsoluteFill>
    );
  }

  if (type === "swipeUp") {
    if (isExiting) {
      const exitProgress = interpolate(exitFrame, [0, EXIT_FRAMES], [0, 1], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      });
      return (
        <AbsoluteFill
          style={{
            transform: `translateY(${exitProgress * -300}px)`,
            opacity: 1 - exitProgress,
          }}
        >
          {children}
        </AbsoluteFill>
      );
    }

    const enterSpring = spring({
      frame,
      fps,
      config: { damping: 12 },
    });
    const translateY = interpolate(enterSpring, [0, 1], [1920, 0]);

    return (
      <AbsoluteFill style={{ transform: `translateY(${translateY}px)` }}>
        {children}
      </AbsoluteFill>
    );
  }

  if (type === "zoom") {
    if (isExiting) {
      const exitProgress = interpolate(exitFrame, [0, EXIT_FRAMES], [0, 1], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      });
      return (
        <AbsoluteFill
          style={{
            transform: `scale(${1 - exitProgress * 0.15})`,
            opacity: 1 - exitProgress,
          }}
        >
          {children}
        </AbsoluteFill>
      );
    }

    const enterSpring = spring({
      frame,
      fps,
      config: { damping: 12 },
    });
    const scale = interpolate(enterSpring, [0, 1], [1.5, 1.0]);
    const opacity = interpolate(frame, [0, ENTER_FRAMES], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });

    return (
      <AbsoluteFill style={{ transform: `scale(${scale})`, opacity }}>
        {children}
      </AbsoluteFill>
    );
  }

  if (type === "cut") {
    const enterOpacity = frame === 0 ? 0 : 1;
    const exitOpacity = frame >= durationInFrames - 1 ? 0 : 1;
    return (
      <AbsoluteFill
        style={{ opacity: Math.min(enterOpacity, exitOpacity) }}
      >
        {children}
      </AbsoluteFill>
    );
  }

  // dissolve (default)
  const enterOpacity = interpolate(frame, [0, ENTER_FRAMES], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const exitOpacity = interpolate(
    frame,
    [exitStart, durationInFrames],
    [1, 0],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );
  const opacity = isExiting ? exitOpacity : enterOpacity;

  return (
    <AbsoluteFill style={{ opacity }}>
      {children}
    </AbsoluteFill>
  );
};
