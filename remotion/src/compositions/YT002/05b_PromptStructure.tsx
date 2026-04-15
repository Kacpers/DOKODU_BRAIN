import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate, spring, useVideoConfig } from "remotion";
import { theme } from "../../style/theme";

const ELEMENTS = [
  {
    num: "01",
    title: "KONTEKST",
    desc: "Co masz, jakie środowisko, jaka wersja",
  },
  {
    num: "02",
    title: "CEL",
    desc: "Co ma powstać — konkretnie, nie ogólnie",
  },
  {
    num: "03",
    title: "OGRANICZENIA",
    desc: "Czego nie robić, jakie konwencje zachować",
  },
  {
    num: "04",
    title: "FORMAT WYJŚCIA",
    desc: "Pliki? Lista? Raport? Powiedz to wprost",
  },
];

const ITEM_DELAY = 28;
const START_FRAME = 18;

export const PromptStructure: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill
      style={{
        backgroundColor: theme.colors.bg,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        padding: "0 140px",
        gap: 32,
      }}
    >
      {/* Nagłówek */}
      <div
        style={{
          fontFamily: theme.fonts.ui,
          fontSize: 44,
          fontWeight: 700,
          color: theme.colors.white,
          marginBottom: 8,
          opacity: interpolate(frame, [0, 14], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          }),
        }}
      >
        Anatomia dobrego promptu
      </div>

      {/* Karty */}
      {ELEMENTS.map((el, i) => {
        const itemStart = START_FRAME + i * ITEM_DELAY;
        const progress = spring({
          frame: frame - itemStart,
          fps,
          config: { damping: 15, stiffness: 130, mass: 0.7 },
        });
        const opacity = interpolate(frame, [itemStart, itemStart + 12], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });
        const translateX = interpolate(progress, [0, 1], [-50, 0]);

        return (
          <div
            key={i}
            style={{
              opacity,
              transform: `translateX(${translateX}px)`,
              display: "flex",
              alignItems: "center",
              gap: 32,
              backgroundColor: theme.colors.bgCard,
              borderRadius: 12,
              padding: "20px 32px",
              borderLeft: `4px solid ${theme.colors.green}`,
            }}
          >
            {/* Numer */}
            <div
              style={{
                fontFamily: theme.fonts.mono,
                fontSize: 36,
                fontWeight: 700,
                color: theme.colors.green,
                minWidth: 52,
                lineHeight: 1,
              }}
            >
              {el.num}
            </div>

            {/* Tekst */}
            <div>
              <div
                style={{
                  fontFamily: theme.fonts.ui,
                  fontSize: 34,
                  fontWeight: 700,
                  color: theme.colors.white,
                  letterSpacing: "0.04em",
                }}
              >
                {el.title}
              </div>
              <div
                style={{
                  fontFamily: theme.fonts.ui,
                  fontSize: 24,
                  color: theme.colors.gray,
                  marginTop: 4,
                }}
              >
                {el.desc}
              </div>
            </div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
