import { apiFetch } from "../api";

/**
 * Get annotations for an item
 */
export async function getAnnotations(itemId) {
  const res = await apiFetch(`/annotations/${itemId}`);
  if (!res.ok) throw new Error("Failed to load annotations");
  return res.json();
}

/**
 * Create annotation
 */
export async function createAnnotation(itemId, labelId, data) {
  const res = await apiFetch(`/annotations/${itemId}`, {
    method: "POST",
    body: JSON.stringify({
      label_id: labelId,
      data,
    }),
  });

  if (!res.ok) throw new Error("Failed to create annotation");
  return res.json();
}
