import React from "react";
import { AbsoluteFill, Series, useCurrentFrame, interpolate } from "remotion";
import { loadFont } from "@remotion/google-fonts/PlusJakartaSans";
import { tiktokTheme as t } from "../../../style/tiktok-theme";

import { KineticText } from "./scenes/KineticText";
import { SlideCard } from "./scenes/SlideCard";
import { StatCounter } from "./scenes/StatCounter";
import { VSCompare } from "./scenes/VSCompare";
import { ScreenMockup } from "./scenes/ScreenMockup";
import { CTACard } from "./scenes/CTACard";
import { TransitionWrapper } from "./transitions/TransitionWrapper";
import { ExplainerVideo } from "./ExplainerVideo";

const { fontFamily } = loadFont();

/**
 * SectionLabel — shows a title card between sections
 */
const SectionLabel: React.FC<{ label: string; sub?: string }> = ({
  label,
  sub,
}) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 10, 35, 45], [0, 1, 1, 0], {
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
          fontSize: 28,
          color: t.colors.accent,
          letterSpacing: 3,
          textTransform: "uppercase",
          marginBottom: 12,
        }}
      >
        {label}
      </div>
      {sub && (
        <div
          style={{ fontFamily, fontSize: 20, color: t.colors.gray }}
        >
          {sub}
        </div>
      )}
    </AbsoluteFill>
  );
};

/**
 * Lookbook — demo reel of all explainer scenes + transitions
 *
 * Structure:
 *  1. Title card
 *  2. KineticText × 3 variants (3 transitions)
 *  3. SlideCard × 2 variants
 *  4. StatCounter × 2 variants
 *  5. VSCompare × 1 variant
 *  6. ScreenMockup × 2 variants (phone + browser)
 *  7. CTACard × 1
 *  8. Full example explainer (~27s)
 *
 *  Total: ~90s
 */
export const Lookbook: React.FC = () => {
  const fps = t.fps;

  // Full example scenario for the finale
  const exampleScenes = [
    {
      type: "KineticText" as const,
      text: "Który AI\nwybrać?",
      emphasis: "wybrać",
      duration: 3,
      transition: "glitch" as const,
    },
    {
      type: "VSCompare" as const,
      left: {
        title: "ChatGPT",
        points: ["Obrazy i DALL-E", "Browsing", "Popularność"],
      },
      right: {
        title: "Claude",
        points: ["Dokumenty", "Kod i analiza", "Długi kontekst"],
      },
      duration: 7,
      transition: "swipeUp" as const,
    },
    {
      type: "SlideCard" as const,
      title: "Gemini",
      icon: "🔍",
      bullets: [
        "Google ekosystem",
        "Duży kontekst",
        "Integracja z Workspace",
      ],
      duration: 5,
      transition: "zoom" as const,
    },
    {
      type: "StatCounter" as const,
      value: 3,
      label: "narzędzia, 3 różne zastosowania",
      duration: 4,
      transition: "dissolve" as const,
    },
    {
      type: "KineticText" as const,
      text: "Nie który lepszy.\nKtóry do CZEGO.",
      emphasis: "CZEGO",
      duration: 4,
      transition: "glitch" as const,
    },
    {
      type: "CTACard" as const,
      duration: 3,
      transition: "dissolve" as const,
    },
  ];

  return (
    <Series>
      {/* ─── Title ─── */}
      <Series.Sequence durationInFrames={fps * 2}>
        <SectionLabel label="Lookbook" sub="Dokodu TikTok Explainer Scenes" />
      </Series.Sequence>

      {/* ─── Section 1: KineticText ─── */}
      <Series.Sequence durationInFrames={fps * 1.5}>
        <SectionLabel label="KineticText" sub="3 warianty" />
      </Series.Sequence>
      <Series.Sequence durationInFrames={fps * 3}>
        <TransitionWrapper type="swipeUp">
          <KineticText
            text="AI zmienia\nzasady gry"
            emphasis="zasady"
          />
        </TransitionWrapper>
      </Series.Sequence>
      <Series.Sequence durationInFrames={fps * 3}>
        <TransitionWrapper type="glitch">
          <KineticText
            text="Przestań pisać\ndługie prompty"
            emphasis="Przestań"
          />
        </TransitionWrapper>
      </Series.Sequence>
      <Series.Sequence durationInFrames={fps * 3}>
        <TransitionWrapper type="zoom">
          <KineticText
            text="6 godzin pracy.\n30 sekund."
            emphasis="30"
            fontSize={80}
          />
        </TransitionWrapper>
      </Series.Sequence>

      {/* ─── Section 2: SlideCard ─── */}
      <Series.Sequence durationInFrames={fps * 1.5}>
        <SectionLabel label="SlideCard" sub="2 warianty" />
      </Series.Sequence>
      <Series.Sequence durationInFrames={fps * 5}>
        <TransitionWrapper type="swipeUp">
          <SlideCard
            title="3 błędy wdrożeń AI"
            icon="⚠️"
            bullets={[
              "Brak zdefiniowanego problemu",
              "Szkolenie bez follow-up",
              "Narzędzie zamiast procesu",
            ]}
          />
        </TransitionWrapper>
      </Series.Sequence>
      <Series.Sequence durationInFrames={fps * 5}>
        <TransitionWrapper type="dissolve">
          <SlideCard
            title="Co robi Dokodu?"
            icon="🚀"
            bullets={[
              "Audyt procesów",
              "Wdrożenie n8n + AI",
              "Szkolenia zespołu",
              "Wsparcie 30 dni",
            ]}
          />
        </TransitionWrapper>
      </Series.Sequence>

      {/* ─── Section 3: StatCounter ─── */}
      <Series.Sequence durationInFrames={fps * 1.5}>
        <SectionLabel label="StatCounter" sub="2 warianty" />
      </Series.Sequence>
      <Series.Sequence durationInFrames={fps * 4}>
        <TransitionWrapper type="zoom">
          <StatCounter value={200} label="maili dziennie" suffix="" />
        </TransitionWrapper>
      </Series.Sequence>
      <Series.Sequence durationInFrames={fps * 4}>
        <TransitionWrapper type="glitch">
          <StatCounter value={6} label="godzin oszczędności tygodniowo" suffix="h" />
        </TransitionWrapper>
      </Series.Sequence>

      {/* ─── Section 4: VSCompare ─── */}
      <Series.Sequence durationInFrames={fps * 1.5}>
        <SectionLabel label="VSCompare" sub="1 wariant" />
      </Series.Sequence>
      <Series.Sequence durationInFrames={fps * 7}>
        <TransitionWrapper type="swipeUp">
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
        </TransitionWrapper>
      </Series.Sequence>

      {/* ─── Section 5: ScreenMockup ─── */}
      <Series.Sequence durationInFrames={fps * 1.5}>
        <SectionLabel label="ScreenMockup" sub="phone + browser" />
      </Series.Sequence>
      <Series.Sequence durationInFrames={fps * 6}>
        <TransitionWrapper type="dissolve">
          <ScreenMockup
            device="phone"
            title="Slack Alert"
            lines={[
              "🔔 Deadline za 24h",
              "Projekt: Raport Q2",
              "Klient: FirmaCorp",
              "Status: Brak odpowiedzi",
            ]}
            highlightLine={3}
          />
        </TransitionWrapper>
      </Series.Sequence>
      <Series.Sequence durationInFrames={fps * 6}>
        <TransitionWrapper type="zoom">
          <ScreenMockup
            device="browser"
            title="n8n Workflow"
            lines={[
              "1. Trigger: Nowy email",
              "2. AI: Analizuj treść",
              "3. CRM: Aktualizuj lead",
              "4. Slack: Powiadom handlowca",
              "5. Calendar: Zaplanuj follow-up",
            ]}
            highlightLine={1}
          />
        </TransitionWrapper>
      </Series.Sequence>

      {/* ─── Section 6: CTACard ─── */}
      <Series.Sequence durationInFrames={fps * 1.5}>
        <SectionLabel label="CTACard" />
      </Series.Sequence>
      <Series.Sequence durationInFrames={fps * 3}>
        <TransitionWrapper type="dissolve">
          <CTACard />
        </TransitionWrapper>
      </Series.Sequence>

      {/* ─── Section 7: Full Example ─── */}
      <Series.Sequence durationInFrames={fps * 2}>
        <SectionLabel
          label="Pełny Explainer"
          sub="ChatGPT vs Claude vs Gemini"
        />
      </Series.Sequence>
      <Series.Sequence
        durationInFrames={exampleScenes.reduce(
          (sum, s) => sum + (s.duration || 4) * fps,
          0
        )}
      >
        <ExplainerVideo scenes={exampleScenes} />
      </Series.Sequence>
    </Series>
  );
};
