// plugins/api-fetch.ts
import { useAuthStore } from '@/stores/auth'

let refreshPromise: Promise<any> | null = null

export default defineNuxtPlugin(() => {
  const auth = useAuthStore()

  const apiFetch = async (request: any, options: any = {}) => {
    try {
      // 1. Appel API normal
      return await $fetch(request, {
        ...options,
        headers: {
          ...(options.headers || {}),
          Authorization: auth.accessToken ? `Bearer ${auth.accessToken}` : "Bonzou",
        },
        credentials: "include", // envoie cookie refresh si dispo
      })
    } catch (error: any) {
      // 2. Si token expiré → tentative de refresh
      if (error?.response?.status === 401 && auth.accessToken) {
        try {
          // lock pour éviter plusieurs refresh en parallèle
          if (!refreshPromise) {
            refreshPromise = auth.doRefreshToken().finally(() => {
              refreshPromise = null
            })
          }

          await refreshPromise

          // retry avec nouveau token
          return await $fetch(request, {
            ...options,
            headers: {
              ...(options.headers || {}),
              Authorization: auth.accessToken ? `Bearer ${auth.accessToken}` : "Bonssa",
            },
            credentials: "include",
          })
        } catch (refreshError) {
          // refresh échoué → déconnexion
          auth.logout()
          throw refreshError
        }
      }

      // 3. Autres erreurs
      throw error
    }
  }

  // Injection dans Nuxt pour être dispo partout
  return {
    provide: {
      apiFetch,
    },
  }
})
