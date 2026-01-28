// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  css: ['@/assets/css/main.css', 'swiper/css'],
  vite: {    
    plugins: [      
      tailwindcss(),   
    ],  
  },
  modules: [
    '@nuxt/icon',
    '@vueuse/motion/nuxt',
    '@pinia/nuxt',
    '@vite-pwa/nuxt',
  ],


  pwa: {
    registerType: 'autoUpdate', // met à jour automatiquement le service worker
    manifest: {
      name: 'Tôswè Africa',
      short_name: 'Tôswè',
      description: 'Une application Nuxt transformée en PWA',
      theme_color: '#ffffff',
      background_color: '#ffffff',
      display: 'standalone',
      start_url: '/',
      icons: [
        {
          src: '/images/logo.png',
          sizes: '192x192',
          type: 'image/png'
        },
        {
          src: '/images/logo.png',
          sizes: '512x512',
          type: 'image/png'
        }
      ]
    },
    workbox: {
      cleanupOutdatedCaches: true,
      clientsClaim: true,
      skipWaiting: true,
    },
    devOptions: {
      enabled: true, // pour tester le service worker en mode dev
      type: 'module'
    }
  },
  app: {
    head: {
      meta: [
        { name: 'apple-mobile-web-app-capable', content: 'yes' },
        { name: 'apple-mobile-web-app-status-bar-style', content: 'black-translucent' },
      ],
      link: [
        {
          rel: "preconnect",
          href: "https://fonts.googleapis.com",
        },
        {
          rel: "preconnect",
          href: "https://fonts.gstatic.com",
        },
        {
          rel: "stylesheet",
          href: "https://fonts.googleapis.com/css2?family=Kenia&family=Kumbh+Sans:wght@400;700&display=swap",
        },
        { rel: 'apple-touch-icon', href: '/images/logo.png' },
      ],
    },
  },
})
