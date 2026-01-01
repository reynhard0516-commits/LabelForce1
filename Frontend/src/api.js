const API_URL = import.meta.env.VITE_API_URL;

/**
 * Centralized API helper
 */
export async function apiFetch(path, options = {}) {
  const token = localStorage.getItem("token");

  const headers = {
    "Content-Type": "application/json",
    ...(token && { Authorization: `Bearer ${token}` }),
    ...options.headers,
  };

  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers,
  });

  // Handle expired / invalid token
  if (response.status === 401) {
    localStorage.removeItem("token");
    throw new Error("Unauthorized");
  }

  return response;
}
