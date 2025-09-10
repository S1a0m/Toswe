<template>
  <aside
    class="fixed top-1/2 left-0 -translate-y-1/2 bg-white shadow-lg flex flex-col items-center justify-around py-6 px-3 rounded-r-2xl border border-gray-200 z-50"
  >
    <!-- Icône Market -->
    <Icon 
      name="uil:shop" 
      size="30"
      :class="[
        isActive('/market') ? 'text-black/60 bg-[#7D260F] p-2 rounded-lg' : 'text-[#7D260F] hover:text-[#5E1D0B]',
        'transition-colors mb-4 hover:cursor-pointer'
      ]"
      @click="goToMarket"
    />

    <!-- Icône Scanner -->
    <Icon 
      name="uil:qrcode-scan" 
      size="30"
      :class="[
        isActive('/scanner') ? 'text-black/60 bg-[#7D260F] p-2 rounded-lg' : 'text-[#7D260F] hover:text-[#5E1D0B]',
        'transition-colors mb-4 hover:cursor-pointer'
      ]"
      @click="goToScanner"
    />

    <!-- Icône Ajouter produit (uniquement vendeur) -->
    <Icon 
      v-if="auth.isSeller"
      name="uil:plus-circle" 
      size="30"
      :class="[
        isActive('/add') ? 'text-black/60 bg-[#7D260F] p-2 rounded-lg' : 'text-[#7D260F] hover:text-[#5E1D0B]',
        'transition-colors mb-4 hover:cursor-pointer'
      ]"
      @click="goToAddProduct"
    />

    <!-- Logo -->
    <div class="relative" v-if="route.path !== '/nehanda'">
      <img
        src="/assets/images/Nehanda.png"
        alt="Logo"
        class="w-10 h-10 object-contain hover:cursor-pointer"
        @click="goToNehanda"
      />

      <!-- Bulle animée -->
      <!--<transition name="fade-slide">
        <div
          v-if="showBubble"
          class="chat-bubble absolute left-12 top-1/2 -translate-y-1/2 bg-[#7D260F] shadow-md rounded-2xl px-4 py-2 text-sm text-white w-[220px] leading-snug"
        >
          Vous recherchez un produit en particulier ?<br />
          <span class="font-semibold">Je peux vous aider.</span>
        </div>
      </transition>-->
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

const showBubble = ref(false)

onMounted(() => {
  setTimeout(() => {
    showBubble.value = true
    setTimeout(() => {
      showBubble.value = false
    }, 6000)
  }, 1500)

  setInterval(() => {
    showBubble.value = true
    setTimeout(() => {
      showBubble.value = false
    }, 6000)
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

/* Style bulle + flèche */
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
