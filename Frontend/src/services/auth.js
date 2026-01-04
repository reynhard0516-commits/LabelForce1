import { apiFetch } from "../api";

export function isLoggedIn() {
  return !!localStorage.getItem("token");
}

export async function login(email, password) {
  const res = await apiFetch("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });

  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Login failed");
  }

  return res.json();
}

export async function register(email, password) {
  const res = await apiFetch("/auth/register", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });

  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Registration failed");
  }

  return res.json();
}

export function logout() {
  localStorage.removeItem("token");
  window.location.href = "/login";
}
