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
      bg: "bg-amber-50 border-amber-200",
      badge: "bg-amber-100 text-amber-700",
      label: "Niska pewnosc",
    };
  }
  if (field.confidence === "medium") {
    return {
      bg: "bg-blue-50 border-blue-200",
      badge: "bg-blue-100 text-blue-700",
      label: "Srednia pewnosc",
    };
  }
  return {
    bg: "bg-green-50 border-green-200",
    badge: "bg-green-100 text-green-700",
    label: "Pewne",
  };
}

export default function FieldPreview({
  fields,
  totalFields,
  filledFields,
}: FieldPreviewProps) {
  const highCount = fields.filter((f) => f.confidence === "high").length;
  const mediumCount = fields.filter((f) => f.confidence === "medium").length;
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
        {highCount > 0 && (
          <span className="inline-flex items-center gap-1 px-2 py-1 rounded bg-green-100 text-green-700">
            {highCount} pewnych
          </span>
        )}
        {mediumCount > 0 && (
          <span className="inline-flex items-center gap-1 px-2 py-1 rounded bg-blue-100 text-blue-700">
            {mediumCount} srednich
          </span>
        )}
        {lowCount > 0 && (
          <span className="inline-flex items-center gap-1 px-2 py-1 rounded bg-amber-100 text-amber-700">
            {lowCount} niepewnych
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
                  {style.label}
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
