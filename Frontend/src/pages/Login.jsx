import { useState } from "react";
import { login } from "../services/auth";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function submit(e) {
    e.preventDefault();
    setError("");

    try {
      const data = await login(email, password);
      localStorage.setItem("token", data.access_token);
      window.location.href = "/";
    } catch {
      setError("Invalid email or password");
    }
  }

  return (
    <form
      onSubmit={submit}
      style={{
        maxWidth: 400,
        margin: "80px auto",
        display: "flex",
        flexDirection: "column",
        gap: 10,
      }}
    >
      <h2>Login</h2>

      <input
        placeholder="Email"
        value={email}
        onChange={e => setEmail(e.target.value)}
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={e => setPassword(e.target.value)}
      />

      <button>Login</button>

      {error && <p style={{ color: "red" }}>{error}</p>}
    </form>
  );
}
