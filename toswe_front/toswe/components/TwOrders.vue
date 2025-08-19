<template>
  <section class="px-4 md:px-8 py-12 max-w-3xl mx-auto">
    <h2 class="text-2xl font-bold text-[#7D260F] mb-6 font-[Kenia]">
      Commandes
    </h2>
    <div class="flex flex-col gap-4">
      <TwOrder
        v-for="order in orders"
        :key="order.id"
        :order="order"
        @click="$emit('select', order)"
      />
    </div>
  </section>
</template>

<script setup>
import TwOrder from './TwOrder.vue'

defineProps({
  orders: {
    type: Array,
    required: true
  }
})

defineEmits(['select'])
</script>
