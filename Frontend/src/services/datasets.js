import { apiFetch } from "../api";

export async function getMyDatasets() {
  const res = await apiFetch("/datasets", {
    method: "GET",
  });

  return res.json();
}
