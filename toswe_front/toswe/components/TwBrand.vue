<template>
  <div
    class="flex flex-col items-center text-center bg-gradient-to-br from-white/90 to-white/80 backdrop-blur-lg 
           rounded-2xl shadow-lg border border-[#7D260F33]/30 p-6 
           w-full max-w-xs sm:max-w-sm md:max-w-md
           hover:shadow-2xl hover:scale-105 transition-all duration-300"
  >
    <!-- Logo -->
    <div class="w-20 h-20 sm:w-24 sm:h-24 bg-white rounded-full flex items-center justify-center shadow-md mb-4">
      <img
        :src="imageSrc"
        :alt="brandName"
        class="w-12 h-12 sm:w-16 sm:h-16 object-contain drop-shadow"
      />
    </div>

    <!-- Nom -->
    <h3 class="font-bold text-base sm:text-lg text-gray-900 mb-1">{{ brandName }}</h3>

    <!-- Slogan -->
    <p class="text-xs sm:text-sm text-gray-600 italic mb-3">{{ slogan }}</p>

    <!-- Étoiles -->
    <div class="flex items-center gap-1 mb-2">
      <Icon
        v-for="n in 5"
        :key="n"
        name="uil:star"
        size="16"
        :class="n <= Math.floor(rating) ? 'text-[#7D260F]' : (n - rating < 1 ? 'text-[#7D260F]/60' : 'text-gray-300')"
      />
      <span class="text-xs text-gray-500">({{ rating.toFixed(1) }})</span>
    </div>

    <!-- Bouton -->
    <button
      class="hover:cursor-pointer mt-3 px-3 py-1.5 sm:px-4 sm:py-2 bg-gradient-to-r bg-[#7D260F] 
             text-white text-sm sm:text-base font-semibold rounded-full shadow-md hover:shadow-lg 
             hover:bg-[#661f0c] transition-all duration-300 flex items-center"
      @click="goToShop"
    >
      <Icon name="carbon:chevron-right" size="16" class="mr-1" /> <span>Boutique</span>
    </button>
  </div>
</template>


<script setup>
import { goToShop } from '@/utils/navigations';
const props = defineProps({
  imageSrc: {
    type: String,
    default: '/assets/images/img1.png'
  },
  brandName: {
    type: String,
    default: 'Nom de la marque'
  },
  slogan: {
    type: String,
    default: 'Votre slogan ici'
  },
  rating: {
    type: Number,
    default: 4.5 // sur 5
  }
})
</script>

<style scoped>
/* Fond général sombre premium */
:global(body) {
  background: linear-gradient(135deg, #1e1e1e 0%, #2a2a2a 100%);
}
</style>
