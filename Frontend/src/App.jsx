import React, { useState } from "react";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import PrelabelDemo from "./components/PrelabelDemo";

const API_URL = import.meta.env.VITE_API_URL || "";

export default function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));

  return (
    <div>
      <header style={{ padding: 12, borderBottom: "1px solid #eee" }}>
        <strong>LabelForce</strong> {API_URL && <span style={{ marginLeft: 12, fontSize: 12 }}>API: {API_URL}</span>}
      </header>

      <main style={{ padding: 20 }}>
        {!token && <Login onLogin={(t) => { localStorage.setItem("token", t); setToken(t); }} />}
        {token && (
          <>
            <Dashboard token={token} setToken={setToken} />
            <hr style={{ margin: "20px 0" }} />
            <PrelabelDemo token={token} />
          </>
        )}
      </main>
    </div>
  );
}
