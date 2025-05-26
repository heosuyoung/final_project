import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
        rewrite: path => path.replace(/^\/api/, ''),
      },
      '/advisor': {
        target: 'http://127.0.0.1:8000',  // Django 백엔드 서버 주소
        changeOrigin: true,
      },
      '/accounts': {
        target: 'http://127.0.0.1:8000',  // Django 백엔드 서버 주소
        changeOrigin: true,
      },
      '/boards': {
        target: 'http://127.0.0.1:8000',  // Django 백엔드 서버 주소
        changeOrigin: true,
      },
    },
  },
})
