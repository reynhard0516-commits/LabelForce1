import { apiFetch } from "../api";

export async function getLabels(datasetId) {
  const res = await apiFetch(`/datasets/${datasetId}/labels`);
  if (!res.ok) throw new Error("Failed to load labels");
  return res.json();
}

export async function createLabel(datasetId, name, color) {
  const res = await apiFetch(`/datasets/${datasetId}/labels`, {
    method: "POST",
    body: JSON.stringify({ name, color }),
  });
  if (!res.ok) throw new Error("Failed to create label");
  return res.json();
}
