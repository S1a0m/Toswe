// stores/auth.ts
import { defineStore } from "pinia"
import { useStorage } from "@vueuse/core"
import { goToMarket } from "@/utils/navigations"

interface User {
  id: number
  phone: string
  is_seller: boolean
  is_premium: boolean
  is_brand: boolean
}



export const useAuthStore = defineStore("auth", {
  state: () => ({
    accessToken: null as string | null, // <-- persisté refreshTokenValue: useStorage<string | null>("refresh_token", null),
    user: useStorage<User | null>("user", null),
  }),

  getters: {
    isAuthenticated: (state) => state.accessToken && !!state.user, // !!state.refreshTokenValue
    isSeller: (state) => state.user?.is_seller ?? false,
    isPremiumSeller: (state) => state.user?.is_premium ?? false,
    isBrand: (state) => state.user?.is_brand ?? false,
  },

  actions: {
    async initConnexion(phone: string) {
      try {
        const res = await $fetch<{ detail: string }>(
          "http://127.0.0.1:8000/api/user/init_connexion/",
          {
            method: "POST",
            body: { phone },
          }
        )
        return res.detail
      } catch (e: any) {
        throw new Error(e?.data?.detail || "Erreur d'initialisation connexion")
      }
    },

    async confirmConnexion(phone: string, otp: string) {
      try {
        const res = await $fetch<{ access: string; user: User }>(
          "http://127.0.0.1:8000/api/user/confirm_connexion/",
          {
            method: "POST",
            body: { phone, session_mdp: otp },
            credentials: "include", // <-- Pour recevoir le cookie
          }
        )

        this.accessToken = res.access
        this.user = res.user
      } catch (e: any) {
        throw new Error(e?.data?.detail || "Code invalide")
      }
    },

    

    async doRefreshToken() {
      try {
        const res = await $fetch<{ access: string }>(
          "http://127.0.0.1:8000/api/refresh_token/",
          {
            method: "POST",
            credentials: "include", // 🔑 très important pour envoyer le cookie
          }
        )
        this.accessToken = res.access
      } catch {
        this.logout()
      }
    },


    async fetchUser() {
      if (!this.accessToken) return
      try {
        const user = await $fetch<User>("http://127.0.0.1:8000/api/user/me/", {
          headers: { Authorization: `Bearer ${this.accessToken}` },
        })
        this.user = user
      } catch {
        this.logout()
      }
    },

    async initialize() {
      try {
        await this.doRefreshToken()
        await this.fetchUser()
      } catch {
        this.logout()
      }
    },

    logout() {
      this.accessToken = null
      this.user = null

      // Optionnel : appel backend pour supprimer le cookie côté serveur
      $fetch("http://127.0.0.1:8000/api/user/logout/", {
        method: "POST",
        credentials: "include",
      }).catch(() => {})

      goToMarket()
    },

    setAccessToken(token: string) {
      this.accessToken = token
    }

  },
})



