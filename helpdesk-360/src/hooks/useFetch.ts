import { useCallback, useEffect, useState } from 'react'
export function useFetch<T>(fn:()=>Promise<T>,deps:unknown[]=[]){
 const [data,setData]=useState<T>();const [loading,setLoading]=useState(true);const [error,setError]=useState<string>()
 const run=useCallback(()=>{setLoading(true);setError(undefined);fn().then(setData).catch(e=>setError(e.message)).finally(()=>setLoading(false))},deps)
 useEffect(()=>{run()},[run]);return{data,loading,error,refetch:run}}
