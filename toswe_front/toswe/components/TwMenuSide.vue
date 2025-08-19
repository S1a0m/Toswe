<template>
  <aside
    class="fixed top-1/2 left-0 -translate-y-1/2 bg-white shadow-lg flex flex-col items-center justify-around py-6 px-3 rounded-r-2xl border border-gray-200 z-50"
  >
    <!-- Logo -->
    <img
      src="/assets/images/Nehanda.png"
      alt="Logo"
      class="w-10 h-10 object-contain mb-4 hover:cursor-pointer"
      @click="goToNehanda"
    />

    <!-- Icônes -->
    <Icon name="uil:qrcode-scan" size="30" class="text-[#7D260F] hover:text-[#5E1D0B] transition-colors mb-4 hover:cursor-pointer" @click="goToScanner"/>
    <Icon name="uil:plus" size="30" class="text-[#7D260F] hover:text-[#5E1D0B] transition-colors hover:cursor-pointer" v-if="auth.isSeller"/>
  </aside>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { goToNehanda, goToScanner } from "@/utils/navigations";

const auth = useAuthStore()
</script>