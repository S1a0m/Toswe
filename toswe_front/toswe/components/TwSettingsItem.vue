<template>
  <button
    @click="$emit('click')"
    class="w-full flex items-center gap-4 px-4 py-3 rounded-lg hover:bg-gray-50 transition-colors"
  >
    <!-- Icône -->
    <div
      class="flex items-center justify-center w-10 h-10 rounded-full bg-gray-100"
      :class="{ 'bg-red-100': danger }"
    >
      <Icon
        :name="icon"
        class="text-xl"
        :class="danger ? 'text-red-500' : 'text-gray-700'"
      />
    </div>

    <!-- Texte -->
    <div class="flex flex-col items-start text-left flex-1">
      <span
        class="text-sm font-medium"
        :class="danger ? 'text-red-600' : 'text-gray-900'"
      >
        {{ label }}
      </span>
      <span v-if="description" class="text-xs text-gray-500">
        {{ description }}
      </span>
    </div>

    <!-- Chevron -->
    <Icon name="uil:angle-right" class="text-gray-400 text-lg" />
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
