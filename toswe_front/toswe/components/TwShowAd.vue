<template>
  <section
    class="relative w-full mt-10 overflow-hidden rounded-3xl shadow-2xl bg-gradient-to-br 
           from-[#A84E2A]/90 to-[#7D260F]/80 text-white transition-all duration-500"
    @mouseenter="pauseCarousel"
    @mouseleave="resumeCarousel"
  >
    <!-- Conteneur principal -->
    <div class="relative h-[300px] sm:h-[380px] md:h-[460px]">
      <transition-group name="fade" tag="div" class="absolute inset-0 w-full h-full">
        <div
          v-for="(ad, index) in ads"
          :key="index"
          v-show="index === currentAd"
          class="absolute inset-0 flex flex-col justify-end items-center transition-all duration-700 ease-in-out"
        >
          <!-- Image principale -->
          <img
            :src="ad.image"
            :alt="ad.title"
            loading="lazy"
            class="w-full h-full object-cover object-center rounded-3xl opacity-95 animate-zoom-infinite"
          />

          <!-- Dégradé + texte -->
          <div
            class="absolute bottom-0 w-full bg-gradient-to-t from-black/70 via-black/50 to-transparent
                   text-center px-6 pb-12 pt-16"
          >
            <h3 class="text-2xl sm:text-3xl font-bold mb-2 drop-shadow-lg leading-tight">
              {{ ad.title }}
            </h3>
            <p
              class="text-white/90 text-sm sm:text-base truncate-lines mb-5 px-4 max-w-2xl mx-auto"
              :title="ad.text"
            >
              {{ ad.text }}
            </p>

            <!-- Bouton -->
            <button
              @click="goToAd(ad.link)"
              class="px-6 py-2.5 bg-white text-[#7D260F] font-semibold rounded-full shadow-lg 
                     hover:scale-105 hover:shadow-xl active:scale-95 transition-all duration-300 
                     focus:outline-none focus:ring-2 focus:ring-white/60"
            >
              {{ ad.button }}
            </button>
          </div>
        </div>
      </transition-group>
    </div>

    <!-- Indicateurs -->
    <div class="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2 z-20">
      <button
        v-for="(ad, index) in ads"
        :key="index"
        @click="currentAd = index"
        class="w-3 h-3 rounded-full transition-all duration-300"
        :class="currentAd === index ? 'bg-white scale-125' : 'bg-white/40 hover:bg-white/70'"
        :aria-label="`Aller à la publicité ${index + 1}`"
      ></button>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { navigateTo } from '#app'

const ads = [
  {
    title: "Faites vos emplettes avec Nehanda 🤖",
    text: "Votre assistante shopping intelligente vous aide à trouver, comparer et acheter les meilleurs produits locaux.",
    image: "/images/slide1.png",
    button: "Découvrir",
    link: "/nehanda",
  },
  {
    title: "Scannez et découvrez 📱",
    text: "Flashez un produit et accédez instantanément à sa fiche complète sur Tôswè. Simple et rapide.",
    image: "/images/slide2.png",
    button: "Essayer",
    link: "/scanner",
  },
  {
    title: "Vendez sans contrainte 💼",
    text: "Rejoignez notre réseau de vendeurs locaux et laissez Tôswè s’occuper de tout : vente, livraison, paiement.",
    image: "/images/slide3.png",
    button: "Devenir vendeur",
    link: "/become-seller",
  },
]

const currentAd = ref(0)
let intervalId

const nextAd = () => (currentAd.value = (currentAd.value + 1) % ads.length)
const startCarousel = () => (intervalId = setInterval(nextAd, 6000))
const pauseCarousel = () => clearInterval(intervalId)
const resumeCarousel = () => startCarousel()

onMounted(startCarousel)
onUnmounted(pauseCarousel)

const goToAd = (link) => navigateTo(link)
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 1s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Couper le texte proprement */
.truncate-lines {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

@keyframes zoom {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); } /* Zoom à 110% au milieu de l'animation */
}
.animate-zoom-infinite {
  animation: zoom 7s infinite ease-in-out;
}
</style>
