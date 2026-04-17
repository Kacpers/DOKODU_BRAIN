import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import { loadFont } from "@remotion/google-fonts/PlusJakartaSans";
import { loadFont as loadMono } from "@remotion/google-fonts/JetBrainsMono";
import { tiktokTheme as t } from "../../../../style/tiktok-theme";

const { fontFamily } = loadFont();
const { fontFamily: monoFamily } = loadMono();

const EXIT_FRAMES = 10;
const CHARS_PER_FRAME = 3;

interface ScreenMockupProps {
  device: "phone" | "monitor" | "browser";
  title?: string;
  lines?: string[];
  highlightLine?: number;
}

/** Compute how many characters have been revealed by a given frame */
function getRevealedChars(lines: string[], frame: number): number {
  return frame * CHARS_PER_FRAME;
}

/** Get char count offset for lines before lineIdx */
function lineOffset(lines: string[], lineIdx: number): number {
  let offset = 0;
  for (let i = 0; i < lineIdx; i++) {
    offset += lines[i].length + 1; // +1 for newline pause
  }
  return offset;
}

export const ScreenMockup: React.FC<ScreenMockupProps> = ({
  device,
  title,
  lines = [],
  highlightLine,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const exitStart = durationInFrames - EXIT_FRAMES;
  const isExiting = frame >= exitStart;

  const exitProgress = interpolate(
    frame,
    [exitStart, durationInFrames],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  // Device frame: fade in + scale spring
  const frameSpring = spring({
    frame,
    fps,
    config: { damping: 14 },
  });

  const frameScale = interpolate(frameSpring, [0, 1], [0.95, 1.0]);
  const frameOpacity = Math.max(0, Math.min(1, frameSpring));

  // Screen content: delayed opacity (screen powering on)
  const screenOpacity = interpolate(frame, [8, 18], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Title fade in
  const titleOpacity = interpolate(frame, [2, 12], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Exit: slide up off screen
  const exitTranslateY = isExiting
    ? interpolate(exitProgress, [0, 1], [0, -1000])
    : 0;

  // Total chars revealed so far (with 8-frame screen-on delay)
  const contentFrame = Math.max(0, frame - 8);
  const totalRevealed = getRevealedChars(lines, contentFrame);

  // Compute per-line text
  const renderedLines = lines.map((line, lineIdx) => {
    const offset = lineOffset(lines, lineIdx);
    const charsInThisLine = Math.max(0, Math.min(line.length, totalRevealed - offset));
    return line.slice(0, charsInThisLine);
  });

  // Frame dimensions per device
  const frameStyles = {
    phone: {
      width: 380,
      height: 700,
      borderRadius: 40,
    },
    monitor: {
      width: 700,
      height: 440,
      borderRadius: 12,
    },
    browser: {
      width: 700,
      height: 480,
      borderRadius: 12,
    },
  };

  const dims = frameStyles[device];

  const renderDeviceChrome = () => {
    if (device === "phone") {
      return (
        // Notch
        <div
          style={{
            position: "absolute",
            top: 0,
            left: "50%",
            transform: "translateX(-50%)",
            width: 120,
            height: 24,
            backgroundColor: t.colors.bg,
            borderRadius: "0 0 14px 14px",
            zIndex: 2,
          }}
        />
      );
    }

    if (device === "monitor") {
      return (
        // Stand below monitor
        <>
          <div
            style={{
              position: "absolute",
              bottom: -40,
              left: "50%",
              transform: "translateX(-50%)",
              width: 0,
              height: 0,
              borderLeft: "50px solid transparent",
              borderRight: "50px solid transparent",
              borderTop: `40px solid ${t.colors.gray}`,
            }}
          />
          <div
            style={{
              position: "absolute",
              bottom: -50,
              left: "50%",
              transform: "translateX(-50%)",
              width: 120,
              height: 10,
              backgroundColor: t.colors.gray,
              borderRadius: 4,
            }}
          />
        </>
      );
    }

    if (device === "browser") {
      // URL bar with dots
      return (
        <div
          style={{
            position: "absolute",
            top: 0,
            left: 0,
            right: 0,
            height: 44,
            backgroundColor: "#2A2A2A",
            borderRadius: "12px 12px 0 0",
            display: "flex",
            alignItems: "center",
            paddingLeft: 16,
            gap: 8,
            zIndex: 2,
          }}
        >
          {/* Traffic light dots */}
          {["#FF5F57", "#FFBD2E", "#28C840"].map((color, i) => (
            <div
              key={i}
              style={{
                width: 12,
                height: 12,
                borderRadius: 6,
                backgroundColor: color,
              }}
            />
          ))}
          {/* URL bar */}
          <div
            style={{
              flex: 1,
              marginLeft: 12,
              marginRight: 16,
              height: 24,
              backgroundColor: "#3A3A3A",
              borderRadius: 6,
            }}
          />
        </div>
      );
    }

    return null;
  };

  const contentTopOffset =
    device === "browser" ? 44 : device === "phone" ? 32 : 0;

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
        gap: 32,
        padding: "0 60px",
        overflow: "hidden",
        transform: `translateY(${exitTranslateY}px)`,
      }}
    >
      {/* Title above frame */}
      {title && (
        <div
          style={{
            fontFamily,
            fontSize: 36,
            fontWeight: 700,
            color: t.colors.text,
            opacity: titleOpacity,
            textAlign: "center",
            paddingLeft: 40,
          paddingRight: 40,
          }}
        >
          {title}
        </div>
      )}

      {/* Device frame wrapper */}
      <div
        style={{
          position: "relative",
          transform: `scale(${frameScale})`,
          opacity: frameOpacity,
        }}
      >
        {/* Outer frame */}
        <div
          style={{
            width: dims.width,
            height: dims.height,
            borderRadius: dims.borderRadius,
            backgroundColor: "#2A2A2A",
            border: `3px solid #3A3A3A`,
            position: "relative",
            overflow: "visible",
          }}
        >
          {/* Device chrome */}
          {renderDeviceChrome()}

          {/* Inner screen area */}
          <div
            style={{
              position: "absolute",
              top: contentTopOffset,
              left: 0,
              right: 0,
              bottom: 0,
              borderRadius:
                device === "phone"
                  ? `0 0 ${dims.borderRadius - 3}px ${dims.borderRadius - 3}px`
                  : device === "browser"
                  ? "0 0 12px 12px"
                  : dims.borderRadius - 3,
              backgroundColor: t.colors.bgCard,
              opacity: screenOpacity,
              overflow: "hidden",
              padding: 20,
              display: "flex",
              flexDirection: "column",
              gap: 4,
            }}
          >
            {/* Lines of text */}
            {lines.map((line, lineIdx) => {
              const isHighlight = highlightLine === lineIdx;
              return (
                <div
                  key={lineIdx}
                  style={{
                    backgroundColor: isHighlight
                      ? `${t.colors.accent}33`
                      : "transparent",
                    borderRadius: 4,
                    padding: "2px 6px",
                  }}
                >
                  <span
                    style={{
                      fontFamily: monoFamily,
                      fontSize: 20,
                      color: isHighlight ? t.colors.text : t.colors.gray,
                      whiteSpace: "pre",
                      lineHeight: 1.6,
                    }}
                  >
                    {renderedLines[lineIdx]}
                  </span>
                  {/* Blinking cursor on active line */}
                  {renderedLines[lineIdx].length < line.length && (
                    <span
                      style={{
                        fontFamily: monoFamily,
                        fontSize: 20,
                        color: t.colors.accent,
                        opacity: Math.round(frame / 8) % 2 === 0 ? 1 : 0,
                      }}
                    >
                      |
                    </span>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
