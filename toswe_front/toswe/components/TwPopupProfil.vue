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
              Profil utilisateur
            </h3>
            <p class="text-sm text-gray-500 dark:text-gray-400 mt-1" v-if="auth.isSeller">
              {{ auth.isSeller ? 'Vendeur' : 'Acheteur' }} 
              <span v-if="auth.isBrand">• Marque</span>
              <span class="ml-2 px-2 py-0.5 text-xs rounded-full" 
                :class="auth.isVerified ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'" v-if="auth.isSeller">
                {{ auth.isVerified ? 'Vérifié' : 'Non vérifié' }}
              </span>
            </p>
          </div>

          <!-- Formulaire -->
          <form class="w-full space-y-4" @submit.prevent="updateUser">
            <div>
              <label class="label">Nom</label>
              <input type="text" placeholder="Nom" class="input" v-model="username" />
            </div>
            <div>
              <label class="label">Téléphone</label>
              <input type="text" placeholder="Téléphone" class="input" v-model="phone" />
            </div>
            <div>
              <label class="label">Adresse</label>
              <input type="text" placeholder="Adresse" class="input" v-model="address" />
            </div>

            <template v-if="auth.isSeller">
              <div>
                <label class="label">Nom de votre boutique</label>
                <input type="text" placeholder="Nom de la boutique" class="input" v-model="shopName" />
              </div>
              <div>
                <label class="label">À propos</label>
                <textarea placeholder="Parlez un peu de votre boutique..." class="input" rows="3" v-model="about"></textarea>
              </div>
              <div>
                <label class="label">Slogan</label>
                <textarea placeholder="Votre slogan" class="input" rows="2" v-model="slogan"></textarea>
              </div>
            </template>

            <!-- Bouton CTA -->
            <button
              type="submit"
              class="w-full px-6 py-3 bg-[#7D260F] text-white text-base font-semibold rounded-full 
                     shadow-md hover:shadow-lg hover:bg-[#661f0c] transition-all duration-300 flex items-center justify-center gap-2"
            >
              <Icon name="uil:check" class="w-5 h-5" />
              Mettre à jour
            </button>
          </form>

          <!-- Lien boutique -->
          <span 
            v-if="auth.isSeller" 
            @click="goToShop" 
            class="text-[#7D260F] hover:text-[#5E1D0B] font-medium transition-colors cursor-pointer"
          >
            Consulter ma boutique →
          </span>
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

const shopName = ref(auth.getShopName)
const about = ref(auth.getAbout)
const slogan = ref(auth.getSlogan)
const address = ref(auth.getAddress)
const phone = ref(auth.getPhone)
const username = ref(auth.getUsername)

const updateUser = async () => {
  await auth.updateUser(
    username.value,
    phone.value,
    address.value,
    shopName.value,
    about.value,
    slogan.value
  )
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
