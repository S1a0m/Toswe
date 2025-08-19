<template>
  <transition name="fade">
    <div
      v-if="visible"
      class="fixed inset-0 z-[2000] flex items-center justify-center px-4"
    >
      <!-- Overlay sombre -->
      <div
        class="absolute inset-0 bg-black/40 backdrop-blur-sm"
        @click="closePopup"
      ></div>

      <!-- Popup style glass -->
      <div
        class="relative z-10 rounded-2xl shadow-2xl w-full max-w-md p-6 border border-white/20 backdrop-blur-lg 
               sm:max-w-lg md:max-w-xl"
        style="background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.05));"
      >
        <!-- Bouton fermer -->
        <button
          @click="closePopup"
          class="absolute top-3 right-3 text-white/80 hover:text-white transition"
        >
          <Icon name="uil:times" class="w-5 h-5" />
        </button>

        <!-- Contenu -->
        <div class="flex flex-col items-center gap-4">
          <h3 class="text-lg sm:text-xl font-bold text-black drop-shadow mb-2 text-center">
            Contactez-nous
          </h3>

          <!-- Boutons de contact -->
          <div class="flex flex-col sm:flex-row gap-3 sm:gap-4 w-full justify-center">
            <!-- Facebook -->
            <a
              href="https://facebook.com/tonpage"
              target="_blank"
              class="flex items-center justify-center gap-2 px-4 py-2 rounded-xl 
                     bg-[#1877F2]/80 text-white font-semibold shadow-md 
                     hover:bg-[#1877F2] w-full sm:w-auto"
            >
              <Icon name="simple-icons:facebook" class="w-5 h-5" />
              Facebook
            </a>

            <!-- TikTok -->
            <a
              href="https://tiktok.com/@toncompte"
              target="_blank"
              class="flex items-center justify-center gap-2 px-4 py-2 rounded-xl 
                     bg-black/80 text-white font-semibold shadow-md 
                     hover:bg-black w-full sm:w-auto"
            >
              <Icon name="simple-icons:tiktok" class="w-5 h-5" />
              TikTok
            </a>

            <!-- WhatsApp -->
            <a
              href="https://wa.me/tonnumero"
              target="_blank"
              class="flex items-center justify-center gap-2 px-4 py-2 rounded-xl 
                     bg-[#25D366]/80 text-white font-semibold shadow-md 
                     hover:bg-[#25D366] w-full sm:w-auto"
            >
              <Icon name="simple-icons:whatsapp" class="w-5 h-5" />
              WhatsApp
            </a>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
const visible = ref(false)

const showPopup = () => {
  visible.value = true
}

const closePopup = () => {
  visible.value = false
}

// Exposé pour bouton externe
defineExpose({ showPopup })
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
