import { apiFetch } from "../api";

/**
 * Get all items in a dataset
 */
export async function getDataItems(datasetId) {
  const res = await apiFetch(`/datasets/${datasetId}/items`);

  if (!res.ok) {
    throw new Error("Failed to load data items");
  }

  return res.json();
}

/**
 * Create a new data item
 */
export async function createDataItem(datasetId, data_type, data_url) {
  const res = await apiFetch(`/datasets/${datasetId}/items`, {
    method: "POST",
    body: JSON.stringify({ data_type, data_url }),
  });

  if (!res.ok) {
    throw new Error("Failed to create data item");
  }

  return res.json();
}
