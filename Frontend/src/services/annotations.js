import { apiFetch } from "../api";

export async function getAnnotations(itemId) {
  const res = await apiFetch(`/items/${itemId}/annotations`);
  if (!res.ok) throw new Error("Failed to load annotations");
  return res.json();
}

export async function createAnnotation(itemId, label_id, value) {
  const res = await apiFetch(`/items/${itemId}/annotations`, {
    method: "POST",
    body: JSON.stringify({ label_id, value }),
  });
  if (!res.ok) throw new Error("Failed to save annotation");
  return res.json();
}
