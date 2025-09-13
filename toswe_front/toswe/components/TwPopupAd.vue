<script setup>
import { ref, onMounted, onUnmounted } from "vue"
import { useNavigation } from '@/composables/useNavigation'

const { goToProductDetails } = useNavigation()

const ads = ref([])
const currentAdIndex = ref(0)
const visible = ref(false)
let intervalId = null

async function fetchAds() {
  try {
    const data = await $fetch("http://127.0.0.1:8000/api/ad/")
    ads.value = data.results || []
  } catch (err) {
    console.error("Erreur chargement ads:", err)
  }
}

function showNextAd() {
  if (!ads.value.length) return
  visible.value = true
  currentAdIndex.value = (currentAdIndex.value + 1) % ads.value.length
}

function closePopup() {
  visible.value = false
}

onMounted(async () => {
  await fetchAds()
  if (ads.value.length) {
    intervalId = setInterval(showNextAd, 60000) // toutes les 15s
    showNextAd()
  }
})

onUnmounted(() => {
  clearInterval(intervalId)
})
</script>

<template>
  <transition name="fade">
    <div
      v-if="visible && ads.length"
      class="fixed bottom-6 right-6 z-50 w-80 h-64 rounded-2xl shadow-2xl border border-white/20 overflow-hidden group"
    >
      <!-- Image full background -->
      <img
        v-if="ads[currentAdIndex]"
        :src="ads[currentAdIndex].image"
        :alt="ads[currentAdIndex].title"
        class="absolute inset-0 w-full h-full object-cover"
      />

      <!-- Overlay sombre lisible -->
      <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/50 to-transparent"></div>

      <!-- Bouton Close -->
      <button
        @click="closePopup"
        class="absolute top-3 right-3 w-8 h-8 flex items-center justify-center rounded-full bg-black/40 text-white transition-all duration-300 hover:bg-black hover:scale-110 hover:rotate-90 z-20"
      >
        <Icon name="uil:times" class="w-5 h-5" />
      </button>

      <!-- Contenu pub -->
      <div
        v-if="ads[currentAdIndex]"
        class="relative z-10 flex flex-col justify-end h-full p-4 text-left"
      >
        <h3 class="text-lg font-bold text-white drop-shadow mb-1 line-clamp-1">
          {{ ads[currentAdIndex].title }}
        </h3>
        <p class="text-sm text-white/80 line-clamp-2">
          {{ ads[currentAdIndex].description }}
        </p>

        <!-- Bouton visible seulement au hover -->
        <button
          class="mt-3 bg-[#7D260F]/90 text-white px-4 py-2 rounded-lg font-medium shadow-md opacity-0 group-hover:opacity-100 transition-all duration-300 hover:bg-[#5b1c0b]/90 hover:shadow-xl hover:scale-105"
          @click="goToProductDetails(ads[currentAdIndex].product)"
        >
          Visitez la boutique
        </button>
      </div>
    </div>
  </transition>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
