import { api } from "../api";

export const exportDataset = (id) => api.get(`/export/${id}`);
export const exportCOCO = (id) => api.get(`/export/coco/${id}`);
export const exportYOLO = (id) => api.get(`/export/yolo/${id}`);
