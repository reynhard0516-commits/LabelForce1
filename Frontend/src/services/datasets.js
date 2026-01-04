import { api } from "../api";

export function getDatasets() {
  return api.get("/datasets");
}

export function getDataset(id) {
  return api.get(`/datasets/${id}`);
}

export function createDataset(name, description) {
  return api.post("/datasets", { name, description });
}
