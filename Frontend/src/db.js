const API_URL = import.meta.env.VITE_API_URL;

// Generic request function
export async function apiRequest(endpoint, method = "GET", data = null) {
  const options = {
    method,
    headers: { "Content-Type": "application/json" },
  };

  if (data) {
    options.body = JSON.stringify(data);
  }

  const res = await fetch(`${API_URL}${endpoint}`, options);

  if (!res.ok) {
    throw new Error(`API error: ${res.status}`);
  }

  return await res.json();
}

// LOGIN request
export function login(email, password) {
  return apiRequest("/login", "POST", { email, password });
}

// REGISTER request (optional)
export function register(email, password) {
  return apiRequest("/register", "POST", { email, password });
}

export default {
  login,
  register,
};
