<template>
  <div class="min-h-screen bg-[#fdf8f5] flex flex-col">
    <!-- Header -->
    <header class="bg-[#fdf8f5]/60 backdrop-blur-sm border-b border-gray-200">
      <div class="max-w-4xl mx-auto px-4 py-4 flex items-center gap-4">
        <img src="/assets/images/Nehanda.png" alt="Nehanda" class="w-12 h-12 rounded-full object-cover shadow-md" />
        <div>
          <h1 class="text-lg font-semibold text-gray-900">Nehanda</h1>
          <p class="text-sm text-gray-600">Posez une question, demandez une recommandation ou programmez une commande.</p>
        </div>
        <div class="ml-auto text-sm text-gray-500">
          <span v-if="auth.isAuthenticated" class="text-sm flex items-center gap-1 font-semibold"><span class="bg-green-500 w-2 h-2 inline-block rounded-full"></span>{{ auth.getUsername}}</span></div>
      </div>
    </header>

    <!-- Main -->
    <main class="flex-1 overflow-hidden">
      <div class="max-w-4xl mx-auto h-full flex flex-col">

        <!-- Conversation area -->
        <div ref="scrollRoot" class="flex-1 overflow-auto px-4 py-6" :class="{'pb-32': true}">
          <div class="space-y-4">
            <div v-for="(msg, idx) in messages" :key="msg.id || idx" class="flex" :class="msg.role === 'user' ? 'justify-end' : 'justify-start'">

              <!-- Avatar -->
              <div v-if="msg.role === 'assistant'" class="mr-3">
                <img src="/assets/images/Nehanda.png" alt="Nehanda" class="w-10 h-10 rounded-full" />
              </div>

              <!-- Message bubble -->
              <div :class="[
                  'max-w-[78%] px-4 py-3 rounded-2xl shadow-sm',
                  msg.role === 'user' ? 'bg-gradient-to-r from-[#7D260F] to-[#A13B20] text-white rounded-br-none' : 'bg-white/90 text-gray-900 rounded-bl-none border border-white/30'
                ]">
                <div class="whitespace-pre-wrap text-sm" v-html="formatContent(msg.content)"></div>
                <div class="mt-2 text-xs text-gray-400 text-right">{{ formatTime(msg.time) }}</div>
              </div>

              <div v-if="msg.role === 'user'" class="ml-3">
                <div class="w-10 h-10 rounded-full bg-gradient-to-tr from-[#f6d8b6] to-[#fff] flex items-center justify-center text-sm font-semibold text-[#7D260F]">{{ auth.getUsername[0] }}</div>
              </div>
            </div>

            <!-- Typing indicator -->
            <div v-if="isTyping" class="flex justify-start">
              <div class="mr-3">
                <img src="/assets/images/Nehanda.png" alt="Nehanda" class="w-10 h-10 rounded-full" />
              </div>
              <div class="bg-white/90 px-4 py-3 rounded-2xl shadow-sm border border-white/30">
                <div class="flex items-center gap-1">
                  <span class="dot w-2 h-2 rounded-full bg-gray-500 animate-bounce-delay"></span>
                  <span class="dot w-2 h-2 rounded-full bg-gray-500 animate-bounce-delay-200"></span>
                  <span class="dot w-2 h-2 rounded-full bg-gray-500 animate-bounce-delay-400"></span>
                </div>
              </div>
            </div>

          </div>
        </div>

        <!-- Composer -->
        <div class="border-t border-gray-200 bg-[#fdf8f5]/80 backdrop-blur-sm py-4 px-4 fixed bottom-0 left-0 right-0">
          <div class="max-w-4xl mx-auto flex flex-col gap-3">

            <!-- Quick prompts -->
            <div class="flex gap-2 flex-wrap">
              <button v-for="(p, i) in quickPrompts" :key="i" @click="usePrompt(p)" class="text-sm px-3 py-1 rounded-full bg-white/90 border border-white/30 text-gray-700 hover:scale-105 transition">{{ p }}</button>
            </div>

            <!-- Input row -->
            <div class="flex items-end gap-3">
              <textarea
                v-model="input"
                @keydown.enter.exact.prevent="send()"
                @keydown.enter.shift.stop
                placeholder="Écrivez votre message... (Entrée pour envoyer, Shift+Entrée nouvelle ligne)"
                class="flex-1 resize-none min-h-[44px] max-h-40 px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-[#7D260F] text-sm"
              ></textarea>

              <div class="flex items-center gap-2">
                <button @click="send" :disabled="sending || !input.trim()" class="inline-flex items-center gap-2 bg-[#7D260F] text-white px-4 py-2 rounded-lg shadow hover:opacity-95 disabled:opacity-50">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path d="M2.94 2.94a1 1 0 011.414 0L17 15.586V17a1 1 0 01-1 1h-1.414L2.94 4.354a1 1 0 010-1.414z"/></svg>
                  Envoyer
                </button>
              </div>
            </div>

            <div class="text-xs text-gray-500">Conversation sauvegardée localement · Suggestions: cliquez une invite</div>
          </div>
        </div>

      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import { v4 as uuidv4 } from 'uuid'
import { useAuthStore } from '@/stores/auth'
const auth = useAuthStore()

const STORAGE_KEY = 'nehanda_conversation_v1'

const defaultMessages = [
  { id: uuidv4(), role: 'assistant', content: "Bonjour — je suis Nehanda. En quoi puis-je vous aider aujourd'hui ?", time: new Date().toISOString() },
  { id: uuidv4(), role: 'user', content: "Je veux meubler ma chambre, quel serait le meilleur matelas à acheter pour cette saison ?", time: new Date().toISOString() },
  { id: uuidv4(), role: 'assistant', content: "Cela dépend de votre budget, de la fermeté désirée et de la taille. Pour cette saison (chaude), un matelas respirant à base de latex ou mousse à mémoire avec bonne aération est recommandé. Souhaitez-vous des options locales ?", time: new Date().toISOString() }
]

const messages = ref([])
const input = ref('')
const sending = ref(false)
const isTyping = ref(false)
const scrollRoot = ref(null)

const { $apiFetch } = useNuxtApp()

const quickPrompts = [
  'Je veux meubler ma chambre',
  "Quel est le meilleur matelas pour cette saison ?",
  'Programmer une commande',
]

function load() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    messages.value = raw ? JSON.parse(raw) : defaultMessages
  } catch (e) {
    messages.value = defaultMessages
  }
}

function save() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(messages.value))
}

watch(messages, () => {
  save()
  // scroll to bottom
  nextTick(() => {
    const el = scrollRoot.value
    if (el) el.scrollTop = el.scrollHeight
  })
}, { deep: true })

onMounted(() => {
  load()
  nextTick(() => {
    const el = scrollRoot.value
    if (el) el.scrollTop = el.scrollHeight
  })
})

function formatTime(iso) {
  try {
    const d = new Date(iso)
    return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  } catch (e) {
    return ''
  }
}

function formatContent(text) {
  // simple -> escape then replace \n with <br>
  return escapeHtml(text).replace(/\n/g, '<br/>')
}

function escapeHtml(unsafe) {
  return unsafe
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;')
}

function usePrompt(p) {
  input.value = p
}

async function send() {
  const text = input.value.trim()
  if (!text) return
  const userMsg = { id: uuidv4(), role: 'user', content: text, time: new Date().toISOString() }
  messages.value.push(userMsg)
  input.value = ''
  sending.value = true
  isTyping.value = true

  try {
    // Récupérer dernier conversation_id si présent
    const lastConv = messages.value.find(m => m.conversation_id)
    const convId = lastConv?.conversation_id

    const payload = { message: text, conversation_id: convId || null }

    // 👉 Ici $apiFetch renvoie déjà du JSON, pas besoin de res.json()
    const json = await $apiFetch('http://127.0.0.1:8080/nehanda/chat', {
      method: 'POST',
      body: payload, // pas besoin de JSON.stringify, $fetch gère
    })

    // Réponse backend
    const assistantReply = json.response

    // Ajoute le message assistant
    messages.value.push({
      id: uuidv4(),
      role: 'assistant',
      content: assistantReply,
      time: new Date().toISOString(),
      conversation_id: json.conversation_id
    })
  } catch (e) {
    console.error('Chat error:', e)
    // fallback
    messages.value.push({
      id: uuidv4(),
      role: 'assistant',
      content: "Désolé, je n’ai pas pu contacter le serveur.",
      time: new Date().toISOString()
    })
  } finally {
    sending.value = false
    isTyping.value = false
  }
}



function cannedReply(userText) {
  if (/matelas|lit|chambre/i.test(userText)) {
    return "Pour meubler la chambre : commencez par choisir la taille du lit (140/160/180), puis optez pour un matelas respirant (latex ou mousse aération). Je peux vous proposer des modèles locaux à petit prix ou premium. Voulez-vous voir des suggestions ?"
  }
  if (/commander|programme/i.test(userText)) {
    return "Je peux vous aider à programmer une commande. Dites-moi quel produit, la quantité et la date souhaitée. Souhaitez-vous continuer ?"
  }
  return "Merci pour votre message — dites-m'en plus pour que je puisse vous aider au mieux."
}

async function simulateStreamReply(text) {
  isTyping.value = true
  const chunkSize = 40
  let built = ''
  for (let i = 0; i < text.length; i += chunkSize) {
    const part = text.slice(i, i + chunkSize)
    built += part
    // update a temporary assistant message
    const tmp = { id: 'tmp', role: 'assistant', content: built, time: new Date().toISOString() }
    // replace last assistant tmp if exists
    const idx = messages.value.findIndex(m => m.id === 'tmp')
    if (idx !== -1) messages.value.splice(idx, 1, tmp)
    else messages.value.push(tmp)

    await new Promise(r => setTimeout(r, 250))
  }
  // finalize
  const final = { id: uuidv4(), role: 'assistant', content: text, time: new Date().toISOString() }
  const tIdx = messages.value.findIndex(m => m.id === 'tmp')
  if (tIdx !== -1) messages.value.splice(tIdx, 1, final)
  else messages.value.push(final)
}
</script>

<style scoped>
.dot { display:inline-block }
@keyframes bounce-delay { 0%, 80%, 100% { transform: translateY(0) } 40% { transform: translateY(-6px) } }
.animate-bounce-delay { animation: bounce-delay 1s infinite }
.animate-bounce-delay-200 { animation: bounce-delay 1s 0.15s infinite }
.animate-bounce-delay-400 { animation: bounce-delay 1s 0.3s infinite }
</style>
