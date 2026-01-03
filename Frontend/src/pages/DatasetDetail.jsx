import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getDataset } from "../services/datasets";
import { getDataItems, createDataItem } from "../services/dataItems";
import { logout } from "../services/auth";

export default function DatasetDetail() {
  const { id } = useParams();
  const [dataset, setDataset] = useState(null);
  const [items, setItems] = useState([]);
  const [type, setType] = useState("image");
  const [url, setUrl] = useState("");
  const [error, setError] = useState("");

  async function load() {
    try {
      setDataset(await getDataset(id));
      setItems(await getDataItems(id));
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    load();
  }, [id]);

  async function handleAdd(e) {
    e.preventDefault();
    try {
      await createDataItem(id, type, url);
      setUrl("");
      load();
    } catch (err) {
      setError(err.message);
    }
  }

  if (!dataset) return <p>Loading...</p>;

  return (
    <div>
      <h1>{dataset.name}</h1>
      <p>{dataset.description}</p>

      <h2>Add Item</h2>
      <form onSubmit={handleAdd}>
        <select value={type} onChange={e => setType(e.target.value)}>
          <option value="image">Image</option>
          <option value="text">Text</option>
          <option value="video">Video</option>
        </select>

        <input
          placeholder="URL or text"
          value={url}
          onChange={e => setUrl(e.target.value)}
          required
        />

        <button type="submit">Add</button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <h2>Items</h2>
      <ul>
        {items.map(item => (
          <li key={item.id}>
            <strong>{item.data_type}</strong>: {item.data_url}
          </li>
        ))}
      </ul>

      <button onClick={logout}>Logout</button>
    </div>
  );
}
