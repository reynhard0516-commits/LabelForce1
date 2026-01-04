import { useState } from "react";
import { login } from "../services/auth";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");

    try {
      const data = await login(email, password);
      localStorage.setItem("token", data.access_token);
      window.location.href = "/";
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div style={{ maxWidth: 400, margin: "100px auto" }}>
      <h2>LabelForce Login</h2>

      <form onSubmit={handleSubmit}>
        <input
          placeholder="Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          required
        />

        <button>Login</button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}
