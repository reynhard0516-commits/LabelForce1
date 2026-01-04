import { api } from "../api";

export function getLabels(datasetId) {
  return api.get(`/labels/${datasetId}`);
}

export function createLabel(datasetId, name) {
  return api.post("/labels", {
    dataset_id: datasetId,
    name,
  });
}
