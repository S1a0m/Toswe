<template>
  <div
    class="w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300
           text-left group cursor-pointer"
    :class="[
      danger
        ? 'text-red-600 hover:bg-red-50'
        : 'text-gray-700 hover:bg-gray-50'
    ]"
    @click="toggle"
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

    <!-- Switch -->
    <div class="ml-auto">
      <button
        type="button"
        class="relative inline-flex h-6 w-11 items-center rounded-full transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-[#7D260F]/50"
        :class="enabled ? 'bg-[#7D260F]' : 'bg-gray-300'"
      >
        <span
          class="inline-block h-4 w-4 transform rounded-full bg-white transition-transform duration-300"
          :class="enabled ? 'translate-x-6' : 'translate-x-1'"
        />
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

interface Props {
  icon: string
  label: string
  modelValue: boolean
  danger?: boolean
}
const props = defineProps<Props>()
const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
}>()

const enabled = ref(props.modelValue)

watch(
  () => props.modelValue,
  (val) => {
    enabled.value = val
  }
)

const toggle = () => {
  enabled.value = !enabled.value
  emit('update:modelValue', enabled.value)
}
</script>
