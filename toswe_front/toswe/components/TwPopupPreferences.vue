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
          </div>

          <!-- Formulaire -->
          <form class="w-full space-y-4" @submit.prevent="">

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
const visible = ref(false)

const showPopup = () => { visible.value = true }
const closePopup = () => { visible.value = false }
defineExpose({ showPopup })

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
.label {
  display: block;
  margin-bottom: 0.25rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}
.input {
  width: 100%;
  border-radius: 0.75rem;
  border: 1px solid #d1d5db;
  padding: 0.75rem 1rem;
  font-size: 0.95rem;
  outline: none;
  transition: border 0.2s, box-shadow 0.2s;
}
.input:focus {
  border-color: #7D260F;
  box-shadow: 0 0 0 2px rgba(125, 38, 15, 0.2);
}
</style>
