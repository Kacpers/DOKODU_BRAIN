import React from "react";
import { AbsoluteFill } from "remotion";
import { AnimatedList } from "../../components/AnimatedList";
import { theme } from "../../style/theme";

const FEATURES = [
  { icon: "📁", text: "Czyta i zapisuje pliki", subtext: "pełny dostęp do systemu plików" },
  { icon: "⚡", text: "Wykonuje komendy shell", subtext: "ls, git, docker, npm — cokolwiek" },
  { icon: "🌐", text: "Przeszukuje web", subtext: "docs, Stack Overflow, GitHub" },
  { icon: "🧠", text: "1 000 000 tokenów kontekstu", subtext: "cały projekt w jednym prompcie" },
];

export const FeaturesList: React.FC = () => {
  return (
    <AbsoluteFill style={{
      backgroundColor: theme.colors.bg,
      display: "flex",
      flexDirection: "column",
      justifyContent: "center",
      padding: "0 160px",
      gap: 48,
    }}>
      <div style={{
        fontFamily: theme.fonts.ui,
        fontSize: 52,
        fontWeight: 700,
        color: theme.colors.white,
        marginBottom: 16,
      }}>
        Co potrafi Gemini CLI?
      </div>

      <AnimatedList items={FEATURES} startFrame={20} itemDelay={25} />
    </AbsoluteFill>
  );
};
