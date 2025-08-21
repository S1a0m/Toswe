<template>
  <div v-if="auth.isSeller" class="w-full max-w-3xl mx-auto mb-4 bg-white/30 backdrop-blur-lg rounded-2xl shadow-lg p-4">
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

    <!-- Contenu 
    <div v-if="activeTab === 'mine'" class="space-y-3">
      <div v-for="order in myOrders" :key="order.id"
        class="flex justify-between items-center bg-white/60 rounded-xl p-3 shadow-md hover:shadow-lg transition">
        <div>
          <h4 class="font-semibold text-gray-800">{{ order.product }}</h4>
          <p class="text-sm text-gray-500">Quantité : {{ order.qty }}</p>
        </div>
        <span class="text-sm font-bold text-[#7D260F]">{{ order.status }}</span>
      </div>
    </div>

    <div v-else class="space-y-3">
      <div v-for="order in clientOrders" :key="order.id"
        class="flex justify-between items-center bg-white/60 rounded-xl p-3 shadow-md hover:shadow-lg transition">
        <div>
          <h4 class="font-semibold text-gray-800">{{ order.client }}</h4>
          <p class="text-sm text-gray-500">Commande : {{ order.product }}</p>
        </div>
        <span class="text-sm font-bold text-green-600">{{ order.status }}</span>
      </div>
    </div>-->
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

const activeTab = ref('mine')

// Simulation données
const myOrders = [
  { id: 1, product: 'Chaussures Nike', qty: 2, status: 'En cours' },
  { id: 2, product: 'T-shirt coton', qty: 1, status: 'Livré' },
]

const clientOrders = [
  { id: 1, client: 'Alice', product: 'Sac en cuir', status: 'En attente' },
  { id: 2, client: 'Jean', product: 'Casque audio', status: 'Confirmé' },
]

const activeClass =
  'pb-2 border-b-2 border-[#7D260F] text-[#7D260F] font-semibold transition'
const inactiveClass =
  'pb-2 text-gray-500 hover:text-[#7D260F] transition'
</script>
