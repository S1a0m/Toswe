<template>
  <section
    class="flex flex-col justify-center items-center min-h-[70vh] bg-[#7D260F] text-white font-[Kumbh_Sans] px-6 py-20 relative overflow-hidden"
  >
    <!-- Contenu principal -->
    <div class="relative z-10 flex flex-col items-center w-full">
      <!-- Titre -->
      <h1
        class="text-3xl md:text-5xl font-bold mb-14 text-center font-[Kenia] leading-tight drop-shadow-xl"
      >
        Nous vendons pour vous.
      </h1>

      <!-- Cartes -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-10 w-full max-w-5xl">
        <!-- Carte Nehanda -->
        <div
          class="group bg-gradient-to-br from-white/10 to-white/5 backdrop-blur-xl rounded-3xl p-8 flex flex-col items-center text-center shadow-lg hover:shadow-2xl hover:scale-[1.03] transition-all duration-300 border border-white/20 cursor-pointer"
          @click="goToNehanda"
        >
          <div class="relative w-full h-40 mb-5">
            <img
              src="/assets/images/Nehanda.png"
              alt="Nehanda"
              class="absolute inset-0 w-full h-full object-cover rounded-2xl"
            />
            <div class="absolute inset-0 bg-black/30 rounded-2xl group-hover:bg-black/20 transition"></div>
          </div>
          <Icon name="uil:robot" size="56" class="text-white drop-shadow-md" />
          <h3 class="text-xl font-semibold mt-4">Faites vos emplettes avec Nehanda</h3>
          <p class="text-sm text-white/80 mt-2">
            Votre assistante shopping intelligente.
          </p>
        </div>

        <!-- Carte Scanner -->
        <div
          class="group bg-gradient-to-br from-white/10 to-white/5 backdrop-blur-xl rounded-3xl p-8 flex flex-col items-center text-center shadow-lg hover:shadow-2xl hover:scale-[1.03] transition-all duration-300 border border-white/20 cursor-pointer"
          @click="goToScanner"
        >
          <div class="relative w-full h-40 mb-5">
            <img
              src="/assets/images/insta.jpeg"
              alt="Scanner"
              class="absolute inset-0 w-full h-full object-cover rounded-2xl"
            />
            <div class="absolute inset-0 bg-black/30 rounded-2xl group-hover:bg-black/20 transition"></div>
          </div>
          <Icon name="uil:qrcode-scan" size="56" class="text-white drop-shadow-md" />
          <h3 class="text-xl font-semibold mt-4">Scannez un produit de chez Tôswè</h3>
          <p class="text-sm text-white/80 mt-2">
            Rapide. Simple. Intelligent.
          </p>
        </div>
      </div>

      <!-- Bouton CTA -->
      <button
        @click="goToMarket"
        class="mt-14 px-10 py-4 rounded-lg bg-gradient-to-r from-white to-white/90 text-[#7D260F] font-semibold text-lg shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300"
      >
        Commencer mes achats
      </button>

      <!-- Accroche -->
      <p
        class="text-base md:text-lg mt-10 max-w-2xl text-center leading-relaxed text-white/90"
      >
        Achetez local et optimisez votre expérience d'achat grâce à nos solutions
        modernes et intuitives.
      </p>
    </div>
  </section>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

const goToNehanda = () => {
  if (auth.isAuthenticated) {
    navigateTo({ path: '/nehanda' })
  } else {
    navigateTo({ path: '/auth' })
  }
}

const goToScanner = () => {
  if (auth.isAuthenticated) {
    navigateTo({ path: '/scanner' })
  } else {
    navigateTo({ path: '/auth' })
  }
}

const goToMarket = () => {
  navigateTo({ path: '/market' })
}
</script>
