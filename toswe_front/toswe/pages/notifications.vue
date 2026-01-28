<!-- pages/notifications.vue -->
<template>
  <section class="px-4 md:px-8 py-12 max-w-6xl mx-auto">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-2xl font-bold text-[#7D260F] font-[Kenia]">
        Notifications
      </h2>

      <div v-if="notifications.length" class="flex gap-3">
        <button
          class="px-4 py-2 text-sm bg-green-600 text-white rounded-lg hover:bg-green-700"
          @click="readAll"
        >
          Tout marquer comme lu
        </button>
        <button
          class="px-4 py-2 text-sm bg-red-600 text-white rounded-lg hover:bg-red-700"
          @click="deleteAll"
        >
          Supprimer tout
        </button>
      </div>
    </div>

    <div v-if="!notifications.length" class="text-center py-20">
      <p class="text-gray-500">Aucune notification pour le moment.</p>
    </div>

    <div class="flex flex-col gap-4" v-else>
      <TwNotification
        v-for="notif in notifications"
        :key="notif.id"
        :id="notif.id"
        :title="notif.title"
        :message="notif.message"
        :time="dayjs(notif.created_at).fromNow()"
        :isRead="notif.is_read"
        @markAsRead="markAsRead(notif.id)"
        @deleteNotif="deleteNotif(notif.id)"
      />

    </div>
  </section>
</template>

<script setup>
import TwNotification from '@/components/TwNotification.vue'
import { useAuthStore } from '@/stores/auth'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import 'dayjs/locale/fr'  // pour le français

dayjs.extend(relativeTime)
dayjs.locale('fr')

const notifications = ref([])
const auth = useAuthStore()

const apiBase = 'http://127.0.0.1:8000/api/notification/'

// 🔄 Récupérer les notifs
async function fetchNotifications() {
  try {
    const response = await $fetch(apiBase, {
      method: 'GET',
      headers: { Authorization: `Bearer ${auth.accessToken}` },
    })
    notifications.value = response.results || response || []
  } catch (error) {
    console.error(error)
  }
}

// ✅ Marquer une notification comme lue
async function markAsRead(id) {
  try {
    await $fetch(`${apiBase}${id}/read/`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${auth.accessToken}` },
    })
    notifications.value = notifications.value.map(n =>
      n.id === id ? { ...n, is_read: true } : n
    )
  } catch (error) {
    console.error(error)
  }
}

// ✅ Supprimer une notification
async function deleteNotif(id) {
  try {
    await $fetch(`${apiBase}${id}/delete/`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${auth.accessToken}` },
    })
    notifications.value = notifications.value.filter(n => n.id !== id)
  } catch (error) {
    console.error(error)
  }
}

// ✅ Marquer toutes comme lues
async function readAll() {
  try {
    await $fetch(`${apiBase}read_all/`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${auth.accessToken}` },
    })
    notifications.value = notifications.value.map(n => ({ ...n, is_read: true }))
  } catch (error) {
    console.error(error)
  }
}

// ✅ Supprimer toutes
async function deleteAll() {
  try {
    await $fetch(`${apiBase}delete_all/`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${auth.accessToken}` },
    })
    notifications.value = []
  } catch (error) {
    console.error(error)
  }
}

onMounted(fetchNotifications)
</script>
