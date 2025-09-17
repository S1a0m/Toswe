<template>
    <div
          class="bg-white rounded-lg shadow hover:shadow-lg transition overflow-hidden"
        >
          <img
            :src="`http://127.0.0.1:8000${item.main_image}`"
            :alt="item.name"
            class="w-full h-40 object-cover"
          />
          <div>
            <div class="p-4">
              <h3 class="font-bold text-lg mb-1">{{ item.name }}</h3>
              <p class="text-sm text-gray-500 mb-2">{{ item.shop_name }}</p>
              <p class="text-red-600 font-bold">{{ item.price }} fcfa</p>
            </div>
            <div class="px-4 pb-4">
              <button
                class="w-full bg-[#7D260F] text-white py-2 rounded-lg hover:bg-[#A13B20] transition"
                @click="goToProductDetails(item.id)"
              >
                Voir le produit
              </button>
          </div>
        </div>
      </div>
</template>
<script setup>
import { useNavigation } from '@/composables/useNavigation';
const { goToProductDetails } = useNavigation()

defineProps({
  item: {
    type: Object,
    required: true
  }
})
</script>
