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
          <span v-if="auth.isAuthenticated" class="text-sm flex items-center gap-1 font-semibold">
            <span class="bg-green-500 w-2 h-2 inline-block rounded-full"></span>{{ auth.getUsername }}
          </span>
        </div>
      </div>
    </header>

    <!-- Main -->
    <main class="flex-1 overflow-hidden">
      <div class="max-w-4xl mx-auto h-full flex flex-col">

        <!-- Conversation area -->
        <div ref="scrollRoot" class="flex-1 overflow-auto px-4 py-6 pb-32">
          <div class="space-y-4">
            <div v-for="(msg, idx) in messages" :key="msg.id || idx" class="flex" :class="msg.role === 'user' ? 'justify-end' : 'justify-start'">

              <!-- Avatar -->
              <div v-if="msg.role === 'assistant'" class="mr-3">
                <img src="/assets/images/Nehanda.png" alt="Nehanda" class="w-10 h-10 rounded-full" />
              </div>

              <!-- Message bubble -->
              <div :class="[
                  'max-w-[78%] px-4 py-3 rounded-2xl shadow-sm',
                  msg.role === 'user'
                    ? 'bg-gradient-to-r from-[#7D260F] to-[#A13B20] text-white rounded-br-none'
                    : 'bg-white/90 text-gray-900 rounded-bl-none border border-white/30'
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

            <div class="text-xs text-gray-500">Suggestions: cliquez une invite</div>
          </div>
        </div>

      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { v4 as uuidv4 } from 'uuid'
import { useAuthStore } from '@/stores/auth'
const auth = useAuthStore()

// Messages initiaux
const messages = ref([
  { id: uuidv4(), role: 'assistant', content: "Bonjour — je suis Nehanda. En quoi puis-je vous aider aujourd'hui ?", time: new Date().toISOString() },
])

const input = ref('')
const sending = ref(false)
const isTyping = ref(false)
const scrollRoot = ref(null)

const quickPrompts = [
  "Quand sort officiellement Tôswè ?",
  "Pourquoi l’app n’est pas encore prête ?",
  "Quel est l’objectif de Tôswè ?",
  "Comment Tôswè aide les vendeurs illettrés ?",
  "Quelles fonctionnalités arrivent bientôt ?",
  "Est-ce que les marques ont une priorité ?",
  "Comment contacter les administrateurs ?",
  "Est-ce que Tôswè rend les produits locaux plus accessibles ?",
]

const quickReplies = {
  "Quand sort officiellement Tôswè ?": "La plateforme est actuellement en phase de test, la sortie officielle est prévue le mois prochain avec plusieurs nouvelles fonctionnalités.",
  "Pourquoi l’app n’est pas encore prête ?": "Tôswè est encore en phase de test afin d’assurer une meilleure expérience aux vendeurs et acheteurs. C’est normal qu’elle ne soit pas encore disponible à grande échelle.",
  "Quel est l’objectif de Tôswè ?": "Notre but est d’aider les vendeurs locaux, qu’ils soient lettrés ou illettrés, à vendre plus facilement leurs produits, tout en valorisant le Made in Africa et en particulier le Made in Bénin.",
  "Comment Tôswè aide les vendeurs illettrés ?": "Tôswè a été pensée pour être simple d’utilisation et inclusive. Même un vendeur illettré pourra publier et gérer ses produits grâce à une interface intuitive et une assistance adaptée.",
  "Quelles fonctionnalités arrivent bientôt ?": "La sortie officielle apportera : la sponsorisation de produits, un Nehanda plus performant, des statistiques de vente pour les vendeurs, ainsi qu’une meilleure visibilité pour les marques.",
  "Est-ce que les marques ont une priorité ?": "Oui, les marques locales bénéficient d’une certaine priorité sur la plateforme afin de valoriser leurs produits et soutenir leur croissance.",
  "Comment contacter les administrateurs ?": "Vous pouvez contacter les administrateurs via email : contact@toswe.com ou par téléphone : +229 00 00 00 00.",
  "Est-ce que Tôswè rend les produits locaux plus accessibles ?": "Absolument. L’un des objectifs de Tôswè est de rendre les produits locaux plus accessibles et abordables pour le citoyen moyen africain et béninois.",
}

onMounted(() => {
  nextTick(() => {
    const el = scrollRoot.value
    if (el) el.scrollTop = el.scrollHeight
  })
})

function formatTime(iso) {
  try {
    const d = new Date(iso)
    return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  } catch {
    return ''
  }
}

function formatContent(text) {
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
    const assistantReply =
      quickReplies[text] ||
      "Désolé, je n’ai pas encore de réponse pour cette question. Essayez une des suggestions ci-dessus."

    messages.value.push({
      id: uuidv4(),
      role: 'assistant',
      content: assistantReply,
      time: new Date().toISOString(),
    })
  } finally {
    sending.value = false
    isTyping.value = false
  }

  // Scroll automatique vers le bas
  nextTick(() => {
    const el = scrollRoot.value
    if (el) el.scrollTop = el.scrollHeight
  })
}
</script>

<style scoped>
.dot { display:inline-block }
@keyframes bounce-delay { 0%, 80%, 100% { transform: translateY(0) } 40% { transform: translateY(-6px) } }
.animate-bounce-delay { animation: bounce-delay 1s infinite }
.animate-bounce-delay-200 { animation: bounce-delay 1s 0.15s infinite }
.animate-bounce-delay-400 { animation: bounce-delay 1s 0.3s infinite }
</style>
