import React, {useState} from 'react'
export default function Login({onLogin}){
  const [email,setEmail]=useState('demo@labelforce.ai')
  const [pw,setPw]=useState('password')
  const submit= async (e)=>{ 
    e.preventDefault(); 
    const res=await fetch('/api/v1/auth/login',{method:'POST',headers:{'Content-Type':'application/json'}, body:JSON.stringify({email,password:pw})});
    if(res.ok){const d=await res.json(); onLogin(d.access_token)} else alert('Login failed')
  }
  return (<form onSubmit={submit} style={{padding:20}}>
    <h3>Login</h3>
    <input value={email} onChange={e=>setEmail(e.target.value)} placeholder="email" /><br/>
    <input value={pw} onChange={e=>setPw(e.target.value)} placeholder="password" type="password"/><br/>
    <button>Login</button>
  </form>)
}
