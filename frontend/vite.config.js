import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from "path"

export default defineConfig({
  plugins: [react()],
  // Point to the root folder where .env lives
  envDir: "../", 
  
  resolve: {
    alias: {
      "@": path.resolve(process.cwd(), "./src"),
    },
  },

  server: {
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
        secure: false,
      },
    },
  },
})