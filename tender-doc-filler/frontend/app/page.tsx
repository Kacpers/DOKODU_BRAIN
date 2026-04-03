"use client";

import { useCallback, useEffect, useState } from "react";
import Upload from "@/components/Upload";
import FieldPreview from "@/components/FieldPreview";
import ProfileCard from "@/components/ProfileCard";
import {
  AnalysisResponse,
  CompanyProfile,
  getProfile,
  uploadDocument,
  getDownloadUrl,
} from "@/lib/api";

const EMPTY_PROFILE: CompanyProfile = {
  nazwa_firmy: "",
  nip: "",
  regon: "",
  krs: "",
  adres: "",
  adres_korespondencyjny: "",
  email: "",
  telefon: "",
  osoba_kontaktowa: "",
  stanowisko: "",
  status_przedsiebiorcy: "",
  miejscowosc: "",
};

export default function Home() {
  const [profile, setProfile] = useState<CompanyProfile>(EMPTY_PROFILE);
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getProfile()
      .then(setProfile)
      .catch(() => {});
  }, []);

  const handleUpload = useCallback(
    async (file: File) => {
      setLoading(true);
      setError(null);
      setResult(null);
      try {
        const res = await uploadDocument(file);
        setResult(res);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Wystapil blad");
      } finally {
        setLoading(false);
      }
    },
    []
  );

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <div className="flex-1 max-w-3xl mx-auto w-full px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            TenderScope Document Filler
          </h1>
          <p className="text-gray-500 mt-2">
            Automatyczne uzupelnianie danych wykonawcy w dokumentach
            przetargowych
          </p>
        </div>

        <div className="flex flex-col gap-6">
          <ProfileCard profile={profile} onUpdate={setProfile} />

          <Upload loading={loading} onUpload={handleUpload} />

          {error && (
            <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-red-700 text-sm">
              {error}
            </div>
          )}

          {result && (
            <>
              <FieldPreview
                fields={result.fields}
                totalFields={result.total_fields}
                filledFields={result.filled_fields}
              />

              <a
                href={getDownloadUrl(result.document_id)}
                download
                className="inline-flex items-center justify-center gap-2 rounded-lg bg-blue-600 px-6 py-3 text-white font-medium hover:bg-blue-700 transition-colors"
              >
                <svg
                  className="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
                Pobierz wypelniony dokument
              </a>
            </>
          )}
        </div>
      </div>

      <footer className="text-center text-gray-400 text-xs py-4 border-t border-gray-100">
        Demo MVP — Dokodu x TenderScope
      </footer>
    </div>
  );
}
