<template>
  <div>
    <TwOrders :orders="orders" @select="selectedOrder = $event" />
  </div>
</template>

<script setup>

definePageMeta({
  middleware: 'auth', // Appliquer le middleware d'authentification
})

const orders = [
  {
    id: 123,
    date: '10 Août 2025',
    status: 'En attente',
    total: 15000,
    products: [
      { name: 'Produit A', price: 5000, quantity: 1, image: '/assets/images/img1.png' },
      { name: 'Produit B', price: 2500, quantity: 4, image: '/assets/images/img2.jpg' }
    ]
  },
  {
    id: 124,
    date: '9 Août 2025',
    status: 'Livrée',
    total: 20000,
    products: [
      { name: 'Produit C', price: 10000, quantity: 2, image: '/assets/images/img2.jpg' }
    ]
  },
  {
    id: 124,
    date: '9 Août 2025',
    status: 'Livrée',
    total: 20000,
    products: [
      { name: 'Produit C', price: 10000, quantity: 2, image: '/assets/images/img2.jpg' }
    ]
  },
  {
    id: 124,
    date: '9 Août 2025',
    status: 'Livrée',
    total: 20000,
    products: [
      { name: 'Produit C', price: 10000, quantity: 2, image: '/assets/images/img2.jpg' }
    ]
  },
  {
    id: 124,
    date: '9 Août 2025',
    status: 'Livrée',
    total: 20000,
    products: [
      { name: 'Produit C', price: 10000, quantity: 2, image: '/assets/images/img2.jpg' }
    ]
  },
  {
    id: 124,
    date: '9 Août 2025',
    status: 'Livrée',
    total: 20000,
    products: [
      { name: 'Produit C', price: 10000, quantity: 2, image: '/assets/images/img2.jpg' }
    ]
  },
  {
    id: 124,
    date: '9 Août 2025',
    status: 'Livrée',
    total: 20000,
    products: [
      { name: 'Produit C', price: 10000, quantity: 2, image: '/assets/images/img2.jpg' }
    ]
  }
]

let selectedOrder = null
</script>
