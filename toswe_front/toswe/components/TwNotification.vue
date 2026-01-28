<!-- components/TwNotification.vue -->
<template>
  <div
    class="relative bg-white/80 backdrop-blur-lg border border-white/40 rounded-xl shadow-lg p-5 flex items-start justify-between gap-4 transition-all duration-300 hover:shadow-2xl hover:scale-[1.02]"
  >
    <!-- Badge état -->
    <span
      class="absolute -left-2 top-5 w-3 h-3 rounded-full"
      :class="isRead ? 'bg-gray-300' : 'bg-red-500'"
    ></span>

    <!-- Contenu texte -->
    <div class="flex-1">
      <h4
        class="text-lg font-bold mb-1"
        :class="isRead ? 'text-gray-500' : 'text-[#7D260F]'"
      >
        {{ title }}
      </h4>
      <p class="text-gray-700 text-sm mb-2">
        {{ message }}
      </p>
      <div class="text-xs text-gray-500">
        Envoyé <time :datetime="time">{{ time }}</time>
      </div>
    </div>

    <!-- Actions -->
    <div class="flex flex-col items-center gap-2">
      <!-- Marquer comme lu -->
      <Icon
        v-if="!isRead"
        name="mdi:check-circle-outline"
        size="22"
        class="text-green-600 cursor-pointer hover:scale-110 transition-transform"
        @click="$emit('markAsRead')"
      />
      <!-- Supprimer -->
      <Icon
        name="mdi:delete-outline"
        size="22"
        class="text-red-500 cursor-pointer hover:scale-110 transition-transform"
        @click="$emit('deleteNotif')"
      />
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  id: { type: Number, required: true },
  title: { type: String, default: "Notification" },
  message: { type: String, default: "Contenu de la notification" },
  time: { type: String, default: "17:01" },
  isRead: { type: Boolean, default: false },
})
</script>
