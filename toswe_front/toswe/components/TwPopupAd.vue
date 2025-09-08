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
    intervalId = setInterval(showNextAd, 15000) // toutes les 15s
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
      class="fixed bottom-6 right-6 z-50 rounded-2xl shadow-2xl w-80 p-4 border border-white/20 backdrop-blur-lg"
      style="background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.05));"
    >
      <button
        @click="closePopup"
        class="absolute top-2 right-2 text-black/80 hover:text-black"
      >
        <Icon name="uil:times" class="w-5 h-5" />
      </button>

      <div v-if="ads[currentAdIndex]" class="flex flex-col items-center text-center">
        <img
          :src="ads[currentAdIndex].image"
          :alt="ads[currentAdIndex].title"
          class="w-full h-40 object-cover rounded-xl mb-4 border border-white/20 shadow-md"
        />
        <h3 class="text-lg font-bold text-black drop-shadow mb-2">
          {{ ads[currentAdIndex].title }}
        </h3>
        <p class="text-sm text-black/80 mb-4">
          {{ ads[currentAdIndex].description }}
        </p>

        <button
          class="bg-[#7D260F]/90 text-white px-5 py-2 rounded-lg font-semibold hover:bg-[#5b1c0b]/90 transition-all shadow-lg"
          @click="goToProductDetails(ads[currentAdIndex].product)"
        >
          Voir les offres
        </button>
      </div>
    </div>
  </transition>
</template>
