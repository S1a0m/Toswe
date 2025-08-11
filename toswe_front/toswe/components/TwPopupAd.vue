<template>
  <transition name="fade">
    <div
      v-if="visible"
      class="fixed bottom-6 right-6 z-50 rounded-2xl shadow-2xl w-80 p-4 border border-white/20 backdrop-blur-lg"
      style="background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.05));"
    >
      <!-- Bouton fermer -->
      <button
        @click="closePopup"
        class="absolute top-2 right-2 text-white/80 hover:text-white transition"
      >
        <Icon name="uil:times" class="w-5 h-5" />
      </button>

      <!-- Contenu pub -->
      <div class="flex flex-col items-center text-center">
        <img
          src="/assets/images/produit.jpg"
          alt="Publicité"
          class="w-full h-40 object-cover rounded-xl mb-4 border border-white/20 shadow-md"
        />
        <h3 class="text-lg font-bold text-black drop-shadow mb-2">
          {{ title }}
        </h3>
        <p class="text-sm text-black/80 mb-4 leading-relaxed">
          {{ description }}
        </p>

        <a
          :href="ctaLink"
          class="bg-[#7D260F]/90 backdrop-blur-sm text-white px-5 py-2 rounded-lg font-semibold hover:bg-[#5b1c0b]/90 transition-all shadow-lg"
        >
          {{ ctaText }}
        </a>
      </div>
    </div>
  </transition>
</template>

<script setup>
const props = defineProps({
  title: { type: String, required: true },
  description: { type: String, required: true },
  ctaText: { type: String, default: 'En savoir plus' },
  ctaLink: { type: String, required: true },
  delay: { type: Number, default: 60000 }
})

const visible = ref(false)
let intervalId = null

const showPopup = () => {
  visible.value = true
}

const closePopup = () => {
  visible.value = false
}

onMounted(() => {
  setTimeout(showPopup, props.delay)
  intervalId = setInterval(showPopup, props.delay)
})

onUnmounted(() => {
  clearInterval(intervalId)
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
