// src/api.js

const API_URL =
  import.meta.env.VITE_API_URL ||
  "https://labelforce-backend-5oaq.onrender.com";

export async function apiFetch(path, options = {}) {
  const token = localStorage.getItem("token");

  const res = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers || {}),
    },
  });

  const contentType = res.headers.get("content-type");
  if (!contentType || !contentType.includes("application/json")) {
    const text = await res.text();
    throw new Error(`Server error: ${text.slice(0, 100)}`);
  }

  return res;
}
