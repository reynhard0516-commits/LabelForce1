import { apiFetch } from "../api";

export async function getItems(datasetId) {
  const res = await apiFetch(`/items/${datasetId}`);
  return res.json();
}

export async function createItem(datasetId, type, value) {
  const res = await apiFetch("/items", {
    method: "POST",
    body: JSON.stringify({
      dataset_id: datasetId,
      data_type: type,
      data_url: value,
    }),
  });
  return res.json();
}

export async function uploadImage(datasetId, file) {
  const token = localStorage.getItem("token");
  const form = new FormData();
  form.append("file", file);
  form.append("dataset_id", datasetId);

  const res = await fetch(
    `${import.meta.env.VITE_API_URL}/items/upload`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: form,
    }
  );

  return res.json();
}
