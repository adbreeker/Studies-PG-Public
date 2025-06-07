import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api/train-scraper': {
        target: process.env.VITE_TRAIN_SCRAPER_API || 'http://localhost:8080',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api\/train-scraper/, '/api'),
      },
      '/api/transaction-manager': {
        target: process.env.VITE_TRANSACTION_MANAGER_API || 'http://localhost:5221',
        secure: false,
        rewrite: (path) => path.replace(/^\/api\/transaction-manager/, '/api'),
      },      '/api/account-manager': {
        target: process.env.VITE_ACCOUNT_MANAGER_API || 'http://localhost:5220',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api\/account-manager/, '/api'),
      },
      '/api/analytics': {
        target: process.env.VITE_ANALYTICS_SERVICE_URL || 'http://localhost:5223',
        changeOrigin: true,
        secure: false,
        ws: true, // Enable WebSocket proxying for SignalR
        rewrite: (path) => path.replace(/^\/api\/analytics/, ''),
      },
    },
  },
});
