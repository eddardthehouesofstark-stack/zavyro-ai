import { useEffect,useState } from 'react'
import { NavLink,Outlet,useNavigate,useLocation } from 'react-router-dom'
import { AnimatePresence,motion } from 'framer-motion'
import { LayoutDashboard,Ticket,PlusCircle,BookOpen,BarChart3,Bell,Sun,Moon,LogOut,Menu } from 'lucide-react'
import { useAuth,useTheme } from '../store'
import { connectSocket } from '../services/api'
import { toast } from 'sonner'
import AIAssistant from '../features/ai/AIAssistant'
export default function Layout(){
 const {user,logout}=useAuth();const {dark,toggle}=useTheme();const nav=useNavigate();const loc=useLocation();const [open,setOpen]=useState(false);const [unread,setUnread]=useState(0)
 useEffect(()=>{document.documentElement.classList.toggle('dark',dark)},[dark])
 useEffect(()=>{if(localStorage.getItem('token')==='dev')return;return connectSocket(e=>{setUnread(n=>n+1);toast(e.text)})},[])
 const r=user!.role
 const links=r==='employee'?[['/employee/dashboard','Dashboard',LayoutDashboard],['/employee/create-ticket','Create ticket',PlusCircle],['/employee/tickets','My tickets',Ticket],['/knowledge-base','Knowledge base',BookOpen]]
  :[['/technician/dashboard','Command center',LayoutDashboard],['/technician/tickets','Tickets',Ticket],['/knowledge-base','Knowledge base',BookOpen],['/analytics','Analytics',BarChart3]]
 return <div className="flex min-h-screen">
  <aside className={`fixed inset-y-0 z-30 w-60 shrink-0 border-r border-slate-200 bg-white p-3 transition-transform dark:border-slate-800 dark:bg-slate-900 md:static md:translate-x-0 ${open?'':'-translate-x-full'}`}>
   <p className="mb-4 px-2 text-lg font-semibold">HelpDesk-360</p>
   <nav className="space-y-1">{links.map(([to,label,Icon]:any)=><NavLink key={to} to={to} onClick={()=>setOpen(false)} className={({isActive})=>`flex items-center gap-2 rounded-lg px-3 py-2 text-sm ${isActive?'bg-brand/15 text-brand':'hover:bg-slate-200/60 dark:hover:bg-slate-800'}`}><Icon size={16}/>{label}</NavLink>)}</nav>
  </aside>
  <div className="flex min-w-0 flex-1 flex-col">
   <header className="flex items-center justify-between border-b border-slate-200 px-4 py-2 dark:border-slate-800">
    <button className="btn-ghost md:hidden" aria-label="Menu" onClick={()=>setOpen(!open)}><Menu size={18}/></button><span className="hidden text-sm text-slate-500 md:block">{user!.name} · {r}</span>
    <div className="flex items-center gap-1">
     <button className="btn-ghost relative" aria-label="Notifications" onClick={()=>{setUnread(0)}}><Bell size={18}/>{unread>0&&<span className="absolute right-1 top-1 h-2 w-2 rounded-full bg-red-500"/>}</button>
     <button className="btn-ghost" aria-label="Toggle theme" onClick={toggle}>{dark?<Sun size={18}/>:<Moon size={18}/>}</button>
     <button className="btn-ghost" aria-label="Log out" onClick={()=>{logout();nav('/login')}}><LogOut size={18}/></button></div></header>
   <main className="flex-1 p-4 md:p-6"><AnimatePresence mode="wait"><motion.div key={loc.pathname} initial={{opacity:0,y:6}} animate={{opacity:1,y:0}} exit={{opacity:0}} transition={{duration:.15}}><Outlet/></motion.div></AnimatePresence></main></div>
  <AIAssistant/></div>}
