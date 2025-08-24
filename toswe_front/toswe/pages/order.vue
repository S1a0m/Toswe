<template>
    <div class="mt-18">
    </div>
    <div class="pt-0.5">
    </div>
  <div class="p-6">
    <!-- Détails d'une commande -->
    <TwOrderDetails :order="order" />
  </div>
</template>

<script setup>

const order = {
  id: 101,
  date: '10 août 2025',
  status: 'En attente', // ou "Livrée", "Annulée"
  total: 15000,
  products: [
    { name: 'Produit A', price: 5000, quantity: 1, image: '/images/img1.png' },
    { name: 'Produit B', price: 2500, quantity: 4, image: '/images/img2.jpg' },
    { name: 'Produit B', price: 2500, quantity: 4, image: '/images/img2.jpg' },
    { name: 'Produit B', price: 2500, quantity: 4, image: '/images/img2.jpg' },
    { name: 'Produit B', price: 2500, quantity: 4, image: '/images/img2.jpg' },
    { name: 'Produit B', price: 2500, quantity: 4, image: '/images/img2.jpg' },
    { name: 'Produit B', price: 2500, quantity: 4, image: '/images/img2.jpg' },
    { name: 'Produit B', price: 2500, quantity: 4, image: '/images/img2.jpg' }
  ]
}
</script>
