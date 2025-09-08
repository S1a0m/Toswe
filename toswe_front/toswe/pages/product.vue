<template>
  <TwProductDetails @seller="handleSeller" />
  <TwComments />

  <!-- Produits du vendeur -->
  <TwProducts 
    v-if="sellerProducts.length" 
    title="Produits du même vendeur" 
    :products="sellerProducts"
  />

  <span 
    @click="goToShop" 
    class="block w-fit mx-auto my-6 px-4 py-2 text-center text-[#7D260F] font-medium 
          border border-[#7D260F]/30 rounded-xl 
          hover:bg-[#7D260F]/10 hover:text-[#5b1c0b] 
          transition-all duration-300 cursor-pointer shadow-sm"
  >
    🛍️ Visiter sa boutique
  </span>

  <!-- Produits similaires -->
  <TwProducts 
    v-if="similarProducts.length" 
    title="Produits similaires" 
    :products="similarProducts"
  />

  <TwMenuSide />
  <TwPopupAd />
  <TwCart />
</template>

<script setup>
import { ref, watch } from 'vue'
import { goToShop } from '@/utils/navigations'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// 🔹 Gestion des produits du vendeur
const sellerId = ref(null)
const sellerProducts = ref([])
const auth = useAuthStore()

function handleSeller(id) {
  sellerId.value = id
}

watch(sellerId, async (id) => {
  if (!id) return
  try {
    const data = await $fetch(`http://127.0.0.1:8000/api/product/${id}/seller_products/`)
    sellerProducts.value = data?.results || []
  } catch (err) {
    console.error("Erreur chargement produits du vendeur:", err)
  }
})

// 🔹 Gestion des produits similaires
const route = useRoute()
const similarProducts = ref([])

try {
  const headers = {}
  if (auth.accessToken) headers["Authorization"] = `Bearer ${auth.accessToken}`
  const { data } = await useAsyncData('similar-products', () =>
    $fetch(`http://127.0.0.1:8000/api/product/${route.query.id}/similar/`, { headers })
  )
  similarProducts.value = data.value || []
} catch (err) {
  console.error("Erreur chargement produits similaires:", err)
}
</script>
