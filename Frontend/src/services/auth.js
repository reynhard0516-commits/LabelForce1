import { apiRequest } from "../api";

export async function login(email, password) {
  return apiRequest("/auth/login", "POST", { email, password });
}

export async function register(email, password) {
  return apiRequest("/auth/register", "POST", { email, password });
}

export async function getMe(token) {
  return apiRequest("/auth/me", "GET", null, token);
}
