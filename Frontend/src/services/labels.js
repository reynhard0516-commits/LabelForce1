import { api } from "../api";

export const getLabels = (datasetId) =>
  api.get(`/labels/${datasetId}`);

export const createLabel = (datasetId, name) =>
  api.post("/labels", { dataset_id: datasetId, name });
