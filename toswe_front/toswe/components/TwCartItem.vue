<template>
  <div class="flex items-center gap-4 p-4 border-b border-gray-200">
    <!-- Image produit -->
    <img
      :src="props.imageSrc"
      :alt="props.productName"
      @click="goToProductDetails(props.product_id)"
      class="w-16 h-16 object-cover rounded cursor-pointer"
    />

    <!-- Infos produit -->
    <div class="flex-1 cursor-pointer" @click="goToProductDetails(props.product_id)">
      <h3 class="text-base font-semibold text-gray-900">{{ props.productName }}</h3>
      <p class="text-sm text-gray-500">{{ props.price.toLocaleString() }} fcfa</p>
    </div>

    <!-- Quantité -->
    <div class="flex items-center gap-2">
      <button
        class="px-2 py-1 border rounded text-gray-600 hover:bg-gray-100"
        @click="number--"
      >-</button>
      <span class="w-6 text-center">{{ number }}</span>
      <button
        class="px-2 py-1 border rounded text-gray-600 hover:bg-gray-100"
        @click="number++"
      >+</button>
    </div>

    <!-- Supprimer -->
    <button
      class="ml-4 text-red-500 hover:text-red-700"
      @click="cart.removeFromCart(props.product_id)"
    >
      <Icon name="uil:trash" class="w-5 h-5" />
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

watch(number, (newVal) => {
  cart.updateQuantity(props.id, Number(newVal))
})
</script>
