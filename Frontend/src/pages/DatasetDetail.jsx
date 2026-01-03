import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";

import { getDataset } from "../services/datasets";
import { getItems, createItem } from "../services/dataItems";
import { getLabels, createLabel } from "../services/labels";
import { createAnnotation } from "../services/annotations";

export default function DatasetDetail() {
  const { id } = useParams();

  const [dataset, setDataset] = useState(null);
  const [items, setItems] = useState([]);
  const [labels, setLabels] = useState([]);

  const [newLabel, setNewLabel] = useState("");
  const [text, setText] = useState("");
  const [error, setError] = useState("");

  async function load() {
    try {
      const ds = await getDataset(id);
      const its = await getItems(id);
      const lbs = await getLabels(id);

      setDataset(ds);
      setItems(its);
      setLabels(lbs);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    load();
  }, [id]);

  async function handleAddItem(e) {
    e.preventDefault();
    await createItem(id, "text", text);
    setText("");
    load();
  }

  async function handleAddLabel(e) {
    e.preventDefault();
    await createLabel(id, newLabel);
    setNewLabel("");
    load();
  }

  async function handleAnnotate(itemId, labelId) {
    await createAnnotation(itemId, labelId, {
      value: "selected",
    });
    alert("Annotation saved");
  }

  if (!dataset) return <p>Loading…</p>;

  return (
    <div>
      <h1>{dataset.name}</h1>
      <p>{dataset.description}</p>

      <hr />

      <h3>Create Label</h3>
      <form onSubmit={handleAddLabel}>
        <input
          value={newLabel}
          onChange={e => setNewLabel(e.target.value)}
          placeholder="Label name"
          required
        />
        <button>Create Label</button>
      </form>

      <ul>
        {labels.map(l => (
          <li key={l.id}>{l.name}</li>
        ))}
      </ul>

      <hr />

      <h3>Add Text Item</h3>
      <form onSubmit={handleAddItem}>
        <textarea
          value={text}
          onChange={e => setText(e.target.value)}
          placeholder="Text to label"
          required
        />
        <br />
        <button>Add Item</button>
      </form>

      <hr />

      <h3>Items</h3>

      {items.length === 0 ? (
        <p>No items yet</p>
      ) : (
        <ul>
          {items.map(item => (
            <li key={item.id}>
              <strong>{item.data_type}</strong>: {item.data_url}
              <br />

              {labels.map(label => (
                <button
                  key={label.id}
                  onClick={() => handleAnnotate(item.id, label.id)}
                  style={{ marginRight: 5 }}
                >
                  {label.name}
                </button>
              ))}
            </li>
          ))}
        </ul>
      )}

      {error && <p style={{ color: "red" }}>{error}</p>}

      <br />
      <Link to="/">← Back</Link>
    </div>
  );
}
