import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Layout from "../components/Layout";
import { getDatasets, createDataset } from "../services/datasets";

export default function Datasets() {
  const [datasets, setDatasets] = useState([]);
  const [name, setName] = useState("");

  async function load() {
    const data = await getDatasets();
    setDatasets(data);
  }

  useEffect(() => {
    load();
  }, []);

  async function create(e) {
    e.preventDefault();
    await createDataset(name, "");
    setName("");
    load();
  }

  return (
    <Layout>
      <h1>Datasets</h1>
      <form onSubmit={create}>
        <input value={name} onChange={e => setName(e.target.value)} />
        <button>Create</button>
      </form>

      <ul>
        {datasets.map(d => (
          <li key={d.id}>
            <Link to={`/datasets/${d.id}`}>{d.name}</Link>
          </li>
        ))}
      </ul>
    </Layout>
  );
}
