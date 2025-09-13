<!-- market.vue -->
<template>
  <TwMenuCategories @categorySelected="activeCategory = $event" />
  <TwMenuSide />
  <TwCart />

  <!-- 1er bloc -->
  <TwProducts
    title="Choisis pour vous"
    :products="firstProducts"
  />

  <div class="max-w-6xl mx-auto my-10 px-4 md:px-8">
    <h2 class="text-xl font-bold text-[#7D260F] mb-2 font-[Kumbh_Sans]">
      Visitez la boutique de nos vendeurs
    </h2>
    <TwSellersMix />
  </div>

  <!-- 2ème bloc -->
  <TwProducts
    title="D'autres clients ont aussi acheté ça"
    :products="secondProducts"
    v-if="secondProducts.length > 0"
  />

  <!-- Bouton Voir plus -->
  <div
    v-if="nextPage"
    class="flex justify-center mt-6"
  >
    <button
      @click="loadMore"
      class="px-6 py-2 bg-[#7D260F] text-white rounded-lg hover:bg-[#5a1b0c] transition"
    >
      Voir plus
    </button>
  </div>

  <div class="max-w-6xl mx-auto my-10 px-4 md:px-8">
    <h2 class="text-xl font-bold text-[#7D260F] mb-2 font-[Kumbh_Sans]">
      Les produits de ces marques pourraient vous intéresser
    </h2>
    <TwBrands />
  </div>

  <TwPopupAd
  />
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { ref, watch } from 'vue'

const activeCategory = ref('Tout')
const auth = useAuthStore()

const firstProducts = ref([])
const secondProducts = ref([])
const nextPage = ref(null)

async function fetchProducts(category) {
  const headers = {}

  // ⚡️ Ajouter Authorization uniquement si un token est présent
  if (auth.accessToken) {
    headers["Authorization"] = `Bearer ${auth.accessToken}`
  }

  const data = await $fetch(`http://127.0.0.1:8000/api/product/suggestions/?category=${category}`, {
    headers,
    credentials: "include",
  })

  firstProducts.value = data.results || []
  secondProducts.value = []
  nextPage.value = data.next

  // Charger 2ème bloc si possible
  if (nextPage.value) {
    const nextData = await $fetch(nextPage.value, {
      headers,
      credentials: "include",
    })
    secondProducts.value = nextData.results || []
    nextPage.value = nextData.next
  }
}

await fetchProducts(activeCategory.value)

watch(activeCategory, (newCat) => {
  fetchProducts(newCat)
})

async function loadMore() {
  if (!nextPage.value) return
  const headers = {}
  if (auth.accessToken) headers["Authorization"] = `Bearer ${auth.accessToken}`

  const moreData = await $fetch(nextPage.value, { headers })
  secondProducts.value.push(...(moreData.results || []))
  nextPage.value = moreData.next
}
</script>

