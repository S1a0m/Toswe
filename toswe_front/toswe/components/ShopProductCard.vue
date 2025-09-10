<!-- ShopProductCard.vue -->
<template>
  <article
    class="group relative bg-gradient-to-br from-white/90 to-white/80 backdrop-blur-lg rounded-2xl shadow-lg border border-white/30 overflow-hidden hover:shadow-2xl hover:scale-105 transition-all duration-300"
    :class="{ 'border-yellow-400 shadow-yellow-200/50': product.is_sponsored }"
  >
    <!-- Ruban Sponsorisé -->
    <div
      v-if="product.is_sponsored"
      class="absolute top-0 right-0 bg-gradient-to-r from-yellow-400 to-yellow-500 text-white text-[10px] font-bold px-2 py-1 rounded-bl-lg shadow-md uppercase tracking-wide"
    >
      Sponsorisé
    </div>

    <!-- Image -->
    <div class="aspect-square bg-gray-50 overflow-hidden group">
      <img
        :src="product.main_image.image"
        :alt="product.name"
        class="size-full object-cover transform group-hover:scale-110 transition-transform duration-500"
      />
    </div>

    <!-- Contenu -->
    <div class="p-5 flex flex-col gap-3">
      <h3 class="text-base font-bold text-gray-900 line-clamp-1">{{ product.name }}</h3>
      <p class="text-sm text-gray-600 line-clamp-2">{{ product.short_description }}</p>

      <div class="flex items-center justify-between mt-2">
        <span class="text-lg font-bold text-[#7D260F]">{{ formatPrice(product.price) }}</span>
        <button
          class="px-4 py-2 bg-gradient-to-r from-[#7D260F] to-[#A13B20] text-white text-sm font-semibold rounded-full shadow-md hover:shadow-lg hover:from-[#A13B20] hover:to-[#7D260F] transition-all duration-300"
        >
          Voir
        </button>
      </div>
    </div>
  </article>
</template>


<script setup>
const props = defineProps({
  product: { type: Object, required: true }
})
function formatPrice(v) {
  if (v == null) return '—'
  try { return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'XOF' }).format(v) }
  catch { return `${v} FCFA` }
}
</script>
