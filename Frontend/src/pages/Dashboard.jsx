import { useEffect, useState } from "react";
import { getDatasets, createDataset } from "../services/datasets";
import { Link } from "react-router-dom";

export default function Dashboard() {
  const [datasets, setDatasets] = useState([]);
  const [name, setName] = useState("");

  useEffect(() => {
    getDatasets().then(setDatasets);
  }, []);

  async function create() {
    await createDataset(name, "");
    setName("");
    setDatasets(await getDatasets());
  }

  return (
    <>
      <h1>Datasets</h1>
      <input value={name} onChange={e => setName(e.target.value)} />
      <button onClick={create}>Create</button>

      <ul>
        {datasets.map(d => (
          <li key={d.id}>
            <Link to={`/datasets/${d.id}`}>{d.name}</Link>
          </li>
        ))}
      </ul>
    </>
  );
}
