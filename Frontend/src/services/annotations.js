import { api } from "../api";

export function createAnnotation(itemId, labelId, value) {
  return api.post("/annotations", {
    item_id: itemId,
    label_id: labelId,
    value,
  });
}

export function getAnnotations(itemId) {
  return api.get(`/annotations/${itemId}`);
}
