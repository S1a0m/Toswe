<!-- components/TwToast.vue -->
<template>
  <transition name="slide-up">
    <div class="fixed right-4 bottom-6 flex flex-col gap-3 z-60">
    <div
      v-if="visible"
      class="text-white px-4 py-2 rounded-md shadow-md flex items-center gap-3"
      :class="bgColor"
    >
      <!-- Icône -->
      <Icon :name="iconName" class="w-5 h-5" />

      <!-- Message -->
      <span class="text-sm font-medium">{{ message }}</span>
    </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"
import { Icon } from "@iconify/vue"

const props = defineProps({
  message: { type: String, required: true },
  type: { type: String, default: "success" }, // success | error | info | warning
  duration: { type: Number, default: 3000 }
})

const visible = ref(true)

const bgColor = computed(() => {
  switch (props.type) {
    case "error": return "bg-red-600"
    case "info": return "bg-blue-600"
    case "warning": return "bg-yellow-500 text-black"
    default: return "bg-emerald-600"
  }
})

const iconName = computed(() => {
  switch (props.type) {
    case "error": return "mdi:alert-circle"
    case "info": return "mdi:information"
    case "warning": return "mdi:alert"
    default: return "mdi:check-circle"
  }
})

onMounted(() => {
  setTimeout(() => {
    visible.value = false
  }, props.duration)
})
</script>

<style>
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.4s ease;
}
.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(20px);
  opacity: 0;
}
</style>
