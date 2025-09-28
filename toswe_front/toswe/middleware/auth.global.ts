// middleware/auth.global.ts
import { useAuthStore } from '@/stores/auth'

export default defineNuxtRouteMiddleware((to) => {
  const auth = useAuthStore()

  // routes publiques autorisées (avec préfixes possibles)
  const publicRoutes = [
    '/auth',
    '/market',
    '/product',
    '/cart',
    '/search',
    '/pc-cgu',
    '/',
  ]

  // Vérifie si la route est publique (match exact ou sous-chemin, ex: /product/123)
  const isPublic = publicRoutes.some((route) =>
    to.path === route || to.path.startsWith(route + '/')
  )

  // Si pas connecté et route protégée
  if (!auth.accessToken && !isPublic) {
    return navigateTo('/auth')
  }

  // Exemple : empêcher un utilisateur connecté d’aller à /auth
  if (auth.accessToken && to.path === '/auth') {
    return navigateTo('/market')
  }
})
