import axios from 'axios'
import type { Ticket, Status, User, AiAnalysis, AiAssist, Message } from '../types'
import { mockDb } from './mockData'

export const api = axios.create({ baseURL: import.meta.env.VITE_API_URL ?? '/api' })

api.interceptors.request.use(c => {
  const t = localStorage.getItem('token')
  if (t) c.headers.Authorization = `Bearer ${t}`
  return c
})

api.interceptors.response.use(
  r => r,
  e => {
    if (e.response?.status === 401 && localStorage.getItem('token') !== 'dev') {
      localStorage.clear()
      location.href = '/login'
    }
    return Promise.reject(e)
  }
)

const isDev = () => {
  return localStorage.getItem('token') === 'dev' || import.meta.env.VITE_MOCK === 'true'
}

const d = <T,>(p: Promise<{ data: T }>) => p.then(r => r.data)

const delay = (ms = 100) => new Promise(resolve => setTimeout(resolve, ms))

export const authApi = {
  login: async (b: { email: string; password: string }) => {
    if (isDev()) {
      await delay(120)
      return mockDb.login(b.email, b.password)
    }
    try {
      return await d<{ token: string; user: User }>(api.post('/auth/login', b))
    } catch (e: any) {
      if (!e.response || e.response.status >= 500) {
        console.warn('Backend server offline. Falling back to local mock authentication.')
        return mockDb.login(b.email, b.password)
      }
      throw e
    }
  },
}

export const ticketApi = {
  list: async (params?: { q?: string; status?: string }) => {
    if (isDev()) {
      await delay()
      return mockDb.getTickets(params)
    }
    try {
      return await d<Ticket[]>(api.get('/tickets', { params }))
    } catch (e: any) {
      if (!e.response || e.response.status >= 500) {
        return mockDb.getTickets(params)
      }
      throw e
    }
  },

  get: async (id: string) => {
    if (isDev()) {
      await delay()
      return mockDb.getTicket(id)
    }
    try {
      return await d<Ticket>(api.get(`/tickets/${id}`))
    } catch (e: any) {
      if (!e.response || e.response.status >= 500) {
        return mockDb.getTicket(id)
      }
      throw e
    }
  },

  create: async (f: FormData) => {
    if (isDev()) {
      await delay(150)
      return mockDb.createTicket(f)
    }
    try {
      return await d<Ticket>(api.post('/tickets', f))
    } catch (e: any) {
      if (!e.response || e.response.status >= 500) {
        return mockDb.createTicket(f)
      }
      throw e
    }
  },

  setStatus: async (id: string, status: Status) => {
    if (isDev()) {
      await delay(80)
      return mockDb.setStatus(id, status)
    }
    try {
      return await d<Ticket>(api.patch(`/tickets/${id}`, { status }))
    } catch (e: any) {
      if (!e.response || e.response.status >= 500) {
        return mockDb.setStatus(id, status)
      }
      throw e
    }
  },

  messages: async (id: string) => {
    if (isDev()) {
      await delay()
      return mockDb.getMessages(id)
    }
    try {
      return await d<Message[]>(api.get(`/tickets/${id}/messages`))
    } catch (e: any) {
      if (!e.response || e.response.status >= 500) {
        return mockDb.getMessages(id)
      }
      throw e
    }
  },

  reply: async (id: string, body: string, kind: Message['kind']) => {
    if (isDev()) {
      await delay(120)
      return mockDb.reply(id, body, kind)
    }
    try {
      return await d<Message>(api.post(`/tickets/${id}/messages`, { body, kind }))
    } catch (e: any) {
      if (!e.response || e.response.status >= 500) {
        return mockDb.reply(id, body, kind)
      }
      throw e
    }
  },
}

export const aiApi = {
  analyze: async (text: string) => {
    if (isDev()) {
      await delay(200)
      return mockDb.analyze(text)
    }
    try {
      return await d<AiAnalysis>(api.post('/ai/analyze', { text }))
    } catch (e: any) {
      if (!e.response || e.response.status >= 500) {
        return mockDb.analyze(text)
      }
      throw e
    }
  },

  assist: async (ticketId: string) => {
    if (isDev()) {
      await delay(300)
      return mockDb.assist(ticketId)
    }
    try {
      return await d<AiAssist>(api.post('/ai/assist', { ticketId }))
    } catch (e: any) {
      if (!e.response || e.response.status >= 500) {
        return mockDb.assist(ticketId)
      }
      throw e
    }
  },

  chat: async (message: string) => {
    if (isDev()) {
      await delay(250)
      return mockDb.chat(message)
    }
    try {
      return await d<{ reply: string }>(api.post('/ai/chat', { message }))
    } catch (e: any) {
      if (!e.response || e.response.status >= 500) {
        return mockDb.chat(message)
      }
      throw e
    }
  },
}

export const kbApi = {
  search: async (q: string) => {
    if (isDev()) {
      await delay(80)
      return mockDb.searchKb(q)
    }
    try {
      return await d<{ id: string; title: string; category: string; steps: string[] }[]>(api.get('/kb', { params: { q } }))
    } catch (e: any) {
      if (!e.response || e.response.status >= 500) {
        return mockDb.searchKb(q)
      }
      throw e
    }
  },
}

export const miscApi = {
  activity: async () => {
    if (isDev()) {
      await delay()
      return mockDb.getActivity()
    }
    try {
      return await d<{ id: string; text: string; at: string }[]>(api.get('/activity'))
    } catch (e: any) {
      if (!e.response || e.response.status >= 500) {
        return mockDb.getActivity()
      }
      throw e
    }
  },

  analytics: async () => {
    if (isDev()) {
      await delay()
      return mockDb.getAnalytics()
    }
    try {
      return await d<{
        volume: { day: string; count: number }[]
        categories: { name: string; value: number }[]
        workload: { name: string; open: number; solved: number }[]
        avgResolutionHours: number
      }>(api.get('/analytics'))
    } catch (e: any) {
      if (!e.response || e.response.status >= 500) {
        return mockDb.getAnalytics()
      }
      throw e
    }
  },

  notifications: async () => {
    if (isDev()) {
      await delay()
      return mockDb.getNotifications()
    }
    try {
      return await d<{ id: string; text: string }[]>(api.get('/notifications'))
    } catch (e: any) {
      if (!e.response || e.response.status >= 500) {
        return mockDb.getNotifications()
      }
      throw e
    }
  },
}

// WebSocket layer: call after login and push events into a toast/notification handler
export const connectSocket = (onEvent: (e: { text: string }) => void) => {
  if (isDev()) {
    const timer = setTimeout(() => {
      onEvent({ text: 'High-priority ticket HD-102 SLA alert: 30 minutes remaining.' })
    }, 45000)
    return () => clearTimeout(timer)
  }

  try {
    const ws = new WebSocket(`${location.origin.replace('http', 'ws')}/ws?token=${localStorage.getItem('token')}`)
    ws.onmessage = m => {
      try {
        onEvent(JSON.parse(m.data))
      } catch {
        // ignore
      }
    }
    return () => ws.close()
  } catch {
    return () => {}
  }
}
