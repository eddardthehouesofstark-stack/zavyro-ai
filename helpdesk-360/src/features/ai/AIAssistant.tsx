import { useState } from 'react'
import { motion,AnimatePresence } from 'framer-motion'
import { Sparkles,X,Send } from 'lucide-react'
import { aiApi } from '../../services/api'
export default function AIAssistant(){
 const [open,setOpen]=useState(false);const [msgs,setMsgs]=useState<{from:'me'|'ai';text:string}[]>([]);const [text,setText]=useState('');const [busy,setBusy]=useState(false)
 const send=async(m=text)=>{if(!m.trim())return;setMsgs(x=>[...x,{from:'me',text:m}]);setText('');setBusy(true)
  try{const r=await aiApi.chat(m);setMsgs(x=>[...x,{from:'ai',text:r.reply}])}catch{setMsgs(x=>[...x,{from:'ai',text:'The AI service is unreachable. Check the API connection and try again.'}])}finally{setBusy(false)}}
 return <div className="fixed bottom-4 right-4 z-40">
  <AnimatePresence>{open&&<motion.div initial={{opacity:0,scale:.95,y:10}} animate={{opacity:1,scale:1,y:0}} exit={{opacity:0,scale:.95}} className="card mb-3 flex h-96 w-80 flex-col shadow-xl">
   <div className="mb-2 flex justify-between font-medium">Ask AI<button aria-label="Close" onClick={()=>setOpen(false)}><X size={16}/></button></div>
   <div className="flex-1 space-y-2 overflow-y-auto text-sm">{msgs.length===0?<div className="space-y-2 text-slate-500">Try one of these:{['My WiFi is not working','Help me create a ticket for a broken laptop'].map(s=><button key={s} className="block w-full rounded-lg border border-slate-300 p-2 text-left dark:border-slate-700" onClick={()=>send(s)}>{s}</button>)}</div>:msgs.map((m,i)=><p key={i} className={`rounded-lg p-2 ${m.from==='me'?'ml-8 bg-brand/15':'mr-8 bg-slate-200/60 dark:bg-slate-800'}`}>{m.text}</p>)}{busy&&<p className="text-slate-500">Thinking…</p>}</div>
   <div className="mt-2 flex gap-2"><input className="input" value={text} onChange={e=>setText(e.target.value)} onKeyDown={e=>e.key==='Enter'&&send()} placeholder="Describe your issue"/><button className="btn" aria-label="Send" onClick={()=>send()}><Send size={14}/></button></div></motion.div>}</AnimatePresence>
  <motion.button initial={{scale:0}} animate={{scale:1}} whileHover={{scale:1.08}} className="btn ml-auto h-12 w-12 justify-center rounded-full" aria-label="Open AI assistant" onClick={()=>setOpen(!open)}><Sparkles size={20}/></motion.button></div>}
