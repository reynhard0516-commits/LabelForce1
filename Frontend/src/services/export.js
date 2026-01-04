import { apiFetch } from "../api";

export async function exportDataset(id) {
  const res = await apiFetch(`/export/${id}`);
  return res.json();
}

export async function exportCOCO(id) {
  const res = await apiFetch(`/export/coco/${id}`);
  return res.json();
}

export async function exportYOLO(id) {
  const res = await apiFetch(`/export/yolo/${id}`);
  return res.json();
}
