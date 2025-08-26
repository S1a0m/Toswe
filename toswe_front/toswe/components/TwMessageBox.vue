<script setup>
defineProps({
  message: {
    type: String,
    required: true
  },
  type: {
    type: String,
    default: "info" // "info", "success", "warning", "error"
  }
})
</script>

<template>
    <transition name="fade">
        <div
            v-if="message"
            class="p-4 mb-4 rounded-lg shadow-md"
            :class="{
            'bg-blue-100 text-blue-800': type === 'info',
            'bg-green-100 text-green-800': type === 'success',
            'bg-yellow-100 text-yellow-800': type === 'warning',
            'bg-red-100 text-red-800': type === 'error'
            }"
        >
            {{ message }}
        </div>
    </transition>
</template>


<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

</style>
