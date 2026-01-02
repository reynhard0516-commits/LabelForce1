import { apiFetch } from "../api";

export async function getMe() {
  const res = await apiFetch("/auth/me");

  if (!res.ok) {
    throw new Error("Not authenticated");
  }

  return res.json();
}

export async function register(email, password) {
  const res = await apiFetch("/auth/register", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });

  return res.json();
}

export async function getMe() {
  const res = await apiFetch("/auth/me", {
    method: "GET",
  });

  return res.json();
}
