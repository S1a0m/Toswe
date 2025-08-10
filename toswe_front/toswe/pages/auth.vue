<template>
  <section class="min-h-screen flex justify-center items-center bg-[#F6F3F0] p-4">
    <div class="bg-white shadow-xl rounded-xl w-full max-w-md p-6">
      <h1 class="text-xl font-bold text-center text-[#7D260F] mb-6">
        Connexion à Toswe via Racine
      </h1>

      <!-- ÉTAPE 1 -->
      <form v-if="step === 1" @submit.prevent="checkRacineId">
        <div class="mb-4">
          <label class="block font-semibold mb-1">ID Racine</label>
          <input
            v-model="racineId"
            type="text"
            class="w-full border rounded p-2 focus:ring-2 focus:ring-[#7D260F]"
            placeholder="Ex: RAC123456"
            required
          />
        </div>
        <button
          type="submit"
          class="w-full bg-[#7D260F] text-white py-2 rounded hover:bg-[#5c1d0c]"
          :disabled="loading"
        >
          {{ loading ? 'Vérification...' : 'Continuer' }}
        </button>
      </form>

      <!-- ÉTAPE 2 -->
      <form v-else-if="step === 2" @submit.prevent="finalLogin">
        <p class="text-gray-600 mb-4 text-sm">
          Veuillez retaper votre ID Racine et entrer le token copié depuis l'app Racine.
        </p>
        <div class="mb-4">
          <label class="block font-semibold mb-1">ID Racine</label>
          <input
            v-model="racineIdConfirm"
            type="text"
            class="w-full border rounded p-2 focus:ring-2 focus:ring-[#7D260F]"
            required
          />
        </div>
        <div class="mb-4">
          <label class="block font-semibold mb-1">Token Racine</label>
          <input
            v-model="racineToken"
            type="text"
            class="w-full border rounded p-2 focus:ring-2 focus:ring-[#7D260F]"
            placeholder="Collez le token ici"
            required
          />
        </div>
        <button
          type="submit"
          class="w-full bg-[#7D260F] text-white py-2 rounded hover:bg-[#5c1d0c]"
          :disabled="loading"
        >
          {{ loading ? 'Connexion...' : 'Se connecter' }}
        </button>
      </form>

      <!-- SUCCÈS -->
      <div v-else class="text-center">
        <p class="text-green-700 font-bold mb-2">
          ✅ Connecté avec succès à Toswe via Racine !
        </p>
        <p class="text-gray-600">Bienvenue, {{ racineId }}</p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const step = ref(1)
const racineId = ref('')
const racineIdConfirm = ref('')
const racineToken = ref('')
const loading = ref(false)

const checkRacineId = () => {
  loading.value = true
  setTimeout(() => {
    // Simulation vérification Racine
    if (racineId.value.trim().length > 5) {
      step.value = 2
    } else {
      alert('ID Racine invalide.')
    }
    loading.value = false
  }, 1000)
}

const finalLogin = () => {
  if (racineIdConfirm.value !== racineId.value) {
    alert("L'ID Racine ne correspond pas.")
    return
  }
  if (racineToken.value.trim().length < 5) {
    alert('Token invalide.')
    return
  }

  loading.value = true
  setTimeout(() => {
    step.value = 3
    loading.value = false
  }, 1000)
}
</script>
