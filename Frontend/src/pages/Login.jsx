import { useState } from "react";
import { login } from "../services/auth";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function submit(e) {
    e.preventDefault();
    try {
      const data = await login(email, password);
      localStorage.setItem("token", data.access_token);
      window.location.href = "/";
    } catch {
      setError("Login failed");
    }
  }

  return (
    <form onSubmit={submit}>
      <h2>Login</h2>
      <input value={email} onChange={e => setEmail(e.target.value)} />
      <input
        type="password"
        value={password}
        onChange={e => setPassword(e.target.value)}
      />
      <button>Login</button>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </form>
  );
}
