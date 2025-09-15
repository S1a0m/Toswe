import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useAuthStore } from '@/stores/auth'

export function useWebSocket(path = "/ws/notifications/") {
  const auth = useAuthStore()
  const socket = ref(null as WebSocket | null)
  const messages = ref([] as any[])

  onMounted(() => {
    // 🔑 On ajoute le token dans la query si nécessaire
    const wsScheme = window.location.protocol === "https:" ? "wss" : "ws"
    const url = `${wsScheme}://${window.location.host}${path}?token=${auth.accessToken}`

    socket.value = new WebSocket(url)

    socket.value.onopen = () => {
      console.log("✅ WebSocket connecté :", url)
    }

    socket.value.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        messages.value.push(data)
        console.log("📩 Notification reçue :", data)
      } catch (err) {
        console.error("Erreur parsing WS:", err)
      }
    }

    socket.value.onclose = () => {
      console.log("❌ WebSocket fermé")
    }
  })

  onBeforeUnmount(() => {
    if (socket.value) {
      socket.value.close()
    }
  })

  return { socket, messages }
}
