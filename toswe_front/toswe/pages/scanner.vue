<template>
  <section class="min-h-screen flex flex-col text-black">
    <TwMenuSide />

    <!-- Titre -->
    <header class="p-6 text-center">
      <h2 class="text-2xl font-bold text-[#7D260F] font-[Kenia] tracking-tight">Scanner un produit</h2>
      <p class="text-gray-600 mt-1">Scannez directement ou importez le QR code</p>
    </header>

    <!-- Zone de prévisualisation -->
    <div class="flex-1 flex flex-col items-center justify-center gap-6 px-4">
      <!-- Vidéo live -->
      <video
        v-if="cameraActive"
        ref="videoEl"
        autoplay
        playsinline
        class="rounded-xl shadow-lg w-full max-w-md border border-gray-200"
      ></video>

      <!-- Aperçu image -->
      <img
        v-if="previewImage && !cameraActive"
        :src="previewImage"
        alt="Aperçu"
        class="rounded-xl shadow-lg w-full max-w-md border border-gray-200"
      />

      <!-- Résultat produit -->
      <div v-if="product" class="mt-6 p-4 bg-white rounded-xl shadow-md border w-full max-w-md">
          <TwProductMixSeller :item="product" />
      </div>

      <!-- Upload invisible -->
      <input
        type="file"
        accept="image/*"
        ref="fileInput"
        class="hidden"
        @change="handleImageUpload"
      />
    </div>

    <!-- Boutons d’action -->
    <footer class="sticky bottom-0 w-full border-t border-gray-200 p-4 flex gap-3 bg-white">
      <button
        @click="toggleCamera"
        class="flex-1 flex items-center justify-center gap-2 py-3 rounded-lg font-semibold bg-green-600 text-white hover:bg-green-700 transition"
      >
        <Icon name="uil:camera" class="w-5 h-5" />
        {{ cameraActive ? 'Arrêter' : 'Caméra' }}
      </button>

      <button
        @click="fileInput.click()"
        class="flex-1 flex items-center justify-center gap-2 py-3 rounded-lg font-semibold bg-blue-600 text-white hover:bg-blue-700 transition"
      >
        <Icon name="uil:image-upload" class="w-5 h-5" />
        Importer
      </button>

      <button
        v-if="cameraActive"
        @click="capturePhoto"
        class="flex-1 flex items-center justify-center gap-2 py-3 rounded-lg font-semibold bg-yellow-500 text-black hover:bg-yellow-600 transition"
      >
        <Icon name="uil:camera-plus" class="w-5 h-5" />
        Prendre
      </button>
    </footer>
  </section>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
//definePageMeta({ layout: false })

import { ref, onBeforeUnmount } from 'vue'
import jsQR from 'jsqr' // 👉 installer: npm install jsqr

const previewImage = ref(null)
const fileInput = ref(null)
const videoEl = ref(null)
const cameraActive = ref(false)
const product = ref(null)

let stream = null
let scanInterval = null

function handleImageUpload(event) {
  const file = event.target.files[0]
  if (file) {
    previewImage.value = URL.createObjectURL(file)
    stopCamera()
    scanFromImage(previewImage.value)
  }
}

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

    scanInterval = setInterval(() => {
      captureAndScan()
    }, 1500)
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

  const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height)
  const code = jsQR(imageData.data, canvas.width, canvas.height)
  if (code) {
    fetchProduct(code.data)
  }
}

function scanFromImage(src) {
  const img = new Image()
  img.src = src
  img.onload = () => {
    const canvas = document.createElement('canvas')
    canvas.width = img.width
    canvas.height = img.height
    const ctx = canvas.getContext('2d')
    ctx.drawImage(img, 0, 0)
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height)
    const code = jsQR(imageData.data, canvas.width, canvas.height)
    if (code) {
      fetchProduct(code.data)
    } else {
      console.warn("Aucun QR code détecté")
    }
  }
}

const auth = useAuthStore()

async function fetchProduct(data) {
  try {
    // 🔹 extraction du signed_id
    let signedId
    try {
      const url = new URL(data)
      signedId = url.pathname.split("/").pop()
    } catch {
      signedId = data
    }

    // 🔹 appel API avec seulement le signed_id propre
    const res = await $fetch(`http://127.0.0.1:8000/api/product/scan_product/?signed_id=${signedId}`,
      { method: 'GET',
        headers: {
          Authorization: `Bearer ${auth.accessToken}`
       },
       credentials: 'include'
      })
    product.value = res
  } catch (e) {
    console.error("Erreur produit :", e)
  }
}


onBeforeUnmount(() => {
  stopCamera()
})
</script>
