import type { ReactNode } from 'react'
import { Inbox,AlertTriangle } from 'lucide-react'
import { Link } from 'react-router-dom'
import type { Status,Priority,Ticket } from '../types'
const S:Record<Status,string>={New:'bg-blue-500/15 text-blue-400',Assigned:'bg-violet-500/15 text-violet-400','In Progress':'bg-amber-500/15 text-amber-400','Waiting for Employee':'bg-slate-500/20 text-slate-400',Resolved:'bg-emerald-500/15 text-emerald-400',Closed:'bg-slate-500/15 text-slate-500'}
const P:Record<Priority,string>={Low:'text-slate-400',Medium:'text-sky-400',High:'text-orange-400',Critical:'text-red-400'}
export const StatusBadge=({s}:{s:Status})=><span className={`rounded-full px-2 py-0.5 text-xs ${S[s]}`}>{s}</span>
export const PriorityBadge=({p}:{p:Priority})=><span className={`text-xs font-medium ${P[p]}`}>● {p}</span>
export const Skeleton=({h='h-16'}:{h?:string})=><div className={`${h} animate-pulse rounded-xl bg-slate-200 dark:bg-slate-800`}/>
export const EmptyState=({title,hint,action}:{title:string;hint?:string;action?:ReactNode})=><div className="flex flex-col items-center gap-2 py-10 text-center"><Inbox className="text-slate-500"/><p className="font-medium">{title}</p>{hint&&<p className="max-w-sm text-sm text-slate-500">{hint}</p>}{action}</div>
export const ErrorState=({msg,retry}:{msg:string;retry?:()=>void})=><div className="flex flex-col items-center gap-2 py-10 text-center"><AlertTriangle className="text-red-400"/><p className="font-medium">Couldn't load this data</p><p className="text-sm text-slate-500">{msg}. Check that the API is running at VITE_API_URL.</p>{retry&&<button className="btn" onClick={retry}>Try again</button>}</div>
export function Async<T>({q,empty,children}:{q:{data?:T;loading:boolean;error?:string;refetch:()=>void};empty?:(d:T)=>boolean;children:(d:T)=>ReactNode}){
 if(q.loading)return <div className="space-y-2"><Skeleton/><Skeleton/><Skeleton/></div>
 if(q.error)return <ErrorState msg={q.error} retry={q.refetch}/>
 if(q.data===undefined||empty?.(q.data))return <EmptyState title="Nothing here yet"/>
 return <>{children(q.data)}</>}
export const Stat=({label,value}:{label:string;value:ReactNode})=><div className="card"><p className="text-sm text-slate-500">{label}</p><p className="mt-1 text-2xl font-semibold">{value}</p></div>
export const Page=({title,actions,children}:{title:string;actions?:ReactNode;children:ReactNode})=><div className="space-y-4"><div className="flex items-center justify-between"><h1 className="text-xl font-semibold">{title}</h1>{actions}</div>{children}</div>
export const TicketTable=({tickets,base}:{tickets:Ticket[];base:string})=><div className="card overflow-x-auto p-0"><table className="w-full"><thead><tr><th className="th">ID</th><th className="th">Title</th><th className="th">Status</th><th className="th">Priority</th><th className="th">Updated</th></tr></thead><tbody>{tickets.map(t=><tr key={t.id} className="border-t border-slate-200 dark:border-slate-800 hover:bg-slate-100/60 dark:hover:bg-slate-800/40"><td className="td"><Link className="text-brand" to={`${base}/${t.id}`}>{t.id}</Link></td><td className="td">{t.title}</td><td className="td"><StatusBadge s={t.status}/></td><td className="td"><PriorityBadge p={t.priority}/></td><td className="td text-slate-500">{new Date(t.updatedAt).toLocaleString()}</td></tr>)}</tbody></table></div>
