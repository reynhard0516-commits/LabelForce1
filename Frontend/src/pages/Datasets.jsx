import { useEffect, useState } from "react";
import { getMyDatasets, createDataset } from "../services/datasets";
import { logout } from "../services/auth";

export default function Datasets() {
  const [datasets, setDatasets] = useState([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState("");

  async function loadDatasets() {
    try {
      const data = await getMyDatasets();
      setDatasets(data);
    } catch (err) {
      setError(err.message || "Failed to load datasets");
    }
  }

  useEffect(() => {
    loadDatasets();
  }, []);

  async function handleCreate(e) {
    e.preventDefault();
    setError("");

    try {
      await createDataset(name, description);
      setName("");
      setDescription("");
      loadDatasets(); // refresh list
    } catch (err) {
      setError(err.message || "Failed to create dataset");
    }
  }

  return (
    <div>
      <h1>My Datasets</h1>

      {/* Create dataset */}
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
        <button type="submit">Create Dataset</button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* Dataset list */}
      {datasets.length === 0 ? (
        <p>No datasets yet</p>
      ) : (
        <ul>
          {datasets.map(ds => (
            <li key={ds.id}>
              <strong>{ds.name}</strong>
              <br />
              {ds.description}
            </li>
          ))}
        </ul>
      )}

      <button onClick={logout}>Logout</button>
    </div>
  );
}
