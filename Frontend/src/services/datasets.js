import { api } from "../api";

export const getDatasets = () => api.get("/datasets");
export const getDataset = (id) => api.get(`/datasets/${id}`);
export const createDataset = (name, description) =>
  api.post("/datasets", { name, description });
