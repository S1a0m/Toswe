<template>
  <div
    class="flex items-center justify-between p-4 bg-white rounded-lg shadow-sm border border-gray-100 hover:shadow-md transition cursor-pointer"
  >
    <!-- Infos commande -->
    <div>
      <p class="text-sm text-gray-500">Commande #{{ order.id }}</p>
      <p class="text-sm text-gray-400">{{ order.created_at }}</p>
      <p
        class="text-xs font-medium mt-1 px-2 py-1 rounded-full inline-block"
        :class="statusClasses[order.status] || statusClasses.default"
      >
        {{ order.status }}
      </p>
    </div>

    <!-- Montant -->
    <div class="text-right">
      <p class="text-base font-bold text-gray-900">{{ order.total }} fcfa</p>
      <Icon name="uil:angle-right" class="text-gray-400 text-lg" />
    </div>
  </div>
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
