import { apiFetch } from "../api";

export async function exportDataset(datasetId) {
  const res = await apiFetch(`/export/${datasetId}`);

  if (!res.ok) {
    throw new Error("Failed to export dataset");
  }

  return res.json();
}
