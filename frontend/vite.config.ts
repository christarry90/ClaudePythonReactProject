import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  base: '/absproxy/5173/',
  server: {
    host: true,
    allowedHosts: ['code.wakehub.org', 'code.home.wakehub.org'],
  },
})
