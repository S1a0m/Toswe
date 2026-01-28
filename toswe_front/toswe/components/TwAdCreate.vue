<template>
  <section class="px-4 md:px-8 py-12 max-w-5xl mx-auto">
    <!-- Titre -->
    <h2 class="text-3xl md:text-4xl font-bold text-[#7D260F] mb-3 font-[Kenia]">
      Créer une annonce générale
    </h2>
    <p class="text-gray-600 mb-8">⚠️ Une fois lancée, vous ne pourrez plus modifier votre annonce!</p>

    <!-- Wizard container -->
    <div class="bg-white shadow-xl rounded-3xl p-6 md:p-10 border border-gray-100">
      <!-- Barre de progression -->
      <div class="relative mb-10">
        <!-- Ligne arrière -->
        <div class="absolute top-1/2 left-0 w-full h-1 bg-gray-200 rounded-full -translate-y-1/2"></div>
        <!-- Ligne avant -->
        <div
          class="absolute top-1/2 left-0 h-1 bg-gradient-to-r from-[#7D260F] to-[#B3451A] rounded-full -translate-y-1/2 transition-all duration-300"
          :style="{ width: ((currentStep + 1) / steps.length) * 100 + '%' }"
        ></div>

        <!-- Points étapes -->
        <div class="flex justify-between relative z-10">
          <div
            v-for="(step, index) in steps"
            :key="index"
            class="flex flex-col items-center text-center w-1/4"
          >
            <div
              class="flex items-center justify-center w-10 h-10 rounded-full font-semibold text-sm shadow transition-colors duration-300"
              :class="[
                currentStep === index
                  ? 'bg-[#7D260F] text-white shadow-lg'
                  : currentStep > index
                  ? 'bg-green-500 text-white'
                  : 'bg-gray-200 text-gray-500'
              ]"
            >
              {{ index + 1 }}
            </div>
            <span
              class="mt-2 text-xs md:text-sm font-medium transition-colors duration-300"
              :class="currentStep === index ? 'text-[#7D260F]' : 'text-gray-400'"
            >
              {{ step }}
            </span>
          </div>
        </div>
      </div>

      <!-- Formulaire multi-étapes -->
      <div class="space-y-8">
        <transition name="fade" mode="out-in">
          <!-- Étape 1: Infos -->
          <div v-if="currentStep === 0" key="step-1" class="space-y-5">
            <div>
              <label for="title" class="block mb-2 font-medium text-gray-700">Titre</label>
              <input
                id="title"
                v-model="form.title"
                type="text"
                class="w-full rounded-2xl border border-gray-300 p-3 focus:ring-2 focus:ring-[#7D260F] focus:border-[#7D260F] transition"
                placeholder="Titre accrocheur..."
                required
              />
            </div>
            <div>
              <label for="description" class="block mb-2 font-medium text-gray-700">Description</label>
              <textarea
                id="description"
                v-model="form.description"
                rows="5"
                class="w-full rounded-2xl border border-gray-300 p-3 focus:ring-2 focus:ring-[#7D260F] focus:border-[#7D260F] transition"
                placeholder="Décrivez votre publicité..."
                required
              ></textarea>
            </div>
          </div>

          <!-- Étape 2: Image -->
          <div v-else-if="currentStep === 1" key="step-2" class="space-y-5">
            <label for="image" class="block mb-2 font-medium text-gray-700">Image</label>
            <input
              id="image"
              type="file"
              @change="onFileChange"
              class="w-full rounded-2xl border border-gray-300 p-2 focus:ring-2 focus:ring-[#7D260F] focus:border-[#7D260F] transition"
            />
            <div
              v-if="form.imagePreview"
              class="mt-4 w-48 h-32 rounded-xl overflow-hidden border shadow-sm"
            >
              <img
                :src="form.imagePreview"
                class="w-full h-full object-cover"
                alt="Aperçu image publicité"
              />
            </div>
          </div>

          <!-- Étape 3: Confirmation -->
          <div v-else key="step-3" class="space-y-4 text-gray-700">
            <h3 class="text-xl font-semibold">Résumé de l’annonce</h3>
            <div class="space-y-3">
              <div v-if="form.imagePreview">
                <img :src="form.imagePreview" class="w-48 h-32 object-cover rounded-xl" />
              </div>
              <p><strong>Titre :</strong> {{ form.title }}</p>
              <p><strong>Description :</strong> {{ form.description }}</p>
            </div>
          </div>
        </transition>

        <!-- Navigation -->
        <div class="flex justify-between pt-6">
          <button
            type="button"
            @click="prevStep"
            v-if="currentStep > 0"
            class="px-5 py-2 rounded-xl border text-gray-600 hover:bg-gray-100 transition"
          >
            Précédent
          </button>

          <button
            v-if="currentStep < steps.length - 1"
            type="button"
            @click="nextStep"
            class="ml-auto px-6 py-3 bg-[#7D260F] text-white font-semibold rounded-xl shadow hover:bg-[#661f0c] transition"
          >
            Suivant
          </button>

          <button
            v-if="currentStep === steps.length - 1"
            @click="showPopup = true"
            class="ml-auto px-6 py-3 bg-green-600 text-white font-semibold rounded-xl shadow hover:bg-green-700 transition"
          >
            Créer l’annonce
          </button>
        </div>
      </div>
    </div>
  </section>

  <!-- Popup paiement -->
  <TwPopupPayment
    v-if="showPopup"
    :visible="showPopup"
    payment-type="advertisement"
    @close="showPopup = false"
    @pay="submitAd"
  />

  <!-- Toast notification -->
  <TwToast
    v-if="toast.visible"
    :message="toast.message"
    :type="toast.type"
    :duration="3000"
  />
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>


<script setup>
import { ref } from "vue"
import { useAuthStore } from '@/stores/auth'
import TwToast from "@/components/TwToast.vue"
import { useNavigation } from "@/composables/useNavigation";

const { goToMyShop } = useNavigation();

const steps = ["Infos", "Image", "Confirmation"]
const currentStep = ref(0)

const auth = useAuthStore()
const showPopup = ref(false)

const form = ref({
  ad_type: "generic",
  title: "",
  description: "",
  image: null,
  imagePreview: null,
  amount: null,
})

const toast = ref({ visible: false, message: "", type: "success" })

const nextStep = () => {
  if (currentStep.value < steps.length - 1) currentStep.value++
}
const prevStep = () => {
  if (currentStep.value > 0) currentStep.value--
}

const onFileChange = (e) => {
  const file = e.target.files[0]
  if (file) {
    form.value.image = file
    form.value.imagePreview = URL.createObjectURL(file)
  }
}

function showToast(message, type = "success") {
  toast.value = { visible: true, message, type }
  setTimeout(() => {
    toast.value.visible = false
  }, 3000)
}

async function submitAd(payload) {
  const formData = new FormData()
  for (const key in form.value) {
    if (form.value[key] !== null) formData.append(key, form.value[key])
  }

  try {
    if (payload.paymentType === "advertisement") {
      const body = { amount: payload.totalPrice }
      formData.append("amount", body.amount)

      const res = await $fetch("http://127.0.0.1:8000/api/ad/", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${auth.accessToken}`,
        },
        credentials: "include",
        body: formData,
      })
      showToast("✅ Annonce créée avec succès !", "success")
      setTimeout(() => goToMyShop(), 700)
      console.log("Annonce envoyée :", res)
    }
  } catch (err) {
    console.error(err)
    showToast("❌ Erreur lors de la création de l’annonce", "error")
  }
}
</script>

