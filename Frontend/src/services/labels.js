import { apiFetch } from "../api";

/**
 * Get labels for a dataset
 */
export async function getLabels(datasetId) {
  const res = await apiFetch(`/labels/${datasetId}`);
  if (!res.ok) throw new Error("Failed to load labels");
  return res.json();
}

/**
 * Create label
 */
export async function createLabel(datasetId, name) {
  const res = await apiFetch(`/labels/${datasetId}?name=${encodeURIComponent(name)}`, {
    method: "POST",
  });
  if (!res.ok) throw new Error("Failed to create label");
  return res.json();
}
