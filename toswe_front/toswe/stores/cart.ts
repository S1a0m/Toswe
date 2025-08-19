import { defineStore } from 'pinia'

interface CartItem {
  id: number | string
  name: string
  price: number
  quantity: number
  [key: string]: any
}

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [] as CartItem[]
  }),
  getters: {
    totalAmount: (state): number =>
      state.items.reduce((acc, item) => acc + item.price * item.quantity, 0),
    totalInBasket: (state): number =>
      state.items.reduce((acc, item) => acc + item.quantity, 0)
  },
  actions: {
    addToCart(product: Partial<CartItem> & { id: number | string; name: string; price: number }) {
    const existing = this.items.find(p => p.id === product.id)
    if (existing) {
        existing.quantity += 1
    } else {
        this.items.push({ ...product, quantity: 1 } as CartItem)
    }
    this.saveToLocalStorage()
    },
    removeFromCart(id: number | string) {
      this.items = this.items.filter(p => p.id !== id)
      this.saveToLocalStorage()
    },
    updateQuantity(id: number | string, newQty: number) {
      const item = this.items.find(p => p.id === id)
      if (item) item.quantity = newQty
      this.saveToLocalStorage()
    },
    saveToLocalStorage() {
      try {
        localStorage.setItem('cart', JSON.stringify(this.items))
      } catch (error) {
        console.error('Erreur lors de la sauvegarde du panier', error)
      }
    },
    loadFromLocalStorage() {
      try {
        const saved = localStorage.getItem('cart')
        if (!saved) return

        const parsed: unknown = JSON.parse(saved)

        // Validation simple : vérifier que c'est un tableau et que chaque élément a id, name, price, quantity
        if (Array.isArray(parsed) && parsed.every(item =>
          item && typeof item === 'object' &&
          'id' in item && 'name' in item && 'price' in item && 'quantity' in item
        )) {
          this.items = parsed as CartItem[]
        } else {
          console.warn('Données du panier invalides dans localStorage')
        }
      } catch (error) {
        console.error('Erreur lors du chargement du panier', error)
      }
    }
  }
})
