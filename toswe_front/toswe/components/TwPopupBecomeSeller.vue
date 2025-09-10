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
              Devenir vendeur
            </h3>
          </div>

          <!-- Formulaire -->
          <form class="w-full space-y-4" @submit.prevent="submitForm">
            <!-- Nom boutique -->
            <div>
              <label class="label">Nom de votre boutique</label>
              <input type="text" placeholder="Nom de la boutique" class="input" v-model="shopName" />
            </div>

            <!-- Catégories -->
            <div>
              <label class="label">Catégorie</label>
              <select class="input" v-model="selectedCategories" multiple>
                <option v-for="category in categories.results" :key="category.id" :value="category.id">
                  {{ category.name }}
                </option>
              </select>
              <p class="text-xs text-gray-500 mt-1">Maintenez <kbd>Ctrl</kbd> (ou <kbd>Cmd</kbd>) pour sélectionner plusieurs.</p>
            </div>

            <!-- Logo + preview -->
            <div>
              <label class="label">Votre logo</label>
              <input type="file" class="input" accept="image/*" @change="onFileChange" />
              <div v-if="logoPreview" class="mt-3 flex justify-center">
                <img :src="logoPreview" alt="Aperçu logo" class="max-h-32 rounded-lg shadow-md" />
              </div>
            </div>

            <!-- À propos -->
            <div>
              <label class="label">À propos</label>
              <textarea placeholder="Parlez un peu de votre boutique..." class="input" rows="3" v-model="about"></textarea>
            </div>

            <!-- Slogan -->
            <div>
              <label class="label">Slogan</label>
              <textarea placeholder="Votre slogan" class="input" rows="2" v-model="slogan"></textarea>
            </div>

            <!-- CTA -->
            <button
              type="submit"
              class="w-full px-6 py-3 bg-[#7D260F] text-white text-base font-semibold rounded-full 
                     shadow-md hover:shadow-lg hover:bg-[#661f0c] transition-all duration-300 flex items-center justify-center gap-2"
            >
              <Icon name="uil:check" class="w-5 h-5" />
              Envoyer ma demande
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

// Champs du formulaire
const shopName = ref("")
// const address = ref(auth.getAddress || "")
const about = ref("")
const slogan = ref("")
const selectedCategories = ref([])
const logoFile = ref(null)
const logoPreview = ref(null)

// Catégories disponibles
const { data: categories, pending, error } = await useAsyncData('categories', () =>
  $fetch('http://127.0.0.1:8000/api/category/')
)
/*const categories = [
  'Accessoires',
  'Agroalimentaire',
  'Artisanat',
  'Céréales',
  'Cosmétiques',
  'Cuisines & Ustensiles',
  'Fruits',
  'Marques',
  'Vêtements',
]*/

// Gestion du fichier
function onFileChange(e) {
  const file = e.target.files[0]
  if (file) {
    logoFile.value = file
    logoPreview.value = URL.createObjectURL(file)
  }
}

// Soumission formulaire
async function submitForm() {
  if (!auth.accessToken) return

  const formData = new FormData()
  formData.append("shop_name", shopName.value)
  formData.append("about", about.value)
  formData.append("slogan", slogan.value)
  //formData.append("address", address.value) // depuis ton store
  formData.append("categories", selectedCategories.value.join(",")) // backend reçoit string CSV
  if (logoFile.value) {
    formData.append("logo", logoFile.value)
  }

  try {
    const json = await $apiFetch("http://127.0.0.1:8000/api/user/become_seller/", {
      method: "POST",
      body: formData,
    })
    console.log("Seller profile created:", json)
    auth.user.is_seller = true
    closePopup()
  } catch (err) {
    console.error("Erreur création vendeur:", err)
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
