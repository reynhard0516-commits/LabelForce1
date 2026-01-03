import { apiFetch } from "../api";

/**
 * Get items for a dataset
 */
export async function getItems(datasetId) {
  const res = await apiFetch(`/items/${datasetId}`);
  if (!res.ok) throw new Error("Failed to load items");
  return res.json();
}

/**
 * Create text item
 */
export async function createItem(datasetId, type, data) {
  const res = await apiFetch(`/items/${datasetId}`, {
    method: "POST",
    body: JSON.stringify({
      data_type: type,
      data_url: data,
    }),
  });

  if (!res.ok) throw new Error("Failed to create item");
  return res.json();
}

/**
 * Upload image item
 */
export async function uploadImage(datasetId, file) {
  const form = new FormData();
  form.append("file", file);

  const res = await apiFetch(`/items/${datasetId}/upload`, {
    method: "POST",
    body: form,
    headers: {}, // IMPORTANT: let browser set multipart headers
  });

  if (!res.ok) throw new Error("Failed to upload image");
  return res.json();
}
