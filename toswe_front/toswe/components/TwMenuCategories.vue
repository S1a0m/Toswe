<template>
  <nav class="bg-white border-b border-gray-200 py-3">
    <div class="max-w-6xl mx-auto px-4 flex items-center gap-4">
      <!-- Icône Filtre -->
      <button class="text-[#7D260F] hover:text-[#5E1D0B] transition-colors">
        <Icon name="tabler:filter" size="24" />
      </button>

      <!-- Liste catégories -->
      <div
        class="flex gap-6 overflow-x-auto scrollbar-hide text-gray-700 font-[Kumbh_Sans] text-sm md:text-base"
      >
        <button
          v-for="category in categories.results"
          :key="category.id"
          @click="activeCategory = category.name"
          class="relative pb-1 transition-colors"
          :class="activeCategory === category.name ? 'text-[#7D260F] font-semibold' : 'hover:text-[#7D260F]'"
        >
          {{ category.name }}
          <!-- Soulignement actif -->
          <span
            v-if="activeCategory === category.name"
            class="absolute bottom-0 left-0 w-full h-[2px] bg-[#7D260F] rounded-full"
          ></span>
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'

const { data: categories, pending, error } = await useAsyncData('categories', () =>
  $fetch('http://127.0.0.1:8000/api/category/')
)


const activeCategory = ref('Tout')

const emit = defineEmits(['categorySelected'])

watch(activeCategory, (newCategory) => {
  emit('categorySelected', newCategory)
})
</script>

<style>
/* Cacher la scrollbar pour un look plus clean */
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
