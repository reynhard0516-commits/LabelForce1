import { apiFetch } from "../api";

/**
 * Raw JSON export
 * GET /export/{dataset_id}
 */
export async function exportDataset(datasetId) {
  const res = await apiFetch(`/export/${datasetId}`);

  if (!res.ok) {
    let message = "Export failed";
    try {
      const err = await res.json();
      message = err.detail || message;
    } catch {}
    throw new Error(message);
  }

  return res.json();
}

/**
 * COCO export
 * GET /export/coco/{dataset_id}
 */
export async function exportCOCO(datasetId) {
  const res = await apiFetch(`/export/coco/${datasetId}`);

  if (!res.ok) {
    let message = "COCO export failed";
    try {
      const err = await res.json();
      message = err.detail || message;
    } catch {}
    throw new Error(message);
  }

  return res.json();
}

/**
 * YOLO export
 * GET /export/yolo/{dataset_id}
 */
export async function exportYOLO(datasetId) {
  const res = await apiFetch(`/export/yolo/${datasetId}`);

  if (!res.ok) {
    let message = "YOLO export failed";
    try {
      const err = await res.json();
      message = err.detail || message;
    } catch {}
    throw new Error(message);
  }

  return res.json();
}
