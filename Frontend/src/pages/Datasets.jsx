import { logout } from "../auth";

export default function Datasets() {
  return (
    <div>
      <h1>My Datasets</h1>
      <p>(Dataset list will appear here)</p>

      <button onClick={logout}>Logout</button>
    </div>
  );
}
