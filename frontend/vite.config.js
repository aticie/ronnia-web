import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vitejs.dev/config/
export default defineConfig({
  root: "src",
  base: "/public/",
  publicDir: "../public",
  plugins: [svelte()],
  server: {
    port: 5000
  },
  build: {
    outDir: '../dist',
    emptyOutDir: true
  }
})