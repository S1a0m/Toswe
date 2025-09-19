<template>
  <section class="px-4 md:px-8 py-12 max-w-6xl mx-auto">
    <h2 class="text-2xl font-bold text-[#7D260F] mb-6 font-[Kenia]">
      Details de la commande
    </h2>

    <div v-if="!order" class="text-center py-20">
      <p  class="text-gray-500">Aucune commande pour le moment.</p>
    </div>
    <div v-else>
      <!-- Détails d'une commande -->
      <TwOrderDetails :order="order" />
    </div>
  </section>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRoute } from 'vue-router'

const route = useRoute()

const order = ref([])

const auth = useAuthStore()
console.log('Route query ID:', auth.accessToken)

async function fetchOrder() {
  try {
    const response = await $fetch(`http://127.0.0.1:8000/api/order/${route.query.id}/for_seller/`,
      { method: 'GET',
        headers: {
          Authorization: `Bearer ${auth.accessToken}`
       },
       credentials: 'include'
      }
    ) /*/ Remplacez par votre endpoint API
    if (!response.ok) {
      throw new Error('Erreur lors de la récupération des order')
    }*/
    order.value = response || response || []

    console.log('order récupérées :', order.value)
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
  fetchOrder()
})
/*const order = {
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
}*/
</script>
