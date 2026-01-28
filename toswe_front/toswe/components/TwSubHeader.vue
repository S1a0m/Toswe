<template>
  <section
    class="relative flex flex-col md:flex-row justify-center items-center min-h-screen text-white font-[Kumbh_Sans] overflow-hidden px-6 md:px-12"
  >
    <!-- 🎥 Vidéo de fond -->
    <video
      autoplay
      muted
      loop
      playsinline
      class="absolute inset-0 w-full h-full object-cover"
    >
      <source src="/videos/bck.mp4" type="video/mp4" />
      Votre navigateur ne supporte pas les vidéos HTML5.
    </video>

    <!-- Dégradé overlay -->
    <div
      class="absolute inset-0 bg-gradient-to-b md:bg-gradient-to-r from-black/70 via-[#7D260F]/85 to-[#7D260F]/95"
    ></div>

    <!-- Contenu principal -->
    <div class="relative z-10 flex flex-col md:flex-row items-center md:items-stretch justify-between w-full max-w-6xl gap-10">
      <!-- 🩸 Partie gauche : texte -->
      <div class="text-center md:text-left md:w-1/2 flex flex-col justify-center">
        <h1
          class="text-4xl md:text-6xl font-bold mb-6 font-[Kenia] leading-tight tracking-tight"
        >
          Nous vendons pour vous.
          <div class="mt-2">100% made in <span class="text-[#F59E0B]">Africa</span><Icon name="mdi:flag" /></div>
        </h1>

        <p class="text-lg md:text-xl text-white/90 mb-10 max-w-lg mx-auto md:mx-0">
          Soyez parmi les premiers vendeurs à tester gratuitement la plateforme
          <span class="font-semibold">Tôswè</span> — votre allié pour vendre local,
          plus facilement et plus loin.
        </p>

        <button
          @click="goToMarket"
          class="mt-4 px-8 py-4 rounded-full bg-white text-[#7D260F] font-semibold text-lg shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300 w-fit mx-auto md:mx-0"
        >
          Commencer mes achats
        </button>
      </div>

      <!-- 🌀 Partie droite : carrousel -->
      <div class="relative w-full md:w-1/2 max-w-xl h-[420px] overflow-hidden rounded-3xl shadow-2xl">
        <transition-group name="fade" tag="div" class="relative w-full h-full">
          <div
            v-for="(item, index) in slides"
            :key="index"
            v-show="index === currentSlide"
            class="absolute inset-0 flex flex-col justify-center items-center text-center transition-all duration-700 ease-in-out px-6"
          >
            <img
              :src="item.image"
              :alt="item.title"
              class="w-full h-64 object-cover rounded-2xl mb-6"
            />
            <h3 class="text-2xl font-semibold mb-2">{{ item.title }}</h3>
            <p class="text-white/80 text-base max-w-md">{{ item.text }}</p>
          </div>
        </transition-group>

        <!-- Indicateurs -->
        <div class="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex space-x-2">
          <button
            v-for="(item, i) in slides"
            :key="i"
            class="w-3 h-3 rounded-full"
            :class="i === currentSlide ? 'bg-white' : 'bg-white/40'"
            @click="currentSlide = i"
          ></button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

// Slides du carrousel
const slides = [
  {
    title: 'Faites vos emplettes avec Nehanda',
    text: 'Votre assistante shopping intelligente vous guide dans vos choix et vous simplifie les achats.',
    image: '/images/slide1.png',
  },
  {
    title: 'Scannez et découvrez',
    text: 'Scannez un produit local et découvrez ses informations instantanément.',
    image: '/images/slide2.png',
  },
  {
    title: 'Vendez sans contrainte',
    text: 'Créez votre boutique, publiez vos produits et laissez Tôswè gérer la livraison.',
    image: '/images/slide3.png',
  },
]

const currentSlide = ref(0)

onMounted(() => {
  setInterval(() => {
    currentSlide.value = (currentSlide.value + 1) % slides.length
  }, 6000)
})

const goToMarket = () => navigateTo('/market')
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 1s ease, transform 1s ease;
}
.fade-enter-from {
  opacity: 0;
  transform: translateY(20px);
}
.fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
