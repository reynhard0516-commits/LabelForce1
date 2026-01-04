import { apiFetch } from "../api";

export async function login(email, password) {
  const res = await apiFetch("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
  return res.json();
}

export async function register(email, password) {
  const res = await apiFetch("/auth/register", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
  return res.json();
}

export async function logout() {
  localStorage.removeItem("token");
  window.location.href = "/login";
}

export function isLoggedIn() {
  return !!localStorage.getItem("token");
}
