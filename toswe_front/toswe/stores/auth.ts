// stores/auth.ts
import { defineStore } from "pinia"
import { get, useStorage } from "@vueuse/core"
import { goToMarket } from "@/utils/navigations"

interface User {
  id: number
  phone: string
  address: string
  is_seller: boolean
  is_premium: boolean
  is_brand: boolean
  is_verified: boolean
  slogan: string
  about: string
  username: string
  shop_name: string
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
    isVerified: (state) => state.user?.is_verified ?? false,
    getSlogan: (state) => state.user?.slogan ?? '',
    getAbout: (state) => state.user?.about ?? '',
    getUsername: (state) => state.user?.username ?? '',
    getShopName: (state) => state.user?.shop_name ?? '',
    getPhone: (state) => state.user?.phone ?? '',
    getAddress: (state) => state.user?.address ?? '',
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

    async updateUser(username: string, phone: string, address: string, shop_name: string, about: string, slogan: string){
      if (!this.accessToken) return
      try {
        const user = await $fetch<any>("http://127.0.0.1:8000/api/user/update_me/", {
          method: 'POST',
          headers: { Authorization: `Bearer ${this.accessToken}` },
          body: { username, phone, address, shop_name, about, slogan }
        })
        this.user = user
      } catch {
        this.logout()
      }
    },

    async verifyAccount(id_card: File, commercial_register: File) {
      if (!this.accessToken) return
      try {
        const formData = new FormData()
        formData.append('id_card', id_card)
        formData.append('commercial_register', commercial_register)

        const res = await $fetch<{ detail: string }>("http://127.0.0.1:8000/api/user/verify_account/", {
          method: "POST",
          headers: { Authorization: `Bearer ${this.accessToken}` },
          body: formData
        })
        this.user!.is_verified = false // en attente de validation admin
      } catch (e: any) {
        throw new Error(e?.data?.detail || "Erreur de vérification du compte")
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

      // Optionnel : appel backend pour supprimer le cookie côté serveur
      $fetch("http://127.0.0.1:8000/api/user/logout/", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${this.accessToken}`,  // 👈 important
        },
        credentials: "include",
      }).catch(() => {})
      this.accessToken = null
      this.user = null

      goToMarket()
    },

    setAccessToken(token: string) {
      this.accessToken = token
    }

  },
})



