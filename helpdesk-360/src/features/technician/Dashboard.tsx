import { useFetch } from '../../hooks/useFetch'
import { ticketApi } from '../../services/api'
import { Async,Page,Stat,TicketTable } from '../../components/ui'
export default function TechDash(){
 const q=useFetch(()=>ticketApi.list(),[])
 return <Page title="Command center"><Async q={q} empty={d=>!d.length}>{t=>{const n=(s:string)=>t.filter(x=>x.status===s).length;const sla=t.filter(x=>x.slaDueAt&&new Date(x.slaDueAt)<new Date()&&!['Resolved','Closed'].includes(x.status)).length;const hi=t.filter(x=>['High','Critical'].includes(x.priority)&&n('New')>=0&&x.status==='New').length
  return <><div className="grid grid-cols-2 gap-3 lg:grid-cols-4"><Stat label="New" value={n('New')}/><Stat label="Assigned" value={n('Assigned')}/><Stat label="In progress" value={n('In Progress')}/><Stat label="SLA alerts" value={sla}/></div>
  {hi>0&&<div className="card border-amber-500/40 text-sm">{hi} high-priority new ticket{hi>1?'s':''} need attention.</div>}
  <TicketTable tickets={[...t].sort((a,b)=>+(b.priority==='Critical')-+(a.priority==='Critical'))} base="/technician/ticket"/></>}}</Async></Page>}
