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
    const endpoint = route.query.mine === "yes"
      ? `/api/order/${route.query.id}/`
      : `/api/order/${route.query.id}/for_seller/`

    const response = await $fetch(`http://127.0.0.1:8000${endpoint}`, // or http://127.0.0.1:8000/api/order/${route.query.id}/
      { method: 'GET',
        headers: {
          Authorization: `Bearer ${auth.accessToken}`
       },
       credentials: 'include'
      }
    ) 
    order.value = response || response || []

    console.log('order récupérées :', order.value)
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
  fetchOrder()
})
</script>
