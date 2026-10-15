import { createBrowserRouter,Navigate } from 'react-router-dom'
import type { ReactNode } from 'react'
import { useAuth } from '../store'
import type { Role } from '../types'
import Layout from '../components/Layout'
import Login from '../features/auth/Login'
import EmpDash from '../features/employee/Dashboard'
import CreateTicket from '../features/employee/CreateTicket'
import { TicketList,TicketDetail } from '../features/tickets/Tickets'
import TechDash from '../features/technician/Dashboard'
import TechTickets from '../features/technician/TicketManagement'
import Workspace from '../features/technician/Workspace'
import KB from '../features/knowledge-base/KB'
import Analytics from '../features/analytics/Analytics'
const Guard=({role,children}:{role?:Role;children:ReactNode})=>{const u=useAuth(s=>s.user);if(!u)return <Navigate to="/login" replace/>;if(role&&u.role!==role)return <Navigate to="/" replace/>;return <>{children}</>}
const Home=()=>{const u=useAuth(s=>s.user);return <Navigate to={u?`/${u.role}/dashboard`:'/login'} replace/>}
export const router=createBrowserRouter([
 {path:'/login',element:<Login/>},{path:'/',element:<Home/>},
 {element:<Guard><Layout/></Guard>,children:[
  {path:'/employee/dashboard',element:<Guard role="employee"><EmpDash/></Guard>},
  {path:'/employee/create-ticket',element:<Guard role="employee"><CreateTicket/></Guard>},
  {path:'/employee/tickets',element:<Guard role="employee"><TicketList base="/employee/tickets"/></Guard>},
  {path:'/employee/tickets/:id',element:<Guard role="employee"><TicketDetail/></Guard>},
  {path:'/technician/dashboard',element:<Guard role="technician"><TechDash/></Guard>},
  {path:'/technician/tickets',element:<Guard role="technician"><TechTickets/></Guard>},
  {path:'/technician/ticket/:id',element:<Guard role="technician"><Workspace/></Guard>},
  {path:'/knowledge-base',element:<KB/>},
  {path:'/analytics',element:<Guard role="technician"><Analytics/></Guard>}]}],{
 future:{
  v7_relativeSplatPath:true
 }
})
