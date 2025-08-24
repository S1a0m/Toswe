<template>
  <div
    class="flex flex-col items-center text-center bg-gradient-to-br from-white/95 to-white/85 backdrop-blur-lg 
           rounded-2xl shadow-lg border border-[#7D260F33]/30 p-6 
           w-full max-w-xs sm:max-w-sm md:max-w-md
           hover:shadow-2xl hover:scale-105 transition-all duration-300"
  >
    <!-- Logo -->
    <div class="w-20 h-20 sm:w-24 sm:h-24 bg-white rounded-full flex items-center justify-center shadow-md mb-4">
      <img
        :src="imageSrc"
        :alt="shopName"
        class="w-12 h-12 sm:w-16 sm:h-16 object-contain drop-shadow"
      />
    </div>

    <!-- Nom de la boutique -->
    <h3 class="font-bold text-base sm:text-lg text-gray-900 mb-2">{{ shopName }}</h3>

    <!-- Nombre de clients fidèles -->
    <p class="text-sm text-gray-700 mb-4">
      <span class="font-semibold text-[#7D260F]">{{ loyalClients }}</span> loycs
    </p>

    <!-- Boutons -->
    <div class="flex gap-3 mt-2">
        <button
            class="flex items-center justify-center w-12 h-12 bg-white text-[#7D260F] 
                    border border-[#7D260F] rounded-full font-semibold
                    shadow-md hover:shadow-lg hover:bg-[#7D260F]/10 
                    transform transition-all duration-300 
                    active:scale-95 focus:outline-none focus:ring-2 focus:ring-[#7D260F]/50"
            @click="becomeLoyalClient"
            >
            <Icon 
                name="uil:heart" 
                class="transition-transform duration-300 hover:scale-125 hover:text-[#7D260F]"
            />
        </button>
      <button
        class="
               px-4 py-2 bg-[#7D260F] text-white text-sm sm:text-base font-semibold 
               rounded-full shadow-md hover:shadow-lg hover:bg-[#661f0c] transition-all duration-300 flex items-center gap-1"
        @click="goToShop"
      >
        Visiter
      </button>
    </div>
  </div>
</template>

<script setup>
import { goToShop } from '@/utils/navigations';

const props = defineProps({
  imageSrc: {
    type: String,
    default: '/images/img1.png'
  },
  shopName: {
    type: String,
    default: 'Nom de la boutique'
  },
  loyalClients: {
    type: Number,
    default: 128 // nombre de clients fidèles
  }
})

const becomeLoyalClient = () => {
  // Ici tu peux gérer l’action (API, toast de confirmation, etc.)
  alert("Vous êtes devenu client fidèle 🎉");
}
</script>

<style scoped>
:global(body) {
  background: linear-gradient(135deg, #1e1e1e 0%, #2a2a2a 100%);
}
</style>
