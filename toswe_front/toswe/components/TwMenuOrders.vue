<template>
  <div v-if="auth.isSeller" class="w-full max-w-6xl mx-auto mb-4 bg-white/30 backdrop-blur-lg rounded-2xl shadow-lg p-4">
    <!-- Tabs -->
    <div class="flex justify-around border-b border-gray-300 mb-4">
      <button
        :class="activeTab === 'mine' ? activeClass : inactiveClass"
        @click="activeTab = 'mine'"
      >
        Mes commandes
      </button>
      <button
        :class="activeTab === 'clients' ? activeClass : inactiveClass"
        @click="activeTab = 'clients'"
      >
        Commandes clients
      </button>
    </div>

    <!-- Affichage commandes -->
    <div v-if="activeTab === 'mine'">
      <slot name="mine"></slot>
    </div>
    <div v-else>
      <slot name="clients"></slot>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const activeTab = ref('mine')

const activeClass = 'pb-2 border-b-2 border-[#7D260F] text-[#7D260F] font-semibold transition'
const inactiveClass = 'pb-2 text-gray-500 hover:text-[#7D260F] transition'
</script>
