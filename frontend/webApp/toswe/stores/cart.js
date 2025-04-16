import { defineStore } from 'pinia'

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: []
  }),
  getters: {
    totalAmount: (state) => {
      return state.items.reduce((acc, item) => acc + item.price * item.quantity, 0)
    },
    totalInBasket: (state) => {
      return state.items.reduce((acc, item) => acc + item.quantity, 0)
    }    
  },
  actions: {
    addToCart(product) {
      const existing = this.items.find(p => p.id === product.id)
      if (existing) {
        existing.quantity += 1
      } else {
        this.items.push({ ...product, quantity: 1 })
      }
      this.saveToLocalStorage()
    },
    removeFromCart(id) {
      this.items = this.items.filter(p => p.id !== id)
      this.saveToLocalStorage()
    },
    updateQuantity(id, newQty) {
      const item = this.items.find(p => p.id === id)
      if (item) item.quantity = newQty
      this.saveToLocalStorage()
    },
    saveToLocalStorage() {
      localStorage.setItem('cart', JSON.stringify(this.items))
    },
    loadFromLocalStorage() {
      const saved = localStorage.getItem('cart')
      if (saved) this.items = JSON.parse(saved)
    }
  }
})
