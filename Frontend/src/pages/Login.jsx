import { useEffect, useState } from "react";
import { apiFetch } from "../api";
import { getMe } from "../services/auth";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [user, setUser] = useState(null);

  // 🔁 AUTO-CHECK LOGIN ON PAGE LOAD
  useEffect(() => {
    async function checkAuth() {
      try {
        const me = await getMe();
        setUser(me);
      } catch {
        localStorage.removeItem("token");
        setUser(null);
      }
    }
    checkAuth();
  }, []);

  async function handleLogin(e) {
    e.preventDefault();
    setError("");

    try {
      const res = await apiFetch("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.detail || "Login failed");
        return;
      }

      localStorage.setItem("token", data.access_token);

      // 🔁 fetch user immediately
      const me = await getMe();
      setUser(me);

    } catch (err) {
      setError(err.message || "Network error");
    }
  }

  // ======================
  // UI
  // ======================

  if (user) {
    return (
      <div>
        <h2>Logged in ✅</h2>
        <p>Email: {user.email}</p>
      </div>
    );
  }

  return (
    <form onSubmit={handleLogin}>
      <h2>Login</h2>

      <input
        value={email}
        onChange={e => setEmail(e.target.value)}
        placeholder="Email"
      />

      <input
        type="password"
        value={password}
        onChange={e => setPassword(e.target.value)}
        placeholder="Password"
      />

      <button type="submit">Login</button>

      {error && <p style={{ color: "red" }}>{error}</p>}
    </form>
  );
}
