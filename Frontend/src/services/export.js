
import { apiFetch } from "../api";

export async function exportCOCO(datasetId) {
  const res = await apiFetch(`/export/coco/${datasetId}`);
  if (!res.ok) throw new Error("Failed to export COCO");
  return res.json();
}

export async function exportYOLO(datasetId) {
  const res = await apiFetch(`/export/yolo/${datasetId}`);
  if (!res.ok) throw new Error("Failed to export YOLO");
  return res.json();
}
