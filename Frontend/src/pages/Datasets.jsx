import { useEffect, useState } from "react";
import { apiFetch } from "../api";
import { logout } from "../auth";

export default function Datasets() {
  const [datasets, setDatasets] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    loadDatasets();
  }, []);

  async function loadDatasets() {
    try {
      const res = await apiFetch("/datasets");
      const data = await res.json();
      setDatasets(data);
    } catch (err) {
      setError(err.message || "Failed to load datasets");
    }
  }

  return (
    <div>
      <h1>My Datasets</h1>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {datasets.length === 0 && <p>No datasets yet</p>}

      <ul>
        {datasets.map(ds => (
          <li key={ds.id}>
            <strong>{ds.name}</strong>
            {ds.description && <p>{ds.description}</p>}
          </li>
        ))}
      </ul>

      <button onClick={logout}>Logout</button>
    </div>
  );
}
