import React from "react";
import { AbsoluteFill } from "remotion";
import { AnimatedList } from "../../components/AnimatedList";
import { theme } from "../../style/theme";

const CASES = [
  { icon: "👤", text: "Solo developer bez DevOps", subtext: "konfiguracja środowisk w kwadrans, nie w godziny" },
  { icon: "🔍", text: "Code review przed deployem", subtext: "wyłapuje oczywiste błędy zanim trafią na produkcję" },
  { icon: "🏢", text: "Konfiguracja wielu środowisk", subtext: "dev / staging / produkcja — spójne, parametryzowalne" },
  { icon: "🚀", text: "Onboarding nowych projektów", subtext: "nowy serwer gotowy w 15 minut zamiast 2 godzin" },
];

export const WhenToUse: React.FC = () => {
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
        marginBottom: 8,
      }}>
        Kiedy ma sens?
      </div>

      <AnimatedList items={CASES} startFrame={20} itemDelay={30} color={theme.colors.white} />
    </AbsoluteFill>
  );
};
