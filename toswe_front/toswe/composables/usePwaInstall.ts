import { ref, onMounted } from 'vue'

export function usePwaInstall() {
  const deferredPrompt = ref<Event | null>(null)
  const canInstall = ref(false)

  onMounted(() => {
    window.addEventListener('beforeinstallprompt', (e: Event) => {
      e.preventDefault() // empêche le prompt auto
      deferredPrompt.value = e
      canInstall.value = true
    })
  })

  const install = async () => {
    if (!deferredPrompt.value) return

    // @ts-ignore : Chrome fournit la méthode prompt()
    const promptEvent = deferredPrompt.value
    // @ts-ignore
    promptEvent.prompt()

    // @ts-ignore : Chrome fournit la méthode userChoice
    const choiceResult = await promptEvent.userChoice
    if (choiceResult.outcome === 'accepted') {
      console.log('✅ L’utilisateur a installé la PWA')
    } else {
      console.log('❌ L’utilisateur a refusé')
    }
    deferredPrompt.value = null
    canInstall.value = false
  }

  return { canInstall, install }
}
