// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  css: ['~/assets/css/main.css', 'swiper/css'],
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
      name: 'Mon Application',
      short_name: 'MonApp',
      description: 'Une application Nuxt transformée en PWA',
      theme_color: '#ffffff',
      background_color: '#ffffff',
      display: 'standalone',
      start_url: '/',
      icons: [
        {
          src: '/pwa-192x192.png',
          sizes: '192x192',
          type: 'image/png'
        },
        {
          src: '/pwa-512x512.png',
          sizes: '512x512',
          type: 'image/png'
        }
      ]
    },
    workbox: {
      navigateFallback: '/', // fallback en cas de navigation offline
    },
    client: {
      installPrompt: true, // active la boîte de dialogue "Installer l'app"
    },
    devOptions: {
      enabled: true, // pour tester le service worker en mode dev
      type: 'module'
    }
  },
  ssr: true,
  app: {
    head: {
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
      ],
    },
  },
})
