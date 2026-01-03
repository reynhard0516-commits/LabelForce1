import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { getDataset } from "../services/datasets";
import { getItems, createItem } from "../services/dataItems";

export default function DatasetDetail() {
  const { id } = useParams();
  const [dataset, setDataset] = useState(null);
  const [items, setItems] = useState([]);
  const [text, setText] = useState("");
  const [error, setError] = useState("");

  async function load() {
    try {
      const ds = await getDataset(id);
      const its = await getItems(id);
      setDataset(ds);
      setItems(its);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    load();
  }, [id]);

  async function handleAdd(e) {
    e.preventDefault();
    setError("");

    try {
      await createItem(id, "text", text);
      setText("");
      load();
    } catch (err) {
      setError(err.message);
    }
  }

  if (!dataset) return <p>Loading…</p>;

  return (
    <div>
      <h1>{dataset.name}</h1>
      <p>{dataset.description}</p>

      <hr />

      <h3>Add Text Item</h3>

      <form onSubmit={handleAdd}>
        <textarea
          value={text}
          onChange={e => setText(e.target.value)}
          placeholder="Enter text to label"
          required
        />
        <br />
        <button type="submit">Add Item</button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <hr />

      <h3>Items</h3>

      {items.length === 0 ? (
        <p>No items yet</p>
      ) : (
        <ul>
          {items.map(item => (
            <li key={item.id}>
              <strong>{item.data_type}</strong>: {item.data_url}
            </li>
          ))}
        </ul>
      )}

      <Link to="/">← Back</Link>
    </div>
  );
}
