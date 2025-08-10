<template>
  <button
    @click="$emit('click')"
    class="w-full flex items-center gap-4 p-4 rounded-lg bg-white hover:bg-gray-50 dark:bg-gray-800 dark:hover:bg-gray-700 border border-gray-200 dark:border-gray-700 transition-colors"
    :class="{ 'text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20': danger }"
  >
    <!-- Icône -->
    <Icon
      :name="icon"
      class="text-2xl flex-shrink-0"
      :class="{ 'text-red-500': danger }"
    />

    <!-- Texte -->
    <div class="flex flex-col items-start text-left">
      <span class="font-medium">{{ label }}</span>
      <span v-if="description" class="text-sm text-gray-500 dark:text-gray-400">
        {{ description }}
      </span>
    </div>

    <!-- Chevron -->
    <Icon name="uil:angle-right" class="ml-auto text-gray-400 text-lg" />
  </button>
</template>

<script setup>
defineProps({
  icon: { type: String, required: true },
  label: { type: String, required: true },
  description: { type: String, default: '' },
  danger: { type: Boolean, default: false }
})

defineEmits(['click'])
</script>
