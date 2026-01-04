import { apiFetch } from "../api";

export async function getLabels(datasetId) {
  const res = await apiFetch(`/labels/${datasetId}`);
  return res.json();
}

export async function createLabel(datasetId, name) {
  const res = await apiFetch("/labels", {
    method: "POST",
    body: JSON.stringify({ dataset_id: datasetId, name }),
  });
  return res.json();
}
