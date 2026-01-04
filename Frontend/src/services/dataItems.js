import { api } from "../api";

export function getItems(datasetId) {
  return api.get(`/items/${datasetId}`);
}

export function createItem(datasetId, dataType, dataUrl) {
  return api.post("/items", {
    dataset_id: datasetId,
    data_type: dataType,
    data_url: dataUrl,
  });
}

export async function uploadImage(datasetId, file) {
  const token = localStorage.getItem("token");
  const formData = new FormData();
  formData.append("file", file);
  formData.append("dataset_id", datasetId);

  const res = await fetch(
    `${import.meta.env.VITE_API_URL}/items/upload`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: formData,
    }
  );

  if (!res.ok) {
    throw new Error("Image upload failed");
  }

  return res.json();
}
