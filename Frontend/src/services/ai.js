import { apiFetch } from "../api";

export async function autoLabel(itemId) {
  const res = await apiFetch(`/ai/auto-label/${itemId}`, {
    method: "POST",
  });

  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "AI labeling failed");
  }

  return res.json();
}
