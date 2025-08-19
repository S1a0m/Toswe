<template>
  <section class="px-4 md:px-8 py-12">
    <h2 class="text-3xl font-bold text-center text-[#7D260F] mb-10 font-[Kenia]">
      {{ title }}
    </h2>

    <div
      class="max-w-6xl mx-auto grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6"
    >
      <TwProduct
        v-for="(product, index) in products"
        :key="index"
        :image-src="product.image"
        :product-name="product.name"
        :description="product.description"
        :price="product.price"
        :rating="product.rating"
        :badge="product.badge"
      />
    </div>
  </section>
</template>


<script setup>
const props = defineProps({
  title: {
    type: String,
    default: 'Produits'
  }
})

const products = [
  {
    image: '/assets/images/img1.jpg',
    name: 'Produit A',
    description: 'Un super produit local.',
    price: 19.99,
    rating: 4.8,
    badge: 'Nouveau'
  },
  {
    image: '/assets/images/img2.jpg',
    name: 'Produit B',
    description: 'Un autre produit qui cartonne.',
    price: 29.99,
    rating: 4.5,
    badge: 'Promo'
  },
  {
    image: '/assets/images/img3.jpg',
    name: 'Produit C',
    description: 'Encore un produit local premium.',
    price: 39.99,
    rating: 5,
    badge: 'Best Seller'
  },
  {
    image: '/assets/images/img3.jpg',
    name: 'Produit C',
    description: 'Encore un produit local premium.',
    price: 39.99,
    rating: 5,
    badge: 'Best Seller'
  },
  {
    image: '/assets/images/img3.jpg',
    name: 'Produit C',
    description: 'Encore un produit local premium.',
    price: 39.99,
    rating: 5,
    badge: 'Best Seller'
  },
  {
    image: '/assets/images/img3.jpg',
    name: 'Produit C',
    description: 'Encore un produit local premium.',
    price: 39.99,
    rating: 5,
    badge: 'Best Seller'
  },
  {
    image: '/assets/images/img3.jpg',
    name: 'Produit C',
    description: 'Encore un produit local premium.',
    price: 39.99,
    rating: 5,
    badge: 'Best Seller'
  }
]
</script>
