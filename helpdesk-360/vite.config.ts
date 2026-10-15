import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        configure: (proxy) => {
          proxy.on('error', (_err, _req, res) => {
            // When backend is not running on port 8000, intercept proxy ECONNREFUSED
            // and return 200 with fallback JSON instead of returning 500
            if (!res.headersSent && !res.writableEnded) {
              res.writeHead(200, { 'Content-Type': 'application/json' })
              res.end(JSON.stringify({ status: 'offline', message: 'Backend not running at port 8000. Mock mode active.' }))
            }
          })
        },
      },
    },
  },
})
