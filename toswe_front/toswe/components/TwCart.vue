<template>
  <button
    class="cursor-pointer fixed bottom-6 right-6 bg-[#7D260F] text-white p-4 rounded-full shadow-lg hover:bg-[#5E1D0B] transition-colors z-100"
    @click="goToCart"
  >
    <Icon name="ion:basket" size="28" />
    
    <!-- Badge du nombre d’articles -->
    <span
      v-if="cart.totalInBasket > 0"
      class="absolute -top-1 -right-1 bg-red-500 text-white text-xs font-bold px-2 py-0.5 rounded-full shadow"
    >
      {{ cart.totalInBasket }}
    </span>
  </button>
</template>

<script setup>
import { ref } from 'vue'
import { goToCart } from '@/utils/navigations'

import { useCartStore } from '@/stores/cart'

const cart = useCartStore()

onMounted(() => {
  cart.loadFromLocalStorage()
})
</script>
