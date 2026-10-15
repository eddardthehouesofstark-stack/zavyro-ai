import { useEffect,useState,useCallback } from 'react'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { useNavigate } from 'react-router-dom'
import { toast } from 'sonner'
import { Page,PriorityBadge } from '../../components/ui'
import { aiApi,ticketApi } from '../../services/api'
import type { AiAnalysis } from '../../types'
const schema=z.object({title:z.string().min(5,'Add a short title'),description:z.string().min(15,'Describe the issue in more detail'),category:z.string().min(1,'Choose a category'),priority:z.string().min(1,'Choose a priority'),department:z.string().min(1,'Required'),device:z.string().min(1,'Required')})
type F=z.infer<typeof schema>
export default function CreateTicket(){
 const {register,handleSubmit,watch,setValue,formState:{errors,isSubmitting}}=useForm<F>({resolver:zodResolver(schema)});const nav=useNavigate()
 const [files,setFiles]=useState<File[]>([]);const [ai,setAi]=useState<AiAnalysis|null>(null);const [aiErr,setAiErr]=useState(false);const desc=watch('description')
 useEffect(()=>{if(!desc||desc.length<15){setAi(null);return}const t=setTimeout(()=>aiApi.analyze(desc).then(r=>{setAi(r);setAiErr(false)}).catch(()=>setAiErr(true)),700);return()=>clearTimeout(t)},[desc])
 const drop=useCallback((e:React.DragEvent)=>{e.preventDefault();setFiles(f=>[...f,...Array.from(e.dataTransfer.files)])},[])
 const submit=async(v:F)=>{const fd=new FormData();Object.entries(v).forEach(([k,x])=>fd.append(k,x));files.forEach(f=>fd.append('attachments',f))
  try{const t=await ticketApi.create(fd);toast.success('Ticket created');nav(`/employee/tickets/${t.id}`)}catch{toast.error('Could not create the ticket. Try again.')}}
 const E=({k}:{k:keyof F})=><span className="text-xs text-red-400">{errors[k]?.message}</span>
 return <Page title="Create ticket"><div className="grid gap-4 lg:grid-cols-3">
  <form onSubmit={handleSubmit(submit)} className="card space-y-3 lg:col-span-2">
   <label className="block text-sm">Issue title<input className="input mt-1" {...register('title')}/><E k="title"/></label>
   <label className="block text-sm">What's happening?<textarea rows={5} className="input mt-1" {...register('description')}/><E k="description"/></label>
   <div className="grid gap-3 sm:grid-cols-2">
    <label className="text-sm">Category<select className="input mt-1" {...register('category')}><option value="">Select</option>{['Hardware','Software','Network','Access','Other'].map(c=><option key={c}>{c}</option>)}</select><E k="category"/></label>
    <label className="text-sm">Priority<select className="input mt-1" {...register('priority')}><option value="">Select</option>{['Low','Medium','High','Critical'].map(c=><option key={c}>{c}</option>)}</select><E k="priority"/></label>
    <label className="text-sm">Department / location<input className="input mt-1" {...register('department')}/><E k="department"/></label>
    <label className="text-sm">Device information<input className="input mt-1" placeholder="e.g. Dell Latitude 5420" {...register('device')}/><E k="device"/></label></div>
   <div onDragOver={e=>e.preventDefault()} onDrop={drop} className="rounded-lg border border-dashed border-slate-400 p-4 text-center text-sm dark:border-slate-600">Drag files here or <label className="cursor-pointer text-brand">browse<input type="file" multiple className="hidden" onChange={e=>setFiles(f=>[...f,...Array.from(e.target.files||[])])}/></label>
    <ul className="mt-2 space-y-1">{files.map((f,i)=><li key={i} className="flex justify-between"><span>{f.name} ({Math.round(f.size/1024)} KB)</span><button type="button" className="text-red-400" onClick={()=>setFiles(files.filter((_,j)=>j!==i))}>Remove</button></li>)}</ul></div>
   <button className="btn" disabled={isSubmitting}>Submit ticket</button></form>
  <aside className="card h-fit space-y-2"><h2 className="font-medium">AI analysis</h2>
   {!ai&&!aiErr&&<p className="text-sm text-slate-500">Describe the issue and AI will suggest a category and priority.</p>}
   {aiErr&&<p className="text-sm text-red-400">AI analysis is unavailable. You can still choose manually.</p>}
   {ai&&<><p className="text-sm"><b>Category:</b> {ai.category}</p><p className="text-sm"><b>Priority:</b> <PriorityBadge p={ai.priority}/></p><p className="text-sm"><b>Summary:</b> {ai.summary}</p>
    <button type="button" className="btn-ghost border border-slate-300 dark:border-slate-700" onClick={()=>{setValue('category',ai.category);setValue('priority',ai.priority)}}>Apply suggestions</button></>}</aside></div></Page>}
