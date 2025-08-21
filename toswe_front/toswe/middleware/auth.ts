// middleware/auth.ts
export default defineNuxtRouteMiddleware((to, from) => {
  const auth = useAuthStore()

  if (!auth.isAuthenticated && !auth.isSeller && !auth.isPremiumSeller) {
    return navigateTo('/auth')
  }
})
