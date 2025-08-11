<template>
  <section class="bg-white rounded-lg shadow-sm p-6 space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-start border-b pb-4">
      <div>
        <h2 class="text-lg font-bold">Commande #{{ order.id }}</h2>
        <p class="text-sm text-gray-500">{{ order.date }}</p>
        <p
          class="mt-1 px-3 py-1 text-xs font-medium rounded-full inline-block"
          :class="statusClasses[order.status] || statusClasses.default"
        >
          {{ order.status }}
        </p>
      </div>
      <p class="text-lg font-bold text-gray-900">{{ order.total }} FCFA</p>
    </div>

    <!-- Produits -->
    <div class="space-y-4">
      <div
        v-for="(product, index) in order.products"
        :key="index"
        class="flex items-center gap-4 border-b pb-4 last:border-none"
      >
        <img
          :src="product.image"
          :alt="product.name"
          class="w-16 h-16 object-cover rounded-lg"
        />
        <div class="flex-1">
          <p class="font-medium text-gray-900">{{ product.name }}</p>
          <p class="text-sm text-gray-500">{{ product.price }} FCFA × {{ product.quantity }}</p>
        </div>
        <p class="font-semibold text-gray-900">
          {{ product.price * product.quantity }} FCFA
        </p>
      </div>
    </div>

    <!-- Actions -->
    <div class="flex justify-end gap-3 pt-4 border-t">
      <button class="px-4 py-2 text-sm rounded-lg border border-gray-300 hover:bg-gray-50">
        Télécharger la facture
      </button>
      <button
        v-if="order.status === 'En attente'"
        class="px-4 py-2 text-sm rounded-lg bg-red-500 text-white hover:bg-red-600"
      >
        Annuler la commande
      </button>
    </div>
  </section>
</template>

<script setup>
defineProps({
  order: {
    type: Object,
    required: true
  }
})

const statusClasses = {
  "En attente": "bg-yellow-100 text-yellow-700",
  "Livrée": "bg-green-100 text-green-700",
  "Annulée": "bg-red-100 text-red-700",
  default: "bg-gray-100 text-gray-500"
}
</script>
