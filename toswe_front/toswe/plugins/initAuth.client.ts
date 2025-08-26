import { useAuthStore } from '~/stores/auth'
import { useCartStore } from '~/stores/cart'

export default defineNuxtPlugin(async () => {
  const auth = useAuthStore()
  const cart = useCartStore()

  // On tente d'initialiser l'utilisateur
  await auth.initialize()
  // await cart.initCart()
})
