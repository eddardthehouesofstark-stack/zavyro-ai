import { Link } from 'react-router-dom'
import { useFetch } from '../../hooks/useFetch'
import { ticketApi,miscApi } from '../../services/api'
import { Async,Page,Stat,TicketTable,EmptyState } from '../../components/ui'
import { useAuth } from '../../store'
export default function EmpDash(){
 const u=useAuth(s=>s.user)!;const q=useFetch(()=>ticketApi.list(),[]);const a=useFetch(()=>miscApi.activity(),[])
 return <Page title={`Welcome, ${u.name.split(' ')[0]}`} actions={<Link className="btn" to="/employee/create-ticket">Create ticket</Link>}>
  <Async q={q}>{t=>{const c=(s:string[])=>t.filter(x=>s.includes(x.status)).length;return <>
   <div className="grid grid-cols-2 gap-3 lg:grid-cols-4"><Stat label="Open" value={c(['New','Assigned'])}/><Stat label="In progress" value={c(['In Progress'])}/><Stat label="Waiting on you" value={c(['Waiting for Employee'])}/><Stat label="Resolved" value={c(['Resolved','Closed'])}/></div>
   {t.length?<TicketTable tickets={t.slice(0,5)} base="/employee/tickets"/>:<div className="card"><EmptyState title="No tickets yet" hint="Describe your issue and AI will suggest a category and priority." action={<Link className="btn" to="/employee/create-ticket">Create ticket</Link>}/></div>}</>}}</Async>
  <div className="grid gap-3 md:grid-cols-2">
   <div className="card"><h2 className="mb-2 font-medium">Recent activity</h2><Async q={a} empty={d=>!d.length}>{d=><ul className="space-y-2 text-sm">{d.map(x=><li key={x.id}>{x.text}<span className="ml-2 text-slate-500">{new Date(x.at).toLocaleString()}</span></li>)}</ul>}</Async></div>
   <div className="card"><h2 className="mb-2 font-medium">Might already be solved</h2><p className="text-sm text-slate-500">Search the knowledge base before you raise a ticket.</p><Link className="btn mt-3" to="/knowledge-base">Search solutions</Link></div></div></Page>}
