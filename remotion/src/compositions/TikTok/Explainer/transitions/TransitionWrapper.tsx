import React from "react";
import {
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
      return <>{children}</>;
    }

    if (isExiting) {
      const opacity = interpolate(exitFrame, [0, EXIT_FRAMES], [1, 0], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      });
      return <div style={{ opacity }}>{children}</div>;
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
      <div style={{ position: "relative", width: "100%", height: "100%" }}>
        {offsets.map((offset, i) => (
          <div
            key={i}
            style={{
              position: "absolute",
              inset: 0,
              transform: `translateX(${offset * (1 - progress)}px)`,
              mixBlendMode: i === 0 ? "normal" : "screen",
            }}
          >
            {children}
            <div
              style={{
                position: "absolute",
                inset: 0,
                backgroundColor: tints[i],
                pointerEvents: "none",
                opacity: 1 - progress,
              }}
            />
          </div>
        ))}
      </div>
    );
  }

  if (type === "swipeUp") {
    if (isExiting) {
      const exitProgress = interpolate(exitFrame, [0, EXIT_FRAMES], [0, 1], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      });
      return (
        <div
          style={{
            transform: `translateY(${exitProgress * -300}px)`,
            opacity: 1 - exitProgress,
          }}
        >
          {children}
        </div>
      );
    }

    const enterSpring = spring({
      frame,
      fps,
      config: { damping: 12 },
    });
    const translateY = interpolate(enterSpring, [0, 1], [1920, 0]);

    return (
      <div style={{ transform: `translateY(${translateY}px)` }}>
        {children}
      </div>
    );
  }

  if (type === "zoom") {
    if (isExiting) {
      const exitProgress = interpolate(exitFrame, [0, EXIT_FRAMES], [0, 1], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      });
      return (
        <div
          style={{
            transform: `scale(${1 - exitProgress * 0.15})`,
            opacity: 1 - exitProgress,
          }}
        >
          {children}
        </div>
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
      <div style={{ transform: `scale(${scale})`, opacity }}>
        {children}
      </div>
    );
  }

  if (type === "cut") {
    const enterOpacity = frame === 0 ? 0 : 1;
    const exitOpacity = frame >= durationInFrames - 1 ? 0 : 1;
    return (
      <div style={{ opacity: Math.min(enterOpacity, exitOpacity) }}>
        {children}
      </div>
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

  return <div style={{ opacity }}>{children}</div>;
};
