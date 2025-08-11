<template>
    <div class="mt-18">
    </div>
    <div class="pt-0.5">
    </div>
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
        <div
          v-for="(item, index) in results"
          :key="index"
          class="bg-white rounded-lg shadow hover:shadow-lg transition overflow-hidden"
        >
          <img
            :src="item.image"
            :alt="item.name"
            class="w-full h-40 object-cover"
          />
          <div class="p-4">
            <h3 class="font-bold text-lg mb-1">{{ item.name }}</h3>
            <p class="text-sm text-gray-500 mb-2">{{ item.brand }}</p>
            <p class="text-red-600 font-bold">{{ item.price }} €</p>
          </div>
        </div>
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

const allProducts = [
  { name: 'Chaussures Running', brand: 'Nike', price: 89.99, image: '/products/shoes.jpg' },
  { name: 'Smartphone Galaxy', brand: 'Samsung', price: 599, image: '/products/phone.jpg' },
  { name: 'Casque Audio', brand: 'Sony', price: 199, image: '/products/headphones.jpg' },
  { name: 'Montre Sport', brand: 'Garmin', price: 149, image: '/products/watch.jpg' },
  { name: 'Sac à Dos', brand: 'North Face', price: 59, image: '/products/backpack.jpg' },
  { name: 'Veste Hiver', brand: 'Adidas', price: 129, image: '/products/jacket.jpg' }
]

const handleSearch = () => {
  loading.value = true
  setTimeout(() => {
    if (query.value.trim().length > 0) {
      results.value = allProducts.filter(
        p =>
          p.name.toLowerCase().includes(query.value.toLowerCase()) ||
          p.brand.toLowerCase().includes(query.value.toLowerCase())
      )
    } else {
      results.value = []
    }
    loading.value = false
  }, 800)
}

const handleImageUpload = (e) => {
  const file = e.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = () => {
      scanImage.value = reader.result
      simulateImageSearch()
    }
    reader.readAsDataURL(file)
  }
}

const openCamera = async () => {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: true })
    video.value.srcObject = stream
    cameraOpen.value = true
  } catch (err) {
    alert('Impossible d’accéder à la caméra.')
  }
}

const capturePhoto = () => {
  const canvas = document.createElement('canvas')
  canvas.width = video.value.videoWidth
  canvas.height = video.value.videoHeight
  const ctx = canvas.getContext('2d')
  ctx.drawImage(video.value, 0, 0)
  scanImage.value = canvas.toDataURL('image/png')
  closeCamera()
  simulateImageSearch()
}

const closeCamera = () => {
  if (stream) {
    stream.getTracks().forEach(track => track.stop())
  }
  cameraOpen.value = false
}

const simulateImageSearch = () => {
  loading.value = true
  setTimeout(() => {
    results.value = allProducts.slice(0, 3) // Simule quelques résultats
    loading.value = false
  }, 1000)
}
</script>
