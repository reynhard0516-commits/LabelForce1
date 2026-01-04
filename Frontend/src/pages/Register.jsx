import { useState } from "react";
import { register } from "../services/auth";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  async function submit(e) {
    e.preventDefault();
    await register(email, password);
    window.location.href = "/login";
  }

  return (
    <form onSubmit={submit}>
      <h2>Register</h2>
      <input value={email} onChange={e => setEmail(e.target.value)} />
      <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
      <button>Create Account</button>
    </form>
  );
}
