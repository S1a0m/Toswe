<template>
  <div v-if="auth.isAuthenticated && !auth.isSeller">
      <TwOrders :orders="orders.results" />
  </div>
  <section class="px-4 md:px-8 py-12 max-w-6xl mx-auto" v-if="auth.isSeller">
    <h2 class="text-2xl font-bold text-[#7D260F] mb-6 font-[Kenia]">
      Commandes
    </h2>

    <TwMenuOrders>
      <!-- Mes commandes -->
      <template #mine>
        <div v-if="orders.length" class="flex flex-col gap-4">
          <TwOrder
            v-for="order in orders"
            :key="order.id"
            :order="order"
            @click="goToOrderDetails(order.id)"
          />
        </div>
        <div v-else class="text-gray-500 text-center py-6">Aucune commande.</div>
      </template>

      <!-- Commandes clients -->
      <template #clients>
        <div v-if="sellerOrders.length" class="flex flex-col gap-4">
          <TwOrder
            v-for="order in sellerOrders"
            :key="order.id"
            :order="order"
            @click="goToOrderDetails(order.id)"
          />
        </div>
        <div v-else class="text-gray-500 text-center py-6">Aucune commande client.</div>
      </template>
    </TwMenuOrders>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useNavigation } from '@/composables/useNavigation'
import TwMenuOrders from '@/components/TwMenuOrders.vue'
import TwOrder from '@/components/TwOrder.vue'

const auth = useAuthStore()
const orders = ref([])
const sellerOrders = ref([])
const { goToOrderDetails } = useNavigation()

async function fetchOrders() {
  try {
    const data = await $fetch("http://127.0.0.1:8000/api/order/", {
      headers: { Authorization: `Bearer ${auth.accessToken}` },
      credentials: "include"
    })
    orders.value = data.results || []
  } catch (err) {
    console.error("Erreur commandes client:", err)
  }
}

async function fetchSellerOrders() {
  try {
    const data = await $fetch("http://127.0.0.1:8000/api/order/as_seller/", {
      headers: { Authorization: `Bearer ${auth.accessToken}` },
      credentials: "include"
    })
    sellerOrders.value = data || []
  } catch (err) {
    console.error("Erreur commandes vendeur:", err)
  }
}

onMounted(() => {
  fetchOrders()
  if (auth.isSeller) {
    fetchSellerOrders()
  }
})
</script>
