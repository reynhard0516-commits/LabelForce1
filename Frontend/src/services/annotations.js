import { api } from "../api";

export const createAnnotation = (itemId, labelId, value) =>
  api.post("/annotations", {
    item_id: itemId,
    label_id: labelId,
    value,
  });

export const getAnnotations = (itemId) =>
  api.get(`/annotations/${itemId}`);
