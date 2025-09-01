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
    <img
      src="/assets/images/Nehanda.png"
      alt="Logo"
      class="w-10 h-10 object-contain hover:cursor-pointer"
      @click="goToNehanda"
    />
  </aside>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { goToNehanda, goToScanner, goToAddProduct, goToMarket } from "@/utils/navigations";
import { useRoute } from 'vue-router'

const auth = useAuthStore()
const route = useRoute()

const isActive = (path) => route.path.startsWith(path)
</script>
