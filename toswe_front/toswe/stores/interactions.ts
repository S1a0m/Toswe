import { defineStore } from 'pinia'
import { useAuthStore } from './auth' // si tu as déjà un store d'auth
import { useFetch } from '#app' // Nuxt3 $fetch

export const useInteractionsStore = defineStore('interactions', {
  state: () => ({
    events: [] as Array<{
      product?: number | null
      action: 'view' | 'click' | 'search' | 'cart' | 'buy'
      timestamp: string
      details?: Record<string, any>
    }>
  }),

  actions: {
    // Charger depuis localStorage au démarrage
    initialize() {
      if (process.client) {
        const saved = localStorage.getItem('interactions')
        if (saved) {
          this.events = JSON.parse(saved)
        }
      }
    },

    // Ajouter une interaction
    addInteraction(action: 'view' | 'click' | 'search' | 'cart' | 'buy', product?: number, details?: Record<string, any>) {
      const event = {
        product: product ?? null,
        action,
        timestamp: new Date().toISOString(),
        details: details ?? {}
      }
      this.events.push(event)

      if (process.client) {
        localStorage.setItem('interactions', JSON.stringify(this.events))
      }

      // Essayer d'envoyer direct si connecté
      this.sync()
    },

    // Envoyer les interactions au backend
    async sync() {
      const authStore = useAuthStore()
      if (!authStore.isAuthenticated) return

      if (this.events.length === 0) return

      try {
        await useFetch('http://127.0.0.1:8000/api/interactions/', {
          method: 'POST',
          body: { events: this.events },
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`
          }
        })

        // Si succès → vider les events stockés
        this.events = []
        localStorage.removeItem('interactions')
      } catch (error) {
        console.error('Erreur sync interactions:', error)
      }
    }
  }
})
