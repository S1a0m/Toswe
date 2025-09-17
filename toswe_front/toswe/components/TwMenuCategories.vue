<template>
  <nav
    class="sticky top-15 z-30 bg-white/80 backdrop-blur-md border-b border-gray-200 shadow-sm"
  >
    <div class="max-w-6xl mx-auto px-4 flex items-center gap-4 py-3">
      <!-- Icône Filtre -->
      <button
        class="p-2 rounded-full bg-[#f8ebe8] text-[#7D260F] hover:bg-[#7D260F] hover:text-white transition-colors shadow-sm flex items-center justify-center"
      >
        <Icon name="uil:filter" size="22" />
      </button>

      <!-- Liste catégories -->
      <div
        class="flex gap-4 overflow-x-auto scrollbar-hide text-gray-700 font-[Kumbh_Sans] text-sm md:text-base"
      >
        <button
          v-for="category in categories.results"
          :key="category.id"
          @click="activeCategory = category.name"
          class="relative px-3 py-1 rounded-full transition-all duration-300 ease-in-out"
          :class="activeCategory === category.name
            ? 'bg-[#7D260F] text-white font-semibold shadow-sm'
            : 'hover:bg-[#f8ebe8] hover:text-[#7D260F]'"
        >
          {{ category.name }}
          <!-- Soulignement actif avec animation -->
          <span
            v-if="activeCategory === category.name"
            class="absolute -bottom-1 left-1/2 -translate-x-1/2 w-3/4 h-[2px] bg-[#7D260F] rounded-full scale-x-0 group-hover:scale-x-100 transition-transform duration-300"
          ></span>
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, watch } from 'vue'

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
/* Scrollbar masquée */
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
