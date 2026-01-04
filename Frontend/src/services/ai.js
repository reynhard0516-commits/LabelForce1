import { apiFetch } from "../api";

/**
 * Auto-label a TEXT item using AI
 * Backend: POST /ai/auto-label/{item_id}
 */
export async function autoLabelItem(itemId) {
  const res = await apiFetch(`/ai/auto-label/${itemId}`, {
    method: "POST",
  });

  if (!res.ok) {
    let message = "AI auto-label failed";
    try {
      const err = await res.json();
      message = err.detail || message;
    } catch {}
    throw new Error(message);
  }

  return res.json();
}
