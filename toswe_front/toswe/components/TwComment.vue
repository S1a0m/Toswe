<template>
  <div class="flex space-x-4 p-4 border border-gray-200 rounded-xl bg-white shadow-sm">
    <!-- Avatar -->
    <div class="flex-shrink-0 w-10 h-10 rounded-full bg-gray-300 flex items-center justify-center text-white font-bold text-lg overflow-hidden">
      {{ username[0].toUpperCase() }}
    </div>

    <!-- Contenu -->
    <div class="flex-1">
      <div class="flex items-center justify-between mb-1">
        <h4 class="font-semibold text-gray-900">{{ username }}</h4>
        <span class="text-xs bg-gray-100 px-2 py-0.5 rounded-full text-gray-600">
          Publié {{ dayjs(date).fromNow() }}
        </span>
      </div>

      <!-- Note -->
      <div class="flex items-center mb-2">
        <Icon
          v-for="n in 5"
          :key="n"
          :name="n <= rating ? 'mdi:star' : 'mdi:star-outline'"
          class="w-4 h-4"
          :class="n <= rating ? 'text-yellow-500' : 'text-gray-300'"
        />
      </div>

      <!-- Texte -->
      <p class="text-gray-700 leading-relaxed text-sm bg-gray-50 rounded-lg p-3">
        {{ content }}
      </p>
    </div>
  </div>
</template>


<script setup>
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import 'dayjs/locale/fr'  // pour le français

dayjs.extend(relativeTime)
dayjs.locale('fr')

defineProps({
  username: String,
  avatar: String,
  content: String,
  date: String,
  rating: Number
})
</script>
