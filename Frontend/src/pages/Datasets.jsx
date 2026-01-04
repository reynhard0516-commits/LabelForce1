import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Layout from "../components/Layout";
import { getDatasets, createDataset } from "../services/datasets";

export default function Datasets() {
  const [datasets, setDatasets] = useState([]);
  const [name, setName] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function load() {
    try {
      const data = await getDatasets();
      setDatasets(data);
    } catch {
      setError("Failed to load datasets");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function create(e) {
    e.preventDefault();
    setError("");

    try {
      await createDataset(name, "");
      setName("");
      load();
    } catch {
      setError("Failed to create dataset");
    }
  }

  return (
    <Layout>
      <h1>My Datasets</h1>

      <form onSubmit={create} style={{ marginBottom: 20 }}>
        <input
          placeholder="Dataset name"
          value={name}
          onChange={e => setName(e.target.value)}
          required
        />
        <button style={{ marginLeft: 8 }}>Create</button>
      </form>

      {loading && <p>Loading datasets…</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      <ul>
        {datasets.map(d => (
          <li key={d.id} style={{ marginBottom: 8 }}>
            <Link to={`/datasets/${d.id}`}>
              <strong>{d.name}</strong>
            </Link>
          </li>
        ))}
      </ul>

      {!loading && datasets.length === 0 && <p>No datasets yet</p>}
    </Layout>
  );
}
