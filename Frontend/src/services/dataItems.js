import { api } from "../api";

export const getItems = (datasetId) =>
  api.get(`/items/${datasetId}`);

export const createItem = (datasetId, type, data) =>
  api.post("/items", {
    dataset_id: datasetId,
    data_type: type,
    data_url: data,
  });

export async function uploadImage(datasetId, file) {
  const token = localStorage.getItem("token");
  const form = new FormData();
  form.append("file", file);
  form.append("dataset_id", datasetId);

  const res = await fetch(
    `${import.meta.env.VITE_API_URL}/items/upload`,
    {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
      body: form,
    }
  );

  if (!res.ok) throw new Error("Upload failed");
  return res.json();
}
