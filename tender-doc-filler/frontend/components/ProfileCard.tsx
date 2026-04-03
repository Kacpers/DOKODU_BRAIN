"use client";

import { useState } from "react";
import { CompanyProfile, updateProfile } from "@/lib/api";

interface ProfileCardProps {
  profile: CompanyProfile;
  onUpdate: (profile: CompanyProfile) => void;
}

const FIELD_LABELS: Record<keyof CompanyProfile, string> = {
  nazwa_firmy: "Nazwa firmy",
  nip: "NIP",
  regon: "REGON",
  krs: "KRS",
  adres: "Adres siedziby",
  adres_korespondencyjny: "Adres korespondencyjny",
  email: "Email",
  telefon: "Telefon",
  osoba_kontaktowa: "Osoba kontaktowa",
  stanowisko: "Stanowisko",
  status_przedsiebiorcy: "Status przedsiebiorcy",
  miejscowosc: "Miejscowosc",
};

export default function ProfileCard({ profile, onUpdate }: ProfileCardProps) {
  const [expanded, setExpanded] = useState(false);
  const [form, setForm] = useState<CompanyProfile>(profile);
  const [saving, setSaving] = useState(false);

  const handleSave = async () => {
    setSaving(true);
    try {
      const updated = await updateProfile(form);
      onUpdate(updated);
    } catch {
      alert("Blad zapisu profilu");
    } finally {
      setSaving(false);
    }
  };

  const filledCount = Object.values(profile).filter(
    (v) => v && v.trim() !== ""
  ).length;

  return (
    <div className="rounded-lg border border-gray-200 bg-white overflow-hidden">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center justify-between px-4 py-3 hover:bg-gray-50 transition-colors"
      >
        <div className="flex items-center gap-2">
          <svg
            className={`w-4 h-4 text-gray-400 transition-transform ${
              expanded ? "rotate-90" : ""
            }`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 5l7 7-7 7"
            />
          </svg>
          <span className="font-medium text-gray-700">Profil firmy</span>
        </div>
        <span className="text-xs text-gray-400">
          {filledCount}/{Object.keys(FIELD_LABELS).length} pol wypelnionych
        </span>
      </button>

      {expanded && (
        <div className="px-4 pb-4 border-t border-gray-100">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-3">
            {(Object.keys(FIELD_LABELS) as (keyof CompanyProfile)[]).map(
              (key) => (
                <div key={key}>
                  <label className="block text-xs font-medium text-gray-500 mb-1">
                    {FIELD_LABELS[key]}
                  </label>
                  <input
                    type="text"
                    value={form[key]}
                    onChange={(e) =>
                      setForm({ ...form, [key]: e.target.value })
                    }
                    className="w-full rounded border border-gray-200 px-3 py-1.5 text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              )
            )}
          </div>
          <div className="mt-4 flex justify-end">
            <button
              onClick={handleSave}
              disabled={saving}
              className="px-4 py-2 bg-green-600 text-white text-sm font-medium rounded-lg hover:bg-green-700 disabled:opacity-50 transition-colors"
            >
              {saving ? "Zapisywanie..." : "Zapisz profil"}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
