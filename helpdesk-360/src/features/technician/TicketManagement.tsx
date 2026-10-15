import { useState } from 'react'
import { Link } from 'react-router-dom'
import { toast } from 'sonner'
import { useFetch } from '../../hooks/useFetch'
import { ticketApi } from '../../services/api'
import { Async,Page,TicketTable,PriorityBadge } from '../../components/ui'
import { STATUSES,type Status,type Ticket } from '../../types'
export default function TechTickets(){
 const [view,setView]=useState<'table'|'kanban'>('table');const [q,setQ]=useState('');const r=useFetch(()=>ticketApi.list(),[]);const [over,setOver]=useState<Status|null>(null)
 const move=async(id:string,s:Status)=>{try{await ticketApi.setStatus(id,s);toast.success(`Moved to ${s}`);r.refetch()}catch{toast.error('Status update failed')}}
 return <Page title="Tickets" actions={<div className="flex gap-2"><input className="input" placeholder="Search" value={q} onChange={e=>setQ(e.target.value)}/>{(['table','kanban'] as const).map(v=><button key={v} className={view===v?'btn':'btn-ghost'} onClick={()=>setView(v)}>{v==='table'?'Table':'Kanban'}</button>)}</div>}>
  <Async q={r} empty={d=>!d.length}>{all=>{const t=all.filter(x=>x.title.toLowerCase().includes(q.toLowerCase()))
   return view==='table'?<TicketTable tickets={t} base="/technician/ticket"/>
   :<div className="flex gap-3 overflow-x-auto pb-2">{STATUSES.map(s=><div key={s} onDragOver={e=>{e.preventDefault();setOver(s)}} onDragLeave={()=>setOver(null)} onDrop={e=>{setOver(null);move(e.dataTransfer.getData('id'),s)}} className={`w-64 shrink-0 rounded-xl p-2 ${over===s?'bg-brand/10':'bg-slate-200/50 dark:bg-slate-900'}`}>
    <p className="mb-2 px-1 text-sm font-medium">{s} <span className="text-slate-500">{t.filter(x=>x.status===s).length}</span></p>
    <div className="space-y-2">{t.filter(x=>x.status===s).map((x:Ticket)=><Link key={x.id} to={`/technician/ticket/${x.id}`} draggable onDragStart={e=>e.dataTransfer.setData('id',x.id)} className="card block p-3 text-sm"><p className="text-xs text-slate-500">{x.id}</p>{x.title}<div className="mt-1"><PriorityBadge p={x.priority}/></div></Link>)}</div></div>)}</div>}}</Async></Page>}
