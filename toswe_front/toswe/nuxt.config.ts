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
    '@vueuse/motion/nuxt'
  ],
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
