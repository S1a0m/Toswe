<template>
  <div
    class="bg-white border border-[#7D260F33] rounded-xl shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden p-6 flex flex-col items-center text-center"
  >
    <!-- Logo -->
    <img
      :src="logo"
      :alt="shopName"
      class="w-20 h-20 rounded-full object-cover mb-4 border-2 border-[#7D260F]"
    />

    <!-- Nom -->
    <h3 class="font-[Kenia] text-xl text-[#7D260F] mb-2">{{ shopName }}</h3>

    <!-- Étoiles -->
    <div class="flex items-center justify-center gap-1 mb-2">
      <Icon
        v-for="n in 5"
        :key="n"
        :name="n <= rating ? 'uil:star' : 'uil:star'"
        size="20"
        :class="n <= rating ? 'text-yellow-500' : 'text-gray-300'"
      />
    </div>

    <!-- Info -->
    <p class="text-gray-600 text-sm">{{ totalProducts }} produits en vente</p>
  </div>
</template>

<script setup>
defineProps({
  logo: String,
  shopName: String,
  rating: Number,
  totalProducts: Number
})
</script>
