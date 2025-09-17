<template>
  <section class="min-h-screen bg-gradient-to-br from-[#fff7f5] to-[#fbe9e7] p-4 flex items-center justify-center">
    <div class="bg-white shadow-2xl rounded-2xl w-full max-w-5xl grid lg:grid-cols-2 overflow-hidden">
      
      <!-- Colonne gauche : Info -->
      <aside class="hidden lg:flex flex-col justify-center bg-[#7D260F] text-white p-8 space-y-6">
        <h2 class="text-2xl font-bold">Rejoignez la communauté Tôswè</h2>
        <p class="leading-relaxed">
          Vous pouvez à tout moment quitter le statut de simple client pour devenir 
          <span class="font-semibold">vendeur</span>.  
          Mettez vos produits en avant et touchez plus de clients grâce à notre plateforme.
        </p>
        <p class="leading-relaxed">
          Notre conviction est simple : 
          <span class="font-semibold">les produits africains méritent une vitrine mondiale</span>.
        </p>
        <ul class="space-y-2 text-sm">
          <li>✔️ Vendez vos produits locaux en ligne</li>
          <li>✔️ Accédez à de nouveaux marchés</li>
          <li>✔️ Simple et rapide à configurer</li>
        </ul>
      </aside>

      <!-- Colonne droite : Formulaire existant -->
      <div class="p-8 relative">
        <!-- Barre de progression -->
        <div class="absolute top-0 left-0 w-full h-1 bg-gray-200">
          <div
            class="h-1 bg-[#7D260F] transition-all duration-500"
            :style="{ width: step === 1 ? '50%' : '100%' }"
          ></div>
        </div>

        <!-- Titre -->
        <h1 class="text-2xl font-bold text-center text-[#7D260F] mb-6">
          Mi do gbe nu mi ɖo Tôswè xwe
        </h1>

        <!-- Étapes -->
        <transition name="fade" mode="out-in">
          <!-- Étape 1 : téléphone -->
          <form
            v-if="step === 1"
            key="step1"
            @submit.prevent="initConnexion"
            class="space-y-4"
          >
            <div>
              <label class="block text-sm font-semibold mb-1">Votre numéro de téléphone</label>
              <div class="relative">
                <input
                  v-model="phone"
                  type="text"
                  class="w-full border rounded-lg p-3 pl-10 focus:ring-2 focus:ring-[#7D260F] outline-none"
                  placeholder="Ex: +229 01 2345678"
                  required
                />
                <span class="absolute left-3 top-3 text-gray-400">📱</span>
              </div>
            </div>
            <button
              type="submit"
              class="w-full bg-[#7D260F] text-white py-3 rounded-lg font-semibold shadow hover:bg-[#5c1d0c] transition flex justify-center items-center"
              :disabled="loading"
            >
              <span v-if="loading" class="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-white mr-2"></span>
              {{ loading ? 'Vérification...' : 'Continuer' }}
            </button>
            <p class="text-xs text-gray-500 text-center mt-4">
              En vous connectant, vous acceptez que vos données soient utilisées pour améliorer 
              votre expérience sur Tôswè, conformément à notre 
              <a href="/politique-confidentialite" class="text-[#7D260F] underline hover:text-[#5c1d0c]">
                politique de confidentialité
              </a>.
            </p>
          </form>

          <!-- Étape 2 : OTP -->
          <form
            v-else-if="step === 2"
            key="step2"
            @submit.prevent="confirmConnexion"
            class="space-y-4"
          >
            <p class="text-gray-600 text-sm">
              Entrez le code reçu par SMS au numéro ci-dessous.
            </p>

            <div>
              <label class="block text-sm font-semibold mb-1">Numéro de téléphone</label>
              <input
                v-model="phone"
                type="text"
                readonly
                class="w-full border rounded-lg p-3 bg-gray-100 text-gray-500 cursor-not-allowed"
              />
            </div>

            <div>
              <label class="block text-sm font-semibold mb-1">Code OTP</label>
              <div class="flex justify-between gap-2">
                <input
                  v-for="(digit, index) in otpInputs"
                  :key="index"
                  v-model="otpInputs[index]"
                  maxlength="1"
                  type="text"
                  class="w-12 h-12 text-center border rounded-lg focus:ring-2 focus:ring-[#7D260F] text-lg font-semibold"
                  @input="moveNext(index, $event)"
                />
              </div>
            </div>

            <!-- Countdown -->
            <div class="text-sm text-center text-gray-500">
              <span v-if="countdown > 0">Renvoyer dans {{ countdown }}s</span>
              <button
                v-else
                type="button"
                class="text-[#7D260F] underline"
                @click="resendOtp"
              >
                Renvoyer le code
              </button>
            </div>

            <button
              type="submit"
              class="w-full bg-[#7D260F] text-white py-3 rounded-lg font-semibold shadow hover:bg-[#5c1d0c] transition flex justify-center items-center"
              :disabled="loading"
            >
              <span v-if="loading" class="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-white mr-2"></span>
              {{ loading ? 'Connexion...' : 'Se connecter' }}
            </button>
            <p class="text-xs text-gray-500 text-center mt-4">
              En vous connectant, vous acceptez que vos données soient utilisées pour améliorer 
              votre expérience sur Tôswè, conformément à notre 
              <a href="/politique-confidentialite" class="text-[#7D260F] underline hover:text-[#5c1d0c]">
                politique de confidentialité
              </a>.
            </p>
          </form>
        </transition>
      </div>
    </div>

    <!-- Toast -->
    <TwToast
      v-if="toast.show"
      :message="toast.message"
      :type="toast.type"
    />
  </section>
</template>


<style>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.4s;
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
    await auth.initConnexion(phone.value)
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
    await auth.confirmConnexion(phone.value, otp)
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
