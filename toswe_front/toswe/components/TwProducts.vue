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
        :id="product.id"
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
    id: 1,
    image: '/images/img1.jpg',
    name: 'Produit A',
    description: 'Un super produit local.',
    price: 19.99,
    rating: 4.8,
    badge: 'Nouveau'
  },
  {
    id: 2,
    image: '/images/img2.jpg',
    name: 'Produit B',
    description: 'Un autre produit qui cartonne.',
    price: 29.99,
    rating: 4.5,
    badge: 'Promo'
  },
  {
    id: 3,
    image: '/images/img3.jpg',
    name: 'Produit C',
    description: 'Encore un produit local premium.',
    price: 39.99,
    rating: 5,
    badge: 'Best Seller'
  },
  {
    id: 4,
    image: '/images/img4.jpg',
    name: 'Produit D',
    description: 'Un produit local exceptionnel.',
    price: 49.99,
    rating: 4.9,
    badge: 'Meilleur Choix'
  },
  {
    id: 5,
    image: '/images/img5.jpg',
    name: 'Produit E',
    description: 'Un produit local innovant.',
    price: 59.99,
    rating: 4.8,
    badge: 'Nouveau'
  },
  {
    id: 6,
    image: '/images/img6.jpg',
    name: 'Produit F',
    description: 'Un produit local révolutionnaire.',
    price: 69.99,
    rating: 4.7,
    badge: 'Nouveau'
  },
  {
    id: 7,  
    image: '/images/img3.jpg',
    name: 'Produit C',
    description: 'Encore un produit local premium.',
    price: 39.99,
    rating: 5,
    badge: 'Best Seller'
  },
  {
    id: 8,
    image: '/images/img3.jpg',
    name: 'Produit C',
    description: 'Encore un produit local premium.',
    price: 39.99,
    rating: 5,
    badge: 'Best Seller'
  }
]
</script>
