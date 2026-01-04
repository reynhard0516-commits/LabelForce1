import { apiFetch } from "../api";

export async function getDatasets() {
  const res = await apiFetch("/datasets");
  return res.json();
}

export async function getDataset(id) {
  const res = await apiFetch(`/datasets/${id}`);
  return res.json();
}

export async function createDataset(name, description) {
  const res = await apiFetch("/datasets", {
    method: "POST",
    body: JSON.stringify({ name, description }),
  });
  return res.json();
}
