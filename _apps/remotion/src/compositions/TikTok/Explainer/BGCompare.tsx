import React from "react";
import {
  AbsoluteFill,
  Series,
  useCurrentFrame,
  interpolate,
} from "remotion";
import { loadFont } from "@remotion/google-fonts/PlusJakartaSans";
import { tiktokTheme as t } from "../../../style/tiktok-theme";

import { DriftingOrbs } from "./backgrounds/DriftingOrbs";
import { GradientMesh } from "./backgrounds/GradientMesh";
import { TechGrid } from "./backgrounds/TechGrid";
import { KineticText } from "./scenes/KineticText";
import { SlideCard } from "./scenes/SlideCard";
import { StatCounter } from "./scenes/StatCounter";
import { VSCompare } from "./scenes/VSCompare";
import { CTACard } from "./scenes/CTACard";

const { fontFamily } = loadFont();

/** Label between sections */
const Label: React.FC<{ text: string; sub?: string }> = ({ text, sub }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 10, 40, 50], [0, 1, 1, 0], {
    extrapolateRight: "clamp",
  });
  return (
    <AbsoluteFill
      style={{
        backgroundColor: t.colors.bg,
        justifyContent: "center",
        alignItems: "center",
        opacity,
      }}
    >
      <div
        style={{
          fontFamily,
          fontSize: 32,
          fontWeight: 700,
          color: t.colors.accent,
          letterSpacing: 3,
          textTransform: "uppercase",
        }}
      >
        {text}
      </div>
      {sub && (
        <div
          style={{
            fontFamily,
            fontSize: 22,
            color: t.colors.textSecondary,
            marginTop: 12,
          }}
        >
          {sub}
        </div>
      )}
    </AbsoluteFill>
  );
};

/**
 * Wrap a scene with a background.
 * The inner AbsoluteFill uses a CSS trick: scenes set their own bg,
 * but we override it to transparent so the animated BG shows through.
 */
const WithBG: React.FC<{
  BG: React.FC;
  children: React.ReactNode;
}> = ({ BG, children }) => (
  <AbsoluteFill>
    <BG />
    {/* This wrapper makes all child AbsoluteFill backgrounds transparent */}
    <AbsoluteFill
      style={{
        // Override scene backgrounds — CSS custom property approach
        // We wrap children and set the scene bg to transparent via a container
      }}
    >
      <div
        style={{
          position: "absolute",
          inset: 0,
          // This targets the first AbsoluteFill child (the scene root)
          // by setting background on the container to transparent
        }}
      >
        <style
          dangerouslySetInnerHTML={{
            __html: `
              .bg-transparent-scene > div {
                background-color: transparent !important;
                background: transparent !important;
              }
            `,
          }}
        />
        <div className="bg-transparent-scene" style={{ position: "absolute", inset: 0 }}>
          {children}
        </div>
      </div>
    </AbsoluteFill>
  </AbsoluteFill>
);

/**
 * BGCompare — shows same scenes on 3 different backgrounds
 * Total: ~75s
 *
 * Section 1: KineticText on each BG (A, B, C)
 * Section 2: SlideCard on each BG
 * Section 3: StatCounter + VSCompare on best-looking BG combos
 * Section 4: Full mini-explainer on Orbs BG
 */
export const BGCompare: React.FC = () => {
  const fps = t.fps;

  return (
    <Series>
      {/* ─── Intro ─── */}
      <Series.Sequence durationInFrames={fps * 2}>
        <Label text="Background Compare" sub="A: Orbs / B: Gradient / C: Grid" />
      </Series.Sequence>

      {/* ─── KineticText × 3 backgrounds ─── */}
      <Series.Sequence durationInFrames={fps * 1.5}>
        <Label text="A: Drifting Orbs" />
      </Series.Sequence>
      <Series.Sequence durationInFrames={fps * 4}>
        <WithBG BG={DriftingOrbs}>
          <KineticText
            text="AI zmienia\nzasady gry"
            emphasis="zasady"
          />
        </WithBG>
      </Series.Sequence>

      <Series.Sequence durationInFrames={fps * 1.5}>
        <Label text="B: Gradient Mesh" />
      </Series.Sequence>
      <Series.Sequence durationInFrames={fps * 4}>
        <WithBG BG={GradientMesh}>
          <KineticText
            text="AI zmienia\nzasady gry"
            emphasis="zasady"
          />
        </WithBG>
      </Series.Sequence>

      <Series.Sequence durationInFrames={fps * 1.5}>
        <Label text="C: Tech Grid" />
      </Series.Sequence>
      <Series.Sequence durationInFrames={fps * 4}>
        <WithBG BG={TechGrid}>
          <KineticText
            text="AI zmienia\nzasady gry"
            emphasis="zasady"
          />
        </WithBG>
      </Series.Sequence>

      {/* ─── SlideCard × 3 backgrounds ─── */}
      <Series.Sequence durationInFrames={fps * 1.5}>
        <Label text="SlideCard" sub="A: Orbs" />
      </Series.Sequence>
      <Series.Sequence durationInFrames={fps * 5}>
        <WithBG BG={DriftingOrbs}>
          <SlideCard
            title="3 błędy wdrożeń AI"
            icon="⚠️"
            bullets={[
              "Brak zdefiniowanego problemu",
              "Szkolenie bez follow-up",
              "Narzędzie zamiast procesu",
            ]}
          />
        </WithBG>
      </Series.Sequence>

      <Series.Sequence durationInFrames={fps * 1.5}>
        <Label text="SlideCard" sub="B: Gradient" />
      </Series.Sequence>
      <Series.Sequence durationInFrames={fps * 5}>
        <WithBG BG={GradientMesh}>
          <SlideCard
            title="3 błędy wdrożeń AI"
            icon="⚠️"
            bullets={[
              "Brak zdefiniowanego problemu",
              "Szkolenie bez follow-up",
              "Narzędzie zamiast procesu",
            ]}
          />
        </WithBG>
      </Series.Sequence>

      <Series.Sequence durationInFrames={fps * 1.5}>
        <Label text="SlideCard" sub="C: Grid" />
      </Series.Sequence>
      <Series.Sequence durationInFrames={fps * 5}>
        <WithBG BG={TechGrid}>
          <SlideCard
            title="3 błędy wdrożeń AI"
            icon="⚠️"
            bullets={[
              "Brak zdefiniowanego problemu",
              "Szkolenie bez follow-up",
              "Narzędzie zamiast procesu",
            ]}
          />
        </WithBG>
      </Series.Sequence>

      {/* ─── StatCounter on Orbs ─── */}
      <Series.Sequence durationInFrames={fps * 1.5}>
        <Label text="StatCounter" sub="A: Orbs" />
      </Series.Sequence>
      <Series.Sequence durationInFrames={fps * 4}>
        <WithBG BG={DriftingOrbs}>
          <StatCounter value={200} label="maili dziennie" />
        </WithBG>
      </Series.Sequence>

      {/* ─── VSCompare on Gradient ─── */}
      <Series.Sequence durationInFrames={fps * 1.5}>
        <Label text="VSCompare" sub="B: Gradient" />
      </Series.Sequence>
      <Series.Sequence durationInFrames={fps * 7}>
        <WithBG BG={GradientMesh}>
          <VSCompare
            left={{
              title: "Ręcznie",
              points: ["4h dziennie", "Błędy ludzkie", "Nuda"],
              color: t.colors.red,
            }}
            right={{
              title: "Z AI",
              points: ["30 minut", "Spójne wyniki", "Skalowalne"],
            }}
          />
        </WithBG>
      </Series.Sequence>

      {/* ─── CTACard on Grid ─── */}
      <Series.Sequence durationInFrames={fps * 1.5}>
        <Label text="CTACard" sub="C: Grid" />
      </Series.Sequence>
      <Series.Sequence durationInFrames={fps * 3}>
        <WithBG BG={TechGrid}>
          <CTACard />
        </WithBG>
      </Series.Sequence>
    </Series>
  );
};
