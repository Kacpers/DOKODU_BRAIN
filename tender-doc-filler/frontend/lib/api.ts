const API_BASE = "/formularze/api";

export interface FieldResult {
  location_id: string;
  location_type: string;
  label: string;
  original_value: string;
  filled_value: string;
  source: "rule" | "ai";
  confidence: "high" | "medium" | "low";
}

export interface AnalysisResponse {
  document_id: string;
  filename: string;
  mode: string;
  fields: FieldResult[];
  total_fields: number;
  filled_fields: number;
}

export interface CompanyProfile {
  nazwa_firmy: string;
  nip: string;
  regon: string;
  krs: string;
  adres: string;
  adres_korespondencyjny: string;
  email: string;
  telefon: string;
  osoba_kontaktowa: string;
  stanowisko: string;
  status_przedsiebiorcy: string;
  miejscowosc: string;
}

export async function uploadDocument(
  file: File,
  mode: "rule" | "ai" | "hybrid" = "hybrid"
): Promise<AnalysisResponse> {
  const formData = new FormData();
  formData.append("file", file);
  const resp = await fetch(`${API_BASE}/upload?mode=${mode}`, {
    method: "POST",
    body: formData,
  });
  if (!resp.ok) throw new Error((await resp.json()).error);
  return resp.json();
}

export async function getProfile(): Promise<CompanyProfile> {
  const resp = await fetch(`${API_BASE}/profile`);
  return resp.json();
}

export async function updateProfile(
  profile: CompanyProfile
): Promise<CompanyProfile> {
  const resp = await fetch(`${API_BASE}/profile`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(profile),
  });
  return resp.json();
}

export function getDownloadUrl(documentId: string): string {
  return `${API_BASE}/documents/${documentId}/download`;
}
