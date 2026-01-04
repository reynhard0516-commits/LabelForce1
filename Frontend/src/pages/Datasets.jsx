import { useEffect, useState } from "react";
import { getMyDatasets, createDataset } from "../services/datasets";
import { logout } from "../services/auth";
import { Link } from "react-router-dom";

export default function Datasets() {
  const [datasets, setDatasets] = useState([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState("");

  async function load() {
    try {
      const data = await getMyDatasets();
      setDatasets(data);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function handleCreate(e) {
    e.preventDefault();
    setError("");

    try {
      await createDataset(name, description);
      setName("");
      setDescription("");
      load();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div style={{ padding: 20 }}>
      <h1>My Datasets</h1>

      <form onSubmit={handleCreate}>
        <input
          placeholder="Dataset name"
          value={name}
          onChange={e => setName(e.target.value)}
          required
        />
        <input
          placeholder="Description"
          value={description}
          onChange={e => setDescription(e.target.value)}
        />
        <button>Create</button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <ul>
        {datasets.map(ds => (
          <li key={ds.id}>
            <Link to={`/datasets/${ds.id}`}>
              <strong>{ds.name}</strong>
            </Link>
          </li>
        ))}
      </ul>

      <button onClick={logout}>Logout</button>
    </div>
  );
}
