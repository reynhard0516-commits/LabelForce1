import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";

import { getDataset } from "../services/datasets";
import { getItems, createItem } from "../services/dataItems";
import { getLabels, createLabel } from "../services/labels";
import { getAnnotations, createAnnotation } from "../services/annotations";

export default function DatasetDetail() {
  const { id } = useParams();

  const [dataset, setDataset] = useState(null);
  const [items, setItems] = useState([]);
  const [labels, setLabels] = useState([]);
  const [annotations, setAnnotations] = useState({});

  const [text, setText] = useState("");
  const [newLabel, setNewLabel] = useState("");
  const [error, setError] = useState("");

  async function loadAll() {
    try {
      const ds = await getDataset(id);
      const its = await getItems(id);
      const lbs = await getLabels(id);

      setDataset(ds);
      setItems(its);
      setLabels(lbs);

      // Load annotations per item
      const annMap = {};
      for (const item of its) {
        annMap[item.id] = await getAnnotations(item.id);
      }
      setAnnotations(annMap);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    loadAll();
  }, [id]);

  async function handleAddItem(e) {
    e.preventDefault();
    setError("");

    try {
      await createItem(id, "text", text);
      setText("");
      loadAll();
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleAddLabel(e) {
    e.preventDefault();
    setError("");

    try {
      await createLabel(id, newLabel, null);
      setNewLabel("");
      loadAll();
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleAnnotate(itemId, labelId) {
    try {
      await createAnnotation(itemId, labelId, "selected");
      loadAll();
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

      {/* ADD ITEM */}
      <h3>Add Text Item</h3>
      <form onSubmit={handleAddItem}>
        <textarea
          value={text}
          onChange={e => setText(e.target.value)}
          placeholder="Enter text to label"
          required
        />
        <br />
        <button type="submit">Add Item</button>
      </form>

      <hr />

      {/* LABELS */}
      <h3>Labels</h3>
      <form onSubmit={handleAddLabel}>
        <input
          placeholder="New label name"
          value={newLabel}
          onChange={e => setNewLabel(e.target.value)}
          required
        />
        <button type="submit">Add Label</button>
      </form>

      <ul>
        {labels.map(label => (
          <li key={label.id}>{label.name}</li>
        ))}
      </ul>

      <hr />

      {/* ITEMS + ANNOTATIONS */}
      <h3>Items</h3>

      {items.length === 0 ? (
        <p>No items yet</p>
      ) : (
        <ul>
          {items.map(item => (
            <li key={item.id} style={{ marginBottom: "1rem" }}>
              <strong>{item.data_type}</strong>: {item.data_url}

              <br />

              {/* Annotate */}
              <select
                defaultValue=""
                onChange={e =>
                  handleAnnotate(item.id, Number(e.target.value))
                }
              >
                <option value="">Assign label</option>
                {labels.map(label => (
                  <option key={label.id} value={label.id}>
                    {label.name}
                  </option>
                ))}
              </select>

              {/* Existing annotations */}
              {annotations[item.id] && annotations[item.id].length > 0 && (
                <ul>
                  {annotations[item.id].map(a => (
                    <li key={a.id}>
                      Label ID: {a.label_id}
                    </li>
                  ))}
                </ul>
              )}
            </li>
          ))}
        </ul>
      )}

      {error && <p style={{ color: "red" }}>{error}</p>}

      <Link to="/">← Back to datasets</Link>
    </div>
  );
}
