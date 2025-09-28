<template>
  <section class="min-h-screen bg-gradient-to-br from-[#fff8f6] to-[#fdece9] px-4 flex items-center justify-center">
    <div class="bg-white shadow-xl rounded-2xl w-full max-w-5xl grid lg:grid-cols-2 overflow-hidden">

      <!-- Colonne gauche : Carrousel -->
      <aside class="hidden lg:flex flex-col justify-center items-center bg-[#7D260F] text-white p-10 space-y-8 relative">
        <!-- Messages -->
        <div class="w-full relative overflow-hidden">
          <div
            class="flex transition-transform duration-700 ease-in-out"
            :style="{ transform: `translateX(-${currentIndex * 100}%)` }"
          >
            <div
              v-for="(msg, idx) in messages"
              :key="idx"
              class="min-w-full px-8 py-10 bg-white/10 backdrop-blur-sm rounded-xl shadow-lg text-center"
            >
              <h2 class="text-2xl font-bold mb-4 tracking-wide">Tôswè</h2>
              <p class="leading-relaxed text-lg font-medium max-w-md mx-auto">
                {{ msg }}
              </p>
            </div>
          </div>
        </div>

        <!-- Indicateurs -->
        <div class="flex space-x-2 absolute bottom-6">
          <button
            v-for="(msg, idx) in messages"
            :key="idx"
            class="w-3 h-3 rounded-full transition transform"
            :class="idx === currentIndex ? 'bg-white scale-110 shadow' : 'bg-white/40 hover:bg-white/60'"
            @click="currentIndex = idx"
          ></button>
        </div>
      </aside>

      <!-- Colonne droite : Formulaire -->
      <div class="p-8 sm:p-12 relative flex flex-col justify-center">

        <!-- Barre de progression -->
        <div class="absolute top-0 left-0 w-full h-1 bg-gray-200">
          <div
            class="h-1 bg-[#7D260F] transition-all duration-500"
            :style="{ width: step === 1 ? '50%' : '100%' }"
          ></div>
        </div>

        <!-- Titre -->
        <h1 class="text-2xl sm:text-3xl font-extrabold text-center text-[#7D260F] mb-8 tracking-tight">
          Mi do gbe nu mi ɖo Tôswè xwe
        </h1>

        <!-- Étapes -->
        <transition name="fade" mode="out-in">
          <!-- Étape 1 -->
          <form
            v-if="step === 1"
            key="step1"
            @submit.prevent="initConnexion"
            class="space-y-6"
          >
            <!-- Téléphone -->
            <div>
              <label class="block text-sm font-medium mb-2 text-gray-700">Votre numéro de téléphone</label>
              <div class="relative">
                <input
                  v-model="phone"
                  type="tel"
                  class="w-full border border-gray-300 rounded-xl p-3 pl-12 focus:ring-2 focus:ring-[#7D260F] outline-none transition"
                  placeholder="+229 01 2345678"
                  required
                />
                <span class="absolute left-4 top-3.5 text-gray-400">📱</span>
              </div>
            </div>

            <!-- Bouton -->
            <button
              type="submit"
              class="w-full bg-[#7D260F] text-white py-3 rounded-xl font-semibold shadow-md hover:bg-[#5c1d0c] transition disabled:opacity-50 disabled:cursor-not-allowed flex justify-center items-center"
              :disabled="loading"
            >
              <span v-if="loading" class="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-white mr-2"></span>
              {{ loading ? 'Vérification...' : 'Continuer' }}
            </button>

            <!-- Politique -->
            <p class="text-xs text-gray-500 text-center">
              En vous connectant, vous acceptez que vos données soient utilisées pour améliorer votre expérience sur Tôswè, conformément à notre
              <a href="/pc-cgu" class="text-[#7D260F] underline hover:text-[#5c1d0c]">politique de confidentialité</a>.
            </p>
          </form>

          <!-- Étape 2 -->
          <form
            v-else-if="step === 2"
            key="step2"
            @submit.prevent="confirmConnexion"
            class="space-y-6"
          >
            <p class="text-gray-600 text-sm mb-2 text-center">
              Entrez le code reçu par SMS 📩
            </p>

            <!-- Numéro affiché -->
            <input
              v-model="phone"
              type="text"
              readonly
              class="w-full border rounded-xl p-3 bg-gray-100 text-gray-500 cursor-not-allowed text-center"
            />

            <!-- OTP -->
            <div class="flex justify-between gap-2">
              <input
                v-for="(digit, index) in otpInputs"
                :key="index"
                v-model="otpInputs[index]"
                maxlength="1"
                type="text"
                inputmode="numeric"
                class="w-12 h-12 text-center border rounded-lg focus:ring-2 focus:ring-[#7D260F] text-lg font-semibold"
                @input="moveNext(index, $event)"
              />
            </div>

            <!-- Champ pseudo si nouvel utilisateur -->
            <div v-if="!isSubscriber" class="mt-4">
              <label class="block text-sm font-medium mb-2 text-gray-700">Choisissez votre pseudo</label>
              <input
                v-model="username"
                type="text"
                class="w-full border border-gray-300 rounded-xl p-3 focus:ring-2 focus:ring-[#7D260F] outline-none transition"
                placeholder="Entrez un nom d’utilisateur"
                required
              />
            </div>

            <!-- Countdown -->
            <div class="text-sm text-center text-gray-500">
              <span v-if="countdown > 0">Renvoyer dans {{ countdown }}s</span>
              <button
                v-else
                type="button"
                class="text-[#7D260F] underline hover:text-[#5c1d0c]"
                @click="resendOtp"
              >
                Renvoyer le code
              </button>
            </div>

            <!-- Bouton -->
            <button
              type="submit"
              class="w-full bg-[#7D260F] text-white py-3 rounded-xl font-semibold shadow-md hover:bg-[#5c1d0c] transition flex justify-center items-center disabled:opacity-50"
              :disabled="loading"
            >
              <span v-if="loading" class="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-white mr-2"></span>
              {{ loading ? 'Connexion...' : 'Se connecter' }}
            </button>
          </form>

        </transition>
      </div>
    </div>

    <!-- Toast -->
    <TwToast v-if="toast.show" :message="toast.message" :type="toast.type" />
  </section>
</template>


<style>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.6s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const step = ref(1)
const phone = ref('')
const loading = ref(false)
const auth = useAuthStore()

const isSubscriber = ref(true) 
const username = ref('') 

const messages = ref([
  "Vous pouvez à tout moment quitter le statut de simple client pour devenir vendeur",
  "Mettez vos produits en avant et touchez plus de clients grâce à notre plateforme",
  "Notre conviction est simple : les produits africains méritent une vitrine mondiale",
])
const currentIndex = ref(0)
let carouselTimer = null

onMounted(() => {
  carouselTimer = setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % messages.value.length
  }, 5000) // défile toutes les 5s
})

onUnmounted(() => {
  if (carouselTimer) clearInterval(carouselTimer)
})


// Toast
const toast = ref({ message: "", type: "success", show: false })
const showToast = (message, type = "success") => {
  toast.value = { message, type, show: true }
  setTimeout(() => { toast.value.show = false }, 3000)
}

// OTP inputs
const otpInputs = ref(["", "", "", "", "", ""])
const countdown = ref(60)
let timer = null

const initConnexion = async () => {
  loading.value = true
  try {
    const res = await auth.initConnexion(phone.value)
    isSubscriber.value = res.is_subscriber  // <-- récupère valeur du backend
    console.log("Abbonne:", isSubscriber.value)
    step.value = 2
    startCountdown()
    showToast("Code envoyé ✅", "success")
  } catch (error) {
    showToast(`Erreur: ${error.detail || 'Échec de la vérification.'}`, "error")
  } finally {
    loading.value = false
  }
}

const confirmConnexion = async () => {
  loading.value = true
  try {
    const otp = otpInputs.value.join("")
    const payload = { phone: phone.value, otp }

    // Ajoute username si utilisateur nouveau
    if (!isSubscriber.value) {
      if (!username.value) {
        showToast("Veuillez choisir un pseudo ✍️", "error")
        loading.value = false
        return
      }
      payload.username = username.value
    }

    await auth.confirmConnexion(payload)
    showToast("Connexion réussie 🎉", "success")
    setTimeout(() => navigateTo("/market"), 1000)
  } catch (error) {
    showToast(`Erreur: ${error.detail || 'Échec de la connexion.'}`, "error")
  } finally {
    loading.value = false
  }
}

const moveNext = (index, event) => {
  if (event.target.value && index < otpInputs.value.length - 1) {
    const next = event.target.parentElement.children[index + 1]
    next.focus()
  }
}

const startCountdown = () => {
  countdown.value = 60
  timer = setInterval(() => {
    if (countdown.value > 0) {
      countdown.value--
    } else {
      clearInterval(timer)
    }
  }, 1000)
}

const resendOtp = async () => {
  try {
    await auth.initConnexion(phone.value)
    startCountdown()
    showToast("Nouveau code envoyé 🔄", "info")
  } catch {
    showToast("Impossible de renvoyer le code ❌", "error")
  }
}

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>
