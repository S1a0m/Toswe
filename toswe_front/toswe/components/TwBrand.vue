<template>
  <div
    class="flex flex-col items-center text-center bg-gradient-to-br from-white/90 to-white/80 backdrop-blur-lg rounded-2xl shadow-lg border border-[#7D260F33]/30 p-6 w-56 hover:shadow-2xl hover:scale-105 transition-all duration-300"
  >
    <!-- Logo -->
    <div class="w-24 h-24 bg-white rounded-full flex items-center justify-center shadow-md mb-4">
      <img
        :src="imageSrc"
        :alt="brandName"
        class="w-16 h-16 object-contain drop-shadow"
      />
    </div>

    <!-- Nom -->
    <h3 class="font-bold text-lg text-gray-900 mb-1">{{ brandName }}</h3>

    <!-- Slogan -->
    <p class="text-sm text-gray-600 italic mb-3">{{ slogan }}</p>

    <!-- Étoiles -->
    <div class="flex items-center gap-1 mb-2">
      <Icon
        v-for="n in 5"
        :key="n"
        name="uil:star"
        size="18"
        :class="n <= Math.floor(rating) ? 'text-[#7D260F]' : (n - rating < 1 ? 'text-[#7D260F]/60' : 'text-gray-300')"
      />
      <span class="text-xs text-gray-500">({{ rating.toFixed(1) }})</span>
    </div>

    <!-- Bouton -->
    <button
      class="mt-3 px-4 py-2 bg-gradient-to-r bg-[#7D260F] text-white font-semibold rounded-full shadow-md hover:shadow-lg hover:bg-[#661f0c] transition-all duration-300"
    > <!--from-yellow-500 to-yellow-400 text-black-->
      Voir la marque
    </button>
  </div>
</template>

<script setup>
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
