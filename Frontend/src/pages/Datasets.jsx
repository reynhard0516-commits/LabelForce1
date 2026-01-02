import { useEffect, useState } from "react";
import { getMyDatasets } from "../services/datasets";

export default function Datasets() {
  const [datasets, setDatasets] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const data = await getMyDatasets();
        setDatasets(data);
      } catch (err) {
        setError(err.message);
      }
    }

    load();
  }, []);

  return (
    <div>
      <h1>My Datasets</h1>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {datasets.length === 0 ? (
        <p>No datasets yet</p>
      ) : (
        <ul>
          {datasets.map(ds => (
            <li key={ds.id}>
              <strong>{ds.name}</strong><br />
              {ds.description}
            </li>
          ))}
        </ul>
      )}

      <button
        onClick={() => {
          localStorage.removeItem("token");
          window.location.reload();
        }}
      >
        Logout
      </button>
    </div>
  );
}
