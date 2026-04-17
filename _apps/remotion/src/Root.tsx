import React from "react";
import { Composition } from "remotion";
import { theme } from "./style/theme";
import { tiktokTheme } from "./style/tiktok-theme";

// YouTube compositions
import { Opener } from "./compositions/YT002/01_Opener";
import { TitleCardComp } from "./compositions/YT002/02_TitleCard";
import { ReactLoop } from "./compositions/YT002/03_ReactLoop";
import { FeaturesList } from "./compositions/YT002/04_FeaturesList";
import { PromptStructure } from "./compositions/YT002/05b_PromptStructure";
import { InstallSummary } from "./compositions/YT002/05_InstallSummary";
import { TimeComparison } from "./compositions/YT002/06_TimeComparison";
import { Demo2Flow } from "./compositions/YT002/07_Demo2Flow";
import { WhenToUse } from "./compositions/YT002/08_WhenToUse";
import { EndScreen } from "./compositions/YT002/09_EndScreen";
import { Thumbnail } from "./compositions/YT002/Thumbnail";

// TikTok compositions
import { TikTokIntro } from "./compositions/TikTok/Intro";
import { TikTokCTA } from "./compositions/TikTok/CTA";
import { TopicCard } from "./compositions/TikTok/TopicCard";

// TikTok Explainer compositions
import { ExplainerVideo, calculateExplainerMetadata } from "./compositions/TikTok/Explainer/ExplainerVideo";
import { Lookbook } from "./compositions/TikTok/Explainer/Lookbook";

export const RemotionRoot: React.FC = () => {
  const base = { width: theme.width, height: theme.height, fps: theme.fps };
  const tikTokBase = {
    width: tiktokTheme.width,
    height: tiktokTheme.height,
    fps: tiktokTheme.fps,
  };

  return (
    <>
      {/* ─── YouTube ─── */}
      <Composition id="YT002-01-Opener"      component={Opener}         durationInFrames={150} {...base} />
      <Composition id="YT002-02-TitleCard"   component={TitleCardComp}  durationInFrames={90}  {...base} />
      <Composition id="YT002-03-ReactLoop"   component={ReactLoop}      durationInFrames={150} {...base} />
      <Composition id="YT002-04-Features"    component={FeaturesList}   durationInFrames={150} {...base} />
      <Composition id="YT002-05b-PromptStr"  component={PromptStructure} durationInFrames={160} {...base} />
      <Composition id="YT002-05-Install"     component={InstallSummary} durationInFrames={120} {...base} />
      <Composition id="YT002-06-TimeComp"    component={TimeComparison} durationInFrames={120} {...base} />
      <Composition id="YT002-07-Demo2Flow"   component={Demo2Flow}      durationInFrames={150} {...base} />
      <Composition id="YT002-08-WhenToUse"   component={WhenToUse}      durationInFrames={180} {...base} />
      <Composition id="YT002-09-EndScreen"   component={EndScreen}      durationInFrames={150} {...base} />
      <Composition id="YT002-Thumbnail"      component={Thumbnail}      durationInFrames={1}   width={1280} height={720} fps={30} />

      {/* ─── TikTok ─── */}
      <Composition id="TikTok-Intro"     component={TikTokIntro} durationInFrames={45}  {...tikTokBase} />
      <Composition id="TikTok-CTA"       component={TikTokCTA}   durationInFrames={75}  {...tikTokBase} />
      <Composition
        id="TikTok-TopicCard"
        component={TopicCard}
        durationInFrames={75}
        {...tikTokBase}
        defaultProps={{ topic: "Temat TikToka", category: "AI Tips" }}
      />

      {/* ─── TikTok Explainer ─── */}
      <Composition
        id="TikTok-Explainer"
        component={ExplainerVideo as any}
        calculateMetadata={calculateExplainerMetadata as any}
        {...tikTokBase}
        defaultProps={{
          scenes: [
            { type: "KineticText", text: "Który AI\nwybrać?", emphasis: "wybrać", duration: 3 },
            { type: "VSCompare", left: { title: "ChatGPT", points: ["Obrazy", "Browsing"] }, right: { title: "Claude", points: ["Dokumenty", "Kod"] }, duration: 7 },
            { type: "CTACard", duration: 3 },
          ],
        }}
      />
      <Composition
        id="TikTok-Lookbook"
        component={Lookbook}
        durationInFrames={2850}
        {...tikTokBase}
      />
    </>
  );
};
