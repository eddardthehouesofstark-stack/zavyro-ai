import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { toast } from 'sonner'
import { Link } from 'react-router-dom'
import { useFetch } from '../../hooks/useFetch'
import { ticketApi,aiApi } from '../../services/api'
import { Async,StatusBadge,PriorityBadge } from '../../components/ui'
import { STATUSES,type AiAssist,type Message,type Status } from '../../types'
export default function Workspace(){
 const {id}=useParams();const t=useFetch(()=>ticketApi.get(id!),[id]);const m=useFetch(()=>ticketApi.messages(id!),[id])
 const [body,setBody]=useState('');const [kind,setKind]=useState<Message['kind']>('technician');const [ai,setAi]=useState<AiAssist|null>(null);const [aiBusy,setAiBusy]=useState(false)
 const send=async()=>{if(!body.trim())return;try{await ticketApi.reply(id!,body,kind);setBody('');m.refetch()}catch{toast.error('Message not sent')}}
 const status=async(s:Status)=>{try{await ticketApi.setStatus(id!,s);toast.success(`Status: ${s}`);t.refetch()}catch{toast.error('Status update failed')}}
 const runAi=async()=>{setAiBusy(true);try{setAi(await aiApi.assist(id!))}catch{toast.error('AI assistant is unavailable')}finally{setAiBusy(false)}}
 return <Async q={t}>{x=>{const left=x.slaDueAt?Math.round((+new Date(x.slaDueAt)-Date.now())/60000):null
  return <div className="grid gap-4 lg:grid-cols-[280px_1fr_320px]">
  <aside className="card h-fit space-y-2 text-sm"><Link className="text-brand" to="/technician/tickets">Back to tickets</Link><p className="text-xs text-slate-500">{x.id}</p><h1 className="font-semibold">{x.title}</h1><p>{x.description}</p>
   <p>Employee: {x.employee??'Unknown'}</p><p>Department: {x.department??'Unknown'}</p><p>Device: {x.device??'Unknown'}</p><p>Category: {x.category}</p><div className="flex gap-2"><StatusBadge s={x.status}/><PriorityBadge p={x.priority}/></div>
   <select className="input" value={x.status} onChange={e=>status(e.target.value as Status)}>{STATUSES.map(s=><option key={s}>{s}</option>)}</select></aside>
  <section className="card flex min-h-[28rem] flex-col"><h2 className="mb-2 font-medium">Conversation</h2>
   <div className="flex-1 space-y-2"><Async q={m} empty={d=>!d.length}>{d=>d.map(i=><div key={i.id} className={`rounded-lg p-2 text-sm ${i.kind==='internal'?'border border-dashed border-amber-500/50 bg-amber-500/10':i.kind==='technician'?'ml-10 bg-brand/15':'mr-10 bg-slate-100 dark:bg-slate-800'}`}><b>{i.author}</b>{i.kind==='internal'&&' (internal note)'}<p>{i.body}</p></div>)}</Async></div>
   <div className="mt-3 space-y-2"><div className="flex gap-2 text-sm">{([['technician','Reply'],['internal','Internal note']] as const).map(([k,l])=><button key={k} className={kind===k?'btn':'btn-ghost'} onClick={()=>setKind(k)}>{l}</button>)}</div>
    <textarea className="input" rows={4} value={body} onChange={e=>setBody(e.target.value)} placeholder={kind==='internal'?'Only technicians can see this':'Write to the employee'}/>
    <div className="flex gap-2"><button className="btn" onClick={send}>Send</button><button className="btn-ghost border border-slate-300 dark:border-slate-700" onClick={async()=>{await send();status('Resolved')}}>Send and resolve</button></div></div></section>
  <aside className="card h-fit space-y-3 text-sm"><h2 className="font-medium">AI assistant</h2>
   {left!==null&&<p className={left<0?'text-red-400':''}>SLA: {left<0?`breached ${-left} min ago`:`${Math.floor(left/60)}h ${left%60}m left`}</p>}
   {!ai?<button className="btn" disabled={aiBusy} onClick={runAi}>{aiBusy?'Analyzing…':'Analyze this ticket'}</button>:<>
    <div><b>Summary</b><p>{ai.summary}</p></div><div><b>Suggested solution</b><p>{ai.solution}</p></div>
    <div><b>Troubleshooting</b><ol className="list-decimal pl-4">{ai.steps.map((s,i)=><li key={i}>{s}</li>)}</ol></div>
    <button className="btn-ghost border border-slate-300 dark:border-slate-700" onClick={()=>{setKind('technician');setBody(ai.draftReply)}}>Use draft reply</button>
    <div><b>Related articles</b>{ai.articles.map(a=><Link key={a.id} to="/knowledge-base" className="block text-brand">{a.title}</Link>)}</div></>}</aside></div>}}</Async>}
