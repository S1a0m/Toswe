// middleware/auth.global.ts
import { useAuthStore } from '@/stores/auth'

export default defineNuxtRouteMiddleware((to) => {
  const auth = useAuthStore()

  // routes publiques autorisées
  const publicRoutes = [
    '/auth', 
    '/market', 
    '/product',
    '/cart',
    '/search',
    '/'
  ]

  if (!auth.accessToken && !publicRoutes.includes(to.path)) {
    return navigateTo('/market')
  }
})
