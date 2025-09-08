import { useAuthStore } from '~/stores/auth'
import { useCartStore } from '~/stores/cart'
import { useInteractionsStore } from '~/stores/interactions'

export default defineNuxtPlugin(async () => {
  const auth = useAuthStore()
  const cart = useCartStore()
  const interactions = useInteractionsStore()

  await auth.initialize()
  await cart.initCart()

  interactions.initialize()
})
