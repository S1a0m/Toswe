<template>
  <section class="px-4 md:px-8 py-12 max-w-6xl mx-auto">
    <h2 class="text-2xl font-bold text-[#7D260F] mb-6 font-[Kenia]">
      Notifications
    </h2>

    <div v-if="!notifications.length" class="text-center py-20">
      <p  class="text-gray-500">Aucune notification pour le moment.</p>
    </div>

    <div class="flex flex-col gap-4" v-else>
      <TwNotification
        v-for="(notif, index) in notifications"
        :key="index"
        :title="notif.title"
        :message="notif.message"
        :time="notif.sent_date"
        @click="notif.detail_link"
      />
    </div>
  </section>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
const notifications = ref([])

const auth = useAuthStore()

async function fetchNotifications() {
  try {
    const response = await $fetch('http://127.0.0.1:8000/api/notification/',
      { method: 'GET',
        headers: {
          Authorization: `Bearer ${auth.accessToken}`
       },
       credentials: 'include'
      }
    ) 
    notifications.value = response.results || response || []

    console.log('Notifications récupérées :', notifications.value)
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
  fetchNotifications()
})
</script>
