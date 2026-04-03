"use client";

export type Mode = "rule" | "ai" | "hybrid";

interface ModeToggleProps {
  mode: Mode;
  onChange: (mode: Mode) => void;
}

const MODES: { value: Mode; label: string; description: string }[] = [
  {
    value: "rule",
    label: "Regulowy",
    description: "Regex + tabele, szybki, 100% pewny",
  },
  {
    value: "ai",
    label: "AI",
    description: "Claude rozpoznaje pola z tresci",
  },
  {
    value: "hybrid",
    label: "Hybrydowy",
    description: "Reguly + AI fallback",
  },
];

export default function ModeToggle({ mode, onChange }: ModeToggleProps) {
  return (
    <div className="flex flex-col gap-2">
      <h3 className="text-sm font-semibold text-gray-600 uppercase tracking-wide">
        Tryb analizy
      </h3>
      <div className="flex gap-2">
        {MODES.map((m) => (
          <button
            key={m.value}
            onClick={() => onChange(m.value)}
            className={`flex-1 rounded-lg px-4 py-3 text-left transition-colors border ${
              mode === m.value
                ? "bg-blue-600 text-white border-blue-600"
                : "bg-white text-gray-700 border-gray-200 hover:border-blue-300"
            }`}
          >
            <div className="font-medium text-sm">{m.label}</div>
            <div
              className={`text-xs mt-1 ${
                mode === m.value ? "text-blue-100" : "text-gray-500"
              }`}
            >
              {m.description}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
