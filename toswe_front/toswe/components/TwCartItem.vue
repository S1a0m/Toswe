<template>
  <div
    class="flex items-center gap-4 p-4 bg-white rounded-2xl shadow hover:shadow-xl transition-shadow duration-300 border border-gray-100"
  >
    <!-- Image produit -->
    <img
      :src="props.imageSrc"
      :alt="props.productName"
      @click="goToProductDetails(props.product_id)"
      class="w-20 h-20 object-cover rounded-2xl cursor-pointer border border-gray-200"
    />

    <!-- Infos produit -->
    <div class="flex-1 cursor-pointer" @click="goToProductDetails(props.product_id)">
      <h3 class="text-base font-semibold text-gray-900 truncate">{{ props.productName }}</h3>
      <p class="text-sm text-gray-500 mt-1">{{ props.price.toLocaleString() }} fcfa</p>
    </div>

    <!-- Quantité -->
    <div class="flex items-center gap-2">
      <button
        class="w-8 h-8 flex items-center justify-center border rounded-lg text-gray-600 hover:bg-gray-100 transition"
        @click="decrement"
      >-</button>
      <span class="w-6 text-center font-medium">{{ number }}</span>
      <button
        class="w-8 h-8 flex items-center justify-center border rounded-lg text-gray-600 hover:bg-gray-100 transition"
        @click="increment"
      >+</button>
    </div>

    <!-- Supprimer -->
    <button
      class="ml-4 text-red-500 hover:text-red-700 transition"
      @click="cart.removeFromCart(props.product_id)"
    >
      <Icon name="uil:trash-alt" class="w-5 h-5" />
    </button>
  </div>
</template>

<script setup>
import { useCartStore } from "@/stores/cart"
import { useNavigation } from '@/composables/useNavigation'

const { goToProductDetails } = useNavigation()

const props = defineProps({
  id: { type: Number, required: true },
  product_id: { type: Number, required: true },
  imageSrc: { type: String, required: true },
  productName: { type: String, required: true },
  price: { type: Number, required: true },
  quantity: { type: Number, required: true }
}) 

const cart = useCartStore()
 
const number = ref(props.quantity)

// 🔼 Fonction d'incrémentation
const increment = () => {
  number.value++
}

// 🔽 Fonction de décrémentation (min 1)
const decrement = () => {
  if (number.value > 1) {
    number.value--
  }
}

console.log("IMAGE SRC:", props.imageSrc)

// 🔄 Synchroniser avec le store
watch(number, (newVal) => {
  cart.updateQuantity(props.product_id, Number(newVal))
})
</script>

