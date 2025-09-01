<script setup lang="ts">
import { ref, onMounted } from 'vue'

const categories = [
  { key: 'all', label: 'Tout' },
  { key: 'agroalimentaire', label: 'Agroalimentaire' },
  { key: 'mode', label: 'Mode' },
  { key: 'electronique', label: 'Électronique' },
  { key: 'beaute', label: 'Beauté' },
  // ajoute selon ton modèle
]

const activeCategory = ref('all')
const products = ref<any[]>([])
const loading = ref(false)

// Consommer l'API suggestions
async function fetchSuggestions(category = 'all') {
  loading.value = true
  try {
    const response = await $fetch(`/api/products/suggestions/`, {
      params: { category: category === 'all' ? undefined : category }
    })
    products.value = response
  } catch (e) {
    console.error('Erreur fetch suggestions:', e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchSuggestions()
})
</script>

<template>
  <div class="w-full">
    <!-- Onglets catégories -->
    <div class="flex space-x-3 border-b mb-4">
      <button
        v-for="cat in categories"
        :key="cat.key"
        @click="() => { activeCategory = cat.key; fetchSuggestions(cat.key) }"
        class="px-4 py-2 text-sm font-medium"
        :class="activeCategory === cat.key 
          ? 'border-b-2 border-blue-500 text-blue-500' 
          : 'text-gray-500 hover:text-blue-400'"
      >
        {{ cat.label }}
      </button>
    </div>

    <!-- Produits -->
    <div v-if="loading" class="text-center text-gray-400 py-6">Chargement...</div>

    <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      <div
        v-for="prod in products"
        :key="prod.id"
        class="bg-white dark:bg-gray-800 shadow rounded-lg p-3 flex flex-col"
      >
        <img
          :src="prod.image"
          alt="Image produit"
          class="h-32 w-full object-cover rounded"
        />
        <div class="mt-2 flex-1">
          <h3 class="text-sm font-semibold line-clamp-2">
            {{ prod.name }}
          </h3>
          <p class="text-xs text-gray-500 line-clamp-2">
            {{ prod.description }}
          </p>
        </div>
        <div class="mt-2 font-bold text-blue-600">{{ prod.price }} FCFA</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
