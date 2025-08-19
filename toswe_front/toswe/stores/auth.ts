import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: true,
    isSeller: true,
    isPremiumSeller: true,
    user: null as null | { id: number; username: string },
  }),

  actions: {
    login(userData: { id: number; username: string }) {
      this.isAuthenticated = true
      this.user = userData
    },

    logout() {
      this.isAuthenticated = false
      this.user = null
    },
  },
})
