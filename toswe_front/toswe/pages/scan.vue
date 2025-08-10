<template>
    <div class="mt-18">
    </div>
    <div class="pt-0.5">
    </div>
  <section class="min-h-screen flex flex-col bg-[#7D260F] text-white">
    <!-- Titre -->
    <header class="p-6 text-center">
      <h1 class="text-2xl font-bold">Scanner un produit</h1>
      <p class="opacity-80 text-sm">Importez une image ou scannez en direct avec votre caméra.</p>
    </header>

    <!-- Zone de prévisualisation -->
    <div class="flex-1 flex flex-col items-center justify-center gap-4 px-4">
      <!-- Vidéo live -->
      <video v-if="cameraActive" ref="videoEl" autoplay playsinline class="rounded-lg shadow-lg w-full max-w-md border border-white/30"></video>

      <!-- Aperçu image -->
      <img v-if="previewImage && !cameraActive" :src="previewImage" alt="Aperçu" class="rounded-lg shadow-lg w-full max-w-md" />

      <!-- Upload -->
      <input
        type="file"
        accept="image/*"
        class="hidden"
        ref="fileInput"
        @change="handleImageUpload"
      />
    </div>

    <!-- Boutons fixes -->
    <footer class="sticky bottom-0 w-full bg-[#5c1b0b] p-4 flex gap-3">
      <button
        @click="toggleCamera"
        class="flex-1 py-3 rounded-lg font-semibold bg-green-600 hover:bg-green-700 transition"
      >
        {{ cameraActive ? 'Arrêter' : 'Caméra' }}
      </button>
      <button
        @click="() => fileInput.click()"
        class="flex-1 py-3 rounded-lg font-semibold bg-blue-600 hover:bg-blue-700 transition"
      >
        Importer
      </button>
      <button
        v-if="cameraActive"
        @click="capturePhoto"
        class="flex-1 py-3 rounded-lg font-semibold bg-yellow-500 hover:bg-yellow-600 transition"
      >
        Prendre
      </button>
    </footer>
  </section>
</template>

<script setup>
import { ref, onBeforeUnmount } from 'vue'

const previewImage = ref(null)
const fileInput = ref(null)
const videoEl = ref(null)
const cameraActive = ref(false)
let stream = null
let scanInterval = null

// Import d'image
function handleImageUpload(event) {
  const file = event.target.files[0]
  if (file) {
    previewImage.value = URL.createObjectURL(file)
    stopCamera()
  }
}

// Démarre ou arrête la caméra
async function toggleCamera() {
  if (cameraActive.value) {
    stopCamera()
  } else {
    await startCamera()
  }
}

async function startCamera() {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
    videoEl.value.srcObject = stream
    cameraActive.value = true

    // Scan en continu (exemple toutes les 2 secondes)
    scanInterval = setInterval(() => {
      captureAndScan()
    }, 2000)
  } catch (err) {
    console.error('Impossible d’accéder à la caméra', err)
  }
}

function stopCamera() {
  if (stream) {
    stream.getTracks().forEach(track => track.stop())
  }
  clearInterval(scanInterval)
  cameraActive.value = false
}

// Capture d'image
function capturePhoto() {
  captureAndScan()
  stopCamera()
}

function captureAndScan() {
  const canvas = document.createElement('canvas')
  canvas.width = videoEl.value.videoWidth
  canvas.height = videoEl.value.videoHeight
  const ctx = canvas.getContext('2d')
  ctx.drawImage(videoEl.value, 0, 0, canvas.width, canvas.height)
  previewImage.value = canvas.toDataURL('image/png')

  // Ici, tu peux envoyer l'image à ton backend
  // uploadScan(previewImage.value)
}

onBeforeUnmount(() => {
  stopCamera()
})
</script>
