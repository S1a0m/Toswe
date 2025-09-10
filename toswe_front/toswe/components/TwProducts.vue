<template>
  <section class="max-w-6xl px-4 md:px-8 py-10 mx-auto">
    <h2 class="text-2xl font-bold text-[#7D260F] mb-2 font-[Kenia]" v-if="title">
      {{ title }}
    </h2>

    <div
      class="max-w-6xl mx-auto grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6"
    >
      <TwProduct
        v-for="(product, index) in products"
        :key="index"
        :id="product.id"
        :image-src="product.main_image.image"
        :product-name="product.name"
        :description="product.short_description"
        :price="product.price"
        :rating="product.total_rating.average"
        :badge="product.status"
        :is-sponsored="product.is_sponsored"
      />
    </div>
  </section>
</template>

<script setup>
const props = defineProps({
  title: {
    type: String,
    default: 'Produits'
  },
  products: {
    type: Array,
    default: () => []
  },
  next: {
    type: String,
    default: null
  }
})
</script>
