import { useState } from "react";
import { login } from "../db";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  async function handleLogin(e) {
    e.preventDefault();

    try {
      const data = await login(email, password);

      // Save token
      localStorage.setItem("token", data.access_token);

      alert("Logged in!");
    } catch (err) {
      alert("Invalid login");
      console.error(err);
    }
  }

  return (
    <form onSubmit={handleLogin}>
      <h2>Login</h2>

      <input
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <button>Login</button>
    </form>
  );
}
