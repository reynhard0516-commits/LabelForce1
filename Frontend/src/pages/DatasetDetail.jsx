import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { getDataset } from "../services/datasets";

export default function DatasetDetail() {
  const { id } = useParams();
  const [dataset, setDataset] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const data = await getDataset(id);
        setDataset(data);
      } catch (err) {
        setError(err.message);
      }
    }
    load();
  }, [id]);

  if (error) {
    return <p style={{ color: "red" }}>{error}</p>;
  }

  if (!dataset) {
    return <p>Loading dataset...</p>;
  }

  return (
    <div>
      <h1>{dataset.name}</h1>
      <p>{dataset.description}</p>

      <hr />

      <p><strong>Dataset ID:</strong> {dataset.id}</p>

      <Link to="/">← Back to datasets</Link>
    </div>
  );
}
