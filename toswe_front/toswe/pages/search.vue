<template>
  <section class="min-h-screen py-6 px-4">
    <!-- Barre de recherche + boutons -->
    <div class="max-w-3xl mx-auto flex flex-col sm:flex-row items-center gap-3 mb-8">
      <!-- Recherche texte -->
      <div class="flex items-center bg-white rounded-full shadow-md overflow-hidden flex-1">
        <input
          v-model="query"
          @input="handleSearch"
          type="text"
          placeholder="Rechercher un produit..."
          class="flex-1 px-4 py-3 outline-none"
        />
        <button
          class="px-4 py-3 text-gray-500 hover:text-gray-700"
          @click="handleSearch"
        >
          <Icon name="uil:search" class="w-5 h-5" />
        </button>
      </div>

      <!-- Bouton importer image -->
      <label
        class="bg-white rounded-full shadow-md px-4 py-2 cursor-pointer flex items-center gap-2 hover:bg-gray-100"
      >
        <Icon name="uil:image-upload" class="w-5 h-5" />
        Importer
        <input
          type="file"
          accept="image/*"
          class="hidden"
          @change="handleImageUpload"
        />
      </label>

      <!-- Bouton prendre photo -->
      <button
        class="bg-white rounded-full shadow-md px-4 py-2 flex items-center gap-2 hover:bg-gray-100"
        @click="openCamera"
      >
        <Icon name="uil:camera" class="w-5 h-5" />
        Photo
      </button>
    </div>

    <!-- Preview image scannée -->
    <div v-if="scanImage" class="max-w-sm mx-auto mb-6">
      <img :src="scanImage" alt="Image scannée" class="rounded-lg shadow-md" />
      <p class="text-center text-gray-500 mt-2 text-sm">Image à analyser...</p>
    </div>

    <!-- Contenu -->
    <div class="max-w-6xl mx-auto">
      <!-- Chargement -->
      <div v-if="loading" class="text-center text-gray-500">
        ⏳ Recherche en cours...
      </div>

      <!-- Aucun résultat -->
      <div v-else-if="results.length === 0 && query.length > 0" class="text-center text-gray-500">
        Aucun résultat trouvé pour "<b>{{ query }}</b>"
      </div>

      <!-- Résultats -->
      <div
        v-else
        class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6"
      >
          <TwProductMixSeller 
          v-for="(item, index) in results"
          :key="index" :item="item" />
      </div>
    </div>

    <!-- Modal caméra -->
    <div
      v-if="cameraOpen"
      class="fixed inset-0 bg-black bg-opacity-70 flex flex-col items-center justify-center z-50"
    >
      <video ref="video" autoplay playsinline class="rounded-lg shadow-lg max-w-sm w-full"></video>
      <div class="mt-4 flex gap-4">
        <button
          class="bg-white px-4 py-2 rounded-lg shadow hover:bg-gray-100"
          @click="capturePhoto"
        >
          📸 Capturer
        </button>
        <button
          class="bg-red-500 text-white px-4 py-2 rounded-lg shadow hover:bg-red-600"
          @click="closeCamera"
        >
          ❌ Fermer
        </button>
      </div>
    </div>
  </section>
  <TwMenuSide />
  <TwCart />
</template>

<script setup>
import { ref } from 'vue'

const query = ref('')
const results = ref([])
const loading = ref(false)
const scanImage = ref(null)

const cameraOpen = ref(false)
const video = ref(null)
let stream = null

const { $apiFetch } = useNuxtApp()

// Recherche texte (inchangé)
const handleSearch = async () => {
  if (query.value.trim().length === 0) {
    results.value = []
    return
  }

  loading.value = true
  try {
    const { data, error } = await useFetch('http://127.0.0.1:8000/api/product/search_products/', {
      query: { q: query.value }
    })

    if (error.value) {
      console.error("Erreur API:", error.value)
      results.value = []
    } else {
      results.value = data.value || []
    }
  } catch (err) {
    console.error(err)
    results.value = []
  } finally {
    loading.value = false
  }
}

// Upload depuis fichier
const handleImageUpload = async (e) => {
  const file = e.target.files[0]
  if (!file) return

  scanImage.value = URL.createObjectURL(file)
  await identifyProduct(file)
}

// Ouvrir la caméra
const openCamera = async () => {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: true })
    video.value.srcObject = stream
    cameraOpen.value = true
  } catch (err) {
    alert('Impossible d’accéder à la caméra.')
  }
}

// Capturer une photo
const capturePhoto = async () => {
  const canvas = document.createElement('canvas')
  canvas.width = video.value.videoWidth
  canvas.height = video.value.videoHeight
  const ctx = canvas.getContext('2d')
  ctx.drawImage(video.value, 0, 0)

  canvas.toBlob(async (blob) => {
    if (blob) {
      scanImage.value = URL.createObjectURL(blob)
      await identifyProduct(blob)
    }
  }, 'image/jpeg')

  closeCamera()
}

// Fermer caméra
const closeCamera = () => {
  if (stream) {
    stream.getTracks().forEach(track => track.stop())
  }
  cameraOpen.value = false
}

// 🔗 Appel API vers Django (endpoint identify)
const identifyProduct = async (imageFile) => {
  loading.value = true
  results.value = []

  try {
    const formData = new FormData()
    formData.append("image", imageFile)

    const response = await $apiFetch("http://127.0.0.1:8000/api/product/identify/", {
      method: "POST",
      body: formData
    })

    if (!response.ok) throw new Error("Erreur API")

    const data = await response.json()
    // Django retourne {"results": [...]}
    results.value = data.results || []
  } catch (err) {
    console.error("Erreur d’identification:", err)
    results.value = []
  } finally {
    loading.value = false
  }
}
</script>
