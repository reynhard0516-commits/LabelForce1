import React, {useState} from "react";

export default function Login({onLogin}){
  const [email,setEmail]=useState("demo@labelforce.ai");
  const [password,setPassword]=useState("password");
  async function submit(e){
    e.preventDefault();
    const res = await fetch("/auth/login", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({email,password})});
    if(res.ok){
      const j = await res.json();
      onLogin(j.access_token || j.token || "");
    } else {
      alert("Login failed");
    }
  }
  return (<form onSubmit={submit} style={{padding:20}}>
    <h3>Login</h3>
    <input value={email} onChange={e=>setEmail(e.target.value)} placeholder="email"/><br/>
    <input value={password} onChange={e=>setPassword(e.target.value)} placeholder="password" type="password"/><br/>
    <button>Login</button>
  </form>);
}
