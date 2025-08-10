<template>
  <div
    class="bg-white/80 backdrop-blur-lg border border-white/40 rounded-xl shadow-lg p-5 flex items-start justify-between gap-4 transition-all duration-300 hover:shadow-2xl hover:scale-[1.02]"
  >
    <!-- Contenu texte -->
    <div class="flex-1">
      <h4 class="text-lg font-bold text-[#7D260F] mb-1">{{ title }}</h4>
      <p class="text-gray-700 text-sm mb-2">
        {{ message }}
      </p>
      <div class="text-xs text-gray-500">
        Envoyé à <time :datetime="time">{{ time }}</time>
      </div>
    </div>

    <!-- Actions -->
    <div class="flex flex-col items-center gap-2">
      <Icon
        name="mdi:check-circle-outline"
        size="22"
        class="text-green-600 cursor-pointer hover:scale-110 transition-transform"
      />
      <Icon
        name="mdi:delete-outline"
        size="22"
        class="text-red-500 cursor-pointer hover:scale-110 transition-transform"
      />
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  title: { type: String, default: "Notification" },
  message: { type: String, default: "Contenu de la notification" },
  time: { type: String, default: "17:01" }
})
</script>
