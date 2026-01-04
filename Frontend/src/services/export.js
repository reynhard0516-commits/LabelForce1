import { api } from "../api";

export function exportDataset(datasetId) {
  return api.get(`/export/${datasetId}`);
}

export function exportCOCO(datasetId) {
  return api.get(`/export/coco/${datasetId}`);
}

export function exportYOLO(datasetId) {
  return api.get(`/export/yolo/${datasetId}`);
}
