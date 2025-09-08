<template>
  <div
    class="flex flex-col items-center text-center bg-gradient-to-br from-white/95 to-white/85 backdrop-blur-lg 
           rounded-2xl shadow-lg border border-[#7D260F33]/30 overflow-hidden
           w-full max-w-xs sm:max-w-sm md:max-w-md
           hover:shadow-2xl hover:scale-105 transition-all duration-300"
  >
    <!-- Image / Logo principal (occupe la moitié de la carte) -->
    <div class="w-full h-40 sm:h-48 flex items-center justify-center bg-white">
      <img
        :src="imageSrc"
        :alt="shopName"
        class="w-full h-full object-contain drop-shadow"
      />
    </div>

    <!-- Contenu texte -->
    <div class="p-6">
      <!-- Nom de la boutique -->
      <h3 class="font-bold text-base sm:text-lg text-gray-900 mb-2">{{ shopName }}</h3>

      <!-- Nombre de clients fidèles -->
      <p class="text-sm text-gray-700 mb-4">
        <span class="font-semibold text-[#7D260F]">{{ loyalClients }}</span> abonnés
      </p>

      <!-- Boutons -->
      <div class="flex gap-3 mt-2 justify-center">
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
          class="px-4 py-2 bg-[#7D260F] text-white text-sm sm:text-base font-semibold 
                 rounded-full shadow-md hover:shadow-lg hover:bg-[#661f0c] 
                 transition-all duration-300 flex items-center gap-1"
          @click="goToShop"
        >
          Visiter
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { goToShop } from '@/utils/navigations';

const props = defineProps({
  imageSrc: {
    type: String,
    default: '/images/pagne.jpg'
  },
  shopName: {
    type: String,
    default: 'Nom de la boutique'
  },
  loyalClients: {
    type: Number,
    default: 128
  }
})

const becomeLoyalClient = () => {
  alert("Vous êtes devenu client fidèle 🎉");
}
</script>
