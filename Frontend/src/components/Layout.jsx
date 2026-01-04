import { logout } from "../services/auth";

export default function Layout({ children }) {
  return (
    <div>
      <header style={{ padding: 10, borderBottom: "1px solid #ccc" }}>
        <strong>LabelForce</strong>
        <button onClick={logout} style={{ float: "right" }}>
          Logout
        </button>
      </header>
      <main style={{ padding: 20 }}>{children}</main>
    </div>
  );
}
