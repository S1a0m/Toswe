<template>
  <section class="min-h-screen flex justify-center items-center bg-gradient-to-br  p-4"> <!-- from-[#fff7f5] to-[#fbe9e7] -->
    <div class="bg-white shadow-2xl rounded-2xl w-full max-w-md p-8 relative overflow-hidden">
      <!-- Barre de progression -->
      <div class="absolute top-0 left-0 w-full h-1 bg-gray-200">
        <div
          class="h-1 bg-[#7D260F] transition-all duration-500"
          :style="{ width: step === 1 ? '50%' : step === 2 ? '100%' : '100%' }"
        ></div>
      </div>

      <!-- Titre -->
      <h1 class="text-2xl font-bold text-center text-[#7D260F] mb-6">
        Connectez-vous
      </h1>

      <!-- Étape 1 -->
      <transition name="fade" mode="out-in">
        <form
          v-if="step === 1"
          key="step1"
          @submit.prevent="checkphone"
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
              <span class="absolute left-3 top-3 text-gray-400">#</span>
            </div>
          </div>
          <button
            @submit="initConnexion"
            type="submit"
            class="w-full bg-[#7D260F] text-white py-3 rounded-lg font-semibold shadow hover:bg-[#5c1d0c] transition"
            :disabled="loading"
          >
            {{ loading ? 'Vérification...' : 'Continuer' }}
          </button>
        </form>

        <!-- Étape 2 -->
        <form
          v-else-if="step === 2"
          key="step2"
          @submit.prevent="confirmConnexion"
          class="space-y-4"
        >
          <p class="text-gray-600 text-sm">
            Retapez votre numéro et entrez le pass qui vous a été envoyé par sms.
          </p>

          <div>
            <label class="block text-sm font-semibold mb-1">Numéro de téléphone</label>
            <div class="relative">
              <input
                v-model="phoneConfirm"
                type="text"
                class="w-full border rounded-lg p-3 pl-10 focus:ring-2 focus:ring-[#7D260F] outline-none"
                required
              />
              <span class="absolute left-3 top-3 text-gray-400">#</span>
            </div>
          </div>

          <div>
            <label class="block text-sm font-semibold mb-1">Pass</label>
            <div class="relative">
              <input
                v-model="otp"
                type="text"
                class="w-full border rounded-lg p-3 pl-10 focus:ring-2 focus:ring-[#7D260F] outline-none"
                placeholder="Collez le token ici"
                required
              />
              <span class="absolute left-3 top-3 text-gray-400">🔑</span>
            </div>
          </div>

          <button
            type="submit"
            class="w-full bg-[#7D260F] text-white py-3 rounded-lg font-semibold shadow hover:bg-[#5c1d0c] transition"
            :disabled="loading"
          >
            {{ loading ? 'Connexion...' : 'Se connecter' }}
          </button>
        </form>
      </transition>
    </div>
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
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const step = ref(1)
const phone = ref('')
const phoneConfirm = ref('')
const racineToken = ref('')
const loading = ref(false)

const auth = useAuthStore()
const router = useRouter()

const otp = ref("")

const initConnexion = async () => {
  await auth.initConnexion(phone.value)
  step.value = 2
}

const confirmConnexion = async () => {
  await auth.confirmConnexion(phone.value, otp.value)
  // Redirection après connexion
  navigateTo("/market")
}

const checkphone = () => {
  loading.value = true
  setTimeout(() => {
    auth.initConnexion(phone.value)
      .then(() => {
        step.value = 2
      })
      .catch((error) => {
        alert(`Erreur: ${error.detail || 'Échec de la vérification de l\'ID Racine.'}`)
      })
      .finally(() => {
        loading.value = false
      })
    loading.value = false
  }, 1000)
}

const finalLogin = () => {
  if (phoneConfirm.value !== phone.value) {
    alert("L'ID Racine ne correspond pas.")
    return
  }
  if (racineToken.value.trim().length < 5) {
    alert('Token invalide.')
    return
  }

  loading.value = true
  setTimeout(() => {
    // Simuler login réussi
    auth.login({
      id_racine: phone.value,
      username: 'John Doe', // simulé
      is_seller: true,      // exemple
      is_premium: false,
    })

    loading.value = false
    router.push('/market')
  }, 1000)
}
</script>
