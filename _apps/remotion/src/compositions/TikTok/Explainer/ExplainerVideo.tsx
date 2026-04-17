import React from "react";
import { Series, useVideoConfig } from "remotion";
import { KineticText } from "./scenes/KineticText";
import { SlideCard } from "./scenes/SlideCard";
import { ScreenMockup } from "./scenes/ScreenMockup";
import { StatCounter } from "./scenes/StatCounter";
import { VSCompare } from "./scenes/VSCompare";
import { CTACard } from "./scenes/CTACard";
import { TransitionWrapper } from "./transitions/TransitionWrapper";

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

export const ExplainerVideo: React.FC<ExplainerVideoProps> = ({ scenes }) => {
  const { fps } = useVideoConfig();

  return (
    <Series>
      {scenes.map((scene, i) => {
        const { type, duration, transition, ...sceneProps } = scene;
        const SceneComponent = SCENES[type];

        if (!SceneComponent) {
          console.warn(`Unknown scene type: ${type}`);
          return null;
        }

        const durationSecs = duration || DEFAULT_DURATIONS[type] || 4;
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
  );
};

export const calculateExplainerMetadata = ({ props }: { props: ExplainerVideoProps }) => {
  const fps = 30;
  const totalFrames = props.scenes.reduce((sum, scene) => {
    const dur = scene.duration || DEFAULT_DURATIONS[scene.type] || 4;
    return sum + dur * fps;
  }, 0);
  return { durationInFrames: totalFrames, fps, width: 1080, height: 1920 };
};
