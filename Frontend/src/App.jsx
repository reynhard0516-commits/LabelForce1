import React, {useState} from 'react'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
export default function App(){
  const [token, setToken] = useState(localStorage.getItem('token'))
  return token ? <Dashboard token={token} setToken={setToken} /> : <Login onLogin={(t)=>{localStorage.setItem('token',t); setToken(t)}} />
}
