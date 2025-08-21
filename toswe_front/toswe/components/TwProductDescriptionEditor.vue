<script setup lang="ts">
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css'
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

// const isPremiumSeller = ref(true) 
const content = ref('')
const images = ref<File[]>([])
const imagePreviews = ref<string[]>([])
const videoLinks = ref<string[]>([''])

const handleImageUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files) {
    Array.from(target.files).forEach(file => {
      images.value.push(file)
      const reader = new FileReader()
      reader.onload = e => {
        imagePreviews.value.push(e.target?.result as string)
      }
      reader.readAsDataURL(file)
    })
  }
}

const removeImage = (index: number) => {
  images.value.splice(index, 1)
  imagePreviews.value.splice(index, 1)
}

const addVideoField = () => {
  videoLinks.value.push('')
}

const removeVideoField = (index: number) => {
  videoLinks.value.splice(index, 1)
}
</script>

<template>
  <div class="space-y-6">
    <!-- Description -->
    <div class="bg-white rounded-2xl shadow p-5">
      <h2 class="text-lg font-semibold text-gray-800 mb-3">
        📝 Description du produit
      </h2>
      <QuillEditor
        v-model:content="content"
        content-type="html"
        theme="snow"
        class="bg-white rounded-lg min-h-[200px]"
      />
    </div>

    <!-- Images -->
    <div class="bg-white rounded-2xl shadow p-5">
      <h2 class="text-lg font-semibold text-gray-800 mb-3">
        🖼️ Images du produit
      </h2>

      <label
        class="block cursor-pointer w-full border-2 border-dashed border-gray-300 rounded-lg p-6 text-center text-gray-500 hover:border-[#7D260F] hover:text-[#7D260F] transition"
      >
        <input
          type="file"
          accept="image/*"
          multiple
          class="hidden"
          @change="handleImageUpload"
        />
        <p class="text-sm">Cliquez ou déposez vos images ici</p>
      </label>

      <!-- Preview des images -->
      <div class="mt-4 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
        <div
          v-for="(img, index) in imagePreviews"
          :key="index"
          class="relative group rounded-lg overflow-hidden shadow"
        >
          <img :src="img" alt="preview" class="object-cover w-full h-32" />
          <button
            type="button"
            @click="removeImage(index)"
            class="absolute top-2 right-2 bg-black/50 text-white rounded-full p-1 opacity-0 group-hover:opacity-100 transition"
          >
            ✕
          </button>
        </div>
      </div>
    </div>

    <!-- Vidéos (premium uniquement) -->
    <div
      v-if="auth.isPremiumSeller"
      class="bg-white rounded-2xl shadow p-5"
    >
      <h2 class="text-lg font-semibold text-gray-800 mb-3">
        🎥 Liens de vidéos
      </h2>
      <p class="text-sm text-gray-500 mb-3">
        Ajoutez des liens YouTube, Vimeo, etc. pour mettre en avant votre produit.
      </p>

      <div class="space-y-3">
        <div
          v-for="(link, index) in videoLinks"
          :key="index"
          class="flex items-center gap-3"
        >
          <input
            v-model="videoLinks[index]"
            type="url"
            placeholder="https://youtube.com/..."
            class="flex-1 rounded-lg border-gray-300 focus:ring-[#7D260F] focus:border-[#7D260F]"
          />
          <button
            v-if="videoLinks.length > 1"
            type="button"
            @click="removeVideoField(index)"
            class="text-red-500 hover:text-red-700"
          >
            ✕
          </button>
        </div>
      </div>

      <button
        type="button"
        @click="addVideoField"
        class="mt-4 px-4 py-2 rounded-lg border border-[#7D260F] text-[#7D260F] text-sm font-medium hover:bg-[#7D260F]/10 transition"
      >
        + Ajouter une vidéo
      </button>
    </div>
    <div class="flex justify-end space-x-3 mt-6">
  <!-- Bouton Annuler -->
  <button 
    class="px-4 py-2 rounded-xl border border-gray-400 text-gray-700 hover:bg-gray-100 transition"
    
  >
    Annuler
  </button>

  <!-- Bouton Mettre à l'achat -->
  <button 
    class="px-4 py-2 rounded-xl bg-green-600 text-white font-semibold hover:bg-green-700 transition"
   
  >
    Mettre à l'achat
  </button>

  <!-- Bouton Enregistrer comme brouillon -->
  <button 
    class="px-4 py-2 rounded-xl bg-blue-600 text-white font-semibold hover:bg-blue-700 transition"
    
  >
    Enregistrer comme brouillon
  </button>
</div>

  </div>
</template>