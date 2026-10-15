import { useEffect,useState } from 'react'
import { kbApi } from '../../services/api'
import { useFetch } from '../../hooks/useFetch'
import { Async,Page } from '../../components/ui'
export default function KB(){
 const [q,setQ]=useState('');const [dq,setDq]=useState('');useEffect(()=>{const t=setTimeout(()=>setDq(q),300);return()=>clearTimeout(t)},[q])
 const r=useFetch(()=>kbApi.search(dq),[dq]);const [open,setOpen]=useState<string|null>(null)
 return <Page title="Knowledge base"><input className="input" placeholder="Search, e.g. WiFi not working" value={q} onChange={e=>setQ(e.target.value)}/>
  <Async q={r} empty={d=>!d.length}>{d=><div className="grid gap-3 md:grid-cols-2">{d.map(a=><button key={a.id} className="card text-left" onClick={()=>setOpen(open===a.id?null:a.id)}><p className="text-xs text-slate-500">{a.category}</p><p className="font-medium">{a.title}</p>{open===a.id&&<ol className="mt-2 list-decimal pl-4 text-sm">{a.steps.map((s,i)=><li key={i}>{s}</li>)}</ol>}</button>)}</div>}</Async></Page>}
