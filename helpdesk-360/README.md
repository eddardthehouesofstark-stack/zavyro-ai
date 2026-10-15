# HelpDesk-360 frontend
npm install && cp .env.example .env && npm run dev
API contract (see src/services/api.ts): POST /auth/login, GET/POST /tickets, PATCH /tickets/:id, GET/POST /tickets/:id/messages, POST /ai/analyze|assist|chat, GET /kb, /activity, /analytics, WS /ws.
In dev mode the login page has Employee/Technician buttons so you can browse the UI without a backend.
