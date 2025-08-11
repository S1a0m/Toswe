<template>
    <div class="mt-18">
    </div>
    <div class="pt-0.5">
    </div>
  <div class="max-w-3xl mx-auto p-6 bg-white shadow rounded">
    <h1 class="text-2xl font-bold mb-6">Créer une publicité</h1>

    <form @submit.prevent="submitAd" class="space-y-5">
      <!-- Titre -->
      <div>
        <label class="block mb-1 font-medium">Titre</label>
        <input
          v-model="form.title"
          type="text"
          class="w-full border rounded p-2"
          placeholder="Titre accrocheur..."
          required
        />
      </div>

      <!-- Description -->
      <div>
        <label class="block mb-1 font-medium">Description</label>
        <textarea
          v-model="form.description"
          rows="4"
          class="w-full border rounded p-2"
          placeholder="Décrivez votre publicité..."
          required
        ></textarea>
      </div>

      <!-- Image -->
      <div>
        <label class="block mb-1 font-medium">Image (URL)</label>
        <input
          v-model="form.image"
          type="url"
          class="w-full border rounded p-2"
          placeholder="https://exemple.com/image.jpg"
        />
      </div>

      <!-- Budget -->
      <div>
        <label class="block mb-1 font-medium">Budget (en FCFA)</label>
        <input
          v-model.number="form.budget"
          type="number"
          min="100"
          class="w-full border rounded p-2"
          placeholder="Ex: 5000"
          required
        />
      </div>

      <!-- Durée -->
      <div>
        <label class="block mb-1 font-medium">Durée (jours)</label>
        <input
          v-model.number="form.duration"
          type="number"
          min="1"
          class="w-full border rounded p-2"
          placeholder="Ex: 7"
          required
        />
      </div>

      <!-- Lien -->
      <div>
        <label class="block mb-1 font-medium">Lien de redirection (optionnel)</label>
        <input
          v-model="form.link"
          type="url"
          class="w-full border rounded p-2"
          placeholder="https://..."
        />
      </div>

      <!-- Bouton -->
      <div class="pt-4">
        <button
          type="submit"
          class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
        >
          Créer la publicité
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const form = ref({
  title: '',
  description: '',
  image: '',
  budget: '',
  duration: '',
  link: ''
})

const submitAd = () => {
  console.log('Publicité envoyée :', form.value)
  alert('Votre publicité a été créée avec succès !')
  // Ici, on pourra envoyer les données à une API avec $fetch ou axios
}
</script>

<style scoped>
body {
  background: #f9fafb;
}
</style>
