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
