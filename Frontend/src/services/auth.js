import { apiFetch } from "../api";

/**
 * Returns true if a token exists
 */
export function isLoggedIn() {
  return Boolean(localStorage.getItem("token"));
}

/**
 * Login user
 */
export async function login(email, password) {
  const res = await apiFetch("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Login failed");
  }

  const data = await res.json();

  if (!data.access_token) {
    throw new Error("Invalid login response");
  }

  localStorage.setItem("token", data.access_token);
  return data;
}

/**
 * Get current user
 */
export async function getMe() {
  const res = await apiFetch("/auth/me");

  if (!res.ok) {
    throw new Error("Not authenticated");
  }

  return res.json();
}

/**
 * Logout
 */
export function logout() {
  localStorage.removeItem("token");
  window.location.href = "/login";
}
