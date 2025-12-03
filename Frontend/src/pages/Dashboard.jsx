import React, { useEffect, useState } from "react";

export default function Dashboard({ token, setToken }) {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    fetch("/tasks/available", { headers: { Authorization: "Bearer " + token } })
      .then(r => r.json())
      .then(setTasks)
      .catch(() => {});
  }, [token]);

  function logout() {
    localStorage.removeItem("token");
    setToken(null);
  }

  return (
    <div>
      <div style={{ marginBottom: 12 }}>
        <button onClick={logout}>Logout</button>
      </div>
      <h3>Available Tasks</h3>
      {tasks.length === 0 && <div>No tasks</div>}
      {tasks.map(t => (
        <div key={t.id} style={{ border: "1px solid #ddd", padding: 8, marginBottom: 8 }}>
          {t.payload} — {t.reward} <button style={{ marginLeft: 8 }} onClick={() => claim(t.id)}>Claim</button>
        </div>
      ))}
    </div>
  );

  function claim(id) {
    fetch(`/tasks/${id}/claim`, { method: "POST", headers: { Authorization: "Bearer " + token } })
      .then(() => alert("Claimed"))
      .catch(() => alert("Failed"));
  }
}
