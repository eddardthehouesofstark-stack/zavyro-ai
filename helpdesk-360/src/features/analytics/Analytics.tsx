import { ResponsiveContainer,LineChart,Line,XAxis,YAxis,Tooltip,PieChart,Pie,Cell,BarChart,Bar,Legend } from 'recharts'
import { useFetch } from '../../hooks/useFetch'
import { miscApi } from '../../services/api'
import { Async,Page,Stat } from '../../components/ui'
const C=['#3b82f6','#8b5cf6','#f59e0b','#10b981','#ef4444']
export default function Analytics(){
 const r=useFetch(()=>miscApi.analytics(),[])
 return <Page title="Analytics"><Async q={r}>{d=><>
  <div className="grid grid-cols-2 gap-3 lg:grid-cols-4"><Stat label="Avg resolution (h)" value={d.avgResolutionHours}/></div>
  <div className="grid gap-3 lg:grid-cols-2">
   <div className="card h-72"><h2 className="mb-2 font-medium">Ticket volume</h2><ResponsiveContainer><LineChart data={d.volume}><XAxis dataKey="day"/><YAxis allowDecimals={false}/><Tooltip/><Line dataKey="count" stroke="#3b82f6"/></LineChart></ResponsiveContainer></div>
   <div className="card h-72"><h2 className="mb-2 font-medium">By category</h2><ResponsiveContainer><PieChart><Pie data={d.categories} dataKey="value" nameKey="name" outerRadius={90}>{d.categories.map((_,i)=><Cell key={i} fill={C[i%C.length]}/>)}</Pie><Tooltip/><Legend/></PieChart></ResponsiveContainer></div>
   <div className="card h-72 lg:col-span-2"><h2 className="mb-2 font-medium">Technician workload</h2><ResponsiveContainer><BarChart data={d.workload}><XAxis dataKey="name"/><YAxis allowDecimals={false}/><Tooltip/><Legend/><Bar dataKey="open" fill="#f59e0b"/><Bar dataKey="solved" fill="#10b981"/></BarChart></ResponsiveContainer></div></div></>}</Async></Page>}
