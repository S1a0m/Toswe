<!-- components/TwProductDescriptionEditor.vue -->
<template>
    <!-- Card container -->
    <div class="bg-white shadow-xl rounded-2xl p-6 grid grid-cols-1 lg:grid-cols-2 gap-6">

      <!-- LEFT: Form wizard -->
      <div>
        <!-- Stepper -->
        <div class="mb-6">
          <div class="flex items-center gap-3">
            <template v-for="n in maxStep" :key="n">
              <div class="flex items-center gap-3 w-full">
                <div
                  :class="[
                    'w-9 h-9 rounded-full flex items-center justify-center text-sm font-semibold',
                    step >= n ? 'bg-[#7D260F] text-white shadow' : 'bg-gray-200 text-gray-700'
                  ]"
                >
                  {{ n }}
                </div>
                <div v-if="n < maxStep" class="flex-1 h-1 rounded-full bg-gray-200">
                  <div
                    :style="{ width: (step > n ? 100 : step === n ? (progressInStep * 100) + '%' : '0%') }"
                    class="h-1 bg-[#7D260F] transition-all"
                  />
                </div>
              </div>
            </template>
          </div>
          <div class="mt-2 text-sm text-gray-600">Étape {{ step }} / {{ maxStep }}</div>
        </div>

        <transition name="slide-fade" mode="out-in">
          <div :key="step">
            <!-- STEP 1: Main info -->
            <section v-if="step === 1" class="space-y-4">
              <h2 class="text-lg font-semibold">Informations principales</h2>

              <label class="block text-sm font-medium">Nom du produit <span class="text-red-500">*</span></label>
              <input
                v-model="name"
                type="text"
                placeholder="Ex: Café de torréfaction locale"
                class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#7D260F]"
                :aria-invalid="!!errors.name"
              />
              <p v-if="errors.name" class="text-xs text-red-500">{{ errors.name }}</p>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label class="block text-sm font-medium">Prix (FCFA) <span class="text-red-500">*</span></label>
                  <input
                    v-model.number="price"
                    type="number"
                    min="0"
                    placeholder="1000"
                    class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#7D260F]"
                    :aria-invalid="!!errors.price"
                  />
                  <p v-if="errors.price" class="text-xs text-red-500">{{ errors.price }}</p>
                </div>
                <div>
                  <label class="block text-sm font-medium">Catégorie <span class="text-red-500">*</span></label>
                  <select
                    v-model="category"
                    class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#7D260F]"
                    :aria-invalid="!!errors.category"
                  >
                    <option value="" disabled>Choisir une catégorie</option>
                    <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
                  </select>
                  <p v-if="errors.category" class="text-xs text-red-500">{{ errors.category }}</p>
                </div>
              </div>

              <!--<div class="mt-2 text-sm text-gray-500">
                <label class="inline-flex items-center gap-2">
                  <input type="checkbox" v-model="isNegotiable" class="rounded" /> Prix négociable
                </label>
              </div>-->
            </section>

            <!-- STEP 2: Description -->
            <section v-else-if="step === 2" class="space-y-4">
              <h2 class="text-lg font-semibold">Description</h2>
              <div class="text-sm text-gray-600">Rédige une description claire — <span class="font-medium">{{ descriptionTextLength }}</span>/1000</div>
              <TwTipTapEditor v-model="description" placeholder="Décris ton produit ici…" />

              <p v-if="errors.description" class="text-xs text-red-500">{{ errors.description }}</p>
            </section>

            <!-- STEP 3: Images -->
            <section v-else-if="step === 3" class="space-y-4">
              <h2 class="text-lg font-semibold">Images</h2>
              <div
                class="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center cursor-pointer hover:bg-gray-50"
                @click="$refs.imageInput.click()"
                @dragover.prevent="onImageDragOver"
                @dragleave.prevent="onImageDragLeave"
                @drop.prevent="onImageDrop"
                :class="{'bg-gray-50': isImageDragOver}"
              >
                <input ref="imageInput" type="file" accept="image/*" multiple class="hidden" @change="handleImageUpload" />
                <div class="flex flex-col items-center justify-center gap-2">
                  <p class="text-sm text-gray-600">Glisse-dépose ou clique pour ajouter des images (max {{ maxImages }})</p>
                  <p class="text-xs text-gray-400">JPG, PNG — max {{ readableMaxImageSize }}</p>
                </div>
              </div>

              <div class="grid grid-cols-2 sm:grid-cols-3 gap-3 mt-4">
                <div v-for="(img, i) in imagePreviews" :key="i" class="relative rounded-lg overflow-hidden border">
                  <img :src="img" class="w-full h-32 object-cover" />
                  <button @click="removeImage(i)" class="absolute top-2 right-2 bg-black/60 text-white p-1 rounded-full">✕</button>
                </div>
                <div v-if="imagePreviews.length === 0" class="text-sm text-gray-500 col-span-full">Aucune image ajoutée</div>
              </div>
              <p v-if="errors.images" class="text-xs text-red-500 mt-2">{{ errors.images }}</p>
            </section>

            <!-- STEP 4: Vidéos (premium sellers) -->
            <section v-else-if="step === 4 && auth.isPremiumSeller" class="space-y-4">
              <h2 class="text-lg font-semibold">Vidéos (optionnel)</h2>
              <div
                class="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center cursor-pointer hover:bg-gray-50"
                @click="$refs.videoInput.click()"
                @dragover.prevent="onVideoDragOver"
                @dragleave.prevent="onVideoDragLeave"
                @drop.prevent="onVideoDrop"
                :class="{'bg-gray-50': isVideoDragOver}"
              >
                <input ref="videoInput" type="file" accept="video/*" multiple class="hidden" @change="handleVideoUpload" />
                <div class="flex flex-col items-center justify-center gap-2">
                  <p class="text-sm text-gray-600">Glisse-dépose ou clique pour ajouter des vidéos (max {{ maxVideos }})</p>
                  <p class="text-xs text-gray-400">MP4, WEBM — max {{ readableMaxVideoSize }}</p>
                </div>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mt-4">
                <div v-for="(vid, i) in videoPreviews" :key="i" class="relative rounded-lg overflow-hidden border">
                  <video :src="vid" controls class="w-full h-36 object-cover" />
                  <button @click="removeVideo(i)" class="absolute top-2 right-2 bg-black/60 text-white p-1 rounded-full">✕</button>
                </div>
                <div v-if="videoPreviews.length === 0" class="text-sm text-gray-500 col-span-full">Aucune vidéo ajoutée</div>
              </div>
              <p v-if="errors.videos" class="text-xs text-red-500 mt-2">{{ errors.videos }}</p>
            </section>
          </div>
        </transition>

        <!-- Navigation -->
        <div class="flex items-center justify-between gap-3 mt-6">
          <button v-if="step > 1" @click="prevStep" class="px-4 py-2 bg-gray-100 rounded-lg hover:bg-gray-200">Précédent</button>

          <div class="flex-1 flex justify-center">
            <button
              v-if="step < maxStep"
              @click="handleNext"
              class="px-6 py-2 bg-[#7D260F] text-white rounded-lg hover:bg-[#661f0c] disabled:opacity-60"
              :disabled="isProcessing"
            >
              Suivant
            </button>

            <button
              v-else
              @click="handleSubmit"
              class="px-6 py-2 bg-green-600 text-white rounded-lg flex items-center gap-2 hover:bg-green-700"
              :disabled="isSubmitting"
            >
              <svg v-if="isSubmitting" class="animate-spin h-5 w-5" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"/></svg>
              Publier
            </button>
            <!--<span v-else>Upload {{ isSubmittingProgress }}%</span>-->
          </div>

          <button v-if="step > 1" @click="resetToFirst" class="px-3 py-2 text-sm text-gray-500">Réinitialiser</button>
        </div>
      </div>

      <!-- RIGHT: Live preview -->
      <aside class="hidden lg:flex flex-col items-center gap-4">
        <div class="w-full border rounded-2xl overflow-hidden shadow-lg">
          <div class="w-full h-44 bg-gray-100">
            <img v-if="imagePreviews[0]" :src="imagePreviews[0]" alt="preview" class="w-full h-full object-cover" />
            <div v-else class="w-full h-full flex items-center justify-center text-gray-400">Aperçu image</div>
          </div>
          <div class="p-4 bg-white">
            <h3 class="text-lg font-semibold truncate">{{ name || 'Titre du produit' }}</h3>
            <div class="text-sm text-gray-500 mt-1 truncate">{{ categoryName }}</div>
            <div class="mt-3 flex items-baseline justify-between">
              <div class="text-xl font-bold text-[#7D260F]">{{ priceText }}</div>
              <button class="px-3 py-1 rounded-md bg-[#7D260F] text-white text-sm" @click="previewGoToDetails" :disabled="!previewHasProduct">Voir la fiche</button>
            </div>
            <p class="text-sm text-gray-600 mt-3 line-clamp-3" v-html="descriptionShort"></p>
          </div>
        </div>

        <div class="w-full text-sm text-gray-500">
          <div class="mb-2">Aperçu média</div>
          <div class="grid grid-cols-3 gap-2">
            <div v-for="(img,i) in imagePreviews" :key="i" class="h-16 w-full rounded overflow-hidden border">
              <img :src="img" class="w-full h-full object-cover"/>
            </div>
          </div>
        </div>
      </aside>
    </div>

    <!-- Toasts -->
    <div class="fixed right-4 bottom-6 flex flex-col gap-3 z-60">
      <div v-for="(t, i) in toasts" :key="t.id" class="bg-gray-900 text-white px-4 py-2 rounded-md shadow-md flex items-center gap-3">
        <div class="text-sm">{{ t.message }}</div>
        <button class="ml-2 text-gray-300" @click="removeToast(t.id)">✕</button>
      </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

type Category = { id: number; name: string }

const auth = useAuthStore()
const router = useRouter()

/* ----- Wizard state ----- */
const step = ref(1)
const maxStep = computed(() => (auth.isPremiumSeller ? 4 : 3))
const progressInStep = ref(0) // for stepper micro-progress (not required but kept)

/* ----- Form data ----- */
const name = ref('')
const price = ref<number | null>(null)
const category = ref<number | null>(null)
const categories = ref<Category[]>([])
const description = ref('')

/* ----- Media ----- */
const images = ref<File[]>([])
const imagePreviews = ref<string[]>([])
const videos = ref<File[]>([])
const videoPreviews = ref<string[]>([])

/* ----- UI state ----- */
const isImageDragOver = ref(false)
const isVideoDragOver = ref(false)
const isProcessing = ref(false)
const isSubmitting = ref(false)
const isSubmittingProgress = ref(0)

/* ----- Limits ----- */
const maxImages = 6
const maxVideos = 2
const maxImageSize = 3 * 1024 * 1024 // 3 MB
const maxVideoSize = 50 * 1024 * 1024 // 50 MB

/* ----- Errors ----- */
const errors = ref<Record<string, string>>({})

/* ----- Toasts ----- */
type Toast = { id: number; message: string }
const toasts = ref<Toast[]>([])
let toastId = 1
const pushToast = (msg: string, ttl = 4000) => {
  const id = toastId++
  toasts.value.push({ id, message: msg })
  setTimeout(() => removeToast(id), ttl)
}
const removeToast = (id: number) => {
  toasts.value = toasts.value.filter(t => t.id !== id)
}

/* ----- Fetch categories ----- */
onMounted(async () => {
  try {
    const res = await $fetch<{ results: Category[] }>('http://127.0.0.1:8000/api/category/')
    categories.value = res.results || []
  } catch (err) {
    console.error(err)
    pushToast('Impossible de charger les catégories')
  }
})

/* ----- Helpers ----- */
const readableBytes = (b: number) => {
  if (b >= 1024 * 1024) return Math.round(b / (1024 * 1024)) + ' Mo'
  if (b >= 1024) return Math.round(b / 1024) + ' Ko'
  return b + ' o'
}
const readableMaxImageSize = readableBytes(maxImageSize)
const readableMaxVideoSize = readableBytes(maxVideoSize)

/* ----- Description length ----- */
const descriptionTextLength = computed(() => {
  // strip HTML
  return description.value.replace(/<[^>]*>?/gm, '').trim().length
})

/* ----- Previews/preview helpers ----- */
const categoryName = computed(() => {
  const c = categories.value.find(cat => cat.id === category.value)
  return c ? c.name : '—'
})
const priceText = computed(() => (price.value ? new Intl.NumberFormat('fr-FR').format(price.value) + ' FCFA' : '--'))
const descriptionShort = computed(() => {
  const s = description.value.replace(/<[^>]*>?/gm, '')
  return s.length ? (s.length > 200 ? s.slice(0, 200) + '…' : s) : 'Aucune description'
})
const previewHasProduct = computed(() => !!name.value && !!price.value)

/* ----- Drag & drop / upload handling ----- */
const handleImageFiles = (files: File[]) => {
  for (const f of files) {
    if (images.value.length >= maxImages) {
      pushToast(`Max ${maxImages} images autorisées`)
      break
    }
    if (f.size > maxImageSize) {
      pushToast(`Image trop lourde (${readableBytes(f.size)}). Max ${readableMaxImageSize}`)
      continue
    }
    images.value.push(f)
    const reader = new FileReader()
    reader.onload = e => imagePreviews.value.push(e.target?.result as string)
    reader.readAsDataURL(f)
  }
}
const handleVideoFiles = (files: File[]) => {
  for (const f of files) {
    if (videos.value.length >= maxVideos) {
      pushToast(`Max ${maxVideos} vidéos autorisées`)
      break
    }
    if (f.size > maxVideoSize) {
      pushToast(`Vidéo trop lourde (${readableBytes(f.size)}). Max ${readableMaxVideoSize}`)
      continue
    }
    videos.value.push(f)
    videoPreviews.value.push(URL.createObjectURL(f))
  }
}

/* Inputs */
const handleImageUpload = (e: Event) => {
  const input = e.target as HTMLInputElement
  if (!input.files) return
  handleImageFiles(Array.from(input.files))
}
const handleVideoUpload = (e: Event) => {
  const input = e.target as HTMLInputElement
  if (!input.files) return
  handleVideoFiles(Array.from(input.files))
}

/* Drag events */
const onImageDragOver = () => (isImageDragOver.value = true)
const onImageDragLeave = () => (isImageDragOver.value = false)
const onImageDrop = (e: DragEvent) => {
  isImageDragOver.value = false
  if (!e.dataTransfer) return
  handleImageFiles(Array.from(e.dataTransfer.files).filter(f => f.type.startsWith('image/')))
}
const onVideoDragOver = () => (isVideoDragOver.value = true)
const onVideoDragLeave = () => (isVideoDragOver.value = false)
const onVideoDrop = (e: DragEvent) => {
  isVideoDragOver.value = false
  if (!e.dataTransfer) return
  handleVideoFiles(Array.from(e.dataTransfer.files).filter(f => f.type.startsWith('video/')))
}

/* Remove */
const removeImage = (i: number) => {
  images.value.splice(i, 1)
  imagePreviews.value.splice(i, 1)
}
const removeVideo = (i: number) => {
  videos.value.splice(i, 1)
  videoPreviews.value.splice(i, 1)
}

/* ----- Validation ----- */
const validateStep = (): boolean => {
  errors.value = {}
  if (step.value === 1) {
    if (!name.value.trim()) errors.value.name = 'Le nom est requis'
    if (!price.value || price.value <= 0) errors.value.price = 'Le prix doit être > 0'
    if (!category.value) errors.value.category = 'Choisir une catégorie'
  }
  if (step.value === 2) {
    if (descriptionTextLength.value < 10) errors.value.description = 'La description est trop courte'
    if (descriptionTextLength.value > 1000) errors.value.description = 'La description est trop longue'
  }
  if (step.value === 3) {
    if (images.value.length === 0) errors.value.images = 'Ajoutez au moins une image'
  }
  if (Object.keys(errors.value).length) {
    // highlight
    pushToast('Veuillez corriger les champs avant de continuer')
    return false
  }
  return true
}

/* ----- Navigation helpers ----- */
const handleNext = () => {
  if (!validateStep()) return
  if (step.value < maxStep.value) {
    step.value++
    progressInStep.value = 0
  }
}
const prevStep = () => {
  if (step.value > 1) step.value--
}
const resetToFirst = () => {
  step.value = 1
}

/* ----- Submit ----- */
const handleSubmit = async () => {
  if (!validateStep()) return
  isSubmitting.value = true
  isSubmittingProgress.value = 0

  const fd = new FormData()
  fd.append('name', name.value)
  fd.append('description', description.value)
  fd.append('price', String(price.value ?? '0'))
  if (category.value) fd.append('category', String(category.value))
  fd.append('is_online', String(true))
  fd.append('status', 'new')

  // images
  images.value.forEach((f) => fd.append('images', f))
  // videos
  videos.value.forEach((f) => fd.append('videos', f))

  // Créer la requête XHR pour suivre l'upload progress
  try {
    await new Promise<void>((resolve, reject) => {
      const xhr = new XMLHttpRequest()
      xhr.open('POST', 'http://127.0.0.1:8000/api/product/', true)

      // Authorization si token présent
      if (auth?.accessToken) {
        xhr.setRequestHeader('Authorization', `Bearer ${auth.accessToken}`)
      }

      xhr.upload.onprogress = (e) => {
        if (e.lengthComputable) {
          isSubmittingProgress.value = Math.round((e.loaded / e.total) * 100)
        }
      }

      xhr.onload = () => {
        isSubmitting.value = false
        if (xhr.status >= 200 && xhr.status < 300) {
          // parse result
          const res = JSON.parse(xhr.responseText || '{}')
          pushToast('Produit publié avec succès')
          // rediriger vers la page produit si id dispo
         /* if (res?.id) {
            setTimeout(() => router.push(`/product/${res.id}`), 700)
          } else {
            setTimeout(() => router.push('/my-products'), 700)
          }*/
          resolve()
        } else {
          // afficher erreurs renvoyées par DRF si format JSON
          let msg = `Erreur serveur (${xhr.status})`
          try {
            const data = JSON.parse(xhr.responseText || '{}')
            // DRF errors usually obj {field: [..], non_field_errors: [...]}
            if (typeof data === 'object') {
              const parts: string[] = []
              for (const k in data) {
                const v = data[k]
                if (Array.isArray(v)) parts.push(`${k}: ${v.join(', ')}`)
                else parts.push(`${k}: ${v}`)
              }
              msg = parts.join(' | ')
            } else {
              msg = String(data)
            }
          } catch (err) {
            // fallback
            msg = xhr.responseText || msg
          }
          pushToast(msg)
          reject(new Error(msg))
        }
      }

      xhr.onerror = () => {
        isSubmitting.value = false
        pushToast('Erreur réseau durant l\'upload')
        reject(new Error('Network error'))
      }

      xhr.send(fd)
    })
  } catch (err) {
    // déjà géré par la promesse
    console.error('Upload error', err)
    isSubmitting.value = false
  } finally {
    isSubmitting.value = false
  }
}

/* ----- Extras: preview go to details ----- */
const previewGoToDetails = () => {
  if (!previewHasProduct.value) {
    pushToast('Complétez le titre et le prix pour prévisualiser')
    return
  }
  // build a temp product preview route or navigate to market with filters
  router.push({ path: '/market', query: { q: name.value } })
}

/* ----- small reactive states ----- */
const isNegotiable = ref(false)
const isProcessingTimeout = ref<number | null>(null)

/* ----- Watchers ----- */
watch(description, () => {
  // clamp description length visually (we only warn)
  if (descriptionTextLength.value > 1000) pushToast('Description dépasse 1000 caractères')
})

</script>

<style scoped>
/* small animations */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.28s ease;
}
.slide-fade-enter-from {
  opacity: 0;
  transform: translateX(12px);
}
.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(-12px);
}

/* clamp helpers (requires line-clamp plugin or simple CSS fallback) */
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
