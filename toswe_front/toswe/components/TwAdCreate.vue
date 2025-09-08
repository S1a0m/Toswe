<template>
  <section class="px-[16px] md:px-8 py-12 max-w-4xl mx-auto">
    <!-- Titre -->
    <h2 class="text-3xl font-bold text-[#7D260F] mb-8 font-[Kenia] text-center">
      Créer une publicité
    </h2>

    <!-- Wizard container -->
    <div class="bg-white shadow-xl rounded-2xl p-8 border border-gray-100">
      <!-- Étapes -->
      <div class="flex justify-between items-center mb-8">
        <div
          v-for="(step, index) in steps"
          :key="index"
          class="flex-1 flex items-center"
        >
          <div
            class="flex items-center justify-center w-8 h-8 rounded-full font-bold text-sm"
            :class="[
              currentStep === index ? 'bg-[#7D260F] text-white' :
              currentStep > index ? 'bg-green-500 text-white' :
              'bg-gray-200 text-gray-600'
            ]"
          >
            {{ index + 1 }}
          </div>
          <span
            class="ml-2 text-sm font-medium"
            :class="currentStep === index ? 'text-[#7D260F]' : 'text-gray-500'"
          >
            {{ step }}
          </span>
        </div>
      </div>

      <!-- Formulaire multi-étapes -->
      <form @submit.prevent="submitAd" class="space-y-6">
        <!-- Étape 1: Infos -->
        <div v-if="currentStep === 0" class="space-y-4">
          <div>
            <label class="block mb-2 text-sm font-semibold text-gray-700">Titre</label>
            <input
              v-model="form.title"
              type="text"
              class="input"
              placeholder="Titre accrocheur..."
              required
            />
          </div>
          <div>
            <label class="block mb-2 text-sm font-semibold text-gray-700">Description</label>
            <textarea
              v-model="form.description"
              rows="4"
              class="input"
              placeholder="Décrivez votre publicité..."
              required
            ></textarea>
          </div>
        </div>

        <!-- Étape 2: Médias -->
        <div v-if="currentStep === 1" class="space-y-4">
          <div>
            <label class="block mb-2 text-sm font-semibold text-gray-700">Image</label>
            <input type="file" @change="onFileChange($event, 'image')" class="input" />
            <img v-if="form.imagePreview" :src="form.imagePreview" class="mt-3 w-32 rounded-[8px] shadow" />
          </div>
          <div>
            <label class="block mb-2 text-sm font-semibold text-gray-700">Vidéo</label>
            <input type="file" @change="onFileChange($event, 'video')" class="input" />
            <video v-if="form.videoPreview" controls class="mt-3 w-48 rounded-[8px] shadow">
              <source :src="form.videoPreview" type="video/mp4" />
            </video>
          </div>
        </div>

        <!-- Étape 3: Budget -->
        <div v-if="currentStep === 2" class="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div>
            <label class="block mb-2 text-sm font-semibold text-gray-700">Budget (FCFA)</label>
            <input
              v-model.number="form.budget"
              type="number"
              min="100"
              class="input"
              placeholder="Ex: 5000"
              required
            />
          </div>
          <div>
            <label class="block mb-2 text-sm font-semibold text-gray-700">Durée (jours)</label>
            <input
              v-model.number="form.duration"
              type="number"
              min="1"
              class="input"
              placeholder="Ex: 7"
              required
            />
          </div>
        </div>

        <!-- Étape 4: Produits -->
        <div v-if="currentStep === 3">
          <label class="block mb-2 text-sm font-semibold text-gray-700">Produits associés</label>
          <p class="text-sm text-gray-500 mb-2">Sélectionnez les produits à promouvoir avec cette publicité.</p>
          <TwProductSelector v-model="form.products" />
        </div>

        <!-- Étape 5: Confirmation -->
        <div v-if="currentStep === 4" class="space-y-4 text-gray-700">
          <h3 class="text-lg font-semibold">Résumé de votre publicité</h3>
          <ul class="space-y-2 text-sm">
            <li><strong>Titre :</strong> {{ form.title }}</li>
            <li><strong>Description :</strong> {{ form.description }}</li>
            <li><strong>Budget :</strong> {{ form.budget }} FCFA</li>
            <li><strong>Durée :</strong> {{ form.duration }} jours</li>
            <li><strong>Produits :</strong> {{ form.products.join(', ') }}</li>
          </ul>
        </div>

        <!-- Navigation -->
        <div class="flex justify-between pt-6">
          <button
            type="button"
            @click="prevStep"
            v-if="currentStep > 0"
            class="px-[16px] py-[8px] rounded-[8px] border text-gray-600 hover:bg-gray-100"
          >
            Précédent
          </button>

          <button
            v-if="currentStep < steps.length - 1"
            type="button"
            @click="nextStep"
            class="ml-auto px-6 py-3 bg-[#7D260F] text-white font-semibold rounded-[8px] shadow hover:bg-[#661f0c] transition"
          >
            Suivant
          </button>

          <button
            v-if="currentStep === steps.length - 1"
            type="submit"
            class="ml-auto px-6 py-3 bg-green-600 text-white font-semibold rounded-[8px] shadow hover:bg-green-700 transition"
          >
            Créer la publicité
          </button>
        </div>

        <!-- Actions secondaires -->
        <div class="text-center mt-4 space-x-4">
          <button type="button" class="text-sm text-gray-500 hover:underline">Enregistrer comme brouillon</button>
          <button type="button" class="text-sm text-gray-500 hover:underline">Annuler</button>
        </div>
      </form>
    </div>
  </section>
</template>

<script setup>
import { ref } from "vue"

const steps = ["Infos", "Médias", "Budget", "Produits", "Confirmation"]
const currentStep = ref(0)

const form = ref({
  title: "",
  description: "",
  image: null,
  imagePreview: null,
  video: null,
  videoPreview: null,
  budget: "",
  duration: "",
  products: [],
})

const nextStep = () => {
  if (currentStep.value < steps.length - 1) currentStep.value++
}
const prevStep = () => {
  if (currentStep.value > 0) currentStep.value--
}

const onFileChange = (e, type) => {
  const file = e.target.files[0]
  if (file) {
    const url = URL.createObjectURL(file)
    if (type === "image") {
      form.value.image = file
      form.value.imagePreview = url
    } else if (type === "video") {
      form.value.video = file
      form.value.videoPreview = url
    }
  }
}

const submitAd = () => {
  console.log("Publicité envoyée :", form.value)
  alert("✅ Votre publicité a été créée avec succès !")
}
</script>

<style scoped>
</style>
