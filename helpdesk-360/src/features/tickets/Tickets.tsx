import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { useFetch } from '../../hooks/useFetch'
import { ticketApi } from '../../services/api'
import { Async,Page,TicketTable,StatusBadge,PriorityBadge } from '../../components/ui'
import { STATUSES } from '../../types'
export function TicketList({base}:{base:string}){
 const [q,setQ]=useState('');const [st,setSt]=useState('');const r=useFetch(()=>ticketApi.list(),[])
 return <Page title="My tickets" actions={<div className="flex gap-2"><input className="input" placeholder="Search tickets" value={q} onChange={e=>setQ(e.target.value)}/><select className="input" value={st} onChange={e=>setSt(e.target.value)}><option value="">All statuses</option>{STATUSES.map(s=><option key={s}>{s}</option>)}</select></div>}>
  <Async q={r} empty={d=>!d.length}>{d=><TicketTable base={base} tickets={d.filter(t=>(!st||t.status===st)&&t.title.toLowerCase().includes(q.toLowerCase()))}/>}</Async></Page>}
export function TicketDetail(){
 const {id}=useParams();const t=useFetch(()=>ticketApi.get(id!),[id]);const m=useFetch(()=>ticketApi.messages(id!),[id])
 return <Async q={t}>{x=><Page title={`${x.id} · ${x.title}`}><div className="grid gap-4 lg:grid-cols-3">
  <div className="card space-y-2 lg:col-span-2"><p className="text-sm">{x.description}</p>
   <h2 className="pt-2 font-medium">Conversation</h2><Async q={m} empty={d=>!d.length}>{d=>d.filter(i=>i.kind!=='internal').map(i=><div key={i.id} className="rounded-lg bg-slate-100 p-2 text-sm dark:bg-slate-800"><b>{i.author}</b><p>{i.body}</p></div>)}</Async></div>
  <aside className="card h-fit space-y-2 text-sm"><StatusBadge s={x.status}/><PriorityBadge p={x.priority}/><p>Category: {x.category}</p>{x.slaDueAt&&<p>SLA due: {new Date(x.slaDueAt).toLocaleString()}</p>}</aside></div></Page>}</Async>}
