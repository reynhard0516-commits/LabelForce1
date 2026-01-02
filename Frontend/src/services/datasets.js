import { apiFetch } from "../api";

export async function getMyDatasets() {
  const res = await apiFetch("/datasets", {
    method: "GET",
  });

  if (!res.ok) {
    throw new Error("Failed to load datasets");
  }

  return res.json();
}
