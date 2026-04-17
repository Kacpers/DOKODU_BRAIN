import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import { loadFont } from "@remotion/google-fonts/PlusJakartaSans";
import { tiktokTheme as t } from "../../../../style/tiktok-theme";

const { fontFamily } = loadFont();

const WORD_STAGGER = 4; // frames between each word
const EXIT_FRAMES = 10;

interface KineticTextProps {
  text: string;
  emphasis?: string;
  fontSize?: number;
}

/** Parsed line structure: each line is an array of word strings */
function parseLines(text: string): string[][] {
  // Handle both real newlines and literal \n from JSON props
  const normalized = text.replace(/\\n/g, "\n");
  return normalized.split("\n").map((line) =>
    line.split(" ").filter((w) => w.length > 0)
  );
}

/** Strip trailing punctuation for emphasis matching */
function stripPunct(word: string): string {
  return word.replace(/[.,!?;:]+$/, "");
}

export const KineticText: React.FC<KineticTextProps> = ({
  text,
  emphasis,
  fontSize = 72,
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames, fps } = useVideoConfig();

  const lines = parseLines(text);

  const exitStart = durationInFrames - EXIT_FRAMES;
  const exitProgress = interpolate(
    frame,
    [exitStart, durationInFrames],
    [0, 1],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );
  const isExiting = frame >= exitStart;

  // Build flat list of (lineIdx, wordIdx, globalIdx) for stagger calculation
  let globalIdx = 0;
  const indexMap: number[][] = lines.map((lineWords) =>
    lineWords.map(() => globalIdx++)
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: t.colors.bg,
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
        gap: fontSize * 0.25,
        padding: "0 60px",
        overflow: "hidden",
      }}
    >
      {lines.map((lineWords, lineIdx) => (
        <div
          key={lineIdx}
          style={{
            display: "flex",
            flexDirection: "row",
            flexWrap: "wrap",
            justifyContent: "center",
            alignItems: "center",
            gap: `0 ${fontSize * 0.28}px`,
            width: "100%",
          }}
        >
          {lineWords.map((word, wordIdx) => {
            const idx = indexMap[lineIdx][wordIdx];
            const isEmphasis =
              emphasis !== undefined &&
              stripPunct(word) === stripPunct(emphasis);

            const enterSpring = spring({
              frame: frame - idx * WORD_STAGGER,
              fps,
              config: { damping: 12 },
            });

            const translateY = interpolate(enterSpring, [0, 1], [40, 0]);
            const enterOpacity = Math.max(0, Math.min(1, enterSpring));

            // Emphasis scale pulse: sin wave period ~20 frames, activates after word appears
            const emphasisScale =
              isEmphasis && enterSpring > 0.9
                ? 1 + 0.15 * Math.abs(Math.sin((frame * Math.PI) / 20))
                : 1;

            const exitScale = isExiting ? 1 - exitProgress * 0.2 : 1;
            const exitOpacity = isExiting ? 1 - exitProgress : 1;

            return (
              <span
                key={wordIdx}
                style={{
                  fontFamily,
                  fontSize,
                  fontWeight: 700,
                  color: isEmphasis ? t.colors.accent : t.colors.text,
                  transform: `translateY(${translateY}px) scale(${emphasisScale * exitScale})`,
                  opacity: enterOpacity * exitOpacity,
                  display: "inline-block",
                  transformOrigin: "center center",
                  lineHeight: 1.2,
                  whiteSpace: "pre",
                }}
              >
                {word}
              </span>
            );
          })}
        </div>
      ))}
    </AbsoluteFill>
  );
};
