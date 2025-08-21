<template>
  <div class="grid grid-cols-2 sm:grid-cols-3 gap-4">
    <div
      v-for="product in products"
      :key="product.id"
      @click="toggleSelection(product)"
      class="cursor-pointer border rounded-lg p-4 shadow-sm hover:shadow-md transition-all duration-200 flex flex-col items-center text-center"
      :class="selectedIds.includes(product.id) ? 'border-[#7D260F] bg-[#7D260F]/5' : 'border-gray-200 bg-white'"
    >
      <img :src="product.image" :alt="product.name" class="w-16 h-16 object-contain mb-2" />
      <h4 class="text-sm font-medium text-gray-700">{{ product.name }}</h4>
      <p class="text-xs text-gray-500">{{ product.price }} FCFA</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue'])

const products = ref([
  { id: 1, name: "Chemise locale", price: 7500, image: "/assets/images/img1.png" },
  { id: 2, name: "Sac artisanal", price: 12000, image: "/assets/images/img2.png" },
  { id: 3, name: "Sandales cuir", price: 9500, image: "/assets/images/img3.png" },
  { id: 4, name: "Épices bio", price: 3500, image: "/assets/images/img4.png" },
])

const selectedIds = ref([...props.modelValue])

const toggleSelection = (product) => {
  if (selectedIds.value.includes(product.id)) {
    selectedIds.value = selectedIds.value.filter(id => id !== product.id)
  } else {
    selectedIds.value.push(product.id)
  }
  emit('update:modelValue', selectedIds.value)
}

watch(() => props.modelValue, (val) => {
  selectedIds.value = [...val]
})
</script>
