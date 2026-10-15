import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { motion } from 'framer-motion'
import { useNavigate } from 'react-router-dom'
import { useState } from 'react'
import { authApi } from '../../services/api'
import { useAuth } from '../../store'
import type { Role } from '../../types'
const schema=z.object({email:z.string().email('Enter a valid email'),password:z.string().min(6,'At least 6 characters'),remember:z.boolean().optional()})
type F=z.infer<typeof schema>
export default function Login(){
 const {register,handleSubmit,formState:{errors,isSubmitting}}=useForm<F>({resolver:zodResolver(schema)});const login=useAuth(s=>s.login);const nav=useNavigate();const [err,setErr]=useState('')
 const submit=async(v:F)=>{setErr('');try{const r=await authApi.login(v);login(r.user,r.token);nav(`/${r.user.role}/dashboard`)}catch{setErr('Sign-in failed. Check your credentials and that the API is running.')}}
 const dev=(role:Role)=>{login({id:'dev',name:'Dev '+role,email:'dev@local',role},'dev');nav(`/${role}/dashboard`)}
 return <div className="grid min-h-screen md:grid-cols-2">
  <div className="relative hidden overflow-hidden bg-gradient-to-br from-blue-950 to-slate-950 p-12 md:flex md:flex-col md:justify-end">
   <motion.div className="absolute left-1/4 top-1/4 h-64 w-64 rounded-full bg-brand/30 blur-3xl" animate={{x:[0,40,0],y:[0,30,0]}} transition={{duration:10,repeat:Infinity}}/>
   <h2 className="relative text-3xl font-semibold text-white">Report it once.<br/>Get it fixed faster.</h2><p className="relative mt-2 text-slate-300">AI triages every ticket so technicians start with the answer.</p></div>
  <motion.form initial={{opacity:0,x:20}} animate={{opacity:1,x:0}} onSubmit={handleSubmit(submit)} className="m-auto w-full max-w-sm space-y-3 p-6">
   <h1 className="text-2xl font-semibold">Sign in to HelpDesk-360</h1>
   <label className="block text-sm">Email<input className="input mt-1" {...register('email')}/><span className="text-xs text-red-400">{errors.email?.message}</span></label>
   <label className="block text-sm">Password<input type="password" className="input mt-1" {...register('password')}/><span className="text-xs text-red-400">{errors.password?.message}</span></label>
   <div className="flex justify-between text-sm"><label className="flex gap-2"><input type="checkbox" {...register('remember')}/>Remember me</label><a href="#" className="text-brand">Forgot password?</a></div>
   {err&&<p className="text-sm text-red-400" role="alert">{err}</p>}
   <button className="btn w-full justify-center" disabled={isSubmitting}>Sign in</button>
   {import.meta.env.DEV&&<div className="border-t border-slate-800 pt-3 text-xs text-slate-500">Dev only, no backend:<div className="mt-1 flex gap-2"><button type="button" className="btn-ghost" onClick={()=>dev('employee')}>Employee view</button><button type="button" className="btn-ghost" onClick={()=>dev('technician')}>Technician view</button></div></div>}</motion.form></div>}
