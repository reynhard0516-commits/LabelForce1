import { apiFetch } from "../api";

async function handleResponse(res) {
  if (!res.ok) {
    let message = "Request failed";
    try {
      const err = await res.json();
      message = err.detail || message;
    } catch {}
    throw new Error(message);
  }
  return res.json();
}

export async function login(email, password) {
  const res = await apiFetch("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
  return handleResponse(res);
}

export async function register(email, password) {
  const res = await apiFetch("/auth/register", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
  return handleResponse(res);
}

export async function getMe() {
  const res = await apiFetch("/auth/me");
  return handleResponse(res);
}

export function logout() {
  localStorage.removeItem("token");
  window.location.href = "/";
}
