<template>
  <div
    class="bg-white border border-[#7D260F33] rounded-xl shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden flex flex-col"
  >
    <!-- Image Produit -->
    <img
      :src="image"
      :alt="name"
      class="w-full h-48 object-cover"
    />

    <!-- Détails -->
    <div class="p-4 flex flex-col flex-1">
      <h3 class="font-[Kumbh_Sans] text-lg font-semibold mb-2">{{ name }}</h3>
      <p class="text-[#7D260F] font-bold mb-4">{{ price.toLocaleString() }} FCFA</p>

      <!-- Bouton ajout + compteur -->
      <div class="mt-auto flex items-center justify-between">
        <button
          @click="addToCart"
          class="bg-[#7D260F] text-white px-4 py-2 rounded-lg hover:bg-[#5E1D0B] transition-colors"
        >
          Ajouter
        </button>
        <span class="text-gray-600 font-medium">{{ quantity }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  image: String,
  name: String,
  price: Number,
  quantity: Number
})

const addToCart = () => {
  // Action d'ajout au panier
}
</script>
