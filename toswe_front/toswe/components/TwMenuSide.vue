<template>
  <aside
    class="fixed top-1/2 left-3 -translate-y-1/2 
           bg-white/80 backdrop-blur-md shadow-xl 
           flex flex-col items-center gap-5 
           py-6 px-3 rounded-2xl border border-gray-200 
           z-50"
  >
    <!-- Icône Market -->
    <button
      @click="goToMarket"
      :class="iconButtonClass('/market')"
      aria-label="Market"
    >
      <Icon name="uil:shop" size="22" />
    </button>

    <!-- Icône Scanner -->
    <button
      @click="goToScanner"
      :class="iconButtonClass('/scanner')"
      aria-label="Scanner"
    >
      <Icon name="uil:qrcode-scan" size="22" />
    </button>

    <!-- Icône Ajouter produit (uniquement vendeur) -->
    <button
      v-if="auth.isSeller"
      @click="goToAddProduct"
      :class="iconButtonClass('/add')"
      aria-label="Ajouter un produit"
    >
      <Icon name="uil:plus-circle" size="22" />
    </button>

    <!-- Logo Nehanda -->
    <div class="relative" v-if="route.path !== '/nehanda'">
      <img
        src="/assets/images/Nehanda.png"
        alt="Logo"
        class="w-11 h-11 object-contain cursor-pointer hover:scale-110 transition-transform duration-300"
        @click="goToNehanda"
      />

      <!-- Bulle animée -->
      <transition name="fade-slide">
        <div
          v-if="showBubble"
          class="chat-bubble absolute left-14 top-1/2 -translate-y-1/2 
                 bg-[#7D260F] shadow-md rounded-2xl px-4 py-2 
                 text-sm text-white w-[220px] leading-snug animate-bounce"
        >
          Vous recherchez un produit en particulier ?<br />
          <span class="font-semibold">Je peux vous aider.</span>
        </div>
      </transition>
    </div>
  </aside>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { goToNehanda, goToScanner, goToAddProduct, goToMarket } from "@/utils/navigations";
import { useRoute } from 'vue-router'
import { ref, onMounted } from "vue"

const auth = useAuthStore()
const route = useRoute()

const isActive = (path) => route.path.startsWith(path)

const iconButtonClass = (path) => [
  "w-12 h-12 flex items-center justify-center rounded-full transition-all duration-300 shadow-md",
  isActive(path)
    ? "bg-[#7D260F] text-white scale-110 ring-2 ring-[#7D260F]/40"
    : "bg-white text-[#7D260F] hover:bg-[#f8ebe8] hover:scale-110"
]

const showBubble = ref(false)

onMounted(() => {
  setTimeout(() => {
    showBubble.value = true
    setTimeout(() => (showBubble.value = false), 6000)
  }, 1500)

  setInterval(() => {
    showBubble.value = true
    setTimeout(() => (showBubble.value = false), 6000)
  }, 20000)
})
</script>

<style scoped>
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.5s ease;
}
.fade-slide-enter-from {
  opacity: 0;
  transform: translateX(-20px);
}
.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

/* Bulle Nehanda + flèche */
.chat-bubble {
  position: absolute;
}
.chat-bubble::before {
  content: "";
  position: absolute;
  top: 50%;
  left: -10px;
  transform: translateY(-50%);
  border-width: 6px;
  border-style: solid;
  border-color: transparent #7D260F transparent transparent;
}
</style>
