<template>
  <div class="flex items-center gap-4 p-4 border-b border-gray-200">
    <!-- Image produit -->
    <img
      :src="imageSrc"
      :alt="productName"
      class="w-16 h-16 object-cover rounded"
    />

    <!-- Infos produit -->
    <div class="flex-1">
      <h3 class="text-base font-semibold text-gray-900">{{ productName }}</h3>
      <p class="text-sm text-gray-500">{{ price.toLocaleString() }} FCFA</p>
    </div>

    <!-- Quantité -->
    <div class="flex items-center gap-2">
      <button
        class="px-2 py-1 border rounded text-gray-600 hover:bg-gray-100"
        @click="$emit('decrease')"
      >-</button>
      <span class="w-6 text-center">{{ quantity }}</span>
      <button
        class="px-2 py-1 border rounded text-gray-600 hover:bg-gray-100"
        @click="$emit('increase')"
      >+</button>
    </div>

    <!-- Supprimer -->
    <button
      class="ml-4 text-red-500 hover:text-red-700"
      @click="$emit('remove')"
    >
      <Icon name="uil:trash" class="w-5 h-5" />
    </button>
  </div>
</template>

<script setup>
const props = defineProps({
  imageSrc: { type: String, required: true },
  productName: { type: String, required: true },
  price: { type: Number, required: true },
  quantity: { type: Number, required: true }
})
</script>
