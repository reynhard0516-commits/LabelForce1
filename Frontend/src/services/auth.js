import { api } from "../api";

export async function login(email, password) {
  const res = await api.post("/auth/login", { email, password });
  localStorage.setItem("token", res.access_token);
  return res;
}

export async function register(email, password) {
  return api.post("/auth/register", { email, password });
}

export function logout() {
  localStorage.removeItem("token");
  window.location.href = "/login";
}

export function isAuthenticated() {
  return Boolean(localStorage.getItem("token"));
}
