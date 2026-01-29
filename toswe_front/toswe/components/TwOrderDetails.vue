<template>
  <section
    class="bg-white rounded-2xl shadow-md p-6 space-y-6 max-w-6xl mx-auto transition hover:shadow-lg"
  >
    <!-- Header -->
    <div class="flex justify-between items-start border-b pb-4">
      <div class="space-y-1">
        <h2 class="text-xl font-semibold text-gray-900 flex items-center gap-2">
          <span class="text-gray-400">Commande #{{ order.id }}</span>
        </h2>
        <p class="text-sm text-gray-500">{{ order.created_at }}</p>
        <span
          class="mt-1 px-3 py-1 text-xs font-medium rounded-full"
          :class="statusClasses[order.status] || statusClasses.default"
        >
          {{ order.status }}
        </span>
      </div>
      <p class="text-xl font-bold text-gray-900">
        {{ formatFcfa(orderTotal) }} fcfa
      </p>
    </div>

    <!-- Produits -->
    <div class="space-y-4">
      <div
        v-for="(item, index) in order.items"
        :key="index"
        class="flex items-start gap-4 border-b pb-4 last:border-none"
      >
        <img
          :src="`http://127.0.0.1:8000${item.main_image}`"
          :alt="item.product.name"
          class="w-16 h-16 object-cover rounded-lg shadow-sm"
        />

        <div class="flex-1 space-y-1">
          <p class="font-medium text-gray-900">
            {{ item.product.name }}
          </p>

          <p class="text-sm text-gray-500">
            {{ item.price }} fcfa × {{ item.quantity }}
          </p>

          <!-- 💰 Gain vendeur -->
          <p class="text-xs text-green-700 font-medium">
            Vous recevez :
            {{ sellerNetPerUnit(item.price) }} fcfa / unité
            ({{ sellerNetPerUnit(item.price) * item.quantity }} fcfa au total)
          </p>

          <!-- 🧾 Commission -->
          <p class="text-xs text-gray-400">
            Commission Tôswè (10 %) :
            {{ commissionPerUnit(item.price) }} fcfa / unité
          </p>
        </div>

        <p class="font-semibold text-gray-900">
          {{ item.price * item.quantity }} fcfa
        </p>
      </div>
    </div>

    <!-- Résumé vendeur -->
    <div class="flex justify-end pt-4 border-t">
      <div class="text-right space-y-1">
        <p class="text-sm text-gray-500">
          Total brut client :
          <span class="font-medium text-gray-800">
            {{ formatFcfa(orderTotal) }} fcfa
          </span>
        </p>

        <p class="text-lg font-bold text-green-700">
          Vous recevrez :
          {{ sellerTotal }} fcfa
        </p>

        <p class="text-xs text-gray-400">
          Commission Tôswè incluse (10 %)
        </p>
      </div>
    </div>


    <!-- Actions -->
    <div class="flex justify-end gap-3 pt-4 border-t" v-if="mine">
      <button
        v-if="order.status === 'pending'"
        @click="cancelOrder"
        class="px-4 py-2 text-sm rounded-lg bg-red-500 text-white hover:bg-red-600 transition"
      >
        Annuler la commande
      </button>
    </div>
  </section>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const COMMISSION_RATE = 0.10 // 🔒 10% Tôswè

const route = useRoute()
const mine = route.query.mine === 'yes'

const props = defineProps({
  order: {
    type: Object,
    required: true
  }
})

const auth = useAuthStore()

// 💰 Montant net vendeur par unité
function sellerNetPerUnit(price) {
  return Math.round(price * (1 - COMMISSION_RATE))
}

// 🧾 Commission Tôswè par unité
function commissionPerUnit(price) {
  return Math.round(price * COMMISSION_RATE)
}

// ❌ Annuler commande
async function cancelOrder() {
  if (!confirm("Êtes-vous sûr de vouloir annuler cette commande ?")) return

  try {
    await $fetch(
      `http://127.0.0.1:8000/api/order/${props.order.id}/cancel/`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${auth.accessToken}`
        }
      }
    )

    props.order.status = "Annulée"
  } catch (err) {
    console.error("Erreur lors de l'annulation :", err)
    alert("Impossible d’annuler cette commande.")
  }
}

import { computed } from 'vue'

const orderTotal = computed(() => {
  if (!props.order?.items) return 0

  return props.order.items.reduce((sum, item) => {
    return sum + item.price * item.quantity
  }, 0)
})

const sellerTotal = computed(() => {
  if (!props.order?.items) return 0

  return props.order.items.reduce((total, item) => {
    const netPerUnit = sellerNetPerUnit(item.price)
    return total + netPerUnit * item.quantity
  }, 0)
})


function formatFcfa(value) {
  return Math.round(value).toLocaleString('fr-FR') + ' fcfa'
}


const statusClasses = {
  pending: "bg-yellow-100 text-yellow-800 ring-1 ring-yellow-300",
  shipped: "bg-blue-100 text-blue-800 ring-1 ring-blue-300",
  delivered: "bg-green-100 text-green-800 ring-1 ring-green-300",
  canceled: "bg-red-100 text-red-800 ring-1 ring-red-300",
  Annulée: "bg-red-100 text-red-800 ring-1 ring-red-300",
  default: "bg-gray-100 text-gray-600 ring-1 ring-gray-200"
}
</script>
