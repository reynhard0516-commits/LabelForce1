import { apiFetch } from "../api";

export async function getItems(datasetId) {
  const res = await apiFetch(`/datasets/${datasetId}/items`);

  if (!res.ok) {
    throw new Error("Failed to load items");
  }

  return res.json();
}

export async function createItem(datasetId, data_type, data_value) {
  const res = await apiFetch(`/datasets/${datasetId}/items`, {
    method: "POST",
    body: JSON.stringify({ data_type, data_value }),
  });

  if (!res.ok) {
    throw new Error("Failed to create item");
  }

  return res.json();
}
