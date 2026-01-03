import { useEffect, useState } from "react";
import { getAnnotations, deleteAnnotation } from "../services/annotations";

export default function AnnotationList({ itemId, labels }) {
  const [annotations, setAnnotations] = useState([]);
  const [error, setError] = useState("");

  async function load() {
    try {
      const data = await getAnnotations(itemId);
      setAnnotations(data);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    load();
  }, [itemId]);

  async function handleDelete(id) {
    if (!window.confirm("Delete annotation?")) return;
    await deleteAnnotation(id);
    load();
  }

  function labelName(id) {
    return labels.find(l => l.id === id)?.name || "Unknown";
  }

  return (
    <div style={{ marginTop: 10 }}>
      <strong>Annotations</strong>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {annotations.length === 0 ? (
        <p>No annotations yet</p>
      ) : (
        <ul>
          {annotations.map(a => (
            <li key={a.id}>
              <span>
                Label: <b>{labelName(a.label_id)}</b>
              </span>

              {a.data?.box && (
                <pre style={{ fontSize: 12 }}>
                  {JSON.stringify(a.data.box, null, 2)}
                </pre>
              )}

              <button
                onClick={() => handleDelete(a.id)}
                style={{ marginLeft: 10 }}
              >
                ❌ Delete
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
