<template>
  <button
    class="fixed bottom-6 right-6 bg-[#7D260F] text-white p-4 rounded-full shadow-lg hover:bg-[#5E1D0B] transition-colors z-50"
  >
    <Icon name="ion:basket" size="28" />
    
    <!-- Badge du nombre d’articles -->
    <span
      v-if="cartCount > 0"
      class="absolute -top-1 -right-1 bg-red-500 text-white text-xs font-bold px-2 py-0.5 rounded-full shadow"
    >
      {{ cartCount }}
    </span>
  </button>
</template>

<script setup>
import { ref } from 'vue'

const cartCount = ref(3) // Exemple : nombre d'articles
</script>
