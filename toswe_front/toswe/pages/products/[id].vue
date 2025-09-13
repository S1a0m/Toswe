<template>
  <div class="max-w-3xl mx-auto p-6">
    <!-- Détails produit -->
    <div class="bg-white rounded-xl shadow p-4">
      <img :src="product.image" class="w-full h-64 object-cover rounded-lg" />
      <h1 class="text-2xl font-bold mt-4 text-[#7D260F]">{{ product.name }}</h1>
      <p class="text-lg text-gray-700">{{ product.price }} FCFA</p>
      <p class="text-gray-600 mt-2">{{ product.description }}</p>
    </div>

    <!-- Actions marketing -->
    <div class="mt-6 space-y-3">
      <h2 class="text-lg font-semibold text-gray-800">Actions marketing</h2>

      <NuxtLink :to="`/products/${product.id}/sponsor`"
        class="block w-full text-center py-3 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700">
        🚀 Sponsoriser ce produit
      </NuxtLink>

      <NuxtLink :to="`/products/${product.id}/promotion`"
        class="block w-full text-center py-3 rounded-lg bg-emerald-600 text-white hover:bg-emerald-700">
        💸 Lancer une promotion
      </NuxtLink>
    </div>
  </div>
</template>

<script setup>
const route = useRoute()

// TODO: remplacer par API fetch
const product = reactive({
  id: route.params.id,
  name: "Chaussures Tôswè",
  price: 15000,
  description: "Chaussures de sport confortables",
  image: "/placeholder-banner.png"
})
</script>
