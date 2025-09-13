<template>
  <div
    class="group relative w-full max-w-xs sm:max-w-sm md:max-w-md overflow-hidden rounded-2xl shadow-lg border border-[#7D260F33]/30 hover:shadow-2xl transition-all duration-300"
  >
    <!-- Image/logo -->
    <img
      :src="imageSrc"
      :alt="brandName"
      class="w-full h-72 object-contain bg-white p-6"
    />

    <!-- Overlay infos (slogan + rating) -->
    <div
      class="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/70 via-black/40 to-transparent text-white px-4 py-3"
    >
      <h3 class="font-semibold text-lg truncate">{{ brandName }}</h3>
      <p class="text-sm italic line-clamp-1 opacity-90">{{ slogan }}</p>

      <!-- Étoiles -->
      <div class="flex items-center gap-1 mt-1">
        <Icon
          v-for="n in 5"
          :key="n"
          name="uil:star"
          size="16"
          :class="n <= Math.floor(rating) ? 'text-yellow-400' : (n - rating < 1 ? 'text-yellow-300/60' : 'text-gray-500')"
        />
        <span class="text-xs text-gray-200">({{ rating.toFixed(1) }})</span>
      </div>
    </div>

    <!-- Overlay hover (Visitez) -->
    <div
      class="absolute inset-0 bg-black/70 flex items-center justify-center text-white text-lg font-semibold opacity-0 group-hover:opacity-100 transition-all duration-300 cursor-pointer"
      @click="goToShopDetails(sellerId)"
    >
      <Icon name="carbon:chevron-right" size="20" class="mr-2" /> Visitez
    </div>
  </div>
</template>

<script setup>
import { useNavigation } from '@/composables/useNavigation'

const props = defineProps({
  imageSrc: { type: String, default: '@/assets/images/img1.png' },
  brandName: { type: String, default: 'Nom de la marque' },
  slogan: { type: String, default: 'Votre slogan ici' },
  rating: { type: Number, default: 4.5 },
  sellerId: { type: Number, required: true }
})

const { goToShopDetails } = useNavigation()
</script>
