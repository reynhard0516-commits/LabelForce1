import { apiFetch } from "../api";

/**
 * Get all datasets owned by the logged-in user
 */
export async function getMyDatasets() {
  const res = await apiFetch("/datasets");

  if (!res.ok) {
    let message = "Failed to load datasets";
    try {
      const err = await res.json();
      message = err.detail || message;
    } catch {}
    throw new Error(message);
  }

  return res.json();
}

/**
 * Alias (optional convenience)
 * Some components may call getDatasets()
 */
export async function getDatasets() {
  return getMyDatasets();
}

/**
 * Get a single dataset by ID
 */
export async function getDataset(datasetId) {
  const res = await apiFetch(`/datasets/${datasetId}`);

  if (!res.ok) {
    let message = "Failed to load dataset";
    try {
      const err = await res.json();
      message = err.detail || message;
    } catch {}
    throw new Error(message);
  }

  return res.json();
}

/**
 * Create a new dataset
 */
export async function createDataset(name, description) {
  const res = await apiFetch("/datasets", {
    method: "POST",
    body: JSON.stringify({
      name,
      description,
    }),
  });

  if (!res.ok) {
    let message = "Failed to create dataset";
    try {
      const err = await res.json();
      message = err.detail || message;
    } catch {}
    throw new Error(message);
  }

  return res.json();
}
/**
 * Get a single dataset by ID
 */
export async function getDataset(datasetId) {
  const res = await apiFetch(`/datasets/${datasetId}`);

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Failed to load dataset");
  }

  return res.json();
}
