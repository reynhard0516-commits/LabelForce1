import React, {useEffect, useState} from 'react'
export default function Dashboard({token,setToken}){
  const [tasks,setTasks]=useState([])
  useEffect(()=>{ fetch('/api/v1/tasks/available',{headers:{'Authorization':'Bearer '+token}}).then(r=>r.json()).then(setTasks).catch(()=>{}) },[token])
  return (<div style={{padding:20}}>
    <h2>LabelForce Dashboard</h2>
    <button onClick={()=>{localStorage.removeItem('token'); setToken(null)}}>Logout</button>
    <div style={{marginTop:20}}>
      <h3>Available Tasks</h3>
      {tasks.length===0 && <div>No tasks</div>}
      {tasks.map(t=> <div key={t.id} style={{border:'1px solid #ddd',padding:8,marginBottom:8}}>{t.payload} - {t.reward} <button style={{marginLeft:10}} onClick={()=>claim(t.id)}>Claim</button></div>)}
    </div>
  </div>)
  function claim(id){ fetch('/api/v1/tasks/'+id+'/claim',{method:'POST',headers:{'Authorization':'Bearer '+token}}).then(()=>alert('claimed')).catch(()=>alert('fail')) }
}
