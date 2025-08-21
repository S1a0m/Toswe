<template>
  <div class="flex space-x-4 border-b border-gray-200">
    <button
      v-for="tab in tabs"
      :key="tab.value"
      @click="selected = tab.value"
      :class="[
        'px-4 py-2 font-medium text-sm rounded-t-lg',
        selected === tab.value
          ? 'border-b-2 border-blue-500 text-blue-600'
          : 'text-gray-500 hover:text-gray-700'
      ]"
    >
      {{ tab.label }}
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const tabs = [
  { label: 'En vente', value: 'on_sale' },
  { label: 'Brouillon', value: 'draft' },
  { label: 'En attente de validation', value: 'pending' },
]

const selected = ref('on_sale')
</script>
