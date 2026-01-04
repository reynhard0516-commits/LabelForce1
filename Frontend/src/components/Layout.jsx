import { logout } from "../services/auth";

export default function Layout({ children }) {
  return (
    <div style={{ fontFamily: "Arial, sans-serif" }}>
      <header
        style={{
          padding: "12px 20px",
          borderBottom: "1px solid #ddd",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <strong style={{ fontSize: 18 }}>LabelForce</strong>
        <button onClick={logout}>Logout</button>
      </header>

      <main style={{ padding: 20, maxWidth: 900, margin: "auto" }}>
        {children}
      </main>
    </div>
  );
}
