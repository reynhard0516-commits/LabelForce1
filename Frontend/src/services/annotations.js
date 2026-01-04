import { apiFetch } from "../api";

export async function createAnnotation(itemId, labelId, value) {
  const res = await apiFetch("/annotations", {
    method: "POST",
    body: JSON.stringify({
      item_id: itemId,
      label_id: labelId,
      value,
    }),
  });
  return res.json();
}

export async function getAnnotations(itemId) {
  const res = await apiFetch(`/annotations/${itemId}`);
  return res.json();
}
