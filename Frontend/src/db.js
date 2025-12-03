// Read backend URL from Render environment variable
export const API = import.meta.env.VITE_API_URL;

// Example API call
export async function login(username, password) {
  const res = await fetch(`${API}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });

  if (!res.ok) {
    throw new Error("Login failed");
  }

  return await res.json();
}

// Another example
export async function getProjects() {
  const res = await fetch(`${API}/projects`);
  return res.json();
}
