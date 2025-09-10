import { defineStore } from "pinia"
import { useAuthStore } from "./auth"

interface CartItem {
  product_id: number | string
  name: string
  price: number
  quantity: number
  main_image: string
  [key: string]: any
}


export const useCartStore = defineStore("cart", {
  state: () => ({
    items: [] as CartItem[],
    isSynching: false, // pour éviter les boucles de sync
  }),

  getters: {
    totalAmount: (state): number =>
      state.items.reduce((acc, item) => acc + item.price * item.quantity, 0),
    totalInBasket: (state): number =>
      state.items.reduce((acc, item) => acc + item.quantity, 0),
  },

  actions: {
    async initCart() {
      // const { $apiFetch } = useNuxtApp()
      const auth = useAuthStore()

      if (auth.isAuthenticated) {
        // Charger depuis le serveur
        try {
          const cart = await $fetch(`http://127.0.0.1:8000/api/cart/me/`, {
            headers: { Authorization: `Bearer ${auth.accessToken}` },
            credentials: "include",
          })
          this.items = cart.items || []
          this.saveToLocalStorage()
        } catch (err) {
          console.warn("Impossible de charger le panier du serveur, fallback localStorage")
          this.loadFromLocalStorage()
        }
      } else {
        // Non connecté → uniquement local
        this.loadFromLocalStorage()
      }
    },

    addToCart(product: Partial<CartItem> & { product_id: number | string; name: string; price: number; main_image: string }) {
      const existing = this.items.find((p) => p.product_id === product.product_id)
      if (existing) {
        existing.quantity += 1
      } else {
        this.items.push({ ...product, quantity: 1 } as CartItem)
      }
      this.persist()
    },

    removeFromCart(product_id: number | string) {
      this.items = this.items.filter((p) => p.product_id !== product_id)
      this.persist()
    },

    updateQuantity(product_id: number | string, newQty: number) {
      const item = this.items.find((p) => p.product_id === product_id)
      if (item) item.quantity = newQty
      this.persist()
    },

    persist() {
      this.saveToLocalStorage()
      this.syncWithServer()
    },

    saveToLocalStorage() {
      if (!process.client) return
      try {
        localStorage.setItem("cart", JSON.stringify(this.items))
      } catch (error) {
        console.error("Erreur lors de la sauvegarde du panier", error)
      }
    },


    loadFromLocalStorage() {
      try {
        const saved = localStorage.getItem("cart")
        if (!saved) return
        const parsed: unknown = JSON.parse(saved)

        if (
          Array.isArray(parsed) &&
          parsed.every(
            (item) =>
              item &&
              typeof item === "object" &&
              "product_id" in item &&
              "name" in item &&
              "price" in item &&
              "quantity" in item
          )
        ) {
          this.items = parsed as CartItem[]
        } else {
          console.warn("Données du panier invalides dans localStorage")
        }
      } catch (error) {
        console.error("Erreur lors du chargement du panier", error)
      }
    },

    async syncWithServer() {
      const auth = useAuthStore()
      if (!auth.isAuthenticated || this.isSynching) return

      this.isSynching = true
      const { $apiFetch } = useNuxtApp()
      try {
        await $apiFetch(`http://127.0.0.1:8000/api/cart/sync/`, {
          method: "POST",
          body: { items: this.items },
        })
      } catch (err) {
        console.error("Erreur lors de la synchronisation du panier", err)
      } finally {
        this.isSynching = false
      }
    },
  },
})
