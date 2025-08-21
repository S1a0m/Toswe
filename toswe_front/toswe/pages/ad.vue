<template>
  <section class="px-4 md:px-8 py-12 max-w-4xl mx-auto">
    <!-- Titre -->
    <h2 class="text-3xl font-bold text-[#7D260F] mb-8 font-[Kenia] text-center">
      Créer une publicité
    </h2>

    <!-- Formulaire -->
    <div class="bg-white shadow-xl rounded-2xl p-8 border border-gray-100">
      <form @submit.prevent="submitAd" class="space-y-6">
        
        <!-- Titre -->
        <div>
          <label class="block mb-2 text-sm font-semibold text-gray-700">Titre</label>
          <input
            v-model="form.title"
            type="text"
            class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-[#7D260F] focus:outline-none"
            placeholder="Titre accrocheur..."
            required
          />
        </div>

        <!-- Description -->
        <div>
          <label class="block mb-2 text-sm font-semibold text-gray-700">Description</label>
          <textarea
            v-model="form.description"
            rows="4"
            class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-[#7D260F] focus:outline-none"
            placeholder="Décrivez votre publicité..."
            required
          ></textarea>
        </div>

        <!-- Image -->
        <div>
          <label class="block mb-2 text-sm font-semibold text-gray-700">Image (URL)</label>
          <input
            v-model="form.image"
            type="url"
            class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-[#7D260F] focus:outline-none"
            placeholder="https://exemple.com/image.jpg"
          />
        </div>

        <!-- Budget & Durée (flex row sur desktop) -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div>
            <label class="block mb-2 text-sm font-semibold text-gray-700">Budget (FCFA)</label>
            <input
              v-model.number="form.budget"
              type="number"
              min="100"
              class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-[#7D260F] focus:outline-none"
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
              class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-[#7D260F] focus:outline-none"
              placeholder="Ex: 7"
              required
            />
          </div>
        </div>

        <!-- Lien -->
        <div>
          <label class="block mb-2 text-sm font-semibold text-gray-700">Lien de redirection</label>
          <input
            v-model="form.link"
            type="url"
            class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-[#7D260F] focus:outline-none"
            placeholder="https://..."
          />
        </div>

        <!-- Produits associés -->
        <div>
          <label class="block mb-2 text-sm font-semibold text-gray-700">Produits associés</label>
          <p class="text-sm text-gray-500 mb-2">Sélectionnez les produits à promouvoir avec cette publicité.</p>
          <TwProductSelector v-model="form.products" />
        </div>

        <!-- Bouton -->
        <div class="pt-6 text-center">
          <button
            type="submit"
            class="bg-[#7D260F] hover:bg-[#661f0c] text-white px-6 py-3 rounded-lg font-semibold shadow-md hover:shadow-lg transition-all duration-300"
          >
            🚀 Créer la publicité
          </button>
        </div>
      </form>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const form = ref({
  title: '',
  description: '',
  image: '',
  budget: '',
  duration: '',
  link: '',
  products: []
})

const submitAd = () => {
  console.log('Publicité envoyée :', form.value)
  alert('✅ Votre publicité a été créée avec succès !')
}
</script>
