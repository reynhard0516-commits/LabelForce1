import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";

import { getDataset } from "../services/datasets";
import { getItems, createItem, uploadImage } from "../services/dataItems";
import { getLabels, createLabel } from "../services/labels";
import { createAnnotation } from "../services/annotations";
import { exportDataset, exportCOCO, exportYOLO } from "../services/export";

import ImageAnnotator from "../components/ImageAnnotator";
import AnnotationList from "../components/AnnotationList";

export default function DatasetDetail() {
  const { id } = useParams();

  const [dataset, setDataset] = useState(null);
  const [items, setItems] = useState([]);
  const [labels, setLabels] = useState([]);

  const [newLabel, setNewLabel] = useState("");
  const [text, setText] = useState("");
  const [imageFile, setImageFile] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // =========================
  // Load dataset data
  // =========================
  async function load() {
    setError("");
    try {
      const ds = await getDataset(id);
      const its = await getItems(id);
      const lbs = await getLabels(id);

      setDataset(ds);
      setItems(its);
      setLabels(lbs);
    } catch (err) {
      setError(err?.message || "Failed to load dataset");
    }
  }

  useEffect(() => {
    load();
  }, [id]);

  // =========================
  // Create text item
  // =========================
  async function handleAddItem(e) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await createItem(id, "text", text);
      setText("");
      await load();
    } catch (err) {
      setError(err?.message || "Failed to add item");
    } finally {
      setLoading(false);
    }
  }

  // =========================
  // Upload image
  // =========================
  async function handleUpload(e) {
    e.preventDefault();
    setError("");
    if (!imageFile) return;

    setLoading(true);
    try {
      await uploadImage(id, imageFile);
      setImageFile(null);
      await load();
    } catch (err) {
      setError(err?.message || "Failed to upload image");
    } finally {
      setLoading(false);
    }
  }

  // =========================
  // Create label
  // =========================
  async function handleAddLabel(e) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await createLabel(id, newLabel);
      setNewLabel("");
      await load();
    } catch (err) {
      setError(err?.message || "Failed to create label");
    } finally {
      setLoading(false);
    }
  }

  // =========================
  // Text annotation
  // =========================
  async function handleAnnotate(itemId, labelId) {
    setError("");
    try {
      await createAnnotation(itemId, labelId, { value: "selected" });
      await load();
    } catch {
      setError("Failed to save annotation");
    }
  }

  // =========================
  // Download helper
  // =========================
  function downloadJSON(data, filename) {
    const blob = new Blob([JSON.stringify(data, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  }

  // =========================
  // Export handlers
  // =========================
  async function handleExportRaw() {
    try {
      const data = await exportDataset(id);
      downloadJSON(data, `${dataset.name}_raw.json`);
    } catch {
      setError("Export failed");
    }
  }

  async function handleExportCOCO() {
    try {
      const data = await exportCOCO(id);
      downloadJSON(data, `${dataset.name}_coco.json`);
    } catch {
      setError("COCO export failed");
    }
  }

  async function handleExportYOLO() {
    try {
      const data = await exportYOLO(id);
      downloadJSON(data, `${dataset.name}_yolo.json`);
    } catch {
      setError("YOLO export failed");
    }
  }

  if (!dataset) return <p>Loading…</p>;

  return (
    <div>
      <h1>{dataset.name}</h1>
      <p>{dataset.description}</p>

      {/* ================= EXPORT ================= */}
      <hr />
      <h3>Export Dataset</h3>
      <button onClick={handleExportRaw}>⬇ Raw JSON</button>{" "}
      <button onClick={handleExportCOCO}>🧠 COCO</button>{" "}
      <button onClick={handleExportYOLO}>🎯 YOLO</button>

      {/* ================= LABELS ================= */}
      <hr />
      <h3>Create Label</h3>
      <form onSubmit={handleAddLabel}>
        <input
          value={newLabel}
          onChange={e => setNewLabel(e.target.value)}
          placeholder="Label name"
          required
        />
        <button disabled={loading}>Create</button>
      </form>

      <ul>
        {labels.map(l => (
          <li key={l.id}>{l.name}</li>
        ))}
      </ul>

      {/* ================= ITEMS ================= */}
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
        <button disabled={loading}>Add</button>
      </form>

      <hr />
      <h3>Upload Image</h3>
      <form onSubmit={handleUpload}>
        <input
          type="file"
          accept="image/*"
          onChange={e => setImageFile(e.target.files[0])}
          required
        />
        <button disabled={loading}>Upload</button>
      </form>

      {/* ================= ITEMS LIST ================= */}
      <hr />
      <h3>Items</h3>

      {items.length === 0 ? (
        <p>No items yet</p>
      ) : (
        <ul>
          {items.map(item => (
            <li key={item.id} style={{ marginBottom: 30 }}>
              {item.data_type === "image" ? (
                <>
                  <ImageAnnotator
                    imageUrl={item.data_url}
                    labels={labels}
                    onSave={data =>
                      createAnnotation(item.id, data.label_id, {
                        box: data.box,
                      })
                    }
                  />
                  <AnnotationList itemId={item.id} labels={labels} />
                </>
              ) : (
                <>
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
                  <AnnotationList itemId={item.id} labels={labels} />
                </>
              )}
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
