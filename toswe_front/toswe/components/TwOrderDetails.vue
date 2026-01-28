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
      <p class="text-xl font-bold text-gray-900">{{ order.total }} fcfa</p>
    </div>

    <!-- Produits -->
    <div class="space-y-4">
      <div
        v-for="(product, index) in order.items"
        :key="index"
        class="flex items-center gap-4 border-b pb-4 last:border-none"
      >
        <img
          :src="product.main_image"
          :alt="product.name"
          class="w-16 h-16 object-cover rounded-lg shadow-sm"
        />
        <div class="flex-1">
          <p class="font-medium text-gray-900">{{ product.name }}</p>
          <p class="text-sm text-gray-500">
            {{ product.price }} fcfa × {{ product.quantity }}
          </p>
        </div>
        <p class="font-semibold text-gray-900">
          {{ product.price * product.quantity }} fcfa
        </p>
      </div>
    </div>

    <!-- Actions -->
    <div class="flex justify-end gap-3 pt-4 border-t" v-if="mine">
      <!--<button
        class="px-4 py-2 text-sm rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-50 transition"
        v-if="order.status === 'delivered'"
      >
        <a :href="order.pdf" target="_blank">Télécharger la facture</a>
      </button>-->
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

const route = useRoute()
const mine = route.query.mine === 'yes'

const props = defineProps({
  order: {
    type: Object,
    required: true
  }
})

const auth = useAuthStore()

// 🎯 Fonction pour annuler une commande
async function cancelOrder() {
  if (!confirm("Êtes-vous sûr de vouloir annuler cette commande ?")) return

  try {
    await $fetch(`http://127.0.0.1:8000/api/order/${props.order.id}/cancel/`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${auth.accessToken}`
      }
    })

    // Mise à jour du statut en local
    props.order.status = "Annulée"
  } catch (err) {
    console.error("Erreur lors de l'annulation :", err)
    alert("Impossible d’annuler cette commande.")
  }
}

const statusClasses = {
  "pending": "bg-yellow-100 text-yellow-800 ring-1 ring-yellow-300",
  "shipped": "bg-blue-100 text-blue-800 ring-1 ring-blue-300",
  "delivered": "bg-green-100 text-green-800 ring-1 ring-green-300",
  "canceled": "bg-red-100 text-red-800 ring-1 ring-red-300",
  "Annulée": "bg-red-100 text-red-800 ring-1 ring-red-300", // fallback si API renvoie en FR
  default: "bg-gray-100 text-gray-600 ring-1 ring-gray-200"
}
</script>
