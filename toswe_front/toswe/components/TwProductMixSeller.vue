<template>
    <div
          class="bg-white rounded-lg shadow hover:shadow-lg transition overflow-hidden"
        >
          <img
            :src="item.main_image"
            :alt="item.name"
            class="w-full h-40 object-cover"
          />
          <div class="p-4">
            <h3 class="font-bold text-lg mb-1">{{ item.name }}</h3>
            <p class="text-sm text-gray-500 mb-2">{{ item.racine_id }}</p>
            <p class="text-red-600 font-bold">{{ item.price }} fcfa</p>
          </div>
        </div>
</template>
<script setup>

defineProps({
  item: {
    type: Object,
    required: true
  }
})
</script>
