<template>
  <div class="flex space-x-4 p-4 border border-gray-200 rounded-lg bg-white shadow-sm">
    <!-- Avatar -->
    <div class="flex-shrink-0">
      <img
        class="w-12 h-12 rounded-full object-cover"
        :src="avatar"
        :alt="username"
      />
    </div>

    <!-- Contenu -->
    <div class="flex-1">
      <div class="flex items-center justify-between mb-1">
        <h4 class="font-semibold text-gray-900">{{ username }}</h4>
        <span class="text-sm text-gray-500">{{ date }}</span>
      </div>

      <!-- Note par étoiles -->
      <div class="flex items-center mb-2">
        <Icon
          v-for="n in 5"
          :key="n"
          name="uil:star"
          class="w-4 h-4"
          :class="n <= rating ? 'text-yellow-500' : 'text-gray-300'"
        />
      </div>

      <p class="text-gray-700 leading-relaxed text-sm">
        {{ content }}
      </p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  username: String,
  avatar: String,
  content: String,
  date: String,
  rating: Number
})
</script>
