<template>
  <button
    class="w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300
           text-left group"
    :class="[
      danger
        ? 'text-red-600 hover:bg-red-50'
        : 'text-gray-700 hover:bg-gray-50'
    ]"
    @click="$emit('click')"
  >
    <!-- Icône -->
    <Icon
      :name="icon"
      class="w-5 h-5 flex-shrink-0 transition-transform duration-300 group-hover:scale-110"
      :class="danger ? 'text-red-500' : 'text-[#7D260F]'"
    />

    <!-- Label -->
    <span class="font-medium text-sm sm:text-base">
      {{ label }}
    </span>

    <!-- Chevron à droite -->
    <Icon
      name="uil:angle-right"
      class="ml-auto w-4 h-4 text-gray-400 group-hover:text-gray-600"
    />
  </button>
</template>

<script setup lang="ts">
interface Props {
  icon: string
  label: string
  danger?: boolean
}
defineProps<Props>()
defineEmits<{
  (e: 'click'): void
}>()
</script>
