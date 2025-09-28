// composables/useNotifications.ts
import { ref, onMounted, onBeforeUnmount } from "vue"
import { useAuthStore } from "@/stores/auth"

const notifications = ref<any[]>([])
const hasNewNotification = ref(false)
let socket: WebSocket | null = null

export function useNotifications() {
  const auth = useAuthStore()

  function connectWebSocket() {
    if (!auth.isAuthenticated) return

    const wsUrl = `ws://127.0.0.1:8000/ws/notifications/`
    socket = new WebSocket(wsUrl)

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      console.log("Notification reçue :", data)

      hasNewNotification.value = true
      notifications.value.unshift({
        title: "Nouvelle notification",
        message: data.message,
        time: data.timestamp,
      })
    }

    socket.onclose = () => {
      console.warn("WebSocket fermé, reconnexion...")
      setTimeout(connectWebSocket, 3000)
    }
  }

  function markAsRead() {
    hasNewNotification.value = false
  }

  onMounted(connectWebSocket)
  onBeforeUnmount(() => socket?.close())

  return {
    notifications,
    hasNewNotification,
    markAsRead,
  }
}
