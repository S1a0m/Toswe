<template>
  <section class="px-4 md:px-8 py-12 max-w-6xl mx-auto">
    <!-- Titre -->
    <h2 class="text-2xl font-bold text-[#7D260F] mb-6 font-[Kenia]">
      Créer une annonce générale
    </h2>

    <!-- Wizard container -->
    <div class="bg-white shadow-lg rounded-2xl p-6 md:p-8 border border-gray-100">
      <!-- Barre de progression -->
      <div class="relative mb-8">
        <div class="absolute top-1/2 left-0 w-full h-[3px] bg-gray-200 -translate-y-4"></div>
        <div
          class="absolute top-1/2 left-0 h-[3px] bg-[#7D260F] -translate-y-4 transition-all duration-300"
          :style="{ width: ((currentStep + 1) / steps.length) * 100 + '%' }"
        ></div>

        <div class="flex justify-between relative z-10">
          <div
            v-for="(step, index) in steps"
            :key="index"
            class="flex flex-col items-center text-center w-1/4"
          >
            <div
              class="flex items-center justify-center w-8 h-8 md:w-10 md:h-10 rounded-full font-bold text-sm transition-colors"
              :class="[
                currentStep === index
                  ? 'bg-[#7D260F] text-white'
                  : currentStep > index
                  ? 'bg-green-500 text-white'
                  : 'bg-gray-200 text-gray-600'
              ]"
            >
              {{ index + 1 }}
            </div>
            <span
              class="mt-2 text-xs md:text-sm font-medium"
              :class="currentStep === index ? 'text-[#7D260F]' : 'text-gray-500'"
            >
              {{ step }}
            </span>
          </div>
        </div>
      </div>

      <!-- Formulaire multi-étapes -->
      <form @submit.prevent="submitAd" class="space-y-6">
        <transition name="fade" mode="out-in">
          <!-- Étape 1: Infos -->
          <div v-if="currentStep === 0" key="step-1" class="space-y-4">
            <div>
              <label for="title" class="block mb-1 font-medium text-gray-700">Titre</label>
              <input
                id="title"
                v-model="form.title"
                type="text"
                class="w-full rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#7D260F] focus:border-[#7D260F]"
                placeholder="Titre accrocheur..."
                required
              />
            </div>
            <div>
              <label for="description" class="block mb-1 font-medium text-gray-700">Description</label>
              <textarea
                id="description"
                v-model="form.description"
                rows="4"
                class="w-full rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#7D260F] focus:border-[#7D260F]"
                placeholder="Décrivez votre publicité..."
                required
              ></textarea>
            </div>
          </div>

          <!-- Étape 2: Image -->
          <div v-else-if="currentStep === 1" key="step-2" class="space-y-4">
            <label for="image" class="block mb-1 font-medium text-gray-700">Image</label>
            <input
              id="image"
              type="file"
              @change="onFileChange"
              class="w-full rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#7D260F] focus:border-[#7D260F]"
            />
            <div
              v-if="form.imagePreview"
              class="mt-3 w-40 h-28 rounded-lg overflow-hidden border shadow-sm"
            >
              <img
                :src="form.imagePreview"
                class="w-full h-full object-cover"
                alt="Aperçu image publicité"
              />
            </div>
          </div>

          <!-- Étape 3: Budget -->
          <div v-else-if="currentStep === 2" key="step-3" class="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div>
              <label for="budget" class="block mb-1 font-medium text-gray-700">Budget (FCFA)</label>
              <input
                id="budget"
                v-model.number="form.amount"
                type="number"
                min="100"
                class="w-full rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#7D260F] focus:border-[#7D260F]"
                placeholder="Ex: 5000"
                required
              />
            </div>
            <div>
              <label for="duration" class="block mb-1 font-medium text-gray-700">Durée (jours)</label>
              <input
                id="duration"
                v-model.number="form.duration"
                type="number"
                min="1"
                class="w-full rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#7D260F] focus:border-[#7D260F]"
                placeholder="Ex: 7"
                required
              />
            </div>
          </div>

          <!-- Étape 4: Confirmation -->
          <div v-else key="step-4" class="space-y-4 text-gray-700">
            <h3 class="text-lg font-semibold">Résumé de l’annonce</h3>
            <ul class="space-y-2 text-sm">
              <li v-if="form.imagePreview">
                <img :src="form.imagePreview" class="w-40 h-28 object-cover rounded-md" />
              </li>
              <li><strong>Titre :</strong> {{ form.title }}</li>
              <li><strong>Description :</strong> {{ form.description }}</li>
              <li><strong>Budget :</strong> {{ form.amount }} FCFA</li>
              <li><strong>Durée :</strong> {{ form.duration }} jours</li>
            </ul>
          </div>
        </transition>

        <!-- Navigation -->
        <div class="flex justify-between pt-6">
          <button
            type="button"
            @click="prevStep"
            v-if="currentStep > 0"
            class="px-4 py-2 rounded-lg border text-gray-600 hover:bg-gray-100 transition"
          >
            Précédent
          </button>

          <button
            v-if="currentStep < steps.length - 1"
            type="button"
            @click="nextStep"
            class="ml-auto px-6 py-2 md:py-3 bg-[#7D260F] text-white font-semibold rounded-lg shadow hover:bg-[#661f0c] transition"
          >
            Suivant
          </button>

          <button
            v-if="currentStep === steps.length - 1"
            type="submit"
            class="ml-auto px-6 py-2 md:py-3 bg-green-600 text-white font-semibold rounded-lg shadow hover:bg-green-700 transition"
          >
            Créer l’annonce
          </button>
        </div>
      </form>
    </div>
  </section>
</template>

<script setup>
import { ref } from "vue"
import { useAuthStore } from '@/stores/auth'

const steps = ["Infos", "Image", "Budget", "Confirmation"]
const currentStep = ref(0)

const auth = useAuthStore()

const form = ref({
  ad_type: "generic", // toujours générique
  title: "",
  description: "",
  image: null,
  imagePreview: null,
  amount: null,
  duration: null,
})

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

const submitAd = async () => {
  const formData = new FormData()
  for (const key in form.value) {
    if (form.value[key] !== null) formData.append(key, form.value[key])
  }

  try {
    const res = await $fetch("http://127.0.0.1:8000/api/ad/", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${auth.accessToken}`,
      },
      credentials: "include",
      body: formData,
    })
    alert("✅ Annonce créée avec succès !")
    console.log("Annonce envoyée :", res)
  } catch (err) {
    console.error(err)
    alert("❌ Erreur lors de la création de l’annonce")
  }
}
</script>

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
