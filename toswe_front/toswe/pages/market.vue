<!-- market.vue -->
<template>
  <TwMenuCategories @categorySelected="activeCategory = $event" />
  <TwMenuSide />
  <TwCart />

  <div class="max-w-6xl mx-auto  px-4 md:px-8">
    <TwShowAd />
  </div>

  <!-- 1er bloc -->
  <TwProducts
    v-if="!isLoadingCategory"
    title="Choisis pour vous"
    :products="firstProducts"
  />

  <TwProductsSkeleton v-else />


  <div class="max-w-6xl mx-auto my-10 px-4 md:px-8">
    <h2 class="text-xl font-bold text-[#7D260F] mb-2 font-[Kumbh_Sans]">
      Visitez la boutique de nos vendeurs
    </h2>
    <TwSellersMix />
  </div>
  <!-- 2ème bloc --><!-- 2ème bloc -->
  <TwProducts
    v-if="!isLoadingCategory && secondProducts.length > 0"
    title="D'autres clients ont aussi acheté ça"
    :products="secondProducts"
  />

  <TwProductsSkeleton
    v-if="isLoadingCategory"
  />

  <!-- Bouton Voir plus -->
  <div
    v-if="nextPage"
    class="flex justify-center mt-6"
  >
    <button
      @click="loadMore"
      :disabled="isLoadingMore"
      class="px-6 py-2 bg-[#7D260F] text-white rounded-lg flex items-center gap-2"
    >
      <span v-if="!isLoadingMore">Voir plus</span>
      <span v-else class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
    </button>

  </div>

  <div class="max-w-6xl mx-auto my-10 px-4 md:px-8">
    <h2 class="text-xl font-bold text-[#7D260F] mb-2 font-[Kumbh_Sans]">
      Les produits de ces marques pourraient vous intéresser
    </h2>
    <TwBrands />
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { ref, watch } from 'vue'

const activeCategory = ref('Tout')
const auth = useAuthStore()

const firstProducts = ref([])
const secondProducts = ref([])
const nextPage = ref(null)

const isLoadingCategory = ref(false)
const isLoadingMore = ref(false)


async function fetchProducts(category) {
  isLoadingCategory.value = true

  firstProducts.value = []
  secondProducts.value = []
  nextPage.value = null

  try {
    const headers = {}
    if (auth.accessToken) {
      headers["Authorization"] = `Bearer ${auth.accessToken}`
    }

    const data = await $fetch(
      `http://127.0.0.1:8000/api/product/suggestions/?category=${category}`,
      { headers, credentials: "include" }
    )

    firstProducts.value = data.results || []
    nextPage.value = data.next

    // Charger le 2e bloc si dispo
    if (nextPage.value) {
      const nextData = await $fetch(nextPage.value, {
        headers,
        credentials: "include",
      })
      secondProducts.value = nextData.results || []
      nextPage.value = nextData.next
    }
  } catch (e) {
    console.error("Erreur chargement produits", e)
  } finally {
    isLoadingCategory.value = false
  }
}


await fetchProducts(activeCategory.value)

watch(activeCategory, (newCat) => {
  fetchProducts(newCat)
})

async function loadMore() {
  if (!nextPage.value || isLoadingMore.value) return

  isLoadingMore.value = true

  try {
    const headers = {}
    if (auth.accessToken) headers["Authorization"] = `Bearer ${auth.accessToken}`

    const moreData = await $fetch(nextPage.value, { headers })
    secondProducts.value.push(...(moreData.results || []))
    nextPage.value = moreData.next
  } finally {
    isLoadingMore.value = false
  }
}

</script>

