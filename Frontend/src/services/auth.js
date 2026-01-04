import { api } from "../api";

export async function login(email, password) {
  const data = await api.post("/auth/login", { email, password });
  localStorage.setItem("token", data.access_token);
  return data;
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
