<template>
  <button
    class="group cursor-pointer fixed bottom-6 right-6 bg-[#7D260F] text-white 
           p-4 rounded-full shadow-lg hover:bg-[#5E1D0B] 
           transition-all duration-300 z-5000 flex items-center justify-center"
    @click="goToCart"
  >
    <!-- Icône panier -->
    <Icon 
      name="mdi:cart-outline" 
      size="28" 
      class="group-hover:scale-110 transition-transform duration-200"
    />

    <!-- Badge du nombre d’articles -->
    <span
      v-if="cart.totalInBasket > 0"
      class="absolute -top-1 -right-1 bg-red-500 text-white 
             text-xs font-bold w-6 h-6 flex items-center justify-center
             rounded-full shadow-md animate-pulse"
    >
      {{ cart.totalInBasket }}
    </span>
  </button>
</template>

<script setup>
import { onMounted } from 'vue'
import { goToCart } from '@/utils/navigations'
import { useCartStore } from '@/stores/cart'

const cart = useCartStore()

onMounted(() => {
  cart.loadFromLocalStorage()
})
</script>
