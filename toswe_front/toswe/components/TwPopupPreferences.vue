<template>
  <transition name="fade">
    <div
      v-if="visible"
      class="fixed inset-0 z-[2000] flex items-center justify-center px-4"
    >
      <!-- Overlay sombre -->
      <div
        class="absolute inset-0 bg-black/40 backdrop-blur-sm"
        @click="closePopup"
      ></div>

      <!-- Popup style glass -->
      <div
        class="relative z-10 rounded-2xl shadow-2xl w-full max-w-md p-6 border border-white/20 backdrop-blur-lg 
               sm:max-w-lg md:max-w-xl"
        style="background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.05));"
      >
        <!-- Bouton fermer -->
        <button
          @click="closePopup"
          class="absolute top-4 right-4 text-gray-600 dark:text-gray-300 hover:text-black dark:hover:text-white transition"
          aria-label="Fermer"
        >
          <Icon name="uil:times" class="w-6 h-6" />
        </button>

        <!-- Contenu -->
        <div class="flex flex-col items-center gap-6">
          <!-- Titre -->
          <div class="text-center">
            <h3 class="text-xl font-bold text-gray-900 dark:text-white">
              Choisissez vos préférences produits
            </h3>
            <p class="text-sm text-gray-500 mt-1">Sélectionnez les produits qui vous intéressent</p>
          </div>

          <!-- Formulaire -->
          <form class="w-full space-y-4" @submit.prevent="submitPreferences">

            <!-- Liste des préférences -->
            <div class="grid grid-cols-2 gap-3">
              <label
                v-for="pref in productPreferences"
                :key="pref"
                class="flex items-center space-x-2 cursor-pointer"
              >
                <input
                  type="checkbox"
                  class="rounded border-gray-300 text-[#7D260F] focus:ring-[#7D260F]"
                  :value="pref"
                  v-model="selectedPreferences"
                />
                <span class="text-sm text-gray-700">{{ pref }}</span>
              </label>
            </div>

            <!-- Bouton CTA -->
            <button
              type="submit"
              class="w-full px-6 py-3 bg-[#7D260F] text-white text-base font-semibold rounded-full 
                     shadow-md hover:shadow-lg hover:bg-[#661f0c] transition-all duration-300 flex items-center justify-center gap-2"
            >
              <Icon name="uil:check" class="w-5 h-5" />
              Soumettre mes préférences
            </button>
          </form>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
const auth = useAuthStore()
const { $apiFetch } = useNuxtApp()

const visible = ref(false)
const showPopup = () => { visible.value = true }
const closePopup = () => { visible.value = false }
defineExpose({ showPopup })

// Liste des préférences produits (tu peux la charger du backend si tu veux)
const productPreferences = [
  "Fruits",
  "Légumes",
  "Vêtements",
  "Cosmétiques",
  "Accessoires",
  "Agroalimentaire",
  "Céréales",
  "Artisanat",
]

// Sélections utilisateur
const selectedPreferences = ref([])

// Soumettre au backend
async function submitPreferences() {
  try {
    const res = await $apiFetch("/user/preferences/", {
      method: "POST",
      body: { preferences: selectedPreferences.value },
    })
    console.log("Préférences sauvegardées:", res)
    closePopup()
  } catch (err) {
    console.error("Erreur lors de l’envoi des préférences:", err)
  }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease, transform 0.4s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}
</style>
