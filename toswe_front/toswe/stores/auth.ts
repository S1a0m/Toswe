// stores/auth.ts
import { defineStore } from 'pinia'
import { useStorage } from '@vueuse/core'
import { goToMarket } from '@/utils/navigations';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: useStorage<string | null>('accessToken', null),
    refreshToken: useStorage<string | null>('refreshToken', null),
    user: useStorage<any>('user', null), // { id_racine, username, is_seller, is_premium }
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken,
    isSeller: (state) => state.user?.is_seller ?? false,
    isPremium: (state) => state.user?.is_premium ?? false,
  },

  actions: {
    login(userData: { id_racine: string; username: string; is_seller?: boolean; is_premium?: boolean }) {
      // Simuler un accessToken
      this.accessToken = 'fake_token_' + Math.random().toString(36).substring(2)
      this.refreshToken = 'fake_refresh_' + Math.random().toString(36).substring(2)
      this.user = {
        ...userData,
        is_seller: userData.is_seller ?? false,
        is_premium: userData.is_premium ?? false,
      }
    },

    logout() {
      this.accessToken = null
      this.refreshToken = null
      this.user = null
      goToMarket()
    },
  },
})



/**
 * // store/auth.ts
import { defineStore } from "pinia"
import { useStorage } from "@vueuse/core" // pratique pour persister automatiquement

export const useAuthStore = defineStore("auth", {
  state: () => ({
    accessToken: useStorage("accessToken", null),
    refreshToken: useStorage("refreshToken", null),
    user: useStorage("user", null) as any, // { id_racine, username, is_seller, is_premium, ... }
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken,
    isSeller: (state) => state.user?.is_seller ?? false,
    isPremium: (state) => state.user?.is_premium ?? false,
  },

  actions: {
    async login(idRacine: string, token: string) {
      try {
        // Ici tu appelles ton backend Toswè (qui parle avec Racine)
        const res = await $fetch("/api/auth/login/", {
          method: "POST",
          body: { id_racine: idRacine, token },
        })

        this.accessToken = res.access
        this.refreshToken = res.refresh
        this.user = res.user
      } catch (error) {
        throw new Error("Connexion échouée")
      }
    },

    async fetchUser() {
      if (!this.accessToken) return
      try {
        const user = await $fetch("/api/auth/me/", {
          headers: { Authorization: `Bearer ${this.accessToken}` },
        })
        this.user = user
      } catch (error) {
        this.logout()
      }
    },

    async refresh() {
      if (!this.refreshToken) return
      try {
        const res = await $fetch("/api/auth/refresh/", {
          method: "POST",
          body: { refresh: this.refreshToken },
        })
        this.accessToken = res.access
      } catch {
        this.logout()
      }
    },

    logout() {
      this.accessToken = null
      this.refreshToken = null
      this.user = null
    },
  },
})

 */