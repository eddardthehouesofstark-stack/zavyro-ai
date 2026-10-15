import { create } from 'zustand'
import type { User } from '../types'
interface Auth{user:User|null;login:(u:User,t:string)=>void;logout:()=>void}
export const useAuth=create<Auth>(set=>({user:JSON.parse(localStorage.getItem('user')||'null'),
 login:(user,t)=>{localStorage.setItem('token',t);localStorage.setItem('user',JSON.stringify(user));set({user})},
 logout:()=>{localStorage.clear();set({user:null})}}))
interface Theme{dark:boolean;toggle:()=>void}
export const useTheme=create<Theme>(set=>({dark:localStorage.getItem('theme')!=='light',
 toggle:()=>set(s=>{localStorage.setItem('theme',s.dark?'light':'dark');return{dark:!s.dark}})}))
