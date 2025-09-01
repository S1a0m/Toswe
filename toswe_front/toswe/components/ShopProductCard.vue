<template>
  <article class="group  border-gray-200 rounded-lg border bg-white hover:shadow-md transition overflow-hidden">
    <div class="aspect-square bg-gray-50">
      <img
        :src="product.image_url || '/placeholder-product.png'"
        :alt="product.title"
        class="size-full object-cover"
      />
    </div>
    <div class="p-3">
      <h3 class="text-sm font-medium truncate">{{ product.title }}</h3>
      <p class="text-sm text-gray-500 line-clamp-2 mt-1">{{ product.subtitle || product.description }}</p>

      <div class="mt-3 flex items-center justify-between">
        <div class="text-base font-semibold">
          {{ formatPrice(product.price) }}
        </div>

        <div class="flex items-center gap-2">
          <span
            v-if="product.is_sponsored"
            class="text-2xs px-2 py-0.5 rounded-full bg-amber-100 text-amber-800"
          >
            Sponsorisé
          </span>
          <button class="text-sm px-3 py-1.5 rounded-lg border hover:bg-gray-50">
            Voir
          </button>
        </div>
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
