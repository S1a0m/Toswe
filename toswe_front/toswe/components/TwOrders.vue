<template>
  <section class="space-y-4">
    <TwOrder
      v-for="order in orders"
      :key="order.id"
      :order="order"
      @click="$emit('select', order)"
    />
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
