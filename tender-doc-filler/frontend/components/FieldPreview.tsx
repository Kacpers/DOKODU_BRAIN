"use client";

import { FieldResult } from "@/lib/api";

interface FieldPreviewProps {
  fields: FieldResult[];
  totalFields: number;
  filledFields: number;
}

function getFieldStyle(field: FieldResult) {
  if (field.confidence === "low") {
    return {
      bg: "bg-red-50 border-red-200",
      badge: "bg-red-100 text-red-700",
      icon: "\uD83D\uDD34",
      label: "Niska pewnosc",
    };
  }
  if (field.source === "rule") {
    return {
      bg: "bg-green-50 border-green-200",
      badge: "bg-green-100 text-green-700",
      icon: "\uD83D\uDFE2",
      label: "Regula",
    };
  }
  return {
    bg: "bg-blue-50 border-blue-200",
    badge: "bg-blue-100 text-blue-700",
    icon: "\uD83D\uDD35",
    label: "AI",
  };
}

export default function FieldPreview({
  fields,
  totalFields,
  filledFields,
}: FieldPreviewProps) {
  const ruleCount = fields.filter(
    (f) => f.source === "rule" && f.confidence !== "low"
  ).length;
  const aiCount = fields.filter(
    (f) => f.source === "ai" && f.confidence !== "low"
  ).length;
  const lowCount = fields.filter((f) => f.confidence === "low").length;

  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-800">
          Wyniki analizy
        </h3>
        <div className="text-sm text-gray-500">
          Wypelniono {filledFields} z {totalFields} pol
        </div>
      </div>

      <div className="flex gap-3 text-sm">
        {ruleCount > 0 && (
          <span className="inline-flex items-center gap-1 px-2 py-1 rounded bg-green-100 text-green-700">
            {"\uD83D\uDFE2"} {ruleCount} regulowe
          </span>
        )}
        {aiCount > 0 && (
          <span className="inline-flex items-center gap-1 px-2 py-1 rounded bg-blue-100 text-blue-700">
            {"\uD83D\uDD35"} {aiCount} AI
          </span>
        )}
        {lowCount > 0 && (
          <span className="inline-flex items-center gap-1 px-2 py-1 rounded bg-red-100 text-red-700">
            {"\uD83D\uDD34"} {lowCount} niska pewnosc
          </span>
        )}
      </div>

      <div className="flex flex-col gap-2">
        {fields.map((field, i) => {
          const style = getFieldStyle(field);
          return (
            <div
              key={`${field.location_id}-${i}`}
              className={`rounded-lg border p-3 ${style.bg}`}
            >
              <div className="flex items-center justify-between mb-1">
                <span className="font-medium text-sm text-gray-800">
                  {field.label || field.location_id}
                </span>
                <span
                  className={`text-xs px-2 py-0.5 rounded-full ${style.badge}`}
                >
                  {style.icon} {style.label}
                </span>
              </div>
              {field.original_value && (
                <div className="text-xs text-gray-500">
                  Oryginalne: {field.original_value}
                </div>
              )}
              <div className="text-sm text-gray-700 mt-1 font-mono">
                {field.filled_value || "(brak wartosci)"}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
