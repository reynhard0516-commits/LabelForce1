import React, { useState } from "react";

export default function Login({ onLogin }) {
  const [email, setEmail] = useState("demo@labelforce.ai");
  const [password, setPassword] = useState("password");

  async function submit(e) {
    e.preventDefault();
    try {
      const res = await fetch("/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      if (!res.ok) throw new Error("Login failed");
      const j = await res.json();
      onLogin(j.access_token || j.token || "");
    } catch (err) {
      alert("Login failed");
    }
  }

  return (
    <form onSubmit={submit}>
      <div><input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="email" /></div>
      <div><input value={password} onChange={(e) => setPassword(e.target.value)} placeholder="password" type="password" /></div>
      <div><button>Login</button></div>
    </form>
  );
}
