import React from "react";
import { AbsoluteFill, Series, useVideoConfig } from "remotion";
import { KineticText } from "./scenes/KineticText";
import { SlideCard } from "./scenes/SlideCard";
import { ScreenMockup } from "./scenes/ScreenMockup";
import { StatCounter } from "./scenes/StatCounter";
import { VSCompare } from "./scenes/VSCompare";
import { CTACard } from "./scenes/CTACard";
import { TransitionWrapper } from "./transitions/TransitionWrapper";
import { GradientMesh } from "./backgrounds/GradientMesh";
import { LogoWatermark } from "./overlays/LogoWatermark";
import { ProgressBar } from "./overlays/ProgressBar";

interface SceneConfig {
  type: "KineticText" | "SlideCard" | "ScreenMockup" | "StatCounter" | "VSCompare" | "CTACard";
  duration?: number;
  transition?: "glitch" | "swipeUp" | "zoom" | "cut" | "dissolve";
  [key: string]: any;
}

export interface ExplainerVideoProps {
  scenes: SceneConfig[];
}

const SCENES: Record<string, React.FC<any>> = {
  KineticText,
  SlideCard,
  ScreenMockup,
  StatCounter,
  VSCompare,
  CTACard,
};

const DEFAULT_DURATIONS: Record<string, number> = {
  KineticText: 3,
  SlideCard: 5,
  ScreenMockup: 6,
  StatCounter: 4,
  VSCompare: 7,
  CTACard: 3,
};

const TRANSITION_ROTATION = ["swipeUp", "zoom", "dissolve", "glitch", "cut"] as const;

/**
 * Smart duration — adjusts default time based on text density in the scene.
 * More text = more reading time. Ensures minimum readability.
 */
function smartDuration(scene: SceneConfig): number {
  if (scene.duration) return scene.duration; // explicit override always wins

  const base = DEFAULT_DURATIONS[scene.type] || 4;

  // Count total text characters in the scene
  let charCount = 0;
  const countText = (val: any) => {
    if (typeof val === "string") charCount += val.length;
    if (Array.isArray(val)) val.forEach(countText);
    if (val && typeof val === "object" && !Array.isArray(val)) {
      Object.values(val).forEach(countText);
    }
  };

  const { type, duration, transition, ...props } = scene;
  countText(props);

  // ~15 chars/second comfortable reading speed on mobile
  const readingTime = charCount / 15;

  // Use whichever is longer: base duration or reading time + 1s buffer
  return Math.max(base, Math.ceil(readingTime + 1));
}

export const ExplainerVideo: React.FC<ExplainerVideoProps> = ({ scenes }) => {
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill>
      {/* Layer 1: Animated background */}
      <GradientMesh />

      {/* Layer 2: Scenes with safe zone padding */}
      <AbsoluteFill
        style={{
          // Safe zone: keep content away from TikTok UI
          paddingTop: 160,
          paddingBottom: 320,
          paddingLeft: 40,
          paddingRight: 100,
        }}
      >
        <AbsoluteFill
          style={{
            position: "relative",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <Series>
            {scenes.map((scene, i) => {
              const { type, duration, transition, ...sceneProps } = scene;
              const SceneComponent = SCENES[type];

              if (!SceneComponent) {
                console.warn(`Unknown scene type: ${type}`);
                return null;
              }

              const durationSecs = smartDuration(scene);
              const durationInFrames = durationSecs * fps;
              const transitionType = transition || TRANSITION_ROTATION[i % TRANSITION_ROTATION.length];

              return (
                <Series.Sequence key={i} durationInFrames={durationInFrames}>
                  <TransitionWrapper type={transitionType}>
                    <SceneComponent {...sceneProps} />
                  </TransitionWrapper>
                </Series.Sequence>
              );
            })}
          </Series>
        </AbsoluteFill>
      </AbsoluteFill>

      {/* Layer 3: Persistent overlays (always on top) */}
      <LogoWatermark />
      <ProgressBar />
    </AbsoluteFill>
  );
};

export const calculateExplainerMetadata = ({ props }: { props: ExplainerVideoProps }) => {
  const fps = 30;
  const totalFrames = props.scenes.reduce((sum, scene) => {
    const dur = smartDuration(scene);
    return sum + dur * fps;
  }, 0);
  return { durationInFrames: totalFrames, fps, width: 1080, height: 1920 };
};
